#!/usr/bin/env python3
"""Get settings for a Dot. device."""

import argparse
import json

from _runtime import DotClient, run


def get_device_settings(device_id):
    return DotClient.from_env().get_device_settings(device_id)


def main():
    parser = argparse.ArgumentParser(description="Get settings for a Dot. device")
    parser.add_argument("--device-id", "-d", required=True)
    args = parser.parse_args()
    result = run(lambda: get_device_settings(args.device_id))
    print(json.dumps(result, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
