---
title: Feature clip okf-frontmatter
status: draft for the owner's review
date: 2026-11-25
---

# Feature clip: okf-frontmatter

**This is the live storyboard, draft for review.** Edit any row marked *(on screen)*: the text is
the clip's exact text (`**bold**` takes the orange accent). Rows marked *(filmed)* describe the
footage of the take: changing them means a new take. Once approved, this file becomes
`docs/demo-video/clips/okf-frontmatter/clip.md` and the clip is rendered from it.

The clip is one continuous shot: a click on the `status` value, a new value typed and saved, then a
zoom on the frontmatter table and the page body. It shows two texts in turn. The times below are
the Griller's proposal; the batch's trial take sets the real ones and adds the pictures. Its
sibling `okf-schema-bundle-frontmatter` films the same page in a schema bundle, with the same
gesture, marks and caption voice.

## Clip

| Field | Content |
| --- | --- |
| Length | 11.5 s |
| Size *(on screen)* | 1280x720 16:9 |
| Frame rate *(on screen)* | 15 fps |
| Outputs | silent, loops; MP4 (X, release), WebM (docs site), GIF 960 px (release notes, docs page) |
| Cards | none |
| Logo | top right |
| Setting filmed | none (edit mode is the scenario's `checks.editMode: "on"`) |
| Filmed on | to be filmed by the batch |
| Stage | `stage/release-note.md` (Studio, the whole window, edit mode): standard frontmatter (`title`, `description`, `status: draft`, `date`, `tags`), no `type`, no `_schema/` folder; a heading, a "Status:" line with `= this.status`, one sentence |

Off camera (`setup`): the toolbar expanded, edit mode on, the pointer parked away from the table.
Frame 0 shows the Names and Values table (keys in source order, `tags` as two dash items) and the
body line "Status: draft".

## 1. Click the value, type, save

Pictures: from the batch's trial take.

| Field | Content |
| --- | --- |
| Time | 0 to 6.2 s (click on the `status` value at 1.0 s: the text box opens; its text selected at 1.8 s; `published` typed from 2.2 s; save at 4.6 s; table and body updated by about 5.4 s) |
| Shot *(filmed)* | Studio in edit mode on `release-note.md`. The pointer clicks the `draft` value of the `status` row: a text box opens in the cell with `draft`. The text is selected and `published` typed over it. Save chord: the box closes, the row reads `published` and the body line reads "Status: published". |
| Text 1 *(on screen)* | Click a frontmatter value to **edit** it in place |
| Badge save *(on screen)* | Ctrl+Enter / ⌘Enter |

## 2. Zoom on the table and the page

Pictures: from the batch's trial take.

| Field | Content |
| --- | --- |
| Time | 6.2 to 11.5 s (zoom from 6.5 s, held to 10.5 s, then back to the start for the loop) |
| Shot *(filmed)* | Zoom (at most 2x) on the frontmatter table and the "Status:" line under the heading: the two columns Names and Values, the five fields, `status` reading `published` in the table and in the page. |
| Zoom | table, hold to 10.5 s |
| Mark 1 *(on screen)* | Orange outline around the `status` row, 7.0 to 8.7 s |
| Mark 2 *(on screen)* | Orange outline around the "Status: published" line, 8.7 to 10.4 s |
| Text 2 *(on screen)* | The table and the page show the **new value** |

Expected result, the scenario's check: `release-note.md` on disk (auto-save is on) is
`stage/release-note.md` with the one line `status: draft` changed to `status: published`, every
other byte the same. In the preview, the `status` row's value reads `published` and the body's
inline value reads `published`.

## Review notes

- Behaviour relied on (origin/main): with no string `type` and no `_schema/` folder, Studio shows
  the generic table, columns Names and Values, keys in source order, no type icons, no Description
  column, no badge (SwRS FMSCHEMA-005, FMSCHEMA-006; `src/core/frontmatter/okfFrontmatter.ts`). A
  click on a value cell in edit mode opens its editor (FMEDIT-001); a string value without a schema
  opens a YAML text box where Enter adds a line and Ctrl/Cmd+Enter saves (FMEDIT-004;
  `src/page/features/frontmatterValueEditor.ts`). Inline code `= this.status` shows the field in the
  body (writing skill `references/examples.md`, `src/core/render/mystRenderer.ts`).
- The fields are the standard set the writing skill names (`title`, `description`, `status`,
  `date`) plus a `tags` list, to show a list as dash items.
- The old text is selected with `t.selectText` (or Ctrl+A in the box) and the new one typed with
  `t.page.keyboard.type`; only the save chord is a logged press, hence the one badge.
- Without a schema a number, boolean or null value is not editable: the clip edits a string on
  purpose. The sibling clip shows the typed controls a schema brings.
- The status text "Saving frontmatter…" then "Saved. Refreshing preview…" may flash in the status
  line; the trial take shows whether it sits in the zoom.
