## Summary

Coder, Inspector and Verifier replies were far longer than the ten-line cap in `worker.md` (Coders 93 to 105 lines, a Verifier 69, measured on an earlier batch's transcripts; **UNVERIFIED:** not re-measured here), and each long reply is paid again on every later turn of the Driver. Out-of-format Inspector and Verifier replies (`APPROVED` for `APPROVE`, a missing `head`) also each cost a restart. This PR gives those three roles an exact reply template, makes a reply that is only too long a note instead of a restart, and makes `chantier verdict` say which words it accepts when it refuses one.

## Deliverables

Before (base `4ecc7cd`) and after (this branch's head) of the `verdict` refusal (exit code 1 both times):

| | Output |
| --- | --- |
| Before | `verdict <cr> VERIFIED \| "NOT VERIFIED"` |
| After | `verdict: "APPROVED" is not a verdict: the accepted words are VERIFIED and "NOT VERIFIED"` |

The three reply templates now end their sections in `skills/chantier/references/worker.md`:

```text
Coder:     Round <n>: done | blocked: <reason> / Notes: / Gate: / Open:
Inspector: one JSON object, keys verdict, head, blocking, minor, confidence
Verifier:  VERIFIED | NOT VERIFIED / Head: / Proof: / Failed:
```

**UNVERIFIED:** the gain in reply length is not measured by this PR.

## Blast radius

Grade: **1**. Two cards, one CLI message and one scenario check; a plain `git revert` restores the previous behaviour.

## Autonomous decisions

- The open points of the specification took its stated defaults: no template for the Investigator, Debugger and Conflict resolver; an extra key in an otherwise correct Inspector JSON is read and noted, not restarted; the gain is measured once afterwards, with no standing card step.

## Known gaps

- The accepted lower-case `verified` word was checked only up to the word check (on an unknown change, which then fails for that reason), not by recording a verdict on a scratch change; the scenario covers recording.
- The gain is not proved by this PR; it is measured on the transcripts of the next batch (reply length of each Coder, Inspector and Verifier compared with the earlier figures in the Summary, which are also not re-measured here).

<details>
<summary>Details</summary>

## Changes

- `skills/chantier/references/worker.md`: the shared paragraph, and the Coder, Inspector and Verifier sections end with the exact reply template; a reply in format that only passes its cap is not a failed worker.
- `skills/chantier/references/driver.md`: the format checks read the Verifier's first line and `Head:` and the Coder's `Notes:` line; a new "long reply is read, not restarted" rule with its `long reply:` note.
- `skills/chantier/scripts/cli/src/chantier/commands/delivery.py`: `verdict`'s refusal quotes the word given and names the accepted words.
- `scenario/run_scenario.py`: the verdict check also reads the refusal's text.

## Human decisions

- The coder, inspector and verifier sections end with an exact reply template.
- An over-long reply is accepted but noted, not restarted.
- The `verdict` refusal names the accepted words.

## Impacts

No visual change. Workers' replies should get shorter, and restarts for out-of-format verdict words should drop (not measured here).

## Test plan

- [ ] New or changed tests: the scenario's verdict check reads the new refusal text
- [x] Local gates at `97e7df7`: `just check` pass (before review); `just scenario` pass
- [x] Evidence: before at `4ecc7cd`, after at `97e7df7`: `verdict <cr> APPROVED` exits 1 both times, with the old usage line before and the new refusal after
- [x] Review: approved at `469a709`, carried from `469a709` over two clean rebases to `97e7df7`
- [x] Verified at `97e7df7`
- [x] CI green at `97e7df7`: `gh pr checks 202`, all 5 jobs pass

## Internal references

- CR-256 worker-reply-length

</details>
