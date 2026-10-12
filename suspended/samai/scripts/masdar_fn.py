import json,collections
rows=json.load(open('masdar_rows.json'))   # (root, verb, past, bab, T, masdar)
BAB={'1':'فعَل يفعُل','2':'فعَل يفعِل','3':'فعَل يفعَل','4':'فعِل يفعَل','5':'فعُل يفعُل','6':'فعِل يفعِل'}
# لكل فعل (بابه وتعديته) مجموعة مصادره في المعجم
verb=collections.defaultdict(set); key={}
for r,v,vt,b,T,m in rows:
    verb[(v,b,T)].add(m)
items=list(verb.items())
print('أفعال (فعل، باب، تعدية):',len(items),'| متوسط المصادر لكل فعل:',round(sum(len(s) for _,s in items)/len(items),2))
def trans(T,mode): return {'م':'متعد','ل':'لازم','ك':'متعد' if mode=='passive' else 'كلاهما'}[T]
def evaluate(feat,name):
    # التنبّؤ: أكثر مصدرٍ عند الأفعال الأخرى ذات المدخل نفسه (ترك-واحد)، والإصابة إن وقع في مجموعة الفعل
    by=collections.defaultdict(collections.Counter)
    for k,s in items:
        for m in s: by[feat(k)][m]+=1
    ok=n=0
    for k,s in items:
        c=by[feat(k)].copy()
        for m in s: c[m]-=1
        c={a:b for a,b in c.items() if b>0}
        if not c: continue
        n+=1; ok+= max(c,key=c.get) in s
    print(f'  {name}: {ok}/{n} = {ok/n:.1%}')
print('الإصابة = المصدر المتنبَّأ به أحدُ مصادر الفعل في المعجم:')
evaluate(lambda k:0,'ثابت')
evaluate(lambda k:k[0][2:4] if False else None,'—') if False else None
past=lambda k: {'1':'a','2':'a','3':'a','4':'i','5':'u','6':'i'}[k[1]]
evaluate(lambda k:past(k),'حركة عين الماضي')
evaluate(lambda k:k[1],'الباب (الماضي + المضارع)')
evaluate(lambda k:(past(k),trans(k[2],'passive')),'الماضي + التعدية (له مجهول ⇒ متعدٍّ)')
evaluate(lambda k:(k[1],trans(k[2],'passive')),'الباب + التعدية (له مجهول ⇒ متعدٍّ)')
evaluate(lambda k:(k[1],k[2]),'الباب + التعدية بأصنافها الثلاثة (م/ل/ك)')
# قاعدة الألفية (من الذاكرة) على مجموعات المصادر
def alf(k):
    p,t=past(k),trans(k[2],'passive')
    if p=='a' and t=='متعد': return {'فَعْل'}
    if p=='i' and t=='لازم': return {'فَعَل'}
    if p=='a' and t=='لازم': return {'فُعُول'}
    if p=='u': return {'فَعَالَة','فُعُولَة','فَعالَة'}
    return None
cov=[(k,s) for k,s in items if alf(k)]
print(f'  قاعدة الألفية الأساس: تغطّي {len(cov)} فعلًا، تصيب {sum(bool(alf(k)&s) for k,s in cov)} = {sum(bool(alf(k)&s) for k,s in cov)/len(cov):.1%}')
for g in [('a','متعد'),('i','لازم'),('a','لازم'),('u','لازم'),('i','متعد')]:
    sub=[(k,s) for k,s in items if (past(k),trans(k[2],'passive'))==g]
    c=collections.Counter(m for _,s in sub for m in s)
    print('   ',g,len(sub),dict(c.most_common(5)))
