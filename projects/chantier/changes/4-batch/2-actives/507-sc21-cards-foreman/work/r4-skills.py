from pathlib import Path

root = Path('C:/Users/gaeta/Projets/chantier.worktrees/batch-31-CR-507/skills')
out = root / 'chantier' / 'cards-next' / 'skills'
out.mkdir(exist_ok=True)

CMD = 'uv run --script "<plugin root>/skills/chantier/scripts/chantier.py"'

LAUNCH = f"""`$CHANTIER` is the CLI, one launcher line:

```
{CMD} [--project <folder>] <command>
```

`<plugin root>` is this skill's folder `../..` made absolute, with forward slashes, quoted. `--project <folder>`, the project's folder in the planning surface, only when the planning lives on an external surface. Carry `$CHANTIER` verbatim into every brief and command: another path form misses the allow rule and meets the host's prompt. The launcher picks the mode itself (chantier's own checkout in a chantier session: the local code, live; else the plugin's build)."""

SYNC = f"""At a session's start, at a batch's start and after a merge that changes `uv.lock`, the steering session, and no other, syncs, with `--sync` first: `{CMD} --sync [--project <folder>]`. It prints `in sync`, `synced`, `plugin mode: no sync (only chantier's own checkout syncs)` or `sync pending: held by <holders>` (go on unsynced: [sync-checkout](../chantier/references/sync-checkout.md))."""

FAIL = """Exit 127 (`chantier launcher: uv is not on PATH (uv is the one tool chantier needs)`) or any other failure of the launcher is a stop: report its text, never another command."""

CARDS = 'Cards: `../chantier/references/`; CLI: `../chantier/scripts/cli/`.'

ROUTER = [
    """- With **no live Chief of Staff in the seat** (none, or a session that looks stopped): ask the user which role they want in this session, the Chief of Staff or a Griller, then load that skill and follow it: `chief-of-staff` with no argument (its mode follows the surface) or `griller`.
- With a **live Chief of Staff in the seat**: ask nothing; behave as `/chantier:chief-of-staff` does.""",
    """Read the seat with `$CHANTIER seat`; what "live" means: `$CHANTIER help seat`. With the argument `reload`, or on "chantier reload", run `$CHANTIER help reload` and follow it, nothing else of this file but the launcher; a session that holds a role (the message names it, or the seat names this session) loads that role's skill with `reload` instead; with no role, ask none.""",
]

CHIEF = [
    """You are the **Chief of Staff**. Run `$CHANTIER brief chief-of-staff` and read the file its last line names, whole, first; run it again when your role changes.""",
    """A `watch: not running` line in any output, a reload's too: start the watcher now, on the session's yes; run the printed command as is: no flag added.""",
    """If the invocation's first word is `foreman` or `direct`, that mode holds for the session; the user's word changes it. With the argument `reload`, or on "chantier reload": run `$CHANTIER help reload`, follow it and run the brief again; of the rest of this file only the launcher and the `watch: not running` rule apply; it sets no mode.""",
]

GRILLER = [
    """You are a **Griller**. Run `$CHANTIER brief griller` and read the file its last line names, whole, first; run it again when your role changes.""",
    """With the argument `reload`, or on "chantier reload": run `$CHANTIER help reload`, follow it and run the brief again, with no `--sync`; nothing else of this file but the launcher.""",
]

STATUS = [
    """You change nothing: no order, no heartbeat, no epoch, no file.""",
    """Read [status-layout](../chantier/references/status-layout.md), only for this action, and nothing else of chantier: not the main skill, not the Chief of Staff's card, not the introduction. Then, for the active batch, or each active batch when there are several (`--batch <batch>`):""",
    """1. `$CHANTIER status --refresh` with no epoch;
2. `$CHANTIER status`;
3. `$CHANTIER cost`.""",
    """Read each CR's icon and label from the batch's `STATUS.md` (the Status column; or `label` in its `STATUS.json`), just refreshed by step 1: the text output of `status` draws no icon. Write the Progress report from their output, in the user's language, by the Progress skeleton of status-layout, with the cost as its tables.""",
    """With no active batch, say so in one line and give the backlog count from `.agents/changes/STATUS.md`.""",
]

BODY = {
    'chantier': ('# chantier: the router', False, ROUTER),
    'chief-of-staff': ('# chantier: Chief of Staff', True, CHIEF),
    'griller': ('# chantier: Griller', True, GRILLER),
    'status': ('# chantier: status', True, STATUS),
}

for name, (title, cards, paras) in BODY.items():
    live = (root / name / 'SKILL.md').read_text(encoding='utf-8').replace('\r\n', '\n')
    front = live[:live.index('\n---\n', 4) + 5]
    parts = [front, title, 'chantier-version: 0.15.1', LAUNCH, SYNC, FAIL]
    if cards:
        parts.append(CARDS)
    parts += paras
    text = '\n\n'.join(p.rstrip('\n') for p in parts) + '\n'
    path = out / f'{name}-SKILL.md'
    path.write_text(text, encoding='utf-8', newline='\n')
    new = path.read_text(encoding='utf-8')
    assert new.startswith(front), name
    print(name, 'live', len((root / name / 'SKILL.md').read_bytes()), 'live-lf', len(live.encode()), 'new', len(text.encode()))
