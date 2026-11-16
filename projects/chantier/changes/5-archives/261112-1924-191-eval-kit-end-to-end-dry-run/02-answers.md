# Answers

- 2026-11-12, the user's go relayed by the parent session, verbatim: "Fait tout ça", after the
  list of the 5 retro items, readme-reorg and release-v0-9-0; earlier: "Fait en autonomie
  maintenant plus de question". The intent and the specification are written without a grill;
  the open points are decided by the Chief of Staff and noted here.
- Decision (Chief of Staff, autonomy, 2026-11-12): the dry run uses a local bare repository as
  the sandbox's origin and touches nothing on GitHub; no model call.
- Decision (Chief of Staff, autonomy, 2026-11-12): "the independent review runs before the
  merge" stays guidance (one line in the kit's rules), not a new role or gate.
- Decision (Chief of Staff, autonomy, 2026-11-12): the dry run is part of `just check`, so every
  eval-kit change proves it; if it cannot stay fast (a few seconds) the Driver keeps it a
  separate `just` recipe that the kit's rules require for an eval-kit change, and says why.
- Decision (Chief of Staff, autonomy, 2026-11-12): the planted faults cover at least the four
  blockers of batch-13; one failing case each.
- Decision (Chief of Staff, autonomy, 2026-11-12): one more round (4 in all) granted for CR-191, under the user's words "Fait en autonomie maintenant plus de question" and "Fait tout ça": the only blocking item left after round 3 is a UTF-8 BOM on evals/kit/dry_run.py. The Driver's J4 exemption (a release tag pushed by name, never -f/--force) is accepted as an autonomous decision listed in the PR body.
- Decision (Chief of Staff, autonomy, 2026-11-12): one more round (5 in all) granted for CR-191, under the same words: the long gate passed locally at 40860c6, and the only red is the new CI job `just eval-dry-run` on ubuntu, where `uv lock --offline` cannot resolve pytest from a cold uv cache. The fix is the Coder's choice within the specification (no network in the dry run itself; the CI job may warm the cache or the dry run may use a lock that needs no registry package).
