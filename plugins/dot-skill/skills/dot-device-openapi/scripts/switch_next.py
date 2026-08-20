#!/usr/bin/env python3
"""Switch a Dot. device to its next content item."""

import argparse

from _runtime import DotClient, run


def switch_next(device_id):
    result = DotClient.from_env().switch_next_content(device_id)
    if isinstance(result, dict):
        print(f"Success: {result.get('message', 'content switched')}")
    return result


def main():
    parser = argparse.ArgumentParser(description="Switch to the next Dot. content")
    parser.add_argument("--device-id", "-d", required=True)
    args = parser.parse_args()
    run(lambda: switch_next(args.device_id))


if __name__ == "__main__":
    main()
