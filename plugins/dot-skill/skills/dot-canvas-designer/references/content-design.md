# Content design for small displays

Start from what the viewer needs to know, then choose the layout. These are design decisions, not extra fields to add to the Canvas payload.

## Establish the content

Write one sentence: “At a glance, the viewer learns [primary fact] about [subject].” If it contains unrelated goals, choose one or split the content.

Resolve the following from the request and available public data before asking questions:

| Decision | What to establish |
| --- | --- |
| Subject and audience | Who reads this, and what decision or observation should it support? |
| Data | Actual sample values, their paths and types, units, timestamps, source, and attribution |
| Target | Device, orientation, usable dimensions, palette, refresh behavior, and delivery route |
| Language | Requested locales, glyph coverage, date/number formats, and realistic text lengths |
| Interaction | The exact source item or useful destination, only if the selected route supports it |
| States | Normal, empty, missing optional values, stale data, and source failure |

Ask only for missing choices that materially change the result. Distinguish supplied facts, assumptions, and verified behavior. Never fill a live display with invented values; keep sample data explicitly confined to examples or previews.

## Choose the content unit

| Family | Composition |
| --- | --- |
| Editorial | Source or context, dominant headline, restrained time or attribution |
| Metric or status | Subject, one primary value, unit and useful comparison |
| List or table | Concise title, aligned bounded rows, source or freshness cue |
| Forecast or timeline | Current or next event first, ordered future points second |
| Quote or learning | Readable statement, attribution or translation |
| Profile | Stable identity, current state, supporting metadata |

Branding may identify the source, but must not replace the information the viewer came for.

## Set an information budget

- P0: the primary fact and the context required to understand it.
- P1: information that changes its interpretation, such as unit, location, time, or comparison.
- P2: optional detail, repeated labels, decoration, and secondary metadata.

For less space, remove P2, reduce P1 rows, shorten labels, and reflow before shrinking P0. With more space, add useful detail or breathing room. Do not add filler or enlarge every label.

Compact screens usually need one fact and its context. Square screens work well with one focal point. Wide screens can support comparison or short rows. Tall screens can add a readable detail trail without becoming an app page.

## Data and states

Bind each visible value to a real field in Canvas `data`, accessed through the documented `inputData` expressions. Prepare sorting, network access, calculations, and data cleanup outside the display tree. Use only the public helpers in [windowdata.md](windowdata.md).

| State | Display behavior |
| --- | --- |
| Empty list | An honest empty message in the list's visual region |
| Missing optional value | Omit its label or region, or use a meaningful default |
| Stale data | Preserve useful last-known content with an accurate time or stale cue |
| Failed source | A concise unavailable state; never substitute a fabricated measurement |
| Missing image | Remove or replace its slot without displacing the primary fact |

Keep state typography and hierarchy consistent with normal content. Do not let optional fields leave dangling separators. Keep units and timestamps when their removal would mislead.

## Language and interaction

Share the layout when only copy changes. Recompose only when language length or reading order requires it. Check realistic long titles, source names, dates, numbers, CJK punctuation, and mixed Latin/CJK text.

Use a source item's exact destination when the content offers a follow-up action. Canvas uses the public top-level `link` field; do not invent child click handlers or navigation controls. When no useful action exists, omit it.

## Deliverable

Return the requested layout, representative data, target assumptions, and relevant empty or failure behavior. State what was actually previewed. Do not describe an unrendered design as verified on hardware. Use [display-design.md](display-design.md) for composition and the existing public examples for JSON syntax.
