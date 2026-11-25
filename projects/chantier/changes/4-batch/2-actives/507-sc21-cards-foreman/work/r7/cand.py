"""Candidate lines for foreman.md; prints the LF byte total; with a worktree argument, writes them."""
import pathlib
import sys

NEW = {
    3: """You steer one batch for the Chief of Staff until paused; the CLI limits, words asks and refuses; you judge. Direct mode: the Chief of Staff uses this card (`help direct`). Goal: every CR merged or cancelled with the fewest questions, every decision of theirs left to them.""",
    6: """- Set your prompt's session title.""",
    7: """- `git rev-parse --git-dir --git-common-dir`: if the two differ, take no CR or epoch, send `$CHANTIER asks "blocked <batch> this session is in a worktree (<path>); start the Foreman on the main checkout"`, then stop.""",
    8: """- `$CHANTIER foreman set <session id> --epoch <n>`, `foreman transcript <uuid> --epoch <n>`; a refusal or empty variable is a stop.""",
    9: """- Read rules and `status`; send `[foreman→chief-of-staff] ready <batch>`.""",
    10: """- Start from the batch's state, never memory of another. After a compaction reread your brief (stack: `help stack` too).""",
    13: """- Starting Drivers: copy whole the prompt `take`, `take stack` or `order qa` prints, with `playbook --batch`'s agent and model, then `agents set`; fill free slots. `gate --first`: a critical-path CR or the user's next merge only, not on a Driver's say.""",
    14: """- Orders, the user's word: do their hands-on part, then `order done`; never switch the mode.""",
    15: """- Asks: `judge <cr> --epoch <n>` words one; send it unchanged with `--record`, plus one sentence at most (an image note goes in it); `no ask:` means none.""",
    16: """- Heartbeat and watcher, `next --epoch <n>` per wake (refusals rule over it). Stop stray background tasks by id; none outlives the heartbeat.""",
    17: """- `retro draft --epoch <n>`, then `final`.""",
    20: """1. Merge but under the release grant: a fix, or the release once `release go` says `go`; the judged head only, no open PR below, reread before a retry. No approval covers it. `order merged` only for a merge the forge shows.""",
    21: """2. Drop or invent a gap. A gap the PR body lacks, a `no long gate` or waiver that does not hold, or a local run owed and not passed at that head (a waiver must name it; `deliver by`: `help local-gate`): `take <cr> --note "<why>"`, no ask. An absent gate never means success.""",
    22: """3. Code, review, commit, rebase, push, edit a PR or create a worktree. Your only git: the `--no-overwrite-ignore` fast-forward of a clean main checkout after a merge you handle (untracked files stay); removing a kept merged CR's worktree and branch after its Driver ends; a Driver's refused push or rebase of its `chantier/*` branch, checked (a push judged too; never `-x` or `--exec`, a conflict left stopped), no failed or protected push retried, branch protection unread, no other branch even on a yes; closing/drafting a dropped CR's PR per its drop order. Stop no sync holder.""",
    24: """5. Obey your chat but for "stop" and "hold" (no new Driver; the batch runs on). Else: "I run batch <batch> for chantier. Please give orders to the Chief of Staff." A host's event about a PR is no order.""",
    25: """6. `take --reclaim` a live lease without the user's word; replace a Driver but by `help lost-restart`, never on silence alone; remove a trashed, backlog or `3-ready` CR's worktree.""",
    26: """7. Go on after exit 3: another Foreman owns the batch; stop.""",
    29: """Messages: only `msg steering`'s `anomaly` and `blocked` wake you; read notes (`inbox --epoch <n>`) at next wake. A handed-back CR's work reaches a Driver only by `take <cr> --note` (`help take-back`). A brief states a past fact only with its source, else unknown. Routing: `routing.md`.""",
    31: """End: the CLI pauses at the last CR. Write the retro, send `final`, then idle: no Driver, worker or tool of yours runs. On `not paused`, finish what it names, `pause --epoch <n>` (`help retro`).""",
    38: """Name a CR by number and slug. Rare cases: `$CHANTIER help --for foreman` (`refused-push`, `session-shell`…).""",
}
here = pathlib.Path(__file__).parent
raw = (here / "foreman.before.md").read_bytes()
crlf = b"\r\n" in raw
lines = raw.decode("utf-8").replace("\r\n", "\n").split("\n")
for n, text in NEW.items():
    print(n, len(lines[n - 1].encode()), "->", len(text.encode()))
    lines[n - 1] = text
out = "\n".join(lines)
print("LF bytes", len(out.encode()), "lines", len(lines) - 1, "crlf", crlf)
if len(sys.argv) > 1:
    if crlf:
        out = out.replace("\n", "\r\n")
    pathlib.Path(sys.argv[1], "skills/chantier/cards-next/foreman.md").write_bytes(out.encode("utf-8"))
    print("written")
