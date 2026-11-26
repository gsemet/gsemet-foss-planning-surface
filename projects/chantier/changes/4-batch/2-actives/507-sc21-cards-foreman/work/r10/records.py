"""Round 10 (round 9's script, updated): write evidence/acceptance-records.md from git, round 7's
quiz plan and round 10's brief log."""

import os
import shutil
import subprocess
import sys
from pathlib import Path

WT = "C:/Users/gaeta/Projets/chantier.worktrees/batch-31-CR-507"
HERE = Path(__file__).parent
CR = HERE.parents[1]
JUST = sys.argv[1] if len(sys.argv) > 1 else None


def git(*args: str) -> str:
    return subprocess.run(["git", "-C", WT, *args], capture_output=True, text=True, encoding="utf-8",
                          check=True).stdout.rstrip("\n")


def clean(text: str) -> str:
    return text.replace(WT, "<worktree>")


index = HERE / "stat.index"
shutil.copyfile(Path(WT) / git("rev-parse", "--git-path", "index"), index)
os.environ["GIT_INDEX_FILE"] = str(index)
new_files = git("ls-files", "--others", "--exclude-standard").split("\n")
git("add", "--intent-to-add", "--", *new_files)
head = git("rev-parse", "HEAD")
assert head.startswith("03f973e4"), head  # the head work/verify.md measured
base = git("rev-parse", "origin/main")
stat = git("diff", "--stat=200", "origin/main")
outside = [p for p in git("diff", "--name-only", "origin/main").split("\n")
           if not p.startswith("skills/chantier/cards-next/")]
assert all(p.startswith("evals/quiz/") for p in outside), outside
assert all(p.startswith("skills/chantier/cards-next/topics/") for p in new_files), new_files
griller = git("diff", "origin/main", "--", "skills/chantier/cards-next/griller.md")
quiz = clean((HERE.parent / "r7/quiz-plan.log").read_text(encoding="utf-8")).rstrip("\n")
briefs = (HERE / "briefs8.log").read_text(encoding="utf-8").rstrip("\n")

out = f"""# Acceptance records

Base: `{base}` (origin/main). Head: `{head}`, plus the uncommitted changes of rounds 7 to 10 unless a line says otherwise.

## `just test`, base and head (Part 1.7, Part 2.8, Part 3.9)

No test is added or changed. Same machine, one run after the other (`work/verify.md`, C25):

```text
base {base[:8]}: 2932 passed, 20 skipped in 192.40s (wall 197.9 s)
head {head[:8]}:  2932 passed, 20 skipped in 171.16s (wall 172.6 s)
```

0 seconds added; the difference between the two is run-to-run variation, not a speed-up.
{{JUST}}
## Brief bytes beside the old start readings (Part 1.3, Part 2.3)

Old start readings, as the specification gives them (study-fable-v2; not measured again):

| role | declared | measured |
| --- | ---: | ---: |
| Foreman | 91 KB | 144 KB |
| Chief of Staff | 202 KB | 218 KB |
| Griller | 145 KB | 36 KB |

`brief`, batch-31, host claude, today's cards (old) and `--cards <worktree>/skills/chantier/cards-next` (new), the working tree's cards. LF bytes of the brief file (round 10's run, `work/r10/briefs8.py`; a unit's brief also holds the unit's facts from the record, so the `coder` bytes move with it):

```text
{briefs}
```

| reading | old | new |
| --- | ---: | ---: |
| `brief foreman` | 55,206 | 22,276 |
| `brief chief-of-staff` | 22,322 | 24,657 |
| `brief griller` | 6,349 | 6,747 |
| direct mode: `brief chief-of-staff` + `brief foreman --epoch 1` | 77,528 | 46,933 |

## `just quiz --plan` (Part 1.4, Part 2.4, Part 3.5)

Round 7's run: no case and no `roles.yaml` line changed since, but cards did, so the cost figures are those of round 7's cards. Plan only: `--plan` stops before any model call, so no model run and no spend. `claude-opus-5-5` is the session roles' `--model`, as the Verifier ran it. The three Driver roles cannot be planned on this set: `roles.yaml` names `driver.md`, which `cards-next/` does not hold. The session roles' plans are above the default `--max-usd 10`. `inspector`, `investigator` and `qa-driver` have no folder under `evals/quiz/`.

```text
{quiz}
```

## `git diff origin/main -- skills/chantier/cards-next/griller.md` (Part 2.1)

```diff
{griller}
```

## `git diff --stat origin/main` (Part 1.1, Part 2.1, Part 3.1)

Every path is under `skills/chantier/cards-next/` but the {len(outside)} under `evals/quiz/`. `--stat=200` keeps the paths whole.

```text
{stat}
```
"""
just = ""
if JUST:
    just = f"\n`just check` on round 10's working tree (tests beside the other checks, so not a timing comparison): `{JUST}`.\n"
out = out.replace("{JUST}", just)
for bad in ("gaeta", "C:/Users", "C:\\Users"):
    assert bad not in out, bad
(CR / "evidence/acceptance-records.md").write_bytes(out.encode("utf-8"))
index.unlink()
print(len(out.splitlines()), "lines;", len(outside), "outside;", len(new_files), "new files")
