# Commands name a paused batch and the way out

`chantier cost --explain` and `cost --by cr` refuse on a paused batch with "no running batch: run `chantier open` first; no batch closed yet" (both runs): the message sends the user to open a new batch, while `--batch <n>` was all that was missing. Pick the only paused batch when there is one, or name it and `--batch` in the refusal.

Same family: `chantier board` failed in run 2 with a bare `[WinError 10048]` (port in use, an earlier board still running): the refusal names the port, that a board may already run, and the way out (its URL, or `--port`) where one exists.

Source: the study of batch-18's two real eval runs of 2026-11-15 (real-foreman run 2, stack, Foreman on Sonnet 5.5; real-direct run 3, parallel, direct mode on Opus 5.5), judged by the retro-critic. Audits: C:/Users/gaeta/Projets/chantier-eval/real-foreman-2026-11-15.audit.md and real-direct-2026-11-15.audit.md. Retro-critic: before release.
