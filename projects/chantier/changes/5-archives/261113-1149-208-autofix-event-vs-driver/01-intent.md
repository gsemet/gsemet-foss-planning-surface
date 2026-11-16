# Claude Desktop's Auto-fix events are left to the CR's Driver; the heartbeat's prompt names no interval

## The request

Three findings, all about `skills/chantier/references/hosts/claude-code.md`:

1. Batch-14's retro: Claude Desktop's Auto-fix event on a CR's PR asked the steering session to
   fix the PR and to merge the base branch in, while the CR's own Driver was fixing it. The
   request: the host reference says an Auto-fix event on a CR with a live Driver is left to that
   Driver, and the project's rebase rule ranks above Auto-fix's merge rule.
2. Real-direct run 1 (2026-11-12, PR 137; `evals/results/real-direct-2026-11-12-run1.md`): the
   app attached the five sandbox PRs the Drivers opened to the steering session, so Auto-fix
   watched them and asked to merge `main` into PRs #2 and #5 while their Drivers were rebasing.
   The host reference could also say how the user turns Auto-fix off for an eval.
3. Same run: the heartbeat's prompt ended in "every 30m", which the `/loop` skill reads as a
   fixed cron interval, while the host card wants each wake scheduled with `ScheduleWakeup`.
   The heartbeat's prompt should not end in "every 30m".

## The problem

- Auto-fix is a feature of the app, not of chantier. The app binds a PR opened by a subagent to
  the session that started it, and then sends that session events ("fix the CI", "merge the base
  in"). The host reference knows the feature only as an allow rule
  (`mcp__ccd_pr__set_monitor`, "No chantier card uses it"): it says nothing of an event that
  arrives.
- An event that is acted on breaks three rules at once: the Foreman never codes, rebases or
  pushes (`foreman.md`); one CR has one Driver, and two writers on one branch race; the project's
  method is a rebase (`concepts.md` rule 8, the project's own rules), and Auto-fix asks for a
  merge commit.
- Even ignored, each event starts a turn of the steering session, which the user pays for.
- The heartbeat section says "runs the `/loop` skill in dynamic mode with `chantier status
  --refresh …`, every `30m`, each wake scheduled with `ScheduleWakeup`". Read literally, the
  agent puts "every 30m" in the loop's prompt, and `/loop` then takes its fixed-interval mode:
  the sentence gives two contradictory orders.

## What would fix it

1. A short section in `hosts/claude-code.md`: what an Auto-fix event is, that the steering
   session never acts on one, that a CR with a live Driver is that Driver's, what happens for a
   CR with no live Driver, and that the project's rules and the cards rank above what the event
   asks (a rebase, never the base merged in).
2. The same section says how the user turns Auto-fix off, and `evals/README.md` asks for it
   before a real campaign.
3. The heartbeat section is reworded so the loop's prompt holds the command only, and the 30
   minutes are the delay of each scheduled wake.

## Out of scope

- chantier arming, disarming or unbinding the app's PR monitor itself: chantier never writes the
  user's settings.
- `hosts/copilot.md`: Copilot has no Auto-fix and its heartbeat is another mechanism.
- How a Driver learns of its own red CI (the backlog item `driver-ci-from-pr-checks`).
- The agent files, the CLI and the mod.
