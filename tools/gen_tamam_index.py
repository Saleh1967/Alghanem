"""فهرسُ قانون التمام (TAMAM_INDEX.md): الصدارةُ والإغلاقُ والوصلُ على آيات المصحف موقعًا موقعًا.

القانونُ `slge.tamam` (مرآةُ `Slge.Tamam`) على كلمات كلّ آيةٍ من مودَع المصحف
(`corpus-certificates.json.gz`
مقطوعًا بأطوال الآيات من `context-certificates.json.gz`). الكلمةُ قراءاتٌ، وكلُّ قراءةٍ سلسلةُ أقسام:
- المغلق (`mughlaq.closed`): السوابقُ حروفًا بأبوابها من الجدول الموحَّد، ثمّ النواةُ ببابها
(`gen_haja_index.babs_of`
  قاعدةً: `haja.core_babs`)، ثمّ اللاحقةُ ضميرًا؛ وإن كانت النواةُ ذاتَ صدارة سقط الجارُّ قبلها في الكلمة
  (`JARR_INSIDE_SADR_WORD`:
  بِمَ، عَمَّ — `Istifham.ma_after_jarr`).
- المفتوح (`jidh`): السوابقُ حروفًا، ثمّ الجذعُ فعلًا أو اسمًا بقالبه، ثمّ اللاحقةُ ضميرًا.
- وما لا قراءةَ له اسمٌ مستقلّ.
سياستان: **ابتداءً** (كلُّ آيةٍ من أوّل الوحدة) و**وصلًا** (الآيةُ من حالات ما قبلها في سورتها؛ والسورةُ من
أوّل الآية
الأولى بموضعها في QAC). مفحوصٌ لا مقيس: لا مرجعَ محجوبًا للتمام.
"""

from __future__ import annotations

import gzip
import json
import sys
from collections import Counter
from pathlib import Path
from typing import Any

from slge import haja as H
from slge import tamam as T
from slge.huruf import TABLE as HURUF
from slge.jidh import jidh
from slge.mughlaq import closed
from slge.wujud import FIL, ont_of_reading

ROOT = Path(__file__).resolve().parent.parent
TARGET = ROOT / "TAMAM_INDEX.md"
DATA = ROOT / "tests" / "data"
Word = tuple[tuple[str, str], ...]
Seq = tuple[T.Tok, ...]

DAMIR: T.Tok = ("mudmar", "damir")
CAP = 2000
"""حدُّ الحالات في الآية الواحدة: ما زاد يُعدّ `STATES_CAPPED` ولا يُحذف منه شيءٌ بصمت."""

_IDX: dict[Word, list[int]] = {}
for _i, _h in enumerate(HURUF):
    _IDX.setdefault(_h.cells, []).append(_i)


def _harf_toks(p: Word) -> list[T.Tok]:
    out: list[T.Tok] = []
    for i in _IDX.get(p, []):
        t = ("harf", H.bab_of(i))
        if H.bab_of(i) in H.HARF_BABS and t not in out:
            out.append(t)
    return out or [("harf", "ghayrMusnad")]


def _head_toks(core: Word) -> list[T.Tok]:
    out: list[T.Tok] = []
    for b in H.core_babs(core):
        t = (H.mufrad_of(b, False) if b != "ghayrMusnad" else "ism", b)
        if t not in out:
            out.append(t)
    return out


def _expand(parts: list[list[T.Tok]]) -> list[Seq]:
    seqs: list[Seq] = [()]
    for alts in parts:
        seqs = [(*s, a) for s in seqs for a in alts]
    return seqs


def readings(w: Word) -> list[Seq]:
    out: list[Seq] = []
    for m in closed(w):
        heads = _head_toks(m.core)
        for h in heads:
            pre = [] if h[1] in H.SADR else [_harf_toks(p) for p in m.pre]
            suf = [[DAMIR]] if m.suf else []
            out += _expand([*pre, [h], *suf])
    if not out:
        for rd in jidh(w):
            leaf = "fil" if ont_of_reading(rd) == FIL else "ism"
            pre = [_harf_toks(p) for p in rd.pre]
            suf = [[DAMIR]] if rd.suf else []
            out += _expand([*pre, [(leaf, "mustaqill")], *suf])
    if not out:
        out = [(("ism", "mustaqill"),)]
    return list(dict.fromkeys(out))


def step_word(states: list[T.St], seqs: list[Seq]) -> list[T.St]:
    nxt: list[T.St] = []
    for seq in seqs:
        nxt += T.run_all(states, [[t] for t in seq])
    return list(dict.fromkeys(nxt))


def _load() -> tuple[list[Word], list[int], list[int], dict[int, str]]:
    with gzip.open(DATA / "corpus-certificates.json.gz", "rt", encoding="utf-8") as f:
        d: dict[str, Any] = json.load(f)
    with gzip.open(DATA / "context-certificates.json.gz", "rt", encoding="utf-8") as f:
        lengths: list[int] = json.load(f)["line_lengths"]
    loc: dict[int, str] = {}
    with gzip.open(DATA / "qac-pos.tsv.gz", "rt", encoding="utf-8") as f:
        for i, row in enumerate(f):
            if i:
                tok, lc, *_ = row.split("\t")
                loc[int(tok)] = lc
    forms = [tuple((a, b) for a, b in x["cells"]) for x in d["forms"]]
    return forms, list(d["stream"]), lengths, loc


def measure() -> dict[str, Any]:
    forms, stream, lengths, loc = _load()
    cache: dict[int, list[Seq]] = {}
    lines_n = len(lengths)
    ibtida_tamm = wasl_tamm = capped = 0
    dead: Counter[str] = Counter()
    dead_wasl = 0
    surah_starts = 0
    pos = 0
    prev: list[T.St] = [T.START]
    for n in lengths:
        idxs = stream[pos:pos + n]
        first = next((loc[k] for k in range(pos, pos + n) if k in loc), "")
        if first.split(":")[1:2] == ["1"] or not prev:
            prev = [T.START]
            surah_starts += first.split(":")[1:2] == ["1"]
        pos += n
        s_i: list[T.St] = [T.START]
        s_w: list[T.St] = prev
        died_at = ""
        hit_cap = False
        for i in idxs:
            if i not in cache:
                cache[i] = readings(forms[i])
            seqs = cache[i]
            if s_i:
                s_i = step_word(s_i, seqs)
                if not s_i:
                    died_at = "+".join(sorted({q[0][1] for q in seqs}))
                elif len(s_i) > CAP:
                    s_i = s_i[:CAP]
                    hit_cap = True
            if s_w:
                s_w = step_word(s_w, seqs)
                if len(s_w) > CAP:
                    s_w = s_w[:CAP]
                    hit_cap = True
        capped += hit_cap
        ibtida_tamm += T.tamm(s_i)
        wasl_tamm += T.tamm(s_w)
        if not s_i:
            dead[died_at] += 1
        dead_wasl += not s_w
        prev = s_w
    return {"lines": lines_n, "surah_starts": surah_starts, "ibtida_tamm": ibtida_tamm,
            "wasl_tamm": wasl_tamm, "ibtida_dead": sum(dead.values()), "wasl_dead": dead_wasl,
            "dead_by_bab": dict(dead.most_common()), "capped": capped}


BAB_AR = {"mustaqill": "مستقلّ", "jarr": "جرّ", "mushabbaha": "مشبّهة", "atf": "عطف",
          "istithna": "استثناء", "shart": "شرط", "nafy": "نفي", "amilFil": "داخلٌ على الفعل",
          "tanbih": "تنبيه", "jawab": "جواب", "rad": "ردع", "istifham": "استفهام", "nida": "نداء",
          "damir": "ضمير", "mawsul": "موصول", "ghayrMusnad": "بلا سند"}


def _pct(a: int, b: int) -> str:
    return f"{100 * a / b:.2f}٪" if b else "—"


def render(m: dict[str, Any]) -> str:
    n = m["lines"]
    out = ["# فهرسُ قانون التمام — الصدارةُ والإغلاقُ والوصل على آيات المصحف", "",
           "مولَّدٌ بـ`python tools/gen_tamam_index.py` من `src/slge/tamam.py` (مرآةُ"
           " `formal/Slge/Tamam.lean`، ADR ٥٧)؛ "
           "لا يُحرَّر باليد. المبرهَن: الوصلُ وراثة (`runAll_append`، `before_after`)، والحدُّ الأدنى"
           " المكتمل كلمةٌ بلا "
           "حاجةٍ قبلُ أو بعدُ (`minimal_complete`)، والحرفُ وحده لا يتمّ (`harf_alone_incomplete`)، وذو"
           " الصدارة "
           "لا يقع وما قبله مفتوح ولا يرى ما قبله (`sadr_needs_closed`، `sadr_forgets`).", "",
           "## على آيات المصحف (مفحوصٌ لا مقيس)", "",
           f"{n:,} آيةً، منها {m['surah_starts']:,} أوّلُ سورةٍ بموضعه في QAC.", "",
           "| السياسة | تامّة (مكدَّسٌ فارغ) | لا طريقَ لها |", "|---|---|---|",
           f"| ابتداءً (كلُّ آيةٍ وحدَها) | {m['ibtida_tamm']:,} ({_pct(m['ibtida_tamm'], n)}) | "
           f"{m['ibtida_dead']:,} ({_pct(m['ibtida_dead'], n)}) |",
           f"| وصلًا (من حالات ما قبلها في سورتها) | {m['wasl_tamm']:,} ({_pct(m['wasl_tamm'], n)})"
           f" | "
           f"{m['wasl_dead']:,} ({_pct(m['wasl_dead'], n)}) |", "",
           "«تامّة» = طريقٌ واحدٌ على الأقلّ يقضي كلَّ حاجةٍ مفتوحة؛ و«لا طريقَ لها» = كلمةٌ لم يبقَ بعدها"
           " طريق. "
           "والآيةُ غيرُ التامّة ولها طريقٌ مفتوحٌ تتمّ بما بعدها أو لا: الآيةُ ليست جملةً "
           "بالضرورة. والفرقُ بين السياستين هو الوصلُ نفسُه: ما يُفتتح بحاجةٍ «قبل» (العطف، "
           "الاستثناء، الردع، الجواب) "
           "يموت ابتداءً ويحيا بحالات ما قبله.", "",
           "### أين انقطع الطريقُ ابتداءً — بابُ رأس الكلمة", "", "| الباب | الآيات |", "|---|---|"]
    for k, v in m["dead_by_bab"].items():
        out.append(f"| {' / '.join(BAB_AR.get(b, b) for b in k.split('+'))} | {v:,} |")
    out += ["", f"آياتٌ بلغت حالاتُها الحدَّ ({CAP:,}) فقُطع ما زاد بترتيبه (`STATES_CAPPED`): "
            f"{m['capped']:,} — "
            "وفيها «تامّة» حدٌّ أدنى و«لا طريقَ لها» حدٌّ أعلى، إذ القطعُ يُسقط طرقًا ولا يزيدها.", "",
            "## ما ليس هنا — باسمه", "",
            "- `AYY_NEEDS_NOT_ENFORCED`: المفسِّرُ والمتعلَّقُ والمشروطُ لا يُلزمها القانون — تُقضى قبلُ أو"
            " بعدُ أو بمقدَّر.",
            "- `ITTISAL_NOT_ENFORCED`: الاتّصالُ المنصوص (الاستثناء والشرط) قيدٌ على الكلام لا على"
            " الكلمة؛ لم يُكتب هنا.",
            "- `JARR_INSIDE_SADR_WORD`: الجارُّ داخلَ كلمة الاستفهام (بِمَ، عَمَّ) يسقط قبل الصدارة.",
            "- `TAMM_NOT_MEASURED`: لا مرجعَ محجوبًا لتمام الكلام؛ فالأرقامُ فحصٌ للتوقيع والقرّاء معًا"
            " لا قياس.", ""]
    return "\n".join(out)


def main(argv: list[str]) -> int:
    text = render(measure())
    if "--check" in argv:
        ok = TARGET.read_text(encoding="utf-8") == text
        sys.stdout.write("TAMAM_INDEX.md مطابق\n" if ok else "TAMAM_INDEX.md غيرُ مطابق\n")
        return 0 if ok else 1
    TARGET.write_text(text, encoding="utf-8")
    sys.stdout.write("كُتب TAMAM_INDEX.md\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
