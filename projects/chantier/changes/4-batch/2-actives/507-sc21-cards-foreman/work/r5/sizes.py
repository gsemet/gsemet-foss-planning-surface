"""Throwaway: LF byte sizes of every file under cards-next/, with base sizes."""

import subprocess
from pathlib import Path

WT = Path("C:/Users/gaeta/Projets/chantier.worktrees/batch-31-CR-507")
CN = WT / "skills/chantier/cards-next"


def lf(path: Path) -> int:
    return len(path.read_bytes().replace(b"\r\n", b"\n"))


def base(rel: str) -> int | None:
    run = subprocess.run(["git", "-C", str(WT), "show", f"HEAD:{rel}"], capture_output=True)
    return len(run.stdout) if run.returncode == 0 else None


for path in sorted(CN.rglob("*")):
    if path.is_file():
        rel = path.relative_to(CN).as_posix()
        head = base(f"skills/chantier/cards-next/{rel}")
        old = base(f"skills/chantier/references/{rel}")
        print(f"{lf(path):7} head={head} ref={old} {rel}")
