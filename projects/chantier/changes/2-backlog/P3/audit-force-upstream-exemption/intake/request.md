# audit.py's set-upstream exemption lets a forced push to main through

audit.py's -u/--set-upstream exemption accepts 'git push -f -u origin main': check forced first (found by CR-191's Inspector, batch-14, pre-existing).