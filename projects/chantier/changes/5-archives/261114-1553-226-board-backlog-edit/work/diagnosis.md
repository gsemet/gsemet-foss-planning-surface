# CR-226 CI diagnosis: `just scenario (ubuntu-latest)`

All four failures are scenario-step errors in `scenario/run_scenario.py`. No product bug found
(`guard.py`, `write_api.py`, `lifecycle/backlog.py`, `board/files.py` behave as designed).

## 1. "`PUT` with the good key answers 405 and no cookie" (line ~1326)

Cause: `guard.exchange` now lets a good-key `PUT` (like `POST`) carry on (`WRITE = ("POST","PUT")`);
a write then needs the cookie or the header, and `/?k=<key>` gives neither, so 401.
Proof (scratch, `guard.exchange` / `guard.authorised` called with `k` = the key):
`PUT exchange-> None authorised False` (so the route answers 401); `DELETE exchange-> 405`.

Fix (step 2 of `remote_board`): keep the 405 test with a method the board does not know, and
add the PUT expectation:

    code, head, _ = fetch(port, f"/?k={link.key}", "DELETE")
    check("`DELETE` with the good key answers 405 and no cookie",
          code == 405 and "set-cookie" not in head, f"{code} {head}")
    code, head, _ = fetch(port, f"/?k={link.key}", "PUT")
    check("`PUT` with only `?k` answers 401 (a write needs the cookie or the header) and no cookie",
          code == 401 and "set-cookie" not in head, f"{code} {head}")

(The `PUT /?k=wrong` -> 401 step and line ~1446 `PUT /api/board` -> 405 with cookie stay.)

## 2, 3, 4. `backlog/new` byte check, `GET file` SHA, `PUT backlog/file` "none.md is not a file"

One cause. `file_idea` -> `new_request` (`lifecycle/filing.py`) writes the request to
`<slug>/intake/request.md`, not `<slug>/*.md`. The scenario does `filed.glob("*.md")` (not
recursive) in line ~1185, finds nothing, falls back to `filed / "none.md"`:
- (2) `request.is_file()` False although the answer is 200 and `ok` (the CI body shows the folder was filed);
- (3) `request.read_bytes()` / `relative_to` give `none.md`: GET 404, no SHA header, `sha == ""`;
- (4) PUT sends `path: "none.md"`, `_editable` answers 400 "none.md is not a file of board-filed-idea",
  then `request.read_bytes()` raises FileNotFoundError (the final "scenario ran to the end" failure).

Proof: in a scratch git repo, `chantier file Board-filed-idea` then listing gives
`.agents/changes/1-inbox/board-filed-idea/intake/request.md` (and nothing else).

Fix (line ~1185): replace

    request = next(iter(filed.glob("*.md")), filed / "none.md") if filed.is_dir() else filed

with

    request = filed / "intake" / "request.md"

Everything after follows: `rel` = `1-inbox/board-filed-idea/intake/request.md` for `GET file`;
the edit's `path` = `intake/request.md` (`request.relative_to(filed)`), accepted by `_editable`
(`.md`, not STATUS.md, no `..`, a file inside the folder). Expected values are consistent with
the code: the body was CRLF-majority so `_with_endings` keeps CRLF
(`b"Board filed idea\r\n\r\nedited\r\n"`), `_file` returns the new `sha256`.

## Not run
The full `just scenario` (about 6 minutes, GitHub forge) was not rerun: the changes are to
the scenario file, which this role does not edit. The coder should rerun `just scenario`.
Side note: Windows PowerShell shows "â†’" for the arrows of `write_api._moved` only because of
console decoding; the file is UTF-8 (CI move checks passed).
