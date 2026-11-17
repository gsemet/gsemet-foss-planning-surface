# End-to-end test: Done on a card title editor replaces only the directive line

SwRS-MDOKFSTUDIO-BLOCK-258 (proposed, CR 209 / #229) says "Done replaces line 8 only", but only the
line mapping (8/8) and the editor content are tested. Add a visual/e2e check that edits the title,
presses Done and asserts the document diff touches only the directive line. Non-blocking Inspector
finding on CR 209.
