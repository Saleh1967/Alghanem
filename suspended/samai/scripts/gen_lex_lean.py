import csv,re,json,sys,collections,hashlib
exec(open('lex_samai.py').read().split('rd=lambda')[0])
rd=lambda p: [r for r in csv.reader(open(p,encoding='utf-8'),delimiter='\t') if r and not r[0].startswith('#')]
D='lex/arramooz/data'
# تفعيل/تفعلة
tf=[]
for r in rd(D+'/nouns/masdar.csv'):
    if len(r)<12 or r[5].strip()!='مصدر' or r[11].strip()!='مفرد': continue
    root=r[3].strip(); w=strip(waqf(r[1]))
    if len(root)!=3 or not w.startswith('ت'): continue
    r1,r2,r3=root
    if r1 in 'وياءأت' or r2 in 'ويا': continue
    typ='naqis' if r3 in 'وي' else ('mahmuz' if r3 in 'ءأ' else 'salim')
    R3='ي' if typ=='naqis' else r3
    if typ=='mahmuz':
        k='tafil' if re.fullmatch('ت'+r1+r2+'ي[ءئ]',w) else ('tafila' if re.fullmatch('ت'+r1+r2+'[ئء]ة',w) else None)
    else:
        k='tafil' if w=='ت'+r1+r2+'ي'+R3 else ('tafila' if w=='ت'+r1+r2+R3+'ة' else None)
    if k: tf.append((r[1].strip(),typ,k))
tf=sorted(set(tf))
pairs=json.load(open('lex_plural_pairs.json'))
def bare(t): return re.sub('[َُِّ]','',t)
src=open('lex_plural_pairs.json','rb').read()
dom=[x for x in pairs if re.fullmatch(r'([مأت]فع[اوي]?ل|فاعلة|فع[اوي]لة)',bare(x[1]))]
g=[x for x in pairs if x[1] in ('فُعلَة','فِعلَة')]
q=lambda s: '"'+s.replace('"','')+'"'
L=[]
L.append('def tafRows : List (String × RootType × MasdarII) := [')
L.append(',\n'.join(f'  ({q(w)}, .{t}, .{k})' for w,t,k in tf)+']')
L.append('def fRows : List (String × String × String) := [')
L.append(',\n'.join(f'  ({q(r)}, {q(a)}, {q(b)})' for r,a,b in dom)+']')
L.append('def gRows : List (String × String × String) := [')
L.append(',\n'.join(f'  ({q(r)}, {q(a)}, {q(b)})' for r,a,b in g)+']')
open('lex_tables.inc','w').write('\n'.join(L))
c=collections.Counter((t,k) for _,t,k in tf)
print(len(tf),dict(c),len(dom),len(g),'sha:',hashlib.sha256(src).hexdigest()[:16])
