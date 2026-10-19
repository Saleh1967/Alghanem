"""تنفيذ PREREG_ajwaf_fuul_and_khalaf.md على القاموس المحيط (المرجع المحجوب)، ثم وصفيًّا على الاستكشاف."""
import json, re, random, collections, itertools, sys
def wt(r):
    if r[0] in 'وي': return 'مثال'
    if r[1] in 'وي': return 'أجوف'
    if r[2] in 'وي': return 'ناقص'
    return 'سالم' if 'ء' not in r and r[1] != r[2] else 'آخر'
def norm(s):
    s = re.sub(r'[ً-ْـ]', '', s)
    return s.replace('أ','ء').replace('إ','ء').replace('آ','ءا').replace('ؤ','ء').replace('ئ','ء').replace('ى','ي')
strip = lambda w: re.sub(r'ا$', '', re.sub(r'^(?:و|ف|ب|ل|ك)?(?:ال)?', '', norm(w)))
def perm(lab, val, seed=1967):
    d0 = lambda L: (sum(v for l, v in zip(L, val) if l) / max(1, sum(L))) - (sum(v for l, v in zip(L, val) if not l) / max(1, len(L) - sum(L)))
    obs = d0(lab); L = lab[:]; random.seed(seed); le = 0
    for _ in range(10000):
        random.shuffle(L); le += d0(L) <= obs
    return obs, (le + 1) / 10001
SEC = {norm(o['root']): o for o in json.load(open('maqayis_sections.json'))}
where = {}
for r, o in SEC.items():
    d = collections.defaultdict(set)
    for x in o['derivatives']:
        if isinstance(x['asl'], int): d[strip(x['word'])].add(x['asl'])
    if len({a for v in d.values() for a in v}) >= 2: where[r] = d
def h5(M):
    by = collections.defaultdict(dict)
    for o in M: by[o['root']].setdefault(o['pattern'], strip(o['masdar']))
    pairs = []
    for r, pm in by.items():
        if r not in where: continue
        lab = {p: next(iter(where[r][w])) for p, w in pm.items() if len(where[r].get(w, ())) == 1}
        for a, b in itertools.combinations(sorted(lab), 2): pairs.append((r, a, lab[a], b, lab[b]))
    return pairs
def h5_test(pairs):
    obs = sum(x[2] != x[4] for x in pairs) / len(pairs)
    pool = {r: [a for w, s in where[r].items() if len(s) == 1 for a in s] for r in {p[0] for p in pairs}}
    random.seed(1967); ge = 0; ex = 0
    for _ in range(10000):
        e = sum(a != b for a, b in (random.sample(pool[p[0]], 2) for p in pairs)) / len(pairs); ex += e; ge += e >= obs
    return obs, ex / 10000, (ge + 1) / 10001
res = {}
for name, f in [('القاموس (تأكيد)', 'qamus_masadir.json'), ('الصحاح (استكشاف)', 'sihah_masadir.json'),
                ('المحكم (استكشاف)', 'muhkam_masadir_v2.json'), ('اللسان (استكشاف)', 'lisan_masadir.json')]:
    M = json.load(open(f))
    rows = [(wt(o['root']), o['pattern'] == 'فعول') for o in M if wt(o['root']) in ('أجوف', 'سالم')]
    na = sum(t == 'أجوف' for t, _ in rows); ns = sum(t == 'سالم' for t, _ in rows)
    fa = sum(v for t, v in rows if t == 'أجوف'); fs = sum(v for t, v in rows if t == 'سالم')
    d, p = perm([t == 'أجوف' for t, _ in rows], [v for _, v in rows])
    v4 = 'غير كافٍ' if na < 60 or ns < 200 else ('تُقبل' if d < 0 and p < 0.05 else 'تُردّ')
    pairs = h5(M)
    if len(pairs) >= 100:
        o5, e5, p5 = h5_test(pairs); v5 = 'تُقبل' if o5 > e5 and p5 < 0.05 else 'تُردّ'
    else:
        o5 = e5 = p5 = None; v5 = 'غير كافٍ'
    print(f'== {name}: ثلاثيات {len(M)}')
    print(f'   H4 فُعول: الأجوف {fa}/{na} = {fa/max(na,1):.1%} | السالم {fs}/{ns} = {fs/max(ns,1):.1%} | p={p:.4f} ⇒ {v4}')
    print(f'   H5 أزواج مصادر منسوبة: {len(pairs)}' + (f' | مختلفة القسم {o5:.1%} مقابل متوقَّع {e5:.1%} | p={p5:.4f}' if o5 is not None else '') + f' ⇒ {v5}')
    res[f] = {'h4': [na, fa, ns, fs, p, v4], 'h5': [len(pairs), o5, e5, p5, v5], 'pairs': pairs}
json.dump(res, open('result_h4_h5.json', 'w'), ensure_ascii=False)
