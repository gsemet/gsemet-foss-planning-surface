## Summary

Web board Dashboard page (Productivity and Spending tabs) over the closed batch records. Figures are computed on the server (`board/dashboard_page.py`) and served by the read-only op `dashboard.get`; charts are drawn by the web client (new `chart` component, no library). CR-448.

Work in progress: round 1 is the server side (figures, op, protocol, tests); the client follows.

## Review

- [ ] Inspector approved

## Known gaps

- Client page not yet in this round.
- No screenshots yet.
