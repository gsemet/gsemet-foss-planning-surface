from editlib import Editor

e = Editor("summaries/sources.py")
r = e.r
r(
    "from chantier.core.files import retry\n",
    "from chantier.core.files import rel_in\nfrom chantier.store import PlanStore\n",
)
r(
    '''def covered_files(folder: Path) -> list[str]:''',
    '''def covered_files(store: PlanStore, folder: Path) -> list[str]:''',
)
r(
    '''    names = [name for name in COVERED if (folder / name).is_file()]
    intake = folder / INTAKE
    if intake.is_dir():
        names += [f"{INTAKE}/{p.name}" for p in intake.glob("*.md") if p.is_file()]
    return sorted(names)''',
    '''    rel = rel_in(store.root, folder)
    names = [name for name in COVERED if store.is_file(f"{rel}/{name}")]
    intake = f"{rel}/{INTAKE}"
    if store.is_dir(intake):
        names += [
            f"{INTAKE}/{n}" for n in store.glob(intake, "*.md") if store.is_file(f"{intake}/{n}")
        ]
    return sorted(names)''',
)
r(
    '''def checksum(path: Path) -> str:''',
    '''def checksum(store: PlanStore, path: Path) -> str:''',
)
r(
    "    data = retry(path.read_bytes).removeprefix(BOM)",
    "    data = store.read_bytes(rel_in(store.root, path)).removeprefix(BOM)",
)
r(
    '''def checksums(folder: Path) -> dict[str, str]:
    """Each covered file of the folder with its checksum."""
    return {name: checksum(folder / name) for name in covered_files(folder)}''',
    '''def checksums(store: PlanStore, folder: Path) -> dict[str, str]:
    """Each covered file of the folder with its checksum."""
    return {name: checksum(store, folder / name) for name in covered_files(store, folder)}''',
)
e.save()

e = Editor("summaries/gaps.py")
r = e.r
r("from chantier.core.files import heading_of, read_text\n", "from chantier.core.files import heading_of, rel_in\n")
r("    current = checksums(folder)\n", "    current = checksums(store, folder)\n")
r(
    '''    request = folder / REQUEST
    if request.is_file() and heading_of(read_text(request, "replace")) is None:''',
    '''    request = rel_in(store.root, folder / REQUEST)
    if store.is_file(request) and heading_of(store.read_text(request, "replace")) is None:''',
)
e.save()

e = Editor("summaries/title.py")
r = e.r
r("from chantier.core.files import heading_of, read_text, title_source\n", "from chantier.core.files import heading_of, rel_in, title_source\n")
r(
    '''    request = cr / REQUEST
    if request.is_file() and heading_of(read_text(request, "replace")) is None:''',
    '''    request = rel_in(repo.store.root, cr / REQUEST)
    if repo.store.is_file(request) and heading_of(repo.store.read_text(request, "replace")) is None:''',
)
e.save()

e = Editor("summaries/origin.py")
r = e.r
r(
    "from chantier.core.files import read_text\nfrom chantier.core.records import Origin\n",
    "from chantier.core.files import rel_in\nfrom chantier.core.records import Origin\nfrom chantier.store import PlanStore\n",
)
r(
    '''def issue_url(folder: Path) -> str | None:''',
    '''def issue_url(store: PlanStore, folder: Path) -> str | None:''',
)
r(
    '''        path = folder / name
        if path.is_file():
            found = ISSUE_LINE.search(read_text(path, errors="replace"))''',
    '''        rel = rel_in(store.root, folder / name)
        if store.is_file(rel):
            found = ISSUE_LINE.search(store.read_text(rel, errors="replace"))''',
)
e.save()

e = Editor("commands/summary.py")
r = e.r
r("crs = [f for f in folders if covered_files(f)]", "crs = [f for f in folders if covered_files(repo.store, f)]")
r("origin_of(issue_url(folder), args.tracker)", "origin_of(issue_url(repo.store, folder), args.tracker)")
r("current.sources = checksums(folder)", "current.sources = checksums(repo.store, folder)")
e.save()

e = Editor("hub/issue_refs.py")
e.r("url = issue_url(folder)", "url = issue_url(repo.store, folder)")
e.save()
