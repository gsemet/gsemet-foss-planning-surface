## Summary

After a release is published, the release Driver's closing steps (record the publication, write the retro, hand back) were one prose bullet among many rules, and in a past release the release Driver stopped after publishing with those steps undone until the user asked. This change turns that bullet into an explicit checklist at the end of the release Driver's card, with a line saying the steps are not optional and need no one's word.

## Deliverables

The end of the `## Release driver` section of `skills/chantier/references/driver.md` now reads:

```md
### Release driver: the end

Once the release is out ..., every item below, in this order, before the host's hand-back ...

- [ ] `$CHANTIER release published <cr> --note "<version> <link>"`.
- [ ] The procedure's checks, and any watch of the deploys it names (a package registry, pages).
- [ ] `<work folder>/retro.md`: ... one line `- [<tag>] <problem>: <long-term fix>` ...
- [ ] `$CHANTIER handback <cr> ready <release link or tag>`, then the host's hand-back ...
```

The old "A release out:" bullet is gone; its text is carried by the four items, with nothing dropped. The failure rules (a product failure gets a fix specification, infrastructure gets one re-run) stay a bullet above the checklist and cover a failing item.

## Blast radius

The change is a few lines of one role card, with no code. Grade: **1**. A plain `git revert` restores the previous card.

## Autonomous decisions

None.

## Known gaps

None.

<details>
<summary>Details</summary>

## Changes

- `skills/chantier/references/driver.md`: the "A release out:" bullet is removed; a `###` sub-section "Release driver: the end" is added as the last part of `## Release driver`, so the startup manifest still loads it with the section.
- No change to the agent files of either host (they hold no contract), to the startup manifest, or to the CLI.

## Human decisions

- The fix is a checklist in the release Driver's card, as the retro of the earlier release suggested.
- The path where the host refuses the publication and the user publishes by hand is left out, to be handled on its own.

## Impacts

No visual change. Release Drivers, on both hosts, read the checklist with the rest of their section.

## Test plan

- [x] No behaviour change (a card text change)
- [x] Local gates carried from `0412345` (clean restack onto CR-309, head `1a57bd0`): `just check` pass (369 passed)
- [ ] Evidence: none, text change
- [x] Review: approved at `0412345`, carried over a clean restack (head `1a57bd0`)
- [x] Verified at `0412345`, carried over a clean restack (head `1a57bd0`)
- [x] CI at `1a57bd0` pending after the restack, including the `just scenario (ubuntu-latest)` job

## Internal references

- CR-310 release-driver-end-checklist

</details>
