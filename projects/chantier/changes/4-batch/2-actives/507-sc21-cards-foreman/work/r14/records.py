"""Round 14 (round 13's script): refresh in evidence/acceptance-records.md the diff stat block, the rounds named on
line 3 and the `just check` line. The rest of the file is kept."""

import os
import re
import shutil
import subprocess
from pathlib import Path

WT = "C:/Users/gaeta/Projets/chantier.worktrees/batch-31-CR-507"
HERE = Path(__file__).resolve().parent
FILE = HERE.parents[1] / "evidence/acceptance-records.md"


def git(*args: str) -> str:
    return subprocess.run(["git", "-C", WT, *args], capture_output=True, text=True, encoding="utf-8",
                          check=True).stdout.rstrip("\n")


def once(pattern: str, new: str, text: str) -> str:
    text, count = re.subn(pattern, lambda _: new, text)
    assert count == 1, (pattern, count)
    return text


index = HERE / "stat.index"
shutil.copyfile(Path(WT) / git("rev-parse", "--git-path", "index"), index)
os.environ["GIT_INDEX_FILE"] = str(index)
new_files = git("ls-files", "--others", "--exclude-standard").split("\n")
git("add", "--intent-to-add", "--", *new_files)
assert git("rev-parse", "HEAD").startswith("03f973e4")
stat = git("diff", "--stat=200", "origin/main")
outside = [p for p in git("diff", "--name-only", "origin/main").split("\n")
           if not p.startswith("skills/chantier/cards-next/")]
assert all(p.startswith("evals/quiz/") for p in outside) and len(outside) == 9, outside
assert all(p.startswith("skills/chantier/cards-next/topics/") for p in new_files), new_files
index.unlink()

passed = re.findall(r"^(\d+ passed, \d+ skipped in [\d.]+s)",
                    (HERE / "just-check.log").read_text(encoding="utf-8"), re.M)
assert len(passed) == 1, passed

data = FILE.read_bytes()
assert not data.startswith(b"\xef\xbb\xbf") and b"\r\n" not in data
text = data.decode("utf-8")
text = once(r"uncommitted changes of rounds 7 to 13 unless", "uncommitted changes of rounds 7 to 14 unless", text)
text = once(r"`just check` on round 13's working tree \([^)]*\): `[^`]*`\.",
            "`just check` on round 14's working tree (tests beside the other checks, so not a timing comparison): "
            f"`{passed[0]}`.", text)
text = once(r"(?s)(?<=`--stat=200` keeps the paths whole\.\n\n```text\n).*?(?=\n```\n)", stat, text)
for bad in ("gaeta", "C:/Users", "C:\\Users"):
    assert bad not in text, bad
FILE.write_bytes(text.encode("utf-8"))
print(passed[0], "|", stat.rsplit("\n", 1)[1], "|", len(outside), "outside;", len(new_files), "new files")
