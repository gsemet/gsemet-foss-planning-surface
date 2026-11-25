"""Round 10: for every inventory row homed in a cards-next file, check that each clause of the
row's source text is in the home. The text checked is the source itself (today's cards at
origin/main), from where the row's sentence starts to where the next row's starts, so a part the
inventory cut is checked too. A reading aid: every flagged row is then read by hand.

usage: audit.py [--home FILE ...] [--ids ID ...] [--min SCORE] [--count] [--all-text]
"""

import argparse
import collections
import math
import pathlib
import re
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from inv import CARDS, home_files, norm, rows, source_lines, source_range  # noqa: E402

STOP = set(
    """the and for its not are with that this when from you your one has have was were will
    may can all any but out only each then than them they their there here also into onto over
    under per via his her him she who whom which what how does did done been being is it in on
    of to a an or by as at be if no so do we our us once such same other own whose where while
    after before until both either neither nor yet just more most some very other another""".split()
)


def stems(text):
    text = re.sub(r"\]\([^)]*\)", "]", text.lower())
    found = re.findall(r"[a-z0-9]+", text)
    return [w[:5] for w in found if len(w) > 2 and w not in STOP]


def spans(text):
    out = []
    for s in re.findall(r"`([^`]+)`", text):
        s = s.replace("$CHANTIER ", "").replace("chantier ", "").strip()
        if s:
            out.append(s)
    return out


def flat(text):
    text = re.sub(r"\]\([^)]*\)", "]", text)
    return norm(text.replace("$CHANTIER ", "").replace("chantier ", ""))


def segments():
    """id -> (row, inventory, the source text from the row's start to the next row's)."""
    data = list(rows())
    texts, offsets = {}, {}
    located = []
    for inv, n, r in data:
        rng = source_range(r["source"])
        path, first, last = rng
        lines = source_lines(path)
        if path not in texts:
            parts, off, pos = [], [0], 0
            for line in lines:
                t = " ".join(line.split())
                parts.append(t)
                pos += len(t) + 1
                off.append(pos)
            texts[path], offsets[path] = " ".join(parts), off
        text, off = texts[path], offsets[path]
        first, last = min(first, len(lines)), min(last, len(lines))
        lo, hi = off[first - 1], off[last]
        said = norm(r["behaviour"]).rstrip("…").strip()
        start = -1
        for size in (60, 35, 20, 10):
            if len(said) >= 10:
                start = text.find(said[:size], max(0, lo - 5))
                if 0 <= start < hi + 5:
                    break
                start = -1
        located.append((inv, r, path, start, lo, hi))
    starts = collections.defaultdict(set)
    for _, _, path, start, _, _ in located:
        if start >= 0:
            starts[path].add(start)
    out = []
    for inv, r, path, start, lo, hi in located:
        text = texts[path]
        if start < 0:
            seg = norm(r["behaviour"])
            if seg.endswith("…"):
                seg = text[lo:hi]
        else:
            later = [s for s in starts[path] if s > start]
            end = min([hi, *later]) if later else hi
            seg = text[start:end].strip()
            said = norm(r["behaviour"]).rstrip("…").strip()
            if len(seg) < len(said):
                seg = said
        out.append((inv, r, path, seg))
    return out


def home_text(files):
    return "\n".join((CARDS / f).read_text(encoding="utf-8") for f in sorted(files))


def windows(text, size=2):
    sents = [s for s in re.split(r"(?<=[.;:])\s+|\n+", text) if s.strip()]
    sets = [set(stems(s)) for s in sents]
    return [set().union(*sets[i : i + size]) for i in range(len(sets))] or [set()]


def idf_table():
    files = [p for p in CARDS.rglob("*") if p.suffix in (".md", ".json")]
    df = collections.Counter()
    for p in files:
        df.update(set(stems(p.read_text(encoding="utf-8"))))
    return {k: math.log(len(files) / v) for k, v in df.items()}, math.log(len(files) * 2)


def check(seg, files, idf, top, cache):
    key = tuple(sorted(files))
    if key not in cache:
        t = home_text(files)
        cache[key] = (flat(t), set(stems(t)), windows(t, 3))
    ftext, have, wins = cache[key]
    lost_spans = [s for s in spans(seg) if s not in ftext and s.rstrip(" .…") not in ftext]
    clauses = [c.strip() for c in re.split(r"[;.:()]\s+|[()]|, (?=and |or |but |never |no |not |else |unless |except |only )| - ", seg) if c.strip()]
    bad = []
    score = 2.0 * len(lost_spans)
    for c in clauses:
        s = set(stems(c))
        if not s:
            continue
        gone = s - have
        best = max(len(s & w) / len(s) for w in wins)
        weight = sum(idf.get(g, top) for g in gone)
        if gone and (len(gone) / len(s) >= 0.34 or weight >= 7) or (len(s) >= 3 and best < 0.5):
            bad.append((c, sorted(gone), round(best, 2)))
            score += weight / 3 + (1 - best) * min(len(s), 6) / 2
    return round(score, 1), lost_spans, bad


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--home", nargs="*")
    ap.add_argument("--ids", nargs="*")
    ap.add_argument("--min", type=float, default=0.1)
    ap.add_argument("--count", action="store_true")
    ap.add_argument("--full", action="store_true")
    args = ap.parse_args()
    idf, top = idf_table()
    cache = {}
    total = textual = 0
    flagged = []
    for inv, r, path, seg in segments():
        total += 1
        files = home_files(r["new home"])
        if args.ids:
            if r["id"] in args.ids:
                print(f"{r['id']} [{r['kind']}] {r['source']} -> {r['new home']}\n  files {sorted(files)}\n  SRC {seg}")
                if files:
                    print("  ", check(seg, files, idf, top, cache))
            continue
        if not files:
            continue
        textual += 1
        score, lost, bad = check(seg, files, idf, top, cache)
        if score >= args.min:
            flagged.append((score, sorted(files), r, seg, lost, bad))
    if args.ids:
        return
    print(f"rows {total}; with a cards-next text home {textual}; flagged (score >= {args.min}) {len(flagged)}")
    by = collections.defaultdict(list)
    for x in flagged:
        by[", ".join(x[1])].append(x)
    if args.count:
        buckets = collections.Counter(min(int(x[0]), 15) for x in flagged)
        print(sorted(buckets.items()))
        print(len(by), "home sets")
        for k, v in sorted(by.items(), key=lambda kv: -len(kv[1]))[:40]:
            print(f"  {len(v):4d} {k}")
        return
    for k in sorted(by):
        if args.home and not any(h in k for h in args.home):
            continue
        print(f"\n===== {k}")
        for score, _, r, seg, lost, bad in sorted(by[k], key=lambda x: x[2]["id"]):
            print(f"{r['id']} {score} [{r['kind']}] {r['source']} -> {r['new home']}")
            if args.full:
                print(f"  S: {seg}")
            else:
                if lost:
                    print(f"  spans: {lost}")
                for c, gone, best in bad:
                    print(f"  - ({best}) {c[:200]} {gone}")


if __name__ == "__main__":
    main()
