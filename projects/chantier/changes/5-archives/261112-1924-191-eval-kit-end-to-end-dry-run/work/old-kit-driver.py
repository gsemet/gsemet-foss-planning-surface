"""Throwaway driver for the old kit: the clean case's steps, taken one by one so each of the
three behaviours under test shows (the old kit has no `sandbox.py merge`, so a stand-in operator
merge, `gh pr merge --rebase` on the fake forge, only lets the staged batch reach the audit)."""
import json, os, sys, tempfile, subprocess
from pathlib import Path
KIT = Path(sys.argv[1]) / "evals" / "kit"
sys.path.insert(0, str(KIT))
import dry_run as d
import sandbox

tmp = Path(tempfile.mkdtemp(prefix="oldkit-")).resolve()
run = d.Run(tmp)
with d.dry_environment(tmp):
    print("== step 1: the reset (b)")
    try:
        d.set_up(d.World(tmp, "reset", run.base()), reset_first=True)
    except d.Mismatch as m:
        print(f"FAIL reset: {m.expected} / {m.got}")
        for l in m.lines[-3:]: print("  " + l)
    print("== step 2: the merge command (c)")
    done = subprocess.run([sys.executable, str(KIT / "sandbox.py"), "merge", "1"], capture_output=True, text=True)
    print(f"FAIL merge: `sandbox.py merge 1` exit {done.returncode}: {done.stderr.strip().splitlines()[-1]}")
    print("== step 3: the staged batch and the audit (a), stand-in merge")
    world = d.World(tmp, "clean", run.base())
    code, out, err = d.captured(d.setup.sandbox_main, "full", world.ws)
    print(f"setup full exit {code}")
    record = json.loads(world.ws.with_name("ws.run.json").read_text(encoding="utf-8"))
    stub = tmp / "stubmerge.py"
    stub.write_text("import subprocess,sys,shutil\nn=sys.argv[1]\nr=subprocess.run([shutil.which('gh'),'pr','merge',n,'--rebase'])\n"
                    "print('merged PR #'+n)\nsys.exit(r.returncode)\n", encoding="utf-8")
    record["merge_command"] = f'"{sys.executable}" "{stub}"'
    record["setup_output"] = out
    batch = d.Batch(world, record, features=True, stale_lock=False)
    batch.play(); batch.write_transcripts()
    world.activate()
    code, text = d.audit_process(world)
    print(f"audit exit {code}")
    for l in text.splitlines():
        if l.startswith("- FAIL") or "[C12]" in l: print(l)
    release = next(c for c in batch.data()["crs"] if c.get("kind") == "release")
    print("release PR", batch.pr_number(batch.links[release["id"]]))
    print("release cr pr field:", release.get("pr"), "| status", release.get("status"))
    print("forge prs:", [(k, v["title"], v["state"], v.get("merged_at")) for k, v in json.loads(world.state.read_text(encoding="utf-8"))["prs"].items()])
    print("created:", batch.data().get("created"), "| prefix:", record.get("prefix"))
    print(subprocess.run([d.sandbox.resolve(["gh"])[0],"pr","list","--repo",record["repository"],"--state","merged","--limit","1000","--json","number,title,mergedAt"],capture_output=True,text=True).stdout)
    print("crs:", [(c["id"], c.get("kind"), c.get("pr"), c["status"]) for c in batch.data()["crs"]])
sandbox.remove(tmp)



