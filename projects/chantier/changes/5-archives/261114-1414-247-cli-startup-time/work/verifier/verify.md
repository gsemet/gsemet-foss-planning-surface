Head: b1ce3968e3342e7a4f2a9fa11b280f628ec1d2ed
E1 (median of 10 warm, ms; head/base c8dc8e4/old 2d9a2aa): --version 240/694/411; --help 240/697/412; status 628/757/473; rules 553/750/455; take 600/735/471. Head --version/--help are faster than old; record-reading commands are above old (+30%), as the PR Known gap states.
E2: import pydantic added to cli.py in a scratch copy: test_the_start_up_imports_only_the_standard_library_and_chantier fails naming pydantic, pydantic_core, typing_extensions, typing_inspection.
E3: 36 cases (root --help, 32 command --help, status --no-such-option, unknown command, no command): base vs head output and exit code identical.
E6: uv run --locked --project <worktree> chantier --version -> 0.9.0; status identical to base; worktree git status clean.
PR body matches diff.
Verdict: VERIFIED
