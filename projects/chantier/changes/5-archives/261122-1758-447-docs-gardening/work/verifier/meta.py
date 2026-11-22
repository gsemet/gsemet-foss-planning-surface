import sys,struct,glob
for f in sorted(glob.glob(sys.argv[1]+'/docs/web-board/*.png')):
    d=open(f,'rb').read(); p=8; out=[]; chunks=[]
    while p<len(d):
        n,=struct.unpack('>I',d[p:p+4]); t=d[p+4:p+8].decode(); b=d[p+8:p+8+n]; p+=12+n
        chunks.append(t)
        if t in('tEXt','zTXt','iTXt','eXIf'): out.append((t,b[:200]))
        if t=='IHDR': w,h=struct.unpack('>II',b[:8])
    extra=[c for c in set(chunks) if c not in('IHDR','IDAT','IEND')]
    print(f.split('/')[-1],w,h,extra,out)
