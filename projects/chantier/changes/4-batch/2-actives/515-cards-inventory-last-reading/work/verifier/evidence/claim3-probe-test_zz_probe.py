"""Verifier probe of the list's `to add` line P14-code, on a throwaway project: what `ship` and
`push` do today on a second PR link and on a merged CR. Prints the codes; asserts nothing."""

from __future__ import annotations

from pathlib import Path

import pytest
from batch_helpers import record
from conftest import Chantier, sh
from stack_world import Batch, stack_of
from test_gate_carry import commit

from chantier.commands import delivery

BASE = "https://github.com/acme/demo/pull/"


def test_probe_ship_and_push_on_a_merged_cr(
    repo: Path, chantier: Chantier, monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    a, b = stack_of(Batch("probe", ("Cr a", "Cr b"), (), 2), repo, chantier, monkeypatch)
    monkeypatch.setattr(delivery, "read_state", lambda link: ("main", False, ""))
    bare = tmp_path / "bare.git"
    sh("git", "init", "--quiet", "--bare", str(bare))
    sh("git", "remote", "set-url", "origin", str(bare), cwd=repo)
    wa = Path(a["worktree"])
    commit(wa, "a.txt", "a\n", "A")

    def cr() -> dict:
        return next(c for c in record(repo)["crs"] if c["id"] == a["id"])

    said: list[str] = []

    def show(label: str, *args: object) -> None:
        code, out, err = chantier(*args)
        first = (out or err.splitlines() or [""])[0]
        said.append(f"PROBE {label}: exit {code}: {first[:150]!r}; status={cr()['status']} pr={cr().get('pr')}")

    show("mode " + record(repo).get("mode", "?") + " first push", "push", a["id"])
    show("ship first link", "ship", a["id"], BASE + "7")
    show("ship second link, working", "ship", a["id"], BASE + "8")
    show("order merged", "order", "merged", a["id"], "--epoch", 1)
    commit(wa, "a2.txt", "a2\n", "A2")
    show("push on merged CR", "push", a["id"])
    show("ship on merged CR, third link", "ship", a["id"], BASE + "9")
    print(chr(10).join(said))
    print("PROBE remote tip == worktree head:",
          sh("git", "--git-dir", str(bare), "rev-parse", "refs/heads/" + a["branch"])
          == sh("git", "rev-parse", "HEAD", cwd=wa))
