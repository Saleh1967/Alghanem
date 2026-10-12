"""شاهدٌ ثانٍ للمواد التي لا عدد لأصولها في النسخة الأصل: النصّ نفسه في نسخ المقاييس الأخرى (من مطلع المادّة، لا قبله)."""
import json,re,sys,collections
exec(open('build_usul.py',encoding='utf-8').read().split('raw=open')[0].replace('PRIMARY,SECOND,OUT=sys.argv[1],sys.argv[2],sys.argv[3]',''))
S=sys.argv[1]
only=lambda t: re.sub(r'\s+',' ',re.sub(r'[^ء-ي ]','',t)).strip()
texts={n:only(clean(open(f'{S}/0395IbnFarisQazwini.MucjamMaqayis.{n}-ara1',encoding='utf-8').read())) for n in ['Masaha003703Vols','Shia003913Vols','JK008008']}
T=json.load(open('maqayis_sections.json')); U={o['root']:o for o in json.load(open('maqayis_usul_table.json'))}
out={}
for o in T:
    if not o['usul_witness'].startswith('مستنبط'): continue
    body=only(U[o['root']]['body']); key=body[:30]
    for n,t in texts.items():
        j=t.find(key)
        if j<0: continue
        n2,how=count_usul(t[j:j+len(body)])
        if how=='نصّ' and n2 is not None:
            out[o['root']]={'usul':n2,'witness':f'{n}: «{t[j:j+90]}»'}; break
json.dump(out,open('resolved_770.json','w'),ensure_ascii=False,indent=0)
print('حُسم بشاهد من نسخة أخرى:',len(out),'من',sum(1 for o in T if o['usul_witness'].startswith('مستنبط')))
for r,v in list(out.items())[:8]: print(' ',r,v['usul'],v['witness'][:110])
