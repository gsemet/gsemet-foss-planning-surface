"""Round 10: write work/r10-body.json, the old/new pairs for pr-body.md, and check them.

pr-body.md is read, never written. Each old text must occur exactly once; the pairs are applied in
memory only, then the result is checked for stale figures and printed table rows.
"""

import json
import re
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
CR = HERE.parents[1]
body = (CR / "pr-body.md").read_bytes().decode("utf-8")
pairs: list[dict[str, str]] = []


def pair(old: str, new: str) -> None:
    assert old != new, old
    pairs.append({"old": old, "new": new})


def row_line(start: str) -> str:
    found = [line for line in body.split("\n") if line.startswith(start)]
    assert len(found) == 1, (start, len(found))
    return found[0]


def english(numbers: list[str]) -> str:
    return numbers[0] if len(numbers) == 1 else ", ".join(numbers[:-1]) + " and " + numbers[-1]


# The topic rows, from siblings.py's list against fe7fbf0f.
out = subprocess.run([sys.executable, "-I", "-X", "utf8", str(HERE / "siblings.py")], capture_output=True,
                     check=True).stdout.decode("utf-8")
section = out.split("#### against fe7fbf0f", 1)[1].split("#### against 03f973e4", 1)[0]
topics: dict[str, list[str]] = {}
for line in section.splitlines()[1:]:
    if line.startswith("topics/"):
        name, _, numbers = line.partition("\t")
        name = name.split(" (from ")[0][len("topics/"):-len(".md")]
        topics[name] = [n.strip() for n in numbers.split(",") if n.strip()]
first_row = {"cr-rounds": ["4"], "refused-push-chief-p1": ["3", "6"], "release-notes": ["4"],
             "ticket-summary-p2": ["7"], "titles": ["4"], "worker-shell": ["9"]}
for name, numbers in first_row.items():
    assert set(numbers) <= set(topics[name]), (name, topics[name])
listing = ", ".join(f"{name} {english(left)}" for name, numbers in sorted(topics.items())
                    if (left := [n for n in numbers if n not in first_row.get(name, [])]))

pair("`topics.json`: 238 topics", "`topics.json`: 240 topics")
for start, new in [
    ("| concepts.md |", "| concepts.md | 73,286 | 26,100 | none set |"),
    ("| pr-template.md |", "| pr-template.md | 16,801 | 12,032 | none set |"),
    ("| release-template.md |", "| release-template.md | 12,155 | 7,002 | none set |"),
    ("| status-layout.md |", "| status-layout.md | 17,475 | 11,486 | none set |"),
    ("| titles.md (now", "| titles.md (now `topics/titles.md`) | 2,684 | 1,495 | 1,500, within |"),
    ("| review-step.md |", "| review-step.md | 3,950 | 1,497 | 1,500, within |"),
    ("| forges/github.md", "| forges/github.md, gitlab.md | 739, 744 | 592, 595 | not larger, within |"),
    ("| topics/host-*.md", "| topics/host-*.md (33 files) | part of the above | 37,088, largest 1,500 | 1,500 each, within |"),
    ("| skills: chantier", "| skills: chantier, chief-of-staff, griller, status | 3,537, 3,664, 3,223, 3,644 | 2,705, 2,785, 2,347, 2,784 | none set |"),
]:
    pair(row_line(start), new)
pair("`foreman.md` 36,927 to 3,999 (4,000)", "`foreman.md` 36,927 to 3,997 (4,000)")
pair("`griller-skill.md` 3,524 (4,000)", "`griller-skill.md` 3,621 (4,000)")

start = body.index("| coder | 9,116 | 6,110 |")
end = body.index("\n", body.index("| direct mode: chief-of-staff"))
pair(body[start:end], """| coder | 9,575 | 6,569 |
| conflict-resolver | 8,859 | 6,460 |
| debugger | 8,648 | 6,247 |
| inspector | 11,010 | 6,966 |
| investigator | 8,520 | 6,452 |
| verifier | 19,547 | 8,078 |
| retro-critic | 4,225 | 2,889 |
| demo-explorer | 4,746 | 2,936 |
| chief-of-staff | 22,322 | 24,657 |
| griller | 6,349 | 6,747 |
| foreman | 55,206 | 22,276 |
| cr-driver, staged card, role only | 59,216 | 8,010 |
| release-driver, staged card, role only | 59,216 | 8,070 |
| stack-driver, staged card, role only | 59,216 | 8,044 |
| qa-driver, staged card, role only | 59,216 | 5,828 |
| spec-writer, on an inbox item | 4,815 | 3,228 |
| spec-critic, on an inbox item | 5,290 | 3,133 |
| board-griller, on an inbox item | 11,964 | 3,132 |
| direct mode: chief-of-staff, then `foreman --epoch 1` | 77,528 | 46,933 |""")
start = body.index("Host claude, no unit but where a row says otherwise.")
end = body.index("Griller 145 / 36 KB.", start) + len("Griller 145 / 36 KB.")
pair(body[start:end], """Host claude, no unit but where a row says otherwise. Every row was measured in one run on the cards of
this PR's last commit. A unit's brief also holds the unit's facts from the record, so the six workers'
bytes, measured on this change's unit, move between rounds on both sides (today's coder brief: 9,575
here, 9,790 and 9,116 in earlier rounds). Start readings before this change, as the specification gives
them (declared / measured): Foreman 91 / 144 KB, Chief of Staff 202 / 218 KB, Griller 145 / 36 KB.""")

pair("lines were also edited where the new set had lost or misstated a rule of today's cards (the topic",
     "lines were also edited where the new set had lost or misstated a rule of today's cards, or held a date,\n"
     "  CR id or trial story the specification bans (the topic")
pair(row_line("| griller-skill.md 24, 31; griller.md 7 |"),
     "| griller-skill.md 5, 24, 29, 31; griller.md 7 | the CR-work never (scratchpad, temp or host-settings folder, "
     "or only chat or memory), a pointer, no secret in the CR folder; `depends.json` only when a CR needs another's "
     "result; no `triage` for a CR marked for the running batch |")
pair(row_line("| topics: cr-rounds 4,"),
     "| topics: " + ", ".join(f"{name} {english(numbers)}" for name, numbers in first_row.items())
     + " | pointer, scoping, links, a folded rule, the folder-change ban |")
pair(row_line("| topics, rules put back:"),
     f"| topics, rules put back: {listing} | a lost or misstated rule or its wording, a date, CR id or trial story the "
     "specification bans, or a split file's lines; line by line in the host and shared inventory |")
pair(row_line("| topics.json |"),
     "| topics.json | the new topics indexed; `sync` also reads `sync-checkout.md`; `direct-mode` also reads the files "
     "of `direct-mode-switch`; `mode-switch`'s trigger names `order mode`; the split topics list their parts; "
     "`ready-asks` and `ask-lines` serve the Foreman and the Chief of Staff |")

start = body.index("- `concepts.md` (line 121) says")
end = body.index("- The rule that repository text is in English", start)
pair(body[start:end], """- `foreman.md` has eight nevers where the specification sets seven: the eighth (CR work in a scratchpad or
  temp folder; a secret or personal data in a CR folder) protects the user, and F5 puts such a rule on a
  card, in the floor or in a refusal.
""")
pair("  The latest changes edit the Foreman's, the Chief of Staff's, the Griller's and the Coder's cards and\n"
     "  many topics: their score is owed at the final head. Plans only, no spend: chief-of-staff with griller 54 runs, about",
     "  The changes edit the Foreman's, the Chief of Staff's, the Griller's and the Coder's cards, the shared files,\n"
     "  the skill texts and many topics: their score is owed at the final head. Plans only, no spend (costs of an\n"
     "  earlier round's cards): chief-of-staff with griller 54 runs, about")
pair("release-driver 3,811 (+739)", "release-driver 3,809 (+737)")
pair("pr-extras 1,898", "pr-extras 1,896")
pair("release-notes\n  2,063,", "release-notes\n  2,055,")
start = body.index("- The home of each protecting row was read at its cited line.")
end = body.index("- Rules, or parts of rules, held by no card", start)
pair(body[start:end], """- Inventory homes: of the 4,224 rows of the four inventories, 3,916 name a text home under `cards-next/`.
  A script compared each one's source sentences at the base with its home's words. At least 1,835 of
  them, every row it still flags included, were read by hand against the home, and the losses found were
  fixed. The other rows (at most 2,081) were not read by hand in that pass, and a lost condition worded
  with the home's own words can escape the script. Each of the four inventories lists the
  protecting-looking rows a topic carries, for the later review.
""")

pair("batch-close-stopped, batch-end,", "batch-close-stopped, batch-end,") if False else None
pair("- All topic names: allow-rules, allow-rules-more, asks,",
     "- All topic names: allow-rules, allow-rules-more, ask-lines, asks,")
pair("grill-critic-steps, grill-options,", "grill-critic-steps, grill-example, grill-options,")

pair("- [x] Local gates at the head: `just check` at `03f973e`: 2932 passed, 20 skipped",
     "- [x] Local gates: `just check` on the tree of the last commit, run before the commit: 2933 passed, 19 skipped")
pair("- [x] Evidence at `03f973e`:", "- [x] Evidence on that tree:")
pair("`git rev-parse HEAD:<path>` gives the same blob under", "`git hash-object <path>` gives the same blob under")
pair("`git grep -n cards-next HEAD -- . ':(exclude)skills/chantier/cards-next'` prints no line,",
     "`git grep --untracked -n cards-next -- . ':(exclude)skills/chantier/cards-next'` prints no line,")
pair("and `git grep -n \"Read this short role contract at boot\\|# chantier-agent:\\|chantier board\" HEAD --\n"
     "    skills/chantier/cards-next` prints no line;",
     "and `git grep --untracked -n \"Read this short role contract at boot\\|# chantier-agent:\\|chantier board\" --\n"
     "    skills/chantier/cards-next` prints no line;")
pair("topic index: 238 topics load, 447 readings resolve", "topic index: 240 topics load, 463 readings resolve")
pair("- [x] Review: approved at `03f973e` (carried from `bb6a563`)",
     "- [ ] Review: owed at the head (approved at `03f973e`, before the last changes)")

result = body
for p in pairs:
    count = body.count(p["old"])
    assert count == 1, (count, p["old"])
    assert result.count(p["old"]) == 1, p["old"]
    result = result.replace(p["old"], p["new"])
(HERE.parent / "r10-body.json").write_bytes((json.dumps(pairs, ensure_ascii=False, indent=1) + "\n").encode("utf-8"))
print(len(pairs), "pairs, each old once")
for stale in (r"\b238\b", r"\b447\b", r"3,999", r"3,524", r"3,811", r"1,898", r"2,063", r"22,278", r"46,935", r"concepts\.md` \(line 121\)"):
    assert not re.search(stale, result), stale
names = result.split("- All topic names: ", 1)[1].split("\n\n", 1)[0]
listed = {n.strip(" .") for n in re.split(r",\s+", names)}
current = json.loads(Path("C:/Users/gaeta/Projets/chantier.worktrees/batch-31-CR-507/skills/chantier/cards-next/"
                          "topics.json").read_text(encoding="utf-8"))["topics"]
assert listed == set(current), (set(current) ^ listed)
print("topic names:", len(listed))
print("mentions of 03f973e left:", [line for line in result.split("\n") if "03f973e" in line])
for line in result.split("\n"):
    if line.startswith("| topics"):
        print(line)
