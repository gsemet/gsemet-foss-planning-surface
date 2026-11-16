# CR-171 verification

Head: 1579dac (worktree C:\Users\gaeta\Projets\chantier.worktrees\batch-09-CR-171)

## Claims

1. `just check` (44 structure tests, release-notes check): PASS at 1579dac, run in the worktree.
2. `just scenario`: not rerun; CI ran it green on all jobs at this head (relied on).
3. Own scratch run of the WORKTREE CLI (script: scratchpad/verify_cr171.py, output: evidence/scratch-run.txt), all PASS at 1579dac:
   - `handback ready` with nothing: exit 2, names both the long gate and the verdict.
   - `--no-gate ""`: exit 1. `--no-gate "<rule>"` without verdict: exit 2, names the verdict only.
   - Two-command gate whose second fails: exit 4, one pass line, one FAIL line, third not run, `gate` events carry a shared `run` id; handback still refused on gate.
   - `verdict 101 VERIFIED`, `verdict cr-101 "NOT VERIFIED"` and `NOT VERIFIED` as two words: all accepted; last verdict decides (NOT VERIFIED after VERIFIED refuses, a later VERIFIED lets through).
   - Bare `101`, `cr-101` and `CR-101` resolve (verdict, handback); unknown bare 165 reports "no batch holds CR-165".
   - After a new shipped commit, the old gate and verdict do not count.
   - `--no-gate "<rule>"` with a verdict: accepted, rule on the printed line and the `handback` event (`no_gate`), STATUS.md has a Verdict step.
   - `take` and `handoff` print the two-gate checklist ("not shipped yet", then marks following events, `NOT VERIFIED` shown when last).
   - `order add --note <folder>` on a running direct batch: `added CR-102, queued`; `order qa` still refused (exit 2).
   - `playbook` prints `spec-writer prompt, first line: chantier spec-writer for the Chief of Staff, in the project <root>.`
4. Hook (`hooks/register.tsx`): UNVERIFIED by running (no claude CLI, no engine types: `types/index.d.ts` has no `agent.spawn`). Judged by reading:
   - Path logic, atom, Write/Edit/NotebookEdit scope, Bash untouched, deny-on-guard-error: as specified.
   - FAIL, decision 10 / part 1: Drivers are NOT left alone. `workerPlace` keys only on a first line starting `chantier ` plus `worktree:` and `folder: ... (work/, evidence/)` lines. A real Driver prompt is built from the lines `take` prints (concepts.md "Starting an agent"), and `take` prints exactly those two lines (evidence/scratch-run.txt lines 8-9). So a real Driver spawn is recorded as a worker and its Write/Edit outside worktree and CR folder are refused, against the spec and against the new section of `hosts/claude-code.md` ("leaves alone ... the Drivers"). The test "a Driver ... not guarded" passes only because its crafted Driver prompt has no `worktree:` line. The hook must key on the role in the first line (e.g. `chantier coder|inspector|verifier|...`, not `chantier driver`), and the test must use a Driver prompt with the real `worktree:` and `folder:` lines.
   - RISK, unprovable here: the record is made after `await next(e)`. If `next` resolves only when the subagent finishes, the record comes after its writes and the guard never applies. The spec asked to check this against the engine types, which are absent here.

## Verdict

NOT VERIFIED (claim 4: the hook also guards Drivers).
