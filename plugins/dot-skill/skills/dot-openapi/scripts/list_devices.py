#!/usr/bin/env python3
"""List all Dot. devices associated with your account."""

import argparse
import json

from _runtime import DotClient, run


def list_devices():
    return DotClient.from_env().list_devices()


def format_devices(devices):
    if not devices:
        print("No devices found.")
        return

    print(f"\nFound {len(devices)} device(s):\n")
    print(
        f"{'Device ID':<20} {'Alias':<20} {'Location':<20} "
        f"{'Series':<10} {'Model':<15} {'Edition':<10}"
    )
    print("-" * 100)
    for device in devices:
        print(
            f"{device.get('id', 'N/A'):<20} "
            f"{device.get('alias') or 'N/A':<20} "
            f"{device.get('location') or 'N/A':<20} "
            f"{device.get('series', 'N/A'):<10} "
            f"{device.get('model', 'N/A'):<15} "
            f"{device.get('edition', 'N/A'):<10}"
        )


def main():
    parser = argparse.ArgumentParser(description="List all Dot. devices")
    parser.add_argument("--json", "-j", action="store_true", help="Output raw JSON")
    args = parser.parse_args()
    result = run(list_devices)
    if args.json:
        print(json.dumps(result, indent=2, ensure_ascii=False))
    else:
        format_devices(result)


if __name__ == "__main__":
    main()
