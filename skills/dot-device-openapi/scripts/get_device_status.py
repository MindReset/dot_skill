#!/usr/bin/env python3
"""Get the status of a Dot. device."""

import argparse
import json

from _runtime import DotClient, run


def get_device_status(device_id):
    return DotClient.from_env().get_device_status(device_id)


def format_status(status_data):
    print(f"\nDevice ID: {status_data.get('deviceId', 'N/A')}")
    print(f"Alias: {status_data.get('alias') or 'Not set'}")
    print(f"Location: {status_data.get('location') or 'Not set'}")
    status = status_data.get("status", {})
    print("\nStatus:")
    print(f"  Version: {status.get('version', 'N/A')}")
    print(f"  Current: {status.get('current', 'N/A')}")
    print(f"  Description: {status.get('description', 'N/A')}")
    print(f"  Battery: {status.get('battery', 'N/A')}")
    print(f"  WiFi: {status.get('wifi', 'N/A')}")
    render_info = status_data.get("renderInfo", {})
    print("\nRender Info:")
    print(f"  Last Render: {render_info.get('last', 'N/A')}")
    current = render_info.get("current", {})
    print("  Current Display:")
    print(f"    Rotated: {current.get('rotated', False)}")
    print(f"    Border: {current.get('border', 0)}")
    print(f"    Images: {', '.join(current.get('image', [])) or 'N/A'}")
    next_render = render_info.get("next", {})
    print("  Next Scheduled:")
    print(f"    Battery: {next_render.get('battery', 'N/A')}")
    print(f"    Power: {next_render.get('power', 'N/A')}")


def main():
    parser = argparse.ArgumentParser(description="Get the status of a Dot. device")
    parser.add_argument("--device-id", "-d", required=True)
    parser.add_argument("--json", "-j", action="store_true", help="Output raw JSON")
    args = parser.parse_args()
    result = run(lambda: get_device_status(args.device_id))
    if args.json:
        print(json.dumps(result, indent=2, ensure_ascii=False))
    else:
        format_status(result)


if __name__ == "__main__":
    main()
