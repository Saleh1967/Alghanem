"""`G0.CASE-0.DATA`: قضايا مكتوبةٌ وتوقُّعاتٌ مجمَّدةٌ قبل أن يُشغَّل المحرّك مرّة.

    MATRIX  ≺  DATA  ≺  READOUT  ≺  DIGEST LEDGER

**والحالةُ تُكتَب ولا تُولَّد** (`ACaseIsAuthoredNotGenerated`): مادّةُ الحالات
ملفّاتُ `JSON` مكتوبةٌ مراجَعةٌ في `case_data/`، لا ناتجُ دوالَّ بايثون. ولو
بَنَت الشِّفرةُ حالاتِها لشارك البرنامجُ الذي سيُقرأ به الدليلُ في تكوين الدليل.
فهذه الوحدةُ **أنواعُ المواصفة وفاحصُ اتّساقها** لا غير: لا تُنشئ وثيقةً، ولا
تفتح ملفًّا، ولا تستورد المحرّك، ولا يستوردها هو. وقراءةُ الملفّات من مجلَّد
`case_data/` شأنُ طبقةِ الاختبار وحدَها، فلا يدخل مسارُ ملفٍّ في هذه المواصفة.

**والتوقُّعُ لا يحمل بصمةَ تنفيذ** (`AnExpectationCarriesNoExecutionDigest`):
`execution_digest` مولودُ القراءة؛ فإدخالُه في `DATA` — ولو فارغًا — خلطٌ
لمرحلتين. تقول `DATA` قبل التشغيل: هذه القضيّةُ وهذا المتوقَّعُ منها؛ ثمّ تُشغِّل
`READOUT` المحرّكَ أوّلَ مرّةٍ فتقارن؛ فإن طابقت القراءةُ التوقُّعَ المجمَّدَ قُيِّدت
البصمةُ في سجلٍّ مستقلٍّ لا يرجع إلى `DATA`، وصارت من القراءة الثانية شاهدَ
انحراف.

**والحالةُ المضادّة أصلٌ صحيحٌ وفرقٌ واحدٌ مُعلَن**
(`AGoldenCounterCaseIsOneDeclaredDifference`):

    GoldenCounterCase  =  ValidBaseline  +  OneDeclaredDifference

فالحالةُ الذهبيّةُ تجيب عن سؤالٍ واحدٍ بأقلّ تركيب. ولا تُجمَع أعطالٌ في وثيقةٍ
واحدةٍ إلّا أن يكون تعدُّدُ المواضيع نفسُه محلَّ البرهان — كإثبات أنّ قانونًا
واحدًا يصحّ أن يثبت على موضوعٍ ويُخالَف على آخر — فيُصرَّح بذلك بالاسم.

**والاستشهادُ دعوى تغطيةٍ لا تغطية** (`ACitationIsAClaimUntilTheReadout`):

    Citation_DATA  ←READOUT→  TraceEntry_actual

فاحصُ `DATA` يثبت أنّ الاستشهاد مشروعٌ ومتّسقٌ مع المصفوفة ومع توقُّع الحالة
نفسِها؛ ولا يثبت أنّ الحالةَ بلغت الخليّةَ التي ادّعتها. ذلك شأنُ `READOUT`
وحدَه، وبه تُمنَع التغطيةُ الورقيّة.

**وعطبُ المحرّك ليس قضيّةَ مستخدم** (`AnInvariantErrorIsNotInTheUserCaseSpace`):

    INVARIANT_ERROR  ∉  UserCaseSpace

فلا يُسمّى `GoldenCase` ولا يُكتَب له `JSON`؛ إنّما هو `EngineSeamWitness` على
حدٍّ داخليٍّ يُبلَغ بمادّةٍ مُشتَقّةٍ ناقصةٍ بعد نجاحٍ مبدئيّ. وكذلك فسادُ الإدخال
هويّةٌ منفصلةٌ: `InvalidInputWitness ≠ GoldenExecutionCase`، لا أثرَ له ولا غلافَ
ولا حكم.

تسجيلٌ لا سلطة: لا ولادةَ ولا حكمَ ولادةٍ ولا تجميدَ `E0`.
"""

from __future__ import annotations

from dataclasses import dataclass, fields
from typing import Any, Final

from .coverage import (
    COVERAGE_MATRIX,
    COVERAGE_MATRIX_DIGEST,
    EVALUATION_SCOPE_OF_LAW,
    CaseDisposition,
    CoverageAxis,
    CoverageRequirement,
    EvaluationScope,
)
from .declaration import CaseDeclaration
from .lawset import LAW_SET_DIGEST, ExecutionLaw
from .outcome import CheckStanding

__all__ = [
    "A_CASE_IS_AUTHORED_NOT_GENERATED",
    "A_CITATION_IS_A_CLAIM_UNTIL_THE_READOUT",
    "A_GOLDEN_COUNTER_CASE_IS_ONE_DECLARED_DIFFERENCE",
    "AN_EXPECTATION_CARRIES_NO_EXECUTION_DIGEST",
    "AN_INVARIANT_ERROR_IS_NOT_IN_THE_USER_CASE_SPACE",
    "CASE_DATA_ID",
    "CORPUS_ROOT_NAME",
    "REFUSED_EXPECTATION_KEYS",
    "VERDICT_DISPOSITIONS",
    "DECLARATION_DOCUMENT_KEYS",
    "CaseDataError",
    "CorpusCoverage",
    "CoverageCitation",
    "DeclaredDifference",
    "EngineSeamWitness",
    "ExpectedTraceRow",
    "GoldenCaseCorpus",
    "GoldenExecutionCase",
    "GoldenExpectation",
    "InvalidInputWitness",
]


CASE_DATA_ID: Final[str] = "alghanem.execution.case_data.G0.CASE-0.DATA"

CORPUS_ROOT_NAME: Final[str] = "case_data"

DECLARATION_DOCUMENT_KEYS: Final[frozenset[str]] = frozenset(
    field.name for field in fields(CaseDeclaration)
)
"""مفاتيحُ وثيقةِ الحالة؛ صورةُ `JSON` هي صورةُ التصريح نفسِها لا صورةٌ أخرى."""

A_CASE_IS_AUTHORED_NOT_GENERATED: Final[str] = (
    "الحالةُ تُكتَب ولا تُولَّد: مادّةُ الحالات ملفّاتُ `JSON` مكتوبةٌ مراجَعة، ولو "
    "بَنَتها الشِّفرةُ لشارك البرنامجُ في تكوين الدليل الذي يُحاسَب به"
)

AN_EXPECTATION_CARRIES_NO_EXECUTION_DIGEST: Final[str] = (
    "التوقُّعُ لا يحمل بصمةَ تنفيذ: البصمةُ مولودةُ القراءة، وإدخالُها في التوقُّع "
    "ولو فارغةً خلطُ مرحلتين؛ وسجلُّ البصمات بعد القراءة الأولى ولا يرجع إلى الحالة"
)

A_GOLDEN_COUNTER_CASE_IS_ONE_DECLARED_DIFFERENCE: Final[str] = (
    "الحالةُ المضادّة أصلٌ صحيحٌ وفرقٌ واحدٌ مُعلَن: حالةٌ ذهبيّةٌ تجيب عن سؤالٍ "
    "واحدٍ بأقلّ تركيب؛ ولا تُجمَع أعطالٌ إلّا أن يكون تعدُّدُ المواضيع محلَّ البرهان"
)

A_CITATION_IS_A_CLAIM_UNTIL_THE_READOUT: Final[str] = (
    "الاستشهادُ دعوى تغطيةٍ لا تغطية: فاحصُ البيانات يثبت مشروعيّتَه واتّساقَه مع "
    "المصفوفة ومع توقُّع حالته، والقراءةُ وحدَها تثبت بلوغَ الخليّة المُدَّعاة"
)

AN_INVARIANT_ERROR_IS_NOT_IN_THE_USER_CASE_SPACE: Final[str] = (
    "عطبُ المحرّك ليس قضيّةَ مستخدم: شاهدُ الحدّ الداخليّ لا وثيقةَ له تُكتَب، "
    "ولا يُسمّى حالةً ذهبيّةً؛ ومن أعطاه وثيقةً جعل العطبَ الداخليَّ مطلبًا يُطلَب"
)

VERDICT_DISPOSITIONS: Final[tuple[CaseDisposition, ...]] = (
    CaseDisposition.PASS,
    CaseDisposition.BLOCK,
    CaseDisposition.DEFER,
)
"""ما تنتهي إليه قضيّةٌ قائمةُ الإدخال؛ وفسادُ الإدخال والعطبُ شاهدان لا حالتان."""

REFUSED_EXPECTATION_KEYS: Final[frozenset[str]] = frozenset(
    {
        "execution_digest",
        "expected_execution_digest",
        "readout_digest",
        "observed_trace",
        "observed_disposition",
    }
)
"""مفاتيحُ تُردّ في التوقُّع: مولودةُ القراءة لا تُكتَب قبلها ولو فارغة."""


class CaseDataError(ValueError):
    """رفضٌ عند قراءة حالةٍ أو توقُّعٍ أو شاهد؛ لا حملَ على أقرب صورةٍ مقبولة."""


def _refuse_a_whole_case_citation_that_disagrees(
    citation: CoverageCitation, requirement: CoverageRequirement
) -> None:
    """مطلبُ القضيّة كلِّها لا يُسمّي قانونًا في منزلة، ويُسمّي موضوعَه إن كان نطاقُه موضوعًا."""

    if citation.law is not None or citation.standing is not None:
        raise CaseDataError("استشهادٌ بمطلبٍ عن القضيّة كلِّها لا يُسمّي قانونًا في منزلة")
    subject_scoped = requirement.evaluation_scope is EvaluationScope.SUBJECT
    if subject_scoped and citation.witness_subject_id is None:
        raise CaseDataError(
            f"مطلبٌ نطاقُه موضوعٌ يُسمّي شاهدَه بموضوعه: «{requirement.requirement_id}»"
        )
    if not subject_scoped and citation.witness_subject_id is not None:
        raise CaseDataError("مطلبُ القضيّة كلِّها تحمله القضيّةُ لا موضوعٌ فيها")


def _refuse_witness_citations(
    citations: tuple[CoverageCitation, ...], disposition: CaseDisposition
) -> None:
    """شاهدٌ لا يستشهد إلّا بمطلبٍ يقيّد منزلتَه هو؛ ولا يدّعي خليّةَ قانونٍ في قضيّة."""

    seen: set[str] = set()
    for citation in citations:
        if citation.requirement_id in seen:
            raise CaseDataError(
                f"استشهادٌ مكرَّرٌ بمطلبٍ واحدٍ في شاهدٍ واحد: «{citation.requirement_id}»"
            )
        seen.add(citation.requirement_id)
        requirement = citation.requirement()
        if not requirement.required or not requirement.reachable:
            raise CaseDataError(
                "لا شاهدَ لخليّةٍ ممتنعةٍ ولا لمطلبٍ غيرِ واجب؛ والممتنعُ يُعلَّل "
                "ولا يُصطنَع له شاهد"
            )
        if requirement.axis is CoverageAxis.LAW_STANDING:
            raise CaseDataError(
                "خليّةُ قانونٍ في منزلةٍ تُبلَغ بقضيّةٍ قامت لا بشاهدٍ على ما دونها"
            )
        if requirement.expected_disposition is not disposition:
            raise CaseDataError(
                f"شاهدٌ يستشهد بمطلبٍ يقيّد منزلةً غيرَ منزلته: "
                f"«{citation.requirement_id}»"
            )
        _refuse_a_whole_case_citation_that_disagrees(citation, requirement)


def _text(value: object, label: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise CaseDataError(f"{label} نصٌّ غير فارغ")
    return value


def _optional_text(value: object, label: str) -> str | None:
    if value is None:
        return None
    return _text(value, label)


def _mapping(value: object, label: str) -> dict[str, Any]:
    if not isinstance(value, dict):
        raise CaseDataError(f"{label} كائنٌ مُصرَّحٌ به")
    return value


def _sequence(value: object, label: str) -> list[Any]:
    if not isinstance(value, list):
        raise CaseDataError(f"{label} قائمةٌ مرتَّبةٌ مُصرَّحٌ بها")
    return value


def _exact_keys(document: dict[str, Any], expected: frozenset[str], label: str) -> None:
    unknown = sorted(set(document) - expected)
    missing = sorted(expected - set(document))
    if unknown:
        raise CaseDataError(f"{label} فيه مفتاحٌ غيرُ مُصرَّحٍ به: {unknown[0]}")
    if missing:
        raise CaseDataError(f"{label} ينقصه مفتاحٌ مطلوب: {missing[0]}")


def _refuse_readout_keys(value: object, label: str) -> None:
    """ردَّ كلَّ مفتاحٍ مولودٍ من القراءة أينما وقع في شجرة التوقُّع."""

    if isinstance(value, dict):
        for key, nested in value.items():
            if key in REFUSED_EXPECTATION_KEYS:
                raise CaseDataError(
                    f"{label} يحمل «{key}»؛ و"
                    + AN_EXPECTATION_CARRIES_NO_EXECUTION_DIGEST
                )
            _refuse_readout_keys(nested, label)
    elif isinstance(value, list):
        for nested in value:
            _refuse_readout_keys(nested, label)


@dataclass(frozen=True, slots=True)
class DeclaredDifference:
    """فرقٌ واحدٌ مُعلَنٌ عن الأصل: موضعُه في الوثيقة، وما صار إليه المعنى."""

    path: str
    statement: str

    def __post_init__(self) -> None:
        _text(self.path, "موضعُ الفرق")
        _text(self.statement, "بيانُ الفرق")

    @classmethod
    def of(cls, document: dict[str, Any]) -> DeclaredDifference:
        _exact_keys(document, frozenset({"path", "statement"}), "الفرقُ المُعلَن")
        return cls(path=document["path"], statement=document["statement"])


@dataclass(frozen=True, slots=True)
class ExpectedTraceRow:
    """سطرُ أثرٍ متوقَّع، مكتوبٌ قبل التشغيل: قانونٌ وموضوعٌ ومنزلةٌ وحاجب."""

    law: ExecutionLaw
    subject_id: str | None
    standing: CheckStanding
    blocked_by: ExecutionLaw | None

    def __post_init__(self) -> None:
        if not isinstance(self.law, ExecutionLaw):
            raise CaseDataError("قانونُ السطر عضوٌ في مفردته المغلقة")
        if not isinstance(self.standing, CheckStanding):
            raise CaseDataError("منزلةُ السطر عضوٌ في مفردتها المغلقة")
        if self.subject_id is not None:
            _text(self.subject_id, "موضوعُ السطر")
        blocked = self.standing is CheckStanding.NOT_EVALUATED_BY_PREREQUISITE
        if blocked != (self.blocked_by is not None):
            raise CaseDataError(
                "المحجوبُ يُسمّي حاجبَه وغيرُ المحجوب لا حاجبَ له؛ والسطرُ يُكتَب "
                "كما يُقرَأ لا كما يُشتهى"
            )

    @classmethod
    def of(cls, document: dict[str, Any]) -> ExpectedTraceRow:
        _exact_keys(
            document,
            frozenset({"law", "subject_id", "standing", "blocked_by"}),
            "سطرُ الأثر المتوقَّع",
        )
        blocker = _optional_text(document["blocked_by"], "حاجبُ السطر")
        return cls(
            law=_member(ExecutionLaw, document["law"], "قانونُ السطر"),
            subject_id=_optional_text(document["subject_id"], "موضوعُ السطر"),
            standing=_member(CheckStanding, document["standing"], "منزلةُ السطر"),
            blocked_by=(
                None if blocker is None else _member(ExecutionLaw, blocker, "الحاجب")
            ),
        )


def _member(vocabulary: Any, value: object, label: str) -> Any:
    try:
        return vocabulary(_text(value, label))
    except ValueError as refusal:
        raise CaseDataError(f"{label} خارجُ مفردته المغلقة: {value!r}") from refusal


@dataclass(frozen=True, slots=True)
class CoverageCitation:
    """دعوى تغطيةٍ لخليّةٍ في المصفوفة، بشاهدها الثلاثيّ لا باسم قانونها."""

    requirement_id: str
    law: ExecutionLaw | None
    witness_subject_id: str | None
    standing: CheckStanding | None

    def __post_init__(self) -> None:
        _text(self.requirement_id, "مُعرِّفُ المطلب المُستشهَد به")
        if self.witness_subject_id is not None:
            _text(self.witness_subject_id, "موضوعُ الشاهد")

    @classmethod
    def of(cls, document: dict[str, Any]) -> CoverageCitation:
        _exact_keys(
            document,
            frozenset({"requirement_id", "law", "witness_subject_id", "standing"}),
            "الاستشهادُ بالمصفوفة",
        )
        law = _optional_text(document["law"], "قانونُ الاستشهاد")
        standing = _optional_text(document["standing"], "منزلةُ الاستشهاد")
        return cls(
            requirement_id=document["requirement_id"],
            law=None if law is None else _member(ExecutionLaw, law, "قانونُ الاستشهاد"),
            witness_subject_id=_optional_text(
                document["witness_subject_id"], "موضوعُ الشاهد"
            ),
            standing=(
                None
                if standing is None
                else _member(CheckStanding, standing, "منزلةُ الاستشهاد")
            ),
        )

    def requirement(self) -> CoverageRequirement:
        """خليّةُ المصفوفة المُستشهَد بها؛ والغيابُ ردٌّ لا تأويل."""

        for item in COVERAGE_MATRIX.requirements:
            if item.requirement_id == self.requirement_id:
                return item
        raise CaseDataError(f"الاستشهادُ بمطلبٍ ليس في المصفوفة: «{self.requirement_id}»")


@dataclass(frozen=True, slots=True)
class GoldenExecutionCase:
    """قضيّةٌ ذهبيّةٌ قائمةُ الإدخال: وثيقتُها وحدَها، ولا حكمَ فيها ولا توقُّع."""

    case_id: str
    document: dict[str, Any]
    baseline_case_id: str | None
    declared_differences: tuple[DeclaredDifference, ...]
    multiplicity_is_the_proof: str | None

    def __post_init__(self) -> None:
        _text(self.case_id, "مُعرِّفُ الحالة")
        _exact_keys(
            _mapping(self.document, "وثيقةُ الحالة"),
            DECLARATION_DOCUMENT_KEYS,
            "وثيقةُ الحالة",
        )
        if self.baseline_case_id is not None:
            _text(self.baseline_case_id, "أصلُ الحالة")
        if self.baseline_case_id is None:
            if self.declared_differences:
                raise CaseDataError("حالةُ الأصل لا فرقَ لها؛ والفرقُ يُقاس إلى أصلٍ مُسمًّى")
            if self.multiplicity_is_the_proof is not None:
                raise CaseDataError("حالةُ الأصل لا تحتجّ بتعدُّدِ مواضيعَ تُثبته")
            return
        if not self.declared_differences:
            raise CaseDataError(
                "حالةٌ مضادّةٌ بلا فرقٍ مُعلَنٍ عن أصلها دعوى بلا موضع؛ و"
                + A_GOLDEN_COUNTER_CASE_IS_ONE_DECLARED_DIFFERENCE
            )
        many = len(self.declared_differences) > 1
        if many and self.multiplicity_is_the_proof is None:
            raise CaseDataError(A_GOLDEN_COUNTER_CASE_IS_ONE_DECLARED_DIFFERENCE)
        if self.multiplicity_is_the_proof is not None:
            _text(self.multiplicity_is_the_proof, "تعليلُ تعدُّدِ الفروق")
            if len(self.declared_differences) < 2:
                raise CaseDataError("تعليلُ التعدُّدِ لا موضعَ له في حالةٍ فرقُها واحد")
        paths = [difference.path for difference in self.declared_differences]
        if len(set(paths)) != len(paths):
            raise CaseDataError("فرقان في موضعٍ واحدٍ فرقٌ واحدٌ كُتِب مرّتين")

    @classmethod
    def of(cls, document: dict[str, Any]) -> GoldenExecutionCase:
        _exact_keys(
            document,
            frozenset(
                {
                    "case_id",
                    "document",
                    "baseline_case_id",
                    "declared_differences",
                    "multiplicity_is_the_proof",
                }
            ),
            "ملفُّ الحالة",
        )
        _refuse_readout_keys(document, "ملفُّ الحالة")
        return cls(
            case_id=document["case_id"],
            document=_mapping(document["document"], "وثيقةُ الحالة"),
            baseline_case_id=_optional_text(document["baseline_case_id"], "أصلُ الحالة"),
            declared_differences=tuple(
                DeclaredDifference.of(_mapping(item, "الفرقُ المُعلَن"))
                for item in _sequence(document["declared_differences"], "فروقُ الحالة")
            ),
            multiplicity_is_the_proof=_optional_text(
                document["multiplicity_is_the_proof"], "تعليلُ تعدُّدِ الفروق"
            ),
        )


@dataclass(frozen=True, slots=True)
class GoldenExpectation:
    """توقُّعُ حالةٍ مجمَّدٌ قبل أوّل قراءة؛ ولا بصمةَ تنفيذٍ فيه ألبتّة."""

    case_id: str
    matrix_digest: str
    law_set_digest: str
    expected_disposition: CaseDisposition
    expected_trace: tuple[ExpectedTraceRow, ...]
    expected_violations: tuple[tuple[ExecutionLaw, str | None], ...]
    expected_residual_subject_ids: tuple[str, ...]
    expected_materialized_identity_id: str | None
    citations: tuple[CoverageCitation, ...]

    def __post_init__(self) -> None:
        _text(self.case_id, "مُعرِّفُ الحالة")
        if self.matrix_digest != COVERAGE_MATRIX_DIGEST:
            raise CaseDataError(
                "توقُّعٌ مشدودٌ إلى مصفوفةٍ أخرى: بصمةُ المصفوفة في التوقُّع تخالف "
                "المصفوفةَ المجمَّدة، ولا يُقرَأ بها مطلب"
            )
        if self.law_set_digest != LAW_SET_DIGEST:
            raise CaseDataError(
                "توقُّعٌ مشدودٌ إلى قائمةِ قوانينَ أخرى؛ والنتيجةُ تحمل قائمتَها"
            )
        if self.expected_disposition not in VERDICT_DISPOSITIONS:
            raise CaseDataError(
                "حالةٌ ذهبيّةٌ تنتهي إلى حكم؛ وفسادُ الإدخال والعطبُ شاهدان بأنواعهما"
            )
        if not self.expected_trace:
            raise CaseDataError("توقُّعٌ بلا أثرٍ متوقَّعٍ لا يُحاسَب عليه")
        self._refuse_a_contradicting_subject()
        self._refuse_an_aggregation_that_disagrees()
        self._refuse_violations_that_are_not_in_the_trace()
        self._refuse_a_materialization_that_disagrees()
        self._refuse_a_citation_that_the_matrix_denies()

    def _refuse_a_contradicting_subject(self) -> None:
        standings: dict[tuple[ExecutionLaw, str | None], CheckStanding] = {}
        for row in self.expected_trace:
            key = (row.law, row.subject_id)
            seen = standings.get(key)
            if seen is not None and seen is not row.standing:
                raise CaseDataError(
                    f"منزلتان متعارضتان لقانونٍ على موضوعٍ واحدٍ في القراءة نفسِها: "
                    f"«{row.law.value}» على «{row.subject_id}»"
                )
            standings[key] = row.standing

    def _refuse_an_aggregation_that_disagrees(self) -> None:
        standings = {row.standing for row in self.expected_trace}
        if CheckStanding.VIOLATED in standings:
            derived = CaseDisposition.BLOCK
        elif CheckStanding.UNRESOLVED in standings:
            derived = CaseDisposition.DEFER
        else:
            derived = CaseDisposition.PASS
        if derived is not self.expected_disposition:
            raise CaseDataError(
                "الحكمُ المتوقَّع يخالف منازلَ الأثر المتوقَّع؛ والرتبةُ "
                "`BLOCK > DEFER > PASS` لا تُستثنى لحالة"
            )

    def _refuse_violations_that_are_not_in_the_trace(self) -> None:
        from_trace = tuple(
            (row.law, row.subject_id)
            for row in self.expected_trace
            if row.standing is CheckStanding.VIOLATED
        )
        if tuple(self.expected_violations) != from_trace:
            raise CaseDataError(
                "المخالفاتُ المتوقَّعةُ هي أسطرُ المخالفة نفسُها بترتيبها؛ ولا "
                "تُصنَع مخالفةٌ من غير سطرٍ ولا يُطوى سطرُ مخالفة"
            )

    def _refuse_a_materialization_that_disagrees(self) -> None:
        passing = self.expected_disposition is CaseDisposition.PASS
        if passing != (self.expected_materialized_identity_id is not None):
            raise CaseDataError(
                "النجاحُ وحدَه يبلغ المادّةَ السلطويّةَ ولا يخلو منها؛ والعلاقةُ "
                "ثنائيّةُ الاتّجاه"
            )

    def _refuse_a_citation_that_the_matrix_denies(self) -> None:
        seen: set[str] = set()
        rows = {(row.law, row.subject_id, row.standing) for row in self.expected_trace}
        for citation in self.citations:
            if citation.requirement_id in seen:
                raise CaseDataError(
                    f"استشهادٌ مكرَّرٌ بمطلبٍ واحدٍ في حالةٍ واحدة: "
                    f"«{citation.requirement_id}»"
                )
            seen.add(citation.requirement_id)
            requirement = citation.requirement()
            if not requirement.required or not requirement.reachable:
                raise CaseDataError(
                    "لا حالةَ لخليّةٍ ممتنعةٍ ولا لمطلبٍ غيرِ واجب؛ والممتنعُ يُعلَّل "
                    "ولا يُصطنَع له شاهد"
                )
            if requirement.axis is CoverageAxis.LAW_STANDING:
                self._refuse_a_law_standing_citation_that_disagrees(
                    citation, requirement, rows
                )
                continue
            _refuse_a_whole_case_citation_that_disagrees(citation, requirement)
            if (
                requirement.expected_disposition is not None
                and requirement.expected_disposition is not self.expected_disposition
            ):
                raise CaseDataError(
                    f"استشهادٌ بمطلبٍ يقيّد حكمًا غيرَ حكم الحالة: "
                    f"«{citation.requirement_id}»"
                )

    def _refuse_a_law_standing_citation_that_disagrees(
        self,
        citation: CoverageCitation,
        requirement: CoverageRequirement,
        rows: set[tuple[ExecutionLaw, str | None, CheckStanding]],
    ) -> None:
        if citation.law is not requirement.law or (
            citation.standing is not requirement.target_standing
        ):
            raise CaseDataError(
                f"استشهادٌ يسمّي قانونًا أو منزلةً غيرَ خليّته: "
                f"«{citation.requirement_id}»"
            )
        assert citation.law is not None and citation.standing is not None
        scope = EVALUATION_SCOPE_OF_LAW[citation.law]
        if scope is EvaluationScope.SUBJECT:
            if citation.witness_subject_id is None:
                raise CaseDataError(
                    f"قانونٌ نطاقُه موضوعٌ يُسمّي شاهدَه بموضوعه: «{citation.law.value}»"
                )
            found = (
                citation.law,
                citation.witness_subject_id,
                citation.standing,
            ) in rows
        else:
            if citation.witness_subject_id is not None:
                raise CaseDataError(
                    f"قانونٌ نطاقُه القضيّةُ لا يُسمّى له شاهدُ موضوع: "
                    f"«{citation.law.value}»"
                )
            found = any(
                row[0] is citation.law and row[2] is citation.standing for row in rows
            )
        if not found:
            raise CaseDataError(
                "استشهادٌ لا يقابله سطرٌ في أثر الحالة المتوقَّع؛ و"
                + A_CITATION_IS_A_CLAIM_UNTIL_THE_READOUT
            )

    @classmethod
    def of(cls, document: dict[str, Any]) -> GoldenExpectation:
        _exact_keys(
            document,
            frozenset(
                {
                    "case_id",
                    "matrix_digest",
                    "law_set_digest",
                    "expected_disposition",
                    "expected_trace",
                    "expected_violations",
                    "expected_residual_subject_ids",
                    "expected_materialized_identity_id",
                    "citations",
                }
            ),
            "ملفُّ التوقُّع",
        )
        _refuse_readout_keys(document, "ملفُّ التوقُّع")
        violations: list[tuple[ExecutionLaw, str | None]] = []
        for raw in _sequence(document["expected_violations"], "المخالفاتُ المتوقَّعة"):
            item = _mapping(raw, "المخالفةُ المتوقَّعة")
            _exact_keys(item, frozenset({"law", "subject_id"}), "المخالفةُ المتوقَّعة")
            violations.append(
                (
                    _member(ExecutionLaw, item["law"], "قانونُ المخالفة"),
                    _optional_text(item["subject_id"], "موضوعُ المخالفة"),
                )
            )
        return cls(
            case_id=document["case_id"],
            matrix_digest=_text(document["matrix_digest"], "بصمةُ المصفوفة"),
            law_set_digest=_text(document["law_set_digest"], "بصمةُ القائمة"),
            expected_disposition=_member(
                CaseDisposition, document["expected_disposition"], "الحكمُ المتوقَّع"
            ),
            expected_trace=tuple(
                ExpectedTraceRow.of(_mapping(item, "سطرُ الأثر"))
                for item in _sequence(document["expected_trace"], "الأثرُ المتوقَّع")
            ),
            expected_violations=tuple(violations),
            expected_residual_subject_ids=tuple(
                _text(item, "موضوعُ البقيّة")
                for item in _sequence(
                    document["expected_residual_subject_ids"], "البقايا المتوقَّعة"
                )
            ),
            expected_materialized_identity_id=_optional_text(
                document["expected_materialized_identity_id"], "المادّةُ السلطويّة"
            ),
            citations=tuple(
                CoverageCitation.of(_mapping(item, "الاستشهاد"))
                for item in _sequence(document["citations"], "استشهاداتُ الحالة")
            ),
        )


@dataclass(frozen=True, slots=True)
class InvalidInputWitness:
    """شاهدُ فساد إدخال: وثيقةٌ لا تقوم منها قضيّة؛ لا أثرَ ولا غلافَ ولا حكم."""

    witness_id: str
    document: dict[str, Any]
    expected_fault_kinds: tuple[str, ...]
    citations: tuple[CoverageCitation, ...]

    def __post_init__(self) -> None:
        _text(self.witness_id, "مُعرِّفُ الشاهد")
        _mapping(self.document, "وثيقةُ الشاهد")
        if not self.expected_fault_kinds:
            raise CaseDataError("شاهدُ فسادٍ بلا عيبٍ مُسمًّى دعوى بلا مادّة")
        if len(set(self.expected_fault_kinds)) != len(self.expected_fault_kinds):
            raise CaseDataError("جنسُ عيبٍ مكرَّرٌ يُخفي عيبًا آخر")
        _refuse_witness_citations(self.citations, CaseDisposition.INVALID_INPUT)

    @classmethod
    def of(cls, document: dict[str, Any]) -> InvalidInputWitness:
        _exact_keys(
            document,
            frozenset({"witness_id", "document", "expected_fault_kinds", "citations"}),
            "ملفُّ شاهد الفساد",
        )
        _refuse_readout_keys(document, "ملفُّ شاهد الفساد")
        return cls(
            witness_id=document["witness_id"],
            document=_mapping(document["document"], "وثيقةُ الشاهد"),
            expected_fault_kinds=tuple(
                _text(item, "جنسُ العيب")
                for item in _sequence(
                    document["expected_fault_kinds"], "أجناسُ العيب المتوقَّعة"
                )
            ),
            citations=tuple(
                CoverageCitation.of(_mapping(item, "الاستشهاد"))
                for item in _sequence(document["citations"], "استشهاداتُ الشاهد")
            ),
        )


@dataclass(frozen=True, slots=True)
class EngineSeamWitness:
    """شاهدُ حدٍّ داخليٍّ للمحرّك؛ بلا وثيقةٍ يكتبها صاحبُ قضيّة."""

    witness_id: str
    seam: str
    reached_by: str
    refused_document_reason: str
    citations: tuple[CoverageCitation, ...]

    def __post_init__(self) -> None:
        for value, label in (
            (self.witness_id, "مُعرِّفُ الشاهد"),
            (self.seam, "موضعُ الحدّ"),
            (self.reached_by, "طريقُ البلوغ"),
            (self.refused_document_reason, "تعليلُ منع الوثيقة"),
        ):
            _text(value, label)
        _refuse_witness_citations(self.citations, CaseDisposition.INVARIANT_ERROR)

    @classmethod
    def of(cls, document: dict[str, Any]) -> EngineSeamWitness:
        _exact_keys(
            document,
            frozenset(
                {
                    "witness_id",
                    "seam",
                    "reached_by",
                    "refused_document_reason",
                    "citations",
                }
            ),
            "ملفُّ شاهد الحدّ",
        )
        if "document" in document:
            raise CaseDataError(AN_INVARIANT_ERROR_IS_NOT_IN_THE_USER_CASE_SPACE)
        return cls(
            witness_id=document["witness_id"],
            seam=document["seam"],
            reached_by=document["reached_by"],
            refused_document_reason=document["refused_document_reason"],
            citations=tuple(
                CoverageCitation.of(_mapping(item, "الاستشهاد"))
                for item in _sequence(document["citations"], "استشهاداتُ الشاهد")
            ),
        )


@dataclass(frozen=True, slots=True)
class CorpusCoverage:
    """قراءةُ تغطيةٍ مُشتَقّة: ما استُشهِد به، وما بقي مُسمًّى لا مطويًّا."""

    cited_requirement_ids: tuple[str, ...]
    uncovered_requirement_ids: tuple[str, ...]

    @property
    def is_complete(self) -> bool:
        """أبلغت الدعاوى كلَّ مطلبٍ واجب؟ ودعوى التغطية غيرُ التغطية."""

        return not self.uncovered_requirement_ids


@dataclass(frozen=True, slots=True)
class GoldenCaseCorpus:
    """المدوّنةُ المقروءةُ من ملفّاتها: حالاتٌ وتوقُّعاتٌ وشاهدان."""

    corpus_id: str
    cases: tuple[GoldenExecutionCase, ...]
    expectations: tuple[GoldenExpectation, ...]
    invalid_input_witnesses: tuple[InvalidInputWitness, ...]
    engine_seam_witnesses: tuple[EngineSeamWitness, ...]
    declared_uncovered_requirement_ids: tuple[str, ...]

    def __post_init__(self) -> None:
        _text(self.corpus_id, "اسمُ المدوّنة")
        case_ids = [case.case_id for case in self.cases]
        if len(set(case_ids)) != len(case_ids):
            raise CaseDataError("مُعرِّفُ حالةٍ مكرَّرٌ يُخفي حالة")
        expectation_ids = [item.case_id for item in self.expectations]
        if len(set(expectation_ids)) != len(expectation_ids):
            raise CaseDataError("توقُّعان لحالةٍ واحدةٍ توقُّعٌ لا يُحاسَب عليه")
        if set(case_ids) != set(expectation_ids):
            raise CaseDataError(
                "كلُّ حالةٍ توقُّعٌ واحدٌ يقابلها؛ وحالةٌ بلا توقُّعٍ أو توقُّعٌ بلا حالةٍ "
                "قطعٌ للسلسلة قبل القراءة"
            )
        for case in self.cases:
            if case.baseline_case_id is None:
                continue
            if case.baseline_case_id not in set(case_ids):
                raise CaseDataError(
                    f"حالةٌ تُقاس إلى أصلٍ ليس في المدوّنة: «{case.baseline_case_id}»"
                )
            if case.baseline_case_id == case.case_id:
                raise CaseDataError("حالةٌ لا تكون أصلًا لنفسها")
        witness_ids = [item.witness_id for item in self.invalid_input_witnesses]
        witness_ids += [item.witness_id for item in self.engine_seam_witnesses]
        if len(set(witness_ids)) != len(witness_ids):
            raise CaseDataError("مُعرِّفُ شاهدٍ مكرَّرٌ يُخفي شاهدًا")
        if set(witness_ids) & set(case_ids):
            raise CaseDataError(
                "شاهدٌ باسم حالةٍ يخلط فضاءَ القضايا بما ليس منه؛ و"
                + AN_INVARIANT_ERROR_IS_NOT_IN_THE_USER_CASE_SPACE
            )
        declared = self.declared_uncovered_requirement_ids
        if len(set(declared)) != len(declared):
            raise CaseDataError("مطلبٌ غيرُ مُغطًّى مُسمًّى مرّتين")
        if tuple(sorted(declared)) != declared:
            raise CaseDataError("المطالبُ المؤجَّلةُ تُسمّى على ترتيبٍ واحدٍ لا يتقلّب")
        if self.coverage.uncovered_requirement_ids != declared:
            raise CaseDataError(
                "ما لم يُغطَّ يُسمّى بالاسم ولا يُطوى: قائمةُ المؤجَّل في البيان تخالف "
                "المُشتَقّةَ من الاستشهادات"
            )

    @property
    def coverage(self) -> CorpusCoverage:
        """التغطيةُ المُشتَقّة؛ دعوًى إلى أن تثبتها القراءةُ سطرًا سطرًا."""

        cited = {
            citation.requirement_id
            for expectation in self.expectations
            for citation in expectation.citations
        }
        cited |= {
            citation.requirement_id
            for witness in self.invalid_input_witnesses
            for citation in witness.citations
        }
        cited |= {
            citation.requirement_id
            for witness in self.engine_seam_witnesses
            for citation in witness.citations
        }
        required = tuple(item.requirement_id for item in COVERAGE_MATRIX.required_cases)
        return CorpusCoverage(
            cited_requirement_ids=tuple(sorted(cited)),
            uncovered_requirement_ids=tuple(
                sorted(item for item in required if item not in cited)
            ),
        )

    @classmethod
    def of(
        cls,
        manifest: dict[str, Any],
        cases: tuple[dict[str, Any], ...],
        expectations: tuple[dict[str, Any], ...],
        invalid_input_witnesses: tuple[dict[str, Any], ...],
        engine_seam_witnesses: tuple[dict[str, Any], ...],
    ) -> GoldenCaseCorpus:
        """اقرأ المدوّنةَ من موادَّ مقروءةٍ سلفًا؛ ولا تفتح هذه الطبقةُ ملفًّا ولا تبني حالة."""

        _exact_keys(
            _mapping(manifest, "بيانُ المدوّنة"),
            frozenset({"corpus_id", "uncovered_requirement_ids"}),
            "بيانُ المدوّنة",
        )
        return cls(
            corpus_id=_text(manifest["corpus_id"], "اسمُ المدوّنة"),
            cases=tuple(
                GoldenExecutionCase.of(_mapping(item, "ملفُّ الحالة")) for item in cases
            ),
            expectations=tuple(
                GoldenExpectation.of(_mapping(item, "ملفُّ التوقُّع"))
                for item in expectations
            ),
            invalid_input_witnesses=tuple(
                InvalidInputWitness.of(_mapping(item, "ملفُّ شاهد الفساد"))
                for item in invalid_input_witnesses
            ),
            engine_seam_witnesses=tuple(
                EngineSeamWitness.of(_mapping(item, "ملفُّ شاهد الحدّ"))
                for item in engine_seam_witnesses
            ),
            declared_uncovered_requirement_ids=tuple(
                _text(item, "مطلبٌ مؤجَّل")
                for item in _sequence(
                    manifest["uncovered_requirement_ids"], "المطالبُ المؤجَّلة"
                )
            ),
        )
