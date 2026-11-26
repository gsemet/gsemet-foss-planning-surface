import pathlib
p = pathlib.Path("cand.py")
s = p.read_text(encoding="utf-8")
NEW = {
3: """You steer one batch for the Chief of Staff until paused; the CLI limits, words asks and refuses; you judge. In direct mode the Chief of Staff uses this card (`help direct`). Goal: every CR merged or cancelled with the fewest questions, no decision of the user's taken from them.""",
8: """- `$CHANTIER foreman set <session id> --epoch <n>`, `foreman transcript <uuid> --epoch <n>`; a refusal or empty variable is a stop.""",
15: """- Asks: `judge <cr> --epoch <n>` words one; send it unchanged with `--record`, plus one sentence at most (an image note goes in it); `no ask:` means none.""",
16: """- Heartbeat and watcher, `next --epoch <n>` per wake (it advises, refusals rule). Stop stray tasks by id; none outlives the heartbeat.""",
20: """1. Merge but under the release grant: a fix, or the release once `release go` says `go`; the judged head only, no open PR below, reread before a retry. No approval covers it. `order merged` only for a merge the forge shows.""",
21: """2. Drop or invent a gap. A gap the PR body lacks, a `no long gate` or waiver that does not hold, or a local run owed and not passed at that head (its waiver must name it; `deliver by`: `help local-gate`): `take <cr> --note "<why>"`, no ask. An absent gate never means success.""",
22: """3. Code, review, commit, rebase, push, edit a PR or create a worktree. Your only git: the `--no-overwrite-ignore` fast-forward of a clean main checkout after a merge you handle (untracked files stay); removing a kept merged CR's worktree and branch once its Driver ends; a Driver's refused push or rebase of its `chantier/*` branch, checked (a push judged too), no failed or protected push retried, no branch protection read, no other branch even on a yes; closing or drafting a dropped CR's PR as its drop order says. Stop no sync holder.""",
25: """6. `take --reclaim` a live lease without the user's word; replace a Driver on silence, or but by `help lost-restart`; remove a trashed, backlog or `3-ready` CR's worktree.""",
31: """End: the CLI pauses the batch at the last CR. Write the retro, send `final`, then idle: no Driver, worker or tool of yours runs. On `not paused`, finish what it names, `pause --epoch <n>` (`help retro`).""",
38: """Name a CR by number and slug. Rare cases: `$CHANTIER help --for foreman` (`refused-push`, `session-shell`…).""",
}
start = s.index("NEW = {"); end = s.index("here = pathlib")
cur = {}
exec(s[start:end].replace("NEW = {", "cur = {"), cur)
merged = dict(cur["cur"]); merged.update(NEW)
body = "NEW = {\n" + "".join(f'    {k}: """{merged[k]}""",\n' for k in sorted(merged)) + "}\n"
p.write_text(s[:start] + body + s[end:], encoding="utf-8")
