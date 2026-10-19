import json, re, collections, math, sys
pl=json.load(open('plural_pairs.json'))
def clean(t):
    t=t.replace('آ','ا').replace('ٓ','').replace('ْ','')          # المدّ، والسكون غير المكتوب = سكون
    t=re.sub('^(.)ّ',r'\1',t)                                       # شدّة إدغام لام التعريف
    t=re.sub('ؤُ?ا?$','ء',t); t=re.sub('ئ$','ء',t)                 # همزة الآخر برسمها
    t=re.sub('ت$','ة',t)                                            # تاء مربوطة مرسومة مبسوطة
    return t
def bare(t): return re.sub('[َُِّ]','',t)
pairs=[]
for r,ts,tp in pl:
    a,b=clean(ts),clean(tp)
    if bare(a)==bare(b) and a.replace('َ','')==b.replace('َ',''): continue   # اللمّة نفسها جمع
    pairs.append((r,a,b))
pairs=sorted(set(pairs))
by=collections.defaultdict(collections.Counter)
for r,a,b in pairs: by[a][b]+=1
# دقّة «ترك واحد»: يُتنبّأ بجمع الزوج بأكثر جموع المفرد نفسه في بقية الأزواج
def loo(group):
    ok=n=0
    for r,a,b in group:
        c=by[a].copy(); c[b]-=1
        c={k:v for k,v in c.items() if v>0}
        if not c: continue
        n+=1; ok+= (max(c,key=c.get)==b)
    return ok,n
heavy=[p for p in pairs if len(bare(p[1]).replace('ة',''))>=4]
light=[p for p in pairs if len(bare(p[1]).replace('ة',''))==3]
for name,g in [('المفرد ثلاثي الحروف (فعل، فعل، فعل…)',light),('المفرد رباعي الحروف فأكثر (مفعل، فاعل، فعيل، فعال…)',heavy)]:
    ok,n=loo(g); print(f'{name}: أزواج={len(g)} قابلة للاختبار={n} دقّة ترك-واحد={ok}/{n}={ok/n:.1%}' if n else name)
print('-- صيغ الجمع التي تبدأ بهمزة: هل يليها ساكن دائمًا؟')
hz=collections.Counter()
for r,a,b in pairs:
    if b.startswith('أ'): hz[(b, b[2:3]=='َ' or b[2:3]=='ُ' or b[2:3]=='ِ')]+=1
for (b,vowel),c in hz.items(): print('   ',b,'يليها متحرك' if vowel else 'يليها ساكن',c)
print('-- صيغ جمع تبدأ بساكن:', [b for r,a,b in pairs if b[1:2] not in 'َُِ'])
print('-- مفرد ← جموعه (الأكثر أزواجًا):')
for a,c in sorted(by.items(),key=lambda x:-sum(x[1].values()))[:16]: print('   ',a,'->',dict(c.most_common(5)))
json.dump(pairs,open('plural_pairs_clean.json','w'),ensure_ascii=False)
