# Before and after (CR-385)

Before: base 4ca2f825 (`before.txt`): `watch --help` has no `--for`; a hub append writes `{"seq","t","by","kind",...}`.
After: head f9fb169ca80a92712c9393ff6253487803491798 (`after.txt`): `--for`, `events: wake every 20s`, version 1 lines (`v`, `source`, `audience`), a version 0 line first, a `v: 2` line.
Reproduce: a scratch git repo, `chantier init`, `chantier watch --help`, a `journal.append` of a `merged` event, `chantier playbook`. No image; paths removed.
