# Workflow and TAI.lab API

## TAI.lab config

| Item | Value |
|---|---|
| Base URL | `http://aigc-gen-video.tarsocial.com` |
| Project ID | 87 |
| Canvas ID | 91 |
| Auth | JWT Bearer token, stored in the workspace `.tailab_config.json` |
| Output params (提需) | provider=`nano`, model=`banana`, resolution=`4K`, aspect_ratio=`3:4`, `batch_count` = 数量 |

Canvas UI: `http://aigc-gen-video.tarsocial.com/canvas/projects/87`

## API endpoints

| Purpose | Method + path |
|---|---|
| Upload asset | `POST /api/canvas/assets/upload` (form: `file` + `asset_type=image`) |
| Create node | `POST /api/canvas/canvases/91/nodes` (`node_type=image_asset` or `image_gen`) |
| Connect edge | `POST /api/canvas/canvases/{id}/edges` (`edge_type=reference`) |
| Trigger generation | `POST /api/canvas/nodes/{id}/run-image` (body `{"trigger":"manual"}`) |
| Status / download | `GET /api/canvas/nodes/{id}/runtime` (returns `node_status`, `progress_percent`, `result_json.preview_urls`) |

## Strict execution order

Never trigger before the edge exists. Skipping step 5 breaks the run (node missing, trigger
error, or output that ignores the reference).

```
[1] upload assets (car image + reference image)   POST /api/canvas/assets/upload
[2] create image_asset node                        POST /api/canvas/canvases/{id}/nodes  (node_type=image_asset)
[3] create image_gen node                          POST /api/canvas/canvases/{id}/nodes  (node_type=image_gen)
[4] verify the nodes really exist (list call)      GET  /api/canvas/canvases/{id}/nodes?keyword=xxx
[5] connect edge (asset -> gen)                    POST /api/canvas/canvases/{id}/edges
                                                   body: {canvas_id, source_node_id, target_node_id, edge_type: "reference"}
[6] trigger generation                             POST /api/canvas/nodes/{gen_id}/run-image  body {"trigger":"manual"}
[7] poll runtime                                   GET  /api/canvas/nodes/{gen_id}/runtime
                                                   when node_status == success, read result_json.preview_urls
```

## Node creation must be verified

A POST-returned node ID is not trustworthy — the single-node GET sometimes returns None.
Confirm against the list endpoint.

```python
def create_gen_node(payload):
    r = requests.post(...)
    nid = r.json()["data"]["id"]
    v = requests.get(
        f"{TAILAB}/api/canvas/canvases/91/nodes?page=1&page_size=200", headers=AUTH
    )
    ids = {n["id"] for n in v.json()["data"]}
    if nid not in ids:
        raise RuntimeError(f"node {nid} failed list verification after creation")
    return nid
```

## Edge failure checklist

If `POST /api/canvas/canvases/{id}/edges` returns 403 / 400, check in order:

| # | Check | How |
|---|---|---|
| 1 | source node exists | `GET .../nodes/{source_node_id}` or list |
| 2 | target node exists | same |
| 3 | canvas_id correct | must match the URL path and the nodes' canvas |
| 4 | edge_type correct | literally the string `"reference"` (not `"ref"`, not `"input"`) |
| 5 | direction correct | source = asset (the referenced image), target = image_gen (the consumer) |
| 6 | JWT not expired | the token from `.tailab_config.json` must return 200 for the nodes list |
| 7 | body is JSON not form | send `Content-Type: application/json` via `requests.post(..., json=body)` |

## Canvas layout (keep it tidy)

- Each gen node connects to exactly **2** edges (1 reference image + 1 car-body image).
- Gen node in the middle; the two asset nodes in a row above it.
- Lay columns out **horizontally** (5 columns), do not stack gen nodes vertically.
- Give each new run a **fresh y region** (e.g. y=15000+) so it never overlaps old nodes.
- Horizontal spacing 700px, vertical spacing 300px — edges drop straight down, no crossings.

```
┌────────┐ ┌────────┐ ┌────────┐ ┌────────┐ ┌────────┐
│ ref_1  │ │ ref_2  │ │ ref_3  │ │ ref_4  │ │ ref_5  │
├────────┤ ├────────┤ ├────────┤ ├────────┤ ├────────┤
│ car_1  │ │ car_2  │ │ car_3  │ │ car_4  │ │ car_5  │
└────────┘ └────────┘ └────────┘ └────────┘ └────────┘
    ↓          ↓          ↓          ↓          ↓
┌────────┐ ┌────────┐ ┌────────┐ ┌────────┐ ┌────────┐
│ gen_1  │ │ gen_2  │ │ gen_3  │ │ gen_4  │ │ gen_5  │
└────────┘ └────────┘ └────────┘ └────────┘ └────────┘
```

## Canvas cleanup

TAI.lab has **no DELETE endpoint** for nodes or edges (these all 404):

- `DELETE /api/canvas/nodes/{id}`
- `DELETE /api/canvas/canvases/91/nodes/{id}`
- `DELETE /api/canvas/canvases/91/edges/{id}`

Workaround: delete nodes manually in the TAI.lab web UI (Shift multi-select), and run each
new version in a fresh y region so old work is left untouched.
