set windows-shell := ["powershell.exe", "-NoLogo", "-NoProfile", "-Command"]

# List the recipes.
default:
    @just --list

# Validate the planning folders (all, or the ones named): stages, then chantier's summary lint.
validate *projects:
    uv run --script scripts/validate-bundles.py {{projects}}
