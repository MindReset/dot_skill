# Dot Device OpenAPI Reference

Base URL: `https://dot.mindreset.tech`

Authentication:

```http
Authorization: Bearer dot_app_<your_api_key>
```

## Endpoints

| Endpoint | Method | Description |
| --- | --- | --- |
| `/api/authV2/open/devices` | GET | List all devices |
| `/api/authV2/open/device/:deviceId/status` | GET | Get device status |
| `/api/authV2/open/device/:deviceId/next` | POST | Switch to next content |
| `/api/authV2/open/device/:deviceId/:taskType/list` | GET | List loop or fixed tasks |
| `/api/authV2/open/device/:deviceId/text` | POST | Display Text API content |
| `/api/authV2/open/device/:deviceId/image` | POST | Display Image API content |
| `/api/authV2/open/device/:deviceId/canvas` | POST | Display Canvas API content |

## Shared Write Parameters

Text API, Image API, and Canvas API support:

| Parameter | Type | Required | Description |
| --- | --- | --- | --- |
| `refreshNow` | boolean | No | Display immediately. Defaults to `true` |
| `taskKey` | string | No | Task identifier when a device has multiple API items |
| `taskAlias` | string \| number | No | Human-readable task name shown in the device task list |

Omit `taskAlias` to keep the existing task name. Send `taskAlias: ""` or `taskAlias: null` only when intentionally clearing the name.

## Text API

```http
POST /api/authV2/open/device/:deviceId/text
```

Before calling this endpoint, the device should already have a Text API content item in its loop task.

| Parameter | Type | Required | Description |
| --- | --- | --- | --- |
| `title` | string | No | Title text |
| `message` | string | No | Main content text. Supports `\n` and `\t` |
| `signature` | string | No | Footer/signature text |
| `icon` | string | No | Base64 PNG icon or full http(s) image URL |
| `link` | string | No | Tap-to-open link |
| `styles` | object | No | Typography overrides |

`styles.title` and `styles.signature` support `fontFamily`, `fontSize`, and `fontWeight`. `styles.message` also supports `lineHeight`.

## Image API

```http
POST /api/authV2/open/device/:deviceId/image
```

Before calling this endpoint, the device should already have an Image API content item in its loop task.

| Parameter | Type | Required | Description |
| --- | --- | --- | --- |
| `image` | string | Yes | Base64 PNG image data or full http(s) image URL |
| `link` | string | No | Tap-to-open link |
| `border` | number | No | Screen border color: `0` white, `1` black |
| `ditherType` | string | No | `DIFFUSION`, `ORDERED`, or `NONE` |
| `ditherKernel` | string | No | `THRESHOLD`, `ATKINSON`, `BURKES`, `FLOYD_STEINBERG`, `SIERRA2`, `STUCKI`, `JARVIS_JUDICE_NINKE`, `DIFFUSION_ROW`, `DIFFUSION_COLUMN`, or `DIFFUSION_2D` |

## Canvas API Sending

```http
POST /api/authV2/open/device/:deviceId/canvas
```

Before calling this endpoint, the device should already have a Canvas API content item in its loop task.

| Parameter | Type | Required | Description |
| --- | --- | --- | --- |
| `data` | object | No | Plain JSON values the layout reads at render time |
| `windowData` | object | Yes | React object-like render tree with a `default` layer array |
| `layoutFull` | object | No | FULL layout override with optional `tw` and `style` |
| `link` | string | No | Tap-to-open link |
| `border` | number | No | Screen border color: `0` white, `1` black |

Use `dot-canvas-designer` to build or revise `windowData`. This device skill only sends the finished payload.

Reserved top-level keys inside Canvas `data`: `type`, `key`, `windowData`, `layoutFull`, `taskAlias`, `link`, `border`, `__proto__`, `constructor`, `prototype`.
