"""Independent Python wrapper for Calabrio ONE recordings, QM and WFM."""

from ._http import InsecureTLSWarning
from .classic import ClassicClient
from .client import CalabrioClient
from .exceptions import (
    APIError,
    AuthenticationError,
    CalabrioError,
    ExportTimeoutError,
    OperationError,
    PermissionDeniedError,
    RateLimitError,
    ResponseError,
    TransportError,
)

__all__ = [
    "CalabrioClient",
    "InsecureTLSWarning",
    "CalabrioError",
    "APIError",
    "AuthenticationError",
    "PermissionDeniedError",
    "RateLimitError",
    "ResponseError",
    "TransportError",
    "OperationError",
    "ClassicClient",
    "ExportTimeoutError",
]
__version__ = "0.1.0a1"
