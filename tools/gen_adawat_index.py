"""فهرسُ الأدوات علاقاتٍ تشغيليّة (ADAWAT_INDEX.md): عملُ الأداة على جارتها وترتيبُها لقراءاتها —
مقيسان على قسمة MASAQ المحجوبة، والرقمُ قبلُ وبعدُ على المودَع نفسه.

على `tests/data/masaq-shibh.json.gz` (40,731 كلمةً بمرجعها وموضعها؛ 29,866 لها تاليةٌ في المودَع):
(١) **العمل**: لكلّ أداةٍ عاملةٍ قائمةٍ بنفسها (صورتُها كلمةٌ من الجدول) تليها كلمةٌ معربة — هل حالةُ
التالية عند المرجع هي ما تعمله الأداة (الجرُّ ← مجرور، نصبُ الاسم والفعل ← منصوب، الجزمُ ← مجزوم)؟
وللجارّ المتّصل (سابقةُ PREP عند المرجع) كذلك. (٢) **الترتيب**: للكلمة التالية لأداةٍ قراءاتٌ من صنفين
(اسمٌ وفعل) — هل القراءةُ الأولى بعد ترتيب الأداة صنفُها صنفُ المرجع (وسمُ MASAQ)؟ قبلُ (ترتيبُ
المقاييس وحدَه) وبعدُ. وعلى مودَع المصحف الكامل (18,179 صورة) كم صورةً صورتُها أداةٌ من الجدول.
"""

from __future__ import annotations

import gzip
import json
import sys
from collections import Counter
from pathlib import Path
from typing import Any

from slge.adawat import ISM, TABLE_ADAWAT, cat_of, fits, of_cells, rank
from slge.jidh import jidh
from slge.maqayis import rank as rank_maqayis

ROOT = Path(__file__).resolve().parent.parent
TARGET = ROOT / "ADAWAT_INDEX.md"
DATA = ROOT / "tests" / "data"
Word = tuple[tuple[str, str], ...]
EXPECT: dict[str, str] = {"جرّ": "مجرور", "نصب الاسم": "منصوب", "نصب الفعل": "منصوب", "جزم": "مجزوم",
                          "جزم فعلين": "مجزوم"}
VERB_TAGS = {"PV", "IV", "CV", "PV_PASS", "IV_PASS"}
NOUN_TAGS = {"NOUN_CONCRETE", "NOUN_ABSTRACT", "GERUND", "NOUN_PROP", "NOUN_ACTIVE_PART",
             "ADJ_QUALIT", "ADJ_COMP", "NOUN_PASSIVE_PART", "NOUN_PROP_FOREIGN", "ADV"}


def corpus_forms() -> list[Word]:
    with gzip.open(DATA / "corpus-certificates.json.gz", "rt", encoding="utf-8") as f:
        d: dict[str, Any] = json.load(f)
    return [tuple((a, b) for a, b in x["cells"]) for x in d["forms"]]


def masaq_rows() -> list[dict[str, Any]]:
    with gzip.open(DATA / "masaq-shibh.json.gz", "rt", encoding="utf-8") as f:
        rows: list[dict[str, Any]] = json.load(f)["rows"]
    return rows


def whole(r: dict[str, Any]) -> Word:
    return (*((a, b) for _, cs in r["pre"] for a, b in cs), *((a, b) for a, b in r["stem"]),
            *((a, b) for _, cs in r["suf"] for a, b in cs))


def measure() -> dict[str, Any]:
    rows = masaq_rows()
    idx = {(r["ref"], r["pos"]): r for r in rows}
    amal: dict[str, Counter[str]] = {}
    attached: Counter[str] = Counter()
    order_before: Counter[str] = Counter()
    order_after: Counter[str] = Counter()
    per_tool: Counter[str] = Counter()
    for r in rows:
        a = of_cells(whole(r))
        nxt = idx.get((r["ref"], r["pos"] + 1))
        if a is None or nxt is None:
            continue
        per_tool[a.harf.name] += 1
        want = EXPECT.get(a.harf.amal)
        if want:
            c = amal.setdefault(a.harf.amal, Counter())
            c["موافق" if nxt["case"] == want else "مبنيّ" if nxt["case"] == "مبني" else "مخالف"] += 1
        gold = "فعل" if nxt["tag"] in VERB_TAGS else ISM if nxt["tag"] in NOUN_TAGS else None
        if gold is None or a.args[0] not in (ISM, "فعل"):
            continue
        rs = rank_maqayis(jidh(whole(nxt)))
        if len({cat_of(x) for x in rs}) < 2:
            continue
        order_before[("موافق" if cat_of(rs[0]) == gold else "مخالف")] += 1
        order_after[("موافق" if cat_of(rank(a, rs)[0]) == gold else "مخالف")] += 1
        assert len(rank(a, rs)) == len(rs) and all(fits(a, x) or not fits(a, x) for x in rs)
    for r in rows:
        if any(t == "PREP" for t, _ in r["pre"]):
            key = "موافق" if r["case"] == "مجرور" else "مبنيّ" if r["case"] == "مبني" else "مخالف"
            attached[key] += 1
    forms = corpus_forms()
    tool_forms = sum(of_cells(w) is not None for w in forms)
    return {"rows": len(rows), "with_next": sum(1 for r in rows if (r["ref"], r["pos"] + 1) in idx),
            "amal": amal, "attached": attached, "before": order_before, "after": order_after,
            "per_tool": per_tool.most_common(12), "forms": len(forms), "tool_forms": tool_forms,
            "table": len(TABLE_ADAWAT)}


def _pct(c: Counter[str], key: str) -> str:
    tot = sum(c.values())
    return f"{c[key]:,} ({100 * c[key] / tot:.1f}%)" if tot else "—"


def render() -> str:
    m = measure()
    lines = [
        "# فهرسُ الأدوات علاقاتٍ تشغيليّة",
        "",
        "مولَّدٌ بـ`python tools/gen_adawat_index.py` من `src/slge/adawat.py`؛ لا يُحرَّر باليد. "
        "البرهانُ: `formal/Slge/Adawat.lean`.",
        "",
        "## البنية", "",
        f"{m['table']} أداةً من جدول الحروف الموحَّد، لكلٍّ: الصورةُ خاناتٍ، الرتبةُ، أصنافُ المعمولات، "
        "العملُ دالّةً على خانة آخر المعمول (`apply`: مرخَّصٌ على المعرب `apply_licensed`، والجزمُ "
        "`apply_jazm_licensed`)، ونوعُ العلاقة **معلَنًا** من كتب حروف المعاني — الخاناتُ لا تحمل معنى "
        "فلا جداولَ صدقٍ هنا. التركيبُ بعينه والكفُّ (`compositions`: كَأَنَّ = كَ ++ أَنَّ، لِكَيْ = لِ ++ "
        "كَيْ، إِنَّمَا = إِنَّ ++ مَا بلا عمل). والأداةُ المجاورة ترتّب قراءاتِ جارتها بصنف معمولها الأوّل "
        "ولا تُسقط قراءةً (`mem_rank`، `length_rank`) — بوّابةُ «الأدوات» في السُّلَّم.",
        "",
        "## العملُ على المرجع المحجوب", "",
        f"على {m['rows']:,} كلمةً من MASAQ ({m['with_next']:,} لها تاليةٌ في المودَع): الأداةُ العاملةُ "
        "القائمةُ بنفسها وحالةُ الكلمة التالية عند المرجع:",
        "",
        "| العمل | موافق | مخالف | التاليةُ مبنيّة (لا يُقاس) |", "|---|---|---|---|",
    ]
    for k in ("جرّ", "نصب الاسم", "نصب الفعل", "جزم", "جزم فعلين"):
        c = m["amal"].get(k, Counter())
        lines.append(f"| {k} | {_pct(c, 'موافق')} | {_pct(c, 'مخالف')} | {c['مبنيّ']:,} |")
    c = m["attached"]
    lines += [
        "",
        f"والجارُّ المتّصلُ (سابقةُ PREP عند المرجع): مجرور {_pct(c, 'موافق')}، مخالف "
        f"{_pct(c, 'مخالف')}، مبنيّ {c['مبنيّ']:,}.",
        "",
        "المخالفُ باسمه: معمولُ الأداة ليس التاليةَ دائمًا (إِنَّ + ظرفٌ/جارٌّ ثمّ الاسم؛ لَمْ + فعلٍ مبنيٍّ "
        "للجماعة يُعدّ مبنيًّا عند المرجع)؛ والصورةُ المشتركة (لَا ×4، وَ ×4، حَتَّى ×3) تُؤخذ هنا بأوّل "
        "مدخلٍ لها، فلَا كلُّها نافيةٌ للجنس في هذا القياس وهو سببُ ضعف «نصب الاسم» — فصلُ المشترك شأنُ "
        "الجملة (ب)، وهذه حدودُ «الأداةُ تعمل في جارتها».",
        "",
        "## الترتيبُ على المرجع المحجوب", "",
        "الكلمةُ التاليةُ لأداةٍ معمولُها اسمٌ أو فعل ولها قراءاتٌ من الصنفين معًا: هل القراءةُ الأولى "
        "صنفُها صنفُ المرجع؟",
        "",
        "| | موافق | مخالف |", "|---|---|---|",
        f"| قبل (ترتيبُ المقاييس وحدَه) | {_pct(m['before'], 'موافق')} "
        f"| {_pct(m['before'], 'مخالف')} |",
        f"| بعد ترتيب الأداة | {_pct(m['after'], 'موافق')} | {_pct(m['after'], 'مخالف')} |",
        "",
        "أكثرُ الأدوات ورودًا قبل تاليةٍ في المودَع: "
        + "، ".join(f"{n} ({k:,})" for n, k in m["per_tool"]) + ".",
        "",
        "## على مودَع المصحف", "",
        f"من {m['forms']:,} صورةً، صورتُها أداةٌ من الجدول: {m['tool_forms']:,}.",
        "",
        "## ما ليس هنا — باسمه", "",
        "- نوعُ العلاقة (جمع، ترتيب، تخيير، شرط…) معلَنٌ لا مقيس: لا مرجعَ محجوبًا للمعنى قبل التفسير "
        "المختوم (د).",
        "- العطفُ والشرطُ ثنائيّا الرتبة: المعمولُ الثاني غيرُ الجار؛ يُقرأ في الجملة لا هنا.",
        "- «و» ليست ∧ و«أو» ليست ∨ و«إنْ» ليست الاستلزام: الأداةُ هنا مؤثِّرٌ على الخانات والقراءات لا "
        "دالّةُ صدق.",
        "",
    ]
    return "\n".join(lines)


def main() -> int:
    text = render()
    if "--check" in sys.argv:
        if TARGET.read_text(encoding="utf-8") != text:
            sys.stderr.write("ADAWAT_INDEX.md غيرُ مطابق؛ شغّل tools/gen_adawat_index.py\n")
            return 1
        sys.stdout.write("ADAWAT_INDEX.md مطابق\n")
        return 0
    TARGET.write_text(text, encoding="utf-8")
    sys.stdout.write("كُتب ADAWAT_INDEX.md\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
