"""Round 4: update the verification notes of the toolbar SwRS whose scenarios are now tested."""

import pathlib
import sys

BASE = pathlib.Path(sys.argv[1]) / "requirements/tiers/swrs/toolbar-navigation"

EDITS = {
    "001": [
        ("compares the title and tooltip pair of the Refresh, Anchor and Edit buttons and the start of the Theme button, equality for all 16 buttons is not asserted;",
         "compares the title and tooltip pair of the Refresh, Anchor and Edit buttons and the start of the Theme button;"),
        ("Scrolling: position fixed and z-index 1100 of the toolbar; the 12 px and 14 px offsets and the covering of scrolled text are untested).",
         "Scrolling: position fixed and z-index 1100 of the toolbar).\n"
         "- Method: test/core/preview/toolbarReq.requirements.test.ts (Every button has a tooltip: each of the 16 buttons has data-tooltip equal to its title, also where the aria-label differs; Tooltip on keyboard focus: one rule shows the bubble for hover and focus-visible, and no focus rule has colours of its own; Scrolling: the toolbar rule is position fixed, 12 px from the top, 14 px from the end, z-index 1100)."),
        ("the keyboard case follows from the shared CSS rule and is not measured).",
         "the keyboard case follows from the shared CSS rule).\n"
         "- Method: test/visual/capture_toolbar_checks.py, check_toolbar_place_and_focus on toolbar-navigation/v06 to v21 (Every button has a tooltip: data-tooltip equals title on the 16 live buttons; Tooltip on keyboard focus: Shift+Tab from Edit reaches Refresh with focus-visible, and its bubble shows \"Refresh preview\" visible at opacity 1 in the colours of the hover bubble; Scrolling: the toolbar box is 12 px from the top and 14 px from the end of the pane at the top and after a scroll, and at a 360 px width a line of text scrolled under the toolbar is under its box for the pointer, the toolbar on top)."),
    ],
    "030": [
        ("Scroll to the end is not measured separately).",
         "Scroll to the end through check_scroll_at_end in test/visual/capture_toolbar_checks.py on the same scenario: at the end, 20 wheel steps down leave the page at the end and the band makes no scrollTo call)."),
    ],
    "054": [
        ("the render gate of previewHistoryGo (pageMessages.ts) is untested.",
         "test/session/toolbarReq.requirements.test.ts (A history state of another render: a previewHistoryGo that names another document, revision or request is refused by the render gate, posts nothing and leaves the history where it is; the current render's move goes back)."),
        ("(a previewHistoryState of another document version is ignored; the other document and request rows are by code only)",
         "(a previewHistoryState of another document version is ignored)"),
    ],
    "090": [
        ("the exact scheme and absolute reason texts are not asserted, and the malformed escape case is untested.",
         "the exact scheme and absolute reason texts are not asserted; a link with a malformed escape (a%zz.md, a cut UTF-8 sequence) is blocked with the undecodable reason, like %5Csecret and %00.md."),
    ],
    "094": [
        ("../secret.md blocked; the second-root relative case is untested, the wikilink test searches every root)",
         "../secret.md blocked; a relative link that resolves below the second folder of the workspace opens, and is blocked when that folder is not a root; the wikilink test searches every root)"),
    ],
    "120": [
        ("- Method: the initial state is untested (markup of the toolbar)\n",
         "- Method: test/core/preview/toolbarReq.requirements.test.ts (Initial state: the Anchor button of the markup is in the off mode, aria-pressed false, with the off title, and not disabled)\n"),
        ("the own-document case is T38 an unpaired preview disables the anchor button and a previewPairing message re-enables it; the other version and request rows are by code only)",
         "the own-document case is T38 an unpaired preview disables the anchor button and a previewPairing message re-enables it)\n"
         "- Method: test/page/toolbarReq.runtime.requirements.test.ts (Foreign document and Own document: a pairing of another document, revision or request leaves the button as it is, both ways; a pairing of the page's own render disables it with the off title, then enables it again)"),
    ],
    "006": [
        ("### Verification notes\n\n### Verification notes\n", "### Verification notes\n"),
        ("- Boundary: the browser find and the scroll to the target are not driven in a unit test; the real-window run of CR 143 covers a table-of-contents jump.",
         "- Method: test/visual/capture_toolbar_checks.py, check_find_opens_folded_section on toolbar-navigation/v06 to v21 (The browser find opens the section: with every section folded, a text fragment #:~:text= on a phrase of a hidden block runs Chromium's own find-in-page, which fires beforematch; the block loses data-okf-folded and hidden, its heading is open and the block is in view).\n"
         "- Boundary: Playwright cannot type into the browser's find bar (Cmd/Ctrl+F) and window.find() fires no beforematch, so the text fragment stands for it; the fixture has one section, so which sections stay folded is the unit test's; the real-window run of CR 143 covers a table-of-contents jump."),
    ],
}

for number, edits in EDITS.items():
    path = BASE / f"SwRS-MDOKFSTUDIO-TOOLBAR-{number}.md"
    text = path.read_bytes().decode("utf-8")
    for before, after in edits:
        assert text.count(before) == 1, f"{number}: not found once: {before[:60]}"
        text = text.replace(before, after)
    path.write_bytes(text.encode("utf-8"))
    print("updated", path.name)
