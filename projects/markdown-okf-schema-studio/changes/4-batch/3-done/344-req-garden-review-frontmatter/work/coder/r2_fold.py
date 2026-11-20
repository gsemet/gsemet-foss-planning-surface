import sys
sys.path.insert(0, sys.argv[1])
from merge import *
R = "REVIEW-"
merge(R + "044", R + "081",
      title="A comment editor sends its text on Save or Cmd+Enter and keeps it until the host accepts it",
      desc="When a reader writes a comment in the comment box or a reply in the reply box of a thread popover, the page SHALL send the typed text to the host only on Save or Reply, Cmd+Enter or Ctrl+Enter with a text that is not blank, and keep the box and its text until the host answers that the text is saved.",
      rename={
        "### Scenario (nominal): The popover of a preview ends with the reply box": "### Scenario (nominal): Reply box: the popover of a preview ends with the reply box",
        "### Scenario (refusal): No reply box without a reply hook": "### Scenario (refusal): Reply box: none without a reply hook",
        "### Scenario (nominal): Reply sends the thread id and the trimmed text": "### Scenario (nominal): Reply box: Reply sends the thread id and the trimmed text",
        "### Scenario (nominal): Keys typed in the reply box stay in the box": "### Scenario (nominal): Reply box: keys typed in the box stay in the box",
        "### Scenario (boundary): Length of the reply": "### Scenario (boundary): Reply box: length of the reply",
        "### Scenario (nominal): A reply accepted by the host empties the box": "### Scenario (nominal): Reply box: a reply accepted by the host empties the box",
        "### Scenario (refusal): A reply the host does not accept keeps its text": "### Scenario (refusal): Reply box: a reply the host does not accept keeps its text",
      })
refs_fix({"REVIEW-081": "REVIEW-044"})
