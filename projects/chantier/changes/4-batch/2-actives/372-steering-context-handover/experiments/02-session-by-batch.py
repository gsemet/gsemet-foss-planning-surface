"""Which transcript steered which batch: priced calls and peak context of each top-level session
inside each batch's window (opened..closed of the records), figures only.

Command: python 02-session-by-batch.py > 02-session-by-batch.csv

Read-only on ~/.claude/projects (the chantier repository's and the planning surface's folders).
A session that steered a batch shows many calls in its window and a peak equal to the record's
"at its peak" figure. The windows are the records' `opened` and `closed` (5-archives/batches).
"""
import csv, glob, json, os, sys
_P = "C--" + os.path.expanduser("~")[3:].replace("\\", "-").replace("/", "-") + "-Projets-"  # the host's folder tag, derived from the home folder

B = os.path.expanduser("~/.claude/projects")
W = {17: ("2026-11-13T17:33:25", "2026-11-14T17:38:29"), 18: ("2026-11-14T18:41:48", "2026-11-15T16:18:18"),
     19: ("2026-11-15T16:20:49", "2026-11-15T18:50:46"), 21: ("2026-11-16T16:30:53", "2026-11-16T19:42:34"),
     22: ("2026-11-16T19:45:52", "2026-11-17T06:42:10"), 23: ("2026-11-17T10:11:33", "2026-11-17T14:32:40"),
     24: ("2026-11-17T17:42:16", "2026-11-18T08:15:25"), 25: ("2026-11-18T10:09:33", "2026-11-18T11:56:53"),
     26: ("2026-11-18T12:16:06", "2026-11-18T14:29:30"), 27: ("2026-11-18T14:33:05", "2026-11-18T17:47:48")}
res = {}
for d in [_P + "chantier", _P + "gsemet-foss-planning-surface"]:
    for p in glob.glob(f"{B}/{d}/*.jsonl"):
        seen = set()
        for l in open(p, encoding="utf-8"):
            if '"type":"assistant"' not in l:
                continue
            x = json.loads(l)
            if x.get("type") != "assistant":
                continue
            m = x.get("message") or {}
            u = m.get("usage")
            if not u or m.get("id") in seen or m.get("model") == "<synthetic>":
                continue
            seen.add(m.get("id"))
            cc = u.get("cache_creation") or {}
            c = (u.get("input_tokens", 0) + cc.get("ephemeral_5m_input_tokens", 0)
                 + cc.get("ephemeral_1h_input_tokens", 0) + u.get("cache_read_input_tokens", 0))
            if not c:
                continue
            ts = x["timestamp"][:19]
            for b, (a, z) in W.items():
                if a <= ts <= z:
                    r = res.setdefault((b, d.replace(_P, ""), os.path.basename(p)[:-6]), [0, 0])
                    r[0] += 1
                    r[1] = max(r[1], c)
w = csv.writer(sys.stdout, lineterminator="\n")
w.writerow(["batch", "folder", "session", "calls_in_window", "peak_context_in_window"])
for k, v in sorted(res.items(), key=lambda kv: (kv[0][0], -kv[1][0])):
    w.writerow([f"batch-{k[0]}", k[1], k[2], v[0], v[1]])
