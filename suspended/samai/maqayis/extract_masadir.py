"""استخراج ثلاثيات (ماضٍ، مضارع، مصدر) من نصّ المحكم (OpenITI، غير مشكول) بشاهدٍ وموضعه.

النمط المعجميّ عند ابن سيده: «صهل الفرس يصهل ويصهل صهيلا».
- المرشّح: مضارعٌ يبدأ بالياء حروفه بعدها حروف الجذر (مع إبدال حرف العلّة)،
  يسبقه في ≤3 كلمات ماضٍ من الجذر نفسه، ويليه في ≤3 كلمات (بعد «و»+مضارع ثانٍ اختياريًّا)
  مصدرٌ منصوبٌ منوَّن (ينتهي بألف التنوين أو بتاء/همزة منصوبة) فيه حروف الجذر بترتيبها.
- صيغة المصدر غير المشكولة: تُصنَّف بالحروف الزائدة بين حروف الجذر (ي/ا/و/ة/ان).
"""
import re, sys, json, collections, csv

TEXT, ROOTS, OUT = sys.argv[1], sys.argv[2], sys.argv[3]
WEAK = set('اويى')
def norm(s):
    s = re.sub(r'[ً-ْـ]', '', s)
    return s.replace('أ', 'ء').replace('إ', 'ء').replace('آ', 'ءا').replace('ؤ', 'ء').replace('ئ', 'ء').replace('ى', 'ي')

def match_root(stem, root):
    """هل في stem حروف الجذر بترتيبها (حرف العلّة يقابل ا/و/ي أو يسقط)؟ يعيد مواضعها أو None."""
    pos = []; i = 0
    for k, r in enumerate(root):
        j = i; found = False
        while j < len(stem):
            c = stem[j]
            if c == r or (r in 'وي' and c in 'اويء'):
                pos.append(j); i = j + 1; found = True; break
            j += 1
        if not found:
            if r in 'وي': pos.append(None); continue   # سقط حرف العلّة (قال، يقول، يقف) ولا يتحرّك المؤشّر
            return None
    return pos

def masdar_pattern(word, root):
    """صيغة غير مشكولة: يُستبدل بحروف الجذر ف ع ل، وتبقى الزوائد."""
    w = norm(word)
    w = re.sub(r'ا$', '', w) if not w.endswith('اءا') else w[:-1]
    p = match_root(w, root)
    if p is None or None in p: return None
    out = []; ks = {pp: 'فعل'[k] for k, pp in enumerate(p)}
    for i, c in enumerate(w):
        out.append(ks.get(i, c))
    s = ''.join(out)
    if root[1] in 'وي': s = s.replace('فءول', 'فعول').replace('فءل', 'فعل')
    return s if s.startswith('ف') else None

STOP = {'ولا','فلا','وما','فما','ولم','فلم','وقد','فقد','وهو','فهو','وهي','ولو','فلو','وإن','ولن','وكل'}
roots = set()
for r in csv.reader(open(ROOTS, encoding='utf-8'), delimiter='\t'):
    if r and not r[0].startswith('#') and len(r) > 1 and len(norm(r[1])) == 3:
        roots.add(norm(r[1]))
def cand_roots(past):
    if len(past) == 2: return {past + past[1]}
    if len(past) != 3: return set()
    r = {past}
    if past[1] == 'ا': r |= {past[0]+'و'+past[2], past[0]+'ي'+past[2]}
    if past[2] in 'اي': r |= {past[:2]+'و', past[:2]+'ي'}
    return r
text = open(TEXT, encoding='utf-8').read()
toks = [(m.start(), m.group(0)) for m in re.finditer(r'[ء-يً-ْ]+', text)]
N = [norm(t) for _, t in toks]
out = []; seen = set()
for i, w in enumerate(N):
    if not w.startswith('ي') or len(w) < 3: continue
    stem = w[1:]
    # المرشّحون: جذورٌ ماضيها قبل المضارع بكلمة إلى ثلاث
    for j in range(max(0, i - 3), i):
        if N[j] in STOP: continue
        stripped = re.sub(r'^(?:و|ف)', '', N[j])
        # الأولويّة للمجرّد من العاطف؛ والواو أصلًا (وقف) لا تُعتبر إلا إن لم يطابق المجرّدُ جذرًا
        cands = [stripped] if any(r in roots and match_root(stem, r) is not None for r in cand_roots(stripped)) else [N[j]]
        roots_here = set()
        for past in cands: roots_here |= cand_roots(past)
        for root in sorted(roots_here):
            if root not in roots: continue
            if match_root(stem, root) is None: continue
            # المصدر بعد المضارع (تُتخطّى «و»+مضارع ثانٍ)
            k = i + 1
            if k < len(N) and N[k].startswith('وي'): k += 1
            got = 0; kk = k
            while kk < min(k + 6, len(N)) and got < 3:
                m = N[kk]
                if got and not m.startswith('و'): break
                mm = m[1:] if got else m
                if re.search(r'(ا|ءا|ة)$', mm) and not mm.startswith('ي'):
                    pat = masdar_pattern(mm, root)
                    if pat and len(pat) >= 3:
                        key = (root, pat)
                        rec = {'root': root, 'past': N[j], 'impf': w, 'masdar': toks[kk][1], 'pattern': pat, 'order': got,
                               'offset': toks[j][0], 'witness': re.sub(r'\s+', ' ', text[toks[j][0]:toks[kk][0] + len(toks[kk][1]) + 1])}
                        if key not in seen: seen.add(key); out.append(rec)
                        got += 1
                elif not got:
                    pass
                elif got: break
                kk += 1
            break
json.dump(out, open(OUT, 'w'), ensure_ascii=False)
c = collections.Counter(o['pattern'] for o in out)
typ = lambda r: 'معتل' if set(r) & set('وي') else ('مهموز' if 'ء' in r else ('مضعف' if r[1] == r[2] else 'سالم'))
print('ثلاثيات (جذر، صيغة مصدر) فريدة:', len(out), '| جذور:', len({o['root'] for o in out}))
print('بحسب نوع الجذر:', dict(collections.Counter(typ(o['root']) for o in out)))
print('أكثر الصيغ:', c.most_common(15))
