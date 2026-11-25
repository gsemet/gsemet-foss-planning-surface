"""Show what the prose check says when S5 uses the specification's angle brackets (scratch copy `h`)."""

import subprocess
from pathlib import Path

head = Path(__file__).parent / "h"
doc = head / "requirements/tiers/swrs/core/SwRS-OKFSCHEMA-CORE-006.md"


def validate(label: str) -> None:
    done = subprocess.run(
        ["okfreq", "validate", str(head / "requirements"), "--prose"],
        capture_output=True, text=True, encoding="utf-8", errors="replace",
    )
    out = (done.stdout + done.stderr).replace(str(head), "<scratch>").replace(head.as_posix(), "<scratch>")
    print(f"--- {label}: okfreq validate requirements --prose -> exit {done.returncode}")
    print(out.strip())


validate("S5 as at head (braces)")
text = doc.read_text(encoding="utf-8")
changed = text.replace("{producer}/{version}", "<producer>/<version>").replace(
    "{prefix}:{identifier}", "<prefix>:<identifier>"
)
assert changed != text
doc.write_text(changed, encoding="utf-8", newline="\n")
validate("S5 with the specification's angle brackets")
