## Summary

Chantier's docs had no picture of what a Release driver does. This adds a diagram that follows one real patch release on a timeline, from the owner's "release" to the archive, anonymised. Like the other docs diagrams it shows the target behaviour, and the README now links it from a new Releases section.

## Deliverables

The new diagram, `docs/release-driver.svg`, has six lanes (owner, Chief of Staff and Foreman, Release driver, CR drivers, CI, forge and registry) on a relative time axis. The owner has four touchpoints; the dashed fix path is marked "not needed in the example"; a loop arrow takes the retro back to the intake. Its texts are in `docs/release-driver-texts.md`.

Render of the diagram at 8e14593 (it paints its own background, so a light and a dark page look the same):

## Blast radius

Docs only: a new SVG, a new texts file and one README section. `git revert` restores the previous state.

Grade: 1

## Autonomous decisions

- The owner's "yes, now" is drawn right after the last stack merge, before the heavy run, since the timeline did not fix that order.
- Two small labels were added on the owner lane ("never an agent", "7 user-visible fixes to a patch").

<details><summary>Details</summary>

## Changes

- `docs/release-driver.svg` (new), `docs/release-driver-texts.md` (new, prose paragraph identical to the SVG description).
- `README.md`: new `## Releases` section after `## Detailed lifecycle`.

## Human decisions

- The diagram shows the target, not today's behaviour.
- The example is anonymised: no names, numbers, tag values, quotes or dates; durations and counts only.
- The version PR is drawn opened ready, as the Release driver's card says.

## Impacts

No code or behaviour change; the README gains one image.

## Test plan

- [x] `just check` passes (CI, 8e14593).
- [x] SVG parses as XML; no font-size below 14; description equals the texts paragraph.
- [x] Anonymisation search of both new files finds nothing (8e14593).
- [x] Light and dark renders read well.

## Internal references

CR-175 release-driver-diagram (batch-11).

</details>
