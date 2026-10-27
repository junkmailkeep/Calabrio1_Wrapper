import json

import httpx
import pytest

from calabrio_one import (
    APIError,
    AuthenticationError,
    ClassicClient,
    ExportTimeoutError,
    OperationError,
    ResponseError,
    TransportError,
)

WAV = b"RIFF\x04\x00\x00\x00WAVE" + b"synthetic-audio" * 10000


@pytest.fixture
def factory():
    clients = []

    def make(handler):
        client = ClassicClient(
            "https://tenant.example.com",
            session_id="synthetic-session",
            transport=httpx.MockTransport(handler),
        )
        clients.append(client)
        return client

    yield make
    for client in clients:
        client.close()


def test_session_lifecycle():
    calls = []

    def handler(request):
        calls.append(request.method)
        if request.method == "POST":
            assert request.url.path == "/api/rest/authorize"
            assert json.loads(request.content) == {
                "userId": "synthetic-user",
                "password": "synthetic-secret",
                "language": "en",
                "tenantId": 1,
            }
            return httpx.Response(200, json={"sessionId": "synthetic-session"})
        assert request.headers["Cookie"] == "hazelcast.sessionId=synthetic-session"
        return (
            httpx.Response(200, json={"id": 123})
            if request.method == "GET"
            else httpx.Response(200)
        )

    with ClassicClient.connect(
        "https://tenant.example.com",
        "synthetic-user",
        "synthetic-secret",
        tenant_id=1,
        transport=httpx.MockTransport(handler),
    ) as client:
        assert client.get_contact(123) == {"id": 123}
    client.close()
    assert calls == ["POST", "GET", "DELETE"]
    assert "Cookie" not in client._http.headers


def test_from_environment(monkeypatch):
    monkeypatch.setenv("CALABRIO_CLASSIC_URL", "https://tenant.example.com")
    monkeypatch.setenv("CALABRIO_USERNAME", "synthetic-user")
    monkeypatch.setenv("CALABRIO_PASSWORD", "synthetic-secret")
    with ClassicClient.from_env(
        transport=httpx.MockTransport(
            lambda r: httpx.Response(200, json={"sessionId": "synthetic-session"})
        )
    ) as client:
        assert not client._http.is_closed


@pytest.mark.parametrize("body", [{}, {"sessionId": "bad; injected=cookie"}])
def test_bad_login(body):
    with pytest.raises(ResponseError):
        ClassicClient.connect(
            "https://tenant.example.com",
            "user",
            "secret",
            transport=httpx.MockTransport(lambda r: httpx.Response(200, json=body)),
        )


def test_transcript_contract(factory):
    def handler(request):
        assert request.method == "PUT"
        assert request.url.path == "/api/rest/cas/speechtextview"
        assert json.loads(request.content) == {"ccrid": 123, "isRootRecording": "false"}
        return httpx.Response(200, json={"transcript": []})

    assert factory(handler).get_transcript("123") == {"transcript": []}


def test_search_range_and_repeated_filters(factory):
    def handler(request):
        assert request.headers["Range"] == "items=101-200"
        assert request.url.params["limit"] == "200"
        assert request.url.params.get_list("ani") == ["111", "222"]
        assert request.url.params["beginDate"] == "2026-01-01"
        assert request.url.params["agent"] == "3"
        return httpx.Response(200, json=[])

    assert (
        factory(handler).search_contacts(
            begin_date="2026-01-01", agent_id=3, start=101, filters={"ani": ["111", "222"]}
        )
        == []
    )


def test_delayed_media_download(factory, tmp_path):
    methods = []

    def handler(request):
        methods.append(request.method)
        assert request.url.params["type"] == "WAV"
        if request.method == "POST":
            return httpx.Response(200, json={"encoding": "true"})
        if len(methods) == 2:
            return httpx.Response(404)
        if len(methods) == 3:
            return httpx.Response(
                500, json={"errorMessage": "File does not exist or may have expired"}
            )
        return httpx.Response(200, content=WAV, headers={"Content-Type": "audio/wav"})

    target = factory(handler).export_recording(123, tmp_path / "call.wav", poll_interval=0.001)
    assert target.read_bytes() == WAV
    assert methods == ["POST", "GET", "GET", "GET"]
    assert list(tmp_path.iterdir()) == [target]


def test_timeout_cleans_up(factory, tmp_path):
    client = factory(lambda r: httpx.Response(202))
    with pytest.raises(ExportTimeoutError):
        client.download_recording(
            123, tmp_path / "call.wav", wait_timeout=0.005, poll_interval=0.001
        )
    assert list(tmp_path.iterdir()) == []


@pytest.mark.parametrize(
    "response,error",
    [
        (httpx.Response(401, text="private-response"), AuthenticationError),
        (httpx.Response(302, headers={"Location": "https://elsewhere.example.com"}), APIError),
        (httpx.Response(200, text="<html>login</html>"), ResponseError),
        (httpx.Response(200, json={"errorMessage": "private-response"}), OperationError),
        (httpx.Response(200, content=b""), ResponseError),
    ],
)
def test_download_failures(factory, tmp_path, response, error):
    calls = []

    def handler(request):
        calls.append(request)
        return response

    with pytest.raises(error) as caught:
        factory(handler).download_recording(123, tmp_path / "call.wav")
    assert "private-response" not in str(caught.value)
    assert len(calls) == 1
    assert list(tmp_path.iterdir()) == []


def test_interrupted_stream(factory, tmp_path):
    class BrokenStream(httpx.SyncByteStream):
        def __iter__(self):
            yield WAV
            raise httpx.ReadError("private transport details")

    with pytest.raises(TransportError):
        factory(lambda r: httpx.Response(200, stream=BrokenStream())).download_recording(
            123,
            tmp_path / "call.wav",
        )
    assert list(tmp_path.iterdir()) == []


def test_existing_file_not_overwritten_or_requested(factory, tmp_path):
    target = tmp_path / "call.wav"
    target.write_text("keep")
    with pytest.raises(FileExistsError):
        factory(lambda r: pytest.fail("Must not send")).export_recording(123, target)
    assert target.read_text() == "keep"


@pytest.mark.parametrize(
    "path",
    [
        "https://elsewhere.example.com/api/rest/recording/contact/1",
        "//elsewhere.example.com/api/rest/recording/contact/1",
        "/api/rest/recording/../authorize",
        "/api/rest/recording/%2e%2e/authorize",
        "/api/rest/recording/contact/1?token=secret",
        "/api/rest/authorize",
    ],
)
def test_unsafe_reference_blocked(factory, path):
    with pytest.raises(ValueError):
        factory(lambda r: pytest.fail("Must not send")).get_resource(path)


def test_complete_bundle(factory, tmp_path):
    def handler(request):
        route = request.url.path
        if route == "/api/rest/recording/contact/123":
            return httpx.Response(
                200,
                json={
                    "id": 123,
                    "metadata": {"$ref": "/api/rest/recording/contact/123/metadata/"},
                    "evaluation": {"id": 7, "score": 90},
                    "evalForm": {"id": 8},
                },
            )
        if "/media/export/" in route:
            if request.method == "POST":
                return httpx.Response(200, json={"encoding": "true"})
            return httpx.Response(200, content=WAV)
        return httpx.Response(200, json={"synthetic": True})

    folder = factory(handler).export_call(
        123,
        tmp_path,
        include_transcript=True,
        extra_resources={"evaluation-comments": "/api/rest/recording/synthetic/comments"},
    )
    assert {p.name for p in folder.iterdir()} == {
        "contact.json",
        "metadata.json",
        "evaluation-summary.json",
        "evaluation-form.json",
        "transcript.json",
        "evaluation-comments.json",
        "recording.wav",
        "manifest.json",
    }
    assert json.loads((folder / "manifest.json").read_text())["complete"]
    assert (folder / "recording.wav").read_bytes() == WAV
    with pytest.raises(FileExistsError):
        factory(handler).export_call(123, tmp_path)


def test_bundle_failure_removes_only_new_bundle(factory, tmp_path):
    (tmp_path / "previous").mkdir()

    def handler(request):
        if request.url.path.endswith("/123"):
            return httpx.Response(200, json={"id": 123})
        return httpx.Response(403)

    with pytest.raises(APIError):
        factory(handler).export_call(123, tmp_path, include_transcript=True)
    assert {p.name for p in tmp_path.iterdir()} == {"previous"}


def test_missing_optional_data_recorded(factory, tmp_path):
    def handler(request):
        if "/media/export/" in request.url.path and request.method == "GET":
            return httpx.Response(200, content=WAV)
        return httpx.Response(200, json={})

    folder = factory(handler).export_call(123, tmp_path)
    manifest = json.loads((folder / "manifest.json").read_text())
    assert manifest["absent"] == ["metadata", "evaluation-summary", "evaluation-form"]
    assert not manifest["transcript_requested"]


def test_batch_keeps_completed_calls(factory, tmp_path):
    def handler(request):
        if request.url.path.endswith("/124"):
            return httpx.Response(403)
        if "/media/export/" in request.url.path and request.method == "GET":
            return httpx.Response(200, content=WAV)
        return httpx.Response(200, json={})

    with pytest.raises(APIError):
        factory(handler).export_calls([123, 124, 125], tmp_path)
    assert {p.name for p in tmp_path.iterdir()} == {"123"}


@pytest.mark.parametrize("identifier", ["../secret", "12/34", True, -1, "1?x=2"])
def test_invalid_id(factory, tmp_path, identifier):
    with pytest.raises(ValueError):
        factory(lambda r: pytest.fail("Must not send")).export_call(identifier, tmp_path)
    assert list(tmp_path.iterdir()) == []


def test_logout_does_not_mask_original_failure():
    def handler(request):
        if request.method == "POST":
            return httpx.Response(200, json={"sessionId": "synthetic-session"})
        return httpx.Response(503)

    with pytest.raises(RuntimeError, match="original"):
        with ClassicClient.connect(
            "https://tenant.example.com", "user", "secret", transport=httpx.MockTransport(handler)
        ):
            raise RuntimeError("original")


@pytest.mark.parametrize(
    "url",
    [
        "http://tenant.example.com",
        "https://tenant.example.com/api",
        "https://user:secret@tenant.example.com",
        "https://tenant.example.com?secret=x",
    ],
)
def test_classic_origin_validation(url):
    with pytest.raises(ValueError):
        ClassicClient(url)


def test_implicit_tls_bypass_rejected():
    with pytest.raises(ValueError):
        ClassicClient("https://tenant.example.com", verify=0)


def test_bundle_rejects_server_reference_to_another_host(factory, tmp_path):
    requests = []

    def handler(request):
        requests.append(request)
        return httpx.Response(
            200,
            json={
                "metadata": {
                    "$ref": "https://elsewhere.example.com/api/rest/recording/contact/123",
                }
            },
        )

    with pytest.raises(ValueError):
        factory(handler).export_call(123, tmp_path)
    assert len(requests) == 1
    assert list(tmp_path.iterdir()) == []


def test_no_clobber_even_if_destination_created_during_download(factory, tmp_path):
    target = tmp_path / "recording.wav"

    def handler(request):
        target.write_bytes(b"keep-existing")
        return httpx.Response(200, content=WAV)

    with pytest.raises(FileExistsError):
        factory(handler).download_recording(123, target)
    assert target.read_bytes() == b"keep-existing"
    assert list(tmp_path.iterdir()) == [target]


@pytest.mark.parametrize("ids", ["123", b"123", 123, None, {123: {"include_transcript": True}}])
def test_batch_rejects_ambiguous_inputs(factory, tmp_path, ids):
    with pytest.raises(TypeError, match="list, tuple or generator"):
        factory(lambda r: pytest.fail("Must not send")).export_calls(ids, tmp_path)
    assert not list(tmp_path.iterdir())


@pytest.mark.parametrize(
    "options",
    [
        {"include_transcript": "false"},
        {"include_evaluation": 1},
        {"is_root_recording": None},
        {"wait_timeout": 0},
        {"poll_interval": True},
        {"poll_interval": float("nan")},
        {"extra_resources": []},
        {"extra_resources": {"con": "/api/rest/recording/test"}},
        {"extra_resources": {"lpt1": "/api/rest/recording/test"}},
        {"extra_resources": {"../escape": "/api/rest/recording/test"}},
        {"extra_resources": {"manifest": "/api/rest/recording/test"}},
    ],
)
def test_export_options_rejected_before_io(factory, tmp_path, options):
    with pytest.raises((ValueError, TypeError)):
        factory(lambda r: pytest.fail("Must not send")).export_call(123, tmp_path, **options)
    assert not list(tmp_path.iterdir())


def test_partial_http_response_is_not_published(factory, tmp_path):
    with pytest.raises(ResponseError, match="complete media response"):
        factory(
            lambda r: httpx.Response(
                206,
                content=WAV,
                headers={
                    "Content-Range": "bytes 0-149999/300000",
                },
            )
        ).download_recording(123, tmp_path / "call.wav")
    assert not list(tmp_path.iterdir())


def test_large_status_response_is_bounded(factory, tmp_path):
    class StatusStream(httpx.SyncByteStream):
        def __iter__(self):
            for _ in range(18):
                yield b" " * 65536
            pytest.fail("Should stop reading oversized status body")

    with pytest.raises(ResponseError, match="unexpectedly large"):
        factory(
            lambda r: httpx.Response(
                200, headers={"Content-Type": "application/json"}, stream=StatusStream()
            )
        ).download_recording(123, tmp_path / "call.wav")
    assert not list(tmp_path.iterdir())


@pytest.mark.parametrize(
    "media_format,content",
    [
        ("opus", b"OggS" + b"\x00" * 20),
        ("WEBM", b"\x1a\x45\xdf\xa3" + b"\x00" * 20),
        ("WEBM_VP8", b"\x1a\x45\xdf\xa3" + b"\x00" * 20),
        ("WEBM_VP9", b"\x1a\x45\xdf\xa3" + b"\x00" * 20),
    ],
)
def test_supported_media_containers(factory, tmp_path, media_format, content):
    target = factory(lambda r: httpx.Response(200, content=content)).download_recording(
        123,
        tmp_path / "media",
        media_format=media_format,
    )
    assert target.read_bytes() == content


def test_invalid_id_object_not_stringified(factory):
    class NotAnID:
        def __str__(self):
            return "123"

    with pytest.raises(ValueError):
        factory(lambda r: pytest.fail("Must not send")).get_contact(NotAnID())
