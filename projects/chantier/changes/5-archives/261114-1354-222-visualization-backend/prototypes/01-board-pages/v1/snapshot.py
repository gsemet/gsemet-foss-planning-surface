"""Prototype 1 only: python -I snapshot.py <planning folder> <out data.js> (fixed file names)."""
import json, sys, pathlib
root = pathlib.Path(sys.argv[1])          # planning folder
out = pathlib.Path(sys.argv[2])           # data.js
d = json.loads((root / "STATUS.json").read_text(encoding="utf-8"))

def md(rel, limit=6000):
    if not rel:
        return None
    p = root / rel
    if p.is_file():
        t = p.read_text(encoding="utf-8", errors="replace")
        return t[:limit] + ("\n\n…" if len(t) > limit else "")
    return None

def docs(folder):
    res = {}
    if not folder:
        return res
    base = root / folder
    if base.is_file():
        base = base.parent
    for name in ("01-intent.md", "02-answers.md", "03-change-spec.md", "STATUS.md"):
        t = md(str((base / name).relative_to(root)))
        if t:
            res[name] = t
    return res

b = d["batches"][0] if d["batches"] else None
batch = None
if b:
    batch = {k: b[k] for k in ("batch", "state", "spent_usd", "budget_usd", "asks_unread", "heartbeat", "slots")}
    batch["crs"] = [{
        "cr": c["cr"], "title": c["title"], "state": c["state"], "round": c["round"],
        "cost": c["cost_usd"], "pr": c["pr"], "waits": c["waits"], "blocked": c["blocked"],
        "folder": c["folder"], "docs": docs(c["folder"]),
    } for c in b["crs"]]
backlog = [{
    "priority": x["priority"], "item": x["item"], "title": x["title"],
    "spec": bool(x.get("spec")), "docs": docs(x["path"]),
} for x in d["backlog"]]
merged = [{"cr": x["cr"], "title": x["title"], "batch": x["batch"], "pr": x["pr"],
           "cost": x["cost_usd"], "when": x["when"]} for x in d["merged"][:12]]
snap = {"updated": d["updated"], "batch": batch, "backlog": backlog, "merged": merged,
        "merged_total": d["merged_total"], "trashed_total": d["trashed_total"]}
out.write_text("window.SNAP = " + json.dumps(snap, ensure_ascii=False) + ";\n", encoding="utf-8")
print(len(backlog), "backlog;", len(batch["crs"]) if batch else 0, "batch;", sorted({x["priority"] for x in backlog}))
