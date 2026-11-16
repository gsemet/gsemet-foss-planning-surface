# before-after

Before (base, origin/main): cards list the `--epoch` commands as examples; no PowerShell note. After (76b0c8732447e9a7cdba26520b2290749f974a7e): exact list, "exit 2" for others, new host note. Reproduce: `git diff origin/main...76b0c87 -- skills/chantier/references`, and `uv run --script skills/chantier/scripts/cli/chantier.py <cmd> --help`. No captures: card text only.