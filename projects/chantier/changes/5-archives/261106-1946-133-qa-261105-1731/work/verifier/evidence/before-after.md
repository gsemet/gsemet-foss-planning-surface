# before / after, CR-133

Head 3a69ea351ab8e88f4f75c234326f9f807ba8f4d5; before = base 0cbdd58 (detached worktree, removed at the end). Windows only; Linux and macOS are CI's.

Reproduce: `powershell -File replay.ps1 -Cli <chantier.py of base|head> -Out <file> -Root <empty dir>` (before.txt / after.txt); `docs.ps1 -Cli <head> -Root <dir>` gives docs-after.txt (batch landing, close, cost without a Foreman).

| Pair | Before (before.txt) | After (after.txt) |
| --- | --- | --- |
| file twice | exit 3, no `--slug` | exit 2, names `--slug <other>` |
| triage backlog -> P3 | exit 1 "not directly inside 1-inbox" | moved, exit 0; same priority: exit 2 "already P3" |
| triage README.md / dir | "not directly inside 1-inbox" | "triage expects a CR folder: 1-inbox/<item> or 2-backlog/P<n>/<item>", exit 1 |
| order drop twice | second: new order O-2, exit 0 | exit 2 "already dropped", orders unchanged (one O-1) |
| order drop 101 | exit 1 unknown CR | accepted (reaches "already dropped"); 101x still exit 1 |
| cancel then order drop | order O-3 recorded, exit 0 | exit 2 "already dropped" |
| order note on cancelled | recorded, exit 0 | exit 2 "cannot note CR-102: it is cancelled" |
| order rounds / budget | bare usage | usage plus why ('0' is not a whole number...; '-5' is not a positive amount...; "no value given") |
| status / land, applied + pending | one "orders pending" line of 8; land lists a Python list | two lines (pending: O-3 qa; applied: O-1, O-2); land says the Foreman ends each with `order done <O-k>` |
| open 2 CRs | titles then `brief:` | `next:` line, then `CR-n title: src -> dest` per CR |
| open QA folder | "missing Change Specification ... grill the CR first" | "is a QA report: an item to triage and split into CRs, not to open", exit 2 |
| open 8 CRs | 10 lines | 10 lines: opened, next, 8 CRs; none cut |
| unchanged | close/close --yes exit 2 nothing deleted; cost exit 2; order qa then status pending qa; order rounds on cancelled exit 0 | same |
