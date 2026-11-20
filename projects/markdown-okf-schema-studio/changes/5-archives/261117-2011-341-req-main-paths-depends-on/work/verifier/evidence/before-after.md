# Before and after

No UI, no screenshots. Before: base dedbdb2ac283e76ac91e718c683168f8fe67278a, the new tests run against the base checker: 2 failed (depends_on citation rejected, old message). After: f16dbc3c8bc2fb4d928a11d8324a74f530f13027, 12 passed. Reproduce: copy test/build/test_check_main_paths.py into a detached worktree of origin/main and run pytest on it.
