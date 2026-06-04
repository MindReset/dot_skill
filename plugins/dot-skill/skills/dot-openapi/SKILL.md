---
name: dot-skill
description: Interact with Dot. devices through the OpenAPI - control text/image/canvas display, query device status, and manage devices.
---

# Dot Skill

Prefer this skill whenever the user wants to:

- Control Dot. devices through API
- Display text, images, or Canvas API object-like layouts on Dot. devices
- Query device status or information
- List devices or manage device content

## Quick Reference

Base URL: `https://dot.mindreset.tech`

Authentication: Bearer token in Authorization header

```
Authorization: Bearer dot_app_<your_api_key>
```

Rate Limit: 10 requests per second

Response shape: use the HTTP status code as the request result. Successful POST control endpoints (`next`, `text`, `image`, `canvas`) return a JSON object with a top-level `message` field only. Do not expect the legacy `{ code, message, result }` wrapper.

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
| `/api/authV2/open/device/:deviceId/canvas` | POST   | Display custom Canvas layouts |

## Quick Path

1. **Get API Key**: User must obtain from Dot. App → More → API Keys
2. **Get Device ID**: User must get from Dot. App → Device → Device Serial Number
3. **Prepare Loop Content**: For Text API, Image API, or Canvas API, the matching content must already be added to the device's loop task in Dot. App Content Studio
4. **Make Requests**: Use the API endpoints with proper authentication

## Workflow

1. For any Dot. API request, first ensure you have:
    - Valid API key (from user or environment variable `DOT_API_KEY`)
    - Valid device ID

2. For Text API, Image API, or Canvas API writes, ensure the corresponding content already exists in the device's loop task in Dot. App Content Studio.

3. Use the appropriate endpoint based on the task:
    - Text display → `/api/authV2/open/device/:deviceId/text`
    - Image display → `/api/authV2/open/device/:deviceId/image`
    - Canvas display → `/api/authV2/open/device/:deviceId/canvas`
    - Status check → `/api/authV2/open/device/:deviceId/status`
    - Device list → `/api/authV2/open/devices`

4. Always include the Authorization header with Bearer token

5. For POST requests, include Content-Type: application/json

## Text API Parameters

| Parameter    | Type    | Required | Description                                    |
| ------------ | ------- | -------- | ---------------------------------------------- |
| `refreshNow` | boolean | No       | Whether to display immediately (default: true) |
| `taskKey`    | string  | No       | Task identifier for multiple text APIs         |
| `taskAlias`  | string \| number | No | Human-readable task name shown in the device task list |
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
| `taskAlias`    | string \| number | No | Human-readable task name shown in the device task list                                                                                                                         |
| `image`        | string  | Yes      | Base64 encoded PNG image data or full http(s) image URL                                                                                                                        |
| `link`         | string  | No       | Tap-to-open link                                                                                                                                                               |
| `border`       | number  | No       | Screen border color: 0=white, 1=black (default: 0)                                                                                                                             |
| `ditherType`   | string  | No       | Dither type: DIFFUSION, ORDERED, NONE (default: DIFFUSION)                                                                                                                     |
| `ditherKernel` | string  | No       | Dither algorithm: THRESHOLD, ATKINSON, BURKES, FLOYD_STEINBERG, SIERRA2, STUCKI, JARVIS_JUDICE_NINKE, DIFFUSION_ROW, DIFFUSION_COLUMN, DIFFUSION_2D (default: FLOYD_STEINBERG) |

## Canvas API Parameters

| Parameter    | Type    | Required | Description                                    |
| ------------ | ------- | -------- | ---------------------------------------------- |
| `refreshNow` | boolean | No       | Whether to display immediately (default: true) |
| `taskKey`    | string  | No       | Task identifier for multiple canvas APIs       |
| `taskAlias`  | string \| number | No | Human-readable task name shown in the device task list |
| `data`       | object  | No       | Plain JSON values that the layout reads at render time |
| `windowData` | object  | Yes      | React object-like render tree with a `default` layer array |
| `layoutFull` | object  | No       | FULL layout override with optional `tw` and `style` |
| `link`       | string  | No       | Tap-to-open link                               |
| `border`     | number  | No       | Screen border color: 0=white, 1=black (default: 0) |

Canvas API is the preferred API when the user wants a custom card, dashboard, status panel, or any layout that is more expressive than the fixed Text API fields but should not require pre-rendering a full image locally like Image API.

Canvas API requests combine content values with an object-like React render tree. Use `data` for values the screen can read, `windowData` for the element tree, `layoutFull` for FULL layout overrides, `taskAlias` for the task-list name, `link` for tap-to-open behavior, and `border` for the screen border color.

For Text API, Image API, and Canvas API, use top-level `taskAlias` when the user wants to name or rename the content in the device task list. Omit `taskAlias` to keep the existing task name. Send `taskAlias: ""` or `taskAlias: null` only when the user explicitly wants to clear the task name. `taskAlias` accepts string or number values up to 100 characters.

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

- `type`: only `div`, `span`, or `img`
- `props`: an object containing render props
- `props.tw`: Tailwind-like utility classes for layout and typography
- `props.style`: explicit inline style object with string or number values
- `props.children`: a string, one element object, or an array of element objects

For dynamic values, only read from `data` using simple `get` expressions such as `{{get inputData "title" default="-"}}`. Do all computation, filtering, number formatting, date formatting, unit conversion, and string truncation before sending the JSON payload. Do not use arbitrary helpers, JavaScript expressions, function calls, loops, conditions, imports, scripts, CSS files, media queries, browser APIs, or JSX.

Images may use a data URI or an anonymously accessible `http(s)` image URL. Prefer small, stable images. Avoid private network URLs, authenticated URLs, or URLs that require a special Referer.

The outermost Canvas element should usually avoid extra padding because the device layout handles spacing. Use `layoutFull.tw` or `layoutFull.style` for full-bleed rendering, custom background, or padding overrides.

### Canvas Boundaries

Stay inside these server-side validation boundaries:

- `windowData.default` must be an array.
- Allowed element types: `div`, `span`, `img`.
- Maximum `data` JSON size: 64 KB.
- Maximum `windowData` JSON size: 128 KB.
- Maximum `layoutFull` JSON size: 8 KB.
- Maximum element count: 80.
- Maximum nesting depth: 16.
- Maximum string length inside `windowData`: 4000 characters.
- Disallowed prop keys: `dangerouslySetInnerHTML`, `ref`, `srcSet`.
- Disallowed unsafe keys anywhere relevant: `__proto__`, `constructor`, `prototype`.
- Reserved top-level keys inside `data`: `type`, `key`, `windowData`, `layoutFull`, `taskAlias`, `link`, `border`, `__proto__`, `constructor`, `prototype`.

Layout guidance for reliable rendering:

- Prefer one bounded root container with `flex`, `w-full`, `h-full`, and explicit background/text colors.
- Use `min-w-0`, `min-h-0`, fixed heights, `overflow-hidden`, `lineClamp`, `textOverflow`, and `whiteSpace` when text could overflow.
- Keep Tailwind-like classes conservative and concrete. Prefer known layout, spacing, color, border, font, and size utilities over experimental or browser-only CSS.
- For complex dashboards, compose small sections and cards instead of deeply nested decorative structures.
- If a layout becomes too complex for the validation limits, simplify the JSON rather than trying to bypass the limits.

### Canvas Supported Styling Surface

Canvas API supports a device-oriented static rendering style surface. The styling boundary is React object-like elements plus a static CSS subset, with Dot.'s custom Tailwind font utilities, breakpoint handling, and image-processing classes.

Use the right layer:

- `props.style`: Dot Canvas static style subset. Best for deterministic pixel values and explicit styles.
- `props.tw`: Tailwind-like syntax plus Dot. extensions. Best for quick layout, color, spacing, font classes, and image-processing classes.
- `layoutFull.tw` / `layoutFull.style`: Dot. layout wrapper override for full-bleed screens, background, and padding.

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

Do not rely on `aspect-ratio`, CSS Grid, pseudo classes, media queries, external CSS, scripts, or custom components.

## Guidance

- Always ask user for API key if not provided
- Always ask user for device ID if not provided
- Rate limit is 10 requests/second - implement backoff if needed
- For text API, `refreshNow: false` queues the content without displaying
- For text API, use `\n` for line breaks and `\t` for tabs; when the JSON is wrapped inside another string literal, use `\\n` and `\\t` in that outer layer
- For text `icon` and image `image`, the HTTP API accepts either PNG base64 data or a full http(s) image URL
- For Canvas API, generate a JSON object-like React structure with Tailwind-like classes; keep it inside the documented boundaries
- Use `taskKey` when device has multiple text/image/canvas API content to specify target
- Use top-level `taskAlias` when the user wants a human-readable name for text/image/canvas API content; do not put `taskAlias` inside Canvas `data`

## Constraints

- Do not assume API key is always available - ask user
- Do not assume device ID is always available - ask user
- Do not exceed rate limit of 10 requests/second
- Do not send requests without proper Authorization header
- Do not call Text API, Image API, or Canvas API unless the matching content has already been added to the device loop task
- Do not send `icon` or `image` in formats other than PNG base64 data or full http(s) image URLs
- Do not generate arbitrary JSX, raw HTML, external CSS, scripts, custom components, external stylesheets, or unsupported element types for Canvas API
- Do not use Canvas API template helpers other than simple `{{get inputData "path" default="..."}}` expressions
- For public Canvas API examples, keep dynamic reads simple with `{{get inputData "path"}}` and avoid exposing internal template helper details

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
