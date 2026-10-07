"""فهرسُ النِّسَب الثلاث على درجات الترخيص التدريجيّ (NISAB_INDEX.md) من `slge.nisab` وشرائح MASAQ.

القياسُ على الشرائح المودَعة: أزواجُ (مبتدأ، خبر) من `masaq-jumla.json`، وأزواجُ (فعل، فاعل) و(فعل،
مفعول به) من `masaq-filiyya.json.gz`، وأزواجُ (الكلمةُ السابقة، اسمٌ مجرور) من `masaq-shibh.json.gz`
— كلُّها بشهادات البوّابة. القارئُ `nisba` يقرأ النسبةَ من الخانتين ويُقاس على وسم MASAQ:
الإسنادُ (مبتدأ/خبر، فعل/فاعل) والتقييدُ (مفعولٌ به، مجرور).
"""

from __future__ import annotations

import gzip
import json
import sys
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any

from slge.cells import index
from slge.nisab import chain, dist, nisba
from slge.wazn import AWZAN

ROOT = Path(__file__).resolve().parent.parent
TARGET = ROOT / "NISAB_INDEX.md"
DATA = ROOT / "tests" / "data"
Word = tuple[tuple[str, str], ...]


def _load(name: str) -> list[dict[str, Any]]:
    p = DATA / name
    if name.endswith(".gz"):
        with gzip.open(p, "rt", encoding="utf-8") as f:
            rows: list[dict[str, Any]] = json.load(f)["rows"]
        return rows
    rows = json.loads(p.read_text(encoding="utf-8"))["rows"]
    return rows


def _cells(r: dict[str, Any], keep: tuple[str, ...] = ("DET",), suffix: bool = False) -> Word:
    pre = [(a, b) for t, cs in r["pre"] for a, b in cs if t in keep]
    suf = [(a, b) for _, cs in r["suf"] for a, b in cs] if suffix else []
    return (*pre, *((a, b) for a, b in r["stem"]), *suf)


def pairs() -> list[tuple[str, Word, Word]]:
    """(وسمُ MASAQ للنسبة، الكلمةُ الأولى، الثانية)."""

    out: list[tuple[str, Word, Word]] = []
    by: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for r in _load("masaq-jumla.json"):
        by[str(r["ref"])].append(r)
    for verse in by.values():
        verse.sort(key=lambda r: int(str(r["pos"])))
        for i, r in enumerate(verse):
            if r["role"] == "مبتدأ" and i + 1 < len(verse) and verse[i + 1]["role"] == "خبر":
                out.append(("إسناد: مبتدأ وخبر", _cells(r), _cells(verse[i + 1])))
    by = defaultdict(list)
    for r in _load("masaq-filiyya.json.gz"):
        by[str(r["ref"])].append(r)
    verbs = ("فعل ماضٍ", "فعل مضارع", "فعل أمر")
    for verse in by.values():
        verse.sort(key=lambda r: int(str(r["pos"])))
        for i, r in enumerate(verse):
            if r["role"] in verbs and i + 1 < len(verse):
                nxt = verse[i + 1]
                v = _cells(r, ("IMPERF_PREF", "IV3MP", "IV3MS"), suffix=True)
                if nxt["role"] == "فاعل":
                    out.append(("إسناد: فعل وفاعل", v, _cells(nxt)))
                elif nxt["role"] == "مفعول به":
                    out.append(("تقييد: مفعول به", v, _cells(nxt, suffix=True)))
    by = defaultdict(list)
    for r in _load("masaq-shibh.json.gz"):
        by[str(r["ref"])].append(r)
    for verse in by.values():
        verse.sort(key=lambda r: int(str(r["pos"])))
        for i, r in enumerate(verse):
            if r["role"] != "اسم مجرور" or i == 0:
                continue
            prv = verse[i - 1]
            adjacent = int(str(prv["pos"])) == int(str(r["pos"])) - 1
            if adjacent and prv["role"] not in ("حرف جر", "حرف جرّ"):
                out.append(("تقييد: مضاف إليه أو مجرور", _cells(prv), _cells(r)))
    return out


def measure() -> dict[str, object]:
    ps = pairs()
    read: Counter[tuple[str, str]] = Counter()
    for tag, a, b in ps:
        read[(tag, nisba(a, b))] += 1
    depths = Counter(dist(k) for k in range(len(AWZAN)))
    return {"pairs": len(ps), "read": read, "depths": depths}


def _w(w: Word) -> str:
    return "-".join(str(index(c)) for c in w)


def render() -> str:
    m = measure()
    read: Counter[tuple[str, str]] = m["read"]  # type: ignore[assignment]
    depths: Counter[int] = m["depths"]  # type: ignore[assignment]
    agree = sum(v for (t, n), v in read.items() if t.split(":")[0] == n)
    deepest = max(range(len(AWZAN)), key=dist)
    lines = [
        "# فهرسُ النِّسَب الثلاث على درجات الترخيص التدريجيّ",
        "",
        "مولَّدٌ بـ`python tools/gen_nisab_index.py` من `src/slge/nisab.py`؛ لا يُحرَّر باليد. البرهانُ: "
        "`formal/Slge/Nisab.lean`.",
        "",
        "## د٤ الخانة — الإسنادُ عمليّةٌ واحدة", "",
        "المسندُ إليه مرفوعٌ بعمليّةٍ واحدةٍ في الجملتين: مبتدأُ الاسميّة وفاعلُ الفعليّة ونائبُه هي "
        "`Nawasikh.raf` بعينه (`isnad_one_operation`)، فيُقرأ رفعًا لكلّ جذع (`isnad_reads_raf`). "
        "والمسندُ: "
        "خبرٌ مرفوع، أو فعلٌ على قالبه، أو شبهُ جملةٍ بكونٍ محذوف (`Jumla.khabarKind`، `Shibh.anchor`).",
        "",
        "## د٨ الحدّ — التقييدُ لا يُنشئ رفعًا", "",
        "كلُّ مقيِّدٍ عمليّةٌ مبرهَنةٌ في بابها: الحالُ والتمييزُ والمفعولُ نصبٌ لكلّ جذع (`taqyid_nasb`)، "
        "والإضافةُ والجارُّ جرٌّ لكلّ اسم (`taqyid_jarr`)، والنعتُ يأخذ حالةَ متبوعه بتبعيّةٍ تناظريّةٍ "
        "انعكاسيّة (`naat_follows`) — فالرفعُ في التقييد تبعٌ لا أصل: ما نُصب أو جُرَّ لا يُقرأ رفعًا، "
        "والتابعُ المرفوعُ إنّما رُفع بمتبوعه (`taqyid_raf_only_by_following`).",
        "",
        "## د١٦ — التضمينُ ترتيبٌ جزئيٌّ على الخانات، والفصلُ قالب", "",
        "التضمينُ على الخانات هو الجزئيّةُ المرتَّبة (`List.Sublist`): انعكاسيٌّ ومتعدٍّ ومتضادُّ التباين "
        "(`contains_refl`، `contains_trans`، `contains_antisymm`) — ترتيبٌ جزئيٌّ من نواة Lean لا "
        "من نوعٍ "
        "مُعرَّفٍ باليد. الصورةُ تتضمّن جذرَها: حواملُ الجذر الثلاثةُ بترتيبها جزءٌ من حوامل الصورة لكلّ قالبٍ "
        "مودَع ولكلّ جذر (`form_contains_root`؛ `slots_ordered`). والفصلُ: الجنسُ الواحد (الميزان) "
        "تشقّه "
        "القوالبُ أنواعًا — ما اختلف قالبُه اختلفت صورتُه على 125 قالبًا (`species_distinct`)؛ "
        "والقالبُ المودَعُ "
        "بمعنيين (فِعَال مصدرًا وجمعًا) صورةٌ واحدة: الفصلُ هناك معنًى. وتضمينُ الأوزان في الشبكة سلسلةُ "
        "أسلافٍ تنتهي بالجذر لكلّ وزن (`chains_end_at_root`).",
        "",
        "| البعدُ عن الجذر | عددُ الأوزان |", "|---|---|",
        *[f"| {d} | {v} |" for d, v in sorted(depths.items())],
        "",
        f"أبعدُ الأوزان: {AWZAN[deepest].name} — سلسلتُه "
        + " ← ".join(AWZAN[k].name for k in chain(deepest)) + ".",
        "",
        "## القارئ", "",
        "`nisba` يقرأ النسبةَ بين كلمتين من خانتيهما: فعلٌ أو شبهُ جملةٍ بعد مبتدأ ⇒ إسناد؛ منصوبٌ أو "
        "مجرور ⇒ تقييد؛ مرفوعٌ بعد نكرةٍ مرفوعةٍ وهو نكرة ⇒ تقييدٌ (نعت)، وبعد مسندٍ إليه ⇒ إسناد "
        "(`nisba_witnesses`). التضمينُ بين كلمتين (الإنسانُ حيوان) معنًى لا خانة — باسمه.",
        "",
        "## القياس على MASAQ", "",
        f"على {m['pairs']:,} زوجًا من الشرائح المودَعة (مبتدأ/خبر، فعل/فاعل، فعل/مفعول، سابق/مجرور) "
        f"بشهادات البوّابة: القارئُ يوافق وسمَ MASAQ في {agree:,}.",
        "",
        "| وسمُ MASAQ | القارئ | العدد |", "|---|---|---|",
        *[f"| {t} | {n} | {v} |" for (t, n), v in read.most_common()],
        "",
        "ما لم يُقرأ: مسندٌ إليه مبنيٌّ غيرُ مجدوَل (إِنَّ وأخواتُها ومعمولاتُها)، وخبرٌ معتلٌّ أو مضافٌ إلى "
        "الياء، وفعلٌ معتلٌّ على غير قالب؛ وما قُرئ إسنادًا ووسمُه تقييدٌ: مفعولٌ به مرفوعُ الصورة بعد فعلٍ "
        "(أسماءُ الشرط والموصول) — بقيّةٌ مسمّاة.",
        "",
        "## ما لا تقرؤه الخانة — باسمه", "",
        "- التضمينُ بين الكلمات (الجنسُ والنوع: الإنسانُ حيوان): معجمٌ ودلالة؛ ما بُرهن هو التضمينُ على "
        "الخانات والقوالب.",
        "- العلمُ المنوَّن (زَيْدٌ) نكرةٌ بالخانة: فزَيْدٌ قَائِمٌ يُقرأ نعتًا — المعجم.",
        "- الحصرُ المُرسَل أحال على ملفّ `differentiation_and_verbal_matrix.lean` لم يُرفَق؛ وفحصُ "
        "إجهاده في "
        "بايثون يعدّ صحيحًا ما بناه صحيحًا بالتعريف (100% بالبناء) — لم يُدخَل منه شيء.",
        "",
    ]
    return "\n".join(lines)


def main() -> int:
    text = render()
    if "--check" in sys.argv:
        if TARGET.read_text(encoding="utf-8") != text:
            sys.stderr.write("NISAB_INDEX.md غيرُ مطابق؛ شغّل tools/gen_nisab_index.py\n")
            return 1
        sys.stdout.write("NISAB_INDEX.md مطابق\n")
        return 0
    TARGET.write_text(text, encoding="utf-8")
    sys.stdout.write("كُتب NISAB_INDEX.md\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
