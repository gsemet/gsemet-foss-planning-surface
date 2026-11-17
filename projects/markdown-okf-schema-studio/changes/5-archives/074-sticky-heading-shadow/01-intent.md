# Soft shadow under the sticky heading

User request (2026-10-23, P2): add a small shadow effect under the sticky heading block of the
preview, so the pinned headings read as floating above the scrolled text.

![Sticky headings over scrolled text (cream theme)](sticky-header.png)

Today the sticky block (`preview.stickyHeadingDepth`, here 3 levels) ends with a flat 1 px line
(arrow in the screenshot); the text scrolling under it is cut sharply.

Expectations to confirm at grill time:
- a subtle shadow (or soft fade) below the sticky block only while content is scrolled under it
  (none at the top of the document);
- stylesheet only, readable in light, dark, cream and current-theme; respects
  `prefers-reduced-motion` if it animates in;
- no layout shift, does not cover the floating toolbar, scroll-sync anchor unchanged;
- visual scenarios light + dark (and cream) at a scrolled position.
