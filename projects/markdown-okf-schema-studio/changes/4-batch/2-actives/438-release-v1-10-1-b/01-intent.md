Patch release v1.10.1 of Markdown OKF-Schema Studio, by the project's own procedure
(`.agents/guidelines/release-process.guidelines.md`), in batch-07.

Scope: the work of batch-07 merged on `main` since v1.10.0: CR-435 (CRLF test fixtures kept CRLF,
save tests on CRLF/LF/mixed files) and CR-436 (the block editor no longer stuck on
"Saving Markdown..." in CRLF files; the file's own line endings are kept). The release waits for
CR-436's merge, as every release CR waits for the batch's other CRs.

The owner reviews the release PR (version commit and release notes) and merges it; the
irreversible steps after the merge wait for the owner's yes, asked with the merge.
