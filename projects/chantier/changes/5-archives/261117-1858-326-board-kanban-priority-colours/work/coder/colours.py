import colorsys,sys
def rgb(h): h=h.lstrip('#'); return tuple(int(h[i:i+2],16)/255 for i in (0,2,4))
def hue(h):
    r,g,b=rgb(h); return colorsys.rgb_to_hls(r,g,b)[0]*360
def lum(h):
    f=lambda c: c/12.92 if c<=0.03928 else ((c+0.055)/1.055)**2.4
    r,g,b=[f(c) for c in rgb(h)]; return .2126*r+.7152*g+.0722*b
def cr(a,b):
    x,y=lum(a),lum(b); x,y=max(x,y),min(x,y); return (x+.05)/(y+.05)
def mix(a,b,t):
    A,B=rgb(a),rgb(b); return '#%02x%02x%02x'%tuple(round((A[i]*(1-t)+B[i]*t)*255) for i in range(3))
S={'blocked':'#d14b5e','working':'#4a76d9','ready':'#2f9e6b','draft':'#a77b4f','local':'#8b6bd8','waits':'#d08a1f','merged':'#2a7a55'}
def gap(h):
    best=min(S,key=lambda k:min(abs(hue(S[k])-h),360-abs(hue(S[k])-h)))
    d=min(abs(hue(S[best])-h),360-abs(hue(S[best])-h)); return best,round(d,1)
if __name__=='__main__':
    for k,v in S.items(): print(k,v,round(hue(v),1))
    for c in sys.argv[1:]:
        print(c,round(hue(c),1),gap(hue(c)))
