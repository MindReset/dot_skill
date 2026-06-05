# Dot Skill

**Languages:** [English](./README.md) | [简体中文](./README.zh-CN.md) | [日本語](./README.ja-JP.md)

![Codex Plugin](https://img.shields.io/badge/Codex-Plugin-black)
![OpenAPI](https://img.shields.io/badge/OpenAPI-3.1-blue)
![MCP Ready](https://img.shields.io/badge/MCP-ready-blueviolet)
![License: MIT](https://img.shields.io/badge/License-MIT-green)

A skill for AI agents to interact with Dot. devices through the OpenAPI.

📚 **Official Documentation**: [https://dot.mindreset.tech/docs/service/open/skill](https://dot.mindreset.tech/docs/service/open/skill)

## What is Dot Skill?

Dot Skill allows you to:

- **Control device content**: Display text, images, Canvas API layouts, and other content on your Dot. devices
- **Design Canvas layouts**: Build `windowData` cards, dashboards, list views, conditions, and formatting with a dedicated Canvas designer skill
- **Name API content**: Set a task alias for text, image, and Canvas API items so they are easy to identify
- **Query device status**: Get real-time information about device battery, WiFi signal, and current display
- **Manage devices**: List your devices, get device IDs, and switch between content

The repository now splits responsibilities into:

- `dot-device-openapi`: device interaction, API calls, and helper scripts
- `dot-canvas-designer`: Canvas API `windowData` design and layout guidance
- `dot-openapi`: compatibility router for older installs

## Prerequisites

- A Dot. account with at least one device
- An API key from the Dot. App
- `python3` installed locally (for using the helper scripts)

## Installation

### Install as a Codex plugin

Add this repository as a Codex marketplace:

```bash
codex plugin marketplace add git@github.com:MindReset/dot_skill.git
```

Then install the plugin:

```bash
codex plugin add dot-skill@mindreset-dot-skill
```

Start a new Codex thread after installation so Codex can load the plugin's skills.

### Use with GPT Actions or OpenAPI-compatible agents

Import the OpenAPI schema:

```text
https://raw.githubusercontent.com/MindReset/dot_skill/master/openapi/dot-openapi.yaml
```

Configure Bearer authentication with a Dot. API key:

```http
Authorization: Bearer dot_app_<your_api_key>
```

Public GPTs or agents that call Dot. APIs should include the Dot. privacy policy and terms:

- Privacy Policy: [https://dot.mindreset.tech/docs/privacy](https://dot.mindreset.tech/docs/privacy)
- Terms of Service: [https://dot.mindreset.tech/docs/terms](https://dot.mindreset.tech/docs/terms)

### Install with `npx skills add` (Recommended)

```bash
npx skills add https://github.com/MindReset/dot_skill.git
```

Install only the device interaction skill:

```bash
npx skills add https://github.com/MindReset/dot_skill.git --skill dot-device-openapi
```

Install only the Canvas designer skill:

```bash
npx skills add https://github.com/MindReset/dot_skill.git --skill dot-canvas-designer
```

### Manual Install

```bash
mkdir -p ~/.agents/skills
ln -sfn /path/to/dot_skill/skills/dot-device-openapi ~/.agents/skills/dot-device-openapi
ln -sfn /path/to/dot_skill/skills/dot-canvas-designer ~/.agents/skills/dot-canvas-designer
```

Restart your agent after installation.

## Quick Start

1. **Get your API key**: Follow the [official documentation](https://dot.mindreset.tech/docs/service/open/get_api)
2. **Get your device ID**: Follow the [official documentation](https://dot.mindreset.tech/docs/service/open/get_device_id)
3. **Start using the API**: See [Device API Reference](skills/dot-device-openapi/references/api_reference.md) for endpoints and [Canvas windowData Reference](skills/dot-canvas-designer/references/windowdata.md) for Canvas layout design

## Agent Platform Compatibility

| Platform | Status | Integration path |
| --- | --- | --- |
| Codex | Supported | Repository marketplace at `.agents/plugins/marketplace.json` |
| OpenAI GPT Actions | Supported via schema | Import `openapi/dot-openapi.yaml` and configure Bearer auth |
| Claude / MCP clients | Planned | Use the OpenAPI schema today; a remote MCP server can be added later |
| Cursor and skill-compatible agents | Supported as skill docs | Install `skills/dot-device-openapi` and/or `skills/dot-canvas-designer`, or read this repository as context |
| MCP Registry | Planned | Publish server metadata after a Dot MCP server exists |

## API Overview

| Endpoint                                           | Method | Description            |
| -------------------------------------------------- | ------ | ---------------------- |
| `/api/authV2/open/devices`                         | GET    | List all your devices  |
| `/api/authV2/open/timezones`                       | GET    | List supported timezones |
| `/api/authV2/open/device/:deviceId/status`         | GET    | Get device status      |
| `/api/authV2/open/device/:deviceId/settings`       | GET    | Get device settings    |
| `/api/authV2/open/device/:deviceId/settings`       | POST   | Update device settings |
| `/api/authV2/open/device/:deviceId/next`           | POST   | Switch to next content |
| `/api/authV2/open/device/:deviceId/text`           | POST   | Display text content   |
| `/api/authV2/open/device/:deviceId/image`          | POST   | Display image content  |
| `/api/authV2/open/device/:deviceId/canvas`         | POST   | Display canvas content |
| `/api/authV2/open/device/:deviceId/:taskType/list` | GET    | List device tasks      |

## Helper Scripts

The `skills/dot-device-openapi/scripts/` directory contains Python helper scripts:

- `send_text.py`: Send text to a device
- `send_image.py`: Send an image to a device
- `send_canvas.py`: Send a Canvas API JSON layout to a device
- `get_device_status.py`: Get current device status
- `get_device_settings.py`: Get device settings
- `update_device_settings.py`: Update device settings
- `list_devices.py`: List all your devices
- `list_tasks.py`: List device loop or fixed tasks
- `switch_next.py`: Switch to the next content

Text, image, and Canvas helper scripts support `--task-alias` to set the human-readable task name shown in the device task list.

## Resources

- [Device API Reference](skills/dot-device-openapi/references/api_reference.md) - Device interaction and endpoint documentation
- [Canvas windowData Reference](skills/dot-canvas-designer/references/windowdata.md) - Canvas layout design rules
- [Canvas Examples](skills/dot-canvas-designer/references/examples.md) - Example Canvas payloads
- [Authentication](skills/dot-device-openapi/references/authentication.md) - How to authenticate requests
- [OpenAPI Schema](openapi/dot-openapi.yaml) - Importable schema for Actions and OpenAPI-compatible tools
- [Security Policy](SECURITY.md) - Credential handling and vulnerability reporting
- [Official Dot. Security Policy](https://dot.mindreset.tech/docs/security_policy) - Responsible disclosure process
- [Support](SUPPORT.md) - Issue reporting guidance
- [Changelog](CHANGELOG.md) - Release notes

## Maintainer Notes

This repository is the public, user-facing skill package for Dot. device control and Canvas design. When Dot Web changes API behavior, keep these surfaces aligned:

- `openapi/dot-openapi.yaml` for OpenAPI-compatible agents and GPT Actions
- `skills/dot-device-openapi` for device interaction scripts and endpoint guidance
- `skills/dot-canvas-designer` for Canvas API payload design rules
- `plugins/dot-skill` for Codex plugin packaging
- Dot Web public docs under `dot_web_docs`

Internal-only Studio V2 implementation, MongoDB migration, and render-debugging workflows belong in `dot_internal_skill`, not this public package.

## License

MIT License - see [LICENSE](./LICENSE) for details.
