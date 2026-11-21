"""Round 1 helper: write the one launch paragraph, the same text, into the four SKILL.md files."""

KEEP = (
    "`<plugin root>` is written absolute, with forward slashes, quoted, the same path as P10's rule "
    "holds (the same slashes, drive letter's case and trailing slash; the rule's quoting may differ, "
    "per the trial); `$CHANTIER` is carried verbatim into every brief and command, since another "
    "form of the path does not match the rule and meets the host's prompt."
)
NEW = (
    "`$CHANTIER` is the CLI, one launch in two modes, checked once at the session's start. The "
    "chantier skill's folder (`<skill folder>` = this file's folder in the `chantier` skill, "
    "`../chantier` from it in the other skills, made absolute) and the plugin root "
    "(`<plugin root>` = `<skill folder>/../..`, made absolute). If `<plugin root>/.git` exists (a "
    "folder or a file), this is chantier's own checkout; when the session's project is chantier "
    "(from the session's context, the project it works on: in a planning surface the project "
    "folder `projects/chantier`, by its name alone; in-project chantier's own repository, which "
    "the plugin manifest at its root confirms, `.claude-plugin/plugin.json` or "
    "`.github/plugin/plugin.json` whose `name` is `chantier`; the question is \"is the project "
    "chantier\", never \"does it use chantier\"), it is the dev mode: run "
    "`uv sync --locked --project \"<plugin root>\"` once, before the first `$CHANTIER` command, "
    "then `$CHANTIER` is `uv run --no-sync --project \"<plugin root>\" chantier`, the local code, "
    "live, with no fetch; only the steering session syncs, never a Foreman, a Driver or a worker. "
    "Otherwise it is the plugin mode, a host's plugin copy or another project, even with the "
    "plugin loaded from chantier's checkout: `$CHANTIER` is "
    "`uvx --from \"<plugin root>\" chantier --skill \"<skill folder>\"`, with no fetch, and the "
    "session never runs `uv sync`. Any failure of the sync or of `$CHANTIER`, in either mode, at "
    "any call, follows `startup-core.md`. In a planning surface, `$CHANTIER` also carries "
    "`--project <the project's folder>`. " + KEEP
)
START = "`$CHANTIER` is the CLI, one launch in two modes"
for name in ("chantier", "chief-of-staff", "griller", "status"):
    path = f"skills/{name}/SKILL.md"
    text = open(path, "rb").read().decode("utf-8")
    lines = text.split("\n")
    i = next(n for n, line in enumerate(lines) if line.startswith(START))
    cr = chr(13) if lines[i].endswith(chr(13)) else ""
    assert lines[i].rstrip(chr(13)).endswith(KEEP), path
    lines[i] = NEW + cr
    open(path, "wb").write("\n".join(lines).encode("utf-8"))
print("ok")
