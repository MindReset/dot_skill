#!/usr/bin/env python3
"""
List tasks/content for a Dot. device.

Usage:
    python list_tasks.py --device-id ABCD1234ABCD --type loop
    python list_tasks.py --device-id ABCD1234ABCD --type fixed

Environment Variables:
    DOT_API_KEY: Your Dot. API key (required)
"""

import argparse
import os
import sys
import urllib.request
import urllib.error
import json


BASE_URL = "https://dot.mindreset.tech"


def get_api_key():
    """Get API key from environment variable."""
    api_key = os.environ.get("DOT_API_KEY")
    if not api_key:
        print("Error: DOT_API_KEY environment variable not set", file=sys.stderr)
        print("Please set it with: export DOT_API_KEY='dot_app_<your_key>'", file=sys.stderr)
        sys.exit(1)
    return api_key


def list_tasks(device_id, task_type="loop"):
    """List tasks for a device."""
    api_key = get_api_key()
    
    url = f"{BASE_URL}/api/authV2/open/device/{device_id}/{task_type}/list"
    
    headers = {
        "Authorization": f"Bearer {api_key}"
    }
    
    req = urllib.request.Request(url, headers=headers)
    
    try:
        with urllib.request.urlopen(req) as response:
            result = json.loads(response.read().decode("utf-8"))
            return result
    except urllib.error.HTTPError as e:
        error_body = e.read().decode("utf-8")
        print(f"Error: HTTP {e.code} - {error_body}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


def format_tasks(tasks):
    """Format task list for display."""
    if not tasks:
        print("No tasks found.")
        return
    
    print(f"\nFound {len(tasks)} task(s):\n")
    
    for i, task in enumerate(tasks, 1):
        task_type = task.get('type', 'N/A')
        task_key = task.get('key') or 'N/A'
        
        print(f"[{i}] Type: {task_type}")
        print(f"    Key: {task_key}")
        
        # Print type-specific fields
        if task_type == 'TEXT_API':
            print(f"    Title: {task.get('title', 'N/A')}")
            print(f"    Message: {task.get('message', 'N/A')}")
            if task.get('signature'):
                print(f"    Signature: {task['signature']}")
        elif task_type == 'IMAGE_API':
            print(f"    Border: {task.get('border', 'N/A')}")
            print(f"    Dither Type: {task.get('ditherType', 'N/A')}")
            print(f"    Dither Kernel: {task.get('ditherKernel', 'N/A')}")
        
        print(f"    Refresh Now: {task.get('refreshNow', False)}")
        print()


def main():
    parser = argparse.ArgumentParser(
        description="List tasks/content for a Dot. device"
    )
    parser.add_argument(
        "--device-id", "-d",
        required=True,
        help="Device serial number (e.g., ABCD1234ABCD)"
    )
    parser.add_argument(
        "--type", "-t",
        choices=["loop", "fixed"],
        default="loop",
        help="Task type: loop (default) or fixed"
    )
    parser.add_argument(
        "--json", "-j",
        action="store_true",
        help="Output raw JSON"
    )
    
    args = parser.parse_args()
    
    result = list_tasks(args.device_id, args.type)
    
    if args.json:
        print(json.dumps(result, indent=2, ensure_ascii=False))
    else:
        format_tasks(result)


if __name__ == "__main__":
    main()
