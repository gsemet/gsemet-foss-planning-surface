# The eval audit gives no false FAIL

Every FAIL of both runs' audits was false:
- J1 (run 1): the retro-critic's prompt was right, but the regex wants "for CR-<n>" or "the stack" after the role; the Chief of Staff and Foreman forms ("for the Chief of Staff") must pass.
- J14 (run 2): the steering session read the project's rules through a shell variable (`$C rules`) in the same shell call as its claim, and the time filter dropped it.
- J26 (run 2): the five fast-forwards happened, but the regex matched text inside a heredoc of the same call.

Fix the three detectors, each with a case in the kit's own tests built from these transcripts' lines.

Source: the study of batch-18's two real eval runs of 2026-11-15 (real-foreman run 2, stack, Foreman on Sonnet 5.5; real-direct run 3, parallel, direct mode on Opus 5.5), judged by the retro-critic. Audits: C:/Users/gaeta/Projets/chantier-eval/real-foreman-2026-11-15.audit.md and real-direct-2026-11-15.audit.md. Retro-critic: before release.
