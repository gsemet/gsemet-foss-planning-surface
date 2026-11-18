"""Where the steering cost goes: per-session summary, cost by context band, wakes by cause.

Command: python 07-analysis.py        (reads 03-steering-calls.csv and 05-compactions.csv; writes
07-job-summary.csv, 07-cost-by-context-band.csv, 07-wake-causes.csv next to itself)

Rows are the steering row of each job: the calls of a turn that is not a grill turn (as the cost
code splits them). A wake's "episode" is its call and the calls up to the next wake; the episode's
dollars are attributed to the wake's cause.
"""
import csv, os, statistics as st
from collections import defaultdict

here = os.path.dirname(os.path.abspath(__file__))
rows = list(csv.DictReader(open(os.path.join(here, "03-steering-calls.csv"), encoding="utf-8")))
comp = list(csv.DictReader(open(os.path.join(here, "05-compactions.csv"), encoding="utf-8")))
by = defaultdict(list)
for r in rows:
    by[r["batch"]].append(r)
BANDS = [(0, 100_000), (100_000, 150_000), (150_000, 200_000), (200_000, 250_000), (250_000, 10**9)]


def f(x):
    return float(x) if x not in ("", None) else 0.0


summ = csv.writer(open(os.path.join(here, "07-job-summary.csv"), "w", newline="", encoding="utf-8"), lineterminator="\n")
summ.writerow(["batch", "kind", "calls", "wakes", "usd", "usd_per_wake", "read_share_pct", "write_share_pct", "out_share_pct", "input_share_pct",
               "timed_calls", "expired_calls", "expired_calls_usd", "expired_calls_usd_share_pct", "compactions", "ctx_avg_at_wake", "ctx_peak",
               "calls_ge_150k_pct", "usd_calls_ge_150k_pct", "span_hours"])
bandw = csv.writer(open(os.path.join(here, "07-cost-by-context-band.csv"), "w", newline="", encoding="utf-8"), lineterminator="\n")
bandw.writerow(["batch", "kind", "band_from", "band_to", "calls", "usd", "usd_per_call", "read_usd", "write_usd"])
cw = csv.writer(open(os.path.join(here, "07-wake-causes.csv"), "w", newline="", encoding="utf-8"), lineterminator="\n")
cw.writerow(["batch", "kind", "cause", "wakes", "wake_share_pct", "episode_calls", "episode_usd", "usd_share_pct"])
for b, rs in by.items():
    kind = rs[0]["kind"]
    s = [r for r in rs if r["grill"] == "0"]
    usd = sum(f(r["usd"]) for r in s)
    wk = [r for r in s if r["wake"] == "1"]
    rd, wr = sum(f(r["usd_read"]) for r in s), sum(f(r["usd_write"]) for r in s)
    # input and output dollars: recompute from tokens' share of the remainder is not possible without prices; take out = usd - read - write - input
    timed = [r for r in s if r["expired"] != ""]
    exp = [r for r in timed if r["expired"] == "1"]
    eu = sum(f(r["usd"]) for r in exp)
    hi = [r for r in s if int(r["context"]) >= 150_000]
    t0, t1 = rs[0]["time"], rs[-1]["time"]
    from datetime import datetime
    hours = (datetime.fromisoformat(t1.replace("Z", "+00:00")) - datetime.fromisoformat(t0.replace("Z", "+00:00"))).total_seconds() / 3600
    nc = sum(1 for c in comp if c["batch"] == b)
    summ.writerow([b, kind, len(s), len(wk), round(usd, 2), round(usd / max(1, len(wk)), 3), round(100 * rd / usd, 1), round(100 * wr / usd, 1),
                   round(100 * sum(f(r["usd_out"]) for r in s) / usd, 1), round(100 * sum(f(r["usd_in"]) for r in s) / usd, 1), len(timed), len(exp), round(eu, 2), round(100 * eu / usd, 1), nc,
                   sum(int(r["context"]) for r in wk) // max(1, len(wk)), max(int(r["context"]) for r in s),
                   round(100 * len(hi) / len(s), 1), round(100 * sum(f(r["usd"]) for r in hi) / usd, 1), round(hours, 1)])
    for lo, hi_ in BANDS:
        sel = [r for r in s if lo <= int(r["context"]) < hi_]
        if sel:
            u = sum(f(r["usd"]) for r in sel)
            bandw.writerow([b, kind, lo, hi_, len(sel), round(u, 2), round(u / len(sel), 4), round(sum(f(r["usd_read"]) for r in sel), 2), round(sum(f(r["usd_write"]) for r in sel), 2)])
    # wake causes: episodes
    ep, cur = defaultdict(lambda: [0, 0, 0.0]), None
    for r in s:
        if r["wake"] == "1":
            cur = r["cause"]
            ep[cur][0] += 1
        if cur:
            ep[cur][1] += 1
            ep[cur][2] += f(r["usd"])
    nw, tu = sum(v[0] for v in ep.values()), sum(v[2] for v in ep.values())
    for cause, (n, c, u) in sorted(ep.items(), key=lambda kv: -kv[1][2]):
        cw.writerow([b, kind, cause, n, round(100 * n / max(1, nw), 1), c, round(u, 2), round(100 * u / max(0.01, tu), 1)])
