#!/usr/bin/env python3
"""
Get the status of a Dot. device.

Usage:
    python get_device_status.py --device-id ABCD1234ABCD

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


def get_device_status(device_id):
    """Get the status of a device."""
    api_key = get_api_key()
    
    url = f"{BASE_URL}/api/authV2/open/device/{device_id}/status"
    
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


def format_status(status_data):
    """Format device status for display."""
    print(f"\nDevice ID: {status_data.get('deviceId', 'N/A')}")
    print(f"Alias: {status_data.get('alias') or 'Not set'}")
    print(f"Location: {status_data.get('location') or 'Not set'}")
    
    status = status_data.get('status', {})
    print(f"\nStatus:")
    print(f"  Version: {status.get('version', 'N/A')}")
    print(f"  Current: {status.get('current', 'N/A')}")
    print(f"  Description: {status.get('description', 'N/A')}")
    print(f"  Battery: {status.get('battery', 'N/A')}")
    print(f"  WiFi: {status.get('wifi', 'N/A')}")
    
    render_info = status_data.get('renderInfo', {})
    print(f"\nRender Info:")
    print(f"  Last Render: {render_info.get('last', 'N/A')}")
    
    current = render_info.get('current', {})
    print(f"  Current Display:")
    print(f"    Rotated: {current.get('rotated', False)}")
    print(f"    Border: {current.get('border', 0)}")
    print(f"    Images: {', '.join(current.get('image', [])) or 'N/A'}")
    
    next_render = render_info.get('next', {})
    print(f"  Next Scheduled:")
    print(f"    Battery: {next_render.get('battery', 'N/A')}")
    print(f"    Power: {next_render.get('power', 'N/A')}")


def main():
    parser = argparse.ArgumentParser(
        description="Get the status of a Dot. device"
    )
    parser.add_argument(
        "--device-id", "-d",
        required=True,
        help="Device serial number (e.g., ABCD1234ABCD)"
    )
    parser.add_argument(
        "--json", "-j",
        action="store_true",
        help="Output raw JSON"
    )
    
    args = parser.parse_args()
    
    result = get_device_status(args.device_id)
    
    if args.json:
        print(json.dumps(result, indent=2, ensure_ascii=False))
    else:
        format_status(result)


if __name__ == "__main__":
    main()
