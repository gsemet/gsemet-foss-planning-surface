# Retro: release v1.8.0

- Local real-window `ci-integration` failed twice at the version head on different steps
  (tall-block-scroll, scroll-sync-suite) while CI integration was green at the same code; it
  cost two local gate runs. Root cause: local window flakiness on an unattended machine. Fix: for a
  release, take the dispatched branch heavy run as the real-window gate and skip the local
  `ci-integration` re-run (step 5 already allows this for a locked screen; widen it to any local
  window flake).
- Post-merge monitoring: the driver started several duplicate waiters on the same `gh run watch`
  and a broad `pkill` stopped its own monitor. Root cause: no single-waiter habit. Fix: one
  background `gh run watch --exit-status` per run, and wait for its notification only.
