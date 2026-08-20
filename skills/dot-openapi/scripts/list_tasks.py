#!/usr/bin/env python3
"""List loop or fixed content tasks for a Dot. device."""

import argparse
import json

from _runtime import DotClient, run


def list_tasks(device_id, task_type="loop"):
    return DotClient.from_env().list_tasks(device_id, task_type)


def format_tasks(tasks):
    if not tasks:
        print("No tasks found.")
        return
    print(f"\nFound {len(tasks)} task(s):\n")
    for index, task in enumerate(tasks, 1):
        task_type = task.get("type", "N/A")
        print(f"[{index}] Type: {task_type}")
        print(f"    Key: {task.get('key') or 'N/A'}")
        if task_type == "TEXT_API":
            print(f"    Title: {task.get('title', 'N/A')}")
            print(f"    Message: {task.get('message', 'N/A')}")
            if task.get("signature"):
                print(f"    Signature: {task['signature']}")
        elif task_type == "IMAGE_API":
            print(f"    Border: {task.get('border', 'N/A')}")
            print(f"    Dither Type: {task.get('ditherType', 'N/A')}")
            print(f"    Dither Kernel: {task.get('ditherKernel', 'N/A')}")
        print(f"    Refresh Now: {task.get('refreshNow', False)}\n")


def main():
    parser = argparse.ArgumentParser(description="List content tasks for a Dot. device")
    parser.add_argument("--device-id", "-d", required=True)
    parser.add_argument("--type", "-t", choices=["loop", "fixed"], default="loop")
    parser.add_argument("--json", "-j", action="store_true", help="Output raw JSON")
    args = parser.parse_args()
    result = run(lambda: list_tasks(args.device_id, args.type))
    if args.json:
        print(json.dumps(result, indent=2, ensure_ascii=False))
    else:
        format_tasks(result)


if __name__ == "__main__":
    main()
