import json, re, collections
pairs=json.load(open('plural_pairs_clean.json'))
def bare(t): return re.sub('[َُِّ]','',t)
# الدالّة المرشَّحة F: تبني الجمع من «أربع خانات» المفرد بقانون واحد:
#   C1 a C2 aa C3 (i|ii) C4 ، والطول في الخانة الأخيرة يُورَث من المفرد.
def F(a):
    b=bare(a)
    m=re.fullmatch(r'([مأت])فعل',b)                       # مفعل، أفعل، تفعل
    if m: return m.group(1)+'َفَاعِل'
    m=re.fullmatch(r'([مأت])فع[اوي]ل',b)                  # مفعال، مفعول، تفعيل ⇒ طول موروث
    if m: return m.group(1)+'َفَاعِيل'
    if re.fullmatch(r'فاعلة?',b): return 'فَوَاعِل'       # الألف بعد الفاء تصير واوًا
    if re.fullmatch(r'فع[اوي]لة',b): return 'فَعَائِل'    # المدّ الثالث يصير همزة
    if re.fullmatch(r'فوعل|فيعل',b): return 'فَوَاعِل' if 'و' in b else 'فَيَاعِل'
    return None
ok=n=0; miss=[]
for r,a,b in pairs:
    p=F(a)
    if p is None: continue
    n+=1
    if p==b: ok+=1
    else: miss.append((r,a,b,p))
print(f'المفردات ذات الخانات الأربع: {n} زوجًا، طابقت الدالّة F: {ok}/{n} = {ok/n:.1%}')
for x in miss: print('   خلاف:',x)
light=[(r,a,b) for r,a,b in pairs if F(a) is None and len(bare(a).replace('ة',''))==3]
print('المفردات الثلاثية (خارج F):',len(light),'زوجًا؛ صيغها:',dict(collections.Counter(bare(a) for _,a,_ in light).most_common()))
