# Answers

No grill: the user said "plus de question" (2026-11-19). Each point below is settled by the
spec-writer from the user's words in `01-intent.md`.

1. **How the reason travels with the order.** `order rounds <cr> --note <n>` takes a whole number
   only (`orders_apply.py` refuses anything else), so the reason cannot sit in that note. The Chief
   of Staff records a second order beside it, `order note <cr> --note "rounds exception: <cause>"`,
   and sends both lines to the Foreman in one message. No CLI change.
   Settled by the spec-writer (2026-11-19).

2. **No CLI refusal.** The CLI knows no role and cannot tell the Chief of Staff's order from the
   user's; a cap at 5 would refuse the user's own larger grants. The exception lives in the cards
   only; the rail (`round` refused past the CR's limit) is unchanged, and so is its message.
   Settled by the spec-writer (2026-11-19).

3. **"4th and 5th" with a configured limit.** The exception raises a CR's limit to the batch's
   `max_rounds` + 1, then + 2, never higher (with the default 3: the 4th, then the 5th). A CR whose
   limit is already at or above `max_rounds` + 2 (by the user's grant) gets no exception grant.
   Settled by the spec-writer (2026-11-19).

4. **One round at a time.** Each exception grant adds one round (`--note <limit + 1>`), each on its
   own cause: the 5th only when the 4th also ran out on a red the batch caused.
   Settled by the spec-writer (2026-11-19).

5. **What counts as a red the batch caused.** The round that ran out failed on a red that appeared
   after an event the CR's own work did not make: a restack or rebase of the CR onto another CR's
   branch, ordered by the Chief of Staff, the Foreman or a stack driver; or a CR merged or moved
   below it. The Chief of Staff judges it from the hand-back, `log <cr>` and the Debugger's
   diagnosis when there is one, and names the event and the failing check in the cause. In doubt,
   it is the user's word, as today.
   Settled by the spec-writer (2026-11-19).

6. **Telling the user.** In the same message that reports the blocked CR: `CR-<n>: round <k>
   granted under the rounds exception: <cause>`. The user's word is not awaited; the user may still
   drop the CR or take the grant back with their own `order rounds`.
   Settled by the spec-writer (2026-11-19).

7. **No escalation on an exception grant.** The red is not the CR's work failing to converge, so
   the next Driver is told `take <cr> --note "rounds exception: <cause>"`, not `escalate: rounds`;
   the Coder keeps the batch's model. `escalate: rounds` stays tied to the user's grant.
   Settled by the spec-writer (2026-11-19).

8. **The Foreman's check.** The Foreman takes an `order rounds` without asking when `status`'s
   order list holds, for the same CR, an `order note` starting `rounds exception:` and the new
   limit is at most `max_rounds` + 2; otherwise it holds the order and asks the Chief of Staff once,
   as today. In direct mode the Chief of Staff applies the rule itself.
   Settled by the spec-writer (2026-11-19).

9. **Scope of files.** Cards only: `chief-of-staff.md`, `concepts.md`, `foreman.md`. The agent
   bodies (`agents/`, `com.github.copilot/agents/`) and the docs carry no round-limit wording to
   mirror; the rail's message in `rails.py` stays as it is.
   Settled by the spec-writer (2026-11-19).

## From the spec critic (2026-11-19)

10. **A hand-back covered by the rounds exception and "blocked twice".** Settled by the Chief of
    Staff (2026-11-19): it does not count toward "blocked twice". concepts.md's "blocked twice" row
    and foreman.md's Escalation bullet say so, and a CR that already holds an `escalated:` note can
    still get the exception. The exception keeps the batch's model, as point 7 says.
11. **How the Foreman treats an `order rounds`.** Settled by the Chief of Staff (2026-11-19): it
    takes every `order rounds`, as the cards say today ("Orders are the user's word"). There is no
    new hold rule. A `rounds exception:` note on the CR changes only the take: `take <cr> --note
    "rounds exception: <cause>"` with no escalation; without the note, `escalate: rounds` as today.
    The Chief of Staff alone answers for using the exception correctly. This replaces point 8's
    hold-and-ask check.
12. **Where the cap is read.** Settled by the Chief of Staff (2026-11-19): the Chief of Staff reads
    the batch's own `settings.max_rounds` from the batch record (or the project configuration),
    never the CR's own limit shown in `status` (`r<k>/<limit>`), which rises with each grant. Each
    exception grant sets the CR's limit to its current limit + 1, and never above the batch's
    `max_rounds` + 2.
13. **The old "unless the user grants more" lines.** Settled by the Chief of Staff (2026-11-19):
    concepts.md (~300-301, "three per CR unless the user grants more") and evals/SCORECARD.md row
    C4 ("the batch's or the one the user granted") add "or the Chief of Staff under the rounds
    exception", and concepts.md ~301 joins the Evidence search list.
14. **Where the Foreman reads the note.** Settled by the Chief of Staff (2026-11-19): in `status`'s
    order list or in the CR's notes (`handoff <cr>`, `log <cr>`), which hold it in full. The
    Foreman marks the note's order done only after its `take`.
