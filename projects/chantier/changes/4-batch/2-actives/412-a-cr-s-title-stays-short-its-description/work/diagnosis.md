# Diagnosis: surface-board, 3 red checks at cdec7de (CR-412)

## Reproduction
From the worktree, `skills/chantier/scripts/cli/src`:
`uv run --no-sync --project <worktree> python -I -c "from chantier.lifecycle.backlog import titled_request; ..."`
- `titled_request("Board filed idea\r\n\r\nbody é\r\n", <bytes>)` -> ChantierError "the request has no short title (its title is 16 characters; the limit is 72) ..." (EXIT_USAGE)
- `titled_request("Board filed idea", <bytes>)` -> ('board-filed-idea', b'# Board filed idea\n')
(Not the full unit; the probe calls the changed function directly. Scenario code: scenario/run_scenario.py lines 1529-1551.)

## Cause
New rule in `lifecycle/backlog.py::titled_request` (used by `write_api._new`): a request with no `title` is accepted as received only if it has a `#` heading of <= 72 chars; a single short line becomes its own heading; anything else (here: several lines, no `#` heading) is refused with 400.
The scenario posts `"Board filed idea\r\n\r\nbody é\r\n"`: three lines, no `# ` heading. So:
1. Check 1 (`POST backlog/new` byte for byte): the POST is refused, nothing is filed, so code != 200 and no request.md.
2. Check 2 (second idea, same slug refused 409): nothing exists, so `POST {"text":"Board filed idea"}` is now FILED (200, as `# Board filed idea\n`) instead of 409. Cascade of 1.
3. Check 3 (`PUT backlog/file` keeps CRLF): request.md is now the LF file `# Board filed idea\n` from step 2 (the sha is read from it), so the PUT writes LF, not CRLF, and the bytes differ from `b"Board filed idea\r\n\r\nedited\r\n"`. Cascade of 1 and 2.
Only the idea text is the root cause; the later PUT/stale/refusal checks still pass.

## Place to fix
The scenario, not the code: the new rule is the CR's intended behaviour (spec: title at most 72). Give the posted text a short heading, e.g. `"# Board filed idea\r\n\r\nbody é\r\n"` (slug stays `board-filed-idea` via idea_slug of the text? check: slug comes from the text, so verify it stays `board-filed-idea`; else pass `"slug"`), and adjust the PUT expectation to the CRLF bytes of that heading (`b"# Board filed idea\r\n\r\nedited\r\n"` with edit text `"# Board filed idea\n\nedited\n"`), and the second-idea POST to the same heading text. Alternatively post a `title` field plus the body, which also exercises the new path (then the file is `# Board filed idea\n\n` + raw, LF heading before CRLF body: CRLF preservation of the PUT would then depend on mixed endings, so the `# heading` route is simpler).

## Side finding (code, minor)
The refusal message for a multi-line text without heading says "its title is 16 characters; the limit is 72", which reads as within the limit and misleads. Worth rewording (e.g. "the request has no heading"), in `titled_request`.
