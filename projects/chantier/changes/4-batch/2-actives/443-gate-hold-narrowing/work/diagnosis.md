# CR-443 diagnosis: `just scenario` red at ce00b80

Both causes are in the harness (`scenario/run_scenario.py`). The CLI behaves as the spec says.
No code was run beyond reading the transcript
(`scenario/results/scenario-20261122-022724-27488.md`) and the code.

Reproduce: `just scenario` units `surface-board` (cause 1) and any unit (cause 2).

## Cause 1: `SurfaceWorld.chantier` hides `gate` from `named_args` (FAIL 1 and 2)

`World.chantier` turns a `gate` call's command words into names only when `args[0] == "gate"`
(line 445), and `named_args` assumes `args[0]` is `gate` (the `i == 0` branch, line 355).
`SurfaceWorld.chantier` (line 9889) prepends `--project demo` before calling
`super().chantier`, so `args[0]` is `--project` and the call goes through unnamed.

Transcript (line 28561): `chantier --project demo gate CR-101 "<py>" -m compileall -q .`
exits 2, `gate CR-101: chantier.yaml names no long gate`. It never reached a free-command refusal:
the file was never written in the code clone, because `gate_named` never ran. (It exits 2, not
0 as the brief says: the check expects 0 and gets 2.) FAIL 2 follows: no gate recorded, so
`handback ready` is refused ("no long gate passed").

Fix, in `World`:

```python
    def named_args(self, args: tuple) -> tuple:
        head = args[:2] if str(args[0]) == "--project" else ()   # SurfaceWorld's global option
        args = args[len(head):]
        out, i, seen_cr = [], 0, False
        ... (loop unchanged) ...
        return (*head, *out)
```

and in `chantier` (line 445):

```python
        if named and self.words(args)[:1] == ["gate"]:
            args = self.named_args(args)
```

(`self.words` already drops the `--project <name>` pair.) `gate_named` then writes
`chantier.yaml` in `self.work`, which in `SurfaceWorld` is the code clone (`root / "code"`), the
main checkout the CLI reads (`Repo.root`; `load_long_gate` takes `commands` from that layer
only). Nothing else is needed for the surface units.

## Cause 2: the harness's own `chantier.yaml` trips `write_scope` (FAIL 3, 4, and one in every unit)

`gate_named`/`sync_gates` now write `chantier.yaml` (the named long gate) at the workspace root
at the first `gate` call. It is untracked and not under `.agents/changes/`, so `write_scope`
(line 10839) reports `['?? chantier.yaml']`. This is not chantier writing outside the planning
folder: the scenario itself wrote it, as the Chief of Staff's user would. It fails in every unit
that gates (stack, release, gates, series-deps, direct, qa-driver, gitlab: 1 check each in the
table), and will do so in `surface-board` once cause 1 is fixed (its `write_scope` runs
`git status` in `w.work`, the clone).

Fix, in `write_scope`: leave out the harness's file, and only it. Cleanest: `World.sync_gates`
keeps the text it wrote (`self.yaml_text`), and `write_scope` drops `?? chantier.yaml` when the
file's text equals it:

```python
    outside = [ln for ln in lines if not ln[3:].startswith(".agents/changes/")
               and not (ln == "?? chantier.yaml" and w.yaml_text is not None
                        and (w.work / "chantier.yaml").read_text("utf-8") == w.yaml_text)]
```

with `self.yaml_text = None` in `__init__` and `self.yaml_text = new` (also when unchanged) at the
end of `sync_gates`. Cases that edit the file (line 3297, 3328, 4167, 5392, 10046...) then
show up as outside writes unless they unlink it at their end, as 3372 and 6187 already do:
if one of them trips, add `(w.work / "chantier.yaml").unlink(missing_ok=True)` at its end or
reset `w.yaml_text = None` after it unlinks. Simpler, less strict alternative: skip any
`?? chantier.yaml` whose text contains `long_gate:`.

An alternative to avoid touching the check: commit the file in `World.build` (it is part of the
project, as `AGENTS.md` is) and keep `sync_gates` rewriting it as a tracked modification;
that needs `M chantier.yaml` allowed too, so the first fix is simpler.

## After the fixes

Rerun `just scenario` (units `surface-board`, `qa-driver`, `gitlab`, and one of `stack` or
`gates`, enough to confirm 1 and 2). Expected: all four FAILs gone. The other FAILs of the
table (stack 216/217, release 142/143, gates 117/118, series-deps, direct) are the same
cause 2, one check each: the transcript's only `- [ ]` lines there are the write-scope ones
(plus the two of surface-board).
