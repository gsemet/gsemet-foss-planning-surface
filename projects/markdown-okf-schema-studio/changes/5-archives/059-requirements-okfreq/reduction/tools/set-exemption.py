#!/usr/bin/env python3
"""Exempt superseded and archived requirements from traceability markers."""
import pathlib
import re
import sys


def run(wt):
    root = pathlib.Path(wt) / "requirements" / "tiers"
    changed = 0
    for path in sorted(root.glob("s*rs/*/*.md")):
        text = path.read_text(encoding="utf-8")
        head, sep, body = text.partition("\n---\n")
        life = re.search(r"^lifecycle: (\S+)$", head, re.M)
        if not life or life.group(1) not in ("superseded", "deprecated"):
            continue
        if re.search(r"^annotation_exemption: true$", head, re.M):
            continue
        by = re.search(r"^superseded_by: (\S+)$", head, re.M)
        if life.group(1) == "superseded" and by:
            reason = f"Superseded by {by.group(1)}; no marker expected."
        else:
            reason = "Archived. Not an observable behaviour; no marker expected."
        head = re.sub(r"^exemption_reason:.*\n(?:  .*\n)*", "", head + "\n", flags=re.M).rstrip("\n")
        line = f'annotation_exemption: true\nexemption_reason: "{reason}"'
        if re.search(r"^annotation_exemption: false$", head, re.M):
            head = re.sub(r"^annotation_exemption: false$", line, head, count=1, flags=re.M)
        else:
            head = re.sub(r"^(tier: .*)$", lambda m: m.group(1) + "\n" + line, head, count=1, flags=re.M)
        path.write_text(head + sep + body, encoding="utf-8")
        changed += 1
    return changed


if __name__ == "__main__":
    print(f"exempted {run(sys.argv[1])} files")
