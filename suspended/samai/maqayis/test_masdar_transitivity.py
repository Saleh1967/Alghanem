"""مصدر الثلاثيّ المجرّد (المحكم) بدالّة: حركة عين الماضي + التعدية المشهودة، شاملًا المعتلّ والمهموز.

التعدية «متعدٍّ» لا تُعطى إلا بشاهد مسمّى:
  (أ) المحكم: مضارعٌ متّصلٌ بضمير مفعول (يلمقها، يردحه، يربعهم)،
  (ب) المصحف QAC: للجذر فعلٌ مجرّد مبنيّ للمجهول (PASS|VF:1)،
  (ج) الصحيحان: صيغة مجهول مشكولة من الجذر (فُعِلَ، يُفْعَلُ، قِيلَ، دُعِيَ).
وما لا شاهد له «غير مشهود التعدّي» — لا يُسمّى «لازمًا» (المادة ١٣: الغياب ليس امتناعًا).
حركة عين الماضي من الرموز الوسيط (باب التصريف)، ويُستبعد الجذر الذي له أكثر من حركة.
"""
import json, re, csv, collections, sys
QAC, BUK, MUS, VERBS = sys.argv[1:5]
csv.field_size_limit(10**9)
def norm(s):
    s = re.sub(r'[ً-ْـ]', '', s)
    return s.replace('أ','ء').replace('إ','ء').replace('آ','ءا').replace('ؤ','ء').replace('ئ','ء').replace('ى','ي')
M = json.load(open('muhkam_masadir.json'))
roots = {o['root'] for o in M}
wit = collections.defaultdict(list)
# (أ) المحكم
for o in M:
    if re.search(r'(ه|ها|هم|هما|هن)$', o['impf']) and len(o['impf']) > 4:
        wit[o['root']].append(('المحكم', o['witness'][:50]))
# (ب) المصحف
for line in open(QAC, encoding='utf-8'):
    loc, form, tag, feat = line.rstrip('\n').split('\t'); f = feat.split('|')
    if tag == 'V' and 'PASS' in f and 'VF:1' in f:
        r = norm([x[5:] for x in f if x.startswith('ROOT:')][0]) if any(x.startswith('ROOT:') for x in f) else ''
        if r in roots and len(wit[r]) < 6: wit[r].append(('المصحف', f'{loc} {form}'))
# (ج) الصحيحان: مجهول الماضي والمضارع، صحيحًا ومعتلًّا
D = '[ً-ْ]*'
def passive_rx(r):
    a, b, c = (re.escape(x) for x in r)
    pats = [f'{a}ُ{b}ِ{c}َ', f'يُ{a}ْ{b}َ{c}ُ', f'تُ{a}ْ{b}َ{c}ُ']
    if r[1] in 'وي': pats.append(f'{a}ِي{c}َ')            # قِيلَ، بِيعَ
    if r[2] in 'وي': pats.append(f'{a}ُ{b}ِيَ')            # دُعِيَ، رُمِيَ
    return re.compile(r'^(?:[وف]َ)?(?:' + '|'.join(pats) + ')')
rx = {r: passive_rx(r) for r in roots if 'ء' not in r}
idx = collections.defaultdict(list)
for r in rx: idx[r[0]].append(r)
for path in (BUK, MUS):
    for row in csv.reader(open(path, encoding='utf-8')):
        for t in re.findall(r'[ء-يً-ْ]+', row[1]):
            core = re.sub(r'^(?:[وف]َ)', '', t); core = re.sub(r'^[يت]ُ', '', core)
            for r in idx.get(core[:1], []):
                if len(wit[r]) < 6 and rx[r].match(t):
                    wit[r].append(('الصحيحان', t))
# حركة عين الماضي
vow = collections.defaultdict(set)
for r in csv.reader(open(VERBS, encoding='utf-8'), delimiter='\t'):
    if r and not r[0].startswith('#') and len(r) > 2 and r[2] in '123456':
        vow[norm(r[1])].add({'1': 'a', '2': 'a', '3': 'a', '4': 'i', '5': 'u', '6': 'i'}[r[2]])
typ = lambda r: 'معتل' if set(r) & set('وي') else ('مهموز' if 'ء' in r else ('مضعف' if r[1] == r[2] else 'سالم'))
rows = []
for o in M:
    v = vow.get(o['root'])
    if not v or len(v) != 1: continue
    t = 'متعد' if wit[o['root']] else 'غير مشهود'
    rows.append((o['root'], next(iter(v)), t, typ(o['root']), o['pattern']))
def loo(feat, R):
    by = collections.defaultdict(collections.Counter)
    for r in R: by[feat(r)][r[4]] += 1
    ok = n = 0
    for r in R:
        c = by[feat(r)].copy(); c[r[4]] -= 1; c = {k: v for k, v in c.items() if v > 0}
        if c: n += 1; ok += max(c, key=c.get) == r[4]
    return ok, n
print('جذور بشاهد تعدية:', sum(1 for r in roots if wit[r]), 'من', len(roots),
      '| بحسب المصدر:', dict(collections.Counter(w[0] for r in roots for w in wit[r][:1])))
print('صفوف الاختبار (حركة ماضٍ وحيدة):', len(rows), dict(collections.Counter(r[3] for r in rows)))
for name, R in [('الكلّ', rows), ('السالم', [r for r in rows if r[3] == 'سالم']), ('المعتلّ والمهموز', [r for r in rows if r[3] != 'سالم'])]:
    print(f'== {name} (n={len(R)})')
    for fname, f in [('ثابت', lambda r: 0), ('حركة الماضي', lambda r: r[1]), ('التعدية المشهودة', lambda r: r[2]),
                     ('حركة الماضي + التعدية', lambda r: (r[1], r[2]))]:
        ok, n = loo(f, R); print(f'   {fname}: {ok}/{n} = {ok/n:.1%}')
by = collections.defaultdict(collections.Counter)
for r in rows: by[(r[1], r[2])][r[4]] += 1
for k, c in sorted(by.items()): print('   ', k, sum(c.values()), dict(c.most_common(5)))
# قاعدة الألفية بالصيغ غير المشكولة؛ «غير مشهود» يقوم مقام «لازم» بإعلان
def alf(v, t):
    if v == 'a' and t == 'متعد': return {'فعل'}
    if v == 'i' and t == 'غير مشهود': return {'فعل'}
    if v == 'a' and t == 'غير مشهود': return {'فعول'}
    if v == 'u': return {'فعالة', 'فعولة'}
    return None
cov = [r for r in rows if alf(r[1], r[2])]; hit = sum(r[4] in alf(r[1], r[2]) for r in cov)
print(f'قاعدة الألفية (غير مشهود = لازم): تغطّي {len(cov)}، تصيب {hit} = {hit/len(cov):.1%}')
json.dump({'rows': rows, 'witness': {r: wit[r][:3] for r in roots if wit[r]}}, open('result_masdar_trans.json', 'w'), ensure_ascii=False)
