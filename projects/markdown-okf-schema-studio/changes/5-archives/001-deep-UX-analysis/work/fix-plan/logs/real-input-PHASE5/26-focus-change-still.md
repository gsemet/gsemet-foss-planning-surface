# 26-focus-change-still

The preview was scrolled, then the editor was clicked and typed in, then a table cell was clicked; the page scroll and the cell's position on screen stayed within 4 px.

Edit mode: on.

Real VS Code window; every action is a real mouse or keyboard event dispatched by Playwright through CDP. Buffer excerpt at capture time:

```markdown
# Operating the fleet

:::{note}
This chapter assumes you have read the depot topology handbook.
It repeats none of it.
:::

Fleet operations is the discipline of keeping vehicles, drivers and legs
aligned when any one of the three is unavailable. The platform does not solve
that problem; it makes the mismatch visible early enough to be fixed by hand.

```{figure} ../external-img/fleet-loop.svg
:name: fig-fleet-loop
:width: 720px

The operating loop: plan, dispatch, observe, correct. Each pass through the
loop consumes the previous pass's corrections {cite}`okoye2019`.
```

## The four states of a leg
```

## Machine checks

- PASS `overlay-covers-text`: no overlay covers preview text
- FAIL `overlay-clipped`: clipped: sphinx-preview-table-menu at 74,1977 460x44
- PASS `identifier-split`: identifier cells stay on one line
- n/a `status-two-lines`: no status with a strong line and message
