## Summary

The sticky heading band now casts a soft shadow onto the text scrolling under it, so the pinned
headings read as floating above the page instead of ending in a flat 1 px line. The shadow shows
only while the page is scrolled; at the top of the document there is none.

## Deliverable showcase

Before: a flat divider, text cut sharply under the band. After: the same divider plus a soft shadow.

```css
/* shown only while the page is more than 1 px below the top */
[data-sphinx-preview-sticky-headings][data-scrolled-under] {
  box-shadow: 0 6px 8px -5px var(--sphinx-preview-band-shadow);
}
```

The shadow colour is set per theme (stronger in dark, warm grey in cream). It is a `box-shadow`, so
it takes no layout space: the content, the reading offset and the scroll-sync anchor do not move,
and the floating toolbar stays stacked above the band. There is no animation.

Content scrolled under the pinned headings, light, dark and cream:

![Sticky heading shadow, light](https://raw.githubusercontent.com/gsemet/markdown-okf-schema-studio/11cdee089045de1161f35c4233b1ca75e2257171/v32-sticky-shadow-light-900.png)
![Sticky heading shadow, dark](https://raw.githubusercontent.com/gsemet/markdown-okf-schema-studio/11cdee089045de1161f35c4233b1ca75e2257171/v33-sticky-shadow-dark-900.png)
![Sticky heading shadow, cream](https://raw.githubusercontent.com/gsemet/markdown-okf-schema-studio/11cdee089045de1161f35c4233b1ca75e2257171/v34-sticky-shadow-cream-900.png)

## Test plan

- [x] `just ci-visual`: 332 scenarios, 222 screenshots, passed (3 new scenarios: light, dark, cream
  at a scrolled position; each asserts the marker, a non-empty downward box-shadow, the band fixed at
  top 0 and the toolbar above it).
- [x] Unit: 2604 tests pass (`just check` unit stage), including the new test that the band is
  marked only when scrolled below 1 px and unmarked again at the top.
- [x] okfreq: validate (1011 requirements, 0 errors), lint, update-coverage all clean.
- The visual check that refused any shadow on the band now accepts exactly the marked one.

## Requirements

New SwRS-MDOKFSTUDIO-TOOLBAR-002 (shadow only while text scrolls under the band), derived from
StRS-MDOKFSTUDIO-TOOLBAR-004; entry added to the requirements log.

## Internal references

- CR 074 (sticky-heading-shadow)

🤖 Generated with [Claude Code](https://claude.com/claude-code)
