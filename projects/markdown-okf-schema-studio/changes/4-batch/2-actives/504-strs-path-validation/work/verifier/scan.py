"""Read-only scan of the requirement bundle and markers at a git revision (no checkout)."""
import collections
import re
import subprocess
import sys

import yaml

REPO = sys.argv[1]
REV = sys.argv[2]


def git(*args):
    return subprocess.run(["git", "-C", REPO, *args], capture_output=True, check=True).stdout


def blobs(rev, paths):
    proc = subprocess.run(
        ["git", "-C", REPO, "cat-file", "--batch"],
        input="".join(f"{rev}:{p}\n" for p in paths).encode(),
        capture_output=True,
        check=True,
    ).stdout
    out, i = {}, 0
    for p in paths:
        nl = proc.index(b"\n", i)
        size = int(proc[i:nl].split()[-1])
        out[p] = proc[nl + 1 : nl + 1 + size].decode("utf-8", "replace")
        i = nl + 1 + size + 1
    return out


files = git("ls-tree", "-r", "--name-only", "-z", REV).decode().split("\0")
files = [f for f in files if f]
req_files = [
    f
    for f in files
    if f.startswith("requirements/tiers/") and re.search(r"/(StRS|SwRS)-[A-Z0-9-]+\.md$", f)
]
reqs = {}
for path, text in blobs(REV, req_files).items():
    m = re.match(r"^---\r?\n(.*?)\r?\n---\r?\n(.*)$", text, re.S)
    fm = yaml.safe_load(m.group(1))
    rid = path.rsplit("/", 1)[1][:-3]
    reqs[rid] = {"fm": fm, "body": m.group(2), "path": path}


def retired(r):
    return r["fm"].get("req_lifecycle") in ("superseded", "deprecated")


CODE = re.compile(r"\.(ts|tsx|js|mjs|cjs|py|css|html|sh|yml|yaml|ps1)$")
code_files = [
    f for f in files if CODE.search(f) and f.split("/")[0] in ("src", "test", "tests", "scripts", "sphinx", "skills")
]
MARK = re.compile(r"@(tests_req|accepts_req|implements_req)\s+((?:StRS|SwRS)-MDOKFSTUDIO-[A-Z]+-\d+)(#[A-Za-z0-9_]+)?")
markers = []
for path, text in blobs(REV, code_files).items():
    for n, line in enumerate(text.split("\n"), 1):
        for m in MARK.finditer(line):
            if m.group(2) in reqs:
                markers.append((path, n, m.group(1), m.group(2), (m.group(3) or "")[1:], line.strip()))

live_strs = [k for k, r in reqs.items() if k.startswith("StRS") and not retired(r)]
live_swrs = [k for k, r in reqs.items() if k.startswith("SwRS") and not retired(r)]
exempt = [k for k in live_swrs if reqs[k]["fm"].get("annotation_exemption")]
nonex = [k for k in live_swrs if k not in exempt]
retired_all = [k for k, r in reqs.items() if retired(r)]
print(f"rev {REV}: requirements {len(reqs)}; live StRS {len(live_strs)}; live SwRS {len(live_swrs)} "
      f"(non-exempt {len(nonex)}, exempt {len(exempt)}: {sorted(exempt)}); retired {len(retired_all)}")

bad = []
decl = {}
for k, r in reqs.items():
    sc = r["fm"].get("scenarios")
    if sc is not None:
        if not sc:
            bad.append((k, "empty scenarios"))
        ids = [e.get("id") for e in sc]
        if any(set(e) != {"id", "title"} for e in sc):
            bad.append((k, "keys"))
        if len(set(ids)) != len(ids) or any(not re.fullmatch(r"S[1-9][0-9]*", str(i)) for i in ids):
            bad.append((k, "ids"))
        decl[k] = {e["id"]: e["title"] for e in sc}
    # fenced blocks are ignored for headings
    body = re.sub(r"^(```+|~~~+).*?^\1\s*$", "", r["body"], flags=re.S | re.M)
    if k.startswith("StRS"):
        heads = re.findall(r"^####\s+Path\s+(\S+?):\s*(.*?)\s*$", body, re.M)
        oldn = re.findall(r"^####\s+Path\s+[0-9].*$", body, re.M)
    else:
        heads = [(a, c) for a, b, c in re.findall(r"^###\s+Scenario\s+(S\d+)(\s+\([^)]*\))?:\s*(.*?)\s*$", body, re.M)]
        oldn = re.findall(r"^###\s+Scenario(?::| \().*$", body, re.M)
    live = not retired(r)
    if live and not r["fm"].get("annotation_exemption" if k.startswith("SwRS") else "_none"):
        if sc is None:
            bad.append((k, "live non-exempt without scenarios"))
        else:
            got = [(i, t) for i, t in heads]
            want = [(e["id"], str(e["title"])) for e in sc]
            if [g[0] for g in got] != [w[0] for w in want]:
                bad.append((k, f"heading ids {[g[0] for g in got]} != {[w[0] for w in want]}"))
            elif got != want:
                bad.append((k, f"heading titles {got} != {want}"))
        if oldn:
            bad.append((k, f"old heading {oldn}"))
        if sc and [e["id"] for e in sc] != [f"S{i}" for i in range(1, len(sc) + 1)]:
            bad.append((k, f"ids not S1.. in order {[e['id'] for e in sc]}"))
    elif sc is not None:
        bad.append((k, "scenarios on retired/exempt"))
print(f"declaration problems: {len(bad)}")
for b in bad[:60]:
    print("  ", b)

print("live StRS with scenarios:", sum(k in decl for k in live_strs), "/", len(live_strs))
print("live non-exempt SwRS with scenarios:", sum(k in decl for k in nonex), "/", len(nonex))
print("approved SwRS:", [k for k, r in reqs.items() if k.startswith("SwRS") and r["fm"].get("approved_by")])
ret_noex = [k for k in retired_all if k.startswith("SwRS") and not (reqs[k]["fm"].get("annotation_exemption") and str(reqs[k]["fm"].get("exemption_reason") or "").strip())]
print("retired SwRS without exemption+reason:", len(ret_noex))

# marker rules (spec Evidence check 5)
D7 = {f"StRS-MDOKFSTUDIO-{t}" for t in ("CORE-007", "CORE-008", "TRUST-014")}
viol = collections.defaultdict(list)
tm = [m for m in markers if m[2] != "implements_req"]
print(f"marker lines: tests {sum(m[2]=='tests_req' for m in markers)}, accepts {sum(m[2]=='accepts_req' for m in markers)}, implements {sum(m[2]=='implements_req' for m in markers)}")
for p, n, verb, rid, frag, line in markers:
    where = f"{p}:{n} {verb} {rid}#{frag}"
    if verb == "implements_req":
        if frag:
            viol["implements fragment"].append(where)
        continue
    if verb == "tests_req" and rid.startswith("StRS") and not frag:
        viol["tests StRS without fragment"].append(where)
    if verb == "tests_req" and rid.startswith("StRS") and p.startswith("test/integration/"):
        viol["tests StRS under integration"].append(where)
    if verb == "accepts_req" and not p.startswith("test/integration/") and rid not in D7:
        viol["accepts outside integration, not D7"].append(where)
    if verb == "accepts_req" and rid.startswith("SwRS"):
        viol["accepts on SwRS"].append(where)
    if rid in decl and not frag:
        viol["fragmentless on declaring target"].append(where)
    if rid in decl and frag and frag not in decl[rid]:
        viol["undeclared fragment"].append(where)
    if rid not in decl and frag:
        viol["fragment on non-declaring target"].append(where)
for k in ("tests StRS without fragment", "tests StRS under integration", "accepts outside integration, not D7",
          "accepts on SwRS", "fragmentless on declaring target", "undeclared fragment",
          "fragment on non-declaring target", "implements fragment"):
    v = viol.get(k, [])
    print(f"  {k}: {len(v)}")
    for x in v[:15]:
        print("      ", x)

marked = collections.defaultdict(set)
for p, n, verb, rid, frag, line in markers:
    if verb != "implements_req" and frag:
        marked[rid].add(frag)
sw_total = sw_un = st_total = st_un = 0
gs = collections.Counter()
gt = collections.Counter()
for k in nonex:
    for i in decl.get(k, {}):
        sw_total += 1
        if i not in marked[k]:
            sw_un += 1
            gs[k.split("-")[2]] += 1
for k in live_strs:
    for i in decl.get(k, {}):
        st_total += 1
        if i not in marked[k]:
            st_un += 1
            gt[k.split("-")[2]] += 1
print(f"SwRS scenarios {sw_total}, unmarked {sw_un}: {', '.join(f'{g} {n}' for g, n in sorted(gs.items()))}")
print(f"StRS paths {st_total}, unmarked {st_un}: {', '.join(f'{g} {n}' for g, n in sorted(gt.items()))}")
acc = {rid for p, n, verb, rid, frag, line in markers if verb == "accepts_req" and rid.startswith("StRS")}
print("live StRS with no @accepts_req:", sum(k not in acc for k in live_strs))
print("StRS paths accepted:", len({(m[3], m[4]) for m in markers if m[2] == "accepts_req" and m[3] in live_strs}),
      "StRS paths tested (tests_req):", len({(m[3], m[4]) for m in markers if m[2] == "tests_req" and m[3] in live_strs}))
print("LIFE-023:", decl.get("StRS-MDOKFSTUDIO-LIFE-023"), [m[:5] for m in markers if m[3] == "StRS-MDOKFSTUDIO-LIFE-023"])
for t in ("BLOCK-027", "TRUST-012", "TRUST-014"):
    print(t, decl.get(f"StRS-MDOKFSTUDIO-{t}"), [(m[0], m[1], m[2], m[4]) for m in markers if m[3] == f"StRS-MDOKFSTUDIO-{t}"])

# SwRS with a test marker per revision, for comparison between revisions
withtest = sorted({rid for p, n, verb, rid, frag, line in markers if verb != "implements_req" and rid in live_swrs and (p.startswith("test") or p.startswith("sphinx/tests"))})
print("live SwRS with a test marker:", len(withtest))
if len(sys.argv) > 3:
    import json
    json.dump({"with": withtest, "markers": markers, "live_swrs": live_swrs, "live_strs": live_strs,
               "decl": decl}, open(sys.argv[3], "w", encoding="utf-8"))
