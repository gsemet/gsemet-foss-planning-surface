T = r"C:\Users\gaeta\Projets\chantier.worktrees\batch-30-CR-452\skills\chantier\scripts\cli\tests" + "\\"


def edit(name, pairs):
    s = open(T + name, encoding="utf-8").read()
    for a, b in pairs:
        assert s.count(a) >= 1, (name, a)
        s = s.replace(a, b)
    open(T + name, "w", encoding="utf-8").write(s)


edit("test_outside_poller.py", [("def unreadable(folder: Path) -> str:", "def unreadable(store: object, folder: Path) -> str:")])
edit(
    "test_leases.py",
    [
        (
            "    where = SimpleNamespace(changes=changes(repo))\n",
            "    where = SimpleNamespace(changes=changes(repo), store=FolderStore(changes(repo)))\n",
        ),
        ("from chantier.rails_idle import running\n", "from chantier.rails_idle import running\nfrom chantier.store import FolderStore\n"),
    ],
)
edit(
    "test_gate_queue_order.py",
    [
        ("from chantier.gate_queue import MARK, QUEUE, ordered, ticket_cr\n", "from chantier.gate_queue import MARK, QUEUE, ordered, ticket_cr\nfrom chantier.store import FolderStore\n"),
        ("for p in ordered(queue)]\n    assert seen", "for p in ordered(FolderStore(tmp_path), queue)]\n    assert seen"),
        ("[p.read_text().split()[0] for p in ordered(queue)] == [ONE, THREE, TWO]", "[\n        p.read_text().split()[0] for p in ordered(FolderStore(tmp_path), queue)\n    ] == [ONE, THREE, TWO]"),
        ("assert ordered(queue, drop=True) == [a, b]\n        assert ticket_cr(a, True) is None\n        assert ticket_cr(b, True) == TWO", "store = FolderStore(tmp_path)\n        assert ordered(store, queue, drop=True) == [a, b]\n        assert ticket_cr(store, a, True) is None\n        assert ticket_cr(store, b, True) == TWO"),
        ('repo: Any = SimpleNamespace(changes=tmp_path / "owner")', 'repo: Any = SimpleNamespace(\n        changes=tmp_path / "owner", store=FolderStore(tmp_path / "owner")\n    )'),
    ],
)
