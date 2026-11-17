# Review checklist

The reviewer works read-only on the code. The only file you write is `reviews/Txx-review-rN.md`.
Review the **diff from the task's base SHA**, not the whole codebase. The user's priority is: *never
break a feature they want*. When in doubt, request changes.

## Inputs

- The task file `tasks/Txx-*.md`: goal, decisions, allowed files, expected test changes, must-not-change list.
- `protected-features.md`, `conventions.md`, `decisions.md` (overrides win over defaults).
- The implementation report `reports/Txx-implementation-rN.md`.
- The gate logs `logs/Txx-*.log` and the gate summary in `STATE.md`.
- The diff: `scripts/diff.sh <BASE>`.
- For UI tasks: the screenshots and notes the task produced (paths are in the report). Open the PNGs
  with the Read tool and look at them.

## Checks (all mandatory)

### A. Scope

1. Every changed or new file is listed in **Allowed files**, or the report justifies it and the
   justification is sound. Unexplained files → BLOCKER.
2. No change touches frozen behaviour (UX-22 link resolution and messages, UX-24 value display,
   UX-34 sticky band text) → otherwise BLOCKER.
3. No unrelated refactor, rename, reformatting, or dependency change. Unrelated churn → MAJOR.

### B. Correctness against the task

4. Each "Done when" criterion of the task is met. Cite the test or evidence that proves it.
5. Each decision referenced by the task is implemented as specified (or as overridden).
6. Edge cases listed in the task are handled and tested.
7. Read the changed functions completely, not only the hunks. Look for: off-by-one errors on
   lines/offsets, `\r\n` splitting, stale identifiers (documentVersion/requestId), listeners
   registered twice, timers not cleared, `activeBlockEdit`/`activeFrontmatterEdit` left set,
   focus lost, promises not handled.

### C. Tests

8. New tests exist for every behaviour change, at the levels the task requires: unit, and
   real-input E2E for interaction bugs.
9. The report shows the new bug tests **failing before the fix** (an excerpt). If it is missing for
   an interaction bug → MAJOR.
10. Existing assertions: compare `git diff <BASE> -- test/`. Every modified or deleted assertion is
    listed in the task's **Expected changes to existing tests** and justified in the report.
    Weakened assertions (broader regex, removed checks, added `skip`/`todo`) → BLOCKER.
11. Tests are meaningful. A test that would also pass without the fix is not evidence.

### D. Regressions

12. All gate levels required by the task passed. Compare failures with the T00 baseline in
    `STATE.md`. A new failure → BLOCKER, even if "flaky", unless the report proves flakiness with
    two clean reruns.
13. Walk through `protected-features.md` for every area the diff touches, and name the IDs you
    checked. For each touched area, state how it is still covered (test name or manual check).
14. Webview runtime changes (`scrollSync.ts`): no backtick or `${` inside the template, every
    backslash doubled, browser APIs guarded, no global `setTimeout`. See `conventions.md` §2.
15. Message protocol: new types and fields are validated in `isPreviewSyncMessage`, and edit paths
    still check versions (P-S2). Data reaching `innerHTML` is escaped (P-S4).
16. Read-only mode: new interactive features are inert when `editModeButton` is absent or
    `preview.readOnly` is true (P-E8).
17. Accessibility did not regress: focusable controls keep accessible names, and keyboard paths
    still work.

### E. Visual (UI tasks only)

18. Open each new or changed screenshot. Check the task's visual criteria and the generic ones: no
    control covers text it should not, nothing is clipped, text is readable in the captured theme,
    and there is no unexpected layout shift elsewhere on the page.
19. Machine checks (from T03) in the notes are PASS for the scenarios the task names.

### F. Docs

20. User-visible behaviour changes are reflected in `README.md`; scroll behaviour changes in
    `docs/scroll-anchoring.md`; identity changes in the repository's `AGENTS.md` when the task says
    so.

## Severity

| Level | Meaning | Effect |
| --- | --- | --- |
| BLOCKER | Regression, data loss risk, frozen behaviour touched, scope violation, failing gate, weakened test | Verdict cannot be PASS |
| MAJOR | Done-when not met, missing required test, decision not applied, unjustified churn | Verdict cannot be PASS |
| MINOR | Small quality issue that does not affect users | PASS allowed; the orchestrator logs it in `followups.md` |
| NIT | Style preference | Mention once; never blocks |

## Report format (`reviews/Txx-review-rN.md`)

```markdown
# Txx review — round N

Base: <sha> · Reviewed diff: <files count> files, +<added>/-<removed>

## Gates
<level>: PASS|FAIL (log path) … and comparison with the T00 baseline

## Done-when
- [x] <criterion> — evidence: <test name / screenshot>
- [ ] <criterion> — why not

## Protected features checked
P-xx: <how it is still covered> …

## Findings
1. [BLOCKER|MAJOR|MINOR|NIT] <file>:<function> — <problem>. Fix: <precise instruction>.

## Existing assertions changed
<list with OK / NOT JUSTIFIED>

VERDICT: PASS | CHANGES REQUESTED
```

Give fix instructions precise enough for a Sonnet implementer to apply them without re-deriving the
analysis: name the function, the exact behaviour, and the test to add.
