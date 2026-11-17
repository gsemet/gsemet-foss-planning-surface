# Change Specification: the board's Configuration page writes the project file with LF

## Goal

The web board's Configuration page (CR-301, PR 256) writes the planning surface's project file
UTF-8 with LF line endings, as CR-301's specification says, also when the existing file has CRLF
line endings. Today `skills/chantier/scripts/cli/src/chantier/playbook/edit_text.py` (lines 94-95)
turns the written text back to CRLF when the existing file is mostly CRLF.

## Behaviour

- A save from the Configuration page writes the project file (the existing one, else a new
  `chantier.yaml`) with LF only, whatever line endings the file had; its content other than the
  edited keys is kept as CR-301 says (comments, order), only its line endings change.
- Any other write that goes through `edit_text.py` keeps its current behaviour, unless the Driver
  finds that the Configuration page is its only caller; then the CRLF branch goes, with its test.
  The Driver says which in the PR.
- The stale-hash check (409) still compares what the page read with what is on disk: a file whose
  only change is the save's own LF conversion is not reported as changed by someone else on the
  next save.

## Evidence

- A test that saves through the page's write path onto a CRLF project file and reads LF only
  (no `\r\n` in the bytes), with the edited key changed and a comment kept.
- `just check` passes; the pipeline job `just scenario (ubuntu-latest)` is green at the PR's head
  (the change is to the CLI).

## Out of scope

- Any other file the board edits (the backlog's Markdown files).
- The phone screenshot's cut "Starts as" column and the PC screenshot's 15-model list (CR-301's
  other known gaps).
