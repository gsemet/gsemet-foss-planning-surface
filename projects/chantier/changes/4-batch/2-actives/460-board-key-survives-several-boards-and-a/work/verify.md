# verify CR-460

Head: 74055b1dff99b9a2c8792f551f7695d3f6998c7a

All claims judged at 74055b1.

1. Tests pass. `uv run --no-sync pytest .../tests/test_board_key_page.py test_board_exposure.py test_board_design.py -q` -> `97 passed in 11.71s`.
2. Live throwaway board (scratch repo, `serve --host 127.0.0.1 --port 0`, port 55050), `work/verifier/probe.py`, output `work/verifier/probe.log`:
   - no key, Accept text/html: `401 text/html; charset=utf-8`, CSP `default-src 'none'; script-src 'none'; style-src 'sha256-...'; form-action 'self'; base-uri 'none'; frame-ancestors 'none'`, no `<script`, `method="get"`, field `k`.
   - wrong `k=WRONG&p=x`: 401 page, the `wrong` line present (apostrophe HTML-escaped), hidden field `p` kept.
   - `Accept-Language: fr-FR`: French lines ("Ce board demande", "Ouvrir").
   - no `Accept: text/html` on `/`, `/api/board`, `/js/main.js`: `401 this board needs the link with its key: ask the Chief of Staff for it` (probe text unchanged).
   - whole link URL-encoded as `k`: `303`, `Set-Cookie: chantier_board_<id>=...; Max-Age=2592000; Path=/; HttpOnly; SameSite=Lax`, `Location: ./`; key with blanks: 303 + cookie.
   - `<script>` in k and in another query value: raw tag absent from the body (escaped).
   - `/x/y/index.html` with X-Forwarded-Host: form action `./index.html`.
3. Web client: `grep -rln "localStorage|sessionStorage|document.cookie" clients/web/js` -> only `api/griller.js`, `core/store.js`; `ui/key-notice.js` writes none. i18n keys `notice.key` (en.js, fr.js), `notice.key_field`, `notice.key_open` (en-board.js, fr-board.js, merged; declared in the PR). DESIGN.md has "The key notice" section (diff read).
4. Docs and cards diff present (server-api.md, web-board.md, chief-of-staff.md); scenario step 16d1b present (diff read; CI scenario green per Driver's note, not rerun here).
5. PR description (pr-body.md) read against the diff: Summary, Deliverables, Changes, Autonomous decisions (16d1b name, en-board.js), Known gaps (iOS Safari, no screenshot) match; no image; renders.
6. Review box: `chantier log 460`: "r1 approved at 53a134e6..., committed as 74055b1d" matches the box's `74055b1`.
7. Not run: the full scenario locally (told not to); step 16d1b judged by diff plus green CI.

Evidence: none captured (no screenshots asked; before/after not applicable beyond the above).

VERIFIED

## PR description pass at 74055b1dff99b9a2c8792f551f7695d3f6998c7a

Command: gh pr view 433 --json body; git diff --stat <base>...HEAD; grep of key_page.py, key.py, guard.py, run_scenario.py; `log 460` for the Review box.
- Audit 1-2, 6, 10: sections in order, fold in place, Blast radius graded 2, Known gaps present (iOS untested, no screenshot).
- Audit 3: CR, batch names only under Internal references.
- Audit 4-5: names exist (key_page.refusal, guard.pasted_key, guard.exchange, SameSite=Lax in key.py, CSP script-src 'none' / form-action 'self', step 16d1b); Changes match the 19-file diff.
- Review box: log note "r1 approved at 53a134e6 ... committed as 74055b1d" matches.
VERIFIED
