Each CR plans what proves its change and leaves that evidence beside its verdict. The cards change; the CLI does not, and a project needs no setup.

- `worker.md`: the Investigator's report ends with an evidence plan; the Verifier captures the before on a detached worktree of the base and the after at the pushed head, into `work/verifier/evidence/` with a `before-after.md`. Evidence that cannot be captured does not alone change the verdict, unless the project's rules require it.
- `driver.md`: the CR Driver validates the plan, writes it when there is no Investigator, passes it to the Verifier, and puts the evidence in this description. Each CR of a stack keeps its own plan.
- `concepts.md`: the `evidence/` line of the folder tree, which the Verifier's new folder would otherwise contradict.

Not changed: `docs/cr-folder-lifecycle.svg` and its texts still label `evidence/` as the Verifier's proofs; the specification names only the cards.

Stacked on #53. Gates at 0578d1a: `just check` 26 passed; `just scenario` 204/204 on github and on gitlab.

## Evidence

The change is card text, with no image or video to upload. Before is a75972e, after is 0578d1a; each row is one card section, extracted by the same command on both sides.

| Section | Before | After |
|---|---|---|
| `worker.md`, Investigator | files, smallest change, risks, questions | the same, ending with an evidence plan |
| `worker.md`, Verifier | `verify.md` and its verdict | also captures before and after into `work/verifier/evidence/` |
| `driver.md`, CR driver | no evidence step | answers for the plan, gives it to the Verifier, puts the evidence in the PR |
| `driver.md`, Stack driver | no plan mentioned | each CR keeps its own plan |
| `driver.md`, Your means | no evidence line | the evidence bullet, with `gh pr edit --attach` |
| `concepts.md`, folder tree | `evidence/`: proof a Verifier keeps | `evidence/`: other proof; the Verifier's is in `work/verifier/evidence/` |

The text files stay in the CR's folder, `work/verifier/evidence/`: six `*.before.txt` and `*.after.txt` pairs, with `before-after.md` listing what each shows and how to reproduce it.
