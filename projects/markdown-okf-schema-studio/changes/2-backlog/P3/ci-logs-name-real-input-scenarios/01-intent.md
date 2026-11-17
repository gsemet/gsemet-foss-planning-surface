# CI logs name each real-input scenario

Found in the table run (CRs 288–293): the integration job's log prints no scenario names for the
real-input suite, so a reviewer cannot see that a new scenario (`exportHtml`, `find-wide-table`,
`table-tab-row`...) ran and passed; only the step's green status proves it.

Expected: the real-input suite logs one line per scenario with its name and result, like the
visual job (`passed: <group>/<id>`).
