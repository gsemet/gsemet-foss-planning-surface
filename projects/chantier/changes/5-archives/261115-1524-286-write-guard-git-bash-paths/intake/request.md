# The write guard reads Git Bash paths

On Windows the plugin's write guard (hooks) refused a write to `/c/Users/...` inside the allowed folder: it does not map a Git Bash drive path to `C:/...`. One wasted call in the eval, but every `/c/` path is refused. Map the drive form before the check. A change to hooks/ passes `just mod`.

Source: the study of batch-18's two real eval runs of 2026-11-15 (real-foreman run 2, stack, Foreman on Sonnet 5.5; real-direct run 3, parallel, direct mode on Opus 5.5), judged by the retro-critic. Audits: C:/Users/gaeta/Projets/chantier-eval/real-foreman-2026-11-15.audit.md and real-direct-2026-11-15.audit.md. Retro-critic: later.
