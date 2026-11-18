"""The cost and context of a fresh steering session at the point it is ready to steer, and the sizes of
the files it reads (figures only).

Command: python 08-fresh-start-figures.py > 08-fresh-start-figures.csv   (reads 04-fresh-starts.csv)

"Ready" = the first call that arms the heartbeat (ScheduleWakeup, or a wake from the /loop command),
starts a Driver (Agent) or messages a session (SendMessage): the figures are those of the call just
before it (its context and the cumulative dollars up to it). First-call context = the host's own base
(system prompt, tools, memory, AGENTS.md) before anything is read.
"""
import csv, os, re, statistics as st, sys

here = os.path.dirname(os.path.abspath(__file__))
rows = list(csv.DictReader(open(os.path.join(here, "04-fresh-starts.csv"), encoding="utf-8")))
w = csv.writer(sys.stdout, lineterminator="\n")
w.writerow(["label", "kind", "first_call_context", "ready_call_seq", "ready_context", "ready_cum_usd", "context_jump_from_first_call"])
seen = []
for label in dict.fromkeys(r["label"] for r in rows):
    rs = [r for r in rows if r["label"] == label]
    idx = next((i for i, r in enumerate(rs) if i > 0 and (set(r["tools"].split("+")) & {"ScheduleWakeup", "Agent", "SendMessage"} or r["wake_cause"] == "loop command")), None)
    if idx is None:
        w.writerow([label, rs[0]["kind"], rs[0]["context"], "not reached in 45 calls", "", "", ""])
        continue
    p = rs[idx - 1]
    w.writerow([label, p["kind"], rs[0]["context"], p["seq"], p["context"], p["cum_usd"], int(p["context"]) - int(rs[0]["context"])])
    seen.append((p["kind"], int(p["context"]), float(p["cum_usd"]), int(rs[0]["context"])))
for kind in ("foreman", "chief"):
    s = [x for x in seen if x[0] == kind]
    if s:
        w.writerow([f"median-{kind}", kind, st.median(x[3] for x in s), "", st.median(x[1] for x in s), round(st.median(x[2] for x in s), 3), "n=%d" % len(s)])
