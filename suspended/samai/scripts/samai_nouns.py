import sys, re, collections, math, json
Q=sys.argv[1]
H='ًٌٍَُِّْٰ'          # diacritics incl. dagger alif
FATHA,DAMMA,KASRA,SUKUN,SHADDA='َ','ُ','ِ','ْ','ّ'
TAN='ًٌٍ'
def norm(s):
    s=s.replace('ٱ','ا').replace('ٰ','ا').replace('ـ','')
    s=re.sub('[ۭۡۢۜ۟۠ۥۦ۪ۨ]','',s)   # Quranic small marks
    return s
def waqf(s):
    s=re.sub('['+TAN+'][اى]?$','',s)          # تنوين (وألف التنوين)
    s=re.sub('[َُِ]$','',s)                     # حركة الإعراب
    return s
def template(s,root):
    out=[];k=0
    for ch in s:
        if k<3 and ch==root[k]:
            out.append('فعل'[k]);k+=1
        else: out.append(ch)
    return ''.join(out) if k==3 else None
def sound(root):
    return len(root)==3 and not set(root)&set('اويءأإؤئى') and len(set(root))==3
def entropy(c):
    n=sum(c.values()); return -sum(v/n*math.log2(v/n) for v in c.values())
def cond_entropy(pairs):
    by=collections.defaultdict(collections.Counter)
    for x,y in pairs: by[x][y]+=1
    n=len(pairs); return sum(sum(c.values())/n*entropy(c) for c in by.values())
rows=[]
for line in open(Q,encoding='utf-8'):
    loc,form,tag,feat=line.rstrip('\n').split('\t')
    f=feat.split('|'); d={x.split(':')[0]:x.split(':',1)[1] for x in f if ':' in x}
    rows.append((loc,norm(form),tag,set(f),d))
# ---- A: المصادر
vn=collections.Counter(); vnform=collections.defaultdict(set); verbpat={}
for loc,form,tag,fs,d in rows:
    r=d.get('ROOT','')
    if tag=='V' and d.get('VF')=='1' and 'PERF' in fs and 'PASS' not in fs and sound(r):
        t=template(norm(d['LEM']),r)
        if t: verbpat.setdefault(r,collections.Counter())[t]+=1
    if tag=='N' and 'VN' in fs and sound(r):
        t=template(waqf(norm(d['LEM'])),r)
        if t: vn[(d['VF'],t)]+=1; vnform[d['VF']].add((r,t))
print('== المصادر (جذور سالمة، صيغة الوقف للَّمّة)')
for vf in sorted(vnform,key=int):
    types=collections.Counter(t for r,t in vnform[vf])
    print(f' VF{vf}: جذور={len(vnform[vf])} صيغ مختلفة={len(types)} H={entropy(types):.2f} بت ->',dict(types.most_common(6)))
# المجرد: الصيغة المصدرية بشرط باب الماضي
pairs=[]
for r,t in vnform.get('1',[]):
    if r in verbpat:
        vp=verbpat[r].most_common(1)[0][0]; pairs.append((vp,t))
types=collections.Counter(t for _,t in pairs)
print(f' VF1 مع باب الماضي: n={len(pairs)} H(مصدر)={entropy(types):.2f} H(مصدر|باب)={cond_entropy(pairs):.2f}')
by=collections.defaultdict(collections.Counter)
for vp,t in pairs: by[vp][t]+=1
for vp,c in by.items(): print('   ',vp,dict(c.most_common(8)))
json.dump(sorted(pairs),open('masdar_pairs.json','w'),ensure_ascii=False)
# ---- B: جمع التكسير
pl=set()
for loc,form,tag,fs,d in rows:
    r=d.get('ROOT','')
    if tag=='N' and ('MP' in fs or 'FP' in fs) and sound(r) and 'PCPL' not in ' '.join(fs) and 'VN' not in fs:
        w=waqf(form)
        if re.search('(ونَ?|ينَ?|ات|اتِ|اتُ|اتٍ|اتٌ)$',re.sub('['+H+']','',form)): continue
        if re.search('ات$',re.sub('['+H+']','',w)): continue
        ts=template(waqf(norm(d['LEM'])),r); tp=template(w,r)
        if ts and tp and ts!=tp: pl.add((r,ts,tp))
print('== جمع التكسير (جذور سالمة، صيغ الوقف)')
pairs=[(ts,tp) for r,ts,tp in pl]
print(f' أزواج={len(pairs)} صيغ جمع={len(set(p for _,p in pairs))} H(جمع)={entropy(collections.Counter(p for _,p in pairs)):.2f} H(جمع|مفرد)={cond_entropy(pairs):.2f}')
by=collections.defaultdict(collections.Counter)
for ts,tp in pairs: by[ts][tp]+=1
for ts,c in sorted(by.items(),key=lambda x:-sum(x[1].values()))[:14]: print('   ',ts,'->',dict(c.most_common(6)))
json.dump(sorted(pl),open('plural_pairs.json','w'),ensure_ascii=False)
