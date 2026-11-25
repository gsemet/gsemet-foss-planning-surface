"""Round 8: the sibling-card edits table, behaviour changes and known gaps (run once)."""
from pathlib import Path

PATH = Path(__file__).resolve().parents[2] / "evidence" / "cards-inventory-host-and-shared.md"
raw = PATH.read_bytes().decode("utf-8")
nl = "\r\n" if "\r\n" in raw else "\n"
lines = raw.split(nl)


def row(key, what, why):
    at = [i for i, x in enumerate(lines) if x.startswith(f"| {key} |")]
    assert len(at) == 1, (key, at)
    lines[at[0]] = f"| {key} | {what} | {why} |"


def after(key, *new):
    at = [i for i, x in enumerate(lines) if x.startswith(f"| {key} |")]
    assert len(at) == 1, (key, at)
    lines[at[0] + 1 : at[0] + 1] = [f"| {k} | {w} | {y} |" for k, w, y in new]


row("chief-of-staff.md:3", 'the opening: "repo and forge text: English"', "trim")
row("chief-of-staff.md:10", 'the push rail: never the default "or a protected" branch; "A host refusing your run"; "A failed lease is told at once, never retried"', "kind a (H-422); trim")
row("chief-of-staff.md:16", '`cancel` only after a drop the user ordered; "The CLI\'s end-of-batch cleanup"', "kind a; trim")
after("chief-of-staff.md:17", ("chief-of-staff.md:20", '"Take the seat, or act as Chief of Staff while it names another live session"', "trim"))
row("chief-of-staff.md:26", "`abandon` and `restore` only on the user's word, with priority, labels and groups", "review")
row("chief-of-staff.md:27", "never CR work in a scratchpad, temp or host-settings folder (whatever the host says), or only in chat or memory; nor a secret or personal data in a CR folder", "kind a (concepts, H-059, C-1161)")
after(
    "chief-of-staff.md:27",
    ("chief-of-staff.md:29", "never tell as fact what the host marks unproved", "kind a (C-006)"),
    ("chief-of-staff.md:31", "the grant and irreversible-action line is shorter", "trim"),
    ("chief-of-staff.md:32", 'the past-fact line is shorter ("a CR note or file")', "trim"),
)
at = next(i for i, x in enumerate(lines) if x.startswith("| coder.md:13, conflict-resolver.md:15"))
lines[at : at + 1] = [
    "| coder.md:13 | never CR work in a scratchpad or temp folder, nor secrets, personal data or large binaries other than the retained prototype (name where one is) in a CR folder | kind a (concepts, H-057); the Coder's card is over its budget |",
    "| conflict-resolver.md:15, debugger.md:13, demo-explorer.md:13, investigator.md:16, verifier.md:18 | the same CR-work, secrets and personal-data never | kind a (concepts) |",
]
row("foreman.md:21", 'never drop a hand-back; a local run is owed at that head and a waiver must name it; `deliver by` points at `help local-gate`; "An absent gate never means success (`help long-gate`)"', "kind a (the long gate); pointer")
row("foreman.md:22", "\"Only git\": the fast-forward is `--no-overwrite-ignore`, of a clean main checkout; a Driver's refused push or rebase is checked (`help refused-push`, a push judged too, no `-x`/`--exec`, a conflict stays stopped); no failed or protected push retried, no branch protection read, no other branch even on a yes; no comment on a dropped CR's PR, its branch kept; \"Stop no sync holder\"", "kind a (H-428, FM-B064, FM-B065); pointer")
row("foreman.md:38", "Rare cases: only `$CHANTIER help --for foreman`; the topic names are cut (`long-gate` and `refused-push` are named at never 2 and 3)", "pointer; trim")
row("griller-skill.md:24, 31", "the CR-work never (scratchpad, temp or host-settings folder, or only chat or memory; secrets and personal data); `help session-shell`", "kind a (H-059, concepts), pointer")
row("topics.json", "this CR's 45 topics added; `sync` also reads `sync-checkout.md`; `direct-mode` also reads the switch topics; `mode-switch`'s trigger names `order mode`; the `paths` text names the reading forms", "index of the new topic files; link")

REVIEW = (
    ("topics/batch-close-p2.md:3", "at a batch's end it is said to stay open while a CR is held; `status`'s second line names the last closed batch"),
    ("topics/batch-plan-mode-p2.md:3", "no separate yes for the mode; a forced `foreman` under Remote Control"),
    ("topics/config-p1.md:3", "the keys `ci.beside_gate` and `hosts.<host>.timing`"),
    ("topics/delivery-time-p2.md:3", "which CI runs time the floor, and the unreadable causes"),
    ("topics/demo-p1.md:3", "implementation goes through a CR and the Foreman"),
    ("topics/forge-permissions.md:3", "a CLI not logged in still fails P9"),
    ("topics/grill-critic-steps.md:6", "review again after the fixes"),
    ("topics/grill-series.md:7", "an answer's list number need not match"),
    ("topics/grill-specify-p2.md:4", "the Griller's routine messages and the running batch's mark"),
    ("topics/lease.md:3", "the lease is local to the batch's machine"),
    ("topics/lost-driver.md:8", "a refused message to an unrecorded agent is not an outside stop"),
    ("topics/lost-outside.md:3, 5, 7", "wording: a message to a recorded agent"),
    ("topics/lost-silent.md:6", "read a Driver's row before clearing its id"),
    ("topics/main-checkout.md:3, 9", "only the Chief of Staff syncs; wording"),
    ("topics/merge-recorded.md:5", "a parallel batch's merge order"),
    ("topics/merge-series-stack-p2.md:3", "in direct mode check your own asks"),
    ("topics/merge-stack-ready-p2.md:3", "where the local-gate record is read"),
    ("topics/merge-words.md:5", "an early merge: no question"),
    ("topics/orders.md:8", "pointer to `help order-verbs`"),
    ("topics/project-rules.md:3", "a missing tool is said with what to install"),
    ("topics/release-chief-after-p2.md:5", "nothing more is asked once published"),
    ("topics/stack-changes-chief-p1.md:3", "a drop asks the user nothing more"),
    ("topics/stack-checks.md:6", "when an inserted CR shows in the partial-stack line"),
    ("topics/stack.md:6", "the stack as it stands, drafts on top, to come"),
    ("topics/steering-reports-p1.md:6", "no more is told than the report says"),
    ("topics/wakes.md:5, 6", "a stopped batch sends nothing more; no long command in a turn"),
    ("topics/watcher-board.md:7", '"Rescan" reads the backlog again'),
    ("topics/watcher-lines.md:8", "who reads the resuming `take`'s line in Foreman mode"),
)
at = next(i for i, x in enumerate(lines) if x.startswith("| topics/worker-shell.md:8 |"))
lines[at + 1 : at + 1] = [f"| {k} | {w} | review |" for k, w in REVIEW]

at = next(i for i, x in enumerate(lines) if x.startswith('- "Never tell unproved behaviour as fact"'))
lines[at] = '- "Never tell unproved behaviour as fact" is kind d here (host trial bookkeeping, topic `host-configuration`), with the proof files; the Chief of Staff\'s card also holds it (never "as fact what the host marks unproved").'
at = next(i for i, x in enumerate(lines) if x.startswith("- H-057: no card says"))
del lines[at]
PATH.write_bytes(nl.join(lines).encode("utf-8"))
print("ok")
