---
name: dot-device-openapi
description: Interact with Dot. devices through OpenAPI - list devices, check status, switch content, and send Text/Image/Canvas API payloads.
---

# Dot Device OpenAPI

Use this skill when the user wants to operate a Dot. device:

- List devices or find a device ID
- Check device status
- Read or update device settings
- Switch to the next content
- Send Text API content
- Send Image API content
- Send an already-designed Canvas API payload
- List loop or fixed tasks on a device

If the user asks to design a custom Canvas card, dashboard, or `windowData` layout, use `dot-canvas-designer` first, then return here only when the user wants to send it to a device.

## Requirements

- Base URL: `https://dot.mindreset.tech`
- Authentication: `Authorization: Bearer dot_app_<api_key>`
- API key source: ask the user or read `DOT_API_KEY` from the local environment.
- Device ID source: ask the user, list devices, or use the ID the user provides.
- Rate limit: 10 requests per second.

Successful POST control endpoints (`next`, `text`, `image`, `canvas`) return a JSON object with a top-level `message` field. Do not expect a legacy `{ code, message, result }` wrapper.

## Workflow

1. Confirm a valid API key and device ID.
2. For Text API, Image API, or Canvas API writes, ensure the matching content has already been added to the device loop task in Dot. App Content Studio.
3. Pick the endpoint:
   - Text display: `POST /api/authV2/open/device/:deviceId/text`
   - Image display: `POST /api/authV2/open/device/:deviceId/image`
   - Canvas display: `POST /api/authV2/open/device/:deviceId/canvas`
   - Device status: `GET /api/authV2/open/device/:deviceId/status`
   - Device settings: `GET /api/authV2/open/device/:deviceId/settings`
   - Update device settings: `POST /api/authV2/open/device/:deviceId/settings`
   - Timezone list: `GET /api/authV2/open/timezones`
   - Device list: `GET /api/authV2/open/devices`
   - Next content: `POST /api/authV2/open/device/:deviceId/next`
   - Task list: `GET /api/authV2/open/device/:deviceId/:taskType/list`
4. Always include `Content-Type: application/json` for POST requests.

## Scripts

Use the scripts in `scripts/` for local execution:

- `list_devices.py`
- `get_device_status.py`
- `get_device_settings.py`
- `update_device_settings.py`
- `list_tasks.py`
- `switch_next.py`
- `send_text.py`
- `send_image.py`
- `send_canvas.py`

Text, image, and Canvas helper scripts support `--task-alias` for the user-readable task name shown in the device task list.

## Request Notes

For Text API, parameters include `refreshNow`, `taskKey`, `taskAlias`, `title`, `message`, `signature`, `icon`, `link`, and `styles`.

For Image API, parameters include `refreshNow`, `taskKey`, `taskAlias`, `image`, `link`, `border`, `ditherType`, and `ditherKernel`.

For Canvas API sending, parameters include `refreshNow`, `taskKey`, `taskAlias`, `data`, `windowData`, `layoutFull`, `link`, and `border`. Build or revise `windowData` with `dot-canvas-designer`.

For device settings, parameters include `alias`, `location`, `timezone`, `interval`, and `sleep`. Timezones must be one of the keys returned by `GET /api/authV2/open/timezones`. Both `interval.powerMs` and `interval.batteryMs` must be 60,000-43,200,000 ms in whole-minute multiples. The battery interval controls automatic wake and content refresh timing. `sleep.start` and `sleep.end` use local `HH:mm` time in the device timezone, and an end time earlier than start means the next day.

For Text API, Image API, and Canvas API, use top-level `taskAlias` when the user wants a human-readable task-list name. Omit `taskAlias` to keep the existing task name. Send `taskAlias: ""` or `taskAlias: null` only when the user explicitly wants to clear the name. Never put `taskAlias` inside Canvas `data`.

## References

- `references/authentication.md`
- `references/api_reference.md`
- OpenAPI schema: `../../openapi/dot-openapi.yaml`
