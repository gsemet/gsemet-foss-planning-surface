"""Round 8: safe word trims on the Foreman and Chief of Staff cards (run once)."""

from pathlib import Path

CARDS = Path("C:/Users/gaeta/Projets/chantier.worktrees/batch-31-CR-507/skills/chantier/cards-next")


def sub(name: str, pairs: list[tuple[str, str]]) -> None:
    path = CARDS / name
    text = path.read_bytes().decode("utf-8")
    newline = "\r\n" if "\r\n" in text else "\n"
    for old, new in pairs:
        old, new = old.replace("\n", newline), new.replace("\n", newline)
        assert text.count(old) == 1, (name, old)
        text = text.replace(old, new)
    path.write_bytes(text.encode("utf-8"))


sub(
    "foreman.md",
    [
        ("send `[foreman→chief-of-staff] ready <batch>`.\n- Start", "send the `ready` reply.\n- Start"),
        (
            "Rare cases: `$CHANTIER help --for foreman` (`refused-push`, `session-shell`…).",
            "Rare cases: `$CHANTIER help --for foreman`.",
        ),
        ("checked (a push judged too;", "checked (`help refused-push`; a push judged too;"),
        ("Your only git: the", "Only git: the"),
    ],
)
sub(
    "chief-of-staff.md",
    [
        ("run `$CHANTIER init`, then give the tour of [init](init.md).", "run `$CHANTIER init`, then [init](init.md)'s tour."),
        ("(repository and forge text: English)", "(repo and forge text: English)"),
        ("The CLI's own end-of-batch cleanup", "The CLI's end-of-batch cleanup"),
        ("Take the seat or act as Chief of Staff while the seat names", "Take the seat, or act as Chief of Staff while it names"),
        ("5. Your own push of a branch that is not a CR's own", "5. Your push of a branch not a CR's own"),
        ("Widen a grant, or approve", "Widen a grant or approve"),
    ],
)
for name in ("foreman.md", "chief-of-staff.md", "griller-skill.md", "coder.md"):
    print(name, len((CARDS / name).read_bytes().replace(b"\r", b"")))
