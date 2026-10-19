---
name: auto-image-prompt-pipeline
description: Build AI image prompts, pull car reference images, and drive the image-gen API from requirement tables. Use for the 提需 car-image workflow. Do not use for KV poster layout design.
---

# Auto Image Prompt Pipeline

Drive the 提需 (requirement) image workflow end to end: read one requirement row from a
Feishu sheet, build a 4K photoreal prompt, locate the car-body reference image by view
angle, wire the reference node to a generation node on TAI.lab, trigger generation, and
download the results.

## When to invoke

Invoke when the user provides a 提需 sheet (or asks to generate car marketing images from
a requirements table) and expects N images per row driven by scene + model + color + count.

Do not invoke for KV poster work — that needs layout design (titles, sub-titles, parameter
grids) and follows a different memory.

## Non-negotiables

1. Read the table literally. Never invent scene details, colors, or angles. A scene written
   as "户外" stays "户外" — do not add "傍晚 / 林间 / 海边".
2. `batch_count` must equal the 数量 column. Generate every requested image, not just the first.
3. One car per image. No extra or background vehicles.
4. Color — if the table specifies a color, force it; if empty, inherit the reference-image
   car color. Never guess (for example, do not assume "银灰色").
5. Wiring order is strict. Never trigger generation before the edge exists — see
   `references/workflow.md`.
6. Verify every created node ID with a list call. A POST-returned ID is not trustworthy.
7. Hidden door handles — handle out means the headlights must be on; handle flush means the
   headlights must be off.
8. Judge car angle by which side (left / right) and which face (front / rear) is exposed,
   never by brightness analysis (lighting interferes).

## Core steps

1. Read the row and map the columns — `references/field-mapping.md`
2. Locate the car-body reference image by view angle — `references/field-mapping.md`
3. Build the prompt — `references/prompt-templates.md`
4. Wire nodes and generate — `references/workflow.md`
5. Download results — `references/workflow.md`

## Prompt sourcing

Write roughly 70% of the prompt yourself; use the AAA library templates only as the skeleton
(about 30%). Do not copy the template verbatim. The car-body image always goes into
position 图2, and the prompt must state that 图2's body structure stays unchanged.

## Before finishing

Run through `references/pitfalls.md`. It lists the hard-won mistakes — invented scenes,
wrong 图2 / 图3 numbering, CSV parsing bugs, canvas cleanup limits, and more.
