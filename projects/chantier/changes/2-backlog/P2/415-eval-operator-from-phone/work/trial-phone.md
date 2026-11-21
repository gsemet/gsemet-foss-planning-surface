# Trial of the eval operator from the phone (CR-415)

Status: **PENDING**, every step. The Driver wrote this file; the Chief of Staff fills it in, with
the user driving from the phone. It names the exact tools and the mode used. It is evidence of a
run on Claude Code.

**The canary rule.** The canary token is never written in this file, in the CR, in a prompt or in
the PR. Record only "matched" or "did not match".

## The trial workspace

Made by setup for a Foreman campaign, after `sandbox.py reset --yes` if the sandbox is not at its
base (no model, no push):

```text
uv run --no-project python evals/kit/setup.py real-foreman <eval root>/trial-phone-<date>
```

The Chief of Staff adds two local things, never pushed.

1. In the workspace's `AGENTS.md`, the line `Trial canary: <token>` (the token drawn at that
   moment, for example 8 random hex characters, written nowhere else), and below it:

   > This workspace is a trial. When chantier's chief-of-staff skill starts here, run `preflight`,
   > report its first lines and the planning folder you use, and stop: open no batch.

2. In the workspace's `.claude/settings.local.json` (written by setup), one allow rule for a
   harmless command that no other settings file of the user allows, for example
   `Bash(git rev-parse --is-bare-repository)`. First check that neither `~/.claude/settings.json`
   nor the steering folder's `.claude/settings*.json` allows it.

Record: workspace path: PENDING. Date: PENDING. Settings rule chosen: PENDING. Check that no other
settings file allows it: PENDING. Eval root holds no `AGENTS.md` and no `CLAUDE.md` (needed only
for route (c)): PENDING.

After the trial the workspace and its `<workspace>.run.json` are deleted. No run number is used.

## Record of each step

Each step records the exact tool call and its output (or a phone screenshot when the output is only
on the phone), then **proved** or **not proved**.

| Step | Result |
| --- | --- |
| 1. Phone drives the steering session under Remote Control; the notice is seen | PENDING |
| 2. Start of the operator with no `cwd` and the bootstrap prompt (route (a)); where it landed | PENDING |
| 3. Move into the workspace, then `clear_session` on `self`: granted, refused or denied | PENDING |
| 4. Check message sent (tool named); answer, files listed, Pass or Fail; settings command; permission mode | PENDING |
| 5. Setup's `prompt` line sent verbatim by message; mode used | PENDING |
| 6. The operator's next turn ran the chief-of-staff skill in the workspace | PENDING |
| 7. Probe session started by the operator with no `cwd`; granted or not; the probe's answer | PENDING |
| 8. The user finds the probe on the phone and types one line | PENDING |
| 9. Sessions archived, workspace deleted | PENDING |

### Step 1. Remote Control

Tool call and output: PENDING. Proved or not proved: PENDING.

### Step 2. Start of the operator

The steering session calls `start_session` with no `cwd`, no `preset`, `use_worktree: false`, the
user's permission mode, and the bootstrap prompt of the hosts card ("The eval operator from a
remote client"), `<workspace>` filled in.
Exact call and output: PENDING. Where the session landed: PENDING. Proved or not proved: PENDING.
Under route (b), this step is the user's start from the phone, in the card's two tries (first the
"Remote Control" entry, then the "Local" group's entry or a saved environment with Worktree off);
record the app, the screen, the choices and the `git rev-parse` output of each try.

### Step 3. Move and self-clear

`change_directory` call and output: PENDING. `clear_session` on `self`: granted, refused or denied
(exact text): PENDING. Proved or not proved: PENDING.

### Step 4. The check

Message tool used (exact): PENDING. The check message as sent, asking, in the next turn and with no
file read: `pwd`, `git rev-parse --git-dir`, `--git-common-dir`, `--show-toplevel`; the path of every
instruction and memory file the context shows; the canary line quoted if its project instructions
hold one, or "no canary"; whether its instructions hold the line "Run `just check` before you hand
back". Record:

- the operator's answer: PENDING
- files listed: PENDING
- canary: "matched" / "did not match" / "no canary": PENDING (never the token)
- chantier's marker: PENDING
- transcript shows no file read and no shell output that could have given the token in that turn: PENDING
- the settings command ran with no prompt: PENDING; the session's permission mode: PENDING. Under auto
  mode a run with no prompt is "not conclusive".
- Pass or Fail: PENDING. Proved or not proved: PENDING.

**Pass rule, (a) and (b):** all hold: `--git-dir` and `--git-common-dir` are the same folder and the
top level is the workspace; the token quoted matches; the marker is absent; no listed instruction or
memory file belongs to chantier's checkout or its auto-memory; no file read and no shell output that
could have given the token in that turn. **(c):** the same, except that "no canary" is expected.

On Fail, or if step 3 was refused, route (a) is not proved: go to (b), then to (c), each run from
step 2 with its own check, until one passes or all three are recorded not proved.

| Route | Date | Result |
| --- | --- | --- |
| (a) self-clear | PENDING | PENDING |
| (b) phone's New session, first try ("Remote Control" entry) | PENDING | PENDING |
| (b) phone's New session, second try ("Local" group or saved environment, Worktree off) | PENDING | PENDING |
| (c) neutral steering folder | PENDING | PENDING |

### Step 5. The `prompt` line

Sent by (tool, exact): PENDING. Mode blank filled with: PENDING. Proved or not proved: PENDING.

### Step 6. The skill ran in the workspace

- `preflight` lines name the workspace's `.agents/changes`: PENDING
- holds the workspace's seat, not a Griller's: PENDING
- stops as the trial line of the workspace's `AGENTS.md` asks: PENDING

A message that does not run the skill is not proved; the route then falls to (b), where the user
pastes the line into the session's own field. Proved or not proved: PENDING.

### Step 7. The probe session

The steering session asks the operator to start one probe session with no `cwd` and this prompt:

> Run `pwd`, `git rev-parse --git-dir`, `git rev-parse --git-common-dir` and
> `git rev-parse --show-toplevel`; list the instruction and memory files your context shows; quote
> the canary line of your project instructions, or say none; say whether they hold the line 'Run
> `just check` before you hand back'; read no file; then stop.

Start granted or not, exact call and output: PENDING. The probe's answer: PENDING. Proved or not
proved: PENDING.

### Step 8. Typing from the phone

The user finds the probe on the phone and types one line (for example `ping`). Found: PENDING.
Line taken: PENDING. The probe answered: PENDING. Proved or not proved: PENDING. This is the trial's
last step.

### Step 9. Cleanup

Operator and probe sessions archived (by whom): PENDING. Workspace and `<workspace>.run.json`
deleted: PENDING.

## Result

PENDING: the route proved ((a), (b), (c) or none), the date, the machine. The PR leaves draft only
once no step is pending and the lines of the specification's decision 6 match this file.
