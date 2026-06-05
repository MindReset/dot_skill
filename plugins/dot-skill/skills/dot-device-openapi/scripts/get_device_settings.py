#!/usr/bin/env python3
"""
Get settings for a Dot. device.

Usage:
    python get_device_settings.py --device-id ABCD1234ABCD

Environment Variables:
    DOT_API_KEY: Your Dot. API key (required)
"""

import argparse
import json
import os
import sys
import urllib.error
import urllib.request


BASE_URL = "https://dot.mindreset.tech"


def get_api_key():
    api_key = os.environ.get("DOT_API_KEY")
    if not api_key:
        print("Error: DOT_API_KEY environment variable not set", file=sys.stderr)
        print("Please set it with: export DOT_API_KEY='dot_app_<your_key>'", file=sys.stderr)
        sys.exit(1)
    return api_key


def get_device_settings(device_id):
    api_key = get_api_key()
    url = f"{BASE_URL}/api/authV2/open/device/{device_id}/settings"
    req = urllib.request.Request(url, headers={"Authorization": f"Bearer {api_key}"})

    try:
        with urllib.request.urlopen(req) as response:
            return json.loads(response.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        error_body = e.read().decode("utf-8")
        print(f"Error: HTTP {e.code} - {error_body}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


def main():
    parser = argparse.ArgumentParser(description="Get settings for a Dot. device")
    parser.add_argument(
        "--device-id", "-d",
        required=True,
        help="Device serial number (e.g., ABCD1234ABCD)",
    )
    args = parser.parse_args()

    result = get_device_settings(args.device_id)
    print(json.dumps(result, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
