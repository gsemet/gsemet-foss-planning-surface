import sys
sys.path.insert(0,r"C:/Users/gaeta/Projets/gsemet-foss-planning-surface/projects/markdown-okf-schema-studio/changes/4-batch/2-actives/345-req-garden-palette-theme-layout/work/coder")
from fm import *
import re
def sub(id,pairs):
    p,t,fm=load(id)
    for a,c in pairs:
        assert t.count(a)==1,(id,a[:60])
        t=t.replace(a,c)
    open(p,"w",encoding="utf-8",newline="\n").write(t)
sub(full("PALETTE-275"),[
("title: Every rendered syntax has a slash menu entry or a documented exception","title: Every syntax the preview renders can be inserted from the slash menu"),
("""description: The extension SHALL list in the slash menu of the palette mode that
  offers it every syntax the writing skill documents as rendered, except the
  syntaxes of a documented exception list that have another way in.""","""description: The extension SHALL let the writer insert from the slash menu every
  syntax the preview renders, in the palette mode that offers it, except the
  documented exceptions that have another way in."""),
("## Every rendered syntax has a slash menu entry or a documented exception","## Every syntax the preview renders can be inserted from the slash menu"),
("""The extension SHALL list in the slash menu of the palette mode that offers it every syntax the writing skill documents as rendered, except the syntaxes of a documented exception list that have another way in.""","""The extension SHALL let the writer insert from the slash menu every syntax the preview renders, in the palette mode that offers it, except the documented exceptions that have another way in."""),
])
sub(full("THEME-034"),[
('title: "Page colours go through one token map of VS Code variables"','title: "A host colour that is set is used, an unset one keeps the fallback"'),
("""description: "When the stylesheet is built, the extension SHALL declare each neutral
  --studio- token on the root and on body as the VS Code variable of the same name,
  so that the --vscode- prefix appears only inside that token map and every --studio-
  token the stylesheet or the Mermaid theme reads is in it.\"""","""description: "When the host sets a colour the page uses, the extension SHALL paint
  the page with that colour, and when the host does not set it, the page SHALL keep
  the fallback colour written in its rule; the --vscode- variables are read through
  one token map and every token the page reads is in it.\""""),
("## Page colours go through one token map of VS Code variables","## A host colour that is set is used, an unset one keeps the fallback"),
("""When the stylesheet is built, the extension SHALL declare each neutral --studio- token on the root and on body as the VS Code variable of the same name, so that the --vscode- prefix appears only inside that token map and every --studio- token the stylesheet or the Mermaid theme reads is in it.""","""When the host sets a colour the page uses, the extension SHALL paint the page with that colour, and when the host does not set it, the page SHALL keep the fallback colour written in its rule. The page reads the host variables through one token map: each neutral --studio- token is declared on the root and on body as the VS Code variable of the same name, the --vscode- prefix appears only inside that map, and every --studio- token the stylesheet or the Mermaid theme reads is in it."""),
])
