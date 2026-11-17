## Summary

Screenshots that agents attach to a pull request, or keep in the planning folder (which is pushed to the forge with the planning surface), could show the user's username or home folder in a local path. A recent PR got such screenshots attached and the leak was caught only after the upload. This PR makes the Driver and Verifier cards require made-up paths in every image, and an explicit look at each image for the username and the home folder before it is kept or uploaded.

## Deliverables

| | Before | After |
|---|---|---|
| Image captured by a Driver or Verifier | no rule on local paths | shows made-up paths, no username, no home folder |
| Before keeping (planning folder) or uploading (forge) | read for what it claims | also given "the look" for the username and home folder; kept or uploaded only once it passes |
| User's own screenshot that fails the look | attached as is | not uploaded or copied; its Known gap stays; the Chief of Staff asks for a new one |
| Leak found after an upload | no rule | image replaced with a clean capture; the user is told the old attachment may stay reachable |
| Verifier on the posted description | clean and consistent | also no attached image showing the username or home folder |

The rule is written once, with its terms, in the Driver card's "Your means", and pointed to from the archive, QA driver and release driver passages; the Verifier card spells the terms out for its own captures.

## Blast radius

Grade: **1**. Cards only (text read by agents); a plain `git revert` restores the previous behaviour.

## Autonomous decisions

- The Foreman card gets one clause relaying the leak report to the Chief of Staff with the ready ask, as the specification's settled open question says, although the "What changes" list names three cards.

## Known gaps

None.

<details>
<summary>Details</summary>

## Changes

- `skills/chantier/references/driver.md`: the rule and terms in "The evidence:"; pointers in "The archive in the PR:", the QA driver and the two release driver bullets.
- `skills/chantier/references/verifier.md`: terms and the capture rule in the capture paragraph; a third condition on the posted description.
- `skills/chantier/references/chief-of-staff.md`: ask for a board pane screenshot with made-up paths; tell the user of an uploaded leak (plain and stack asks).
- `skills/chantier/references/foreman.md`: relay that report with the ready ask.
- No `## Startup core` section changes.

## Human decisions

- Every image a Driver or Verifier keeps or uploads shows made-up paths and no username, with a look before each keep and each upload.
- A user's own screenshot that shows the username or home folder is not uploaded; the gap stays and the user is asked for a new one.
- Images already committed or uploaded are left as they are.
- A leak found after upload is replaced and reported to the user.

## Impacts

No visual change; agents' behaviour with images changes.

## Test plan

- [x] New or changed tests: No behaviour change in code (cards only)
- [x] Local gates carried from `d3a37e7` (clean rebase, patch unchanged): `just check` pass; `just scenario` runs as the pipeline job
- [ ] Evidence: none, no visible change
- [x] Review: approved, carried from `d3a37e7`
- [x] Verified, carried from `d3a37e7` (clean rebase, patch unchanged)
- [x] CI at `2017763` pending after the restack, incl. just scenario (ubuntu-latest)

## Internal references

CR-311 "images use made-up paths" (batch-23).

</details>
