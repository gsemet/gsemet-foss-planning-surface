# Take ownership of external PR 404: list item edit scope, list items in the TOC (opt-in)

## Owner's words (2026-11-20)

"Après tu vas rebase et stack la PR ouvert sur
https://github.com/gsemet/markdown-okf-schema-studio/pull/404#issuecomment-7026045927 par un
contributeur externe. Il faut vérifier si c'est au standard donc je pense que c'est un nouveau
flux: lancer un driver qui va faire une verifier et peut être d'éventuelle ajustement. L'idée est
de prendre ownership de cette contribution mais de ne pas faire confiance il faut verifier que tout
est aligné et que le use case est \"légal\" et ne viole pas des req discrètement"

## Source

- PR: https://github.com/gsemet/markdown-okf-schema-studio/pull/404, by the external
  contributor `pspozio`, from the fork branch `pspozio/markdown-okf-schema-studio:markspec-entry-edit-scope`,
  one commit, 40 files, +1062 -108, a draft.
- Its last rework is described in
  https://github.com/gsemet/markdown-okf-schema-studio/pull/404#issuecomment-7026045927 :
  - a click on a list item edits that item only, and a click on the list outside its items edits the whole list;
  - the keyboard walks from the list to its items and blocks (Right, Left, Enter);
  - an opt-in setting, `preview.listItemsInToc`, off by default.

## What is asked

1. **Take the contribution.** Fetch the contributor's commit.
   - Put it on this CR's branch, rebased on the batch's stack (the CR below it).
   - Keep the contributor as the commit author. Add `Co-authored-by` lines as the commit guideline allows.
   - Open this CR's own PR in the batch's stack, as for any CR.
   - Do not push to the contributor's fork.
   - Do not comment on, close or edit PR 404: the owner decides what to tell the contributor.
   - The new PR's body names PR 404 and its author as the origin.
2. **Do not trust it.** Treat every line as unreviewed code from outside, and verify it against the
   project's rules exactly as for our own CRs: the constitution, AGENTS.md, the project guidelines,
   the PR guideline and the requirements guidelines.
   - **Is the use case legal?** Check each behaviour change against the approved StRS and SwRS of
     the scopes it touches (edit mode, block editor, structural navigation, TOC, settings).
   - **No hidden requirement violation.** Look for any change that silently contradicts, narrows or
     removes a published requirement. Examples: a changed test assertion "whose intent changed", a
     hover or click target that an SwRS fixes, or the TOC contents.
   - Never delete a published requirement.
   - **Requirements work the change needs.** Write or update the SwRS for item-level editing,
     keyboard list/item/block navigation and the `listItemsInToc` setting, with
     `@implements_req` and `@tests_req` markers. Then run `just requirements-update` and add the log entry.
   - **Other checks.** Look for dead code, for what is specific to one document format (the
     contributor says there is none, so verify it), for import boundaries and file size, and for
     the settings registry and the generated `package.json`. Check docs, changelog and glossary
     against their guidelines, and check the screenshot evidence.
   - **Security.** Look for any external resource, script or network access the change adds.
3. **Adjust.** Fix what fails the standard in this CR's rounds, keeping the contributor's intent.
4. **Gate.** Run the long gate and the heavy CI (the real VS Code jobs, since it changes edit mode),
   then get the Verifier's verdict.

## Stop rule (owner question)

Stop and hand back blocked with the question in these cases:

- the use case contradicts an approved StRS;
- the change would need a new or re-approved StRS;
- a published requirement would have to change its meaning;
- a behaviour choice of the contributor is not covered by any requirement and is not obviously
  within an existing one.

## Done

- This CR's PR in the stack carries the contributor's work, rebased, verified, adjusted and
  traced to requirements.
- Its body lists every finding: what was fixed, and what was kept and why.
- The PR holds every requirement change, with each StRS question named for the owner.
