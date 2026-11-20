# Release notes highlights: text first, picture cropped on the change

Priority: P1, next batch. Owner, 2026-11-20, after the 1.10.0 notes: "pour le modele prochaine dans la release notes j aimerais que le paragraphe commence par le texte, et que l'image soit cropper sur le point d attention", then "fait ca en P1 prochain batch".

The owner's example (the 1.10.0 highlight, reordered):

    ## ✏️ Edit one list item, not the whole list

    A click on the list itself, outside its items, still edits the whole list.

    ![Left, a click on a list item opens the whole list in the editor; right, the same click opens only that item](edit-one-list-item.png)

Change to `.agents/guidelines/release-process.guidelines.md`, section "Release notes" ("Writing"
and the skeleton item 3), for the next release:

1. **Text first.** A highlight is its heading, then its sentences (at most two), then the picture.
   Today the rule is heading, picture, then text.
2. **Crop on the point of attention.** Each picture is cropped to the part of the screen where
   the change happens: no toolbar, empty margin or unrelated content around it. In the 1.10.0
   joined before|after image, the floating toolbar and the frontmatter table take a third of the
   frame. A joined before|after image crops both halves to the same region, at the same scale.
   The drag capture keeps the list and its handles, not the alerts below.
3. Keep the other rules (joined before|after image, no text under a picture that shows the whole
   change, settings named as settings).

The generic part (text first, crop) is also sent to chantier for `release-template.md`. Studio
keeps its own copy because chantier may not be updated by the next release.
