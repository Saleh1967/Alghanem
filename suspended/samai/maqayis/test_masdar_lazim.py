"""تنفيذ التسجيل المسبق PREREG_masdar_lazim.md كما كُتب، دون تعديل."""
import json, re, random, collections
U = {r['root']: r for r in json.load(open('maqayis_usul_table.json'))}
rows = json.load(open('masdar_rows.json'))          # (root, verb, past, bab, T, masdar)
def nm(m):
    m = m.replace('ْ', '')
    return re.sub(r'(?<=[فعل])ا', 'َا', m)
CLASSES = [('داء', r'داء|مرض|وجع|علة|سقم', {'فُعَال'}),
           ('صوت', r'صوت|صياح|صراخ', {'فُعَال', 'فَعِيل'}),
           ('امتناع', r'امتناع|إباء|نفار|شراد', {'فِعَال'}),
           ('اضطراب', r'اضطراب|تقلب|تحرك|حركة', {'فَعَلَان'}),
           ('سير', r'سير|مشي|ذهاب|مضي|سرعة', {'فَعِيل'})]
BASE = {'فُعُول'}
def klass(root):
    e = U.get(root)
    if not e: return None
    h = e['body'][:250]
    for name, rx, _ in CLASSES:
        if re.search(rx, h): return name
    return '—'
PRED = {name: p for name, _, p in CLASSES}; PRED['—'] = BASE
verbs = collections.defaultdict(set); vroot = {}
for r, v, vt, b, T, m in rows:
    verbs[(v, b, T)].add(nm(m)); vroot[(v, b, T)] = r
# ===== H1
L = [(k, s) for k, s in verbs.items() if k[1] in '123' and k[2] == 'ل' and klass(vroot[k]) is not None]
cls = [klass(vroot[k]) for k, _ in L]
sets = [s for _, s in L]
def acc(classes):
    return sum(bool(PRED[c] & s) for c, s in zip(classes, sets))
base = sum(bool(BASE & s) for s in sets)
allm = collections.Counter(m for s in sets for m in s); top, _ = allm.most_common(1)[0]
const = sum(top in s for s in sets)
h1 = acc(cls)
random.seed(1967); ge = 0
for _ in range(10000):
    c2 = cls[:]; random.shuffle(c2)
    ge += acc(c2) >= h1
p1 = (ge + 1) / 10001
n = len(L)
print(f'H1  عيّنة فعَل اللازم (موجودة في المقاييس): {n} فعلًا')
print(f'    توزيع الأصناف: {dict(collections.Counter(cls))}')
print(f'    القاعدة الأساس (فُعول للجميع): {base}/{n} = {base/n:.1%}')
print(f'    الثابت الأغلب ({top}): {const}/{n} = {const/n:.1%}')
print(f'    H1 (فروع المعنى من المقاييس): {h1}/{n} = {h1/n:.1%}   p(تبديل) = {p1:.4f}')
for name in [c[0] for c in CLASSES] + ['—']:
    idx = [i for i, c in enumerate(cls) if c == name]
    if idx:
        hit = sum(bool(PRED[name] & sets[i]) for i in idx)
        dist = collections.Counter(m for i in idx for m in sets[i]).most_common(4)
        print(f'      {name}: {hit}/{len(idx)}  مصادرها: {dict(dist)}')
verdict1 = h1 > base and h1 > const and p1 < 0.05
print('    الحكم:', 'تُقبل H1' if verdict1 else 'تُردّ H1')
# ===== H2
A = [(len(s), U[vroot[k]]['usul']) for k, s in verbs.items() if vroot[k] in U and U[vroot[k]]['usul'] in (1, 2, 3, 4, 5)]
multi = [a for a, u in A if u >= 2]; single = [a for a, u in A if u == 1]
diff = sum(multi)/len(multi) - sum(single)/len(single)
pool = multi + single; random.seed(1967); ge = 0
for _ in range(10000):
    random.shuffle(pool)
    d = sum(pool[:len(multi)])/len(multi) - sum(pool[len(multi):])/len(single)
    ge += d >= diff
p2 = (ge + 1) / 10001
print(f'H2  أفعال المجرّد السالمة ذات عدد أصول مصرَّح: {len(A)}')
print(f'    متوسط المصادر: أصلان فأكثر {sum(multi)/len(multi):.3f} (n={len(multi)}) مقابل أصل واحد {sum(single)/len(single):.3f} (n={len(single)})')
print(f'    الفرق {diff:+.3f}  p(تبديل) = {p2:.4f}  الحكم:', 'تُقبل H2' if diff > 0 and p2 < 0.05 else 'تُردّ H2')
json.dump({'H1': {'n': n, 'base': base, 'const': const, 'h1': h1, 'p': p1, 'accepted': verdict1,
                  'rows': [[vroot[k], k[0], c, sorted(s)] for (k, s), c in zip(L, cls)]},
           'H2': {'multi': len(multi), 'single': len(single), 'diff': diff, 'p': p2}},
          open('result_masdar_lazim.json', 'w'), ensure_ascii=False)
