# Answers

## 2026-11-12: picked for the next batch

Owner, 2026-11-12: « je suis d'accord. grille avec un advisor fable et fini par une CR de release. demande moi uniquement quand il y a un impact utilisateur », agreeing to add this item to the batch after the v1.7.1 retro items.
Priority P1. Open questions: a Fable advisor answers them; the owner is asked only on a user impact.

## 2026-11-12: delivery of the batch

Owner, 2026-11-12: « tu livreras une stack prete a mergée avec le PR de release en dernier ».
Open: this conflicts with the release-process guideline (the version commit is never stacked on
top of development; the stack lands first, then the heavy run on `main` HEAD, then the version PR).
The conflict was reported to the owner.

Owner, 2026-11-12, on the conflict: « Yes, and update the guide ». The release PR is the top of the
stack; before it turns ready, the heavy run is dispatched on the stack's top branch
(`gh workflow run ci.yml --ref <branch> -f heavy=true`); the owner merges the whole stack by
rebase in order; the version push on `main` stays the final gate and makes the tag.

## 2026-11-12: Fable advisor

A Fable advisor (read-only, at origin/main cb968299) answered the INTERNAL questions; its report is
`intake/advisor-grill.md` (the section of this CR). Its INTERNAL recommendations are adopted, per the
owner's instruction to be asked only on a user impact. USER-IMPACT questions go to the owner.

## 2026-11-12: USER-IMPACT answers

Owner, 2026-11-12: « exclu "Open VSX" pour l'instant. ok pour tout le reste. »
- Cmd+S / Ctrl+S with focus in the preview saves the Markdown document the preview shows.
- An open block or cell editor stays open with its caret; the typed text is written to the document first, then saved.
- The command is hidden from the Command Palette (like editUndo); the key can be rebound in Keyboard Shortcuts.
Batch: Open VSX is out, so the release is v1.8.0 (Cmd+S is a feature; honest commit types).

## 2026-11-12: front matter field and Cmd+S

Owner, 2026-11-12: « b, and go ». With the focus in a front matter field editor (properties table),
Cmd/Ctrl+S writes the typed value and closes the field, as a navigation does today, then saves the
document. Block and cell editors stay open (earlier answer).

## Night autonomy: round 4 (Chief of Staff, 2026-11-13)

Round 4 granted under the owner's night autonomy (order O-1). It adds the
`activeCustomEditorId == 'markdown-okf-schema-studio.editor'` clause to the save binding and its
contract test, checks that `runSaveCommand` finds the custom editor's session, and re-runs the
heavy run on the new head. **For the morning review:** keep that clause (the spec's rule) or drop
the custom-editor step and leave native save as it is.

## Round 4 decision (owner order O-1)

- Keep the clause: the save key binding is now `activeWebviewPanelId == '...preview' || activeCustomEditorId == '...editor'`, like the find, undo and redo bindings. `runSaveCommand` finds the custom editor's session through `panel.active`, as `runFindCommand` does. Package contract test updated. Commit aed1a0ad.
