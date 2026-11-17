# Batch-18: Completion report

Batch-18 is closed: 42 CRs merged, the last 19 of them (CR-276 to CR-294) in one parallel round of
8 slots, fixes from the study of the two real eval runs of 2026-11-15.

## Final cost

| | Cost | Share |
|---|---|---|
| Foreman | $41.38 | 22% |
| Drivers | $63.52 | 35% |
| Workers | $79.02 | 43% |
| **Total** | **$183.92** of a $450 budget | |

- Most costly CRs: CR-254 $12.49, CR-266 $10.78, CR-262 $7.64.
- Foreman: 226 wakes, context 166,848 tokens on average, 265,766 at its peak.
- Outside the budget, the Chief of Staff: $49.39 steering, $45.92 grilling with the user and
  writing 34 specifications.

## What the round shipped

| CR | Change | PR |
|---|---|---|
| CR-276 | The README says what a batch costs, Foreman or direct | #226 |
| CR-277 | The ready line of a stacked CR names the CR it waits on | #231 |
| CR-278 | Commands name a paused batch and the way out | #229 |
| CR-279 | The spend is fresh when the budget is checked (about 1.5 s per round) | #233 |
| CR-280 | Direct mode's cost report names the Chief of Staff, its lines add up | #230 |
| CR-281 | The merge route works for a PR of a native GitHub stack | #227 |
| CR-282 | The scenario's stack unit fits its budget | #238 |
| CR-283 | The eval judge follows a PR whose head was replaced | #228 |
| CR-284 | The eval audit gives no false FAIL | #232 |
| CR-285 | The sandbox merge waits for the restack's checks | #236 |
| CR-286 | The write guard reads Git Bash paths | #234 |
| CR-287 | The stack driver starts when the stack can form | #242 |
| CR-288 | The eval campaign lists what a release claims | #235 |
| CR-289 | A Driver that ended with no hand-back is flagged | #239 |
| CR-290 | A clean rebase carries the Verifier's verdict | #240 |
| CR-291 | One short card per worker role | #244 |
| CR-292 | The Chief of Staff stays quiet on a Foreman's turn end | #237 |
| CR-293 | Anyone can run an eval campaign from the README | #243 |
| CR-294 | close sees a finished agent from its transcript's end | #241 |

At the close, `close` refused once on a Driver cut by an app restart 15 hours earlier (its last
record a prompt with no answer); on the user's word it passed with `close --stopped <agent>`,
recorded in the batch archive. The local Windows gate (`just scenario`) passed at CR-291's head.
