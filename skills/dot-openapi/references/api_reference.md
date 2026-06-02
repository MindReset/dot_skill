# API Reference

## Base URL

```
https://dot.mindreset.tech
```

## Authentication

All requests require an Authorization header:

```http
Authorization: Bearer dot_app_<your_api_key>
```

## Rate Limiting

- **Limit**: 10 requests per second
- **Exceeding limit**: Returns HTTP 429 (Too Many Requests)

---

## List Devices

Get a list of all devices associated with your account.

```http
GET /api/authV2/open/devices
```

### Response

```json
[
  {
    "alias": "My Dot",
    "location": "Study",
    "series": "quote",
    "model": "quote_0",
    "edition": 1,
    "id": "ABCD1234ABCD"
  }
]
```

| Field | Type | Description |
|-------|------|-------------|
| `alias` | string \| null | Device alias |
| `location` | string \| null | Device location |
| `series` | string | Device series (e.g., "quote") |
| `model` | string | Device model (e.g., "quote_0") |
| `edition` | number | Device edition (1 or 2) |
| `id` | string | Device serial number |

---

## Get Device Status

Get the current status of a specific device.

```http
GET /api/authV2/open/device/:deviceId/status
```

### Path Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `deviceId` | string | Yes | Device serial number |

### Response

```json
{
  "deviceId": "ABCD1234ABCD",
  "alias": null,
  "location": null,
  "status": {
    "version": "1.0.0",
    "current": "电源活跃中",
    "description": "设备电源活跃中，随时可以使用",
    "battery": "充电中",
    "wifi": "-62 dBm"
  },
  "renderInfo": {
    "last": "2025 年 12 月 18 日 14:11",
    "current": {
      "rotated": false,
      "border": 0,
      "image": ["https://example.com/render/0.png"]
    },
    "next": {
      "battery": "2025 年 12 月 18 日 17:11",
      "power": "2025 年 12 月 18 日 14:16"
    }
  }
}
```

---

## Switch to Next Content

Immediately switch to the next content in the rotation.

```http
POST /api/authV2/open/device/:deviceId/next
```

### Path Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `deviceId` | string | Yes | Device serial number |

### Response

```json
{
  "code": 200,
  "message": "设备 ABCD1234ABCD 已成功切换到下一个内容",
  "result": {
    "message": "设备 ABCD1234ABCD 已成功切换到下一个内容"
  }
}
```

---

## Display Text

Display text content on the device.

```http
POST /api/authV2/open/device/:deviceId/text
```

> Before calling this endpoint, make sure the device already has a Text API content item in its loop task in Dot. App Content Studio.

### Path Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `deviceId` | string | Yes | Device serial number |

### Body Parameters

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `refreshNow` | boolean | No | `true` | Display immediately or queue |
| `taskKey` | string | No | - | Task identifier for multiple text APIs |
| `title` | string | No | - | Title text |
| `message` | string | No | - | Main content text. Supports `\n` and `\t` |
| `signature` | string | No | - | Signature/footer text |
| `icon` | string | No | - | Base64 encoded PNG icon or full http(s) image URL |
| `link` | string | No | - | Tap-to-open link |
| `styles` | object | No | - | Optional typography overrides for `title`, `message`, and `signature` |

### Text Style Object

`styles.title` and `styles.signature` support `fontFamily`, `fontSize`, and `fontWeight`. `styles.message` additionally supports `lineHeight`.

| Field | Type | Required | Range | Description |
|-------|------|----------|-------|-------------|
| `fontFamily` | string | No | See supported fonts | Font family registered by the V2 renderer |
| `fontSize` | number | No | 8-48 | Font size in px |
| `fontWeight` | number | No | 100, 200, 300, 400, 500, 600, 700, 800, 900 | Font weight |
| `lineHeight` | number | No | 0.8-3 | Unitless line height for `styles.message` only |

Supported `fontFamily` values:

`ChillDuanSans`, `ChillKSans`, `ChillKSanslatin`, `ChillOrganic`, `ChillRoundF`, `ChillRoundGothic`, `Cusong16`, `DotGothic16`, `FusionPixel8`, `FusionPixel10`, `FusionPixel12`, `Liusong24`, `LogoSCUnboundedSans`, `MaokenYingBiKaiShuJ0.09`, `PlayfairDisplay`, `Quan8`, `Unifont16`, `UnifontExMono16`, `XiaoyaPixel12`, `Zihunzhoukesong`, `Zpix12`.

Use `\n` for new lines and `\t` for tabs in the JSON payload. If the JSON is wrapped inside another string literal, escape them as `\\n` and `\\t` in that outer layer.

### Example Request

```bash
curl -X POST \
  https://dot.mindreset.tech/api/authV2/open/device/ABCD1234ABCD/text \
  -H 'Authorization: Bearer dot_app_<your_key>' \
  -H 'Content-Type: application/json' \
  -d '{
    "title": "验证码小助手",
    "message": "一个来自「少数派」的验证码\n205112",
    "signature": "2025年8月4日 19:58",
    "styles": {
      "title": { "fontFamily": "ChillDuanSans", "fontSize": 30, "fontWeight": 700 },
      "message": { "fontFamily": "FusionPixel12", "fontSize": 22, "lineHeight": 1.25 },
      "signature": { "fontFamily": "ChillDuanSans", "fontSize": 16 }
    }
  }'
```

### Response

```json
{
  "code": 200,
  "message": "设备文本 API 内容已切换",
  "result": {
    "message": "设备 ABCD1234ABCD 文本 API 内容已切换"
  }
}
```

---

## Display Image

Display image content on the device.

```http
POST /api/authV2/open/device/:deviceId/image
```

> Before calling this endpoint, make sure the device already has an Image API content item in its loop task in Dot. App Content Studio.

### Path Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `deviceId` | string | Yes | Device serial number |

### Body Parameters

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `refreshNow` | boolean | No | `true` | Display immediately or queue |
| `taskKey` | string | No | - | Task identifier for multiple image APIs |
| `image` | string | Yes | - | Base64 encoded PNG image data or full http(s) image URL |
| `link` | string | No | - | Tap-to-open link |
| `border` | number | No | `0` | Screen border color: 0=white, 1=black |
| `ditherType` | string | No | `"DIFFUSION"` | Dither type: DIFFUSION, ORDERED, NONE |
| `ditherKernel` | string | No | `"FLOYD_STEINBERG"` | Dither algorithm |

### Dither Algorithms

- `THRESHOLD`
- `ATKINSON`
- `BURKES`
- `FLOYD_STEINBERG` (default)
- `SIERRA2`
- `STUCKI`
- `JARVIS_JUDICE_NINKE`
- `DIFFUSION_ROW`
- `DIFFUSION_COLUMN`
- `DIFFUSION_2D`

### Example Request

```bash
curl -X POST \
  https://dot.mindreset.tech/api/authV2/open/device/ABCD1234ABCD/image \
  -H 'Authorization: Bearer dot_app_<your_key>' \
  -H 'Content-Type: application/json' \
  -d '{
    "image": "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mP8z8BQDwAEhQGAhKmMIQAAAABJRU5ErkJggg==",
    "border": 0,
    "ditherType": "DIFFUSION",
    "ditherKernel": "FLOYD_STEINBERG"
  }'
```

### Response

```json
{
  "code": 200,
  "message": "设备图像 API 内容已切换",
  "result": {
    "message": "设备 ABCD1234ABCD 图像 API 内容已切换"
  }
}
```

---

## List Device Tasks

Get a list of tasks/content for a specific device.

```http
GET /api/authV2/open/device/:deviceId/:taskType/list
```

### Path Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `deviceId` | string | Yes | Device serial number |
| `taskType` | string | Yes | Content type: `loop` or `fixed` |

### Response

```json
[
  {
    "type": "TEXT_API",
    "key": "text_task_1",
    "refreshNow": true,
    "title": "Hello",
    "message": "World"
  },
  {
    "type": "IMAGE_API",
    "key": "image_task_1",
    "refreshNow": true,
    "border": 0,
    "ditherType": "DIFFUSION",
    "ditherKernel": "FLOYD_STEINBERG"
  }
]
```

| Field | Type | Description |
|-------|------|-------------|
| `type` | string | Content type: `TEXT_API`, `IMAGE_API`, or `GENERAL` |
| `key` | string \| null | Task unique identifier (use as `taskKey` parameter) |

---

## Error Codes

| HTTP Status | Description |
|-------------|-------------|
| `200` | Success |
| `401` | Unauthorized - Invalid API key |
| `404` | Not Found - Device not found |
| `429` | Too Many Requests - Rate limit exceeded |
| `500` | Internal Server Error |
