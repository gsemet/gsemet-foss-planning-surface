"""The Driver's own context threshold (130,000 tokens, driver.md "Your means") applied to a steering session.

Command: python 11-driver-threshold-replay.py [--no-driver-cost]
(reuses the replay of 09-replay.py by loading it, which rewrites the 09 files with the same figures;
writes 11-replay-130k.csv, or 11-replay-130k-no-driver.csv with the flag; figures only).
The option is the replay's "context X" with X = 130,000 and the same yes delays, on the same jobs;
saving is against `none` replayed, a negative saving is a loss.
"""
import csv
import importlib.util
import os

here = os.path.dirname(os.path.abspath(__file__))
spec = importlib.util.spec_from_file_location("replay09", os.path.join(here, "09-replay.py"))
r9 = importlib.util.module_from_spec(spec)
spec.loader.exec_module(r9)
with open(os.path.join(here, "11-replay-130k" + r9.SUF + ".csv"), "w", newline="", encoding="utf-8") as f:
    w = csv.writer(f, lineterminator="\n")
    w.writerow(["kind", "yes_delay", "batches", "none_usd", "option_usd", "saving_usd", "handovers"])
    for kind in ("foreman", "direct"):
        js = [J for J in r9.jobs.values() if J["kind"] == kind]
        base = sum(r9.run(J, None)["steering"] for J in js)
        for dname, d in r9.DELAYS:
            res = [r9.run(J, ("ctx", 130_000, False, d)) for J in js]
            o = sum(x["steering"] for x in res)
            w.writerow([kind, dname, len(js), round(base, 2), round(o, 2), round(base - o, 2), sum(x["handovers"] for x in res)])
