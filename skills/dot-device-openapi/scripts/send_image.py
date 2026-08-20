#!/usr/bin/env python3
"""Send image content to a Dot. device."""

import argparse
import base64

from _runtime import DotClient, run


def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode("utf-8")


def send_image(
    device_id,
    image_path,
    link=None,
    border=0,
    dither_type="DIFFUSION",
    dither_kernel="FLOYD_STEINBERG",
    refresh_now=True,
    task_key=None,
    task_alias=None,
):
    data = {
        "refreshNow": refresh_now,
        "image": encode_image(image_path),
        "border": border,
        "ditherType": dither_type,
        "ditherKernel": dither_kernel,
    }
    for key, value in {
        "link": link,
        "taskKey": task_key,
        "taskAlias": task_alias,
    }.items():
        if value is not None:
            data[key] = value
    result = DotClient.from_env().send_image(device_id, data)
    if isinstance(result, dict):
        print(f"Success: {result.get('message', 'image sent')}")
    return result


def main():
    parser = argparse.ArgumentParser(description="Send image content to a Dot. device")
    parser.add_argument("--device-id", "-d", required=True)
    parser.add_argument("--image", "-i", required=True, help="Path to PNG image")
    parser.add_argument("--link", "-l")
    parser.add_argument("--border", "-b", type=int, choices=[0, 1], default=0)
    parser.add_argument("--dither-type", choices=["DIFFUSION", "ORDERED", "NONE"], default="DIFFUSION")
    parser.add_argument(
        "--dither-kernel",
        choices=[
            "THRESHOLD", "ATKINSON", "BURKES", "FLOYD_STEINBERG", "SIERRA2",
            "STUCKI", "JARVIS_JUDICE_NINKE", "DIFFUSION_ROW", "DIFFUSION_COLUMN",
            "DIFFUSION_2D",
        ],
        default="FLOYD_STEINBERG",
    )
    parser.add_argument("--refresh-now", action="store_true", default=True)
    parser.add_argument("--no-refresh-now", action="store_false", dest="refresh_now")
    parser.add_argument("--task-key")
    parser.add_argument("--task-alias")
    args = parser.parse_args()
    run(
        lambda: send_image(
            device_id=args.device_id,
            image_path=args.image,
            link=args.link,
            border=args.border,
            dither_type=args.dither_type,
            dither_kernel=args.dither_kernel,
            refresh_now=args.refresh_now,
            task_key=args.task_key,
            task_alias=args.task_alias,
        )
    )


if __name__ == "__main__":
    main()
