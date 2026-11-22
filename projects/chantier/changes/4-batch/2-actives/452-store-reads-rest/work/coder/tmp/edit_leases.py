from editlib import Editor

e = Editor("core/leases.py")
r = e.r
r("from chantier.core.files import read_json\n", "from chantier.core.files import rel_in\n")
r(
    '''    for p in sorted(repo.changes.glob(f"{HOLD}.*.run")):
        m = _HOLD_NAME.fullmatch(p.name)
        if not m or (unit is not None and m[1] != unit):
            continue
        try:
            data = read_json(p)
            pid = int(data["pid"])
            recorded = p.stat().st_mtime
        except (OSError, ValueError, KeyError, TypeError):
            continue''',
    '''    store = repo.store
    for name in store.glob(".", f"{HOLD}.*.run"):
        p = repo.changes / name
        m = _HOLD_NAME.fullmatch(name)
        if not m or (unit is not None and m[1] != unit):
            continue
        try:
            data = json.loads(store.read_text(name))
            pid = int(data["pid"])
            stamp = store.stat(name)
            if stamp is None:
                raise FileNotFoundError(name)
            recorded = stamp[1] / 1e9
        except (OSError, ValueError, KeyError, TypeError):
            continue''',
)
r(
    '''    if v is not None and v.holder is not None and holder_alive(v.slot.lock, v.holder, True):
        return "gate running"
    queue = repo.changes / QUEUE
    if any(ticket_cr(p, False) == unit for p in sorted(queue.glob("[0-9]*"))):''',
    '''    store = repo.store
    if v is not None and v.holder is not None and holder_alive(store, v.slot.lock, v.holder, True):
        return "gate running"
    queue = repo.changes / QUEUE
    tickets = [queue / n for n in store.glob(rel_in(store.root, queue), "[0-9]*")]
    if any(ticket_cr(store, p, False) == unit for p in tickets):''',
)
r(
    '''    taken = {
        int(m[2]) for p in repo.changes.glob(f"{HOLD}.*.run")
        if (m := _HOLD_NAME.fullmatch(p.name)) and m[1] == unit
    }  # fmt: skip''',
    '''    taken = {
        int(m[2]) for name in repo.store.glob(".", f"{HOLD}.*.run")
        if (m := _HOLD_NAME.fullmatch(name)) and m[1] == unit
    }  # fmt: skip''',
)
e.save()
