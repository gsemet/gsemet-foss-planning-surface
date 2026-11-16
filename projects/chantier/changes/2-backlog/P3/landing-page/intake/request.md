# A landing page on GitHub Pages that shows what chantier brings at a glance

## The user's words (2026-11-09, French, verbatim)

> Et il me faudra une landing page à mettre sur github pages qui soit elle un tour dynamique
> avec de beaux effets pour expliquer d'un coup ce qu'apporte Chantier.
> Regarde la qualité de la landing page https://blume.codes
> Sans aller aussi loin, je veux quelque chose de très proche.
> Ça c'est une autre CR

(Filed apart from the Sphinx documentation CR, on the user's word.)

## Chief of Staff notes (what blume.codes does, read 2026-11-09)

- Built with Astro; no video and no canvas: about 900 inline SVGs and HTML/CSS animation.
- Type: a serif display face (Gelica, falling back to Fraunces) for titles, a rounded sans
  (SN Pro) for text, a system monospace for code.
- The page's arc:
  1. Hero: one claim ("Know what your agents built") and one sentence.
  2. A live, scripted mock of the product in HTML: deliveries, a review waiting on the user,
     evidence with a failing threshold, the plan, phases on a timeline, the PR. It reads as
     the real app, not a screenshot.
  3. A "works with" strip of agent harnesses.
  4. "Three challenges": visibility, trust, review.
  5. The model: "the unit of work is the delivery".
  6. What you get: output, confidence, quality.
  7. Get started in numbered steps with a download button.
  8. A roadmap vision, then a closing claim and the call to action again.
- It carries ad and analytics pixels (TikTok, Reddit, X, Meta, Google, PostHog): not wanted.

chantier's equivalent of the mock would be a scripted tour of one session: the user files an
item, the Chief of Staff grills it, "run them", the Foreman and Drivers work, PRs land as a
stack, the user merges. Existing material: the SVGs in `docs/` (how-chantier-works, the CR
and batch lifecycles), the visual release notes.

## Open questions for the grill

- Stack: plain HTML/CSS/JS in the repo, or a static generator (Astro), and the GitHub Pages
  workflow; how it stays inside `just check`.
- The tour's script: which story, how long, scroll-driven or autoplay, mobile.
- Shared visual identity with the Sphinx site (separate CR); domain.
- Accessibility and `prefers-reduced-motion`; no trackers.
- How it is kept true when chantier changes (who updates it, at release?).
