"""Fix inventory check phrases that never matched their card (commas dropped; an escaped regex)."""

from pathlib import Path

EV = Path("C:/Users/gaeta/Projets/gsemet-foss-planning-surface/projects/chantier/changes/4-batch/"
          "2-actives/507-sc21-cards-foreman/evidence")
FIX = {
    "chief-of-staff": [("grep -c 'Widen a grant or approv' ", "grep -c 'Widen a grant, or approve' "),
                       ("grep -c 'Grill specify triage or' ", "grep -c 'Grill, specify, triage' ")],
    "griller": [("grep -c 'Grill specify or triage' ", "grep -c 'Grill, specify or triage' ")],
    "foreman": [("grep 'merge-tree\\|git:' ", "grep -c 'Your only git' ")],
}
for inv, pairs in FIX.items():
    path = EV / f"cards-inventory-{inv}.md"
    text = path.read_bytes().decode("utf-8")
    for old, new in pairs:
        print(inv, text.count(old), repr(old), "->", repr(new))
        text = text.replace(old, new)
    path.write_bytes(text.encode("utf-8"))
