import sys
B = r"C:/Users/gaeta/Projets/gsemet-foss-planning-surface/projects/markdown-okf-schema-studio/changes/4-batch/2-actives/345-req-garden-palette-theme-layout/work/coder"
sys.path.insert(0, B)
from fm import *

# ---- PALETTE-021: the autosave scroll row goes to PALETTE-279
sid = full("PALETTE-021")
body = getbody(sid)
lines = body.split("\n")
rows = [l for l in lines if l.startswith("| the text of a paste is applied to the document by the autosave")]
assert len(rows) == 1
i = lines.index(rows[0])
lines[i] = None
body = "\n".join(l for l in lines if l is not None)
old = "| the palette is still above the frame (not stuck) and the caret line is above its bottom | the page does not scroll |\n"
assert old in body
body = body.replace(old, old + "\nThe page does not follow the scroll that an applied edit causes in the text editor: see SwRS-MDOKFSTUDIO-PALETTE-279.\n", 1)
setbody(sid, body)

# ---- PALETTE-002: the rule icon goes to PALETTE-280
sid = full("PALETTE-002")
body = getbody(sid)
reps = [
    ("## Every edit bar button shows the slide-in tooltip and the rule button a dashes icon",
     "## Every edit bar button shows the slide-in tooltip"),
    (", so that hovering or focusing the button shows the same sliding tooltip bubble as the floating toolbar, and SHALL draw the Horizontal rule button as three dashes.",
     ", so that hovering or focusing the button shows the same sliding tooltip bubble as the floating toolbar."),
    ("### Scenario (boundary): Shortcut and rule icon", "### Scenario (boundary): Shortcut in the tooltip"),
    ("(for example \"Bold (Ctrl+B)\"), the title stays for the accessible hint, and the Horizontal rule icon is three separate dashes on one line, not the lines of centred text",
     "(for example \"Bold (Ctrl+B)\") and the title stays for the accessible hint"),
    ("(T21b: every palette button carries a data-tooltip equal to its title; the rule icon is dashes)",
     "(T21b: every palette button carries a data-tooltip equal to its title)"),
    ("visual scenarios palette-slash/v23-edit-bar-tooltip-rule-cream-900 and v24-edit-bar-tooltip-rule-dark-900 (hovered rule button shows its bubble)",
     "visual scenarios palette-slash/v23-edit-bar-tooltip-rule-cream-900 and v24-edit-bar-tooltip-rule-dark-900 (hovered button shows its bubble)"),
    ("; the rule icon path has no segment other than three short horizontal dashes.", "."),
]
for o, n in reps:
    assert o in body, o[:40]
    body = body.replace(o, n)
setbody(sid, body)
setfield(sid, "title", "Every edit bar button shows the slide-in tooltip")
setfield(sid, "description",
         "While a block editor is open, the extension SHALL give every button of its edit bar the data-tooltip attribute with the text of its title, so that hovering or focusing the button shows the same sliding tooltip bubble as the floating toolbar.")
