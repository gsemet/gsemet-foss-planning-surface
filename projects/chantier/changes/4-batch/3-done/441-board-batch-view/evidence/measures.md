# CR-441 measures

Worktree head `9b22d87` plus the uncommitted change. Run: `evidence_run.py` (work/scratch).

## Pictures

- picture: `before-graph-unlit.png`
- picture: `before-graph-cr148-hovered.png`
- picture: `after-graph-unlit.png`

## Unlit, base layer (`svg.edges:not(.top)`)

- heads into CR-148: 1 (expected 1); heads in all: 4, arrows: 6
- head tip (graph coordinates): [1186, 87.59375]; middle of CR-148's left edge: [1186.00, 87.59]
- tip distance: dx 0.00 px, dy 0.00 px: within 1 px
- arrows into CR-148: 3 (expected 3)
  - from CR-141: last L = [1186, 87.59375], distance 0.00 px: ok
  - from CR-145: last L = [1186, 87.59375], distance 0.00 px: ok
  - from CR-146: last L = [1186, 87.59375], distance 0.00 px: ok
- top layer children, unlit: 0 (expected 0)
- picture: `after-graph-cr148-hovered.png`
- picture: `after-graph-cr148-hovered-arrows-from-cr141-and-cr146-over-the-cards.png`

## CR-148 hovered, top layer (`svg.edges.top`)

- arrows: ['CR-141>CR-148', 'CR-145>CR-148', 'CR-146>CR-148']; heads: 1 (expected 3 arrows, 1 head)
- arrow stroke: ['rgb(29, 92, 99)', 'rgb(29, 92, 99)', 'rgb(29, 92, 99)']; head fill: ['rgb(29, 92, 99)']; accent resolves to rgb(29, 92, 99)
- top layer z-index 2, pointer-events none
- picture: `after-graph-cr146-keyboard-focus.png`

## CR-146 focused with Tab

- active element: `CR-146`; top layer arrows: ['CR-146>CR-148']; heads: 1

## The switch's tooltips (1400 x 860, running batch, mode stack)

- picture: `after-switch-tip-series-en.png`
  - en series: text `To switch, ask the Chief of Staff to "change the batch to series"`; right 1302.6 <= innerWidth 1400: ok
- picture: `after-switch-tip-stack-en.png`
  - en stack: text `This batch's mode.`; right 1243.0 <= innerWidth 1400: ok
- click on Series, unchanged? url: True; page text: True; batch.json: True
- picture: `after-switch-tip-series-fr.png`
  - fr series: text `Pour changer, demande au Chief of Staff : « passe le batch en série »`; right 1295.6 <= innerWidth 1400: ok
- picture: `after-switch-tip-stack-fr.png`
  - fr stack: text `Le mode de ce batch.`; right 1242.4 <= innerWidth 1400: ok
- picture: `after-closed-batch-switch-no-tooltip.png`

## Closed batch (mobile-app batch-01)

- mode words: 3; tabindex of each: [None, None, None]; `.tip` elements: 0; visible after hover: 0
- picture: `after-graph-phone-375.png`

## 375 x 812

- `.bmode .ms` display: none; heads into CR-148: 1; scrollWidth/innerWidth/body: [375, 375, 375] (no horizontal scroll: True)
