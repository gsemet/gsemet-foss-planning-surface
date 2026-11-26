"""Third pass: the six requirements the edited body lines name, base vs head, and their test markers.

Usage: python -I mainreqs.py <worktree> <old base> <base> <head>
"""
import re
import subprocess
import sys

W, OLD, BASE, HEAD = sys.argv[1:5]
IDS = ["DIAG-009", "DIAG-121", "DIAG-123", "DIAG-128", "LAYOUT-023", "CORE-096"]


def git(*args, ok=(0,)):
    done = subprocess.run(["git", "-C", W, *args], capture_output=True, encoding="utf-8")
    if done.returncode not in ok:
        raise SystemExit(done.stderr)
    return done.stdout


def split(text):
    _, front, body = text.split("---\n", 2)
    keys, name = {}, None
    for line in front.splitlines():
        found = re.match(r"([A-Za-z_]+):(.*)$", line)
        if found:
            name = found.group(1)
            keys[name] = [found.group(2)]
        else:
            keys[name].append(line)
    return keys, body


def strip_ids(body):
    return re.sub(r"(?m)^(### Scenario) S\d+", r"\1", body)


changed = [p for p in git("diff", "--name-only", OLD, BASE, "--", "requirements/tiers/swrs", "requirements/tiers/strs").split() if not p.endswith("index.md")]
print("requirement files main changed since the old base:", len(changed))
for path in changed:
    was = git("show", f"{OLD}:{path}", ok=(0, 128))
    now = git("show", f"{BASE}:{path}")
    if not was:
        print("  added", path.rsplit("/", 1)[1])
        continue
    a, b = split(was), split(now)
    keys = sorted(k for k in set(a[0]) | set(b[0]) if a[0].get(k) != b[0].get(k))
    print("  ", path.rsplit("/", 1)[1], "front matter changed", keys, "body changed", a[1] != b[1])

files = git("ls-tree", "-r", "--name-only", HEAD, "requirements/tiers/swrs").split()
for short in IDS:
    path = next(p for p in files if p.endswith(f"SwRS-MDOKFSTUDIO-{short}.md"))
    a = split(git("show", f"{BASE}:{path}"))
    b = split(git("show", f"{HEAD}:{path}"))
    keys = sorted(k for k in set(a[0]) | set(b[0]) if a[0].get(k) != b[0].get(k))
    left, right = strip_ids(a[1]), strip_ids(b[1])
    blocks = lambda t: sorted(x.strip() for x in re.split(r"(?m)^(?=##)", t))
    same_blocks = blocks(left) == blocks(right)
    same_lines = sorted(l for l in left.splitlines() if l) == sorted(l for l in right.splitlines() if l)
    headings = re.findall(r"(?m)^### Scenario.*$", b[1])
    numbered = [h for h in headings if re.match(r"### Scenario S\d+ ", h)]
    print(short, "front", keys, "| body identical apart from ids", left == right, "| same non-empty lines", same_lines, "| same heading blocks", same_blocks,
          "| scenario headings", len(headings), "numbered", len(numbered), "| declared", "scenarios" in b[0])

pattern = r"@(tests|accepts|implements)_req SwRS-MDOKFSTUDIO-(" + "|".join(IDS) + ")"
lines = git("grep", "-n", "-E", pattern, HEAD, "--", "test", "tests").splitlines()
bare = [l for l in lines if re.search(r"@(tests|accepts)_req", l) and not re.search(r"-\d{3}#S\d+", l)]
print("test marker lines of the six at head:", len(lines), "without #S:", len(bare))
for short in IDS:
    print("  ", short, sum(1 for l in lines if short in l))
for line in bare:
    print("  BARE", line)
