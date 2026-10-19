# Field Mapping

## Reading a sheet

Use `lark-cli` with `+cells-get` (not `+csv-get`) — embedded images live in the cell's
`rich_text` as an `image_token` and are invisible to CSV export.

```bash
lark-cli sheets +cells-get \
  --url "https://<host>/wiki/<token>?sheet=<sheet-id>" \
  --sheet-id "<sheet-id>" \
  --range "A1:O20"
```

Known trap: to download an embedded image you must use a **relative** output path, not an
absolute one.

```bash
lark-cli api GET "/open-apis/drive/v1/medias/{token}/download" -o "./ref1.jpg"
```

## Column maps

Column layout varies per workbook. Confirm the header row before reading; the two layouts
seen in practice:

### Layout A — 8.24 sheet (sheet_id `eeFlpB`)

| Field | Column | Empty-value handling |
|---|---|---|
| 场景 scene | C | use the literal text ("户外" / "街景"), do not elaborate |
| 车型 model | D | use as written, do not pad |
| 车色 color | L (车色参考) | if present use it; if empty → "颜色继承参考图" |
| 数量 count | M | `batch_count = M` (exact number) |
| 参考图 refs | E–H (图片示例) | find the embedded image, download |

Example data:

| row | 场景 (C) | 车型 (D) | 车色 (L) | 数量 (M) |
|---|---|---|---|---|
| r1 | 户外 | S90 | (empty → inherit) | 5 |
| r2 | 户外,停车场 | S90 | (empty → inherit) | 3 |
| r3 | 街景 | EM90 | 黑色 | 3 |
| r4 | 户外 | EM90 | 黑色 | 3 |
| r5 | 户外 | S90 | (empty → inherit) | 2 |

### Layout B — 沃尔沃 `4bPmqp` sheet

| Column | Field | Notes |
|---|---|---|
| A | 序号 | 1, 2, 3 … |
| B | 提需人 | e.g. "小猪" |
| C | 场景 | "门店内" / "户外" |
| D | 车型 | "沃尔沃EM90" (strip the prefix → EM90) |
| E–L | 图片示例 | **8** reference images (not 4) |
| M | 需求 / 备注 | multi-line text |
| N | 数量 | image count |
| O | 交付时间 | often empty |

### Layout C — 沃尔沃 `20WHxN` sheet (晶晶)

Reference of a real batch (41 images total). Reconfirm views with the user before running —
the memory records that confirming views up front saves tokens.

| 序号 | model | views (confirmed) | count | note |
|---|---|---|---|---|
| 1 | XC70 | 左后 | 1 | only swap the left car against the wall, black |
| 2 | XC90+S90 | 纯正/纯侧/纯侧/右前 | 4 | two cars (XC90 left, S90 right), white |
| 3 | S90 | 左前/左后/左前 | 3 | inherit color |
| 4 | XC70 | 左前×4 | 4 | pink, inherit |
| 5 | XC40 | 左前×4 | 4 | pink, inherit |
| 6 | XC60+XC40 | 左前 | 1 | one image, two cars (XC60 left, XC40 right) |
| 7 | XC70 | 左前 | 1 | swap a Xiaomi car to XC70 |
| 8–15 | XC40 / XC70 | mixed | … | see original batch notes |

## Car-body reference lookup

Car packages live in a per-model directory, one file per view angle:
`车包/沃尔沃车型/{model}/{view}.webp`.

```python
from pathlib import Path

VIEWS = ["左前", "左后", "右前", "右后", "纯侧", "纯后", "纯正"]


def normalize_car(car):
    c = car.strip()
    for prefix in ("沃尔沃 ", "沃尔沃", "Volvo ", "Volvo"):
        if c.startswith(prefix):
            return c[len(prefix):].strip()
    return c


def find_car_image(car_model, view="左前", root="/Users/mac/Desktop/车包/沃尔沃车型"):
    car_dir = Path(root) / car_model
    if not car_dir.exists():
        return None
    for ext in (".webp", ".jpg", ".jpeg", ".png"):
        p = car_dir / f"{view}{ext}"
        if p.exists():
            return p
    return None
```

## Angle determination

Decide the view by what is physically exposed, not by brightness:

- which side is visible — left / right
- which face is visible — front / rear

Priority for the injected view: the 提需 description first, then a 视角 column in the sheet,
then default 左前.
