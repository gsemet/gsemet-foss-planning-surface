"""Probe the actor behaviour of the okf_schema source tree given as argv[1]."""

import sys
from pathlib import Path

sys.dont_write_bytecode = True
sys.path.insert(0, sys.argv[1])

from okf_schema import validator  # noqa: E402
from okf_schema.api import show_bundle  # noqa: E402
from okf_schema.validator import Report  # noqa: E402

where = Path(validator.__file__).as_posix()
print("module:", "base src" if "/scratch/vb/" in where else "head src (CR worktree)")
if "/scratch/vb/" not in where and "batch-01-CR-104/src" not in where:
    raise SystemExit("unexpected module location: " + where)
print("pattern:", validator._ACTOR_RE.pattern)
path = Path("f.md")
values = [
    "reference_agent/gemini-2.5-pro", "langchain.agents/0.3", "process:nightly-check",
    "process:finance-nightly", "bot:okf-schema", "acme.ci:nightly", "alice", "Alice", "human:",
    "human:alice", "human:ahormati", "Human:alice", 42, 0, True, ["x"], {"a": 1}, "", None,
]
print(f"{'by':36} {'tier':18} codes")
for by in values:
    fm = {"verified": [{"by": by, "at": "2026-01-01"}]}
    report = Report()
    validator._validate_okf2_verified(path, fm, report)
    codes = [f.code for f in report.errors] + [f.code for f in report.warnings]
    print(f"{by!r:36} {validator._derive_trust_tier(fm):18} {codes}")
at = "2026-01-01"
extra = {
    "no by key": {"verified": [{"at": at}]},
    "verified absent": {},
    "verified empty list": {"verified": []},
    "verified string": {"verified": "alice"},
    "non-dict entry": {"verified": ["alice"]},
    "bare mapping producer/version": {"verified": {"by": "reference_agent/gemini-2.5-pro", "at": at}},
    "producer/version + human": {"verified": [{"by": "reference_agent/gemini-2.5-pro", "at": at},
                                              {"by": "human:alice", "at": at}]},
}
for name, fm in extra.items():
    print(f"{name:36} {validator._derive_trust_tier(fm)}")
report = Report()
validator._validate_okf2_verified(
    path, {"verified": [{"by": "human:alice", "at": at}, {"by": "alice", "at": at}]}, report
)
messages = [f.message for f in report.warnings if f.code == "W10"]
print("W10 count:", len(messages))
for m in messages:
    print("W10 message:", m)
    print("contains '{i}':", "{i}" in m, "| level warnings only, errors:", report.errors)
expected = (
    f"File '{path}': verified entry [1] has malformed 'by' value 'alice'. "
    "OKF 0.2 actors are '<producer>/<version>' (e.g. 'reference_agent/gemini-2.5-pro'), "
    "'human:<id>' or 'process:<id>'; any '<prefix>:<identifier>' is also accepted. "
    "Only a 'human:<id>' actor makes the concept human-reviewed. "
    f"Fix: correct the 'by' value in verified entry [1]."
)
print("equals specification text:", messages == [expected])

import shutil  # noqa: E402

root = Path(__file__).parent / "api-bundle"
shutil.rmtree(root, ignore_errors=True)
(root / "things").mkdir(parents=True)
for by in ["reference_agent/gemini-2.5-pro", "alice", "human:", "human:alice"]:
    (root / "things" / "c.md").write_text(
        "---\ntype: concept\ntitle: T\ndescription: D\n"
        f"verified: [{{by: '{by}', at: '2026-01-01'}}]\n---\n\n# T\n",
        encoding="utf-8",
    )
    print(f"show_bundle trust_tier for {by!r}: {show_bundle(root, 'things/c.md').trust_tier}")

from click.testing import CliRunner  # noqa: E402

from okf_schema.cli import cli  # noqa: E402

(root / "things" / "c.md").write_text(
    "---\ntype: concept\ntitle: T\ndescription: D\n"
    "verified: [{by: reference_agent/gemini-2.5-pro, at: '2026-01-01'}]\n---\n\n# T\n",
    encoding="utf-8",
)
res = CliRunner().invoke(cli, ["show", "--path", str(root), "things/c.md"])
print("cli show exit:", res.exit_code)
print("\n".join(line for line in res.output.splitlines() if line.startswith(("trust", "Usage", "Error"))))

# Spec evidence 5: validate-md --strict on both actors.
schemas = Path(__file__).parent / "schemas"
schemas.mkdir(exist_ok=True)
(schemas / "concept.schema.json").write_text(
    '{"type": "object", "properties": {"type": {"type": "string"}}, "required": ["type"]}',
    encoding="utf-8",
)
cases = {
    "ok": ("reference_agent/gemini-2.5-pro", "reference_agent/gemini-2.5-pro", ""),
    "alice": ("reference_agent/gemini-2.5-pro", "alice", ""),
    "unchecked": ("alice", "human:alice", "sources: [{id: s1, resource: 'https://example.com/x', author: alice}]\n"),
}
for name, (gen, ver, extra_fm) in cases.items():
    f = Path(__file__).parent / name / "c.md"
    f.parent.mkdir(exist_ok=True)
    f.write_text(
        "---\ntype: concept\ntitle: Test\ndescription: Test\n"
        f'generated: {{at: "2024-01-01T00:00:00Z", by: {gen}}}\n'
        f'verified: [{{by: {ver}, at: "2024-01-02T00:00:00Z"}}]\n'
        f"{extra_fm}---\n\n# Test\n",
        encoding="utf-8",
    )
    res = CliRunner().invoke(
        cli, ["validate-md", "--input", str(f), "--schemas-dir", str(schemas), "--strict"]
    )
    print(f"--- validate-md --strict [{name}] generated.by={gen} verified.by={ver}: exit {res.exit_code}")
    print(res.output.replace(str(Path(__file__).parent), "<scratch>").rstrip())
shutil.rmtree(root)
