---
name: dot-canvas-designer
description: Design Dot. Canvas API windowData layouts - JSON element trees, layout, styles, list rendering, conditions, and display formatting.
---

# Dot Canvas Designer

Use this skill when the user wants to design or revise a Dot. Canvas API card, dashboard, status panel, or `windowData` layout.

Do not use this skill merely to send an existing payload to a device. For device operations, use `dot-device-openapi`.

## Output Boundary

Produce a Canvas payload or a `windowData` object. Do not handle API keys, device IDs, or device sending here.

When the user asks to design and send a Canvas card:

1. Use this skill to build the Canvas payload.
2. Use `dot-device-openapi` to send it.

## Composition Model

Build `windowData` as JSON, not JSX, JavaScript, raw HTML, external CSS, or an image.

Root shape:

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

Element shape:

- `type`: `div`, `span`, or `img`
- `props`: render props
- `props.tw`: Tailwind-like utility classes
- `props.style`: explicit inline style object
- `props.children`: a string, one element object, or an array of element objects

Dynamic values should read Canvas `data` through simple `get` expressions such as `{{get inputData "title" default="-"}}`.

## Supported Template Logic

Use stable display-layer helpers only:

- `$for` / `$empty`: list structures
- `$ifAny` / `$then` / `$else`: structural conditions
- `if` / `else`: short content branches based on whether a value has content
- `compare`: short text branches
- `formatDate`: date display
- `formatCompactNumber`: number display
- `get`: read JSON paths

Avoid internal cleaning or transformation helpers such as `imageSrc`, `stripHtml`, `math`, or `regexMatch` in public Canvas payloads. Do data cleanup and heavy computation before building the JSON payload.

## Layout Guidance

- Prefer one bounded root container with `flex`, `w-full`, `h-full`, and explicit background/text colors.
- Use `min-w-0`, `min-h-0`, fixed heights, `overflow-hidden`, `lineClamp`, `textOverflow`, and `whiteSpace` when text could overflow.
- The outermost Canvas element usually should not add padding; device layout spacing comes from `layoutFull`.
- Use `layoutFull.tw` or `layoutFull.style` for full-bleed rendering, background, or padding overrides.
- Keep element count and nesting low. Compose clear sections instead of deeply nested decoration.

## References

- `references/windowdata.md`
- `references/examples.md`
