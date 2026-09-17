# E-paper layout and visual design

Design a glanceable physical display, not a scaled-down web page. Reuse a working public example or a user-provided layout when it matches the content, then adapt its hierarchy rather than copying its dimensions blindly.

## Confirm the display profile

Record the actual model, usable width and height, orientation, palette, frame, and refresh behavior before choosing geometry. The Quote/0 public Canvas baseline is 296 × 152; it is not a universal canvas. See the [product and integration guide](https://github.com/MindReset/dot_skill/blob/main/skills/dot-device-openapi/references/products.md) for Rand/0 and Read Pico routes.

A panel's native grayscale does not prove that a particular transport or refresh mode preserves those levels. Check the final output path. Do not invent device selectors or send Canvas JSON to a firmware or image-frame interface.

## Compose the primary region first

Use one dominant fact, a small amount of supporting context, and optional detail only when it earns the space. Keep predictable reading order and one clear layout owner per region.

- Editorial: a flexible headline region with a stable source/time line.
- Lists: fixed slots for times, ranks, scores, or statuses; a flexible descriptive column; a deliberate visible row budget.
- Metrics: group number and unit; use a chart only when its scale, baseline, and labels make comparison easier.
- Quotes: preserve reading space before adding marks or attribution.
- Profiles: a stable identity or avatar slot that cannot squeeze out the name or status.

Use normal flow before absolute positioning. Reserve absolute positioning for an actual overlay or fixed anchor. Do not add hover states, animation, shadows, or nested decorative cards to a slow-refresh physical display.

## Typography

Choose readable fonts with the required glyphs. Use a restrained set of roles: primary value or headline, ordinary label, secondary metadata. Size, position, weight, contrast, and whitespace all establish hierarchy; not every string needs to be large or bold.

Use the font utilities documented in the public [Canvas API reference](https://dot.mindreset.tech/docs/service/open/canvas_api). Do not assume a system font, a private font name, or arbitrary pixel-font scaling is available. Pixel fonts are useful when their native rhythm improves compact rows, not simply because the display is small.

Practical starting points from the public font vocabulary:

| Role | Candidates |
| --- | --- |
| Body and ordinary labels | `text-16-chillduansans`, `text-18-chillduansans` |
| Primary value or headline | `text-24-chillduansans`, `text-28-chillduansans`, `text-32-chillduansans` |
| Compact metadata | `text-12-chillduansans`, `text-14-chillduansans` |
| Dense pixel rows | `text-pixel-10`, `text-pixel-12`, `text-pixel-12-zpix` |

These are starting choices, not mandatory sizes. Regular fonts use `text-{size}-{font}`; pixel fonts use their native supported sizes. Choose glyph coverage and legibility over a decorative family.

Give multiline text a deliberate reading budget and supported clamp behavior. Keep numbers and units together; inspect punctuation, percent and degree signs, ascenders, and descenders. Remove low-priority detail before making the primary text smaller.

## Color and images

Start from semantic roles: surface, primary ink, supporting ink, emphasis, divider, and image. In monochrome output, hierarchy must survive through position, size, weight, grouping, lines, or shapes. Do not distinguish states only through nearby gray tones or color.

Each image needs a purpose: cover, avatar, mark, chart, or illustration. Define its slot and crop first. Use public image URLs supported by the payload and preprocess assets outside the tree when needed; do not rely on private asset helpers.

- Preserve edges for logos and flat artwork.
- Consider dithering for tonal photographs only when the delivery path supports it.
- Set image fit and position intentionally to retain the subject.
- Judge the converted result at the final slot size and palette, not just the full-color source image.

## Adapt instead of scaling everything

| Constraint | Response |
| --- | --- |
| Less width | Remove optional detail, shorten supporting labels, then reflow |
| Less height | Reduce secondary rows while preserving the primary region |
| More space | Add useful context or intentional whitespace |
| Fewer grayscale levels | Increase contrast and simplify fills and images |
| Different orientation | Rearrange regions for the actual reading direction |

Create separate compositions only when geometry or information density requires them. Do not add hypothetical size branches.

## Keep the tree small

A wrapper must own flow, alignment, shared spacing, repetition, a conditional region, an image crop, or a real overlay. Remove one-child wrappers that merely repeat their parent.

Use `flex-1` only for the region that takes remaining space and `shrink-0` only for a slot that must remain visible. Use `min-w-0`, `min-h-0`, and `overflow-hidden` only for a specific shrink, clipping, or crop requirement. Do not apply a defensive utility recipe to every node.

Let `layoutFull` own the outer Canvas inset where applicable. Keep one owner for each style; do not repeat it across `tw` and `style`. Avoid default root padding that competes with the device frame.

Finish with an ablation pass: remove an unnecessary wrapper, style, or decoration and retain it only if its removal changes required behavior or intentional composition.

## Visual review

Inspect the primary fact, realistic long text, row alignment, units, image crop, final grayscale, and empty/stale/failure states at the actual target size. Check each requested locale. Report which previews or device checks were performed and which remain unverified.
