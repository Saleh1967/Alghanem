import json,re
pairs=json.load(open('plural_pairs_clean.json'))
def esc(s): return s.replace('"','\\"')
rows=',\n    '.join(f'("{esc(r)}", "{esc(a)}", "{esc(b)}")' for r,a,b in pairs)
open('plural_table.lean.inc','w').write(rows)
print(len(pairs))
