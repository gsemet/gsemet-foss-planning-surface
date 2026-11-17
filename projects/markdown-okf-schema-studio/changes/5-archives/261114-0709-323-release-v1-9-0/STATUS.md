# CR-323 Change Specification: release v1.9.0

✅ merged · batch-04

**Now:** Merged: its PR/MR.
**Next:** Nothing.

## Progress

- [x] Note: draft: /Users/az02065/Projects/DevTools/markdown-okf-schema-studio.worktrees/batch-04-CR-323/docs/releases-notes/2026-11-14-v1.9.0/release-notes.md
- [x] Note: draft: /Users/az02065/Projects/DevTools/markdown-okf-schema-studio.worktrees/batch-04-CR-323/docs/releases-notes/2026-11-14-v1.9.0/tweet.md
- [x] Note: Attempt 1: notes, thread and hero (CR-318 Verifier cream capture, cropped 4:3) drafted in docs/releases-notes/2026-11-14-v1.9.0; waiting for the heavy run of main 1191fb6c (run 43532691444).
- [x] Note: Heavy run 43532691444 on main 1191fb6c: integration red at one step (toc: Edit toggle click never reached the page, 3 tries), looks like a real-window flake; re-run of the failed jobs once when stress ends, per the procedure.
- [x] Note: Re-run attempt 2 of 43532691444 green on main 1191fb6c (integration, stress success): toc step was a flake. Making the version commit.
- [x] Long gate fail: f12ba53b
- [x] Note: Branch heavy run 43536948441 at f12ba53b: integration red at real-input (Heading 2 prefix timeout), a different step from main's flake; re-run of the failed jobs once. Local preflight: static ok, visual 1 scenario red (v31, passes in CI), integration red at tall-block-scroll (local window).
- [x] Note: Local ci-visual re-run: v31-mark-editor-selection-light-900 red again; intermittent local failure already seen in CR-315 and CR-322 gates (passes in CR-317..321 and in CI visual), not caused by the release commit (versions and docs only).
- [x] Shipped: https://github.com/gsemet/markdown-okf-schema-studio/pull/395
- [x] Note: PR 395 CI green at f12ba53b (static, static-windows, visual, report, checks pass); branch heavy run 43536948441 attempt 2 green at the same head. Ready for the Foreman to merge by rebase.
- [x] Blocked: merge: https://github.com/gsemet/markdown-okf-schema-studio/pull/395
- [x] Merged
- [x] Handed back

## Documents

- [request](intake/request.md)
- [intent](01-intent.md)
- [answers](02-answers.md)
- [specification](03-change-spec.md)
- [body-sections](work/body-sections.md)
- [pr-body](work/pr-body.md)
- [long gate log](work/gates/ci-visual-rerun.log)
- [.agents/guidelines/release-process.guidelines.md](../../../guidelines/release-process.guidelines.md)
- [CONTRIBUTING.md](../../../../CONTRIBUTING.md)

## Where

- Branch: `chantier/batch-04/cr-323-change-specification-release-v1-9-0`
- Worktree: `/Users/az02065/Projects/DevTools/markdown-okf-schema-studio.worktrees/batch-04-CR-323`
- Driver: `a1541be76e92e542d`

## Decisions and open questions

- Local ci-visual re-run: v31-mark-editor-selection-light-900 red again; intermittent local failure already seen in CR-315 and CR-322 gates (passes in CR-317..321 and in CI visual), not caused by the release commit (versions and docs only).
- PR 395 CI green at f12ba53b (static, static-windows, visual, report, checks pass); branch heavy run 43536948441 attempt 2 green at the same head. Ready for the Foreman to merge by rebase.
- merged: https://github.com/gsemet/markdown-okf-schema-studio/pull/395
- merged: None
- published: v1.9.0 https://github.com/gsemet/markdown-okf-schema-studio/releases/tag/v1.9.0
- Owner, 2026-11-14: « fait tout ça dans le batch en cours et fait un release 1.9.1 ». Second release of grant O-11 (releases=2): v1.9.1 (patch) after CR-324, CR-325 and CR-326 are merged. Settled: same procedure as v1.9.0; the owner merges the version PR; success = the version push's Release VSIX run (dispatched, branch main) publishes to Open VSX with no recovery dispatch, else one recovery dispatch and report it as a failure of CR-324; watch both registries 10-15 min; no hero image; thread drafted, never posted. Decisions in .agents/changes/1-inbox/release-v1-9-1/02-answers.md (the CLI allows one release CR per batch).
- fix: CR-327 must merge first; then the procedure starts again from its first step
- Owner, 2026-11-14, on the palette stress failure of main's heavy run 43582068953: « Oui si ça arrive tu fais une CR de fix ». If attempt 2 is red, the Chief of Staff files a fix CR for the palette focus bounce (B/B2), fix for CR-323, merged before the v1.9.1 version PR; no further ask to the owner.
- Owner, 2026-11-14, on A-12: « Ok pour après la release »: the toc-after-readme-html bug (inbox toc-edit-toggle-clicks-lost-after-readme-html) does not block v1.9.1; it is taken after the release.
- published: v1.9.1 https://github.com/gsemet/markdown-okf-schema-studio/releases/tag/v1.9.1

## Cost

$7.04.
