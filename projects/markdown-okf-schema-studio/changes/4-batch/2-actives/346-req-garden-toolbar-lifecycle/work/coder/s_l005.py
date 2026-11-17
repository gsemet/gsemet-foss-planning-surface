from st import *
A="StRS-MDOKFSTUDIO-LIFE-005"
t=rd(A)
old=("- When another tool, a file change on disk or an undo changes the previewed document, the changed blocks glow once, so the reader notices what an agent, another extension or an undo changed.\n"
"- Typing in the text editor and the preview's own edits never glow; a change spread over too many places glows nowhere, and nothing glows when the system asks for reduced motion.\n")
new=("- When another tool, a file change on disk or an undo changes the previewed document, the changed blocks glow once so that the reader notices what changed; typing in the text editor, the preview's own edits, a change spread over too many places and a system that asks for reduced motion never make a block glow.\n")
assert old in t; wr(A,t.replace(old,new))
A="StRS-MDOKFSTUDIO-LIFE-007"
t=rd(A)
old="""   - Option SwRS-MDOKFSTUDIO-LIFE-049 (refusal): a pending notice that is oversized or malformed is ignored
2. The status reads Preview ready
   - Option SwRS-MDOKFSTUDIO-LIFE-049 (refusal): a failed render is labelled in the status
"""
new="""   - Option SwRS-MDOKFSTUDIO-LIFE-049 (refusal): a pending notice that is oversized or malformed is ignored
   - Option SwRS-MDOKFSTUDIO-LIFE-049 (refusal): a failed render is labelled in the status
2. The status reads Preview ready
"""
assert old in t; wr(A,t.replace(old,new))
