# Board key: several boards in one browser, a paste field, SameSite=Lax

Change Specification, written 2026-11-22 from `intake/request.md` and the Chief of Staff's brief
(the user's words of 2026-11-22: "C'est possible que j'ai plusieurs board ouvert sur la même surface
ou sur d'autres. Il faut que ca marche", and "Met le à la fin de ce batch"). No `01-intent.md` or
`02-answers.md`: the brief's three points are the decisions. No issue. Batch-30, its last CR, after
CR-447 (docs gardening); it builds on CR-456 (PR #430, `serve`, `webui`, the per-server cookie
`chantier_board_<id>` of `board/key.cookie_name`, the free port when another surface's board holds
the default) and on CR-457 (two keys, the read key's cookie `chantier_board_<id>_read`), both
landed before it; CR-458 (`remote-cli-commands-through-the-surface-`, part C of the A→B→C stack)
also sits below it, and this CR changes nothing it reads (the keys, the access header, the
exchange's `303`). One Driver, at most 3 rounds. It touches the CLI's `src/` (the board server), the
web client, the cards, the docs and the scenario: `just check` and `just eval-dry-run` before the
first push, `just scenario (ubuntu-latest)` green before the PR. No change under `hooks/` or
`types/`; no change to what the CR board pane draws.

## Goal

The user may have several boards open at once, of one surface or of several, in one browser, on a
laptop or an iPhone: each keeps working across reloads, across the restarts of the others, and with
several tabs of one board. When a browser holds no cookie for a board (a home-screen web app, a
private tab, an in-app browser, a cleared jar), the page lets the user paste the key or the whole
link and goes on, instead of a dead end that sends them back to the Chief of Staff.

## Decisions carried (the brief)

1. Prove, in tests and the scenario, one cookie jar with two or three servers of different
   surfaces on one host (different ports) and several tabs of one server: each keeps working
   across reloads and across restarts of the others.
2. The refusal page: when neither a cookie nor the header carries a good key (either key, CR-457),
   the web page offers a field to paste the key or the whole link, then gets the cookie through the
   existing `?k=` exchange. No key is ever stored in `localStorage` or `sessionStorage`.
3. iOS Safari and `SameSite=Strict`: decided from evidence below: the cookie moves to
   `SameSite=Lax`; writes stay guarded by `guard.refusal` and `auth.own_origin`.
4. The web client's `DESIGN.md` stays true; AGENTS.md's rules apply.

## Why the iOS refresh failed, and the decision on `SameSite`

Evidence, each labelled:

- **Documented** (RFC 6265bis, the `SameSite` attribute; MDN, "Set-Cookie: SameSite"): a `Strict`
  cookie is withheld from every request that is cross-site, a top-level navigation from another
  site included (a link in a webmail, a chat's web page, a GitHub PR, a terminal's link handed to a
  browser through a web page). A `Lax` cookie is also sent on a cross-site top-level navigation
  with a safe method (`GET`, `HEAD`), and withheld from every cross-site subresource request
  (`fetch`, XHR, a WebSocket handshake, an `<img>`) and every cross-site `POST`.
- **Documented**: browsers judge a redirect after a cross-site navigation as cross-site too. The
  board's exchange is such a redirect: `/?k=<key>` answers `303` with the cookie, and the browser
  follows to `./`. Under `Strict`, when the link was opened from another site, the cookie the `303`
  just set is not sent on the follow-up `GET`, and that page answers 401 "this board needs the link
  with its key". Under `Lax` it is sent.
- **Documented**: on iOS, a web app added to the Home Screen keeps its own cookie storage apart from
  Safari's, and the address it saves is the one shown at that moment: after the exchange's `303`,
  the address with no `k`. Its jar then holds no cookie for the board at a later launch, whatever
  `SameSite` says. Only a way to give the key on the page itself mends that (decision 2).
- **Known** (CR-456's intake): every board used one cookie name, `chantier_board`, and cookies do
  not tell ports apart: a second board on the same host overwrote the first's. CR-456 fixed it with
  the per-server name.
- **Not tested**: whether iOS Safari sends a `Strict` cookie on a link opened from another app (no
  initiating page). The specifications treat a navigation with no initiator as same-site; WebKit's
  handling of a link from another app is not exercised here. `Lax` sends the cookie in either case,
  so the decision does not hang on it.

The decision: `key.set_cookie` writes `SameSite=Lax` (both cookies, the private one and CR-457's
`_read` one), `HttpOnly`, `Path=/`, `Max-Age` 30 days, as today otherwise.

Why `Lax` is safe here. What `Lax` adds over `Strict` is the cookie on a cross-site top-level
`GET` or `HEAD`, and nothing else:

- The board's `GET`s change nothing: the frame's routes (`routes._frame`) serve the page and its
  files and the probe; every op that writes goes through `POST` (`POST api/v1/call/<op>`, the
  WebSocket, the legacy `POST`/`PUT` routes).
- On `/api/v1/` (HTTP and the WebSocket's upgrade), `auth.source_of` counts a cookie only when
  `auth.own_origin` holds (`Sec-Fetch-Site` absent or `same-origin`, `Origin` absent or the
  board's own). A cross-site navigation to an API address is refused 401, with the cookie present,
  where the browser sends `Sec-Fetch-Site` (`cross-site`); a browser that sends none (Safari
  before 16.4), on a navigation `GET` that sends no `Origin`, passes `own_origin`: that `GET` only
  reads, and its answer is shown to the user alone, in the user's own tab, never to the other site
  (same-origin policy, below). Unchanged.
- A write from another site: `Lax` withholds the cookie from a cross-site `POST` and from a
  cross-site WebSocket handshake; `guard.refusal` (the frame's writes) and `auth.own_origin` (the
  API) refuse it again on `Sec-Fetch-Site` and `Origin`. Unchanged, two locks.
- A read from another site: a page that navigates the top level to the board cannot read the
  answer (same-origin policy); `frame-ancestors 'none'` keeps it out of a frame; the API's CORS
  never allows credentials. The `?k=` exchange sets a cookie only for a good key, which another
  site does not have, so it cannot plant its own.
- Chrome's two-minute "Lax+POST" allowance applies only to a cookie with no `SameSite` attribute;
  this cookie names `Lax`, so it does not apply.

## What changes

### 1. The server's refusal page (`board/key_page.py`, new; `board/routes.py`, `board/guard.py`)

- `routes._frame` and `guard.exchange` answer a request that has no good key with
  `key_page.refusal(req, wrong)` instead of `text(401, guard.NEEDS_KEY)` when the request is a page
  load: method `GET` or `HEAD`, a path not under `/api/`, and an `Accept` header that names
  `text/html`. Every other request keeps today's `401` text `this board needs the link with its
  key: ask the Chief of Staff for it` (`guard.NEEDS_KEY`, unchanged): the probe
  (`address._says_needs_key` reads it, an older build's probe too), `/api/board`, `/api/v1/`, the
  WebSocket's denial, a static file fetched by a script.
- The page: status `401`, `text/html; charset=utf-8`, the board's `SECURITY` headers and
  `Cache-Control: no-store` (as every reply), and its own `Content-Security-Policy`:
  `default-src 'none'; script-src 'none'; style-src 'sha256-<hash of its one inline style>';
  form-action 'self'; base-uri 'none'; frame-ancestors 'none'` (the hash computed at import from
  the module's style constant; the reply's own header replaces `reply.HTML_POLICY`, as
  `Reply.all_headers` lets a route's header win). No script at all.
- Its content: the title "chantier board"; the line "This board needs the link with its key."; a
  `<form method="get">` whose action is relative, built as `guard.exchange` builds its `Location`
  (`"./" + quote(req.path.rsplit("/", 1)[-1], safe="")`), so a proxy's path prefix is kept
  (`docs/server-api.md`, "Behind a proxy"), with one text field named `k`
  (`autocomplete="off"`, `autocapitalize="off"`, `spellcheck="false"`, a label "Paste the key or
  the whole link"), the request's other query parameters but `k` as hidden fields (so the `303`
  lands on the same page, `?p=`, `?v=`, `transport=http` kept), and a button "Open"; then the line
  "The Chief of Staff gives the link (chantier webui prints it). Nothing is kept but the board's
  cookie." When the request carried a `k` that is not a good key (`wrong`), a line above the form:
  "That key is not this board's: a link of another board opens that board, not this one." The
  words in French when the first language of `Accept-Language` is `fr` ("Ce board demande le lien
  avec sa clé.", "Colle la clé ou le lien entier", "Ouvrir", "Le Chief of Staff donne le lien
  (chantier webui l'affiche). Rien n'est gardé que le cookie du board.", "Cette clé n'est pas celle
  de ce board : le lien d'un autre board ouvre cet autre board, pas celui-ci."), else in English;
  both sets are constants of the module. Every value it repeats from the request (the path, the
  hidden fields) is HTML-escaped. A `viewport` meta so it reads on a phone.
- The pasted text, in the exchange (`guard.exchange`, one helper `guard.pasted_key(raw)`), which
  accepts every link form `commands/live.from_link` accepts (an `http(s)` link with a host, any
  path prefix, `k` among other parameters), read the same way (`urlsplit`, then `parse_qs`'s
  first `k`; one shared reader when the Driver can share it without `from_link`'s refusals), and
  never raises: the
  value of `k`, stripped of blanks; when it holds `k=` (a key never does: `secrets.token_urlsafe`
  uses only letters, digits, `-` and `_`), it is read as a link or a query
  (`urllib.parse.urlsplit`, then `parse_qs`; a text starting `?` or `k=` too) and its `k` is the
  candidate; a link with no `k` gives an empty candidate (refused). The candidate is then judged as
  CR-457's exchange judges `k`: the private key sets `chantier_board_<id>`, the read key sets
  `chantier_board_<id>_read`, anything else is refused (the HTML page with the `wrong` line on a
  page load, today's text otherwise), and a good one answers `303` to the same address without `k`
  as today. The printed links (`?k=<key>`) take the same path unchanged.
- The page is the server's, not the web client's (no file under `clients/web/`), so it shows with
  `--ui none` and with `--ui <folder>` too.

### 2. The web client's key notice (`clients/web/`)

Read `clients/web/DESIGN.md` first and keep it true.

- When the server refuses the page's key after the page loaded (`state.denied`: a WebSocket closed
  4401, an HTTP 401, `--new-key` while the page is open, the cookie expired or cleared), the
  header's notice (`ui/header.js` `notice`, drawn by `main.js` `drawNotice`, which paints markup
  in place of plain text) holds the line, a text field and an "Open" button, in place of the line
  alone. "Open" (or Enter) builds the page's own address (`new URL(location.href)`) with
  `searchParams.set('k', <the field's text>)` and navigates to it (`location.assign`): the server's
  exchange (section 1) reads a key or a whole link, sets the cookie and answers `303` to the same
  page with no `k`. The text goes into no variable that outlives the click, no store field, no
  `localStorage`, no `sessionStorage`, no cookie written by script (the cookie is `HttpOnly`).
- The words, through i18n keys in `js/i18n/en.js` and `fr.js`: `notice.key` becomes "This board
  needs the link with its key: paste it here, or ask the Chief of Staff for it." / "Ce board demande
  le lien avec sa clé : colle-le ici, ou demande-le au Chief of Staff."; new `notice.key_field`
  ("The key or the whole link" / "La clé ou le lien entier") and `notice.key_open` ("Open" /
  "Ouvrir"). Another tab of the same board that is also denied recovers at its next reload, the
  cookie being the browser's.
- Styling in `css/shell.css` beside `.notice`, tokens only (no new token, no literal, no side
  accent): the field and the button are the existing form controls' look.
- `DESIGN.md` gains a short section "The key notice": the notice's field and button, the
  navigation to the page's own address with `k`, that the text is never kept (no store field, no
  web storage), that the server's own refusal page (before any page loads) belongs to the server
  (`board/key_page.py`), not to the client, and that other tabs recover at their reload.

### 3. The cookie

- `board/key.set_cookie`: `SameSite=Lax` in place of `SameSite=Strict`; nothing else changes
  (name per CR-456 and CR-457, `Max-Age` 30 days, `Path=/`, `HttpOnly`). Its docstring says why
  (the section above, in two lines: a link from another site or app, followed by the exchange's
  `303`; writes guarded by `Sec-Fetch-Site`/`Origin` and `POST`).

### 4. Docs and cards

- `docs/server-api.md`, its key section (section 7): the cookie is `SameSite=Lax`, with the safety
  line (cross-site `GET` only, reads only, the API counts the cookie from the own origin only);
  a page load with no good key gets the HTML refusal page with its field, every other request the
  `401` text.
- `docs/web-board.md`, "The link": a browser with no cookie for the board (a home-screen web app on
  iOS, a private tab, an app's built-in browser, a cleared jar) shows a field: paste the key or the
  whole link there; several boards, of one surface or several, work side by side in one browser,
  each with its own cookie; the cookie is kept for 30 days, `SameSite=Lax`.
- `chief-of-staff.md`, the row "board on my phone", "where is the board?": "a page that lost its
  cookie (a home-screen app, a private tab) asks for the link on the page: the user pastes the link
  there".
- AGENTS.md: unchanged (the key still reaches the server in the page's URL; no new tool, no new
  write).

## Out of scope

- A server that restarts on another free port (its default held by another surface's board): its
  own open tabs point at the old port and stop; the cookie still holds (it ignores the port), so the
  new link, or the new port typed with no key, opens it at once. Keeping a server's last free port
  across its own restarts is a separate item (offered to the inbox).
- A read-only mode of the page (CR-457's out of scope).
- Any change to the keys, the exchange's `303`, the WebSocket's `hello`, the CORS rules.

## Evidence

- Tests, in-process (`tests/test_board_exposure.py`, or a new `tests/test_board_key_page.py`),
  parametrized:
  - `guard.pasted_key`: a bare key, a key with blanks around, `http://127.0.0.1:8765/?k=<key>`, a
    link with other parameters before and after `k`, `?k=<key>`, `k=<key>`, a link with no `k`
    (empty), a URL-encoded link as the outer `k`'s value; and the exchange of each against a
    prepared server state: the private key sets only `chantier_board_<id>`, the read key only
    `chantier_board_<id>_read`, both with `SameSite=Lax`, a `303` with a relative `Location` and
    no `k`.
  - The refusal page: `GET /` with `Accept: text/html` and no cookie answers 401 HTML holding the
    form (`method="get"`, a field named `k`), the CSP with `script-src 'none'` and `form-action
    'self'` and a `style-src` hash that matches the shipped style constant (computed from the
    module, not copied); no `<script` in the body; `Accept-Language: fr` gives the French lines; a
    query `?p=x&v=batch` gives hidden fields `p` and `v`; a query value `<script>` comes back
    escaped; a request whose path sits under a proxy's prefix (`/pre/fix/index.html`, with
    `X-Forwarded-Host`) gets a relative form action (`./index.html`), never an absolute path; a wrong `k` on a page load gives the `wrong` line; the same requests with no
    `Accept: text/html` (the probe, `/api/board`, `/api/v1/...`, `/js/main.js`) answer the `401`
    text holding `guard.NEEDS_KEY`, so `address.probe` still answers `another-key` for a board of
    another key.
  - `key.set_cookie` holds `SameSite=Lax` and no `Strict` (read from the shipped function): the
    line that flips is `tests/test_board_exposure.py:123`
    (`test_the_cookie_lasts_30_days_and_the_exchange_sets_it`, today `"SameSite=Strict" in
    cookie`).
  - `guard.pasted_key` accepts each link `commands/live.from_link`'s tests accept (parametrized
    over the same links).
  - The web client, read from the repository as it ships (`clients/web/js/**/*.js`): `localStorage`
    and `sessionStorage` appear only in `core/store.js` and `api/griller.js` (today's two uses); the
    module holding the key field writes neither and sets no `document.cookie`; `notice.key`,
    `notice.key_field` and `notice.key_open` exist in `en.js` and `fr.js`; `DESIGN.md` names "The
    key notice". `test_board_design.py` still passes on `css/shell.css`. A prepared JS text calling
    `localStorage.setItem` in another file proves the check finds it.
- Scenario (`scenario/run_scenario.py`, beside `serve_and_webui`, a step "16d2. Several boards in
  one browser"), with one `urllib` opener over one `http.cookiejar.CookieJar` (it keeps cookies per
  host, not per port, as a browser does), no `X-Chantier-Board-Key` header anywhere:
  - Three `SurfaceWorld`s, each built and `init`ed, their servers started on 127.0.0.1 (the first on
    the default port when free, the others taking free ports, or each on an explicit free port when
    the default is held by another program here, as `serve_and_webui` says it).
  - Opening each server's printed link: the `303`, read through an opener without a redirect
    handler sharing the same jar, whose `Set-Cookie` header holds `SameSite=Lax` (the attribute is
    checked on the header, the jar keeping no `SameSite`); the jar then holds three distinct
    `chantier_board_<id>` cookies for 127.0.0.1.
  - A reload of each (`GET /` through the opener) answers 200 with the page; `/api/board` through
    the opener answers 200 from each (the jar's cookie, from the own origin).
  - Two tabs of the first server: two WebSocket connections carrying the jar's `Cookie` header and
    the own `Origin` are both welcomed; one is closed and the other still answers a `call` of
    `board.get`.
  - The second server is stopped and started again (same surface, so same key and cookie name):
    the first and third still answer 200 through the jar during and after; the second answers 200
    through the jar at its new start, on whatever port it took, with no new link.
  - With CR-457: the first server's read-only link opened through the same jar adds
    `chantier_board_<id>_read`; the first server's answers still carry `X-Chantier-Access: write`;
    the third's are unchanged.
  - A fresh jar (a home-screen app's, a private tab's): `GET /` with `Accept: text/html` answers
    401 with the form; submitting it as a browser would (`GET /?k=<the whole printed link,
    URL-encoded>`) answers `303` and sets the cookie; the reload answers 200.
  - The existing check at 16d, `scenario/run_scenario.py:3307-3310` (`/?k=<key>` answers 303 with
    "HttpOnly, SameSite=Strict"), flips to `SameSite=Lax`.
- Browser evidence, labelled: the cookie jar of Python's standard library: exercised (scenario);
  `SameSite` handling by a real browser (Chromium, Firefox, iOS Safari): documented, not tested;
  iOS Safari's handling of a link opened from another app: not tested. The PR's Known gaps names
  "not checked on iOS Safari", so the Chief of Staff asks the user to open a board from another app
  on the phone, then a home-screen launch with the paste field, after the merge.

Host and default matrix: none; nothing here depends on Claude Code or Copilot, or on a configured
value.

## Open questions

None.
