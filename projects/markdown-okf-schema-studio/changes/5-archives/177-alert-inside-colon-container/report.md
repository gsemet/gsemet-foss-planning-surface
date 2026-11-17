# 177 — GitHub alert inside a ::: container closes it early — report

Landed 2026-10-28. PR https://github.com/gsemet/markdown-okf-schema-studio/pull/188 merged as
cb1f2adc (normal CI green on the pre-rebase head, run 40781042323).

- Inside an open colon container the alert is now emitted as a backtick directive (fence >= 4
  backticks, longer than any backtick fence in the body); outside, still a `:::` admonition. A
  longer colon fence cannot work (it would close the parent). Output line count unchanged: the
  alert line map stays exact.
- Tests (written first, failing before): alert in a card, a tab-item, a card in a nested grid,
  after closed containers, four-backtick code in an alert body; exact data-line/data-end-line.
- Opus: round 1 changes (closing fences counted as openers; 4-backtick body), round 2 APPROVE.
- Follow-ups: nested `> > [!TIP]`; alerts inside backtick-fenced directives.
