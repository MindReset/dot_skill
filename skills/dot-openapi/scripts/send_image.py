#!/usr/bin/env python3
"""
Send image content to a Dot. device.

Usage:
    python send_image.py --device-id ABCD1234ABCD --image path/to/image.png
    python send_image.py --device-id ABCD1234ABCD --image path/to/image.png --border 1

Environment Variables:
    DOT_API_KEY: Your Dot. API key (required)
"""

import argparse
import os
import sys
import base64
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


def encode_image(image_path):
    """Encode image file to base64."""
    with open(image_path, "rb") as f:
        return base64.b64encode(f.read()).decode("utf-8")


def send_image(device_id, image_path, link=None, border=0, 
               dither_type="DIFFUSION", dither_kernel="FLOYD_STEINBERG",
               refresh_now=True, task_key=None):
    """Send image content to a device."""
    api_key = get_api_key()
    
    url = f"{BASE_URL}/api/authV2/open/device/{device_id}/image"
    
    # Encode image
    image_data = encode_image(image_path)
    
    data = {
        "refreshNow": refresh_now,
        "image": image_data
    }
    
    if link is not None:
        data["link"] = link
    if border is not None:
        data["border"] = border
    if dither_type is not None:
        data["ditherType"] = dither_type
    if dither_kernel is not None:
        data["ditherKernel"] = dither_kernel
    if task_key is not None:
        data["taskKey"] = task_key
    
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    req = urllib.request.Request(
        url,
        data=json.dumps(data).encode("utf-8"),
        headers=headers,
        method="POST"
    )
    
    try:
        with urllib.request.urlopen(req) as response:
            result = json.loads(response.read().decode("utf-8"))
            print(f"Success: {result['message']}")
            return result
    except urllib.error.HTTPError as e:
        error_body = e.read().decode("utf-8")
        print(f"Error: HTTP {e.code} - {error_body}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


def main():
    parser = argparse.ArgumentParser(
        description="Send image content to a Dot. device"
    )
    parser.add_argument(
        "--device-id", "-d",
        required=True,
        help="Device serial number (e.g., ABCD1234ABCD)"
    )
    parser.add_argument(
        "--image", "-i",
        required=True,
        help="Path to PNG image file"
    )
    parser.add_argument(
        "--link", "-l",
        help="Tap-to-open link URL"
    )
    parser.add_argument(
        "--border", "-b",
        type=int,
        choices=[0, 1],
        default=0,
        help="Screen border color: 0=white (default), 1=black"
    )
    parser.add_argument(
        "--dither-type",
        choices=["DIFFUSION", "ORDERED", "NONE"],
        default="DIFFUSION",
        help="Dither type (default: DIFFUSION)"
    )
    parser.add_argument(
        "--dither-kernel",
        choices=[
            "THRESHOLD", "ATKINSON", "BURKES", "FLOYD_STEINBERG",
            "SIERRA2", "STUCKI", "JARVIS_JUDICE_NINKE",
            "DIFFUSION_ROW", "DIFFUSION_COLUMN", "DIFFUSION_2D"
        ],
        default="FLOYD_STEINBERG",
        help="Dither algorithm (default: FLOYD_STEINBERG)"
    )
    parser.add_argument(
        "--refresh-now",
        action="store_true",
        default=True,
        help="Display immediately (default: true)"
    )
    parser.add_argument(
        "--no-refresh-now",
        action="store_false",
        dest="refresh_now",
        help="Queue without displaying immediately"
    )
    parser.add_argument(
        "--task-key",
        help="Task identifier for multiple image APIs"
    )
    
    args = parser.parse_args()
    
    send_image(
        device_id=args.device_id,
        image_path=args.image,
        link=args.link,
        border=args.border,
        dither_type=args.dither_type,
        dither_kernel=args.dither_kernel,
        refresh_now=args.refresh_now,
        task_key=args.task_key
    )


if __name__ == "__main__":
    main()
