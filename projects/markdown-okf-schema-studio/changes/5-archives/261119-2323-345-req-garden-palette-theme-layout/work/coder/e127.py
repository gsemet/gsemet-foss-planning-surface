import sys
sys.path.insert(0,r"C:/Users/gaeta/Projets/gsemet-foss-planning-surface/projects/markdown-okf-schema-studio/changes/4-batch/2-actives/345-req-garden-palette-theme-layout/work/coder")
from fm import *
def edit(id,pairs):
    b=getbody(id)
    for a,c in pairs:
        assert b.count(a)==1,(id,a[:50])
        b=b.replace(a,c)
    setbody(id,b)
i=full("PALETTE-127")
edit(i,[
("""### Related requirements

- SwRS-MDOKFSTUDIO-PALETTE-130: the Custom entry writes a titled admonition with a class.
- SwRS-MDOKFSTUDIO-PALETTE-137: Dropdown writes a note admonition with the dropdown class.
""","""### Scenario (nominal): Custom writes a titled admonition with a class

- GIVEN the selected text Body
- WHEN Custom is chosen
- THEN the text is `:::{admonition} Title` with the option `:class: note` and Body, and Title is selected

- GIVEN the caret after Intro
- WHEN Custom is chosen
- THEN a new titled fence follows Intro, set apart by a blank line, with Title selected

| Input | Outcome |
| --- | --- |
| Custom chosen | The option line `:class: note` is followed by a blank line |

### Scenario (nominal): Dropdown writes a note admonition with the dropdown class

- GIVEN the caret after intro
- WHEN Dropdown is pressed
- THEN a note admonition with the title Title and the option `:class: dropdown` and the content Content follows intro after a blank line, with Title selected; with a selection the touched lines are wrapped instead of the sample

- GIVEN a selection that is a tip fence of three colons
- WHEN Dropdown is pressed
- THEN the outer fence has four colons, as in the scenario of the colon count

### Related requirements

"""),
("- Criteria: The option values","""- Method: test/page/modules/editActions.test.ts (unit tests "custom admonition writes a titled block with a class and selects the title": Custom wrap, empty and option line; "dropdown inserts a note with :class: dropdown or wraps the touched lines": Dropdown sample and nested fence)
- Criteria: The option values"""),
])
i=full("PALETTE-238")
edit(i,[
("(see SwRS-MDOKFSTUDIO-PALETTE-268)","(see the scenario of the admonition entries below)"),
("""### Scenario (boundary): The Key commands in MyST mode""","""### Scenario (nominal): MyST admonitions are listed with their icons

- GIVEN the MyST mode and an empty text box
- WHEN / is typed
- THEN the list holds an entry "<kind> admonition" for note, tip, hint, important, warning, caution, attention, danger, error, seealso, versionadded, versionchanged and deprecated, and "Custom admonition", each with the icon of its preview callout badge

| Kind | Icon (as the preview callout badge) |
| --- | --- |
| note | information circle |
| tip, hint, versionadded | light bulb |
| important | star |
| warning, attention, versionchanged | triangle |
| caution | octagon |
| danger, error, deprecated | circle with a cross |
| seealso | circle with an arrow |
| Custom admonition | the Admonition icon |

- GIVEN the MyST mode and an empty text box
- WHEN /versionadded is typed and Enter is pressed
- THEN the text box holds the block `:::{versionadded} 1.0`, an empty line and `:::`, with 1.0 selected, in one undo step; versionchanged and deprecated write the same block with their name

- GIVEN the GFM mode, or the Admonition type popover of the MyST mode
- WHEN the slash menu or the popover is opened
- THEN the GFM menu lists no admonition entry, and the popover keeps offering only the ten simple types and Custom (the version admonitions are not options of the popover, see SwRS-MDOKFSTUDIO-PALETTE-127)

### Scenario (boundary): The Key commands in MyST mode"""),
("- Method: test/page/modules/editPalette.test.ts, unit test \"CR038","""- Method: test/page/modules/slashMenu.test.ts, unit tests "P11: the MyST slash menu lists every admonition directive, each with its own icon" and "P11: /versionadded inserts a valid version admonition with the version selected"; visual scenarios palette-slash/v34-slash-myst-admonitions-light-900 and palette-slash/v35-slash-myst-admonitions-dark-900 (the menu scrolled to its last entries, with the icons). The block renders as an admonition titled with the version (see SwRS-MDOKFSTUDIO-MYST-001).
- Method: test/page/modules/editPalette.test.ts, unit test "CR038"""),
])
