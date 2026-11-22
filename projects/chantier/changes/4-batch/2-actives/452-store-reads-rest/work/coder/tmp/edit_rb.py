from editlib import Editor

e = Editor("lifecycle/running_batch.py")
r = e.r
r(
    "from chantier.core.errors import EXIT_PRECONDITION, EXIT_USAGE, ChantierError\nfrom chantier.core.repo import Repo\n",
    "from chantier.core.errors import EXIT_PRECONDITION, EXIT_USAGE, ChantierError\nfrom chantier.core.files import rel_in\nfrom chantier.core.repo import Repo\n",
)
r(
    "from chantier.lifecycle.stages import PRIORITIES, changes_lock, stage_layout\nfrom chantier.status.write import write_dashboard\n",
    "from chantier.lifecycle.stages import PRIORITIES, changes_lock, stage_layout\nfrom chantier.status.write import write_dashboard\nfrom chantier.store import PlanStore\n",
)
r(
    '''def marked_for(folder: Path) -> str | None:
    """The batch id a folder's mark names; None with no mark."""
    path = mark_path(folder)
    if not path.is_file():
        return None
    words = path.read_text(encoding="utf-8").split()
    return words[-1] if words else ""


def grilled(folder: Path) -> bool:
    return (folder / "work" / SPECIFYING).exists() or (folder / SPECIFICATION).is_file()
''',
    '''def _rel(store: PlanStore, path: Path) -> str:
    return rel_in(store.root, path)


def marked_for(store: PlanStore, folder: Path) -> str | None:
    """The batch id a folder's mark names; None with no mark."""
    rel = _rel(store, mark_path(folder))
    if not store.is_file(rel):
        return None
    words = store.read_text(rel).split()
    return words[-1] if words else ""


def grilled(store: PlanStore, folder: Path) -> bool:
    return store.exists(_rel(store, folder / "work" / SPECIFYING)) or store.is_file(
        _rel(store, folder / SPECIFICATION)
    )
''',
)
r(
    "if (source.parent != paths[\"inbox\"] and not held) or not source.is_dir():",
    "if (source.parent != paths[\"inbox\"] and not held) or not repo.store.is_dir(\n        _rel(repo.store, source)\n    ):",
)
r("if not grilled(source):", "if not grilled(repo.store, source):")
r(
    '''    path = mark_path(folder)
    if path.is_file():
        repo.store.remove(repo.rel(path))''',
    '''    path = mark_path(folder)
    if repo.store.is_file(_rel(repo.store, path)):
        repo.store.remove(repo.rel(path))''',
)
r(
    '''def _state(folder: Path) -> str:
    if (folder / "work" / SPECIFYING).exists():
        return "specifying"
    return "written" if (folder / SPECIFICATION).is_file() else "no specification"''',
    '''def _state(store: PlanStore, folder: Path) -> str:
    if store.exists(_rel(store, folder / "work" / SPECIFYING)):
        return "specifying"
    written = store.is_file(_rel(store, folder / SPECIFICATION))
    return "written" if written else "no specification"''',
)
r(
    '''    return [
        d
        for place in places
        if place.is_dir()
        for d in sorted(place.iterdir())
        if mark_path(d).is_file()
    ]''',
    '''    store = repo.store
    return [
        d
        for place in places
        if store.is_dir(_rel(store, place))
        for d in (place / n for n in store.listdir(_rel(store, place)))
        if store.is_file(_rel(store, mark_path(d)))
    ]''',
)
r("folder, owner = repo.rel(d), marked_for(d)", "folder, owner = repo.rel(d), marked_for(repo.store, d)")
r("state = _state(d)", "state = _state(repo.store, d)")
e.save()

e = Editor("lifecycle/backlog.py")
r = e.r
r(
    "from chantier.core.files import heading_of, inside, markdown_title, read_json, retry\n",
    "from chantier.core.files import heading_of, inside, markdown_title, rel_in\n",
)
r(
    "from chantier.status.write import write_dashboard\n",
    "from chantier.status.write import write_dashboard\nfrom chantier.store import PlanStore\n",
)
r(
    "        if mark_path(source).is_file() and _holds(repo, source, to):",
    "        if repo.store.is_file(rel_in(repo.store.root, mark_path(source))) and _holds(\n            repo, source, to\n        ):",
)
r(
    '''            if (place / slug).is_dir():
                return place / slug''',
    '''            if repo.store.is_dir(rel_in(repo.store.root, place / slug)):
                return place / slug''',
)
r(
    '''    return [d for place in places if place.is_dir() for d in sorted(place.iterdir()) if d.is_dir()]''',
    '''    store = repo.store
    found: list[Path] = []
    for place in places:
        rel = rel_in(store.root, place)
        if store.is_dir(rel):
            found += [place / n for n in store.listdir(rel) if store.is_dir(f"{rel}/{n}")]
    return found''',
)
r(
    '''def _editable(folder: Path, relpath: str) -> Path:''',
    '''def _editable(store: PlanStore, folder: Path, relpath: str) -> Path:''',
)
r(
    "    if target is None or not target.is_file():",
    "    if target is None or not store.is_file(rel_in(store.root, target)):",
)
r("    target = _editable(folder, relpath)", "    target = _editable(repo.store, folder, relpath)")
r("        old = retry(target.read_bytes)", "        old = repo.store.read_bytes(rel_in(repo.store.root, target))")
r(
    '''    path = repo.changes / NEXT_BATCH
    try:
        found = read_json(path) if path.is_file() else None
    except (OSError, ValueError):''',
    '''    store = repo.store
    try:
        found = json.loads(store.read_text(NEXT_BATCH)) if store.is_file(NEXT_BATCH) else None
    except (OSError, ValueError):''',
)
r("import hashlib\nimport re\n", "import hashlib\nimport json\nimport re\n")
r(
    '''        ready = stage_layout(repo)["ready"]
        slugs = sorted(p.name for p in ready.iterdir() if p.is_dir()) if ready.is_dir() else []''',
    '''        store = repo.store
        ready = rel_in(store.root, stage_layout(repo)["ready"])
        slugs = (
            [n for n in store.listdir(ready) if store.is_dir(f"{ready}/{n}")]
            if store.is_dir(ready)
            else []
        )''',
)
e.save()
