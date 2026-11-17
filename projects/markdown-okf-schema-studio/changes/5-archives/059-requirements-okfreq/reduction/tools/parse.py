# Parse every okfreq requirement into one JSON file.
import json, re, sys, pathlib, yaml
root = pathlib.Path(sys.argv[1]) / "requirements/tiers"
out = []
for f in sorted(root.glob("*/*/*.md")):
    if f.name == "index.md": continue
    t = f.read_text()
    m = re.match(r"^---\n(.*?)\n---\n(.*)$", t, re.S)
    fm = yaml.safe_load(m.group(1)); body = m.group(2)
    scen = re.findall(r"### Scenario: (.*?)\n(.*?)(?=\n### |\Z)", body, re.S)
    ver = re.search(r"### Verification notes\n(.*?)(?=\n### |\Z)", body, re.S)
    ki = re.findall(r"Known issue[^\n]*", body)
    out.append(dict(id=fm["id"], type=fm["type"], scope=fm["scope"], lifecycle=fm["lifecycle"],
        title=fm["title"], description=" ".join(str(fm["description"]).split()),
        derives_from=fm.get("derives_from") or [], derived_by=fm.get("derived_by") or [],
        impl=fm.get("implemented_in_files") or [], tests=fm.get("tested_in_files") or [],
        exempt=fm.get("annotation_exemption"), scenarios=[s[0] for s in scen],
        scenario_text=[" ".join(s[1].split()) for s in scen],
        verification=" ".join(ver.group(1).split()) if ver else "", known_issue=bool(ki),
        body_len=len(body)))
json.dump(out, open(sys.argv[2], "w"), indent=1)
print(len(out))
