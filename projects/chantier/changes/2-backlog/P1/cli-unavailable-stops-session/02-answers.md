# Answers

- The user (2026-11-18): "Oui, spécifie les P1", after the standing word of the day "plus de question" (no more questions): no grill; the behaviour choices below are the Chief of Staff's.

## Settled by the Chief of Staff

- **The rule.** One rule in the startup core of every role (Chief of Staff, Griller, router, Foreman, Driver, every worker): if `` cannot run, in the dev mode or the plugin mode, at the start or at any later call (a fetch refused, a sandbox with no network, a cloud session, a crash on start), the session reports the exact error and stops. It does no work as that role, takes no seat, writes nothing in the planning folder, and never goes on "without it".
- **Who it reaches.** A steering session tells the user; an agent started by another (a Driver, a worker) ends its turn with the error as its reply to its parent, which then applies the same rule to itself only if its own `` fails.
- **The exception lines.** The "a tool a role lacks is not a stop: work without it" lines name the CLI as excluded, explicitly.
- **No retry loop, no repair.** No upgrade, reinstall, substitute launch or alternative route, as the dev mode's `uv sync` rule already says; one plain retry of the same command is allowed only when the error itself is a transient network error, then the stop.
- Spec critic: yes, it changes every role's startup contract.
