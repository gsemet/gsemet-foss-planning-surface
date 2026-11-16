# Answers: pr-details-fold

Grilled with the user on 2026-11-09 (Battlestation session), in French; recorded in English.

## 1. What stays visible, what is folded

Visible, in this order (what a reviewer reads in 30 seconds):

1. **Summary**: the why, in two or three sentences.
2. **Deliverables**: the main visual, and the impactful choices made (see 3).
3. **Blast radius**: the grade and its one or two lines.
4. **Autonomous decisions**: right after Blast radius and kept visible: the user wants to review
   each one.

Folded in one `<details><summary>Details</summary>` block, in this order:

- Changes
- **Human decisions** (new, see 2)
- Impacts, except the before/after screenshots of a visible change, which stay outside the fold
- Test plan
- Internal references, still last

The Inspector's audit keeps checking every section in order, and also that the fold is in place.

## 2. A new folded section: Human decisions

- The impactful decisions the user took during the grill (the interview of the idea), extracted
  from the CR's `02-answers.md`.
- Only the decisions that shape the change, not every answer.
- The user always missed this in a PR: it shows what was decided by a person, beside the
  Autonomous decisions that agents took alone.
- Same rule as the rest of the body: no internal reference, written for a reader outside the team.

## 3. Deliverables shows the impactful choices

Deliverables shows the choices that matter, by kind of change:

- **UI:** the important choices are aesthetic and behaviour.
- **Architecture:** the architecture choices.
- **Rework or refactoring:** the targets set, e.g. scores to reach.

They come with the visuals already asked for (diagram, before/after, code sketch).

## 4. Assumptions stated by the Chief of Staff, not yet confirmed

- A project's own PR template still ranks above this one; only chantier's default changes.
- A CR with no grill (e.g. a quick fix) writes "None" under Human decisions.
- The Inspector also checks that Human decisions matches `02-answers.md`.

## 5. The assumptions, answered (2026-11-10)

- A project's own PR template still ranks above this one; only chantier's default changes.
  (Confirmed.)
- A CR with no grill (e.g. a quick fix) **omits** the Human decisions section; it does not write
  "None". (The user chose "Section omise" over the recommended "None".)
- The Inspector also checks that Human decisions matches `02-answers.md`: nothing dropped,
  nothing invented. (Confirmed.)

## 6. The specification's two questions (2026-11-10)

Not asked: the same day, on claude-code-config, the user said such detail is for the agents
("Trop détaillé laisse le vérifier faire son boulot"). The spec's recommendations stand:

- The before/after screenshots of a visible change go in Deliverables, as its main visual.
- A grilled CR whose answers hold no decision that shapes the change leaves Human decisions
  out, as a CR with no grill does.

## Status

Restated to the user on 2026-11-09; assumptions answered on 2026-11-10; restated in full the
same day. Grilled enough, on the user's word ("Oui les deux", 2026-11-10): specification by the
spec-writer.
