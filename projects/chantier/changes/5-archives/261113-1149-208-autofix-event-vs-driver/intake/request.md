batch-14 retro: Claude Desktop's Auto-fix event on a CR's PR asked the steering session to fix it and merge the base branch in, while the CR's own Driver was fixing it. Fix: hosts/claude-code.md says an Auto-fix event on a CR with a live Driver is left to that Driver, and the project's rebase rule ranks above Auto-fix's merge rule.

Also seen in real-direct run 1 (2026-11-12, PR 137): the app attached the 5 sandbox PRs the Drivers opened to the steering session, so Auto-fix watched them and asked to merge main into PRs #2 and #5 while their Drivers were rebasing. The host reference could also say how the user turns Auto-fix off for an eval.

Also (real-direct run 1): the heartbeat's prompt ended in "every 30m", which the /loop skill reads as a fixed cron interval while the host card wants ScheduleWakeup: the heartbeat's prompt should not end in "every 30m".
