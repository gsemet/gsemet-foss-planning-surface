"""Description-only pass: figures of the posted PR body against the tree. argv: WT mode."""

import json
import subprocess
import sys

WT = sys.argv[1]
MODE = sys.argv[2]
BASE = "266b784"
HEAD = "5d2626d"
REFS = "skills/chantier/references"


def git(*args):
    return subprocess.run(
        ["git", "-C", WT, *args], capture_output=True, check=True
    ).stdout


def sizes(rev):
    out = {}
    for line in git("ls-tree", "-r", "-l", rev, "--", REFS).decode("utf-8").splitlines():
        meta, path = line.split("\t", 1)
        out[path[len(REFS) + 1 :]] = int(meta.split()[3])
    return out


def cards():
    old, new = sizes(BASE), sizes(HEAD)
    targets = {
        "chief-of-staff.md": 6000, "griller-skill.md": 4000, "foreman.md": 4000,
        "cr-driver.md": 4096, "stack-driver.md": 4096, "release-driver.md": 3072,
        "qa-driver.md": 2048, "coder.md": 1500, "conflict-resolver.md": 1500,
        "debugger.md": 1500, "investigator.md": 1500, "demo-explorer.md": 1500,
        "spec-writer.md": 1500, "spec-critic.md": 1500, "retro-critic.md": 1500,
        "inspector.md": 2000, "verifier.md": 3000, "griller.md": 2000, "floor.md": 1200,
    }
    for name, target in targets.items():
        o, n = old[name], new[name]
        state = "over" if n > target else "within"
        moved = "changed" if o != n else "unchanged"
        print(f"{name} base {o} head {n} target {target} {state} {moved}")
    print("top-level cards with no target here:",
          sorted(k for k in new if "/" not in k and k.endswith(".md") and k not in targets))


def topics():
    old, new = sizes(BASE), sizes(HEAD)
    changed = [k for k in new if k.startswith("topics/") and old.get(k) != new[k]]
    for k in sorted(changed):
        print(f"{k} base {old.get(k)} head {new[k]} over1500 {new[k] > 1500} over1536 {new[k] > 1536}")
    print("changed topics", len(changed))


def body():
    posted = json.loads(
        subprocess.run(
            ["gh", "pr", "view", "489", "--repo", "gsemet/chantier", "--json", "body"],
            capture_output=True, check=True,
        ).stdout.decode("utf-8")
    )["body"].replace("\r\n", "\n").rstrip("\n")
    local = open(sys.argv[3], encoding="utf-8").read().replace("\r\n", "\n").rstrip("\n")
    print("posted == pr-body.md:", posted == local, len(posted), len(local))
    rows = [l.split("|")[1].strip() for l in posted.split("\n")
            if l.startswith("| ") and ".md |" in l]
    cards_ = [l.split("|")[2].strip() for l in posted.split("\n")
              if l.startswith("| ") and ".md |" in l]
    print("table rows", len(rows))
    inv = git("show", f"{HEAD}:docs/proofs/cards-inventory.md").decode("utf-8").split("\n")
    opened = git("show", f"{HEAD}:docs/proofs/cards-inventory-open.tsv").decode("utf-8")
    open_ids = {l.split("\t")[0] for l in opened.split("\n") if l}
    for rid, card in zip(rows, cards_):
        lines = [l for l in inv if l.startswith(f"| {rid} |")]
        home = lines[0].rstrip(" |").rsplit(" | ", 2)[-2] if lines else "NO ROW"
        ok = home.startswith(f"card {card}:")
        span = home.split('"')[1] if '"' in home else ""
        text = " ".join(git("show", f"{HEAD}:{REFS}/{card}").decode("utf-8").split())
        before = " ".join(git("show", f"{BASE}:{REFS}/{card}").decode("utf-8").split())
        want = " ".join(span.split())
        print(f"{rid} {card} home-names-card {ok} open {rid in open_ids} "
              f"span head {want in text} base {want in before}")
        if not ok:
            print("   home:", home)


{"cards": cards, "topics": topics, "body": body}[MODE]()
