"""Compare the merged visual campaign of the head run with the base run's, reading the zips only."""

import collections
import hashlib
import json
import sys
import zipfile

base_zip, head_zip = sys.argv[1], sys.argv[2]


def digest(path):
    sha = hashlib.sha256()
    with open(path, "rb") as stream:
        for block in iter(lambda: stream.read(1 << 20), b""):
            sha.update(block)
    return sha.hexdigest()


def load(archive, name):
    return json.loads(archive.read(name).decode("utf-8"))


base = zipfile.ZipFile(base_zip)
head = zipfile.ZipFile(head_zip)
print("base zip sha256", digest(base_zip))
print("head zip sha256", digest(head_zip))


def find(archive, suffix):
    return [name for name in archive.namelist() if name.endswith(suffix)]


print("head manifests", find(head, "run-manifest.json") + [n for n in head.namelist() if "run-manifest.part" in n or "run-manifest.partial" in n])
print("base manifests", find(base, "run-manifest.json") + [n for n in base.namelist() if "run-manifest.part" in n])
hm = load(head, "e2e/screenshots/run-manifest.json")
bm = load(base, "e2e/screenshots/run-manifest.json")
keys = ["runId", "campaignStartedAt", "startedAt", "completedAt", "revision", "status", "partial", "parts", "scenarioCount",
        "pngCount", "stepPngCount", "screenshotCount", "passedScenarioCount", "failedScenarioCount", "failureCount",
        "duplicateImages", "workerCount", "worktreeStatus"]
for key in keys:
    value_head = hm.get(key)
    value_base = bm.get(key)
    if isinstance(value_head, list) and key == "duplicateImages":
        value_head, value_base = len(value_head), len(value_base)
    print(f"{key:22} base={value_base!r} head={value_head!r}")
print("manifest keys only in head", sorted(set(hm) - set(bm)), "only in base", sorted(set(bm) - set(hm)))

hr = {r["id"]: r for r in hm["results"]}
br = {r["id"]: r for r in bm["results"]}
print("results head", len(hm["results"]), "unique", len(hr), "base", len(bm["results"]), "unique", len(br))
print("ids only in base", sorted(set(br) - set(hr)))
print("ids only in head", sorted(set(hr) - set(br)))
print("same order", [r["id"] for r in hm["results"]] == [r["id"] for r in bm["results"]])
print("head statuses", dict(collections.Counter(r["status"] for r in hm["results"])))


def captures(result):
    return sorted(c["file"] for c in result.get("captures", []))


def checks(result):
    return sorted((c["id"], c["applicable"], c["pass"]) for c in (result.get("finalState", {}).get("machineChecks") or []))


for label, function in (("capture files", captures), ("machine checks (id, applicable, pass)", checks),
                        ("capture flag", lambda r: bool(r.get("capture"))), ("status", lambda r: r["status"]),
                        ("assertion keys", lambda r: sorted(r.keys()))):
    different = [i for i in br if i in hr and function(br[i]) != function(hr[i])]
    print(f"scenarios whose {label} differ: {len(different)} {different[:5]}")
print("machine check rows total base", sum(len(checks(r)) for r in br.values()), "head", sum(len(checks(r)) for r in hr.values()))

head_pngs = {n for n in head.namelist() if n.startswith("e2e/screenshots/visual/") and n.endswith(".png")}
base_pngs = {n for n in base.namelist() if n.startswith("e2e/screenshots/visual/") and n.endswith(".png")}
print("visual PNG files base", len(base_pngs), "head", len(head_pngs), "only base", len(base_pngs - head_pngs), "only head", len(head_pngs - base_pngs))
referenced = {"e2e/screenshots/" + c["file"] for r in hm["results"] for c in r.get("captures", [])}
print("head referenced captures", len(referenced), "missing from zip", len(referenced - set(head.namelist())))
hashes = collections.defaultdict(list)
for name in sorted(referenced):
    hashes[hashlib.sha256(head.read(name)).hexdigest()].append(name)
print("identical referenced PNG groups in head", [v for v in hashes.values() if len(v) > 1])
for prefix in ("breakout/", "visual/first-gap/", "visual/width-margins/", "e2e/screenshots/"):
    b = [n for n in base.namelist() if n.startswith(prefix) and not n.endswith("/")]
    h = [n for n in head.namelist() if n.startswith(prefix) and not n.endswith("/")]
    only_b = sorted(set(b) - set(h))
    only_h = sorted(set(h) - set(b))
    print(f"{prefix:24} base {len(b)} head {len(h)} only-base {len(only_b)} {only_b[:4]} only-head {len(only_h)} {only_h[:8]}")
print("breakout files head", [n for n in head.namelist() if n.startswith("breakout/")][:8])
for name in ("e2e/screenshots/MACHINE-CHECKS.md", "e2e/screenshots/INDEX.md"):
    h = head.read(name).decode("utf-8").splitlines()
    b = base.read(name).decode("utf-8").splitlines()
    print(name, "lines base", len(b), "head", len(h))
    delta = [(x, y) for x, y in zip(b, h) if x != y]
    print("  differing lines", len(delta), delta[:3])
print("campaign file head", load(head, "e2e/campaign-visual.json"))
print("review index files head", [n for n in head.namelist() if n in ("e2e/REVIEW.md", "e2e/e2e-manifest.json", "e2e/GALLERY.md")])
if "e2e/e2e-manifest.json" in head.namelist():
    manifest = load(head, "e2e/e2e-manifest.json")
    print("e2e-manifest", {k: v for k, v in manifest.items() if not isinstance(v, (list, dict))}, "keys", list(manifest))
    print("  stages", json.dumps(manifest.get("stages"))[:900])
