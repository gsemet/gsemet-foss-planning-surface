# `just check` rejects a byte-order mark; the worker cards repeat the rule

## The request

Two retros report the same fault. In batch-14, CR-191's round 3 Coder wrote a UTF-8 byte-order
mark (BOM) into `evals/kit/dry_run.py` on Windows, and a whole round existed only to strip it.
In real-direct run 1 (2026-11-12, PR 137), conflict resolutions twice left a BOM in files of the
sandbox. The request asks for two things: `just check` rejects a BOM in any tracked text file,
and the Coder and Conflict-resolver cards repeat the no-BOM rule.

## The problem

- The rule exists already, once: `skills/chantier/references/concepts.md`, rule 9 ("Every file
  you write, a PR body included, is UTF-8 without a byte-order mark"). It names the cause too:
  on Windows PowerShell 5.1, `Out-File` and `Set-Content -Encoding utf8` add one. The workers
  read `concepts.md`, yet the fault came back twice, both times from a worker that writes files
  through a shell (the Coder, the Conflict-resolver).
- Nothing mechanical catches it. `just check` (`test` and `release-notes`) has one BOM check
  only: `tests/test_structure.py` refuses a BOM at the head of an agent file, because it hides
  the frontmatter from a host. Any other file passes the gate with a BOM, so the fault is found
  at review, one round later.
- No tracked file carries a BOM today (checked on 2026-11-12, 291 tracked files), so the gate
  can be strict from its first day.

## What would fix it

1. In this repository: `just check` is red when a tracked file starts with the UTF-8 BOM
   (`EF BB BF`), on the three systems, and its message names each file. A Driver's fast gate
   then stops the fault in the round that made it.
2. In every project chantier runs in: the worker card (`worker.md`) says it again where the
   fault happens, in the Coder's and the Conflict-resolver's sections, with the Windows cause.
   This is the only part that reaches a user's project, such as the sandbox of PR 137.

## Out of scope

- A CLI refusal (`gate`, `ship`) of a BOM in a user's project: a project owns its gate, and some
  projects keep a BOM on purpose.
- Other encodings and marks (UTF-16, UTF-32), line endings, and any other content check.
- Stripping BOMs from existing files: there are none here, and a user's project is not ours to
  rewrite.
- The agent files (`agents/`, `com.github.copilot/agents/`): the rule lives in the cards.
