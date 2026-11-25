from pathlib import Path

path = Path("C:/Users/gaeta/Projets/gsemet-foss-planning-surface/projects/chantier/changes/4-batch/"
            "2-actives/507-sc21-cards-foreman/evidence/cards-inventory-foreman.md")
text = path.read_bytes().decode("utf-8")
old = "grep 'merge-tree" + chr(92) * 2 + "|git:' "
print(text.count(old))
path.write_bytes(text.replace(old, "grep -c 'Your only git' ").encode("utf-8"))
