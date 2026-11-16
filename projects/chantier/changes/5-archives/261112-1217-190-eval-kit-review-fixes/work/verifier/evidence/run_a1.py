import importlib.util, json, sys, pathlib
S = pathlib.Path(sys.argv[1])  # scratch folder holding audit_old.py and its siblings
WT = pathlib.Path(r"C:\Users\gaeta\Projets\chantier.worktrees\batch-13-CR-190\evals\kit")

def load(name, path):
    sys.path.insert(0, str(path.parent))
    for m in ("judge", "sandbox"):
        sys.modules.pop(m, None)
    spec = importlib.util.spec_from_file_location(name, path)
    m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m); return m

REPO = "gsemet/chantier-eval-sandbox"
PFX = "[eval 9 2026-11-14 full]"
def link(n): return f"https://github.com/{REPO}/pull/{n}"

def make(variant):
    crs = [
        {"id": "CR-1", "title": "feat", "kind": "feature", "status": "merged", "pr": link(11), "notes": [], "order": 1, "round": 1},
        {"id": "CR-2", "title": "release v0.2.0", "kind": "release", "status": "merged", "pr": None,
         "notes": [f"merged: {link(12)}"], "order": 2, "round": 1},
    ]
    events = [{"kind": "ship", "cr": "CR-2", "pr": link(12)},
              {"kind": "order", "order_kind": "merged", "actor": "foreman", "cr": "CR-2"}]
    if variant == "closed":
        crs[1]["notes"] = [f"merged: {link(13)}"]
        events = [{"kind": "ship", "cr": "CR-2", "pr": link(12)}, {"kind": "ship", "cr": "CR-2", "pr": link(13)},
                  {"kind": "order", "order_kind": "merged", "actor": "foreman", "cr": "CR-2"}]
    data = {"created": "2026-11-14T10:00:00", "crs": crs, "release": True, "settings": {"default_branch": "main"}}
    return data, events

green = [{"name": "t", "conclusion": "SUCCESS"}]
red = [{"name": "t", "conclusion": "FAILURE"}]
def views(variant):
    def v(state, roll): return {"title": f"{PFX} x", "state": state, "baseRefName": "main", "autoMergeRequest": None,
                                "statusCheckRollup": roll, "headRefOid": "a" * 40, "mergedAt": "2026-11-14T11:00:00Z"}
    m = {"11": v("MERGED", green), "12": v("MERGED", green), "13": v("MERGED", green)}
    if variant == "closed": m["12"] = v("CLOSED", red)
    return m

def run(modname, path, variant):
    a = load(modname, path)
    data, events = make(variant); vs = views(variant)
    a.forge_view = lambda l: (vs[l.rsplit("/", 1)[-1]], "")
    listing = [{"number": n, "title": t, "mergedAt": d} for n, t, d in
               [(11, PFX + " a", "2026-11-14T11:00:00Z"), (12, PFX + " r", "2026-11-14T12:00:00Z"),
                (13, PFX + " r2", "2026-11-14T13:00:00Z"), (5, "[eval 8 2026-11-01 full] old", "2026-11-01T11:00:00Z")]]
    listing = [x for x in listing if x["number"] != (12 if variant == "closed" else 13)]
    a.run_cmd = lambda cmd, cwd=None, timeout=90: (True, json.dumps(listing))
    chk = a.Checks(scored=False)
    run_rec = {"prefix": PFX, "repository": REPO}
    a.sandbox_checks(data, events, run_rec, chk)
    print(f"--- {modname} / {variant}")
    for ok, label, rail in chk.items:
        print({True: "PASS", False: "FAIL", None: "NOT SEEN"}[ok], label)
    if hasattr(a, "batch_prs"):
        print("batch_prs =", json.dumps(a.batch_prs(data, events)))

run("audit_old", S / "audit_old.py", "base")
run("audit_new", WT / "audit.py", "base")
run("audit_new2", WT / "audit.py", "closed")

