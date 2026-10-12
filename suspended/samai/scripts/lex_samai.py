import csv,re,collections,math,json,sys
D=sys.argv[1]
DIA='ًٌٍَُِّْ'
def strip(s): return re.sub('['+DIA+'ٰ]','',s)
def waqf(s):
    s=s.strip(); s=re.sub('[ًٌٍ]ا?$','',s); s=re.sub('[َُِ]$','',s); return s
def templ(s,root):
    out=[];k=0
    for ch in s:
        if k<3 and ch==root[k]: out.append('فعل'[k]);k+=1
        else: out.append(ch)
    return ''.join(out) if k==3 else None
def sound(r): return len(r)==3 and not set(r)&set('اويءأإؤئى') and len(set(r))==3
def H(c):
    n=sum(c.values()); return -sum(v/n*math.log2(v/n) for v in c.values() if v)
def condH(pairs):
    by=collections.defaultdict(collections.Counter)
    for x,y in pairs: by[x][y]+=1
    n=len(pairs); return sum(sum(c.values())/n*H(c) for c in by.values())
def loo(pairs):
    by=collections.defaultdict(collections.Counter)
    for x,y in pairs: by[x][y]+=1
    ok=n=0
    for x,y in pairs:
        c=by[x].copy(); c[y]-=1; c={k:v for k,v in c.items() if v>0}
        if not c: continue
        n+=1; ok+= max(c,key=c.get)==y
    return ok,n
rd=lambda p: [r for r in csv.reader(open(p,encoding='utf-8'),delimiter='\t') if r and not r[0].startswith('#')]
V=rd(D+'/verbs/verb_triliteral.csv')
verbs=collections.defaultdict(list)          # الفعل المشكول -> [(باب، تعدية)]
for r in V:
    if len(r)>3 and r[2]: verbs[r[0].strip()].append((r[2],r[3]))
M=rd(D+'/nouns/masdar.csv')
# ===== أ. مصدر المجرّد
rows=[]
for r in M:
    if len(r)<12 or r[5].strip()!='مصدر' or r[11].strip()!='مفرد': continue
    root=r[3].strip(); verb=r[6].strip()
    if not sound(root) or verb not in verbs: continue
    t=templ(waqf(r[1]),root); vt=templ(verb,root)
    if not t or not vt or vt not in ('فَعَلَ','فَعِلَ','فَعُلَ'): continue
    for bab,T in set(verbs[verb]): rows.append((root,verb,vt,bab,T,t))
rows=sorted(set(rows))
y=collections.Counter(r[5] for r in rows)
print(f'== أ. مصدر المجرّد: {len(rows)} صفًّا (جذر، فعل، باب، تعدية، مصدر)، {len(set(r[0] for r in rows))} جذرًا، {len(y)} صيغة')
print('   الصيغ:',dict(y.most_common(12)))
maj=y.most_common(1)[0][1]
print(f'   سقف القوانين الثلاثة (هيكل مقطعيّ واحد ⇒ دالّة ثابتة): {maj}/{len(rows)} = {maj/len(rows):.1%}  H={H(y):.2f} بت')
feats={'حركة عين الماضي':lambda r:r[2],'الباب':lambda r:r[3],'التعدية':lambda r:r[4],
       'حركة الماضي+التعدية':lambda r:(r[2],r[4]),'الباب+التعدية':lambda r:(r[3],r[4])}
for k,f in feats.items():
    p=[(f(r),r[5]) for r in rows]; ok,n=loo(p)
    print(f'   {k}: H(مصدر|·)={condH(p):.2f}  دقّة ترك-واحد={ok}/{n}={ok/n:.1%}')
# قاعدة الألفية (من الذاكرة): فعَل المتعدّي ← فَعْل؛ فعِل اللازم ← فَعَل؛ فعَل اللازم ← فُعُول؛ فعُل ← فَعالة/فُعولة
def alfiyya(vt,T):
    if vt=='فَعَلَ' and T=='م': return {'فَعْل'}
    if vt=='فَعِلَ' and T=='ل': return {'فَعَل'}
    if vt=='فَعَلَ' and T=='ل': return {'فُعُول'}
    if vt=='فَعُلَ': return {'فَعَالَة','فُعُولَة'}
    return None
cov=[r for r in rows if alfiyya(r[2],r[4])]
hit=[r for r in cov if r[5] in alfiyya(r[2],r[4])]
print(f'   قاعدة الألفية الأساس: تغطّي {len(cov)} صفًّا، تصيب {len(hit)} = {len(hit)/len(cov):.1%}')
for key in [('فَعَلَ','م'),('فَعِلَ','ل'),('فَعَلَ','ل'),('فَعُلَ','ل')]:
    c=collections.Counter(r[5] for r in rows if (r[2],r[4])==key); n=sum(c.values())
    print('     ',key,n,dict(c.most_common(6)))
json.dump(rows,open('masdar_rows.json','w'),ensure_ascii=False)
# ===== ب. تفعيل/تفعلة بحسب نوع الجذر
c=collections.Counter()
ex=collections.defaultdict(list)
for r in M:
    if len(r)<12 or r[5].strip()!='مصدر' or r[11].strip()!='مفرد': continue
    root=r[3].strip(); w=strip(waqf(r[1]))
    if len(root)!=3 or not w.startswith('ت'): continue
    r1,r2,r3=root
    if r1 in 'وياءأ' or r2 in 'ويا': continue
    typ='ناقص' if r3 in 'وي' else ('مهموز اللام' if r3 in 'ءأ' else 'سالم')
    R3 = 'ي' if typ=='ناقص' else r3
    if typ=='مهموز اللام':
        if re.fullmatch('ت'+r1+r2+'ي[ءئ]',w): k='تفعيل'
        elif re.fullmatch('ت'+r1+r2+'[ئء]ة',w): k='تفعلة'
        else: continue
    elif w=='ت'+r1+r2+'ي'+R3: k='تفعيل'
    elif w=='ت'+r1+r2+R3+'ة': k='تفعلة'
    else: continue
    c[(typ,k)]+=1; ex[(typ,k)].append(r[1])
print('== ب. مصدر فعّل: تفعيل أم تفعلة؟')
for typ in ['سالم','مهموز اللام','ناقص']:
    a,b=c[(typ,'تفعيل')],c[(typ,'تفعلة')]
    print(f'   {typ}: تفعيل {a}، تفعلة {b}   أمثلة تفعلة: {ex[(typ,"تفعلة")][:6]}  أمثلة تفعيل: {ex[(typ,"تفعيل")][:4]}')
