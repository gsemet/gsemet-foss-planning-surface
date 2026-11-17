# The stress run's launch deadline no longer fits its rounds

CR-326 (PR #398) grew the stress list to 17 scenarios, about 68 s a round. `just ci-stress` keeps
a fixed 26-minute launch deadline (`STUDIO_LAUNCH_TIMEOUT_MS=1560000`), sized when 20 rounds took
about 18 minutes. The default 20 rounds now take about 23 minutes: a slow runner times out a
healthy run. Heavy run 43581058313 with `stress_repeat=60` died at round 23 of 60 with "LAUNCH
TIMEOUT: trusted-suite.js exceeded its 1560000 ms deadline", all 391 scenario lines PASS.

The version push runs stress, and stress gates the tag and the publish: v1.9.1 may stall.

Found by the CR-326 Driver after the merge, relayed by the Foreman, 2026-11-14.
