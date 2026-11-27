"""Compare every requirement file between base and head, ignoring the mechanical migration."""
import collections
import re
import subprocess
import sys

import yaml

REPO, BASE, HEAD = sys.argv[1:4]


def git(*args):
    return subprocess.run(["git", "-C", REPO, *args], capture_output=True, check=True).stdout


def blobs(rev, paths):
    proc = subprocess.run(["git", "-C", REPO, "cat-file", "--batch"],
                          input="".join(f"{rev}:{p}\n" for p in paths).encode(),
                          capture_output=True, check=True).stdout
    out, i = {}, 0
    for p in paths:
        nl = proc.index(b"\n", i)
        size = int(proc[i:nl].split()[-1])
        out[p] = proc[nl + 1:nl + 1 + size].decode("utf-8").replace("\r\n", "\n")
        i = nl + 1 + size + 1
    return out


def reqs(rev):
    fs = [f for f in git("ls-tree", "-r", "--name-only", "-z", rev, "requirements/tiers").decode().split("\0")
          if re.search(r"/(StRS|SwRS)-[A-Z0-9-]+\.md$", f)]
    out = {}
    for p, t in blobs(rev, fs).items():
        m = re.match(r"^---\n(.*?)\n---\n(.*)$", t, re.S)
        out[p.rsplit("/", 1)[1][:-3]] = (yaml.safe_load(m.group(1)), m.group(2), p)
    return out


b, h = reqs(BASE), reqs(HEAD)
print("added:", sorted(set(h) - set(b)), "removed:", sorted(set(b) - set(h)))
d5 = []
fmkeys = collections.Counter()
bodyother = []
headingprob = []
approved = []
for k in sorted(set(b) & set(h)):
    (bf, bb, p), (hf, hb, _) = b[k], h[k]
    changed = {x for x in set(bf) | set(hf) if bf.get(x) != hf.get(x)}
    for c in changed:
        fmkeys[(k[:4], c)] += 1
    if hf.get("annotation_exemption") and not bf.get("annotation_exemption"):
        d5.append((k, bf.get("req_lifecycle"), hf.get("superseded_by"), hf.get("exemption_reason"), bf.get("approved_by")))
    if bf.get("approved_by") or hf.get("approved_by"):
        approved.append((k, bf.get("req_lifecycle"), bf.get("approved_by"), hf.get("approved_by"),
                         str(bf.get("approved_at")), str(hf.get("approved_at")), sorted(changed),
                         str((hf.get("verified") or {}).get("at"))))
    # headings: strip the S<n> id and compare bodies
    pat_s = r"^(###\s+Scenario)\s+S\d+" if k.startswith("SwRS") else r"^(####\s+Path)\s+S(\d+)"
    if bb != hb:
        if k.startswith("SwRS"):
            norm = re.sub(pat_s, r"\1", hb, flags=re.M)
            if norm != bb:
                bodyother.append(k)
        else:
            # old StRS headings are "Path <n>", ids follow them; LIFE-023 renumbers from 0
            off = 1 if k.endswith("LIFE-023") else 0
            norm = re.sub(pat_s, lambda m: f"{m.group(1)} {int(m.group(2)) - off}", hb, flags=re.M)
            if norm != bb:
                bodyother.append(k)
    # titles: base heading order equals head order
    if "scenarios" in hf:
        if k.startswith("SwRS"):
            old = re.findall(r"^###\s+Scenario(\s+\([^)]*\))?:\s*(.*?)\s*$", bb, re.M)
            new = re.findall(r"^###\s+Scenario\s+S\d+(\s+\([^)]*\))?:\s*(.*?)\s*$", hb, re.M)
        else:
            old = re.findall(r"^####\s+Path\s+\d+():\s*(.*?)\s*$", bb, re.M)
            new = re.findall(r"^####\s+Path\s+S\d+():\s*(.*?)\s*$", hb, re.M)
        if old != new[:len(old)] or len(new) != len(old):
            headingprob.append((k, len(old), len(new), old != new[:len(old)]))

print("frontmatter keys changed:")
for kk, n in sorted(fmkeys.items()):
    print("  ", kk, n)
print("D5 newly exempt:", len(d5), "by lifecycle", dict(collections.Counter(x[1] for x in d5)), "approved among them:", [x[0] for x in d5 if x[4]])
bad = []
for k, lc, sb, reason, _ in d5:
    r = str(reason or "")
    if lc == "superseded":
        ok = r.startswith("Superseded by SwRS-") and all(x in r for x in (sb or []))
    else:
        ok = r.startswith("Archived. ") and len(r) > 12
    if not ok:
        bad.append((k, lc, sb, r))
print("D5 reasons not in the specified form:", len(bad))
for x in bad[:12]:
    print("  ", x)
print("D5 reason samples:")
for k, lc, sb, reason, _ in d5[:3] + [x for x in d5 if x[1] == "deprecated"]:
    print("  ", k, lc, sb, "|", reason)
print("approved requirements:", len(approved))
for a in approved:
    print("  ", a)
print("bodies differing beyond the heading ids:", len(bodyother))
for k in bodyother:
    print("  ", k, h[k][0].get("req_lifecycle"))
print("heading list differences (count old, new, retitled):", len(headingprob))
for x in headingprob:
    print("  ", x)
descch = [k for k in set(b) & set(h) if any(b[k][0].get(f) != h[k][0].get(f) for f in ("description", "title", "req_lifecycle", "derives_from", "user_need"))]
print("title/description/lifecycle/derives_from/user_need changed:", sorted(descch))
