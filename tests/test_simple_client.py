import json

import httpx
import pytest

from calabrio_one import CalabrioClient, ResponseError


@pytest.fixture
def connect():
    clients = []

    def make(handler):
        def route(request):
            if request.url.path == "/api/rest/authorize":
                if request.method == "POST":
                    assert json.loads(request.content)["userId"] == "api_user"
                    return httpx.Response(200, json={"sessionId": "synthetic-session"})
                return httpx.Response(204)
            assert request.headers["Cookie"] == "hazelcast.sessionId=synthetic-session"
            assert "Authorization" not in request.headers
            return handler(request)

        client = CalabrioClient(
            url="https://tenant.example.com",
            username="api_user",
            password="synthetic-password",
            transport=httpx.MockTransport(route),
        )
        clients.append(client)
        return client

    yield make
    for client in clients:
        client.close()


def test_user_workflow_prepares_recording_automatically(connect, tmp_path):
    routes = []

    def handler(request):
        routes.append((request.method, request.url.path))
        if request.url.path.endswith("/metadata/"):
            return httpx.Response(200, json={"synthetic-field": "value"})
        if request.url.path.endswith("/speechtextview"):
            return httpx.Response(200, json={"transcript": []})
        if "/media/export/" in request.url.path:
            if request.method == "POST":
                return httpx.Response(200, json={"encoding": "true"})
            return httpx.Response(200, content=b"RIFF\x04\x00\x00\x00WAVE")
        return httpx.Response(
            200,
            json={
                "id": 123456,
                "metadata": {
                    "$ref": "/api/rest/recording/contact/123456/metadata/",
                },
            },
        )

    client = connect(handler)
    assert client.get_contact(123456)["id"] == 123456
    assert client.get_metadata("123456") == {"synthetic-field": "value"}
    assert client.get_transcript(123456) == {"transcript": []}
    target = client.download_recording(123456, tmp_path / "recording.wav")
    assert target.exists()
    assert routes[-2:] == [
        ("POST", "/api/rest/recording/media/export/contact/123456"),
        ("GET", "/api/rest/recording/media/export/contact/123456"),
    ]
    client.close()
    assert client._http.is_closed


@pytest.mark.parametrize(
    "contact,expected",
    [
        ({}, None),
        ({"metadata": {}}, {}),
        ({"metadata": {"tag": "synthetic"}}, {"tag": "synthetic"}),
    ],
)
def test_inline_and_absent_metadata(connect, contact, expected):
    requests = []

    def handler(request):
        requests.append(request)
        return httpx.Response(200, json=contact)

    assert connect(handler).get_metadata(123) == expected
    assert len(requests) == 1


def test_metadata_external_reference_rejected(connect):
    client = connect(
        lambda r: httpx.Response(
            200,
            json={
                "metadata": {
                    "$ref": "https://other.example.com/api/rest/recording/contact/123",
                }
            },
        )
    )
    with pytest.raises(ValueError):
        client.get_metadata(123)


@pytest.mark.parametrize("reference", [{"id": 7}, {"$ref": "/api/rest/recording/evalform/7"}])
def test_evaluation_resolves_form(connect, reference):
    def handler(request):
        if request.url.path.endswith("/evalform/7"):
            return httpx.Response(200, json={"sections": []})
        return httpx.Response(200, json={"evaluation": {"score": 90}, "evalForm": reference})

    assert connect(handler).get_evaluation(123) == {
        "summary": {"score": 90},
        "form": {"sections": []},
    }


def test_absent_evaluation_and_inline_form(connect):
    assert connect(lambda r: httpx.Response(200, json={})).get_evaluation(123) == {
        "summary": None,
        "form": None,
    }
    assert connect(
        lambda r: httpx.Response(200, json={"evalForm": {"sections": []}})
    ).get_evaluation(123)["form"] == {"sections": []}


def test_resume_does_not_request_conversion(connect, tmp_path):
    def handler(request):
        assert request.method == "GET"
        return httpx.Response(200, content=b"RIFF\x04\x00\x00\x00WAVE")

    connect(handler).download_recording(123, tmp_path / "resume.wav", prepare=False)


@pytest.mark.parametrize(
    "kwargs",
    [
        {"url": "https://tenant.example.com", "username": "api_user"},
        {"url": "https://tenant.example.com", "password": "synthetic"},
        {
            "url": "https://tenant.example.com",
            "username": "api_user",
            "password": "synthetic",
            "token": "synthetic",
        },
        {
            "url": "https://tenant.example.com",
            "base_url": "https://other.example.com",
            "token": "synthetic",
        },
    ],
)
def test_invalid_auth_combinations_do_not_send(kwargs):
    with pytest.raises(ValueError):
        CalabrioClient(
            **kwargs, transport=httpx.MockTransport(lambda r: pytest.fail("Must not send"))
        )


def test_wrong_api_methods_fail_without_sending(connect):
    with CalabrioClient(
        "https://tenant.example.com/api",
        "synthetic",
        transport=httpx.MockTransport(lambda r: pytest.fail("Must not send")),
    ) as wfm:
        with pytest.raises(ValueError, match="Recording methods require"):
            wfm.get_contact(123)
    with pytest.raises(ValueError, match="WFM methods require"):
        connect(lambda r: pytest.fail("Must not send")).all_business_units()


def test_context_logout_preserves_original_error():
    def handler(request):
        if request.method == "POST":
            return httpx.Response(200, json={"sessionId": "synthetic"})
        return httpx.Response(503)

    with pytest.raises(RuntimeError, match="original"):
        with CalabrioClient(
            url="https://tenant.example.com",
            username="synthetic",
            password="synthetic",
            transport=httpx.MockTransport(handler),
        ):
            raise RuntimeError("original")


def test_bad_login_raises():
    with pytest.raises(ResponseError):
        CalabrioClient(
            url="https://tenant.example.com",
            username="api_user",
            password="synthetic",
            transport=httpx.MockTransport(lambda r: httpx.Response(200, json={})),
        )


def test_environment_selection(monkeypatch):
    for name in [
        "CALABRIO_CLASSIC_URL",
        "CALABRIO_USERNAME",
        "CALABRIO_PASSWORD",
        "CALABRIO_BASE_URL",
        "CALABRIO_TOKEN",
    ]:
        monkeypatch.delenv(name, raising=False)
    monkeypatch.setenv("CALABRIO_CLASSIC_URL", "https://tenant.example.com")
    monkeypatch.setenv("CALABRIO_USERNAME", "api_user")
    monkeypatch.setenv("CALABRIO_PASSWORD", "synthetic")
    transport = httpx.MockTransport(lambda r: httpx.Response(200, json={"sessionId": "synthetic"}))
    with CalabrioClient.from_env(transport=transport) as client:
        assert client._classic is not None
    monkeypatch.setenv("CALABRIO_BASE_URL", "https://tenant.example.com/api")
    monkeypatch.setenv("CALABRIO_TOKEN", "synthetic")
    with pytest.raises(ValueError, match="Both API settings"):
        CalabrioClient.from_env()
    with CalabrioClient.from_env(api="wfm", transport=transport) as client:
        assert client._classic is None


@pytest.mark.parametrize(
    "method,expected",
    [
        (
            "export_contact",
            {"id": 123, "metadata": {"synthetic": True}, "evaluation": {"score": 90}},
        ),
        ("export_metadata", {"synthetic": True}),
        ("export_transcript", {"transcript": []}),
        ("export_evaluation", {"summary": {"score": 90}, "form": None}),
    ],
)
def test_one_call_json_exports(connect, tmp_path, method, expected):
    def handler(request):
        if request.url.path.endswith("speechtextview"):
            return httpx.Response(200, json={"transcript": []})
        return httpx.Response(
            200, json={"id": 123, "metadata": {"synthetic": True}, "evaluation": {"score": 90}}
        )

    target = tmp_path / "nested" / "data.json"
    client = connect(handler)
    assert getattr(client, method)(123, target) == target
    assert json.loads(target.read_text()) == expected
    assert len(list(target.parent.iterdir())) == 1
    with pytest.raises(FileExistsError):
        getattr(client, method)(123, target)


def test_json_exports_do_not_request_when_file_exists(connect, tmp_path):
    target = tmp_path / "data.json"
    target.write_text("existing")
    with pytest.raises(FileExistsError):
        connect(lambda r: pytest.fail("Must not send")).export_transcript(123, target)
    assert target.read_text() == "existing"


def test_json_export_cleanup_on_write_failure(connect, tmp_path, monkeypatch):
    def fail_write(value, output, **kwargs):
        output.write("partial")
        raise OSError("synthetic disk error")

    monkeypatch.setattr("calabrio_one._files.json.dump", fail_write)
    with pytest.raises(OSError):
        connect(lambda r: httpx.Response(200, json={"id": 123})).export_contact(
            123, tmp_path / "data.json"
        )
    assert not list(tmp_path.iterdir())


def test_json_export_preserves_a_racing_destination(connect, tmp_path):
    target = tmp_path / "data.json"

    def handler(request):
        target.write_text("existing")
        return httpx.Response(200, json={"id": 123})

    with pytest.raises(FileExistsError):
        connect(handler).export_contact(123, target)
    assert target.read_text() == "existing"
    assert list(tmp_path.iterdir()) == [target]


def test_date_export_paginates_short_pages_and_writes_all_resources(connect, tmp_path):
    ranges = []

    def handler(request):
        if request.url.path == "/api/rest/recording/contact":
            ranges.append(request.headers["Range"])
            assert request.url.params["beginDate"] == "2026-01-01"
            assert request.url.params["endDate"] == "2026-02-01"
            return httpx.Response(200, json=[{"id": len(ranges)}] if len(ranges) < 3 else [])
        if request.url.path.endswith("speechtextview"):
            return httpx.Response(200, json={"text": "Synthetic transcript"})
        if "/media/export/" in request.url.path:
            if request.method == "POST":
                return httpx.Response(200, json={})
            return httpx.Response(200, content=b"RIFF\x04\x00\x00\x00WAVE")
        return httpx.Response(200, json={"evaluation": {"score": 90}, "evalForm": {"sections": []}})

    folders = connect(handler).export_by_date("2026-01-01", "2026-02-01", tmp_path, page_size=2)
    assert ranges == ["items=1-2", "items=2-3", "items=3-4"]
    assert folders == [tmp_path / "1", tmp_path / "2"]
    for folder in folders:
        assert (folder / "recording.wav").exists()
        assert (folder / "transcript.json").exists()
        assert (folder / "evaluation-summary.json").exists()
        assert json.loads((folder / "manifest.json").read_text())["complete"]


def test_date_export_transcripts_only_and_times(connect, tmp_path):
    pages = []

    def handler(request):
        if request.url.path == "/api/rest/recording/contact":
            pages.append(request)
            assert request.url.params["beginTime"] == "09:00"
            assert request.url.params["endTime"] == "17:00:00"
            return httpx.Response(200, json=[{"id": 1}] if len(pages) == 1 else [])
        assert "/media/" not in request.url.path
        return httpx.Response(200, json={})

    folders = connect(handler).export_by_date(
        "2026-01-01",
        "2026-01-01",
        tmp_path,
        begin_time="09:00",
        end_time="17:00:00",
        include_recording=False,
        include_evaluation=False,
    )
    assert sorted(p.name for p in folders[0].iterdir()) == [
        "contact.json",
        "manifest.json",
        "transcript.json",
    ]


@pytest.mark.parametrize(
    "options",
    [
        {"begin_date": "2026-02-01", "end_date": "2026-01-01"},
        {"begin_date": "bad"},
        {"begin_time": "09:00"},
        {"begin_time": "25:00", "end_time": "17:00:00"},
        {"page_size": False},
        {"max_pages": 0},
        {"filters": {"limit": 10}},
        {"include_recording": False, "include_transcript": False, "include_evaluation": False},
    ],
)
def test_date_export_rejects_invalid_options_before_search(connect, tmp_path, options):
    client = connect(lambda r: pytest.fail("Unexpected request"))
    args = dict(begin_date="2026-01-01", end_date="2026-02-01", output_dir=tmp_path)
    args.update(options)
    with pytest.raises(ValueError):
        client.export_by_date(**args)
    assert not list(tmp_path.iterdir())


@pytest.mark.parametrize("page", [{"contacts": []}, [{}], [{"id": True}], [{"id": 1}, {"id": "1"}]])
def test_date_export_rejects_malformed_pages(connect, tmp_path, page):
    client = connect(lambda r: httpx.Response(200, json=page))
    with pytest.raises(ResponseError):
        client.export_by_date("2026-01-01", "2026-02-01", tmp_path)
    assert not list(tmp_path.iterdir())


@pytest.mark.parametrize("max_pages, message", [(1, "max_pages"), (2, "repeated")])
def test_date_export_pagination_guard_preserves_completed_calls(
    connect, tmp_path, max_pages, message
):
    client = connect(
        lambda r: httpx.Response(
            200, json=[{"id": 1}] if r.url.path == "/api/rest/recording/contact" else {}
        )
    )
    with pytest.raises(ResponseError, match=message):
        client.export_by_date(
            "2026-01-01",
            "2026-02-01",
            tmp_path,
            include_recording=False,
            include_evaluation=False,
            max_pages=max_pages,
        )
    assert (tmp_path / "1" / "manifest.json").exists()
