from editlib import Editor

e = Editor("lifecycle/layout_check.py")
r = e.r
r("import os\nimport re", "import re")
r(
    "from chantier.core import waits\nfrom chantier.core.repo import Repo\n",
    "from chantier.core import waits\nfrom chantier.core.files import rel_in\nfrom chantier.core.repo import Repo\n",
)
r(
    "from chantier.summaries.sources import INTAKE\n",
    "from chantier.store import PlanStore\nfrom chantier.summaries.sources import INTAKE\n",
)
r(
    '''def _dirs(folder: Path) -> list[Path]:
    """The folders directly in `folder`, dot names left out, sorted."""
    if not folder.is_dir():
        return []
    return sorted(p for p in folder.iterdir() if p.is_dir() and not p.name.startswith("."))


def _cr_like(folder: Path) -> bool:
    return any((folder / name).exists() for name in CR_LIKE)


def _holds_cr(folder: Path) -> bool:
    return any(_cr_like(child) for child in _dirs(folder))
''',
    '''def _rel(store: PlanStore, path: Path) -> str:
    return rel_in(store.root, path)


def _dirs(store: PlanStore, folder: Path) -> list[Path]:
    """The folders directly in `folder`, dot names left out, sorted."""
    rel = _rel(store, folder)
    if not store.is_dir(rel):
        return []
    return [
        folder / name
        for name in store.listdir(rel)
        if not name.startswith(".") and store.is_dir(f"{rel}/{name}")
    ]


def _cr_like(store: PlanStore, folder: Path) -> bool:
    return any(store.exists(_rel(store, folder / name)) for name in CR_LIKE)


def _holds_cr(store: PlanStore, folder: Path) -> bool:
    return any(_cr_like(store, child) for child in _dirs(store, folder))
''',
)
r(
    "def _misplaced_priority(paths: dict[str, Path], folder: Path) -> bool:",
    "def _misplaced_priority(store: PlanStore, paths: dict[str, Path], folder: Path) -> bool:",
)
r("not inside and _holds_cr(folder)", "not inside and _holds_cr(store, folder)")
r(
    '''    live = [f for f in cr_folders(paths) if not f.name.startswith(".")]
    closed = [*_dirs(paths["archives"]), *_dirs(paths["trash"])]
    closed = [f for f in closed if f != paths["archives"] / "batches"]
    return (
        [f for f in live if not _misplaced_priority(paths, f)],
        [f for f in closed if not _misplaced_priority(paths, f)],
    )''',
    '''    store = repo.store
    live = [f for f in cr_folders(store, paths) if not f.name.startswith(".")]
    closed = [*_dirs(store, paths["archives"]), *_dirs(store, paths["trash"])]
    closed = [f for f in closed if f != paths["archives"] / "batches"]
    return (
        [f for f in live if not _misplaced_priority(store, paths, f)],
        [f for f in closed if not _misplaced_priority(store, paths, f)],
    )''',
)
r(
    '''def _nested(cr: Path) -> Iterator[Path]:
    """The CR-like folders under a CR folder, at any depth, the outermost of each."""
    for root, dirs, _ in os.walk(cr):
        dirs[:] = sorted(d for d in dirs if not d.startswith("."))
        for name in list(dirs):
            if _cr_like(Path(root) / name):
                dirs.remove(name)
                yield Path(root) / name''',
    '''def _nested(store: PlanStore, cr: Path) -> Iterator[Path]:
    """The CR-like folders under a CR folder, at any depth, the outermost of each."""
    for root, dirs, _ in store.walk(_rel(store, cr)):
        dirs[:] = sorted(d for d in dirs if not d.startswith("."))
        for name in list(dirs):
            if _cr_like(store, store.root / root / name):
                dirs.remove(name)
                yield store.root / root / name''',
)
r(
    '''        for folder in _dirs(repo.changes.resolve())
        if folder.name not in STAGES and (_cr_like(folder) or _holds_cr(folder))''',
    '''        for folder in _dirs(repo.store, repo.changes.resolve())
        if folder.name not in STAGES
        and (_cr_like(repo.store, folder) or _holds_cr(repo.store, folder))''',
)
r(
    '''    found: list[Finding] = []
    for folder in _dirs(paths["backlog"]):
        if folder.name in PRIORITIES:
            continue
        text = "not a priority folder (P1..P4)"
        if _cr_like(folder):''',
    '''    found: list[Finding] = []
    store = repo.store
    for folder in _dirs(store, paths["backlog"]):
        if folder.name in PRIORITIES:
            continue
        text = "not a priority folder (P1..P4)"
        if _cr_like(store, folder):''',
)
r('for folder in _dirs(paths["batches"])', 'for folder in _dirs(store, paths["batches"])')
r(
    'for folder in _dirs(paths["archives"])\n        if folder.name != "batches"',
    'for folder in _dirs(repo.store, paths["archives"])\n        if folder.name != "batches"',
)
r(
    '''            for folder in _dirs(paths[stage])
            if _misplaced_priority(paths, folder)''',
    '''            for folder in _dirs(repo.store, paths[stage])
            if _misplaced_priority(repo.store, paths, folder)''',
)
r("for inner in _nested(cr)", "for inner in _nested(repo.store, cr)")
r(
    '''    if name == waits.FILE and entry.is_file():
        return _waits_finding(repo, cr, entry)
    if name in CR_FOLDERS and not entry.is_dir():
        return Finding("error", path, "a file where chantier reads a folder")
    if name in CR_FILES and entry.is_dir():''',
    '''    store = repo.store
    if name == waits.FILE and store.is_file(_rel(store, entry)):
        return _waits_finding(repo, cr, entry)
    if name in CR_FOLDERS and not store.is_dir(_rel(store, entry)):
        return Finding("error", path, "a file where chantier reads a folder")
    if name in CR_FILES and store.is_dir(_rel(store, entry)):''',
)
r(
    '''def _has_request(cr: Path) -> bool:
    intake = cr / INTAKE
    return (
        (intake.is_dir() and any(p.is_file() for p in intake.glob("*.md")))
        or (cr / "01-intent.md").is_file()
        or (cr / "03-change-spec.md").is_file()
    )''',
    '''def _has_request(store: PlanStore, cr: Path) -> bool:
    rel = _rel(store, cr)
    intake = f"{rel}/{INTAKE}"
    return (
        (
            store.is_dir(intake)
            and any(store.is_file(f"{intake}/{name}") for name in store.glob(intake, "*.md"))
        )
        or store.is_file(f"{rel}/01-intent.md")
        or store.is_file(f"{rel}/03-change-spec.md")
    )''',
)
r(
    '''    found = [
        f
        for entry in sorted(cr.iterdir())
        if not entry.name.startswith(".") and (f := _entry(repo, cr, entry))
    ]
    if not _has_request(cr):''',
    '''    store = repo.store
    found = [
        f
        for name in store.listdir(_rel(store, cr))
        if not name.startswith(".") and (f := _entry(repo, cr, cr / name))
    ]
    if not _has_request(store, cr):''',
)
r(
    '''    for stage in stages:
        found += [''',
    '''    store = repo.store
    for stage in stages:
        rel = _rel(store, stage)
        found += [''',
)
r(
    '''            for item in (sorted(stage.iterdir()) if stage.is_dir() else [])
            if item.is_file() and not item.name.startswith(".")''',
    '''            for item in (stage / n for n in (store.listdir(rel) if store.is_dir(rel) else []))
            if store.is_file(_rel(store, item)) and not item.name.startswith(".")''',
)
e.save()

for p, a, b in [
    ("commands/summary.py", "or cr_folders(paths)", "or cr_folders(repo.store, paths)"),
    ("commands/waits.py", "in cr_folders(paths):", "in cr_folders(repo.store, paths):"),
    ("hub/issue_refs.py", "cr_folders(stage_layout(repo))", "cr_folders(repo.store, stage_layout(repo))"),
]:
    ed = Editor(p)
    ed.r(a, b)
    ed.save()
