# Pitfalls

Hard-won mistakes from real 提需 runs. Check this list before finishing a batch.

## Scene and fields

- **Do not invent scene details.** A scene written as "户外" stays "户外". Never add
  "傍晚 / 老建筑 / 路灯亮起 / 夕阳光线" that the table did not ask for.
- Use the table's literal text for 场景 and 车型. Do not elaborate.
- Color: if the table specifies one, force it. If empty, inherit the reference-image car
  color. Never guess a color such as "银灰色".

## Count and cars

- `batch_count` = 数量 column, exactly. Generate every requested image, not only the first.
- One car per image — no extra vehicles, no background vehicles.

## Prompt roles

- The car-body image belongs in position **图2**, and the prompt must state that 图2's body
  structure stays unchanged. Otherwise some outputs come out with a warped or wrong body.
- Do not write "keep 图2's EM90 body structure unchanged" when the reference car is actually
  a different model — the instruction must say to **swap** the reference car for the target car.
- 图1 = 提需参考图 (scene + composition + original paint). 图3 = car body only in the
  scene-swap template. Keep the numbering straight per template.

## Door handles and lights

- Hidden door handle: handle out → headlights on; handle flush → headlights off. Applies to
  L6 and EM90 and similar.

## Data handling

- Do not parse CSV with `line.split(",")` — multi-line fields break it. Use `csv.reader`.
- Embedded reference images are cell-embedded; `+csv-get` cannot see them. Use `+cells-get`
  and read the `image_token` from `rich_text`.
- Download embedded images to a **relative** output path, not an absolute one.

## Angles

- Determine angle by exposed side (left / right) + face (front / rear), not by brightness
  analysis (lighting misleads).
- Confirm views with the user before running a batch — guessing wastes tokens.

## Canvas

- Never skip the connect step before triggering generation.
- Verify node IDs via a list call; POST-returned IDs may not really exist.
- No DELETE API exists — clean up manually in the web UI, and run new versions in a fresh
  y region.

## Car package correctness

- Confirm the car package folder actually contains the model it claims. A past example: an
  `XC70/` folder was filled entirely with `EX90` images, so every "XC70" output was an EX90.
  Verify the model before trusting the folder name.
