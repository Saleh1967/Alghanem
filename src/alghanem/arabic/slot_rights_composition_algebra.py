"""جبرٌ على ثلاث طبقات: حقوقُ الخانة، ثمّ هندسةُ التركيب، ثمّ القيدُ مصنَّفًا بنوع العلاقة.

**ما تفعله هذه الوحدة**: تبني الطبقاتِ الثلاثَ بناءً مستقلًّا على بايتات هذه
الشجرة وحدَها، وتُبرهن مبرهنتين تُفحصان آليًّا عند الاستيراد، وتقيس ما يُقاس
بدالّةٍ تُشغَّل لا بثابتٍ منقول. و**لا تمنح وسمَ «مرخّص» لشيء**: لا لأنّ القياسَ
أخفق، بل لأنّ شرطَي الترخيص المكتوبَين لم يتحقّقا.

``THE_LICENCE_IS_WITHHELD_ON_ITS_OWN_TERMS``: شرطُ الترخيص المُعلَن شرطان
معًا — أن يُكتَب القيدُ قبل النظر في البيانات، وأن يتّفق مصدران. وهذه الوحدة
تُصرّح أنّ **كليهما منتفٍ ههنا**: خلايا الطبقة الثالثة عُرِضت أرقامُها قبل أن
يُكتَب شرطُها، وبايتاتُ المصدر الثاني (جذور المدوّنة المُوسَّمة) **ليست في هذه
الشجرة**. فكلُّ ما دونَه هنا قياسٌ بقاعدته، لا حكمٌ مرخَّص. وكتابةُ ذلك هي
عينُ ما يمنع الوحدةَ أن تكون دعوى.

``A_SECOND_SOURCE_IS_NOT_A_SECOND_RUN``: تكرارُ التجربة بمُولِّدٍ آخر ليس
مصدرًا ثانيًا. المصدرُ الثاني بايتاتٌ أخرى، وهي غائبةٌ — يُعلَن غيابُها
بـ``second_source_is_resolvable()`` ولا يُسدّ بتكرارٍ على المصدر الأوّل.

# الطبقة الأولى: حقوقُ الخانة

منزلةُ حقِّ الحرف ``c`` في الخانة ``i`` ثلاثُ قيم لا رابعَ لها: **مشهود**، أو
**مرشّحٌ للمنع**، أو **غيرُ محسوم**. وليس في ``RightStanding`` قيمةُ «ممنوع»
أصلًا (``THERE_IS_NO_PROHIBITED_STANDING``)، لأنّ الغيابَ في مُودَعٍ متناهٍ
غيابُ شاهدٍ لا شاهدُ منع.

**مبرهنة ح١ (اطّرادُ الشهادة)**: إن كانت ``X ⊆ Y`` من الجذور، فكلُّ خليةٍ
مشهودةٍ في ``X`` مشهودةٌ في ``Y``. والبرهان سطر: الشهادةُ وجودُ جذرٍ في
المجموعة يحمل ``c`` في ``i``، وذلك الجذرُ باقٍ في ``Y`` بحكم الاحتواء. فمنزلةُ
«مشهود» **اطّراديّةٌ صاعدة**، ومنزلةُ «مرشّح للمنع» ليست كذلك — وهذا وحدَه
يكفي لمنع قلب الغياب منعًا. تُفحَص آليًّا في ``verify_witness_monotonicity``.

**ولادةُ الخانة** لا تقع إلّا بثلاثة شروطٍ مجتمعة، وهي في ``SlotBirthConditions``:
حاملان مختلفان في الخانة، وزوجُ استبدالٍ مشهود (جذران يتساويان إلّا فيها)،
وسقوطُ النموذج الأضعف ``M₀`` الذي يجعل الخاناتِ الثلاثَ قابلةً للتبادل داخل
الجذر. فبدون الثالث تكون «الخانة» ترتيبَ كتابةٍ لا منزلةً في الجبر.

# الطبقة الثانية: هندسةُ التركيب

**مبرهنة ت١ (التركيبُ متماثلٌ والسؤالُ في مكانٍ آخر)**: ليكن
``L = P(a,b)·P(c|b)`` و``R = P(a|b)·P(b,c)``. فكلاهما يساوي
``P(a|b)·P(c|b)·P(b)`` تطابقًا كلّما كان ``P(b) > 0``، فـ``L = R`` **هويّةٌ
جبريّة لا واقعةٌ في البيانات**، ولا يُختبَر بها شيء. والسؤالُ الذي يُختبَر هو
``L = P(a,b,c)``، وهو صحيحٌ لكلّ ``(a,b,c)`` إذا وفقط إذا انعدمت المعلومةُ
الشرطيّة ``I(C₁;C₃|C₂)``. تُفحَص الهويّةُ آليًّا في ``verify_composition_identity``.

**مبرهنة ت٢ (النموذجُ الصفريّ لا بدّ أن يحفظ وحدةَ التحليل)**: المُودَعُ
**معجمُ أنواع**: لا يتكرّر فيه جذر. فنموذجٌ صفريٌّ يُعيد سحب خانةٍ من هوامشها
يُنتج مُخرَجًا فيه جذورٌ مكرّرة باحتمالٍ يقارب الواحد عند هذه الأحجام، فيخرج
من فضاء العيّنة الذي وقعت فيه المشاهدة. والبرهان بالعدّ: عددُ المواضع
الممكنة ``|A|³`` وعددُ الجذور ``N`` متقاربان في الرتبة، فاحتمالُ خلوّ السحب من
تكرارٍ يؤول إلى الصفر بحدّ التزاحم. وعليه **يُرفَض** كلُّ نموذجٍ صفريٍّ لا
يشترط التمايز، ويُستعاض عنه بسلسلة تبديلٍ بالمقايضة تحفظ الجدولين وتمايزَ
الجذور معًا (``distinctness_preserving_swap_chain``). تُفحَص آليًّا في
``verify_naive_null_breaks_distinctness``.

``A_CHAIN_IS_NOT_AN_EXHAUSTIVE_ENUMERATION``: سلسلةُ المقايضة تمشي في فضاء
التشكيلات ولا تُثبَت هنا وصوليّتُها التامّة. فقيمُها تقريبٌ بسلسلةٍ مُعلَنةِ
البذرة والطول، لا عدٌّ تامّ؛ وهذا قيدٌ على كلّ رقمٍ يخرج منها.

# الطبقة الثالثة: القيدُ مصنَّفًا بنوع العلاقة

القيدُ دالّةٌ على ثلاثة: فئةٌ، ونوعُ خليّةٍ، ونوعُ علاقة. ونوعُ الخليّة
مفصولٌ من أوّل الأمر لا بعد فشلٍ: ``CellKind.IDENTITY`` للحرف بعينه،
و``CellKind.CLASS`` للحرفين المختلفين من فئةٍ واحدة
(``AN_IDENTITY_CELL_IS_NOT_A_CLASS_CELL``). وخلطُهما يجعل تخمةَ المضاعف تُقرأ
تجانسًا، وهو الخطأُ الذي تمنعه هذه القسمة قبل وقوعه.

و``OCP`` على هذا **فرعٌ في مجموعة القيود Γ لا أصلُها**: هو الحكمُ على
``CellKind.IDENTITY`` و``CellKind.CLASS`` في العلاقتين المتجاورتين، وليس له
حكمٌ في ``C1C3`` إلّا بقياسٍ مستقلّ (``OCP_IS_A_BRANCH_OF_GAMMA_NOT_ITS_ROOT``).

``THE_PERMUTATION_FLOOR_BINDS_THE_CORRECTION``: أصغرُ قيمة ``p`` تُرصَد في
``B`` تبديلةً هي ``1/(B+1)``. فإن كان تصحيحُ بونفيروني أدقَّ من هذا الحدّ صار
الرفضُ **متعذّرًا لا منتفيًا**، ويُخرَج حينئذٍ ``VerdictStanding.UNRESOLVABLE_AT_THIS_B``
لا «غيرُ دالّ». والعتبةُ والعددُ يُعلَنان مع كلّ حكم.

**خمولٌ سلطويّ**: لا ولادةَ هنا، ولا حكمَ ولادة، ولا تجميدَ ``E0``، ولا
استيرادَ من ``kernel/`` ولا من ``program/``.
"""

from __future__ import annotations

import random
from collections import defaultdict
from collections.abc import Mapping, Sequence
from dataclasses import dataclass
from enum import Enum
from typing import Final

from .maqayis_adjacency_constraint import (
    THE_DECLARED_PLACE_CLASSES,
    folded_roots,
    place_of,
)
from .masaq_corpus_deposit import masaq_bytes_are_resolvable

__all__ = [
    "AN_IDENTITY_CELL_IS_NOT_A_CLASS_CELL",
    "A_CHAIN_IS_NOT_AN_EXHAUSTIVE_ENUMERATION",
    "A_SECOND_SOURCE_IS_NOT_A_SECOND_RUN",
    "AsymmetryLocus",
    "CellKind",
    "CellVerdict",
    "ClosureReading",
    "AlgebraLicenceStanding",
    "OCP_IS_A_BRANCH_OF_GAMMA_NOT_ITS_ROOT",
    "RelationType",
    "RightStanding",
    "SLOT_RIGHTS_ALGEBRA_NAMED_RESIDUALS",
    "THERE_IS_NO_PROHIBITED_STANDING",
    "THE_FOLD_IS_A_UNIT_OF_ANALYSIS_DECISION",
    "THE_LICENCE_IS_WITHHELD_ON_ITS_OWN_TERMS",
    "THE_PERMUTATION_FLOOR_BINDS_THE_CORRECTION",
    "THE_PREREGISTERED_LICENCE_CONDITION",
    "THE_QUOTED_ALGEBRA_FIGURES",
    "SlotBirthConditions",
    "SlotRight",
    "SlotRightsAlgebraError",
    "VerdictStanding",
    "algebra_substrate",
    "distinctness_preserving_swap_chain",
    "exchangeability_rejection",
    "fold_collapse_count",
    "licence_standing",
    "measure_closure",
    "positional_asymmetry_locus",
    "quoted_against_measured",
    "second_source_is_resolvable",
    "slot_birth_conditions",
    "slot_rights",
    "substitution_pairs",
    "typed_cell_verdicts",
    "verify_composition_identity",
    "verify_naive_null_breaks_distinctness",
    "verify_witness_monotonicity",
]


class SlotRightsAlgebraError(RuntimeError):
    """رفضٌ مُسمًّى في جبر حقوق الخانة؛ ولا يخرج منه رقمٌ صامت."""


# ---------------------------------------------------------------------------
# المفردات المغلقة
# ---------------------------------------------------------------------------


class RightStanding(Enum):
    """منزلةُ حقّ حرفٍ في خانة: ثلاثُ قيمٍ لا رابعَ لها، وليس فيها «ممنوع»."""

    WITNESSED = "مشهود"
    CANDIDATE_FOR_PROHIBITION = "مرشّحٌ للمنع"
    UNDECIDED = "غيرُ محسوم"


class RelationType(Enum):
    """نوعُ العلاقة بين خانتين؛ والثلاثةُ تستغرق أزواجَ الجذر الثلاثيّ."""

    C1C2 = "ج١ج٢"
    C2C3 = "ج٢ج٣"
    C1C3 = "ج١ج٣"

    @property
    def slots(self) -> tuple[int, int]:
        """دليلا الخانتين بالصفر."""

        return {
            RelationType.C1C2: (0, 1),
            RelationType.C2C3: (1, 2),
            RelationType.C1C3: (0, 2),
        }[self]

    @property
    def is_adjacent(self) -> bool:
        """أمتجاورتان هما؟ و``C1C3`` وحدَها غيرُ متجاورة."""

        return self is not RelationType.C1C3


class CellKind(Enum):
    """نوعُ الخليّة: الحرفُ بعينه، أو حرفان مختلفان من فئةٍ واحدة."""

    IDENTITY = "تماثل"
    CLASS = "تجانس"


class VerdictStanding(Enum):
    """منزلةُ الحكم على خليّة؛ و«متعذّر» ليس «غيرَ دالّ»."""

    SUPPRESSED = "مكبوت"
    GORGED = "تخمة"
    NEUTRAL = "محايد"
    UNRESOLVABLE_AT_THIS_B = "متعذّرٌ عند هذا العدد"


class AlgebraLicenceStanding(Enum):
    """منزلةُ الترخيص؛ ولا يُمنح «مرخّص» إلّا باجتماع الشرطين المكتوبين."""

    LICENSED = "مرخّص"
    WITHHELD_NO_PRIOR_CONDITION = "محجوبٌ لغياب الشرط السابق"
    WITHHELD_ONE_SOURCE_ONLY = "محجوبٌ لمصدرٍ واحد"


# ---------------------------------------------------------------------------
# البقايا المُسمّاة
# ---------------------------------------------------------------------------

THERE_IS_NO_PROHIBITED_STANDING: Final[str] = (
    "ليس في منازل الحقّ قيمةُ «ممنوع»: الغيابُ في مُودَعٍ متناهٍ غيابُ شاهدٍ لا "
    "شاهدُ منع، وأقصى ما يُقال فيه «مرشّحٌ للمنع» وهو وسمُ انتظارٍ لا حكم."
)

THE_LICENCE_IS_WITHHELD_ON_ITS_OWN_TERMS: Final[str] = (
    "شرطُ الترخيص شرطان: قيدٌ مكتوبٌ قبل النظر في البيانات، واتّفاقُ مصدرين. "
    "وكلاهما منتفٍ في هذا الإيداع، فلا يُمنح وسمُ «مرخّص» لبندٍ واحدٍ فيه."
)

THE_FOLD_IS_A_UNIT_OF_ANALYSIS_DECISION: Final[str] = (
    "طيُّ صور الهمزة والألف يُلحِم جذورًا متمايزةً قبله، فوحدةُ التحليل هنا "
    "النوعُ المطويّ؛ والمُلحَمُ يُسقَط ويُعَدّ إسقاطُه، إذ بقاؤه يُكذِب شرطَ "
    "التمايز في أوّل خطوةٍ من السلسلة."
)

A_SECOND_SOURCE_IS_NOT_A_SECOND_RUN: Final[str] = (
    "المصدرُ الثاني بايتاتٌ أخرى لا تكرارُ تشغيلٍ على البايتات نفسها؛ وبايتاتُ "
    "المصدر الثاني غائبةٌ عن هذه الشجرة، وغيابُها يُعلَن ولا يُسدّ بالتكرار."
)

AN_IDENTITY_CELL_IS_NOT_A_CLASS_CELL: Final[str] = (
    "خليّةُ التماثل مفصولةٌ من أوّل الأمر عن خليّة التجانس: الجذرُ المضاعفُ "
    "مكتوبٌ مُظهَرَ التضعيف، فخلطُهما يقرأ تخمةَ المضاعف تجانسًا في المخرج."
)

OCP_IS_A_BRANCH_OF_GAMMA_NOT_ITS_ROOT: Final[str] = (
    "OCP حكمٌ على نوعَي خليّةٍ في علاقتين متجاورتين، فهو فرعٌ في Γ؛ ولا حكمَ "
    "له في العلاقة غير المتجاورة إلّا بقياسٍ مستقلٍّ عنه."
)

A_CHAIN_IS_NOT_AN_EXHAUSTIVE_ENUMERATION: Final[str] = (
    "سلسلةُ المقايضة لا تُثبَت هنا وصوليّتُها التامّة في فضاء التشكيلات، فأرقامُها "
    "تقريبٌ بسلسلةٍ مُعلَنةِ البذرة والطول لا عدٌّ تامّ."
)

THE_PERMUTATION_FLOOR_BINDS_THE_CORRECTION: Final[str] = (
    "أصغرُ ما يُرصَد في B تبديلةً هو 1/(B+1) في الوجه الواحد، و**ضِعفُه** في "
    "الوجهين؛ فإن كانت عتبةُ بونفيروني أدقَّ من الحدّ كان الرفضُ متعذّرًا لا "
    "منتفيًا، ويُوسَم `UNRESOLVABLE_AT_THIS_B` لا «محايدًا». وخلطُ الحدَّين "
    "يُخرِج حيادًا مصنوعًا من ضيق العدد لا من البيانات."
)

SLOT_RIGHTS_ALGEBRA_NAMED_RESIDUALS: Final[dict[str, str]] = {
    "THERE_IS_NO_PROHIBITED_STANDING": THERE_IS_NO_PROHIBITED_STANDING,
    "THE_LICENCE_IS_WITHHELD_ON_ITS_OWN_TERMS": (
        THE_LICENCE_IS_WITHHELD_ON_ITS_OWN_TERMS
    ),
    "A_SECOND_SOURCE_IS_NOT_A_SECOND_RUN": A_SECOND_SOURCE_IS_NOT_A_SECOND_RUN,
    "THE_FOLD_IS_A_UNIT_OF_ANALYSIS_DECISION": (
        THE_FOLD_IS_A_UNIT_OF_ANALYSIS_DECISION
    ),
    "AN_IDENTITY_CELL_IS_NOT_A_CLASS_CELL": AN_IDENTITY_CELL_IS_NOT_A_CLASS_CELL,
    "OCP_IS_A_BRANCH_OF_GAMMA_NOT_ITS_ROOT": OCP_IS_A_BRANCH_OF_GAMMA_NOT_ITS_ROOT,
    "A_CHAIN_IS_NOT_AN_EXHAUSTIVE_ENUMERATION": (
        A_CHAIN_IS_NOT_AN_EXHAUSTIVE_ENUMERATION
    ),
    "THE_PERMUTATION_FLOOR_BINDS_THE_CORRECTION": (
        THE_PERMUTATION_FLOOR_BINDS_THE_CORRECTION
    ),
}

THE_PREREGISTERED_LICENCE_CONDITION: Final[str] = (
    "يُمنَح وسمُ «مرخّص» لخليّةٍ إذا وفقط إذا اجتمع لها: (١) قيمةُ p أصغرَ من "
    "0.05 مقسومةً على عدد الخلايا المفحوصة كلِّها، (٢) وعددُ التبديلات B كبيرٌ "
    "بحيث 1/(B+1) أصغرُ من تلك العتبة، (٣) واتّفاقُ اتّجاه الحكم في مصدرين "
    "مختلفَي البايتات. وهذا الشرطُ مُجمَّدٌ ليُفحَص به تشغيلٌ لاحقٌ على مصدرٍ "
    "ثانٍ، ولا يُدّعى أنّه سبق أرقامَ هذا الإيداع."
)


# ---------------------------------------------------------------------------
# الركيزة
# ---------------------------------------------------------------------------


def algebra_substrate() -> tuple[tuple[str, str, str], ...]:
    """جذورُ المُودَع مطويّةً إلى الحروف المُصنَّفة، مقروءةً من القرص كلَّ مرّة.

    والطيُّ والتصنيفُ ليسا من عمل هذه الوحدة: هما مُعلَنان قبلها في
    ``maqayis_adjacency_constraint``، وتُقرَأ منه لئلّا يُصطنَع تصنيفٌ ثانٍ.

    ووحدةُ التحليل **النوعُ المطويّ** لا السطرُ المطويّ: الطيُّ يُلحِم جذورًا
    كانت متمايزةً قبله، فيُسقَط المكرّرُ ويُعَدّ إسقاطُه في
    ``fold_collapse_count()``. وتركُه يُدخِل في الجسم جذرًا مرّتين، فيَكذِب
    شرطُ التمايز الذي تقوم عليه مبرهنة ت٢ في أوّل خطوة.
    """

    seen: set[tuple[str, str, str]] = set()
    kept: list[tuple[str, str, str]] = []
    for root in folded_roots():
        if root in seen:
            continue
        seen.add(root)
        kept.append(root)
    return tuple(kept)


def fold_collapse_count() -> int:
    """عدّةُ الجذور التي ألحمها الطيُّ فأُسقِطت؛ وهي إسقاطٌ معدودٌ لا مطويّ."""

    rows = folded_roots()
    return len(rows) - len(set(rows))


def second_source_is_resolvable() -> bool:
    """أبايتاتُ المصدر الثاني في هذه الشجرة؟ والجوابُ واقعةٌ لا اختيار."""

    return masaq_bytes_are_resolvable()


def licence_standing() -> AlgebraLicenceStanding:
    """منزلةُ الترخيص في هذا الإيداع؛ ولا تُخرِج ``LICENSED`` بحالٍ ههنا.

    فشرطُ القيد المكتوب قبل النظر منتفٍ في هذه الوحدة بتصريحها، وهو سببٌ
    يسبق غيابَ المصدر الثاني ولا يرتفع بحضوره.
    """

    return AlgebraLicenceStanding.WITHHELD_NO_PRIOR_CONDITION


# ---------------------------------------------------------------------------
# الطبقة الأولى: حقوقُ الخانة
# ---------------------------------------------------------------------------


@dataclass(frozen=True, slots=True)
class SlotRight:
    """حقُّ حرفٍ في خانةٍ بمنزلته وعدّة شاهده."""

    letter: str
    slot: int
    standing: RightStanding
    witnesses: int

    def __post_init__(self) -> None:
        if len(self.letter) != 1:
            raise SlotRightsAlgebraError("حقُّ الخانة يقع على حرفٍ واحد.")
        if self.slot not in (0, 1, 2):
            raise SlotRightsAlgebraError("الخاناتُ ثلاثٌ، ولا رابعةَ لها ههنا.")
        if self.witnesses < 0:
            raise SlotRightsAlgebraError("عدّةُ الشاهد لا تكون سالبة.")
        if (self.witnesses > 0) != (self.standing is RightStanding.WITNESSED):
            raise SlotRightsAlgebraError(
                "«مشهود» هو وجودُ شاهدٍ بعينه: لا شاهدَ بلا منزلةٍ ولا منزلةَ بلا شاهد."
            )


def slot_rights(
    roots: Sequence[tuple[str, str, str]] | None = None,
) -> tuple[SlotRight, ...]:
    """حقوقُ كلّ حرفٍ في كلّ خانة، مقيسةً لا منقولة.

    والخليّةُ الخاليةُ تُوسَم ``CANDIDATE_FOR_PROHIBITION`` لا «ممنوعة»؛ فالغيابُ
    لا يُقلَب منعًا في مُودَعٍ متناهٍ.
    """

    body = tuple(roots) if roots is not None else algebra_substrate()
    if not body:
        raise SlotRightsAlgebraError("لا حقوقَ تُقاس على مجموعةٍ خالية.")
    alphabet = sorted({letter for root in body for letter in root})
    counts: dict[tuple[str, int], int] = defaultdict(int)
    for root in body:
        for slot, letter in enumerate(root):
            counts[(letter, slot)] += 1
    rights: list[SlotRight] = []
    for letter in alphabet:
        for slot in (0, 1, 2):
            seen = counts.get((letter, slot), 0)
            standing = (
                RightStanding.WITNESSED
                if seen
                else RightStanding.CANDIDATE_FOR_PROHIBITION
            )
            rights.append(SlotRight(letter, slot, standing, seen))
    return tuple(rights)


def verify_witness_monotonicity(
    roots: Sequence[tuple[str, str, str]] | None = None,
) -> bool:
    """فحصُ مبرهنة ح١ آليًّا: ما شُهد في جزءٍ مشهودٌ في الكلّ.

    والفحصُ على أجزاءٍ متداخلةٍ صاعدة؛ وتخلّفُ المبرهنة يرفع لا يُخرِج ``False``
    صامتًا، لأنّ كذبَها يُبطِل الطبقةَ كلَّها.
    """

    body = tuple(roots) if roots is not None else algebra_substrate()
    if len(body) < 8:
        raise SlotRightsAlgebraError("فحصُ الاطّراد يحتاج جسمًا لا أجزاءَ نزرة.")
    previous: set[tuple[str, int]] = set()
    for cut in (len(body) // 4, len(body) // 2, (3 * len(body)) // 4, len(body)):
        witnessed = {
            (right.letter, right.slot)
            for right in slot_rights(body[:cut])
            if right.standing is RightStanding.WITNESSED
        }
        if not previous <= witnessed:
            raise SlotRightsAlgebraError(
                "سقطت مبرهنة ح١: خليّةٌ شُهدت في جزءٍ ثمّ غابت عمّا يحويه."
            )
        previous = witnessed
    return True


def substitution_pairs(
    slot: int, roots: Sequence[tuple[str, str, str]] | None = None
) -> int:
    """عددُ أزواج الاستبدال المشهودة في خانة: جذران يتساويان إلّا فيها."""

    if slot not in (0, 1, 2):
        raise SlotRightsAlgebraError("الخاناتُ ثلاثٌ، ولا رابعةَ لها ههنا.")
    body = tuple(roots) if roots is not None else algebra_substrate()
    groups: dict[tuple[str, ...], set[str]] = defaultdict(set)
    for root in body:
        key = tuple(letter for index, letter in enumerate(root) if index != slot)
        groups[key].add(root[slot])
    return sum(len(values) * (len(values) - 1) // 2 for values in groups.values())


def exchangeability_rejection(
    roots: Sequence[tuple[str, str, str]] | None = None,
    *,
    draws: int = 200,
    seed: int = 20260922,
) -> tuple[float, float, int]:
    """سقوطُ ``M₀``: أتُبدَّل الخاناتُ الثلاثُ داخل الجذر بلا أثر؟

    يُخرِج الإحصاءَ المرصود، وقيمةَ ``p`` بالتبديل، وعددَ السحبات. والإحصاءُ
    مجموعُ مربّع الفرق بين هوامش الخانات الثلاث منسوبًا إلى المتوقَّع تحت
    التبادليّة؛ وقيمةُ ``p`` محدودةٌ من أسفلَ بـ``1/(draws+1)``.
    """

    body = tuple(roots) if roots is not None else algebra_substrate()
    if draws < 1:
        raise SlotRightsAlgebraError("عددُ السحبات موجبٌ، وصفرٌ ليس تبديلًا.")

    def statistic(sample: Sequence[tuple[str, str, str]]) -> float:
        totals: dict[str, int] = defaultdict(int)
        for root in sample:
            for letter in root:
                totals[letter] += 1
        columns: list[dict[str, int]] = [defaultdict(int) for _ in range(3)]
        for root in sample:
            for slot, letter in enumerate(root):
                columns[slot][letter] += 1
        score = 0.0
        for letter, total in totals.items():
            expected = total / 3.0
            for slot in range(3):
                score += (columns[slot].get(letter, 0) - expected) ** 2 / expected
        return score

    observed = statistic(body)
    generator = random.Random(seed)
    atleast = 0
    for _ in range(draws):
        shuffled: list[tuple[str, str, str]] = []
        for root in body:
            letters = list(root)
            generator.shuffle(letters)
            shuffled.append((letters[0], letters[1], letters[2]))
        if statistic(shuffled) >= observed:
            atleast += 1
    return observed, (atleast + 1) / (draws + 1), draws


@dataclass(frozen=True, slots=True)
class SlotBirthConditions:
    """شروطُ ولادة الخانة الثلاثةُ مجتمعةً، ولا تُولَد بدون واحدٍ منها."""

    slot: int
    distinct_carriers: int
    witnessed_substitution_pairs: int
    exchangeability_p: float
    exchangeability_draws: int

    def __post_init__(self) -> None:
        if self.slot not in (0, 1, 2):
            raise SlotRightsAlgebraError("الخاناتُ ثلاثٌ، ولا رابعةَ لها ههنا.")
        if self.distinct_carriers < 0 or self.witnessed_substitution_pairs < 0:
            raise SlotRightsAlgebraError("عدّةٌ سالبةٌ ليست رصدًا.")
        if not 0.0 < self.exchangeability_p <= 1.0:
            raise SlotRightsAlgebraError("قيمةُ p في مجال ]0,1]، وصفرٌ حدٌّ لا قيمة.")

    @property
    def is_born(self) -> bool:
        """أوُلدت الخانةُ بالشروط الثلاثة؟ والعتبةُ هنا حدُّ التبديل نفسُه."""

        return (
            self.distinct_carriers >= 2
            and self.witnessed_substitution_pairs >= 1
            and self.exchangeability_p <= 1.0 / (self.exchangeability_draws + 1)
        )


def slot_birth_conditions(
    roots: Sequence[tuple[str, str, str]] | None = None,
    *,
    draws: int = 200,
    seed: int = 20260922,
) -> tuple[SlotBirthConditions, ...]:
    """شروطُ الولادة للخانات الثلاث، والنموذجُ الأضعفُ يُختبَر مرّةً لها جميعًا."""

    body = tuple(roots) if roots is not None else algebra_substrate()
    _, probability, used = exchangeability_rejection(body, draws=draws, seed=seed)
    return tuple(
        SlotBirthConditions(
            slot=slot,
            distinct_carriers=len({root[slot] for root in body}),
            witnessed_substitution_pairs=substitution_pairs(slot, body),
            exchangeability_p=probability,
            exchangeability_draws=used,
        )
        for slot in (0, 1, 2)
    )


# ---------------------------------------------------------------------------
# الطبقة الثانية: هندسةُ التركيب
# ---------------------------------------------------------------------------


def verify_composition_identity(*, trials: int = 64, seed: int = 20260922) -> bool:
    """فحصُ مبرهنة ت١ آليًّا بشقَّيها على جداولَ مُولَّدة.

    الشقُّ الأوّل: ``L = R`` على كلّ ثلاثيّةٍ وفي كلّ جدول — هويّةٌ لا واقعة.
    الشقُّ الثاني: ``L = P₁₂₃`` على كلّ ثلاثيّةٍ **إذا وفقط إذا** انعدمت
    ``I(C₁;C₃|C₂)``؛ فيُبنى جدولٌ مستقلٌّ شرطيًّا بالبناء ويُطلَب التطابق،
    ويُبنى جدولٌ غيرُ مستقلٍّ ويُطلَب التخلّف. وتخلّفُ أيّ شقٍّ يُرفَع، إذ كذبُه
    يُبطِل الطبقة.
    """

    if trials < 1:
        raise SlotRightsAlgebraError("فحصٌ بلا محاولةٍ ليس فحصًا.")
    generator = random.Random(seed)

    def composed(
        joint: Mapping[tuple[int, int, int], float],
    ) -> tuple[float, float, float]:
        middle = [
            sum(joint[(a, b, c)] for a in range(2) for c in range(2)) for b in range(2)
        ]
        worst_gap = 0.0
        worst_identity = 0.0
        for a in range(2):
            for b in range(2):
                for c in range(2):
                    left_pair = sum(joint[(a, b, z)] for z in range(2))
                    right_pair = sum(joint[(z, b, c)] for z in range(2))
                    left = left_pair * (right_pair / middle[b])
                    right = (left_pair / middle[b]) * right_pair
                    worst_identity = max(worst_identity, abs(left - right))
                    worst_gap = max(worst_gap, abs(left - joint[(a, b, c)]))
        return worst_identity, worst_gap, sum(joint.values())

    for _ in range(trials):
        middle = [generator.random() + 0.1 for _ in range(2)]
        mass = sum(middle)
        middle = [value / mass for value in middle]
        first = [[generator.random() + 0.1 for _ in range(2)] for _ in range(2)]
        third = [[generator.random() + 0.1 for _ in range(2)] for _ in range(2)]
        for row in (*first, *third):
            total = sum(row)
            row[:] = [value / total for value in row]
        conditional: dict[tuple[int, int, int], float] = {
            (a, b, c): middle[b] * first[b][a] * third[b][c]
            for a in range(2)
            for b in range(2)
            for c in range(2)
        }
        identity_gap, closure_gap, mass_check = composed(conditional)
        if identity_gap > 1e-12:
            raise SlotRightsAlgebraError(
                "سقط الشقُّ الأوّل من ت١: التركيبان غيرُ متطابقين وهما هويّة."
            )
        if abs(mass_check - 1.0) > 1e-9:
            raise SlotRightsAlgebraError("جدولٌ مُولَّدٌ لا يجمع واحدًا؛ فلا يُقاس عليه.")
        if closure_gap > 1e-12:
            raise SlotRightsAlgebraError(
                "سقط الشقُّ الثاني من ت١: استقلالٌ شرطيٌّ بالبناء ولم ينغلق التركيب."
            )
        tilted = dict(conditional)
        tilted[(0, 0, 0)] *= 2.0
        mass = sum(tilted.values())
        tilted = {key: value / mass for key, value in tilted.items()}
        identity_gap, closure_gap, _ = composed(tilted)
        if identity_gap > 1e-12:
            raise SlotRightsAlgebraError(
                "سقط الشقُّ الأوّل من ت١ على جدولٍ غيرِ مستقلٍّ شرطيًّا."
            )
        if closure_gap <= 1e-12:
            raise SlotRightsAlgebraError(
                "سقط الشقُّ الثاني من ت١: انغلق التركيب بلا استقلالٍ شرطيّ."
            )
    return True


def distinctness_preserving_swap_chain(
    roots: Sequence[tuple[str, str, str]],
    *,
    slot: int,
    block_slot: int | None,
    steps: int,
    generator: random.Random,
    state: list[tuple[str, str, str]] | None = None,
) -> list[tuple[str, str, str]]:
    """سلسلةُ مقايضةٍ تحفظ الهوامش وتمايزَ الجذور معًا.

    تُقايَض قيمةُ ``slot`` بين جذرين، وتُرفَض المقايضةُ إن ولّدت جذرًا موجودًا.
    فإن أُعطيت ``block_slot`` لم تقع المقايضةُ إلّا بين جذرين يتّفقان فيها،
    فيُحفَظ جدولُ العلاقة بينهما تامًّا لا تقريبًا.
    """

    if slot not in (0, 1, 2):
        raise SlotRightsAlgebraError("الخاناتُ ثلاثٌ، ولا رابعةَ لها ههنا.")
    if block_slot is not None and block_slot == slot:
        raise SlotRightsAlgebraError("لا تُثبَّت الخانةُ المُقايَضةُ نفسُها.")
    if steps < 0:
        raise SlotRightsAlgebraError("عددُ الخطوات لا يكون سالبًا.")
    current = list(state) if state is not None else list(roots)
    present = set(current)
    if len(present) != len(current):
        raise SlotRightsAlgebraError(
            "السلسلةُ تحفظ التمايز، فلا تبدأ من حالةٍ فيها جذرٌ مكرّر."
        )
    blocks: dict[str | None, list[int]] = defaultdict(list)
    for index, root in enumerate(current):
        blocks[root[block_slot] if block_slot is not None else None].append(index)
    keys = [key for key, members in blocks.items() if len(members) > 1]
    if not keys:
        return current
    weights = [len(blocks[key]) for key in keys]
    for _ in range(steps):
        key = generator.choices(keys, weights=weights)[0]
        members = blocks[key]
        first, second = generator.sample(members, 2)
        left, right = current[first], current[second]
        if left[slot] == right[slot]:
            continue
        made_left = list(left)
        made_right = list(right)
        made_left[slot], made_right[slot] = right[slot], left[slot]
        new_left = (made_left[0], made_left[1], made_left[2])
        new_right = (made_right[0], made_right[1], made_right[2])
        if new_left in present or new_right in present:
            continue
        present.discard(left)
        present.discard(right)
        present.add(new_left)
        present.add(new_right)
        current[first] = new_left
        current[second] = new_right
    return current


def verify_naive_null_breaks_distinctness(
    roots: Sequence[tuple[str, str, str]] | None = None,
    *,
    seed: int = 20260922,
) -> int:
    """فحصُ مبرهنة ت٢ آليًّا: النموذجُ الساذجُ يُنتج جذورًا مكرّرة.

    يُخرِج عددَ الجذور المكرّرة في سحبةٍ واحدةٍ من نموذجٍ يُعيد خلطَ الخانة
    الثالثة داخل كتل الثانية بلا اشتراط تمايز. وصفرٌ هنا يُرفَع، لأنّ المبرهنة
    تُسنَد إلى وقوع التزاحم لا إلى احتماله.
    """

    body = tuple(roots) if roots is not None else algebra_substrate()
    generator = random.Random(seed)
    blocks: dict[str, list[int]] = defaultdict(list)
    for index, root in enumerate(body):
        blocks[root[1]].append(index)
    drawn = list(body)
    for members in blocks.values():
        thirds = [body[index][2] for index in members]
        generator.shuffle(thirds)
        for index, third in zip(members, thirds, strict=True):
            drawn[index] = (body[index][0], body[index][1], third)
    collisions = len(drawn) - len(set(drawn))
    if collisions <= 0:
        raise SlotRightsAlgebraError(
            "لم يقع تزاحمٌ في السحبة الساذجة؛ ومبرهنة ت٢ تُسنَد إلى وقوعه."
        )
    return collisions


@dataclass(frozen=True, slots=True)
class ClosureReading:
    """قراءةُ إغلاق التركيب: أيُستغنى بالرابطتين المتجاورتين عن الثالثة؟"""

    observed_same_place: int
    observed_identity: int
    null_mean_same_place: float
    null_mean_identity: float
    same_place_p_low: float
    identity_p_low: float
    draws: int

    def __post_init__(self) -> None:
        if self.draws < 1:
            raise SlotRightsAlgebraError("قراءةٌ بلا سحبةٍ ليست قراءة.")
        if self.null_mean_same_place <= 0 or self.null_mean_identity <= 0:
            raise SlotRightsAlgebraError("متوسّطٌ صفريٌّ غيرُ موجبٍ لا تُنسَب إليه نسبة.")

    @property
    def same_place_ratio(self) -> float:
        """نسبةُ المرصود إلى المتوقَّع في اجتماع الطرفين من مخرجٍ واحد."""

        return self.observed_same_place / self.null_mean_same_place

    @property
    def identity_ratio(self) -> float:
        """نسبةُ المرصود إلى المتوقَّع في تماثل الطرفين حرفًا بعينه."""

        return self.observed_identity / self.null_mean_identity

    @property
    def closure_holds(self) -> bool:
        """أيُغلَق التركيب؟ والإغلاقُ يسقط بأيّ طرفٍ يخرج عن حدّ التبديل."""

        floor = 1.0 / (self.draws + 1)
        return not (self.same_place_p_low <= floor or self.identity_p_low <= floor)


def measure_closure(
    roots: Sequence[tuple[str, str, str]] | None = None,
    *,
    draws: int = 200,
    burn_in: int = 20000,
    sweep: int = 2000,
    seed: int = 20260922,
) -> ClosureReading:
    """قياسُ إغلاق التركيب تحت نموذجٍ يثبّت الجدولين ويحفظ تمايزَ الجذور.

    النموذجُ الصفريُّ سلسلةُ مقايضةٍ للخانة الثالثة داخل كتل الثانية: فجدولُ
    ``C1C2`` لا يُمسّ أصلًا، وجدولُ ``C2C3`` محفوظٌ تامًّا لأنّ المقايضةَ داخلَ
    الكتلة، والتمايزُ مشروطٌ في كلّ خطوة. وما يتحرّك هو اجتماعُ ``C1`` و``C3``
    وحدَه.
    """

    body = tuple(roots) if roots is not None else algebra_substrate()
    if draws < 1:
        raise SlotRightsAlgebraError("قياسٌ بلا سحبةٍ ليس قياسًا.")
    places = {letter: place_of(letter) for root in body for letter in root}

    def readings(sample: Sequence[tuple[str, str, str]]) -> tuple[int, int]:
        same = sum(1 for root in sample if places[root[0]] == places[root[2]])
        identical = sum(1 for root in sample if root[0] == root[2])
        return same, identical

    observed_same, observed_identity = readings(body)
    generator = random.Random(seed)
    state = distinctness_preserving_swap_chain(
        body, slot=2, block_slot=1, steps=burn_in, generator=generator
    )
    same_totals = 0.0
    identity_totals = 0.0
    same_atmost = 0
    identity_atmost = 0
    for _ in range(draws):
        state = distinctness_preserving_swap_chain(
            body, slot=2, block_slot=1, steps=sweep, generator=generator, state=state
        )
        same, identical = readings(state)
        same_totals += same
        identity_totals += identical
        same_atmost += same <= observed_same
        identity_atmost += identical <= observed_identity
    return ClosureReading(
        observed_same_place=observed_same,
        observed_identity=observed_identity,
        null_mean_same_place=same_totals / draws,
        null_mean_identity=identity_totals / draws,
        same_place_p_low=(same_atmost + 1) / (draws + 1),
        identity_p_low=(identity_atmost + 1) / (draws + 1),
        draws=draws,
    )


# ---------------------------------------------------------------------------
# الطبقة الثالثة: القيدُ مصنَّفًا بنوع العلاقة
# ---------------------------------------------------------------------------


@dataclass(frozen=True, slots=True)
class CellVerdict:
    """حكمٌ على خليّةٍ بفئتها ونوعها ونوع علاقتها، ومعه منزلتُه وترخيصُه."""

    place_class: str
    kind: CellKind
    relation: RelationType
    observed: int
    null_mean: float
    probability: float
    threshold: float
    draws: int
    standing: VerdictStanding
    licence: AlgebraLicenceStanding

    def __post_init__(self) -> None:
        if self.place_class not in THE_DECLARED_PLACE_CLASSES:
            raise SlotRightsAlgebraError("فئةٌ خارج المخارج المُعلَنة لا تُحكَم ههنا.")
        if self.observed < 0 or self.null_mean < 0:
            raise SlotRightsAlgebraError("عدّةٌ سالبةٌ ليست رصدًا.")
        if not 0.0 < self.probability <= 1.0:
            raise SlotRightsAlgebraError("قيمةُ p في مجال ]0,1].")
        if self.licence is AlgebraLicenceStanding.LICENSED:
            raise SlotRightsAlgebraError(
                "لا يُمنح وسمُ «مرخّص» في هذا الإيداع: شرطاه المكتوبان منتفيان."
            )

    @property
    def ratio(self) -> float | None:
        """نسبةُ المرصود إلى المتوقَّع، أو لا شيءَ إن كان المتوقَّعُ صفرًا."""

        return self.observed / self.null_mean if self.null_mean else None


def typed_cell_verdicts(
    roots: Sequence[tuple[str, str, str]] | None = None,
    *,
    draws: int = 200,
    burn_in: int = 20000,
    sweep: int = 2000,
    seed: int = 20260922,
) -> tuple[CellVerdict, ...]:
    """أحكامُ الخلايا لكلّ فئةٍ ونوعِ خليّةٍ ونوعِ علاقة، بتصحيح بونفيروني.

    وخليّةُ التماثل مفصولةٌ عن خليّة التجانس في العدّ نفسِه لا بعدَه؛ والفئةُ
    ذاتُ الحرف الواحد لا خليّةَ تجانسٍ لها أصلًا فلا تُعَدّ ولا تدخل التصحيح.
    """

    body = tuple(roots) if roots is not None else algebra_substrate()
    places = {letter: place_of(letter) for root in body for letter in root}
    classes = tuple(THE_DECLARED_PLACE_CLASSES)
    plural = tuple(
        name for name in classes if len(THE_DECLARED_PLACE_CLASSES[name]) > 1
    )
    tested = len(classes) * len(RelationType) + len(plural) * len(RelationType)
    threshold = 0.05 / tested
    floor = 2.0 / (draws + 1)

    def tally(
        sample: Sequence[tuple[str, str, str]], relation: RelationType
    ) -> tuple[dict[str, int], dict[str, int]]:
        left, right = relation.slots
        identity: dict[str, int] = defaultdict(int)
        classwise: dict[str, int] = defaultdict(int)
        for root in sample:
            one, two = root[left], root[right]
            if places[one] != places[two]:
                continue
            if one == two:
                identity[places[one]] += 1
            else:
                classwise[places[one]] += 1
        return identity, classwise

    verdicts: list[CellVerdict] = []
    for relation in RelationType:
        left, right = relation.slots
        observed_identity, observed_class = tally(body, relation)
        generator = random.Random(seed + left * 31 + right)
        state = distinctness_preserving_swap_chain(
            body, slot=right, block_slot=None, steps=burn_in, generator=generator
        )
        totals: dict[tuple[str, CellKind], float] = defaultdict(float)
        atmost: dict[tuple[str, CellKind], int] = defaultdict(int)
        atleast: dict[tuple[str, CellKind], int] = defaultdict(int)
        for _ in range(draws):
            state = distinctness_preserving_swap_chain(
                body,
                slot=right,
                block_slot=None,
                steps=sweep,
                generator=generator,
                state=state,
            )
            drawn_identity, drawn_class = tally(state, relation)
            for name in classes:
                key = (name, CellKind.IDENTITY)
                value = drawn_identity.get(name, 0)
                totals[key] += value
                atmost[key] += value <= observed_identity.get(name, 0)
                atleast[key] += value >= observed_identity.get(name, 0)
            for name in plural:
                key = (name, CellKind.CLASS)
                value = drawn_class.get(name, 0)
                totals[key] += value
                atmost[key] += value <= observed_class.get(name, 0)
                atleast[key] += value >= observed_class.get(name, 0)
        for name in classes:
            for kind in CellKind:
                if kind is CellKind.CLASS and name not in plural:
                    continue
                key = (name, kind)
                seen = (
                    observed_identity.get(name, 0)
                    if kind is CellKind.IDENTITY
                    else observed_class.get(name, 0)
                )
                mean = totals[key] / draws
                low = (atmost[key] + 1) / (draws + 1)
                high = (atleast[key] + 1) / (draws + 1)
                probability = min(1.0, 2.0 * min(low, high))
                if floor >= threshold:
                    standing = VerdictStanding.UNRESOLVABLE_AT_THIS_B
                elif probability > threshold:
                    standing = VerdictStanding.NEUTRAL
                elif seen < mean:
                    standing = VerdictStanding.SUPPRESSED
                else:
                    standing = VerdictStanding.GORGED
                verdicts.append(
                    CellVerdict(
                        place_class=name,
                        kind=kind,
                        relation=relation,
                        observed=seen,
                        null_mean=mean,
                        probability=probability,
                        threshold=threshold,
                        draws=draws,
                        standing=standing,
                        licence=AlgebraLicenceStanding.WITHHELD_NO_PRIOR_CONDITION,
                    )
                )
    return tuple(verdicts)


@dataclass(frozen=True, slots=True)
class AsymmetryLocus:
    """موضعُ الفرق بين العلاقتين المتجاورتين: أفي التماثل هو أم في التجانس؟"""

    identity_difference: int
    class_difference: int
    identity_probability: float
    class_probability: float
    threshold: float
    draws: int

    def __post_init__(self) -> None:
        if self.draws < 1:
            raise SlotRightsAlgebraError("قراءةٌ بلا سحبةٍ ليست قراءة.")
        for probability in (self.identity_probability, self.class_probability):
            if not 0.0 < probability <= 1.0:
                raise SlotRightsAlgebraError("قيمةُ p في مجال ]0,1].")

    @property
    def locus(self) -> CellKind | None:
        """نوعُ الخليّة التي يسكنها الفرق وحدَه، أو لا شيءَ إن لم ينفرد بها."""

        in_identity = self.identity_probability <= self.threshold
        in_class = self.class_probability <= self.threshold
        if in_identity and not in_class:
            return CellKind.IDENTITY
        if in_class and not in_identity:
            return CellKind.CLASS
        return None


def positional_asymmetry_locus(
    roots: Sequence[tuple[str, str, str]] | None = None,
    *,
    draws: int = 200,
    seed: int = 20260922,
) -> AsymmetryLocus:
    """أين يسكن الفرقُ بين ``C1C2`` و``C2C3``: في التماثل أم في التجانس؟

    والنموذجُ الصفريُّ هنا **قلبُ الجذر** حول خانته الوسطى بسكّةٍ عادلة: فهو
    يُبادل العلاقتين المتجاورتين دون أن يمسّ حرفًا ولا هامشًا ولا تمايزَ جذر،
    فيقيس الفرقَ بينهما وحدَه. وقيمتا ``p`` في الوجهين.

    وهذا هو المحكُّ الذي يفصل دعوى «الرابطتان مختلفتان» عن سببها: فإن سكن
    الفرقُ خليّةَ التماثل وحدَها فالاختلافُ في المضاعف لا في المخرج، ودعوى
    اختلافِ الرابطتين في المخرج تسقط وإن صدق الرقمُ الأوّل.
    """

    body = tuple(roots) if roots is not None else algebra_substrate()
    if draws < 1:
        raise SlotRightsAlgebraError("قياسٌ بلا سحبةٍ ليس قياسًا.")
    places = {letter: place_of(letter) for root in body for letter in root}

    def differences(sample: Sequence[tuple[str, str, str]]) -> tuple[int, int]:
        identity = 0
        classwise = 0
        for root in sample:
            first, middle, last = root
            identity += (middle == last) - (first == middle)
            classwise += (middle != last and places[middle] == places[last]) - (
                first != middle and places[first] == places[middle]
            )
        return identity, classwise

    observed_identity, observed_class = differences(body)
    generator = random.Random(seed)
    identity_atleast = 0
    class_atleast = 0
    for _ in range(draws):
        flipped = [
            (root[2], root[1], root[0]) if generator.random() < 0.5 else root
            for root in body
        ]
        drawn_identity, drawn_class = differences(flipped)
        identity_atleast += abs(drawn_identity) >= abs(observed_identity)
        class_atleast += abs(drawn_class) >= abs(observed_class)
    return AsymmetryLocus(
        identity_difference=observed_identity,
        class_difference=observed_class,
        identity_probability=(identity_atleast + 1) / (draws + 1),
        class_probability=(class_atleast + 1) / (draws + 1),
        threshold=0.05 / 2,
        draws=draws,
    )


# ---------------------------------------------------------------------------
# المنقولُ في وجه المقيس
# ---------------------------------------------------------------------------

THE_QUOTED_ALGEBRA_FIGURES: Final[Mapping[str, str]] = {
    "عدّةُ جذور المقاييس المنقولة": "4,362 جذرًا",
    "عدّةُ جذور المدوّنة المنقولة": "1,602 جذرًا",
    "خلايا الحقوق المنقولة": "84 خليّةً كلُّها مشهودة",
    "خلايا التفضيل والكبت المنقولة": "10 تفضيلٍ و6 كبت",
    "اجتماعُ الطرفين من مخرجٍ واحدٍ منقولًا": "0.48 من المتوقَّع",
    "تماثلُ الطرفين منقولًا": "0.14 و0.12 من المتوقَّع",
    "تخمةُ المضاعف منقولةً": "444 بإزاء 186.6 متوقَّعًا",
    "كبتُ ج١ج٢ منقولًا": "2 بإزاء 174.5 متوقَّعًا",
    "تجانسُ الذلقيّ في ج١ج٣ منقولًا": "0.89 و0.91",
}
"""أرقامٌ وصلت نثرًا من محادثةٍ أخرى؛ تُسجَّل بقيدها ولا يُبنى عليها حكم.

ونظيرُها المقيسُ في هذه الشجرة يُخرِجه ``quoted_against_measured()`` بدالّةٍ
تُشغَّل، فيُقرأ الفرقُ ولا يُطوى.
"""


def quoted_against_measured(
    roots: Sequence[tuple[str, str, str]] | None = None,
) -> tuple[tuple[str, str, str, bool], ...]:
    """المنقولُ بإزاء ما يقيسه القرصُ الآن، وحكمُ التطابق في كلّ سطر.

    ولا يُقاس ههنا إلّا ما تكفيه بايتاتُ هذه الشجرة وحدَها؛ وما لا تكفيه —
    وأوّلُه عدّةُ جذور المصدر الثاني — يُخرَج بنصّ الغياب لا بصفر.
    """

    body = tuple(roots) if roots is not None else algebra_substrate()
    witnessed = sum(
        1 for right in slot_rights(body) if right.standing is RightStanding.WITNESSED
    )
    cells = len(slot_rights(body))
    rows: list[tuple[str, str, str, bool]] = [
        (
            "عدّةُ جذور المقاييس",
            "4,362 جذرًا",
            f"{len(body):,} جذرًا مطويًّا تحت المخارج المُعلَنة",
            len(body) == 4362,
        ),
        (
            "عدّةُ جذور المدوّنة",
            "1,602 جذرًا",
            (
                "بايتاتُ المصدر الثاني ليست في هذه الشجرة"
                if not second_source_is_resolvable()
                else "بايتاتُ المصدر الثاني محلولة"
            ),
            False,
        ),
        (
            "خلايا الحقوق",
            "84 خليّةً كلُّها مشهودة",
            f"{witnessed} من {cells} مشهودة",
            witnessed == cells == 84,
        ),
    ]
    return tuple(rows)


# ---------------------------------------------------------------------------
# فحصُ المبرهنتين وحراسةُ الخمول عند الاستيراد
# ---------------------------------------------------------------------------


def _refuse_operative_vocabulary() -> None:
    """حراسةُ الخمول: لا اسمَ في هذه الوحدة يَعِد بولادةٍ أو ترخيصٍ ممنوح."""

    for name in __all__:
        if name.startswith(("birth_", "licence_grant", "freeze_")):
            raise SlotRightsAlgebraError(
                f"الاسمُ {name!r} يَعِد بسلطةٍ لا تملكها هذه الوحدة."
            )
    if AlgebraLicenceStanding.LICENSED.value not in {
        member.value for member in AlgebraLicenceStanding
    }:  # pragma: no cover - حراسةُ اكتمالٍ لا فرع
        raise SlotRightsAlgebraError("منزلةُ الترخيص المُعلَنة ناقصة.")


_refuse_operative_vocabulary()
verify_composition_identity()
