#!/usr/bin/env python3
"""
Update settings for a Dot. device.

Usage:
    python update_device_settings.py --device-id ABCD1234ABCD --alias "Office Dot"
    python update_device_settings.py --device-id ABCD1234ABCD --timezone Asia/Shanghai --sleep-start 23:00 --sleep-end 07:00 --sleep-enabled
    python update_device_settings.py --device-id ABCD1234ABCD --power-ms 300000 --battery-ms 10800000

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


def update_device_settings(device_id, data):
    api_key = get_api_key()
    url = f"{BASE_URL}/api/authV2/open/device/{device_id}/settings"
    req = urllib.request.Request(
        url,
        data=json.dumps(data).encode("utf-8"),
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        },
        method="POST",
    )

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
    parser = argparse.ArgumentParser(description="Update settings for a Dot. device")
    parser.add_argument(
        "--device-id", "-d",
        required=True,
        help="Device serial number (e.g., ABCD1234ABCD)",
    )
    parser.add_argument("--alias", help="Device alias. Use an empty string to clear it")
    parser.add_argument("--location", help="Device location. Use an empty string to clear it")
    parser.add_argument("--timezone", help="Timezone key, for example Asia/Shanghai")
    parser.add_argument(
        "--power-ms",
        type=int,
        help="Power refresh interval in milliseconds (60,000-43,200,000)",
    )
    parser.add_argument(
        "--battery-ms",
        type=int,
        help="Battery automatic wake and refresh interval in milliseconds (60,000-43,200,000)",
    )
    parser.add_argument("--sleep-start", help="Sleep start time in HH:mm")
    parser.add_argument("--sleep-end", help="Sleep end time in HH:mm")
    parser.add_argument(
        "--sleep-enabled",
        action="store_true",
        help="Enable sleep when sleep times are provided",
    )
    parser.add_argument(
        "--sleep-disabled",
        action="store_true",
        help="Disable sleep when sleep times are provided",
    )
    args = parser.parse_args()

    data = {}
    if args.alias is not None:
        data["alias"] = args.alias
    if args.location is not None:
        data["location"] = args.location
    if args.timezone is not None:
        data["timezone"] = args.timezone
    if args.power_ms is not None or args.battery_ms is not None:
        data["interval"] = {}
        if args.power_ms is not None:
            data["interval"]["powerMs"] = args.power_ms
        if args.battery_ms is not None:
            data["interval"]["batteryMs"] = args.battery_ms
    if args.sleep_start is not None or args.sleep_end is not None:
        if args.sleep_start is None or args.sleep_end is None:
            print("Error: --sleep-start and --sleep-end must be provided together", file=sys.stderr)
            sys.exit(1)
        if args.sleep_enabled and args.sleep_disabled:
            print("Error: choose only one of --sleep-enabled or --sleep-disabled", file=sys.stderr)
            sys.exit(1)
        data["sleep"] = {
            "enabled": not args.sleep_disabled,
            "start": args.sleep_start,
            "end": args.sleep_end,
        }

    if not data:
        print("Error: provide at least one setting to update", file=sys.stderr)
        sys.exit(1)

    result = update_device_settings(args.device_id, data)
    print(f"Success: {result.get('message', 'settings updated')}")


if __name__ == "__main__":
    main()
