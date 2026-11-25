"""Run the example recipes in the scratch copy `h` and report what they change."""

import os
import subprocess
from pathlib import Path

here = Path(__file__).parent
head = here / "h"
env = dict(os.environ)
env["UV_PROJECT_ENVIRONMENT"] = "C:/Users/gaeta/Projets/okf-schema.worktrees/batch-01-CR-104/.venv"
env.pop("VIRTUAL_ENV", None)
paths = ["examples", "justfile", "pyproject.toml", "uv.lock", ".gitattributes", ".gitignore"]


def run(*args: str, show_tail: int = 0) -> str:
    done = subprocess.run(
        list(args), cwd=head, env=env, capture_output=True, text=True, encoding="utf-8", errors="replace"
    )
    out = done.stdout + done.stderr
    print(f"$ {' '.join(args)}  -> exit {done.returncode}")
    if show_tail:
        print("\n".join(out.strip().splitlines()[-show_tail:]))
    return done.stdout


print("scratch HEAD:", run("git", "rev-parse", "HEAD").strip())
print("diff before:", repr(run("git", "diff", "HEAD", "--stat", "--", *paths)))
run("just", "refresh-all-examples", show_tail=6)
print("git diff HEAD (content) after refresh-all-examples:",
      repr(run("git", "diff", "HEAD", "--stat", "--", *paths)))
status = run("git", "status", "--porcelain", "--untracked-files=all", "--", *paths).splitlines()
modified = [line for line in status if not line.startswith("??")]
print("status entries:", len(modified), "modified;", len(status) - len(modified), "untracked")
for line in status:
    print("  ", line)
for line in modified:
    rel = line[3:]
    blob = subprocess.run(["git", "show", "HEAD:" + rel], cwd=head, capture_output=True).stdout
    now = (head / rel).read_bytes()
    print("   same bytes ignoring CR:", blob.replace(b"\r\n", b"\n") == now.replace(b"\r\n", b"\n"), rel)

validated = run("uv", "run", "--no-sync", "--", "okf-schema", "validate", "--strict", "--path",
                "examples/okfkb-hw-knowledge-base/", show_tail=4)
print("W10 in output:", "W10" in validated)
bots = run("git", "grep", "-c", "by: bot:okf-schema", "--", "examples").splitlines()
print("example files carrying 'by: bot:okf-schema':", len(bots))

schema = head / "examples/okfkb-hw-knowledge-base/_schema/Base.schema.yaml"
old = "Actor string identifying the producer (e.g. 'human:alice', 'bot:ci')."
text = schema.read_text(encoding="utf-8")
new_line = next(line for line in text.splitlines() if "Actor string (OKF 0.2" in line)
schema.write_text(text.replace(new_line.strip(), "description: " + old), encoding="utf-8", newline="\n")
print("-- existing knowledge base: description put back to the old text, then the update recipe")
run("just", "refresh-okfkb-example", show_tail=3)
print("old description still there after `okfkb update`:", old in schema.read_text(encoding="utf-8"))
