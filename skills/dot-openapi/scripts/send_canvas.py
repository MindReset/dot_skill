#!/usr/bin/env python3
"""
Send Canvas API content to a Dot. device.

Usage:
    python send_canvas.py --device-id ABCD1234ABCD --payload canvas_payload.json
    python send_canvas.py --device-id ABCD1234ABCD --data data.json --window-data window_data.json
    python send_canvas.py --device-id ABCD1234ABCD --payload canvas_payload.json --task-alias "Morning Dashboard"
    python send_canvas.py --device-id ABCD1234ABCD --payload canvas_payload.json --dry-run

Environment Variables:
    DOT_API_KEY: Your Dot. API key (required unless --dry-run is used)
"""

import argparse
import json
import os
import re
import sys
import urllib.error
import urllib.request


BASE_URL = "https://dot.mindreset.tech"

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


def compact_json_bytes(value):
    return len(json.dumps(value, separators=(",", ":"), ensure_ascii=False).encode("utf-8"))


def load_json_file(path):
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except json.JSONDecodeError as error:
        raise ValueError(f"{path} is not valid JSON: {error}") from error


def get_api_key():
    api_key = os.environ.get("DOT_API_KEY")
    if not api_key:
        print("Error: DOT_API_KEY environment variable not set", file=sys.stderr)
        print("Please set it with: export DOT_API_KEY='dot_app_<your_key>'", file=sys.stderr)
        sys.exit(1)
    return api_key


def validate_template_string(value):
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


def validate_plain_json_value(value, depth, path):
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


def validate_canvas_element(node, context, depth, path):
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
                    validate_canvas_element(child, context, depth + 1, f"{path}.children.{index}")
            elif isinstance(value, dict):
                validate_canvas_element(value, context, depth + 1, f"{path}.children")
            elif isinstance(value, str):
                validate_template_string(value)
            elif value is not None:
                raise ValueError(
                    f"Canvas children at {path}.props.children must be a string, "
                    "element object, or element array"
                )
            continue

        validate_plain_json_value(value, depth + 1, f"{path}.props.{key}")


def validate_layout_full(layout_full):
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


def validate_canvas_payload(payload):
    if not isinstance(payload, dict):
        raise ValueError("Canvas payload must be a JSON object")

    data = payload.get("data", {})
    if data is None:
        data = {}
    if not isinstance(data, dict):
        raise ValueError("data must be an object")
    if compact_json_bytes(data) > MAX_CANVAS_DATA_JSON_BYTES:
        raise ValueError("data is too large: max 64 KB")
    for key in data.keys():
        if key in RESERVED_DATA_KEYS:
            raise ValueError(f"data uses a reserved Canvas API key: {key}")

    window_data = payload.get("windowData")
    if not isinstance(window_data, dict):
        raise ValueError("windowData is required and must be an object")
    if compact_json_bytes(window_data) > MAX_CANVAS_WINDOW_DATA_JSON_BYTES:
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


def build_payload(args):
    if args.payload:
        payload = load_json_file(args.payload)
    else:
        if not args.window_data:
            raise ValueError("Either --payload or --window-data is required")
        payload = {
            "windowData": load_json_file(args.window_data),
        }
        if args.data:
            payload["data"] = load_json_file(args.data)
        if args.layout_full:
            payload["layoutFull"] = load_json_file(args.layout_full)

    if args.link is not None:
        payload["link"] = args.link
    if args.border is not None:
        payload["border"] = args.border
    if args.task_key is not None:
        payload["taskKey"] = args.task_key
    if args.task_alias is not None:
        payload["taskAlias"] = args.task_alias
    if args.refresh_now is None:
        payload.setdefault("refreshNow", True)
    else:
        payload["refreshNow"] = args.refresh_now

    return payload


def send_canvas(device_id, payload):
    api_key = get_api_key()
    url = f"{BASE_URL}/api/authV2/open/device/{device_id}/canvas"

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }

    req = urllib.request.Request(
        url,
        data=json.dumps(payload, ensure_ascii=False).encode("utf-8"),
        headers=headers,
        method="POST",
    )

    try:
        with urllib.request.urlopen(req) as response:
            result = json.loads(response.read().decode("utf-8"))
            print(f"Success: {result['message']}")
            return result
    except urllib.error.HTTPError as e:
        error_body = e.read().decode("utf-8")
        print(f"Error: HTTP {e.code} - {error_body}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


def main():
    parser = argparse.ArgumentParser(
        description="Send Canvas API content to a Dot. device"
    )
    parser.add_argument(
        "--device-id",
        "-d",
        required=True,
        help="Device serial number (e.g., ABCD1234ABCD)",
    )
    parser.add_argument(
        "--payload",
        help="Path to full Canvas API JSON payload",
    )
    parser.add_argument(
        "--data",
        help="Path to data JSON file used by the Canvas layout",
    )
    parser.add_argument(
        "--window-data",
        help="Path to windowData JSON file",
    )
    parser.add_argument(
        "--layout-full",
        help="Path to layoutFull JSON file",
    )
    parser.add_argument(
        "--link",
        "-l",
        help="Tap-to-open link URL",
    )
    parser.add_argument(
        "--border",
        "-b",
        type=int,
        choices=[0, 1],
        help="Screen border color: 0=white, 1=black",
    )
    parser.add_argument(
        "--refresh-now",
        action="store_true",
        default=None,
        help="Display immediately (default: true)",
    )
    parser.add_argument(
        "--no-refresh-now",
        action="store_false",
        dest="refresh_now",
        help="Queue without displaying immediately",
    )
    parser.add_argument(
        "--task-key",
        help="Task identifier for multiple Canvas API contents",
    )
    parser.add_argument(
        "--task-alias",
        help="Human-readable task name shown in the device task list",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Validate and print the payload without sending it",
    )

    args = parser.parse_args()

    try:
        payload = build_payload(args)
        validate_canvas_payload(payload)
    except ValueError as error:
        print(f"Error: {error}", file=sys.stderr)
        sys.exit(1)

    if args.dry_run:
        print(json.dumps(payload, indent=2, ensure_ascii=False))
        return

    send_canvas(args.device_id, payload)


if __name__ == "__main__":
    main()
