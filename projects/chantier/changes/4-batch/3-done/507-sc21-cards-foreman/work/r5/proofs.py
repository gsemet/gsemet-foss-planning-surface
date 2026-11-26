"""Write evidence/part3-proofs.md from the working tree as it will be committed (nothing is
committed here). Reads the repository only; writes the evidence file and a staging copy of
concepts.md for proof 8. briefs.json comes from briefs.py, run first."""

import json
import re
import shutil
import subprocess
from pathlib import Path

import chantier
import chantier.driver_prompt as dp

WT = Path("C:/Users/gaeta/Projets/chantier.worktrees/batch-31-CR-507")
SKILL = WT / "skills/chantier"
CN = SKILL / "cards-next"
REFS = SKILL / "references"
CR = Path("C:/Users/gaeta/Projets/gsemet-foss-planning-surface/projects/chantier/changes/4-batch/"
          "2-actives/507-sc21-cards-foreman")
R5 = CR / "work/r5"
OUT = CR / "evidence/part3-proofs.md"
BASE = "bf4e4c42"
EXCLUDE = ":(exclude)skills/chantier/cards-next"
out: list[str] = []


def say(*lines: str) -> None:
    out.extend(lines)


def block(command: str, text: str) -> None:
    say("```text", f"$ {command}", *(text.rstrip("\n").split("\n") if text.strip() else []), "```", "")


def run(*cmd: str) -> tuple[int, str]:
    p = subprocess.run(list(cmd), capture_output=True, text=True, encoding="utf-8", errors="replace",
                       cwd=str(WT))
    return p.returncode, p.stdout + p.stderr


def git(*args: str) -> tuple[int, str]:
    return run("git", "-C", str(WT), *args)


def lf_bytes(path: Path) -> bytes:
    return path.read_bytes().replace(b"\r\n", b"\n")


def size(path: Path) -> int | None:
    return len(lf_bytes(path)) if path.is_file() else None


def blob(rel: str) -> int | None:
    p = subprocess.run(["git", "-C", str(WT), "cat-file", "-s", f"{BASE}:{rel}"], capture_output=True)
    return int(p.stdout) if p.returncode == 0 else None


def num(n: int | None) -> str:
    return "none" if n is None else f"{n:,}"


def verdict(new: int | None, target: int | None) -> str:
    if target is None:
        return "no target"
    return "within" if new <= target else f"over by {new - target:,}"


head = git("rev-parse", "--short=8", "HEAD")[1].strip()
assert head == BASE, head
say("# PART 3 proofs (round 5)", "",
    f"Worktree `{WT.as_posix()}`, head `{head}` plus the uncommitted changes of rounds 4 and 5: "
    "nothing is committed, so every command runs against the working tree (the files as they will "
    "be committed), and where the specification says `HEAD` the comparison is stated. Byte counts "
    "are LF bytes (the checkout has `core.autocrlf=true`). Written by `work/r5/proofs.py`.", "")

# 2
say("## 2. Byte-identical copies", "",
    f"`git hash-object` of the working file (the checkout's filters applied) against the blob at "
    f"`{BASE}` under `references/`.", "")
lines = []
for rel in ("floor.md", "hosts/claude-code.json", "hosts/copilot.json"):
    new = git("hash-object", "--path", f"skills/chantier/cards-next/{rel}", str(CN / rel))[1].strip().split("\n")[-1]
    old = git("rev-parse", f"{BASE}:skills/chantier/references/{rel}")[1].strip()
    same = lf_bytes(CN / rel) == lf_bytes(REFS / rel)
    lines.append(f"{rel}: cards-next {new} | references at {BASE} {old} | "
                 f"{'identical' if new == old else 'DIFFERENT'}; LF content equal: {same}")
    assert new == old and same, rel
block("work/r5/proofs.py (proof 2)", "\n".join(lines))

# 3
say("## 3. Bytes", "", "| file | today | new | target | result |", "| --- | ---: | ---: | --- | --- |")
rows = [
    ("concepts.md", None, "none set (open question 1)"),
    ("pr-template.md", None, "none set (open question 1)"),
    ("release-template.md", None, "none set (open question 1)"),
    ("status-layout.md", None, "none set (open question 1)"),
    ("titles.md", 1500, "1,500 if a topic (folded into `topics/titles.md`)"),
    ("ticket-summary-example.md", None, "none set (may fold into a topic)"),
    ("routing.md", None, "none set (open question 1)"),
    ("init.md", None, "none set (open question 1)"),
    ("review-step.md", 1500, "1,500"),
    ("sync-checkout.md", 1500, "1,500 if a topic"),
    ("forges/github.md", 739, "unchanged or smaller (739)"),
    ("forges/gitlab.md", 744, "unchanged or smaller (744)"),
    ("hosts/claude-code.json", blob("skills/chantier/references/hosts/claude-code.json"), "byte-identical"),
    ("hosts/copilot.json", blob("skills/chantier/references/hosts/copilot.json"), "byte-identical"),
    ("hosts/claude-code.md", None, "no byte target: Allow rules section only"),
    ("hosts/copilot.md", None, "not carried: its text is in `topics/host-*.md`"),
    ("floor.md", 1200, "1,200, byte-identical"),
]
for rel, target, label in rows:
    today = blob(f"skills/chantier/references/{rel}")
    if rel == "titles.md":
        new = size(CN / "topics/titles.md")
        say(f"| {rel} -> topics/titles.md | {num(today)} | {num(new)} | {label} | {verdict(new, target)} |")
        continue
    new = size(CN / rel)
    result = "no target (file not carried)" if new is None else verdict(new, target)
    say(f"| {rel} | {num(today)} | {num(new)} | {label} | {result} |")
topic_files = sorted((CN / "topics").glob("*.md"))
committed = set(git("ls-tree", "-r", "--name-only", BASE, "--", "skills/chantier/cards-next/topics")[1].split())
new_topics = [p for p in topic_files if f"skills/chantier/cards-next/topics/{p.name}" not in committed]
hosts = [p for p in topic_files if p.name.startswith("host-")]
for label, group in (("topics/host-*.md", hosts), ("topics/<name>.md (others)", [p for p in topic_files if p not in hosts])):
    over = [p for p in group if size(p) > 1500]
    say(f"| {label}: {len(group)} files | part of the above | {sum(map(size, group)):,} in all, "
        f"largest {max(map(size, group)):,} | 1,500 each | "
        f"{f'{len(over)} over (listed below)' if over else 'within'} |")
say(f"| topics.json | {num(blob('skills/chantier/references/topics.json'))} | {num(size(CN / 'topics.json'))} | none set | no target |")
for name in ("chantier", "chief-of-staff", "griller", "status"):
    say(f"| skills/{name}-SKILL.md | {num(blob(f'skills/{name}/SKILL.md'))} | {num(size(CN / 'skills' / f'{name}-SKILL.md'))} | section 6 (no byte target) | no target |")
say("", f"New topic files of this uncommitted work (not in `{BASE}`): {len(new_topics)}, largest "
    f"{max(map(size, new_topics)):,} bytes ({max(new_topics, key=size).name}); over 1,500: "
    f"{[p.name for p in new_topics if size(p) > 1500] or 'none'}.", "")
assert all(size(p) <= 1500 for p in new_topics)
say("Every topic over 1,500 (each exists at the base head of this round):", "",
    f"| topic file | at {BASE} | new | over by |", "| --- | ---: | ---: | ---: |")
over_topics = [p for p in topic_files if size(p) > 1500]
for p in over_topics:
    say(f"| topics/{p.name} | {num(blob(f'skills/chantier/cards-next/topics/{p.name}'))} | {size(p):,} | {size(p) - 1500:,} |")
say("")
say("Role cards of the whole branch (Foreman, Chief of Staff and Griller against their budgets; "
    "the others because this round edits them). `references` is today's card at the base; the "
    "base's Chief of Staff and Griller cards are the two `SKILL.md`.", "",
    f"| card | references | at {BASE} | new | budget | result |", "| --- | ---: | ---: | ---: | ---: | --- |")
cards = [
    ("foreman.md", "references/foreman.md", 4000), ("chief-of-staff.md", "references/chief-of-staff.md", 6000),
    ("griller-skill.md", "references/griller-skill.md", 4000), ("griller.md", "references/griller.md", 2000),
    ("coder.md", None, 1500), ("conflict-resolver.md", None, 1500), ("debugger.md", None, 1500),
    ("demo-explorer.md", None, 1500), ("investigator.md", None, 1500), ("retro-critic.md", None, 1500),
    ("spec-critic.md", None, 1500), ("spec-writer.md", None, 1500), ("inspector.md", None, 2000),
    ("verifier.md", None, 3000), ("cr-driver.md", None, 4096), ("stack-driver.md", None, 4096),
    ("release-driver.md", None, 3072), ("qa-driver.md", None, 2048),
]
over_cards = []
for name, ref, budget in cards:
    ref = ref or f"references/{name}"
    new = size(CN / name)
    say(f"| {name} | {num(blob('skills/chantier/' + ref))} | {num(blob(f'skills/chantier/cards-next/{name}'))} | {new:,} | {budget:,} | {verdict(new, budget)} |")
    if new > budget:
        over_cards.append((name, new, new - budget, blob(f"skills/chantier/cards-next/{name}")))
say("")

# 4
data = json.loads((R5 / "briefs.json").read_text(encoding="utf-8"))
study = {
    "chief-of-staff": "11,636 / 11,708 / 202,396", "griller": "11,197 / 11,267 / 145,087",
    "foreman": "7,740 / 8,566 / 91,019", "cr-driver": "8,519 / 10,541 / 27,180",
    "stack-driver": "8,542 / 10,564 / 34,054", "qa-driver": "8,468 / 10,490 / 24,122",
    "release-driver": "8,577 / 10,599 / 25,806", "verifier": "8,556 / 9,382 / 23,963",
    "inspector": "8,552 / 9,378 / 15,422", "coder": "8,531 / 9,357 / 13,966",
    "board-griller": "10,242 / 11,096 / 19,655",
}
other = "no own row (\"Other workers\": 8.2 to 8.7 KB / +826 / +826)"
say("## 4. `brief` for all 18 roles", "",
    "Command, from the worktree's CLI: `uv run --no-sync --project <worktree> chantier --project "
    "<planning folder of chantier> brief <role> [unit] [--lease n] --batch batch-31 [--cards "
    "<worktree>/skills/chantier/cards-next]`. The CLI of the main checkout has no `brief` command "
    f"(exit {data['main_cli']['exit']}, argparse usage), so the worktree's is the one that runs. "
    "Batch-31's host is `claude`, so every row is the Claude column; Copilot is untested.", "",
    "`brief` records nothing. It writes `<planning surface's git folder>/chantier/briefs/chantier/"
    "batch-31/<name>-<role>.md`; each path was written by the new-cards run and then by the "
    "today's-cards run, so the files left there hold today's cards. Bytes were read after each run.", "",
    "study-fable-v2 (section 2.2) gives \"boot, base / boot, new / start, new Claude\". Its boot is "
    "the declared readings (cores, manifest, wrapper or skill, startup sections), another measure "
    "than the brief file's bytes.", "",
    "### The runs as the specification gives them", "",
    "| role | unit (lease) | new: exit, bytes | old: exit, bytes | study-fable-v2 |",
    "| --- | --- | --- | --- | --- |")
units = {"cr-driver": "CR-507 (2)", "release-driver": "CR-507 (2)", "stack-driver": "stack (11)",
         "qa-driver": "O-1 (1)", "spec-writer": "this CR folder", "spec-critic": "this CR folder",
         "board-griller": "this CR folder"}
for r in ("coder", "conflict-resolver", "debugger", "inspector", "investigator", "verifier"):
    units[r] = "CR-507"


def cell(x: dict) -> str:
    return f"0, {x['bytes']:,}" if x["exit"] == 0 else f"{x['exit']}, refused"


for role in data["roles"]:
    r = data["spec"][role]
    say(f"| {role} | {units.get(role, 'none')} | {cell(r['new'])} | {cell(r['old'])} | {study.get(role, other)} |")
ok = [r for r in data["roles"] if data["spec"][r]["new"]["exit"] == 0]
bad = [r for r in data["roles"] if r not in ok]
say("", f"With `--cards`, {len(ok)} of {len(data['roles'])} roles exit 0 as specified; refused: "
    f"{', '.join(bad)}. **\"Each exits 0\" is not met.** The refusals, quoted:", "")
text = []
for role in data["roles"]:
    for kind in ("new", "old"):
        x = data["spec"][role][kind]
        if x["exit"]:
            text.append(f"[{role}, {kind}] exit {x['exit']}: {x['text']}")
block("brief ... (refusals)", "\n".join(text))
say("Causes:", "",
    "- The four Drivers, new cards: `roles.yaml` names their card `driver.md`, which `cards-next/` "
    "does not hold (it holds `cr-driver.md`, `stack-driver.md`, `release-driver.md`, "
    "`qa-driver.md`). `brief` reads the card before the facts, so even a role-only brief is "
    "refused. The specification's \"For child 24\" names the Chief of Staff's and the Griller's "
    "`card` only: child 24 must change the Drivers' too (and `concepts.md`'s Driver table, whose "
    "card cell stays `driver.md` here by section 2.1).",
    "- The three folder roles: this CR is in `4-batch/`, and `brief` takes an inbox, backlog or "
    "`3-ready` folder only (old cards refused the same).",
    "- release-driver, stack-driver, qa-driver, old cards: batch-31 holds no release CR, no live "
    "`stack` lease 11 and no open QA order `O-1` (a finished `add` order).", "",
    "### Extra runs, not the specified ones", "",
    "A staging folder per Driver (`work/r5/staging/<role>/`: `driver.md` copied from "
    "`cards-next/<role>.md`, plus `floor.md`), as the sibling CR-505's evidence did; and an inbox "
    "item (`1-inbox/simplify-cards-and-prompts`, a CR folder in the specification's sense) for "
    "the folder roles.", "",
    "| role | unit | new: exit, bytes | old: exit, bytes |", "| --- | --- | --- | --- |")
for role, runs in data["drivers_staged"].items():
    for unit, r in runs.items():
        say(f"| {role} (staged) | {'none (role only)' if unit == 'role-only' else unit + ' (lease 2)'} | {cell(r['new'])} | {cell(r['old'])} |")
for role, r in data["inbox"].items():
    say(f"| {role} | the inbox item | {cell(r['new'])} | {cell(r['old'])} |")
say("", "The Chief of Staff's and the Griller's new briefs are larger than the old ones: today's "
    "`card` for them is the short `SKILL.md`, which then sends the session to its readings; the "
    "new brief holds the whole card.", "")

# 5
changed = sorted(
    p.removeprefix("skills/chantier/cards-next/")
    for p in git("diff", "--name-only", BASE, "--", "skills/chantier/cards-next/*.md")[1].split("\n")
    if p.startswith("skills/chantier/cards-next/") and "/topics/" not in p
)
roles_changed = sorted({c.removesuffix(".md").replace("griller-skill", "griller").replace("griller", "griller")
                        for c in changed})
card_role = {"griller-skill.md": "griller", "griller.md": "board-griller"}
roles_changed = sorted({card_role.get(c, c.removesuffix(".md")) for c in changed if c.removesuffix(".md") in data["roles"] or c in card_role})
quiz = {r: (WT / "evals/quiz" / r).is_dir() and any((WT / "evals/quiz" / r).glob("*.json")) for r in roles_changed}
say("## 5. Quiz (not run)", "",
    f"No quiz was run (the brief: `just quiz` is not run). Roles whose card changed against "
    f"`{BASE}` ({len(roles_changed)} of {len(data['roles'])}; unchanged: "
    f"{', '.join(r for r in data['roles'] if r not in roles_changed) or 'none'}):", "",
    "| role | cases under `evals/quiz/<role>/` |", "| --- | --- |")
for r in roles_changed:
    say(f"| {r} | {'yes: quiz owed' if quiz[r] else 'none: no quiz owed'} |")
say("", "Quiz case change of round 4: `evals/quiz/chief-of-staff/a8-ask-foreign-branch.json` "
    "removed, `a8-push-refused-default-branch.json` added.", "")


# 6
def slug(h: str) -> str:
    h = re.sub(r"[`*]", "", h.strip().lower())
    return re.sub(r"[^\w\- ]", "", h).replace(" ", "-")


def anchors(p: Path) -> set[str]:
    return {slug(h) for h in re.findall(r"^#{1,6} (.*)$", p.read_text(encoding="utf-8"), re.M)}


links, broken, scanned = [], [], 0
for p in sorted(CN.rglob("*")):
    if not p.is_file() or p.suffix not in (".md", ".json"):
        continue
    scanned += 1
    if p.suffix != ".md":
        continue
    rel = p.relative_to(CN).as_posix()
    body = re.sub(r"```.*?```", lambda m: "\n" * m.group(0).count("\n"), p.read_text(encoding="utf-8"), flags=re.S)
    for m in re.finditer(r"\]\(([^)\s]+)\)", body):
        target = m.group(1)
        n = body[: m.start()].count("\n") + 1
        if re.match(r"[a-z]+:", target):
            links.append((rel, n, target, "web link (not relative)"))
            continue
        path, _, frag = target.partition("#")
        if rel.startswith("skills/"):
            home = WT / "skills" / p.name.removesuffix("-SKILL.md")
            if path.startswith("../chantier/references/"):
                q = CN / path.removeprefix("../chantier/references/")
            else:
                q = home / path
        else:
            q = p.parent / path if path else p
        q = q.resolve()
        problem = ""
        if not q.exists():
            problem = "BROKEN: no such file"
        elif frag and q.suffix == ".md" and frag not in anchors(q):
            problem = "BROKEN: no such heading"
        elif q.is_relative_to(REFS.resolve()):
            problem = "BROKEN: into references/"
        elif (not q.is_relative_to(CN.resolve()) and not (rel.startswith("forges/") and q.is_relative_to((WT / "docs").resolve()))
              and q != (SKILL / "assets/tour.html").resolve()):
            problem = "BROKEN: outside cards-next/"
        where = q.relative_to(WT.resolve()).as_posix() if q.is_relative_to(WT.resolve()) else q.as_posix()
        shown = where.removeprefix("skills/chantier/")
        if not problem and not q.is_relative_to(CN.resolve()):
            shown += " (outside cards-next/, from the target depth)"
            if rel == "init.md":
                assert f"]({target})" in (REFS / "init.md").read_text(encoding="utf-8")
        links.append((rel, n, target, problem or shown))
        if problem:
            broken.append((rel, n, target, problem))
say("## 6. Links", "",
    f"{scanned} `.md` and `.json` files under `cards-next/` read; fenced blocks skipped. "
    "`skills/*-SKILL.md` links resolve under section 6's mapping (`../chantier/references/` to "
    "`cards-next/`, `./` to `skills/<skill>/`); `forges/` links to `docs/` resolve from the same "
    f"depth as `references/forges/`. Links: {len(links)}; broken: {len(broken)}; no link points into "
    "`references/`. Outside `cards-next/`: the two `forges/` links to `docs/`, and one more the "
    "specification's wording does not name, `init.md`'s link to the shipped asset "
    "`assets/tour.html` (today's link, unchanged; it resolves from the same depth after the swap).", "",
    "| file:line | link | resolves to |", "| --- | --- | --- |")
for rel, n, target, where in links:
    say(f"| {rel}:{n} | `{target}` | {where} |")
say("")
into = git("grep", "--untracked", "-n", "references/", "--", "skills/chantier/cards-next")
say("Text naming `references/` (not links), quoted:", "")
block("git grep --untracked -n \"references/\" -- skills/chantier/cards-next  (long lines cut at 220)",
      "\n".join(line[:220] for line in into[1].splitlines()) + f"\n(exit {into[0]})")
assert not broken, broken

# 7
code, text = run("uv", "run", "--no-sync", "--project", str(WT), "python", str(R5 / "topics_check.py"))
say("## 7. `topics.json`", "", "Throwaway script `work/r5/topics_check.py`, with `load_topics` from "
    "`commands/help.py`. No base name is renamed.", "")
block("uv run --no-sync --project <worktree> python work/r5/topics_check.py", text + f"(exit {code})")
assert code == 0

# 8
stage = R5 / "dp-stage"
(stage / "references").mkdir(parents=True, exist_ok=True)
shutil.copyfile(CN / "concepts.md", stage / "references/concepts.md")
base_rows = dp.driver_table()
real = dp.skill_dir
dp.skill_dir = lambda: stage
new_rows = dp.driver_table()
dp.skill_dir = real
cr_grep = git("grep", "--untracked", "-n", "Change Request", "--", "skills/chantier/cards-next/concepts.md")
say("## 8. The Driver table", "",
    "`driver_prompt.driver_table()` reads `skill_dir()/references/concepts.md`; for the new file "
    "`skill_dir` was pointed at a staging folder holding a copy of `cards-next/concepts.md` "
    "(`work/r5/dp-stage/`).", "")
block("work/r5/proofs.py (proof 8)",
      f"parser from {Path(dp.__file__).as_posix()}\nrows, references/concepts.md: {len(base_rows)}\n"
      f"rows, cards-next/concepts.md: {len(new_rows)}\nequal, cell for cell: {base_rows == new_rows}\n"
      + "\n".join(repr(r) for r in (new_rows.values() if isinstance(new_rows, dict) else new_rows)))
block("git grep --untracked -n \"Change Request\" -- skills/chantier/cards-next/concepts.md",
      "\n".join(line[:220] for line in cr_grep[1].splitlines()) + f"\n(exit {cr_grep[0]})")
assert base_rows == new_rows and len(new_rows) == 4 and cr_grep[0] == 0

# the Allow rules checks
say("## The Allow rules section (section 3)", "",
    "The named test reads today's `references/hosts/claude-code.md`, which this child does not "
    "edit; `work/r5/allow_check.py` runs the same assertions on `cards-next/hosts/claude-code.md`.", "")
test = ("skills/chantier/scripts/cli/tests/test_cli_runs.py::"
        "test_the_allow_rules_json_block_lists_exactly_what_preflight_checks")
code, text = run("uv", "run", "--no-sync", "--project", str(WT), "pytest", test, "-q", "-p", "no:cacheprovider")
print("pytest", code, text[-1500:])
block(f"pytest {test}", text + f"(exit {code})")
code2, text2 = run("uv", "run", "--no-sync", "--project", str(WT), "python", str(R5 / "allow_check.py"))
block("python work/r5/allow_check.py", text2 + f"(exit {code2})")
assert code == 0 and code2 == 0
say(f"`hosts/claude-code.md`: {num(blob('skills/chantier/references/hosts/claude-code.md'))} bytes today, "
    f"{num(size(CN / 'hosts/claude-code.md'))} new. Round 5 cut the dated trial text and stories from the "
    "kept section (the JSON block and the Capabilities table unchanged); the file before the cut is "
    "`work/r5/claude-code.before.md`, and the cut stories are already told in `docs/proofs/claude-code.md`.", "")

# 9 to 11
say("## 9. `just test`", "", "No test is added or changed (`git diff --name-only` against the base "
    "shows nothing under any `tests/` folder). Base and head times were not measured separately.", "",
    "## 10. Inventory and completeness table", "",
    "`evidence/cards-inventory-host-and-shared.md` (how the sources were walked, the rows, the "
    "manifest action table, the completeness table, the sibling-card edits with their lines), "
    "written by `work/r5/gen.py`.", "",
    "## 11. Unloaded", "", "Run against the working tree with `--untracked`, since nothing is committed.", "")
for args in (["grep", "--untracked", "-n", "cards-next", "--", ".", EXCLUDE],
             ["grep", "--untracked", "-n",
              "Read this short role contract at boot\\|# chantier-agent:\\|chantier board",
              "--", "skills/chantier/cards-next"]):
    code, text = git(*args)
    shown = "git " + " ".join(f'"{a}"' if any(c in a for c in " :|") else a for a in args)
    block(shown, text + f"(no line; exit {code})" if not text.strip() else text + f"(exit {code})")
    assert code == 1 and not text.strip(), (args, code, text)
tests = [p for p in git("status", "--porcelain", "--untracked-files=all")[1].splitlines() if "tests/" in p]
assert not tests, tests

say("## 12. Gates (round 5, on the uncommitted working tree)", "",
    "- `just check` from the PowerShell tool, whose environment sets `NO_COLOR=1`: exit 1, `2 failed, "
    "2930 passed, 20 skipped`; both failures are `test_live_ready.py::"
    "test_the_interactive_screen_links_the_pr_and_colours_the_state_words` (it expects colour codes, "
    "which rich drops under `NO_COLOR`). No file of `src/` or `tests/` is changed by this CR.",
    "- `just check` from the Bash tool, where `NO_COLOR` is not set, same tree: exit 0, `2932 passed, "
    "20 skipped`.",
    "- Not run here: `just quiz`, `just scenario (ubuntu-latest)` and the local `scenario` gate "
    "(they need the pushed head; the Driver's part).", "")

# gaps
say("## Known gaps", "",
    "- **\"Each exits 0\" (item 4) is not met**: " + ", ".join(bad) + " are refused as specified "
    "(quoted above). The four Drivers with `--cards` need `roles.yaml`'s `card` changed at the "
    "swap (child 24).",
    "- **Cards over budget** (Q4): " + "; ".join(
        f"`{n}` {s:,} (over by {o:,}; {b:,} at `{BASE}`)" for n, s, o, b in over_cards) + ". The "
    "bytes are rules whose home must be a card (kind a) and the pointer to `help session-shell`; "
    "a sibling card's other lines are not this child's to cut (section 1), and only the owner raises "
    "a budget. `retro-critic.md` and `spec-critic.md` are over by the pointer line alone: without it "
    "they are within, and the folder-change ban reaches them through the topic's role list only.",
    f"- **Topics over 1,500** (Q4): {len(over_topics)}, listed in item 3; all exist at `{BASE}`. "
    "This round grew `release-notes.md` and `cr-rounds.md` (a link and a pointer).",
    "- Real run not done (child 28). Quiz not run (item 5). Copilot untested.",
    "- Do not merge: merges with children 19 to 28 as one unit, after child 28's campaign.", "")
# no home folder in a published file
final = "\n".join(out).rstrip("\n") + "\n"
surface = CR.parents[5]
for path, name in ((WT, "<worktree>"), (surface / "projects/chantier", "<planning>"), (surface, "<surface>")):
    for form in (path.as_posix(), str(path)):
        final = re.sub(re.escape(form), name, final, flags=re.I)
assert not re.search(r"(?i)Users[\\/](?!<user>)", final), re.findall(r"(?i).{40}Users[\\/].{40}", final)
say_note = ("Paths: `<worktree>` is the CR's worktree, `<surface>` the planning surface's checkout, "
            "`<planning>` its `projects/chantier` folder.")
final = final.replace("Written by `work/r5/proofs.py`.", f"Written by `work/r5/proofs.py`. {say_note}")
OUT.write_bytes(final.encode("utf-8"))
print(f"wrote {OUT.as_posix()}: {OUT.stat().st_size} bytes; links {len(links)}; broken {len(broken)}; "
      f"over cards {[(n, o) for n, _, o, _ in over_cards]}; over topics {len(over_topics)}; "
      f"new topics {len(new_topics)}; roles changed {len(roles_changed)}; chantier {chantier.__version__}")
