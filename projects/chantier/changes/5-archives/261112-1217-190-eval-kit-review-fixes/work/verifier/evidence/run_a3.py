import json, subprocess, sys, pathlib
KIT = pathlib.Path(r"C:\Users\gaeta\Projets\chantier.worktrees\batch-13-CR-190\evals\kit")
scratch = pathlib.Path(sys.argv[1])
sys.path.insert(0, str(KIT))
import sandbox, setup

PFX = "[eval 9 2026-11-14 full]"
SHA = "1234567890abcdef1234567890abcdef12345678"
ok = [{"name": "gate", "conclusion": "SUCCESS"}]
def view(state="OPEN", title=PFX + " feat", roll=ok, n=3):
    return {"number": n, "state": state, "title": title, "headRefOid": SHA, "statusCheckRollup": roll}

cases = {
    "MERGED": view("MERGED"), "CLOSED": view("CLOSED"), "no prefix": view(title="feat: x"),
    "failed check": view(roll=[{"name": "gate", "conclusion": "FAILURE"}]),
    "pending check": view(roll=[{"name": "gate", "state": "PENDING"}, {"context": "ci", "conclusion": "SUCCESS"}]),
    "no check": view(roll=[]), "open+prefixed+green": view(),
}
print("== merge_refusal")
for k, v in cases.items():
    print(f"{k:22} -> {sandbox.merge_refusal(v, PFX)!r}")
print("checks_green: skipped/neutral ->", sandbox.checks_green([{"conclusion": "SKIPPED"}]),
      sandbox.checks_green([{"conclusion": "NEUTRAL"}]), "; all success ->", sandbox.checks_green(ok))

print("\n== cmd_merge end to end, sandbox.gh replaced by a recorder")
ws = scratch / "ws"; ws.mkdir(exist_ok=True)
(scratch / "ws.run.json").write_text(json.dumps({"prefix": PFX, "repository": sandbox.REPO}), encoding="utf-8")
calls = []
def fake_gh(*args, code=4):
    calls.append(args)
    if args[:2] == ("pr", "view"):
        return json.dumps(CURRENT)
    return ""
sandbox.gh = fake_gh
class A:  # the parsed arguments
    pr = "3"; workspace = str(ws)
for k, v in cases.items():
    CURRENT = v; calls.clear()
    code = sandbox.cmd_merge(A)
    merges = [c for c in calls if c[:2] == ("pr", "merge")]
    print(f"{k:22} exit {code}; pr merge calls: {merges}")

print("\n== command line (no gh reached)")
def cli(*a):
    r = subprocess.run([sys.executable, str(KIT / "sandbox.py"), "merge", *a], capture_output=True, text=True, cwd=str(scratch))
    print(f"merge {' '.join(a)} -> exit {r.returncode}; stderr: {r.stderr.strip().splitlines()[-1:]}")
cli("abc")
cli("https://github.com/other/repo/pull/3")
empty = scratch / "norecord"; empty.mkdir(exist_ok=True)
cli("3", "--workspace", str(empty))
(scratch / "bad.run.json").write_text("{not json", encoding="utf-8")
bad = scratch / "bad"; bad.mkdir(exist_ok=True)
cli("3", "--workspace", str(bad))
(scratch / "other.run.json").write_text(json.dumps({"prefix": PFX, "repository": "x/y"}), encoding="utf-8")
other = scratch / "other"; other.mkdir(exist_ok=True)
cli("3", "--workspace", str(other))

print("\n== merge_command / allow_rules")
print("merge_command:", setup.merge_command())
for c in ("full", "real-foreman", "real-direct", "copilot"):
    spec = setup.CAMPAIGNS[c]
    print(f"\n{c} (host {spec['host']}):")
    for r in setup.allow_rules(spec):
        print("  ", r)
