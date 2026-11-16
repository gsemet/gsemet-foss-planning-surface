"""Throwaway: run real-direct run 1's recorded transcripts through an audit.py's own patterns and logic.
Usage: uv run --no-project python run1_recheck.py <path to audit.py>
Never committed to the kit."""
import importlib.util
import re
import sys
from pathlib import Path

sys.path.insert(0, "C:/Users/gaeta/Projets/chantier.worktrees/batch-15-CR-209/evals/kit")  # judge.py, shared
spec = importlib.util.spec_from_file_location("audit_under_test", sys.argv[1])
audit = importlib.util.module_from_spec(spec)
sys.modules["audit_under_test"] = audit
spec.loader.exec_module(audit)

ROOT = Path("C:/Users/gaeta/.claude/projects/C--Users-gaeta-Projets-chantier-eval-real-direct-2026-11-12")
main = next(ROOT.glob("*.jsonl"))
steer = audit.Agent(main, {"agentType": "chief-of-staff"})
subs = {f.stem.removeprefix("agent-")[:10]: audit.Agent(f, {}) for f in main.with_suffix("").rglob("agent-*.jsonl")}

# the claim: the first `open` of the steering session (its rules were read before it)
opens = [(t, c) for (n, i), t in zip(steer.tools, steer.when) if n in ("Bash", "PowerShell")
         for c in [i.get("command", "")] if re.search(audit.CLI_CALL + r"open\b", c, re.I | re.M)]
steer.since = opens[0][0] if opens else ""
print(f"claim (first `open`): {steer.since}")
print(f"audit.py: {sys.argv[1]}\n")

# J3 worktrees: the three Verifiers, with the audit's own rule (the lawful_worktree helper when it exists)
lawful = getattr(audit, "lawful_worktree", None)
for sid in ("a575690943", "aa4b6f3168", "ac57a2037e"):
    a = subs[sid]
    a.role = "verifier"
    if lawful:
        trees = [c for c in a.bash() if any(not lawful(a.role, c, m)
                                            for m in audit.GIT_WORKTREE_ADD.finditer(c))]
    else:  # the old audit: any `git worktree add` is a breach
        trees = [c for c in a.bash() if audit.GIT_WORKTREE_ADD.search(c)]
    adds = [c[m.start():m.start() + 70].splitlines()[0] for c in a.bash() for m in audit.GIT_WORKTREE_ADD.finditer(c)]
    print(f"{'PASS' if not trees else 'FAIL'} [J3] {sid} (verifier) worktree add: {adds}")

# J3 write outside notes and proof: the Verifier ab3ea4ac68, with the audit's own OWN_FILES rule
a = subs["ab3ea4ac68"]
a.role = "verifier"
outside = [w for w in a.writes() if not any(o in w.replace("\\", "/") for o in audit.OWN_FILES)] \
    + a.shell_writes()
print(f"{'PASS' if not outside else 'FAIL'} [J3] ab3ea4ac68 (verifier) edits nothing but its notes "
      f"and proof: {outside[:2]}")

# C9: the steering session's commands from its claim, with the audit's own epoch pattern (direct mode)
cmds = steer.bash(steer.since)
no_epoch = [c for c in cmds if audit.DIRECT_EPOCH_COMMANDS.search(c) and "--epoch" not in c]
print(f"{'PASS' if not no_epoch else 'FAIL'} [C9] direct: every steering command of the list carries "
      f"its epoch ({len(no_epoch)} without)" + (f": {no_epoch[0][:80]}" if no_epoch else ""))
refresh_no_epoch = [c for c in cmds if re.search(audit.CLI_CALL + r"status --refresh\b", c, re.I | re.M)
                    and "--epoch" not in c]
print(f"   ({len(refresh_no_epoch)} `status --refresh` with no epoch in the steering session)")

# J14: rules read from the claim on (the audit's own RULES_COMMAND)
rules = [c for c in cmds if audit.RULES_COMMAND.search(c)]
print(f"{'PASS' if rules else 'FAIL'} [J14] the steering session read the project's rules "
      f"(`chantier rules`): {len(rules)} from the claim on")

