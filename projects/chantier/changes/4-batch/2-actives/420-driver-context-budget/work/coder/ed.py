def load(p):
    return open(p,encoding='utf-8',newline='').read().replace('\r\n','\n')
class Doc:
    def __init__(s,p): s.p=p; s.t=load(p)
    def rep(s,a,b):
        assert s.t.count(a)==1,(s.t.count(a),a[:80])
        s.t=s.t.replace(a,b)
    def save(s): open(s.p,'w',encoding='utf-8',newline='').write(s.t.replace('\n','\r\n'))
