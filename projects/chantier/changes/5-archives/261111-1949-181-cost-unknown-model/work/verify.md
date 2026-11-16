# Verify CR-181 cost-unknown-model

Head: 6590219ad1a4d5245eccc5222a982c4d833ef15d

Claims (all judged at 6590219):

1. Fast gate: `$CHANTIER gate CR-181 "just check"` -> `pass just check at 6590219` (log work/gates/20261111-185611.log).
2. Long gate: `$CHANTIER gate CR-181 "just scenario"` -> `pass just scenario at 6590219` (log work/gates/20261111-191010.log). The scenario holds the spec's steps 1 to 7 (floor wording in cost/status/STATUS.md/board/close, take not refused, all-unpriced close refused, prices: entry and dated id priced, five yaml refusals with lines, shares add to 100 and ratio line, Copilot ratio not measured, no "Driver" line naming the steering session).
3. Pricing rule, own probe (python -I, ephemeral): sonnet call + `mystery-model` + `mystery-model-20270101` -> calls 1, usd 0.022, unpriced {mystery-model: 1, mystery-model-20270101: 1} (the dated id of an unknown model is not priced); with prices={mystery-model: ...} -> calls 3, unpriced {}; `_price("claude-sonnet-5-5-foo")` and `_price("claude-sonnet")` -> None (no prefix/family match).
4. Unit tests in test_costs.py cover unknown model counted once with calls == 1, dated id priced, project price ranks first; the old refusal case left the list (diff read).
5. Copilot: playbook prints "prices: not used on Copilot, whose records carry the price" (playbook.py:461).
6. PR description (read on the forge at 6590219): renders, sections consistent with the diff (costs, playbook, commands/rails/status, card, README/docs, tests). The built-in table gained no model: marked UNVERIFIED in the body, accepted by the brief (no price page readable, none invented).
   Note: the Test plan checkboxes still hold `<sha7>` placeholders and are unchecked; the Driver fills them at its handback.
7. CI at the time of reading: ubuntu `just check` success; macOS, Windows and ubuntu scenario still in progress (not relied on).

Not proved: a built-in price for any new model (spec part 1, decision 1), accepted and marked UNVERIFIED; Windows/macOS CI result.

VERIFIED
