## Summary

The requirement for references to figures and tables without a caption says that a `{numref}`
role pointing at such a figure or table shows its number (`Figure 1`, `Table 1`), as Sphinx does.
An earlier review read that rule as contradicted by the code, and no test covered the `{numref}`
case. The code already numbers these references: the placeholder seen in that review came from a
`{numref}` to a heading label, which is a different, documented case. This PR adds the missing
test and corrects the requirement's verification notes and log, so the rule and its proof agree.

## Deliverables

What a `{numref}` and a `{ref}` to a captionless figure or table render, now checked by a unit
test (the figure is a `{figure}` with `:name: fig-empty` and no body, the table a `{table}` with
`:label: tbl-empty` and no title):

| Source | Rendered link | Covered by a test before this PR |
| --- | --- | --- |
| ``{ref}`fig-empty` `` | `<a href="#fig-empty">fig-empty</a>` | yes |
| ``{ref}`tbl-empty` `` | `<a href="#tbl-empty">tbl-empty</a>` | yes |
| ``{numref}`fig-empty` `` | `<a href="#fig-empty">Figure 1</a>` | no, now yes |
| ``{numref}`tbl-empty` `` | `<a href="#tbl-empty">Table 1</a>` | no, now yes |

A `{numref}` to a heading label still renders the inert placeholder its own requirement
documents; that case and its test are unchanged.

## Changes

- `test/core/render/mystFeatures.test.ts`: new test "a numref to a captionless figure or table
  shows its number" (hrefs, link texts, no empty link, no unresolved-role placeholder, no
  diagnostics); the existing captionless `{ref}` test now carries the requirement's test marker.
- `requirements/tiers/swrs/myst/SwRS-MDOKFSTUDIO-MYST-019.md`: the verification notes name both
  tests and no longer say the `{numref}` case is untested; normative text unchanged.
- `requirements/tiers/log.md`: a dated entry explaining that the reported contradiction was a
  `{numref}` to a heading label, and that the captionless case is now tested.

## Impacts

No visual change: the rendered output is the same before and after; only the test suite and the
requirement's notes change.

## Blast radius

- **1**: local and isolated; a plain `git revert` restores the previous behaviour.
- **2**: several features or shared code; revert is possible but needs checks or follow-ups.
- **3**: wide impact (data, formats, CI, release, public API); rollback is complex or partial.

Grade: 1. Test and requirement-text changes only; no shipped code changes, a revert removes the
test and the notes.

## Autonomous decisions

- No code change: the new test passed on a fresh build of the unchanged renderer, so the
  renderer already does what the requirement says; the test was shown failing once against a
  placeholder expectation to prove it can fail.

## Known gaps

None.

## Human decisions

- The requirement is right: a `{numref}` to a captionless figure or table shows its number
  (`Figure 1`, `Table 1`), as Sphinx does; the missing test is added.

## Test plan

- [x] New or changed tests: the new test passes on the unchanged renderer; it failed when its
      expected texts were temporarily set to the unresolved-role placeholder (the renderer already
      numbered these references, so no earlier code fails it)
- [x] Requirements: SwRS verification notes updated, test marker added, `just requirements-update`
      (no generated file changed)
- [x] Changelog: No user-facing change
- [x] Local gates: `just check` and `just preflight` (Windows: static stage) pass on this patch
      after the restack (a `requirements/tiers/log.md` conflict resolved), carried to `2bea4c6` by
      a clean rebase with the patch unchanged
- [x] Review: the restack's `requirements/tiers/log.md` resolution approved on this patch, carried
      to `2bea4c6`
- [x] Verified at `2bea4c6`
- [x] CI green at `2bea4c6` (`gh pr checks 437`): `checks`, `report`, `static`, `static-windows`
      and `visual` pass; the push-only jobs skip on a pull request

## Internal references

- CR-430 numref-captionless (found while checking requirements in PR #419).

🤖 Generated with [Claude Code](https://claude.com/claude-code)
