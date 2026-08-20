"""Shared Dot. API client and local MCP server runtime."""

from .canvas import CanvasValidator, validate_canvas_payload
from .client import (
    BASE_URL,
    DotAPIError,
    DotAuthError,
    DotClient,
    DotError,
    DotNetworkError,
    DotResponseError,
    get_api_key,
)

__all__ = [
    "BASE_URL",
    "CanvasValidator",
    "DotAPIError",
    "DotAuthError",
    "DotClient",
    "DotError",
    "DotNetworkError",
    "DotResponseError",
    "get_api_key",
    "validate_canvas_payload",
]
