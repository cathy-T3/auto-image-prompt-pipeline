"""TAI.lab image-generation client.

Implements the strict order: create node -> verify via list -> connect edge ->
trigger -> poll. Never trigger before the edge exists.

Fill in AUTH from the workspace .tailab_config.json. Do not commit the token.
"""
import json
import time
from pathlib import Path

import requests

BASE = "http://aigc-gen-video.tarsocial.com"
CANVAS_ID = 91
CONFIG_PATH = Path.cwd() / ".tailab_config.json"


def load_auth(config_path=CONFIG_PATH):
    token = json.loads(Path(config_path).read_text(encoding="utf-8"))["token"]
    return {"Authorization": f"Bearer {token}"}


AUTH = load_auth() if CONFIG_PATH.exists() else {"Authorization": "Bearer <JWT>"}


def list_node_ids():
    r = requests.get(
        f"{BASE}/api/canvas/canvases/{CANVAS_ID}/nodes",
        params={"page": 1, "page_size": 200},
        headers=AUTH,
    )
    r.raise_for_status()
    return {n["id"] for n in r.json()["data"]}


def upload_asset(path, asset_type="image"):
    with open(path, "rb") as fh:
        r = requests.post(
            f"{BASE}/api/canvas/assets/upload",
            files={"file": fh},
            data={"asset_type": asset_type},
            headers=AUTH,
        )
    r.raise_for_status()
    return r.json()["data"]


def create_node(node_type, payload):
    """Create a node and confirm it exists via the list endpoint."""
    r = requests.post(
        f"{BASE}/api/canvas/canvases/{CANVAS_ID}/nodes",
        json={"node_type": node_type, **payload},
        headers={**AUTH, "Content-Type": "application/json"},
    )
    r.raise_for_status()
    node_id = r.json()["data"]["id"]
    if node_id not in list_node_ids():
        raise RuntimeError(f"node {node_id} failed list verification after creation")
    return node_id


def connect(source_node_id, target_node_id):
    body = {
        "canvas_id": CANVAS_ID,
        "source_node_id": source_node_id,
        "target_node_id": target_node_id,
        "edge_type": "reference",
    }
    r = requests.post(
        f"{BASE}/api/canvas/canvases/{CANVAS_ID}/edges",
        json=body,
        headers={**AUTH, "Content-Type": "application/json"},
    )
    r.raise_for_status()
    return r.json()


def run_image(node_id):
    r = requests.post(
        f"{BASE}/api/canvas/nodes/{node_id}/run-image",
        json={"trigger": "manual"},
        headers={**AUTH, "Content-Type": "application/json"},
    )
    r.raise_for_status()
    return r.json()


def poll(node_id, timeout=600, interval=10):
    deadline = time.time() + timeout
    while time.time() < deadline:
        r = requests.get(f"{BASE}/api/canvas/nodes/{node_id}/runtime", headers=AUTH)
        r.raise_for_status()
        data = r.json()["data"]
        status = data.get("node_status")
        if status == "success":
            return data["result_json"]["preview_urls"]
        if status == "failed":
            raise RuntimeError(f"node {node_id} failed")
        time.sleep(interval)
    raise TimeoutError(f"node {node_id} timed out after {timeout}s")


def generate_one(ref_image_path, car_image_path, prompt, batch_count=1):
    """Full strict-order run for one 提需 row: 2 assets -> 1 gen node -> edge -> run -> poll."""
    ref_asset = upload_asset(ref_image_path)
    car_asset = upload_asset(car_image_path)
    ref_node = create_node("image_asset", {"asset_id": ref_asset["id"]})
    car_node = create_node("image_asset", {"asset_id": car_asset["id"]})
    gen_node = create_node(
        "image_gen",
        {
            "prompt": prompt,
            "batch_count": batch_count,
            "provider": "nano",
            "model": "banana",
            "resolution": "4K",
            "aspect_ratio": "3:4",
            # car body image stays in position 2
            "reference_asset_ids": [ref_node, car_node],
        },
    )
    connect(ref_node, gen_node)
    connect(car_node, gen_node)
    run_image(gen_node)
    return poll(gen_node)
