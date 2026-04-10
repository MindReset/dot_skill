# Dot. OpenAPI Skill

[English](./README.md) | [简体中文](./README.zh-CN.md)

A skill for AI agents to interact with Dot. devices through the OpenAPI.

## What is Dot. OpenAPI?

Dot. OpenAPI allows you to:

- **Control device content**: Display text, images, and other content on your Dot. devices
- **Query device status**: Get real-time information about device battery, WiFi signal, and current display
- **Manage devices**: List your devices, get device IDs, and switch between content

## Prerequisites

- A Dot. account with at least one device
- An API key from the Dot. App
- `python3` installed locally (for using the helper scripts)

## Installation

### Install with `npx skills add` (Recommended)

```bash
npx skills add <your-github-username>/dot-openapi-skill
```

Install only this skill:

```bash
npx skills add <your-github-username>/dot-openapi-skill --skill dot-openapi
```

### Manual Install

```bash
mkdir -p ~/.agents/skills
ln -sfn /path/to/dot-openapi-skill/skills/dot-openapi ~/.agents/skills/dot-openapi
```

Restart your agent after installation.

## Quick Start

1. **Get your API key**: Follow the guide in [docs/get_api_key.md](docs/get_api_key.md)
2. **Get your device ID**: Follow the guide in [docs/get_device_id.md](docs/get_device_id.md)
3. **Start using the API**: See [docs/api_reference.md](docs/api_reference.md) for all available endpoints

## API Overview

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/authV2/open/devices` | GET | List all your devices |
| `/api/authV2/open/device/:deviceId/status` | GET | Get device status |
| `/api/authV2/open/device/:deviceId/next` | POST | Switch to next content |
| `/api/authV2/open/device/:deviceId/text` | POST | Display text content |
| `/api/authV2/open/device/:deviceId/image` | POST | Display image content |
| `/api/authV2/open/device/:deviceId/:taskType/list` | GET | List device tasks |

## Helper Scripts

The `scripts/` directory contains Python helper scripts:

- `send_text.py`: Send text to a device
- `send_image.py`: Send an image to a device
- `get_device_status.py`: Get current device status
- `list_devices.py`: List all your devices

## Resources

- [API Reference](docs/api_reference.md) - Complete API documentation
- [Authentication](docs/authentication.md) - How to authenticate requests
- [Error Handling](docs/error_handling.md) - Common errors and solutions

## License

MIT License - see [LICENSE](./LICENSE) for details.
