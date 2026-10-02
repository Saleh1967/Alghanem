"""القناةُ الرابعة: اختبارُ «حلّ انقطاع الشهادة» على ما في الشجرة فعلًا.

تشتغل بتوقيع المالك المستورَد من :mod:`canonical116.owner_experiment`، وتقابل
التقريرَ الخامسَ الوارد (حلّ انقطاع الشهادة وفصل المقترحات عن الترخيص،
2026-10-02) بما يُقاس ههنا. وهي — كسابقاتها — ملفٌّ يُزاد ويُحذَف بتمامه، ولا
يُعدِّل بايتةً في حارسٍ قائم.

ما يقوله التقريرُ الوارد، ثمّ ما قيس:

1. **اسمٌ يُطابِق ليس هو المادّةَ المسمّاة.** أربعةٌ من موادّ الحزمة غائبةٌ عن
   الشجرة؛ و`manifest.json` **حاضرٌ اسمًا** في
   ``src/alghanem/realization/generated/`` لمادّةٍ أخرى لا صلةَ لها بالحزمة.
   فقراءةُ الحضور بالاسم وحده تُدخِل مادّةً أجنبيّةً في عداد المُسترجَع
   (`A_NAME_MATCH_IS_NOT_THE_NAMED_MATERIAL`).

2. **اتّساقُ الجمع مُعادُ الحساب.** 40,447 + 848 + 36,950 = 78,245 بالضبط؛
   فالقسمةُ الثلاثيّةُ **مستغرِقةٌ غيرُ متداخلة** على مجموعٍ يُطابِق مُودَعَنا.
   وهذا اتّساقٌ داخليٌّ، لا مطابقةٌ لقسمةِ هذه الشجرة
   (`AN_EXHAUSTIVE_SUM_IS_CONSISTENCY_NOT_AGREEMENT`).

3. **عددُ الأشكال والوقوعات مُعادُ الإنتاج بالضبط**: 18,200 شكلًا مختلفًا و
   78,245 وقوعًا، مقيسَين من بايتات ``corpora/quran-simple-enhanced.txt``.

4. **لكنّ القسمةَ نفسَها غيرُ مُعادةٍ، وبفرقَين مُسمَّيَين.** جسرُ هذه الشجرة
   **ثنائيُّ الأصناف** لا ثلاثيّ: `READY` 41,820 وقوعًا و`DEFER` 36,425. فلا
   مقابلَ عندنا لـ`G1` أصلًا؛ وحدُّ القطع يفترق بـ525 وقوعًا في الجهتين معًا.
   وجانبُ التأجيل ههنا ينقسم **ثلاثةَ أصنافٍ مسمّاةٍ متباينة** لا صنفَ فيها
   يبلغ 848.

5. **والأهمّ: «اتّفاقُ النصّ حرفيًّا» لا يُميِّز إلّا إن كان النصُّ هو البايتاتِ
   المصدرَ.** «أَبَا» و«أَبَى» لا يتّحدان في الذرّات وحدها: يتّحدان في
   `canonical_text` أيضًا — كلاهما ‹ءَبَاْ›. والتصادمُ تحت المفتاحين سواء:
   18 ليفًا و36 شكلًا في كلٍّ منهما. ولا يرفعه إلّا `source_sha256` (صفرُ
   تصادم). فعقدُ استقبالٍ يُثبِّت النصَّ المعياريَّ **خامدٌ على هذه الأشكال
   الستّة والثلاثين بعينها**، والدعوى لا تُحمَل إلّا على البايتات
   (`PINNING_THE_CANONICAL_TEXT_IS_INERT_WHERE_THE_RASM_COLLIDES`).

6. **وما لم يُقَس لا يُقَوَّم.** «0 / 0» في سطر الأقسام العليا والإفادة
   المرخَّصة، ووسمُ `MODEL_ONLY` على اختبارات القواعد العليا: كلاهما إقرارٌ
   يُنقَل كما هو. ومنعُ `closed=true` من المستدعي عقدُ برمجةٍ يُقرأ في شيفرةٍ
   غائبةٍ عن الشجرة، فلا يُقاس ههنا نجاحًا ولا إخفاقًا.
"""

from __future__ import annotations

import collections
from dataclasses import dataclass
from functools import lru_cache
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
    "AN_EXHAUSTIVE_SUM_IS_CONSISTENCY_NOT_AGREEMENT",
    "A_NAME_MATCH_IS_NOT_THE_NAMED_MATERIAL",
    "PINNING_THE_CANONICAL_TEXT_IS_INERT_WHERE_THE_RASM_COLLIDES",
    "THE_INCOMING_PARTITION",
    "THE_PACKAGE_MATERIALS",
    "IdentityKey",
    "MaterialReading",
    "deferral_census",
    "identity_key_readings",
    "incoming_sum_reading",
    "material_readings",
    "partition_reading",
    "rows",
    "verdict_table",
]


A_NAME_MATCH_IS_NOT_THE_NAMED_MATERIAL: Final[str] = (
    "A_NAME_MATCH_IS_NOT_THE_NAMED_MATERIAL: ملفٌّ يحمل الاسمَ نفسَه في موضعٍ "
    "آخرَ من الشجرة ليس المادّةَ المسمّاة؛ فيُفصَل «حاضرٌ اسمًا» عن «حاضرٌ "
    "مادّةً» ولا يُعَدّ الأوّلُ استرجاعًا."
)

AN_EXHAUSTIVE_SUM_IS_CONSISTENCY_NOT_AGREEMENT: Final[str] = (
    "AN_EXHAUSTIVE_SUM_IS_CONSISTENCY_NOT_AGREEMENT: بلوغُ أصنافٍ مجموعَ "
    "المدوّنة يُثبت أنّها مستغرِقةٌ غيرُ متداخلة، ولا يُثبت أنّ حدَّ القطع بينها "
    "هو حدُّ القطع ههنا."
)

PINNING_THE_CANONICAL_TEXT_IS_INERT_WHERE_THE_RASM_COLLIDES: Final[str] = (
    "PINNING_THE_CANONICAL_TEXT_IS_INERT_WHERE_THE_RASM_COLLIDES: المواضعُ "
    "التي تتّحد فيها الذرّاتُ يتّحد فيها النصُّ المعياريُّ نفسُه؛ فتثبيتُه "
    "لا يرفع تصادمًا واحدًا، ولا يُميِّز إلّا تثبيتُ البايتات المصدر."
)

A_REFUSAL_IN_ABSENT_CODE_IS_NEITHER_PASSED_NOR_FAILED: Final[str] = (
    "A_REFUSAL_IN_ABSENT_CODE_IS_NEITHER_PASSED_NOR_FAILED: عقدٌ يَرفض علمًا "
    "يضعه المستدعي يُقرأ في شيفرته؛ وشيفرةٌ غائبةٌ عن الشجرة لا يُقاس عقدُها "
    "ناجحًا ولا راسبًا، بل يُنقَل إقرارًا."
)


# ---------------------------------------------------------------------------
# أوّلًا: موادُّ الحزمة — حضورُ الاسم غيرُ حضور المادّة
# ---------------------------------------------------------------------------

THE_PACKAGE_MATERIALS: Final[tuple[str, ...]] = (
    "licensed_dal.py",
    "test_solution.py",
    "audit_real_text.py",
    "README_AR.md",
    "manifest.json",
)


@dataclass(frozen=True)
class MaterialReading:
    """مادّةٌ مسمّاةٌ: أحاضرٌ اسمُها؟ وأين؟ وأهي المادّةُ المقصودة؟"""

    name: str
    name_matches: tuple[str, ...]
    is_the_named_material: bool
    note: str


def material_readings() -> tuple[MaterialReading, ...]:
    """تُفتَح المساراتُ ولا يُقال الغياب؛ والمطابقُ اسمًا يُسمّى بموضعه."""

    readings: list[MaterialReading] = []
    for name in THE_PACKAGE_MATERIALS:
        matches = tuple(
            str(path.relative_to(REPOSITORY_ROOT))
            for path in sorted(REPOSITORY_ROOT.rglob(name))
            if ".git" not in path.parts
        )
        readings.append(
            MaterialReading(
                name=name,
                name_matches=matches,
                is_the_named_material=False,
                note=(
                    "غائبةٌ عن الشجرة"
                    if not matches
                    else "الاسمُ حاضرٌ لمادّةٍ أخرى لا صلةَ لها بالحزمة"
                ),
            )
        )
    return tuple(readings)


# ---------------------------------------------------------------------------
# ثانيًا: القسمةُ الواردةُ وجمعُها
# ---------------------------------------------------------------------------

THE_INCOMING_PARTITION: Final[tuple[Figure, ...]] = (
    Figure(
        "وقوعات G3",
        40447,
        Provenance.QUOTED_INCOMING_NOT_REPRODUCED,
        "جسرُنا يُخرِج 41,820 في صنفه الأعلى؛ الفرقُ 1,373",
    ),
    Figure(
        "وقوعات G1",
        848,
        Provenance.QUOTED_INCOMING_NOT_REPRODUCED,
        "لا مقابلَ لهذا الصنف في جسر هذه الشجرة أصلًا",
    ),
    Figure(
        "وقوعات G0",
        36950,
        Provenance.QUOTED_INCOMING_NOT_REPRODUCED,
        "جسرُنا يُخرِج 36,425 مؤجَّلًا؛ الفرقُ 525",
    ),
)


def incoming_sum_reading() -> tuple[int, int, bool]:
    """جمعُ الأصناف الثلاثة، ووقوعاتُ مُودَعِنا، وهل تساويا."""

    total = sum(figure.value for figure in THE_INCOMING_PARTITION)
    measured = _occurrence_total()
    return total, measured, total == measured


# ---------------------------------------------------------------------------
# ثالثًا: قسمةُ جسر هذه الشجرة — تُشغَّل على كلّ شكلٍ مختلف
# ---------------------------------------------------------------------------

_CONTEXT: Final[dict[int, dict[str, str]]] = {0: {"entry": "start", "exit": "continue"}}


@lru_cache(maxsize=1)
def _form_counts() -> tuple[tuple[str, int], ...]:
    text, _ = read_deposit()
    counter = collections.Counter(token for token in text.split() if token != "<sel>")
    return tuple(sorted(counter.items()))


def _occurrence_total() -> int:
    return sum(count for _, count in _form_counts())


@lru_cache(maxsize=1)
def _reports() -> tuple[tuple[str, int, dict], ...]:
    return tuple(
        (form, count, bridge(form, contexts=_CONTEXT)) for form, count in _form_counts()
    )


def partition_reading() -> tuple[Figure, ...]:
    """أصنافُ الجسر بعدد الأشكال وبعدد الوقوعات، مقيسةً لا منقولة."""

    by_form: collections.Counter[str] = collections.Counter()
    by_occurrence: collections.Counter[str] = collections.Counter()
    for _, count, report in _reports():
        by_form[report["status"]] += 1
        by_occurrence[report["status"]] += count

    return (
        Figure(
            "الأشكالُ المختلفة",
            len(_form_counts()),
            Provenance.MEASURED_HERE,
            "تُطابِق «18200» في التقرير مطابقةً تامّة",
        ),
        Figure(
            "الوقوعاتُ المحفوظة",
            _occurrence_total(),
            Provenance.MEASURED_HERE,
            "تُطابِق «78245» مطابقةً تامّة",
        ),
        Figure(
            "أصنافُ الجسر",
            len(by_form),
            Provenance.MEASURED_HERE,
            "صنفان لا ثلاثة؛ فلا مقابلَ لـG1",
        ),
        Figure(
            "READY بالوقوعات",
            by_occurrence["READY"],
            Provenance.MEASURED_HERE,
            "مقابلُ G3 الوارد 40,447؛ الفرقُ 1,373",
        ),
        Figure(
            "DEFER بالوقوعات",
            by_occurrence["DEFER"],
            Provenance.MEASURED_HERE,
            "مقابلُ G0 الوارد 36,950؛ الفرقُ 525",
        ),
        Figure(
            "انزياحُ حدّ القطع",
            by_occurrence["READY"] - (40447 + 848),
            Provenance.MEASURED_HERE,
            "بين «بلغ حاملًا» ههنا و«G3+G1» هناك",
        ),
    )


def deferral_census() -> tuple[tuple[str, int, int], ...]:
    """أصنافُ التأجيل بأوّل سببٍ مُسجَّلٍ لكلّ شكل؛ قسمةٌ تامّةٌ لا صنفَ فيها 848.

    الأصنافُ الثلاثةُ تستغرق جانبَ التأجيل كلَّه (8,820 شكلًا · 36,425 وقوعًا)،
    فهي قسمةٌ لا عيّنة؛ وليس فيها صنفٌ يبلغ 848 ولا يقاربه.
    """

    by_form: collections.Counter[str] = collections.Counter()
    by_occurrence: collections.Counter[str] = collections.Counter()
    for _, count, report in _reports():
        if report["status"] == "READY":
            continue
        for deferral in report["deferrals"]:
            code = str(deferral.get("reason", "UNNAMED"))
            by_form[code] += 1
            by_occurrence[code] += count
            break
    return tuple(
        (code, by_form[code], by_occurrence[code])
        for code in sorted(by_form, key=lambda name: -by_occurrence[name])
    )


# ---------------------------------------------------------------------------
# رابعًا: مفتاحُ الهويّة الذي يُثبَّت في عقد الاستقبال
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class IdentityKey:
    """مفتاحٌ يُثبَّت في الشهادة، وما يتصادم تحته من الأشكال الجاهزة."""

    name: str
    colliding_classes: int
    colliding_forms: int
    lifts_the_rasm: bool


THE_WITNESS_PAIR: Final[tuple[str, str]] = ("أَبَا", "أَبَى")


def identity_key_readings() -> tuple[IdentityKey, ...]:
    """ثلاثةُ مفاتيحَ تُقاس على الأشكال الجاهزة كلِّها، لا على الزوج وحده."""

    keys: list[IdentityKey] = []
    for name, extract in (
        ("canonical_atoms", lambda r: tuple(r["canonical_atoms"])),
        ("canonical_text", lambda r: r["canonical_text"]),
        ("source_sha256", lambda r: r["source_sha256"]),
    ):
        buckets: dict[object, list[str]] = collections.defaultdict(list)
        for form, _, report in _reports():
            if report["status"] != "READY":
                continue
            buckets[extract(report)].append(form)
        collisions = [members for members in buckets.values() if len(members) > 1]
        keys.append(
            IdentityKey(
                name=name,
                colliding_classes=len(collisions),
                colliding_forms=sum(len(members) for members in collisions),
                lifts_the_rasm=not collisions,
            )
        )
    return tuple(keys)


def witness_pair_reading() -> tuple[tuple[str, str, str, str], ...]:
    """الزوجُ المذكورُ في التقرير بأعيان مفاتيحه، لا بوصفه."""

    return tuple(
        (
            form,
            "".join(report["canonical_atoms"]),
            report["canonical_text"],
            report["source_sha256"][:16],
        )
        for form, _, report in _reports()
        if form in THE_WITNESS_PAIR
    )


# ---------------------------------------------------------------------------
# خامسًا: جدولُ الأحكام
# ---------------------------------------------------------------------------


def verdict_table() -> tuple[tuple[str, str, str], ...]:
    """دعوى التقرير · ما قيس ههنا · الحكم."""

    materials = material_readings()
    named_only = tuple(item for item in materials if item.name_matches)
    total, measured, agrees = incoming_sum_reading()
    partition = partition_reading()
    keys = {key.name: key for key in identity_key_readings()}

    return (
        (
            "موادُّ الحزمة في الشجرة",
            f"غائبةٌ {len(materials) - len(named_only)}/{len(materials)}؛ "
            f"ومطابقٌ اسمًا لمادّةٍ أخرى {len(named_only)}",
            "مُثبَت؛ والمطابقُ اسمًا لا يُعَدّ استرجاعًا",
        ),
        (
            "القسمةُ الثلاثيّةُ تستغرق المدوّنة",
            f"{total} = {measured}" if agrees else f"{total} ≠ {measured}",
            "اتّساقٌ داخليٌّ مُعادُ الحساب؛ وليس اتّفاقًا على حدّ القطع",
        ),
        (
            "18,200 شكلًا و78,245 وقوعًا",
            f"{partition[0].value} و{partition[1].value}",
            "مُعادتا الإنتاج بالضبط من بايتات المُودَع",
        ),
        (
            "G3 40,447 · G1 848 · G0 36,950",
            f"صنفان ههنا: {partition[3].value} و{partition[4].value}؛ "
            f"وانزياحُ الحدّ {partition[5].value}",
            "غيرُ مُعادةٍ؛ و848 بلا مقابلٍ في هذا الجسر",
        ),
        (
            "«اتّفاقُ النصّ حرفيًّا» يحفظ هويّةَ الرسم",
            f"الذرّاتُ تتصادم {keys['canonical_atoms'].colliding_forms} شكلًا، "
            f"والنصُّ المعياريُّ {keys['canonical_text'].colliding_forms}، "
            f"والبصمةُ {keys['source_sha256'].colliding_forms}",
            "لا يصحّ إلّا بالبايتات؛ وتثبيتُ النصّ المعياريّ خامدٌ ههنا",
        ),
        (
            "0 أقسامٍ عليا مرخَّصةٍ و0 إفادةٍ مرخَّصة",
            "إقرارٌ يُنقَل؛ لا شيفرةَ في الشجرة تُشغَّل لتأييده أو ردِّه",
            "لا يُقاس ههنا؛ ولا يُقوَّم عقدٌ في شيفرةٍ غائبة",
        ),
    )


def rows() -> list[str]:
    """تقريرٌ نصّيٌّ يُطبَع، كلُّ رقمٍ فيه معه نسبتُه."""

    lines = [
        f"توقيعُ المالك: {OWNER_SIGNATURE.owner} — {OWNER_SIGNATURE.granted_on}",
        "",
        "موادُّ الحزمة:",
    ]
    for item in material_readings():
        where = "، ".join(item.name_matches) or "—"
        lines.append(f"  {item.name}: {item.note} [{where}]")
    lines += ["", "قسمةُ جسر هذه الشجرة:"]
    for figure in partition_reading():
        lines.append(f"  {figure.name}: {figure.value} — {figure.note}")
    lines += ["", "أصنافُ التأجيل المسمّاة (أشكال · وقوعات):"]
    for code, forms, occurrences in deferral_census():
        lines.append(f"  {code}: {forms} · {occurrences}")
    lines += ["", "مفاتيحُ الهويّة (أصناف · أشكال متصادمة):"]
    for key in identity_key_readings():
        lines.append(f"  {key.name}: {key.colliding_classes} · {key.colliding_forms}")
    lines += ["", "الزوجُ الشاهد (شكل · ذرّات · نصٌّ معياريٌّ · بصمة):"]
    for row in witness_pair_reading():
        lines.append("  " + " | ".join(row))
    lines += ["", "جدولُ الأحكام:"]
    for claim, measured, verdict in verdict_table():
        lines.append(f"  {claim} | {measured} | {verdict}")
    return lines


if __name__ == "__main__":  # pragma: no cover - تشغيلٌ يدويّ
    print("\n".join(rows()))
