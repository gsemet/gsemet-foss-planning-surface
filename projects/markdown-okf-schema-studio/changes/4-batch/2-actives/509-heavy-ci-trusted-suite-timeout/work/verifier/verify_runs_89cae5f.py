"""Parse GitHub job logs (untrusted data) of the heavy runs at 89cae5f: launches, part durations, step names.

Usage: python -I verify_runs_89cae5f.py <work/scratch folder>
"""
import re
import sys
from datetime import datetime

NEW = ["45794678556", "45795351595"]
REFERENCE = "45476952370"
TS = re.compile(r"(\d{4}-\d\d-\d\dT\d\d:\d\d:\d\d\.\d+)Z (.*)$")
ANSI = re.compile(r"\x1b\[[0-9;]*m")
OTHER = ("standalone-suite", "reverse-migration-suite", "scroll-sync-suite", "untrusted-suite")
BAD = re.compile(r"STEP failed|LAUNCH TIMEOUT|LAUNCH HANG|Timed out waiting|Studio frame lookup")


def lines_of(path):
    with open(path, encoding="utf-8", errors="replace") as handle:
        for number, raw in enumerate(handle, 1):
            parts = raw.rstrip("\n").split("\t", 2)
            if len(parts) != 3:
                continue
            match = TS.search(parts[2])
            if not match:
                continue
            stamp = datetime.fromisoformat(match.group(1)[:26])
            yield number, stamp, ANSI.sub("", match.group(2))


def hms(stamp):
    return stamp.strftime("%H:%M:%S.%f")[:12]


def parse(path):
    groups, current, launches, bad = [], None, [], []
    for number, stamp, text in lines_of(path):
        if text.startswith("TRUSTED LAUNCH:"):
            launches.append("L%d %s %s" % (number, hms(stamp), text.strip()))
        if BAD.search(text):
            bad.append("L%d %s %s" % (number, hms(stamp), text[:220]))
        if text.startswith("STEP start: setup"):
            current = {"start": stamp, "line": number, "done": []}
            groups.append(current)
        match = re.match(r"STEP done: (\S+) \((\d+) ms\)", text)
        if match and current is not None and match.group(1) not in OTHER:
            current["done"].append((match.group(1), int(match.group(2)), stamp, number))
    return groups, launches, bad


def main():
    base = sys.argv[1].rstrip("/") + "/"
    reference_groups = parse(base + "verify-" + REFERENCE + "/integration.log")[0]
    reference = [d[0] for g in reference_groups for d in g["done"]]
    print("reference 63ef752: %d done, %d distinct" % (len(reference), len(set(reference))))
    for run in NEW:
        for job in ("integration", "stress"):
            groups, launches, bad = parse(base + "artifacts-" + run + "/" + job + ".log")
            print("=" * 10, run, job)
            for line in launches:
                print("  " + line)
            print("  failure or frame-timeout lines: %d" % len(bad))
            for line in bad:
                print("    " + line)
            for index, group in enumerate(groups):
                last = group["done"][-1]
                print("  launch %d: L%d setup start %s -> last done %s (L%d) %s = %.1f s, %d done" % (
                    index + 1, group["line"], hms(group["start"]), last[0], last[3], hms(last[2]),
                    (last[2] - group["start"]).total_seconds(), len(group["done"])))
                durations = {d[0]: d[1] for d in group["done"]}
                print("    " + ", ".join("%s=%d ms" % (k, durations[k]) for k in
                      ("setup", "real-input", "preview-editing", "open-at-line", "open-at-line-probe",
                       "open-at-line-studio") if k in durations))
            if job == "integration":
                one, two = [[d[0] for d in g["done"]] for g in groups]
                expected = [n for n in reference if n not in ("real-input", "preview-editing")]
                print("  part1 %d == reference without real-input/preview-editing, in order: %s" % (len(one), one == expected))
                print("  part2 %s" % two)
                print("  union == reference: %s; in both: %s" % (set(one) | set(two) == set(reference), sorted(set(one) & set(two))))


main()
