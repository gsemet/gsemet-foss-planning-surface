def sub(path, pairs):
    raw=open(path,encoding='utf-8',newline='').read()
    crlf='\r\n' in raw
    s=raw.replace('\r\n','\n')
    for a,b in pairs:
        assert a in s,(path,a)
        s=s.replace(a,b)
    if crlf: s=s.replace('\n','\r\n')
    open(path,'w',encoding='utf-8',newline='').write(s)
