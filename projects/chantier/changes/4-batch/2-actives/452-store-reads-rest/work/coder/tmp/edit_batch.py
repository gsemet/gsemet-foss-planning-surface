from editlib import Editor

e = Editor("core/batch.py")
r = e.r
r(
    "    if not source.is_dir():\n        raise ChantierError(f\"CR folder not found: {source}\", EXIT_USAGE)",
    "    if not repo.store.is_dir(rel_in(repo.store.root, source)):\n        raise ChantierError(f\"CR folder not found: {source}\", EXIT_USAGE)",
)
r(
    "        if path.exists():\n            if self._create",
    "        if self.repo.store.exists(rel_in(self.repo.store.root, path)):\n            if self._create",
)
r(
    "            if gone.exists():\n",
    "            if self.repo.store.exists(rel_in(self.repo.store.root, gone)):\n",
)
r(
    "            if not destination.exists() or source.exists():",
    "            store = self.repo.store\n            if not store.exists(rel_in(store.root, destination)) or store.exists(\n                rel_in(store.root, source)\n            ):",
)
r(
    "    children = [c for root in roots if root.is_dir() for c in root.iterdir() if c.is_dir()]\n    for child in children:\n        name = re.sub(r\"^(?:\\d{6}-\\d{4}-)+\", \"\", child.name)  # the date is no number",
    "    store = repo.store\n    children: list[str] = []\n    for root in roots:\n        rel = rel_in(store.root, root)\n        if store.is_dir(rel):\n            children += [n for n in store.listdir(rel) if store.is_dir(f\"{rel}/{n}\")]\n    for child in children:\n        name = re.sub(r\"^(?:\\d{6}-\\d{4}-)+\", \"\", child)  # the date is no number",
)
e.save()
e = Editor("core/batch.py")
e.r("    LOCK_TIMEOUT_S,\n    try_lock,", "    LOCK_TIMEOUT_S,\n    rel_in,\n    try_lock,")
e.save()
