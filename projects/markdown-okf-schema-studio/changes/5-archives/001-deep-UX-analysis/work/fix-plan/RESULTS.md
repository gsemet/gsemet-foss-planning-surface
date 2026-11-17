# Deep UX fix campaign — results

Branch `dev/gsemet-deep-ux-analysis`. The plan's commits are `aeb9c03..7a21a2b`: 43 commits on top
of `1a5f8d8`, not pushed, to be squashed into one. T40 verified HEAD `50cd143` on 2026-10-13. Six
more tasks landed after it (T41, T42, T43, T30, T33 and T34, the last in three rounds). A final
regression replay checked HEAD `8d1ee21` on 2026-10-14. Every task after T40 passed the full gate
(`unit types contracts full visual`) and an Opus review.

## Verification summary

| Check | Result | Evidence |
| --- | --- | --- |
| Unit, types, contracts at `7a21a2b` | PASS, 655 unit tests (315 before the plan) | `logs/T34r3-{unit,types,contracts}.log` |
| Full integration at `7a21a2b` (scroll, untrusted, trusted + 40 real-input scenarios, standalone, reload) | PASS, 266 s | `logs/T34r3-full.log` |
| Visual campaign vs the T00 baseline at `7a21a2b` | PASS, 0 new failure lines | `logs/visual-T34r3` |
| Bug replay at `50cd143` (T40, QA skill, real input) | 30 fixed, 1 not fixed (UX-28, then blocked), 3 frozen unchanged | `replay/` |
| Final regression replay at `8d1ee21` (all 37 scenarios) | **0 regressions**; 4 expected changes (UX-21, UX-27 label, UX-28, UX-30), each traced to a decision | `replay-final/SUMMARY.md` |
| UX-28 re-measured at `7a21a2b` | **0** full page reloads for 32 fast characters in a 70 KB chapter, in 4 runs (T40: 26); 16 with the setting off | `replay-final/UX-28.md` |
| Agent visual review (QA-03 step 2) | 143 images: 112 pass, 31 fail; **0 regressions** after triage against T00 | `visual-review/SUMMARY.md` |

## Approved findings

The proving tests are named after their task: `RI-Txx` is a real-input scenario in
`test/integration/realInput.test.ts`. The unit and contract tests are listed in
`reports/Txx-implementation-r*.md`.

| ID | Sev. | Status | Commit(s) | Proving tests | Replay | Notes |
| --- | --- | --- | --- | --- | --- | --- |
| UX-01 | High | fixed | 27c7aff (T08) | RI-T08, unit | [UX-01](replay/UX-01.md) | Escape keeps autosaved text |
| UX-03 | High | fixed | aa43cbf (T10) | RI-T10, unit | [UX-03](replay/UX-03.md) | Undo stays in the textarea (Open With) |
| UX-04 | High | fixed | e4d9e7c (T11) | RI-T11, unit | [UX-04](replay/UX-04.md) | Enter adds a sibling list item |
| UX-12 | High | fixed | 98f6247 (T04) | RI-T04, round-trip unit | [UX-12](replay/UX-12.md) | One cell edit is a one-line diff; part-2 aligned and compact tables kept |
| UX-16 | High | fixed | b3ee36d, 84fc00d (T05, T06) | RI-T05, RI-T06, round-trip unit | [UX-16](replay/UX-16.md) | Part-2 folded scalar, flow sequence and comments are byte-identical |
| UX-17 | High | fixed | 0ffd6ba (T07) | RI-T07, unit | [UX-17](replay/UX-17.md) | Enter saves one-line fields; Cmd+Enter in multi-line fields |
| UX-25 | High | fixed | 433bbd8 (T13) | RI-T13 | [UX-25](replay/UX-25.md) | 0 reloads when a non-Markdown editor gets focus |
| QA-01 | High | fixed | 52a79e0 (T01) | round-trip fixtures in the source style | — | Proven by the unit suite |
| QA-02 | High | fixed | ee8c9bf (T02) | the real-input E2E suite (`realInput.test.ts`) | — | 27 RI scenarios, real mouse and keyboard |
| UX-02 | Med. | fixed | 3a1c944 (T09) | unit, trusted | [UX-02](replay/UX-02.md) | One undo step per edit session |
| UX-05 | Med. | fixed | a39ebb4 (T12) | RI-T12, unit | [UX-05](replay/UX-05.md) | Tab and Shift+Tab indent |
| UX-06 | Med. | fixed | b9317ba (T14) | RI-T14, unit | [UX-06](replay/UX-06.md) | Caret at the click position |
| UX-07 | Med. | fixed | 1bf9c8a (T15) | RI-T15, unit | [UX-07](replay/UX-07.md) | Outline, Done/Revert, shortcut hint |
| UX-10 | Med. | fixed | da76908, fed90bd (T27, T28) | RI-T28, unit | [UX-10](replay/UX-10.md) | Insert between blocks; an empty document is UX-37 (not approved) |
| UX-13 | Med. | fixed | fa73a7f (T17) | RI-T17, unit | [UX-13](replay/UX-13.md) | Tab moves between cells; Tab on the last cell adds a row |
| UX-18 | Med. | fixed | 28ac5b8 (T20) | RI-T20 | [UX-18](replay/UX-18.md) | One click toggles |
| UX-19 | Med. | fixed | 43e1711, cf66e90 (T21, T22) | RI-T21, RI-T22 | [UX-19](replay/UX-19.md) | Enter, Backspace, link suggestions, click edits |
| UX-23 | Med. | fixed | 25fefa5 (T26) | RI-T26, unit | [UX-23](replay/UX-23.md) | "File not found" labels, badge jumps to the first issue |
| UX-28 | Med. | fixed | e26e836, a9d4545, 0f4605a, 8d1ee21, 7a21a2b (T43, T30, T33, T34) | RI-T43, RI-T30, RI-T34 (with a 70 KB document), unit | [UX-28](replay-final/UX-28.md) | 0 reloads while typing 32 fast characters in a 70 KB chapter (was 26); kill switch `incrementalUpdates` |
| UX-30 | Med. | fixed | 9659cda, fabc1fa (T36, T42) | RI-T36, package contract | [UX-30](replay/UX-30.md) | Title-bar button, Explorer entry, Cmd+K Shift+V; command category (D-20) |
| QA-03 | Med. | fixed | ce5784e (T03) + T40 | visual machine checks; agent review | — | Machine checks (T03) and the agent review (`visual-review/`) |
| UX-08 | Low | fixed | 1bf9c8a (T15) | RI-T15 | [UX-08](replay/UX-08.md) | Monospace editor, tab size 4 |
| UX-09 | Low | fixed | 7041461 (T16) | RI-T16 | [UX-09](replay/UX-09.md) | No reflow in edit mode |
| UX-11 | Low | fixed | d596de8 (T32) | RI-T32 | [UX-11](replay/UX-11.md) | 0 px drift for blocks; table jump only with End ([probe](replay/table-commit-scroll.md)) |
| UX-14 | Low | fixed | b2c5476 (T18) | RI-T18 | [UX-14](replay/UX-14.md) | Toolbar above the table, labelled |
| UX-15 | Low | fixed | 21106e0 (T19) | visual machine checks | [UX-15](replay/UX-15.md) | Short identifiers do not wrap; overflow cue (D-19) |
| UX-20 | Low | fixed | 24d5ab9 (T23) | RI-T23 | [UX-20](replay/UX-20.md) | Row actions in the edited row, nothing clipped |
| UX-21 | Low | fixed | d67a757, 4b2d6b8, 50eab0f (T24, T25, T41) | RI-T24, RI-T25, RI-T41 | [UX-21](replay-final/UX-21.md) | Gaps closed by T41 (D-21) |
| UX-26 | Low | fixed | 9cb75e1 (T35) | RI-T35, wording unit | [UX-26](replay/UX-26.md) | No user-facing "Sphinx"; status title and message on two lines |
| UX-27 | Low | fixed | 50cd143 (T39) | RI-T39 | [UX-27](replay/UX-27.md) | Locked preview group; released on close |
| UX-29 | Low | fixed | 29a3df8 (T31) | RI-T31 | [UX-29](replay/UX-29.md) | Case 1 replayed; case 2 not reproducible before the fix |
| UX-31 | Low | fixed | 0d0ada9 (T37) | package contract | [UX-31](replay/UX-31.md) | "MyST + OKF Studio" |
| UX-32 | Low | fixed | 0d0ada9 (T37) | RI, unit | [UX-32](replay/UX-32.md) | "Studio · file.md" / "file.md" |
| UX-33 | Low | fixed | 0c5c352 (T38) | RI-T38, unit | [UX-33](replay/UX-33.md) | Anchor disabled without an editor; edit mode remembered |

### Frozen findings (must not change)

| ID | Replay | Status |
| --- | --- | --- |
| UX-22 | [UX-22](replay/UX-22.md) | unchanged: E10 without `projectRoot`; setting it still fixes the link |
| UX-24 | [UX-24](replay/UX-24.md) | unchanged: YAML-style values |
| UX-34 | [UX-34](replay/UX-34.md) | unchanged: `#` markers in the sticky band |

## Decision D-10 as shipped

The setting `markdownOkfSchemaStudio.preview.incrementalUpdates` ships with the default **`true`**.
T34 passed every gate and three Opus reviews. The setting is documented in the README, and turning
it off restores full page loads live, without a window reload (`replay-final/UX-28.md`).

## Tasks after T40

| Task | Commit | Rounds | What |
| --- | --- | --- | --- |
| T42 | fabc1fa | 1 | Command category "Markdown OKF-Schema Studio", short titles (D-20) |
| T41 | 50eab0f | 2 | UX-21 gaps: new fields where the table shows them, a one-line custom key, Escape closes (D-21) |
| T43 | e26e836 | 2 | No reload while a render is pending; delayed overlay after 1.5 s (D-22, replaces T29) |
| T30 | a9d4545 | 1 | Properties table and link updates patched in place |
| T33 | 0f4605a | 1 | Runtime refactor: content initialization can run again |
| T34 | 8d1ee21, 7a21a2b | 3 | Content patched in place, behind a setting; chained patches while typing fast |

T29 is superseded by T43 and was never committed. No task is blocked.

## Open follow-ups worth a decision

The full list is in `followups.md`. The main ones:

1. **The `bug-edition-mode` request** (`../../bug-edition-mode/01-intent.md`). It covers:
   - the block editor's layout, a smaller font, and Cancel;
   - Esc behaving like Cancel, which replaces the UX-01 behaviour;
   - Home/End moving the caret within the block. Today, on macOS, they scroll the whole preview,
     and End shifts a table by about 440 px.
2. **Part-2 findings UX-35 to UX-48**, not approved yet. UX-35 (CRLF inline edits) is the most
   severe.
3. **T39.** With `workbench.editor.closeEmptyGroups: false`, closing the preview can unlock an
   empty group that the user locked on purpose.
4. **T34 follow-ups.**
   - The PlantUML patch has no fallback timer.
   - Link-target hints can stay stale until the next full load.
   - `patchPropertiesTable` and the PlantUML patch still need the page to be fully caught up, so
     they can fall back to a full load during a burst.
5. **Harness.**
   - The visual "sticky heading overlaps the toolbar row" check is too strict.
   - The UX-30 scenario's tooltip check is stale since T42.
   - RI-T32's table case presses End.
6. **Seen once, not investigated.** VS Code's own webview host throws "Found unexpected null"
   when a frame is replaced quickly. `401` bursts come from short-lived `fake.html` frames.
