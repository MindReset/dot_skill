#!/usr/bin/env python3
"""
List all Dot. devices associated with your account.

Usage:
    python list_devices.py
    python list_devices.py --json

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


def list_devices():
    """List all devices."""
    api_key = get_api_key()
    
    url = f"{BASE_URL}/api/authV2/open/devices"
    
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


def format_devices(devices):
    """Format device list for display."""
    if not devices:
        print("No devices found.")
        return
    
    print(f"\nFound {len(devices)} device(s):\n")
    
    # Print header
    print(f"{'Device ID':<20} {'Series':<10} {'Model':<15} {'Edition':<10}")
    print("-" * 60)
    
    # Print devices
    for device in devices:
        device_id = device.get('id', 'N/A')
        series = device.get('series', 'N/A')
        model = device.get('model', 'N/A')
        edition = device.get('edition', 'N/A')
        
        print(f"{device_id:<20} {series:<10} {model:<15} {edition:<10}")


def main():
    parser = argparse.ArgumentParser(
        description="List all Dot. devices"
    )
    parser.add_argument(
        "--json", "-j",
        action="store_true",
        help="Output raw JSON"
    )
    
    args = parser.parse_args()
    
    result = list_devices()
    
    if args.json:
        print(json.dumps(result, indent=2, ensure_ascii=False))
    else:
        format_devices(result)


if __name__ == "__main__":
    main()
