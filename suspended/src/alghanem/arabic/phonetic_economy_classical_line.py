"""إيداعُ الجدول التقليديّ خطَّ دليلٍ مستقلًّا، وما ظهر حين حُسِب به فعلًا.

قالت بقيّةُ `INDEPENDENT_CLOSURE_NOT_MET` سببَ الفشل بعينه: جدولُ المخارج
«من ابتكار الجلسة لم يُقابَل بمصدرٍ صوتيّاتٍ مستقلّ». وهذه الوحدةُ تُقابله:
تُودِع جدولَ `classical_makharij_table` — ترتيبَ المخارج التقليديَّ المتواترَ
خارجَ الجلسة — وتُمرِّره ببوّابة `phonetic_economy_independent_line`، فيُقبَل
خطًّا ينفكّ على محورَي **الأداة** و**تعريف المقياس**، فينقلب الفحصُ المحسوب
إلى `PASS` وحكمُ البطاقة المُمدَّدة إلى `CLOSURE_MET_PENDING_AUTHORITY`.

**وأهمُّ ما في هذه الوحدة ليس انقلابَ الفحص، بل ما ظهر حين حُسِب بالجدول
المستقلّ**: اتّجاهُ الدعوى صمد، ومقاديرُ الجلسة انهارت.

```
                  الجلسة      الجدول التقليديّ
النون الساكنة       4.0              2.33
لامُ التعريف        9.5              1.74
```

فالنسبتان تبقيان فوق الواحد — أي إنّ الإظهارَ والقمريَّ أبعدُ مخرجًا فعلًا،
وهو اتّجاهُ الدعوى — لكنّ التباينَ الحادَّ الذي كانت تقوم عليه قوّةُ النتيجة
(٩٫٥ للّام خاصّةً) **يسقط إلى ١٫٧٤**، أي إلى ما يقارب حدَّ اللافرق. ومعنى ذلك
بلا تلطيف: **المقاديرُ كانت أثرَ جدولِ الجلسة نفسِه لا أثرَ ظاهرةٍ في
العربية**؛ وقد سُجِّل ذلك بقيّةَ `SESSION_MAGNITUDES_ARE_TABLE_ARTEFACTS`،
تُحسَب حيًّا بمقارنةِ رقمِ الجلسة بما يُخرجه الجدولُ المُودَعُ الآن، فلا
يُستبدَل رقمٌ برقمٍ ولا يُعدَّل جدولٌ لإجبار تطابق.

**وانقلابُ الفحص لا يُقرأ اجتيازًا للدعوى**: `PASS` يعني أنّ خطَّ الدليل صار
له مصدرُ أداةٍ ومقياسٍ مستقلٌّ، لا أنّ الدعوى صحّت؛ وحكمُ
`CLOSURE_MET_PENDING_AUTHORITY` أقصى ما يُبلَغ — لا ولادةَ، فسلطتُها غيرُ
قائمةٍ في هذا المستودع أصلًا.

**والبطاقةُ المُسجَّلةُ لا تُمسّ**: `PHONETIC_ECONOMY_CANDIDATE` تبقى `FAIL`
و`DEFER_IN_SCOPE` كما سُجِّلت، وهذه بطاقةٌ ثانيةٌ تُعاد قيمةً جديدة. فنتيجةٌ
سلبيةٌ سُجِّلت لا تُمحى بقلبِ حالٍ لاحق.

**وخطٌّ واحدٌ يُقبَل لا خطّان**: لامُ التعريف تُقرأ هنا مقارنةً لا خطَّ دليلٍ
ثانيًا، لأنّ إدخالَها بالجدول نفسِه على ظاهرةٍ مجاورةٍ هو عينُ ما رُدَّت به
الجلسةُ أوّلَ مرّة — أداةٌ واحدةٌ طُبِّقت مرّتين.

**وثلاثُ حدودٍ تبقى قائمةً مُسجَّلةً بقاياها**: محورُ الكوربص ما زال منطبقًا
(الحسابان كلاهما على مجموعاتِ حروفٍ تقليديةٍ لا على قياسٍ في نصّ)، وجعلُ فرقِ
الرتبة مسافةً خطوةُ نمذجةٍ منّا لا قولُ المصدر، والترتيبُ مُودَعٌ بايتاتٍ
مُعادةَ البصمة لا منسوخًا عن طبعةٍ بصفحتها.
"""

from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass
from types import MappingProxyType
from typing import Final

from .classical_makharij_table import (
    CLASSICAL_METRIC_DEFINITION,
    CLASSICAL_ORDERING_IS_NOT_EDITION_CITED_NOTE,
    CLASSICAL_SOURCE_ATTESTATION,
    CLASSICAL_TABLE_DIGEST,
    CLASSICAL_TABLE_MODULE_PATH,
    JAWF_AND_KHAYSHUM_ARE_UNRANKED_NOTE,
    ORDINAL_DISTANCE_IS_OUR_MODELLING_STEP_NOTE,
    classical_lam_f,
    classical_nun_f,
)
from .phonetic_economy_candidate import (
    LAM_TARIF_EVIDENCE,
    NUN_SAKIN_EVIDENCE,
    PHONETIC_ECONOMY_CANDIDATE,
    ChainVerdict,
    ClosureOutcome,
    IndependenceAxis,
    PhoneticEconomyCandidate,
    PhoneticEvidenceItem,
    RegisteredResidual,
    ResidualScope,
)
from .phonetic_economy_independent_line import (
    AdmittedIndependentLine,
    ExternalSourceDeposit,
    IndependentLineAdmissionError,
    admit_independent_line,
    candidate_with_admitted_line,
)

__all__ = [
    "CLASSICAL_EXTENDED_CANDIDATE",
    "CLASSICAL_MAKHARIJ_DEPOSIT",
    "CLASSICAL_NUN_LINE",
    "CLASSICAL_NUN_LINE_ADMISSION",
    "CLASSICAL_TABLE_READINGS",
    "CORPUS_AXIS_STILL_COLLAPSED",
    "MAGNITUDE_COLLAPSE_RESIDUAL_CODE",
    "ORDINAL_DISTANCE_IS_A_MODELLING_STEP",
    "PASS_IS_NOT_A_VERDICT_ON_THE_CLAIM_NOTE",
    "SESSION_MAGNITUDES_ARE_TABLE_ARTEFACTS",
    "ClassicalTableReading",
]

MAGNITUDE_COLLAPSE_RESIDUAL_CODE: Final[str] = "SESSION_MAGNITUDES_ARE_TABLE_ARTEFACTS"

PASS_IS_NOT_A_VERDICT_ON_THE_CLAIM_NOTE: Final[str] = (
    "PASS_IS_NOT_A_VERDICT_ON_THE_CLAIM: انقلابُ الإغلاق إلى `PASS` يعني أنّ "
    "خطَّ الدليل صار له مصدرُ أداةٍ ومقياسٍ مستقلٌّ عن الجلسة، لا أنّ الدعوى "
    "صحّت؛ وأقصى ما يُبلَغ `CLOSURE_MET_PENDING_AUTHORITY`، ولا ولادةَ ولا "
    "تجميدَ ولا `E0`، وسلطةُ الولادة غيرُ قائمةٍ في هذا المستودع"
)


@dataclass(frozen=True, slots=True)
class ClassicalTableReading:
    """قراءةٌ بالجدول المُودَع مقابلَ رقمِ الجلسة؛ والقيمتان تُحسَبان لا تُكتَبان.

    ولا حقلَ حكمٍ هنا: بقاءُ الاتّجاه وانهيارُ المقدار دالّتان على الرقمَين،
    فيُعاد الحسابُ على جدولٍ آخرَ بلا تعديلِ سطر.
    """

    phenomenon_key: str
    session_value: float
    classical_reading: str

    def __post_init__(self) -> None:
        if self.classical_reading not in _CLASSICAL_READINGS:
            raise IndependentLineAdmissionError(
                f"لا حسابَ مُودَعًا بهذا الاسم: {self.classical_reading!r}؛ "
                "وأسماءُ الحساب مُسجَّلةٌ مغلقة."
            )

    @property
    def classical_value(self) -> float:
        """ما يُخرجه الجدولُ التقليديُّ المُودَعُ الآن، لا رقمًا منسوخًا."""

        return _CLASSICAL_READINGS[self.classical_reading]()

    @property
    def direction_preserved(self) -> bool:
        """اتّجاهُ الدعوى: أتبقى النسبةُ فوق الواحد بالجدول المستقلّ؟"""

        return self.classical_value > 1.0

    @property
    def magnitude_ratio(self) -> float:
        """نسبةُ ما أخرجه الجدولُ المستقلُّ إلى ما أعلنته الجلسة."""

        return self.classical_value / self.session_value

    @property
    def reproduces_session_magnitude(self) -> bool:
        """أيُطابق مقدارُ الجدول المستقلّ مقدارَ الجلسة إلى منزلةٍ واحدة؟"""

        return round(self.classical_value, 1) == round(self.session_value, 1)


_CLASSICAL_READINGS: Final[MappingProxyType[str, Callable[[], float]]] = (
    MappingProxyType(
        {
            "classical_nun_f": classical_nun_f,
            "classical_lam_f": classical_lam_f,
        }
    )
)

CLASSICAL_MAKHARIJ_DEPOSIT: Final[ExternalSourceDeposit] = ExternalSourceDeposit(
    source_id="ترتيبُ المخارج التقليديّ المُودَع في `classical_makharij_table`",
    citation=CLASSICAL_SOURCE_ATTESTATION,
    licensed_axes=(IndependenceAxis.أداة, IndependenceAxis.تعريف_المقياس),
    payload_digest=CLASSICAL_TABLE_DIGEST,
)

CLASSICAL_NUN_LINE: Final[PhoneticEvidenceItem] = PhoneticEvidenceItem(
    key="NUN_SAKIN_CLASSICAL_TABLE",
    phenomenon=(
        "النونُ الساكنة: إدغامُها (يرملون) في مقابل إظهارِها (ءهعحغخ)، "
        "مقيسةً على ترتيبِ المخارج التقليديّ لا على جدولِ الجلسة"
    ),
    statistic_name="F",
    statistic_value=classical_nun_f(),
    corpus_identity=NUN_SAKIN_EVIDENCE.corpus_identity,
    tool_identity=CLASSICAL_TABLE_MODULE_PATH,
    metric_definition=CLASSICAL_METRIC_DEFINITION,
)

CLASSICAL_NUN_LINE_ADMISSION: Final[AdmittedIndependentLine] = admit_independent_line(
    CLASSICAL_NUN_LINE, CLASSICAL_MAKHARIJ_DEPOSIT
)

CLASSICAL_TABLE_READINGS: Final[tuple[ClassicalTableReading, ...]] = (
    ClassicalTableReading(
        phenomenon_key=NUN_SAKIN_EVIDENCE.key,
        session_value=NUN_SAKIN_EVIDENCE.statistic_value,
        classical_reading="classical_nun_f",
    ),
    ClassicalTableReading(
        phenomenon_key=LAM_TARIF_EVIDENCE.key,
        session_value=LAM_TARIF_EVIDENCE.statistic_value,
        classical_reading="classical_lam_f",
    ),
)

SESSION_MAGNITUDES_ARE_TABLE_ARTEFACTS: Final[RegisteredResidual] = RegisteredResidual(
    code=MAGNITUDE_COLLAPSE_RESIDUAL_CODE,
    statement=(
        "حُسِبت الدعوى بجدولِ مخارجَ مستقلٍّ عن الجلسة، فصمد اتّجاهُها "
        "وانهارت مقاديرُها: النسبتان تبقيان فوق الواحد — أي إنّ الإظهارَ "
        "والقمريَّ أبعدُ مخرجًا فعلًا — لكنّ ٤٫٠ تصير ٢٫٣٣ و٩٫٥ تصير ١٫٧٤. "
        "والتباينُ الحادُّ الذي قامت عليه قوّةُ النتيجة، ولامُ التعريف خاصّةً، "
        "أثرُ جدولِ الجلسة المُبتكَر لا أثرُ ظاهرةٍ في العربية. ولا يُستبدَل "
        "رقمٌ برقمٍ ولا يُعدَّل جدولٌ لإجبار تطابق؛ والفارقُ يُحسَب حيًّا "
        "بتشغيل الجدولَين"
    ),
    scope=ResidualScope.هذا_المرشّح,
)

CORPUS_AXIS_STILL_COLLAPSED: Final[RegisteredResidual] = RegisteredResidual(
    code="CORPUS_AXIS_STILL_COLLAPSED",
    statement=(
        "انفكّ محورا الأداةِ وتعريفِ المقياس بالجدول المُودَع، ومحورُ الكوربص "
        "باقٍ منطبقًا: الحسابان كلاهما على مجموعاتِ حروفٍ تقليديةٍ مقسومةٍ "
        "سلفًا (يرملون، ءهعحغخ، الشمسيّة، القمريّة)، لا على قياسِ تلازمٍ في "
        "نصّ. فليس في هذا كوربصٌ ثانٍ، ولا يُقرأ `PASS` كأنّه ثلاثةُ انفكاكات"
    ),
    scope=ResidualScope.هذا_المرشّح,
)

ORDINAL_DISTANCE_IS_A_MODELLING_STEP: Final[RegisteredResidual] = RegisteredResidual(
    code="ORDINAL_DISTANCE_IS_OUR_MODELLING_STEP",
    statement=ORDINAL_DISTANCE_IS_OUR_MODELLING_STEP_NOTE
    + " — "
    + CLASSICAL_ORDERING_IS_NOT_EDITION_CITED_NOTE
    + " — "
    + JAWF_AND_KHAYSHUM_ARE_UNRANKED_NOTE,
    scope=ResidualScope.هذا_المرشّح,
)


def _extended_candidate() -> PhoneticEconomyCandidate:
    upgraded = candidate_with_admitted_line(
        PHONETIC_ECONOMY_CANDIDATE, CLASSICAL_NUN_LINE_ADMISSION
    )
    added: tuple[RegisteredResidual, ...] = (
        CORPUS_AXIS_STILL_COLLAPSED,
        ORDINAL_DISTANCE_IS_A_MODELLING_STEP,
    )
    if any(
        not reading.reproduces_session_magnitude for reading in CLASSICAL_TABLE_READINGS
    ):
        added = (SESSION_MAGNITUDES_ARE_TABLE_ARTEFACTS,) + added
    return PhoneticEconomyCandidate(
        claim=upgraded.claim,
        session_identity=upgraded.session_identity,
        closure_check=upgraded.closure_check,
        weaker_exhaustion=upgraded.weaker_exhaustion,
        tool_readings=upgraded.tool_readings,
        residuals=upgraded.residuals + added,
    )


CLASSICAL_EXTENDED_CANDIDATE: Final[PhoneticEconomyCandidate] = _extended_candidate()


if CLASSICAL_NUN_LINE_ADMISSION.broken_axes != (
    IndependenceAxis.أداة,
    IndependenceAxis.تعريف_المقياس,
):  # pragma: no cover - حارس
    raise RuntimeError(
        "الخطُّ المُودَعُ ينفكّ على محورَي الأداةِ وتعريفِ المقياس وحدَهما؛ "
        "ومحورُ الكوربص باقٍ منطبقًا، فلا يُقرأ انفكاكًا ثالثًا."
    )
if CLASSICAL_EXTENDED_CANDIDATE.closure_check.outcome is not ClosureOutcome.PASS:
    raise RuntimeError(  # pragma: no cover - حارس
        "الخطُّ المُودَعُ يقلب الفحصَ المحسوبَ إلى `PASS`؛ وبقاؤه `FAIL` "
        "يعني أنّ الإيداعَ لم يُقرأ أصلًا."
    )
if (
    CLASSICAL_EXTENDED_CANDIDATE.verdict
    is not ChainVerdict.CLOSURE_MET_PENDING_AUTHORITY
):  # pragma: no cover - حارس
    raise RuntimeError("أقصى ما تبلغه البطاقةُ المُمدَّدة انتظارُ سلطةٍ لم تُبنَ؛ ولا ولادةَ.")
if PHONETIC_ECONOMY_CANDIDATE.closure_check.outcome is not ClosureOutcome.FAIL:
    raise RuntimeError(  # pragma: no cover - حارس
        "البطاقةُ المُسجَّلةُ نتيجةٌ سلبيةٌ لا تُمسّ؛ وهذه الوحدةُ تُعيد " "قيمةً جديدةً ولا تُبدّلها."
    )
