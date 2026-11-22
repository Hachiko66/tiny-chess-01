import json,os,sys,urllib.request as r
E=os.environ.get("MAKEFUN_ENV_URL")
F="abcdefgh";C="pnbrqk";V=[100,320,330,500,900]
P=bytes([0]*16+[10,20,30,40,50,40,30,20]*4+[15]*16+[20]*32+[0]*16)
def I():
 b=[-1]*128
 for i in range(8):b[i]=i+6;b[i+16]=i;b[i+96]=i+6
 b[112:120]=[15,13,14,16,17,14,13,15]
 return b,0
def L(f):
 b=[-1]*128
 p=f.split();x=p[0].split("/")
 for i in range(8):
  q=(7-i)*16
  for c in x[i]:
   if"1"<=c<="9":q+=ord(c)-48
   else:b[q]=C.find(c.lower())+(0 if c<"a"else 6);q+=1
 return b,0 if p[1]=="w"else 1
def A(b,s,p):
 for d in(15,17):
  t=s+d if p==0 else s-d
  if t&0x88==0and b[t]==p*6:return 1
 for d in(31,33,14,18,-14,-18,-31,-33):
  t=s+d
  if t&0x88==0and b[t]==p*6+1:return 1
 for d in(1,-1,16,-16):
  t=s+d
  while t&0x88==0:
   z=b[t]
   if z!=-1:
    if z in(p*6+3,p*6+4):return 1
    break
   t+=d
 for d in(15,17,-15,-17):
  t=s+d
  while t&0x88==0:
   z=b[t]
   if z!=-1:
    if z in(p*6+2,p*6+4):return 1
    break
   t+=d
 for d in(1,-1,16,-16,15,17,-15,-17):
  t=s+d
  if t&0x88==0and b[t]==p*6+5:return 1
 return 0
def G(b,p):
 M=[];o=p*6+6
 for s in range(128):
  u=b[s]
  if u<0 or u<o-6 or u>o-1:continue
  t=u-o+6
  if t==0:
   d=16 if p==0 else-16
   t2=s+d
   if t2&0x88==0and b[t2]==-1:
    if(p==0and s>=112)or(p==1and s<16):
     for z in(1,2,3,4):M.append((s,t2,z))
    else:M.append((s,t2,0))
    if(p==0and 16<=s<24)or(p==1and 96<=s<104):
     t2=s+d+d
     if t2&0x88==0and b[t2]==-1:M.append((s,t2,0))
   for d in(15,17):
    t2=s+d if p==0 else s-d
    if t2&0x88==0and b[t2]!=-1and b[t2]>=o:M.append((s,t2,0))
  elif t==1:
   for d in(31,33,14,18,-14,-18,-31,-33):
    t2=s+d
    if t2&0x88==0and(b[t2]==-1or b[t2]>=o):M.append((s,t2,0))
  elif t<4:
   for d in([15,17,-15,-17]if t==2 else[1,-1,16,-16]if t==3 else[1,-1,16,-16,15,17,-15,-17]):
    t2=s+d
    while t2&0x88==0:
     if b[t2]==-1:M.append((s,t2,0))
     elif b[t2]>=o:M.append((s,t2,0));break
     else:break
     t2+=d
  else:
   for d in(1,-1,16,-16,15,17,-15,-17):
    t2=s+d
    if t2&0x88==0and(b[t2]==-1or b[t2]>=o):M.append((s,t2,0))
 return M
def E(b):
 s=0
 for i in range(128):
  u=b[i]
  if u<0 or u in(5,11):continue
  v=V[u%6]
  if u<6:s+=v+P[i]*(u!=5)
  else:s-=v+P[127-i]*(u!=11)
 return s
K={}
def S(b,p,d,a,B,n):
 n[0]+=1
 if n[0]>5e5:return E(b)if p==0 else-E(b)
 if d<=0:
  s=E(b)if p==0 else-E(b)
  if s>=B:return B
  if s>a:a=s
  ms=[m for m in G(b,p)if b[m[1]]!=-1]
  ms.sort(key=lambda m:(-V[b[m[1]]%6]*(b[m[1]]>=6))+V[b[m[0]]%6])
  for m in ms:
   nb=b[:];nb[m[1]]=nb[m[0]];nb[m[0]]=-1
   k=next(i for i in range(128)if nb[i]==5+p*6)
   if A(nb,k,1-p):continue
   sc=-S(nb,1-p,0,-B,-a,n)
   if sc>a:a=sc
   if a>=B:break
  return a
 ms=G(b,p);ms.sort(key=lambda m:(-V[b[m[1]]%6]*(b[m[1]]>=6))+V[b[m[0]]%6]+(K.get(m[1],0)<<8))
 bst=-9e5
 for m in ms:
  nb=b[:];nb[m[1]]=nb[m[0]];nb[m[0]]=-1
  if m[2]:nb[m[1]]=m[2]+6*p
  k=next(i for i in range(128)if nb[i]==5+p*6)
  if A(nb,k,1-p):continue
  sc=-S(nb,1-p,d-1,-B,-a,n)
  if sc>bst:bst=sc
  if sc>a:a=sc
  if a>=B:K[m[1]]=K.get(m[1],0)+1;break
 return bst
def T(b,p):
 ba=-9e5;bm=None
 for d in range(1,6):
  n=[0];ms=G(b,p)
  if not ms:return None
  ms.sort(key=lambda m:(-V[b[m[1]]%6]*(b[m[1]]>=6))+V[b[m[0]]%6]+(K.get(m[1],0)<<8))
  for m in ms:
   nb=b[:];nb[m[1]]=nb[m[0]];nb[m[0]]=-1
   if m[2]:nb[m[1]]=m[2]+6*p
   k=next(i for i in range(128)if nb[i]==5+p*6)
   if A(nb,k,1-p):continue
   sc=-S(nb,1-p,d-1,-9e5,9e5,n)
   if sc>ba:ba=sc;bm=m
  if n[0]>2e5:break
 return bm
def P(P,b):
 req=r.Request(E+P,data=json.dumps(b).encode(),headers={"content-type":"application/json"})
 try:
  with r.urlopen(req)as x:return json.load(x)
 except r.HTTPError as e:sys.exit(f"{P}:{e.code}")
b,s=I()
while 1:
 g=P("/game",{})
 if g.get("status")=="done":break
 b,s=L(g["fen"])
 while g.get("status")=="your_move":
  m=T(b,s)
  if m is None:P("/resign",{"game":g["game"]});break
  nb=b[:];nb[m[1]]=nb[m[0]];nb[m[0]]=-1
  if m[2]:nb[m[1]]=m[2]+6*s
  b=nb;s=1-s
  u=F[m[0]&7]+str(8-(m[0]>>4))+F[m[1]&7]+str(8-(m[1]>>4))+(C[m[2]]if m[2]else"")
  g=P("/move",{"game":g["game"],"move":u})