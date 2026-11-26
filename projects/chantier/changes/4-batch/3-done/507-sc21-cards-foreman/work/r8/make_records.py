"""Make work/r8/records.py from work/r7/records.py: round 8's brief log and wording, and the new
(untracked) files counted through a copy of the index, so the worktree's own index is not touched."""

from pathlib import Path

R8 = Path(__file__).parent
src = (R8.parent / "r7/records.py").read_text(encoding="utf-8")


def swap(old: str, new: str, count: int = 1) -> None:
    global src
    assert src.count(old) == count, (old, src.count(old))
    src = src.replace(old, new)


swap('"""Write evidence/acceptance-records.md from git, work/quiz-plan and brief logs of round 7."""',
     '"""Write evidence/acceptance-records.md from git, round 7\'s quiz plan and round 8\'s brief log."""')
swap("import subprocess\nimport sys\n", "import os\nimport shutil\nimport subprocess\nimport sys\n")
swap('''head = git("rev-parse", "HEAD")''', '''index = HERE / "stat.index"
shutil.copyfile(Path(WT) / git("rev-parse", "--git-path", "index"), index)
os.environ["GIT_INDEX_FILE"] = str(index)
new_files = git("ls-files", "--others", "--exclude-standard").split("\\n")
git("add", "--intent-to-add", "--", *new_files)
head = git("rev-parse", "HEAD")''')
swap('''assert not [x for x in git("status", "--porcelain").split("\\n") if not x.startswith(" M ")]''',
     '''assert all(p.startswith("skills/chantier/cards-next/topics/") for p in new_files), new_files''')
swap('(HERE / "quiz-plan.log")', '(HERE.parent / "r7/quiz-plan.log")')
swap('(HERE / "briefs7.log")', '(HERE / "briefs8.log")')
swap("plus this round's uncommitted card edits unless", "plus the uncommitted changes of rounds 7 and 8 unless")
swap("`just check` on this round's working tree", "`just check` on round 8's working tree")
swap("| `brief foreman` | 55,206 | 22,279 |", "| `brief foreman` | 55,206 | 22,278 |")
swap("| `brief griller` | 6,349 | 6,627 |", "| `brief griller` | 6,349 | 6,650 |")
swap("| 77,528 | 46,936 |", "| 77,528 | 46,935 |")
swap("Plan only: `--plan` stops", "Round 7's run (no case, no `roles.yaml` line changed since). Plan only: `--plan` stops")
swap('''print(len(out.splitlines()), "lines;", len(outside), "outside")''',
     '''index.unlink()
print(len(out.splitlines()), "lines;", len(outside), "outside;", len(new_files), "new files")''')
(R8 / "records.py").write_text(src, encoding="utf-8", newline="\n")
print("written")
