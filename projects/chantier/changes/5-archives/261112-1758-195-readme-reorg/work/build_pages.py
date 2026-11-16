import pathlib, sys
root = pathlib.Path(sys.argv[1])
L = (root / "README.md").read_text(encoding="utf-8").split("\n")
def seg(a, b):  # 1-based inclusive
    return L[a-1:b]
def strip_trail(x):
    while x and x[-1] == "": x.pop()
    return x
def lower(lines):
    out = []; fence = False
    for l in lines:
        if l.startswith("```"): fence = not fence
        if not fence and l.startswith("### "): l = l[1:]
        out.append(l)
    return out
pages = {}
pages["boards.md"] = ["# Boards", "", "The CR board in Claude Code and the remote board, two read-only views of the planning folder.", ""] + lower(strip_trail(seg(231, 265)))
pages["gates.md"] = ["# Your gates", "", "The fast gate and the long gate that guard every change, and how to declare them.", ""] + strip_trail(seg(269, 295))
pages["agents-and-models.md"] = ["# Your own agents and models", "", "How to run your own agents in a role, which model each role runs, and the no-fallback rule.", ""] + lower(strip_trail(seg(297, 357)))
pages["planning-folder.md"] = ["# The planning folder", "", "The layout of the planning folder, in your project or in an external surface (see [planning modes](planning-modes.md) for the full account of a surface), what is published, the STATUS files, the worktrees, and a batch's pause and close.", ""] + strip_trail(seg(361, 427))
pages["hosts.md"] = ["# Supported hosts", "", "The hosts Foreman and direct mode run on, the forges, and Windows.", ""] + strip_trail(seg(431, 464))
pages["costs.md"] = ["# Costs and budgets", "", "How chantier measures what a batch costs, and the budget.", ""] + strip_trail(seg(468, 491))
rw = [("[the remote board](#the-remote-board)", "[the remote board](boards.md#the-remote-board)"),
      ("[modes](#batch-modes)", "[modes](../README.md#batch-modes)")]
for n, ls in pages.items():
    t = "\n".join(ls) + "\n"
    for a, b in rw: t = t.replace(a, b)
    (root / "docs" / n).write_bytes(t.encode("utf-8"))
print("ok")
