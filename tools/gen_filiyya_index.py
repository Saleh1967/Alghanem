"""فهرسُ الجملة الفعليّة على درجات الترخيص التدريجيّ (FILIYYA_INDEX.md) من `slge.filiyya` وشريحة MASAQ.

الشريحةُ `tests/data/masaq-filiyya.json.gz`: أفعالُ المصحف وما وسمه MASAQ فاعلًا أو مفعولًا به أو نائبَ
فاعلٍ أو ظرفًا أو مفعولًا لأجله أو مطلقًا أو معه، خاناتُها من شهادات بوّابة الغانم (الجذعُ والسوابقُ
واللواحقُ بأوسامها). الثلاثيّاتُ (فعل، فاعل، مفعول) تُبنى هنا: لكلّ فعلٍ أقربُ فاعلٍ ومفعولٍ ظاهرين في
نافذته (إلى الفعل التالي).
"""

from __future__ import annotations

import gzip
import json
import sys
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any

from slge.cells import index
from slge.filiyya import (
    WITNESSES,
    Filiyya,
    admissible,
    has_object,
    has_subject,
    naib_kind,
    order,
    past_ending,
    sort_fadla,
)
from slge.tawabi import case_class

ROOT = Path(__file__).resolve().parent.parent
TARGET = ROOT / "FILIYYA_INDEX.md"
SLICE = ROOT / "tests" / "data" / "masaq-filiyya.json.gz"
KEEP = ("PREP", "IMPERF_PREF", "IV3MP", "IV3MS", "DET")
VERBS = ("فعل ماضٍ", "فعل مضارع", "فعل أمر", "فعل ماضٍ مبني للمجهول", "فعل مضارع مبني للمجهول")
Word = tuple[tuple[str, str], ...]


def _cells(r: dict[str, Any], keep: tuple[str, ...] = KEEP, suffix: bool = False) -> Word:
    pre = [(a, b) for t, cs in r["pre"] for a, b in cs if t in keep]
    suf = [(a, b) for _, cs in r["suf"] for a, b in cs] if suffix else []
    return (*pre, *((a, b) for a, b in r["stem"]), *suf)


def _rows() -> list[dict[str, Any]]:
    with gzip.open(SLICE, "rt", encoding="utf-8") as f:
        rows: list[dict[str, Any]] = json.load(f)["rows"]
    return rows


def triples() -> list[tuple[dict[str, Any], dict[str, Any] | None, dict[str, Any] | None]]:
    rows = _rows()
    by: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for r in rows:
        by[str(r["ref"])].append(r)
    out: list[tuple[dict[str, Any], dict[str, Any] | None, dict[str, Any] | None]] = []
    for verse in by.values():
        verse.sort(key=lambda r: int(str(r["pos"])))
        idx = [i for i, r in enumerate(verse) if r["role"] in VERBS]
        used: set[int] = set()
        for n, i in enumerate(idx):
            lo = idx[n - 1] if n > 0 else -1
            hi = idx[n + 1] if n + 1 < len(idx) else len(verse)
            f = next((r for r in verse[i + 1:hi] if r["role"] == "فاعل"), None)
            mi = next((j for j in range(i + 1, hi) if verse[j]["role"] == "مفعول به"), None)
            if mi is None:  # المفعولُ قبل الفعل (صدارة): بين الفعل السابق وهذا الفعل، ما لم يُؤخذ
                mi = next((j for j in range(lo + 1, i)
                           if verse[j]["role"] == "مفعول به" and j not in used), None)
            if mi is not None:
                used.add(mi)
            out.append((verse[i], f, verse[mi] if mi is not None else None))
    return out


def measure() -> dict[str, object]:
    rows = _rows()
    endings: Counter[tuple[str, str]] = Counter()
    subj: Counter[tuple[str, bool]] = Counter()
    obj: Counter[tuple[str, bool]] = Counter()
    naib: Counter[str] = Counter()
    zarf: Counter[tuple[str, str]] = Counter()
    fadla: Counter[tuple[str, str]] = Counter()
    sym = {"فتح": "الفتحة", "كسر": "الكسرة", "ضم": "الضمة", "سكون": "السكون", "—": "—"}
    for r in rows:
        role = str(r["role"])
        if role in VERBS:
            vw = _cells(r, suffix=True)
            tags = tuple(str(t) for t, _ in r["suf"])
            has_s = any(t.startswith(("SUBJ", "PVSUFF_SUBJ", "IVSUFF_SUBJ")) for t in tags)
            has_o = any(t.startswith("OBJ") for t in tags)
            subj[(role, has_subject(vw) == has_s)] += 1
            obj[(role, has_object(vw) == has_o)] += 1
            if role == "فعل ماضٍ":
                suf = tuple((a, b) for t, cs in r["suf"] for a, b in cs
                            if str(t).startswith(("SUBJ", "PVSUFF_SUBJ")))
                endings[(str(r["marker"]), sym[past_ending(suf)])] += 1
        elif role == "نائب فاعل":
            naib[naib_kind(_cells(r))] += 1
        elif role in ("ظرف زمان", "ظرف مكان"):
            zarf[(role, case_class(_cells(r)))] += 1
    rutba: Counter[tuple[str, str, bool]] = Counter()
    verbs = {(str(r["ref"]), int(str(r["pos"]))): r for r in rows if r["role"] in VERBS}
    for v, f, m in triples():
        vc = _cells(v, suffix=True)
        fc: Word = _cells(f, ("DET",)) if f else ()
        mc: Word = _cells(m, ("DET",), suffix=True) if m else ()
        vpos = int(str(v["pos"]))
        if m and int(str(m["pos"])) < vpos:
            pos = "س٢ ف س١"
        elif has_object(vc) and not has_subject(vc):
            pos = "ف س٢ س١"  # المفعولُ المتّصل قبل كلّ ظاهر
        elif f and m:
            pos = "ف س١ س٢" if int(str(f["pos"])) < int(str(m["pos"])) else "ف س٢ س١"
        else:
            pos = "ف س١ س٢"
        j = Filiyya(vc, fc, mc, pos)
        kind = "ثلاثيّ" if f and m else "فاعلٌ ظاهر" if f else "مفعولٌ ظاهر" if m else "الفعلُ وحدَه"
        rutba[(kind, order(j), admissible(j))] += 1
    for r in rows:
        if r["role"] in ("مفعول لأجله", "مفعول مطلق"):
            prev = next((verbs[(str(r["ref"]), p)] for p in range(int(str(r["pos"])) - 1, 0, -1)
                         if (str(r["ref"]), p) in verbs), None)
            vc = _cells(prev, suffix=True) if prev else ()
            fadla[(str(r["role"]), sort_fadla(_cells(r), vc))] += 1
    return {"n": len(rows), "endings": endings, "subj": subj, "obj": obj, "naib": naib,
            "zarf": zarf, "fadla": fadla, "rutba": rutba, "triples": len(triples())}


def _w(w: Word) -> str:
    return "-".join(str(index(c)) for c in w)


def render() -> str:
    m = measure()
    endings: Counter[tuple[str, str]] = m["endings"]  # type: ignore[assignment]
    subj: Counter[tuple[str, bool]] = m["subj"]  # type: ignore[assignment]
    obj: Counter[tuple[str, bool]] = m["obj"]  # type: ignore[assignment]
    naib: Counter[str] = m["naib"]  # type: ignore[assignment]
    zarf: Counter[tuple[str, str]] = m["zarf"]  # type: ignore[assignment]
    fadla: Counter[tuple[str, str]] = m["fadla"]  # type: ignore[assignment]
    rutba: Counter[tuple[str, str, bool]] = m["rutba"]  # type: ignore[assignment]
    ok = sum(v for (_, _, a), v in rutba.items() if a)
    agree_end = sum(v for (a, b), v in endings.items() if a == b)
    lines = [
        "# فهرسُ الجملة الفعليّة على درجات الترخيص التدريجيّ",
        "",
        "مولَّدٌ بـ`python tools/gen_filiyya_index.py` من `src/slge/filiyya.py`؛ لا يُحرَّر باليد. "
        "البرهانُ: "
        "`formal/Slge/Filiyya.lean`.",
        "",
        "## د٤ الخانة — الفعلُ ثلاثُ حالات، والفاعلُ ثلاثُ صور", "",
        "الماضي مبنيٌّ وآخرُه تقرؤه لاحقتُه: فتحٌ بلا لاحقة، سكونٌ قبل التاء ونَا ونون النسوة، ضمٌّ قبل واو "
        "الجماعة (`pastEnding` على جدول `Damair.rafSuffixes`؛ `past_endings`)، والماضي بلاحقته "
        "مرخَّصٌ لكلّ "
        "جذعٍ سالم (`past_licensed`). المضارعُ معربٌ بعلاماتٍ ثلاثٍ عمليّاتٍ ثلاثٍ مبرهَنةٍ في "
        "`Jazm` و`Afal`. "
        "الأمرُ مبنيٌّ على ما يُجزم به مضارعُه: آخرُ كلّ قالب أمرٍ مودَعٍ ساكنٌ كآخر `Jazm.sukun` "
        "(`amr_ends_like_jazm`). الفاعلُ رفعٌ يُقرأ لكلّ جذع (`fail_reads_raf`)؛ البارزُ المتّصل "
        "لاحقةٌ من "
        "الجدول بحالة ما قبلها — لكلّ فعلٍ (`attached_subject`)، والمستترُ لا خانةَ له، والمصدرُ "
        "المؤوّل تيار.",
        "",
        "## د٨ الحدّ — رتبُ التباديل من الخانات لا من الموضع", "",
        "الرتبةُ دالّةٌ في الخانات (`order`؛ `order_swap`): الفاعلُ متّصلٌ بالفعل ⇒ الفاعلُ أوّلًا لكلّ فعلٍ "
        "ومفعول (`attached_subject_first`)؛ المفعولُ متّصلٌ ⇒ المفعولُ أوّلًا لكلّ فعلٍ وفاعل "
        "(`attached_object_first`)؛ الضميرُ العائدُ في الفاعل ⇒ المفعولُ أوّلًا؛ خفاءُ العلامة في "
        "الطرفين ⇒ "
        "الفاعلُ أوّلًا؛ اسمُ الصدارة ⇒ قبل الفعل؛ وما سواه جواز. الحصرُ بإلّا تيار.",
        "",
        "| الجملة | الفعل | الفاعل | المفعول | الرتبة |", "|---|---|---|---|---|",
        *[f"| {n} | `{_w(j.fil)}` | `{_w(j.fail)}` | `{_w(j.maful)}` | {order(j)} |"
          for n, j in WITNESSES.items()],
        "",
        "## د١٦ — النيابةُ عمليّتان، والمفاعيلُ نصبٌ وقراءة", "",
        "المبنيُّ للمجهول عمليّتان على الحالات لا الحروف (ضمُّ الأوّل وكسرُ ما قبل الآخر؛ "
        "`majhul`): فَعَلَ ← فُعِلَ "
        "ويَفْعَلُ ← يُفْعَلُ لكلّ جذر بقالبي الشبكة (`majhul_fill`). نائبُ الفاعل بالرفع نفسِه "
        "(`naib_eq_fail`)، "
        "وصورُه الأربع يقرؤها الجدولُ والصدرُ (`naibKind`؛ الترتيبُ معلَن). المفعولُ نصبٌ فتنوين "
        "يُقرأ نصبًا لكلّ "
        "جذع (`maful_reads_nasb`). المفعولُ فيه من جداول الظروف منصوبًا (`zarf_reads_nasb`)؛ "
        "والمختصُّ خارج "
        "الجدول — معجم. المفعولُ لأجله مصدرٌ على قالبه لا مشتقٌّ (`sorting_masdar_hal`: رَغْبَةً/رَاغِبًا). "
        "والمطلقُ مصدرٌ بجذر الفعل بعينه (`sortFadla`: ضَرَبْتُ ضَرْبًا). "
        "المفعولُ معه واوٌ متّصلةٌ فنصب يحفظ الترخيص (`maiyya_licensed`)؛ المشاركةُ على تَفَاعَلَ عطفٌ "
        "(`tafaala_is_ataf`) وما سواه معجم. المفعولُ المطلق مصدرُ الفعل بجذره: الجذرُ يُستردّ منه "
        "لكلّ جذر "
        "(`mutlaq_shares_root`).",
        "",
        "## القياس على MASAQ", "",
        f"على {m['n']:,} كلمةً (أفعالُ المصحف وعُمدُها وفضلاتُها بشهادات البوّابة).", "",
        f"### آخرُ الماضي قبل اللاحقة: علامةُ MASAQ × قراءةُ اللاحقة — متوافقٌ {agree_end:,}", "",
        "| علامة MASAQ | قراءةُ اللاحقة | العدد |", "|---|---|---|",
        *[f"| {a} | {b} | {v} |" for (a, b), v in endings.most_common()],
        "",
        "الفتحةُ المقدَّرة (قَالَ، رَمَى) والضمّةُ المقدَّرة (رَمَوْا): الآخرُ معتلٌّ — الخانةُ تقرأ اللاحقةَ لا "
        "الحركةَ المقدَّرة؛ موافقةٌ بالاسم. والمخالفُ (سكونٌ/فتحة): تاءُ التأنيث الساكنة ونونُ النسوة بعد "
        "فتحٍ مقدَّر — بقيّةٌ مسمّاة.",
        "",
        "### الفاعلُ والمفعولُ المتّصلان: القارئُ × وسمُ MASAQ", "",
        "| الفعل | الفاعلُ المتّصل موافق | العدد |", "|---|---|---|",
        *[f"| {a} | {'نعم' if b else 'لا'} | {v} |" for (a, b), v in sorted(subj.items())],
        "",
        "| الفعل | المفعولُ المتّصل موافق | العدد |", "|---|---|---|",
        *[f"| {a} | {'نعم' if b else 'لا'} | {v} |" for (a, b), v in sorted(obj.items())],
        "",
        f"### الرتبة: القارئُ مقابل موضع المصحف — المقبولُ {ok:,} من {m['triples']:,}", "",
        "| الجملة | رتبةُ القارئ | مقبول | العدد |", "|---|---|---|---|",
        *[f"| {a} | {b} | {'نعم' if c else 'لا'} | {v} |" for (a, b, c), v in rutba.most_common()],
        "",
        "الموضعُ: المفعولُ المتّصلُ قبل كلّ ظاهر؛ والمفعولُ قبل الفعل إن سبقه في الآية. ما رُفض: مَا/مَنْ "
        "موصولتين أو شرطيّتين تقرؤهما الخانةُ استفهامًا (صورةٌ واحدة)، وفاعلٌ بعد فعلٍ فيه لاحقةُ فاعلٍ "
        "(البدلُ والتوكيد — تيار).",
        "",
        "### نائبُ الفاعل بالقارئ", "",
        "| الصورة | العدد |", "|---|---|",
        *[f"| {a} | {v} |" for a, v in naib.most_common()],
        "",
        "### الظرفُ وحالتُه المقروءة", "",
        "| الدور | الحالة | العدد |", "|---|---|---|",
        *[f"| {a} | {b} | {v} |" for (a, b), v in zarf.most_common()],
        "",
        "ما لا تقرؤه الخانة من الظروف: المبنيُّ (إِذْ، إِذَا، حِينَئِذٍ) والمعتلُّ الآخر؛ والمرفوعُ المقطوعُ "
        "(قَبْلُ، بَعْدُ) بقراءة `Zuruf.qat`.",
        "",
        "### المفعولُ لأجله والمطلق بقانون الفرز", "",
        "| الدور | القارئ | العدد |", "|---|---|---|",
        *[f"| {a} | {b} | {v} |" for (a, b), v in fadla.most_common()],
        "",
        "## ما لا تقرؤه الخانة — باسمه", "",
        "- الفاعلُ المستتر: لا خانةَ له (زَيْدٌ قَامَ)؛ والمصدرُ المؤوّل فاعلًا: تيار.",
        "- نونُ النسوة ونونُ الأصل (سَكَنَ)، وكافُ الخطاب وكافُ الأصل، وياءُ المخاطبة وياءُ المتكلّم بلا نون "
        "وقاية: الخانةُ تقرؤها بحالة ما قبلها؛ وما بقي معجم.",
        "- الحصرُ بإلّا وإنّما في الرتبة: تيار. والمفعولُ الثاني والثالث (ظنّ وأخواتها): `Nawasikh`.",
        "- اسمُ المصدر (الدَّرْس) والمصدرُ على قالبٍ واحد؛ والمختصُّ من الظروف (المسجد)؛ وفعلُ "
        "المشاركة خارج "
        "تَفَاعَلَ (اشْتَرَكَ): معجم.",
        "- ترتيبُ النائب (المفعولُ قبل المجرور قبل الظرف قبل المصدر): معلَن.",
        "- شريحةُ MASAQ: 2,644 كلمةً مستبعَدة (مرفوضٌ بالاسم 1,556، عدٌّ مخالف 740، غيرُ محاذاة 348).",
        "",
    ]
    return "\n".join(lines)


def main() -> int:
    text = render()
    if "--check" in sys.argv:
        if TARGET.read_text(encoding="utf-8") != text:
            sys.stderr.write("FILIYYA_INDEX.md غيرُ مطابق؛ شغّل tools/gen_filiyya_index.py\n")
            return 1
        sys.stdout.write("FILIYYA_INDEX.md مطابق\n")
        return 0
    TARGET.write_text(text, encoding="utf-8")
    sys.stdout.write("كُتب FILIYYA_INDEX.md\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
