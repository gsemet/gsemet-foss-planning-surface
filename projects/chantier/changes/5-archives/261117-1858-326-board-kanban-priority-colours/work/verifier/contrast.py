import colorsys
def rgb(h): h=h.lstrip('#'); return [int(h[i:i+2],16)/255 for i in (0,2,4)]
def L(h):
    f=lambda c: c/12.92 if c<=0.03928 else ((c+0.055)/1.055)**2.4
    r,g,b=map(f,rgb(h)); return 0.2126*r+0.7152*g+0.0722*b
def cr(a,b):
    x,y=sorted((L(a),L(b)),reverse=True); return (x+.05)/(y+.05)
def hue(h): r,g,b=rgb(h); return colorsys.rgb_to_hls(r,g,b)[0]*360
pairs={'P1':('#ffffff','#1d5c63'),'P2':('#ffffff','#4a7e83'),'P3':('#123d42','#88acb0'),'P4':('#123d42','#cfe2e3'),'nav':('#123d42','#e9f1f1'),
'm0':('#a02e78','#f2e2ec'),'m1':('#1a6c88','#dfeaee'),'m2':('#3a7222','#e3ebe0'),'m3':('#8a3aa8','#efe3f3'),'m4':('#666c12','#eaeade'),'m5':('#1a736d','#dfebeb')}
for k,(a,b) in pairs.items(): print(k,round(cr(a,b),2))
st={'blocked':'#d14b5e','working':'#4a76d9','ready':'#2f9e6b','draft':'#a77b4f','local':'#8b6bd8','waits':'#d08a1f','merged':'#2a7a55'}
for i,m in enumerate(['#a02e78','#1a6c88','#3a7222','#8a3aa8','#666c12','#1a736d']):
    g={n:min(abs(hue(m)-hue(s)),360-abs(hue(m)-hue(s))) for n,s in st.items()}
    n=min(g,key=g.get); print('mark',i,round(hue(m),1),n,round(g[n],1))
