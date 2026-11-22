from editlib import Editor

e = Editor("gate_slots.py")
r = e.r
r(
    "from chantier import procs\nfrom chantier.core.repo import Repo\n",
    "from chantier import procs\nfrom chantier.core.files import rel_in\nfrom chantier.core.repo import Repo\nfrom chantier.store import PlanStore\n",
)
r(
    '''def mtime(path: Path) -> float:
    """When the file was last written; 0 if it is gone, which no live process predates."""
    try:
        return path.stat().st_mtime
    except OSError:
        return 0.0
''',
    '''def mtime(store: PlanStore, path: Path) -> float:
    """When the file was last written; 0 if it is gone, which no live process predates."""
    found = store.stat(rel_in(store.root, path))
    return found[1] / 1e9 if found else 0.0
''',
)
r(
    '''def holder_alive(lock: Path, h: Holder, unreadable: bool) -> bool:''',
    '''def holder_alive(store: PlanStore, lock: Path, h: Holder, unreadable: bool) -> bool:''',
)
r("    recorded = mtime(lock)\n", "    recorded = mtime(store, lock)\n")
r(
    '''    for p in repo.changes.glob(".long-gate*.lock"):
        m = re.fullmatch(r"\\.long-gate(?:\\.(\\d+))?\\.lock", p.name)''',
    '''    for name in repo.store.glob(".", ".long-gate*.lock"):
        m = re.fullmatch(r"\\.long-gate(?:\\.(\\d+))?\\.lock", name)''',
)
e.save()

e = Editor("gate_queue.py")
r = e.r
r(
    "from chantier.core.errors import ChantierError\nfrom chantier.core.records import read_batch_json\n",
    "from chantier.core.errors import ChantierError\nfrom chantier.core.files import rel_in\nfrom chantier.core.records import read_batch_json\n",
)
r(
    "from chantier.stacks import next_merge\n",
    "from chantier.stacks import next_merge\nfrom chantier.store import PlanStore\n",
)
r(
    '''def read_ticket(p: Path) -> tuple[str, int] | None:''',
    '''def read_ticket(store: PlanStore, p: Path) -> tuple[str, int] | None:''',
)
r(
    '''            m = re.fullmatch(r"(\\S+) pid (\\d+)", p.read_text(encoding="utf-8").strip())''',
    '''            m = re.fullmatch(r"(\\S+) pid (\\d+)", store.read_text(rel_in(store.root, p)).strip())''',
)
r("def ticket_cr(p: Path, drop: bool) -> str | None:", "def ticket_cr(store: PlanStore, p: Path, drop: bool) -> str | None:")
r("    t = read_ticket(p)\n    if t is None:", "    t = read_ticket(store, p)\n    if t is None:")
r("procs.alive_since(t[1], mtime(p), True)", "procs.alive_since(t[1], mtime(store, p), True)")
r(
    '''def next_merge_cr(queue: Path) -> str | None:''',
    '''def next_merge_cr(store: PlanStore, queue: Path) -> str | None:''',
)
r(
    '''    from chantier.store import FolderStore  # noqa: PLC0415 - the store imports modules above

    store = FolderStore(queue.parent)  # the planning folder; reads are the same on every backend
    path = queue.parent / "4-batch" / "batch.json"
    if not store.is_file("4-batch/batch.json"):
        return None''',
    '''    path = queue.parent / "4-batch" / "batch.json"
    if not store.is_file(rel_in(store.root, path)):
        return None''',
)
r(
    '''def ordered(queue: Path, drop: bool = False) -> list[Path]:''',
    '''def ordered(store: PlanStore, queue: Path, drop: bool = False) -> list[Path]:''',
)
r(
    '''    tickets = sorted(queue.glob("[0-9]*"))
    marks = {p.name for p in queue.glob(f"{MARK}*")}''',
    '''    rel = rel_in(store.root, queue)
    tickets = [queue / n for n in store.glob(rel, "[0-9]*")]
    marks = set(store.glob(rel, f"{MARK}*"))''',
)
r("    nxt = next_merge_cr(queue)\n", "    nxt = next_merge_cr(store, queue)\n")
r("t = read_ticket(p) if nxt else None", "t = read_ticket(store, p) if nxt else None")
r(
    "    crs = (ticket_cr(p, False) for p in ordered(repo.changes / QUEUE))",
    "    store = repo.store\n    crs = (ticket_cr(store, p, False) for p in ordered(store, repo.changes / QUEUE))",
)
r(
    "    live = [(p, ticket_cr(p, False)) for p in ordered(queue)]",
    "    live = [(p, ticket_cr(repo.store, p, False)) for p in ordered(repo.store, queue)]",
)
r("holder_alive(v.slot.lock, v.holder, True):\n            live.append", "holder_alive(repo.store, v.slot.lock, v.holder, True):\n            live.append")
e.save()

e = Editor("commands/gate_lock.py")
r = e.r
r("for p in ordered(self.queue, drop=True):", "for p in ordered(self.repo.store, self.queue, drop=True):")
r("cr = ticket_cr(p, True)", "cr = ticket_cr(self.repo.store, p, True)")
r("parse_holder(left), mtime(self.slot.lock)", "parse_holder(left), mtime(self.repo.store, self.slot.lock)")
e.save()

e = Editor("commands/gate_run.py")
r = e.r
r("def ask_stop(s: Slot, h: Holder)", "def ask_stop(store: PlanStore, s: Slot, h: Holder)")
r("    recorded = mtime(s.lock)\n", "    recorded = mtime(store, s.lock)\n")
r("def stop_and_wait(s: Slot, h: Holder, timeout_s: float)", "def stop_and_wait(store: PlanStore, s: Slot, h: Holder, timeout_s: float)")
r("    gate_alive, pg = ask_stop(s, h)\n    if not gate_alive:\n        return None", "    gate_alive, pg = ask_stop(store, s, h)\n    if not gate_alive:\n        return None")
r("procs.wait_gone(h.pid, mtime(s.lock), timeout_s)", "procs.wait_gone(h.pid, mtime(store, s.lock), timeout_s)")
r("    gate_alive, pg = ask_stop(s, h)\n    if not gate_alive and run", "    gate_alive, pg = ask_stop(b.repo.store, s, h)\n    if not gate_alive and run")
e.save()

e = Editor("commands/orders_merged.py")
e.r("stop_and_wait(v.slot, v.holder, STOP_WAIT_S)", "stop_and_wait(repo.store, v.slot, v.holder, STOP_WAIT_S)")
e.save()

e = Editor("commands/release.py")
e.r("procs.alive_since(h.pg, mtime(v.slot.lock), False)", "procs.alive_since(h.pg, mtime(repo.store, v.slot.lock), False)")
e.save()
