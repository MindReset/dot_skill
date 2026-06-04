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
  "message": "Device ABCD1234ABCD content switched."
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
| `taskAlias` | string \| number | No | - | Human-readable task name shown in the device task list. Max 100 characters |
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
    "taskAlias": "验证码",
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
  "message": "Device ABCD1234ABCD text API content switched."
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
| `taskAlias` | string \| number | No | - | Human-readable task name shown in the device task list. Max 100 characters |
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
    "taskAlias": "Photo",
    "image": "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mP8z8BQDwAEhQGAhKmMIQAAAABJRU5ErkJggg==",
    "border": 0,
    "ditherType": "DIFFUSION",
    "ditherKernel": "FLOYD_STEINBERG"
  }'
```

### Response

```json
{
  "message": "Device ABCD1234ABCD Image API content switched."
}
```

---

## Display Canvas

Display a custom Canvas API layout on the device.

```http
POST /api/authV2/open/device/:deviceId/canvas
```

> Before calling this endpoint, make sure the device already has a Canvas API content item in its loop task in Dot. App Content Studio.

### Path Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `deviceId` | string | Yes | Device serial number |

### Body Parameters

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `refreshNow` | boolean | No | `true` | Display immediately or queue |
| `taskKey` | string | No | - | Task identifier for multiple canvas APIs |
| `taskAlias` | string \| number | No | - | Human-readable task name shown in the device task list. Max 100 characters |
| `data` | object | No | `{}` | Plain JSON values that the layout reads at render time |
| `windowData` | object | Yes | - | React object-like render tree with a `default` layer array |
| `layoutFull` | object | No | - | FULL layout override with optional `tw` and `style` |
| `link` | string | No | - | Tap-to-open link |
| `border` | number | No | `0` | Screen border color: 0=white, 1=black |

Canvas API is the preferred endpoint for custom cards, dashboards, status panels, and other layouts that need more structure than Text API but should not require pre-rendering a complete image locally like Image API.

Canvas API requests combine content values with an object-like React render tree. Use `data` for values the screen can read, `windowData` for the element tree, `layoutFull` for FULL layout overrides, `taskAlias` for the task-list name, `link` for tap-to-open behavior, and `border` for the screen border color.

For Text API, Image API, and Canvas API, use top-level `taskAlias` when the content should have a human-readable name in the device task list. Omit `taskAlias` to keep the existing task name. Send `taskAlias: ""` or `taskAlias: null` only when intentionally clearing the task name.

### Canvas Composition Model

Build `windowData` as JSON, not JSX, JavaScript, raw HTML, external CSS, or an image. CSS-like styling belongs in `props.style` or `props.tw`. The root must be:

```json
{
  "default": [
    {
      "type": "div",
      "props": {
        "tw": "flex flex-col flex-1 bg-white text-black",
        "children": "Hello Dot."
      }
    }
  ]
}
```

Use this shape for every element:

| Field | Allowed Value |
|-------|---------------|
| `type` | `div`, `span`, or `img` |
| `props` | Object containing render props |
| `props.tw` | Tailwind-like utility classes |
| `props.style` | Inline style object with string or number values |
| `props.children` | String, one element object, or an array of element objects |

For dynamic values, only read from `data` using simple `get` expressions such as `{{get inputData "title" default="-"}}`. Do all computation, filtering, number formatting, date formatting, unit conversion, and string truncation before sending the JSON payload. Do not use arbitrary helpers, JavaScript expressions, function calls, loops, conditions, imports, scripts, CSS files, media queries, browser APIs, or JSX.

Images may use a data URI or an anonymously accessible `http(s)` image URL. Prefer small, stable images. Avoid private network URLs, authenticated URLs, or URLs that require a special Referer.

The outermost Canvas element should usually avoid extra padding because the device layout handles spacing. Use `layoutFull.tw` or `layoutFull.style` for full-bleed rendering, custom background, or padding overrides.

### Canvas Boundaries

Stay inside these server-side validation boundaries:

| Boundary | Limit |
|----------|-------|
| `data` JSON size | 64 KB |
| `windowData` JSON size | 128 KB |
| `layoutFull` JSON size | 8 KB |
| Element count | 80 |
| Nesting depth | 16 |
| String length inside `windowData` | 4000 characters |

Additional constraints:

- `windowData.default` must be an array.
- Allowed element types are only `div`, `span`, and `img`.
- Disallowed prop keys: `dangerouslySetInnerHTML`, `ref`, `srcSet`.
- Disallowed unsafe keys anywhere relevant: `__proto__`, `constructor`, `prototype`.
- Reserved top-level keys inside `data`: `type`, `key`, `windowData`, `layoutFull`, `taskAlias`, `link`, `border`, `__proto__`, `constructor`, `prototype`.

Layout guidance for reliable rendering:

- Prefer one bounded root container with `flex`, `w-full`, `h-full`, and explicit background/text colors.
- Use `min-w-0`, `min-h-0`, fixed heights, `overflow-hidden`, `lineClamp`, `textOverflow`, and `whiteSpace` when text could overflow.
- Keep Tailwind-like classes conservative and concrete. Prefer known layout, spacing, color, border, font, and size utilities over experimental or browser-only CSS.
- For complex dashboards, compose small sections and cards instead of deeply nested decorative structures.
- If a layout becomes too complex for the validation limits, simplify the JSON rather than trying to bypass the limits.

### Supported Styles And Custom Tailwind Classes

Canvas API supports a device-oriented static rendering style surface. The styling boundary is React object-like elements plus a static CSS subset, with Dot.'s custom Tailwind font utilities, breakpoint handling, and image-processing classes.

Use the right layer:

| Syntax | Source | Notes |
|--------|--------|-------|
| `props.style` | Dot Canvas static style subset | Best for deterministic pixel values and explicit styles |
| `props.tw` | Tailwind-like syntax + Dot. extensions | Best for quick layout, color, spacing, font classes, and image-processing classes |
| `layoutFull.tw` / `layoutFull.style` | Dot. layout wrapper override | Use for full-bleed screens, background, and padding overrides |

The `props.style` support list is aligned with the static CSS support table. Dot Canvas style categories include CSS variables, `display`, `position`, `color`, `margin`, `padding`, `top/right/bottom/left`, `width/height`, `minWidth/minHeight/maxWidth/maxHeight`, `border*`, `borderRadius*`, Flexbox, `gap`, `fontFamily`, `fontSize`, `fontWeight`, `fontStyle`, `tabSize`, `textAlign`, `textIndent`, `textTransform`, `textOverflow`, `textDecoration`, `textShadow`, `letterSpacing`, `lineHeight`, `whiteSpace`, `lineClamp`, `wordBreak`, `textWrap`, `backgroundColor`, `backgroundImage`, `backgroundPosition`, `backgroundSize`, `backgroundClip`, `backgroundRepeat`, `transform`, `transformOrigin`, `objectFit`, `objectPosition`, `opacity`, `boxSizing`, `boxShadow`, `overflow`, `filter`, `clipPath`, `mask*`, and `WebkitTextStroke*`.

This style list only describes `props.style`. Font utilities, breakpoint processing, and `img-*` image-processing classes are Dot. custom Tailwind extensions on top of `props.tw`.

Canvas API is not a full browser environment. Do not use `<style>`, external `<link>`, `<script>`, 3D transforms, `z-index`, or `calc()`. `currentColor` is only reliable on the `color` property. Advanced typography and RTL languages are not current stable targets. Canvas API also must not generate JSX, arbitrary JS expressions, React hooks, browser APIs, external CSS, or custom components.

Common `props.tw` classes include `flex`, `flex-row`, `flex-col`, `flex-1`, `shrink-0`, `grow`, `items-*`, `justify-*`, `w-full`, `h-full`, `w-[84px]`, `h-[40px]`, `min-w-0`, `min-h-0`, `max-h-[200px]`, `gap-*`, `gap-[5px]`, `p-*`, `px-[8px]`, `py-[5px]`, `bg-*`, `text-*`, `border*`, `rounded*`, `overflow-hidden`, `box-border`, `box-content`, `fill-black`, and `fill-white`. If a Tailwind class is uncertain, prefer `props.style`.

Font class formats:

- Regular fonts: `text-{size}-{font}`, for example `text-18-chillduansans`
- Regular fonts with px size: `text-[Npx]-{font}`, for example `text-[20px]-playfairdisplay`
- Tailwind size keys: `text-{xs/sm/base/lg/xl/2xl...}-{font}`, for example `text-lg-chillduansans`
- Pixel fonts: `text-pixel-{size}[-variant]`, for example `text-pixel-12-zpix`

Common regular font keys: `chillduansans`, `chillksans`, `chillorganic`, `chillroundf`, `chillroundgothic`, `logoscunboundedsans`, `maokenyingbikaishuj0.09`, `playfairdisplay`, `zihunzhoukesong`.

Pixel font classes: `text-pixel-8`, `text-pixel-8-quan`, `text-pixel-10`, `text-pixel-12`, `text-pixel-12-xiaoya`, `text-pixel-12-zpix`, `text-pixel-16`, `text-pixel-16-cusong`, `text-pixel-16-unifont`, `text-pixel-16-unifontmono`, `text-pixel-24`.

Image elements support e-ink image-processing classes in `img.props.tw`:

- Dither: `img-dither-none`, `img-dither-diffusion`, `img-dither-ordered`
- Kernel: `img-kernel-threshold`, `img-kernel-atkinson`, `img-kernel-burkes`, `img-kernel-floyd-steinberg`, `img-kernel-sierra2`, `img-kernel-stucki`, `img-kernel-jarvis-judice-ninke`, `img-kernel-diffusion-row`, `img-kernel-diffusion-column`, `img-kernel-diffusion-2d`
- Color levels: `img-levels-2`, `img-levels-3`, `img-levels-4`, `img-levels-8`, `img-levels-16`

### Example Request

```bash
curl -X POST \
  https://dot.mindreset.tech/api/authV2/open/device/ABCD1234ABCD/canvas \
  -H 'Authorization: Bearer dot_app_<your_key>' \
  -H 'Content-Type: application/json' \
  -d '{
    "taskAlias": "Canvas Demo",
    "data": {
      "title": "Canvas API",
      "message": "Hello Dot."
    },
    "windowData": {
      "default": [
        {
          "type": "div",
          "props": {
            "tw": "flex flex-col flex-1 bg-white text-black gap-[8px]",
            "children": [
              {
                "type": "div",
                "props": {
                  "tw": "text-28-chillduansans font-bold",
                  "children": "{{get inputData \"title\"}}"
                }
              },
              {
                "type": "div",
                "props": {
                  "tw": "text-18-chillduansans",
                  "children": "{{get inputData \"message\"}}"
                }
              }
            ]
          }
        }
      ]
    },
    "layoutFull": {
      "tw": "p-0 bg-white",
      "style": {
        "padding": 0
      }
    },
    "border": 0
  }'
```

### Response

```json
{
  "message": "Device ABCD1234ABCD Canvas API content switched."
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
  },
  {
    "type": "CANVAS_API",
    "key": "canvas_task_1",
    "border": 0,
    "link": "https://dot.mindreset.tech"
  }
]
```

| Field | Type | Description |
|-------|------|-------------|
| `type` | string | Content type: `TEXT_API`, `IMAGE_API`, `CANVAS_API`, or `GENERAL` |
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
