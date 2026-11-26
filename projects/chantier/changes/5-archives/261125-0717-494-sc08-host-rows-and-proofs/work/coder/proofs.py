import json
import re
import sys
from pathlib import Path

sys.dont_write_bytecode = True
WT = Path(sys.argv[1])
CARDS = WT / "skills/chantier/references/hosts"
OUT = WT / "docs/proofs"
OUT.mkdir(parents=True, exist_ok=True)

LINK = re.compile(r"\[([^\]]+)\]\((?!https?://|mailto:)([^)]+)\)")
DATE = re.compile(r"\d{4}-\d{2}-\d{2}|batch-\d+")


def fix(text):
    return LINK.sub(lambda m: f"`{m.group(1)}`", text)


def sections(lines):
    out = [(None, [])]
    fence = False
    for ln in lines:
        if ln.startswith("```"):
            fence = not fence
        if not fence and ln.startswith("## "):
            out.append((ln[3:].strip(), []))
        else:
            out[-1][1].append(ln)
    return out


def strip_fences(lines):
    out, fence = [], False
    for ln in lines:
        if ln.startswith("```"):
            fence = not fence
            continue
        if not fence:
            out.append(ln)
    return out


def tidy(lines):
    text = fix("\n".join(strip_fences(lines)))
    return re.sub(r"\n{3,}", "\n\n", text).strip("\n")


def rows_of(lines):
    rows = []
    for ln in lines:
        if ln.startswith("| ") and not ln.startswith("| ---") and not ln.startswith("| Generic"):
            s = ln.strip()
            body = s[2:-2] if s.endswith(" |") else s[2:]
            first, _, rest = body.partition(" | ")
            mid, sep, last = rest.rpartition(" | ")
            rows.append((first, mid if sep else rest, last if sep else ""))
    return rows


def find_row(rows, prefix, exact=False):
    for r in rows:
        if (r[0] == prefix) if exact else r[0].startswith(prefix):
            return r
    raise SystemExit(f"no row {prefix!r}")


def R(p, exact=False):
    return ("row", p, exact)


CLAUDE = {
    "start-foreman": [R("Start the Foreman's session")],
    "own-session-id": [R("Own session id")],
    "set-own-title": [R("Set a session's own title")],
    "skills": [R("The skills")],
    "load-skill": [R("Load another skill")],
    "list-sessions": [R("List the sessions")],
    "message-session": [R("Message another session")],
    "session-link": [R("A session's link")],
    "start-driver": [R("Start a Driver or a worker")],
    "model-at-start": [R("Models at an agent's start")],
    "start-spec-writer": [R("Start the Spec-writer")],
    "start-spec-critic": [R("Start the Spec critic")],
    "start-retro-critic": [R("Start the Retro critic")],
    "message-driver": [R("Message a Driver")],
    "message-chief": [R("Message the Chief of Staff")],
    "driver-hand-back": [R("A Driver messages its steering session")],
    "driver-messages-steering-direct": [R("A Driver messages its steering session")],
    "stop-driver": [R("Stop a Driver")],
    "stop-woken-driver": [R("Stop an ended Driver")],
    "driver-start-folder": [R("A CR Driver's start folder")],
    "stop-own-background-task": [R("Stop a background task")],
    "name-env-holders": [R("Name the holders")],
    "stop-session": [R("Stop another session")],
    "agent-ids": [R("Agent ids")],
    "models": [R("Models", True)],
    "session-skills-tools": [R("Skills and tools of a session")],
    "preflight-p2": [R("Preflight P2")],
    "ask-questions": [R("Ask the user a series")],
    "run-board": [R("Run the board")],
    "board-griller": [R("The board's Griller")],
    "workspace-trust": [R("Trust of a workspace")],
    "move-session": [R("Move a started session")],
    "prompt-cache-ttl": [R("Prompt cache TTL")],
    "steering-wake-bound": [R("Steering wake bound")],
    "heartbeat": [("sec", "Heartbeat")],
    "run-watcher": [R("Run the watcher")],
    "watcher-session-end": [R("The watcher when the session ends")],
    "board-session-end": [R("The board when the session ends")],
    "message-limit": [("para", "**Limit on messages.**")],
    "end-turn-background": [("srow", "End a subagent's turn")],
    "subagent-stops": [("srow", "A background subagent stops")],
    "subagent-stopped-outside": [("srow", "A background subagent is stopped from outside")],
    "resume-subagent": [("srow", "Resume a stopped subagent")],
    "compact": [("sec", "Compacting")],
    "reload-after-compact": [("sec", "Reload after a compaction")],
    "write-guard": [("sec", "The write guard")],
    "griller-in-worktree": [("sec", "Sessions of one repository")],
    "surface-session-writes": [
        ("note", "The trials of this row are in the section `Other: Classes of session` below.")
    ],
}
CLAUDE_WORDS = {
    "heartbeat": "Proved: same.",
    "message-limit": "Proved in use, same; the figure comes from the earlier card, with no dated trial.",
    "compact": "documented and measured once; the recommendation is not a proved fact.",
    "reload-after-compact": "unproved until seen in a session.",
    "write-guard": "the refusals are proved by `hooks/register.test.tsx`; the passes are unproved until the eval reports.",
    "griller-in-worktree": "Unproved; trial: one file sent and placed.",
    "surface-session-writes": "the class row of the planning surface, unproved.",
}
CLAUDE_OTHER = [
    "Startup core",
    "Auto-fix events",
    "The Foreman's turn-end notice",
    "A Driver's silence",
    "Configuration",
    "Classes of session",
    "Surfaces and options",
    "A Foreman in a worktree asks",
    "Reusing the last Foreman",
    'The "For you" block',
]

COPILOT = {
    "start-foreman": [R("Start the Foreman's session")],
    "own-session-id": [R("Own session id")],
    "set-own-title": [R("Set the Foreman's own title"), R("Set a session's own title")],
    "skills": [R("The skills")],
    "list-sessions": [R("List the sessions")],
    "message-session": [R("Message another session")],
    "start-driver": [R("Start a Driver or a worker")],
    "model-at-start": [R("Models at an agent's start")],
    "start-generic-agent": [R("Start a generic agent")],
    "model-ran-on": [R("The model a role ran on")],
    "start-spec-writer": [R("Start the Spec-writer")],
    "start-spec-critic": [R("Start the Spec critic")],
    "start-retro-critic": [R("Start the Retro critic")],
    "message-driver": [R("Message a Driver")],
    "message-chief": [R("Message the Chief of Staff")],
    "driver-hand-back": [R("A Driver's hand-back")],
    "driver-messages-steering-direct": [R("A Driver's hand-back")],
    "stop-driver": [R("Stop a Driver")],
    "driver-start-folder": [R("A Driver's start folder")],
    "stop-own-background-task": [R("Stop a background task")],
    "name-env-holders": [R("Name the holders")],
    "agent-ids": [R("Agent ids")],
    "models": [R("Models", True)],
    "session-skills-tools": [R("Skills and tools of a session")],
    "preflight-p2": [R("Preflight P2")],
    "ask-questions": [R("Ask the user a series")],
    "run-board": [R("Run the board")],
    "board-griller": [R("The board's Griller")],
    "prompt-cache-ttl": [R("Prompt cache TTL")],
    "steering-wake-bound": [R("`/every` in whole minutes")],
    "heartbeat": [("sec", "Heartbeat")],
    "run-watcher": [R("Run the watcher")],
    "board-session-end": [R("The board when the session ends")],
    "subagent-stopped-outside": [("sec", "Sessions")],
    "compact": [("sec", "Compacting")],
    "reload-after-compact": [("sec", "Reload after a compaction")],
    "griller-in-worktree": [R("A Griller in a worktree")],
    "surface-session-writes": [R("A session in a planning surface")],
}
COPILOT_OTHER = ["Startup core", "Known host issues", "Configuration", "Surfaces and options"]
NOSTORY_COPILOT = "No trial recorded on this host; the card's Startup core marks every line unproved."
NOSTORY_CLAUDE = "No trial recorded on this host; the card names no trial for this capability."

INTRO = (
    "No role loads this file. It holds the trials, dates, batches, models and marks behind\n"
    "`references/hosts/{file}.json`, copied from the host card. A row's mark changes only with a\n"
    "trial recorded here."
)


def build(host, cardname, jsonname, title, mapping, words, other, nostory):
    lines = (CARDS / cardname).read_text(encoding="utf-8").split("\n")
    secs = dict(sections(lines))
    trows = rows_of(secs["Tools"])
    srows = rows_of(secs.get("Surfaces and options", []))
    data = json.loads((CARDS / jsonname).read_text(encoding="utf-8"))
    out = [f"# {title}", "", INTRO.format(file=jsonname[:-5]), ""]
    for row in data["rows"]:
        cap, mark = row["capability"], row["mark"]
        body, header = [], None
        for src in mapping.get(cap, []):
            kind = src[0]
            if kind == "row":
                g, means, last = find_row(trows, src[1], src[2])
                if host == "claude":
                    header = last or None
                    body.append(f"Card row: {g}.")
                    if DATE.search(means):
                        body.append(f"Means in the card: {means}")
                else:
                    text = f"{g}: {means}" + (f" | {last}" if last else "")
                    if re.search(r"proved|trial|\d{4}-\d{2}-\d{2}|batch-\d+", text):
                        body.append(f"Card row: {text}")
            elif kind == "srow":
                g, means, last = find_row(srows, src[1])
                header = last
                body.append(f"Card row: {g}: {means} | {last}")
            elif kind == "sec":
                body.append(tidy(secs[src[1]]))
            elif kind == "para":
                chunk = "\n".join(lines)
                i = chunk.index(src[1])
                body.append(chunk[i:].split("\n\n", 1)[0])
            elif kind == "note":
                body.append(src[1])
        if host == "claude":
            says = words.get(cap) or header or "see below"
            first = f"Mark: {mark} (card: {says})"
        else:
            first = f"Mark: {mark} (card: Startup core, every line unproved unless it says otherwise)"
        out += [f"## {cap}", "", fix(first), ""]
        out += [fix(b) for b in body] if body else [nostory]
        out.append("")
    for t in other:
        out += [f"## Other: {t}", ""]
        if t == "Known host issues":
            chunk = "\n".join(lines)
            i = chunk.index("Known host issues:")
            out.append(fix(chunk[i:].split("\n\n", 1)[0]))
        else:
            out.append(tidy(secs[t]))
        out.append("")
    return "\n".join(out).rstrip("\n") + "\n"


(OUT / "claude-code.md").write_text(
    build("claude", "claude-code.md", "claude-code.json", "Claude Code: the trials behind the host rows",
          CLAUDE, CLAUDE_WORDS, CLAUDE_OTHER, NOSTORY_CLAUDE), encoding="utf-8", newline="\n")
(OUT / "copilot.md").write_text(
    build("copilot", "copilot.md", "copilot.json", "Copilot: the trials behind the host rows",
          COPILOT, {}, COPILOT_OTHER, NOSTORY_COPILOT), encoding="utf-8", newline="\n")
print("ok")
