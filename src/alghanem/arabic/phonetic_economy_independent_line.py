"""بوّابةُ قبولِ خطِّ دليلٍ مستقلٍّ حقًّا، لا اختلاقُ خطٍّ يقلب الحكم.

سجّلت وحدةُ `phonetic_economy_candidate` نتيجةً سلبية: فحصُ الإغلاق المستقلّ
`FAIL`، وحكمُ السلسلة `DEFER_IN_SCOPE`، لأنّ خطَّي الدليل خرجا من كوربصٍ واحد
وأداةٍ واحدة وتعريفِ مقياسٍ واحد. وقالت الوحدةُ إنّ الفحص محسوبٌ لا مكتوب،
فـ«إن زُوِّد لاحقًا دليلٌ من كوربصٍ آخر أو أداةٍ أخرى أو تعريفِ مقياسٍ آخر،
أُعيد تشغيلُ الفحص نفسِه بلا تعديلِ سطرٍ واحد».

**والعطبُ الذي تسدُّه هذه الوحدة**: ذلك الوعدُ صحيحٌ حسابيًّا وقابلٌ للتلاعب
عمليًّا. فالمقارنةُ نصّيةٌ بحتة، فيكفي أن يُعاد وصفُ الكوربص نفسِه بمسافةٍ
زائدةٍ أو تطويلٍ أو حركةٍ مُشكَّلة ليصير «كوربصًا آخر» حسابيًّا، فينقلب
`FAIL` إلى `PASS` بلا مصدرٍ جديدٍ البتّة. وتسميةُ ذلك استقلالًا هي عينُ
العطب الذي سُجِّل، مُرتكَبًا من الجهة الأخرى.

**فما تفعله هذه الوحدة**: تُقدِّم بوّابةً يمرّ بها أيُّ خطِّ دليلٍ مقترَح قبل
أن يدخل الفحص، وهي تشترط شرطَين لا واحدًا:

١) **انفكاكٌ محسوبٌ بعد التقييس**: يُقاس الاختلافُ على المحاور الثلاثة بعد
   تطبيع `NFKC` وإسقاطِ التشكيل والتطويل وطيِّ المسافات وحالةِ الحرف، فلا
   يُعدُّ الفرقُ الإملائيُّ وحدَه انفكاكًا. ومحورُ الأداة يُرَدُّ خاصّةً إن
   أشار إلى الأداة المرفقة نفسِها في `phonetic_economy_tool.py`.

٢) **مصدرٌ مُودَعٌ ببصمته**: `ExternalSourceDeposit` لا يكون مُودَعًا
   بالاستشهاد وحدَه، بل ببصمةِ محتوًى بشكل `alghanem.canonical_content`؛ وكلُّ
   محورٍ انفكَّ يجب أن يكون مأذونًا في المصدر المُودَع. وهذا هو الدرسُ نفسُه
   الذي تقوم عليه وحدةُ إعادةِ اشتقاقِ بصمةِ المصدر المستورَد: الآلةُ تُبنى
   مُختبَرة، والحمولةُ إن لم تُودَع قيل ذلك صراحةً ولم يُبنَ عليها ادّعاءُ
   تحقّق.

**وما لا تفعله**: لا تختلق هذه الوحدةُ خطًّا مستقلًّا ولا تُودِع مصدرًا ليس
عندنا. فلا خطَّ مقبولٌ واحدٌ فيها — `ADMITTED_INDEPENDENT_LINES` صفٌّ فارغ،
وبقيّةُ `NO_INDEPENDENT_LINE_DEPOSITED` تقول ذلك بمداها — وبطاقةُ
`PHONETIC_ECONOMY_CANDIDATE` تبقى `FAIL` و`DEFER_IN_SCOPE` كما سُجِّلت، وحارسُ
استيرادٍ هنا يفحص ذلك فعلًا. والمتغيِّرُ قابليةُ القلبِ لا حالُ الدليل.

**ولا سلطةَ لهذه الوحدة**: حتى على فرع `PASS` أقصى ما يُبلَغ
`CLOSURE_MET_PENDING_AUTHORITY` — لا ولادةَ ولا تجميدَ ولا `E0`؛ ولا يقرؤها
`IndependentClosureGate` ولا `BirthVerdictGate`، ولا تدخل في
`BirthExperimentSpecification`، ولا تُرقّي AIM-K3.
"""

from __future__ import annotations

import unicodedata
from dataclasses import dataclass, field, fields
from enum import Enum
from typing import Final

from alghanem.canonical_content import is_canonical_digest

from .phonetic_economy_candidate import (
    CLOSURE_BLOCKING_RESIDUAL_CODE,
    PHONETIC_ECONOMY_CANDIDATE,
    ChainVerdict,
    ClosureOutcome,
    IndependenceAxis,
    IndependentClosureCheck,
    PhoneticEconomyCandidate,
    PhoneticEconomyRegistrationError,
    PhoneticEvidenceItem,
    RegisteredResidual,
    ResidualScope,
)
from .phonetic_economy_tool import TOOL_MODULE_PATH

__all__ = [
    "ADMITTED_INDEPENDENT_LINES",
    "NO_INDEPENDENT_LINE_DEPOSITED",
    "NO_INDEPENDENT_LINE_RESIDUAL_CODE",
    "SESSION_BASELINE_EVIDENCE",
    "AdmittedIndependentLine",
    "ExternalSourceDeposit",
    "IndependentLineAdmissionError",
    "SourceDepositState",
    "admit_independent_line",
    "candidate_with_admitted_line",
    "closure_check_with_admitted_line",
    "cosmetic_axis_key",
]


class IndependentLineAdmissionError(PhoneticEconomyRegistrationError):
    """رُفض خطٌّ مقترَحٌ خارج شرطه؛ ولا يُحمَل على أقرب حالةٍ مقبولة.

    وهو فرعٌ من خطأ وحدةِ التسجيل الأمّ، فمن أمسك الأمَّ أمسك هذا معها ولا
    يتسرّب رفضٌ من صنفٍ جديدٍ غيرِ مُلتقَط.
    """


class SourceDepositState(Enum):
    """حالُ المصدر: مُودَعٌ ببصمته، أم مذكورٌ باستشهاده وحدَه."""

    مُودَع = "مُودَع"
    غير_مُودَع = "غير_مُودَع"


_COSMETIC_STRIPPED: Final[frozenset[str]] = frozenset(
    {
        "\u0640",  # تطويل
    }
)


def cosmetic_axis_key(value: str) -> str:
    """مفتاحُ المحور بعد إسقاطِ ما لا يُغيِّر المرجع: تشكيلٌ وتطويلٌ ومسافات.

    الغرضُ واحد: ألّا يصير إعادةُ رسمِ الوصف نفسِه مصدرًا ثانيًا. وما بقي بعد
    التقييس مختلفًا فهو اختلافُ نصٍّ لا اختلافُ مرجعٍ بالضرورة، ولذلك لا
    يكفي وحدَه للقبول دون مصدرٍ مُودَع.
    """

    if not isinstance(value, str):
        raise IndependentLineAdmissionError("مفتاحُ المحور يُشتقُّ من نصٍّ لا من غيره.")
    normalized = unicodedata.normalize("NFKC", value)
    without_marks = "".join(
        character
        for character in normalized
        if not unicodedata.combining(character) and character not in _COSMETIC_STRIPPED
    )
    return " ".join(without_marks.casefold().split())


@dataclass(frozen=True, slots=True)
class ExternalSourceDeposit:
    """مصدرٌ خارجيٌّ مُستشهَدٌ به، وحالُ إيداعه مُشتقٌّ من بصمته لا مكتوب.

    الاستشهادُ وحدَه لا يُودِع شيئًا: من ادّعى مصدرًا صوتيّاتٍ مستقلًّا ولم
    يُودِع بصمةَ محتواه، فدعواه وصفٌ لا يُعادُ فحصُه. ولذلك `state` دالّةٌ على
    `payload_digest` لا حقلٌ يُعلَن.
    """

    source_id: str
    citation: str
    licensed_axes: tuple[IndependenceAxis, ...]
    payload_digest: str | None = None

    def __post_init__(self) -> None:
        for value, label in (
            (self.source_id, "هويّةُ المصدر"),
            (self.citation, "استشهادُ المصدر"),
        ):
            if not isinstance(value, str) or not value.strip():
                raise IndependentLineAdmissionError(
                    f"{label} نصٌّ غير فارغ؛ ولا يُترَك صمتًا."
                )
        if not isinstance(self.licensed_axes, tuple) or not self.licensed_axes:
            raise IndependentLineAdmissionError(
                "مصدرٌ لا يأذن في محورِ استقلالٍ واحدٍ لا يُودَع أصلًا؛ "
                "والمحاورُ المأذونةُ تُسمّى."
            )
        seen: set[IndependenceAxis] = set()
        for axis in self.licensed_axes:
            if not isinstance(axis, IndependenceAxis):
                raise IndependentLineAdmissionError(
                    "المحورُ المأذونُ عضوٌ في مفردته المغلقة الثلاثية."
                )
            if axis in seen:
                raise IndependentLineAdmissionError(
                    f"محورٌ مُعادٌ في إذنِ المصدر: {axis.value}."
                )
            seen.add(axis)
        if self.payload_digest is not None and not is_canonical_digest(
            self.payload_digest
        ):
            raise IndependentLineAdmissionError(
                "بصمةُ الحمولة تُودَع بشكلِ بصمةِ `alghanem.canonical_content` "
                "أو لا تُودَع؛ ونصٌّ على غير شكلها إيداعٌ مُدَّعًى."
            )

    @property
    def state(self) -> SourceDepositState:
        """مُودَعٌ متى كانت بصمةُ الحمولة قائمةً بشكلها، وإلّا فغيرُ مُودَع."""

        if self.payload_digest is None:
            return SourceDepositState.غير_مُودَع
        return SourceDepositState.مُودَع

    def licenses(self, axis: IndependenceAxis) -> bool:
        """أيأذن هذا المصدرُ في هذا المحور؟"""

        return axis in self.licensed_axes


_ADMISSION_TOKEN: Final[object] = object()


@dataclass(frozen=True, slots=True)
class AdmittedIndependentLine:
    """خطُّ دليلٍ قُبل مستقلًّا؛ لا يُبنى إلّا بإصدارٍ من البوّابة وحدَها.

    والمحاورُ المنفكّة **تُحسَب** هنا من الخطّ وخطِّ الأساس معًا، فلا يُنقَل
    قبولٌ حُكم على أدلّةٍ إلى أدلّةٍ غيرِها.
    """

    evidence: PhoneticEvidenceItem
    deposit: ExternalSourceDeposit
    baseline: tuple[PhoneticEvidenceItem, ...]
    _token: object | None = field(default=None, repr=False, compare=False)

    def __post_init__(self) -> None:
        if self._token is not _ADMISSION_TOKEN:
            raise IndependentLineAdmissionError(
                "القبولُ يُصدَر من `admit_independent_line` وحدَها؛ وبناءُ "
                "الصنف مباشرةً التفافٌ على البوّابة لا قبول."
            )

    @property
    def broken_axes(self) -> tuple[IndependenceAxis, ...]:
        """المحاورُ التي انفكّ فيها الخطُّ عن خطِّ الأساس بعد التقييس."""

        return _broken_axes(self.evidence, self.baseline)


SESSION_BASELINE_EVIDENCE: Final[tuple[PhoneticEvidenceItem, ...]] = (
    PHONETIC_ECONOMY_CANDIDATE.closure_check.evidence
)

NO_INDEPENDENT_LINE_RESIDUAL_CODE: Final[str] = "NO_INDEPENDENT_LINE_DEPOSITED"

NO_INDEPENDENT_LINE_DEPOSITED: Final[RegisteredResidual] = RegisteredResidual(
    code=NO_INDEPENDENT_LINE_RESIDUAL_CODE,
    statement=(
        "بوّابةُ قبولِ الخطّ المستقلّ مبنيّةٌ مُختبَرة، ولا خطَّ مقبولٌ واحدٌ "
        "مُودَعٌ في هذا المستودع: لا كوربصَ ثانيًا ولا أداةً مقابَلةً بمصدرِ "
        "صوتيّاتٍ مستقلٍّ ولا تعريفَ مقياسٍ منفصلًا. فبطاقةُ الاقتصاد الصوتيّ "
        "تبقى `FAIL` و`DEFER_IN_SCOPE` كما سُجِّلت، والمتغيِّرُ قابليةُ القلب "
        "لا حالُ الدليل؛ ولا يُعدُّ وجودُ الآلة إيداعًا ولا يُقرأ استعدادُها "
        "اجتيازًا"
    ),
    scope=ResidualScope.كل_نتائج_الجلسة,
)

ADMITTED_INDEPENDENT_LINES: Final[tuple[AdmittedIndependentLine, ...]] = ()


def _broken_axes(
    line: PhoneticEvidenceItem,
    baseline: tuple[PhoneticEvidenceItem, ...],
) -> tuple[IndependenceAxis, ...]:
    """المحاورُ التي يخالف فيها الخطُّ كلَّ أدلّةِ الأساس بعد التقييس.

    ومخالفةُ بعضِها لا تكفي: خطٌّ يوافق دليلًا واحدًا من الأساس على محورٍ
    مشتركٌ معه فيه، والاشتراكُ مع واحدٍ اشتراك.
    """

    broken: list[IndependenceAxis] = []
    for axis in IndependenceAxis:
        line_key = cosmetic_axis_key(line.axis_value(axis))
        if all(
            line_key != cosmetic_axis_key(item.axis_value(axis)) for item in baseline
        ):
            broken.append(axis)
    return tuple(broken)


def _validate_baseline(baseline: object) -> tuple[PhoneticEvidenceItem, ...]:
    if not isinstance(baseline, tuple) or not baseline:
        raise IndependentLineAdmissionError(
            "خطُّ الأساس صفُّ أدلّةٍ مُصاغةٍ غيرُ فارغ؛ ولا يُقاس الانفكاكُ " "عن لا شيء."
        )
    for item in baseline:
        if not isinstance(item, PhoneticEvidenceItem):
            raise IndependentLineAdmissionError(
                "كلُّ دليلِ أساسٍ سجلٌّ مُصاغٌ بحقول استقلاله، لا نصٌّ حرّ."
            )
    return baseline


def admit_independent_line(
    line: PhoneticEvidenceItem,
    deposit: ExternalSourceDeposit,
    baseline: tuple[PhoneticEvidenceItem, ...] = SESSION_BASELINE_EVIDENCE,
) -> AdmittedIndependentLine:
    """اقبل خطًّا مستقلًّا حقًّا، أو رُدَّه؛ والانفكاكُ محسوبٌ والمصدرُ مُودَع."""

    if not isinstance(line, PhoneticEvidenceItem):
        raise IndependentLineAdmissionError(
            "الخطُّ المقترَحُ سجلٌّ مُصاغٌ بحقول استقلاله الثلاثة، لا نصٌّ حرّ."
        )
    if not isinstance(deposit, ExternalSourceDeposit):
        raise IndependentLineAdmissionError(
            "المصدرُ سجلُّ إيداعٍ مُصاغ، لا اسمٌ يُذكَر في وصف."
        )
    checked_baseline = _validate_baseline(baseline)
    if any(item.key == line.key for item in checked_baseline):
        raise IndependentLineAdmissionError(
            f"خطٌّ بمفتاحِ دليلٍ قائمٍ ليس خطًّا ثانيًا: {line.key}."
        )
    broken = _broken_axes(line, checked_baseline)
    if not broken:
        raise IndependentLineAdmissionError(
            "الخطُّ المقترَحُ يوافق الأساسَ على المحاور الثلاثة بعد إسقاطِ "
            "التشكيل والتطويل والمسافات وحالةِ الحرف؛ وإعادةُ رسمِ الوصف "
            "نفسِه ليست مصدرًا ثانيًا."
        )
    if IndependenceAxis.أداة in broken and cosmetic_axis_key(
        TOOL_MODULE_PATH
    ) in cosmetic_axis_key(line.tool_identity):
        raise IndependentLineAdmissionError(
            "الأداةُ المُعلَنةُ هي الأداةُ المرفقةُ نفسُها في "
            f"{TOOL_MODULE_PATH}؛ وتسميتُها باسمٍ آخر لا تجعلها أداةً أخرى."
        )
    if deposit.state is not SourceDepositState.مُودَع:
        raise IndependentLineAdmissionError(
            "المصدرُ مُستشهَدٌ به غيرُ مُودَعٍ ببصمةِ حمولته؛ والاستشهادُ "
            "وحدَه دعوى استقلالٍ لا يُعادُ فحصُها."
        )
    unlicensed = tuple(axis for axis in broken if not deposit.licenses(axis))
    if unlicensed:
        raise IndependentLineAdmissionError(
            "محاورُ انفكاكٍ لا يأذن فيها المصدرُ المُودَع: "
            + "، ".join(axis.value for axis in unlicensed)
            + "؛ والانفكاكُ النصّيُّ بلا مصدرٍ يسنده ليس استقلالًا."
        )
    return AdmittedIndependentLine(
        evidence=line,
        deposit=deposit,
        baseline=checked_baseline,
        _token=_ADMISSION_TOKEN,
    )


def _validate_admission(
    admission: object, evidence: tuple[PhoneticEvidenceItem, ...]
) -> AdmittedIndependentLine:
    if not isinstance(admission, AdmittedIndependentLine):
        raise IndependentLineAdmissionError(
            "التمديدُ يجري بخطٍّ أصدرته البوّابةُ، لا بدليلٍ مُمرَّرٍ حولها."
        )
    if admission.baseline != evidence:
        raise IndependentLineAdmissionError(
            "الخطُّ قُبل مقيسًا على أدلّةٍ غيرِ هذه؛ ولا يُنقَل قبولٌ من " "أساسٍ إلى أساس."
        )
    return admission


def closure_check_with_admitted_line(
    check: IndependentClosureCheck,
    admission: AdmittedIndependentLine,
) -> IndependentClosureCheck:
    """فحصٌ جديدٌ بأدلّةِ الأوّل وخطِّه المقبول؛ وحكمُه يُحسَب كما هو بلا تعديل."""

    if not isinstance(check, IndependentClosureCheck):
        raise IndependentLineAdmissionError("التمديدُ يجري على فحصِ إغلاقٍ مُصاغ.")
    validated = _validate_admission(admission, check.evidence)
    return IndependentClosureCheck(evidence=check.evidence + (validated.evidence,))


def candidate_with_admitted_line(
    candidate: PhoneticEconomyCandidate,
    admission: AdmittedIndependentLine,
) -> PhoneticEconomyCandidate:
    """بطاقةٌ جديدةٌ بالخطّ المقبول؛ وبقيّةُ منعِ الإغلاق تسقط متى سقط سببُها.

    ولا تُبنى بطاقةٌ ثانيةٌ بدلَ الأولى: المُسجَّلُ يبقى كما سُجِّل، وهذه
    قيمةٌ جديدةٌ تُعاد، فلا يُمحى نصُّ نتيجةٍ سلبيةٍ بقلبِ حالٍ لاحق.
    """

    if not isinstance(candidate, PhoneticEconomyCandidate):
        raise IndependentLineAdmissionError("التمديدُ يجري على بطاقةِ مرشّحٍ مُصاغة.")
    extended = closure_check_with_admitted_line(candidate.closure_check, admission)
    residuals = candidate.residuals
    if extended.outcome is not ClosureOutcome.FAIL:
        residuals = tuple(
            residual
            for residual in residuals
            if residual.code != CLOSURE_BLOCKING_RESIDUAL_CODE
        )
    return PhoneticEconomyCandidate(
        claim=candidate.claim,
        session_identity=candidate.session_identity,
        closure_check=extended,
        weaker_exhaustion=candidate.weaker_exhaustion,
        tool_readings=candidate.tool_readings,
        residuals=residuals,
    )


_FORBIDDEN_FIELD_TOKENS: Final[tuple[str, ...]] = (
    "verdict",
    "birth",
    "born",
    "certified",
    "freeze",
    "passed",
    "admitted",
    "independent_closure_met",
)


def _assert_no_written_verdict_field() -> None:
    """حارسُ استيراد: لا قبولٌ ولا حكمٌ يتسلّل حقلًا يُكتَب بدل أن يُحسَب."""

    for declaring_type in (ExternalSourceDeposit, AdmittedIndependentLine):
        for declared in fields(declaring_type):
            lowered = declared.name.lower()
            for token in _FORBIDDEN_FIELD_TOKENS:
                if token in lowered:
                    raise RuntimeError(  # pragma: no cover - حارس
                        f"حقلُ قبولٍ تسلّل إلى {declaring_type.__name__}: "
                        f"{declared.name}؛ والقبولُ مُشتَقٌّ لا مكتوب."
                    )


if ADMITTED_INDEPENDENT_LINES:  # pragma: no cover - حارس
    raise RuntimeError(
        "لا خطَّ مستقلًّا مُودَعًا في هذا المستودع؛ وإدراجُ واحدٍ هنا بلا "
        "مصدرٍ مُودَعٍ هو عينُ ما تمنعه البوّابة."
    )
if PHONETIC_ECONOMY_CANDIDATE.closure_check.outcome is not ClosureOutcome.FAIL:
    raise RuntimeError(  # pragma: no cover - حارس
        "بطاقةُ الاقتصاد الصوتيّ المُسجَّلة نتيجةٌ سلبيةٌ فحصُها `FAIL`؛ "
        "وهذه الوحدةُ لا تقلبها."
    )
if PHONETIC_ECONOMY_CANDIDATE.verdict is not ChainVerdict.DEFER_IN_SCOPE:
    raise RuntimeError(  # pragma: no cover - حارس
        "حكمُ البطاقة المُسجَّلة `DEFER_IN_SCOPE`؛ وهذه الوحدةُ بوّابةُ قبولٍ " "لا ترقيةُ حكم."
    )
_assert_no_written_verdict_field()
