set windows-shell := ["powershell.exe", "-NoLogo", "-NoProfile", "-Command"]

# List the recipes.
default:
    @just --list

# Validate the project bundles (all, or the ones named) against _schemas/ with okf-schema.
validate *projects:
    uv run --script scripts/validate-bundles.py {{projects}}
