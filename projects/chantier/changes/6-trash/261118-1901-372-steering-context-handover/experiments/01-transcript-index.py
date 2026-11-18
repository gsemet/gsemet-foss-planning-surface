"""Index the Claude Code transcripts that could hold a steering session (figures only).

Command (from anywhere, read-only on ~/.claude/projects):
    python 01-transcript-index.py > 01-transcript-index.csv

For each transcript of the chantier repository's and the planning surface's project folders (top
level and under <session>/subagents/) it writes one CSV row: the folder, the session id, whether it
is a subagent's, the first and last record time, the priced calls, the wakes (as costs/transcripts.py
`_wakes`), the peak context, the `foreman set ... --epoch N` claims and the `--batch batch-NN` ids
its shell commands name. It prints no message text.
"""
import csv, glob, json, os, re, sys
_P = "C--" + os.path.expanduser("~")[3:].replace("\\", "-").replace("/", "-") + "-Projets-"  # the host's folder tag, derived from the home folder

BASE = os.path.expanduser("~/.claude/projects")
DIRS = [_P + "chantier", _P + "gsemet-foss-planning-surface"]
CLAIM = re.compile(r"foreman set \S+ --epoch (\d+)")
BATCH = re.compile(r"--batch (batch-\d+)")


def wakes(rec):
    c = (rec.get("message") or {}).get("content")
    return not (isinstance(c, list) and c and all(isinstance(p, dict) and p.get("type") == "tool_result" for p in c))


def scan(path):
    first = last = None
    seen, calls, nw, peak, ncomp = set(), 0, 0, 0, 0
    claims, batches = [], {}
    with open(path, encoding="utf-8") as f:
        for line in f:
            if not line.strip():
                continue
            d = json.loads(line)
            ts = d.get("timestamp")
            if ts:
                first = first or ts
                last = ts
            k = d.get("type")
            if k == "user" and wakes(d):
                nw += 1
            if k == "system" and d.get("subtype") == "compact_boundary":
                ncomp += 1
            if k == "assistant" and isinstance(d.get("message"), dict):
                m = d["message"]
                u = m.get("usage")
                if u and m.get("model") != "<synthetic>" and m.get("id") not in seen:
                    seen.add(m.get("id"))
                    cc = u.get("cache_creation") or {}
                    t = (u.get("input_tokens", 0), cc.get("ephemeral_5m_input_tokens", 0),
                         cc.get("ephemeral_1h_input_tokens", 0), u.get("cache_read_input_tokens", 0))
                    if any(t):
                        calls += 1
                        peak = max(peak, sum(t))
                for b in m.get("content") or []:
                    if isinstance(b, dict) and b.get("type") == "tool_use" and b.get("name") == "Bash":
                        cmd = str((b.get("input") or {}).get("command", ""))
                        for e in CLAIM.findall(cmd):
                            claims.append((ts, e))
                        for x in BATCH.findall(cmd):
                            batches[x] = batches.get(x, 0) + 1
    return first, last, calls, nw, peak, ncomp, claims, batches


w = csv.writer(sys.stdout, lineterminator="\n")
w.writerow(["folder", "session", "subagent", "first", "last", "calls", "wakes", "peak_context",
            "compactions", "claim_epochs", "batches_named"])
for d in DIRS:
    files = sorted(glob.glob(f"{BASE}/{d}/*.jsonl")) + sorted(glob.glob(f"{BASE}/{d}/*/subagents/*.jsonl"))
    for p in files:
        first, last, calls, nw, peak, ncomp, claims, batches = scan(p)
        w.writerow([d.replace(_P, ""), os.path.basename(p)[:-6],
                    "subagents" in p.replace("\\", "/"), first, last, calls, nw, peak, ncomp,
                    ";".join(sorted({e for _, e in claims})),
                    ";".join(f"{b}:{n}" for b, n in sorted(batches.items()))])
