#!/usr/bin/env python3
"""
Send text content to a Dot. device.

Usage:
    python send_text.py --device-id ABCD1234ABCD --title "Hello" --message "World"
    python send_text.py --device-id ABCD1234ABCD --message "Test message" --refresh-now

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


def send_text(device_id, title=None, message=None, signature=None, 
              icon=None, link=None, refresh_now=True, task_key=None):
    """Send text content to a device."""
    api_key = get_api_key()
    
    url = f"{BASE_URL}/api/authV2/open/device/{device_id}/text"
    
    data = {
        "refreshNow": refresh_now
    }
    
    if title is not None:
        data["title"] = title
    if message is not None:
        data["message"] = message
    if signature is not None:
        data["signature"] = signature
    if icon is not None:
        data["icon"] = icon
    if link is not None:
        data["link"] = link
    if task_key is not None:
        data["taskKey"] = task_key
    
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    req = urllib.request.Request(
        url,
        data=json.dumps(data).encode("utf-8"),
        headers=headers,
        method="POST"
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
        description="Send text content to a Dot. device"
    )
    parser.add_argument(
        "--device-id", "-d",
        required=True,
        help="Device serial number (e.g., ABCD1234ABCD)"
    )
    parser.add_argument(
        "--title", "-t",
        help="Title text"
    )
    parser.add_argument(
        "--message", "-m",
        help="Main content text"
    )
    parser.add_argument(
        "--signature", "-s",
        help="Signature/footer text"
    )
    parser.add_argument(
        "--icon",
        help="Path to PNG icon file (will be base64 encoded)"
    )
    parser.add_argument(
        "--link", "-l",
        help="Tap-to-open link URL"
    )
    parser.add_argument(
        "--refresh-now",
        action="store_true",
        default=True,
        help="Display immediately (default: true)"
    )
    parser.add_argument(
        "--no-refresh-now",
        action="store_false",
        dest="refresh_now",
        help="Queue without displaying immediately"
    )
    parser.add_argument(
        "--task-key",
        help="Task identifier for multiple text APIs"
    )
    
    args = parser.parse_args()
    
    # Read icon file if provided
    icon_data = None
    if args.icon:
        import base64
        with open(args.icon, "rb") as f:
            icon_data = base64.b64encode(f.read()).decode("utf-8")
    
    send_text(
        device_id=args.device_id,
        title=args.title,
        message=args.message,
        signature=args.signature,
        icon=icon_data,
        link=args.link,
        refresh_now=args.refresh_now,
        task_key=args.task_key
    )


if __name__ == "__main__":
    main()
