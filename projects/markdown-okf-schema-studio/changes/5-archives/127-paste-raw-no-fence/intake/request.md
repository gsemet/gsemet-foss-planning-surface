# 127 — Pasting a large document inserts the raw text, never a fence around it

Type: fix · Priority: P1 · From backlog: `02-backlog/P1/bug-paste-wrapped-in-fence`

## Intent (user)

See [01-intent.md](../01-intent.md) (moved from the backlog, verbatim).

## Autonomous decisions

- Decided by the main session on 2026-10-27 under the user's instruction "lance 4 CR max en parallèle pour fixer tout ça et finaliser une nouvelle stack PR" (same autonomous mode as the previous run). List these in the PR body under "Autonomous decisions".
- Find the paste path that adds the ```` fence and remove that behaviour for text/plain and Markdown pastes; rich HTML paste conversion (existing feature) is left alone unless it is the cause.
- Reproduce first with a large document containing fenced code blocks; the e2e fails on the current code.
- Driver 2026-10-27: reviewer r1 approved without screenshots (assertion-level e2e); requirements-lint failure (okfreq --check-links) is pre-existing on main. Coder noted WINDOW-TESTS.lock vanished before release (possibly removed by another CR).
