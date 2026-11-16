Release v0.9.0 of chantier (minor: new features since v0.8.0).

Known so far (2026-11-12): 59 commits on main since v0.8.0 (be32d09). Main lines:
- the changes tree v2 (3-ready, 4-batch, 5-archives, 6-trash), one batch at a time, three batch modes (parallel, series, stack);
- several sessions on one repository (a Chief of Staff, Grillers beside it, a skill per role), `/chantier:status`, the Chief of Staff keeps its rules through compaction;
- an external planning surface; an optional `chantier.yaml` playbook, prices from it;
- `chantier board`, a read-only web view for the user in remote;
- rails: a passed long gate bound to the full head commit and a VERIFIED verdict before `handback ready`, the budget refuses a round, `restore` brings a trashed CR back, the worker write guard;
- Driver liveness (per-CR activity lines, restart from the recorded state), a ready CR handed back again, the heartbeat true in direct mode;
- tracker reports, Sonnet by default for the Foreman and Drivers, a retro at each pause kept at close, the Chief of Staff judges a refused force push;
- the eval campaigns redesigned (real-foreman, real-direct, claude-planted, copilot) and the CLI reads files through a UTF-8 BOM.

Procedure: CONTRIBUTING.md "Release" and docs/release-process.md; the release CR joins the batch whose work it ships.
Both real campaigns before a release (CONTRIBUTING.md): real-foreman passed with findings on 2026-11-12; real-direct runs now.

To settle with the user (grill): the version (0.9.0 proposed), whether the real-direct batch's merged work is in it (the release then joins that batch), the grant (default: each irreversible action waits for the user), a docs diagram in the notes or not, and the price of claude-fable-5-2 (A-9) before the notes quote costs.