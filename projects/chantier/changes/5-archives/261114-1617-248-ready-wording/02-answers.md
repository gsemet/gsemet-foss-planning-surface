# Answers

Grilled with the user on 2026-11-14.

Short name: `ready-wording`.

1. **The two words** (2026-11-14). The user: "Prete localement / prête à merger": a CR whose work is done and proven but whose PR is still a draft (it sits on a CR not merged yet) is **ready locally**; a CR whose PR is out of draft and can be merged now is **ready to merge**. (Chosen over verified/mergeable, done/ready to merge, stacked/mergeable.)
2. **Where the words apply** (2026-11-14). Everywhere, one vocabulary: what the Chief of Staff tells the user, the Foreman's asks, the STATUS tables, the board and the CLI's output (chosen over the user-facing text only).
3. **When a stacked PR turns ready to merge** (2026-11-14). When every PR under it is ready to merge too, so the user can merge up to it; the top of the stack ready to merge means the whole stack is mergeable (chosen over: when its PR is out of draft on the forge, whatever is under it).
4. **Grilled enough, and when** (2026-11-14). The user, after the full restatement: yes, to the specification, then P2 at the end of batch-17's stack.
5. **The stack's own words** (2026-11-14). Renamed too, one vocabulary: `stack-ready` becomes `stack-ready-to-merge`, `forge-stack`'s `stack #N ready:` becomes `stack #N ready to merge:`, `concepts.md`'s **Stack ready** becomes **Stack ready to merge** (chosen over keeping them).
6. **The icon for ready locally** (2026-11-14). 🟣 (purple): 🟠 stays queued and 🔵 stays ready to merge. (The user first chose 🟠, then, told that 🟠 already marks queued in `STATUS`, chose 🟣.)
7. **Board, pane and status aligned** (2026-11-14). The user: "Tu t'assureras dans le design de la board mod et status que tout soit aligné": the web board (CR-222 and the views CR-225 to CR-228 add, whatever they hold once below this CR), the Claude Code pane (`hooks/register.tsx`'s mod) and the STATUS files and `status` output show the same two words and the same icons (🟣 ready locally, 🔵 ready to merge, 🟠 waits), with no place left on `ready` alone. The PR shows each one side by side.
8. **Three states, not two** (2026-11-14). Read in a report "draft and mergeable", the user: "Si une PR est mergeable elle ne peut pas être en draft, c'est donc que quelque chose ne va pas. Tu as "prête localement" = pas de PR / PR en draft / PR prête à merger". Restated and confirmed: **ready locally** (🟣), the work is done and proven and there is no PR yet; **PR in draft** (⚪), the PR is open and waits for what is under it; **ready to merge** (🔵), the PR is out of draft and the user can merge it, everything under it being ready to merge too (answer 3). 🟠 stays waits. This replaces answers 1 and 6 where they differ. Also: the forge's word "mergeable" (no conflict) is never used to the user for a draft PR.
9. **Ready locally in today's flow** (2026-11-14). Told that a CR never has no PR once ready (the Driver opens it before the long gate, and `handback ready` needs one), the user kept the current flow (chosen over opening the PR only when the CR joins the stack): 🟣 ready locally stays in the vocabulary and is rare.
10. **The icon for PR in draft** (2026-11-14). 🟤 (brown), since ⚪ already marks not started or dropped in `STATUS`. This replaces answer 8's ⚪.
11. **Ready to merge follows the forge** (2026-11-14). A stacked CR shows 🔵 ready to merge only once its PR is really out of draft on the forge, never ahead of it (the CLI records the forge's draft state; chosen over deriving it from answer 3 alone). Answer 3's rule (everything under it ready to merge) still holds as well.
12. ready-wording-Q12: **The icon for ready to merge.** 🟢 (green), replacing 🔵: the "go" light;
    ✅ stays distinct by its shape. 🔵 no longer marks a state. (Chosen over: keeping 🔵.)
13. ready-wording-Q13: **The icon for merged.** ✅ unchanged: the checked square means done, the
    green dot means go. (Chosen over: 🏁.)
14. ready-wording-Q15: **The other icons.** Unchanged: ⚪ not started or dropped, 🟡 working, 🟠 waiting for a named thing on its way, 🔴 blocked, 🟣 ready locally, 🟤 PR in draft. (Chosen over: changing one.)
15. (the user, 2026-11-14) **The icon is the PR's current state.** Told "La prochaine PR prête
    sera 🟢 #171 CR-237" while #171 was a draft waiting for its gate, the user: "Tu me dis que 171
    sera merger plus tard mais tu me met l'icône verte. Il faut que tu utilise l'icône qui
    représente son état actuel". The icon beside a PR or a CR is always its state now, as `label`
    gives it; what it will become is said in words, never with an icon ("🟤 #171 CR-237, do not
    merge: it waits for its gate; it will be the next ready to merge").
16. (the user, 2026-11-14) **A draft is announced "do not merge".** After a draft PR of a stack
    branch (#179, based on CR-222's branch) was merged into that branch because a report called
    it "prête": every PR in draft named to the user says "do not merge" ("ne pas merger") and what
    blocks it, e.g. "🟤 #174 CR-222: do not merge, base = CR-237's branch".
17. (the user, 2026-11-14) **"You can merge it" only for 🟢.** The Chief of Staff tells the user
    they can merge a PR only when it is ready to merge (🟢: out of draft, CI green, no conflict,
    based on the default branch or with everything under it ready to merge); never "mergeable" or
    "ready" of a draft.
18. (the user, 2026-11-14, after #174 was shown 🟤 while its CR was rebasing) **A draft's icon is
    its CR's state, not "draft".** 🟤 is only for a PR whose CR has nothing left to do and that
    sits in draft (waiting for the PRs under it or for the user's word). A draft whose CR is
    rebasing, running CI or a Verifier is 🟡; one waiting for another CR's work (not its merge) is 🟠; one blocked is 🔴.
    The Chief of Staff reads the icon from the batch's `STATUS.md` just refreshed, never from the
    PR's draft flag alone. Example: "🟡 #174 CR-222: ne pas merger, rebase sur main en cours, CI
    4/5", not "🟤 #174".
