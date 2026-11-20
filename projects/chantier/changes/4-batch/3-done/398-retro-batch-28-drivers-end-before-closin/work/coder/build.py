import re
D = "C:/Users/gaeta/Projets/gsemet-foss-planning-surface/projects/chantier/changes/4-batch/2-actives/398-retro-batch-28-drivers-end-before-closin/work/coder/"
OUT = "C:/Users/gaeta/Projets/chantier.worktrees/batch-29-CR-398/skills/chantier/references/driver.md"
src = open(D + "driver.orig.md", encoding="utf8", newline="").read().replace("\r\n", "\n")
L = src.split("\n")


def seg(a, b):
    return "\n".join(L[a - 1 : b])


def rx(marker):
    return r"\s+".join(re.escape(w) for w in marker.split())


def cut(text, start, end, repl=""):
    m = re.search(rx(start) + r".*?" + rx(end), text, re.S)
    assert m, start[:40]
    return text[: m.start()] + repl + text[m.end() :], m.group(0)


def sub(text, old, new):
    ms = re.findall(rx(old), text)
    assert len(ms) == 1, (len(ms), old[:50])
    m = re.search(rx(old), text)
    return text[: m.start()] + new + text[m.end() :]


def bullet(t):
    t = t.strip()
    return t if t.startswith("- ") else "- " + t


# ---- opening
op = seg(1, 63)
op = sub(op, '- **Deferred:** "Your means" and the full role section ("CR driver", "Stack driver",\n  "QA driver" or "Release driver") are read before the action that needs them. Another Driver\'s\n  section is not read.',
 '- **Deferred:** the `Means:` sections your role\'s line of `startup-manifest.json` lists (the\n  common path) and the full role section ("CR driver", "Stack driver", "QA driver" or "Release\n  driver") are read before the action that needs them, each when its step comes. A `Means:` or\n  `CR driver:` section that no manifest line lists is a trigger section: read it only when its\n  trigger arises, as a link of this card says. Another Driver\'s section is not read.')
op = sub(op, 'only when its reply needs checking beyond what "Your means"\n    gives. "Your means" already gives each reply\'s format.',
 'only when its reply needs checking beyond what "Means: the\n    record and the workers" gives. That section already gives each reply\'s format.')
op = sub(op, "- **How to read a section:** Grep the heading in the file, then Read with offset and limit, up to\n  the next heading of the same level. A section a link names is read in full: never a few lines\n  of it.",
 "- **How to read a card:** Grep the heading in the file, then Read with offset and limit, up to\n  the next heading of the same level. A section a link names is read in full: never a few lines\n  of it. A card is never printed with `cat`, `sed`, `awk` or `Get-Content`, nor read again once\n  in your context.\n- **Images and git:** a Driver never opens an image file (`.png`, `.jpg`, `.gif`, `.webp`): it\n  attaches the images the Verifier or the Demo explorer names, by path and caption, and judges\n  them from their reply. It never runs `git branch -a` or `git branch --list` with no pattern,\n  nor `git status` outside its worktree: it names its branch or its worktree.")
i0 = op.index("  - `resume: closing`")
i1 = op.index("- A rule you did not read still binds you.")
op = op[:i0] + (
 "  - `resume: closing` (the CR's earlier Driver stopped in its closing): after `handoff <cr>` and\n"
 "    `log <cr>`, read `pr-body.md`, `work/verify.md` and the evidence files it names, by name and\n"
 "    caption, not opened (except a text file a body line needs); read\n"
 "    [pr-template.md](pr-template.md) only before the first body edit, and only the sections that\n"
 "    edit needs. Do not open the specification, `investigation.md`, the `r<n>.md` notes or the\n"
 "    diff, nor a section of this card beyond the Startup core, the closing paragraph of \"CR\n"
 "    driver\" and the `Means:` section of a step you carry out. Start at the first closing step\n"
 "    with no `closing:` note in the log (the closing paragraph names the steps and their notes).\n"
 "    A step outside the closing (a red check, a move, a review item on the code, a `rebase:`\n"
 "    note) brings back the card's usual rules and reads.\n"
 "  - `rebase:`, `restack`, `folded:` or another re-take note: read \"CR driver: re-takes\".\n"
) + op[i1:]

# ---- Means 1: record and workers
rec = seg(66, 68)
ch = seg(69, 95)
ch, w_first = cut(ch, "A worker refused for its first line", "never retried without the model.",
  'A worker refused for its first line, or ended by a host failure: "Means: a worker that fails".')
rp_common = seg(96, 115)
w_restart = seg(116, 127)
longreply = seg(128, 134)
wprompt = seg(164, 173)
esc_means = seg(174, 176)
phase = seg(177, 185)
msgs = seg(637, 646)

# ---- Means 2: context and folder
ctx = seg(135, 163)
ctx = sub(ctx, 'or for the closing hand-off of "CR\n  driver" (`context: closing: …`); a Driver that stops for any other reason\n  names that reason, never `context:` (the closing hand-off of "CR driver" excepted).',
 'or for the closing hand-off of "CR\n  driver" (`context: closing: …`: at 100,000 or more at `VERIFIED`, or at 130,000 or more during the\n  closing); a Driver that stops for any other reason names that reason, never `context:`.')
gitnames = seg(186, 200)
gitnames, wrongplace = cut(gitnames, "A git command run in the\n  wrong place by mistake", "never cleaned by force.",
  'A git command run in the wrong place by mistake: "Means: a git command in the wrong place".')
folder = seg(201, 214)

# ---- Means 3: worktree, rebase, push
wt = seg(215, 220)
rebase = seg(221, 231)
pre = seg(232, 243)
push = seg(337, 382)
push, ship_tail = cut(push, "`ship` refuses, and\n  records nothing, a PR on the default branch", "as the stack driver section asks.",
  '`ship` also refuses a PR whose head carries another CR\'s (`… carries CR-x …`): "Means: carries, conflicts and the early push".')
push = sub(push, "- Push: a plain",
  "- Push and the PR. A remote command that fails with a forge server error or a network failure:\n  \"Means: a remote command fails\". A force push the host refuses: \"Means: a force push the host\n  refuses\". `take` printing `archive: in the PR at <path>`: \"Means: the archive in the PR\". Push: a plain")
push, gitlab = cut(push, "For GitLab, use `glab`'s", "byte for byte.", 'For GitLab: "Means: GitLab forms".')
push, gl2 = cut(push, "(GitLab's `draft` field is unproved", "the CR reading `ready to merge`)", '(GitLab and Copilot: "Means: GitLab forms")')
forge_err = seg(322, 336)
force = seg(606, 636)
archive = seg(441, 459)

# ---- Means 4: long gate
gate = seg(244, 321)
gate, g_carry = cut(gate, "After a rebase with no conflict that leaves the CR's patch unchanged, run no long gate and no `verifier`: the pass and the Verifier's verdict",
  "The CLI reads no forge: you read CI at the new head, which must be green.",
  'A rebase that leaves the CR\'s patch unchanged needs no new long gate and no `verifier`; one with a conflict resolved takes `ship --conflict` and the early push ("Means: carries, conflicts and the early push"). The CLI reads no forge: you read CI at the new head, which must be green.')
gate, g_early = cut(gate, "**Early push** (every batch", "unless the project chose `ci: beside_gate: true`.")
gate, g_top = cut(gate, "A rule that also asks the stack's\n  top for a local run is met by that CR's Driver", "never the top and runs no local gate for this rule.",
  'A rule that asks the batch\'s or the stack\'s top for a local run: "Means: carries, conflicts and the early push".')

gate, g_stop = cut(gate, "Stop only your own CR's running long gate", "never a Driver's, whatever the reason.",
  "Stopping a gate (`gate <cr> --stop`: only your own CR's, only when its result can no longer count) and a long wait in the queue: \"Means: stopping a long gate\". `cancel` is the steering session's, never a Driver's.")
# ---- Means 5: CI
ci = seg(462, 533)
ci, ci_beside = cut(ci, "  - With the `ci: beside the long gate` line (a CR Driver only)", "The 3-hour limit, the \"no CI\" looks, the head check and the CI note's form stay.",
  '  - With the `ci: beside the long gate` line, or an early push: "Means: CI beside the long gate".')

ci, ci_nociv = cut(ci, '  - "No CI" needs two looks', "at most once per pushed head, never a loop.",
  '  - "No CI" needs two looks, a minute apart: "Means: when CI lists no check".')
# ---- Means 6: commits, PR state, evidence
commits = seg(383, 395)
draft = seg(396, 402)
commits, fold = cut(commits, "Before the branch's first push, a checkpoint", "is still the\n  ordinary rule).", 'A checkpoint that is your head before the first push may be folded: "Means: checkpoint commits".')
ev = seg(403, 440)
ev, ev_look = cut(ev, "No image shows the user's username or home folder;", "Nothing about the leak goes\n  in the public PR.",
  'Every image is given the look before it is kept or uploaded: "Means: images and the look".')
logs = seg(460, 461)

# ---- Means 7: your end
end = seg(534, 605)
end, e_waiver = cut(end, "a CR whose `take` or `handoff` prints\n  `gate: waived", "goes on the top PR or a PR above it;",
  '(a waived CR, or the stack\'s top: "Means: hand-backs out of the ordinary")')
end, e_refused = cut(end, "A Driver still recorded on a CR it handed back `blocked`", "by the host's means), and end.",
  'A hand-back refused (`is ready`, `is blocked`, `is merged`, a head `ship` did not record), or a Driver still recorded on a CR it handed back `blocked`: "Means: hand-backs out of the ordinary".')
end, e_budget = cut(end, "`budget:` follows only a CLI refusal", "are never refused for it.", 'A `budget:` hand-back follows only a CLI refusal on the budget: "Means: hand-backs out of the ordinary".')
pre = sub(pre, "The step holds whichever way the first push happens: before `gate` runs; before the push when the long gate is a pipeline job; before the push with the `ci: beside the long gate` line. It is not a third gate, and the long gate stays as it is.",
  "It holds whichever way the first push happens (before `gate` runs, before a pipeline job's push, before the push with the `ci: beside the long gate` line); it is not a third gate.")
end = sub(end, "`context: closing: VERIFIED at <sha7>; next: <what is left>`, the CR driver's closing hand-off):",
  "`context: closing: <where it stopped>; next: <what is left>`, the CR driver's closing hand-off):")
end = sub(end, "The CR driver's closing hand-off, `context: closing: …`, is the same\n  hand-back, made at the pushed-head `VERIFIED` (see \"CR driver\").",
  "The CR driver's closing hand-off, `context: closing: …`, is the same\n  hand-back, made at the pushed-head `VERIFIED` at 100,000 tokens or more, or at the context rule\n  during the closing (see \"CR driver\").")

# ---- CR driver
crhead = seg(647, 659)
crhead, boardw = cut(crhead, "A CR that touches the board's write paths", "names the scratch folder each role's runs use.", 'A CR that touches the board\'s write paths: "CR driver: the board\'s write paths".')
never = seg(660, 670)
never, failed_cr = cut(never, "After a coder that failed", "goes to a `conflict-resolver`.", 'After a failed coder or a failed rebase: "Means: a worker that fails".')
main = seg(671, 735)
main, matrix = cut(main, "then, while the CR\nhas never been pushed and has a matrix,", "`VERIFIED` goes on,",
  'then, while the CR has never been pushed and has a matrix, the matrix probe ("CR driver: matrix probe"),')
main, _old_closing = cut(main, "When that\n`verifier` replies `VERIFIED`, your prompt's `Note:`", "needs no description pass.",
 "@@CLOSING@@")
CLOSING = (
"When that `verifier` replies `VERIFIED` at the pushed head, any claim it could not prove is already\n"
"`UNVERIFIED` or narrowed in `pr-body.md`. Unless your `log <cr>` already holds a `closing: VERIFIED at`\n"
"note (a `resume: closing` Driver carries on from the notes), record one note that holds everything\n"
"the closing needs: `$CHANTIER note <cr> \"closing: VERIFIED at <sha7>; PR <link>; base <branch>;\n"
"pr-body.md posted at <sha7 or not yet>; evidence: <the files verify.md names>; UNVERIFIED: <claims\n"
"or none>; next: evidence in Deliverables, Test plan boxes, pre-post audit and post, description\n"
"pass, PR ready then `ship <cr> <link>`, `handback ready <link>` with the body's gaps\"`. A matrix\n"
"probe's `VERIFIED` and a verdict carried by `ship` need no closing note.\n"
"\n"
"The closing: when the last `context:` line you read is below 100,000 tokens, you carry it out\n"
"yourself, in this order, one note as each step ends (a fresh Driver resumes at the first step with\n"
"no note):\n"
"\n"
"1. The evidence in Deliverables and the Test plan boxes updated (the boxes and the captions carry\n"
"   the SHAs of the [PR template](pr-template.md); a claim the Verifier could not prove is marked\n"
"   `UNVERIFIED` or narrowed in `pr-body.md` first), the pre-post audit, and the post\n"
"   (`gh pr edit --body-file`): `closing: body posted at <sha7>`.\n"
"2. Once the description is final, a short `verifier` pass on the posted description alone\n"
"   (`NOT VERIFIED` is fixed in the description, then checked again by a new short `verifier`\n"
"   start, never a message to the Verifier that replied): `closing: description pass VERIFIED at\n"
"   <sha7>`.\n"
"3. The PR turned ready when its base is the default branch, `closing: PR ready` (a PR that stays\n"
"   a draft: `closing: PR kept draft on <base>`), then `ship <cr> <link>`.\n"
"4. `handback ready <pr link>` with the gaps that the body's Known gaps hold. `ship` and `handback`\n"
"   are in the log as their own events.\n"
"\n"
"At 100,000 tokens or more, or with `context: not measured`, hand off instead: `handback <cr>\n"
"blocked context: closing: VERIFIED at <sha7>; next: <what is left>`, and end; the Foreman starts a\n"
"fresh Driver with `Note: resume: closing`. Besides `context: host asked the hand-back …`, this\n"
"hand-off is the only `context:` hand-back that needs no `context:` line at 130,000 or more. During\n"
"the closing the context rule still applies: at 130,000 tokens or more, or when the host asks for\n"
"the hand-back, hand back `blocked context: closing: <last closing step done>; next: <what is\n"
"left>`. The last edit of the PR body comes before the description pass; any later edit runs the\n"
"pass again before the PR turns ready, never in the same command as the edit. One exception: after\n"
"a carried verdict, the edit that only changes SHA marks to `at <head7> (carried from <sha7>)`\n"
"(\"CR driver: re-takes\") needs no description pass."
)
main = main.replace("@@CLOSING@@", CLOSING)
main, matrix2 = cut(main, "when the specification or the evidence plan names a matrix", "the whole matrix every round)",
  'a matrix: "CR driver: matrix probe")')
main, matrix3 = cut(main, "(and, with a\nmatrix, the last", "the old and new base)", '(with a matrix: "CR driver: matrix probe")')
main = sub(main, '(see "Your means")', '("Means: worktree, rebase and push")')
matrix = matrix.strip() + "\n- " + matrix2.strip().rstrip(")") + ".\n- " + matrix3.strip("()") + "."
gap = seg(736, 739)
ci_sys = seg(740, 746)
esc_cr = seg(747, 752)
move = seg(753, 765)
approve = seg(766, 781)
retakes = seg(782, 843)

moves_pointer = ("After a move (any change of the head after a judgment: a round, a rebase, a restack, a conflict\n"
 "resolution): \"CR driver: moves and conflicts\". A re-take note (`rebase:`, `restack`, `folded:`, a\n"
 "stack base): \"CR driver: re-takes\". Before `handback ready`, no proof in the PR is stale.")

REST = seg(844, len(L))


def sec(h, *bodies):
    return "## " + h + "\n\n" + "\n".join(b.strip("\n") for b in bodies) + "\n"


out = [op, ""]
out.append(sec("Means: the record and the workers", rec, ch, rp_common.rstrip(), "- A reply out of format, a failed worker, a long reply: \"Means: a worker that fails\".", wprompt, phase, "- Escalation: \"Means: escalation\". A `[foreman→driver <cr>]` message: \"Means: the steering session's messages\".", logs))
out.append(sec("Means: context and your folder", ctx, gitnames, folder))
out.append(sec("Means: worktree, rebase and push", wt, rebase, pre, push))
out.append(sec("Means: the long gate", gate))
out.append(sec("Means: CI", ci))
out.append(sec("Means: commits, the PR's state and the evidence", commits, draft, ev))
out.append(sec("Means: your end", end))
out.append(sec("Means: a worker that fails", bullet(w_first), "- " + w_restart.strip(), "- " + failed_cr.strip(), "- " + longreply.strip().lstrip("- ")))
out.append(sec("Means: escalation", esc_means, "- " + esc_cr.strip()))
out.append(sec("Means: a remote command fails", forge_err))
out.append(sec("Means: a force push the host refuses", force))
out.append(sec("Means: the archive in the PR", archive))
out.append(sec("Means: images and the look", bullet(ev_look)))
out.append(sec("Means: carries, conflicts and the early push", "- " + g_carry.strip(), "- " + g_early.strip(), "- " + g_top.strip(), "- " + ship_tail.strip()))
out.append(sec("Means: CI beside the long gate", bullet(ci_beside), "- " + ci_sys.strip()))
out.append(sec("Means: hand-backs out of the ordinary", bullet(e_waiver), bullet(e_refused), "- " + e_budget.strip()))
out.append(sec("Means: stopping a long gate", "- " + g_stop.strip()))
out.append(sec("Means: when CI lists no check", "- " + ci_nociv.strip().replace('  - "No CI"', '"No CI"', 1).lstrip("- ")))
out.append(sec("Means: GitLab forms", "- " + gitlab.strip(), "- Unproved on GitLab and Copilot: " + gl2.strip("()")))
out.append(sec("Means: a git command in the wrong place", "- " + wrongplace.strip()))
out.append(sec("Means: checkpoint commits", "- " + fold.strip()))
out.append(sec("Means: the steering session's messages", msgs))
out.append(crhead.rstrip() + "\n\n" + never + "\n\n" + main + "\n\n" + gap + "\n\n" + moves_pointer + "\n\n" + approve + "\n")
out.append(sec("CR driver: re-takes", retakes))
out.append(sec("CR driver: matrix probe", matrix))
out.append(sec("CR driver: the board's write paths", boardw.strip()))
out.append(sec("CR driver: moves and conflicts", move))
text = "\n".join(out) + "\n" + REST
text = re.sub(r'\(the "Your folder and your\s+background tasks" bullet above\)', '(the "Your folder and your background tasks" bullet of "Means: context and your folder")', text)
text = text.replace('as "Your end" says', 'as "Means: your end" says')
text = text.replace('(Your means, The evidence)', '("Means: images and the look")')
text = text.replace('as "Your means", "Your folder and your background tasks", says', 'as "Means: context and your folder" says')
text = re.sub(r'as "Your\s+means" orders it', 'as "Means: your end" orders it', text)
text = text.replace("\n\n\n\n", "\n\n").replace("\n\n\n", "\n\n")
open(OUT, "w", encoding="utf8", newline="").write(text.replace("\n", "\r\n"))
print(len(text.encode()))
