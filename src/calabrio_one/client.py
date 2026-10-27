"""Simple public client for recordings/QM and token-based WFM operations."""

from __future__ import annotations

import json
import os
import re
import ssl
from collections.abc import Iterable, Mapping
from datetime import date, datetime
from pathlib import Path
from typing import Any
from uuid import UUID

import httpx

from ._arguments import normalize
from ._files import destination_path, write_json
from ._http import decode_json, https_url, positive_seconds, verify_tls
from .classic import ClassicClient, _id
from .endpoints import WFMEndpoints
from .exceptions import ResponseError, TransportError


def _json_default(value: Any) -> str:
    if isinstance(value, (date, datetime)):
        return value.isoformat()
    if isinstance(value, UUID):
        return str(value)
    raise TypeError(f"Unsupported JSON value type: {type(value).__name__}")


class CalabrioClient(WFMEndpoints):
    """Connect with url/username/password for calls, or base_url/token for WFM.

    Username/password construction logs in immediately. Call close() when finished,
    or use a with block to log out automatically. Downloads prepare media once and
    wait for it; no separate export setup is required.

    verify defaults to True. Pass a trusted-CA SSLContext for private certificates,
    or explicitly False to skip server identity checks (emits InsecureTLSWarning).
    """

    def __init__(
        self,
        base_url: str | None = None,
        token: str | None = None,
        *,
        url: str | None = None,
        username: str | None = None,
        password: str | None = None,
        language: str = "en",
        tenant_id: int | None = None,
        timeout: float = 30.0,
        auth_mode: str = "bearer",
        transport: httpx.BaseTransport | None = None,
        verify: ssl.SSLContext | bool = True,
    ) -> None:
        self._classic: ClassicClient | None = None
        if base_url is not None and url is not None:
            raise ValueError("Use url or base_url, not both")
        address = url if url is not None else base_url
        if address is None:
            raise ValueError("Provide the server url")
        if username is not None or password is not None:
            if token is not None or auth_mode != "bearer":
                raise ValueError("Use username/password for recordings or token for WFM, not both")
            if not isinstance(username, str) or not isinstance(password, str):
                raise ValueError("Both username and password are required")
            self._classic = ClassicClient.connect(
                address,
                username,
                password,
                language=language,
                tenant_id=tenant_id,
                timeout=timeout,
                verify=verify,
                transport=transport,
            )
            self._http = self._classic._http
            return
        if tenant_id is not None or language != "en":
            raise ValueError("language and tenant_id apply only to username/password login")
        base_url = address
        https_url(base_url)
        positive_seconds(timeout)
        verify_tls(verify)
        if (
            not isinstance(token, str)
            or not token
            or any(ord(c) < 33 or ord(c) > 126 for c in token)
        ):
            raise ValueError("token must be a nonempty token without whitespace")
        if auth_mode not in {"bearer", "basic"}:
            raise ValueError("auth_mode must be 'bearer' or 'basic'")
        headers = {"Accept": "application/json", "User-Agent": "calabrio-one-wrapper/0.1.0a2"}
        auth = None
        if auth_mode == "bearer":
            headers["Authorization"] = f"Bearer {token}"
        else:
            auth = httpx.BasicAuth("__token__", token)
        self._http = httpx.Client(
            base_url=base_url.rstrip("/") + "/",
            headers=headers,
            auth=auth,
            timeout=timeout,
            follow_redirects=False,
            transport=transport,
            trust_env=False,
            verify=verify,
        )

    @classmethod
    def from_env(cls, *, api: str | None = None, **kwargs: Any) -> CalabrioClient:
        """Read Classic credentials or WFM token settings. Never loads .env files.

        If both sets exist, choose api="classic" or api="wfm" explicitly.
        """
        classic_keys = ("CALABRIO_CLASSIC_URL", "CALABRIO_USERNAME", "CALABRIO_PASSWORD")
        wfm_keys = ("CALABRIO_BASE_URL", "CALABRIO_TOKEN")
        if api is None:
            classic_set = any(os.environ.get(key) for key in classic_keys)
            wfm_set = any(os.environ.get(key) for key in wfm_keys)
            if classic_set and wfm_set:
                raise ValueError("Both API settings exist; choose api='classic' or api='wfm'")
            api = "classic" if classic_set else "wfm"
        if api == "classic":
            address, username, password = (os.environ.get(key) for key in classic_keys)
            if not address or not username or not password:
                raise ValueError(
                    "Set CALABRIO_CLASSIC_URL, CALABRIO_USERNAME and CALABRIO_PASSWORD"
                )
            return cls(url=address, username=username, password=password, **kwargs)
        if api == "wfm":
            base_url = os.environ.get("CALABRIO_BASE_URL")
            token = os.environ.get("CALABRIO_TOKEN")
            if not base_url or not token:
                raise ValueError("Set CALABRIO_BASE_URL and CALABRIO_TOKEN")
            return cls(base_url, token, **kwargs)
        raise ValueError("api must be 'classic' or 'wfm'")

    def __enter__(self) -> CalabrioClient:
        return self

    def __exit__(self, exc_type: Any, exc: Any, traceback: Any) -> None:
        if self._classic is not None:
            self._classic.__exit__(exc_type, exc, traceback)
        else:
            self.close()

    def close(self) -> None:
        """Log out a recordings session and release connections. Safe to call twice."""
        if self._classic is not None:
            self._classic.close()
        else:
            self._http.close()
            self._http.headers.pop("Authorization", None)
            self._http.cookies.clear()
            self._http.auth = httpx.Auth()

    def _recordings(self) -> ClassicClient:
        if self._classic is None:
            raise ValueError(
                "Recording methods require CalabrioClient(url=..., username=..., password=...)"
            )
        return self._classic

    def get_contact(self, contact_id: int | str) -> dict:
        """Return contact details for one integer or numeric-string contact ID."""
        return self._recordings().get_contact(contact_id)

    def get_metadata(self, contact_id: int | str) -> Any:
        """Return call metadata, following its local reference if needed; None if absent."""
        return self._recordings().get_metadata(contact_id)

    def get_transcript(self, contact_id: int | str, *, is_root_recording: bool = False) -> Any:
        """Return transcript JSON for one call; no files are written."""
        return self._recordings().get_transcript(contact_id, is_root_recording=is_root_recording)

    def get_evaluation(self, contact_id: int | str) -> dict:
        """Return {'summary': ..., 'form': ...}; not completed question-level answers."""
        return self._recordings().get_evaluation(contact_id)

    def get_evaluation_form(self, form_id: int | str) -> Any:
        """Return the form definition for a form ID, not a contact ID."""
        return self._recordings().get_evaluation_form(form_id)

    def list_evaluation_forms(self) -> Any:
        return self._recordings().list_evaluation_forms()

    def get_resource(self, reference: str) -> Any:
        """Read an exact verified local recording/analytics resource path."""
        return self._recordings().get_resource(reference)

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
        """Return one search page; filters retain the server's field names."""
        return self._recordings().search_contacts(
            begin_date=begin_date,
            end_date=end_date,
            agent_id=agent_id,
            start=start,
            count=count,
            filters=filters,
        )

    def download_recording(
        self,
        contact_id: int | str,
        destination: str | Path,
        *,
        media_format: str = "WAV",
        wait_timeout: float = 120,
        poll_interval: float = 2,
        prepare: bool = True,
    ) -> Path:
        """Prepare, wait for and save one recording. Existing files are never overwritten.

        Set prepare=False only to resume an export that was already requested.
        """
        if not isinstance(prepare, bool):
            raise ValueError("prepare must be a boolean")
        recordings = self._recordings()
        download = recordings.export_recording if prepare else recordings.download_recording
        return download(
            contact_id,
            destination,
            media_format=media_format,
            wait_timeout=wait_timeout,
            poll_interval=poll_interval,
        )

    def export_recording(
        self,
        contact_id: int | str,
        destination: str | Path,
        *,
        media_format: str = "WAV",
        wait_timeout: float = 120,
        poll_interval: float = 2,
    ) -> Path:
        """Alias for download_recording(): prepare and download one recording."""
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
        """Save one call bundle: media, metadata and requested transcript/QA data."""
        return self._recordings().export_call(
            contact_id,
            output_dir,
            media_format=media_format,
            include_recording=include_recording,
            include_transcript=include_transcript,
            is_root_recording=is_root_recording,
            include_evaluation=include_evaluation,
            extra_resources=extra_resources,
            wait_timeout=wait_timeout,
            poll_interval=poll_interval,
        )

    def export_calls(
        self,
        contact_ids: Iterable[int | str],
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
    ) -> list[Path]:
        """Save bundles for a list/tuple/generator of IDs with these shared options."""
        return self._recordings().export_calls(
            contact_ids,
            output_dir,
            media_format=media_format,
            include_recording=include_recording,
            include_transcript=include_transcript,
            is_root_recording=is_root_recording,
            include_evaluation=include_evaluation,
            extra_resources=extra_resources,
            wait_timeout=wait_timeout,
            poll_interval=poll_interval,
        )

    def export_by_date(
        self,
        begin_date: str | date,
        end_date: str | date,
        output_dir: str | Path = "exports",
        *,
        include_recording: bool = True,
        include_transcript: bool = True,
        include_evaluation: bool = True,
        begin_time: str | None = None,
        end_time: str | None = None,
        agent_id: int | None = None,
        filters: Mapping[str, Any] | None = None,
        page_size: int = 100,
        max_pages: int = 10000,
        media_format: str = "WAV",
        is_root_recording: bool = False,
        wait_timeout: float = 120,
        poll_interval: float = 2,
    ) -> list[Path]:
        """Export matching calls, including all three resources by default.

        Start is inclusive; end is exclusive. Dates are YYYY-MM-DD or date objects.
        Optional times must be paired: begin HH:MM, end HH:MM:SS. Timezone follows
        the server's search semantics. Stops on failure, retaining completed calls.
        Pages until empty; duplicate IDs or the page guard fail rather than silently
        declaring a complete export. Server permissions and retention still apply.
        """
        self._recordings()

        def parse_date(value: str | date) -> date:
            if isinstance(value, datetime):
                raise ValueError("Pass a date and separate begin_time/end_time")
            if isinstance(value, date):
                return value
            if not isinstance(value, str) or not re.fullmatch(r"\d{4}-\d{2}-\d{2}", value):
                raise ValueError("Dates must use YYYY-MM-DD")
            return date.fromisoformat(value)

        begin, end = parse_date(begin_date), parse_date(end_date)
        if (begin_time is None) != (end_time is None):
            raise ValueError("Supply both begin_time and end_time")
        if begin_time is not None:
            if not isinstance(begin_time, str) or not re.fullmatch(
                r"(?:[01]\d|2[0-3]):[0-5]\d", begin_time
            ):
                raise ValueError("begin_time must use HH:MM")
            if not isinstance(end_time, str) or not re.fullmatch(
                r"(?:[01]\d|2[0-3]):[0-5]\d:[0-5]\d", end_time
            ):
                raise ValueError("end_time must use HH:MM:SS")
        start_boundary = (begin, begin_time + ":00" if begin_time else "00:00:00")
        end_boundary = (end, end_time or "00:00:00")
        if start_boundary >= end_boundary:
            raise ValueError("End must be after start")
        for name, value, maximum in [
            ("page_size", page_size, 100),
            ("max_pages", max_pages, 1000000),
        ]:
            if isinstance(value, bool) or not isinstance(value, int) or not 1 <= value <= maximum:
                raise ValueError(f"{name} must be between 1 and {maximum}")
        if not all(
            isinstance(value, bool)
            for value in (
                include_recording,
                include_transcript,
                include_evaluation,
                is_root_recording,
            )
        ):
            raise ValueError("Include/root options must be booleans")
        if not any((include_recording, include_transcript, include_evaluation)):
            raise ValueError("Select at least one resource to export")
        self._recordings()._format(media_format)
        positive_seconds(wait_timeout)
        positive_seconds(poll_interval)
        params = dict(filters or {})
        if params.keys() & {
            "beginDate",
            "endDate",
            "beginTime",
            "endTime",
            "limit",
            "searchStats",
            "range",
        }:
            raise ValueError(
                "Use date/time arguments; pagination and searchStats are managed automatically"
            )
        if agent_id is not None and "agent" in params:
            raise ValueError("Agent filter supplied twice")
        if begin_time is not None:
            params.update(beginTime=begin_time, endTime=end_time)
        paths: list[Path] = []
        seen: set[str] = set()
        start = 1
        for _ in range(max_pages):
            page = self.search_contacts(
                begin_date=begin.isoformat(),
                end_date=end.isoformat(),
                agent_id=agent_id,
                start=start,
                count=page_size,
                filters=params,
            )
            if not isinstance(page, list) or len(page) > page_size:
                raise ResponseError("Expected a contact list within the requested page size")
            if not page:
                return paths
            ids = []
            for contact in page:
                try:
                    contact_id = _id(contact["id"]) if isinstance(contact, dict) else None
                    if contact_id is None:
                        raise ValueError
                except (KeyError, TypeError, ValueError) as exc:
                    raise ResponseError("Search returned a contact without a valid ID") from exc
                if contact_id in seen:
                    raise ResponseError(
                        "Search repeated a contact; results may have changed or pagination was ignored"
                    )
                seen.add(contact_id)
                ids.append(contact_id)
            for contact_id in ids:
                paths.append(
                    self.export_call(
                        contact_id,
                        output_dir,
                        include_recording=include_recording,
                        include_transcript=include_transcript,
                        include_evaluation=include_evaluation,
                        media_format=media_format,
                        is_root_recording=is_root_recording,
                        wait_timeout=wait_timeout,
                        poll_interval=poll_interval,
                    )
                )
            start += len(page)
        raise ResponseError(
            "Search reached max_pages; completed exports remain, but more calls may exist"
        )

    def export_contact(self, contact_id: int | str, destination: str | Path) -> Path:
        """Save contact details as JSON; returns the saved Path. No overwrites."""
        self._recordings()
        target = destination_path(destination)
        return write_json(self.get_contact(contact_id), target)

    def export_metadata(self, contact_id: int | str, destination: str | Path) -> Path:
        """Save resolved metadata as JSON (null if absent); returns the saved Path."""
        self._recordings()
        target = destination_path(destination)
        return write_json(self.get_metadata(contact_id), target)

    def export_transcript(
        self, contact_id: int | str, destination: str | Path, *, is_root_recording: bool = False
    ) -> Path:
        """Save transcript JSON in one call; returns the saved Path. No overwrites."""
        self._recordings()
        target = destination_path(destination)
        return write_json(
            self.get_transcript(contact_id, is_root_recording=is_root_recording), target
        )

    def export_evaluation(self, contact_id: int | str, destination: str | Path) -> Path:
        """Save QA summary/form as JSON; not completed question-level answers."""
        self._recordings()
        target = destination_path(destination)
        return write_json(self.get_evaluation(contact_id), target)

    def _operation(self, path: str, names: dict, payload: dict | None, kwargs: dict) -> Any:
        if payload is not None and kwargs:
            raise TypeError("Use a payload dictionary or keyword arguments, not both")
        if payload is not None and not isinstance(payload, dict):
            raise TypeError("payload must be a dictionary")
        if kwargs.keys() - names.keys():
            raise TypeError("Unknown keyword argument; see docs/endpoints.md for accepted fields")
        if payload is not None:
            return self.request(path, payload)
        values = {names[key]: value for key, value in kwargs.items()}
        values = normalize(values, self._wfm_requests[path], self._wfm_schemas)
        return self.request(path, values)

    def request(self, path: str, payload: dict[str, Any] | None = None) -> Any:
        """POST JSON to a relative WFM query/command path, preserving the response.

        This escape hatch supports newly added endpoints without a package update.
        Use original API field names in payload, including nested objects.
        """
        if self._classic is not None:
            raise ValueError(
                "WFM methods require a separate CalabrioClient(base_url=..., token=...)"
            )
        if not isinstance(path, str) or not re.fullmatch(
            r"/?(?:query|command)/[A-Za-z0-9_-]+(?:/[A-Za-z0-9_-]+)*", path
        ):
            raise ValueError("path must be a relative query/ or command/ API path")
        if payload is not None and not isinstance(payload, dict):
            raise TypeError("payload must be a dictionary")
        body = json.dumps(
            {} if payload is None else payload, default=_json_default, allow_nan=False
        )
        try:
            response = self._http.post(
                path.lstrip("/"), content=body, headers={"Content-Type": "application/json"}
            )
        except httpx.RequestError:
            raise TransportError(
                "Calabrio request could not complete; check connectivity."
            ) from None
        return decode_json(response)
