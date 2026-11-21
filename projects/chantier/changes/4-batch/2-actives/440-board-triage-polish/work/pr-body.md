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

Screenshots: not yet attached.

## Blast radius

The web client only (one new module, a lane's markup, two sheets, two word files, the journal panel). A plain `git revert` restores the previous page; the stored preference is then ignored.

Grade: 1

## Autonomous decisions

- A selected post-it that another write moves into an already folded row leaves the selection too, so the selection bar never acts on a hidden post-it.

## Known gaps

- **UNVERIFIED:** the behaviour in a browser (fold, reload, drag onto a folded head, phone width) is not yet proven; the project has no JavaScript test runner.

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

## Impacts

Triage rows can be folded and the writes count is explained. Nothing else on the board changes.

## Test plan

- [ ] New or changed tests (they fail on the previous code)
- [ ] Local gates at `<sha7>`:
- [ ] Evidence: before at `<sha7>`, after at `<sha7>`
- [ ] Review: approved at `<sha7>`
- [ ] Verified at `<sha7>`
- [ ] CI green at `<sha7>`

## Internal references

- CR-440 board-triage-polish

</details>
