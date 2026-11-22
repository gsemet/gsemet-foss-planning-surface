## Summary

On the web board's Triage page, the four priority rows of the Backlog column (P1 to P4) could not be hidden, and the "N writes since your last 'rescan'" button gave no clear account of what its count means or what to tell the Chief of Staff (chantier's planning agent). Each priority row now folds on a click on its head, and the button's panel explains the count in plain words, in English and French.

## Deliverables

- A priority row's head carries a chevron button (`aria-expanded`, labelled in both languages). A click on the head or the chevron hides the row's post-its and keeps its chip, count and grill-state counts. A folded head still takes drops, and the selection bar's "-> P<n>" still works on it.
- The choice is kept on the device (the browser's `localStorage`, key `chantier.triageFolded`), one choice per row, the same for every project. All rows are open by default, and a value that cannot be read reads as open.
- The journal panel now opens on three lines (what the count is, why the Chief of Staff may not know of the writes, what to type: "rescan"), and the button carries a one-sentence tooltip.

```js
// js/ui/column.js: new optional parts of lane(parts)
lane({ fold: 'P2', folded: true, foldLabel: t('triage.unfold', { row: 'P2' }), ... })
```

Screenshots at 9b22d87, from Chromium on a demo board:

![Triage with the P2 row folded: its post-its are hidden, its chip, count and grill-state counts stay, the chevron points right](https://github.com/user-attachments/assets/c75cff39-38fd-40cb-a45f-6a585a2c7ec9)

![The journal panel in English: heading, then what the count is, why the Chief of Staff may not know of the writes, what to type, then the list](https://github.com/user-attachments/assets/8905b969-ca31-448d-bfca-45c9af842973)

![The same panel in French](https://github.com/user-attachments/assets/47c8d1e2-99b7-41ae-9955-ef769d134b5b)

![A folded row at a phone width of 390 px](https://github.com/user-attachments/assets/36496890-06da-4493-adba-def0bcdf9b8d)

## Blast radius

The web client only (one new module, a lane's markup, two sheets, two word files, the journal panel). A plain `git revert` restores the previous page; the stored preference is then ignored.

Grade: 1

## Autonomous decisions

- A selected post-it that another write moves into an already folded row leaves the selection too, so the selection bar never acts on a hidden post-it.

## Known gaps

- Some lines added in `js/ui/column.js` are long: two header comments (lines 9 and 10, up to 120 characters) and two template lines (155 and 235 characters). Cosmetic: the web frame's checks (Biome and the repository's tests) pass.

<details>
<summary>Details</summary>

## Changes

- `js/triage/fold.js` (new): reads and writes the folded rows, toggles a row, drops from the selection the post-its drawn in a row being folded.
- `js/ui/column.js`, `js/triage/columns.js`, `js/views/triage.js`, `js/core/store.js`: the `fold`, `folded` and `foldLabel` lane parts and the stored field.
- `js/triage/selection.js`: the selection leaves out post-its drawn in a folded row.
- `js/journal/journal.js`, `css/journal.css`: the three explanation lines above the list, the bottom note removed, the button's tooltip.
- `js/i18n/en-write.js`, `js/i18n/fr-write.js`: new words in both languages.
- `css/components/column.css`: the folded row, the chevron button, the phone-width head.
- `DESIGN.md`, `docs/web-board.md`: the new section and bullets.
- `tests/test_board_design.py`: a guard on the shipped words and markup.

## Human decisions

- Only the four priority rows of the Backlog column fold, each on its own; no "fold all", no other column.
- A folded row keeps its head (chip, counts, chevron); all rows are open by default.
- The choice is kept on the device, one per row, the same for every project; nothing on the server.
- A folded head is still a drop target, and the row stays folded after a drop.
- Folding a row removes from the selection only the post-its drawn in it.
- The explanation says what the count is, why the Chief of Staff may not know of the writes (the board never messages it), and to type "rescan"; it replaces the old bottom note, in both languages.

## Impacts

Triage rows can be folded and the writes count is explained. Nothing else on the board changes.

## Test plan

- [x] New or changed tests (they fail on the previous code): `test_the_fold_and_the_writes_count_explanation_ship` in `tests/test_board_design.py`
- [x] Local gates at 9b22d87: `just check` pass, `just eval-dry-run` pass (18 of 18), `just scenario` pass
- [x] Evidence: after at 9b22d87 (a new behaviour, no before): the four screenshots above, and the 14 browser steps of the specification, all passing
- [x] Review: approved at 9b22d87 (the patch approved at c5af034, then the conflict-resolving rebase approved at 9b22d87)
- [x] Verified at 9b22d87
- [x] CI green at 9b22d87

## Internal references

- CR-440 board-triage-polish

</details>
