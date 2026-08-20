"""Canvas payload validation shared by scripts and MCP tools."""

from __future__ import annotations

import json
import re
from typing import Any


MAX_CANVAS_DATA_JSON_BYTES = 64 * 1024
MAX_CANVAS_WINDOW_DATA_JSON_BYTES = 128 * 1024
MAX_CANVAS_LAYOUT_FULL_JSON_BYTES = 8 * 1024
MAX_CANVAS_WINDOW_NODES = 80
MAX_CANVAS_WINDOW_DEPTH = 16
MAX_CANVAS_STRING_LENGTH = 4000

ALLOWED_ELEMENT_TYPES = {"div", "span", "img"}
BLOCKED_PROP_KEYS = {"dangerouslySetInnerHTML", "ref", "srcSet"}
UNSAFE_KEYS = {"__proto__", "constructor", "prototype"}
RESERVED_DATA_KEYS = {
    "type",
    "key",
    "windowData",
    "layoutFull",
    "taskAlias",
    "link",
    "border",
    "__proto__",
    "constructor",
    "prototype",
}


class CanvasValidator:
    """Reusable Canvas payload validator for scripts and MCP tools."""

    def validate(self, payload: Any) -> dict[str, Any]:
        return validate_canvas_payload(payload)


def compact_json_bytes(value: Any) -> int:
    return len(
        json.dumps(value, separators=(",", ":"), ensure_ascii=False).encode("utf-8")
    )


def validate_template_string(value: str) -> None:
    if len(value) > MAX_CANVAS_STRING_LENGTH:
        raise ValueError(
            f"Canvas string is too long: max {MAX_CANVAS_STRING_LENGTH} characters"
        )

    contains_template_token = "{{" in value or "}}" in value
    matched_template_token = False
    for match in re.finditer(r"{{{?([^{}]+)}}}?", value):
        matched_template_token = True
        expression = (match.group(1) or "").strip()
        if not re.match(r"^get\s+inputData(?:\s|$)", expression) or "(" in expression:
            helper = expression.split()[0] if expression.split() else expression
            raise ValueError(
                "Unsupported Canvas template helper: "
                f"{helper}. Use simple {{get inputData \"path\" default=\"-\"}} reads only."
            )

    if contains_template_token and not matched_template_token:
        raise ValueError("Malformed Canvas template expression")


def validate_plain_json_value(value: Any, depth: int, path: str) -> None:
    if depth > MAX_CANVAS_WINDOW_DEPTH:
        raise ValueError(
            f"Canvas windowData is too deeply nested at {path}: "
            f"max depth {MAX_CANVAS_WINDOW_DEPTH}"
        )

    if value is None or isinstance(value, (int, float, bool)):
        return
    if isinstance(value, str):
        validate_template_string(value)
        return
    if isinstance(value, list):
        for index, item in enumerate(value):
            validate_plain_json_value(item, depth + 1, f"{path}.{index}")
        return
    if isinstance(value, dict):
        for key, nested_value in value.items():
            if key in UNSAFE_KEYS:
                raise ValueError(f"Unsafe key in Canvas payload at {path}: {key}")
            validate_plain_json_value(nested_value, depth + 1, f"{path}.{key}")
        return
    raise ValueError(f"Invalid JSON value in Canvas payload at {path}")


def validate_canvas_element(
    node: Any, context: dict[str, int], depth: int, path: str
) -> None:
    if depth > MAX_CANVAS_WINDOW_DEPTH:
        raise ValueError(
            f"Canvas windowData is too deeply nested at {path}: "
            f"max depth {MAX_CANVAS_WINDOW_DEPTH}"
        )
    if isinstance(node, str):
        validate_template_string(node)
        return
    if not isinstance(node, dict):
        raise ValueError(f"Canvas element at {path} must be an object or string")

    context["count"] += 1
    if context["count"] > MAX_CANVAS_WINDOW_NODES:
        raise ValueError(
            f"Canvas windowData has too many elements: max {MAX_CANVAS_WINDOW_NODES}"
        )

    element_type = node.get("type")
    if element_type not in ALLOWED_ELEMENT_TYPES:
        raise ValueError(
            f"Unsupported Canvas element type at {path}: {element_type}. "
            "Allowed types are div, span, and img."
        )

    props = node.get("props", {})
    if props is None:
        props = {}
    if not isinstance(props, dict):
        raise ValueError(f"Canvas props at {path}.props must be an object")

    for key, value in props.items():
        if key in UNSAFE_KEYS or key in BLOCKED_PROP_KEYS:
            raise ValueError(f"Unsupported Canvas prop at {path}.props: {key}")
        if key == "style":
            if not isinstance(value, dict):
                raise ValueError(f"Canvas style at {path}.props.style must be an object")
            for style_key, style_value in value.items():
                if style_key in UNSAFE_KEYS:
                    raise ValueError(
                        f"Unsafe Canvas style key at {path}.props.style: {style_key}"
                    )
                if not isinstance(style_value, (str, int, float)):
                    raise ValueError(
                        f"Canvas style value at {path}.props.style.{style_key} "
                        "must be a string or number"
                    )
            continue
        if key == "children":
            if isinstance(value, list):
                for index, child in enumerate(value):
                    validate_canvas_element(
                        child, context, depth + 1, f"{path}.props.children.{index}"
                    )
            elif isinstance(value, dict):
                validate_canvas_element(value, context, depth + 1, f"{path}.props.children")
            elif isinstance(value, str):
                validate_template_string(value)
            elif value is not None:
                raise ValueError(
                    f"Canvas children at {path}.props.children must be a string, "
                    "element object, or element array"
                )
            continue
        validate_plain_json_value(value, depth + 1, f"{path}.props.{key}")


def validate_layout_full(layout_full: Any) -> None:
    if layout_full is None:
        return
    if not isinstance(layout_full, dict):
        raise ValueError("layoutFull must be an object")
    if compact_json_bytes(layout_full) > MAX_CANVAS_LAYOUT_FULL_JSON_BYTES:
        raise ValueError("layoutFull is too large: max 8 KB")

    tw = layout_full.get("tw")
    if tw is not None and not isinstance(tw, str):
        raise ValueError("layoutFull.tw must be a string")

    style = layout_full.get("style")
    if style is not None:
        if not isinstance(style, dict):
            raise ValueError("layoutFull.style must be an object")
        for key, value in style.items():
            if key in UNSAFE_KEYS or not isinstance(value, (str, int, float)):
                raise ValueError(
                    "layoutFull.style values must be strings or numbers and cannot use unsafe keys"
                )


def validate_canvas_payload(payload: Any) -> dict[str, Any]:
    """Validate a Canvas payload and return safe size/node metrics."""

    if not isinstance(payload, dict):
        raise ValueError("Canvas payload must be a JSON object")

    data = payload.get("data", {})
    if data is None:
        data = {}
    if not isinstance(data, dict):
        raise ValueError("data must be an object")
    data_bytes = compact_json_bytes(data)
    if data_bytes > MAX_CANVAS_DATA_JSON_BYTES:
        raise ValueError("data is too large: max 64 KB")
    for key in data.keys():
        if key in RESERVED_DATA_KEYS:
            raise ValueError(f"data uses a reserved Canvas API key: {key}")

    window_data = payload.get("windowData")
    if not isinstance(window_data, dict):
        raise ValueError("windowData is required and must be an object")
    window_data_bytes = compact_json_bytes(window_data)
    if window_data_bytes > MAX_CANVAS_WINDOW_DATA_JSON_BYTES:
        raise ValueError("windowData is too large: max 128 KB")

    default_layer = window_data.get("default")
    if not isinstance(default_layer, list):
        raise ValueError("windowData.default must be an array")

    context = {"count": 0}
    for index, node in enumerate(default_layer):
        validate_canvas_element(node, context, 1, f"windowData.default.{index}")

    validate_layout_full(payload.get("layoutFull"))

    border = payload.get("border")
    if border is not None and border not in (0, 1):
        raise ValueError("border must be 0 or 1")

    return {
        "valid": True,
        "nodeCount": context["count"],
        "dataBytes": data_bytes,
        "windowDataBytes": window_data_bytes,
    }
