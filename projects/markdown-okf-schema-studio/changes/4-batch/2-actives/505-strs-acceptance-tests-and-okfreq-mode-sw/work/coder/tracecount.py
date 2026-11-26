"""Count trust SwRS scenarios without a tests marker, from the okfreq trace JSON."""

import glob
import json
import os
import re
import sys

root, trace_path = sys.argv[1], sys.argv[2]
with open(trace_path, encoding="utf-8") as handle:
    markers = json.load(handle)["scenario_markers"]
covered = {(m["id"], m["fragment"]) for m in markers if m["marker"] == "tests"}
total = 0
missing = []
pattern = os.path.join(root, "requirements/tiers/swrs/trust-security/SwRS-*.md")
for path in sorted(glob.glob(pattern)):
    with open(path, encoding="utf-8") as handle:
        front = handle.read().split("---")[1]
    lifecycle = re.search(r"req_lifecycle: (\S+)", front).group(1)
    if lifecycle in ("deprecated", "superseded") or "annotation_exemption: true" in front:
        continue
    ident = re.search(r"^id: (\S+)", front, re.M).group(1)
    for scenario in re.findall(r"^- id: (S\d+)", front, re.M):
        total += 1
        if (ident, scenario) not in covered:
            missing.append(f"{ident}#{scenario}")
print("trace: trust SwRS scenarios", total, "without a tests marker", len(missing), missing)
for kind in ("tests", "accepts"):
    got = sorted({f'{m["id"][-9:]}#{m["fragment"]}' for m in markers
                  if m["marker"] == kind and m["id"].startswith("StRS") and "-TRUST-" in m["id"]})
    print("trace:", kind, "markers on trust StRS paths", got)
