Short name: `marker-gate`

# Answers

## 2026-11-17, owner

Questions asked in the Chief of Staff session with a recommendation each; the owner answered "Ok pour tout", then "Tu peux lancer tout ce que tu m'as dis, avec le foreman réutilisé et finissant sur une stack de PR". Every recommendation is taken:

1. marker-gate-Q1: **SwRS with no source marker.** An in-force, non-exempt SwRS with no @implements_req fails `just check`; DIAG-128 is fixed in the same CR.
2. marker-gate-Q2: **Marker lists.** A marker comment names at most 3 IDs; a companion file (`*.markers.ts`, checked by `just check-markers`) names, for each ID, the scenario that checks it (for example `@tests_req X — scenarioPalette`).
3. marker-gate-Q3: **Existing offenders.** The check starts from a baseline list of today's offenders that can only shrink (a ratchet); the six req-garden CRs empty it.
4. marker-gate-Q4: **Where.** In Studio, extending `scripts/check-marker-companions.mjs`; okfreq may take it over later through okf-schema's CR okfreq-gardening-skill-audit-checks.
5. **Way:** launched without the owner reviewing the specification ("lance tout"): a short specification the owner does not review. Spec critic: yes, it changes what the static checks (CI) refuse.

## 2026-11-17, owner (open questions of the specification; critic: 4 points, 3 fixes, 1 question)

6. marker-gate-Q5: **realInput/markers.ts.** A. Rule 3 covers any tracked file with a `// Companion of:` line; this file goes on a rule-3 baseline until the req-garden CRs name each scenario.
7. marker-gate-Q6: **Companion @implements_req lines.** A. Yes to both: they name their code point, and a companion whose lines are all named escapes the 3-ID cap.
8. marker-gate-Q7: **Name checked.** A. Yes: the named scenario or code point must exist in the host file or its folder.
- Order (critic fix, Chief of Staff): req-use-case-diagrams lands after this CR and writes its companion line in the rule-3 form.
