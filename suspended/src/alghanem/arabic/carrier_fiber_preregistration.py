"""تجميدُ مواصفة اختبار ليف الحامل قبل دليلها: محاورُ الحالة أوّلًا، ثمّ الفرضية.

هذه الوحدةُ **مواصفةٌ مُجمَّدة قبل الدليل**، على منوال
`probe_preregistration`: تُعلَن كاملةً، وتُبصَم بمحتواها، ولا تحمل حقلَ نتيجةٍ
واحدًا. وما تُجمِّده ثلاثةُ أشياءَ كان الاعتراضُ عليها سابقًا لتخطّيها:

**أوّلًا: الحالةُ ليست مجموعةً مسطّحة.** تجميدُ ثمانٍ من العلامات بوصفها

    S = {s_1, ..., s_8}

قيمًا متنافيةً يفترض ما يجب أن يُقاس: الشدّةُ تجتمع مع الحركة، والتنوينُ قد
يكون بعدًا آخرَ لا بديلًا، والمدُّ قد يكون تحوّلًا لا حالةً بديلة. فمَن سوّاها
في محورٍ واحدٍ فقد يُثبِت «ليفيةً» صنعَتْها هندسةُ الترميز لا اللغة. لذلك
تُجمَّد `StateSchema` **أوّلًا**، وتقول صراحةً أَمحورٌ واحدٌ هي أم حاصلُ محاور:

    S(C) = S_vowel(C) × S_gemination(C) × S_nunation(C) × ...

والتنافي داخلَ المحور **دعوى تُختبَر لا تُفترَض**
(`AXIS_EXCLUSIVITY_IS_TESTED_NOT_ASSUMED`)، وتعامدُ المحاور بعضِها على بعض
كذلك (`AXIS_ORTHOGONALITY_IS_DECLARED_NOT_PROVEN`)؛ ومحورٌ لم يُفحَص تنافيه
يُعلَن `DECLARED_PENDING_EXCLUSIVITY_TEST`، ومحورٌ قد يكون تحوّلًا لا حالةً
يُعلَن `DEFERRED_NOT_READ_AS_A_STATE` ولا يدخل الحالةَ المقيسة أصلًا.

**ثانيًا: فرضيةُ العدم استقلالٌ شرطيّ لا مقارنةُ أعداد.** لا:

    H0: |S_obs(C)| تحدّده freq(C)

بل:

    H0: State ⟂ Carrier | Frequency, Position, Boundary
    H1: State ⟂̸ Carrier | Frequency, Position, Boundary

ولذلك يُجمَّد مقياسان لا واحد: `CAPACITY(C) = |S_obs(C)|`، و
`COMPOSITION(C) = {s : s ∈ S_obs(C)}`؛ فحاملان قد يتساويان في السعة ويختلفان
في التركيب، والسعةُ وحدَها تُفقِد البنية (`CAPACITY_IS_NOT_COMPOSITION`).
وتمثيلُ التوزيع `P(S | C, Pos, Boundary)` مُعلَنٌ مؤجَّلًا لا مطويًّا
(`COMPOSITION_IS_NOT_DISTRIBUTION`).

**ثالثًا: المشاركاتُ المضبوطة مُجمَّدةٌ الآن، والمتعذّرُ يُسمّى لا يُختلَق.**
`FREQUENCY` و`POSITION` و`BOUNDARY` تُجمَّد ضوابطَ؛ و`WORD_ROLE` يُسجَّل
`DEFERRED_COVARIATE` لأنّه يحتاج وسمًا صرفيًّا غيرَ متاحٍ في هذه الشجرة،
واختلاقُه أسوأُ من غيابه (`WORD_ROLE_IS_A_DEFERRED_COVARIATE`). ودَورُ المدوّنة
مُعلَنٌ في المواصفة نفسِها: الفاتحةُ `CALIBRATION_WITNESS` لا اختبارٌ حاسم،
والمواصفةُ نفسُها تُشغَّل لاحقًا على مدوّنةٍ مستقلّة
(`CALIBRATION_IS_NOT_CONFIRMATION`).

**ولا سلطةَ لهذه الوحدة**: لا ولادةَ، ولا حكمَ ولادةٍ، ولا تجميدَ `E0`، ولا
تقرؤها بوّابةٌ في `kernel/`؛ وسجلُّ التجميد هنا سجلٌّ محليٌّ لطبقة التوثيق لا
سلطةَ نواة.
"""

from __future__ import annotations

from dataclasses import dataclass, field, fields
from enum import Enum
from typing import Final

from ..canonical_content import (
    CANONICAL_HASH_ALGORITHM,
    canonical_bytes,
    canonical_digest,
    is_canonical_digest,
)

__all__ = [
    "AXIS_EXCLUSIVITY_IS_TESTED_NOT_ASSUMED",
    "AXIS_ORTHOGONALITY_IS_DECLARED_NOT_PROVEN",
    "CALIBRATION_IS_NOT_CONFIRMATION",
    "CAPACITY_IS_NOT_COMPOSITION",
    "CARRIER_FIBER_PREREGISTRATION_NAMED_RESIDUALS",
    "CARRIER_FIBER_STATE_SCHEMA",
    "COMPOSITION_IS_NOT_DISTRIBUTION",
    "FROZEN_CARRIER_FIBER_SPECIFICATION",
    "GEMINATION_AXIS",
    "MADD_AXIS",
    "NULL_HYPOTHESIS_TEXT",
    "NUNATION_AXIS",
    "QUIESCENCE_AXIS",
    "VOWEL_AXIS",
    "ALTERNATIVE_HYPOTHESIS_TEXT",
    "WORD_ROLE_IS_A_DEFERRED_COVARIATE",
    "AxisStanding",
    "CanonicalCarrierFiberSpecificationEncoder",
    "CanonicalCarrierFiberSpecificationManifest",
    "CarrierFiberPreregistrationError",
    "CarrierFiberSpecificationContentBinding",
    "CarrierFiberSpecificationContentIdentity",
    "CorpusRole",
    "Covariate",
    "CovariateDeclaration",
    "CovariateStanding",
    "FiberMeasure",
    "FiberOutcome",
    "FrozenCarrierFiberSpecification",
    "FrozenPreEvidenceCarrierFiberManifest",
    "PreEvidenceCarrierFiberSpecificationRegistry",
    "StateAxisDeclaration",
    "StateSchema",
    "freeze_declared_specification",
]


class CarrierFiberPreregistrationError(ValueError):
    """رفضٌ عند الإنشاء: مواصفةٌ تُخفي جوابًا، أو محورٌ يُفترَض تنافيه."""


_CANONICALIZATION_VERSION: Final = "carrier-fiber-specification-manifest-v1"

_PREREGISTRATION_TOKEN: Final = object()


# --- مفرداتٌ مغلقة: لا عضوَ يُضاف وقتَ القراءة -------------------------------


class AxisStanding(Enum):
    """منزلةُ محورِ حالةٍ مُعلَن؛ والتنافي دعوى في الاسم لا فرضٌ في الصمت."""

    MEASURED_AS_ORTHOGONAL_AXIS = "MEASURED_AS_ORTHOGONAL_AXIS"
    DECLARED_PENDING_EXCLUSIVITY_TEST = "DECLARED_PENDING_EXCLUSIVITY_TEST"
    DEFERRED_NOT_READ_AS_A_STATE = "DEFERRED_NOT_READ_AS_A_STATE"

    @property
    def enters_the_measured_state(self) -> bool:
        """أيدخل هذا المحورُ الحالةَ المقيسة؟ الاستبعادُ مُصرَّحٌ به لا مطويّ."""

        return self is not AxisStanding.DEFERRED_NOT_READ_AS_A_STATE


class Covariate(Enum):
    """المشاركاتُ التي يجوز الضبطُ عليها، مُعلَنةً قبل أيّ رقم."""

    FREQUENCY = "FREQUENCY"
    POSITION = "POSITION"
    BOUNDARY = "BOUNDARY"
    WORD_ROLE = "WORD_ROLE"


class CovariateStanding(Enum):
    """أمضبوطةٌ هذه المشاركةُ في هذه المواصفة أم مؤجَّلةٌ بتصريح؟"""

    FROZEN_CONTROL = "FROZEN_CONTROL"
    DEFERRED_COVARIATE = "DEFERRED_COVARIATE"


class FiberMeasure(Enum):
    """مقاييسُ الليف؛ السعةُ والتركيبُ مقياسان لا مقياسٌ واحدٌ بوجهين."""

    CAPACITY = "CAPACITY"
    COMPOSITION = "COMPOSITION"
    CONDITIONAL_DISTRIBUTION = "CONDITIONAL_DISTRIBUTION"

    @property
    def is_measured_in_this_specification(self) -> bool:
        """التوزيعُ الشرطيّ مُعلَنٌ مؤجَّلًا في هذه المواصفة، لا مقيسًا فيها."""

        return self is not FiberMeasure.CONDITIONAL_DISTRIBUTION


class FiberOutcome(Enum):
    """مفردةُ المخرجات الثلاثية، مُجمَّدةً قبل الدليل لا بعده."""

    NARROWER_THAN_CHANCE = "NARROWER_THAN_CHANCE"
    INDISTINGUISHABLE_FROM_CHANCE = "INDISTINGUISHABLE_FROM_CHANCE"
    UNDETERMINED = "UNDETERMINED"


class CorpusRole(Enum):
    """دورُ المدوّنة في التشغيل؛ والمعايرةُ ليست تأكيدًا."""

    CALIBRATION_WITNESS = "CALIBRATION_WITNESS"
    CONFIRMATORY_CORPUS = "CONFIRMATORY_CORPUS"


# --- الفرضيتان نصًّا، مُجمَّدتين قبل أيّ عدّ ---------------------------------


NULL_HYPOTHESIS_TEXT: Final[str] = (
    "H0: State ⟂ Carrier | Frequency, Position, Boundary — بعد ضبط تردّد "
    "الحامل وموضعه وطرفيّته، لا تعتمد حالةُ الذرّة على هوية حاملها"
)

ALTERNATIVE_HYPOTHESIS_TEXT: Final[str] = (
    "H1: State ⟂̸ Carrier | Frequency, Position, Boundary — يبقى قيدٌ مرتبطٌ "
    "بهوية الحامل نفسِه بعد ذلك الضبط"
)


def _require_non_blank(value: object, label: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise CarrierFiberPreregistrationError(f"{label} نصٌّ غير فارغ")
    return value


def _require_positive(value: object, label: str) -> int:
    if not isinstance(value, int) or isinstance(value, bool) or value <= 0:
        raise CarrierFiberPreregistrationError(f"{label} عددٌ صحيحٌ موجب")
    return value


# --- مخطَّطُ الحالة: محاورٌ مُعلَنةٌ لا مجموعةٌ مسطّحة -------------------------


@dataclass(frozen=True, slots=True)
class StateAxisDeclaration:
    """محورُ حالةٍ واحد: اسمُه، وعلاماتُه، ومنزلتُه، ودعوى التنافي داخله.

    والعلاماتُ نقاطُ يونيكود مفردة، مُعلَنةٌ هنا لا مُستنبَطةٌ من خاصّةٍ في
    العربية؛ ومحورٌ بلا علامةٍ واحدةٍ محورٌ لا يُقاس فيُرفَض.
    """

    axis_id: str
    marks: tuple[str, ...]
    standing: AxisStanding
    exclusivity_within_axis_is_claimed: bool
    declared_reason: str

    def __post_init__(self) -> None:
        _require_non_blank(self.axis_id, "اسمُ المحور")
        _require_non_blank(self.declared_reason, "سببُ منزلة المحور")
        if not isinstance(self.standing, AxisStanding):
            raise CarrierFiberPreregistrationError("منزلةُ المحور عضوٌ في مفردتها")
        if type(self.exclusivity_within_axis_is_claimed) is not bool:
            raise CarrierFiberPreregistrationError(
                "دعوى التنافي داخل المحور قيمةٌ منطقيّةٌ مُصرَّحٌ بها"
            )
        if not isinstance(self.marks, tuple) or not self.marks:
            raise CarrierFiberPreregistrationError("محورٌ بلا علاماتٍ لا يُقاس")
        for mark in self.marks:
            if not isinstance(mark, str) or len(mark) != 1:
                raise CarrierFiberPreregistrationError("علامةُ المحور نقطةٌ واحدة")
        if len(set(self.marks)) != len(self.marks):
            raise CarrierFiberPreregistrationError("تكرّرت علامةٌ في محورٍ واحد")

    def as_canonical_content(self) -> dict[str, object]:
        """محتوى المحور للبصمة؛ كلُّ حقلٍ مذكورٌ لا مطويّ."""

        return {
            "axis_id": self.axis_id,
            "marks": list(self.marks),
            "standing": self.standing.value,
            "exclusivity_within_axis_is_claimed": (
                self.exclusivity_within_axis_is_claimed
            ),
            "declared_reason": self.declared_reason,
        }


@dataclass(frozen=True, slots=True)
class StateSchema:
    """مخطَّطُ الحالة: أمحورٌ واحدٌ هي أم حاصلُ محاور؟ مُعلَنًا لا مُستنتَجًا.

    ولا يجوز أن تشترك علامةٌ واحدةٌ في محورين، لأنّ اشتراكَها يجعل المحورين
    محورًا واحدًا بتسميتين، وهو عينُ التسطيح الذي وُجد المخطَّطُ لمنعه.
    """

    schema_id: str
    axes: tuple[StateAxisDeclaration, ...]

    def __post_init__(self) -> None:
        _require_non_blank(self.schema_id, "اسمُ المخطَّط")
        if not isinstance(self.axes, tuple) or not self.axes:
            raise CarrierFiberPreregistrationError("مخطَّطُ الحالة محورٌ فأكثر")
        for axis in self.axes:
            if type(axis) is not StateAxisDeclaration:
                raise CarrierFiberPreregistrationError("كلُّ محورٍ تصريحُ محورٍ مُعلَن")
        axis_ids = [axis.axis_id for axis in self.axes]
        if len(set(axis_ids)) != len(axis_ids):
            raise CarrierFiberPreregistrationError("تكرّر اسمُ محورٍ في المخطَّط")
        seen: set[str] = set()
        for axis in self.axes:
            for mark in axis.marks:
                if mark in seen:
                    raise CarrierFiberPreregistrationError(
                        "علامةٌ واحدةٌ في محورين تجعلهما محورًا واحدًا بتسميتين"
                    )
                seen.add(mark)
        if not self.measured_axes:
            raise CarrierFiberPreregistrationError(
                "مخطَّطٌ كلُّ محاوره مؤجَّلةٌ لا يُقاس به شيء"
            )

    @property
    def measured_axes(self) -> tuple[StateAxisDeclaration, ...]:
        """المحاورُ التي تدخل الحالةَ المقيسة، بترتيب إعلانها."""

        return tuple(
            axis for axis in self.axes if axis.standing.enters_the_measured_state
        )

    @property
    def deferred_axes(self) -> tuple[StateAxisDeclaration, ...]:
        """المحاورُ المؤجَّلةُ بتصريح؛ تُسمّى ولا تُقاس ولا تُطوى."""

        return tuple(
            axis for axis in self.axes if not axis.standing.enters_the_measured_state
        )

    @property
    def is_single_axis(self) -> bool:
        """أمحورٌ واحدٌ هي الحالة؟ الجوابُ مُشتَقٌّ من المخطَّط لا مكتوبٌ بجانبه."""

        return len(self.measured_axes) == 1

    @property
    def is_product_of_axes(self) -> bool:
        """أحاصلُ محاورَ هي الحالة؟ وهو نقيضُ سابقِه بالبناء لا بالتصريح."""

        return len(self.measured_axes) > 1

    @property
    def declared_product_shape(self) -> tuple[tuple[str, int], ...]:
        """شكلُ الحاصل المُعلَن: لكلّ محورٍ مقيسٍ اسمُه وعددُ قيمه مع الغياب.

        والغيابُ قيمةٌ في كلّ محور: حاملٌ بلا فتحةٍ ولا ضمّةٍ ولا كسرةٍ حالتُه
        على محور الحركة «غائبة»، لا «لا شيء» يُطرَح من الحساب.
        """

        return tuple((axis.axis_id, len(axis.marks) + 1) for axis in self.measured_axes)

    def as_canonical_content(self) -> dict[str, object]:
        """محتوى المخطَّط للبصمة."""

        return {
            "schema_id": self.schema_id,
            "axes": [axis.as_canonical_content() for axis in self.axes],
        }


@dataclass(frozen=True, slots=True)
class CovariateDeclaration:
    """مشاركةٌ واحدةٌ ومنزلتُها؛ والمؤجَّلُ يُسمّى ولا يُختلَق."""

    covariate: Covariate
    standing: CovariateStanding
    declared_reason: str

    def __post_init__(self) -> None:
        if not isinstance(self.covariate, Covariate):
            raise CarrierFiberPreregistrationError("المشاركةُ عضوٌ في مفردتها المغلقة")
        if not isinstance(self.standing, CovariateStanding):
            raise CarrierFiberPreregistrationError("منزلةُ المشاركة عضوٌ في مفردتها")
        _require_non_blank(self.declared_reason, "سببُ منزلة المشاركة")
        if (
            self.covariate is Covariate.WORD_ROLE
            and self.standing is CovariateStanding.FROZEN_CONTROL
        ):
            raise CarrierFiberPreregistrationError(WORD_ROLE_IS_A_DEFERRED_COVARIATE)

    def as_canonical_content(self) -> dict[str, object]:
        """محتوى التصريح للبصمة."""

        return {
            "covariate": self.covariate.value,
            "standing": self.standing.value,
            "declared_reason": self.declared_reason,
        }


# --- المواصفةُ المُجمَّدة: بلا حقلِ نتيجةٍ واحد -------------------------------


_RESULT_BEARING_FIELD_MARKERS: Final[tuple[str, ...]] = (
    "observed",
    "measured_value",
    "result",
    "outcome",
    "verdict",
    "p_value",
    "rank",
    "conclusion",
)


@dataclass(frozen=True, slots=True)
class FrozenCarrierFiberSpecification:
    """مواصفةُ اختبار ليف الحامل، مُعلَنةً كاملةً قبل دليلها.

    ولا حقلَ فيها يحمل جوابًا: لا قيمةً مرصودة، ولا رتبة، ولا احتمالًا، ولا
    حكمًا؛ وفحصُ ذلك بنيويٌّ عند الاستيراد لا وعدٌ في التوثيق.
    """

    experiment_id: str
    revision_id: str
    revision_sequence: int
    state_schema: StateSchema
    covariates: tuple[CovariateDeclaration, ...]
    measures: tuple[FiberMeasure, ...]
    outcome_vocabulary: tuple[FiberOutcome, ...]
    corpus_role: CorpusRole
    resampling_count: int
    resampling_seed: int
    alpha_permille: int
    minimum_carrier_support: int
    null_hypothesis: str
    alternative_hypothesis: str

    def __post_init__(self) -> None:
        _require_non_blank(self.experiment_id, "معرّفُ التجربة")
        _require_non_blank(self.revision_id, "معرّفُ المراجعة")
        if (
            not isinstance(self.revision_sequence, int)
            or isinstance(self.revision_sequence, bool)
            or self.revision_sequence < 0
        ):
            raise CarrierFiberPreregistrationError("ترتيبُ المراجعة عددٌ غيرُ سالب")
        if type(self.state_schema) is not StateSchema:
            raise CarrierFiberPreregistrationError(
                "المواصفةُ تلزمها `StateSchema` مُعلَنةٌ قبل أيّ عدّ"
            )
        self._check_covariates()
        self._check_measures()
        self._check_outcome_vocabulary()
        if not isinstance(self.corpus_role, CorpusRole):
            raise CarrierFiberPreregistrationError("دورُ المدوّنة عضوٌ في مفردته")
        _require_positive(self.resampling_count, "عددُ إعادات التوزيع")
        _require_positive(self.minimum_carrier_support, "أدنى دعمٍ للحامل")
        if (
            not isinstance(self.resampling_seed, int)
            or isinstance(self.resampling_seed, bool)
            or self.resampling_seed < 0
        ):
            raise CarrierFiberPreregistrationError(
                "بذرةُ إعادة التوزيع عددٌ صحيحٌ غيرُ سالبٍ مُجمَّدٌ قبل الدليل"
            )
        _require_positive(self.alpha_permille, "مستوى الرفض بالألف")
        if self.alpha_permille >= 500:
            raise CarrierFiberPreregistrationError(
                "مستوى رفضٍ يبلغ نصفَ الاحتمال ليس مستوى رفض"
            )
        if self.null_hypothesis != NULL_HYPOTHESIS_TEXT:
            raise CarrierFiberPreregistrationError(
                "نصُّ فرضية العدم هو الاستقلالُ الشرطيُّ المُجمَّد في هذه الوحدة"
            )
        if self.alternative_hypothesis != ALTERNATIVE_HYPOTHESIS_TEXT:
            raise CarrierFiberPreregistrationError(
                "نصُّ الفرضية المقابلة هو نقيضُ الاستقلال الشرطيّ بعينه"
            )

    def _check_covariates(self) -> None:
        if not isinstance(self.covariates, tuple) or not self.covariates:
            raise CarrierFiberPreregistrationError("المشاركاتُ تُعلَن غيرَ فارغة")
        for declaration in self.covariates:
            if type(declaration) is not CovariateDeclaration:
                raise CarrierFiberPreregistrationError("كلُّ مشاركةٍ تصريحٌ مُعلَن")
        declared = [declaration.covariate for declaration in self.covariates]
        if len(set(declared)) != len(declared):
            raise CarrierFiberPreregistrationError("تكرّرت مشاركةٌ في المواصفة")
        if set(declared) != set(Covariate):
            raise CarrierFiberPreregistrationError(
                "كلُّ مشاركةٍ في المفردة تُعلَن منزلتُها؛ والسكوتُ عن واحدةٍ "
                "يجعل تأجيلَها غيرَ مقروء"
            )
        controls = {
            declaration.covariate
            for declaration in self.covariates
            if declaration.standing is CovariateStanding.FROZEN_CONTROL
        }
        if controls != {Covariate.FREQUENCY, Covariate.POSITION, Covariate.BOUNDARY}:
            raise CarrierFiberPreregistrationError(
                "الضوابطُ المُجمَّدة في هذه المرحلة هي التردّدُ والموضعُ والطرفيّة"
            )

    def _check_measures(self) -> None:
        if not isinstance(self.measures, tuple) or not self.measures:
            raise CarrierFiberPreregistrationError("المقاييسُ تُعلَن غيرَ فارغة")
        for measure in self.measures:
            if not isinstance(measure, FiberMeasure):
                raise CarrierFiberPreregistrationError("كلُّ مقياسٍ عضوٌ في مفردته")
        if len(set(self.measures)) != len(self.measures):
            raise CarrierFiberPreregistrationError("تكرّر مقياسٌ في المواصفة")
        if set(self.measures) != {FiberMeasure.CAPACITY, FiberMeasure.COMPOSITION}:
            raise CarrierFiberPreregistrationError(
                "المقيسان في هذه المرحلة السعةُ والتركيبُ معًا؛ "
                f"و{CAPACITY_IS_NOT_COMPOSITION}"
            )

    def _check_outcome_vocabulary(self) -> None:
        if not isinstance(self.outcome_vocabulary, tuple):
            raise CarrierFiberPreregistrationError("مفردةُ المخرجات تُعلَن مجموعةً")
        for outcome in self.outcome_vocabulary:
            if not isinstance(outcome, FiberOutcome):
                raise CarrierFiberPreregistrationError("كلُّ مخرجٍ عضوٌ في مفردته")
        if len(set(self.outcome_vocabulary)) != len(self.outcome_vocabulary):
            raise CarrierFiberPreregistrationError("تكرّر مخرجٌ في المفردة")
        if set(self.outcome_vocabulary) != set(FiberOutcome):
            raise CarrierFiberPreregistrationError(
                "مفردةُ المخرجات تُغطّي أعضاءَها كلَّهم؛ ومخرجٌ غيرُ مُعلَنٍ "
                "مخرجٌ لا يُبلَغ بالبناء"
            )

    @property
    def frozen_controls(self) -> tuple[Covariate, ...]:
        """المشاركاتُ المضبوطة، بترتيب المفردة لا بترتيب الكتابة."""

        controls = {
            declaration.covariate
            for declaration in self.covariates
            if declaration.standing is CovariateStanding.FROZEN_CONTROL
        }
        return tuple(member for member in Covariate if member in controls)

    @property
    def deferred_covariates(self) -> tuple[Covariate, ...]:
        """المشاركاتُ المؤجَّلةُ بتصريح."""

        deferred = {
            declaration.covariate
            for declaration in self.covariates
            if declaration.standing is CovariateStanding.DEFERRED_COVARIATE
        }
        return tuple(member for member in Covariate if member in deferred)

    @property
    def freeze_key(self) -> tuple[str, str, int]:
        """هويةُ التجميد: التجربةُ ومراجعتُها وترتيبُها."""

        return (self.experiment_id, self.revision_id, self.revision_sequence)


_DECLARED_VOCABULARY_FIELDS: Final[tuple[str, ...]] = ("outcome_vocabulary",)
"""حقولُ المفردات المُعلَنة، مُستثناةً بالاسم لا بصمتٍ عن الفحص البنيويّ.

فمفردةُ المخرجات المُعلَنة قبل الدليل ليست مخرجًا؛ واستثناؤها يُكتَب هنا حتى
يُقرأ، ولا يُترَك لعبارةٍ فضفاضةٍ في قائمة العلامات تُدخِل غيرَه معه.
"""


for _field in fields(FrozenCarrierFiberSpecification):  # pragma: no cover - guard
    if _field.name in _DECLARED_VOCABULARY_FIELDS:
        continue
    if any(marker in _field.name for marker in _RESULT_BEARING_FIELD_MARKERS):
        raise RuntimeError(
            "a pre-evidence specification may not carry a result-bearing field"
        )


# --- البصمةُ والبيانُ القانونيّ: لا يصدران إلا عن المُرمِّز -------------------


@dataclass(frozen=True, slots=True)
class CarrierFiberSpecificationContentIdentity:
    """بصمةُ محتوى مواصفةٍ، لا تصدر إلا عن المُرمِّز القانونيّ."""

    algorithm: str
    canonicalization_version: str
    digest: str
    _token: object | None = field(default=None, repr=False, compare=False)

    def __post_init__(self) -> None:
        if self._token is not _PREREGISTRATION_TOKEN:
            raise CarrierFiberPreregistrationError(
                "بصمةُ المحتوى لا تصدر إلا عن "
                "CanonicalCarrierFiberSpecificationEncoder"
            )
        if (
            self.algorithm != CANONICAL_HASH_ALGORITHM
            or self.canonicalization_version != _CANONICALIZATION_VERSION
            or not is_canonical_digest(self.digest)
        ):
            raise CarrierFiberPreregistrationError("بصمةُ محتوى المواصفة غيرُ سليمة")


@dataclass(frozen=True, slots=True)
class CanonicalCarrierFiberSpecificationManifest:
    """المحتوى القانونيُّ الكاملُ لمواصفةٍ واحدة، ببصمته."""

    content_bytes: bytes
    content_id: CarrierFiberSpecificationContentIdentity
    _token: object | None = field(default=None, repr=False, compare=False)

    def __post_init__(self) -> None:
        if self._token is not _PREREGISTRATION_TOKEN:
            raise CarrierFiberPreregistrationError(
                "البيانُ القانونيُّ لا يصدر إلا عن المُرمِّز"
            )
        if canonical_digest(self.content_bytes) != self.content_id.digest:
            raise CarrierFiberPreregistrationError("بايتاتُ البيان تخالف بصمتَه")


class CanonicalCarrierFiberSpecificationEncoder:
    """المُصدِرُ الوحيدُ للبيانات القانونية لمواصفات ليف الحامل."""

    COVERAGE: Final = (
        "experiment_id",
        "revision_id",
        "revision_sequence",
        "state_schema",
        "covariates",
        "measures",
        "outcome_vocabulary",
        "corpus_role",
        "resampling_count",
        "resampling_seed",
        "alpha_permille",
        "minimum_carrier_support",
        "null_hypothesis",
        "alternative_hypothesis",
    )

    @classmethod
    def encode(
        cls, specification: FrozenCarrierFiberSpecification
    ) -> CanonicalCarrierFiberSpecificationManifest:
        if type(specification) is not FrozenCarrierFiberSpecification:
            raise CarrierFiberPreregistrationError(
                "الترميزُ القانونيُّ يلزمه مواصفةَ ليف حامل"
            )
        cls._assert_schema_coverage()
        encoded = {
            "alpha_permille": specification.alpha_permille,
            "alternative_hypothesis": specification.alternative_hypothesis,
            "corpus_role": specification.corpus_role.value,
            "covariates": [
                declaration.as_canonical_content()
                for declaration in specification.covariates
            ],
            "experiment_id": specification.experiment_id,
            "measures": [measure.value for measure in specification.measures],
            "minimum_carrier_support": specification.minimum_carrier_support,
            "null_hypothesis": specification.null_hypothesis,
            "outcome_vocabulary": [
                outcome.value for outcome in specification.outcome_vocabulary
            ],
            "resampling_count": specification.resampling_count,
            "resampling_seed": specification.resampling_seed,
            "revision_id": specification.revision_id,
            "revision_sequence": specification.revision_sequence,
            "state_schema": specification.state_schema.as_canonical_content(),
            "version": _CANONICALIZATION_VERSION,
        }
        content = canonical_bytes(encoded)
        content_id = CarrierFiberSpecificationContentIdentity(
            algorithm=CANONICAL_HASH_ALGORITHM,
            canonicalization_version=_CANONICALIZATION_VERSION,
            digest=canonical_digest(content),
            _token=_PREREGISTRATION_TOKEN,
        )
        return CanonicalCarrierFiberSpecificationManifest(
            content_bytes=content,
            content_id=content_id,
            _token=_PREREGISTRATION_TOKEN,
        )

    @classmethod
    def _assert_schema_coverage(cls) -> None:
        declared = {item.name for item in fields(FrozenCarrierFiberSpecification)}
        if declared != set(cls.COVERAGE):
            raise RuntimeError(
                "canonical carrier-fiber manifest coverage must explicitly "
                "account for every frozen specification field"
            )


@dataclass(frozen=True, slots=True)
class FrozenPreEvidenceCarrierFiberManifest:
    """محتوى مواصفةٍ مُجمَّدٌ قبل دليله؛ لا يصدر إلا عن سجلّ التجميد."""

    canonical_manifest: CanonicalCarrierFiberSpecificationManifest
    _token: object | None = field(default=None, repr=False, compare=False)

    def __post_init__(self) -> None:
        if self._token is not _PREREGISTRATION_TOKEN:
            raise CarrierFiberPreregistrationError(
                "البيانُ المُجمَّد قبل الدليل لا يصدر إلا عن سجلّ التجميد"
            )

    @property
    def content_id(self) -> CarrierFiberSpecificationContentIdentity:
        """بصمةُ المحتوى المُجمَّد."""

        return self.canonical_manifest.content_id


class PreEvidenceCarrierFiberSpecificationRegistry:
    """سجلُّ تجميدٍ محلّيٌّ لطبقة التوثيق؛ ليس سلطةَ نواةٍ ولا يشبهها في المفعول."""

    def __init__(self) -> None:
        self._frozen: dict[
            tuple[str, str, int], FrozenPreEvidenceCarrierFiberManifest
        ] = {}

    def freeze(
        self, specification: FrozenCarrierFiberSpecification
    ) -> FrozenPreEvidenceCarrierFiberManifest:
        """جمِّد محتوى مواصفةٍ قبل دليلها، وارفض تغييرًا لاحقًا تحت هويتها."""

        if type(specification) is not FrozenCarrierFiberSpecification:
            raise CarrierFiberPreregistrationError("التجميدُ يلزمه مواصفةَ ليف حامل")
        manifest = CanonicalCarrierFiberSpecificationEncoder.encode(specification)
        key = specification.freeze_key
        existing = self._frozen.get(key)
        if existing is not None:
            if existing.canonical_manifest.content_bytes != manifest.content_bytes:
                raise CarrierFiberPreregistrationError(
                    "محتوى المواصفة يخالف ما جُمِّد تحت هذه الهوية؛ فالتغييرُ بعد "
                    "التجميد يحتاج مراجعةً جديدةً لا كتابةً فوق القديمة"
                )
            return existing
        frozen = FrozenPreEvidenceCarrierFiberManifest(
            canonical_manifest=manifest, _token=_PREREGISTRATION_TOKEN
        )
        self._frozen[key] = frozen
        return frozen


@dataclass(frozen=True, slots=True)
class CarrierFiberSpecificationContentBinding:
    """يُثبِت أنّ مواصفةً حيّةً تُعيد إنتاج محتوًى مُجمَّدًا قبل دليله بعينه."""

    specification: FrozenCarrierFiberSpecification
    frozen_manifest: FrozenPreEvidenceCarrierFiberManifest
    content_id: CarrierFiberSpecificationContentIdentity = field(init=False)

    def __post_init__(self) -> None:
        if type(self.specification) is not FrozenCarrierFiberSpecification:
            raise CarrierFiberPreregistrationError("الربطُ يلزمه مواصفةَ ليف حامل")
        if type(self.frozen_manifest) is not FrozenPreEvidenceCarrierFiberManifest:
            raise CarrierFiberPreregistrationError("الربطُ يلزمه بيانًا مُجمَّدًا قبل الدليل")
        runtime = CanonicalCarrierFiberSpecificationEncoder.encode(self.specification)
        if (
            runtime.content_bytes
            != self.frozen_manifest.canonical_manifest.content_bytes
        ):
            raise CarrierFiberPreregistrationError(
                "محتوى المواصفة الحيّة لا يطابق المحتوى المُجمَّد قبل الدليل"
            )
        object.__setattr__(self, "content_id", self.frozen_manifest.content_id)


# --- المواصفةُ المُعلَنة لهذه المرحلة ------------------------------------------


_FATHA: Final = "\u064e"
_DAMMA: Final = "\u064f"
_KASRA: Final = "\u0650"
_FATHATAN: Final = "\u064b"
_DAMMATAN: Final = "\u064c"
_KASRATAN: Final = "\u064d"
_SUKUN: Final = "\u0652"
_SHADDA: Final = "\u0651"
_MADDA_ABOVE: Final = "\u0653"
_SUPERSCRIPT_ALEF: Final = "\u0670"


VOWEL_AXIS: Final = StateAxisDeclaration(
    axis_id="vowel",
    marks=(_FATHA, _DAMMA, _KASRA),
    standing=AxisStanding.MEASURED_AS_ORTHOGONAL_AXIS,
    exclusivity_within_axis_is_claimed=True,
    declared_reason=(
        "الحركاتُ الثلاثُ مُعلَنةٌ متنافيةً داخلَ محورها، والتنافي دعوى يقيسها "
        "الجدولُ صفًّا صفًّا ولا تُفترَض هنا"
    ),
)

NUNATION_AXIS: Final = StateAxisDeclaration(
    axis_id="nunation",
    marks=(_FATHATAN, _DAMMATAN, _KASRATAN),
    standing=AxisStanding.MEASURED_AS_ORTHOGONAL_AXIS,
    exclusivity_within_axis_is_claimed=True,
    declared_reason=(
        "التنوينُ مُعلَنٌ محورًا على حدةٍ لا قيمةً بديلةً في محور الحركة، لأنّ "
        "قراءتَه بديلًا تفترض ما يجب أن يُقاس"
    ),
)

GEMINATION_AXIS: Final = StateAxisDeclaration(
    axis_id="gemination",
    marks=(_SHADDA,),
    standing=AxisStanding.MEASURED_AS_ORTHOGONAL_AXIS,
    exclusivity_within_axis_is_claimed=True,
    declared_reason=(
        "الشدّةُ تجتمع مع الحركة في الرسم، فجعلُها قيمةً بديلةً في محور الحركة "
        "يصنع تنافيًا لا وجودَ له"
    ),
)

QUIESCENCE_AXIS: Final = StateAxisDeclaration(
    axis_id="quiescence",
    marks=(_SUKUN,),
    standing=AxisStanding.MEASURED_AS_ORTHOGONAL_AXIS,
    exclusivity_within_axis_is_claimed=True,
    declared_reason=(
        "السكونُ مُعلَنٌ محورًا مستقلًّا، وتنافيه مع الحركة دعوى تُقرأ من "
        "الجدول لا شرطٌ يُفرَض على القراءة"
    ),
)

MADD_AXIS: Final = StateAxisDeclaration(
    axis_id="madd",
    marks=(_MADDA_ABOVE, _SUPERSCRIPT_ALEF),
    standing=AxisStanding.DEFERRED_NOT_READ_AS_A_STATE,
    declared_reason=(
        "المدُّ قد يكون تحوّلًا أو دَورًا لا حالةً بديلة، فيُسمّى محورًا مؤجَّلًا "
        "ولا يدخل الحالةَ المقيسة حتى يُفصَل التحوّلُ عن الحالة"
    ),
    exclusivity_within_axis_is_claimed=False,
)


CARRIER_FIBER_STATE_SCHEMA: Final = StateSchema(
    schema_id="carrier-fiber-state-schema-v1",
    axes=(VOWEL_AXIS, NUNATION_AXIS, GEMINATION_AXIS, QUIESCENCE_AXIS, MADD_AXIS),
)


FROZEN_CARRIER_FIBER_SPECIFICATION: Final = FrozenCarrierFiberSpecification(
    experiment_id="carrier-fiber-conditional-independence",
    revision_id="r1",
    revision_sequence=0,
    state_schema=CARRIER_FIBER_STATE_SCHEMA,
    covariates=(
        CovariateDeclaration(
            covariate=Covariate.FREQUENCY,
            standing=CovariateStanding.FROZEN_CONTROL,
            declared_reason=(
                "تردّدُ الحامل محفوظٌ بالبناء: إعادةُ التوزيع تُبقي الحواملَ في "
                "مواضعها وتُعيد توزيعَ الحالات عليها"
            ),
        ),
        CovariateDeclaration(
            covariate=Covariate.POSITION,
            standing=CovariateStanding.FROZEN_CONTROL,
            declared_reason=(
                "الموضعُ داخل الكلمة طبقةٌ في إعادة التوزيع، فلا تنتقل حالةٌ من "
                "موضعٍ إلى موضعٍ آخر"
            ),
        ),
        CovariateDeclaration(
            covariate=Covariate.BOUNDARY,
            standing=CovariateStanding.FROZEN_CONTROL,
            declared_reason=(
                "الطرفيّةُ (أوّلُ الكلمة، وسطُها، آخرُها) طبقةٌ ثانيةٌ في إعادة "
                "التوزيع، لأنّ غيابَ حالةٍ عن حاملٍ قد يكون أثرَ موضعه"
            ),
        ),
        CovariateDeclaration(
            covariate=Covariate.WORD_ROLE,
            standing=CovariateStanding.DEFERRED_COVARIATE,
            declared_reason=(
                "دورُ الكلمة يحتاج وسمًا صرفيًّا غيرَ متاحٍ في هذه الشجرة، "
                "واختلاقُه من الرسم أسوأُ من غيابه"
            ),
        ),
    ),
    measures=(FiberMeasure.CAPACITY, FiberMeasure.COMPOSITION),
    outcome_vocabulary=tuple(FiberOutcome),
    corpus_role=CorpusRole.CALIBRATION_WITNESS,
    resampling_count=2000,
    resampling_seed=20260917,
    alpha_permille=50,
    minimum_carrier_support=5,
    null_hypothesis=NULL_HYPOTHESIS_TEXT,
    alternative_hypothesis=ALTERNATIVE_HYPOTHESIS_TEXT,
)


def freeze_declared_specification() -> CarrierFiberSpecificationContentBinding:
    """جمِّد المواصفةَ المُعلَنة في هذه الوحدة، وارجع ربطًا متحقَّقًا من محتواها.

    ومدخلٌ عديمُ الوسائط عن قصد: ما وجب له وسيطٌ لا يصلح أن يكون المواصفةَ
    التي يُقاس عليها.
    """

    registry = PreEvidenceCarrierFiberSpecificationRegistry()
    frozen = registry.freeze(FROZEN_CARRIER_FIBER_SPECIFICATION)
    return CarrierFiberSpecificationContentBinding(
        specification=FROZEN_CARRIER_FIBER_SPECIFICATION,
        frozen_manifest=frozen,
    )


# --- ما لا تحسمه هذه المواصفة، مُسمًّى ----------------------------------------


AXIS_EXCLUSIVITY_IS_TESTED_NOT_ASSUMED: Final[str] = (
    "AXIS_EXCLUSIVITY_IS_TESTED_NOT_ASSUMED: تنافي القيم داخلَ المحور الواحد "
    "دعوى مُعلَنةٌ في حقلٍ على المحور، ويُقرأ خرقُها من صفوف الوقوع؛ ومحورٌ "
    "يفترض تنافيه من غير قياسٍ يصنع بنيةً لم تُرصَد"
)

AXIS_ORTHOGONALITY_IS_DECLARED_NOT_PROVEN: Final[str] = (
    "AXIS_ORTHOGONALITY_IS_DECLARED_NOT_PROVEN: كون المحاور أبعادًا مستقلّة "
    "تصريحٌ في هذه المواصفة لا برهان؛ واجتماعُ علامتين من محورين في الرسم "
    "شاهدٌ على عدم التنافي، لا برهانٌ على استقلالٍ إحصائيّ"
)

WORD_ROLE_IS_A_DEFERRED_COVARIATE: Final[str] = (
    "WORD_ROLE_IS_A_DEFERRED_COVARIATE: دورُ الكلمة مشاركةٌ مؤجَّلةٌ لا مضبوطة؛ "
    "ويحتاج وسمًا صرفيًّا غيرَ متاحٍ هنا، فيُسجَّل تأجيلُه ولا يُختلَق تقريبُه"
)

CAPACITY_IS_NOT_COMPOSITION: Final[str] = (
    "CAPACITY_IS_NOT_COMPOSITION: حاملان قد يتساويان في |S(C)| ويختلفان في "
    "أعضائه؛ فالسعةُ وحدَها تُفقِد بنيةَ الليف، ولذلك جُمِّد المقياسان معًا"
)

COMPOSITION_IS_NOT_DISTRIBUTION: Final[str] = (
    "COMPOSITION_IS_NOT_DISTRIBUTION: التركيبُ مجموعةٌ لا توزيع؛ وقد يتساوى "
    "حاملان في S(C) ويختلف P(S | C, Pos, Boundary) اختلافًا شديدًا، "
    "والتوزيعُ مُعلَنٌ مؤجَّلًا في `FiberMeasure` لا مقيسًا هنا"
)

CALIBRATION_IS_NOT_CONFIRMATION: Final[str] = (
    "CALIBRATION_IS_NOT_CONFIRMATION: دورُ المدوّنة في هذه المواصفة "
    "`CALIBRATION_WITNESS`؛ وما يخرج منها معايرةٌ وشاهدٌ بنيويٌّ لا اختبارٌ "
    "حاسم، والحسمُ يحتاج تشغيلَ المواصفة نفسِها على مدوّنةٍ مستقلّة"
)

CARRIER_FIBER_PREREGISTRATION_NAMED_RESIDUALS: Final[dict[str, str]] = {
    "AXIS_EXCLUSIVITY_IS_TESTED_NOT_ASSUMED": AXIS_EXCLUSIVITY_IS_TESTED_NOT_ASSUMED,
    "AXIS_ORTHOGONALITY_IS_DECLARED_NOT_PROVEN": (
        AXIS_ORTHOGONALITY_IS_DECLARED_NOT_PROVEN
    ),
    "WORD_ROLE_IS_A_DEFERRED_COVARIATE": WORD_ROLE_IS_A_DEFERRED_COVARIATE,
    "CAPACITY_IS_NOT_COMPOSITION": CAPACITY_IS_NOT_COMPOSITION,
    "COMPOSITION_IS_NOT_DISTRIBUTION": COMPOSITION_IS_NOT_DISTRIBUTION,
    "CALIBRATION_IS_NOT_CONFIRMATION": CALIBRATION_IS_NOT_CONFIRMATION,
}
"""ما لا تحسمه هذه المواصفة، مُسمًّى هنا لا متروكًا ليُفترَض."""
