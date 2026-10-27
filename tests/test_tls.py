"""Real TLS handshakes using fresh, synthetic certificates and loopback only."""

import json
import ssl
import threading
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

import pytest
import trustme

from calabrio_one import CalabrioClient, ClassicClient, InsecureTLSWarning, TransportError
from calabrio_one._http import verify_tls


@pytest.fixture
def tls_server():
    ca = trustme.CA()
    cert = ca.issue_cert("127.0.0.1")
    requests = []

    class Handler(BaseHTTPRequestHandler):
        def log_message(self, *args):
            pass

        def respond(self):
            self.rfile.read(int(self.headers.get("Content-Length", 0)))
            requests.append((self.command, self.path))
            value = (
                {"sessionId": "synthetic-session"}
                if self.path == "/api/rest/authorize"
                else {"id": 1}
            )
            data = json.dumps(value).encode()
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.send_header("Content-Length", str(len(data)))
            self.end_headers()
            self.wfile.write(data)

        do_POST = respond
        do_GET = respond
        do_DELETE = respond

    server = ThreadingHTTPServer(("127.0.0.1", 0), Handler)
    context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
    cert.configure_cert(context)
    server.socket = context.wrap_socket(server.socket, server_side=True)
    thread = threading.Thread(
        target=server.serve_forever, kwargs={"poll_interval": 0.01}, daemon=True
    )
    thread.start()
    trusted = ssl.create_default_context()
    ca.configure_trust(trusted)
    try:
        yield f"https://127.0.0.1:{server.server_port}", trusted, requests
    finally:
        server.shutdown()
        server.server_close()
        thread.join(timeout=5)


def call(url, mode, verify):
    if mode == "wfm":
        with CalabrioClient(url=url + "/api", token="synthetic-token", verify=verify) as client:
            return client.all_business_units()
    if mode == "classic":
        with CalabrioClient(
            url=url, username="synthetic-user", password="synthetic-password", verify=verify
        ) as client:
            return client.get_contact(1)
    with ClassicClient(url, session_id="synthetic-session", verify=verify) as client:
        return client.get_contact(1)


@pytest.mark.parametrize("mode", ["wfm", "classic", "borrowed"])
def test_untrusted_certificate_fails_without_sending_http(tls_server, mode):
    url, _, requests = tls_server
    with pytest.raises(TransportError) as error:
        call(url, mode, True)
    assert requests == []
    assert url not in str(error.value)
    assert "synthetic-password" not in str(error.value)


@pytest.mark.parametrize("mode", ["wfm", "classic", "borrowed"])
def test_explicit_certificate_bypass_warns_and_connects(tls_server, mode):
    url, _, requests = tls_server
    with pytest.warns(InsecureTLSWarning, match="Server identity is not checked") as warnings:
        assert call(url, mode, False) == {"id": 1}
    assert len(warnings) == 1
    assert requests
    assert url not in str(warnings[0].message)


@pytest.mark.parametrize("mode", ["wfm", "classic", "borrowed"])
def test_trusted_private_ca_connects(tls_server, mode):
    url, trusted, _ = tls_server
    assert call(url, mode, trusted) == {"id": 1}


@pytest.mark.parametrize("api", ["classic", "wfm"])
def test_from_env_passes_certificate_option(tls_server, monkeypatch, api):
    url, _, _ = tls_server
    for key, value in {
        "CALABRIO_CLASSIC_URL": url,
        "CALABRIO_USERNAME": "synthetic-user",
        "CALABRIO_PASSWORD": "synthetic-password",
        "CALABRIO_BASE_URL": url + "/api",
        "CALABRIO_TOKEN": "synthetic-token",
    }.items():
        monkeypatch.setenv(key, value)
    with pytest.warns(InsecureTLSWarning):
        with CalabrioClient.from_env(api=api, verify=False) as client:
            assert (client.get_contact(1) if api == "classic" else client.all_business_units()) == {
                "id": 1
            }


@pytest.mark.parametrize("value", [0, 1, None, "false", "False", "path/to/cert.pem"])
def test_verification_requires_explicit_boolean_or_context(value):
    with pytest.raises(ValueError):
        verify_tls(value)


def test_insecure_context_cannot_silently_disable_verification():
    context = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
    context.check_hostname = False
    context.verify_mode = ssl.CERT_NONE
    with pytest.raises(ValueError):
        verify_tls(context)


def test_bypass_still_requires_https():
    with pytest.raises(ValueError, match="HTTPS"):
        CalabrioClient(url="http://tenant.example.com", token="synthetic-token", verify=False)
