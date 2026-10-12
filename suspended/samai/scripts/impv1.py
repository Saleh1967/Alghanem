import sys, collections
words=collections.OrderedDict()
for line in open(sys.argv[1],encoding='utf-8'):
    loc,form,tag,feat=line.rstrip('\n').split('\t')
    s,v,w,seg=map(int,loc.split(':'))
    words.setdefault((s,v,w),[]).append((form,tag,feat))
T=collections.Counter(); EX={}
for (s,v,w),segs in words.items():
    for i,(form,tag,feat) in enumerate(segs):
        f=feat.split('|')
        if tag=='V' and 'IMPV' in f and 'VF:1' in f:
            r=[x[5:] for x in f if x.startswith('ROOT:')]
            if not r or r[0][0]!='أ': continue
            ctx='وصل(بعد و/ف)' if i>0 else 'ابتداء الكلمة'
            hz=any(c in form for c in 'ءأإؤئٔ')
            k=(r[0],ctx,'الهمزة ثابتة' if hz else 'الهمزة محذوفة')
            T[k]+=1; EX.setdefault(k,f"{s}:{v} {''.join(g[0] for g in segs)}")
for k in sorted(T): print(*k, T[k], EX[k], sep=' | ')
