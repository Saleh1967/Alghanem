"""تقسيم كلّ مادّة من المقاييس إلى أقسام أصولها، ونسبة كلّ مشتقّ إلى قسمه، بشاهدٍ نصّيّ وموضعه.

المدخل: maqayis_usul_table.json (من build_usul.py).
المخرج: maqayis_sections.json — لكلّ مادّة: عدد الأصول المحسوم وشاهده، والأقسام بنصّها،
وقائمة المشتقّات (كلمة، قسم، موضع، شاهد، طريقة النسبة).
"""
import json, re, collections, sys

ORD = {'الأول': 1, 'الثاني': 2, 'الثالث': 3, 'الرابع': 4, 'الخامس': 5}
# علامات بدء القسم (بعد صدر المادّة)
START = re.compile(
    r'(?:^|(?<=[\s.،:;]))(?:ف|و)(?:أما\s+)?(?:الأصل\s+|الباب\s+)?'
    r'(الأول|الثاني|الثالث|الرابع|الخامس|الآخر)(?=[\s،:.])')
# نسبة صريحة داخل الجملة: «فمن الباب الأول»، «من باب التغير»
EXPL_ORD = re.compile(r'من\s+(?:ال)?باب\s+(?:ال)?(الأول|الثاني|الثالث|الرابع|الآخر)')
EXPL_NAME = re.compile(r'من\s+باب\s+([^.،:;]+)')
SHADH = re.compile(r'(?:ومن|ومما)\s+(?:ال)?شا?ذ')

def letters(root):
    return [c for c in root]

def is_derivative(tok, root):
    t = re.sub(r'^(?:و|ف|ب|ل|ك)?(?:ال)?', '', tok)
    t = re.sub(r'[^ء-ي]', '', t)
    if len(t) < len(root): return False
    # حروف الجذر بترتيبها، مع إبدال الهمزة وحروف العلّة
    norm = lambda c: {'أ': 'ء', 'إ': 'ء', 'آ': 'ء', 'ؤ': 'ء', 'ئ': 'ء', 'ى': 'ي'}.get(c, c)
    tt = [norm(c) for c in t]; rr = [norm(c) for c in root]
    i = 0
    for c in tt:
        if i < len(rr) and (c == rr[i] or (rr[i] in 'وي' and c in 'اوي')):
            i += 1
    return i == len(rr)

def resolve_count(e, ords_seen):
    """يحسم عدد الأصول: النصّ المصرَّح أوّلًا، ثمّ علامات الأقسام شاهدًا."""
    if e['how'] == 'نصّ':
        return e['usul'], 'نصّ مصرَّح في صدر المادّة'
    if ords_seen:
        m = max(ords_seen)
        return m, f'علامات الأقسام في المادّة (أعلاها: {m})'
    if e['usul'] == 0:
        return 0, 'نصّ: ليس بأصل'
    if e['how'].startswith('مستنبط'):
        return 1, 'نصّ: «يدل على» بمعنى واحد مسمّى'
    return 1, 'مستنبط: لا عدد مصرَّح ولا علامة قسمة (غيابُ شاهدٍ لا شاهد)'

def segment(e):
    body = e['body']; root = e['root']
    # صدر المادّة ينتهي عند أوّل «فالأول»/«فأما الأول»/... إن وُجد، وإلّا عند أوّل نقطة
    first = None
    for m in START.finditer(body):
        if m.group(1) == 'الأول' and m.start() > 15:
            first = m; break
    head_end = first.start() if first else (body.find('.') + 1 or len(body))
    head = body[:head_end]
    # أوصاف الأصول من الصدر: «أحدها …، والثاني …، والثالث …»
    desc = {}
    hm = re.split(r'(?:أحدهما|أحدها|والثاني|والآخر|والثالث|والرابع|والخامس)\s*', head)
    labels = re.findall(r'(أحدهما|أحدها|والثاني|والآخر|والثالث|والرابع|والخامس)', head)
    for lab, txt in zip(labels, hm[1:]):
        k = {'أحدهما': 1, 'أحدها': 1, 'والثاني': 2, 'والآخر': 2, 'والثالث': 3, 'والرابع': 4, 'والخامس': 5}[lab]
        desc[k] = re.split(r'[،.]', txt)[0].strip()
    # الأقسام
    cuts = []; ords_seen = set(); cur_max = 0
    for m in START.finditer(body, head_end):
        w = m.group(1)
        k = ORD.get(w) or (cur_max + 1 if cur_max >= 1 else 2)
        if w == 'الآخر' and cur_max == 0: k = 2
        cuts.append((m.start(), k, m.group(0).strip())); ords_seen.add(k); cur_max = max(cur_max, k)
    for m in SHADH.finditer(body, head_end):
        cuts.append((m.start(), 'شاذ', m.group(0).strip()))
    cuts.sort(key=lambda x: x[0])
    n, how = resolve_count(e, ords_seen if first or len(ords_seen) > 1 else set())
    sections = []
    start, k, mark = head_end, (1 if n and n >= 1 else 0), 'صدر/بلا علامة'
    for pos, kk, mk in cuts + [(len(body), None, None)]:
        if pos > start:
            sections.append({'asl': k, 'marker': mark, 'start': start, 'text': body[start:pos]})
        if kk is not None: start, k, mark = pos, kk, mk
    # المشتقّات: كلّ كلمة فيها حروف الجذر بترتيبها، تُنسب إلى قسمها؛ والنسبة الصريحة تتقدّم
    derivs = []
    for sec in sections:
        for sent_m in re.finditer(r'[^.]+\.?', sec['text']):
            sent = sent_m.group(0); off = sec['start'] + sent_m.start()
            asl, method = sec['asl'], f'قسم: {sec["marker"]}'
            eo = EXPL_ORD.search(sent); en = EXPL_NAME.search(sent)
            if eo:
                w = eo.group(1); asl = ORD.get(w, 2); method = f'نسبة صريحة: «{eo.group(0)}»'
            elif en:
                words = {re.sub(r'^و?ال', '', w) for w in re.findall(r'[ء-ي]+', en.group(1)) if len(w) >= 3}
                for kk, d in desc.items():
                    dw = {re.sub(r'^و?ال', '', w) for w in re.findall(r'[ء-ي]+', d)}
                    if words & dw:
                        asl = kk; method = f'نسبة صريحة باسم الأصل: «{en.group(0)[:40]}»'; break
            if re.search(r'\{[^}]*\}', sent): pass
            for tm in re.finditer(r'[ء-ي]+', sent):
                tok = tm.group(0)
                if tok in ('الخاء', 'واللام', 'والفاء') or len(tok) < 3: continue
                if is_derivative(tok, root):
                    derivs.append({'word': tok, 'asl': asl, 'offset': off + tm.start(),
                                   'witness': sent.strip()[:160], 'method': method})
    return {'root': root, 'usul': n, 'usul_witness': how, 'usul_desc': desc,
            'head': head[:300], 'sections': [{k: v for k, v in s.items() if k != 'text'} | {'text': s['text'][:400]} for s in sections],
            'derivatives': derivs}

if __name__ == '__main__':
    T = json.load(open(sys.argv[1]))
    out = [segment(e) for e in T]
    json.dump(out, open(sys.argv[2], 'w'), ensure_ascii=False)
    c = collections.Counter(o['usul_witness'].split(':')[0].split(' (')[0] for o in out)
    print('مواد:', len(out))
    print('حسم عدد الأصول بحسب الشاهد:', dict(c.most_common()))
    print('توزيع العدد:', dict(collections.Counter(o['usul'] for o in out).most_common()))
    multi = [o for o in out if (o['usul'] or 0) >= 2]
    sec_ok = sum(1 for o in multi if len({s['asl'] for s in o['sections'] if isinstance(s['asl'], int)}) >= 2)
    print(f'مواد متعدّدة الأصول: {len(multi)}؛ قُسِّمت إلى قسمين فأكثر: {sec_ok}')
    print('مشتقّات منسوبة:', sum(len(o['derivatives']) for o in out))
