## Summary

- Documents the known limit of the side preview: it does not follow the multi-file diff editor nor the merge editor, because the VS Code API gives them no tab input class.
- Written in `docs/known-limitations.md`, `docs/user/open-studio.md` and SwRS-MDOKFSTUDIO-LIFE-026 (new boundary scenario and known limit), with a dated entry in `requirements/tiers/log.md`.
- Documentation and requirements only, no code change (owner decision "Documenter la limite", 2026-11-21).

## Test plan

- `just requirements-update` and `just requirements-lint` pass.
- `just preflight` static stage.

## Review

- [ ] Inspector approved
