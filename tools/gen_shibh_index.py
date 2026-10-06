"""فهرسُ شبه الجملة على درجات الترخيص التدريجيّ (SHIBH_INDEX.md) من `slge.shibh` وشريحة MASAQ.

الشريحةُ `tests/data/masaq-shibh.json.gz`: كلماتُ المصحف التي فيها حرفُ جرٍّ أو ظرفٌ أو اسمٌ مجرور،
وجاراتُها (الكلمةُ قبلها وبعدها)، خاناتُها من شهادات بوّابة الغانم بأوسام MASAQ. القياسُ: صورةُ شبه الجملة
بالقارئ،
وجرُّ ما بعد الحرف، والمرتكزُ والمحلُّ ممّا قبلها حيث وسم MASAQ الوظيفةَ (خبر، نائب فاعل).
"""

from __future__ import annotations

import gzip
import json
import sys
from collections import Counter
from pathlib import Path
from typing import Any

from slge.cells import index
from slge.shibh import anchor, kind, mahall, zaid_restores
from slge.tawabi import case_class

ROOT = Path(__file__).resolve().parent.parent
TARGET = ROOT / "SHIBH_INDEX.md"
SLICE = ROOT / "tests" / "data" / "masaq-shibh.json.gz"
JARR = ("حرف جر", "حرف جرّ")
Word = tuple[tuple[str, str], ...]


def _rows() -> list[dict[str, Any]]:
    with gzip.open(SLICE, "rt", encoding="utf-8") as f:
        rows: list[dict[str, Any]] = json.load(f)["rows"]
    return rows


def _cells(r: dict[str, Any], keep: tuple[str, ...] = ("PREP", "DET"), suffix: bool = True) -> Word:
    pre = [(a, b) for t, cs in r["pre"] for a, b in cs if t in keep]
    suf = [(a, b) for _, cs in r["suf"] for a, b in cs] if suffix else []
    return (*pre, *((a, b) for a, b in r["stem"]), *suf)


def measure() -> dict[str, object]:
    rows = _rows()
    by = {int(r["idx"]): r for r in rows}
    kinds: Counter[tuple[str, str]] = Counter()
    majrur: Counter[str] = Counter()
    anch: Counter[tuple[str, str]] = Counter()
    mah: Counter[tuple[str, str]] = Counter()
    zarf: Counter[tuple[str, str]] = Counter()
    restored = 0
    for r in rows:
        roles = list(r["stem_roles"])
        pfs = list(r["pfs"])
        has_jarr = any(x in JARR for x in roles)
        role = str(r["role"])
        if has_jarr or role in ("ظرف زمان", "ظرف مكان"):
            w = _cells(r)
            masaq = "جار ومجرور" if has_jarr else "ظرف"
            kinds[(masaq, kind(w))] += 1
            if role in ("ظرف زمان", "ظرف مكان"):
                zarf[(role, kind(w))] += 1
        if has_jarr and role not in JARR and "اسم مجرور" in roles:  # الحرفُ سابقةٌ والمجرورُ جذعُها
            majrur[case_class(_cells(r, ("DET",), suffix=False))] += 1
        if has_jarr and role in JARR:
            nxt = by.get(int(r["idx"]) + 1)
            if nxt is not None and str(nxt["role"]) == "اسم مجرور":
                majrur[case_class(_cells(nxt, ("DET",), suffix=False))] += 1
                restored += zaid_restores(_cells(nxt, ("DET",), suffix=False))
        pf = next((p for p in pfs if p), "")
        if "شبه جملة" in r["phrases"] and pf:
            prv = by.get(int(r["idx"]) - 1)
            if prv is not None:
                pc = _cells(prv, ("DET",))
                anch[(pf, anchor(pc))] += 1
                mah[(pf, mahall(pc))] += 1
    return {"n": len(rows), "kinds": kinds, "majrur": majrur, "anchor": anch, "mahall": mah,
            "zarf": zarf, "restored": restored}


def _w(w: Word) -> str:
    return "-".join(str(index(c)) for c in w)


def render() -> str:
    m = measure()
    kinds: Counter[tuple[str, str]] = m["kinds"]  # type: ignore[assignment]
    majrur: Counter[str] = m["majrur"]  # type: ignore[assignment]
    anch: Counter[tuple[str, str]] = m["anchor"]  # type: ignore[assignment]
    mah: Counter[tuple[str, str]] = m["mahall"]  # type: ignore[assignment]
    zarf: Counter[tuple[str, str]] = m["zarf"]  # type: ignore[assignment]
    lines = [
        "# فهرسُ شبه الجملة على درجات الترخيص التدريجيّ",
        "",
        "مولَّدٌ بـ`python tools/gen_shibh_index.py` من `src/slge/shibh.py`؛ لا يُحرَّر باليد. البرهانُ: "
        "`formal/Slge/Shibh.lean`.",
        "",
        "## د٤ الخانة — صورتان لا ثالثَ لهما", "",
        "الجارُّ والمجرور: حرفٌ من جدول `Majrurat.harfs` ثمّ جرٌّ على الخانة الأخيرة "
        "(`jarrMajrur`)؛ المجرورُ "
        "بعد الحرف بعينه ويُقرأ جرًّا لكلّ اسم (`jarr_majrur_reads_jarr`)، والتركيبُ مرخَّصٌ لكلّ حرفٍ واسم "
        "(`jarr_majrur_licensed`). الظرفُ: اسمٌ من جداول `Zuruf`/`Zaman` منصوبًا (`zarf`؛ "
        "`zarf_reads_nasb`). "
        "القارئُ `kind` يفرز الصورتين من الجدول والصدر، وما سواهما ليس شبهَ جملة (`kind_witnesses`).",
        "",
        "**الزائد**: الجرُّ بالحرف الزائد عمليّةٌ على الخانة الأخيرة لا تمسّ المحلّ: ردُّه رفعٌ "
        "يُعيد الاسمَ بعينه "
        "لكلّ اسم — `raf (jarr w) = raf w` (`zaid_restores`؛ `setLast_setLast`): مَا جَاءَ مِنْ "
        "أَحَدٍ = مَا جَاءَ "
        "أَحَدٌ على الخانة (`zaid_witness`). وخروجُ المجرور بالزائد من شبه الجملة اصطلاحًا: معلَن.",
        "",
        "**قانونُ الحظر**: جدولُ الظروف حاصر (17 ظرفَ مكان وظروفُ الزمان)؛ المسجدُ ليس فيه فلا "
        "يُقرأ ظرفًا "
        "بالنصب، ويُجرّ بالحرف شبهَ جملةٍ من الصورة الأولى (`masjid_not_zarf`).",
        "",
        "## د٨ الحدّ — التعلّق", "",
        "المرتكزُ ممّا قبل شبه الجملة: فعلٌ على قالبه، أو مشتقٌّ على قالب الوصف، وإلّا فالكونُ "
        "العامُّ المحذوف "
        "(`anchor`): جَلَسَ {فِي الحَدِيقَةِ}، قَائِمٌ {أَمَامَكَ}، الْعِلْمُ {فِي الصُّدُورِ} (`anchor_witnesses`). "
        "الثلاثةُ حاصرةٌ بالبناء. (برهانُ Lean في الحصر المُرسَل — `isCompositionValid` كلُّ فروعه "
        "`true` — "
        "تحصيلُ حاصلٍ على نوعٍ مُعرَّفٍ باليد؛ وما هنا يقرأ المرتكزَ من الخانات.)",
        "",
        "## د١٦ — مصفوفةُ المحلّ والكونُ المحذوف", "",
        "حين يكون المرتكزُ كونًا محذوفًا، محلُّ شبه الجملة تقرؤه خانةُ ما قبلها (`mahall`): بعد "
        "الموصول صلةٌ "
        "لكلّ الموصولات (`mahall_after_mawsul`)، بعد النكرة المحضة نعتٌ لكلّ جذع "
        "(`mahall_after_nakira`)، بعد "
        "المعرفة بأل مرفوعةً خبرٌ لكلّ جذع (`mahall_after_al_raf`)، وبعد المنصوبة حالٌ "
        "(`mahall_witnesses`). "
        "والكونُ المحذوفُ يأخذ حالةَ المحلّ (`kawn`؛ `kawn_reads`): كَائِنٌ خبرًا، كَائِنًا نعتًا وحالًا، "
        "اسْتَقَرَّ صلةً — تقديرُه معلَنٌ وحالتُه مقروءة.",
        "",
        "| المحلّ | الكونُ المحذوف |", "|---|---|",
        *[f"| {k} | `{_w(w)}` |" for k, w in (("خبر", _kawn("خبر")), ("نعت", _kawn("نعت")),
                                                ("حال", _kawn("حال")), ("صلة", _kawn("صلة")))],
        "",
        "## القياس على MASAQ", "",
        f"على {m['n']:,} كلمةً (الحروفُ والظروفُ والمجروراتُ وجاراتُها بشهادات البوّابة).", "",
        "### الصورةُ: وسمُ MASAQ × القارئ", "",
        "| وسم MASAQ | القارئ | العدد |", "|---|---|---|",
        *[f"| {a} | {b} | {v} |" for (a, b), v in kinds.most_common()],
        "",
        "الظرفُ خارج الجدول (إِذْ، إِذَا، يَوْمَئِذٍ، عِنْدَ بالضمير…) لا يقرؤه القارئ ظرفًا: الجدولُ حاصرٌ "
        "بالمودَع، وما سواه بقيّةٌ مسمّاة.",
        "",
        "| دورُ الظرف | القارئ | العدد |", "|---|---|---|",
        *[f"| {a} | {b} | {v} |" for (a, b), v in zarf.most_common()],
        "",
        f"### المجرورُ بعد الحرف: حالتُه المقروءة — والزائدُ يُردّ بعينه في {m['restored']:,}", "",
        "| الحالة | العدد |", "|---|---|",
        *[f"| {a} | {v} |" for a, v in majrur.most_common()],
        "",
        "ما لا تقرؤه الخانة جرًّا: المبنيُّ (الضمائرُ والموصولات) والمقصورُ والمضافُ إلى الياء — "
        "حالتُه محلّ.",
        "",
        "### المرتكزُ والمحلُّ ممّا قبل شبه الجملة (حيث وسم MASAQ وظيفتَها)", "",
        "| وظيفة MASAQ | المرتكزُ بالقارئ | العدد |", "|---|---|---|",
        *[f"| {a} | {b} | {v} |" for (a, b), v in anch.most_common()],
        "",
        "| وظيفة MASAQ | المحلُّ بالقارئ | العدد |", "|---|---|---|",
        *[f"| {a} | {b} | {v} |" for (a, b), v in mah.most_common()],
        "",
        "خبرُ الناسخ بعد كَانَ/إِنَّ: الكلمةُ قبل شبه الجملة اسمُ الناسخ لا المبتدأ، فالقارئُ يقرأ محلَّها من "
        "حالته (نصبٌ ⇒ حال، رفعٌ ⇒ خبر) — والناسخُ يفصل (`Nawasikh`). ونائبُ الفاعل: المرتكزُ "
        "الفعلُ المجهول "
        "بالقراءة.",
        "",
        "## ما لا تقرؤه الخانة — باسمه", "",
        "- الأصليُّ والزائدُ خانةٌ واحدة (مِنْ): الزيادةُ معنًى؛ والردُّ عمليّةٌ.",
        "- تقديرُ الكون (مُسْتَقِرٌّ/كَائِنٌ/اسْتَقَرَّ): معلَن؛ حالتُه مقروءة.",
        "- المختصُّ من الأمكنة (المسجد): خارج الجدول باسمه؛ والحدودُ الطوبولوجيّة معجم.",
        "- المرتكزُ البعيد (غيرُ الكلمة السابقة) وتعلّقُ الظرف بالمصدر: تيار.",
        "- شريحةُ MASAQ: 3,370 كلمةً مستبعَدة (غيرُ محاذاة 1,512، مرفوضٌ بالاسم 1,444، عدٌّ مخالف 414).",
        "",
    ]
    return "\n".join(lines)


def _kawn(m: str) -> Word:
    from slge.shibh import kawn

    return kawn(m)


def main() -> int:
    text = render()
    if "--check" in sys.argv:
        if TARGET.read_text(encoding="utf-8") != text:
            sys.stderr.write("SHIBH_INDEX.md غيرُ مطابق؛ شغّل tools/gen_shibh_index.py\n")
            return 1
        sys.stdout.write("SHIBH_INDEX.md مطابق\n")
        return 0
    TARGET.write_text(text, encoding="utf-8")
    sys.stdout.write("كُتب SHIBH_INDEX.md\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
