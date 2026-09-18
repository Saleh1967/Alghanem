"""قلبُ `G0.LEX-0`: عقدُ الوقوع السطحيّ، وسلَّمُ المُرشَّحات، ومرساةُ الدلالة.

**هذا القلبُ لا يقرأ مدوَّنة**: `SurfaceOccurrence` عقدٌ عامٌّ لا يعرف قرآنًا
ولا MASAQ ولا أيَّ ملفّ؛ والمحوّلاتُ عملاءُ الطبقة لا أجزاؤها، والاتّجاه
`adapter → core` ولا عكس. وبذلك يدخل نصٌّ عربيٌّ مستقلٌّ لاحقًا بلا إعادةِ بناء.

**وفصلُ الصرف شرطٌ لا ترتيبُ حقول**: `DerivedMorphologicalCandidate` ينتجه
النظامُ من الوقوع وحدَه، و`ReportedMorphologicalEvidence` يأتي من مصدرٍ خارجيٍّ
شاهدًا **محجوبًا عن التوليد**؛ ولا يحلُّ أحدُهما محلَّ الآخر، ولا يُرجَّح أحدُهما
على الآخر في `MorphologicalAgreementRecord`. وذلك امتدادُ
`FrozenExpectationIsNotGenerativeInput` إلى الصرف، وحالةٌ خاصّةٌ من
`NecessaryRelationIsNotGenerativeAuthority`.

**واسمُ أثر التطبيع مُقيَّدٌ عمدًا** (`LexicalNormalizationTrace`): في الشجرة
`NormalizationTrace` مرّتين بمعنيين مختلفين (`arabic/encoding/normalization.py`
و`masaq_fractal_experiment.py`)، فاسمٌ ثالثٌ مطابقٌ لهما يجعل المستورِدَ يقرأ
غيرَ ما استورد. والدورُ هو الدورُ نفسُه في سقف النواة.

**والمرساةُ واحدةٌ والإسقاطاتُ ثلاثة**: `PrimarySignificationAnchor(L, M, E)`
تُبنى هنا، وتُقرأ في المحاور الثلاثة إسقاطًا مستقلًّا لا اشتقاقًا متسلسلًا.

تسجيلٌ لا سلطة: لا معنًى نهائيّ، ولا إفادة، ولا حكم، ولا `E0`، ولا استيراد من
`kernel/`.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Final

from .lexical_evidence_specification import (
    A_MATCH_IS_NOT_A_MEANING_NOTE,
    AMBIGUITY_IS_RECORDED_NOT_RESOLVED_NOTE,
    EXACT_FORM_IS_PRESERVED_UNDER_EVERY_NORMALIZED_BRANCH_NOTE,
    NORMALIZATION_BRANCH_RULE_NAMES,
    NOT_COMPARABLE_IS_NOT_FAILURE_NOTE,
    REPORTED_MORPHOLOGY_IS_NOT_DERIVED_MORPHOLOGY_NOTE,
    NormalizationBranch,
)

__all__ = [
    "LEXICAL_TRACE_NAME_IS_QUALIFIED_NOTE",
    "LexicalAmbiguityRecord",
    "DerivedMorphologicalCandidate",
    "LexicalComparativeStanding",
    "LexicalEvidenceCandidate",
    "LexicalEvidenceLayerError",
    "LexicalMatchCandidate",
    "LexicalNormalizationTrace",
    "LexicalTaskOutcome",
    "MorphologicalAgreement",
    "MorphologicalAgreementRecord",
    "PrimarySignificationAnchor",
    "ReportedMorphologicalEvidence",
    "SignifierCandidate",
    "SurfaceOccurrence",
    "derive_comparative_standing",
    "derive_task_outcome",
    "refuse_reported_morphology_as_generative_input",
]


class LexicalEvidenceLayerError(ValueError):
    """رفضٌ صريحٌ في قلب الطبقة؛ ولا يُحمَل المدخلُ على أقرب حالةٍ مقبولة."""


LEXICAL_TRACE_NAME_IS_QUALIFIED_NOTE: Final[str] = (
    "LexicalTraceNameIsQualifiedNotDuplicated: اسمُ `NormalizationTrace` مأخوذٌ "
    "في هذه الشجرة بمعنيين مختلفين، فاسمُ أثر هذه الطبقة مُقيَّدٌ لئلّا يقرأ "
    "المستورِدُ غيرَ ما استورد؛ والدورُ هو الدورُ نفسُه"
)


def _require_text(value: str, label: str) -> None:
    if not isinstance(value, str) or not value.strip():
        raise LexicalEvidenceLayerError(f"{label} نصٌّ غير فارغ.")


@dataclass(frozen=True, slots=True)
class LexicalNormalizationTrace:
    """أثرُ تطبيعٍ واحد: الفرعُ، واسمُ قاعدته، والصورتان معًا، وما أتلفته.

    ولا تخرج صورةٌ مُطبَّعةٌ مفردةً: الخامُّ محفوظٌ في الأثر نفسه تحت
    `ExactFormIsPreservedUnderEveryNormalizedBranch`.
    """

    branch: NormalizationBranch
    raw_form: str
    normalized_form: str
    what_it_destroys: str
    fusions: tuple[tuple[str, str], ...] = ()

    def __post_init__(self) -> None:
        if not isinstance(self.branch, NormalizationBranch):
            raise LexicalEvidenceLayerError("فرعُ التطبيع عضوٌ في مفردته الثلاثية.")
        _require_text(self.raw_form, "الصورةُ الخام")
        _require_text(self.normalized_form, "الصورةُ المُطبَّعة")
        if self.branch is NormalizationBranch.EXACT:
            if self.normalized_form != self.raw_form:
                raise LexicalEvidenceLayerError(
                    "فرعُ `EXACT` لا يُعمِل قاعدةً، فصورتاه واحدة."
                )
            if self.fusions:
                raise LexicalEvidenceLayerError("فرعُ `EXACT` لا ينصهر تحته شيء.")
        else:
            _require_text(self.what_it_destroys, "ما تُتلفه القاعدة")
        for pair in self.fusions:
            if len(pair) != 2 or not all(str(item).strip() for item in pair):
                raise LexicalEvidenceLayerError(
                    "الانصهارُ زوجٌ من صورتين متمايزتين بأعيانهما."
                )

    @property
    def rule_name(self) -> str | None:
        """اسمُ القاعدة المُعمَلة، أو لا شيءَ في الفرع الصريح."""

        return NORMALIZATION_BRANCH_RULE_NAMES[self.branch]

    @property
    def preserves_exact_form(self) -> bool:
        """أمحفوظةٌ الصورةُ الخام؟ مُشتَقٌّ من الأثر لا حقلٌ يُكتَب."""

        return bool(self.raw_form)


@dataclass(frozen=True, slots=True)
class SurfaceOccurrence:
    """عقدٌ عامّ: وقوعٌ سطحيٌّ بصورته الخام وموضعه في مصدرٍ مُصرَّح.

    ولا حقلَ هنا لمدوَّنةٍ بعينها: `source_id` مُعرِّفُ مصدرٍ يُصرِّح به
    المحوّل، و`source_position` موضعُه كما ورد في المصدر، و`local_position`
    موضعٌ مشتقٌّ في التسلسل المقروء — واثنان لأنّ `SourceWordNo` ليس
    `DerivedLocalPosition`.
    """

    source_id: str
    occurrence_id: str
    raw_form: str
    source_position: str
    local_position: int

    def __post_init__(self) -> None:
        _require_text(self.source_id, "مُعرِّفُ المصدر")
        _require_text(self.occurrence_id, "مُعرِّفُ الوقوع")
        _require_text(self.raw_form, "الصورةُ الخام")
        _require_text(self.source_position, "الموضعُ في المصدر")
        if not isinstance(self.local_position, int) or self.local_position < 0:
            raise LexicalEvidenceLayerError("الموضعُ المحلّيُّ عددٌ غيرُ سالب.")

    @property
    def reference(self) -> str:
        """مرجعُ الوقوع الذي تشير إليه المُرشَّحات؛ مُشتَقٌّ لا مكتوب."""

        return f"{self.source_id}#{self.occurrence_id}"


@dataclass(frozen=True, slots=True)
class SignifierCandidate:
    """الدالُّ مُرشَّحًا: وقوعُه، وأثرُ تطبيعه في فرعٍ مُسمًّى.

    والصورةُ الخامُّ تُقرأ من الوقوع لا تُكتَب ثانيةً، فالكتابةُ تسمح بصورةٍ
    تخالف وقوعَها ولا يردُّها شيء.
    """

    occurrence: SurfaceOccurrence
    trace: LexicalNormalizationTrace

    def __post_init__(self) -> None:
        if not isinstance(self.occurrence, SurfaceOccurrence):
            raise LexicalEvidenceLayerError("الدالُّ يقوم على وقوعٍ سطحيّ.")
        if not isinstance(self.trace, LexicalNormalizationTrace):
            raise LexicalEvidenceLayerError("الدالُّ يحمل أثرَ تطبيعه.")
        if self.trace.raw_form != self.occurrence.raw_form:
            raise LexicalEvidenceLayerError(
                "أثرُ التطبيع يبدأ من صورة الوقوع الخام نفسِها؛ "
                + EXACT_FORM_IS_PRESERVED_UNDER_EVERY_NORMALIZED_BRANCH_NOTE
            )

    @property
    def exact_form(self) -> str:
        return self.occurrence.raw_form

    @property
    def normalized_form(self) -> str:
        return self.trace.normalized_form


@dataclass(frozen=True, slots=True)
class DerivedMorphologicalCandidate:
    """صورةٌ صرفيّةٌ **ينتجها النظام** من الدالّ وحده، بأساسِ اشتقاقها مُصرَّحًا."""

    signifier: SignifierCandidate
    proposed_root: str
    derivation_basis: str

    def __post_init__(self) -> None:
        if not isinstance(self.signifier, SignifierCandidate):
            raise LexicalEvidenceLayerError("المُرشَّحُ الصرفيُّ يقوم على دالٍّ مُرشَّح.")
        _require_text(self.proposed_root, "الجذرُ المُقترَح")
        _require_text(self.derivation_basis, "أساسُ الاشتقاق")


@dataclass(frozen=True, slots=True)
class ReportedMorphologicalEvidence:
    """صورةٌ صرفيّةٌ **مُبلَّغٌ عنها** في مصدرٍ خارجيّ؛ شاهدٌ محجوبٌ عن التوليد.

    `is_generative_input` ثابتةٌ على `False` لا حقلًا يُضبَط، لأنّ حجبَها شرطٌ
    في هويّتها لا خيارًا للمُنشئ.
    """

    reporting_source: str
    reported_root: str
    source_trace: str

    def __post_init__(self) -> None:
        _require_text(self.reporting_source, "المصدرُ المُبلِّغ")
        _require_text(self.reported_root, "الجذرُ المُبلَّغ عنه")
        _require_text(self.source_trace, "أثرُ المصدر")

    @property
    def is_generative_input(self) -> bool:
        return False


def refuse_reported_morphology_as_generative_input(
    evidence: ReportedMorphologicalEvidence,
) -> None:
    """ارفض تمريرَ الشاهد المُبلَّغ عنه إلى مولِّد؛ رفضًا يُرفَع لا تنبيهًا يُكتَب."""

    if not isinstance(evidence, ReportedMorphologicalEvidence):
        raise LexicalEvidenceLayerError("الشاهدُ المُبلَّغ عنه من بنيته وحدها.")
    raise LexicalEvidenceLayerError(REPORTED_MORPHOLOGY_IS_NOT_DERIVED_MORPHOLOGY_NOTE)


class MorphologicalAgreement(Enum):
    """موقعُ المُشتَقِّ من المُبلَّغ عنه؛ خماسيّةٌ مغلقةٌ بلا عضوٍ يُرجِّح."""

    AGREE = "AGREE"
    DISAGREE = "DISAGREE"
    ONLY_DERIVED = "ONLY_DERIVED"
    ONLY_REPORTED = "ONLY_REPORTED"
    NEITHER = "NEITHER"


@dataclass(frozen=True, slots=True)
class MorphologicalAgreementRecord:
    """أثرُ تدقيقٍ لا ناتجَ نواة: يقارن الطرفين ولا يُرجِّح أحدَهما.

    ولا حقلَ فيه للموقع: يُشتَقّ من الطرفين، فكتابتُه تسمح بموقعٍ يخالفهما.
    """

    derived: DerivedMorphologicalCandidate | None
    reported: ReportedMorphologicalEvidence | None

    def __post_init__(self) -> None:
        if self.derived is not None and not isinstance(
            self.derived, DerivedMorphologicalCandidate
        ):
            raise LexicalEvidenceLayerError("الطرفُ المُشتَقُّ من بنيته أو لا شيء.")
        if self.reported is not None and not isinstance(
            self.reported, ReportedMorphologicalEvidence
        ):
            raise LexicalEvidenceLayerError("الطرفُ المُبلَّغُ من بنيته أو لا شيء.")

    @property
    def agreement(self) -> MorphologicalAgreement:
        if self.derived is None and self.reported is None:
            return MorphologicalAgreement.NEITHER
        if self.reported is None:
            return MorphologicalAgreement.ONLY_DERIVED
        if self.derived is None:
            return MorphologicalAgreement.ONLY_REPORTED
        if self.derived.proposed_root == self.reported.reported_root:
            return MorphologicalAgreement.AGREE
        return MorphologicalAgreement.DISAGREE


@dataclass(frozen=True, slots=True)
class LexicalMatchCandidate:
    """مطابقةُ مدخلٍ معجميٍّ تحت فرعِ تطبيعٍ مُسمًّى، بلا دمجٍ بين الفروع."""

    signifier: SignifierCandidate
    lexicon_id: str
    matched_entry_ref: str
    indexing_unit: str

    def __post_init__(self) -> None:
        if not isinstance(self.signifier, SignifierCandidate):
            raise LexicalEvidenceLayerError("المطابقةُ تقوم على دالٍّ مُرشَّح.")
        _require_text(self.lexicon_id, "مُعرِّفُ المعجم")
        _require_text(self.matched_entry_ref, "مرجعُ المدخل المُطابَق")
        _require_text(self.indexing_unit, "وحدةُ الفهرسة")

    @property
    def branch(self) -> NormalizationBranch:
        return self.signifier.trace.branch

    @property
    def normalization_rule_ref(self) -> str | None:
        return self.signifier.trace.rule_name

    @property
    def exact_form(self) -> str:
        """الصورةُ الخامُّ محفوظةٌ تحت كلّ فرع، لا في الفرع الصريح وحده."""

        return self.signifier.exact_form


@dataclass(frozen=True, slots=True)
class LexicalEvidenceCandidate:
    """أقصى ما تبلغه هذه المرحلة: شاهدٌ معجميٌّ منقولٌ بموضعه، لا مدلولٌ مُثبَت.

    والحقولُ المنقولةُ تُسمّى بلاحقة `_as_reported` في بُناها الخاصّة بالمصدر،
    لأنّ النقلَ جزءٌ من اسم الحقل لا تعليقٌ عليه؛ وهنا يُحفَظ مرجعُ المنقول
    وأثرُه فقط تحت `QuotedDefinitionIsNotDerivedSignified`.
    """

    match: LexicalMatchCandidate
    evidence_ref: str
    source_trace: str

    def __post_init__(self) -> None:
        if not isinstance(self.match, LexicalMatchCandidate):
            raise LexicalEvidenceLayerError("الشاهدُ المعجميُّ يقوم على مطابقة.")
        _require_text(self.evidence_ref, "مرجعُ الشاهد")
        _require_text(self.source_trace, "أثرُ المصدر")

    @property
    def is_a_meaning(self) -> bool:
        """شاهدٌ لا معنًى؛ الجوابُ ثابتٌ ومعه نصُّ رفضه."""

        return False

    @property
    def refusal_note(self) -> str:
        return A_MATCH_IS_NOT_A_MEANING_NOTE


@dataclass(frozen=True, slots=True)
class PrimarySignificationAnchor:
    """مرساةُ الدلالة الأصليّة المُرخَّصة: لفظٌ، ومدلولٌ، ودليلٌ، ومرجعُ ترخيص.

    وعليها تقوم الإسقاطاتُ الثلاثة؛ ولا يُفتح فرعٌ من فروع الدلالة قبلها، لأنّ
    الجزئيّةَ واللزومَ شرطان لا موجِبان.
    """

    signifier: SignifierCandidate
    signified_ref: str
    license_ref: str
    evidence_refs: tuple[str, ...]

    def __post_init__(self) -> None:
        if not isinstance(self.signifier, SignifierCandidate):
            raise LexicalEvidenceLayerError("المرساةُ تقوم على دالٍّ مُرشَّح.")
        _require_text(self.signified_ref, "مرجعُ المدلول")
        _require_text(self.license_ref, "مرجعُ الترخيص")
        if not self.evidence_refs:
            raise LexicalEvidenceLayerError("مرساةٌ بلا دليلٍ واحد لا تُرسي شيئًا.")
        for reference in self.evidence_refs:
            _require_text(reference, "مرجعُ الدليل")

    @property
    def reference(self) -> str:
        return f"{self.signifier.occurrence.reference}→{self.signified_ref}"


@dataclass(frozen=True, slots=True)
class LexicalAmbiguityRecord:
    """تعدُّدُ المُرشَّحات مُسجَّلًا بأعيانه؛ ولا حقلَ فيه للحسم."""

    occurrence_ref: str
    candidate_refs: tuple[str, ...]

    def __post_init__(self) -> None:
        _require_text(self.occurrence_ref, "مرجعُ الوقوع")
        if len(self.candidate_refs) < 2:
            raise LexicalEvidenceLayerError("سجلُّ التعدُّد يقتضي مُرشَّحَين فأكثر بأعيانهما.")
        for reference in self.candidate_refs:
            _require_text(reference, "مرجعُ المُرشَّح")

    @property
    def resolution_note(self) -> str:
        return AMBIGUITY_IS_RECORDED_NOT_RESOLVED_NOTE


class LexicalTaskOutcome(Enum):
    """حالُ المهمّة للكلمة الواحدة؛ مستقلٌّ عن موقع المقارنة."""

    MATCHED = "MATCHED"
    UNMATCHED = "UNMATCHED"
    UNRESOLVED = "UNRESOLVED"


class LexicalComparativeStanding(Enum):
    """موقعُ المقارنة؛ و`NOT_COMPARABLE` ليس فشلًا ولا دعمًا."""

    BOTH_SUCCEED = "BOTH_SUCCEED"
    LEXICAL_ONLY = "LEXICAL_ONLY"
    WEAKER_ONLY = "WEAKER_ONLY"
    BOTH_FAIL = "BOTH_FAIL"
    NOT_COMPARABLE = "NOT_COMPARABLE"

    @property
    def refusal_note(self) -> str:
        """نصُّ `NotComparableIsNotFailure`؛ مقروءٌ من التخصيص لا مُعادُ تهجئته."""

        return NOT_COMPARABLE_IS_NOT_FAILURE_NOTE


def derive_task_outcome(
    *, reached_evidence: bool, anchor_resolved: bool
) -> LexicalTaskOutcome:
    """اشتقّ حالَ المهمّة؛ ولا يُكتَب حقلًا يخالف شرطيه."""

    if not anchor_resolved:
        return LexicalTaskOutcome.UNRESOLVED
    return (
        LexicalTaskOutcome.MATCHED if reached_evidence else LexicalTaskOutcome.UNMATCHED
    )


def derive_comparative_standing(
    *,
    lexicon_indexing_unit: str,
    comparator_indexing_unit: str | None,
    lexical_reached: bool,
    comparator_reached: bool,
) -> LexicalComparativeStanding:
    """اشتقّ موقعَ المقارنة، وامتنع عنها حين تختلف وحدةُ الفهرسة.

    مقارنةُ معجمٍ مفهرسٍ بالجذر بمُقارِنٍ سطحيٍّ مقارنةٌ بين جنسين، فتُرَدّ
    `NOT_COMPARABLE` ولا تُقلَب فشلًا (`NotComparableIsNotFailure`).
    """

    _require_text(lexicon_indexing_unit, "وحدةُ فهرسة المعجم")
    if comparator_indexing_unit is None:
        return LexicalComparativeStanding.NOT_COMPARABLE
    _require_text(comparator_indexing_unit, "وحدةُ فهرسة المُقارِن")
    if comparator_indexing_unit != lexicon_indexing_unit:
        return LexicalComparativeStanding.NOT_COMPARABLE
    if lexical_reached and comparator_reached:
        return LexicalComparativeStanding.BOTH_SUCCEED
    if lexical_reached:
        return LexicalComparativeStanding.LEXICAL_ONLY
    if comparator_reached:
        return LexicalComparativeStanding.WEAKER_ONLY
    return LexicalComparativeStanding.BOTH_FAIL
