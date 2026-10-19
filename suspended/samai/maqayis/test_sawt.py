"""تنفيذ PREREG_sawt_faeel.md كما كُتب."""
import json, re, random, collections, sys
QAC, BUK, MUS = sys.argv[1:4]
U = {r['root']: r for r in json.load(open('maqayis_usul_table.json'))}
def norm(s):
    s = re.sub(r'[ً-ْـ]', '', s)
    return s.replace('أ','ء').replace('إ','ء').replace('آ','ءا').replace('ؤ','ء').replace('ئ','ء').replace('ى','ي')
SAWT = {norm(r) for r, e in U.items() if re.search(r'صوت|صياح|صراخ', e['body'][:250])}
print('جذور الصوت في المقاييس:', len(SAWT))
def perm_test(groups):          # groups: list of (is_sawt, is_faeel)
    def diff(g):
        a = [f for s, f in g if s]; b = [f for s, f in g if not s]
        return sum(a)/len(a) - sum(b)/len(b), len(a), len(b), sum(a), sum(b)
    d, na, nb, fa, fb = diff(groups)
    lab = [s for s, _ in groups]; val = [f for _, f in groups]
    random.seed(1967); ge = 0
    for _ in range(10000):
        random.shuffle(lab)
        a = [v for s, v in zip(lab, val) if s]; b = [v for s, v in zip(lab, val) if not s]
        ge += (sum(a)/len(a) - sum(b)/len(b)) >= d
    return d, (ge+1)/10001, na, nb, fa, fb
# 1. المحكم
M = json.load(open('muhkam_masadir.json'))
g1 = [(o['root'] in SAWT, o['pattern'] == 'فعيل') for o in M]
d, p, na, nb, fa, fb = perm_test(g1)
print(f'1. المحكم: صوت {fa}/{na} = {fa/na:.1%} | غيرها {fb}/{nb} = {fb/nb:.1%} | الفرق {d:+.3f} p={p:.4f} ⇒',
      'تُقبل' if d > 0 and p < 0.05 else 'تُردّ')
print('   شواهد فعيل من جذور الصوت:', [o['witness'][:40] for o in M if o['root'] in SAWT and o['pattern']=='فعيل'][:8])
print('   مصادر جذور الصوت الأخرى:', collections.Counter(o['pattern'] for o in M if o['root'] in SAWT).most_common(6))
# 2. المصحف
g2 = []; ex = []
for line in open(QAC, encoding='utf-8'):
    loc, form, tag, feat = line.rstrip('\n').split('\t'); f = feat.split('|')
    if tag == 'N' and 'VN' in f and 'VF:1' in f:
        d_ = {x.split(':')[0]: x.split(':', 1)[1] for x in f if ':' in x}
        root = norm(d_.get('ROOT', '')); lem = norm(d_.get('LEM', ''))
        if len(root) != 3: continue
        fae = bool(re.fullmatch(re.escape(root[0]) + re.escape(root[1]) + 'ي' + re.escape(root[2]) + 'ة?', lem))
        g2.append((root in SAWT, fae)); 
        if root in SAWT: ex.append((loc, lem))
na = sum(s for s, _ in g2)
if na >= 5:
    d, p, na, nb, fa, fb = perm_test(g2)
    print(f'2. المصحف (VN|VF:1): صوت {fa}/{na} | غيرها {fb}/{nb} | الفرق {d:+.3f} p={p:.4f} ⇒', 'تُقبل' if d > 0 and p < 0.05 else 'تُردّ')
else:
    print(f'2. المصحف: مصادر جذور الصوت الموسومة {na} (< 5) ⇒ غير كافٍ للحكم. أمثلتها: {ex}')
# 3. الصحيحان (وصفيّ)
import csv; csv.field_size_limit(10**9)
cnt = collections.Counter()
for path in (BUK, MUS):
    for row in csv.reader(open(path, encoding='utf-8')):
        for t in re.findall(r'[ء-يً-ْ]+', row[1]):
            n = re.sub(r'^(?:و|ف|ب|ل)?(?:ال)?', '', norm(t))
            m = re.fullmatch(r'(.)(.)ي(.)', n)
            if m and 'ِي' in t:
                r = ''.join(m.groups()); cnt[(r in SAWT, r)] += 1
s = sum(v for (a, r), v in cnt.items() if a); o_ = sum(v for (a, r), v in cnt.items() if not a)
print(f'3. الصحيحان (وصفيّ): كلمات فَعِيل من جذور الصوت {s}، من غيرها {o_}؛ أكثرها من الصوت:',
      [(r, v) for (a, r), v in cnt.most_common() if a][:10])
json.dump({'sawt_roots': sorted(SAWT), 'muhkam': [[o['root'], o['pattern'], o['root'] in SAWT] for o in M]},
          open('result_sawt.json', 'w'), ensure_ascii=False)
