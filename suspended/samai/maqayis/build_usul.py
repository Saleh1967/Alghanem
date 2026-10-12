"""بناء جدول «جذر ← أصوله» من مقاييس اللغة (OpenITI)، مع شاهد ثانٍ من نسخة أخرى."""
import re,sys,json,collections,hashlib
PRIMARY,SECOND,OUT=sys.argv[1],sys.argv[2],sys.argv[3]
W={'واحد':1,'واحدة':1,'اثنان':2,'ثلاثة':3,'أربعة':4,'خمسة':5,'ستة':6,'سبعة':7}
def clean(s):
    s=re.sub(r'#\s*Page\S+|ms\d+|@\d+@|PageV\d+P\d+','',s)
    s=re.sub(r'\n~~|\n#\s*',' ',s); s=re.sub(r'[|%"]',' ',s)
    s=re.sub(r'[ً-ْ]','',s)
    return re.sub(r'\s+',' ',s).strip()
def count_usul(h):
    h=h[:350]
    m=re.search(r'(ثلاثة|أربعة|خمسة|ستة|سبعة)\s+(?:\S+\s+){0,2}(?:أصول|معان)|(?:أصول|معان)\s+(?:\S+\s+){0,2}(ثلاثة|أربعة|خمسة|ستة|سبعة)',h)
    if m: return W[m.group(1) or m.group(2)],'نصّ'
    if re.search(r'أصلان|أصلين|معنيان|معنيين|كلمتان|كلمتين|بابان|بابين',h): return 2,'نصّ'
    if re.search(r'أصل\s+(?:\S+\s+){0,3}واحد|معنى\s+(?:\S+\s+){0,2}واحد|كلمة\s+(?:\S+\s+){0,2}واحدة|باب\s+(?:\S+\s+){0,2}واحد',h): return 1,'نصّ'
    if re.search(r'ليس (?:بأصل|أصلا)|لا أصل|ليس بشيء|ليس فيه شيء|لا يعول عليه|لا يقاس',h): return 0,'نصّ'
    if re.search(r'(?:يدل|تدل)\s+على',h): return 1,'مستنبط: «يدل على» بلا عدد'
    return None,'لم يُلتقط'
def usul_text(h):
    m=re.search(r'(?:أصول|أصلان|معنيان|أصل[^:]{0,20}واحد|معان)[^:]{0,30}:\s*(.{0,300})',h)
    return m.group(1) if m else ''
raw=open(PRIMARY,encoding='utf-8').read()
parts=re.split(r'\n### \| \(([^)]+)\)\s*\n',raw)
# الشاهد الثاني: نصّ مطبَّع واحد
sec=clean(open(SECOND,encoding='utf-8').read())
only=lambda t: re.sub(r'[^ء-ي ]','',t)
sec_l=re.sub(r'\s+',' ',only(sec))
rows=[];agree=collections.Counter()
for i in range(1,len(parts)-1,2):
    root=re.sub(r'\s','',parts[i]); body=clean(parts[i+1])
    n,how=count_usul(body)
    # البحث عن مطلع المادّة نفسها في الشاهد الثاني
    key=re.sub(r'\s+',' ',only(body)).strip()[:40]
    j=sec_l.find(key) if len(key)>=25 else -1
    L=len(re.sub(r'\s+',' ',only(body)).strip())
    n1=count_usul(re.sub(r'\s+',' ',only(body)).strip())[0]
    n2=count_usul(sec_l[j:j+L])[0] if j>=0 else None
    status='لم يوجد في الشاهد' if j<0 else ('متّفق' if n2==n1 else 'مختلف')
    agree[status]+=1
    rows.append({'root':root,'usul':n,'how':how,'usul_text':usul_text(body),'witness2':status,'body':body})
json.dump(rows,open(OUT,'w'),ensure_ascii=False)
print('مواد:',len(rows))
print('عدد الأصول:',dict(collections.Counter(r['usul'] for r in rows).most_common()))
print('طريقة الاستخراج:',dict(collections.Counter(r['how'] for r in rows).most_common()))
print('الشاهد الثاني:',dict(agree))
print('sha256 الجدول:',hashlib.sha256(open(OUT,'rb').read()).hexdigest()[:16])
