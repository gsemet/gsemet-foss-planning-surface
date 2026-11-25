from pathlib import Path

root = Path('C:/Users/gaeta/Projets/chantier.worktrees/batch-31-CR-507/skills')
out = root / 'chantier' / 'cards-next' / 'skills'
out.mkdir(exist_ok=True)

LAUNCH = (
    '`$CHANTIER` is the CLI: `uv run --script "<plugin root>/skills/chantier/scripts/chantier.py"`, '
    '`<plugin root>` being this skill\'s folder `../..` made absolute, with forward slashes, quoted. '
    'Carry it verbatim into every brief and command: another path form misses the allow rule and meets '
    'the host\'s prompt. In a planning surface it also carries `--project <the project\'s folder>`. '
    'The launcher picks the mode itself (chantier\'s own checkout and a chantier session: the local '
    'code, live; else the plugin\'s build).'
)
SYNC = (
    'In chantier\'s own checkout run `$CHANTIER --sync` before the first command, at a batch\'s start '
    'and after a merge that changes `uv.lock` ([sync-checkout](../chantier/references/sync-checkout.md)).'
)
FAIL = (
    'Exit 127 (`chantier launcher: uv is not on PATH`) or any other failure of `$CHANTIER` is a stop: '
    'report its text, never another command; `sync pending` alone lets you go on.'
)
CARDS = 'Cards: `../chantier/references/`; CLI: `../chantier/scripts/cli/`.'

BODY = {
    'chantier': ('# chantier: the router', False, [
        '- With **no live Chief of Staff in the seat** (none, or a session that looks stopped): ask the '
        'user which role they want in this session, the Chief of Staff or a Griller, then load that '
        'skill and follow it: `chief-of-staff` with no argument (its mode follows the surface) or '
        '`griller`.\n'
        '- With a **live Chief of Staff in the seat**: ask nothing; behave as `/chantier:chief-of-staff` '
        'does.\n\n'
        'Read the seat with `$CHANTIER seat`; what "live" means: `$CHANTIER help seat`. With the '
        'argument `reload`, or on "chantier reload", run `$CHANTIER help reload` and follow it, nothing '
        'else of this file; a session that holds a role (the message names it, or the seat names this '
        'session) loads that role\'s skill with `reload` instead; with no role, ask none.'
    ]),
    'chief-of-staff': ('# chantier: Chief of Staff', True, [
        'A `watch: not running` line in any output, a reload\'s too: start the watcher now, on the '
        'session\'s yes; run the printed command as is: no flag added.',
        'You are the **Chief of Staff**. Run `$CHANTIER brief chief-of-staff` and read the file its '
        'last line names, whole, first; run it again when your role changes. If the invocation\'s first '
        'word is `foreman` or `direct`, that mode holds for the session; the user\'s word changes it. '
        'With the argument `reload`, or on "chantier reload", run `$CHANTIER help reload` and follow it, '
        'nothing else of this file but this Startup core; it sets no mode.'
    ]),
    'griller': ('# chantier: Griller', True, [
        'You are a **Griller**. Run `$CHANTIER brief griller` and read the file its last line names, '
        'whole, first; run it again when your role changes. With the argument `reload`, or on '
        '"chantier reload", run `$CHANTIER help reload` and follow it with no `--sync`; nothing else of '
        'this file.'
    ]),
    'status': ('# chantier: status', True, [
        'You change nothing: no order, no heartbeat, no epoch, no file.',
        'Read [status-layout](../chantier/references/status-layout.md), only for this action, and '
        'nothing else of chantier: not the main skill, not the Chief of Staff\'s card, not the '
        'introduction. Then, for the active batch, or each active batch when there are several '
        '(`--batch <batch>`):',
        '1. `$CHANTIER status --refresh` with no epoch;\n2. `$CHANTIER status`;\n3. `$CHANTIER cost`.',
        'Read each CR\'s icon and label from the batch\'s `STATUS.md` (the Status column; or `label` in '
        'its `STATUS.json`), just refreshed by step 1: the text output of `status` draws no icon. Write '
        'the Progress report from their output, in the user\'s language, by the Progress skeleton of '
        'status-layout, with the cost as its tables.',
        'With no active batch, say so in one line and give the backlog count from '
        '`.agents/changes/STATUS.md`.'
    ]),
}

for name, (title, cards, paras) in BODY.items():
    live = (root / name / 'SKILL.md').read_text(encoding='utf-8').replace('\r\n', '\n')
    front = live[:live.index('\n---\n', 4) + 5]
    parts = [front, title, 'chantier-version: 0.15.1', LAUNCH, SYNC, FAIL]
    if cards:
        parts.append(CARDS)
    parts += ['## Startup core'] + paras
    text = '\n\n'.join(p.rstrip('\n') for p in parts) + '\n'
    path = out / f'{name}-SKILL.md'
    path.write_text(text, encoding='utf-8', newline='\n')
    old = len(live.encode())
    print(name, old, len(text.encode()))
