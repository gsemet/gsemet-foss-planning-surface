import sys,re,glob
root="C:/Users/gaeta/Projets/markdown-okf-schema-studio.worktrees/batch-06-CR-346/requirements/tiers"
for a in sys.argv[1:]:
    p=glob.glob(f"{root}/*/*/*-{a}.md")[0].replace("\\","/")
    t=open(p,encoding='utf-8').read()
    i=t.find('<!-- okf:links:start')
    print("=====",p.split('/tiers/')[1]);print(t[:i] if i>0 else t)
