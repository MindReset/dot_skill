#!/usr/bin/env python3
"""Validate and send a Canvas API payload to a Dot. device."""

import argparse
import json
import sys

from _runtime import DotClient, run
from dot_mcp.canvas import (
    compact_json_bytes,
    validate_canvas_element,
    validate_canvas_payload,
    validate_layout_full,
    validate_plain_json_value,
    validate_template_string,
)


def load_json_file(path):
    try:
        with open(path, "r", encoding="utf-8") as json_file:
            return json.load(json_file)
    except json.JSONDecodeError as error:
        raise ValueError(f"{path} is not valid JSON: {error}") from error


def build_payload(args):
    if args.payload:
        payload = load_json_file(args.payload)
    else:
        if not args.window_data:
            raise ValueError("Either --payload or --window-data is required")
        payload = {"windowData": load_json_file(args.window_data)}
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
    result = DotClient.from_env().send_canvas(device_id, payload)
    if isinstance(result, dict):
        print(f"Success: {result.get('message', 'canvas sent')}")
    return result


def main():
    parser = argparse.ArgumentParser(description="Send Canvas content to a Dot. device")
    parser.add_argument("--device-id", "-d", required=True)
    parser.add_argument("--payload")
    parser.add_argument("--data")
    parser.add_argument("--window-data")
    parser.add_argument("--layout-full")
    parser.add_argument("--link", "-l")
    parser.add_argument("--border", "-b", type=int, choices=[0, 1])
    parser.add_argument("--refresh-now", action="store_true", default=None)
    parser.add_argument("--no-refresh-now", action="store_false", dest="refresh_now")
    parser.add_argument("--task-key")
    parser.add_argument("--task-alias")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    try:
        payload = build_payload(args)
        validate_canvas_payload(payload)
    except ValueError as error:
        print(f"Error: {error}", file=sys.stderr)
        raise SystemExit(1) from error

    if args.dry_run:
        print(json.dumps(payload, indent=2, ensure_ascii=False))
        return
    run(lambda: send_canvas(args.device_id, payload))


if __name__ == "__main__":
    main()
