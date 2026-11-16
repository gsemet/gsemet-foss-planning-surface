# Every CLI command accepts a CR's bare number

Batch-09 retro, 2026-11-11 (`4-batch/retro.md`, point 11).

## What happened

`ship 165` was refused ("unknown CR 165"); `CR-165` was needed. `--batch` already accepts a bare
number. Each such refusal costs a retry.

## Proposed fix (to grill)

Every command that takes a CR accepts `165`, `CR-165` and `cr-165` alike.
