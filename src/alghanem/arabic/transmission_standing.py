"""درجاتُ اليقين الثلاث ونطاقُ الاستقراء، مُشتَقَّين من حوامل لا مكتوبَين.

ثلاثُ درجات لا سُلَّمٌ متدرِّج بينها: الانتقال بينها مشروطٌ بشروطٍ **نوعيّة**، لا
بعددٍ يكبر حتى ينقلب يقينًا. فالعددُ وحده لا يُنتج تواترًا، وتكرارُ الادّعاء لا
يُنتج قياسًا:

* **متواتر**: (١) علمٌ لا ظنّ، مستندٌ إلى مشاهدةٍ مباشرة لا إلى استنتاج؛
  (٢) استقلالُ مصادرَ يستحيل معه التواطؤ — لا حجمُ عيّنةٍ وحده؛ (٣) تكرارٌ عبر
  أجيالٍ أو دوراتٍ مستقلّة متعاقبة، لا دفعةً واحدة.
* **آحاد**: ظنٌّ مقبولٌ شرطيًّا، يحتاج تثبّتَ روايةٍ ودرايةٍ معًا قبل **كلّ**
  قبول، ولا يُعفى أبدًا من إعادة الفحص.
* **فرض**: مجرّدُ تقديرٍ لم يقع عليه حسٌّ مستقلٌّ بعد؛ ولا يتحوّل إلى آحادٍ أو
  تواترٍ إلا بقياسٍ مستقلٍّ فعليّ، لا بتكرار الادّعاء.

**لا حقلَ عددٍ في أيّ صنفٍ هنا** (§٤ من `docs/AIMS.md`: «التعدادُ خاصّيةٌ تُحسَب
لا حقلٌ يُكتَب»)، ويُفحَص ذلك عند الاستيراد على حقول الأصناف نفسها. وإدخالُ عددِ
مصادرَ هنا يُعيد بابَ «كثرةُ الرواة تُنتج تواترًا» الذي تُغلقه الشروط النوعيّة.

**الدرجةُ تُشتَقّ من ثلاثة حوامل مغلقة ولا تُكتَب**، على منوال حوامل
`word_class_formal.py`: أساسُ العلم، واستقلالُ المصادر، ونمطُ التكرار. وأيُّ
درجةٍ مكتوبةٍ تخالف المُشتَقّة تُرفَض عند الإنشاء، فلا موضعَ تُكتَب فيه النتيجة
مباشرةً.

**المتواتر مُعلَنٌ في المفردة وغيرُ قابلٍ للبناء اليوم**، بالانضباط نفسه الذي
مُنع به `شاهد_لكل_فرع` و`CLOSED_BY_FROZEN_EXPERIMENT` و`مُتحقَّق_محليًّا`: لا
سلطةَ في هذا المستودع تفحص استقلالَ مصادرَ عبر أجيالٍ متعاقبة، فإصدارُ الدرجة
ادّعاءُ فحصٍ لم يجرِ. ويُرفَض برسالته الخاصّة **قبل** الرسالة العامّة، كيلا
يُقرَأ رفضٌ مبنيٌّ على انعدام السلطة رفضًا أضعفَ مبنيًّا على نقص حامل.

**الاستقراء نطاقان لا مبلغان من الدقّة**: تامٌّ داخل مجموعةٍ مغلقة فيُنتج يقينًا
**داخل حدودها**، وناقصٌ خارجها فيبقى ظنيًّا مهما اتّسع. وجملةُ النطاق **تُشتَقّ
ولا تُكتَب**: الحقلُ المكتوب يُقابَل بالمُشتَقّ ويُرفَض عند الاختلاف، فالتعميمُ
المباشر من مدوّنةٍ مغلقة إلى اللسان الذي أُخذت منه ممتنعٌ بنيويًّا لا مُتّقًى
بتحفّظٍ في النثر.

**إعفاءُ «المعلومات المنظّمة الأولى» سؤالٌ مفتوح لا إعفاءٌ ممنوح**: يُسجَّل بلا
حقل جوابٍ أصلًا، على منوال `Phase2OpenQuestion`، لأنّ بداهةَ الشيء عند الباحث
ليست تواترًا، والفرقُ بينهما هو بعينه ما تفصله الشروطُ النوعيّة أعلاه.

**خمولٌ سلطويّ**: `TransmissionStanding != BirthVerdict` و
`ScopedFinding != CertifiedResidual`؛ لا ولادةَ ولا تجميدَ ولا `E0`، ولا تقرأ
هذه الوحدةَ أيّ بوّابةٍ في `kernel/`، وحقولُ التدقيق الخارجيّ تبقى متطابقةً
بايتًا.
"""

from __future__ import annotations

from dataclasses import dataclass, fields
from enum import Enum
from typing import Final

_FORBIDDEN_COUNT_FIELD_MARKERS: Final = (
    "count",
    "number",
    "size",
    "total",
    "verdict",
    "birth",
)


class TransmissionStandingError(ValueError):
    """درجةٌ أو نطاقٌ مرفوض؛ لا يُحمَل على أقرب درجةٍ مقبولة."""


class KnowledgeBasis(Enum):
    """حاملُ أساس العلم: أمشاهدةٌ مباشرة، أم استنتاجٌ من غيرها؟"""

    DIRECT_OBSERVATION = "مشاهدة_مباشرة"
    INFERENCE = "استنتاج"


class SourceIndependence(Enum):
    """حاملُ استقلال المصادر: أيستحيل التواطؤ، أم لم يُثبَت استحالتُه؟"""

    COLLUSION_IMPOSSIBLE = "يستحيل_معه_التواطؤ"
    NOT_ESTABLISHED = "غير_مُثبَت"


class RepetitionPattern(Enum):
    """حاملُ نمط التكرار: أأجيالٌ متعاقبة، أم دفعةٌ واحدة، أم لا تكرار؟"""

    SUCCESSIVE_GENERATIONS = "دورات_مستقلة_متعاقبة"
    SINGLE_BATCH = "دفعة_واحدة"
    NONE = "لا_تكرار"


class TransmissionStanding(Enum):
    """الدرجاتُ الثلاث، مفردةً مغلقة؛ ولا تدرّجَ بينها بل انتقالٌ بشروط."""

    MUTAWATIR = "متواتر"
    AHAD = "آحاد"
    FARD = "فرض"


class IstiqraScope(Enum):
    """نطاقُ الاستقراء: تامٌّ داخل مجموعةٍ مغلقة، أو ناقصٌ خارجها."""

    COMPLETE_WITHIN_CLOSED_SET = "تام_داخل_مجموعة_مغلقة"
    INCOMPLETE = "ناقص"


class ExemptionHypothesis(Enum):
    """احتمالاتُ سؤال الإعفاء الثلاثة كاملةً، فالثنائيةُ هنا كاذبة."""

    EXEMPT_BY_GENUINE_RECURRENCE = "مُعفاة_لبلوغها_تواترًا_حقيقيًّا"
    NOT_EXEMPT_MERE_SELF_EVIDENCE = "غير_معفاة_وبداهتها_ليست_تواترًا"
    EXEMPTION_QUESTION_ILL_POSED = "السؤال_نفسه_غير_مستقيم_الوضع"


if len(TransmissionStanding) != 3:  # pragma: no cover - guard
    raise RuntimeError("the transmission standings are deliberately three")
if len(IstiqraScope) != 2:  # pragma: no cover - guard
    raise RuntimeError("induction scope is deliberately two-valued")
if len(ExemptionHypothesis) != 3:  # pragma: no cover - guard
    raise RuntimeError("the exemption question declares exactly three hypotheses")


MUTAWATIR_IS_UNCONSTRUCTIBLE_NOTE: Final = (
    "المتواترُ مُعلَنٌ وغيرُ قابلٍ للبناء هنا: لا سلطةَ في هذا المستودع تفحص "
    "استقلالَ مصادرَ يستحيل معه التواطؤ ولا تعاقبَ دوراتٍ مستقلّة عبر أجيال، "
    "فإصدارُ الدرجة ادّعاءُ فحصٍ لم يجرِ لا اختصارُ طريق"
)

COUNT_IS_NOT_RECURRENCE_NOTE: Final = (
    "حجمُ العيّنة ليس استقلالًا، وكثرةُ النقل ليست تعاقبَ أجيال: الشروطُ نوعيّةٌ "
    "لا عدديّة، فلا حقلَ عددٍ هنا يُرقّي درجةً"
)

FARD_NEEDS_MEASUREMENT_NOT_REPETITION_NOTE: Final = (
    "الفرضُ تقديرٌ لم يقع عليه حسٌّ مستقلٌّ بعد؛ ولا يتحوّل إلى آحادٍ أو تواترٍ "
    "إلا بقياسٍ مستقلٍّ فعليّ، وتكرارُ الادّعاء ليس قياسًا"
)

AHAD_IS_NEVER_EXEMPT_FROM_RECHECK_NOTE: Final = (
    "الآحادُ مقبولٌ شرطيًّا: يحتاج تثبّتَ روايةٍ ودرايةٍ معًا قبل كلّ قبول، ولا "
    "يُعفى أبدًا من إعادة الفحص مهما تكرّر قبولُه سابقًا"
)

DIRECT_GENERALIZATION_IS_REFUSED_NOTE: Final = (
    "استقراءٌ تامٌّ داخل مدوّنةٍ مغلقة يُنتج يقينًا داخل حدودها وحدها؛ والتعميمُ "
    "المباشر على اللسان الذي أُخذت منه يبقى ظنيًّا حتى يُستقرَأ كوربصٌ مستقلٌّ "
    "ثانٍ، فجملةُ النطاق تُشتَقّ ولا تُكتَب"
)

TRANSMISSION_AUTHORITY_NOTE: Final = (
    "تسجيلٌ فقط: لا تُصدر هذه الوحدة ولادةً ولا حكمًا ولا تجميدًا ولا `E0`، ولا "
    "تقرؤها أيّ بوّابةٍ في النواة"
)


def _require_non_blank(value: str, field_name: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise TransmissionStandingError(f"{field_name} نصٌّ غير فارغ")
    return value


def derive_standing(
    basis: KnowledgeBasis,
    independence: SourceIndependence,
    repetition: RepetitionPattern,
) -> TransmissionStanding:
    """اشتقّ الدرجةَ من حواملها الثلاثة؛ دالّةٌ تامّةٌ بلا فرعٍ افتراضيّ."""

    for value, expected, name in (
        (basis, KnowledgeBasis, "حاملُ أساس العلم"),
        (independence, SourceIndependence, "حاملُ استقلال المصادر"),
        (repetition, RepetitionPattern, "حاملُ نمط التكرار"),
    ):
        if not isinstance(value, expected):
            raise TransmissionStandingError(f"{name} من مفردته المغلقة")

    if basis is KnowledgeBasis.INFERENCE:
        return TransmissionStanding.FARD
    if (
        independence is SourceIndependence.COLLUSION_IMPOSSIBLE
        and repetition is RepetitionPattern.SUCCESSIVE_GENERATIONS
    ):
        return TransmissionStanding.MUTAWATIR
    return TransmissionStanding.AHAD


@dataclass(frozen=True, slots=True)
class TransmissionStandingRecord:
    """درجةُ خبرٍ واحد بحواملها الثلاثة، مُشتَقّةً ومُقابَلةً بالمكتوب."""

    report_id: str
    basis: KnowledgeBasis
    independence: SourceIndependence
    repetition: RepetitionPattern
    declared_standing: TransmissionStanding
    justification: str

    def __post_init__(self) -> None:
        _require_non_blank(self.report_id, "معرّف الخبر")
        _require_non_blank(self.justification, "تبرير الدرجة")
        if not isinstance(self.declared_standing, TransmissionStanding):
            raise TransmissionStandingError("الدرجةُ المكتوبة من مفردتها المغلقة")

        derived = derive_standing(self.basis, self.independence, self.repetition)
        if derived is TransmissionStanding.MUTAWATIR:
            raise TransmissionStandingError(MUTAWATIR_IS_UNCONSTRUCTIBLE_NOTE)
        if self.declared_standing is TransmissionStanding.MUTAWATIR:
            raise TransmissionStandingError(MUTAWATIR_IS_UNCONSTRUCTIBLE_NOTE)
        if self.declared_standing is not derived:
            raise TransmissionStandingError(
                "الدرجةُ المكتوبة تخالف المُشتَقّة من الحوامل: "
                f"{self.declared_standing.value} مكتوبةً و{derived.value} مُشتَقّة"
            )

    @property
    def standing(self) -> TransmissionStanding:
        """الدرجةُ المُشتَقّة من الحوامل، لا المكتوبةُ بجانبها."""

        return derive_standing(self.basis, self.independence, self.repetition)

    @property
    def requires_recheck_before_every_acceptance(self) -> bool:
        """أيلزم تثبّتٌ جديد قبل كلّ قبول؟ نعم في الدرجتين المتاحتين هنا."""

        return True

    @property
    def awaits_independent_measurement(self) -> bool:
        """أينتظر هذا الخبرُ قياسًا مستقلًّا لم يقع بعد؟ مُشتَقٌّ لا مكتوب."""

        return self.standing is TransmissionStanding.FARD


def derive_scope_statement(
    scope: IstiqraScope, enumerated_set: str, wider_set: str
) -> str:
    """اشتقّ جملةَ النطاق الواجبة؛ لا موضعَ تُكتَب فيه هذه الجملةُ حرًّا."""

    if not isinstance(scope, IstiqraScope):
        raise TransmissionStandingError("نطاقُ الاستقراء من مفردته المغلقة")
    enumerated = _require_non_blank(enumerated_set, "المجموعة المُستقرأة").strip()
    wider = _require_non_blank(wider_set, "المجموعة الأوسع").strip()
    if scope is IstiqraScope.COMPLETE_WITHIN_CLOSED_SET:
        return (
            f"ثبت الأمر يقينًا داخل {enumerated}، ويبقى ظنيًّا بخصوص {wider} "
            "حتى يُستقرَأ كوربصٌ مستقلٌّ ثانٍ"
        )
    return (
        f"لم يُستقرَأ {enumerated} استقراءً تامًّا، فيبقى الأمر ظنيًّا داخله "
        f"وبخصوص {wider} معًا"
    )


@dataclass(frozen=True, slots=True)
class ScopedFinding:
    """نتيجةٌ بنطاقها: الجملةُ مُشتَقّةٌ من المجموعتين، والمكتوبُ يُقابَل بها."""

    finding_id: str
    scope: IstiqraScope
    enumerated_set: str
    wider_set: str
    declared_statement: str

    def __post_init__(self) -> None:
        _require_non_blank(self.finding_id, "معرّف النتيجة")
        _require_non_blank(self.enumerated_set, "المجموعة المُستقرأة")
        _require_non_blank(self.wider_set, "المجموعة الأوسع")
        _require_non_blank(self.declared_statement, "جملة النطاق المكتوبة")
        if not isinstance(self.scope, IstiqraScope):
            raise TransmissionStandingError("نطاقُ الاستقراء من مفردته المغلقة")
        if self.enumerated_set.strip() == self.wider_set.strip():
            raise TransmissionStandingError(
                "المجموعةُ المُستقرأة والمجموعةُ الأوسع واحدة: فلا نطاقَ يُتجاوَز "
                "أصلًا، وتسجيلُ ذلك يُوهم حدًّا لا وجود له"
            )
        if self.declared_statement.strip() != self.derived_statement:
            raise TransmissionStandingError(
                f"جملةُ النطاق تُشتَقّ ولا تُكتَب. {DIRECT_GENERALIZATION_IS_REFUSED_NOTE}"
            )

    @property
    def derived_statement(self) -> str:
        """جملةُ النطاق الواجبة، مُشتَقّةً من النطاق والمجموعتين وحدها."""

        return derive_scope_statement(self.scope, self.enumerated_set, self.wider_set)

    @property
    def is_certain_within_the_enumerated_set(self) -> bool:
        """أيقينٌ داخل المجموعة المُستقرأة؟ مُشتَقٌّ من النطاق لا مكتوب."""

        return self.scope is IstiqraScope.COMPLETE_WITHIN_CLOSED_SET

    @property
    def is_certain_beyond_the_enumerated_set(self) -> bool:
        """`False` بنيويًّا: لا استقراءَ تامٌّ يُخرج يقينًا من حدوده."""

        return False


@dataclass(frozen=True, slots=True)
class ExemptionOpenQuestion:
    """سؤالُ إعفاء المعلومات المنظّمة الأولى: احتمالاته كلّها، ولا جوابَ فيه."""

    question_id: str
    hypotheses: tuple[ExemptionHypothesis, ...]
    why_open: str

    def __post_init__(self) -> None:
        _require_non_blank(self.question_id, "معرّف السؤال")
        _require_non_blank(self.why_open, "سبب بقاء السؤال مفتوحًا")
        if not isinstance(self.hypotheses, tuple):
            raise TransmissionStandingError("الاحتمالات تُعلَن مجموعةً مرتَّبة")
        for hypothesis in self.hypotheses:
            if not isinstance(hypothesis, ExemptionHypothesis):
                raise TransmissionStandingError("كلُّ احتمالٍ من مفردته المغلقة")
        if set(self.hypotheses) != set(ExemptionHypothesis) or len(
            self.hypotheses
        ) != len(ExemptionHypothesis):
            raise TransmissionStandingError(
                "السؤالُ المفتوح يُعلِن احتمالاته كلّها بلا تكرار؛ وإسقاطُ احتمالٍ "
                "منها يصنع ثنائيةً كاذبة"
            )

    @property
    def remains_open(self) -> bool:
        """هل بقي السؤال بلا جواب؟ نعم دائمًا في هذه المرحلة، بنيويًّا."""

        return True


FIRST_ORGANIZED_INFORMATION_QUESTION: Final = ExemptionOpenQuestion(
    question_id="first-organized-information-exemption",
    hypotheses=tuple(ExemptionHypothesis),
    why_open=(
        "الإعفاءُ من بروتوكول الولادة الكامل مشروطٌ ببلوغ تواترٍ حقيقيّ بالمعنى "
        "النوعيّ أعلاه — إجماعٌ مؤسّسيّ أو علميّ مستقلٌّ عبر مصادرَ متنوّعةٍ "
        "فعلًا — لا بمجرّد بداهةِ الأمر عند الباحث؛ ولا سلطةَ هنا تفحص ذلك، فلا "
        "يُسجَّل إعفاءٌ ممنوح ولا مَنعٌ مُثبَت، بل سؤالٌ مفتوحٌ باحتمالاته الثلاثة"
    ),
)


def _assert_no_fields_matching(
    declaring_type: type, markers: tuple[str, ...], message: str
) -> None:
    for item in fields(declaring_type):
        if any(marker in item.name for marker in markers):
            raise RuntimeError(message)


for _declaring_type in (
    TransmissionStandingRecord,
    ScopedFinding,
    ExemptionOpenQuestion,
):
    _assert_no_fields_matching(
        _declaring_type,
        _FORBIDDEN_COUNT_FIELD_MARKERS,
        "no type here may carry a count, size, verdict, or birth field",
    )


__all__ = [
    "AHAD_IS_NEVER_EXEMPT_FROM_RECHECK_NOTE",
    "COUNT_IS_NOT_RECURRENCE_NOTE",
    "DIRECT_GENERALIZATION_IS_REFUSED_NOTE",
    "FARD_NEEDS_MEASUREMENT_NOT_REPETITION_NOTE",
    "FIRST_ORGANIZED_INFORMATION_QUESTION",
    "MUTAWATIR_IS_UNCONSTRUCTIBLE_NOTE",
    "TRANSMISSION_AUTHORITY_NOTE",
    "ExemptionHypothesis",
    "ExemptionOpenQuestion",
    "IstiqraScope",
    "KnowledgeBasis",
    "RepetitionPattern",
    "ScopedFinding",
    "SourceIndependence",
    "TransmissionStanding",
    "TransmissionStandingError",
    "TransmissionStandingRecord",
    "derive_scope_statement",
    "derive_standing",
]
