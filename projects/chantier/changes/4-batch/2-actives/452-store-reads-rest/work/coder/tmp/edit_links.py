from editlib import Editor

e = Editor("lifecycle/links.py")
r = e.r
r("import os\nimport posixpath", "import posixpath")
r(
    "from chantier.core.files import read_text\nfrom chantier.core.repo import Repo\nfrom chantier.lifecycle.layout_check import Finding\n",
    "from chantier.core.files import rel_in\nfrom chantier.core.repo import Repo\nfrom chantier.lifecycle.layout_check import Finding\nfrom chantier.store import PlanStore\n",
)
r(
    '''def _listing(cache: dict[Path, set[str]], folder: Path) -> set[str]:
    if folder not in cache:
        try:
            cache[folder] = set(os.listdir(folder))
        except OSError:''',
    '''def _listing(store: PlanStore, cache: dict[Path, set[str]], folder: Path) -> set[str]:
    if folder not in cache:
        try:
            cache[folder] = set(store.listdir(rel_in(store.root, folder)))
        except OSError:''',
)
r(
    "def _exists(cache: dict[Path, set[str]], base: Path, parts: list[str]) -> bool:",
    "def _exists(\n    store: PlanStore, cache: dict[Path, set[str]], base: Path, parts: list[str]\n) -> bool:",
)
r("if part not in _listing(cache, folder):", "if part not in _listing(store, cache, folder):")
r(
    '''def _markdown_files(base: Path) -> list[Path]:
    found: list[Path] = []
    for root, dirs, files in os.walk(base):
        top = Path(root) == base
        dirs[:] = sorted(d for d in dirs if not d.startswith(".") and not (top and d in SKIPPED))
        found += [
            Path(root) / f for f in sorted(files) if f.lower().endswith(".md") and f != "STATUS.md"
        ]
    return found''',
    '''def _markdown_files(store: PlanStore, base: Path) -> list[Path]:
    found: list[Path] = []
    for root, dirs, files in store.walk("."):
        top = root == "."
        dirs[:] = sorted(d for d in dirs if not d.startswith(".") and not (top and d in SKIPPED))
        found += [
            base / root / f for f in sorted(files) if f.lower().endswith(".md") and f != "STATUS.md"
        ]
    return found''',
)
r(
    '''    for file in _markdown_files(base):
        for target in targets(read_text(file, "replace")):
            parts = _resolved(file.parent, base, target)
            if parts and not _exists(cache, base, parts):''',
    '''    store = repo.store
    for file in _markdown_files(store, base):
        for target in targets(store.read_text(rel_in(store.root, file), "replace")):
            parts = _resolved(file.parent, base, target)
            if parts and not _exists(store, cache, base, parts):''',
)
e.save()

e = Editor("lifecycle/moveout.py")
r = e.r
r(
    "from chantier.core.errors import EXIT_PRECONDITION, ChantierError\n",
    "from chantier.core.errors import EXIT_PRECONDITION, ChantierError\nfrom chantier.core.files import rel_in\n",
)
r(
    "    found = next((t for t in taken if t.exists()), None)",
    "    found = next((t for t in taken if repo.store.exists(rel_in(repo.store.root, t))), None)",
)
r(
    '''    intent = target / "01-intent.md"
    note = intent if intent.is_file() else target / "notes.md"
    old = note.read_bytes() if note.is_file() else None''',
    '''    store = repo.store
    intent = target / "01-intent.md"
    note = intent if store.is_file(rel_in(store.root, intent)) else target / "notes.md"
    old = store.read_bytes(rel_in(store.root, note)) if store.is_file(rel_in(store.root, note)) else None''',
)
e.save()
