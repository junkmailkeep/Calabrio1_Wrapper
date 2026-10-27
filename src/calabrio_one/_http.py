"""Shared connection validation and sanitized API errors."""

from __future__ import annotations

import math
import ssl
import warnings
from typing import Any
from urllib.parse import SplitResult, urlsplit

import httpx

from .exceptions import (
    APIError,
    AuthenticationError,
    OperationError,
    PermissionDeniedError,
    RateLimitError,
    ResponseError,
)


class InsecureTLSWarning(UserWarning):
    """Certificate verification was explicitly disabled for this client."""


def positive_seconds(value: float) -> None:
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise ValueError("Duration must be a positive finite number of seconds")
    try:
        valid = math.isfinite(value) and value > 0
    except OverflowError:
        valid = False
    if not valid:
        raise ValueError("Duration must be a positive finite number of seconds")


def https_url(value: str) -> SplitResult:
    try:
        if not isinstance(value, str):
            raise ValueError
        url = urlsplit(value)
        valid = (
            url.scheme == "https"
            and url.hostname
            and url.username is None
            and url.password is None
            and not url.query
            and not url.fragment
            and url.port != 0
            and not any(c.isspace() or ord(c) < 32 or ord(c) == 127 for c in value)
        )
    except (ValueError, TypeError):
        valid = False
    if not valid:
        raise ValueError("base_url must be an HTTPS URL without credentials, query or fragment")
    return url


def verify_tls(verify: ssl.SSLContext | bool) -> None:
    if verify is True:
        return
    if verify is False:
        warnings.warn(
            "TLS certificate verification is disabled. Server identity is not checked; "
            "credentials and call data could be intercepted. Prefer a trusted CA SSLContext.",
            InsecureTLSWarning,
            stacklevel=3,
        )
        return
    if not isinstance(verify, ssl.SSLContext):
        raise ValueError("verify must be True, False, or a verified SSLContext")
    if verify.verify_mode != ssl.CERT_REQUIRED or not verify.check_hostname:
        raise ValueError("SSLContext must verify certificates and hostnames")


def check_status(response: httpx.Response) -> None:
    if not 200 <= response.status_code < 300:
        error = {401: AuthenticationError, 403: PermissionDeniedError, 429: RateLimitError}.get(
            response.status_code,
            APIError,
        )
        raise error(response.status_code)


def decode_json(response: httpx.Response) -> Any:
    check_status(response)
    if response.status_code == 204:
        return None
    try:
        value = response.json()
    except ValueError:
        raise ResponseError("Calabrio returned an invalid JSON response.") from None
    if isinstance(value, dict) and (value.get("errorMessage") or value.get("Errors")):
        raise OperationError("Calabrio reported an operation error.")
    return value
