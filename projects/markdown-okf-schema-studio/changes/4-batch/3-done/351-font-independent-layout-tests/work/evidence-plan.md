# Evidence plan (written by the Driver; no investigator: the specification maps the code)

Host and default matrix: the machine's own font is the variable. Cells:

| Cell | Host | Result it must show | Real flow that proves it |
| --- | --- | --- | --- |
| W-pin | Windows (local) | tableBreakout tests 1-6 pass; tick matrix natural width and twelve case widths with the pinned KaTeX fonts | `npm run test:unit` (or `just check`) in the worktree; widths printed by a temporary local probe, not committed |
| W-nopin | Windows (local) | with the pin temporarily removed, widths are Segoe UI's (tick matrix about 705 px) | same probe, pin call commented out locally, never committed |
| L-pin | Linux (CI `ci-static`, or a Linux run) | same widths as W-pin within 1 px; tests pass | the PR's `ci-static (ubuntu-latest)` job; widths read from a log line of a temporary probe or a Linux run |
| Pin holds | any | computed font-family of a table cell starts with the sans family, of inline code with the mono family; `document.fonts.check` true | the new assertion in test 1 |
| Missing font | any | the helper throws with the file name when a face does not load | code reading of `pinTestFonts` (a temporary local run with a wrong path is welcome) |

Gates: fast gate `just check` (Windows); long gate `just preflight` (Windows: static stage); CI
`ci-static` on Linux and Windows; heavy dispatch on the branch (`-f heavy=true`).

Stop rule: any verdict of `CASES` or precondition of tests 2-6 that flips with the pin: no change
to verdicts, cases, column; measured widths in the PR body; hand back `blocked question`.

No visual change to the product: Impacts says "No visual change" (test-only change).
