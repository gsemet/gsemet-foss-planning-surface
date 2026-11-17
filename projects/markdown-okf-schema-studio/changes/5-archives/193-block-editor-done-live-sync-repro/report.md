# 193 — Block editor Done during live sync: NOT REPRODUCED (closed, no PR)

Owner rule: act only once reproduced; one short attempt (2026-10-29 night batch).

- Attempt: headless page-runtime test, 4 orderings of Done vs a live sync / content patch (A: autosave
  flushed, Done, then patch; B: Done twice, then patch; C: patch, then Done; D: host refuses the final
  save). Result on origin/main cb1f2adc: 4/4 pass. Test kept at `reports/blockEditorDoneLiveSync.test.ts`;
  details in `reports/repro-attempt.md`.
- Why it passes: `postBlockEditSave` guards with `edit.finishing` and cancels the autosave timer;
  `applyContentPatch` always closes the editor and clears the status; an error reply resets
  `finishing`.
- Residual hypotheses (host side, unverified): no timeout/ack for the final save (status could stay
  "Saving Markdown…" if the host sends neither a patch nor an error); autosave and final save carry the
  same `originalText`/lines, so a host applying both against moved lines could duplicate source.
- Reopen only with a real reproduction (a recording or a host-side `previewEditSave` test).
