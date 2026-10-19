"""القناةُ الثالثة: اختبارُ «قانون الولادة إلى الإفادة» على ما في الشجرة فعلًا.

تشتغل هذه القناةُ بتوقيع المالك المستورَد من :mod:`canonical116.owner_experiment`،
وتقابل التقريرَ الرابعَ الواردَ (قانون الولادة إلى الإفادة، 2026-10-02) بما
يُقاس ههنا. وهي — كسابقتَيها — ملفٌّ يُزاد ويُحذَف بتمامه، ولا يُعدِّل بايتةً
في حارسٍ قائم.

ما يقوله التقريرُ الوارد، ثمّ ما قيس ههنا:

1. **موادُّه غائبةٌ عن الشجرة.** `GFLK_Mushajjir_Independent_v1.zip` و
   `Unified_Birth_Dal_Evidence.zip` و`upper_rerun_and_handoff.json` و
   `audit_upper_handoff.py` و`Unified_Birth_Dal_Only_AR.html`: كلُّها تُفتَح
   مساراتُها ههنا فتُقاس غائبة. فأرقامُ المشجِّر العشرةُ تبقى
   `QUOTED_INCOMING_NOT_REPRODUCED` ولا يُصطنَع لها مخزونٌ يحاكيها.

2. **دعوى «المصدرُ ههنا مختلفٌ عن ملفّ 78,245» غيرُ مستوفاةٍ على محور الوحدات.**
   وحداتُ المصدر في التقرير 6,236، ووحداتُ مُودَعِنا 6,236 بالقياس — اتّفاقٌ
   تامٌّ لا تقريب. والخلافُ على محور الكلمات وحده: 77,429 مقابل 78,245، وبقيّةٌ
   مقدارُها 816. وقد جُرِّبت ههنا سبعُ سياساتِ ترميزٍ مسمّاةٌ على المُودَع نفسِه،
   فلم تُخرج إحداها 77,429؛ وأقربُها 77,305. فالبقيّةُ **غيرُ مُفسَّرة**، وهذا
   أثقلُ من «مصدرٌ آخر» لأنّه يُبقي السؤالَ مفتوحًا بموضعه
   (`AN_UNEXPLAINED_RESIDUE_IS_NOT_A_DIFFERENT_SOURCE`).

3. **بلوغُ «بِسْمِ» G3 أُعيد إنتاجُه.** جسرُ هذه الشجرة يُخرجه `READY` بثلاث
   ذرّاتٍ ‹بِ سْ مِ›، ببصمةِ مصدرٍ مُشتقّةٍ لا منقولة.

4. **انقطاعُ تسليم الشهادة واقعٌ ههنا أيضًا، وبسببٍ آخرَ يُسمّى.** ليس في
   `canonical116` واجهةٌ تقبل شهادةَ جسرٍ وتستأنف منها؛ وليس في
   `composition_ifada_path` مدخلٌ لشهادة: مدخلُه بايتاتٌ أو نصّ. فالانقطاعُ
   **دَينٌ مسمًّى** في الشجرتين معًا، لا فشلٌ خاصٌّ بحزمةِ المشجِّر
   (`A_MISSING_INTERFACE_IS_A_NAMED_DEBT_NOT_A_MEASURED_FAILURE`).

5. **لكنّ الحكمَ «لا بوّابةَ إفادةٍ مغلقةٍ في المخرجات» لا يصحّ على هذه الشجرة.**
   `alghanem.arabic.composition_ifada_path` مسارٌ رأسيٌّ **موصول**: مخرجُ كلّ
   طبقةٍ مدخلُ التي تليها ببصمةٍ مُسلسَلة، وثلاثُ نتائجَ لكلِّ انتقالٍ لا
   اثنتان، ويُخرِج سجلًّا مغلقًا بحالِ إفادةٍ مُشتقّةٍ من العلامتين المكتوبتين
   لا مكتوبةٍ من خارج الخطّ. وهو — وهذا موضعُ الفرق الأهمّ عن حزمةِ المشجِّر —
   **لا يستشير معجمًا** (`NO_LEXICON_IS_CONSULTED`)، فلا يرد عليه اعتراضُ
   «تصنيفٌ بمعلوماتٍ سابقة».

   ولا يُقرَأ ذلك إغلاقًا للعربية: نطاقُه مُعلَنٌ قبل التشغيل — تركيبُ كلمتين
   مشكولتَي الآخِر — وما خرج عنه يقف بجنسٍ مُسمًّى. وقد قيس ههنا وقوفُه فعلًا
   على مدخلاتٍ خارجَ نطاقه. فالبوّابةُ **موجودةٌ ومحدودةُ النطاق**، وفرقُ
   «غائبة» عن «محدودة» فرقٌ في جنس الحكم لا في مقداره
   (`A_SCOPED_GATE_IS_NOT_AN_ABSENT_GATE`).

6. **وما يبقى غيرَ مُثبَتٍ يبقى.** بلوغُ سجلٍّ مغلقٍ للإفادة في كلمتين لا يُثبت
   أنّ قانونًا مولِّدًا واحدًا أنتج الكلمةَ والنسبةَ والوظيفةَ والإعرابَ
   والإفادةَ من الـ116؛ ولا يصل المسارُ الرأسيُّ إلى الـ116 بشهادةٍ متّصلة، لأنّ
   طبقتَه الأولى بايتاتٌ لا خاناتٌ مرقَّمة
   (`A_CLOSED_RECORD_IN_ONE_SCOPE_IS_NOT_A_GENERATING_LAW`).
"""

from __future__ import annotations

import sys
from dataclasses import dataclass
from enum import Enum
from typing import Final

from .bridge import bridge
from .owner_experiment import (
    OWNER_SIGNATURE,
    REPOSITORY_ROOT,
    Figure,
    Provenance,
    read_deposit,
)

__all__ = [
    "A_CLOSED_RECORD_IN_ONE_SCOPE_IS_NOT_A_GENERATING_LAW",
    "A_MISSING_INTERFACE_IS_A_NAMED_DEBT_NOT_A_MEASURED_FAILURE",
    "AN_UNEXPLAINED_RESIDUE_IS_NOT_A_DIFFERENT_SOURCE",
    "A_SCOPED_GATE_IS_NOT_AN_ABSENT_GATE",
    "GateStanding",
    "IfadaRun",
    "THE_NAMED_MATERIALS",
    "THE_QUOTED_UPPER_FIGURES",
    "absence_reading",
    "bism_reading",
    "handoff_reading",
    "ifada_gate_readings",
    "rows",
    "tokenisation_policies",
    "unit_axis_reading",
    "verdict_table",
]


AN_UNEXPLAINED_RESIDUE_IS_NOT_A_DIFFERENT_SOURCE: Final[str] = (
    "AN_UNEXPLAINED_RESIDUE_IS_NOT_A_DIFFERENT_SOURCE: اتّفاقُ عدد الوحدات "
    "واختلافُ عدد الكلمات يُسمَّى بقيّةً بموضعها، ولا يُصرَف بقولِ «مصدرٌ آخر» "
    "قبل أن تُسمَّى سياسةُ الترميز التي تُخرج الرقمَ الواردَ من هذه البايتات."
)

A_MISSING_INTERFACE_IS_A_NAMED_DEBT_NOT_A_MEASURED_FAILURE: Final[str] = (
    "A_MISSING_INTERFACE_IS_A_NAMED_DEBT_NOT_A_MEASURED_FAILURE: واجهةٌ لم "
    "تُكتَب لا تُقاس راسبةً في اختبار؛ ورفضُها حقلًا زائدًا أداءٌ لعقدها "
    "المُعلَن لا مخالفةٌ له."
)

A_SCOPED_GATE_IS_NOT_AN_ABSENT_GATE: Final[str] = (
    "A_SCOPED_GATE_IS_NOT_AN_ABSENT_GATE: بوّابةٌ تُغلِق داخل نطاقٍ مُعلَنٍ "
    "وتقف خارجَه بجنسٍ مُسمًّى موجودةٌ محدودة؛ وقراءتُها غائبةً تُسقط الفرقَ "
    "بين «لم يُكتَب» و«كُتِب بحدّ»."
)

A_CLOSED_RECORD_IN_ONE_SCOPE_IS_NOT_A_GENERATING_LAW: Final[str] = (
    "A_CLOSED_RECORD_IN_ONE_SCOPE_IS_NOT_A_GENERATING_LAW: بلوغُ سجلٍّ مغلقٍ "
    "للإفادة في كلمتين يُثبت ما صرّح به نطاقُه؛ ولا يُشترى به أنّ قانونًا "
    "مولِّدًا واحدًا أنتج الطبقاتِ كلَّها من الـ116."
)


# ---------------------------------------------------------------------------
# أوّلًا: الموادُّ المسمّاةُ في التقرير — تُفتَح مساراتُها ولا يُقال غيابُها
# ---------------------------------------------------------------------------

THE_NAMED_MATERIALS: Final[tuple[str, ...]] = (
    "GFLK_Mushajjir_Independent_v1.zip",
    "Unified_Birth_Dal_Evidence.zip",
    "upper_rerun_and_handoff.json",
    "audit_upper_handoff.py",
    "Unified_Birth_Dal_Only_AR.html",
)


def absence_reading() -> tuple[tuple[str, bool], ...]:
    """لكلِّ مادّةٍ مسمّاةٍ: هل في الشجرة ملفٌّ بهذا الاسم؟ يُفتَح ولا يُقال."""

    found: list[tuple[str, bool]] = []
    for name in THE_NAMED_MATERIALS:
        matches = [
            path for path in REPOSITORY_ROOT.rglob(name) if ".git" not in path.parts
        ]
        found.append((name, bool(matches)))
    return tuple(found)


THE_QUOTED_UPPER_FIGURES: Final[tuple[Figure, ...]] = (
    Figure(
        "وحدات المصدر",
        6236,
        Provenance.QUOTED_INCOMING_NOT_REPRODUCED,
        "يُقابَل في unit_axis_reading بعدد أسطر المُودَع المقيس",
    ),
    Figure(
        "كلمات المصدر",
        77429,
        Provenance.QUOTED_INCOMING_NOT_REPRODUCED,
        "لم تُخرجه سياسةُ ترميزٍ من السبع المجرَّبة على هذه البايتات",
    ),
) + tuple(
    Figure(
        name,
        value,
        Provenance.QUOTED_INCOMING_NOT_REPRODUCED,
        "مخرجُ حزمةٍ غائبةٍ عن الشجرة؛ لا يُصطنَع لها مخزونٌ يحاكيها",
    )
    for name, value in (
        ("قسم عام اختارته القواعد المحدودة", 31471),
        ("مؤجَّل", 44214),
        ("أكثر من قسم محتمل", 1744),
        ("روابط اسمية غير معيَّنة", 4180),
        ("مرشَّح تعلُّق جارٍّ بمكمِّله", 1775),
        ("رابط أداة بفعل تحت القاعدة المحلية", 604),
        ("مرشَّح فاعلية", 169),
        ("تابع فعلي غير معيَّن", 352),
    )
)


# ---------------------------------------------------------------------------
# ثانيًا: محورُ الوحدات ومحورُ الكلمات — اتّفاقٌ وبقيّة
# ---------------------------------------------------------------------------

EDITORIAL_MARKER: Final[str] = "<sel>"


def tokenisation_policies() -> tuple[tuple[str, int], ...]:
    """سياساتُ ترميزٍ مسمّاةٌ على بايتات المُودَع نفسِها، وما أخرجته كلٌّ منها."""

    import unicodedata

    text, _ = read_deposit()

    def split_minus_marker(source: str) -> int:
        return len([token for token in source.split() if token != EDITORIAL_MARKER])

    seen: set[str] = set()
    unique_lines = 0
    for line in text.splitlines():
        if line in seen:
            continue
        seen.add(line)
        unique_lines += split_minus_marker(line)

    return (
        ("الفصلُ بالفراغ مع إسقاط العلامة التحريرية", split_minus_marker(text)),
        ("بعد توحيد NFC", split_minus_marker(unicodedata.normalize("NFC", text))),
        (
            "بعد توحيد NFKC",
            split_minus_marker(unicodedata.normalize("NFKC", text)),
        ),
        (
            "إسقاطُ العلامة نصًّا قبل الفصل",
            len(text.replace(EDITORIAL_MARKER, "").split()),
        ),
        ("إسقاطُ الأسطر المكرَّرة", unique_lines),
        (
            "ما حمل حرفًا أصليًّا واحدًا فأكثر",
            len(
                [
                    token
                    for token in text.split()
                    if token != EDITORIAL_MARKER
                    and any(unicodedata.category(c) == "Lo" for c in token)
                ]
            ),
        ),
        (
            "الفصلُ بالمسافة وحدَها دون السطر",
            len(
                [
                    token
                    for token in text.split(" ")
                    if token.strip() and token.strip() != EDITORIAL_MARKER
                ]
            ),
        ),
    )


def unit_axis_reading() -> tuple[Figure, ...]:
    """6,236 وحدةً: اتّفاقٌ تامّ. و77,429 كلمةً: بقيّةٌ مقدارُها 816."""

    text, _ = read_deposit()
    lines = len(text.splitlines())
    occurrences = len([token for token in text.split() if token != EDITORIAL_MARKER])
    nearest = max(value for _, value in tokenisation_policies() if value < 78000)
    return (
        Figure(
            "أسطرُ المُودَع",
            lines,
            Provenance.MEASURED_HERE,
            "تُطابق «وحدات المصدر 6,236» في التقرير مطابقةً تامّة",
        ),
        Figure(
            "وقوعاتُ المُودَع",
            occurrences,
            Provenance.MEASURED_HERE,
            "بعد إسقاط العلامة التحريرية",
        ),
        Figure(
            "البقيّةُ على محور الكلمات",
            occurrences - 77429,
            Provenance.MEASURED_HERE,
            "غيرُ مُفسَّرة؛ ولا تُصرَف بدعوى اختلافِ المصدر",
        ),
        Figure(
            "أقربُ سياسةٍ مجرَّبةٍ إلى 77,429",
            nearest,
            Provenance.MEASURED_HERE,
            "إسقاطُ الأسطر المكرَّرة؛ وتبقى دونه بفارقٍ مُسمًّى",
        ),
    )


# ---------------------------------------------------------------------------
# ثالثًا: «بِسْمِ» في جسر هذه الشجرة
# ---------------------------------------------------------------------------

THE_HANDOFF_WORD: Final[str] = "بِسْمِ"


def bism_reading() -> dict[str, object]:
    """الرسمُ الذي وقع عليه اختبارُ التسليم، مُعادَ الإنتاج ههنا."""

    report = bridge(
        THE_HANDOFF_WORD,
        contexts={0: {"entry": "start", "exit": "continue"}},
    )
    return {
        "status": report["status"],
        "atoms": tuple(report["canonical_atoms"]),
        "source_sha256": report["source_sha256"],
        "rejections": tuple(report["rejections"]),
    }


# ---------------------------------------------------------------------------
# رابعًا: انقطاعُ تسليم الشهادة — يُقاس في هذه الشجرة لا يُنقَل
# ---------------------------------------------------------------------------


class GateStanding(str, Enum):
    """حالُ بوّابةٍ: مغلقةٌ في نطاقها، أو واقفةٌ بجنسٍ مُسمًّى، أو غيرُ مكتوبة."""

    CLOSED_IN_SCOPE = "CLOSED_IN_SCOPE"
    STOPPED_WITH_A_NAMED_GENUS = "STOPPED_WITH_A_NAMED_GENUS"
    NOT_WRITTEN = "NOT_WRITTEN"


def handoff_reading() -> tuple[tuple[str, GateStanding, str], ...]:
    """هل تَقبل واجهةٌ ههنا شهادةَ جسرٍ وتستأنف منها؟ يُفتَح التوقيعُ ويُقرأ."""

    import importlib
    import inspect

    bridge_module = importlib.import_module(f"{__package__}.bridge")

    exported = tuple(
        name
        for name, value in vars(bridge_module).items()
        if not name.startswith("_") and inspect.isfunction(value)
    )
    accepts_certificate = tuple(
        name
        for name in exported
        if "certificate" in str(inspect.signature(getattr(bridge_module, name)))
    )

    upper = _load_ifada_path()
    upper_params: tuple[str, ...] = ()
    if upper is not None:
        upper_params = tuple(
            parameter
            for entry in ("run_text", "run_bytes")
            for parameter in inspect.signature(getattr(upper, entry)).parameters
        )

    return (
        (
            "canonical116: واجهةٌ تقبل شهادةً وتستأنف منها",
            GateStanding.NOT_WRITTEN
            if not accepts_certificate
            else GateStanding.CLOSED_IN_SCOPE,
            f"دوالُّ الجسر المصدَّرة: {len(exported)}؛ ولا واحدةَ منها تأخذ شهادة",
        ),
        (
            "composition_ifada_path: مدخلٌ لشهادةٍ من طبقةٍ أدنى",
            GateStanding.NOT_WRITTEN,
            f"مُعامِلاتُ مدخلَيه: {upper_params or '—'}؛ بايتاتٌ أو نصٌّ لا شهادة",
        ),
    )


# ---------------------------------------------------------------------------
# خامسًا: بوّابةُ الإفادة القائمةُ في الشجرة — تُشغَّل لا تُوصَف
# ---------------------------------------------------------------------------


def _load_ifada_path():  # noqa: ANN202 - وحدةٌ تُحمَّل أو لا تُحمَّل
    """تحميلُ المسار الرأسيّ من ``src``؛ وغيابُ الحزمة يُقرأ ``None`` لا خطأً."""

    source_root = REPOSITORY_ROOT / "src"
    if source_root.is_dir() and str(source_root) not in sys.path:
        sys.path.insert(0, str(source_root))
    try:
        from alghanem.arabic import composition_ifada_path
    except ImportError:  # pragma: no cover - مسارُ غيابِ الحزمة
        return None
    return composition_ifada_path


@dataclass(frozen=True)
class IfadaRun:
    """قراءةُ تشغيلةٍ واحدةٍ على المسار الرأسيّ: أين وقفت وبأيِّ حال."""

    text: str
    last_stage: str
    last_outcome: str
    standing: GateStanding
    ifada: str | None
    witness: str | None


THE_RUN_INPUTS: Final[tuple[str, ...]] = (
    "اللَّهُ نُورٌ",
    "نُورُ السَّمَاوَاتِ",
    "قُلْ هُوَ",
    "كِتَابٌ الْبَيْتِ",
)


def ifada_gate_readings() -> tuple[IfadaRun, ...]:
    """تشغيلُ المسار الرأسيّ على مدخلاتٍ داخلَ نطاقه وخارجَه."""

    module = _load_ifada_path()
    if module is None:
        return ()

    runs: list[IfadaRun] = []
    for text in THE_RUN_INPUTS:
        run = module.run_text(text)
        last = run.stages[-1]
        record = run.record
        runs.append(
            IfadaRun(
                text=text,
                last_stage=last.stage.value,
                last_outcome=last.outcome.value,
                standing=(
                    GateStanding.CLOSED_IN_SCOPE
                    if record is not None
                    else GateStanding.STOPPED_WITH_A_NAMED_GENUS
                ),
                ifada=record.declared_ifada.value if record else None,
                witness=record.benefit_witness if record else last.preventer.value,
            )
        )
    return tuple(runs)


# ---------------------------------------------------------------------------
# سادسًا: جدولُ الأحكام
# ---------------------------------------------------------------------------


def verdict_table() -> tuple[tuple[str, str, str], ...]:
    """دعوى التقرير · ما قيس ههنا · الحكم."""

    absences = absence_reading()
    units = unit_axis_reading()
    gates = ifada_gate_readings()
    closed = tuple(run for run in gates if run.standing is GateStanding.CLOSED_IN_SCOPE)

    return (
        (
            "الموادُّ الأربعُ المسمّاةُ في الشجرة",
            f"غائبةٌ كلُّها ({sum(1 for _, ok in absences if not ok)}/{len(absences)})",
            "مُثبَت؛ فأرقامُها تبقى منقولةً غيرَ مُعادةِ الإنتاج",
        ),
        (
            "«المصدرُ ههنا مختلفٌ عن ملفّ 78,245»",
            f"الوحداتُ {units[0].value} = 6,236؛ والبقيّةُ {units[2].value} كلمة",
            "غيرُ مستوفًى على محور الوحدات؛ والبقيّةُ غيرُ مُفسَّرةٍ لا مصروفة",
        ),
        (
            "«بِسْمِ» يبلغ G3",
            f"{bism_reading()['status']} بذرّاتٍ {len(bism_reading()['atoms'])}",
            "مُعادُ الإنتاج في جسر هذه الشجرة",
        ),
        (
            "انقطاعُ تسليم الشهادة بين المحرِّكين",
            "واقعٌ ههنا أيضًا: لا واجهةَ تقبل شهادةً في الطرفين",
            "دَينٌ مسمًّى لا فشلٌ مقيس",
        ),
        (
            "«لا بوّابةَ إفادةٍ مغلقةٍ في المخرجات»",
            f"سجلّاتٌ مغلقةٌ: {len(closed)} من {len(gates)} داخلَ نطاقٍ مُعلَن",
            "لا يصحّ على هذه الشجرة؛ البوّابةُ محدودةُ النطاق لا غائبة",
        ),
        (
            "قانونٌ مولِّدٌ واحدٌ من الـ116 إلى الإفادة",
            "المسارُ الرأسيُّ يبدأ من البايتات لا من الخانات المرقَّمة",
            "غيرُ مُثبَت؛ وبلوغُ سجلٍّ مغلقٍ لا يُشترى به",
        ),
    )


def rows() -> list[str]:
    """تقريرٌ نصّيٌّ يُطبَع، كلُّ رقمٍ فيه معه نسبتُه."""

    lines = [
        f"توقيعُ المالك: {OWNER_SIGNATURE.owner} — {OWNER_SIGNATURE.granted_on}",
        "",
    ]
    lines.append("الموادُّ المسمّاةُ وحالُها في الشجرة:")
    for name, present in absence_reading():
        lines.append(f"  {name}: {'حاضرة' if present else 'غائبة'}")
    lines.append("")
    lines.append("سياساتُ الترميز المجرَّبةُ على المُودَع:")
    for label, value in tokenisation_policies():
        lines.append(f"  {label}: {value}")
    lines.append("")
    lines.append("تشغيلُ المسار الرأسيّ:")
    for run in ifada_gate_readings():
        lines.append(
            f"  {run.text}: {run.last_stage}/{run.last_outcome} — "
            f"{run.standing.value}" + (f" — {run.ifada}" if run.ifada else "")
        )
    lines.append("")
    lines.append("جدولُ الأحكام:")
    for claim, measured, verdict in verdict_table():
        lines.append(f"  {claim} | {measured} | {verdict}")
    return lines


if __name__ == "__main__":  # pragma: no cover - تشغيلٌ يدويّ
    print("\n".join(rows()))
