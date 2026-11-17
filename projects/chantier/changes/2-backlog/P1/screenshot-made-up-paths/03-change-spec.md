# Change Specification: images use made-up paths, checked before any upload

## Goal

No image an agent sends to the forge shows the user's username or home folder. In batch-22,
CR-305 attached screenshots of the live board to PR 254 that showed a local path with the
username; only the description pass caught it, after the upload. The long-term fix, in the user's
terms (`02-answers.md`, paths-Q1): the Driver and Verifier cards require made-up paths and no
username in any image, and an explicit check before every upload to the forge: the agent looks at
the image for the user's username and home folder, and uploads only once neither shows.

The CR has no `issue:` line. The folder has no `01-intent.md`; `intake/request.md` and
`02-answers.md` are the whole input.

## What changes

Cards only, in the plugin repository (`C:/Users/gaeta/Projets/chantier`). No CLI code, no agent
file (`agents/`, `com.github.copilot/agents/`), no hook, no test, no scenario step changes. The
new text goes in the cards' full sections, not in their `## Startup core` sections (those count
toward the 12288-byte startup limit of `skills/chantier/references/startup-manifest.json`).

### Terms used in both cards

- **The user's username**: both values the machine can show, and the check looks for each: the
  login name of the machine the agent runs on (`$env:USERNAME` on Windows, `$USER` on Linux and
  macOS), and the last part of the home folder's path. They are usually the same, but can differ
  (on Windows, after an account rename the home folder keeps its old name); when they differ, the
  check looks for both.
- **The user's home folder**: its full path (`C:\Users\<name>`, `/Users/<name>`, `/home/<name>`),
  in any form it can take on screen (back or forward slashes, `~` expanded, inside a longer path
  such as a temporary folder under it, e.g. `C:\Users\<name>\AppData\Local\Temp\...`).
- **A made-up path**: a path that holds neither of the two, shown wherever the image shows a
  local path (a planning folder, a worktree, a file, a terminal prompt, a window title). The
  agent chooses how to get it (a scratch folder at a neutral location, a project or folder name
  that is made up, the replacements of [release-template](release-template.md), "Visible
  evidence": `~`, `user`); the card names the result, not the means.
- **An upload to the forge**: any way an image leaves the machine for the forge: `gh pr edit
  --attach` (or another forge CLI's attach), a release asset upload, and a push of a commit that
  adds or changes an image file (the CR's cleaned archive in the PR with its `evidence/`, a
  release folder's images).

### `skills/chantier/references/driver.md`

1. `## Your means`, the bullet "The evidence:" (now around line 324): add that every image the
   Driver uploads shows made-up paths and no username, and that before each upload it opens the
   image (reads it as an image, not its file name) and looks for the user's username and home
   folder, and uploads only once neither shows. An image of its own that shows one is captured
   again with made-up paths, or asked again of the Verifier, before the upload; none is uploaded
   in the meantime. The same check covers the taken-back note `evidence: <path>` image of the same
   bullet (what happens when that image fails it: open question 1).
2. `## Your means`, the bullet "The archive in the PR:" (now around line 330): before the commit
   that adds or changes an image in the archive (`evidence/`, a retained prototype's images), the
   same check on each such image; one that fails stays out of the commit until it passes.
3. `## Release driver`, the bullets "The release notes and the announcement thread..." (now
   around line 941) and "Images in the body:" (now around line 960): keep "anonymised before it
   leaves the machine" and add the explicit check before each upload (a release asset, a push of
   the release folder's images): the Driver opens each image and uploads it only once neither the
   username nor the home folder shows. It does not replace release-template's existing rule that
   the Driver reads each image it produced before keeping it; it is the last look before the
   upload.
4. `## QA driver` (line 903): its screenshots go to the work folder's `evidence/`, not to the
   forge; no change, unless the Driver judges a one-clause pointer to the rule useful when such a
   screenshot later reaches a PR (it would then fall under item 1 anyway).

Write the rule once (in "Your means", next to "The evidence:") and point to it from the other
places, rather than repeating it three times.

### `skills/chantier/references/verifier.md`

1. `## Your part`, the paragraph "At the end, with the technique of the plan you were given,
   capture the evidence..." (now around line 108): every before and after image the Verifier
   captures shows made-up paths and no username (both terms as above, spelled out in the card).
   It opens each capture, as it already does for what the capture claims, and also looks for the
   user's username and home folder; a capture that shows one is captured again with made-up paths
   before it is kept in `<work folder>/verifier/evidence/`; one it cannot capture that way is
   named in `before-after.md` with why, as evidence that cannot be captured already is.
2. `## Your part`, the paragraph "The PR's description, as posted on the forge, is one of the
   claims: it must be clean (...) and consistent with (...). A description that fails either is
   `NOT VERIFIED`." (now around lines 73-76): add a third condition next to "clean" and
   "consistent": no image attached to the description shows the user's username or home folder
   (both terms as above). The sentence becomes "a description that fails any of the three is
   `NOT VERIFIED`". This is a new condition, not an application of "clean" or "consistent". The
   capture paragraph's last sentence ("On the description pass, check that the images attached
   are the ones captured at the SHA they name.") points to it: on the description pass, the
   Verifier opens each attached image and looks for the username and the home folder too.

The Verifier never uploads (it never pushes or edits the PR); its part is the capture and the
description check, which make the Driver's check the second look, not the only one.

## Decisions carried from `02-answers.md`

- paths-Q1: the Driver and Verifier cards require made-up paths and no username in any image:
  Driver items 1 to 3, Verifier items 1 and 2.
- paths-Q1: an explicit check before every upload to the forge, the agent looking at the image
  for the user's username and home folder, and uploading only once neither shows: Driver items 1
  to 3 (the Driver is the one that uploads); the Verifier's checks of its captures and of the
  description (items 1 and 2) are how its card requires the same of the images it produces.
- The spec critic's note (it changes two roles' cards and what may reach the forge) is the scope
  of this specification.

## Out of scope

- Any CLI change: no scan of images, no new command, no board option to hide or mask paths
  (`chantier board` and its `--now` flag are unchanged). A new CLI tool comes only from measured
  token cost (AGENTS.md).
- Text (PR bodies, comments): already covered elsewhere (the Chief of Staff's ticket check,
  release-template's anonymisation); this CR is about images.
- Other roles' cards: the Chief of Staff (its ticket comment `--attach`, its ask to the user for a
  board pane screenshot), the Foreman, the Inspector, the Demo explorer, the Investigator. Only the
  Driver and Verifier cards change, as the answer says.
- Other personal data in images (email, git user name, session ids, private repositories): the
  answer names the username and the home folder only; release-template keeps its own wider list
  for release images.
- Images already on the forge (PR 254's): no clean-up is part of this CR.

## Evidence

- `git diff` of the PR touches only `skills/chantier/references/driver.md` and
  `skills/chantier/references/verifier.md`; neither `## Startup core` section changes.
- A reading of each changed passage against the items above: the rule is in the Driver's "Your
  means" with pointers from the archive bullet and the Release driver's two bullets, and in the
  Verifier's capture paragraph and, as a third condition, in its paragraph on the PR's description.
- `just check` passes (lint, the structure tests including the startup manifest's size limit, the
  release notes check).
- `just scenario` passes (AGENTS.md: a change to the cards passes it before its PR), with the
  pipeline's `just scenario (ubuntu-latest)` job green at the PR's head.
- No screenshot of the board pane is needed (the pane is not touched).
- The PR's own Deliverables, if they carry any image, follow the new rule.

## Open questions

1. The user's own screenshot, taken back as `evidence: <path>` (a board pane image the Chief of
   Staff asked the user for), shows the username or home folder: what does the Driver do? The
   Driver cannot capture it again. Proposed: it does not upload it, keeps the Known gap, says why
   in a `note` and in its hand-back, and the Chief of Staff asks the user for a new one with
   made-up paths. Alternatives: the Driver edits the image (a crop or a mask) and uploads it once
   neither shows; or it stops with `handback blocked question:`.
