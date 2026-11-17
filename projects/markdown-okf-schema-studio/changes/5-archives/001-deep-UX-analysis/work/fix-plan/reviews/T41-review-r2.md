# T41 review — round 2

Base: fabc1fa · Reviewed diff (extension): 6 files, ~+460/-34.
Round 2 changes only `src/frontmatter/okfFrontmatter.ts` and `test/frontmatter/okfFrontmatter.test.ts`.

## Gates
- unit, types, contracts: PASS.
- visual: PASS against the baseline, 0 new.
- full: PASS in 256 s (`logs/T41r2b-full.log`).
- One `full` run (`logs/T41r2-full.log`) and one run by the implementer failed in
  `checkboxToggle.test.ts:146`, "one undo to restore the original source". Two `trusted` reruns and
  one `full` rerun on the same tree passed.
- **Is the flake related to T41? No.**
  - That test drives the host only: `showTextDocument` followed by the `undo` command. It sends no
    keyboard Escape and opens no frontmatter editor.
  - T41's host change is confined to `handleFrontmatterSave`, which runs only for a
    `previewFrontmatterSave` message.
  - The new webview listener does nothing unless all of these hold:
    - the key is Escape;
    - an `activeFrontmatterEdit` exists;
    - the target is inside `[data-okf-properties]`.
  - Nothing in the diff touches checkbox toggling, the checkbox message path or undo grouping.
  - I agree with logging it as a focus-dependent flake in `followups.md`. Two clean reruns meet the
    checklist's bar (item 12).

## Done-when
- [x] **D-21 a, position.** Unchanged since round 1, and verified there.
  - The `leading` case now inserts at the first key's line, after any leading comments. Probes:
    - `# header` / `title` gives `# header`, `a: ""`, `title: x`;
    - CRLF with two header comments gives `# h1`, `# h2`, `a: ""`, `title: x`, keeping CRLF;
    - with no comment, the key goes at offset 0.
- [x] **D-21 b, quoted only when YAML requires it.**
  - `isPlainSafeScalar` now also requires the YAML 1.1 `stringify` round-trip, and rejects a tab
    and a bare `=` or `<<`.
  - Probe against `out/`: `2026-10-13`, `1_000`, `0b101`, `12:30`, `=`, `<<` and `a\tb` now give
    `false`.
  - `Ann`, `two words` and `?x` give `true`, and each round-trips as a string.
- [x] **D-21 c, Escape.** Unchanged since round 1, and verified there.

## Findings from round 1
1. MAJOR `isPlainSafeScalar`: **fixed as specified.** `T41: plain scalar safety` now holds the full
   list, and `T41: plainScalar quotes a date-like value` writes `approver: "2026-10-13"`. Both
   failed before the fix (`logs/T41-pre2-unit.log`).
2. MINOR, the `leading` offset: **fixed as specified.** The test is `T41: beforeField on the first
   key inserts after leading comment lines`, with LF and CRLF.
3. NIT: no action, as agreed.

Local run: `node --test out/test/frontmatter/okfFrontmatter.test.js` gives 61 pass and 0 fail.

## Protected features checked
- **P-F one-line diffs and comments:**
  - the new header test is a one-line diff;
  - the earlier RI-T41 `lineDelta` checks and the existing frontmatter suite pass.
- **Existing values keep their style:** I re-ran the probe, and `title: '"Ann"'` is unchanged
  without `plainScalar`.
- **D-08 required fields:** not touched (RI-T24 passes).
- **Read-only mode (P-E8), messages (P-S2), escaping (P-S4) and the webview template rules:**
  unchanged since round 1.

## Scope and hygiene
- In the extension, the only files changed since fabc1fa are the six allowed files.
- The modified `.agents/skills/...` and `.agents/thinking/...` files were already modified before
  T41 started (see the session's starting git status). They are not part of this task.
- No `console.log` or `debugger` statements in the changed sources.
- No dependency changes.

## Existing assertions changed
- RI-T24 and RI-T25: as in round 1, required by D-21 a and b. **OK.**
- Round 2 changed no existing assertion; the safety test was only extended.

VERDICT: PASS
