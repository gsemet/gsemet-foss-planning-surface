# Integration flake: `checkbox-toggle` times out waiting for the first checkbox render

Seen in CI on PR #365 (CR 288, head 601e0bf1, heavy run 43079731969 attempt 1): the integration
job failed on a `checkbox-toggle` step timeout while waiting for the first checkbox to render.
Attempt 2 passed. Unrelated to the change under test.

Expected: the step waits on a reliable render signal, or the cause of the slow first render is
found; the scenario passes without reruns.
