#!/usr/bin/env python3
"""Update settings for a Dot. device."""

import argparse

from _runtime import DotClient, run


def update_device_settings(device_id, data):
    return DotClient.from_env().update_device_settings(device_id, data)


def main():
    parser = argparse.ArgumentParser(description="Update settings for a Dot. device")
    parser.add_argument("--device-id", "-d", required=True)
    parser.add_argument("--alias")
    parser.add_argument("--location")
    parser.add_argument("--timezone")
    parser.add_argument("--power-ms", type=int)
    parser.add_argument("--battery-ms", type=int)
    parser.add_argument("--sleep-start")
    parser.add_argument("--sleep-end")
    parser.add_argument("--sleep-enabled", action="store_true")
    parser.add_argument("--sleep-disabled", action="store_true")
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
            parser.error("--sleep-start and --sleep-end must be provided together")
        if args.sleep_enabled and args.sleep_disabled:
            parser.error("choose only one of --sleep-enabled or --sleep-disabled")
        data["sleep"] = {
            "enabled": not args.sleep_disabled,
            "start": args.sleep_start,
            "end": args.sleep_end,
        }
    if not data:
        parser.error("provide at least one setting to update")

    result = run(lambda: update_device_settings(args.device_id, data))
    if isinstance(result, dict):
        print(f"Success: {result.get('message', 'settings updated')}")


if __name__ == "__main__":
    main()
