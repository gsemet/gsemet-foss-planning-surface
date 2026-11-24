# Heavy CI red on main: preview-smoke finds no admonition in a real window

The real-VS-Code CI jobs (`integration`, `stress`, run on each push to `main` and by
`gh workflow run ci.yml --ref <branch> -f heavy=true`) have failed on `main` since d762a732, at
their first step `preview-smoke`: "The input did not match the regular expression /admonition/iu".
The last green run is at d9b3cd6b (run 45142308892). The first red is at d762a732 (run 45156102152),
and 2e2efa6c is red too (run 45187475612).

The commits in between came from batch-08 and batch-09's first stack, which merged with no heavy run on their heads:
20b12216 (render reads conf.py, toctree and resources through the async port), 35258332, c19e5a77,
7b8339e9 (core and session paths through one module), b4a8cb12 (PlantUML through ProcessRunner),
f9911175 and d762a732.

Find the cause, then fix what is wrong. If the real preview lost its admonitions, fix the product.
If only the test drifted, fix the test. Then get the heavy run green again. This must land before
1.12.1, at the bottom of batch-09's stack, so that the other CRs and the release are proven in a
real window.
