"""CR-136 verifier probe. Usage: probe.py <repo root holding scenario/run_scenario.py> <out file>

Drives the CLI of that checkout in a throwaway repository with the scenario's fake forge, and
writes, for each state, the label every record draws and what `take` says. Run it on the head and
on a detached worktree of the base for the before/after."""
import argparse
import importlib.util
import json
import sys
import tempfile
import shutil
from pathlib import Path

root = Path(sys.argv[1]).resolve()
out_file = Path(sys.argv[2])
sys.argv = [sys.argv[0]]
spec = importlib.util.spec_from_file_location("rs", root / "scenario" / "run_scenario.py")
rs = importlib.util.module_from_spec(spec)
sys.modules["rs"] = rs
spec.loader.exec_module(rs)
rs.ARGS = argparse.Namespace(forge="github", verbose=False, keep=False)
LINES = []


def p(s=""):
    LINES.append(s)


def cps(s):
    return " ".join(f"U+{ord(c):04X}" for c in s[:1])


def observe(w, cr, tag):
    d = json.loads((w.folder() / "batch.json").read_text("utf-8"))
    c = next(x for x in d["crs"] if x["id"] == cr)
    own_dir = w.work / c["path"]
    own = json.loads((own_dir / "STATUS.json").read_text("utf-8"))
    bj = json.loads((w.folder() / "STATUS.json").read_text("utf-8"))
    row = next(r for r in bj["crs"] if r["cr"] == cr)
    idx = json.loads((w.state / "3-requests/STATUS.json").read_text("utf-8"))
    irows = [r["label"] for b in idx["batches"] for r in b["crs"] if r["cr"] == cr]
    bmd = (w.folder() / "STATUS.md").read_text("utf-8")
    omd = (own_dir / "STATUS.md").read_text("utf-8")
    lab = row["label"]
    p(f"### {tag}  [{cr} status={c['status']}]")
    p(f"- batch STATUS.json : {lab}   first char {cps(lab)}  severity={row['severity']}")
    p(f"- batch STATUS.md has it : {lab in bmd}   line: " +
      next((ln for ln in bmd.splitlines() if '['+lab+']' in ln), "(not found)"))
    p(f"- index STATUS.json : {irows or '(not listed: ended)'}")
    p(f"- own STATUS.json   : {own['label']}   own STATUS.md has it : {lab in omd}")
    p(f"- Now : {own['now']}")
    p(f"- Next: {own['next']}")
    p(f"- waits: {own['waits']}")
    same = {lab, own["label"]} | set(irows)
    p(f"- ONE STRING EVERYWHERE : {len(same) == 1 and lab in bmd and lab in omd}")
    p()


def take(w, cr, tag):
    code, _ = w.chantier("take", cr, expect=None)
    p(f"- `take {cr}` ({tag}) -> exit {code}: {w.last_stderr}")


def guarded(name, fn, w):
    p(f"## {name}")
    try:
        fn(w)
    except Exception as e:
        p(f"!! {type(e).__name__}: {e}")
    p()


def new(w, n, *flags, titles=None):
    w.reset()
    crs = [rs.prepare_cr(w, t)[1] for t in (titles or [f"Case {i}" for i in range(n)])]
    w.start(*map(str, crs), *flags, *rs.FROM_AGENTS_MD)
    w.env["CHANTIER_BATCH"] = w.name
    return [c["id"] for c in w.batch()["crs"]], crs


def case_free_and_slots(w):
    (a, b), _ = new(w, 2, "--parallel", "--slots", 2)
    observe(w, b, "queued, slot free, no waits (expect white)")
    w.chantier("take", a)
    observe(w, a, "working (expect yellow)")
    observe(w, b, "queued, 1 of 2 slots held (expect white)")
    w.chantier("order", "qa", "--note", "try it")
    take(w, b, "slots held by a working CR plus an open QA order")
    observe(w, b, "queued, working CR + open QA order hold both slots (expect orange)")
    w.chantier("order", "done", "O-1")
    observe(w, b, "queued after `order done` (expect white)")
    # blocked / ready / merged on a
    rs.start_driver(w, a)
    w.chantier("handback", a, "blocked", "waits: the stack driver")
    observe(w, a, "blocked waits: (expect orange)")
    w.chantier("take", a, "--note", "the stack driver landed")
    w.chantier("handback", a, "blocked", "question: which one?")
    observe(w, a, "blocked question: (expect red)")
    w.chantier("take", a, "--note", "answered")
    rs.driver_round(w, a, "probe_a.py", "A = 1\n")
    w.chantier("handback", a, "ready", w.cr(a)["pr"])
    observe(w, a, "ready (expect blue)")
    w.chantier("order", "merged", a)
    observe(w, a, "merged (expect check mark)")


def case_full(w):
    (a, b), _ = new(w, 2, "--slots", 1)
    w.chantier("take", a)
    take(w, b, "slots 1, held by a working CR")
    observe(w, b, "queued, slots full (expect orange)")


def case_waits_drop(w):
    (a, b, c), crs = new(w, 3, "--parallel", "--slots", 3)
    rs.depends_on  # noqa
    w.chantier("order", "after", b, "--note", a)
    take(w, b, "waits for a CR")
    observe(w, b, "queued with waits (expect orange)")
    observe(w, a, "queued, free slot, no waits (expect white)")
    w.chantier("order", "drop", c)
    observe(w, c, "dropped (expect white)")


def case_budget(w):
    (a, b), _ = new(w, 2, "--parallel", "--slots", 2)
    observe(w, b, "queued, budget not set (expect white)")
    state = w.folder() / "batch.json"
    w.chantier("order", "budget", "--note", "10")
    state.write_text(json.dumps({**w.batch(), "spent_usd": 2}))
    w.chantier("order", "budget", "--note", "1")
    take(w, b, "spent budget")
    observe(w, b, "queued on a spent budget (expect orange; Now says the budget)")
    w.chantier("order", "budget", "--note", "10")
    observe(w, b, "budget raised (expect white)")


def case_release_behind(w):
    (a,), _ = new(w, 1, "--slots", 2)
    _, rel_folder = rs.prepare_cr(w, "Release v9.9.0")
    w.chantier("order", "add", "--release", "--note", str(rel_folder))
    rel = w.batch()["crs"][-1]["id"]
    take(w, rel, "release behind other CRs")
    observe(w, rel, "queued release behind other CRs (expect orange)")
    w.chantier("take", a)
    rs.start_driver(w, a)
    rs.driver_round(w, a, "rel_a.py", "A = 1\n")
    w.chantier("handback", a, "ready", w.cr(a)["pr"])
    w.chantier("order", "merged", a)
    take(w, rel, "release waits for the user's word")
    observe(w, rel, "queued release waiting for the confirmation (expect orange)")


def case_release_fix(w):
    (a,), _ = new(w, 1, "--slots", 1)
    mk = lambda t: rs.prepare_cr(w, t)[1]
    rel_f, fix1, fix2 = mk("Release v8.8.0"), mk("Fix one"), mk("Fix two")
    w.chantier("order", "add", "--release", "--note", str(rel_f))
    rel = w.batch()["crs"][-1]["id"]
    w.chantier("take", a)
    rs.start_driver(w, a)
    rs.driver_round(w, a, "fx_a.py", "A = 1\n")
    w.chantier("handback", a, "ready", w.cr(a)["pr"])
    w.chantier("order", "merged", a)
    w.chantier("order", "confirm", rel, "--note", "v8.8.0")
    w.chantier("take", rel)
    w.chantier("order", "add", "--note", str(fix1), "--fix-for", rel)
    w.chantier("release", "start", rel)
    w.chantier("order", "merged", rel)
    w.chantier("order", "add", "--note", str(fix2), "--fix-for", rel)
    take(w, rel, "queued release with a pending fix")
    observe(w, rel, "queued release with a pending fix (expect orange)")
    for x in w.batch()["crs"]:
        if x.get("fix_for") == rel:
            w.chantier("order", "drop", x["id"])
    observe(w, rel, "fixes ended (expect white)")


tmp = Path(tempfile.mkdtemp(prefix="cr136-probe-"))
w = rs.World(tmp)
try:
    w.build()
    p(f"# probe on {root}")
    p()
    for name, fn in [("slots, working, waits:, question:, ready, merged", case_free_and_slots),
                     ("slots full by a working CR", case_full),
                     ("waits and dropped", case_waits_drop),
                     ("spent budget", case_budget),
                     ("release behind other CRs", case_release_behind),
                     ("release with a pending fix", case_release_fix)]:
        guarded(name, fn, w)
finally:
    subprocess = rs.subprocess
    subprocess.run(["git", "worktree", "prune"], cwd=w.work, capture_output=True)
    shutil.rmtree(tmp, ignore_errors=True)
out_file.parent.mkdir(parents=True, exist_ok=True)
out_file.write_text("\n".join(LINES) + "\n", encoding="utf-8")
print(f"wrote {out_file}")
