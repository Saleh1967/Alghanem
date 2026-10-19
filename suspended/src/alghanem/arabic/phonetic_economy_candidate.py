"""تسجيلُ أقوى مرشّحٍ في جلسة GFLK، وحكمُ سلسلة G0 عليه فعلًا: `DEFER_IN_SCOPE`.

**ما جرى، بلا تلطيف**: جلسةٌ خارجية (جبرُ الحامل/الحالة على نصّ المصحف) أنتجت
نحو ١٣٠ نتيجةً إحصائية. وأقواها — «الإدغام يقع حين تصغر مسافةُ المخرج بين
الساكن والحرف التالي، والإظهار حين تكبر» — أُجري على سلسلة G0 حرفيًّا
(BirthQuery ← Evidence ← LicensedWeakerExhaustion ← IndependentClosureCheck ←
BirthVerdict) **بوّابةً فعلية لا وصفًا**. والنتيجةُ الفعلية: **فشلَ عند
`IndependentClosureCheck`**. فالدليلان (النون الساكنة: F=4.0؛ ولامُ التعريف
الشمسيّة/القمريّة: F=9.5) خرجا من **الكوربص الواحد نفسِه، والأداةِ المُبتكَرة
نفسِها، وتعريفِ المقياس نفسِه**، مُطبَّقًا مرّتين على ظاهرتَين صوتيّتَين
متجاورتَين — لا خطَّي دليلٍ مستقلَّين. فالحكم: `DEFER_IN_SCOPE`.

**وهذه الوحدةُ تسجيلٌ لنتيجةٍ سلبية، لا ادّعاءُ `BirthCandidate`**، على منوال
`distributional_probe_report.py`. وقيمتُها شيئان: صدقُ النتيجة السلبية، وشكلُ
`IndependentClosureCheck` القابلُ لإعادة الاستعمال في فحص مرشّحين لاحقين من
هذه الجلسة أو من غيرها.

**والفحصُ محسوبٌ لا مكتوب**: `IndependentClosureCheck.outcome` يُشتقُّ من
الأدلّة نفسِها — `FAIL` حين يجتمع `same_corpus` و`same_tool` و
`same_metric_definition` ثلاثتُها، و`PASS` حين ينفكّ واحدٌ منها. فإن زُوِّد
لاحقًا دليلٌ من كوربصٍ آخر أو أداةٍ أخرى أو تعريفِ مقياسٍ آخر، أُعيد تشغيلُ
الفحص نفسِه بلا تعديلِ سطرٍ واحد، ولا حكمَ مُثبَّتًا في حقلٍ يُنقَض.

**والرفضُ بنيويٌّ لا تحذيرٌ في وثيقة**، على منوال `SectionExcerpt` الذي يرفض
أيَّ موضعٍ فوق `موضع_غير_متحقق`: لا وجودَ لصنفِ `CertifiedPhoneticEconomyFinding`
إلّا بإصدارٍ من `certify_phonetic_economy_candidate`، وهذه تردّ ما دامت بقيّةُ
`INDEPENDENT_CLOSURE_NOT_MET` قائمة. فلا يمكن بنيويًّا تسميةُ هذا الكائن
`DEFER_IN_SCOPE` نتيجةً مُصدَّقة.

**وبقيّتان اثنتان لا واحدة**: مع `INDEPENDENT_CLOSURE_NOT_MET` تُسجَّل
`TOOL_IS_APPROXIMATE_RECONSTRUCTION`، فالأداةُ المرفقة في
`phonetic_economy_tool.py` إعادةُ بناءٍ مُبسَّطة لأداةِ الجلسة الأصلية القائمة
على تباعد KL، ومخرجُها ٣٫٤٣ و٩٫٩٦ لا ٤٫٠ و٩٫٥. والفارقُ **يُحسَب حيًّا** هنا
بمقارنة رقمِ الجلسة المُسجَّل بما تُخرجه الأداةُ فعلًا، فلا يُستبدَل الرقمُ
المُبسَّط برقم الجلسة، ولا يُعدَّل الجدولُ لإجبار التطابق، ولا تُبنى بطاقةٌ
أصلًا وفيها فارقٌ بلا بقيّتِه.

**وتعميمٌ مُسجَّلٌ بقيّةً لا تعليقًا**: نتائجُ الجلسة كلُّها — نحو ١٣٠ — تشترك
في أصلِ الكوربصِ الواحد والأداةِ الواحدة، فلا يُفترَض في واحدةٍ منها اجتيازُ
الإغلاق المستقلّ بلا مصدرٍ أو أداةٍ أو تعريفِ مقياسٍ منفصلٍ حقًّا. وهذه
الوحدةُ **المثالُ المشغول، لا الحالةُ الخاصّة**.

**ولا سلطةَ لهذه الوحدة**: لا ترقّيَ إلى AIM-K3، ولا بوّابةَ تشغيلٍ جديدة (ولا
واحدةَ قائمةً بعدُ بحسب `CONSTITUTION.md`)، ولا ولادةَ ولا تجميدَ ولا `E0`؛
ولا يقرؤها `IndependentClosureGate` ولا `BirthVerdictGate`، ولا تدخل في
`BirthExperimentSpecification`. ولا عنوانَ نجاحٍ فيها أصلًا.
"""

from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass, field, fields
from enum import Enum
from math import isfinite
from types import MappingProxyType
from typing import Final

from .phonetic_economy_tool import (
    TOOL_IS_AN_APPROXIMATE_RECONSTRUCTION_NOTE,
    TOOL_MODULE_PATH,
    TOOL_TABLE_IS_SELF_INVENTED_NOTE,
    compute_lam_f,
    compute_nun_f,
)

__all__ = [
    "CLOSURE_BLOCKING_RESIDUAL_CODE",
    "GFLK_SESSION_FINDINGS_SHARE_ONE_ORIGIN",
    "GFLK_SESSION_IDENTITY",
    "INDEPENDENT_CLOSURE_NOT_MET",
    "LAM_TARIF_EVIDENCE",
    "NOT_A_GATE_NOTE",
    "NUN_SAKIN_EVIDENCE",
    "PHONETIC_ECONOMY_CANDIDATE",
    "PHONETIC_ECONOMY_CLAIM",
    "REGISTERED_RESIDUALS",
    "TOOL_IS_APPROXIMATE_RECONSTRUCTION",
    "TOOL_RECONSTRUCTION_RESIDUAL_CODE",
    "CertifiedPhoneticEconomyFinding",
    "ChainVerdict",
    "ClosureOutcome",
    "IndependenceAxis",
    "IndependentClosureCheck",
    "LicensedWeakerExhaustion",
    "PhoneticEconomyCandidate",
    "PhoneticEconomyRegistrationError",
    "PhoneticEvidenceItem",
    "RegisteredResidual",
    "ResidualScope",
    "ToolReconstructionReading",
    "WeakerModelAttempt",
    "WeakerModelOutcome",
    "certify_phonetic_economy_candidate",
    "registered_residual_for",
]


class PhoneticEconomyRegistrationError(ValueError):
    """رُفض مدخلٌ خارج شرطه؛ ولا يُحمَل على أقرب حالةٍ مقبولة."""


class IndependenceAxis(Enum):
    """محاورُ الاستقلال الثلاثة؛ مفردةٌ مغلقة، ولا رابعَ يُضاف بالوصف."""

    كوربص = "كوربص"
    أداة = "أداة"
    تعريف_المقياس = "تعريف_المقياس"


class WeakerModelOutcome(Enum):
    """نتيجةُ نموذجٍ أضعفَ واحد؛ ثنائيةٌ مغلقة، ولا حالةَ ثالثةَ ملتبسة."""

    فشل = "فشل"
    فسّر_البقيّة = "فسّر_البقيّة"


class ClosureOutcome(Enum):
    """حكمُ الإغلاق المستقلّ؛ ثنائيٌّ وكلا فرعَيه قابلٌ للبلوغ بالحساب."""

    PASS = "PASS"
    FAIL = "FAIL"


class ChainVerdict(Enum):
    """حكمُ السلسلة؛ ولا عضوَ فيه اسمُه «وُلِد» ولا «مُصدَّق».

    حتى على فرع `PASS` لا يصير الحكمُ ولادةً: سلطةُ الولادة غيرُ قائمةٍ في
    هذا المستودع، فأقصى ما يُقال «انفكّ الإغلاقُ وبقي الحكمُ موقوفًا على
    سلطةٍ لم تُبنَ».
    """

    DEFER_IN_SCOPE = "DEFER_IN_SCOPE"
    CLOSURE_MET_PENDING_AUTHORITY = "CLOSURE_MET_PENDING_AUTHORITY"


class ResidualScope(Enum):
    """مدى البقيّة: هذا المرشّحُ وحدَه، أم نتائجُ الجلسة كلُّها."""

    هذا_المرشّح = "هذا_المرشّح"
    كل_نتائج_الجلسة = "كل_نتائج_الجلسة"


CLOSURE_BLOCKING_RESIDUAL_CODE: Final[str] = "INDEPENDENT_CLOSURE_NOT_MET"
TOOL_RECONSTRUCTION_RESIDUAL_CODE: Final[str] = "TOOL_IS_APPROXIMATE_RECONSTRUCTION"
SESSION_ORIGIN_RESIDUAL_CODE: Final[str] = "GFLK_SESSION_FINDINGS_SHARE_ONE_ORIGIN"

GFLK_SESSION_IDENTITY: Final[str] = (
    "جلسةُ GFLK الخارجية: عملُ جبرِ الحامل/الحالة على نصّ المصحف، أنتجت نحو "
    "١٣٠ نتيجةً إحصائية؛ ولم يُزوَّد لها سجلٌّ مُجمَّدٌ ولا بصمةُ إصدار"
)

PHONETIC_ECONOMY_CLAIM: Final[str] = (
    "الإدغامُ يقع حين تصغر مسافةُ المخرج بين الساكن والحرف التالي له، "
    "والإظهارُ حين تكبر"
)

NOT_A_GATE_NOTE: Final[str] = (
    "PHONETIC_ECONOMY_REGISTRATION_IS_NOT_A_GATE: تسجيلٌ لا بوّابة؛ لا ولادةَ "
    "ولا تجميدَ ولا `E0`، ولا يقرؤه `IndependentClosureGate` ولا "
    "`BirthVerdictGate`، ولا يدخل في `BirthExperimentSpecification`، ولا "
    "يُرقّي AIM-K3 ولا يفتح بوّابةَ تشغيلٍ لم تُبنَ"
)


def _require_non_blank(value: object, label: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise PhoneticEconomyRegistrationError(f"{label} نصٌّ غير فارغ؛ ولا يُترَك صمتًا.")
    return value


def _require_finite(value: object, label: str) -> float:
    if isinstance(value, bool) or not isinstance(value, int | float):
        raise PhoneticEconomyRegistrationError(f"{label} عددٌ مقيس، لا وصفٌ ولا راية.")
    number = float(value)
    if not isfinite(number):
        raise PhoneticEconomyRegistrationError(f"{label} عددٌ منتهٍ؛ ولا يُسجَّل لا-عدد.")
    return number


@dataclass(frozen=True, slots=True)
class PhoneticEvidenceItem:
    """دليلٌ واحد، وحقولُ استقلالِه الثلاثة مُلزَمةٌ لا تُطوى.

    الحذفُ هو عينُ العطب الذي يحرسه هذا الصنف: دليلٌ بلا كوربصٍ مُسمًّى أو
    أداةٍ مُسمّاةٍ أو تعريفِ مقياسٍ مكتوبٍ يُخفي اشتراكَه مع غيره، فيبدو
    الخطَّان المتطابقان خطَّين مستقلَّين. فكلُّ واحدٍ منها يُرَدُّ فارغًا.
    """

    key: str
    phenomenon: str
    statistic_name: str
    statistic_value: float
    corpus_identity: str
    tool_identity: str
    metric_definition: str

    def __post_init__(self) -> None:
        _require_non_blank(self.key, "مفتاحُ الدليل")
        _require_non_blank(self.phenomenon, "الظاهرةُ المقيسة")
        _require_non_blank(self.statistic_name, "اسمُ الإحصاءة")
        _require_finite(self.statistic_value, "قيمةُ الإحصاءة")
        _require_non_blank(self.corpus_identity, "هويّةُ الكوربص")
        _require_non_blank(self.tool_identity, "هويّةُ الأداة")
        _require_non_blank(self.metric_definition, "تعريفُ المقياس")

    def axis_value(self, axis: IndependenceAxis) -> str:
        """قيمةُ الدليل على محورِ استقلالٍ واحد؛ ومحورٌ خارجَ المفردة يُرَدّ."""

        if axis is IndependenceAxis.كوربص:
            return self.corpus_identity
        if axis is IndependenceAxis.أداة:
            return self.tool_identity
        if axis is IndependenceAxis.تعريف_المقياس:
            return self.metric_definition
        raise PhoneticEconomyRegistrationError(
            "محورُ الاستقلال عضوٌ في مفردته المغلقة الثلاثية."
        )


@dataclass(frozen=True, slots=True)
class WeakerModelAttempt:
    """محاولةُ نموذجٍ أضعف، ونتيجتُها من مفردةٍ ثنائيةٍ مغلقة."""

    model_name: str
    outcome: WeakerModelOutcome

    def __post_init__(self) -> None:
        _require_non_blank(self.model_name, "اسمُ النموذج الأضعف")
        if not isinstance(self.outcome, WeakerModelOutcome):
            raise PhoneticEconomyRegistrationError(
                "نتيجةُ النموذج الأضعف عضوٌ في مفردتها المغلقة."
            )


@dataclass(frozen=True, slots=True)
class LicensedWeakerExhaustion:
    """استنفادُ النماذج الأضعف؛ وبقاءُ البقيّة مُشتقٌّ من النتائج لا مكتوب."""

    attempts: tuple[WeakerModelAttempt, ...]

    def __post_init__(self) -> None:
        if not isinstance(self.attempts, tuple) or not self.attempts:
            raise PhoneticEconomyRegistrationError(
                "استنفادٌ بلا محاولةٍ واحدةٍ ليس استنفادًا؛ وتُسمّى النماذجُ "
                "المُجرَّبةُ بأسمائها."
            )
        seen: set[str] = set()
        for attempt in self.attempts:
            if not isinstance(attempt, WeakerModelAttempt):
                raise PhoneticEconomyRegistrationError("كلُّ محاولةٍ سجلٌّ مُصاغ، لا نصٌّ حرّ.")
            if attempt.model_name in seen:
                raise PhoneticEconomyRegistrationError(
                    f"نموذجٌ أضعفُ مُعادٌ باسمه نفسِه ليس محاولةً ثانية: "
                    f"{attempt.model_name}."
                )
            seen.add(attempt.model_name)

    @property
    def residual_survives(self) -> bool:
        """تبقى البقيّةُ إن فشل كلُّ نموذجٍ أضعفَ جُرِّب؛ وواحدٌ يُفسِّرها يُسقطها."""

        return all(
            attempt.outcome is WeakerModelOutcome.فشل for attempt in self.attempts
        )


@dataclass(frozen=True, slots=True)
class IndependentClosureCheck:
    """فحصُ الإغلاق المستقلّ، محسوبًا من الأدلّة نفسِها في كلّ نداء.

    لا حقلَ حكمٍ هنا: `outcome` دالّةٌ على محتوى الأدلّة، فيُعاد تشغيلُ الفحص
    على أدلّةٍ جديدةٍ بلا تعديلِ سطر، ولا يُحفَظ `FAIL` مُثبَّتًا في حقلٍ
    يُخالف محتواه لاحقًا.
    """

    evidence: tuple[PhoneticEvidenceItem, ...]

    def __post_init__(self) -> None:
        if not isinstance(self.evidence, tuple) or len(self.evidence) < 2:
            raise PhoneticEconomyRegistrationError(
                "الإغلاقُ المستقلُّ سؤالٌ عن العلاقة بين خطَّي دليلٍ فأكثر؛ "
                "فدليلٌ واحدٌ لا يُفحَص استقلالُه أصلًا."
            )
        seen: set[str] = set()
        for item in self.evidence:
            if not isinstance(item, PhoneticEvidenceItem):
                raise PhoneticEconomyRegistrationError(
                    "كلُّ دليلٍ سجلٌّ مُصاغٌ بحقول استقلالِه، لا نصٌّ حرّ."
                )
            if item.key in seen:
                raise PhoneticEconomyRegistrationError(
                    f"دليلٌ مُعادٌ بمفتاحه نفسِه ليس دليلًا ثانيًا: {item.key}."
                )
            seen.add(item.key)

    def _shares(self, axis: IndependenceAxis) -> bool:
        first = self.evidence[0].axis_value(axis)
        return all(item.axis_value(axis) == first for item in self.evidence)

    @property
    def same_corpus(self) -> bool:
        """أخرجت الأدلّةُ كلُّها من كوربصٍ واحد؟"""

        return self._shares(IndependenceAxis.كوربص)

    @property
    def same_tool(self) -> bool:
        """أخرجت الأدلّةُ كلُّها من أداةٍ واحدة؟"""

        return self._shares(IndependenceAxis.أداة)

    @property
    def same_metric_definition(self) -> bool:
        """أخرجت الأدلّةُ كلُّها من تعريفِ مقياسٍ واحد؟"""

        return self._shares(IndependenceAxis.تعريف_المقياس)

    @property
    def collapsed_axes(self) -> tuple[IndependenceAxis, ...]:
        """المحاورُ التي انطبقت عليها الأدلّةُ كلُّها؛ فالفشلُ مُسمًّى لا مُبهَم."""

        return tuple(axis for axis in IndependenceAxis if self._shares(axis))

    @property
    def outcome(self) -> ClosureOutcome:
        """`FAIL` حين تنطبق المحاورُ الثلاثةُ جميعًا، و`PASS` حين ينفكّ واحد."""

        if len(self.collapsed_axes) == len(IndependenceAxis):
            return ClosureOutcome.FAIL
        return ClosureOutcome.PASS


@dataclass(frozen=True, slots=True)
class ToolReconstructionReading:
    """قراءةُ فارقِ الأداة: رقمُ الجلسة، وما تُخرجه الأداةُ المرفقةُ فعلًا.

    القيمةُ المُعادُ بناؤها **تُحسَب عند القراءة** بتشغيل الأداة نفسِها، فلا
    يُكتَب الفارقُ يدويًّا ولا يُخفى بتحرير رقمٍ في جدول.
    """

    evidence_key: str
    session_value: float
    reconstruction: str

    def __post_init__(self) -> None:
        _require_non_blank(self.evidence_key, "مفتاحُ الدليل")
        _require_finite(self.session_value, "رقمُ الجلسة")
        if self.reconstruction not in _RECONSTRUCTIONS:
            raise PhoneticEconomyRegistrationError(
                f"لا حسابَ مُرفَقًا بهذا الاسم: {self.reconstruction!r}؛ "
                "وأسماءُ الحساب مُسجَّلةٌ مغلقة."
            )

    @property
    def reconstructed_value(self) -> float:
        """ما تُخرجه الأداةُ المرفقةُ الآن، لا رقمًا منسوخًا في حقل."""

        return _RECONSTRUCTIONS[self.reconstruction]()

    @property
    def reproduces_session_value(self) -> bool:
        """أيُطابق الحسابُ المُرفَقُ رقمَ الجلسة إلى منزلتَين؟"""

        return round(self.reconstructed_value, 2) == round(self.session_value, 2)


_RECONSTRUCTIONS: Final[MappingProxyType[str, Callable[[], float]]] = MappingProxyType(
    {
        "compute_nun_f": compute_nun_f,
        "compute_lam_f": compute_lam_f,
    }
)


@dataclass(frozen=True, slots=True)
class RegisteredResidual:
    """بقيّةٌ مُسمّاةٌ بمداها؛ كائنٌ يُعدّ ويُفحَص، لا تعليقٌ في وثيقة."""

    code: str
    statement: str
    scope: ResidualScope

    def __post_init__(self) -> None:
        _require_non_blank(self.code, "رمزُ البقيّة")
        _require_non_blank(self.statement, "نصُّ البقيّة")
        if not isinstance(self.scope, ResidualScope):
            raise PhoneticEconomyRegistrationError("مدى البقيّة عضوٌ في مفردته المغلقة.")


INDEPENDENT_CLOSURE_NOT_MET: Final[RegisteredResidual] = RegisteredResidual(
    code=CLOSURE_BLOCKING_RESIDUAL_CODE,
    statement=(
        "تكرارُ الكوربصِ الواحد والأداةِ الواحدة وتعريفِ المقياس الواحد على "
        "ظاهرتَين صوتيّتَين متجاورتَين ليس استقلالًا: هو خطُّ دليلٍ واحدٌ "
        "طُبِّق مرّتين. وقانونُ `NoBedrockWithoutRecurringDirayaSurvival` يجعل "
        "كلَّ تطبيقٍ مستقلٍّ جديد — كوربصًا آخر أو أداةً أخرى أو نطاقًا آخر — "
        "فرصةَ هزيمةٍ جديدة، والتكرارُ داخلَ التطبيق الواحد ليس منها. وجدولُ "
        "المخارجِ نفسُه من ابتكار الجلسة لم يُقابَل بمصدرٍ صوتيّاتٍ مستقلّ، "
        "فحكمُ السلسلة `DEFER_IN_SCOPE` لا تمريرٌ مشروط"
    ),
    scope=ResidualScope.هذا_المرشّح,
)

TOOL_IS_APPROXIMATE_RECONSTRUCTION: Final[RegisteredResidual] = RegisteredResidual(
    code=TOOL_RECONSTRUCTION_RESIDUAL_CODE,
    statement=TOOL_IS_AN_APPROXIMATE_RECONSTRUCTION_NOTE
    + " — "
    + TOOL_TABLE_IS_SELF_INVENTED_NOTE,
    scope=ResidualScope.هذا_المرشّح,
)

GFLK_SESSION_FINDINGS_SHARE_ONE_ORIGIN: Final[RegisteredResidual] = RegisteredResidual(
    code=SESSION_ORIGIN_RESIDUAL_CODE,
    statement=(
        "نتائجُ جلسة GFLK كلُّها — نحو ١٣٠ — تشترك في أصلٍ واحد: كوربصٌ واحد "
        "وأداةٌ واحدة من ابتكار الجلسة. فلا يُفترَض في واحدةٍ منها اجتيازُ "
        "`IndependentClosure` ما لم يُزوَّد لها مصدرٌ أو أداةٌ أو تعريفُ "
        "مقياسٍ منفصلٌ حقًّا؛ وهذا المرشّحُ — أقواها — هو المثالُ المشغول، لا "
        "الحالةُ الخاصّة المستثناة"
    ),
    scope=ResidualScope.كل_نتائج_الجلسة,
)


_CERTIFICATION_TOKEN: Final[object] = object()


@dataclass(frozen=True, slots=True)
class PhoneticEconomyCandidate:
    """بطاقةُ المرشّح: الدعوى، والأدلّة، والاستنفاد، والبقايا — وحكمٌ مُشتَقّ.

    ولا يُبنى هذا الصنفُ أصلًا في حالتَين: فحصٌ فاشلٌ بلا بقيّةِ
    `INDEPENDENT_CLOSURE_NOT_MET`، وفارقُ أداةٍ قائمٌ بلا بقيّةِ
    `TOOL_IS_APPROXIMATE_RECONSTRUCTION`. فالبقيّةُ شرطُ وجودٍ لا تحسينُ توثيق.
    """

    claim: str
    session_identity: str
    closure_check: IndependentClosureCheck
    weaker_exhaustion: LicensedWeakerExhaustion
    tool_readings: tuple[ToolReconstructionReading, ...]
    residuals: tuple[RegisteredResidual, ...]

    def __post_init__(self) -> None:
        _require_non_blank(self.claim, "نصُّ الدعوى")
        _require_non_blank(self.session_identity, "هويّةُ الجلسة")
        if not isinstance(self.closure_check, IndependentClosureCheck):
            raise PhoneticEconomyRegistrationError(
                "فحصُ الإغلاق المستقلّ سجلٌّ مُصاغٌ يُحسَب، لا حكمٌ يُكتَب."
            )
        if not isinstance(self.weaker_exhaustion, LicensedWeakerExhaustion):
            raise PhoneticEconomyRegistrationError(
                "استنفادُ النماذج الأضعف سجلٌّ مُصاغ، لا رايةٌ تُرفَع."
            )
        if not isinstance(self.tool_readings, tuple):
            raise PhoneticEconomyRegistrationError("قراءاتُ الأداة صفٌّ مُصاغ.")
        for reading in self.tool_readings:
            if not isinstance(reading, ToolReconstructionReading):
                raise PhoneticEconomyRegistrationError(
                    "كلُّ قراءةِ أداةٍ سجلٌّ مُصاغٌ يُحسَب عند قراءته."
                )
        if not isinstance(self.residuals, tuple) or not self.residuals:
            raise PhoneticEconomyRegistrationError(
                "مرشّحٌ بلا بقيّةٍ مُسمّاةٍ واحدة؛ وحدودُ التسجيل تُسمّى ولا " "تُترَك للقارئ."
            )
        seen: set[str] = set()
        for residual in self.residuals:
            if not isinstance(residual, RegisteredResidual):
                raise PhoneticEconomyRegistrationError(
                    "كلُّ بقيّةٍ كائنٌ مُسمًّى بمداه، لا سطرُ تعليق."
                )
            if residual.code in seen:
                raise PhoneticEconomyRegistrationError(
                    f"بقيّةٌ مُعادةٌ برمزها نفسِه: {residual.code}."
                )
            seen.add(residual.code)
        if self.closure_check.outcome is ClosureOutcome.FAIL:
            if CLOSURE_BLOCKING_RESIDUAL_CODE not in seen:
                raise PhoneticEconomyRegistrationError(
                    "فحصُ الإغلاق فشل ولا بقيّةَ `INDEPENDENT_CLOSURE_NOT_MET` "
                    "على البطاقة؛ وفشلٌ بلا بقيّتِه تلطيفٌ لا تسجيل."
                )
        elif CLOSURE_BLOCKING_RESIDUAL_CODE in seen:
            raise PhoneticEconomyRegistrationError(
                "بقيّةُ `INDEPENDENT_CLOSURE_NOT_MET` مكتوبةٌ وفحصُ الإغلاق "
                "لم يفشل؛ والبقايا تُطابق المحسوبَ ولا تُكتَب على خلافه."
            )
        if any(not reading.reproduces_session_value for reading in self.tool_readings):
            if TOOL_RECONSTRUCTION_RESIDUAL_CODE not in seen:
                raise PhoneticEconomyRegistrationError(
                    "الأداةُ المرفقةُ تُخرج غيرَ رقمِ الجلسة ولا بقيّةَ "
                    "`TOOL_IS_APPROXIMATE_RECONSTRUCTION` على البطاقة؛ "
                    "واستعمالُ الرقم المُبسَّط مكانَ رقم الجلسة تزوير."
                )

    @property
    def residual_codes(self) -> tuple[str, ...]:
        """رموزُ البقايا بترتيب تسجيلها."""

        return tuple(residual.code for residual in self.residuals)

    @property
    def is_closure_blocked(self) -> bool:
        """أقائمةٌ بقيّةُ منعِ الإغلاق؟ وهي شرطُ الرفضِ في التصديق."""

        return CLOSURE_BLOCKING_RESIDUAL_CODE in self.residual_codes

    @property
    def unreproduced_tool_readings(self) -> tuple[ToolReconstructionReading, ...]:
        """القراءاتُ التي لم تُطابق رقمَ الجلسة؛ الفارقُ مُسمًّى لا مطويّ."""

        return tuple(
            reading
            for reading in self.tool_readings
            if not reading.reproduces_session_value
        )

    @property
    def verdict(self) -> ChainVerdict:
        """حكمُ السلسلة، مُشتقًّا من الفحص المحسوب وحدَه لا من حقلٍ يُكتَب."""

        if self.closure_check.outcome is ClosureOutcome.FAIL:
            return ChainVerdict.DEFER_IN_SCOPE
        return ChainVerdict.CLOSURE_MET_PENDING_AUTHORITY


@dataclass(frozen=True, slots=True)
class CertifiedPhoneticEconomyFinding:
    """نتيجةٌ مُصدَّقة؛ لا تُبنى إلّا بإصدارٍ من الدالّة المُخوَّلة وحدَها.

    وجودُ هذا الصنف منفصلًا هو الرفضُ البنيويّ بعينه: بطاقةُ `DEFER_IN_SCOPE`
    ليست من هذا النوع أصلًا، فلا تُسمّى نتيجةً مُصدَّقةً بنقلِ حقلٍ ولا
    بتجاهلِ تحذيرٍ في وثيقة.
    """

    candidate: PhoneticEconomyCandidate
    _token: object | None = field(default=None, repr=False, compare=False)

    def __post_init__(self) -> None:
        if self._token is not _CERTIFICATION_TOKEN:
            raise PhoneticEconomyRegistrationError(
                "التصديقُ يُصدَر من `certify_phonetic_economy_candidate` وحدَها؛ "
                "وبناءُ الصنف مباشرةً التفافٌ على البوّابة لا تصديق."
            )
        if not isinstance(self.candidate, PhoneticEconomyCandidate):
            raise PhoneticEconomyRegistrationError("المُصدَّقُ بطاقةُ مرشّحٍ مُصاغة.")


def certify_phonetic_economy_candidate(
    candidate: PhoneticEconomyCandidate,
) -> CertifiedPhoneticEconomyFinding:
    """صدِّق المرشّحَ، أو رُدَّ ما دامت بقيّةُ منعِ الإغلاق قائمة."""

    if not isinstance(candidate, PhoneticEconomyCandidate):
        raise PhoneticEconomyRegistrationError("التصديقُ يجري على بطاقةِ مرشّحٍ مُصاغة.")
    if candidate.closure_check.outcome is ClosureOutcome.FAIL:
        raise PhoneticEconomyRegistrationError(
            "فحصُ الإغلاق المستقلّ فاشلٌ محسوبًا؛ ولا تُصدَّق بطاقةٌ حكمُها "
            "`DEFER_IN_SCOPE`. " + INDEPENDENT_CLOSURE_NOT_MET.statement
        )
    if candidate.is_closure_blocked:
        raise PhoneticEconomyRegistrationError(
            "بقيّةُ `INDEPENDENT_CLOSURE_NOT_MET` قائمةٌ على البطاقة؛ ولا "
            "تُرفَع بالتصديق، بل بدليلٍ من مصدرٍ أو أداةٍ أو تعريفِ مقياسٍ "
            "منفصلٍ حقًّا."
        )
    return CertifiedPhoneticEconomyFinding(
        candidate=candidate, _token=_CERTIFICATION_TOKEN
    )


_SESSION_CORPUS: Final[str] = (
    "نصُّ المصحف كما استُعمل في جلسة GFLK؛ كوربصٌ واحدٌ لم تُسمَّ روايتُه ولا "
    "إصدارُه الرقميّ ولا بصمتُه"
)

_SESSION_METRIC: Final[str] = (
    "مسافةُ المخرج بين الساكن والحرف التالي، محسوبةً على ترقيمِ المخارج "
    "التسعة المُبتكَر في الجلسة، ثمّ نسبةُ متوسّطِ المجموعة البعيدة إلى "
    "متوسّطِ المجموعة القريبة"
)


NUN_SAKIN_EVIDENCE: Final[PhoneticEvidenceItem] = PhoneticEvidenceItem(
    key="NUN_SAKIN",
    phenomenon="النونُ الساكنة: إدغامُها (يرملون) في مقابل إظهارِها (ءهعحغخ)",
    statistic_name="F",
    statistic_value=4.0,
    corpus_identity=_SESSION_CORPUS,
    tool_identity=TOOL_MODULE_PATH,
    metric_definition=_SESSION_METRIC,
)

LAM_TARIF_EVIDENCE: Final[PhoneticEvidenceItem] = PhoneticEvidenceItem(
    key="LAM_TARIF",
    phenomenon="لامُ التعريف: الحروفُ الشمسيّة في مقابل القمريّة",
    statistic_name="F",
    statistic_value=9.5,
    corpus_identity=_SESSION_CORPUS,
    tool_identity=TOOL_MODULE_PATH,
    metric_definition=_SESSION_METRIC,
)

_CLOSURE_CHECK: Final[IndependentClosureCheck] = IndependentClosureCheck(
    evidence=(NUN_SAKIN_EVIDENCE, LAM_TARIF_EVIDENCE)
)

_WEAKER_EXHAUSTION: Final[LicensedWeakerExhaustion] = LicensedWeakerExhaustion(
    attempts=(
        WeakerModelAttempt(
            model_name="خطُّ أساسٍ عشوائيّ",
            outcome=WeakerModelOutcome.فشل,
        ),
        WeakerModelAttempt(
            model_name="الثِّقَلُ وحدَه",
            outcome=WeakerModelOutcome.فشل,
        ),
    )
)

PHONETIC_ECONOMY_CANDIDATE: Final[PhoneticEconomyCandidate] = PhoneticEconomyCandidate(
    claim=PHONETIC_ECONOMY_CLAIM,
    session_identity=GFLK_SESSION_IDENTITY,
    closure_check=_CLOSURE_CHECK,
    weaker_exhaustion=_WEAKER_EXHAUSTION,
    tool_readings=(
        ToolReconstructionReading(
            evidence_key="NUN_SAKIN",
            session_value=4.0,
            reconstruction="compute_nun_f",
        ),
        ToolReconstructionReading(
            evidence_key="LAM_TARIF",
            session_value=9.5,
            reconstruction="compute_lam_f",
        ),
    ),
    residuals=(
        INDEPENDENT_CLOSURE_NOT_MET,
        TOOL_IS_APPROXIMATE_RECONSTRUCTION,
        GFLK_SESSION_FINDINGS_SHARE_ONE_ORIGIN,
    ),
)

REGISTERED_RESIDUALS: Final[MappingProxyType[str, RegisteredResidual]] = (
    MappingProxyType(
        {residual.code: residual for residual in PHONETIC_ECONOMY_CANDIDATE.residuals}
    )
)


def registered_residual_for(code: str) -> RegisteredResidual:
    """البقيّةُ برمزها؛ ورمزٌ غيرُ مُسجَّلٍ يُرَدّ ولا يُحمَل على أقربه."""

    if not isinstance(code, str) or code not in REGISTERED_RESIDUALS:
        raise PhoneticEconomyRegistrationError(
            f"لا بقيّةَ مُسجَّلةً بهذا الرمز: {code!r}؛ والرموزُ مُسجَّلةٌ مغلقة."
        )
    return REGISTERED_RESIDUALS[code]


_FORBIDDEN_FIELD_TOKENS: Final[tuple[str, ...]] = (
    "verdict",
    "birth",
    "born",
    "certified",
    "freeze",
    "passed",
    "independent_closure_met",
)


def _assert_no_written_verdict_field() -> None:
    """حارسُ استيراد: لا حكمَ يتسلّل حقلًا يُكتَب بدل أن يُحسَب."""

    for declaring_type in (
        PhoneticEvidenceItem,
        IndependentClosureCheck,
        LicensedWeakerExhaustion,
        ToolReconstructionReading,
        PhoneticEconomyCandidate,
    ):
        for declared in fields(declaring_type):
            lowered = declared.name.lower()
            for token in _FORBIDDEN_FIELD_TOKENS:
                if token in lowered:
                    raise PhoneticEconomyRegistrationError(
                        f"حقلُ حكمٍ تسلّل إلى {declaring_type.__name__}: "
                        f"{declared.name}؛ والحكمُ مُشتَقٌّ لا مكتوب."
                    )


if len(IndependenceAxis) != 3:  # pragma: no cover - حارس
    raise RuntimeError(
        "محاورُ الاستقلال ثلاثة: كوربصٌ وأداةٌ وتعريفُ مقياس؛ وإسقاطُ واحدٍ "
        "منها يجعل التكرارَ استقلالًا."
    )
if len(ClosureOutcome) != 2:  # pragma: no cover - حارس
    raise RuntimeError("حكمُ الإغلاق ثنائيٌّ مغلق.")
if any(member.name in {"BORN", "CERTIFIED"} for member in ChainVerdict):
    raise RuntimeError(  # pragma: no cover - حارس
        "مفردةُ حكمِ السلسلة لا تحمل ولادةً ولا تصديقًا: سلطتُهما غيرُ قائمة."
    )
_assert_no_written_verdict_field()
