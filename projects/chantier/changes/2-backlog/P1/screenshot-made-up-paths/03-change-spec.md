# Change Specification: images use made-up paths, checked before they are kept or uploaded

## Goal

No image an agent sends to the forge, or keeps in the planning folder (pushed to GitHub with the
planning surface), shows the user's username or home folder. In batch-22, CR-305 attached
screenshots of the live board to PR 254 that showed a local path with the username; only the
description pass caught it, after the upload. The long-term fix, in the user's terms
(`02-answers.md`): the Driver and Verifier cards require made-up paths and no username in any
image, and an explicit look at each image for the user's username and home folder before it is
uploaded to the forge (paths-Q1) and before it is kept in the planning folder (paths-Q3); the
image goes on only once neither shows. The user's own screenshot that shows one is not uploaded
(paths-Q2), and a leak found after an upload is replaced and reported to the user (paths-Q4).

The CR has no `issue:` line. The folder has no `01-intent.md`; `intake/request.md` and
`02-answers.md` are the whole input.

## What changes

Cards only, in the plugin repository (`C:/Users/gaeta/Projets/chantier`). No CLI code, no agent
file (`agents/`, `com.github.copilot/agents/`), no hook, no test, no scenario step changes. The
new text goes in the cards' full sections, not in their `## Startup core` sections (those count
toward the 12288-byte startup limit of `skills/chantier/references/startup-manifest.json`).

### Terms used in the cards

Spelled out once in each changed card (the Driver's and the Verifier's), as follows.

- **The user's username**: both values the machine can show, and the look checks each: the
  login name of the machine the agent runs on (`$env:USERNAME` on Windows, `$USER` on Linux and
  macOS), and the last part of the home folder's path. They are usually the same, but can differ
  (on Windows, after an account rename the home folder keeps its old name); when they differ, the
  look checks both.
- **The user's home folder**: its full path (`C:\Users\<name>`, `/Users/<name>`, `/home/<name>`),
  in any form it can take on screen (back or forward slashes, `~` expanded, inside a longer path
  such as a temporary folder under it, e.g. `C:\Users\<name>\AppData\Local\Temp\...`).
- **A made-up path**: a path that holds neither of the two, shown wherever the image shows a
  local path (a planning folder, a worktree, a file, a terminal prompt, a window title). The
  agent chooses how to get it (a scratch folder at a neutral location, a project or folder name
  that is made up, the replacements of [release-template](https://github.com/gsemet/chantier/blob/main/skills/chantier/references/release-template.md), "Visible
  evidence": `~`, `user`); the card names the result, not the means.
- **The look**: the agent opens the image (reads it as an image, not its file name) and looks
  for the user's username and home folder. An image passes once neither shows.
- **Keeping an image**: writing an image file anywhere in the planning folder (`.agents/changes/`
  or the project's folder of an external planning surface), whatever the sub-folder: a CR's
  `evidence/` or `work/` (the Verifier's `work/verifier/evidence/`, a Driver's file its forge's CLI
  cannot upload, the release Driver's captures), a QA work folder's `evidence/`. The planning
  folder is pushed with the surface (only `work/gates/` and `*.log` are gitignored), so a kept
  image reaches the forge too.
- **An upload to the forge**: any way an image leaves the machine for the forge: `gh pr edit
  --attach` (or another forge CLI's attach), a release asset upload, and a push of a commit that
  adds or changes an image file (the CR's cleaned archive in the PR with its `evidence/`, a
  release folder's images).

### `skills/chantier/references/driver.md`

1. `## Your means`, the bullet "The evidence:" (now around line 324), where the rule is written
   once, with the terms above:
   - Every image the Driver keeps or uploads shows made-up paths and no username. It gives each
     image the look before it keeps it and again before each upload, and keeps or uploads it only
     once it passes (paths-Q1, paths-Q3). An image of its own that fails is captured again with
     made-up paths; one from the Verifier that fails is asked again of the Verifier; none is kept
     or uploaded in the meantime.
   - The user's own screenshot (a taken-back note `evidence: <path>`, same bullet) gets the look
     before the upload. When it fails (paths-Q2), the Driver does not upload it, keeps the Known
     gap it was meant to close (the bullet stays in the PR's Known gaps, so the ready line quotes
     it), and says why (the image shows the username or the home folder) in a `note` and in its
     hand-back report. It does not copy that image into the planning folder.
   - A leak found after an upload, on the description pass (the Driver's own, or the Verifier's
     `NOT VERIFIED` on it, item 2 of the Verifier below) (paths-Q4): the Driver replaces the image
     in the description with a clean capture (captured again with made-up paths, given the look),
     and says in a `note` and in its hand-back report that the old one was uploaded (the PR, which
     image, at which SHA). A removed attachment can stay reachable on the forge, which is why the
     user is told. When the leaked image is the user's own screenshot, which the Driver cannot
     capture again, it removes it from the description and puts the Known gap back, as for
     paths-Q2, with the same `note` and report.
2. `## Your means`, the bullet "The archive in the PR:" (now around line 330): a pointer to the
   rule: before the commit that adds or changes an image in the archive (`evidence/`, a retained
   prototype's images), each such image passes the look; one that fails stays out of the commit
   until it passes.
3. `## QA driver` (now around line 903): a pointer to the rule (paths-Q3): each screenshot kept in
   the work folder's `evidence/` shows made-up paths and passes the look before it is kept; one
   that fails is captured again with made-up paths, and one that cannot be is not kept and
   `04-result.md` says so in the finding it belonged to. The QA driver holds no CR and makes no
   hand-back, so paths-Q2 and paths-Q4 do not apply to it.
4. `## Release driver`, the bullets "The release notes and the announcement thread..." (now
   around line 941) and "Images in the body:" (now around line 960): keep "anonymised before it
   leaves the machine" and point to the rule: each capture the release Driver keeps in the work
   folder (`work/`) or in the folder the procedure commits passes the look before it is kept
   (paths-Q3), and again before each upload (a release asset, a push of the release folder's
   images). It does not replace release-template's existing rule that the Driver reads each image
   it produced before keeping it, nor its wider anonymisation list; it adds the look for the
   username and the home folder to that reading, and the last look before the upload.

Write the rule once (in "Your means", next to "The evidence:") and point to it from the other
places, rather than repeating it.

### `skills/chantier/references/verifier.md`

1. `## Your part`, the paragraph "At the end, with the technique of the plan you were given,
   capture the evidence..." (now around line 108): every before and after image the Verifier
   captures shows made-up paths and no username (the terms as above, spelled out in the card). It
   opens each capture, as it already does for what the capture claims, and also gives it the look;
   a capture that fails is captured again with made-up paths before it is kept in
   `<work folder>/verifier/evidence/` (paths-Q1, paths-Q3); one it cannot capture that way is not
   kept and is named in `before-after.md` with why, as evidence that cannot be captured already is.
2. `## Your part`, the paragraph "The PR's description, as posted on the forge, is one of the
   claims: it must be clean (...) and consistent with (...). A description that fails either is
   `NOT VERIFIED`." (now around lines 73-76): add a third condition next to "clean" and
   "consistent": no image attached to the description shows the user's username or home folder.
   The sentence becomes "a description that fails any of the three is `NOT VERIFIED`". This is a
   new condition, not an application of "clean" or "consistent". The capture paragraph's last
   sentence ("On the description pass, check that the images attached are the ones captured at
   the SHA they name.") points to it: on the description pass, the Verifier gives each attached
   image the look too, and its `verify.md` names an image that fails (which one, what shows), so
   the Driver replaces it (Driver item 1, paths-Q4).

The Verifier never uploads (it never pushes or edits the PR); its part is the capture and the
description check, which make the Driver's look the second one, not the only one.

### `skills/chantier/references/chief-of-staff.md`

The answers give the Chief of Staff two acts; its card says them, in the bullet "A plain
`ready-to-merge <cr> <link> gaps: …` ask" (now around lines 1011-1019) and its stack counterpart
(now around lines 1050-1055):

1. paths-Q2: where it asks the user for the board pane screenshot, it asks for one with made-up
   paths, no username and no home folder in it. When the Driver's report says the user's
   screenshot was not uploaded because it showed one, it says so to the user and asks for a new
   one with made-up paths (the gap is still quoted, so the existing ask applies).
2. paths-Q4: when a Driver's `note` or hand-back report says an image that showed the username or
   home folder was uploaded and replaced, it tells the user: the PR, the image, and that the old
   attachment may stay reachable on the forge. It does nothing more (no clean-up; the user
   decides). How that report reaches it: open question 1.

## Decisions carried from `02-answers.md`

- paths-Q1: the Driver and Verifier cards require made-up paths and no username in any image:
  Driver items 1 to 4, Verifier items 1 and 2.
- paths-Q1: an explicit look before every upload to the forge, uploading only once neither the
  username nor the home folder shows: Driver items 1, 2 and 4 (the Driver is the one that
  uploads); the Verifier's checks of its captures and of the description (items 1 and 2) are how
  its card requires the same of the images it produces.
- paths-Q2: the user's own screenshot that shows the username or home folder is not uploaded;
  the Known gap stays; the Driver says why in a `note` and its hand-back; the Chief of Staff asks
  the user for a new one with made-up paths: Driver item 1, Chief of Staff item 1.
- paths-Q3: every image a Driver or Verifier keeps in the planning folder follows the rule and
  gets the same look before it is kept, the QA driver's `evidence/` and the release Driver's
  `work/` captures included: the term "keeping an image", Driver items 1, 3 and 4, Verifier item 1.
- paths-Q3: images already committed (CR-305's) are left as they are: out of scope.
- paths-Q4: a leak found after upload, on the description pass: the Driver replaces the image
  with a clean capture and says in a `note` and its hand-back that the old one was uploaded; the
  Chief of Staff tells the user: Driver item 1, Verifier item 2, Chief of Staff item 2. The case
  of the user's own screenshot found after upload (it cannot be captured again) composes paths-Q4
  with paths-Q2: removed, the Known gap put back.
- The spec critic's note on paths-Q1 (it changes two roles' cards and what may reach the forge)
  set the scope; the answers to paths-Q2 and paths-Q4 add the two Chief of Staff acts above,
  nothing more of its card.

## Out of scope

- Any CLI change: no scan of images, no new command, no board option to hide or mask paths
  (`chantier board` and its `--now` flag are unchanged). A new CLI tool comes only from measured
  token cost (AGENTS.md).
- Text (PR bodies, comments, notes): already covered elsewhere (the Chief of Staff's ticket
  check, release-template's anonymisation); this CR is about images.
- Other roles' cards beyond the Chief of Staff's two acts: the Foreman, the Inspector, the Coder,
  the Debugger, the Investigator, the Conflict resolver, the Demo explorer; the Chief of Staff's
  ticket comment `--attach` and the images it saves in a CR's `evidence/` during a grill. Only the
  Driver and Verifier cards carry the rule, as the answers say.
- Other personal data in images (email, git user name, session ids, private repositories): the
  answers name the username and the home folder only; release-template keeps its own wider list
  for release images.
- Images already committed or uploaded (CR-305's in the planning surface, PR 254's on the forge):
  no clean-up; the user leaves them as they are (paths-Q3). A leak found later is told to the
  user, not removed from the forge's storage by an agent.
- Editing an image (crop, mask) to hide a path: not one of the answers' routes; a failing image is
  captured again or, for the user's, asked again.

## Evidence

- `git diff` of the PR touches only `skills/chantier/references/driver.md`,
  `skills/chantier/references/verifier.md` and `skills/chantier/references/chief-of-staff.md`;
  no `## Startup core` section changes.
- A reading of each changed passage against the items above: the rule and the terms in the
  Driver's "Your means", with pointers from the archive bullet, the QA driver and the Release
  driver's two bullets; the paths-Q2 and paths-Q4 cases in the same "Your means" bullet; in the
  Verifier's capture paragraph, and, as a third condition, in its paragraph on the PR's
  description; the Chief of Staff's two acts in its gap bullets.
- `just check` passes (lint, the structure tests including the startup manifest's size limit, the
  release notes check).
- `just scenario` passes (AGENTS.md: a change to the cards passes it before its PR), with the
  pipeline's `just scenario (ubuntu-latest)` job green at the PR's head.
- No screenshot of the board pane is needed (the pane is not touched).
- The PR's own Deliverables, and any image kept in this CR's planning folder, follow the new rule.

## Open questions

None. The Chief of Staff settled the last one (2026-11-17): the paths-Q4 report reaches the Chief of
Staff through the Foreman, which relays that part of the Driver's hand-back report with the ready
ask (one clause in `foreman.md`); in direct mode the Chief of Staff reads the hand-back itself. The
Driver's `note` stays the record. Nothing about the leak goes in the public PR.
