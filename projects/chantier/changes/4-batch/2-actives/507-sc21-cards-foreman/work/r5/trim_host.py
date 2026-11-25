"""Cut dated trial text and stories from cards-next/hosts/claude-code.md's Allow rules section.

Prints each cut mark so it can be listed for child 24 (all are in docs/proofs/claude-code.md).
"""

P = "C:/Users/gaeta/Projets/chantier.worktrees/batch-31-CR-507/skills/chantier/cards-next/hosts/claude-code.md"

COL = [
    ("(`driver.md`: `git push -u <remote> <branch>`, branches", "(`git push -u <remote> <branch>`, branches"),
    ("one command per branch (`driver.md`, Push)", "one command per branch"),
    ("(`driver.md`, Push); the rule's `*`", "(floor rule 2); the rule's `*`"),
    (", the form refused 4 times as \"Git Destructive\"", ""),
    ("(`foreman-refused.md`, \"A Driver's refused force push\")", "(`help refused-push-judgement`)"),
    (" (`driver.md`, \"Means: rebase and push\")", ""),
    (" (the command refused in markdown-okf-schema-studio batch-09, 2026-11-23)", ""),
    (" (`driver.md`)", ""),
    (" (`chief-of-staff.md`, the surface's checkout)", " (the surface's checkout)"),
    (" (`merge`, `ship`, `spawn`\u2026 were refused 5 times)", ""),
    (" (refused once as \"Git Destructive\")", ""),
    ("; refused in batch-15", ""),
    ("(`driver.md`: `glab mr create --draft`)", "(`glab mr create --draft`)"),
    (" (refused twice)", ""),
]

t = open(P, encoding="utf-8", newline="").read()
assert "\r" not in t
lines = t.split("\n")
i = lines.index("| Rule | chantier's use | Risk accepted | Mark |") + 2
while lines[i].startswith("| "):
    cells = lines[i][2:-2].split(" | ")
    assert len(cells) == 4, (i, len(cells))
    rule, use, risk, mark = cells
    for a, b in COL:
        if a in use or a in risk:
            print("cut use/risk", rule[:50], "||", a)
        use = use.replace(a, b)
        risk = risk.replace(a, b)
    if "refused with the rule set" in mark:
        new = "refused"
    elif "proved (main session" in mark:
        new = "proved (main session); unproved (auto mode, a Driver)"
    elif rule.startswith("`Bash(uv sync --locked --check"):
        new = "documented; unproved (rule matching, auto mode, a Driver)"
    elif "subagent's matching command" in mark:
        new = "documented; unproved (a subagent); refused with no rule set"
    elif mark.startswith("**unproved**"):
        new = "unproved"
    else:
        assert mark == "documented (rule form)", mark
        new = "documented"
    if mark != "documented (rule form)":
        print("mark", rule[:50], "||", mark)
    lines[i] = "| " + " | ".join([rule, use, risk, new]) + " |"
    i += 1

t = "\n".join(lines)
before, after = t.split("### Capabilities and their commands\n")
body = after.split("\n")
marks = {
    "| Every batch ": "documented; unproved (the `chantier` and `SendMessage` rules); refused (a Driver's `git -C` force push and rebase): the ladder is `help refused-push` and `help refused-rebase`",
    "| A stack ": "unproved (the rule form of an extension command)",
    "| A release on its own ": "documented; unproved (a merge in a native stack, by an agent). ",
    "| Fixes on a grant ": "documented; unproved (a merge in a native stack, by an agent). ",
}
for n, ln in enumerate(body):
    for key, new in marks.items():
        if ln.startswith(key):
            head, mark = ln[:-2].rsplit(" | ", 1)
            print("mark", key.strip("| "), "||", mark)
            if new.endswith(". "):
                new += mark[mark.index("Risk:"):]
            body[n] = head + " | " + new + " |"
t = before + "### Capabilities and their commands\n" + "\n".join(body)
open(P, "w", encoding="utf-8", newline="").write(t)
