# Tests: skip symlink tests on hosts that cannot create symlinks

Asked by the user on 2026-11-25, during batch-01, in their words: "pour la gate qui passe pas sur
la machine, met les tests en skip avec un message qui explique" (for the gate that does not pass on
the machine, skip the tests with a message that explains why). Filed, not grilled. A few minutes
later the same day the user enabled Windows Developer Mode, which unblocked the gate on that
machine.

Observed at `41fcd6d` (branch of CR `show-extensionless-names`) on a Windows host without the
symlink privilege (Developer Mode off, session not elevated): `just preflight` failed with 8 failed,
1112 passed, 21 skipped. The failures are symlink creation refused (`WinError 1314`), in tests that
CR does not edit. Test files that call `symlink_to`: `tests/test_cli_core.py`,
`tests/test_file_links.py`, `tests/test_kb_install.py`, `tests/test_skill_installer.py`,
`tests/test_skill_resources.py`.

Wanted: on a host that cannot create symlinks, those tests are skipped and the skip message says
why. The new symlink tests of CR `show-extensionless-names` already skip on such a host.

Open for the grill: skip only when symlink creation is refused (the Linux, macOS and Windows CI jobs
keep running them), and what the message tells the contributor to enable.
