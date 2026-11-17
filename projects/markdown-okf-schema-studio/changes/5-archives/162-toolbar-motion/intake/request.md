# Motion for the floating toolbar and its tooltips

Type: feat · Priority: P2 · Filed 2026-10-28 from a grill with the user · Start after PR #167
(CR 153, five-row toolbar) is merged, from `main` (not stacked).

## User request (verbatim, French)

> je vois que je les animations sur les tooltips de la barre principale, j'ai une animation on
> dirait d'apparition sur ceux de la toolbar d'edition. j'aimais bien celle qui faisait une sorte de
> slide depuis la gauche. ensuite j'aimerais bien une petite animation de la toolbar principale a
> l'expansion/close des sous items, et une animation au chargement de la page, quand la toolbar est
> collapsed, elle apparaissent en expand et qu'elle se collapse, pour indiquer qu'elle peut
> s'etendre. c'est un peu de motion design sympa et simple a faire.

## Current state (2026-10-28, `src/core/preview/styles/pageChromeStyles.ts`)

- Main toolbar tooltips: opacity fade only (100 ms), anchored to the right edge, `transform: none`.
- Edit palette tooltips: `sphinx-preview-edit-tooltip-in`, 3 px drop + fade (100 ms).
- A comment still says the palette tooltip slides in "like the floating toolbar's": the slide-in
  the user liked was lost in a refactor.

## Decisions (user, grill 2026-10-28)

1. **Tooltips**: one shared animation for every tooltip (main toolbar, edit palette, table menu):
   slide in from the left (about 6 px) with a fade, about 120 ms.
2. **Expand / collapse of the main toolbar**: rows 2 to 5 unroll as ONE block (height + fade,
   about 160 ms); collapsing reverses it. No per-row cascade.
3. **Load hint**: when the toolbar's saved state is collapsed, a newly opened preview shows it
   expanded, then collapses it, to show it can expand. Plays on **every preview opening**; never on
   a content patch, a refresh, or a reload of the same preview.

## Defaults (not asked; list under "Autonomous decisions" in the PR)

- `prefers-reduced-motion: reduce` disables all three (SwRS-MDOKFSTUDIO-CORE-050, `motion.ts`).
- The hint is an explicit exception to the motion rule "a page that loads never animates what it
  restores"; it does not change the saved collapsed/expanded preference, and any pointer or key
  press during the hint cancels it and leaves the toolbar collapsed.
- Hint timing: expanded for about 700 ms, then the normal collapse animation.
- PR needs before/after evidence (short GIF or screenshot sequence) and requirement updates.
