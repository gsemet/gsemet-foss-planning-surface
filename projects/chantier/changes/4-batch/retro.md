
## 2026-11-23: CR-463, CR-464

- nothing worth changing (critic: 3 points dropped)

## 2026-11-26: CR-465, CR-466, CR-467, CR-468, CR-469, CR-470, CR-471, CR-472, CR-473, CR-474, CR-475, CR-476, CR-477, CR-478, CR-479, CR-480, CR-481, CR-482, CR-483, CR-484, CR-485, CR-486, CR-487, CR-488, CR-489, CR-490, CR-491, CR-492, CR-493, CR-494, CR-495, CR-496, CR-497, CR-498, CR-499, CR-500, CR-501, CR-502, CR-503, CR-504, CR-505, CR-506, CR-507, CR-508, CR-509, CR-510, CR-511, CR-512, CR-513, CR-514

- [project] Flaky tests: `test_serve_webui` failed its port walk in macOS CI on CR-491, CR-492 and CR-493, and the board-griller moved-folder test failed once on CR-481: fix or isolate them.
- [chantier] Card rewrite CRs far past their budget (CR-507 15 rounds and $135.54, CR-510 $54.57, CR-511 $28.98; CR-505 and CR-507 spent their 3 rounds before the last part; batch budget raised 400, 600, 800; CR-512..514 dropped to the backlog): the specification splits such a CR into parts that each fit the round limit.
- [chantier] PR descriptions repeatedly came back NOT VERIFIED, many on the description alone (CR-467, 473, 480, 490, 507, 510, 511), each costing another Verifier run: the CLI writes the body's factual parts (gates, heads, gaps) from the record.
- [chantier] Workers or Drivers acted outside their role or folder (stray files outside `writes:` on CR-474, Verifiers changing into the CR folder on CR-507 and CR-510, a Driver editing code with no Coder on CR-477 and CR-497): enforce it by the write guard and a CLI rail, not card lines.
- [chantier] CRs labelled ready to merge while their own gaps said not to merge them alone (CR-505, 507, 510), and the owner merged CR-510 while CR-511 still worked, against the order that every Driver finish first: the CLI words a held state instead of ready to merge.
- [chantier] Cards and CLI disagree after the swap (`help <topic>` refuses the `--batch` of the brief's CLI line; `next` asks for a stack ask while `judge` words an alone ask; `push`'s `next:` line and the card order differ on the gate; the watcher outlives the heartbeat in `wakes-p1` and is stopped by `wakes-p2` and the Foreman card; the PR template's "nothing follows </details>" clashes with the host's attribution line; `ship` and closing disagree on a description-only NOT VERIFIED; stale sentences quoting removed CLI output, O-175 and O-176): tests that tie card sentences to the CLI's output.

(critic: kept 6, dropped 10)
