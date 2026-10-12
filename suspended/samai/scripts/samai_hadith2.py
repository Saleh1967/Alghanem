import sys, re, csv, collections, json
csv.field_size_limit(10**9)
# لاحقة الأمر: المفرد (ساكن/مكسور للوصل) والجمع والمؤنث والمثنى، ثم ضمير مفعول اختياري
END = r'(?:ْ|ِ|ُوا|ُو|ِي|َا)'
OBJ = r'(?:هُ|هِ|هَا|هُمْ|هُمَا|هُنَّ|نَا|نِي|كَ|كِ)?'
def rx(stem): return re.compile(r'^(?P<pre>[وف]َ)?(?:' + stem + r')' + r'(?:' + END + OBJ + r'|ْ' + OBJ + r')$')
pats = {
 ('أمر','محذوفة'): rx('مُر'),
 ('أمر','ثابتة'):  rx('(?:[اٱ]ُ?ؤْ|أُو|أْ)مُر'),
 ('أخذ','محذوفة'): rx('خُذ'),
 ('أخذ','ثابتة'):  rx('(?:[اٱ]ُ?ؤْ|أُو|أْ)خُذ'),
 ('أكل','محذوفة'): rx('كُل'),
 ('أكل','ثابتة'):  rx('(?:[اٱ]ُ?ؤْ|أُو|أْ)كُل'),
 ('أمل','محذوفة'): rx('مُل'),
 ('أمل','ثابتة'):  rx('(?:[اٱ]ُ?ؤْ|أُو|أْ)مُل'),
}
T=collections.Counter(); EX=collections.defaultdict(list); FORMS=collections.Counter()
for path in sys.argv[1:]:
    book = 'B' if 'bukhari' in path else 'M'
    for row in csv.reader(open(path,encoding='utf-8')):
        toks = [t for t in re.split(r'[\s‏‎,.:;!?()«»"{}\[\]،؛؟\-]+', row[1]) if t]
        for j,t in enumerate(toks):
            for (root,st),r in pats.items():
                m = r.match(t)
                if m:
                    ctx = 'وصل(بعد و/ف)' if m.group('pre') else 'ابتداء الكلمة'
                    T[(root,ctx,st)] += 1; FORMS[(root,ctx,st,t)] += 1
                    EX[(root,ctx,st)].append(f"{book}{row[0]}: {' '.join(toks[max(0,j-3):j+3])}")
for k in sorted(T): print(*k, T[k], sep=' | ')
print('-- الصور:')
for k,v in sorted(FORMS.items(), key=lambda x:(x[0][:3],-x[1])): print(' ', *k, v)
json.dump({' | '.join(k): v for k,v in EX.items()}, open('samai_examples2.json','w'), ensure_ascii=False, indent=1)
