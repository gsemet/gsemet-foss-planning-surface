"""Verifier of CR-505: which parts of each changed requirement file differ between two commits.

usage: python -I reqdiff.py <repo> <base> <head>
"""
import re
import subprocess
import sys

repo, base, head = sys.argv[1:4]


def git(*args):
    return subprocess.run(["git", "-C", repo, *args], capture_output=True, check=True).stdout.decode("utf-8")


def parts(text):
    text = text.replace("\r\n", "\n")
    front, body = text.split("\n---\n", 1)
    fields, key = {}, None
    for line in front.split("\n")[1:]:
        m = re.match(r"([a-z_]+):", line)
        if m:
            key = m.group(1)
            fields[key] = line
        elif key:
            fields[key] += "\n" + line
    body = body.split("<!-- okf:links:start -->")[0]
    sections, name = {}, "(title)"
    for line in body.split("\n"):
        if line.startswith("### "):
            name = line[4:]
        sections[name] = sections.get(name, "") + line + "\n"
    notes = sections.pop("Verification notes", "")
    criteria = "\n".join(l for l in notes.split("\n") if l.startswith("- Criteria"))
    method = "\n".join(l for l in notes.split("\n") if not l.startswith("- Criteria"))
    return fields, sections, method.strip(), criteria.strip()


changed = [f for f in git("diff", "--name-only", f"{base}..{head}", "--", "requirements").split("\n") if f]
print("changed files under requirements:", len(changed))
groups = {}
for f in changed:
    if not re.search(r"(SwRS|StRS)-MDOKFSTUDIO-[A-Z]+-\d+\.md$", f):
        print("other:", f)
        continue
    a, b = parts(git("show", f"{base}:{f}")), parts(git("show", f"{head}:{f}"))
    fields = sorted(k for k in set(a[0]) | set(b[0]) if a[0].get(k) != b[0].get(k))
    sections = sorted(k for k in set(a[1]) | set(b[1]) if a[1].get(k) != b[1].get(k))
    what = []
    if [k for k in fields if k != "tested_in_files" and k != "implemented_in_files"]:
        what.append("frontmatter " + ",".join(k for k in fields if k not in ("tested_in_files", "implemented_in_files")))
    if sections:
        what.append(f"requirement text: {sections}")
    if a[2] != b[2]:
        what.append("verification notes")
    if a[3] != b[3]:
        what.append("criteria")
    if not what:
        what.append("generated file lists only (" + ",".join(fields) + ")")
    groups.setdefault(" + ".join(what), []).append(f.rsplit("/", 1)[1][:-3].replace("-MDOKFSTUDIO", ""))
for what, names in sorted(groups.items()):
    print(f"{len(names):3d}  {what}\n     {' '.join(names)}")
text = [n for w, ns in groups.items() if "requirement text" in w for n in ns]
notes = [n for w, ns in groups.items() if "verification notes" in w or "criteria" in w for n in ns]
print("requirement files with changed requirement text:", len(text))
print("requirement files with changed verification notes or criteria:", len(notes), sorted(notes))
