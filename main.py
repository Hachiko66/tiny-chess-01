import json,os,sys,urllib.request as r
E=os.environ.get("MAKEFUN_ENV_URL")
F="abcdefgh";C="pnbrqk";V=[100,320,330,500,900]
def nb():
 b=[-1]*128
 for i in range(8):b[i]=i+6;b[16+i]=i;b[96+i]=i+6
 b[112:120]=[15,13,14,16,17,14,13,15]
 return b,0
def lf(fen):
 b=[-1]*128
 p=fen.split()
 x=p[0].split("/")
 for i in range(8):
  q=(7-i)*16
  for c in x[i]:
   if c>="1"and c<="9":q+=ord(c)-48
   else:b[q]=C.find(c.lower())+(0 if c<"a" else 6);q+=1
 sd=0 if p[1]=="w" else 1
 return b,sd
def at(b,sq,by):
 p=by*6
 for d in (15,17):
  t=sq+d if by==0 else sq-d
  if t&0x88==0 and b[t]==p:return 1
 for d in (31,33,14,18,-14,-18,-31,-33):
  t=sq+d
  if t&0x88==0 and b[t]==p+1:return 1
 for d in (1,-1,16,-16):
  t=sq+d
  while t&0x88==0:
   z=b[t]
   if z!=-1:
    if z==p+3 or z==p+4:return 1
    break
   t+=d
 for d in (15,17,-15,-17):
  t=sq+d
  while t&0x88==0:
   z=b[t]
   if z!=-1:
    if z==p+2 or z==p+4:return 1
    break
   t+=d
 for d in (1,-1,16,-16,15,17,-15,-17):
  t=sq+d
  if t&0x88==0 and b[t]==p+5:return 1
 return 0
def gen(b,sd):
 M=[];p=sd*6;o=p+6
 for q in range(128):
  c=b[q]
  if c<0 or c<p or c>p+5:continue
  t=c-p
  if t==0:
   d=16 if sd==0 else -16
   t2=q+d
   if t2&0x88==0 and b[t2]==-1:
    if (sd==0 and q>=112) or (sd==1 and q<16):
     for z in (1,2,3,4):M.append((q,t2,z))
    else:M.append((q,t2,0))
    if (sd==0 and 16<=q<24) or (sd==1 and 96<=q<104):
     t2=q+d+d
     if t2&0x88==0 and b[t2]==-1:M.append((q,t2,0))
   for d in (15,17):
    t2=q+d if sd==0 else q-d
    if t2&0x88==0 and b[t2]!=-1 and b[t2]>=o:M.append((q,t2,0))
  elif t==1:
   for d in (31,33,14,18,-14,-18,-31,-33):
    t2=q+d
    if t2&0x88==0 and (b[t2]==-1 or b[t2]>=o):M.append((q,t2,0))
  elif t<4:
   D=[15,17,-15,-17] if t==2 else [1,-1,16,-16]
   if t==4:D=[1,-1,16,-16,15,17,-15,-17]
   for d in D:
    t2=q+d
    while t2&0x88==0:
     if b[t2]==-1:M.append((q,t2,0))
     elif b[t2]>=o:M.append((q,t2,0));break
     else:break
     t2+=d
  else:
   for d in (1,-1,16,-16,15,17,-15,-17):
    t2=q+d
    if t2&0x88==0 and (b[t2]==-1 or b[t2]>=o):M.append((q,t2,0))
 return M
def ev(b):
 r=0
 for i in range(128):
  c=b[i]
  if c<0 or c==5 or c==11:continue
  r+=V[c] if c<6 else -V[c-6]
 return r
def S(b,sd,d,a,be,nl):
 nl[0]+=1
 if nl[0]>5e5:return ev(b) if sd==0 else -ev(b)
 if d<=0:
  st=ev(b) if sd==0 else -ev(b)
  if st>=be:return be
  if st>a:a=st
  ms=[m for m in gen(b,sd) if b[m[1]]!=-1]
  ms.sort(key=lambda m:-(V[b[m[1]]-6] if b[m[1]]>=6 else 0)+V[b[m[0]]%6])
  for m in ms:
   nb=b[:];nb[m[1]]=nb[m[0]];nb[m[0]]=-1
   k=next(i for i in range(128) if nb[i]==5+sd*6)
   if at(nb,k,1-sd):continue
   sc=-S(nb,1-sd,-be,-a,1-sd,nl)
   if sc>a:a=sc
   if a>=be:break
  return a
 ms=gen(b,sd);ms.sort(key=lambda m:-(V[b[m[1]]-6] if b[m[1]]>=6 else 0)+V[b[m[0]]%6])
 best=-999999
 for m in ms:
  nb=b[:];nb[m[1]]=nb[m[0]];nb[m[0]]=-1
  k=next(i for i in range(128) if nb[i]==5+sd*6)
  if at(nb,k,1-sd):continue
  sc=-S(nb,1-sd,d-1,-be,-a,1-sd,nl)
  if sc>best:best=sc
  if sc>a:a=sc
  if a>=be:break
 return best
def T(b,sd):
 ba=-999999;bm=None
 for d in range(1,5):
  nl=[0];ms=gen(b,sd)
  if not ms:return None
  ms.sort(key=lambda m:-(V[b[m[1]]-6] if b[m[1]]>=6 else 0)+V[b[m[0]]%6])
  for m in ms:
   nb=b[:];nb[m[1]]=nb[m[0]];nb[m[0]]=-1
   k=next(i for i in range(128) if nb[i]==5+sd*6)
   if at(nb,k,1-sd):continue
   sc=-S(nb,1-sd,d-1,-999999,999999,1-sd,nl)
   if sc>ba:ba=sc;bm=m
  if nl[0]>5e5:break
 return bm
def p(P,b):
 req=r.Request(E+P,data=json.dumps(b).encode(),headers={"content-type":"application/json"})
 try:
  with r.urlopen(req) as x:return json.load(x)
 except r.HTTPError as e:sys.exit(f"{P}:{e.code}")
b,sd=nb()
while True:
 g=p("/game",{})
 if g.get("status")=="done":break
 b,sd=lf(g["fen"])
 while g.get("status")=="your_move":
  m=T(b,sd)
  if m is None:p("/resign",{"game":g["game"]});break
  nb=b[:];nb[m[1]]=nb[m[0]];nb[m[0]]=-1
  if m[2]:nb[m[1]]=m[2]+6*sd
  b=nb;sd=1-sd
  u=F[m[0]&7]+str(8-(m[0]>>4))+F[m[1]&7]+str(8-(m[1]>>4))+(C[m[2]] if m[2] else "")
  g=p("/move",{"game":g["game"],"move":u})
  b,sd=lf(g["fen"])