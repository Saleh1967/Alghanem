"""تسجيلٌ قَبْليٌّ مُجمَّد لقياس دعوى المفعولية، قبل قراءة بايتة علاقةٍ واحدة.

أغلقت خطوةُ الصفر سؤالَ الوجود: طبقةُ العلاقات في `ar_padt` و`ar_pud` مملوءةٌ
في كلِّ سطرِ كلمة (`ud_relation_layer_step0`). وختمت تلك الوحدةُ نفسَها بشرطٍ
مكتوب: `STEP_ZERO_IS_NOT_A_READER` — «لا تُغني عن تسجيلٍ قَبْليٍّ مجمَّدٍ يسبق
أيَّ قياسٍ لاحق». وهذه الوحدةُ ذلك التسجيل، ولا شيءَ غيرَه.

**الدعوى المقيسة هي الدعوى الأولى بعينها**: «الكلمةُ التاليةُ للفعل الماضي، إذا
خُتِمت بفتحة، فهي مفعولٌ به». قيست في `irab_case_readout` على مدوَّنةٍ تُوسِّم
**الحالة** لا **الوظيفة**، فبقي الأصلُ غيرَ مقيسٍ باعتراف الوحدة نفسِها
(`ACCUSATIVE_IS_NOT_OBJECTHOOD`). ووجودُ طبقةِ علاقاتٍ مملوءةٍ يفتح — لأوّل مرّة
في هذه الشجرة — إمكانَ قياسِ الوظيفة نفسِها.

**وهذه الوحدة لا تقيس** (`A_PREREGISTRATION_IS_NOT_A_MEASUREMENT`): لا عددَ
فيها مقروءًا من ملفّ علاقات، ولا حقلَ نتيجةٍ البتّة، وحارسٌ عند الاستيراد يمنع
تسلّلَ حقلٍ كهذا لاحقًا. المُودَعُ هنا: نصُّ الدعوى، وقاعدةُ التنبّؤ بحروفها،
والعمودُ الذي تُقرأ منه الحركة، وتعريفُ المجتمع، وتعريفُ المتعذّر، وقسمةُ
التطوير والحجب، وعتبتا الحسم، وما لا يجوز أن يُقرأ من الرقم إذا خرج.

**وما رآه هذا التسجيل قبل أن يُكتَب يُسمّى ولا يُطوى**
(`STEP_ZERO_COUNTS_WERE_KNOWN_BEFORE_THIS_PREREGISTRATION`): أعدادُ الكلمات
و`obj` و`Case=Acc` في تلك الملفّات مُودَعةٌ في خطوة الصفر ومقروءةٌ سلفًا. ولم
تُقرأ قطُّ حركةٌ من تلك البايتات، ولا عُدَّ موضعٌ واحدٌ تالٍ لفعلٍ ماضٍ فيها،
فالعتباتُ أدناه لم تُختَر على رقمٍ منظور.

وهذه الوحدة تسجيلٌ لا سلطة: لا ولادةَ فيها، ولا حكمَ ولادة، ولا تجميدَ `E0`،
ولا تستورد من `kernel/` شيئًا، ولا تقرؤها وحدةٌ فيه.
"""

from __future__ import annotations

from dataclasses import dataclass, fields
from enum import Enum
from typing import Final

from alghanem.canonical_content import canonical_bytes, canonical_digest

from .ud_relation_layer_step0 import (
    OBJ_VS_OBL_IS_PARTLY_CASE_DEFINED_NOTE,
    REGISTER_IS_NEWSWIRE_NOT_QURANIC_NOTE,
    UNVOCALIZED_FORMS_ARE_NOT_CARRIER_STATE_INPUT_NOTE,
)

__all__ = [
    "A_PREREGISTRATION_IS_NOT_A_MEASUREMENT_NOTE",
    "FrozenObjecthoodPreregistration",
    "OBJECTHOOD_PREREGISTRATION",
    "OBJECTHOOD_PREREGISTRATION_NAMED_RESIDUALS",
    "OBJ_IS_UD_OBJECTHOOD_NOT_CLASSICAL_MAFUL_NOTE",
    "ObjecthoodDecision",
    "ObjecthoodPreregistrationError",
    "ObjecthoodPositionOutcome",
    "STEP_ZERO_COUNTS_WERE_KNOWN_BEFORE_THIS_PREREGISTRATION_NOTE",
    "VFORM_IS_AN_ANNOTATORS_VOCALIZATION_NOTE",
]


class ObjecthoodPreregistrationError(ValueError):
    """رُفض تسجيلٌ قَبْليٌّ لا يُقاس به شيءٌ كما هو مكتوب."""


class ObjecthoodPositionOutcome(Enum):
    """منزلةُ الموضع الواحد؛ ثلاثٌ مغلقةٌ لا رابعَ لها ولا جمعَ بين اثنتين."""

    PREDICTED_AND_IS_OBJECT = "أصاب"
    PREDICTED_AND_IS_NOT_OBJECT = "أخطأ"
    UNREADABLE_SURFACE = "متعذّر_القياس"


class ObjecthoodDecision(Enum):
    """حسمُ الدعوى؛ ثلاثُ قيمٍ مغلقةٍ تُشتقّ من الرقم ولا تُودَع حقلًا."""

    CLAIM_UPHELD = "الدعوى_قائمة"
    CLAIM_REFUTED = "الدعوى_ساقطة"
    CLAIM_UNDECIDED_IN_BAND = "لا_حسم_في_النطاق"


A_PREREGISTRATION_IS_NOT_A_MEASUREMENT_NOTE: Final[str] = (
    "APreregistrationIsNotAMeasurement: لا رقمَ في هذه الوحدة مقروءًا من ملفِّ "
    "علاقات، ولا تُجيب عن الدعوى شيئًا؛ وتجميدُ المواصفة ليس تشغيلَها، ومن "
    "قرأ منها حكمًا قرأ ما لم يُقَس"
)

STEP_ZERO_COUNTS_WERE_KNOWN_BEFORE_THIS_PREREGISTRATION_NOTE: Final[str] = (
    "StepZeroCountsWereKnownBeforeThisPreregistration: أعدادُ الكلمات و`obj` "
    "و`Case=Acc` في الملفّات المُسمّاة هنا كانت مقروءةً ومُودَعةً في خطوة الصفر "
    "قبل كتابة هذا التسجيل، فلا يُوصَف بأنّه سابقٌ لكلِّ قراءةِ بايت. والذي لم "
    "يُقرأ منها قطُّ: حركةٌ واحدة، وموضعٌ واحدٌ تالٍ لفعلٍ ماضٍ، وهما مادّةُ "
    "هذا القياس وحدَه"
)

VFORM_IS_AN_ANNOTATORS_VOCALIZATION_NOTE: Final[str] = (
    "VformIsAnAnnotatorsVocalization: الحركةُ المقروءةُ هنا من حقل `Vform` في "
    "عمود `MISC`، وهي شكلُ المُوسِّم لا شكلُ النصِّ المنشور؛ فالقياسُ على "
    "شكلٍ مُضافٍ بالتوسيم، ومن نقله إلى نصٍّ غيرِ مشكولٍ نقل ما ليس فيه"
)

OBJ_IS_UD_OBJECTHOOD_NOT_CLASSICAL_MAFUL_NOTE: Final[str] = (
    "ObjIsUdObjecthoodNotClassicalMaful: علاقةُ `obj` في مخطَّط Universal "
    "Dependencies ليست «المفعولَ به» في اصطلاح النحو العربيّ: المفعولُ المطلق "
    "والظرفُ يُوسَمان عندها خارجَ `obj`، والمفعولُ الثاني `iobj`، والمفعولُ "
    "بحرفٍ `obl`. فسقوطُ الدعوى على `obj` سقوطٌ على تعريف المخطَّط، وقيامُها "
    "قيامٌ عليه، وفي الحالين لا يُنقَل الحكمُ إلى اصطلاحٍ آخرَ بلا تحويلٍ مُبيَّن"
)

OBJECTHOOD_PREREGISTRATION_NAMED_RESIDUALS: Final[dict[str, str]] = {
    "APreregistrationIsNotAMeasurement": A_PREREGISTRATION_IS_NOT_A_MEASUREMENT_NOTE,
    "StepZeroCountsWereKnownBeforeThisPreregistration": (
        STEP_ZERO_COUNTS_WERE_KNOWN_BEFORE_THIS_PREREGISTRATION_NOTE
    ),
    "VformIsAnAnnotatorsVocalization": VFORM_IS_AN_ANNOTATORS_VOCALIZATION_NOTE,
    "ObjIsUdObjecthoodNotClassicalMaful": (
        OBJ_IS_UD_OBJECTHOOD_NOT_CLASSICAL_MAFUL_NOTE
    ),
    "ObjVsOblIsPartlyCaseDefined": OBJ_VS_OBL_IS_PARTLY_CASE_DEFINED_NOTE,
    "RegisterIsNewswireNotQuranic": REGISTER_IS_NEWSWIRE_NOT_QURANIC_NOTE,
    "UnvocalizedFormsAreNotCarrierStateInput": (
        UNVOCALIZED_FORMS_ARE_NOT_CARRIER_STATE_INPUT_NOTE
    ),
}

_RESULT_BEARING_WORDS: Final[frozenset[str]] = frozenset(
    {
        "result",
        "outcome",
        "decision",
        "verdict",
        "accuracy",
        "precision",
        "correct",
        "wrong",
        "measured",
        "upheld",
        "refuted",
    }
)


@dataclass(frozen=True, slots=True)
class FrozenObjecthoodPreregistration:
    """مواصفةُ قياسٍ قادمٍ مُجمَّدةٌ قبل دليله؛ لا حقلَ نتيجةٍ فيها البتّة."""

    hypothesis_as_stated: str
    predictor_rule: str
    gold_relation: str
    surface_column: str
    population_definition: str
    untestable_definition: str
    development_files: tuple[str, ...]
    held_out_files: tuple[str, ...]
    claim_stands_at_or_above: float
    claim_falls_at_or_below: float
    refused_readings: tuple[str, ...]

    def __post_init__(self) -> None:
        for label, text in (
            ("نصُّ الدعوى", self.hypothesis_as_stated),
            ("قاعدةُ التنبّؤ", self.predictor_rule),
            ("العلاقةُ المرجعية", self.gold_relation),
            ("العمودُ المقروء", self.surface_column),
            ("تعريفُ المجتمع", self.population_definition),
            ("تعريفُ المتعذّر", self.untestable_definition),
        ):
            if not isinstance(text, str) or not text.strip():
                raise ObjecthoodPreregistrationError(
                    f"{label} نصٌّ غير فارغ؛ وبندٌ مُجمَّدٌ صامتٌ لا يُلزِم أحدًا."
                )
        for label, paths in (
            ("ملفّاتُ التطوير", self.development_files),
            ("الملفّاتُ المحجوبة", self.held_out_files),
        ):
            if not isinstance(paths, tuple) or not paths:
                raise ObjecthoodPreregistrationError(
                    f"{label} أسماءُ ملفّاتٍ مُسمّاةٌ قبل القياس؛ وقسمةٌ فارغةٌ "
                    f"قسمةٌ تُختار بعدَه."
                )
            if len(set(paths)) != len(paths):
                raise ObjecthoodPreregistrationError(
                    f"{label} لا يتكرّر فيها ملفّ؛ وتكرارُه يُضاعِف وزنَه صمتًا."
                )
        overlap = set(self.development_files) & set(self.held_out_files)
        if overlap:
            raise ObjecthoodPreregistrationError(
                "الملفُّ المحجوبُ لا يكون ملفَّ تطويرٍ في آنٍ؛ وتداخلُ القسمين "
                f"يُبطِل معنى الحجب: {sorted(overlap)}."
            )
        for label, ratio in (
            ("عتبةُ القيام", self.claim_stands_at_or_above),
            ("عتبةُ السقوط", self.claim_falls_at_or_below),
        ):
            if not isinstance(ratio, float) or not 0.0 < ratio < 1.0:
                raise ObjecthoodPreregistrationError(
                    f"{label} نسبةٌ بين الصفر والواحد حصرًا؛ وعتبةٌ عند الحدَّين "
                    f"عتبةٌ لا تُخالَف."
                )
        if self.claim_falls_at_or_below >= self.claim_stands_at_or_above:
            raise ObjecthoodPreregistrationError(
                "عتبةُ السقوط دون عتبة القيام؛ وتساويهما يُلغي نطاقَ عدم "
                "الحسم ويُحوّل كلَّ رقمٍ إلى حكم."
            )
        if not isinstance(self.refused_readings, tuple) or not self.refused_readings:
            raise ObjecthoodPreregistrationError(
                "ما لا يجوز أن يُقرأ من الرقم يُسمّى قبل خروجه؛ وتركُه فراغًا "
                "يترك التأويلَ لمن يُعجبه الرقم."
            )
        for reading in self.refused_readings:
            if not isinstance(reading, str) or not reading.strip():
                raise ObjecthoodPreregistrationError("كلُّ قراءةٍ مرفوضةٍ نصٌّ غير فارغ.")

    @property
    def content_digest(self) -> str:
        """بصمةُ المواصفة مُشتقّةٌ من حروفها، فمن بدّل حرفًا بعد التجميد افتُضح."""

        return canonical_digest(
            canonical_bytes(
                {
                    "hypothesis_as_stated": self.hypothesis_as_stated,
                    "predictor_rule": self.predictor_rule,
                    "gold_relation": self.gold_relation,
                    "surface_column": self.surface_column,
                    "population_definition": self.population_definition,
                    "untestable_definition": self.untestable_definition,
                    "development_files": list(self.development_files),
                    "held_out_files": list(self.held_out_files),
                    "claim_stands_at_or_above": self.claim_stands_at_or_above,
                    "claim_falls_at_or_below": self.claim_falls_at_or_below,
                    "refused_readings": list(self.refused_readings),
                }
            )
        )

    def decide(self, precision_on_decided: float) -> ObjecthoodDecision:
        """يُطبَّق الحسمُ المُعلَنُ سلفًا على نسبةٍ مقيسة؛ ولا عتبةَ تُختار بعدها."""

        if not isinstance(precision_on_decided, float) or not (
            0.0 <= precision_on_decided <= 1.0
        ):
            raise ObjecthoodPreregistrationError(
                "النسبةُ المحسومُ عليها بين الصفر والواحد؛ وما خرج عنهما ليس نسبة."
            )
        if precision_on_decided >= self.claim_stands_at_or_above:
            return ObjecthoodDecision.CLAIM_UPHELD
        if precision_on_decided <= self.claim_falls_at_or_below:
            return ObjecthoodDecision.CLAIM_REFUTED
        return ObjecthoodDecision.CLAIM_UNDECIDED_IN_BAND


def _refuse_result_bearing_fields() -> None:
    """يمنع عند الاستيراد تسلّلَ حقلِ نتيجةٍ إلى مواصفةٍ تسبق دليلَها."""

    for field in fields(FrozenObjecthoodPreregistration):
        for word in field.name.split("_"):
            if word in _RESULT_BEARING_WORDS:
                raise ObjecthoodPreregistrationError(
                    f"`{field.name}` حقلٌ يحمل نتيجةً في مواصفةٍ قَبْلية؛ "
                    f"والمواصفةُ تسبق الدليلَ ولا تحمله."
                )


_refuse_result_bearing_fields()


OBJECTHOOD_PREREGISTRATION: Final[FrozenObjecthoodPreregistration] = (
    FrozenObjecthoodPreregistration(
        hypothesis_as_stated=(
            "«الكلمةُ التاليةُ للفعل الماضي، إذا خُتِمت بفتحة، فهي مفعولٌ به». "
            "تُشغَّل كما نُطِق بها بلا استثناءٍ ولا قاعدةٍ مضافة، وهي الدعوى "
            "التي ادُّعيت لها ١٠٠٪ ثمّ ٤٨٪، ثمّ قيست في `irab_case_readout` على "
            "وَسْم الحالة لا على وَسْم الوظيفة"
        ),
        predictor_rule=(
            "يُتنبَّأ بأنّ الكلمة مفعولٌ به إذا كانت آخرُ حركةٍ قصيرةٍ في صورتها "
            "المشكولة فتحةً (`\\u064e`) أو فتحتين (`\\u064b`)، بعد تطبيع `NFC` "
            "وحذفِ ما ليس حرفًا عربيًّا ولا حركة. ولا تُجرَّد لاحقةٌ، ولا يُحذَف "
            "حرفُ جرٍّ ملحق، ولا تُستثنى صيغةٌ: هذه القواعدُ الأربعُ من "
            "`irab_case_readout` مطروحةٌ عمدًا لأنّ المقيسَ هو الدعوى كما نُطِق بها"
        ),
        gold_relation="obj",
        surface_column="MISC:Vform",
        population_definition=(
            "كلُّ كلمةٍ نحوية (سطرٌ رقمُه صحيحٌ مفرد، لا مدًى `n-m` ولا فارغٌ "
            "`n.m`) تسبقها في الجملة نفسِها كلمةٌ نحويةٌ عمودُ `UPOS` فيها "
            "`VERB` وسماتُها تحمل `Aspect=Perf`. والسبقُ سبقُ الكلمة النحوية "
            "المباشرِ لا سبقُ الرمز المُدمَج"
        ),
        untestable_definition=(
            "موضعٌ لا يحمل حقلَ `Vform` في عمود `MISC`، أو يحمله ولا حركةَ "
            "قصيرةً ولا تنوينَ في آخر حروفه، يُسجَّل `متعذّر_القياس` ولا يُحسَب "
            "خطأً ولا صوابًا؛ وجمعُه مع أحدهما يُحرّك النسبةَ في اتجاهٍ مُختار"
        ),
        development_files=("ar_padt-ud-dev.conllu",),
        held_out_files=("ar_padt-ud-test.conllu",),
        claim_stands_at_or_above=0.9,
        claim_falls_at_or_below=0.6,
        refused_readings=(
            "لا يُقرأ الرقمُ الخارجُ من هنا حكمًا على العربية: المقيسُ نصٌّ "
            "صحفيٌّ حديثٌ مُبَصَّم، والدعوى نُطِق بها على لسانٍ قرآنيّ",
            "لا يُقرأ قيامُ الدعوى على `obj` قيامًا لها على «المفعول به» في "
            "اصطلاح النحو العربيّ؛ فالتعريفان متغايران",
            "لا يُقرأ سقوطُ الدعوى إبطالًا لصلةِ الفتحة بالنصب: الفتحةُ علامةُ "
            "حالةٍ، والحالةُ ليست الوظيفة، وذاك مقيسٌ في موضعٍ آخر",
            "لا يُقرأ رقمُ قسم التطوير رقمًا مُعلَنًا: المُعلَنُ رقمُ القسم "
            "المحجوب وحدَه، والفرقُ بينهما مقدارُ الملاءمة",
        ),
    )
)
