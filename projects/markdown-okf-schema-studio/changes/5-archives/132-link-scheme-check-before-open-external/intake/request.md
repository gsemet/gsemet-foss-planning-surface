# 132 — Only http, https and mailto links are opened outside VS Code

Type: fix · Priority: P1 · From backlog: `02-backlog/P1/security-link-scheme-open-external`

## Intent (user)

See [01-intent.md](../01-intent.md) (moved from the backlog, verbatim).

## Autonomous decisions

- Decided by the main session on 2026-10-27 under the user's instruction "pars sur les nouveaux P1/P2" (same autonomous mode as the previous runs). List these in the PR body under "Autonomous decisions".
- Follow the item's expected behaviour. A link refused by the check is rendered as an unsupported link (no click action) with a tooltip naming the reason.
- Security fix: the PR body describes the class of link refused without a ready-to-use exploit path.
