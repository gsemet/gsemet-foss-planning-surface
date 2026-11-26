"""Rows naming a reading file as a topic name its topic instead (the file in brackets)."""

from pathlib import Path

path = Path("C:/Users/gaeta/Projets/gsemet-foss-planning-surface/projects/chantier/changes/4-batch/"
            "2-actives/507-sc21-cards-foreman/evidence/cards-inventory-foreman.md")
text = path.read_bytes().decode("utf-8")
for name, topic in (("lease-steering", "lease"), ("refused-push-steering", "refused-push")):
    old = f"topic {name} | help {name} |"
    new = f"topic {topic} (`topics/{name}.md`) | help {topic} |"
    print(name, text.count(old))
    text = text.replace(old, new)
path.write_bytes(text.encode("utf-8"))
