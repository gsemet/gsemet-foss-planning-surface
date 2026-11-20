import re,json,sys
sys.path.insert(0,"C:/Users/gaeta/Projets/gsemet-foss-planning-surface/projects/markdown-okf-schema-studio/changes/4-batch/2-actives/346-req-garden-toolbar-lifecycle/work/coder")
from lib import *

def setfm(a,key,text):
    t=rd(a); fm,body=split_fm(t)
    m=re.search(rf"^{key}:.*\n(?:[ \t]+.*\n)*",fm,re.M)
    assert m,(a,key)
    fm=fm[:m.start()]+f"{key}: "+json.dumps(text,ensure_ascii=False)+"\n"+fm[m.end():]
    wr(a,"---\n"+fm+"---\n"+body)

def getfm(a,key):
    fm,_=split_fm(rd(a))
    m=re.search(rf"^{key}:[ ]*(.*\n(?:[ \t]+.*\n)*)",fm,re.M)
    v=m.group(1)
    v=" ".join(x.strip() for x in v.splitlines())
    if v[:1] in "\"'": v=v[1:-1]
    return v

def section(a,heading,new):
    """replace the content of '### heading' (up to the next '### ' or the links block) by new"""
    t=rd(a)
    i=t.index("### "+heading+"\n")
    j=len(t)
    for h in ("\n### ","\n<!-- okf:links:start -->"):
        k=t.find(h,i+5)
        if k>=0: j=min(j,k+1)
    t=t[:i]+"### "+heading+"\n\n"+new.strip("\n")+"\n\n"+t[j:]
    wr(a,t)

def set_title(a,title):
    t=rd(a)
    old=getfm(a,"title")
    fm,body=split_fm(t)
    m=re.search(r"^title:.*\n(?:[ \t]+.*\n)*",fm,re.M)
    fm=fm[:m.start()]+"title: "+json.dumps(title,ensure_ascii=False)+"\n"+fm[m.end():]
    body=body.replace("## "+old+"\n","## "+title+"\n",1)
    wr(a,"---\n"+fm+"---\n"+body)

def set_need(a,need):
    """user_need in the frontmatter and the Preserved stakeholder intent section"""
    setfm(a,"user_need",need)
    section(a,"Preserved stakeholder intent",need)

def set_description(a,desc):
    setfm(a,"description",desc)
    section(a,"Normative behavior",desc)

def add_diagram(a,diagram,caption=None):
    t=rd(a)
    if "### Use case diagram" in t:
        return
    cap=("\n"+caption+"\n") if caption else ""
    block="### Use case diagram\n\n```mermaid\n"+diagram.strip("\n")+"\n```\n"+cap+"\n"
    i=t.find("### Main paths")
    if i<0: i=t.find("<!-- okf:links:start -->")
    wr(a,t[:i]+block+t[i:])

def set_main_paths(a,text):
    t=rd(a)
    i=t.index("### Main paths")
    j=t.find("<!-- okf:links:start -->",i)
    wr(a,t[:i]+"### Main paths\n\n"+text.strip("\n")+"\n\n"+t[j:])
