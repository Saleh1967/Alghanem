"""معايير تصنيفٍ أربعةٌ تُقاس مفصولةً، ونتيجةُ الاسترجاع لا تُقرأ تحليلًا.

ثبت لـ`ArabicRoundTripV1` على إيداع الفاتحة تسعٌ وعشرون من تسعٍ وعشرين. وهذا
**عددٌ كتابيٌّ يبقى أساسًا** ولا يُبنى عليه حكمٌ صرفيٌّ ولا إعرابيّ. وما يُضاف
ههنا جدولُ **تغطيةٍ** بأربعة محاور، لكلّ فئةٍ فيه عددُ كلماتٍ، ونتيجةُ استرجاعٍ،
وموضعُ فشلٍ مستقلّ.

`THE_AXES_ARE_MEASURED_APART_NOT_MERGED`: المحاورُ أربعةٌ لا تُخلَط: أصلُ
الكلمة وبنيتُها الصرفيّة، وحالتُها الإعرابيّة العامّة، وأبنيةُ الفعل المبنيّ،
وحالاتُ الفعل المُعرَب. ولا تُنسَب كلمةٌ إلى فئتَين من محورٍ واحد، فلا يُخلَط
البناءُ بالإعراب، ولا حالُ الفعل بحال الاسم.

`ROOT_IS_NOT_A_CATEGORY_BESIDE_JAMID_AND_MASDAR_AND_MUSHTAQQ`: الجذرُ **أصلٌ
صرفيٌّ محتمَل**، والجامدُ والمصدرُ والمشتقُّ أوصافٌ لبنية الكلمة؛ فليسا من بابٍ
واحد. ولذلك لا عضوَ باسم الجذر في `ClassificationCategory`، وإنّما يُسجَّل
الجذرُ في `RootRecord` إلى جانب وصف البنية. ولا يُستخرَج جذرٌ قسرًا من كلّ
كلمة: الحروفُ والأدواتُ والأسماءُ المبنيّةُ تُسجَّل
`غير_مُرخَّصٍ_لهذه_الكلمة` ولا يُفتعَل لها تحليلٌ جذريّ.

`A_MASDAR_IS_ITS_OWN_CATEGORY_WITHOUT_A_PRESUPPOSED_DERIVATION`: المصدرُ فئةُ
قياسٍ مستقلّة، ولا يُفترَض ههنا أنّ كلَّ مصدرٍ مشتقٌّ من فعل، ولا أنّ العلاقةَ
بينهما محسومةٌ في كلّ حال.

`A_DECLARED_TARGET_IS_NOT_A_RESULT`: ما يُكتَب في `COVERAGE_ITEMS` من تصنيفٍ
وعلامةٍ ودليلٍ هو **ما يُراد اختبارُه**، لا ما أثبته المحرّك. ولا حقلَ في هذه
الوحدة يحمل تصنيفًا أخرجه الخطُّ، لأنّ الخطَّ لا يُخرِج تصنيفًا: الصرفُ والنحوُ
خارجُ طبقاته كما يُقرأ في `LAYERS_NOT_IN_THIS_PIPELINE`.

`AN_UNRESOLVED_ANALYSIS_IS_NOT_A_CORRECT_ONE`: كلُّ فحصٍ تحليليٍّ ههنا يخرج
`غير_محسوم_لم_يجرِ_تحليل`، ولا يُحسَب صحيحًا. ولذلك `AnalysisAccuracy` ليست
صفرًا ولا واحدًا بل **ممتنعةٌ** لانعدام مقسومٍ عليه، وتُعرَض شرطةً باسم سببها.

`THE_ANALYTIC_REFERENCE_IS_NAMED_AND_NOT_YET_DEPOSITED`: المرجعُ المُسمّى
`MAQSAD` يُطبَع يدويًّا ولم تُودَع بايتاتُه في هذه الشجرة ولا بصمتُه. فمرتبتُه
`يُطبَع_يدويًّا`، ولا تُحسَب دقّةٌ تحليليّةٌ إلّا إذا صار `مُودَعًا_مُبصَّمًا`.

`AN_EMPTY_CATEGORY_HAS_NO_RATE`: الفئةُ التي لا كلمةَ لها في هذا الإيداع تبقى
في الجدول صفًّا بصفرٍ ولا تُحذَف، ونسبتُها ممتنعةٌ لا مئةٌ بالمئة. وخلوُّ
أربعِ فئاتٍ من أصل إحدى عشرة هو **الدليلُ المقيس** على أنّ مجتمع الفاتحة أضيقُ
من هذه المعايير، وأنّ المطلوب توسيعُ المدوّنة لا رفعُ نسبةٍ بلغت تمامها.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Final

from .arabic_round_trip_v1 import (
    LayerOutcome,
    RoundTripLayer,
    RoundTripRefusal,
    run_token,
    tokens_from_text,
)
from .fatiha_source_text import FATIHA_SOURCE_TEXT

__all__ = [
    "ANALYSIS_REFERENCE",
    "AN_EMPTY_CATEGORY_HAS_NO_RATE_NOTE",
    "AN_UNRESOLVED_ANALYSIS_IS_NOT_A_CORRECT_ONE_NOTE",
    "A_DECLARED_TARGET_IS_NOT_A_RESULT_NOTE",
    "A_MASDAR_IS_ITS_OWN_CATEGORY_WITHOUT_A_PRESUPPOSED_DERIVATION_NOTE",
    "AXIS_REFERENCE_REQUIREMENTS",
    "COVERAGE_ITEMS",
    "ROOT_IS_NOT_A_CATEGORY_BESIDE_JAMID_AND_MASDAR_AND_MUSHTAQQ_NOTE",
    "THE_ANALYTIC_REFERENCE_IS_NAMED_AND_NOT_YET_DEPOSITED_NOTE",
    "THE_AXES_ARE_MEASURED_APART_NOT_MERGED_NOTE",
    "AnalysisCheck",
    "AnalysisOutcome",
    "AnalysisQuestion",
    "AnalysisReference",
    "AxisReferenceRequirement",
    "CategoryClaim",
    "CategoryCoverage",
    "ClassificationAxis",
    "ClassificationCategory",
    "ClassificationCoverageError",
    "CoverageItem",
    "CoverageReport",
    "CoverageRow",
    "ReferenceStanding",
    "RootRecord",
    "RootStanding",
    "axis_of",
    "deposit_tokens",
    "render_coverage",
    "run_coverage",
]


class ClassificationCoverageError(ValueError):
    """رُوجِع الجدولُ بما لا يقوم به؛ ولا يُحمَل على أقربِ حالةٍ مقبولة."""


class ClassificationAxis(Enum):
    """محاورُ القياس الأربعة؛ مفردةٌ مغلقةٌ، ولكلّ محورٍ سؤالُه وعدادُه."""

    ORIGIN_AND_MORPHOLOGICAL_STRUCTURE = "ORIGIN_AND_MORPHOLOGICAL_STRUCTURE"
    GENERAL_IRAB_STANDING = "GENERAL_IRAB_STANDING"
    BUILT_VERB_FORM = "BUILT_VERB_FORM"
    INFLECTED_VERB_CASE = "INFLECTED_VERB_CASE"


class ClassificationCategory(Enum):
    """فئاتُ القياس؛ ولا عضوَ فيها باسم الجذر، فالجذرُ ليس وصفَ بنية."""

    JAMID = "JAMID"
    MASDAR = "MASDAR"
    MUSHTAQQ = "MUSHTAQQ"
    MABNI = "MABNI"
    MURAB = "MURAB"
    PAST_VERB = "PAST_VERB"
    IMPERATIVE_VERB = "IMPERATIVE_VERB"
    BUILT_PRESENT_VERB = "BUILT_PRESENT_VERB"
    PRESENT_MARFU = "PRESENT_MARFU"
    PRESENT_MANSUB = "PRESENT_MANSUB"
    PRESENT_MAJZUM = "PRESENT_MAJZUM"


_CATEGORY_AXIS: Final[dict[ClassificationCategory, ClassificationAxis]] = {
    ClassificationCategory.JAMID: (
        ClassificationAxis.ORIGIN_AND_MORPHOLOGICAL_STRUCTURE
    ),
    ClassificationCategory.MASDAR: (
        ClassificationAxis.ORIGIN_AND_MORPHOLOGICAL_STRUCTURE
    ),
    ClassificationCategory.MUSHTAQQ: (
        ClassificationAxis.ORIGIN_AND_MORPHOLOGICAL_STRUCTURE
    ),
    ClassificationCategory.MABNI: ClassificationAxis.GENERAL_IRAB_STANDING,
    ClassificationCategory.MURAB: ClassificationAxis.GENERAL_IRAB_STANDING,
    ClassificationCategory.PAST_VERB: ClassificationAxis.BUILT_VERB_FORM,
    ClassificationCategory.IMPERATIVE_VERB: ClassificationAxis.BUILT_VERB_FORM,
    ClassificationCategory.BUILT_PRESENT_VERB: ClassificationAxis.BUILT_VERB_FORM,
    ClassificationCategory.PRESENT_MARFU: ClassificationAxis.INFLECTED_VERB_CASE,
    ClassificationCategory.PRESENT_MANSUB: ClassificationAxis.INFLECTED_VERB_CASE,
    ClassificationCategory.PRESENT_MAJZUM: ClassificationAxis.INFLECTED_VERB_CASE,
}


def axis_of(category: ClassificationCategory) -> ClassificationAxis:
    """محورُ هذه الفئة؛ ولا فئةَ بلا محورٍ مُسمًّى، فالخلطُ يبدأ من ههنا."""

    if not isinstance(category, ClassificationCategory):
        raise ClassificationCoverageError("الفئةُ عضوٌ في مفردتها المغلقة لا نصٌّ حُرّ")
    try:
        return _CATEGORY_AXIS[category]
    except KeyError as error:  # pragma: no cover - يُمنَع ببناء المفردة
        raise ClassificationCoverageError(
            f"الفئةُ {category.value} بلا محورٍ مُسنَد"
        ) from error


_MARKER_BEARING_AXES: Final[frozenset[ClassificationAxis]] = frozenset(
    {
        ClassificationAxis.GENERAL_IRAB_STANDING,
        ClassificationAxis.BUILT_VERB_FORM,
        ClassificationAxis.INFLECTED_VERB_CASE,
    }
)
"""المحاورُ التي يسأل سؤالُها عن علامةٍ ودليل؛ ومحورُ البنية ليس منها."""


class RootStanding(Enum):
    """منزلةُ الجذر؛ والعليا بلا مدخلٍ حتى يُودَع مرجعٌ يُقرأ منه."""

    READ_FROM_A_DEPOSITED_REFERENCE = "مقروء_من_مرجعٍ_مُودَع"
    AWAITING_THE_REFERENCE = "مُرخَّص_ينتظر_المرجع"
    NOT_LICENSED_FOR_THIS_WORD = "غير_مُرخَّصٍ_لهذه_الكلمة"


class ReferenceStanding(Enum):
    """منزلةُ المرجع التحليليّ؛ ولا تُحسَب دقّةٌ إلّا في العليا."""

    DEPOSITED_AND_FINGERPRINTED = "مُودَع_مُبصَّم"
    BEING_TRANSCRIBED_BY_HAND = "يُطبَع_يدويًّا"
    NAMED_ONLY = "مُسمًّى_فقط"


class AnalysisQuestion(Enum):
    """ما يُسأل عنه في كلّ دعوى: الفئةُ، ثمّ علامتُها، ثمّ دليلُها."""

    CATEGORY = "CATEGORY"
    MARKER = "MARKER"
    EVIDENCE = "EVIDENCE"


class AnalysisOutcome(Enum):
    """حكمُ الفحص التحليليّ؛ واثنان منه بلا مدخلٍ حتى يُودَع المرجع."""

    MATCHED_THE_REFERENCE = "طابق_المرجع"
    CONTRADICTED_THE_REFERENCE = "خالف_المرجع"
    UNRESOLVED_NO_ANALYZER_RAN = "غير_محسوم_لم_يجرِ_تحليل"


@dataclass(frozen=True, slots=True)
class RootRecord:
    """سجلُّ الجذر إلى جانب وصف البنية؛ ولا يُكتَب جذرٌ بلا مرجعٍ مُودَع."""

    standing: RootStanding
    root: str | None
    why: str

    def __post_init__(self) -> None:
        if not isinstance(self.standing, RootStanding):
            raise ClassificationCoverageError("منزلةُ الجذر عضوٌ في مفردتها المغلقة")
        if self.standing is RootStanding.READ_FROM_A_DEPOSITED_REFERENCE:
            raise ClassificationCoverageError(
                "لا مرجعَ جذريٌّ مُودَعٌ في هذه الشجرة، فلا تُرفَع منزلةُ الجذر بالكتابة"
            )
        if self.root is not None:
            raise ClassificationCoverageError(
                "لا يُكتَب جذرٌ إلّا مقروءًا من مرجعٍ مُودَع، ولا يُستخرَج قسرًا"
            )
        if not self.why.strip():
            raise ClassificationCoverageError("منزلةُ الجذر تُعلَّل ولا تُترَك بلا سبب")


@dataclass(frozen=True, slots=True)
class CategoryClaim:
    """دعوى تصنيفٍ واحدةٌ مُعلَنةٌ للاختبار: فئةٌ، ومعها علامتُها ودليلُها."""

    category: ClassificationCategory
    declared_marker: str | None
    declared_evidence: str | None

    def __post_init__(self) -> None:
        axis = axis_of(self.category)
        wants_marker = axis in _MARKER_BEARING_AXES
        has_marker = bool(self.declared_marker and self.declared_marker.strip())
        has_evidence = bool(self.declared_evidence and self.declared_evidence.strip())
        if wants_marker and not (has_marker and has_evidence):
            raise ClassificationCoverageError(
                f"سؤالُ محور {axis.value} يطلب علامةً ودليلًا، فلا تُعلَن فئتُه بدونهما"
            )
        if not wants_marker and (has_marker or has_evidence):
            raise ClassificationCoverageError(
                "محورُ البنية الصرفيّة لا علامةَ إعرابٍ فيه؛ ولا يُخلَط البناءُ بالإعراب"
            )

    @property
    def questions(self) -> tuple[AnalysisQuestion, ...]:
        """ما يُفحَص في هذه الدعوى؛ مشتقٌّ من محورها لا مكتوبٌ إلى جانبها."""

        if axis_of(self.category) in _MARKER_BEARING_AXES:
            return (
                AnalysisQuestion.CATEGORY,
                AnalysisQuestion.MARKER,
                AnalysisQuestion.EVIDENCE,
            )
        return (AnalysisQuestion.CATEGORY,)


def deposit_tokens() -> tuple[bytes, ...]:
    """كلماتُ الإيداع كما يقرؤها الخطّ؛ لا تُعاد كتابتُها في هذه الوحدة."""

    return tokens_from_text(FATIHA_SOURCE_TEXT)


@dataclass(frozen=True, slots=True)
class CoverageItem:
    """كلمةٌ من الإيداع بدعاواها المُعلَنة؛ وسطحُها مأخوذٌ لا مُعاد كتابته."""

    key: str
    token_index: int
    claims: tuple[CategoryClaim, ...]
    root_record: RootRecord
    why_it_is_here: str

    def __post_init__(self) -> None:
        if not self.key.strip():
            raise ClassificationCoverageError("لكلّ كلمةٍ مفتاحٌ غيرُ فارغ")
        tokens = deposit_tokens()
        if not 0 <= self.token_index < len(tokens):
            raise ClassificationCoverageError(
                "موضعُ الكلمة يُحيل إلى الإيداع نفسِه، ولا يُكتَب سطحٌ من خارجه"
            )
        if not self.claims:
            raise ClassificationCoverageError("لا تدخل كلمةٌ الجدولَ بلا دعوى واحدة")
        axes = [axis_of(claim.category) for claim in self.claims]
        if len(set(axes)) != len(axes):
            raise ClassificationCoverageError(
                "لا تُنسَب كلمةٌ إلى فئتَين من محورٍ واحد؛ والمحاورُ تُقاس مفصولة"
            )
        if not self.why_it_is_here.strip():
            raise ClassificationCoverageError("لا تدخل كلمةٌ الجدولَ بلا سببٍ مكتوب")

    @property
    def raw_bytes(self) -> bytes:
        """بايتاتُ هذه الكلمة من الإيداع؛ مشتقّةٌ بالموضع لا منسوخةٌ باليد."""

        return deposit_tokens()[self.token_index]

    @property
    def surface(self) -> str:
        """سطحُ الكلمة؛ يُقرأ من بايتات الإيداع ولا يُكتَب إلى جانبها."""

        return self.raw_bytes.decode("utf-8")

    @property
    def categories(self) -> tuple[ClassificationCategory, ...]:
        return tuple(claim.category for claim in self.claims)


@dataclass(frozen=True, slots=True)
class AnalysisCheck:
    """فحصٌ تحليليٌّ واحد: أيُّ سؤالٍ، وفي أيّ فئة، وبأيّ حكم."""

    category: ClassificationCategory
    question: AnalysisQuestion
    outcome: AnalysisOutcome

    def __post_init__(self) -> None:
        if self.outcome is not AnalysisOutcome.UNRESOLVED_NO_ANALYZER_RAN:
            raise ClassificationCoverageError(
                "لا محلّلَ صرفيًّا ولا إعرابيًّا في هذا الخطّ، فلا يُكتَب حكمٌ محسوم"
            )

    @property
    def is_resolved(self) -> bool:
        """أحُسِم الفحصُ؟ وغيرُ المحسوم لا يُعَدّ صحيحًا ولا يدخل المقسومَ عليه."""

        return self.outcome in (
            AnalysisOutcome.MATCHED_THE_REFERENCE,
            AnalysisOutcome.CONTRADICTED_THE_REFERENCE,
        )


@dataclass(frozen=True, slots=True)
class CoverageRow:
    """صفُّ كلمةٍ واحدة: أين وقفت كتابيًّا، وما فُحص من دعاواها تحليليًّا."""

    item: CoverageItem
    reached: RoundTripLayer
    outcome: LayerOutcome
    refusal: RoundTripRefusal | None
    checks: tuple[AnalysisCheck, ...]

    def __post_init__(self) -> None:
        if not self.checks:
            raise ClassificationCoverageError("صفٌّ بلا فحصٍ واحدٍ ليس صفَّ تغطية")

    @property
    def bytes_returned(self) -> bool:
        """أعادت الكلمةُ بايتاتها كما دخلت؟ مقروءٌ من التشغيل لا من دعوى."""

        return (
            self.reached is RoundTripLayer.FINAL_BYTES
            and self.outcome is LayerOutcome.RECONSTRUCTED
        )

    @property
    def failure_position(self) -> str:
        """موضعُ الفشل مستقلًّا: الطبقةُ التي وقفت عندها، وحكمُها، وسببُه."""

        if self.bytes_returned:
            return "—"
        reason = "" if self.refusal is None else f"/{self.refusal.value}"
        return f"{self.reached.value}/{self.outcome.value}{reason}"


@dataclass(frozen=True, slots=True)
class CategoryCoverage:
    """تغطيةُ فئةٍ واحدة: عددُ كلماتها، واسترجاعُها، وفحوصُها، وفشلُها."""

    category: ClassificationCategory
    rows: tuple[CoverageRow, ...]

    @property
    def axis(self) -> ClassificationAxis:
        return axis_of(self.category)

    @property
    def word_total(self) -> int:
        return len(self.rows)

    @property
    def returned_total(self) -> int:
        return sum(1 for row in self.rows if row.bytes_returned)

    @property
    def refused_total(self) -> int:
        return sum(1 for row in self.rows if row.outcome is LayerOutcome.REFUSED)

    @property
    def mismatched_total(self) -> int:
        return sum(1 for row in self.rows if row.outcome is LayerOutcome.MISMATCHED)

    @property
    def checks(self) -> tuple[AnalysisCheck, ...]:
        """فحوصُ هذه الفئة وحدَها؛ فحصُ فئةٍ أخرى لا يُحسَب ههنا."""

        return tuple(
            check
            for row in self.rows
            for check in row.checks
            if check.category is self.category
        )

    @property
    def resolved_total(self) -> int:
        return sum(1 for check in self.checks if check.is_resolved)

    @property
    def matched_total(self) -> int:
        return sum(
            1
            for check in self.checks
            if check.outcome is AnalysisOutcome.MATCHED_THE_REFERENCE
        )

    @property
    def unresolved_total(self) -> int:
        """الفحوصُ التي لم تُحسَم؛ تُعرَض ولا تُحسَب تصنيفًا صحيحًا."""

        return len(self.checks) - self.resolved_total

    @property
    def round_trip(self) -> float | None:
        """نسبةُ الاسترجاع؛ ممتنعةٌ في فئةٍ خاليةٍ ولا تُكتَب مئةً بالمئة."""

        if self.word_total == 0:
            return None
        return self.returned_total / self.word_total

    @property
    def analysis_accuracy(self) -> float | None:
        """دقّةُ التحليل؛ ممتنعةٌ ما لم يُحسَم فحصٌ واحدٌ بمرجعٍ مُودَع."""

        if self.resolved_total == 0:
            return None
        return self.matched_total / self.resolved_total

    @property
    def failure_positions(self) -> tuple[str, ...]:
        """مواضعُ الفشل في هذه الفئة؛ لكلّ فئةٍ موضعُها مستقلًّا."""

        return tuple(row.failure_position for row in self.rows if not row.bytes_returned)


@dataclass(frozen=True, slots=True)
class AxisReferenceRequirement:
    """ما يلزم من مرجعٍ مستقلٍّ ليُقاس محورٌ من المحاور الأربعة."""

    axis: ClassificationAxis
    question_the_axis_asks: str
    what_the_reference_must_supply: str

    def __post_init__(self) -> None:
        if not isinstance(self.axis, ClassificationAxis):
            raise ClassificationCoverageError("المحورُ عضوٌ في مفردته المغلقة")
        if not self.question_the_axis_asks.strip():
            raise ClassificationCoverageError("سؤالُ المحور يُكتَب ولا يُطوى")
        if not self.what_the_reference_must_supply.strip():
            raise ClassificationCoverageError("شرطُ المرجع يُكتَب ولا يُترَك فارغًا")


@dataclass(frozen=True, slots=True)
class AnalysisReference:
    """المرجعُ التحليليُّ المُسمّى: اسمُه، ومنزلتُه، وبصمتُه إن أُودع."""

    name: str
    standing: ReferenceStanding
    digest: str | None
    how_it_is_being_obtained: str

    def __post_init__(self) -> None:
        if not self.name.strip():
            raise ClassificationCoverageError("المرجعُ يُسمّى باسمه لا بوصفه")
        if not isinstance(self.standing, ReferenceStanding):
            raise ClassificationCoverageError("منزلةُ المرجع عضوٌ في مفردتها المغلقة")
        deposited = self.standing is ReferenceStanding.DEPOSITED_AND_FINGERPRINTED
        if deposited and not (self.digest and self.digest.strip()):
            raise ClassificationCoverageError("لا يُقال مُودَعٌ مُبصَّمٌ بلا بصمةٍ مكتوبة")
        if not deposited and self.digest is not None:
            raise ClassificationCoverageError(
                "بصمةٌ بلا بايتاتٍ مُودَعةٍ دعوى إيداعٍ لم يقع"
            )
        if not self.how_it_is_being_obtained.strip():
            raise ClassificationCoverageError("طريقُ تحصيل المرجع يُكتَب ولا يُطوى")

    @property
    def can_settle_an_analysis(self) -> bool:
        """أيصلح هذا المرجعُ لحسم فحص؟ لا يصلح حتى تُودَع بايتاتُه وتُبصَّم."""

        return self.standing is ReferenceStanding.DEPOSITED_AND_FINGERPRINTED


@dataclass(frozen=True, slots=True)
class CoverageReport:
    """تقريرُ التغطية: صفوفُ الكلمات، وتغطيةُ كلِّ فئةٍ من الإحدى عشرة."""

    rows: tuple[CoverageRow, ...]
    coverages: tuple[CategoryCoverage, ...]
    reference: AnalysisReference

    def __post_init__(self) -> None:
        if not self.rows:
            raise ClassificationCoverageError("تقريرٌ بلا صفٍّ واحدٍ ليس تقريرًا")
        keys = [row.item.key for row in self.rows]
        if len(set(keys)) != len(keys):
            raise ClassificationCoverageError("مفاتيحُ الجدول لا تتكرّر")
        listed = [coverage.category for coverage in self.coverages]
        if set(listed) != set(ClassificationCategory) or len(listed) != len(set(listed)):
            raise ClassificationCoverageError(
                "كلُّ فئةٍ تُعرَض ولو خلت من الكلمات؛ والخاليةُ لا تُحذَف من الجدول"
            )

    def coverage(self, category: ClassificationCategory) -> CategoryCoverage:
        """تغطيةُ فئةٍ بعينها؛ وتُطلَب بعضوٍ مغلقٍ لا بنصٍّ حُرّ."""

        for coverage in self.coverages:
            if coverage.category is category:
                return coverage
        raise ClassificationCoverageError(f"لا صفَّ للفئة {category!r}")

    def axis_coverages(
        self, axis: ClassificationAxis
    ) -> tuple[CategoryCoverage, ...]:
        """تغطياتُ محورٍ واحد؛ ولا تُخلَط بتغطيات محورٍ آخر."""

        if not isinstance(axis, ClassificationAxis):
            raise ClassificationCoverageError("المحورُ عضوٌ في مفردته المغلقة")
        return tuple(
            coverage for coverage in self.coverages if coverage.axis is axis
        )

    @property
    def word_total(self) -> int:
        return len(self.rows)

    @property
    def returned_total(self) -> int:
        return sum(1 for row in self.rows if row.bytes_returned)

    @property
    def unresolved_total(self) -> int:
        """كلُّ فحصٍ لم يُحسَم في التقرير؛ مشتقٌّ بالعدّ لا مكتوب."""

        return sum(
            1 for row in self.rows for check in row.checks if not check.is_resolved
        )

    @property
    def empty_categories(self) -> tuple[ClassificationCategory, ...]:
        """الفئاتُ الخاليةُ من الكلمات؛ وهي قياسُ ضيقِ هذا المجتمع لا عيبُه."""

        return tuple(
            coverage.category
            for coverage in self.coverages
            if coverage.word_total == 0
        )


ANALYSIS_REFERENCE: Final[AnalysisReference] = AnalysisReference(
    name="MAQSAD",
    standing=ReferenceStanding.BEING_TRANSCRIBED_BY_HAND,
    digest=None,
    how_it_is_being_obtained=(
        "يُطبَع يدويًّا ولم تُودَع بايتاتُه في هذه الشجرة، فلا بصمةَ له بعد؛ "
        "ومتى أُودع وبُصِّم صار حسمُ الفحوص ممكنًا بالتشغيل لا بالقول"
    ),
)
"""المرجعُ التحليليُّ المُسمّى؛ ومنزلتُه تمنع حسمَ فحصٍ واحدٍ حتى اليوم."""


AXIS_REFERENCE_REQUIREMENTS: Final[tuple[AxisReferenceRequirement, ...]] = (
    AxisReferenceRequirement(
        axis=ClassificationAxis.ORIGIN_AND_MORPHOLOGICAL_STRUCTURE,
        question_the_axis_asks=(
            "ما أصلُ الكلمة؟ وما نوعُ بنيتها؟ وهل الاشتقاقُ ثابتٌ بدليل؟"
        ),
        what_the_reference_must_supply=(
            "وصفُ بنيةٍ لكلّ كلمةٍ (جامدٌ أو مصدرٌ أو مشتقّ)، ومعه — حيث يُرخَّص — "
            "جذرٌ مُصرَّحٌ به، وتصريحٌ بما لا جذرَ له؛ ولا يُقبَل جذرٌ مُستنبَطٌ من "
            "الشكل المقيس نفسِه"
        ),
    ),
    AxisReferenceRequirement(
        axis=ClassificationAxis.GENERAL_IRAB_STANDING,
        question_the_axis_asks=(
            "هل يلزم آخرُ الكلمة صورةً واحدة، أم يتغيّر بحسب العامل؟"
        ),
        what_the_reference_must_supply=(
            "حكمُ بناءٍ أو إعرابٍ لكلّ كلمةٍ موضعًا موضعًا، لا قاعدةٌ عامّةٌ "
            "تُطبَّق، لأنّ الحكمَ ههنا سياقيٌّ لا صُوَريّ"
        ),
    ),
    AxisReferenceRequirement(
        axis=ClassificationAxis.BUILT_VERB_FORM,
        question_the_axis_asks="هل حدّد النظامُ نوعَ الفعل وعلامةَ بنائه؟",
        what_the_reference_must_supply=(
            "نوعُ الفعل المبنيّ وعلامةُ بنائه وسببُها، ومنها بناءُ المضارع في "
            "مواضعه؛ ولا يُقبَل حكمٌ بلا علامةٍ مُسمّاة"
        ),
    ),
    AxisReferenceRequirement(
        axis=ClassificationAxis.INFLECTED_VERB_CASE,
        question_the_axis_asks="هل حدّد النظامُ حالةَ الإعراب وعلامتَها ودليلَها؟",
        what_the_reference_must_supply=(
            "حالةُ المضارع (رفعٌ أو نصبٌ أو جزم) وعلامتُها والعاملُ الدالُّ "
            "عليها؛ والعاملُ دليلٌ لا زينةٌ في العبارة"
        ),
    ),
)
"""شرطُ القياس، محورًا محورًا؛ ولا يُقاس محورٌ بمرجعٍ لمحورٍ آخر."""


COVERAGE_ITEMS: Final[tuple[CoverageItem, ...]] = (
    CoverageItem(
        key="allathina",
        token_index=21,
        claims=(
            CategoryClaim(
                category=ClassificationCategory.JAMID,
                declared_marker=None,
                declared_evidence=None,
            ),
            CategoryClaim(
                category=ClassificationCategory.MABNI,
                declared_marker="مبنيٌّ على الفتح",
                declared_evidence="اسمٌ موصولٌ يلزم آخرُه صورةً واحدة",
            ),
        ),
        root_record=RootRecord(
            standing=RootStanding.NOT_LICENSED_FOR_THIS_WORD,
            root=None,
            why="اسمٌ مبنيٌّ لا يُتاح له تحليلٌ جذريٌّ مُرخَّص، فلا يُنتزَع منه جذرٌ قسرًا",
        ),
        why_it_is_here=(
            "الموضعُ المطلوبُ اختبارُه: أتُحفَظ هويّتُها اسمًا موصولًا فلا تُقرأ "
            "«أل تعريف + ذين»؟"
        ),
    ),
    CoverageItem(
        key="ad_dallina",
        token_index=28,
        claims=(
            CategoryClaim(
                category=ClassificationCategory.MUSHTAQQ,
                declared_marker=None,
                declared_evidence=None,
            ),
            CategoryClaim(
                category=ClassificationCategory.MURAB,
                declared_marker="مجرورٌ بالياء",
                declared_evidence="جمعُ مذكّرٍ سالمٌ مجرورٌ في هذا السياق",
            ),
        ),
        root_record=RootRecord(
            standing=RootStanding.AWAITING_THE_REFERENCE,
            root=None,
            why="مشتقٌّ يُتاح له تحليلٌ جذريّ، ولم يُقرأ جذرُه من مرجعٍ مُودَع",
        ),
        why_it_is_here="لامُها من لام التعريف، وهي الطرفُ الآخرُ في موضع الخلط",
    ),
    CoverageItem(
        key="ihdina",
        token_index=17,
        claims=(
            CategoryClaim(
                category=ClassificationCategory.IMPERATIVE_VERB,
                declared_marker="مبنيٌّ على حذف حرف العلّة",
                declared_evidence="فعلُ أمرٍ معتلُّ الآخر، متّصلٌ بضمير",
            ),
            CategoryClaim(
                category=ClassificationCategory.MABNI,
                declared_marker="مبنيٌّ على حذف حرف العلّة",
                declared_evidence="الأمرُ مبنيٌّ لا يتغيّر آخرُه بالعامل",
            ),
        ),
        root_record=RootRecord(
            standing=RootStanding.AWAITING_THE_REFERENCE,
            root=None,
            why="فعلٌ يُتاح له تحليلٌ جذريّ، ولم يُقرأ جذرُه من مرجعٍ مُودَع",
        ),
        why_it_is_here="أمرٌ معتلٌّ متّصلٌ بضمير: نوعُ الفعل وعلامةُ بنائه معًا",
    ),
    CoverageItem(
        key="nabudu",
        token_index=14,
        claims=(
            CategoryClaim(
                category=ClassificationCategory.PRESENT_MARFU,
                declared_marker="مرفوعٌ بالضمّة",
                declared_evidence="مضارعٌ لم يسبقه ناصبٌ ولا جازم",
            ),
            CategoryClaim(
                category=ClassificationCategory.MURAB,
                declared_marker="مرفوعٌ بالضمّة",
                declared_evidence="يتغيّر آخرُه بحسب العامل الداخل عليه",
            ),
        ),
        root_record=RootRecord(
            standing=RootStanding.AWAITING_THE_REFERENCE,
            root=None,
            why="فعلٌ يُتاح له تحليلٌ جذريّ، ولم يُقرأ جذرُه من مرجعٍ مُودَع",
        ),
        why_it_is_here="مضارعٌ مُعرَب: الحالةُ وعلامتُها ودليلُها ثلاثةُ فحوصٍ لا واحد",
    ),
    CoverageItem(
        key="anamta",
        token_index=22,
        claims=(
            CategoryClaim(
                category=ClassificationCategory.PAST_VERB,
                declared_marker="مبنيٌّ على السكون",
                declared_evidence="اتّصلت به تاءُ الفاعل",
            ),
            CategoryClaim(
                category=ClassificationCategory.MABNI,
                declared_marker="مبنيٌّ على السكون",
                declared_evidence="الماضي مبنيٌّ لا يدخله عاملُ إعراب",
            ),
        ),
        root_record=RootRecord(
            standing=RootStanding.AWAITING_THE_REFERENCE,
            root=None,
            why="فعلٌ يُتاح له تحليلٌ جذريّ، ولم يُقرأ جذرُه من مرجعٍ مُودَع",
        ),
        why_it_is_here="ماضٍ اتّصلت به تاءُ الفاعل: البناءُ وعلامتُه وسببُها",
    ),
)
"""كلماتُ الجدول: خمسٌ من الإيداع، ودعاواها **أهدافُ اختبارٍ لا نتائج**."""


def run_coverage(
    items: tuple[CoverageItem, ...] = COVERAGE_ITEMS,
    reference: AnalysisReference = ANALYSIS_REFERENCE,
) -> CoverageReport:
    """شغِّل التغطية: استرجاعٌ بالتشغيل، وفحوصٌ تحليليّةٌ لا تُحسَم بلا مرجع."""

    if not items:
        raise ClassificationCoverageError("جدولٌ بلا كلمةٍ واحدةٍ لا يُشغَّل")
    if reference.can_settle_an_analysis:
        raise ClassificationCoverageError(
            "أُعلن المرجعُ مُودَعًا، فلا يُشغَّل هذا الجدولُ الذي لا يقرأ مرجعًا"
        )
    rows: list[CoverageRow] = []
    for item in items:
        trace = run_token(item.raw_bytes)
        checks = tuple(
            AnalysisCheck(
                category=claim.category,
                question=question,
                outcome=AnalysisOutcome.UNRESOLVED_NO_ANALYZER_RAN,
            )
            for claim in item.claims
            for question in claim.questions
        )
        rows.append(
            CoverageRow(
                item=item,
                reached=trace.reached,
                outcome=trace.outcome,
                refusal=trace.refusal,
                checks=checks,
            )
        )
    coverages = tuple(
        CategoryCoverage(
            category=category,
            rows=tuple(row for row in rows if category in row.item.categories),
        )
        for category in ClassificationCategory
    )
    return CoverageReport(
        rows=tuple(rows), coverages=coverages, reference=reference
    )


def _rate(value: float | None) -> str:
    return "—" if value is None else f"{value * 100:.4f}%"


def render_coverage(report: CoverageReport) -> str:
    """اعرض التغطيةَ محورًا محورًا؛ ولا يُدمَج عمودُ الاسترجاع بعمود التحليل."""

    lines: list[str] = []
    for axis in ClassificationAxis:
        lines.append(axis.value)
        lines.append(
            f"  {'category':<20}{'words':>6}{'returned':>10}{'RoundTrip':>12}"
            f"{'REFUSED':>9}{'MISMATCH':>10}{'UNRESOLVED':>12}{'Accuracy':>10}"
        )
        for coverage in report.axis_coverages(axis):
            lines.append(
                f"  {coverage.category.value:<20}{coverage.word_total:>6}"
                f"{coverage.returned_total:>10}{_rate(coverage.round_trip):>12}"
                f"{coverage.refused_total:>9}{coverage.mismatched_total:>10}"
                f"{coverage.unresolved_total:>12}"
                f"{_rate(coverage.analysis_accuracy):>10}"
            )
        lines.append("")
    lines.append("failure positions, per category and independent:")
    for coverage in report.coverages:
        positions = coverage.failure_positions
        shown = "—" if not positions else " ".join(positions)
        lines.append(f"  {coverage.category.value:<20}{shown}")
    lines.append("")
    lines.append(
        f"words: {report.word_total}; bytes returned: {report.returned_total}"
        f"/{report.word_total}; unresolved analyses: {report.unresolved_total}"
    )
    lines.append(
        f"empty categories: {len(report.empty_categories)}/"
        f"{len(ClassificationCategory)} — مجتمعُ الفاتحة أضيقُ من هذه المعايير"
    )
    lines.append(
        f"analytic reference: {report.reference.name} "
        f"({report.reference.standing.value}) — "
        "ولا تُحسَب دقّةُ تحليلٍ قبل إيداعه وتبصيمه"
    )
    return "\n".join(lines)


THE_AXES_ARE_MEASURED_APART_NOT_MERGED_NOTE: Final[str] = (
    "TheAxesAreMeasuredApartNotMerged: المحاورُ أربعةٌ لكلٍّ منها عدّادُه وسؤالُه "
    "وموضعُ فشله، ولا تُنسَب كلمةٌ إلى فئتَين من محورٍ واحد؛ فلا يُخلَط أصلُ "
    "الكلمة ببنيتها، ولا البناءُ بالإعراب، ولا حالُ الفعل بحال الاسم"
)

ROOT_IS_NOT_A_CATEGORY_BESIDE_JAMID_AND_MASDAR_AND_MUSHTAQQ_NOTE: Final[str] = (
    "RootIsNotACategoryBesideJamidAndMasdarAndMushtaqq: الجذرُ أصلٌ صرفيٌّ "
    "محتمَل، والجامدُ والمصدرُ والمشتقُّ أوصافُ بنية؛ فلا عضوَ للجذر في مفردة "
    "الفئات، ويُسجَّل في `RootRecord` إلى جانب الوصف، ولا يُنتزَع من الحروف "
    "والأدوات والأسماء المبنيّة قسرًا"
)

A_MASDAR_IS_ITS_OWN_CATEGORY_WITHOUT_A_PRESUPPOSED_DERIVATION_NOTE: Final[str] = (
    "AMasdarIsItsOwnCategoryWithoutAPresupposedDerivation: المصدرُ فئةُ قياسٍ "
    "مستقلّة، ولا يُفترَض أنّ كلَّ مصدرٍ مشتقٌّ من فعل، ولا أنّ العلاقةَ بينهما "
    "محسومةٌ في كلّ حال"
)

A_DECLARED_TARGET_IS_NOT_A_RESULT_NOTE: Final[str] = (
    "ADeclaredTargetIsNotAResult: ما في `COVERAGE_ITEMS` من فئةٍ وعلامةٍ ودليلٍ "
    "هو المطلوبُ اختبارُه لا المُثبَت؛ ولا يُخرِج هذا الخطُّ تصنيفًا أصلًا، "
    "فالصرفُ والنحوُ خارجُ طبقاته"
)

AN_UNRESOLVED_ANALYSIS_IS_NOT_A_CORRECT_ONE_NOTE: Final[str] = (
    "AnUnresolvedAnalysisIsNotACorrectOne: الفحصُ غيرُ المحسوم لا يُعَدّ صحيحًا "
    "ولا يدخل مقسومَ `AnalysisAccuracy` عليه؛ فالدقّةُ ممتنعةٌ لا صفرٌ ولا واحد، "
    "وتُعرَض شرطةً باسم سببها"
)

THE_ANALYTIC_REFERENCE_IS_NAMED_AND_NOT_YET_DEPOSITED_NOTE: Final[str] = (
    "TheAnalyticReferenceIsNamedAndNotYetDeposited: `MAQSAD` مرجعٌ مُسمًّى "
    "يُطبَع يدويًّا، ولم تُودَع بايتاتُه ولا بصمتُه؛ فمنزلتُه `يُطبَع_يدويًّا` "
    "ولا يحسم فحصًا حتى يصير `مُودَعًا_مُبصَّمًا`"
)

AN_EMPTY_CATEGORY_HAS_NO_RATE_NOTE: Final[str] = (
    "AnEmptyCategoryHasNoRate: الفئةُ الخاليةُ تبقى صفًّا بصفرٍ ونسبتُها ممتنعة، "
    "ولا تُحذَف ولا تُكتَب مئةً بالمئة؛ وعددُ الفئات الخالية قياسٌ على أنّ "
    "المطلوب توسيعُ المدوّنة لا رفعُ نسبةٍ بلغت تمامها"
)
