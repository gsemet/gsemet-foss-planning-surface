"""Move each command's argparse declaration from the old cli._parser into its module's register(sub)."""
import ast
import subprocess
from collections import defaultdict
from pathlib import Path

REPO = Path(r"C:\Users\gaeta\Projets\chantier.worktrees\batch-17-CR-221")
PKG = REPO / "skills/chantier/scripts/cli/src/chantier"
MODS = {
    "preflight": "commands/preflight", "init": "commands/intake", "file": "commands/intake",
    "triage": "commands/intake", "abandon": "commands/intake", "restore": "commands/intake",
    "open": "commands/opening", "order": "commands/orders", "foreman": "commands/seat",
    "seat": "commands/seat", "board": "board/server", "status": "commands/batch_status",
    "asks": "commands/batch_status", "agents": "commands/batch_status", "take": "commands/driver",
    "round": "commands/driver", "handback": "commands/driver", "note": "commands/driver",
    "log": "commands/driver", "rules": "commands/rules", "playbook": "commands/rules",
    "handoff": "commands/facts", "gate": "commands/gate", "verdict": "commands/delivery",
    "ship": "commands/delivery", "stack": "commands/delivery", "forge-stack": "commands/forge_stack",
    "release": "commands/release", "cancel": "commands/release", "pause": "commands/closing",
    "close": "commands/closing", "cost": "commands/cost/command",
}
text = subprocess.run(["git", "show", "HEAD:skills/chantier/scripts/cli/src/chantier/cli.py"],
                      cwd=REPO, capture_output=True, check=True).stdout.decode("utf-8")
tree = ast.parse(text)
parser = next(n for n in tree.body if isinstance(n, ast.FunctionDef) and n.name == "_parser")
groups = []  # (name, [stmt source...])
for st in parser.body:
    call = st.value if isinstance(st, (ast.Assign, ast.Expr)) else None
    if isinstance(call, ast.Call) and getattr(call.func, "id", "") == "cmd":
        args = call.args
        name = ast.literal_eval(args[0])
        fn = ast.get_source_segment(text, args[1]).replace("commands.", "")
        if fn.startswith("board."):
            fn = "board"
        if fn.startswith("forge_stack."):
            fn = "forge_stack"
        help_src = ast.get_source_segment(text, args[2])
        batch = True
        if len(args) > 3:
            batch = ast.literal_eval(args[3])
        epoch = any(k.arg == "epoch" and ast.literal_eval(k.value) for k in call.keywords)
        scope = "BATCH_EPOCH" if epoch else ("BATCH" if batch else "NO_BATCH")
        target = "s = " if isinstance(st, ast.Assign) else ""
        groups.append((name, [f"    {target}add_command(sub, {ast.get_source_segment(text, args[0])}, {fn}, {help_src}, {scope})"]))
    elif groups and isinstance(st, (ast.Assign, ast.Expr)):
        src = ast.get_source_segment(text, st)
        groups[-1][1].append("    " + src)
bymod = defaultdict(list)
for name, stmts in groups:
    bymod[MODS[name]].append("\n".join(stmts))
for mod, blocks in bymod.items():
    path = PKG / (mod + ".py")
    t = path.read_text(encoding="utf-8")
    body = "\n\n".join(blocks)
    t = t.rstrip("\n") + "\n\n\ndef register(sub: Subparsers) -> None:\n    \"\"\"Declare this module's commands.\"\"\"\n" + body + "\n"
    imp = ""
    regs = "from chantier.commands.registry import " + ", ".join(
        sorted({"add_command", "Subparsers"} | {w for w in ("BATCH", "BATCH_EPOCH", "NO_BATCH") if w in body})) + "\n"
    i = t.index("\nfrom __future__ import annotations\n") + len("\nfrom __future__ import annotations\n")
    t = t[:i] + "\n" + imp + regs + t[i:]
    path.write_text(t, encoding="utf-8", newline="\n")
print(sorted(bymod))
