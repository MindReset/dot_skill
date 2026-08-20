#!/usr/bin/env python3
"""Send text content to a Dot. device."""

import argparse
import base64

from _runtime import DotClient, run


def send_text(
    device_id,
    title=None,
    message=None,
    signature=None,
    icon=None,
    link=None,
    refresh_now=True,
    task_key=None,
    task_alias=None,
):
    data = {"refreshNow": refresh_now}
    for key, value in {
        "title": title,
        "message": message,
        "signature": signature,
        "icon": icon,
        "link": link,
        "taskKey": task_key,
        "taskAlias": task_alias,
    }.items():
        if value is not None:
            data[key] = value
    result = DotClient.from_env().send_text(device_id, data)
    if isinstance(result, dict):
        print(f"Success: {result.get('message', 'text sent')}")
    return result


def main():
    parser = argparse.ArgumentParser(description="Send text content to a Dot. device")
    parser.add_argument("--device-id", "-d", required=True)
    parser.add_argument("--title", "-t")
    parser.add_argument("--message", "-m")
    parser.add_argument("--signature", "-s")
    parser.add_argument("--icon", help="Path to PNG icon file")
    parser.add_argument("--link", "-l")
    parser.add_argument("--refresh-now", action="store_true", default=True)
    parser.add_argument("--no-refresh-now", action="store_false", dest="refresh_now")
    parser.add_argument("--task-key")
    parser.add_argument("--task-alias")
    args = parser.parse_args()

    icon_data = None
    if args.icon:
        with open(args.icon, "rb") as icon_file:
            icon_data = base64.b64encode(icon_file.read()).decode("utf-8")

    run(
        lambda: send_text(
            device_id=args.device_id,
            title=args.title,
            message=args.message,
            signature=args.signature,
            icon=icon_data,
            link=args.link,
            refresh_now=args.refresh_now,
            task_key=args.task_key,
            task_alias=args.task_alias,
        )
    )


if __name__ == "__main__":
    main()
