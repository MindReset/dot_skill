# Dot Canvas windowData Reference

Canvas API combines `data` values with a React object-like render tree.

Top-level Canvas send payload:

```json
{
  "data": {
    "title": "Canvas API"
  },
  "windowData": {
    "default": []
  },
  "layoutFull": {
    "tw": "p-0 bg-white",
    "style": {
      "padding": 0
    }
  },
  "border": 0
}
```

## Elements

Allowed element types:

- `div`
- `span`
- `img`

Each element should be:

```json
{
  "type": "div",
  "props": {
    "tw": "flex flex-col",
    "style": {
      "lineHeight": "24px"
    },
    "children": "Text"
  }
}
```

## Dynamic Values

Read values with `get`:

```hbs
{{get inputData "title" default="-"}}
{{get inputData "user.name" default="-"}}
```

## Lists: `$for` / `$empty`

Put `$for` inside the `props` of the node to repeat. The repeated unit is that node itself. `$empty` sits next to `$for` and replaces that node when the array is empty.

```json
{
  "type": "div",
  "props": {
    "$for": {
      "items": "inputData.tasks",
      "as": "task",
      "index": "index"
    },
    "$empty": {
      "type": "div",
      "props": {
        "children": "No tasks"
      }
    },
    "children": "{{index}}. {{get task \"title\" default=\"\"}}"
  }
}
```

`limit` is optional. When omitted, all rows are rendered and the device layout decides how many fit on screen.

## Structural Conditions: `$ifAny` / `$then` / `$else`

Use structural conditions to add, replace, or remove whole elements during JSON compilation.

```json
{
  "$ifAny": ["inputData.icon", "inputData.signature"],
  "$then": {
    "type": "div",
    "props": {
      "children": "{{get inputData \"signature\" default=\"\"}}"
    }
  },
  "$else": {
    "type": "div",
    "props": {
      "children": "No signature"
    }
  }
}
```

## Text Conditions

Use template `if` / `else` syntax for short content branches based on whether a value has content:

```hbs
{{#if (get inputData "title" default="")}}{{get inputData "title"}}{{else}}Untitled{{/if}}
```

Use `compare` when two values must be compared explicitly:

```hbs
{{#compare inputData.status "===" "done"}}Done{{else}}In progress{{/compare}}
```

## Formatting

Dates:

```hbs
{{formatDate inputData.date "yyyy/MM/dd" "Asia/Shanghai"}}
{{formatDate inputData.date "EEE" "Asia/Shanghai"}}
```

Numbers:

```hbs
{{formatCompactNumber inputData.count}}
{{formatCompactNumber inputData.count "en-US" "standard" 0}}
```

## Styling

Use `props.tw` for Tailwind-like classes and `props.style` for explicit values.

Common `props.tw` classes:

- `flex`, `flex-row`, `flex-col`, `flex-1`, `shrink-0`, `grow`
- `items-*`, `justify-*`
- `w-full`, `h-full`, `w-[84px]`, `h-[40px]`
- `min-w-0`, `min-h-0`, `max-h-[200px]`
- `gap-*`, `gap-[5px]`, `p-*`, `px-[8px]`, `py-[5px]`
- `bg-*`, `text-*`, `border*`, `rounded*`
- `overflow-hidden`, `box-border`, `box-content`, `fill-black`, `fill-white`

Use `props.style` for deterministic CSS subset values such as `display`, `position`, `color`, `margin`, `padding`, `width`, `height`, `borderRadius`, Flexbox, `gap`, `fontSize`, `fontWeight`, `textAlign`, `textOverflow`, `letterSpacing`, `lineHeight`, `whiteSpace`, `lineClamp`, `backgroundColor`, `objectFit`, `opacity`, `boxSizing`, `overflow`, `filter`, `clipPath`, and `mask*`.

Image elements support e-ink image processing classes in `img.props.tw`:

- Dither: `img-dither-none`, `img-dither-diffusion`, `img-dither-ordered`
- Kernel: `img-kernel-threshold`, `img-kernel-atkinson`, `img-kernel-burkes`, `img-kernel-floyd-steinberg`, `img-kernel-sierra2`, `img-kernel-stucki`, `img-kernel-jarvis-judice-ninke`, `img-kernel-diffusion-row`, `img-kernel-diffusion-column`, `img-kernel-diffusion-2d`
- Color levels: `img-levels-2`, `img-levels-3`, `img-levels-4`, `img-levels-8`, `img-levels-16`

## Boundaries

- `windowData.default` must be an array.
- `data` JSON size <= 64 KB.
- `windowData` JSON size <= 128 KB.
- `layoutFull` JSON size <= 8 KB.
- Element count <= 80.
- Nesting depth <= 16.
- String length inside `windowData` <= 4000 characters.
- Disallowed prop keys: `dangerouslySetInnerHTML`, `ref`, `srcSet`.
- Disallowed unsafe keys: `__proto__`, `constructor`, `prototype`.
- Reserved top-level keys inside `data`: `type`, `key`, `windowData`, `layoutFull`, `taskAlias`, `link`, `border`, `__proto__`, `constructor`, `prototype`.
