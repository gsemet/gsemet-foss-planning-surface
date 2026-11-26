"""Write work/r8-body.json: the pairs the Driver applies to pr-body.md (which is not edited).
Every "old" must occur exactly once at the moment it is applied; a preview goes to
work/r8/pr-body.preview.md."""

import json
from pathlib import Path

CR = Path(__file__).resolve().parents[2]
body = (CR / "pr-body.md").read_bytes().decode("utf-8")
NL = "\r\n" if "\r\n" in body else "\n"
pairs: list[tuple[str, str]] = []


def pair(old: str, new: str) -> None:
    pairs.append((old.replace("\n", NL), new.replace("\n", NL)))


def line(start: str, new: str) -> None:
    """Replace the one body line that starts with `start`."""
    found = [x for x in body.split(NL) if x.startswith(start)]
    assert len(found) == 1, (start, len(found))
    pair(found[0], new)


# sizes
pair("| Index | `topics.json`: 234 topics |", "| Index | `topics.json`: 238 topics |")
pair("| sync-checkout.md | 4,801 | 1,115 | 1,500, within |", "| sync-checkout.md | 4,801 | 1,202 | 1,500, within |")
pair("`foreman.md` 36,927 to 4,000 (4,000);", "`foreman.md` 36,927 to 3,999 (4,000);")
pair("`griller-skill.md` 3,501 (4,000);", "`griller-skill.md` 3,524 (4,000);")

# briefs
pair("| coder | 9,790 | 6,714 |", "| coder | 9,116 | 6,110 |")
pair("| griller | 6,349 | 6,627 |", "| griller | 6,349 | 6,650 |")
pair("| foreman | 55,206 | 22,279 |", "| foreman | 55,206 | 22,278 |")
pair("| direct mode: chief-of-staff, then `foreman --epoch 1` | 77,528 | 46,936 |",
     "| direct mode: chief-of-staff, then `foreman --epoch 1` | 77,528 | 46,935 |")
pair("""Host claude, no unit but where a row says otherwise. chief-of-staff, griller, foreman and
direct mode: measured on the cards of this PR's last commit. The other rows: an earlier round, their cards
unchanged since (the six workers on this change's unit; a later run at `03f973e` gave them 742 bytes less on
both sides, same differences, cause not traced).""",
     """Host claude, no unit but where a row says otherwise. coder (both sides), chief-of-staff, griller,
foreman and direct mode: measured on the cards of this PR's last commit. The other rows: an earlier round,
their cards unchanged since (workers on this change's unit). Today's coder brief was 9,790 in that earlier
round and is 9,116 now; a run at `03f973e` also gave the six workers lower values on both sides (742
bytes, same differences). Cause not traced.""")

# autonomous decisions
pair("""- "Never tell unproved behaviour as fact" is filed as host-trial bookkeeping, with the proof files.""",
     """- "Never tell unproved behaviour as fact" is filed as host-trial bookkeeping, with the proof files;
  the Chief of Staff's card also holds it ("or as fact what the host marks unproved"). The Foreman
  card's two notes that a Copilot path is unproved (B012, B017) are dropped as bookkeeping.""")
pair("""  two permitted reasons; they keep the folder-change ban and the review step's brief reachable). Each,
  with its line:""",
     """  two permitted reasons; they keep the folder-change ban and the review step's brief reachable). Topic
  lines were also edited where the new set had lost or misstated a rule of today's cards (the topic
  row marked "rules put back" below), which goes beyond them too. Each, with its line:""")

# sibling edits
line("| chief-of-staff.md 13, 14, 16, 24, 27 |",
     "| chief-of-staff.md 13, 14, 16, 24, 27, 29 | writes on the user's yes; stopping a Foreman or a process the "
     "session did not start, its own board or watcher too, only on a yes, never by name, pattern or PID; `cancel` "
     "only after an ordered drop; no tracker text naming a CR, batch, role or cost; CR work never in a scratchpad, "
     "temp or host-settings folder, nor only in chat or memory, no secret or personal data in a CR folder; never "
     "tell as fact what the host marks unproved |")
line("| chief-of-staff.md 3, 39, 41 |",
     "| chief-of-staff.md 3, 10, 16, 20, 31, 32, 39, 41 | wording trims for the 6,000 budget; pointers to new "
     "topics; on `init` or \"I am new here\", run `$CHANTIER init` and give the tour of `init.md` |")
line("| griller-skill.md 24, 31; griller.md 7 |",
     "| griller-skill.md 24, 31; griller.md 7 | the CR-work never (scratchpad, temp or host-settings folder, or "
     "only chat or memory), a pointer, no secret in the CR folder |")
line("| foreman.md 20, 21 |",
     "| foreman.md 20, 21 | a granted merge takes the judged head only, no open PR below, reread before a retry; "
     "never drop a hand-back; a local run is owed at that head and a waiver must name it; an absent gate never "
     "means success (`help long-gate`) |")
line("| foreman.md 22 |",
     "| foreman.md 22 | the fast-forward is `--no-overwrite-ignore`, of a clean main checkout; a Driver's refused "
     "push or rebase checked (`help refused-push`, a push judged too); no failed or protected push retried, no "
     "branch protection read; no comment on a dropped CR's PR, its branch kept; stop no sync holder |")
line("| foreman.md 38 |",
     "| foreman.md 38 | Rare cases: only `$CHANTIER help --for foreman`; the topic names are cut (`long-gate` and "
     "`refused-push` are named at never 2 and 3) |")
line("| coder.md 13, conflict-resolver.md 15,",
     "| coder.md 13, conflict-resolver.md 15, debugger.md 13, demo-explorer.md 13, investigator.md 16, "
     "verifier.md 18, cr-driver.md 18 | the same temp-folder and secrets never; `coder.md` also large binaries "
     "other than the retained prototype |")
TOPIC_LINES = (
    "batch-close-p2 3, batch-plan-mode-p2 3, config-p1 3, delivery-time-p2 3, demo-p1 3, forge-permissions 3, "
    "grill-critic-steps 6, grill-series 7, grill-specify-p2 4, lease 3, lost-driver 8, lost-outside 3, 5 and 7, "
    "lost-silent 6, main-checkout 3 and 9, merge-recorded 5, merge-series-stack-p2 3, merge-stack-ready-p2 3, "
    "merge-words 5, orders 8, project-rules 3, refused-push-chief-p2 3, release-chief-after-p2 5, "
    "stack-changes-chief-p1 3, stack-checks 6, stack 6, steering-reports-p1 6, wakes 5 and 6, watcher-board 7, "
    "watcher-lines 8"
)
found = [x for x in body.split(NL) if x.startswith("| topics: cr-rounds 4,")]
assert len(found) == 1
pair(found[0], found[0] + "\n"
     f"| topics, rules put back: {TOPIC_LINES} | a lost or misstated rule or its wording, line by line in the "
     "host and shared inventory |\n"
     "| topics.json | the new topics indexed; `sync` also reads `sync-checkout.md`; `direct-mode` also reads "
     "the mode-switch files; `mode-switch`'s trigger names `order mode` |")

# known gaps
pair("""  This PR's last commit changed the Foreman's, the Chief of Staff's and the Griller's cards: their
  score is owed at the final head.""",
     """  The latest changes edit the Foreman's, the Chief of Staff's, the Griller's and the Coder's cards and
  many topics: their score is owed at the final head.""")
pair("- Cards over budget (only the owner raises a budget): coder 1,533 (+33),",
     "- Cards over budget (only the owner raises a budget): coder 1,603 (+103),")
pair("""- The home of each protecting row was read at its cited line. Each of the four inventories lists the
  protecting-looking rows a topic carries, for the later review.""",
     """- The home of each protecting row was read at its cited line. Of the other rows, at least a few of
  each inventory section were read against their home and the wrong homes corrected; not every row was
  read. Each of the four inventories lists the protecting-looking rows a topic carries, for the later
  review.""")
pair("""- Rules, or parts of rules, held by no card, floor or refusal: large binaries are never kept in a CR
  folder (H-057; `coder.md` is over its budget); the host's settings are never a CR's place (H-059,
  part); never rewrite an earlier retro section (FM-026); never tell as a fact what is marked unproved
  (C-006); a held agent that has ended with no transcript is cleared on the user's word, or once known
  not to run (C-304, C-885).""",
     """- Rules, or parts of rules, held by no card, floor or refusal: never rewrite an earlier retro section
  (FM-026); a held agent that has ended with no transcript is cleared on the user's word (C-304);
  another session's Driver is cleared only on the user's word that it does not run (C-885, part: the
  close refusal holds "if it is not running").""")

# test plan figure and boundary table
pair("  - topic index: 234 topics load, 415 readings resolve, no base name missing;",
     "  - topic index: 238 topics load, 432 readings resolve, no base name missing;")
pair("direct-mode-epoch,", "direct-mode-epoch, direct-mode-switch,")
pair("options, orders, orders-queue,", "options, order-drop, order-verbs, orders, orders-queue,")
pair("qa-results, ready-to-merge,", "qa-results, ready-asks, ready-to-merge,")
pair("(B012: Copilot host row)", "(B012: dropped, unproved bookkeeping; no host row holds it)")
pair("B017: Copilot host row,", "B017: dropped, unproved bookkeeping (no host row holds it),")

text = body
for old, new in pairs:
    assert text.count(old) == 1 and body.count(old) == 1 and old != new, (old[:80], text.count(old), body.count(old))
    text = text.replace(old, new)
out = CR / "work/r8-body.json"
out.write_bytes((json.dumps([{"old": o, "new": n} for o, n in pairs], indent=1, ensure_ascii=False) + "\n")
                .encode("utf-8"))
(CR / "work/r8/pr-body.preview.md").write_bytes(text.encode("utf-8"))
print(len(pairs), "pairs; newline", repr(NL), "; body", len(body), "->", len(text))
