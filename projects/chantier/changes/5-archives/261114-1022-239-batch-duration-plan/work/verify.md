# Verification, CR-239 (head af970ea758e6f8a25786e66f99b786bffea8ae5e)

## Only two cards change
`git diff origin/main --stat` -> chief-of-staff.md (76 +/-), status-layout.md (4 +/-); 2 files, 78 insertions, 2 deletions.

## Reading pass (grep "floor" in the two cards, at af970ea)
- chief-of-staff.md:53 Hard rule "No delivery time without the floor"
- :387 plan item (floor, two terms, critical path, delivery time or unknown)
- :425-431 "The cut" paragraph
- :501 `### The floor` (under "## Starting a batch", before "## While it runs" at :545)
- :551 Reports sentence (remaining floor, updated delivery time, slip of an hour)
- :566 bullet "When the time will not hold"
- :1099 Never: "Tell the user when a batch or a CR will be done without its floor."
- status-layout.md:76 Notes list gains floor / slip / partial stack; :89 the Notes floor line paragraph; Completion gets no floor line.
Extra (answer 10): `partial stack mergeable below <commit>` is in chief-of-staff.md:555 and status-layout.md:89.

## Links
`[The floor](#the-floor)` (lines 53, 387, 551) resolves to the heading `### The floor` (:501). `status-layout.md` and `concepts.md` exist in references/ (Test-Path True).

## Worked example, batch-17, 13 CRs, depth 6
Gate time (events.jsonl, run 20261113-190315-26164, result pass, last event t = 2026-11-13T18:27:15Z):
- start from the id: 19:03:15 local; machine zone Romance Standard Time, offset on 2026-11-13 = +01:00 (`[TimeZoneInfo]::Local.GetUtcOffset`) -> 18:03:15Z
- 18:27:15Z - 18:03:15Z = 24 min. So G = 24 min (not the 35 min of the card's example, which is request.md's figure; the card example is a symbol-style illustration).
- Other passed runs vary (e.g. 20261114-084919-15892: 07:49:19Z -> 09:03:41Z = 74 min, with rounds); the card says "latest passed runs", the example uses the one named.

CI time (`gh run list --repo gsemet/chantier --status success --limit 8 --json startedAt,updatedAt,...`), start -> update:
08:27:14->08:37:38 = 10m24s; 07:50:51->08:00:27 = 9m36s; 07:13:34->07:26:13 = 12m39s; 06:46:00->06:55:16 = 9m16s; 06:36:21->06:49:32 = 13m11s; 05:45:56->05:55:44 = 9m48s; 05:22:16->05:34:46 = 12m30s; 04:29:08->04:41:08 = 12m00s.
Latest = 10m24s (about 10.4 min); mean of the 8 = 5364 s / 8 = 670.5 s (about 11.2 min). Use C = 10.4 min.

Terms:
- lock term = 13 x 24 min = 312 min = 5.2 h
- chain term = 6 x (24 + 10.4) min = 6 x 34.4 = 206.4 min = 3.44 h (with C = 11.2: 6 x 35.2 = 211.2 min)
- floor = max(312, 206.4) = 312 min = at least about 5.2 h, the lock term. Critical path: CR-221 -> CR-237 -> CR-222 -> CR-225 -> CR-226 -> CR-228.
- From 2026-11-13 19:03 local start, delivery "not before" 00:15 local (+312 min).

## Verdict
All Evidence items met by reading; just check / just scenario reported passed at this head by the caller (not rerun by me). Observation: the card's example uses 35 min x 13 = 7.6 h from request.md while the record gives 24 min; harmless as an illustration, and the example is labelled "batch-17's figures".
