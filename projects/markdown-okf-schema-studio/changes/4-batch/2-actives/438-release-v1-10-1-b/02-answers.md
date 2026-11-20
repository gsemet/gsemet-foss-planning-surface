Short name: `rel-1101`

1. rel-1101-Q1: **Version.** Owner, 2026-11-20: "super, fais une release (patch)": v1.10.1.
2. rel-1101-Q2: **Scope.** Set by the Chief of Staff from the owner's go: batch-07 (CR-435,
   CR-436). The headline is the CR-436 fix: a block left unchanged in a CRLF file no longer
   leaves the editor stuck on "Saving Markdown...", and Studio keeps each file's own line endings
   ("Markdown studio doit respecter le format original c'est dans son ADN").
3. rel-1101-Q3: **Release notes shape.** The owner's wish for the next notes, 2026-11-20 (backlog
   item `relnotes-text-first-crop`, not yet in the guideline): "pour le modele prochaine dans la
   release notes j aimerais que le paragraphe commence par le texte, et que l'image soit cropper
   sur le point d attention". For this release: each highlight is its heading, then its text (at
   most two sentences), then the picture, cropped to where the change happens. A patch with no
   visible change may have no picture.

Owner, 2026-11-20, late evening: "je t'autorise a faire la release tout seul et a autoapprover la release notes et merger la PR de release."
- rel-1101-Q4: the release runs under a grant (releases=1): the steering session approves the release
  notes, merges the release PR (by rebase) and runs the post-merge steps (tag, GitHub release,
  Marketplace). The announcement stays a draft for the owner.
- rel-1101-Q5: refiled after CR-437 was cancelled (it had been dropped to let the night's CRs join; the
  owner's grant then made a release tonight possible). Same version, scope and notes shape.
