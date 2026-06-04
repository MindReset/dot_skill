---
name: dot-openapi
description: Compatibility router for Dot. OpenAPI work. Prefer dot-device-openapi for device operations and dot-canvas-designer for Canvas layout design.
---

# Dot OpenAPI Compatibility Router

This skill remains for backward compatibility with older installs that reference `dot-openapi`.

Prefer the split skills:

- Use `dot-device-openapi` for device interaction:
  - list devices
  - check device status
  - switch to next content
  - list tasks
  - send Text API, Image API, or a finished Canvas API payload
- Use `dot-canvas-designer` for Canvas design:
  - build or revise `windowData`
  - design Canvas cards, dashboards, and status panels
  - use `$for` / `$empty`, `$ifAny` / `$then` / `$else`, `compare`, `formatDate`, and `formatCompactNumber`
  - reason about layout, style, overflow, and rendering boundaries

If a task asks to design and send a Canvas card, use both skills in sequence:

1. `dot-canvas-designer` to produce the Canvas payload.
2. `dot-device-openapi` to send it to the device.

Base URL: `https://dot.mindreset.tech`

Authentication:

```http
Authorization: Bearer dot_app_<your_api_key>
```

OpenAPI schema: `../../openapi/dot-openapi.yaml`
