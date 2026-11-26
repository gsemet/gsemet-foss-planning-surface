"""Point the grep checks at phrases the edited cards hold now (inventory rows only)."""

import sys
from pathlib import Path

EVIDENCE = Path(__file__).resolve().parents[2] / "evidence"

# (inventory, card, old phrase) -> new phrase, or {row id: new phrase}
MOVES = {
    ("cards-inventory-chief-of-staff.md", "ticket-summary-example.md", "Closes #336"): "Closes #<n>",
}
H = "cards-inventory-host-and-shared.md"
for old, new in (
    (": a typed wait of a CR", ": what a CR waits for"),
    (": a short claim on a unit", ": a numbered 10-minute claim"),
    ("s folder in an external planning surface", "is where chantier writes everything"),
    ("is written only when a CR needs the result", "only when a CR needs the result"),
    ("s Chief of Staff session.", "Chief of Staff session (its session id"),
    ("The prompt is the whole brief:", "The prompt is the whole brief; it names the card"),
    ("No escalation printed: the trigger takes", "the trigger takes its usual route"),
):
    MOVES[(H, "concepts.md", old)] = new
MOVES[(H, "release-template.md", ": it undoes a mistake of an earlier release;")] = (
    "it undoes a mistake of an earlier release (a revert"
)
MOVES[(H, "release-template.md", ": nothing the user sees changes.")] = (
    "nothing the user sees changes (tooling, tests, docs process)"
)
MOVES[(H, "release-driver.md", "keep or upload an image that shows the")] = (
    "keep or upload an image showing the username or home folder"
)
MOVES[(H, "review-step.md", "A review the project added to the team.")] = (
    "A review the project added to the team in its"
)
MOVES[(H, "forges/github.md", "the forge hub reads the PRs a running batch")] = (
    "the forge hub reads only the PRs a running batch"
)
MOVES[(H, "forges/gitlab.md", "the forge hub reads the MRs a running batch")] = (
    "the forge hub reads only the MRs a running batch"
)

# Rows whose new phrase names their own definition rather than the group's.
ROWS = {
    "H-078": "is a git repository of its own, one folder per project",
    "H-079": "holds its own rules",
    "H-091": "whether the archive is also in the PR",
    "H-094": "complete and self-contained",
    "H-095": "by default) says what the CR must do",
}


def main() -> None:
    dry = "--apply" not in sys.argv
    for name in sorted({key[0] for key in MOVES}):
        path = EVIDENCE / name
        raw = path.read_bytes()
        lines = raw.decode("utf-8-sig").split("\n")
        changed = 0
        for index, line in enumerate(lines):
            for (inventory, card, old), new in MOVES.items():
                if inventory != name or "grep" not in line:
                    continue
                needle = f"'{old}' {card}"
                if needle not in line:
                    continue
                row = line.split("|")[1].strip()
                phrase = ROWS.get(row, new)
                assert "'" not in phrase, phrase
                lines[index] = line = line.replace(needle, f"'{phrase}' {card}")
                changed += 1
                print(f"{name}:{index + 1} {row} -> {phrase}")
        print(f"{name}: {changed} rows")
        if changed and not dry:
            bom = b"\xef\xbb\xbf" if raw.startswith(b"\xef\xbb\xbf") else b""
            path.write_bytes(bom + "\n".join(lines).encode("utf-8"))


main()
