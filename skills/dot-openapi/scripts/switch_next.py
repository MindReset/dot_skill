#!/usr/bin/env python3
"""
Switch to the next content on a Dot. device.

Usage:
    python switch_next.py --device-id ABCD1234ABCD

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


def switch_next(device_id):
    """Switch to next content on a device."""
    api_key = get_api_key()
    
    url = f"{BASE_URL}/api/authV2/open/device/{device_id}/next"
    
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    req = urllib.request.Request(
        url,
        data=json.dumps({}).encode("utf-8"),
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
        description="Switch to the next content on a Dot. device"
    )
    parser.add_argument(
        "--device-id", "-d",
        required=True,
        help="Device serial number (e.g., ABCD1234ABCD)"
    )
    
    args = parser.parse_args()
    
    switch_next(args.device_id)


if __name__ == "__main__":
    main()
