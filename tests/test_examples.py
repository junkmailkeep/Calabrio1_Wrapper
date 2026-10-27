"""Run the shipped example against synthetic API responses, without credentials."""

import importlib.util
import json
from pathlib import Path

import httpx
import pytest

from calabrio_one import CalabrioClient

SPEC = importlib.util.spec_from_file_location(
    "export_example",
    Path(__file__).parents[1] / "examples/export_calls.py",
)
example = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(example)


@pytest.mark.parametrize("kind", ["call", "recording", "transcript", "evaluation"])
def test_script_modes_with_multiple_ids(kind, tmp_path, monkeypatch):
    routes = []

    def handler(request):
        routes.append(request.url.path)
        if request.url.path == "/api/rest/authorize":
            return httpx.Response(200, json={"sessionId": "synthetic"})
        if "/media/export/" in request.url.path:
            if request.method == "POST":
                return httpx.Response(200, json={"encoding": "true"})
            return httpx.Response(200, content=b"RIFF\x04\x00\x00\x00WAVE")
        if "/evalform/" in request.url.path:
            return httpx.Response(200, json={"sections": []})
        if request.url.path.endswith("speechtextview"):
            return httpx.Response(200, json={"transcript": []})
        return httpx.Response(200, json={"evaluation": {"score": 90}, "evalForm": {"id": 7}})

    client = CalabrioClient(
        url="https://tenant.example.com",
        username="synthetic",
        password="synthetic",
        transport=httpx.MockTransport(handler),
    )
    monkeypatch.setattr(CalabrioClient, "from_env", lambda **kwargs: client)
    args = ["--kind", kind, "--ids", "123456", "123457", "--output", str(tmp_path)]
    if kind == "call":
        args.append("--transcript")
    assert example.main(args) == 0
    assert client._http.is_closed
    assert len(list(tmp_path.iterdir())) == 2
    if kind in {"transcript", "evaluation"}:
        assert not any("/media/export/" in route for route in routes)
    if kind == "evaluation":
        assert json.loads((tmp_path / "123456-evaluation.json").read_text()) == {
            "summary": {"score": 90},
            "form": {"sections": []},
        }


def test_script_failure_does_not_print_server_details(tmp_path, monkeypatch, capsys):
    def handler(request):
        if request.url.path == "/api/rest/authorize":
            return httpx.Response(200, json={"sessionId": "synthetic"})
        return httpx.Response(403, text="synthetic-confidential-response")

    client = CalabrioClient(
        url="https://tenant.example.com",
        username="synthetic",
        password="synthetic",
        transport=httpx.MockTransport(handler),
    )
    monkeypatch.setattr(CalabrioClient, "from_env", lambda **kwargs: client)
    assert example.main(["--kind", "transcript", "--ids", "123", "--output", str(tmp_path)]) == 1
    assert "synthetic-confidential-response" not in capsys.readouterr().out
    assert not list(tmp_path.iterdir())
    assert client._http.is_closed


def test_quickstart_script_uses_the_simple_client(tmp_path, monkeypatch):
    spec = importlib.util.spec_from_file_location(
        "quickstart",
        Path(__file__).parents[1] / "examples/quickstart.py",
    )
    quickstart = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(quickstart)
    requests = []

    def handler(request):
        requests.append((request.method, request.url.path))
        if request.url.path == "/api/rest/authorize":
            return httpx.Response(200, json={"sessionId": "synthetic"})
        if "/media/export/" in request.url.path:
            if request.method == "POST":
                return httpx.Response(200, json={"encoding": "true"})
            return httpx.Response(200, content=b"RIFF\x04\x00\x00\x00WAVE")
        if request.url.path.endswith("speechtextview"):
            return httpx.Response(200, json={"transcript": []})
        return httpx.Response(200, json={"id": 123456, "metadata": {"synthetic": True}})

    def constructor(**kwargs):
        return CalabrioClient(**kwargs, transport=httpx.MockTransport(handler))

    monkeypatch.setattr(quickstart, "CalabrioClient", constructor)
    monkeypatch.chdir(tmp_path)
    quickstart.main()
    assert (tmp_path / "recording.wav").exists()
    assert requests[0] == ("POST", "/api/rest/authorize")
    assert requests[-1] == ("DELETE", "/api/rest/authorize")


def test_wfm_script_uses_named_arguments(tmp_path, monkeypatch):
    spec = importlib.util.spec_from_file_location(
        "wfm_example", Path(__file__).parents[1] / "examples/wfm.py"
    )
    wfm = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(wfm)
    requests = []

    def handler(request):
        requests.append(request)
        if request.url.path.endswith("ScheduleByPersonId"):
            assert json.loads(request.content)["Period"] == {
                "StartDate": "2026-01-01",
                "EndDate": "2026-01-07",
            }
        return httpx.Response(200, json={"Result": []})

    def constructor(**kwargs):
        return CalabrioClient(**kwargs, transport=httpx.MockTransport(handler))

    monkeypatch.setattr(wfm, "CalabrioClient", constructor)
    result = wfm.main()
    assert len(requests) == 4
    assert result["schedule"] == {"Result": []}
    assert all("/query/" in str(request.url) for request in requests)
