"""فهرسُ معاني الحروف (MAANI_INDEX.md): الجدولُ بترتيب المصدر، وأثرُ القرينتين على MASAQ، وشواهدُ
المصدر القرآنيّة.

(١) الجدول: كلُّ حرفٍ ومعانيه كما ذكرها المصدر، والمتعدّدُ بأرقامه. (٢) على `masaq-shibh.json.gz`:
كلُّ حرفٍ له معانٍ — مستقلًّا (وسمُه PREP) أو سابقةً (PREP في سوابق الكلمة) — كم مرّةً وقع، وكم مرّةً أطلقت
قرينةُ الظرف بعده أو النفي قبله، وتوزيعُ المعنى الأوّل بعد الترتيب. (٣) شواهدُ المصدر القرآنيّة على
المعاني غير الأولى (إلى بمعنى مع، في بمعنى على، الباء بمعنى من أجل، اللامُ زائدة، الباءُ زائدة…)
تُفتَّش في MASAQ ويُذكر هل يقدّم الترتيبُ معنى المصدر — رقمٌ يُنشر كما هو.
"""

from __future__ import annotations

import gzip
import json
import sys
from collections import Counter
from pathlib import Path
from typing import Any

from slge.adawat import TABLE_ADAWAT, of_cells
from slge.huruf import TABLE as HURUF
from slge.maani import MULTI, is_zarf, jarr_uncovered, rank, senses_of

ROOT = Path(__file__).resolve().parent.parent
TARGET = ROOT / "MAANI_INDEX.md"
DATA = ROOT / "tests" / "data"
Word = tuple[tuple[str, str], ...]

WITNESSES: tuple[tuple[str, str, str, str], ...] = (
    # (الحرفُ كما في المصدر، كلمةُ المجرور في MASAQ، معنى المصدر، نصُّ الشاهد)
    ("إِلَى", "أَمْوَالِكُمْ", "بمعنى مع", "وَلَا تَأْكُلُوا أَمْوَالَهُمْ إِلَى أَمْوَالِكُمْ"),
    ("فِي", "جُذُوعِ", "بمعنى على", "وَلَأُصَلِّبَنَّكُمْ فِي جُذُوعِ النَّخْلِ"),
    ("بِ", "بِدُعَائِكَ", "بمعنى من أجل", "وَلَمْ أَكُنْ بِدُعَائِكَ رَبِّ شَقِيًّا"),
    ("لِ", "لَكُمْ", "زائدة", "رَدِفَ لَكُم"),
    ("بِ", "بِأَيْدِيكُمْ", "زائدة", "وَلَا تُلْقُوا بِأَيْدِيكُمْ إِلَى التَّهْلُكَةِ"),
    ("عَنْ", "أَمْرِهِ", "المباعدة", "فَلْيَحْذَرِ الَّذِينَ يُخَالِفُونَ عَنْ أَمْرِهِ"),
)


def rows() -> list[dict[str, Any]]:
    with gzip.open(DATA / "masaq-shibh.json.gz", "rt", encoding="utf-8") as f:
        out: list[dict[str, Any]] = json.load(f)["rows"]
    return out


def whole(r: dict[str, Any]) -> Word:
    return (*((a, b) for _, cs in r["pre"] for a, b in cs), *((a, b) for a, b in r["stem"]),
            *((a, b) for _, cs in r["suf"] for a, b in cs))


def host(r: dict[str, Any]) -> Word:
    """الكلمةُ بعد سابقة الجرّ: الجذعُ ولواحقُه."""

    return (*((a, b) for a, b in r["stem"]), *((a, b) for _, cs in r["suf"] for a, b in cs))


def occurrences(rs: list[dict[str, Any]]) -> list[tuple[int, Word, Word, dict[str, Any]]]:
    """(فهرسُ الحرف، ما قبله، ما بعده، الصفّ) لكلّ حرفٍ له معانٍ في المصدر."""

    idx = {(r["ref"], r["pos"]): r for r in rs}
    out = []
    for r in rs:
        prev = idx.get((r["ref"], r["pos"] - 1))
        before: Word = whole(prev) if prev else ()
        if r["tag"] == "PREP":
            a = of_cells(whole(r))
            if a is not None and senses_of(TABLE_ADAWAT.index(a)):
                nxt = idx.get((r["ref"], r["pos"] + 1))
                out.append((TABLE_ADAWAT.index(a), before, whole(nxt) if nxt else (), r))
            continue
        for label, cs in r["pre"]:
            if label != "PREP":
                continue
            a = of_cells(tuple((x, y) for x, y in cs))
            if a is not None and senses_of(TABLE_ADAWAT.index(a)):
                out.append((TABLE_ADAWAT.index(a), before, host(r), r))
    return out


def measure() -> dict[str, Any]:
    rs = rows()
    occ = occurrences(rs)
    per: dict[int, Counter[str]] = {}
    tops: dict[int, Counter[str]] = {}
    for h, before, after, _ in occ:
        c = per.setdefault(h, Counter())
        c["n"] += 1
        b = of_cells(before) if before else None
        nafy = bool(b and b.rel == "نفي")
        zarf = is_zarf(after)
        c["nafy"] += nafy
        c["zarf"] += zarf
        c["either"] += nafy or zarf
        ranked = rank(senses_of(h), nafy_before=nafy, zarf_after=zarf)
        c["changed"] += ranked != senses_of(h)
        tops.setdefault(h, Counter())[ranked[0]] += 1
    found: list[tuple[str, str, str, str | None, bool | None]] = []
    for harf, word, stated, text in WITNESSES:
        hit = next((o for o in occ if o[3]["word"] == word or (o[3]["tag"] == "PREP" and
                     o[3]["word"] == harf and o[2] and _word_after(o[3], rs) == word)), None)
        if hit is None:
            found.append((harf, text, stated, None, None))
            continue
        h, before, after, _ = hit
        b = of_cells(before) if before else None
        ranked = rank(senses_of(h), nafy_before=bool(b and b.rel == "نفي"),
                      zarf_after=is_zarf(after))
        found.append((harf, text, stated, ranked[0], stated in ranked))
    return {"occ": len(occ), "per": per, "tops": tops, "witnesses": found}


def _word_after(r: dict[str, Any], rs: list[dict[str, Any]]) -> str:
    nxt = next((x for x in rs if x["ref"] == r["ref"] and x["pos"] == r["pos"] + 1), None)
    return nxt["word"] if nxt else ""


def render() -> str:
    m = measure()
    lines = [
        "# فهرسُ معاني الحروف — تعدّدُ معاني الحرف الواحد مرتَّبًا بالقرينة",
        "",
        "مولَّدٌ بـ`python tools/gen_maani_index.py` من `src/slge/maani.py`؛ لا يُحرَّر "
        "باليد. البرهانُ: "
        "`formal/Slge/Maani.lean`؛ الجدولُ `formal/Slge/MaaniTable.lean` مولَّدٌ من "
        "المودَع المختوم "
        "`tests/data/nabhani-huruf.json` (`tools/deposit_maani.py --check`): مبحثُ «الحرف» "
        "في الشخصيّة "
        "الإسلاميّة ج3، نقلًا بترتيب المصدر.",
        "",
        "## الجدول — بترتيب المصدر", "",
        "| # | الحرف | المعاني |", "|---|---|---|",
    ]
    for h in sorted(set(MULTI) | {i for i in range(len(HURUF)) if senses_of(i)}):
        lines.append(f"| {h} | {HURUF[h].name} | {' › '.join(senses_of(h))} |")
    lines += [
        "",
        f"المتعدّدُ ({len(MULTI)} أحرف، `multi_eq`): {', '.join(HURUF[h].name for h in MULTI)}. "
        f"حروفُ الجرّ بلا معنًى في المصدر (`jarr_uncovered`): "
        f"{', '.join(HURUF[h].name for h in jarr_uncovered())} — مدخلُها نثرٌ عن الاستثناء. "
        "مبرهَن: حيث ذكر المصدرُ معنى غايةٍ ذكره أوّلًا (`ghaya_first_in_source`)؛ "
        "الترتيبُ بالقرينتين لا "
        "يُسقط معنًى (`mem_rank`، `length_rank`)، وبلا قرينةٍ يعيد ترتيبَ المصدر (`rank_none`).",
        "",
        "## القرينتان على MASAQ (معلَنتان، مقيستان)", "",
        f"وقع حرفٌ له معانٍ {m['occ']:,} مرّةً (مستقلًّا أو سابقةً). القرينتان: ظرفُ مكانٍ "
        f"أو زمانٍ بعده "
        "(`is_zarf`: جدولا `zuruf`/`zaman` بصورهما) يقدّم الغاية؛ ونفيٌ قبله (أداةٌ سابقة "
        "علاقتُها «نفي») يقدّم "
        "«زائدة» — تعميمٌ لشاهد المصدر «ما جاءني من أحد». «غيّرت الترتيب» = المرّاتُ التي "
        "خالف فيها الترتيبُ "
        "ترتيبَ المصدر (الظرفُ يثبّت الأصلَ الأوّل فلا يغيّر — `ghaya_first_in_source`).",
        "",
        "| الحرف | المرّات | ظرفٌ بعده | نفيٌ قبله | غيّرت الترتيب | المعنى الأوّل بعد الترتيب |",
        "|---|---|---|---|---|---|",
    ]
    for h in sorted(m["per"]):
        c, t = m["per"][h], m["tops"][h]
        top = "، ".join(f"{s} {n:,}" for s, n in t.most_common())
        lines.append(f"| {HURUF[h].name} | {c['n']:,} | {c['zarf']:,} | {c['nafy']:,} | "
                     f"{c['changed']:,} | {top} |")
    lines += ["", "## شواهدُ المصدر القرآنيّة على المعاني غير الأولى", "",
              "| الشاهد | الحرف | معنى المصدر | الأوّلُ عندنا | المصدرُ في القائمة |",
              "|---|---|---|---|---|"]
    ok = 0
    for harf, text, stated, top, inlist in m["witnesses"]:
        if top is None:
            lines.append(f"| {text} | {harf} | {stated} | — لم يوجد في الشريحة | — |")
            continue
        ok += top == stated
        lines.append(f"| {text} | {harf} | {stated} | {top} | {'نعم' if inlist else 'لا'} |")
    n = sum(1 for w in m["witnesses"] if w[3] is not None)
    lines += ["",
              f"يقدّم الترتيبُ معنى المصدر في {ok} من {n} شواهدَ وُجدت: القرينتان لا تبلغان "
              f"«بمعنى مع» ولا "
              "«بمعنى على» ولا «من أجل» — تلزمها قرينةُ المتعلَّق (الفعلُ العامل وجنسُ "
              "المجرور) وهي دينٌ باسمه؛ "
              "والمعنى المذكور في المصدر حاضرٌ في القائمة لا محذوف.",
              "", "## ما ليس هنا — باسمه", "",
              "- النواسخُ (كان، إنّ، ظنّ، الشروع) لا معاني لها في مبحث الحرف إلّا "
              "المشبّهةُ بالفعل (توكيد/استدراك/"
              "تشبيه/تمنٍّ/ترجٍّ) وهي في `Adawat.Rel` أصلًا؛ وصفُها معلَن.",
              "- «أو» بالشكّ والتخيير والإباحة قرينتُها المقامُ (خبر/أمر/استفهام) بنصّ "
              "المصدر — تحتاج `Uslub` على "
              "الجملة لا على الكلمة؛ لم تُنفَّذ.",
              "- حروفُ الجواب (نعم، بلى، أجل، جير) خارج `Huruf.table`: في المودَع تحت `skipped` "
              "باسمها.",
              ""]
    return "\n".join(lines)


def main() -> int:
    text = render()
    if "--check" in sys.argv:
        if TARGET.read_text(encoding="utf-8") != text:
            sys.stderr.write("MAANI_INDEX.md غيرُ مطابق؛ شغّل tools/gen_maani_index.py\n")
            return 1
        sys.stdout.write("MAANI_INDEX.md مطابق\n")
        return 0
    TARGET.write_text(text, encoding="utf-8")
    sys.stdout.write("كُتب MAANI_INDEX.md\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
