import csv,re,collections,json,sys
exec(open('lex_samai.py').read().split('rd=lambda')[0])
rd=lambda p: [r for r in csv.reader(open(p,encoding='utf-8'),delimiter='\t') if r and not r[0].startswith('#')]
D=sys.argv[1]+'/nouns/'
def clean(t):
    t=t.replace('آ','ا').replace('ٓ','').replace('ْ',''); t=re.sub('^(.)ّ',r'\1',t)
    t=re.sub('[ؤئ]$','ء',t); return t.strip()
pairs=set()
for f in ['jamid.csv','fa3il.csv','mouchabbaha.csv','sifates.csv','masdar.csv']:
    for r in rd(D+f):
        if len(r)<14: continue
        root=r[3].strip()
        if not sound(root): continue
        if r[11].strip()=='مفرد':
            for p in r[12].split(';'):
                p=p.strip()
                if not p or '+' in p or p.startswith('ات') or p.startswith('ج'): continue
                pairs.add((root,r[1].strip(),p))
        elif r[11].strip()=='جمع' and r[13].strip():
            pairs.add((root,r[13].strip(),r[1].strip()))
out=[]
for root,s,p in pairs:
    a=templ(waqf(s),root); b=templ(waqf(p),root)
    if not a or not b: continue
    a,b=clean(a),clean(b)
    if strip(b).endswith('ات') or strip(b).endswith('ون') or strip(b).endswith('ين'): continue
    if strip(a)==strip(b): continue
    out.append((root,a,b))
out=sorted(set(out))
print('أزواج (جذر، مفرد، جمع مكسَّر) من الرموز الوسيط، جذور سالمة:',len(out))
# --- اختبار F خارج العيّنة (صيغت على المصحف)
def bare(t): return re.sub('[َُِّ]','',t)
def F(a):
    b=bare(a)
    m=re.fullmatch(r'([مأت])فعل',b)
    if m: return m.group(1)+'َفَاعِل'
    m=re.fullmatch(r'([مأت])فع[اوي]ل',b)
    if m: return m.group(1)+'َفَاعِيل'
    if re.fullmatch(r'فاعلة',b): return 'فَوَاعِل'
    if re.fullmatch(r'فع[اوي]لة',b): return 'فَعَائِل'
    return None
dom=[x for x in out if F(x[1])]
hit=[x for x in dom if bare(F(x[1]))==bare(x[2])]
print(f'F (مصوغة على المصحف) على معجمٍ مستقلّ: مجالها {len(dom)} زوجًا، تطابق {len(hit)} = {len(hit)/len(dom):.1%}')
mc=collections.Counter((bare(x[1]),bare(x[2])) for x in dom if x not in hit)
print('   أكثر الخلاف:',mc.most_common(10))
by_s=collections.Counter(bare(x[1]) for x in dom); by_h=collections.Counter(bare(x[1]) for x in hit)
for s in by_s: print(f'     {s}: {by_h[s]}/{by_s[s]}')
# --- المفرد الثلاثيّ: هيكل مقطعيّ (ما تراه القوانين) مقابل الصيغة كاملة
def skeleton(t):
    t=t.replace('ة','')
    s='';i=0
    while i<len(t):
        ch=t[i]
        if ch in 'َُِ':
            if i+1<len(t) and t[i+1] in 'اوي' and (i+2>=len(t) or t[i+2] not in 'َُِ'): s+='VV';i+=2;continue
            s+='V'
        elif ch=='ّ': s+='C'
        elif ch in 'اوي' and (i==0 or t[i-1] not in 'َُِ') and (i+1>=len(t) or t[i+1] not in 'َُِ'): s+='VV'
        else: s+='C'
        i+=1
    return s
tri=[x for x in out if len(bare(x[1]).replace('ة',''))==3]
print(f'المفرد الثلاثي: {len(tri)} زوجًا، {len(set(x[2] for x in tri))} صيغة جمع')
for name,f in [('ثابت (لا شيء)',lambda x:0),('الهيكل المقطعي للمفرد (ما تراه القوانين)',lambda x:skeleton(x[1])),
               ('صيغة المفرد كاملة (بالحركات)',lambda x:x[1]),('صيغة المفرد + التاء',lambda x:(x[1],'ة' in x[1]))]:
    p=[(f(x),bare(x[2])) for x in tri]; ok,n=loo(p)
    print(f'   {name}: H(جمع|·)={condH(p):.2f} بت، دقّة ترك-واحد={ok}/{n}={ok/n:.1%}')
by=collections.defaultdict(collections.Counter)
for x in tri: by[x[1]][bare(x[2])]+=1
for s,c in sorted(by.items(),key=lambda z:-sum(z[1].values()))[:8]:
    print('     ',s,skeleton(s),sum(c.values()),dict(c.most_common(5)))
# --- فاعِل المذكّر
fa=collections.Counter(bare(x[2]) for x in out if bare(x[1])=='فاعل')
print('فاعِل المذكّر ← جموعه:',sum(fa.values()),dict(fa.most_common(8)))
json.dump(out,open('lex_plural_pairs.json','w'),ensure_ascii=False)
