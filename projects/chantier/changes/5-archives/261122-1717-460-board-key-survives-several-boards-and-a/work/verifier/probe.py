import urllib.parse, http.client
K="NYgwxzkrE2XSIN23OHgS88AFPIQ1FrnRSico9S4hYHw"
def get(path, **h):
    c=http.client.HTTPConnection("127.0.0.1",55050); c.request("GET",path,headers=h); r=c.getresponse(); b=r.read().decode()
    return r.status, dict((k.lower(),v) for k,v in r.getheaders()), b
HT={"Accept":"text/html"}
s,h,b=get("/",**HT); print("nokey",s,h.get("content-type"),h.get("content-security-policy"),'<script' in b,'method="get"' in b,'name="k"' in b)
s,h,b=get("/?k=WRONG&p=x",**HT); print("wrong",s,"not this board's" in b, 'name="p"' in b)
s,h,b=get("/",**{"Accept":"text/html","Accept-Language":"fr-FR,fr;q=0.9"}); print("fr",s,"Ce board demande" in b,"Ouvrir" in b)
s,h,b=get("/",**{"Accept":"*/*"}); print("probe-ish",s,b.strip())
s,h,b=get("/api/board",**HT); print("api",s,b.strip())
s,h,b=get("/js/main.js"); print("js",s,b.strip())
link="http://127.0.0.1:55050/?k="+K
s,h,b=get("/?k="+urllib.parse.quote(link,safe=""),**HT); print("pasted link",s,h.get("set-cookie"),h.get("location"))
s,h,b=get("/?k=%20"+K+"%20",**HT); print("blanks",s,h.get("set-cookie","")[:30])
s,h,b=get("/?k=%3Cscript%3E&q=%3Cscript%3E",**HT); print("escape raw script tag in body:", "<script>" in b)
s,h,b=get("/x/y/index.html",**{**HT,"X-Forwarded-Host":"h"}); print("prefix", 'action="./index.html"' in b)
