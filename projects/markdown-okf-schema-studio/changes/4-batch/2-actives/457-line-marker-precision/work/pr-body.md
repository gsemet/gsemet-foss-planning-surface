## Summary

The line marker (CR-445) becomes precise in three places: a pipe table marks the row of the line, a line in a hidden tab selects that tab and is marked on its exact line, and a front matter line marks its property row.

Renderer risk: content in directive bodies and tab items now carries whole-file `data-okf-marker-line` attributes (never mapped, never a click target); render tests cover each container.

## Review

- [ ] Inspector approved

## Evidence

In progress (round 1: code and unit tests).
