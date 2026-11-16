"""Prototype only: a snapshot of the planning folder for prototype/index.html.

Usage: python -I snapshot.py <planning folder> <out data.js>
Walks each CR's whole folder (every file, whatever its name): text shown (cut past 60 KB, and
only listed past 200 KB, like a generated data.js), images inlined up to 400 KB, anything else
listed with its size.
"""
import json, sys, pathlib, base64
root = pathlib.Path(sys.argv[1])          # planning folder
out = pathlib.Path(sys.argv[2])           # data.js
TEXT = {".md", ".json", ".jsonl", ".txt", ".log", ".yml", ".yaml", ".patch", ".diff", ".csv", ".html", ".py", ".sh", ".toml", ".js"}
IMG = {".png": "image/png", ".jpg": "image/jpeg", ".jpeg": "image/jpeg", ".gif": "image/gif", ".svg": "image/svg+xml"}

def folder(rel):
    """Every file of a CR folder, as it is: names are not known in advance."""
    base = root / rel
    files = []
    for p in sorted(base.rglob("*")):
        if not p.is_file():
            continue
        r = p.relative_to(base).as_posix()
        f = {"path": r, "size": p.stat().st_size}
        ext = p.suffix.lower()
        if ext in TEXT and f["size"] <= 60000:
            f["text"] = p.read_text(encoding="utf-8", errors="replace")
        elif ext in TEXT and f["size"] <= 200000:
            f["text"] = p.read_text(encoding="utf-8", errors="replace")[:60000]
            f["cut"] = True
        elif ext in IMG and f["size"] <= 400000:
            f["img"] = "data:%s;base64,%s" % (IMG[ext], base64.b64encode(p.read_bytes()).decode())
        files.append(f)
    return files

st = json.loads((root / "STATUS.json").read_text(encoding="utf-8"))
bj = json.loads((root / "4-batch" / "batch.json").read_text(encoding="utf-8"))
after = {c["id"]: c.get("after") or [] for c in bj["crs"]}
b = st["batches"][0] if st["batches"] else None
batch = None
if b:
    batch = {k: b.get(k) for k in ("batch", "state", "spent_usd", "budget_usd", "asks_unread", "heartbeat",
                                   "heartbeat_stopped", "orders_pending", "slots")}
    batch["mode"] = bj.get("mode"); batch["max_rounds"] = (bj.get("settings") or {}).get("max_rounds")
    batch["default_branch"] = (bj.get("settings") or {}).get("default_branch"); batch["steering"] = bj.get("steering"); batch["created"] = bj.get("created")
    live = {c["cr"]: c for c in b["crs"]}
    batch["crs"] = []
    for c in bj["crs"]:                   # every CR of the batch, merged ones included
        s = live.get(c["id"], {})
        rel = s.get("folder") or c["path"]
        if not (root / rel).is_dir():
            hits = [p for p in root.glob("*/*" + rel.split("/")[-1] + "*") if p.is_dir()] + \
                   [p for p in root.glob("5-archives/*" + rel.split("/")[-1]) if p.is_dir()]
            rel = hits[0].relative_to(root).as_posix() if hits else rel
        batch["crs"].append({
            "cr": c["id"], "title": c["title"], "state": s.get("state") or c["status"], "round": c.get("round", 0),
            "cost": c.get("cost_usd"), "rounds": c.get("rounds"), "pr": c.get("pr"), "waits": s.get("waits", []),
            "blocked": s.get("blocked") or c.get("blocked_reason"), "kind": c.get("kind"),
            "updated": c.get("updated"), "folder": rel, "order": c.get("order"), "stacked": bool(c.get("stacked")),
            "branch": c.get("branch"), "after": after.get(c["id"], []),
            "files": folder(rel) if (root / rel).is_dir() else []})
    ev = [json.loads(l) for l in (root / "4-batch" / "events.jsonl").read_text(encoding="utf-8").splitlines() if l.strip()]
    keep = {"open", "add", "take", "round", "gate", "verdict", "ship", "handback", "ask", "order", "merged", "close", "pause", "note"}
    batch["events"] = [{k: e.get(k) for k in ("t", "actor", "kind", "cr", "result", "pr", "note", "order_kind", "reason", "command", "round")}
                       for e in ev if e.get("kind") in keep][-40:]
seat = root / "seat.json"
seat = json.loads(seat.read_text(encoding="utf-8")) if seat.is_file() else None
items = []
for x in st["backlog"]:
    rel = x["path"]
    if (root / rel).is_file():
        rel = str(pathlib.PurePosixPath(rel).parent)
    items.append({"priority": x["priority"], "item": x["item"], "title": x["title"],
                  "spec": bool(x.get("spec")), "folder": rel, "files": folder(rel)})
merged = [{"cr": x["cr"], "title": x["title"], "batch": x["batch"], "pr": x["pr"],
           "cost": x["cost_usd"], "when": x["when"]} for x in st["merged"][:8]]
snap = {"updated": st["updated"], "batch": batch, "items": items, "merged": merged,
        "merged_total": st["merged_total"], "trashed_total": st.get("trashed_total"),
        "seat": {k: seat.get(k) for k in ("title", "env")} if seat else None}
out.write_text("window.SNAP = " + json.dumps(snap, ensure_ascii=False) + ";\n", encoding="utf-8")
print(len(items), "items;", len(batch["crs"]) if batch else 0, "batch CRs;", out.stat().st_size, "bytes")
print(sorted({x["priority"] for x in items}), [x["folder"] for x in items][:3])
