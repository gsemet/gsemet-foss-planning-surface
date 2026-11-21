# Verify CR-461

Head: afc00137a4b83eaef1c3d7d9372e6bb296dc3922

Verdict: VERIFIED (content claims). The posted PR body still shows "Review pending" and "CI green pending" boxes: the description pass is the Driver's later step.

## Claims (all judged at afc00137)

1. 02-answers.md (mm-Q1): no code, limit in docs/known-limitations.md and in the SwRS of the side preview that follows the active editor, with the reason (no tab input class in the VS Code API).
   - Command: `git diff origin/main...HEAD` (worktree, head afc00137). Output: 4 files only: docs/known-limitations.md (bullet now names the multi-file diff editor and the merge editor (3-way merge), the reason, the workaround), docs/user/open-studio.md (one sentence), requirements/tiers/swrs/lifecycle-sync/SwRS-MDOKFSTUDIO-LIFE-026.md (boundary scenario "Editors the side preview does not follow" with two rows, the reason, and a Known issues line), requirements/tiers/log.md (dated entry). No file under src/ or test/. PROVED.
2. LIFE-026 is the SwRS of the side preview that follows the active editor (text diff following).
   - Diff context shows its scenarios "a text diff whose real file ... switches" in the same file. PROVED.
3. The limit is real: the side preview does not render the multi-file diff nor the merge editor.
   - Command: `grep -n "class TabInput" node_modules/@types/vscode/index.d.ts` (typings 1.140.0). Output: only TabInputText, TabInputTextDiff, TabInputCustom, TabInputWebview, TabInputNotebook, TabInputNotebookDiff, TabInputTerminal. `grep -c "MultiDiff\|TextMerge"` on the same file: 0.
   - Command: `grep -rn "TabInputTextDiff" src`. Output: the only diff-following hook is src/host-vscode/activation.ts:201, `tab.input instanceof vscode.TabInputTextDiff`, and src/host-vscode/diffRealFile.ts; `grep -rniE "multi-file|multidiff|merge editor" src` finds only src/host-vscode/openingWatcher.ts:49 ("the merge editor has no input class in the API: it is `other`"). No code recognises either editor. PROVED.
4. Docs wording matches the code (button/command/following do not apply; workaround: text editor or single-file diff).
   - open-studio.md says the button, command and following do not apply; the following is driven by activation.ts:198-204 (active text editor and TabInputTextDiff only). Consistent. PROVED.
5. Requirements and gate: `just preflight` passed at this head. Command: first line of work/gates/20261121-211414.log is `gate CR-461 branch chantier/batch-07/cr-461-side-preview-multi-file-diff-and-merge-e head afc00137a4b83eaef1c3d7d9372e6bb296dc3922`, last lines `ci-static: passed` and `result: pass at afc00137a4b83eaef1c3d7d9372e6bb296dc3922`. `$CHANTIER log` shows `gate result=pass head=afc00137...`. Worktree clean (`git status --short` empty). PROVED.
6. PR body (read with `gh pr view 470`): Summary, Deliverables, Changes match the diff (4 files, no code; the Known gaps entry about the untested limit is consistent). It still holds the unchecked "Review" and "CI green" boxes: to be completed by the Driver before the description pass. Not a content failure.

No before/after evidence: documentation only, no UI change (nothing to capture).
