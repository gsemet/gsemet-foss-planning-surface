# Local just scenario passes while the user's board runs

Retro of batch-30: the scenario's serve/webui cases bind the default port 8765 and expect no board, so a local `just scenario` fails while the user's own board runs; the top CR's local Windows run was waived twice for that. Those cases take a free port and init their own folders.