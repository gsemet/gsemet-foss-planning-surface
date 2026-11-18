"""One CSV row per priced call of the steering sessions, parsed as chantier's cost code parses a
transcript (skills/chantier/scripts/cli/src/chantier/costs/transcripts.py, read, not imported).

Command: python 03-steering-calls.py > 03-steering-calls.csv

Read-only on ~/.claude/projects. Figures only: the CSV holds times, token counts, dollars, a cause
class for each wake (a fixed label, never message text) and flags; no message text is written.

Rules taken from transcripts.py: a wake is a user record that is not only tool results; the context
of a call is input + 5-minute write + 1-hour write + cache read tokens; calls are deduplicated by
message id; a call whose counts are all zero, or whose model is "<synthetic>", is skipped; the
dollars use the price table below (copied from transcripts.py at v0.13.0); a call is "expired" when
the gap from the previous call is over 300 s after a 5-minute write or 3600 s after a 1-hour write;
a call's turn is "grill" when the turn has a strict grill use (a spec-writer or spec-critic started,
or a Write/Edit whose path ends in 01-intent.md, 02-answers.md, 03-change-spec.md or
work/specifying) inside the steering window. Assumption: the steering window of each job is the
batch's whole opened..closed window (the archived records do not keep the claims that give the
cost code's own windows).
"""
import csv
import json
import os
_P = "C--" + os.path.expanduser("~")[3:].replace("\\", "-").replace("/", "-") + "-Projets-"  # the host's folder tag, derived from the home folder
import re
import sys
from datetime import datetime

B = os.path.expanduser("~/.claude/projects")
CH, PS = _P + "chantier", _P + "gsemet-foss-planning-surface"
PRICE = {  # $/MTok: input, 5-min write, 1-h write, cache read, output (transcripts.py, v0.13.0)
    "claude-opus-5-5": (4, 5, 8, 0.20, 20), "claude-sonnet-5-5": (2, 2.5, 4, 0.10, 10),
    "claude-fable-5-2": (8, 10, 16, 0.20, 40), "claude-haiku-5-5": (0.10, 0.125, 0.20, 0.01, 0.50)}
GRILL_NAMES = ("01-intent.md", "02-answers.md", "03-change-spec.md", "work/specifying")
WRITE_PATHS = {"Write": "file_path", "Edit": "file_path", "MultiEdit": "file_path", "NotebookEdit": "notebook_path"}
WINDOW = {17: ("2026-11-13T17:33:25", "2026-11-14T17:38:29"), 18: ("2026-11-14T18:41:48", "2026-11-15T16:18:18"),
          19: ("2026-11-15T16:20:49", "2026-11-15T18:50:46"), 21: ("2026-11-16T16:30:53", "2026-11-16T19:42:34"),
          22: ("2026-11-16T19:45:52", "2026-11-17T06:42:10"), 23: ("2026-11-17T10:11:33", "2026-11-17T14:32:40"),
          24: ("2026-11-17T17:42:16", "2026-11-18T08:15:25"), 25: ("2026-11-18T10:09:33", "2026-11-18T11:56:53"),
          26: ("2026-11-18T12:16:06", "2026-11-18T14:29:30"), 27: ("2026-11-18T14:33:05", "2026-11-18T17:47:48")}
# (batch, kind, folder, session)
JOBS = [(17, "foreman", CH, "bd1945f6-9982-485f-b29f-477277e80753"), (18, "foreman", CH, "446cff2e-8291-4f73-9ff0-f19c29743e6e"),
        (19, "direct", CH, "91f1382a-eacd-437e-b5a8-f9e545753a8c"), (21, "direct", CH, "91f1382a-eacd-437e-b5a8-f9e545753a8c"),
        (22, "direct", CH, "91f1382a-eacd-437e-b5a8-f9e545753a8c"), (23, "foreman", CH, "1b6c0af3-8055-48dc-975e-95b0619755c4"),
        (24, "foreman", CH, "1b6c0af3-8055-48dc-975e-95b0619755c4"), (25, "foreman", CH, "cc65c0a9-973c-4a5c-bde4-616fc2581097"),
        (26, "foreman", CH, "993a179a-630e-4ad6-913f-c10286a32ded"), (27, "foreman", CH, "62abbcd1-9358-4768-abec-8aa99767d8eb")]
FIELDS = ["batch", "kind", "session", "seq", "time", "turn", "wake", "cause", "context", "input", "w5m", "w1h", "read",
          "out", "model", "usd", "usd_in", "usd_write", "usd_read", "usd_out", "gap_s", "expired", "grill", "compactions_before"]


def when(s):
    return datetime.fromisoformat(s.replace("Z", "+00:00")) if s else None


def text_of(d):
    c = (d.get("message") or {}).get("content")
    if isinstance(c, str):
        return c
    return " ".join(p.get("text", "") for p in c if isinstance(p, dict)) if isinstance(c, list) else ""


def is_wake(d):
    c = (d.get("message") or {}).get("content")
    return not (isinstance(c, list) and c and all(isinstance(p, dict) and p.get("type") == "tool_result" for p in c))


def grill_strict(block):
    if not isinstance(block, dict) or block.get("type") != "tool_use":
        return False
    g = block.get("input")
    if isinstance(g, dict) and str(g.get("subagent_type", "")).endswith(("spec-writer", "spec-critic")):
        return True
    key = WRITE_PATHS.get(str(block.get("name")))
    t = g.get(key) if key and isinstance(g, dict) else None
    return isinstance(t, str) and t.replace("\\", "/").endswith(GRILL_NAMES)


def classify(d, own_tools):
    """A fixed label for what woke the session; nothing of the text is kept."""
    t = text_of(d).strip()
    if t.startswith("Another Claude session sent a message:"):
        m = re.search(r"\[([\w-]+)\s*→\s*([\w-]+)\]", t[:900])
        if "<cross-session-message" in t[:400]:
            return f"cross-session [{m.group(1)}>{m.group(2)}]" if m else "cross-session (other)"
        if "[Subagent hand-back]" in t[:600]:
            return "subagent hand-back"
        return f"agent message [{m.group(1)}>{m.group(2)}]" if m else "agent message (other)"
    if t.startswith("<task-notification"):
        m = re.search(r"<tool-use-id>(\w+)</tool-use-id>", t[:600])
        cmd = own_tools.get(m.group(1)) if m else None
        if cmd is None:
            return "task end (not started by this session)"
        return "task end: watcher" if re.search(r"\bwatch\b", cmd) else "task end: own task"
    if "status --refresh" in t[:120]:
        return "heartbeat"
    if t.startswith(("# /loop", "<command-message>loop")):
        return "loop command"
    if t.startswith(("This session is being continued", "<system-reminder>\n<tools-used-before-summary",
                     "<artifact-content-authored-by-others/>\nThe summarized", "<local-command", "<command-name>/compact")):
        return "compaction or reload"
    if t.startswith(("<system-reminder>", "<command-name>", "<command-message>")):
        return "other system"
    return "user turn"


def calls(path, since, until):
    """Return a list of dicts, one per priced call inside [since, until], in order."""
    a, z = when(since + "+00:00"), when(until + "+00:00")
    seen, turn, cause, comp, own_tools = set(), 0, None, 0, {}
    grill_turns, rows, prev, life = set(), [], None, 0
    with open(path, encoding="utf-8") as f:
        for line in f:
            if not line.strip():
                continue
            d = json.loads(line)
            ts = when(d.get("timestamp"))
            inside = ts is not None and a <= ts <= z
            k = d.get("type")
            if k == "user" and is_wake(d):
                turn += 1
            if k == "assistant" and isinstance(d.get("message"), dict):
                content = d["message"].get("content")
                if isinstance(content, list):
                    for b in content:
                        if isinstance(b, dict) and b.get("type") == "tool_use":
                            own_tools[b.get("id")] = str((b.get("input") or {}).get("command", "")) if b.get("name") == "Bash" else ""
                    if inside and any(grill_strict(b) for b in content):
                        grill_turns.add(turn)
            if not inside:
                continue
            if k == "system" and d.get("subtype") == "compact_boundary":
                comp += 1
            if k == "user" and is_wake(d):
                cause = cause or classify(d, own_tools)  # the first wake since the last call names the cause
            if k != "assistant":
                continue
            m = d.get("message")
            u = m.get("usage") if isinstance(m, dict) else None
            if not u or m.get("model") == "<synthetic>" or m.get("id") in seen:
                continue
            cc = u.get("cache_creation") or {}
            t = (u.get("input_tokens", 0), cc.get("ephemeral_5m_input_tokens", 0), cc.get("ephemeral_1h_input_tokens", 0),
                 u.get("cache_read_input_tokens", 0), u.get("output_tokens", 0))
            if not any(t):
                continue
            seen.add(m["id"])
            rate = PRICE.get(re.sub(r"-\d{8}$", "", m["model"]))
            parts = [x * y / 1e6 for x, y in zip(t, rate)] if rate else [0] * 5
            gap = (ts - prev).total_seconds() if prev else None
            rows.append(dict(time=d["timestamp"], turn=turn, wake=int(cause is not None), cause=cause or "", context=sum(t[:4]),
                             input=t[0], w5m=t[1], w1h=t[2], read=t[3], out=t[4], model=m["model"], usd=round(sum(parts), 6), usd_in=round(parts[0], 6), usd_out=round(parts[4], 6),
                             usd_write=round(parts[1] + parts[2], 6), usd_read=round(parts[3], 6),
                             gap_s=None if gap is None else round(gap),
                             expired=None if gap is None or not life else int(gap > life), _turn=turn,
                             compactions_before=comp))
            prev = ts
            life = 3600 if t[2] else 300 if t[1] else life
            cause = None
    for r in rows:
        r["grill"] = int(r.pop("_turn") in grill_turns)
    return rows


if __name__ == "__main__":
    w = csv.DictWriter(sys.stdout, FIELDS, lineterminator="\n", extrasaction="ignore")
    w.writeheader()
    for batch, kind, folder, sid in JOBS:
        for i, r in enumerate(calls(f"{B}/{folder}/{sid}.jsonl", *WINDOW[batch]), 1):
            w.writerow(dict(r, batch=f"batch-{batch}", kind=kind, session=sid[:8], seq=i))
