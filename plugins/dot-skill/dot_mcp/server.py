"""Local stdio MCP server for Dot. device operations."""

from __future__ import annotations

from typing import Any, Literal

try:
    from mcp.server.fastmcp import FastMCP
except ImportError:  # MCP Python SDK 2.x renamed FastMCP to MCPServer.
    from mcp.server.mcpserver import MCPServer as FastMCP

try:
    from mcp.types import ToolAnnotations
except ImportError:  # MCP Python SDK 2.x exposes protocol types in mcp_types.
    from mcp_types import ToolAnnotations

from .canvas import CanvasValidator
from .client import DotClient
from .models import CanvasContentInput, DeviceSettingsInput, ImageContentInput, TextContentInput


mcp = FastMCP("dot-skill")
CANVAS_VALIDATOR = CanvasValidator()

READ_ANNOTATIONS = ToolAnnotations(
    readOnlyHint=True,
    destructiveHint=False,
    idempotentHint=True,
    openWorldHint=True,
)
WRITE_ANNOTATIONS = ToolAnnotations(
    readOnlyHint=False,
    destructiveHint=False,
    idempotentHint=False,
    openWorldHint=True,
)


def _client() -> DotClient:
    return DotClient.from_env()


@mcp.tool(
    name="dot_list_devices",
    description="[read-only] List Dot. devices associated with the authenticated account.",
    annotations=READ_ANNOTATIONS,
)
def dot_list_devices() -> Any:
    return _client().list_devices()


@mcp.tool(
    name="dot_get_device_status",
    description="[read-only] Read battery, Wi-Fi, display, and render status for one Dot. device.",
    annotations=READ_ANNOTATIONS,
)
def dot_get_device_status(device_id: str) -> Any:
    return _client().get_device_status(device_id)


@mcp.tool(
    name="dot_get_device_settings",
    description="[read-only] Read editable settings for one Dot. device.",
    annotations=READ_ANNOTATIONS,
)
def dot_get_device_settings(device_id: str) -> Any:
    return _client().get_device_settings(device_id)


@mcp.tool(
    name="dot_list_timezones",
    description="[read-only] List timezone keys accepted by Dot. device settings.",
    annotations=READ_ANNOTATIONS,
)
def dot_list_timezones() -> Any:
    return _client().list_timezones()


@mcp.tool(
    name="dot_list_tasks",
    description="[read-only] List loop or fixed content tasks for one Dot. device.",
    annotations=READ_ANNOTATIONS,
)
def dot_list_tasks(
    device_id: str, task_type: Literal["loop", "fixed"] = "loop"
) -> Any:
    return _client().list_tasks(device_id, task_type)


@mcp.tool(
    name="dot_update_device_settings",
    description="[write; device settings change] Update one or more settings for a Dot. device. The request is sent once without automatic retries.",
    annotations=WRITE_ANNOTATIONS,
)
def dot_update_device_settings(
    device_id: str, settings: DeviceSettingsInput
) -> Any:
    payload = settings.model_dump(exclude_unset=True, by_alias=True)
    return _client().update_device_settings(device_id, payload)


@mcp.tool(
    name="dot_switch_next_content",
    description="[write; display change] Switch a Dot. device to its next content item. The request is sent once without automatic retries.",
    annotations=WRITE_ANNOTATIONS,
)
def dot_switch_next_content(device_id: str) -> Any:
    return _client().switch_next_content(device_id)


@mcp.tool(
    name="dot_send_text",
    description="[write; display change] Send text content to a Dot. device that has a matching Text API item. The request is sent once without automatic retries.",
    annotations=WRITE_ANNOTATIONS,
)
def dot_send_text(device_id: str, content: TextContentInput) -> Any:
    payload = content.model_dump(exclude_unset=True, by_alias=True)
    return _client().send_text(device_id, payload)


@mcp.tool(
    name="dot_send_image",
    description="[write; display change] Send image content to a Dot. device that has a matching Image API item. The request is sent once without automatic retries.",
    annotations=WRITE_ANNOTATIONS,
)
def dot_send_image(device_id: str, content: ImageContentInput) -> Any:
    payload = content.model_dump(exclude_unset=True, by_alias=True)
    return _client().send_image(device_id, payload)


@mcp.tool(
    name="dot_validate_canvas",
    description="[read-only] Validate a Canvas payload locally without contacting Dot. or changing a device.",
    annotations=READ_ANNOTATIONS,
)
def dot_validate_canvas(payload: CanvasContentInput) -> dict[str, Any]:
    return CANVAS_VALIDATOR.validate(payload.model_dump(exclude_unset=True, by_alias=True))


@mcp.tool(
    name="dot_send_canvas",
    description="[write; display change] Validate and send a Canvas payload to a Dot. device that has a matching Canvas API item. The request is sent once without automatic retries.",
    annotations=WRITE_ANNOTATIONS,
)
def dot_send_canvas(device_id: str, payload: CanvasContentInput) -> Any:
    payload_dict = payload.model_dump(exclude_unset=True, by_alias=True)
    CANVAS_VALIDATOR.validate(payload_dict)
    return _client().send_canvas(device_id, payload_dict)


def run() -> None:
    """Run the server over local stdio."""

    mcp.run(transport="stdio")
