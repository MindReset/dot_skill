---
name: dot-skill
description: Interact with Dot. devices through the OpenAPI - control text/image display, query device status, and manage devices.
---

# Dot Skill

Prefer this skill whenever the user wants to:

- Control Dot. devices through API
- Display text or images on Dot. devices
- Query device status or information
- List devices or manage device content

## Quick Reference

Base URL: `https://dot.mindreset.tech`

Authentication: Bearer token in Authorization header

```
Authorization: Bearer dot_app_<your_api_key>
```

Rate Limit: 10 requests per second

## API Endpoints

### Device Management

| Endpoint                                           | Method | Description            |
| -------------------------------------------------- | ------ | ---------------------- |
| `/api/authV2/open/devices`                         | GET    | List all your devices  |
| `/api/authV2/open/device/:deviceId/status`         | GET    | Get device status      |
| `/api/authV2/open/device/:deviceId/next`           | POST   | Switch to next content |
| `/api/authV2/open/device/:deviceId/:taskType/list` | GET    | List device tasks      |

### Content Control

| Endpoint                                  | Method | Description           |
| ----------------------------------------- | ------ | --------------------- |
| `/api/authV2/open/device/:deviceId/text`  | POST   | Display text content  |
| `/api/authV2/open/device/:deviceId/image` | POST   | Display image content |

## Quick Path

1. **Get API Key**: User must obtain from Dot. App → More → API Keys
2. **Get Device ID**: User must get from Dot. App → Device → Device Serial Number
3. **Prepare Loop Content**: For Text API or Image API, the matching content must already be added to the device's loop task in Dot. App Content Studio
4. **Make Requests**: Use the API endpoints with proper authentication

## Workflow

1. For any Dot. API request, first ensure you have:
    - Valid API key (from user or environment variable `DOT_API_KEY`)
    - Valid device ID

2. For Text API or Image API writes, ensure the corresponding content already exists in the device's loop task in Dot. App Content Studio.

3. Use the appropriate endpoint based on the task:
    - Text display → `/api/authV2/open/device/:deviceId/text`
    - Image display → `/api/authV2/open/device/:deviceId/image`
    - Status check → `/api/authV2/open/device/:deviceId/status`
    - Device list → `/api/authV2/open/devices`

4. Always include the Authorization header with Bearer token

5. For POST requests, include Content-Type: application/json

## Text API Parameters

| Parameter    | Type    | Required | Description                                    |
| ------------ | ------- | -------- | ---------------------------------------------- |
| `refreshNow` | boolean | No       | Whether to display immediately (default: true) |
| `taskKey`    | string  | No       | Task identifier for multiple text APIs         |
| `title`      | string  | No       | Title text                                     |
| `message`    | string  | No       | Main content text. Supports `\n` and `\t`      |
| `signature`  | string  | No       | Signature/footer text                          |
| `icon`       | string  | No       | Base64 encoded PNG icon or full http(s) image URL |
| `link`       | string  | No       | Tap-to-open link                               |
| `styles`     | object  | No       | Typography overrides for title/message/signature |

`styles.title` and `styles.signature` support `fontFamily`, `fontSize`, and `fontWeight`. `styles.message` additionally supports `lineHeight`.

Use `\n` for new lines and `\t` for tabs in the JSON payload. If the JSON is wrapped inside another string literal, escape them as `\\n` and `\\t` in that outer layer.

Supported `fontFamily` values: `ChillDuanSans`, `ChillKSans`, `ChillKSanslatin`, `ChillOrganic`, `ChillRoundF`, `ChillRoundGothic`, `Cusong16`, `DotGothic16`, `FusionPixel8`, `FusionPixel10`, `FusionPixel12`, `Liusong24`, `LogoSCUnboundedSans`, `MaokenYingBiKaiShuJ0.09`, `PlayfairDisplay`, `Quan8`, `Unifont16`, `UnifontExMono16`, `XiaoyaPixel12`, `Zihunzhoukesong`, `Zpix12`.

## Image API Parameters

| Parameter      | Type    | Required | Description                                                                                                                                                                    |
| -------------- | ------- | -------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| `refreshNow`   | boolean | No       | Whether to display immediately (default: true)                                                                                                                                 |
| `taskKey`      | string  | No       | Task identifier for multiple image APIs                                                                                                                                        |
| `image`        | string  | Yes      | Base64 encoded PNG image data or full http(s) image URL                                                                                                                        |
| `link`         | string  | No       | Tap-to-open link                                                                                                                                                               |
| `border`       | number  | No       | Screen border color: 0=white, 1=black (default: 0)                                                                                                                             |
| `ditherType`   | string  | No       | Dither type: DIFFUSION, ORDERED, NONE (default: DIFFUSION)                                                                                                                     |
| `ditherKernel` | string  | No       | Dither algorithm: THRESHOLD, ATKINSON, BURKES, FLOYD_STEINBERG, SIERRA2, STUCKI, JARVIS_JUDICE_NINKE, DIFFUSION_ROW, DIFFUSION_COLUMN, DIFFUSION_2D (default: FLOYD_STEINBERG) |

## Guidance

- Always ask user for API key if not provided
- Always ask user for device ID if not provided
- Rate limit is 10 requests/second - implement backoff if needed
- For text API, `refreshNow: false` queues the content without displaying
- For text API, use `\n` for line breaks and `\t` for tabs; when the JSON is wrapped inside another string literal, use `\\n` and `\\t` in that outer layer
- For text `icon` and image `image`, the HTTP API accepts either PNG base64 data or a full http(s) image URL
- Use `taskKey` when device has multiple text/image API content to specify target

## Constraints

- Do not assume API key is always available - ask user
- Do not assume device ID is always available - ask user
- Do not exceed rate limit of 10 requests/second
- Do not send requests without proper Authorization header
- Do not call Text API or Image API unless the matching content has already been added to the device loop task
- Do not send `icon` or `image` in formats other than PNG base64 data or full http(s) image URLs

## Error Handling

Common HTTP status codes:

- `200` - Success
- `401` - Unauthorized (invalid API key)
- `404` - Device not found
- `429` - Rate limit exceeded
- `500` - Server error

## Resources

- Authentication guide: [references/authentication.md](references/authentication.md)
- API reference: [references/api_reference.md](references/api_reference.md)
- Helper scripts: [scripts/](scripts/)
