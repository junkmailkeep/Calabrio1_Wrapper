"""Errors deliberately omit URLs, credentials and server response bodies."""


class CalabrioError(Exception):
    """Base error for this client."""


class TransportError(CalabrioError):
    """The request could not complete; a command may still have been applied."""


class ResponseError(CalabrioError):
    """The server returned an unexpected response."""


class APIError(CalabrioError):
    def __init__(self, status_code: int):
        self.status_code = status_code
        super().__init__(f"Calabrio API request failed (HTTP {status_code}).")


class AuthenticationError(APIError):
    """Credentials were rejected (401)."""


class PermissionDeniedError(APIError):
    """The token lacks the required access (403)."""


class RateLimitError(APIError):
    """The server rate limit was reached (429)."""


class OperationError(CalabrioError):
    """A successful HTTP response contained nonempty API Errors."""


class ExportTimeoutError(CalabrioError):
    """An export did not become available or finish within its polling budget."""
