"""Classic recording/QM API and streaming call exports."""

from __future__ import annotations

import json
import os
import re
import shutil
import ssl
import tempfile
import time
from collections.abc import Iterable, Mapping
from pathlib import Path
from typing import Any

import httpx

from ._http import check_status, decode_json, https_url, positive_seconds, verify_tls
from .exceptions import (
    CalabrioError,
    ExportTimeoutError,
    ResponseError,
    TransportError,
)

_FORMATS = {"WAV": "wav", "OPUS": "opus", "WEBM": "webm", "WEBM_VP8": "webm", "WEBM_VP9": "webm"}


def _id(value: int | str) -> str:
    if (
        isinstance(value, bool)
        or not isinstance(value, (int, str))
        or not re.fullmatch(r"[0-9]+", str(value))
    ):
        raise ValueError("ID must contain only decimal digits")
    return str(value)


class ClassicClient:
    """Classic session authentication; use a site origin, without /api.

    Connect with ``ClassicClient.connect(...)`` or ``ClassicClient.from_env()``.
    An explicitly supplied session_id is borrowed and is not logged out on close.
    verify=True checks certificates; a trusted-CA SSLContext supports private CAs.
    Explicit verify=False skips server identity checks and emits InsecureTLSWarning.
    """

    def __init__(
        self,
        base_url: str,
        *,
        session_id: str | None = None,
        timeout: float = 30,
        verify: ssl.SSLContext | bool = True,
        transport: httpx.BaseTransport | None = None,
    ) -> None:
        if https_url(base_url).path not in {"", "/"}:
            raise ValueError("Classic base_url must be a site origin, without /api")
        positive_seconds(timeout)
        verify_tls(verify)
        self._timeout = timeout
        self._owned_session = False
        self._http = httpx.Client(
            base_url=base_url.rstrip("/"),
            timeout=timeout,
            verify=verify,
            transport=transport,
            trust_env=False,
            follow_redirects=False,
            headers={"Accept": "application/json", "User-Agent": "calabrio-one-wrapper/0.1.0a1"},
        )
        if session_id is not None:
            try:
                self._set_session(session_id)
            except BaseException:
                self._http.close()
                raise

    def _set_session(self, session_id: str) -> None:
        if not isinstance(session_id, str) or not re.fullmatch(r"[A-Za-z0-9._-]+", session_id):
            raise ResponseError("Invalid session ID.")
        self._http.cookies.clear()
        self._http.headers["Cookie"] = f"hazelcast.sessionId={session_id}"

    @classmethod
    def connect(
        cls,
        base_url: str,
        username: str,
        password: str,
        *,
        language: str = "en",
        tenant_id: int | None = None,
        **kwargs: Any,
    ) -> ClassicClient:
        if (
            not isinstance(username, str)
            or not isinstance(password, str)
            or not username
            or not password
        ):
            raise ValueError("username and password are required")
        if "session_id" in kwargs:
            raise ValueError("Use credentials or an existing session, not both")
        client = cls(base_url, **kwargs)
        payload: dict[str, Any] = {"userId": username, "password": password, "language": language}
        if tenant_id is not None:
            payload["tenantId"] = tenant_id
        try:
            result = client._request("POST", "/api/rest/authorize", json=payload)
            if not isinstance(result, dict) or not result.get("sessionId"):
                raise ResponseError("Authorization response did not contain a session ID.")
            client._set_session(result["sessionId"])
            client._owned_session = True
            return client
        except BaseException:
            client._http.close()
            raise

    @classmethod
    def from_env(cls, **kwargs: Any) -> ClassicClient:
        base_url = os.environ.get("CALABRIO_CLASSIC_URL")
        username = os.environ.get("CALABRIO_USERNAME")
        password = os.environ.get("CALABRIO_PASSWORD")
        if not base_url or not username or not password:
            raise ValueError("Set CALABRIO_CLASSIC_URL, CALABRIO_USERNAME and CALABRIO_PASSWORD")
        return cls.connect(base_url, username, password, **kwargs)

    def __enter__(self) -> ClassicClient:
        return self

    def __exit__(self, exc_type: Any, exc: Any, traceback: Any) -> None:
        try:
            self.close()
        except CalabrioError:
            if exc_type is None:
                raise

    def close(self) -> None:
        if self._http.is_closed:
            return
        try:
            if self._owned_session:
                # Logout may have an empty 200 response.
                try:
                    check_status(self._http.delete("/api/rest/authorize"))
                except httpx.RequestError:
                    raise TransportError("Calabrio logout could not complete.") from None
        finally:
            self._owned_session = False
            self._http.headers.pop("Cookie", None)
            self._http.cookies.clear()
            self._http.close()

    @staticmethod
    def _resource_path(path: str) -> str:
        # References are untrusted. Never allow a remote host, traversal or encoded separators.
        if not isinstance(path, str) or not re.fullmatch(
            r"/api/rest/(?:recording|cas)/[A-Za-z0-9_-]+(?:/[A-Za-z0-9_-]+)*/?",
            path,
        ):
            raise ValueError("Expected a local recording or analytics API resource path")
        return path

    def _request(self, method: str, path: str, **kwargs: Any) -> Any:
        try:
            response = self._http.request(method, path, **kwargs)
        except httpx.RequestError:
            raise TransportError("Calabrio request could not complete.") from None
        return decode_json(response)

    def get_resource(self, reference: str) -> Any:
        """Read an exact local $ref or an independently verified resource path."""
        return self._request("GET", self._resource_path(reference))

    def get_contact(self, contact_id: int | str) -> dict:
        result = self._request("GET", f"/api/rest/recording/contact/{_id(contact_id)}")
        if not isinstance(result, dict):
            raise ResponseError("Expected a contact object.")
        return result

    def get_metadata(self, contact_id: int | str) -> Any:
        """Return inline metadata or fetch its local $ref; None when absent."""
        return self._resolve_resource(self.get_contact(contact_id).get("metadata"))

    def _resolve_resource(self, value: Any) -> Any:
        if isinstance(value, dict) and "$ref" in value:
            return self.get_resource(value["$ref"])
        return value

    def _contact_form(self, contact: dict) -> Any:
        form = contact.get("evalForm")
        if isinstance(form, dict):
            if "$ref" in form:
                return self._resolve_resource(form)
            if "id" in form:
                return self.get_evaluation_form(form["id"])
            if "sections" in form:
                return form
        return None

    def get_evaluation(self, contact_id: int | str) -> dict:
        """Return a call's summary and form definition; either may be None.

        These do not establish the selected answers to every evaluation question.
        """
        contact = self.get_contact(contact_id)
        return {"summary": contact.get("evaluation"), "form": self._contact_form(contact)}

    def search_contacts(
        self,
        *,
        begin_date: str | None = None,
        end_date: str | None = None,
        agent_id: int | None = None,
        start: int = 1,
        count: int = 100,
        filters: Mapping[str, Any] | None = None,
    ) -> Any:
        """Get one search page. Additional filters retain their documented API names."""
        if isinstance(start, bool) or not isinstance(start, int) or start < 1:
            raise ValueError("start must be a positive integer")
        if isinstance(count, bool) or not isinstance(count, int) or not 1 <= count <= 100:
            raise ValueError("count must be an integer between 1 and 100")
        params = dict(filters or {})
        for key, value in [("beginDate", begin_date), ("endDate", end_date), ("agent", agent_id)]:
            if value is not None:
                if key in params:
                    raise ValueError("Filter supplied more than once")
                params[key] = value
        # The server limit caps total results, so later ranges must raise that cap.
        params.setdefault("limit", start + count - 1)
        return self._request(
            "GET",
            "/api/rest/recording/contact",
            params=params,
            headers={"Range": f"items={start}-{start + count - 1}"},
        )

    def list_evaluation_forms(self) -> Any:
        return self._request("GET", "/api/rest/recording/evalform")

    def get_evaluation_form(self, form_id: int | str) -> Any:
        return self._request("GET", f"/api/rest/recording/evalform/{_id(form_id)}")

    def get_transcript(self, contact_id: int | str, *, is_root_recording: bool = False) -> Any:
        """Retrieve the transcript using the documented read-via-PUT operation."""
        if not isinstance(is_root_recording, bool):
            raise ValueError("is_root_recording must be a boolean")
        return self._request(
            "PUT",
            "/api/rest/cas/speechtextview",
            json={
                "ccrid": int(_id(contact_id)),
                "isRootRecording": str(is_root_recording).lower(),
            },
        )

    def start_recording_export(self, contact_id: int | str, *, media_format: str = "WAV") -> Any:
        media_format = self._format(media_format)
        return self._request(
            "POST",
            f"/api/rest/recording/media/export/contact/{_id(contact_id)}",
            params={"type": media_format},
        )

    @staticmethod
    def _format(value: str) -> str:
        if not isinstance(value, str):
            raise ValueError("media_format must be a string")
        value = value.upper()
        if value not in _FORMATS:
            raise ValueError(
                "Unsupported media format; choose WAV, OPUS, WEBM, WEBM_VP8 or WEBM_VP9"
            )
        return value

    def download_recording(
        self,
        contact_id: int | str,
        destination: str | Path,
        *,
        media_format: str = "WAV",
        wait_timeout: float = 120,
        poll_interval: float = 2,
    ) -> Path:
        """Download an already-requested export; poll only the download GET.

        Writes through a private temporary file, never overwrites an existing file.
        wait_timeout bounds polling and is checked between streamed chunks; the HTTP
        inactivity timeout also applies, so this is not a hard wall-clock deadline.
        """
        contact_id, media_format = _id(contact_id), self._format(media_format)
        positive_seconds(wait_timeout)
        positive_seconds(poll_interval)
        destination = Path(destination)
        if destination.exists() or destination.is_symlink():
            raise FileExistsError("Destination already exists")
        destination.parent.mkdir(parents=True, exist_ok=True)
        deadline = time.monotonic() + wait_timeout
        path = f"/api/rest/recording/media/export/contact/{contact_id}"
        while True:
            remaining = deadline - time.monotonic()
            if remaining <= 0:
                raise ExportTimeoutError("Recording export was not ready before the timeout.")
            try:
                with self._http.stream(
                    "GET",
                    path,
                    params={"type": media_format},
                    headers={"Accept": "*/*"},
                    timeout=min(self._timeout, remaining),
                ) as response:
                    pending = response.status_code in {202, 404}
                    if not pending:
                        content_type = response.headers.get("Content-Type", "").lower()
                        if "json" in content_type and response.status_code in {200, 500}:
                            # Status bodies are small; do not buffer unbounded JSON/error data.
                            data = bytearray()
                            for chunk in response.iter_bytes(chunk_size=65536):
                                if time.monotonic() >= deadline:
                                    raise ExportTimeoutError(
                                        "Export status response exceeded its timeout."
                                    )
                                if len(data) + len(chunk) > 1024 * 1024:
                                    raise ResponseError(
                                        "Export status response was unexpectedly large."
                                    )
                                data.extend(chunk)
                            response = httpx.Response(response.status_code, content=bytes(data))
                            try:
                                value = response.json()
                            except ValueError:
                                raise ResponseError("Invalid export response.") from None
                            pending = isinstance(value, dict) and (
                                value.get("encoding") in (True, "true")
                                or "does not exist or may have expired"
                                in str(value.get("errorMessage", ""))
                            )
                            if not pending:
                                decode_json(response)
                                raise ResponseError("Export returned JSON instead of media.")
                        else:
                            check_status(response)
                            if response.status_code != 200:
                                raise ResponseError(
                                    "Expected a complete media response (HTTP 200)."
                                )
                            return self._save_media(response, destination, media_format, deadline)
            except httpx.RequestError:
                raise TransportError("Recording download could not complete.") from None
            remaining = deadline - time.monotonic()
            if remaining <= 0:
                raise ExportTimeoutError("Recording export was not ready before the timeout.")
            time.sleep(min(poll_interval, remaining))

    @staticmethod
    def _save_media(
        response: httpx.Response, destination: Path, media_format: str, deadline: float
    ) -> Path:
        temp_path = None
        try:
            with tempfile.NamedTemporaryFile(
                dir=destination.parent, prefix=".calabrio-", delete=False
            ) as output:
                temp_path = Path(output.name)
                prefix = bytearray()
                for chunk in response.iter_bytes(chunk_size=65536):
                    if time.monotonic() >= deadline:
                        raise ExportTimeoutError("Recording download exceeded its timeout.")
                    if len(prefix) < 12:
                        prefix.extend(chunk[: 12 - len(prefix)])
                    output.write(chunk)
                if media_format == "WAV":
                    valid = prefix[:4] in (b"RIFF", b"RF64") and prefix[8:12] == b"WAVE"
                elif media_format == "OPUS":
                    valid = prefix[:4] in (b"OggS", b"\x1a\x45\xdf\xa3")
                else:
                    valid = prefix[:4] == b"\x1a\x45\xdf\xa3"
                if not valid:
                    raise ResponseError("Download did not contain the expected media format.")
            # Atomic no-clobber publication; temp and destination share a filesystem.
            os.link(temp_path, destination)
            return destination
        finally:
            if temp_path is not None:
                temp_path.unlink(missing_ok=True)

    def export_recording(
        self,
        contact_id: int | str,
        destination: str | Path,
        *,
        media_format: str = "WAV",
        wait_timeout: float = 120,
        poll_interval: float = 2,
    ) -> Path:
        """Request conversion once, then wait for and download the result."""
        if Path(destination).exists() or Path(destination).is_symlink():
            raise FileExistsError("Destination already exists")
        positive_seconds(wait_timeout)
        positive_seconds(poll_interval)
        self.start_recording_export(contact_id, media_format=media_format)
        return self.download_recording(
            contact_id,
            destination,
            media_format=media_format,
            wait_timeout=wait_timeout,
            poll_interval=poll_interval,
        )

    def export_call(
        self,
        contact_id: int | str,
        output_dir: str | Path,
        *,
        media_format: str = "WAV",
        include_recording: bool = True,
        include_transcript: bool = False,
        is_root_recording: bool = False,
        include_evaluation: bool = True,
        extra_resources: Mapping[str, str] | None = None,
        wait_timeout: float = 120,
        poll_interval: float = 2,
    ) -> Path:
        """Write output_dir/contact_id with media, metadata and selected JSON resources.

        extra_resources maps a simple name to a verified local GET path, for example
        evaluation-answers or evaluation-comments. No answer endpoint is guessed.
        Fails on requested-resource errors and removes this call's incomplete bundle.
        """
        contact_id, media_format = _id(contact_id), self._format(media_format)
        positive_seconds(wait_timeout)
        positive_seconds(poll_interval)
        if not all(
            isinstance(value, bool)
            for value in (
                include_recording,
                include_transcript,
                include_evaluation,
                is_root_recording,
            )
        ):
            raise ValueError("Export include/root options must be booleans")
        if extra_resources is not None and not isinstance(extra_resources, Mapping):
            raise TypeError("extra_resources must map names to resource paths")
        reserved = {
            "contact",
            "metadata",
            "transcript",
            "evaluation-summary",
            "evaluation-form",
            "manifest",
            "recording",
        }
        for name, reference in (extra_resources or {}).items():
            if (
                not isinstance(name, str)
                or not re.fullmatch(r"[a-z][a-z0-9_-]{0,99}", name)
                or name in reserved
                or name in {"con", "prn", "aux", "nul"}
                or re.fullmatch(r"(?:com|lpt)[1-9]", name)
            ):
                raise ValueError("Extra resource name is invalid or reserved")
            self._resource_path(reference)
        folder = Path(output_dir) / contact_id
        folder.parent.mkdir(parents=True, exist_ok=True)
        folder.mkdir(mode=0o700)  # Exclusive creation: never merge with previous exports.
        files = []
        missing = []

        def save(name: str, value: Any) -> None:
            target = folder / f"{name}.json"
            with target.open("x", encoding="utf-8") as output:
                json.dump(value, output, ensure_ascii=False, indent=2)
                output.write("\n")
            files.append(target.name)

        try:
            contact = self.get_contact(contact_id)
            save("contact", contact)
            if contact.get("metadata") is not None:
                save("metadata", self._resolve_resource(contact["metadata"]))
            else:
                missing.append("metadata")
            if include_evaluation:
                if contact.get("evaluation") is not None:
                    save("evaluation-summary", contact["evaluation"])
                else:
                    missing.append("evaluation-summary")
                form = self._contact_form(contact)
                if form is not None:
                    save("evaluation-form", form)
                else:
                    missing.append("evaluation-form")
            if include_transcript:
                save(
                    "transcript",
                    self.get_transcript(contact_id, is_root_recording=is_root_recording),
                )
            for name, reference in (extra_resources or {}).items():
                save(name, self.get_resource(reference))
            if include_recording:
                media = self.export_recording(
                    contact_id,
                    folder / f"recording.{_FORMATS[media_format]}",
                    media_format=media_format,
                    wait_timeout=wait_timeout,
                    poll_interval=poll_interval,
                )
                files.append(media.name)
            save(
                "manifest",
                {
                    "complete": True,
                    "files": list(files),
                    "absent": missing,
                    "recording_requested": include_recording,
                    "transcript_requested": include_transcript,
                    "evaluation_requested": include_evaluation,
                },
            )
            return folder
        except BaseException:
            shutil.rmtree(folder)
            raise

    def export_calls(
        self, contact_ids: Iterable[int | str], output_dir: str | Path, **kwargs: Any
    ) -> list[Path]:
        """Export supplied IDs sequentially, stopping on the first failure.

        Earlier completed bundles remain. This is not the server bulk-export API.
        """
        if isinstance(contact_ids, (str, bytes, Mapping)) or not isinstance(contact_ids, Iterable):
            raise TypeError("Pass a list, tuple or generator of IDs; use export_call() for one ID")
        return [self.export_call(contact_id, output_dir, **kwargs) for contact_id in contact_ids]
