"""Replay of the hand-over options on the recorded steering sessions (figures only).

Command: python 09-replay.py [--no-driver-cost]  (the flag: no Driver lost at a hand-over; files get the suffix -no-driver)        (reads 03-steering-calls.csv, 05-compactions.csv, 06-drivers.csv,
08-fresh-start-figures.csv; writes 09-replay.csv, 09-replay-by-kind.csv and 09-calibration.csv)

Method (the study, part 4, states it in words):
- Each job is one steering session in one batch window (batch-17, 18, 23, 24, 26, 27 Foreman;
  batch-19, 21, 22 Chief of Staff, direct). batch-25 is left out: its steering row joins two sessions
  and only 12 of its 14 wakes are the Foreman's.
- The session's calls are replayed in order. The context after each call grows as it did (the
  recorded step from the previous call; the step across a compaction is 0). The host compacts when the
  context reaches COMPACT_AT: the context becomes P (the mean first-call-after-compaction context
  measured in 05-compactions.csv for that session, else for its kind) and the next call rewrites the
  whole context; a compaction costs COMPACT_USD more (the cost code's "about $0.12", no record).
- A call's cost is re-priced from the new context: input and output tokens as recorded; written tokens
  as recorded, except a call that rewrote its whole context (cache expiry, first call after a
  compaction: written >= half the context) which rewrites the new context; the rest is cache read.
  Prices: the model's, from 03's table.
- "none" replayed this way is compared with the recorded cost (09-calibration.csv): the replay's own
  error. Every option's saving is against "none" replayed, so the error cancels.
- An option's trigger is evaluated at each wake: the context at that call >= X (context option), or the
  number of wakes since the session began steering this batch or its last hand-over >= N (wakes
  option, all wakes, or all but the task-end wakes: "leftover" wakes). The offer waits for the user's
  yes for D (0, 30 min, 2 h, 8 h): the hand-over happens at the first wake at or after offer time + D;
  until then the old session goes on (its calls are paid as recorded). "refused" = never = none.
- At a hand-over: the new session's context is F (the median measured at the point a fresh session is
  ready, 08-fresh-start-figures.csv, by kind) and its cost C_START (the median cumulative dollars to
  that point); plus the old session's last turn (3 calls: cache read of its context + 3,000 output
  tokens), plus the messages between the two (the offer and the yes: 2 wakes of the old session at its
  recorded dollars per wake; for a Foreman, also 2 wakes of the Chief of Staff at the direct sessions'
  dollars per wake), plus the restart of each Driver running at that time (06-drivers.csv: time range
  meets the hand-over time) at C_DRIVER (the median cumulative dollars at a Driver's 15th call).
  Not priced: the work a restarted Driver loses, the user's time, any quality difference.
"""
import csv
import importlib.util
import os
import statistics as st
from datetime import datetime

here = os.path.dirname(os.path.abspath(__file__))
spec = importlib.util.spec_from_file_location("calls03", os.path.join(here, "03-steering-calls.py"))
m = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)
PRICE = m.PRICE
COMPACT_AT, COMPACT_USD = 266_500, 0.12
EXCLUDED = {"batch-25"}


def rd(name):
    with open(os.path.join(here, name), encoding="utf-8") as f:
        return list(csv.DictReader(f))


def T(s):
    return datetime.fromisoformat(s.replace("Z", "+00:00"))


calls = rd("03-steering-calls.csv")
comps = rd("05-compactions.csv")
drivers = rd("06-drivers.csv")
fresh = {r["label"]: r for r in rd("08-fresh-start-figures.csv")}
F = {"foreman": float(fresh["median-foreman"]["ready_context"]), "direct": float(fresh["median-chief"]["ready_context"])}
C_START = {"foreman": float(fresh["median-foreman"]["ready_cum_usd"]), "direct": float(fresh["median-chief"]["ready_cum_usd"])}
import sys
NO_DRIVER = "--no-driver-cost" in sys.argv  # bound: no Driver is lost at a hand-over
SUF = "-no-driver" if NO_DRIVER else ""
C_DRIVER = 0.0 if NO_DRIVER else st.median(float(r["cum_usd_at_call_15"]) for r in drivers if r["cum_usd_at_call_15"])
by = {}
for r in calls:
    by.setdefault(r["batch"], []).append(r)
direct_wakes = [r for b, rs in by.items() if rs[0]["kind"] == "direct" for r in rs if r["grill"] == "0" and r["wake"] == "1"]
direct_usd = sum(float(r["usd"]) for b, rs in by.items() if rs[0]["kind"] == "direct" for r in rs if r["grill"] == "0")
CHIEF_USD_PER_WAKE = direct_usd / len(direct_wakes)


def prep(batch):
    rs = by[batch]
    sess = rs[0]["session"]
    kind = rs[0]["kind"]
    cs = [c for c in comps if c["batch"] == batch]
    post = [int(c["ctx_first_call_after"]) for c in cs if c["ctx_first_call_after"]]
    kind_post = [int(c["ctx_first_call_after"]) for c in comps if c["kind"] == kind and c["ctx_first_call_after"]]
    P = st.mean(post) if post else st.mean(kind_post)
    ws = [(int(r["w5m"]) + int(r["w1h"])) for r in rs]
    inc = st.median([w for w, r in zip(ws, rs) if w < 0.5 * int(r["context"])])
    w1 = sum(int(r["w1h"]) for r in rs)
    h_job = w1 / max(1, sum(ws))
    dr = [(T(d["first"]), T(d["last"])) for d in drivers if d["batch"] == batch and d["steering_session"] == sess[:8]]
    wake_per_usd = sum(float(r["usd"]) for r in rs if r["grill"] == "0") / max(1, sum(1 for r in rs if r["grill"] == "0" and r["wake"] == "1"))
    return dict(rs=rs, kind=kind, P=P, inc=inc, h_job=h_job, dr=dr, usd_per_wake=wake_per_usd)


def cost_call(r, ctx, forced_rewrite, boundary, J):
    inp, out = int(r["input"]), int(r["out"])
    w = int(r["w5m"]) + int(r["w1h"])
    full = w >= 0.5 * int(r["context"])
    if forced_rewrite or (full and not boundary):
        wn = max(0, ctx - inp)
    elif boundary:
        wn = J["inc"]
    else:
        wn = w
    wn = min(wn, max(0, ctx - inp))
    h = int(r["w1h"]) / w if (w and not (forced_rewrite or boundary)) else J["h_job"]
    P = PRICE[r["model"]]
    return (inp * P[0] + wn * (h * P[2] + (1 - h) * P[1]) + max(0, ctx - inp - wn) * P[3] + out * P[4]) / 1e6


def run(J, opt):
    """opt = None (none) or (kind, value, leftover_excluded, delay_s). Return a dict of totals."""
    rs, kind = J["rs"], J["kind"]
    ctx = int(rs[0]["context"])
    prev_ctx_actual = ctx
    prev_comp = int(rs[0]["compactions_before"])
    forced = False
    steering = grill = extra = 0.0
    handovers = compactions = 0
    wakes_since = 0
    pending = None  # time at which the hand-over takes place
    offered_at = None
    peak = 0
    wake_ctx = []
    for i, r in enumerate(rs):
        c_act = int(r["context"])
        boundary = int(r["compactions_before"]) > prev_comp
        prev_comp = int(r["compactions_before"])
        if i:
            ctx += 0 if boundary else (c_act - prev_ctx_actual)
        prev_ctx_actual = c_act
        t = T(r["time"])
        # a pending hand-over takes place at the first wake at or after its time
        if pending is not None and r["wake"] == "1" and t >= pending:
            n_dr = sum(1 for a, z in J["dr"] if a <= t <= z)
            P = PRICE[r["model"]]
            last_turn = 3 * (ctx * P[3] + 3000 * P[4]) / 1e6
            msgs = 2 * J["usd_per_wake"] + (2 * CHIEF_USD_PER_WAKE if kind == "foreman" else 0)
            extra += C_START[kind] + last_turn + msgs + n_dr * C_DRIVER
            ctx = int(F[kind])
            handovers += 1
            wakes_since = 0
            pending = None
            forced = False
        if forced is False and ctx >= COMPACT_AT and not (i and False):
            pass
        if r["wake"] == "1" and r["grill"] == "0":
            wakes_since += 1
        usd = cost_call(r, ctx, forced, boundary, J)
        forced = False
        if r["grill"] == "0":
            steering += usd
        else:
            grill += usd
        peak = max(peak, ctx)
        if r["wake"] == "1" and r["grill"] == "0":
            wake_ctx.append(ctx)
        # the offer: evaluated at a wake, when nothing is pending
        if opt and r["wake"] == "1" and pending is None:
            okind, val, excl, delay = opt
            counted = wakes_since
            if okind == "ctx" and ctx >= val:
                pending = t.timestamp() and datetime.fromtimestamp(t.timestamp() + delay, t.tzinfo)
            elif okind == "wakes" and counted >= val:
                pending = datetime.fromtimestamp(t.timestamp() + delay, t.tzinfo)
        if opt and opt[2] and r["wake"] == "1" and r["cause"].startswith("task end"):
            wakes_since -= 1 if r["grill"] == "0" and wakes_since > 0 else 0
        if ctx >= COMPACT_AT:  # the host compacts before the next call
            ctx = int(J["P"])
            forced = True
            compactions += 1
            extra += COMPACT_USD
    return dict(steering=steering + extra, grill=grill, extra=extra, handovers=handovers, compactions=compactions, peak=peak,
                ctx_avg=sum(wake_ctx) / max(1, len(wake_ctx)))


jobs = {b: prep(b) for b in by if b not in EXCLUDED}
DELAYS = [("0", 0), ("30min", 1800), ("2h", 7200), ("8h", 28800)]
OPTIONS = ([("ctx", x, False) for x in (180_000, 200_000, 230_000, 250_000)]
           + [("wakes", n, False) for n in (30, 60, 100)] + [("wakes", n, True) for n in (30, 60, 100)])

calf = open(os.path.join(here, "09-calibration" + SUF + ".csv"), "w", newline="", encoding="utf-8")
cal = csv.writer(calf, lineterminator="\n")
cal.writerow(["batch", "kind", "recorded_steering_usd", "replayed_none_usd", "error_pct", "recorded_compactions", "replayed_compactions", "start_context_F", "start_cost", "driver_restart_cost", "chief_usd_per_wake"])
outf = open(os.path.join(here, "09-replay" + SUF + ".csv"), "w", newline="", encoding="utf-8")
out = csv.writer(outf, lineterminator="\n")
out.writerow(["batch", "kind", "option", "value", "wakes_exclude_leftover", "yes_delay", "recorded_usd", "none_usd", "option_usd", "saving_usd", "saving_pct_of_steering", "handovers", "compactions", "ctx_avg_at_wake", "ctx_peak", "extra_usd"])
rec = {}
for b, J in jobs.items():
    rec[b] = sum(float(r["usd"]) for r in J["rs"] if r["grill"] == "0")
    base = run(J, None)
    ncomp = sum(1 for c in comps if c["batch"] == b)
    cal.writerow([b, J["kind"], round(rec[b], 2), round(base["steering"], 2), round(100 * (base["steering"] - rec[b]) / rec[b], 1), ncomp, base["compactions"], round(F[J["kind"]]), C_START[J["kind"]], round(C_DRIVER, 3), round(CHIEF_USD_PER_WAKE, 3)])
    out.writerow([b, J["kind"], "none", "", "", "", round(rec[b], 2), round(base["steering"], 2), round(base["steering"], 2), 0, 0, 0, base["compactions"], round(base["ctx_avg"]), base["peak"], round(base["extra"], 2)])
    for okind, val, excl in OPTIONS:
        for dname, d in DELAYS:
            o = run(J, (okind, val, excl, d))
            out.writerow([b, J["kind"], okind, val, int(excl), dname, round(rec[b], 2), round(base["steering"], 2), round(o["steering"], 2), round(base["steering"] - o["steering"], 2),
                          round(100 * (base["steering"] - o["steering"]) / base["steering"], 1), o["handovers"], o["compactions"], round(o["ctx_avg"]), o["peak"], round(o["extra"], 2)])

calf.close()
outf.close()
# sums by kind
rows = list(csv.DictReader(open(os.path.join(here, "09-replay" + SUF + ".csv"), encoding="utf-8")))
agg = csv.writer(open(os.path.join(here, "09-replay-by-kind" + SUF + ".csv"), "w", newline="", encoding="utf-8"), lineterminator="\n")
agg.writerow(["kind", "option", "value", "wakes_exclude_leftover", "yes_delay", "batches", "none_usd", "option_usd", "saving_usd", "saving_pct", "mean_saving_usd_per_batch", "batches_that_save", "handovers"])
keys = sorted({(r["kind"], r["option"], r["value"], r["wakes_exclude_leftover"], r["yes_delay"]) for r in rows if r["option"] != "none"})
for k in keys:
    sel = [r for r in rows if (r["kind"], r["option"], r["value"], r["wakes_exclude_leftover"], r["yes_delay"]) == k]
    n = sum(float(r["none_usd"]) for r in sel)
    o = sum(float(r["option_usd"]) for r in sel)
    agg.writerow([*k, len(sel), round(n, 2), round(o, 2), round(n - o, 2), round(100 * (n - o) / n, 1), round((n - o) / len(sel), 2), sum(1 for r in sel if float(r["saving_usd"]) > 0), sum(int(r["handovers"]) for r in sel)])
