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
| `/api/authV2/open/timezones` | GET | List supported timezone keys |
| `/api/authV2/open/device/:deviceId/status` | GET | Get device status |
| `/api/authV2/open/device/:deviceId/settings` | GET | Get device settings |
| `/api/authV2/open/device/:deviceId/settings` | POST | Update device settings |
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

## Device Settings

```http
GET /api/authV2/open/device/:deviceId/settings
POST /api/authV2/open/device/:deviceId/settings
```

Use `GET` to read editable settings. Use `POST` to update one or more settings; omitted fields are left unchanged.

```json
{
	"alias": "Office Dot",
	"location": "Desk",
	"timezone": "Asia/Shanghai",
	"interval": {
		"powerMs": 300000,
		"batteryMs": 10800000
	},
	"sleep": {
		"enabled": true,
		"start": "23:00",
		"end": "07:00"
	}
}
```

| Parameter | Type | Required | Description |
| --- | --- | --- | --- |
| `alias` | string \| null | No | Device alias. Send `null` or an empty string to clear it |
| `location` | string \| null | No | Device location. Send `null` or an empty string to clear it |
| `timezone` | string | No | Must be a key returned by `GET /api/authV2/open/timezones` |
| `interval.powerMs` | number | No | Power refresh interval in milliseconds. Must be 60,000-86,400,000 and a multiple of 60,000 |
| `interval.batteryMs` | number | No | Battery refresh interval in milliseconds. Must be 900,000-43,200,000 and a multiple of 60,000 |
| `sleep.enabled` | boolean | Yes, when `sleep` is sent | Enable or disable sleep |
| `sleep.start` | string | Yes, when `sleep` is sent | Local `HH:mm` start time in the device timezone |
| `sleep.end` | string | Yes, when `sleep` is sent | Local `HH:mm` end time in the device timezone. If earlier than start, it means the next day |

`sleep.start` and `sleep.end` cannot be the same time.

## Timezones

```http
GET /api/authV2/open/timezones
```

Returns supported timezone keys, localized names, and current UTC offsets. Device settings only accept timezone keys from this list.

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
| `icon` | string | No | Optional PNG icon. Send bare PNG Base64, `data:image/png;base64,` data URL, or full http(s) image URL. Base64 payloads must decode to at most 1MB. Remote URLs must be anonymously accessible, at most 2048 characters, return `image/*`, and the response body must be at most 3MB. |
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
| `image` | string | Yes | Required image content. Send bare PNG Base64, `data:image/png;base64,` data URL, or full http(s) image URL. Base64 payloads must decode to at most 3MB. Remote URLs must be anonymously accessible, at most 2048 characters, return `image/*`, and the response body must be at most 3MB. |
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
