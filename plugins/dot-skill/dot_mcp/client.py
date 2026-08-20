"""Shared HTTP client for Dot. OpenAPI operations.

The client deliberately performs one HTTP request per call. In particular, write
requests are never retried automatically because a successful write may already
have changed the device state even when a response is lost.
"""

from __future__ import annotations

import json
import os
import urllib.error
import urllib.parse
import urllib.request
from collections.abc import Callable, Mapping
from typing import Any


BASE_URL = "https://dot.mindreset.tech"
DEFAULT_TIMEOUT_SECONDS = 30


class DotError(Exception):
    """Base error exposed by the shared runtime."""


class DotAuthError(DotError):
    """Raised when the local API key is not available."""


class DotNetworkError(DotError):
    """Raised when the request could not reach the Dot. service."""


class DotResponseError(DotError):
    """Raised when Dot. returns a response that is not valid JSON."""


class DotAPIError(DotError):
    """Raised for an HTTP error returned by Dot."""

    def __init__(
        self,
        status_code: int,
        response_body: str,
        *,
        method: str,
        path: str,
    ) -> None:
        self.status_code = status_code
        self.response_body = response_body
        self.method = method
        self.path = path
        super().__init__(self._format_message())

    def _format_message(self) -> str:
        detail = ""
        try:
            parsed = json.loads(self.response_body)
        except (TypeError, json.JSONDecodeError):
            parsed = None

        if isinstance(parsed, Mapping):
            message = parsed.get("message")
            if isinstance(message, str) and message:
                detail = f": {message}"
        elif self.response_body:
            detail = f": {self.response_body[:500]}"

        return f"Dot API request failed with HTTP {self.status_code}{detail}"


def get_api_key() -> str:
    """Read the only supported credential source: ``DOT_API_KEY``."""

    api_key = os.environ.get("DOT_API_KEY")
    if not api_key:
        raise DotAuthError(
            "DOT_API_KEY environment variable is not set. "
            "Set it before using Dot tools."
        )
    return api_key


class DotClient:
    """Small, dependency-free client for the Dot. OpenAPI contract."""

    def __init__(
        self,
        api_key: str,
        *,
        base_url: str = BASE_URL,
        timeout: float = DEFAULT_TIMEOUT_SECONDS,
        opener: Callable[..., Any] | None = None,
    ) -> None:
        if not api_key:
            raise DotAuthError("A Dot. API key is required")
        self.api_key = api_key
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout
        self._opener = opener or urllib.request.urlopen

    @classmethod
    def from_env(
        cls,
        *,
        base_url: str = BASE_URL,
        timeout: float = DEFAULT_TIMEOUT_SECONDS,
        opener: Callable[..., Any] | None = None,
    ) -> "DotClient":
        return cls(
            get_api_key(),
            base_url=base_url,
            timeout=timeout,
            opener=opener,
        )

    @staticmethod
    def _device_path(device_id: str, suffix: str) -> str:
        if not isinstance(device_id, str) or not device_id.strip():
            raise ValueError("device_id must be a non-empty string")
        encoded_device_id = urllib.parse.quote(device_id, safe="")
        return f"/api/authV2/open/device/{encoded_device_id}/{suffix.lstrip('/')}"

    def _request(
        self,
        method: str,
        path: str,
        payload: Mapping[str, Any] | None = None,
    ) -> Any:
        url = f"{self.base_url}{path}"
        headers = {
            "Accept": "application/json",
            "Authorization": f"Bearer {self.api_key}",
        }
        data = None
        if payload is not None:
            headers["Content-Type"] = "application/json"
            data = json.dumps(payload, ensure_ascii=False).encode("utf-8")

        request = urllib.request.Request(
            url,
            data=data,
            headers=headers,
            method=method,
        )

        try:
            response = self._opener(request, timeout=self.timeout)
        except urllib.error.HTTPError as error:
            response_body = error.read().decode("utf-8", errors="replace")
            raise DotAPIError(
                error.code,
                response_body,
                method=method,
                path=path,
            ) from error
        except (urllib.error.URLError, TimeoutError, OSError) as error:
            raise DotNetworkError(
                f"Dot API request could not reach the service: {error}"
            ) from error

        try:
            raw_body = response.read()
        finally:
            close = getattr(response, "close", None)
            if callable(close):
                close()

        if not raw_body:
            return {}
        try:
            return json.loads(raw_body.decode("utf-8"))
        except (UnicodeDecodeError, json.JSONDecodeError) as error:
            raise DotResponseError(
                f"Dot API returned an invalid JSON response for {method} {path}"
            ) from error

    def get(self, path: str) -> Any:
        return self._request("GET", path)

    def post(self, path: str, payload: Mapping[str, Any] | None = None) -> Any:
        return self._request("POST", path, payload or {})

    def list_devices(self) -> Any:
        return self.get("/api/authV2/open/devices")

    def list_timezones(self) -> Any:
        return self.get("/api/authV2/open/timezones")

    def get_device_status(self, device_id: str) -> Any:
        return self.get(self._device_path(device_id, "status"))

    def get_device_settings(self, device_id: str) -> Any:
        return self.get(self._device_path(device_id, "settings"))

    def list_tasks(self, device_id: str, task_type: str = "loop") -> Any:
        if task_type not in {"loop", "fixed"}:
            raise ValueError("task_type must be 'loop' or 'fixed'")
        return self.get(self._device_path(device_id, f"{task_type}/list"))

    def update_device_settings(
        self, device_id: str, payload: Mapping[str, Any]
    ) -> Any:
        return self.post(self._device_path(device_id, "settings"), payload)

    def switch_next_content(self, device_id: str) -> Any:
        return self.post(self._device_path(device_id, "next"), {})

    def send_text(self, device_id: str, payload: Mapping[str, Any]) -> Any:
        return self.post(self._device_path(device_id, "text"), payload)

    def send_image(self, device_id: str, payload: Mapping[str, Any]) -> Any:
        return self.post(self._device_path(device_id, "image"), payload)

    def send_canvas(self, device_id: str, payload: Mapping[str, Any]) -> Any:
        return self.post(self._device_path(device_id, "canvas"), payload)
