def rd(f): return open(f,encoding='utf-8',newline='').read()
def wr(f,t): open(f,'w',encoding='utf-8',newline='').write(t)
def ins(t,text,head="### Related requirements"):
    i=t.index(head); return t[:i]+text+t[i:]
def edit(f,fn):
    t=rd(f); nl='\r\n' if '\r\n' in t else '\n'
    t=fn(t.replace('\r\n','\n')); wr(f,t.replace('\n',nl))
OLDREL="- SwRS-MDOKFSTUDIO-LIFE-097: the settings that decide how the panes follow each other\n"
NEWREL="- SwRS-MDOKFSTUDIO-LIFE-071: a change of the scroll settings replaces the page document\n"
def f100(t):
    t=ins(t,"""### Scenario (boundary): Defaults and the setting off

| Input | Outcome |
| --- | --- |
| No stored value for markdownOkfSchemaStudio.preview.scrollPreviewWithEditor, settings and page boot context read | The setting is true (on by default); a boot entry that is absent or not false reads as on |
| scrollPreviewWithEditor set to false and the writer scrolls the text editor | The preview stays where it is; the Anchor button overrides the setting for one panel |

""")
    t=t.replace(OLDREL,NEWREL)
    t=t.replace("- Criteria:","- Method: test/core/configuration/settingsRegistry.test.ts (Defaults): \"the page reads missing or odd boot entries with the page defaults\"; test/page/pageSettings.test.ts: \"page settings default to following both ways, without selection marks or double-click reveal\".\n- Criteria: readPreviewConfiguration returns true for no value of scrollPreviewWithEditor;",1)
    if 'StRS-MDOKFSTUDIO-LIFE-021' not in t.split('---')[1]:
        t=t.replace("- StRS-MDOKFSTUDIO-LIFE-005\n","- StRS-MDOKFSTUDIO-LIFE-005\n- StRS-MDOKFSTUDIO-LIFE-021\n",1)
    return t
def f108(t):
    t=ins(t,"""### Scenario (boundary): Defaults, the setting off and the double click

| Input | Outcome |
| --- | --- |
| No stored value for markdownOkfSchemaStudio.preview.scrollEditorWithPreview, preview settings read | The setting is true (on by default) |
| scrollEditorWithPreview set to false and the reader scrolls or clicks in the preview | The editor does not move |
| The reader double-clicks rendered content outside edit mode | The page posts nothing beyond the reveals of its two clicks; there is no double-click setting (a doubleClickToSwitchToEditor value left in the user settings is not a setting of the extension and has no effect) |

""")
    t=t.replace(" (see SwRS-MDOKFSTUDIO-LIFE-097 for the settings)","")
    t=t.replace(OLDREL,NEWREL)
    t=t.replace("- Criteria:","- Method: test/page/pageSettings.test.ts (Defaults): \"page settings default to following both ways, without selection marks or double-click reveal\"; test/page/runtimeScroll.test.ts (the double click): \"executes source and preview synchronization across layout changes\" (a dblclick posts nothing more). The click path with scrollEditorWithPreview off has no test (untested); checked by reading revealFromPage and revealEditorLine.\n- Criteria: readPreviewConfiguration returns true for no value of scrollEditorWithPreview; revealEditorLine returns before any reveal when scrollEditorWithPreview is false; the page registers no double-click listener;",1)
    if 'StRS-MDOKFSTUDIO-LIFE-021' not in t.split('---')[1]:
        t=t.replace("- StRS-MDOKFSTUDIO-LIFE-010\n","- StRS-MDOKFSTUDIO-LIFE-010\n- StRS-MDOKFSTUDIO-LIFE-021\n",1)
    return t
d='requirements/tiers/swrs/lifecycle-sync/SwRS-MDOKFSTUDIO-LIFE-'
edit(d+'100.md',f100); edit(d+'108.md',f108)
