# Reproduction, 2026-11-20 (main 1.10.0, no fix)

Reproduced every time. Cause: CRLF line endings, not a timing race.

## Sequence
1. Open a Markdown file with CRLF line endings and a multi-line block (a hard-wrapped paragraph
   of 2+ lines, a list item with nested items, or a list's last item whose range takes the
   trailing blank line).
2. Edit mode, click the block.
3. Leave without a real change (Done, Ctrl+Enter, click another block, arrow past the edge; or
   type a character and delete it).
4. "Saving Markdown..." stays; Done, Cancel, Escape do nothing; only a reload clears it.

The owner's screenshot is chantier's README.md, CRLF (core.autocrlf=true, no eol=lf rule there).
Studio and the planning surface force eol=lf, so it never shows there: hence "intermittent".

## Root cause
- Page: src/page/features/blockSourceEditor.ts:138-141 fills the textarea; the browser turns
  \r\n into \n. src/page/features/blockEditor.ts:376-386 (postBlockEditSave) rebuilds
  textarea.value + trailingLineEnding = "a\nb\r\n", differs from originalText "a\r\nb\r\n",
  sets finishing and "Saving Markdown..." (389-392), posts a final previewEditSave. The same
  mismatch makes each keystroke post an autosave.
- Host: src/session/features/blockEdits.ts:319-330 normalises with withLineEndingOf
  (src/core/edits/sourceEdits.ts:288): equal to lastSavedText, nothing written;
  completeActiveBlockEdit (297-314) has refreshes=false, so no render, no patch, no error:
  the host sends nothing back.
- Page has no way out: only a content patch (contentPatch.ts:56) or a previewEditSource error
  (blockSourceEditor.ts:54-58) resets finishing; Cancel/Escape return early (blockEditor.ts:533).

Timing races on LF files: 1,800 random steps, ~174 final saves, 30/200 ms latency, outside edits
mid-save: 0 stuck.

## Fix
1. Page: put the edited text in the source's own line ending before comparing or posting (same
   rule as withLineEndingOf). Also in moveBlockFromEditor (blockEditor.ts:214) and any table or
   convert path that reads the textarea.
2. Host safety net: every final save or cancel gets an answer; when completeActiveBlockEdit ends
   with no refresh, send an "edit done" reply for that editId (or re-send the patch). Also covers
   the sourceAvailable=false and same-revision paths.

## Tests
- Host: CRLF document, open a multi-line block, final save with LF text: a patch, error or reply
  must arrive. scratch/crlfNoopSave.test.ts fails on 1.10.0 (nested-list case).
- Page runtime: CRLF multi-line source, Done with no change: editor closes, no previewEditSave.
- Both need an SwRS (BLOCK-047/042 area).
- scratch/savingStress.ts: stress harness (real host + page in Chromium), `--minimal --crlf`
  shows the stuck state at once.
