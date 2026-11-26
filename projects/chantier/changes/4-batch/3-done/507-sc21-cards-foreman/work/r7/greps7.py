import pathlib
card = pathlib.Path(r"C:/Users/gaeta/Projets/chantier.worktrees/batch-31-CR-507/skills/chantier/cards-next/foreman.md").read_text(encoding="utf-8").split("\n")
P = ['local run owed','fast-forward','chantier/','Merge but','rev-parse','Merge but under the release grant: a fix,','foreman set','invent a gap','release grant','stop','Code, review, commit, rebase, push, edit a','reclaim','copy whole','past fact','s event','trashed','a live lease without the user','--epoch','batch','[foreman→chief-of-staff] final <STATUS.md path>','final','status','take stack','take','planning surface','ready <batch>','exit 3','unchanged','s word','take-back','dropped CR','edit a PR','release go','Your only git','Starting Drivers: copy whole the prompt','Obey your chat but for']
for p in P:
    n = [i+1 for i,l in enumerate(card) if p in l]
    print(repr(p), n if n else "MISSING")
