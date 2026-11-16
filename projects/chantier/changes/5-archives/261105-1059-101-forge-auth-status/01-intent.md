# Intent

The Chief of Staff's card asks for `gh auth status` before a batch (P9). The eval kit's fake forge
refuses that call, so a live eval cannot pass preflight as the card writes it, and the audit would
count the call as forbidden.

This CR is also a real-tools eval of chantier on its own repository: the PR is opened on GitHub,
with real CI, and is never merged.
