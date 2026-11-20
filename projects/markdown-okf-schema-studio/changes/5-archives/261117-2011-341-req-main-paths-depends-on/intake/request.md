# Let a StRS Main path cite an SwRS the StRS depends on

From the requirements gardening (CR requirements-gardening, owner answer garden-Q3, 2026-11-17). Today `scripts/check_main_paths.py` and the "Main paths of a StRS" rule of `requirements/guidelines/project.guidelines.md` accept in a Main path only SwRS that derive from the StRS. Shared rules (for example LIFE-169/170, BLOCK-041/058) are therefore derived by many StRS instead of cited with `depends_on`.
