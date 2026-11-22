from editlib import Editor

e = Editor("commands/crs.py")
r = e.r
r(
    "    if not source.is_file() or cr_directory(repo, rel) not in source.parents:",
    "    if (\n        not repo.store.is_file(rel_in(repo.store.root, source))\n        or cr_directory(repo, rel) not in source.parents\n    ):",
)
r(
    '''    if short_heading(read_text(source, "replace")) is None:''',
    '''    store = repo.store
    where = rel_in(store.root, source)
    if short_heading(store.read_text(where, "replace")) is None:''',
)
r("    folder = new_request(repo, target.name, source.read_bytes())\n", "    folder = new_request(repo, target.name, store.read_bytes(where))\n")
r('repo.rel(folder / "03-change-spec.md"), source.read_bytes())', 'repo.rel(folder / "03-change-spec.md"), store.read_bytes(where))')
e.save()
