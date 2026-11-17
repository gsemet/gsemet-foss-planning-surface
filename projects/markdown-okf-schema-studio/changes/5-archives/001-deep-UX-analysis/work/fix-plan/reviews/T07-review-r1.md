# T07 review — round 1

Base: 84fc00d · Reviewed diff: 4 task files, +186/-5 (`book/chapters/05-skills.md` also differs from
base but is the user's pre-existing uncommitted work, not part of T07; the orchestrator must not stage it)

## Gates
compile: PASS · unit: PASS (logs/T07-unit.log) · types: PASS
trusted: NOT RUN by the reviewer (screen locked, per orchestrator). Implementer logs:
logs/T07-impl-trusted.log shows RI-T07 screenshots 11/12 PASS with the fix;
logs/T07-impl-prefix-trusted.log shows RI-T07 failing on pre-fix source
("Timed out waiting for the title to reach the source buffer."). The checkboxToggle "one undo"
failure reproduces on HEAD source and matches the locked-screen environment issue. The orchestrator
must still run `trusted` after unlock before committing.

## Done-when
- [x] Enter saves a one-line text field; Shift+Enter does not — unit "Enter saves a one-line frontmatter text field and Shift+Enter does not"; RI-T07 part 1
- [x] Multi-line: Enter inserts, Cmd/Ctrl+Enter saves — unit "Enter in a multi-line frontmatter text value…"; RI-T07 part 2 (`…a\nb`)
- [x] Trailing line breaks stripped unless original ended with one — unit "saving a frontmatter text field strips trailing line breaks…" (both branches)
- [x] YAML editor: Enter newline, Ctrl+Enter saves — unit "Enter in the YAML frontmatter editor…"
- [x] aria-keyshortcuts + title — asserted in unit test 1
- [x] README sentence — added
- [ ] trusted gate on a quiet machine — pending orchestrator run (not a code finding)

## Protected features checked
P-E7: Escape branch untouched (cancel); list editor excluded via `!useListEditorValue` (both in
keydown and the strip); non-TEXTAREA controls (enum/date/number/key editor) still save on Enter;
checkbox untouched. Covered by existing frontmatter tests in scrollSync.test.ts (unit PASS) and
RI 08–10 in the trusted log.
P-E3/P-E4: block editor keydown not touched.
P-E8: change lives inside the frontmatter editor, which only opens in edit mode.
P-S2/P-S4: no new message types; title/aria set via setAttribute with constant strings.
Runtime template (conventions §2): `"\\n"`, `/(?:\\r?\\n)+$/u`, `\\u00b7` correctly doubled; no
backticks or `${`; `isComposing` guard added (IME-safe).
Visual: 11-frontmatter-title-enter.png shows the title saved as a single-quoted one-line scalar,
table re-rendered, editor closed, no layout issue.

## Findings
1. [MINOR] README.md — the edited line exceeds the 100-column wrap
   rule ("…as generic YAML. In a one-line text field, Enter saves and"). Fix: rewrap the paragraph at
   100 columns at clause boundaries.
2. [NIT] scrollSync.ts keydown — `multiline` checks only `"\n"`; a lone `"\r"` value is
   theoretical in a textarea. No action.

## Existing assertions changed
None (diff of test/ is additions only).

VERDICT: PASS
