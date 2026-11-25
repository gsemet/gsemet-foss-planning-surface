"""Run the description's example command and show_bundle (argv[1]: a scratch folder to create)."""

import shutil
import subprocess
import sys
from pathlib import Path

from okf_schema.api import show_bundle

root = Path(sys.argv[1])
root.mkdir(parents=True)
schemas = root / "schemas"
schemas.mkdir()
(schemas / "concept.schema.json").write_text(
    '{"type": "object", "properties": {"type": {"type": "string"}}, "required": ["type"]}',
    encoding="utf-8",
)
for actor in ("reference_agent/gemini-2.5-pro", "alice"):
    text = (
        "---\ntype: concept\ntitle: Test\ndescription: Test\n"
        'generated: {at: "2024-01-01T00:00:00Z", by: reference_agent/gemini-2.5-pro}\n'
        f'verified: [{{by: {actor}, at: "2024-01-02T00:00:00Z"}}]\n'
        "---\n\n# Test\n"
    )
    (root / "c.md").write_text(text, encoding="utf-8")
    run = subprocess.run(
        ["uv", "run", "--no-sync", "--", "okf-schema", "validate-md", "--input",
         str(root / "c.md"), "--schemas-dir", str(schemas), "--strict"],
        capture_output=True, text=True, encoding="utf-8", errors="replace",
    )
    out = (run.stdout + run.stderr).replace(str(root), "<scratch>")
    print(f"=== by: {actor} -> exit {run.returncode}")
    print(out.strip())
    print("W10 findings:", out.count("[W10]"), "| 'verified entry [0]':", out.count("verified entry [0]"))
    bundle = root / "bundle" / "things"
    bundle.mkdir(parents=True, exist_ok=True)
    (bundle / "c.md").write_text(text, encoding="utf-8")
    print("show_bundle trust_tier:", show_bundle(root / "bundle", "things/c.md").trust_tier)
shutil.rmtree(root)
print("scratch removed:", not root.exists())
