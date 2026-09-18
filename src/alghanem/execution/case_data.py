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
حدٍّ داخليٍّ يُبلَغ بمادّةٍ مُشتَقّةٍ ناقصةٍ بعد نجاحٍ مبدئيّ. وكذلك بطلانُ تكوين
القضيّة هويّةٌ منفصلةٌ: `InvalidInputWitness ≠ GoldenExecutionCase`، لا أثرَ له ولا
غلافَ ولا حكم.

**والوثيقةُ المجمَّدةُ لا تُحوَّر** (`AFrozenDocumentIsDeeplyImmutable`):

    FrozenData  ≺  Readout

فالحالةُ والشاهدُ يحفظان محتوًى مجمَّدًا تجميدًا متعدِّيًا وتُشتَقّ الوثيقةُ من
جديدٍ عند كلّ قراءة؛ إذ لو أمسكت `READOUT` قاموسًا داخل حالةٍ «مجمَّدةٍ» فغيَّرته
لسقط الفصلُ التاريخيُّ بين البيانات والقراءة.

**والفرقُ المُعلَن هو الفرقُ الواقع**
(`ADeclaredDifferenceIsTheActualDifference`):

    Diff(BaselineDocument, CounterDocument)  =  DeclaredDifferences

فيُقاس النصّان المؤلَّفان بعضُهما ببعض — لا يُشغَّل المحرّك ولا يُخرَق
`DATA ≺ READOUT` — فيُستخرَج فرقٌ بنيويٌّ عمليّتُه `ADD` أو `REMOVE` أو `REPLACE`،
بموضعه وحالتِه قبلُ وبعدُ، ثمّ يُطابَق بالمُعلَن مطابقةً تامّة. وبهذا صار
`GoldenCounterCase = ValidBaseline + OneDeclaredDifference` مطلبًا مفروضًا لا
إفادةً من المؤلِّف. وسلسلةُ الأصول تُقاس خطوةً واحدةً إلى الأصل المُسمّى، ولا
تعود على نفسها حلقةً.

**والعقدُ على الصنف لا على مصنعه** (`AContractBindsTheClassNotItsFactory`):
المُنشئُ العامُّ في بايثون طريقٌ قانونيٌّ كمثل `of`، فلو اكتفى `of` بالتجميد بقي
للحالة بابٌ تُبنى منه بقاموسٍ حيٍّ يُغيَّر بعد بنائها. ولذلك تُعاد الوثيقةُ — وما
كان الفرقُ المُعلَنُ وما صار — مجمَّدةً في `__post_init__` نفسِه، فلا يُستثنى من
العقد طريق.

تسجيلٌ لا سلطة: لا ولادةَ ولا حكمَ ولادةٍ ولا تجميدَ `E0`.
"""

from __future__ import annotations

from collections.abc import Mapping
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
from .frozen_json import (
    A_DIFFERENCE_IS_AN_OPERATION_NOT_A_PATH,
    A_FROZEN_DOCUMENT_IS_DEEPLY_IMMUTABLE,
    DiffOperation,
    FrozenJson,
    FrozenJsonError,
    StructuralDiff,
    freeze_json,
    frozen_equal,
    structural_diff,
    thaw_json,
)
from .lawset import LAW_SET_DIGEST, ExecutionLaw
from .outcome import CheckStanding
from .standing import InputFaultKind

__all__ = [
    "A_BASELINE_CHAIN_DOES_NOT_TURN_BACK_ON_ITSELF",
    "A_CONTRACT_BINDS_THE_CLASS_NOT_ITS_FACTORY",
    "A_CASE_IS_AUTHORED_NOT_GENERATED",
    "A_CITATION_IS_A_CLAIM_UNTIL_THE_READOUT",
    "A_DECLARED_DIFFERENCE_IS_THE_ACTUAL_DIFFERENCE",
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

A_DECLARED_DIFFERENCE_IS_THE_ACTUAL_DIFFERENCE: Final[str] = (
    "الفرقُ المُعلَن هو الفرقُ الواقع: يُقاس النصّان المؤلَّفان فيُستخرَج فرقُهما "
    "عمليّةً وموضعًا وحالةً قبلُ وبعدُ، ثمّ يُطابَق بالمُعلَن؛ ومن اكتفى بتصريح "
    "المؤلِّف جعل الفرقَ دعوًى لا شهادة"
)

A_CONTRACT_BINDS_THE_CLASS_NOT_ITS_FACTORY: Final[str] = (
    "العقدُ على الصنف لا على مصنعه: المُنشئُ العامُّ طريقٌ قانونيٌّ كمثل مصنعه، "
    "فتُعاد الوثيقةُ وحالتا الفرق مجمَّدةً في بناء الكائن نفسِه؛ ومن جمَّد في "
    "المصنع وحدَه ترك للقاموس الحيِّ بابًا"
)

A_BASELINE_CHAIN_DOES_NOT_TURN_BACK_ON_ITSELF: Final[str] = (
    "سلسلةُ الأصول لا تعود على نفسها: الأصلُ سابقٌ على ما تفرَّع عنه، وحلقةٌ "
    "دائرةٌ تجعل كلَّ حالةٍ فيها أصلًا لنفسها بواسطة؛ فلا أصلَ يُقاس إليه"
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
"""ما تنتهي إليه قضيّةٌ قائمةُ الإدخال؛ وبطلانُ التكوين والعطبُ شاهدان لا حالتان."""

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


def _frozen(value: object, label: str) -> FrozenJson:
    """جمّدْ قيمةً مقروءةً تجميدًا متعدِّيًا؛ وما خرج عن عقد `JSON` يُردّ."""

    try:
        return freeze_json(value, label)
    except FrozenJsonError as refusal:
        raise CaseDataError(str(refusal)) from refusal


def _frozen_mapping(value: object, label: str) -> Mapping[str, FrozenJson]:
    """وثيقةٌ مجمَّدةٌ تجميدًا متعدِّيًا؛ لا قاموسَ مشترَكٌ يُعدَّل بعد التجميد."""

    frozen = _frozen(_mapping(value, label), label)
    if not isinstance(frozen, Mapping):  # pragma: no cover - حارسُ نوع
        raise CaseDataError(f"{label} كائنٌ مُصرَّحٌ به")
    return frozen


def _refrozen_document(value: object, label: str) -> Mapping[str, FrozenJson]:
    """أعدْ تجميدَ وثيقةٍ بُنِيت بالمُنشئ العامّ؛ فالعقدُ على الصنف لا على مصنعه."""

    if not isinstance(value, Mapping):
        raise CaseDataError(
            f"{label} محتوًى مجمَّدٌ متعدٍّ؛ و" + A_FROZEN_DOCUMENT_IS_DEEPLY_IMMUTABLE
        )
    frozen = _frozen(dict(value), label)
    if not isinstance(frozen, Mapping):  # pragma: no cover - حارسُ نوع
        raise CaseDataError(f"{label} كائنٌ مُصرَّحٌ به")
    return frozen


def _sequence(value: object, label: str) -> list[Any]:
    if not isinstance(value, list):
        raise CaseDataError(f"{label} قائمةٌ مرتَّبةٌ مُصرَّحٌ بها")
    return value


def _exact_keys(
    document: Mapping[str, Any], expected: frozenset[str], label: str
) -> None:
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
    """فرقٌ واحدٌ مُعلَنٌ عن الأصل: عمليّتُه، وموضعُه، وما كان، وما صار، ثمّ بيانُه."""

    operation: DiffOperation
    path: str
    before: FrozenJson
    after: FrozenJson
    statement: str

    def __post_init__(self) -> None:
        if not isinstance(self.operation, DiffOperation):
            raise CaseDataError("عمليّةُ الفرق عضوٌ في مفردتها المغلقة")
        _text(self.path, "موضعُ الفرق")
        _text(self.statement, "بيانُ الفرق")
        object.__setattr__(self, "before", _frozen(self.before, f"{self.path}: ما كان"))
        object.__setattr__(self, "after", _frozen(self.after, f"{self.path}: ما صار"))
        if self.operation is DiffOperation.ADD and self.before is not None:
            raise CaseDataError("الزيادةُ لا حالةَ لها قبلَ وقوعها")
        if self.operation is DiffOperation.REMOVE and self.after is not None:
            raise CaseDataError("الحذفُ لا حالةَ له بعد وقوعه")
        if self.operation is DiffOperation.REPLACE and frozen_equal(
            self.before, self.after
        ):
            raise CaseDataError("إبدالُ الشيء بنفسه ليس فرقًا يُعلَن")

    @classmethod
    def of(cls, document: Mapping[str, Any]) -> DeclaredDifference:
        _exact_keys(
            document,
            frozenset({"operation", "path", "before", "after", "statement"}),
            "الفرقُ المُعلَن",
        )
        return cls(
            operation=_member(DiffOperation, document["operation"], "عمليّةُ الفرق"),
            path=document["path"],
            before=_frozen(document["before"], "حالةُ الموضع قبل الفرق"),
            after=_frozen(document["after"], "حالةُ الموضع بعد الفرق"),
            statement=document["statement"],
        )

    def as_structural_diff(self) -> StructuralDiff:
        """صورةُ الفرق المُعلَن بنيويّةً، ليُطابَق بالفرق المُستخرَج من النصّين."""

        return StructuralDiff(
            operation=self.operation,
            path=self.path,
            before=self.before,
            after=self.after,
        )


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
    document_content: Mapping[str, FrozenJson]
    baseline_case_id: str | None
    declared_differences: tuple[DeclaredDifference, ...]
    multiplicity_is_the_proof: str | None

    def __post_init__(self) -> None:
        _text(self.case_id, "مُعرِّفُ الحالة")
        object.__setattr__(
            self,
            "document_content",
            _refrozen_document(self.document_content, "وثيقةُ الحالة"),
        )
        _exact_keys(
            self.document_content,
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

    @property
    def document(self) -> dict[str, Any]:
        """وثيقةُ الحالة مُشتَقّةً من جديدٍ في كلّ قراءة؛ فلا نسخةَ مشتركةٌ تُعدَّل."""

        return {key: thaw_json(value) for key, value in self.document_content.items()}

    @classmethod
    def of(cls, document: Mapping[str, Any]) -> GoldenExecutionCase:
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
            document_content=_frozen_mapping(document["document"], "وثيقةُ الحالة"),
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
                "حالةٌ ذهبيّةٌ تنتهي إلى حكم؛ وبطلانُ التكوين والعطبُ شاهدان بأنواعهما"
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
    """شاهدُ بطلانِ تكوين: وثيقةٌ لا تقوم منها قضيّة؛ لا أثرَ ولا غلافَ ولا حكم."""

    witness_id: str
    document_content: Mapping[str, FrozenJson]
    expected_fault_kinds: tuple[InputFaultKind, ...]
    citations: tuple[CoverageCitation, ...]

    def __post_init__(self) -> None:
        _text(self.witness_id, "مُعرِّفُ الشاهد")
        object.__setattr__(
            self,
            "document_content",
            _refrozen_document(self.document_content, "وثيقةُ الشاهد"),
        )
        if not self.expected_fault_kinds:
            raise CaseDataError("شاهدُ بطلانٍ بلا عيبٍ مُسمًّى دعوى بلا مادّة")
        for kind in self.expected_fault_kinds:
            if not isinstance(kind, InputFaultKind):
                raise CaseDataError("جنسُ العيب عضوٌ في مفردته المغلقة")
        if len(set(self.expected_fault_kinds)) != len(self.expected_fault_kinds):
            raise CaseDataError("جنسُ عيبٍ مكرَّرٌ يُخفي عيبًا آخر")
        _refuse_witness_citations(self.citations, CaseDisposition.INVALID_INPUT)

    @property
    def document(self) -> dict[str, Any]:
        """وثيقةُ الشاهد مُشتَقّةً من جديدٍ في كلّ قراءة؛ فلا نسخةَ مشتركةٌ تُعدَّل."""

        return {key: thaw_json(value) for key, value in self.document_content.items()}

    @classmethod
    def of(cls, document: Mapping[str, Any]) -> InvalidInputWitness:
        _exact_keys(
            document,
            frozenset({"witness_id", "document", "expected_fault_kinds", "citations"}),
            "ملفُّ شاهد البطلان",
        )
        _refuse_readout_keys(document, "ملفُّ شاهد البطلان")
        return cls(
            witness_id=document["witness_id"],
            document_content=_frozen_mapping(document["document"], "وثيقةُ الشاهد"),
            expected_fault_kinds=tuple(
                _member(InputFaultKind, item, "جنسُ العيب")
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
        self._refuse_a_baseline_chain_that_turns_back()
        self._refuse_a_difference_that_the_two_documents_deny()
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

    def _refuse_a_baseline_chain_that_turns_back(self) -> None:
        """سلسلةُ الأصول شجرةٌ لا حلقة؛ ومنعُ الأصل لنفسه لا يمنع دورةً بواسطة."""

        baselines = {case.case_id: case.baseline_case_id for case in self.cases}
        for start in baselines:
            seen = {start}
            current = baselines[start]
            while current is not None:
                if current in seen:
                    raise CaseDataError(
                        f"سلسلةُ أصولٍ تعود على نفسها عند «{current}»؛ و"
                        + A_BASELINE_CHAIN_DOES_NOT_TURN_BACK_ON_ITSELF
                    )
                seen.add(current)
                current = baselines.get(current)

    def _refuse_a_difference_that_the_two_documents_deny(self) -> None:
        """الفرقُ المُعلَن يساوي الفرقَ المُستخرَج من الوثيقتين؛ مقارنةً بخطوةٍ واحدة."""

        by_id = {case.case_id: case for case in self.cases}
        for case in self.cases:
            if case.baseline_case_id is None:
                continue
            baseline = by_id[case.baseline_case_id]
            try:
                actual = structural_diff(
                    baseline.document_content, case.document_content
                )
            except FrozenJsonError as refusal:
                raise CaseDataError(
                    f"«{case.case_id}» لا يُقاس فرقُه إلى «{baseline.case_id}»: "
                    + str(refusal)
                ) from refusal
            self._refuse_a_case_that_matches_its_baseline(case, actual)
            self._refuse_a_declaration_that_is_not_the_difference(case, actual)
            self._refuse_a_multiplicity_that_the_documents_deny(case, actual)

    @staticmethod
    def _refuse_a_case_that_matches_its_baseline(
        case: GoldenExecutionCase, actual: tuple[StructuralDiff, ...]
    ) -> None:
        if not actual:
            raise CaseDataError(
                f"حالةٌ مضادّةٌ لا تخالف أصلَها في موضع: «{case.case_id}»؛ و"
                + A_DECLARED_DIFFERENCE_IS_THE_ACTUAL_DIFFERENCE
            )

    @staticmethod
    def _refuse_a_declaration_that_is_not_the_difference(
        case: GoldenExecutionCase, actual: tuple[StructuralDiff, ...]
    ) -> None:
        found = {item.path: item for item in actual}
        declared = {
            item.path: item.as_structural_diff() for item in case.declared_differences
        }
        for path in sorted(found):
            if path not in declared:
                raise CaseDataError(
                    f"فرقٌ واقعٌ لم يُعلَن في «{case.case_id}»: «{path}»؛ و"
                    + A_DECLARED_DIFFERENCE_IS_THE_ACTUAL_DIFFERENCE
                )
        for path in sorted(declared):
            if path not in found:
                raise CaseDataError(
                    f"فرقٌ مُعلَنٌ لا يقع في «{case.case_id}»: «{path}»؛ و"
                    + A_DECLARED_DIFFERENCE_IS_THE_ACTUAL_DIFFERENCE
                )
            claimed, real = declared[path], found[path]
            if (
                claimed.operation is not real.operation
                or not frozen_equal(claimed.before, real.before)
                or not frozen_equal(claimed.after, real.after)
            ):
                raise CaseDataError(
                    f"فرقٌ مُعلَنٌ يصف غيرَ ما وقع في «{case.case_id}»: «{path}»؛ و"
                    + A_DIFFERENCE_IS_AN_OPERATION_NOT_A_PATH
                )

    @staticmethod
    def _refuse_a_multiplicity_that_the_documents_deny(
        case: GoldenExecutionCase, actual: tuple[StructuralDiff, ...]
    ) -> None:
        if case.multiplicity_is_the_proof is None:
            if len(actual) != 1:
                raise CaseDataError(
                    f"حالةٌ مضادّةٌ فرقُها الواقعُ أكثرُ من واحدٍ بلا تعليل: "
                    f"«{case.case_id}»؛ و"
                    + A_GOLDEN_COUNTER_CASE_IS_ONE_DECLARED_DIFFERENCE
                )
        elif len(actual) < 2:
            raise CaseDataError(
                f"تعليلُ التعدُّدِ لا موضعَ له في حالةٍ فرقُها الواقعُ واحد: "
                f"«{case.case_id}»"
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
                InvalidInputWitness.of(_mapping(item, "ملفُّ شاهد البطلان"))
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
