import hashlib, os, subprocess, sys, shutil
from pathlib import Path

WT = Path(r"C:\Users\gaeta\Projets\chantier.worktrees\batch-18-CR-255")
SKILL = WT / "skills" / "chantier"
root = Path(sys.argv[1])
if root.exists():
    shutil.rmtree(root, ignore_errors=True)
root.mkdir(parents=True)
work = root / "proj"
origin = root / "origin.git"
env = {**os.environ, "PYTHONPATH": str(SKILL / "scripts" / "cli" / "src"), "CHANTIER_SKILL_DIR": str(SKILL),
       "CLAUDE_CODE_ENTRYPOINT": "claude-desktop", "CHANTIER_HOST": "claude", "CLAUDE_CODE_SESSION_ID": "uuid-chief",
       "CHANTIER_CLAUDE_PROJECTS": str(root / "cp")}
for v in ("CHANTIER_ROOT", "CHANTIER_BATCH", "CHANTIER_PLUGIN_ROOT", "COPILOT_AGENT_SESSION_ID"):
    env.pop(v, None)

def sh(*a, cwd=None):
    return subprocess.run(a, cwd=cwd or work, check=True, capture_output=True, text=True).stdout.strip()

sh("git", "init", "--quiet", "--bare", "-b", "main", str(origin), cwd=root)
sh("git", "init", "--quiet", "-b", "main", str(work), cwd=root)
sh("git", "config", "user.name", "v"); sh("git", "config", "user.email", "v@example.com")
(work / "AGENTS.md").write_text("# P\n\nDefault branch: `main`. Remote: `origin`.\n")
(work / "app.py").write_text("x=1\n")
sh("git", "add", "."); sh("git", "commit", "--quiet", "-m", "init")
sh("git", "remote", "add", "origin", str(origin)); sh("git", "push", "--quiet", "-u", "origin", "main")

def c(*args):
    p = subprocess.run([sys.executable, "-m", "chantier", *map(str, args)], cwd=work, env=env,
                       capture_output=True, text=True, encoding="utf-8")
    print(f"$ chantier {' '.join(map(str, args))}\n  exit {p.returncode}")
    for l in p.stdout.strip().splitlines(): print("  out: " + l)
    for l in p.stderr.strip().splitlines(): print("  err: " + l)
    return p.returncode, p.stdout.strip().splitlines(), p.stderr.strip()

def prep(title):
    _, out, _ = c("file", title)
    inbox = work / out[0].removeprefix("filed ").split(";", 1)[0]
    (inbox / "01-intent.md").write_text(f"# {title}\n")
    (inbox / "02-answers.md").write_text("# D\n")
    (inbox / "03-change-spec.md").write_text(f"# {title}\n")
    _, out, _ = c("triage", inbox, "--priority", "P1")
    return work / out[0].removeprefix("triaged ").rsplit(" (", 1)[0]

items = [prep("Fix login"), prep("Add export")]
code, out, _ = c("open", *items, "--slots", 2, "--default-branch", "main")
state = work / ".agents" / "changes" / "4-batch"
c("foreman", "set", "local_f1", "--epoch", 1)
c("foreman", "transcript", "uuid-f", "--epoch", 1)
c("take", "CR-101", "--epoch", 1)

def snap():
    return {f: hashlib.sha256((state / f).read_bytes()).hexdigest() for f in ("batch.json", "events.jsonl") if (state / f).exists()}

def refused(label, *args):
    print(f"\n=== {label}")
    before = snap()
    code, _, err = c(*args)
    after = snap()
    noword = "epoch" not in err.replace("--epoch", "")
    print(f"  RESULT exit={code} (want 2) no-epoch-word-outside-flag={noword} files-identical={before == after}")
    print(f"  before={before}\n  after ={after}")

print("\n##### CLAIM 1: take CR-102 without --epoch")
refused("take CR-102", "take", "CR-102")
print("\n##### CLAIM 2")
refused("pause", "pause")
refused("agents set CR-101 -", "agents", "set", "CR-101", "-")
refused("agents set CR-101 id", "agents", "set", "CR-101", "agent1")
refused("agents set stack", "agents", "set", "stack", "agent1")
refused("order done O-1", "order", "done", "O-1")
refused("foreman transcript", "foreman", "transcript", "uuid-x")
refused("foreman set", "foreman", "set", "local_f9")
refused("status --stop-heartbeat", "status", "--stop-heartbeat")
refused("take stack", "take", "stack")
print("\n##### exceptions")
code, _, _ = c("status", "--refresh"); print("  status --refresh exit", code)
code, _, _ = c("status"); print("  status exit", code)
print("\n##### order merged without --epoch (any refusal must not be about --epoch)")
c("order", "merged", "CR-102")
print("\n##### CLAIM 3: stale")
c("foreman", "set", "local_f2", "--epoch", 2)
c("status", "--refresh", "--epoch", 1)
c("take", "CR-102", "--epoch", 1)
c("foreman", "set", "local_f1b", "--epoch", 1)
