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

2026-11-21, Chief of Staff under the owner's autonomy rule ("tu es maintenant autonome. plus de question.
... tu me livres a la fin de la nuit une stack mergeable"):
- rel-1110-Q1: **Version 1.11.0, not 1.10.1.** The release now ships the whole batch-07 stack, which adds
  features (Delete block button, blank-lines block, open at a searched line), so it is a minor version.
  CR-437 and CR-438 (1.10.1) were cancelled so the night's CRs could join the batch: a started release
  refuses new CRs, and its PR could not be merged before morning.
- rel-1110-Q2: **Scope:** every CR of batch-07 (CR-435, CR-436 already merged, CR-439 to CR-445). Notes
  follow the new text-first, cropped-picture rule (CR-442).
- rel-1110-Q3: **Merge and post-merge steps.** The owner's earlier grant ("je t'autorise a faire la release
  tout seul et a autoapprover la release notes et merger la PR de release") could not be used tonight (the
  Foreman's start was refused by its safety check). The release PR sits at the top of the stack; the owner
  merges the stack in the morning, and tag, GitHub release and Marketplace wait for the owner's word.
