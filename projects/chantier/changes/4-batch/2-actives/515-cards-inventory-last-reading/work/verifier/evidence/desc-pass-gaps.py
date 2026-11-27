"""Check the Known gaps bullets and the second judging of a posted description (read only).

Usage: gaps_check.py <worktree> <body.md> <body.html> <CR work folder>
"""

import re
import subprocess
import sys
from pathlib import Path

WT, BODY, HTML, WORK = sys.argv[1], Path(sys.argv[2]), Path(sys.argv[3]), Path(sys.argv[4])
body = BODY.read_text(encoding="utf-8").replace("\r\n", "\n")
rendered = HTML.read_text(encoding="utf-8")


def git(*args):
    return subprocess.run(["git", "-C", WT, *args], capture_output=True).stdout.decode("utf-8")


rules = git("show", "HEAD:docs/protective-rules.md").split("\n")
for ident in ("P15/C8", "N1", "N7", "C4", "B18", "P11", "P2-code", "N5", "B6"):
    for line in rules:
        if line.startswith(f"| {ident} |"):
            print(line[:700])

print("== P15/C8 code at head")
src = "skills/chantier/scripts/cli/src/chantier/commands/orders_waive.py"
print(git("grep", "-n", "-E", "follow.up|^def ", "HEAD", "--", src))

print("== B18 page")
print(git("grep", "-n", "-A1", "temporary folders named by a", "HEAD", "--", "skills/chantier/references/topics/host-refused.md"))

print("== protective ids: first judging against the posted lines")
first = (WORK / "investigator/investigation-rows.md").read_text(encoding="utf-8")
ids1 = set(re.findall(r"^- ([A-Z]+-[A-Z]?\d+) \[[a-f]\] PROTECTIVE", first, re.M))
sect = body.split("### The last reading of the open rows")[1].split("### Homes kept")[0]
ids2 = set(re.findall(r"^- ([A-Z]+-[A-Z]?\d+): ", sect, re.M))
print("first:", len(ids1), "posted:", len(ids2), "dropped since:", sorted(ids1 - ids2), "added:", len(ids2 - ids1), sorted(ids2 - ids1))

print("== rendering")
for tag in ("em", "strong", "del", "blockquote", "a"):
    print(f"<{tag}>:", len(re.findall(rf"<{tag}[ >]", rendered)))
outside = re.sub(r"`[^`\n]*`", "", body)
print("angle brackets outside code:", sorted(set(re.findall(r"<[^>\n]{0,40}>", outside))))
print("odd backtick lines:", [i + 1 for i, l in enumerate(body.split("\n")) if l.count("`") % 2])
home_path = re.escape(Path.home().name) + "|[A-Z]:[" + re.escape(chr(92)) + "/]Users|/home/"
print("user name or home path:", bool(re.search(home_path, body, re.I)))
