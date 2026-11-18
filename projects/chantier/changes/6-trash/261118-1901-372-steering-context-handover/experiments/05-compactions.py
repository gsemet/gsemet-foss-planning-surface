"""The compactions of the steering sessions, per batch window (figures only).

Command: python 05-compactions.py > 05-compactions.csv

One row per `compact_boundary` record inside a job's window (jobs and windows as in
03-steering-calls.py): the time, the trigger (auto or manual), the host's own pre- and post-compaction
token counts (`compactMetadata.preTokens`, `postTokens`), the context of the first call after it
and of the 10th call after it (the context once the role session has reloaded), and the wake
number (steering wakes so far in the window). Message text is not read.
"""
import csv, importlib.util, json, os, sys

spec = importlib.util.spec_from_file_location("calls03", os.path.join(os.path.dirname(os.path.abspath(__file__)), "03-steering-calls.py"))
m = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)
calls_by = {}
w = csv.writer(sys.stdout, lineterminator="\n")
w.writerow(["batch", "kind", "session", "time", "trigger", "pre_tokens", "post_tokens", "ctx_first_call_after", "ctx_10th_call_after", "wakes_before"])
for batch, kind, folder, sid in m.JOBS:
    a, z = (m.when(x + "+00:00") for x in m.WINDOW[batch])
    rows = m.calls(f"{m.B}/{folder}/{sid}.jsonl", *m.WINDOW[batch])
    events = []
    with open(f"{m.B}/{folder}/{sid}.jsonl", encoding="utf-8") as f:
        for line in f:
            if '"compact_boundary"' not in line:
                continue
            d = json.loads(line)
            ts = m.when(d.get("timestamp"))
            if d.get("subtype") == "compact_boundary" and a <= ts <= z:
                cm = d.get("compactMetadata") or {}
                events.append((d["timestamp"], cm.get("trigger"), cm.get("preTokens"), cm.get("postTokens")))
    for t, trig, pre, post in events:
        after = [r for r in rows if r["time"] > t]
        before = [r for r in rows if r["time"] <= t]
        w.writerow([f"batch-{batch}", kind, sid[:8], t, trig, pre, post, after[0]["context"] if after else "",
                    after[9]["context"] if len(after) > 9 else "", sum(r["wake"] for r in before if not r["grill"])])
