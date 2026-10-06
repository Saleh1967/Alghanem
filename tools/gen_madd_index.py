"""فهرسُ المدود على درجات الترخيص التدريجيّ (MADD_INDEX.md) من `slge.madd` ومودَع شهادات المصحف.

القياسُ على `tests/data/corpus-certificates.json.gz` (شهاداتُ المدوّنة المختومة خاناتٍ، بترتيب المصحف):
أحكامُ كلّ حرف مدٍّ وصلًا (التاليةُ قرينةُ المنفصل والصلة)، وما يصير عارضًا أو لينًا وقفًا؛ واللازمُ يُقابَل
بالصور الثلاثيّة فقط. والصلةُ تُقاس على `masaq-shibh.json.gz`: وسمُ اللاحقة (PRON_3MS…) قرينةٌ تفصل هاءَ
الكناية من هاء الكلمة (اللَّه).
"""

from __future__ import annotations

import gzip
import json
import sys
from collections import Counter
from pathlib import Path
from typing import Any

from slge.cells import licensed
from slge.madd import continue_licensed, has_vc, kinds, madd

ROOT = Path(__file__).resolve().parent.parent
TARGET = ROOT / "MADD_INDEX.md"
DATA = ROOT / "tests" / "data"
Word = tuple[tuple[str, str], ...]
PRON_H = ("PRON_3MS", "POSS_PRON_3MS", "PVSUFF_DO:3MS", "IVSUFF_DO:3MS", "POSS_PRON", "OBJ_PRON")
KINDS = ("طبيعيّ", "متّصل", "منفصل", "لازم مثقَّل", "لازم مخفَّف", "صلة صغرى", "صلة كبرى", "محجوب")


def corpus() -> tuple[list[Word], list[int]]:
    with gzip.open(DATA / "corpus-certificates.json.gz", "rt", encoding="utf-8") as f:
        d: dict[str, Any] = json.load(f)
    forms = [tuple((a, b) for a, b in x["cells"]) for x in d["forms"]]
    return forms, list(d["stream"])


def masaq_words() -> list[tuple[Word, tuple[str, ...]]]:
    with gzip.open(DATA / "masaq-shibh.json.gz", "rt", encoding="utf-8") as f:
        rows: list[dict[str, Any]] = json.load(f)["rows"]
    out = []
    for r in rows:
        w: Word = (*((a, b) for _, cs in r["pre"] for a, b in cs), *((a, b) for a, b in r["stem"]),
                   *((a, b) for _, cs in r["suf"] for a, b in cs))
        out.append((w, tuple(t for t, _ in r["suf"])))
    return out


def measure() -> dict[str, object]:
    forms, stream = corpus()
    wasl: Counter[str] = Counter()
    waqf: Counter[str] = Counter()
    letters = 0
    for pos, i in enumerate(stream):
        if i < 0:
            continue
        w = forms[i]
        nxt_i = stream[pos + 1] if pos + 1 < len(stream) else -1
        nxt: Word = forms[nxt_i] if nxt_i >= 0 else ()
        for _, k in madd(w, nxt, False):
            wasl[k] += 1
        for _, k in madd(w, (), True):
            if k in ("عارض", "لين"):
                waqf[k] += 1
        letters += kinds(w).count("v")
    tern_only = [w for w in forms if not licensed(w)]
    lazim_forms = [w for w in forms if has_vc(w)]
    cont = sum(continue_licensed(w) for w in forms)
    sila_total = sila_pron = 0
    for w, suf in masaq_words():
        hits = [k for _, k in madd(w, (("ك", "فتح"),), False) if k.startswith("صلة")]
        if hits:
            sila_total += 1
            sila_pron += any(t in PRON_H for t in suf)
    return {"forms": len(forms), "tokens": sum(i >= 0 for i in stream), "letters": letters,
            "wasl": wasl, "waqf": waqf, "ternary_only": len(tern_only),
            "ternary_only_all_lazim": all(has_vc(w) for w in tern_only),
            "lazim_forms": len(lazim_forms),
            "lazim_all_ternary_only": all(not licensed(w) for w in lazim_forms),
            "continue_licensed": cont, "sila_total": sila_total, "sila_pron": sila_pron}


def render() -> str:
    m = measure()
    wasl: Counter[str] = m["wasl"]  # type: ignore[assignment]
    waqf: Counter[str] = m["waqf"]  # type: ignore[assignment]
    sila_total: int = m["sila_total"]  # type: ignore[assignment]
    sila_pron: int = m["sila_pron"]  # type: ignore[assignment]
    lines = [
        "# فهرسُ المدود على درجات الترخيص التدريجيّ",
        "",
        "مولَّدٌ بـ`python tools/gen_madd_index.py` من `src/slge/madd.py`؛ لا يُحرَّر باليد. "
        "البرهانُ: "
        "`formal/Slge/Madd.lean`.",
        "",
        "## د٣ الخانة — حرفُ المدّ", "",
        "حرفُ المدّ خانةٌ ساكنةٌ بعد حركتها: ألفٌ بعد فتحٍ، واوٌ بعد ضمٍّ، ياءٌ بعد كسر — وهو "
        "الصنفُ `v` في "
        "التقطيع الثلاثيّ (`kinds`: مرآةُ `gate.licence.kind_of` على الخانات، مطابَقةٌ بجدول "
        "`madd.csv`). "
        "لا مدَّ في صدر كلمةٍ (`kinds_head_not_v`) ولا مدّان متجاوران (`no_adjacent_madd`) — "
        "لكلّ كلمة.",
        "",
        "## د٤ الترخيص — اللازمُ فاصلُ الثلاثيّ عن الثنائيّ", "",
        "الترخيصُ الثنائيُّ هو `binOK` على الأصناف لكلّ كلمة (`licensed_eq_binOK`)؛ وفي كلمةٍ "
        "مرخَّصةٍ وصلًا "
        "(ثلاثيًّا) مدٌّ لازمٌ — مدٌّ ثمّ ساكنٌ — ⇔ ليست مرخَّصةً ثنائيًّا "
        "(`lazim_iff_not_binary`، لكلّ كلمة). "
        f"على المصحف: الصورُ المرخَّصةُ وصلًا {m['continue_licensed']:,} من {m['forms']:,}؛ "
        f"الثلاثيّةُ فقط "
        f"{m['ternary_only']} وكلُّها ذاتُ مدٍّ لازم "
        f"({'✓' if m['ternary_only_all_lazim'] else '✗'})، وصورُ "
        f"اللازم {m['lazim_forms']} وكلُّها ثلاثيّةٌ فقط "
        f"({'✓' if m['lazim_all_ternary_only'] else '✗'}).",
        "",
        "## الأحكامُ من الخانة التالية والحدّ", "",
        "بعد المدّ همزةٌ في الكلمة ⇒ متّصل؛ ساكنٌ ⇒ لازم (مثقَّلٌ إن كان أوّلَ مضعَّف، "
        "مخفَّفٌ وإلّا)؛ المدُّ آخرَ "
        "الكلمة والتاليةُ صدرُها همزة ⇒ منفصلٌ وصلًا (`munfasil_iff_next_hamza`)؛ قبل الأخيرة "
        "وقفًا ⇒ عارضٌ "
        "للسكون، والكلمةُ نفسُها طبيعيٌّ وصلًا (`arid_iff_pause`)؛ وإلّا طبيعيّ. اللينُ واوٌ "
        "أو ياءٌ ساكنةٌ بعد فتحٍ "
        "قبل الأخيرة وقفًا. الصلةُ هاءٌ آخرَ الكلمة مضمومةٌ أو مكسورةٌ بين متحرّكين: كبرى إن "
        "صدرُ التالية همزة. "
        "الواوُ الساقطةُ لفظًا (أُولَئِكَ…) محجوبةٌ بالجدول (`silent_waw_tabled`). الشواهدُ "
        "`madd_witnesses`.",
        "",
        "## القياس على المصحف (مودَع الشهادات)", "",
        f"{m['tokens']:,} كلمةً مشهودةً بترتيبها، فيها {m['letters']:,} حرفَ مدٍّ بالخانة. "
        f"الأحكامُ وصلًا "
        "(التاليةُ قرينةُ المنفصل والصلة):",
        "",
        "| الحكم | العدد |", "|---|---|",
        *[f"| {k} | {wasl[k]:,} |" for k in KINDS if wasl[k]],
        "",
        f"وقفًا على كلّ كلمة: عارضٌ للسكون {waqf['عارض']:,}، لينٌ {waqf['لين']:,} (موضعُ "
        f"الوقف قرارُ القارئ لا "
        "الخانة؛ فالعددان سقفٌ لما يصير عارضًا أو لينًا إذا وُقف).",
        "",
        "## الصلةُ على MASAQ", "",
        f"الهاءُ آخرَ الكلمة بين متحرّكين في {sila_total:,} كلمة؛ قرينةُ المرجع (وسمُ "
        f"اللاحقة) تقول إنّها هاءُ الكناية في {sila_pron:,} ({100 * sila_pron / sila_total:.1f}%) "
        "— والباقي هاءُ "
        "الكلمة (اللَّه، وَجْه…): الخانةُ لا تفصل الضميرَ من الأصل، فالصلةُ قراءةٌ بشرط القرينة.",
        "",
        "## ما لا تقرؤه الخانة — باسمه", "",
        "- المقاديرُ (حركتان/أربع/ستّ) معلَنةٌ لا تُقرأ من الخانة.",
        "- الألفُ الخنجريّة والحروفُ الصغيرة ليست في المدوّنة المختومة: ذَلِكَ وهَذَا بلا "
        "مدٍّ على الخانة.",
        "- مدُّ العوض: ألفُ التنوين بقيّةُ رسمٍ تُردّ في الغانم؛ ومدُّ البدل تسميةٌ للطبيعيّ "
        "بعد همزة.",
        "- فواتحُ السور غيرُ مشكولةٍ (DEFER) فلا يُقرأ اللازمُ الحرفيّ.",
        "- الصفرُ المستطيل (أَنَا وصلًا) لا خانةَ له: الألفُ تُقرأ مدًّا.",
        "- الحصرُ المُرسَل: شجرةٌ نصّيّة وعلاماتُ ضبطٍ عثمانيّة — لم يُدخَل منه شيء؛ ودخل "
        "معناه على الخانات.",
        "",
    ]
    return "\n".join(lines)


def main() -> int:
    text = render()
    if "--check" in sys.argv:
        if TARGET.read_text(encoding="utf-8") != text:
            sys.stderr.write("MADD_INDEX.md غيرُ مطابق؛ شغّل tools/gen_madd_index.py\n")
            return 1
        sys.stdout.write("MADD_INDEX.md مطابق\n")
        return 0
    TARGET.write_text(text, encoding="utf-8")
    sys.stdout.write("كُتب MADD_INDEX.md\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
