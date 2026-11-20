import sys,re
f=sys.argv[1]
L=open(f,encoding="utf-8").read().replace("\r\n","\n").split("\n")
for a in sys.argv[2:]:
    lo,hi=map(int,(a.split("-")+[a])[:2]) if "-" in a else (int(a),int(a))
    for i in range(max(0,lo-1),min(len(L),hi)):
        if re.match(r'\s*(test|it|describe)\(',L[i]):
            j=i-1; mk=[]
            while j>=0 and re.match(r'\s*//',L[j]):
                if '_req' in L[j]: mk.append(re.sub(r'.*@(tests|implements)_req (SwRS|StRS)-MDOKFSTUDIO-',lambda m:('S:' if m.group(2)=='StRS' else ''),L[j]))
                j-=1
            print(f"{i+1}: {L[i].strip()[:80]} <- {mk[::-1]}")
