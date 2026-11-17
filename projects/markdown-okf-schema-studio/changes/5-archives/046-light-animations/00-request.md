# 046 — light-animations

From backlog `P3/animation-markdown-studio` (`01-intend.md`: "Propose light and elegant animation").

## Decisions (user grill, 2026-10-23)

1. Scope (all four):
   - block, table-cell and frontmatter editors: open/close (short fade/expand);
   - floating bar, `/` palette and menus: soft appearance;
   - preview theme switch: colour transition;
   - content update: a changed block glows briefly after an external change or an undo.
2. Light and elegant: about 100–200 ms, CSS only through the stylesheet (no inline `style=`),
   no layout shift, no animation on initial render or scroll sync.
   `prefers-reduced-motion: reduce` disables them all. Readable in light, dark, cream, current-theme.
3. Tests must stay deterministic: visual tests disable animations (or wait for `animationend`
   / transitions via a test hook), never a sleep. Unit test for the reduced-motion rule and for the
   update-glow trigger.
4. PR shows before/after screenshots (or a short clip from the visual run if available).
5. Speed: Opus everywhere, reviewer on the round diff, ready when `checks` is green. Rounds: 3.
6. PR written for an external reader.
