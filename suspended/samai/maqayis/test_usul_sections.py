"""تنفيذ PREREG_masdar_usul_sections.md."""
import json, re, csv, random, collections, sys, itertools
MASDAR = sys.argv[1]
def norm(s):
    s = re.sub(r'[ً-ْـ]', '', s)
    return s.replace('أ','ء').replace('إ','ء').replace('آ','ءا').replace('ؤ','ء').replace('ئ','ء').replace('ى','ي')
strip = lambda w: re.sub(r'^(?:و|ف|ب|ل|ك)?(?:ال)?', '', norm(w)).rstrip('ا') if not norm(w).endswith('اء') else re.sub(r'^(?:و|ف)?(?:ال)?', '', norm(w))
S = {norm(o['root']): o for o in json.load(open('maqayis_sections.json'))}
# مواضع الكلمات في الأقسام المرقّمة
where = {}
for r, o in S.items():
    d = collections.defaultdict(set)
    for x in o['derivatives']:
        if isinstance(x['asl'], int): d[strip(x['word'])].add(x['asl'])
    if len({a for v in d.values() for a in v}) >= 2: where[r] = d
verbs = collections.defaultdict(set)
for row in csv.reader(open(MASDAR, encoding='utf-8'), delimiter='\t'):
    if len(row) < 12 or row[0].startswith('#') or row[5].strip() != 'مصدر' or row[11].strip() != 'مفرد': continue
    r = norm(row[3].strip())
    if r in where: verbs[(r, row[6].strip())].add(strip(row[1].strip()))
pairs = []; wit = []
for (r, v), ms in verbs.items():
    lab = {m: next(iter(where[r][m])) for m in ms if len(where[r].get(m, ())) == 1}
    for a, b in itertools.combinations(sorted(lab), 2):
        pairs.append((r, lab[a], lab[b])); wit.append((r, v, a, lab[a], b, lab[b]))
obs = sum(a != b for _, a, b in pairs) / len(pairs)
# التبديل: أقسام الكلمات المنسوبة داخل الجذر
pool = {r: [a for m, s in where[r].items() if len(s) == 1 for a in s] for r in {p[0] for p in pairs}}
random.seed(1967); ge = 0; exp_acc = 0
for _ in range(10000):
    diff = 0
    for r, _, _ in pairs:
        a, b = random.sample(pool[r], 2); diff += a != b
    e = diff / len(pairs); exp_acc += e; ge += e >= obs
p = (ge + 1) / 10001
print(f'أزواج مصادر لفعلٍ واحد، منسوبٌ كلٌّ منها إلى قسمٍ واحد: {len(pairs)} (جذور: {len({x[0] for x in pairs})})')
print(f'في قسمين مختلفين: مشاهَد {obs:.1%}، متوقَّع {exp_acc/10000:.1%}، p = {p:.4f} ⇒',
      'تُقبل' if obs > exp_acc/10000 and p < 0.05 else 'تُردّ')
print('شواهد (جذر، فعل، مصدر١/قسمه، مصدر٢/قسمه):'); [print('  ', w) for w in wit[:12]]
json.dump({'pairs': pairs, 'witness': wit, 'obs': obs, 'expected': exp_acc/10000, 'p': p}, open('result_usul_sections.json', 'w'), ensure_ascii=False)
