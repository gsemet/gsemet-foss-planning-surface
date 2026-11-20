import sys
sys.path.insert(0, sys.argv[1])
from merge import *


def cut_scenario(t, heading):
    h = "### Scenario " + heading
    i = t.index(h)
    j = t.find("\n### ", i + 5)
    return t[i:j + 1], t[:i] + t[j + 1:]


# ---- REVIEW-086: normative text covers Delete
p = swrs_path("REVIEW-086")
t = read(p)
body, tail = split_links(t)
body = set_head(body, desc="When a reader presses Resolve or Reopen in a thread popover, or presses Delete and confirms it in the popover, the extension SHALL send the new flag or the delete to the host, wait for its answer, change the highlight or remove the thread only when the thread is posted again, and run one such action at a time.")
write(p, body + tail)

# ---- REVIEW-094 / REVIEW-119: move two scenarios
p119 = swrs_path("REVIEW-119")
t119 = read(p119)
b119, tail119 = split_links(t119)
typing, b119 = cut_scenario(b119, "(refusal): Typing writes nothing")
clean, b119 = cut_scenario(b119, "(boundary): Change of a clean document")
# the notes of 119 lose the parts that belong to the moved scenarios
for a, b in [
    ("; no write while typing and the page follows", ""),
    ("; `a document without unsaved changes that changes drops the followed lines, a dirty one shifts them` (change of a clean document)", ""),
    ("; `an undo or a redo shifts the followed lines and marks every thread to be checked again` (undo and redo)", ""),
    ("; `an unrelated undo keeps a short-quote thread on its followed line, far beyond the search window` (undo and redo: the check starts from the lines followed in memory)", ""),
    ("; `a clean document that changes is checked again even when the comments file did not change` (change of a clean document, same comments file text)", ""),
    ("view is set to undefined when the changed document is not dirty; after an undo or a redo flagged dirty, the view has recheck true and its thread line is shifted (4 to 5), and the short-quote thread followed in memory to line 73 is posted on line 73 with orphaned false after an unrelated undo; ", ""),
]:
    assert a in b119, a
    b119 = b119.replace(a, b, 1)
write(p119, b119 + tail119)

p094 = swrs_path("REVIEW-094")
t094 = read(p094)
b094, tail094 = split_links(t094)
old_desc = fm_get(b094, "description")
b094 = set_head(b094,
                title="Edits move the stored lines of a thread in memory and write nothing to its file",
                desc=old_desc.rstrip(".") + "; the edit writes nothing to the comments file, and a change of a document without unsaved changes drops the lines followed in memory so that every thread is checked again against the new text.")
k = b094.index("\n### Verification notes\n") + 1
b094 = b094[:k] + typing.rstrip("\n") + "\n\n" + clean.rstrip("\n") + "\n\n" + b094[k:]
b094 = b094.rstrip("\n") + "\n" + """- Method: test/integration/commentAnchors.test.ts (no write while typing and the page follows: Typing writes nothing).
- Method: test/session/reviewReqComments.requirements.test.ts: `a document without unsaved changes that changes drops the followed lines, a dirty one shifts them` and `an undo or a redo shifts the followed lines and marks every thread to be checked again` (Change of a clean document, the undo and redo rows), `an unrelated undo keeps a short-quote thread on its followed line, far beyond the search window` (the check starts from the lines followed in memory), `a clean document that changes is checked again even when the comments file did not change` (the same comments file text).
- Criteria: The comments file text is identical before and after the edits; the view is set to undefined when the changed document is not dirty; after an undo or a redo flagged dirty, the view has recheck true and its thread line is shifted (4 to 5), and the short-quote thread followed in memory to line 73 is posted on line 73 with orphaned false after an unrelated undo.

"""
write(p094, b094 + tail094)
set_list("REVIEW-094", "relates_to", add=[], swrs=True) if False else None
