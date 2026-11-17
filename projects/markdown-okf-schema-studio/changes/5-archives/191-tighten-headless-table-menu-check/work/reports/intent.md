# Tighten the headless table menu position check to `relative` only

Type: test · Priority: P2 · Filed 2026-10-28 by the Foreman (Chief of Staff decision) · After
release 1.0.0 · Normal CI only.

## Problem

`test/visual/capture_edit_checks.py:1115` (headless) accepts a table menu `position` of `static` or
`relative`. Since PR #181 (table menu painted above the row and column handles) the product sets
`position: relative; z-index: 3` with no offset. Accepting `static` lets a regression back to the
old layout pass. The real-window check (`test/integration/realInput/editorWidgets.ts`, r06) was
already tightened in #181 (`eca17c42`): exactly `relative`, top/left/bottom/right `auto` or `0px`,
z-index `3`. The #181 reviewer recommended the same for this headless check.

## Expected

- Assert exactly `relative`, offsets `auto` or `0px`, z-index `3`, like r06.
- The check must fail on a `static` menu (prove it once by pointing it at the pre-#181 CSS).
- `@tests_req SwRS-MDOKFSTUDIO-TABLE-064` if the check carries markers.
