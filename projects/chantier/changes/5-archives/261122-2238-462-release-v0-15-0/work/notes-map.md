## Highlight: the web board as the place to steer
- e15fccb3 feat(board): an Inbox page of what needs the user
- dda590d9 feat(board): History page of what was done per day, week or month
- e3877937 feat(board): Dashboard page, productivity and spending by closed batch
- dc50ba39 feat(board): a Help page of chantier's concepts and roles
- e4171908 feat(board): batch page Kanban of the batch's three folders
- 63e23360 feat(board): batch graph with transitive reduction, merged CRs folded, fewer crossings
- ce706c2d feat(griller): the web board's Grill button and discussion panel (round 4)
- 113bf187 feat(griller): the board's Griller engine, API ops, write guard and docs (rounds 2-3)
- 86fe6966 feat(griller): the board's Griller roles, defaults and rules (round 1)

## Highlight: the CLI run remotely, two keys
- f7171e1f feat(cli): rename the surface server's command to serve; add webui
- dd30ecd7 feat(board): a public read-only key beside the private key
- bb8765a4 feat(board): a paste field for a lost key and SameSite=Lax cookies
- 28bb7f91 feat(cli): run CLI commands remotely through the surface server
- d60b3538 feat(board): listen on this machine by default, open to the network on ask, cookie lasts 30 days
- ef2361fb feat(board): the server's API over a WebSocket, the web board one client among others
- d7b5a019 feat(board): the web client moves to clients/web; board --ui <folder>|none
- bbb236fe feat(cli): chantier live, a read-only terminal client of the board's API
- dce2c644 feat(live): keys to scroll and filter, and up to four boards in one screen

## Highlight: the forge followed for you
- c51aea6a feat(cli): forge connectors as plugins, and a hub that polls only what is awaited
- 9b55b0a4 feat(cli): typed waits, a CR records what it waits for
- 75a73d59 feat(cli): an outside poller writes issue events into the journal
- f7c18f1a feat(writer): the surface server commits, rebases and pushes the plan
- 22bc9e51 feat(board): the server watches the planning files and reads the forge only while observed
- 4f0ff6d8 feat(watch): the watcher subscribes to the surface server and starts the board
- 3866d764 feat(journal): typed events name@N, version 2 lines, published schemas

## Smaller: board polish
- 49245a7b feat(board): one arrowhead per waiting CR, lit arrows on top, a tooltip on the mode switch
- 35ab0d19 feat(board): the Batch page's mode and legend move into the title row
- 24ae4045 feat(board): the Batch page's mode and legend move into the title row
- 82cebbc4 feat(board): fold each Triage priority row and explain the writes count
- adca88a1 feat(board): split the backlog's last column into running batch and next batch

## Smaller: orders and stacks
- a6a4ac22 feat(orders): order drop names where the CR goes (trash, inbox or backlog)
- ab2e44cf feat(order): drop a CR to ready, never to the inbox
- f9087d67 feat(order): hold a ready CR out of the stack
- e7feda55 feat(order): hold a live CR in every batch mode
- 99fa847f feat(park): the Foreman parks a CR stuck on an outside wait
- 3b3eba06 feat: replace the factory mode with a choice of destination at the grill
- 1f86ece9 feat(cli): a CR taken out of a batch comes back under its number, with its branch and PR
- aa0befe3 feat(stack): check an ordered stack as a git chain at ship and stack --out-of-draft
- 92c7a795 feat(stack): start a stack CR on another CR's branch only once it is ready
- a70d0557 feat(stack): a stack batch keeps its shape after compactions
- 96d5e0b7 feat(cli): take's base and the ready word follow the forge

## Smaller: other visible
- 56681802 feat(cli): a CR's title stays short, at most 72 characters, checked by validate, summary lint, file and the board
- 9bd055ec feat(archives): archive a PR merged without chantier; validate checks an outside archive's name
- daec1986 feat(cli): access explains why a session may or may not write, claim or push
- e461ffd2 feat(cli): Driver leases on what take gave them: --lease, lease renew/hold, take --reclaim
- 2a19b7de feat(gate): run only named long gates and make lease hold run nothing
- 906e5fd1 feat(launch): dev mode only for chantier itself, other projects in plugin mode
- 56f753e6 feat(sync): a blocked uv sync names chantier's holders, waits, never kills
- 33d10454 feat(preflight): allow rules name real paths and broad ones are named
- 0e36d1f8 feat(cards): a refused force push climbs Foreman, Chief of Staff, then the user
- fd970ca9 feat(release): just tag fast-forwards the main checkout before it tags
- 299d2c1f feat(cards): one Driver per CR, a smaller driver card and a closing step that resumes from the record
- 687a4723 feat(board): tell a dev session when the surface server runs a foreign build
- e9f086af feat(writer): downloaded CI artifacts stay out of the published plan; path-too-long blocked reason

## All fixes: board and stack
- 9e2a29f9 fix(board): the phone's bottom bar scrolls sideways when its items no longer fit
- 16949f41 fix(board): a batch CR's card shows its batch folder, not its old priority chip
- 392b2811 fix(board): a native stack's merges into the branch below are told landed
- c79f01e7 fix(titles): record and show a CR's plain subject, without the Change Specification lead
- 72886c96 fix(griller): fit the startup size and code-size gates after the rebase
- 9f847fc5 fix(board): keep the lease-hold file pattern constant after the restack
- c992715b fix(stacks): a CR started on a held CR starts on the default branch
- fe825f70 fix(stacks): an ended start_on owner still falls back below; only a held one goes to the default branch
- 0b7868b7 fix(stacks): one base function for an unplaced CR of a stack batch
- db0000e7 fix(stacks): a placed CR keeps only its recorded start base
- 8d67da41 fix(carry): a clean rebase in a stack carries whatever branch the record names
- b2ea51bf fix(open): refuse a missing project clone instead of crashing
- 27269e99 fix(store): wait out a held CR folder on Windows, then refuse with the cause
- ef4eff6d fix(hub): a transient read error no longer erases the server's state entries
- 8bd198b1 fix(gate): the long gate's queue survives a sharing violation on a ticket or mark
- dda8ac97 fix(cli): a several-line request with no heading is refused with the long-title message, as specified
- f1d1c911 fix(release): version.py dispatches the ff-main subcommand
- bd5befc7 fix(writer): the test's pre-commit hook is executable, so git runs it on POSIX
- 8febc005 fix(cli): split the Driver's record registration to keep functions small after the rebase
- 18a6c0c2 fix(cli): keep the merged hub journal docstring short and Interest's meta a keyword after the rebase
- ddc5a525 fix(store): callers of journal.read pass the store after the restack
- 18f2ac2b fix(store): journal.py import order after the restack

## All fixes: tests and scenario
- 7afbc5f3 fix(scenario): read the typed journal lines and a full-length head
- 1acb0d66 feat(scenario): typed_waits case in the gitlab unit, with the fake glab's graphql answer
- d2f56037 fix(scenario): the board's idea text starts with a heading; the no-heading refusal says so
- fc537bfd fix(scenario): the inbox refusal of order drop exits usage
- 3b76a63e fix(scenario): name the gate under a project flag and ignore the harness's own chantier.yaml
- 7fab8717 fix(scenario): the link's cookie carries the server's per-server cookie name
- 0ae11477 fix(scenario): init the planning folder of serve_and_webui's surfaces
- d61a0a60 fix(scenario): serve_and_webui starts its servers without a seat
- 54736c33 fix(scenario): keep the events frames seen while waiting for a move result
- cb914330 fix(scenario): the server scenario's cli_form follows the plugin-mode form
- 8a295840 fix(scenario): the welcome check counts the 21 ops and 7 topics
- 5691a05d fix(scenario): the server's welcome counts the new cli.run op
- 42063735 fix(scenario): the welcome lists 21 ops since dashboard.get
- e5dc6952 fix(test): recognise stdlib frames by real path in the store run-time proof
- a5d928a9 fix(test): make the live --only refusal and the folder-lock test deterministic

## Contributors: store
- a8f17555 feat(cli): the plan's storage behind a minimal store interface
- c710478b feat(store): the plan's store reads the planning folder through one read interface
- eb69264a feat(store): the last readers read the planning folder through the store
