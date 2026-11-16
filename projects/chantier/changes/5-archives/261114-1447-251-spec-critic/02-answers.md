# Answers

Grilled with the user on 2026-11-14.

Short name: `spec-critic`.

1. spec-critic-Q1: **When it runs.** On the CRs the Chief of Staff judges impactful, whatever their
   subject: the Chief of Staff cannot know in advance on which subject it will be needed, and the
   priority is no indicator of criticality, complexity or impact. (The user's own answer; the
   options offered were every spec, on request, or only P1s or CRs touching the CLI or hooks.)
2. spec-critic-Q2: **Who gets the findings.** The one who grills (the Chief of Staff or the
   Griller): it asks the user the findings that touch behaviour, in the grill's format, and sends
   the rest to the spec-writer. (Chosen over: the spec-writer directly.)
3. spec-critic-Q3: **Passes.** One pass per spec; it runs again only if the user's new answers
   change behaviour. (Chosen over: until no finding.)
4. spec-critic-Q4: **What the user sees.** The questions, plus one summary line, e.g. "10 findings,
   6 fixed without you, 4 questions". (Chosen over: the full report.)5. spec-critic-Q5: **Saying when it runs or not.** The asker says it in the restatement, one line
   before "grilled enough?", e.g. "critic: yes, it touches the Drivers' contract" or "critic: no,
   two lines of docs"; the user can then ask for it or cancel it. (Chosen over: saying nothing.)
6. spec-critic-Q6: **Who judges.** The one who grills judges, the Chief of Staff or a Griller,
   with the same criterion. (Chosen over: only the Chief of Staff.)7. spec-critic-Q7: **Grilled enough.** Yes: triaged P1, specified, the critic runs on its spec, then added to batch-17 after CR-250 (both touch the grill section of chief-of-staff.md).
8. (decided in lifecycle-line-Q6) **The critic's icon.** 🧐, used by no other role.
9. spec-critic-Q8: **The critic's model.** Opus 5.5 by default, Fable as an option (the user can
   ask for it). (The user's own answer; the options offered were Opus 5.5, Sonnet 5.5, or the
   project's escalation model.)
10. spec-critic-Q9: **Where its cost shows.** On the "grill and specifications with the user" line
    of `cost`, outside any batch budget, with the small change it needs in the CLI's `costs/`
    code. (Chosen over: no CLI change, landing on the Chief of Staff's steering line.)
11. spec-critic-Q10: **Asking for or cancelling the critic.** No new option at "grilled enough?":
    the three options stay; the user says it in the free answer or as a correction ("specify,
    no critic"). (Chosen over: a fourth option.)
12. spec-critic-Q11: **Keeping the full list.** No: it lives in the critic's reply only, shown on
    request during the session; `02-answers.md` keeps the yes or no. (Chosen over: a
    `work/04-spec-critic.md` file, which would give the critic a Write tool.)13. spec-critic-Q12: **Specs the Chief of Staff writes itself** (a release CR, a fix). The critic
    runs on them too when judged impactful; the Chief of Staff applies the fixes itself. (Chosen
    over: no critic on those specs.)
14. spec-critic-Q13: **When the fixes without the user land.** Before the user sees the critic's
    questions: one spec-writer run applies the non-behaviour fixes first, so the summary line's
    "fixed" is true; a second run folds the user's answers. (Chosen over: one run with the
    answers, the line saying "to fix".)
15. spec-critic-Q14: **The cost line, confirmed.** Answer 10 stands knowing that it puts a second
    role name (`spec-critic`, beside `spec-writer`) in the CLI's cost code, against AGENTS.md's
    "the CLI knows no role": the specification states it as a named exception. (Chosen over: no
    CLI change.)16. spec-critic-Q15: **The exception in AGENTS.md.** Yes: AGENTS.md's "The CLI knows no role" line gets a clause naming the cost exception (spec-writer and spec-critic matched by agent type). (Chosen over: in the specification only.)
