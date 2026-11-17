# Reload-campaign watchdog does not fail a hung campaign

Seen once in CI on PR #365 (CR 288, head ffca17bf): the integration job hung in the final reload
campaign (`runWatchedReloadCampaign`). The watchdog did not fire and no VS Code process was alive,
so the job ran until its timeout. Not reproduced; the next run was green.

Expected: when the campaign stops making progress or its VS Code process is gone, the watchdog
fails the job quickly with a message naming the campaign step.
