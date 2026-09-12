"""تسجيلٌ مسبقٌ لمسح علامات دلالة القيد، مكتوبٌ **قبل** أن يُنقَل نصٌّ واحدٌ
إلى تعداد إسنادات بطاقة التركيب.

**لماذا الآن ولِمَ قبل النصّ؟** `derive_qayd_signification` في
`level_two_manat.py` يمسح نصوصَ الاقتباسات بعلامتين مُجمَّدتين
(`SPECIFYING_TRANSMISSION_MARKERS` و`TARDI_TRANSMISSION_MARKERS`)، فإن اجتمع
الطرفان أُخرِج `دلالة_القيد_متعارضة` وأُوقِف الرابطُ بجنسه المُسمّى. ولمّا كان
المنتظَرُ إدخالُ نقلٍ حقيقيٍّ في «سائمة الغنم» يُتوقَّع أن يُخرِج هذا العضوَ
بعينه، صار توسيعُ مفردة العلامات **بعد** رؤية النصّ تفصيلًا للأداة على مقاس
النتيجة المرجوّة. فيُجمَّد هنا — قبل النصّ — ما يُرخّصه كلُّ مُخرَجٍ وما يمنعه،
وشرطُ أيّ توسيعٍ لاحق، وحدودُ المسح المعلومة اليوم.

**وهذا امتثالٌ صريحٌ للسؤال الاستباقيّ** في
`STRUCTURALLY_UNFALSIFIABLE_NEGATIVE_IS_A_RECURRING_PATTERN_NOTE`: أيُّ مدخلٍ
واقعيٍّ يُفنّد هذه القراءة؟ ولذلك لا تُكتَب حدودُ المسح هنا نثرًا وحسب، بل
تُسمّى أعضاءً في مفردةٍ مغلقة يُقابلها في الاختبار **مدخلٌ فعليٌّ يُظهِرها**؛
فمتى زال حدٌّ منها سقط اختبارُه، ولم يبقَ في الشجرة ادّعاءُ حدٍّ لا يقع.

**وما يُخرِجه المسحُ ليس حكمًا على النصّ**: العلامةُ لفظٌ يقع في الاقتباس، لا
قصدُ قائله ولا جهةُ كلامه؛ والمسحُ لا يرى نفيًا ولا ترددًا ولا ناقلًا عن خصمه،
ولا يُفرّق بين «أخرج» إخراجًا من الحكم و«أخرجه» تخريجًا للحديث. فكلُّ مُخرَجٍ
منه يُقرأ بما سُجِّل له هنا، لا بما يشتهيه قارئه بعد وقوعه.

**ولا يُقدَّم هنا نصٌّ ولا تُملأ بطاقة**: هذا التسجيلُ يسبق النقلَ ولا يقوم
مقامه، وتعدادُ إسنادات بطاقة التركيب يبقى على حاله حتى يُنقَل نصٌّ حرفيٌّ
بموضعه.

**خمولٌ سلطويّ**: لا ولادةَ هنا ولا حكمَ ولادةٍ ولا تجميدَ ولا `E0`، ولا تقرأ
هذه المخرجاتِ بوّابةٌ في `kernel/`.
"""

from __future__ import annotations

from dataclasses import dataclass, fields
from enum import Enum
from types import MappingProxyType
from typing import Final

from .compound_layer_preregistration import NamedRefusal
from .level_two_manat import (
    FRACTAL_VERDICT_IS_NOT_ISSUED_HERE_NOTE,
    LEVEL_TWO_LINK_IS_NOT_THE_TADMIN_TAQYID_CERTIFICATE_NOTE,
    SPECIFICATION_IS_A_KIND_NOT_A_DEGREE_NOTE,
    TRANSMITTED_CONFLICT_IS_A_CASE_NOT_A_CRASH_NOTE,
    QaydSignification,
)
from .text_key import comparison_key

__all__ = [
    "MARKER_SCAN_READS_THE_EXCERPT_ALONE_NOTE",
    "MARKER_VOCABULARY_IS_FROZEN_BEFORE_ITS_TEXT_NOTE",
    "NAMED_RESIDUALS",
    "QAYD_MARKER_PREREGISTRATION",
    "SCAN_BLINDNESS_IS_NOT_A_READING_OF_THE_TEXT_NOTE",
    "TRANSMITTED_CONFLICT_CERTIFIES_NOTHING_FROZEN_NOTE",
    "VERBATIM_TEXT_IS_NOT_SUPPLIED_HERE",
    "MarkerOutcomeRegistration",
    "MarkerScanLimit",
    "QaydMarkerPreregistration",
    "QaydMarkerPreregistrationError",
]


MARKER_SCAN_READS_THE_EXCERPT_ALONE_NOTE: Final[str] = (
    "MarkerScanReadsTheExcerptAlone: مسحُ العلامات يقع على نصّ "
    "`الاقتباس_المنقول` وحده، لا على اسم السلطة ولا على الموضع ولا على شيءٍ "
    "من بقيّة البطاقة؛ فعلامةٌ واقعةٌ في اسم سلطةٍ أو في موضعٍ لا تُغيّر "
    "دلالةَ القيد بحرف، وهذا حدُّ سطحٍ مُشتَقٌّ يُظهِره مدخلٌ فعليّ لا دعوى"
)

MARKER_VOCABULARY_IS_FROZEN_BEFORE_ITS_TEXT_NOTE: Final[str] = (
    "MarkerVocabularyIsFrozenBeforeItsText: مفردتا العلامات مُجمَّدتان قبل "
    "نقل نصّ هذه البطاقة؛ فمن أراد توسيعَهما وسّعهما بتسجيلٍ مُعلَّلٍ **يسبق** "
    "رؤية أثره على بطاقةٍ بعينها ويُسمّي ما يُرخّصه وما يمنعه. وتوسيعُها بعد "
    "قراءة نصٍّ لتُخرِج منه النتيجةَ المتوقَّعة تفصيلُ أداةٍ على مقاس مُخرَجها، "
    "لا كشفُ دلالةٍ في النصّ"
)

SCAN_BLINDNESS_IS_NOT_A_READING_OF_THE_TEXT_NOTE: Final[str] = (
    "ScanBlindnessIsNotAReadingOfTheText: حدودُ المسح المُسمّاة هنا حدودُ "
    "أداةٍ لا أحكامٌ على نصوصٍ بعينها: المسحُ يقع على اللفظ فلا يرى نفيًا ولا "
    "ترددًا ولا ناقلًا عن خصمه ولا اشتراكَ لفظٍ؛ فمُخرَجُه علامةٌ وقعت، "
    "لا دلالةٌ ثبتت عن قائلٍ بعينه"
)

TRANSMITTED_CONFLICT_CERTIFIES_NOTHING_FROZEN_NOTE: Final[str] = (
    "TransmittedConflictCertifiesNothingFrozen: وقوعُ `دلالة_القيد_متعارضة` "
    "على بطاقةٍ حقيقيةٍ يُسجَّل حالًا مُسمّاةً وحسب؛ فلا يفتح مرحلةَ "
    "«التضمين والتقييد» المُجمَّدة ولا يجعل شهادتَها قابلةً للبناء "
    f"({LEVEL_TWO_LINK_IS_NOT_THE_TADMIN_TAQYID_CERTIFICATE_NOTE})، ولا يُصدر "
    f"حكمًا بتوازٍ فركتاليّ ({FRACTAL_VERDICT_IS_NOT_ISSUED_HERE_NOTE})"
)

VERBATIM_TEXT_IS_NOT_SUPPLIED_HERE: Final[str] = "VERBATIM_TEXT_IS_NOT_SUPPLIED_HERE"

_SCAN_BLINDNESS_RESIDUAL: Final[str] = "SCAN_IS_BLIND_TO_NEGATION_AND_STANCE"


class QaydMarkerPreregistrationError(ValueError):
    """رفضٌ صريحٌ في تسجيل علامات دلالة القيد؛ لا يُحمَل على أقرب حالةٍ مقبولة."""


class MarkerScanLimit(Enum):
    """حدودُ المسح المعلومة اليوم، مُسمّاةٌ قبل النصّ ويُقابل كلَّ واحدٍ مدخلٌ يُظهِره."""

    عمى_عن_النفي = "عمى_عن_النفي"
    عمى_عن_جهة_القول = "عمى_عن_جهة_القول"
    عمى_عن_ناقل_العلامة = "عمى_عن_ناقل_العلامة"
    عمى_عن_اشتراك_اللفظ = "عمى_عن_اشتراك_اللفظ"


if len(MarkerScanLimit) != 4:  # pragma: no cover - guard
    raise RuntimeError(
        "حدودُ المسح أربعةٌ مُسمّاةٌ قبل النصّ: النفي، وجهةُ القول، وناقلُ "
        "العلامة، واشتراكُ اللفظ؛ وطيُّ واحدٍ منها يُخفي حدَّ أداةٍ واقعًا"
    )


def _require_text(value: object, label: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise QaydMarkerPreregistrationError(f"{label} نصٌّ غير فارغ")
    return value


@dataclass(frozen=True, slots=True)
class MarkerOutcomeRegistration:
    """مُخرَجٌ واحدٌ مُسجَّلٌ قبل النصّ: ما يُرخّصه، وما يمنعه، كلاهما بنصّه."""

    signification: QaydSignification
    licensed_reading: str
    refused_reading: str

    def __post_init__(self) -> None:
        if not isinstance(self.signification, QaydSignification):
            raise QaydMarkerPreregistrationError("المُخرَجُ من مفردته المغلقة")
        _require_text(self.licensed_reading, f"ما يُرخّصه {self.signification.value}")
        _require_text(self.refused_reading, f"ما يمنعه {self.signification.value}")


@dataclass(frozen=True, slots=True)
class QaydMarkerPreregistration:
    """تسجيلُ المسح كلَّه: سطحُه، وحدودُه، ومخرجاتُه، وشرطُ توسيع مفردته."""

    scan_surface: str
    limits: tuple[tuple[MarkerScanLimit, str], ...]
    outcomes: tuple[MarkerOutcomeRegistration, ...]
    widening_condition: str
    refusals: tuple[NamedRefusal, ...]

    def __post_init__(self) -> None:
        _require_text(self.scan_surface, "سطحُ المسح")
        _require_text(self.widening_condition, "شرطُ توسيع المفردة")

        registered_limits: list[MarkerScanLimit] = []
        for limit, statement in self.limits:
            if not isinstance(limit, MarkerScanLimit):
                raise QaydMarkerPreregistrationError("حدُّ المسح من مفردته المغلقة")
            if limit in registered_limits:
                raise QaydMarkerPreregistrationError(f"حدٌّ مكرَّر: {limit.value}")
            _require_text(statement, f"بيانُ {limit.value}")
            registered_limits.append(limit)
        missing_limits = tuple(
            limit for limit in MarkerScanLimit if limit not in registered_limits
        )
        if missing_limits:
            raise QaydMarkerPreregistrationError(
                "حدٌّ غيرُ مُسمًّى قبل النصّ: "
                + "، ".join(limit.value for limit in missing_limits)
            )

        registered_outcomes: list[QaydSignification] = []
        for registration in self.outcomes:
            if not isinstance(registration, MarkerOutcomeRegistration):
                raise QaydMarkerPreregistrationError(
                    "كلُّ مُخرَجٍ `MarkerOutcomeRegistration` بنصَّيه"
                )
            if registration.signification in registered_outcomes:
                raise QaydMarkerPreregistrationError(
                    f"مُخرَجٌ مكرَّر: {registration.signification.value}"
                )
            registered_outcomes.append(registration.signification)
        missing_outcomes = tuple(
            member for member in QaydSignification if member not in registered_outcomes
        )
        if missing_outcomes:
            raise QaydMarkerPreregistrationError(
                "مُخرَجٌ غيرُ مُسجَّلٍ قبل النصّ: "
                + "، ".join(member.value for member in missing_outcomes)
                + "؛ والتغطيةُ تسبق القراءة، ومُخرَجٌ لم يُسجَّل يُقرأ بعد "
                "وقوعه بما يشتهيه قارئه"
            )

        if not self.refusals:
            raise QaydMarkerPreregistrationError(
                "تسجيلٌ بلا رفضٍ مُسمًّى واحد: حدودُ المسح تُسمّى ولا تُترَك للقارئ"
            )
        seen_names: set[str] = set()
        for refusal in self.refusals:
            if not isinstance(refusal, NamedRefusal):
                raise QaydMarkerPreregistrationError(
                    "كلُّ رفضٍ `NamedRefusal` باسمه وبيانه"
                )
            key = comparison_key(refusal.name)
            if key in seen_names:
                raise QaydMarkerPreregistrationError(f"رفضٌ مكرَّر: {refusal.name}")
            seen_names.add(key)

    @property
    def registered_limits(self) -> tuple[MarkerScanLimit, ...]:
        """حدودُ المسح بترتيب تسجيلها، مُشتَقّةً من التسجيلات نفسها."""

        return tuple(limit for limit, _ in self.limits)

    def statement_for(self, limit: MarkerScanLimit) -> str:
        """بيانُ حدٍّ بعينه؛ والحدُّ موجودٌ بحكم التغطية المفحوصة عند الإنشاء."""

        for registered, statement in self.limits:
            if registered is limit:
                return statement
        raise QaydMarkerPreregistrationError(f"لا بيانَ للحدّ {limit.value}")

    def registration_for(
        self, signification: QaydSignification
    ) -> MarkerOutcomeRegistration:
        """تسجيلُ مُخرَجٍ بعينه؛ والمُخرَجُ موجودٌ بحكم التغطية المفحوصة."""

        for registration in self.outcomes:
            if registration.signification is signification:
                return registration
        raise QaydMarkerPreregistrationError(f"لا تسجيلَ للمُخرَج {signification.value}")


QAYD_MARKER_PREREGISTRATION: Final[QaydMarkerPreregistration] = (
    QaydMarkerPreregistration(
        scan_surface=(
            "نصُّ `الاقتباس_المنقول` في كلّ إسنادٍ من إسنادات طريق نقل القيد "
            "وحده، مقروءًا بمفتاح المقابلة `comparison_key`؛ ولا يُمسَح اسمُ "
            "السلطة ولا الموضع ولا شيءٌ من بقيّة البطاقة"
        ),
        limits=(
            (
                MarkerScanLimit.عمى_عن_النفي,
                "علامةٌ واقعةٌ داخل نفيٍ تُقرأ علامةً وقعت: «لا مفهوم "
                "للمخالفة» يحمل لفظَ `مفهوم المخالفة` فيُشتَقّ منه تخصيصٌ، وهو "
                "عكسُ مراد قائله. فمن أدخل نصًّا منفيًّا فليعلم أنّ المسح "
                "يقرؤه مثبَتًا",
            ),
            (
                MarkerScanLimit.عمى_عن_جهة_القول,
                "المسحُ لا يُفرّق بين جزمٍ وترددٍ واحتمالٍ يُذكَر للاستيفاء: "
                "«يحتمل أنّه لا مفهوم له» و«لا مفهوم له» يقعان عنده سواءً. "
                "فترددُ قائلٍ لا يُقرأ من مُخرَج المسح نسبةً جازمةً إليه",
            ),
            (
                MarkerScanLimit.عمى_عن_ناقل_العلامة,
                "المسحُ يقرأ نصَّ الاقتباس لا قائلَه: فعلامةٌ يَنقُلها ناقلٌ عن "
                "خصمه ليردّها تقع عنده كالعلامة يقولها عن نفسه. فاجتماعُ "
                "العلامتين في نصٍّ واحدٍ قد يكون حكايةَ خلافٍ لا تعارضَ رأيين "
                "منسوبين",
            ),
            (
                MarkerScanLimit.عمى_عن_اشتراك_اللفظ,
                "مفتاحُ المقابلة يطوي الهمزَ وما في حكمه، فـ«أخرج» و«إخراج» "
                "و«أخرجه» تقع كلُّها على علامةٍ واحدة؛ و«أخرجه البخاريّ» "
                "تخريجٌ للحديث لا إخراجٌ من الحكم، ويقع عند المسح علامةَ "
                "تخصيص. وهذا أرجحُ مواقع المصادفة العارضة في نصوص الشروح",
            ),
        ),
        outcomes=(
            MarkerOutcomeRegistration(
                signification=QaydSignification.قيد_مخصص,
                licensed_reading=(
                    "وقعت علامةُ تخصيصٍ ولم تقع علامةُ طرديّة: يُقرأ أنّ في "
                    "الطريق نقلًا يُصرّح بإخراج ما عدا القيد، ويقوم الرابطُ "
                    "الموازي إن قامت درجةُ النقل"
                ),
                refused_reading=(
                    "ولا يُقرأ حكمًا فقهيًّا في المسألة، ولا يُقرأ نسبةَ "
                    "التخصيص إلى قائلٍ بعينه قبل مقابلة نصّه بجهته: "
                    + SCAN_BLINDNESS_IS_NOT_A_READING_OF_THE_TEXT_NOTE
                ),
            ),
            MarkerOutcomeRegistration(
                signification=QaydSignification.وصف_طردي,
                licensed_reading=(
                    "وقعت علامةُ طرديّةٍ ولم تقع علامةُ تخصيص: يُقرأ أنّ في "
                    "الطريق نقلًا يُصرّح بأن لا مفهومَ للقيد، ويقف الرابطُ "
                    "بجنسه المُسمّى"
                ),
                refused_reading=(
                    "ويمتنع أن يُقرأ ترددُ قائلٍ طرديّةً مُثبَتةً عنه: المسحُ "
                    "أعمى عن الجهة، فما وقع منه علامةٌ لا نسبة"
                ),
            ),
            MarkerOutcomeRegistration(
                signification=QaydSignification.دلالة_القيد_متعارضة,
                licensed_reading=(
                    "وقعت العلامتان معًا: تُسجَّل حالُ تعارضٍ منقولٍ بجنس وقوفٍ "
                    "مُسمًّى، وهي نتيجةٌ تُقرأ قضيّةً لا عطلًا "
                    f"({TRANSMITTED_CONFLICT_IS_A_CASE_NOT_A_CRASH_NOTE})"
                ),
                refused_reading=(
                    "ولا يُحمَل التعارضُ على أحد طرفيه، ولا يُقرأ شهادةً "
                    "لمرحلةٍ مُجمَّدةٍ ولا حكمًا فركتاليًّا: "
                    + TRANSMITTED_CONFLICT_CERTIFIES_NOTHING_FROZEN_NOTE
                ),
            ),
            MarkerOutcomeRegistration(
                signification=QaydSignification.دلالة_القيد_غير_محسومة,
                licensed_reading=(
                    "لم تقع علامةٌ من الطرفين: يُقرأ أنّ الطريق لم يَنقُل في "
                    "دلالة القيد تصريحًا تعرفه هذه المفردة، ويقف الرابطُ "
                    "بجنسه المُسمّى"
                ),
                refused_reading=(
                    "ويمتنع أن تُقرأ سالبةُ التخصيص إثباتًا للطرديّة، وأن "
                    "تُوسَّع المفردةُ بعد رؤية هذا النصّ لتُخرِج منه غيرَ ما "
                    f"أخرجت: {SPECIFICATION_IS_A_KIND_NOT_A_DEGREE_NOTE}"
                ),
            ),
        ),
        widening_condition=(
            "توسيعُ مفردة العلامات جائزٌ بشرطين معًا: أن يُكتَب التوسيعُ "
            "بعلّته وبما يُرخّصه وما يمنعه في تسجيلٍ مستقلّ، وأن يسبق هذا "
            "التسجيلُ رؤيةَ أثره على بطاقةٍ بعينها. "
            + MARKER_VOCABULARY_IS_FROZEN_BEFORE_ITS_TEXT_NOTE
        ),
        refusals=(
            NamedRefusal(
                name="MarkerVocabularyIsFrozenBeforeItsText",
                statement=MARKER_VOCABULARY_IS_FROZEN_BEFORE_ITS_TEXT_NOTE,
            ),
            NamedRefusal(
                name="MarkerScanReadsTheExcerptAlone",
                statement=MARKER_SCAN_READS_THE_EXCERPT_ALONE_NOTE,
            ),
            NamedRefusal(
                name="ScanBlindnessIsNotAReadingOfTheText",
                statement=SCAN_BLINDNESS_IS_NOT_A_READING_OF_THE_TEXT_NOTE,
            ),
            NamedRefusal(
                name="TransmittedConflictCertifiesNothingFrozen",
                statement=TRANSMITTED_CONFLICT_CERTIFIES_NOTHING_FROZEN_NOTE,
            ),
        ),
    )
)


NAMED_RESIDUALS: Final[MappingProxyType[str, str]] = MappingProxyType(
    {
        _SCAN_BLINDNESS_RESIDUAL: (
            "مسحُ العلامات لفظيٌّ لا يرى نفيًا ولا جهةَ قولٍ ولا ناقلًا عن "
            "خصمه ولا اشتراكَ لفظ، وحدودُه الأربعة مُسمّاةٌ في "
            "`MarkerScanLimit` ويُقابل كلَّ واحدٍ منها مدخلٌ فعليٌّ يُظهِره في "
            "الاختبار. ورفعُ هذه الفضلة يحتاج قراءةَ جهة الكلام لا توسيعَ "
            "قائمة ألفاظ، وهو بابٌ لم يُفتَح في هذه الشجرة بعد. "
            + SCAN_BLINDNESS_IS_NOT_A_READING_OF_THE_TEXT_NOTE
        ),
        VERBATIM_TEXT_IS_NOT_SUPPLIED_HERE: (
            "هذا التسجيلُ يسبق النقلَ ولا يقوم مقامه: لا نصَّ حرفيًّا يُقدَّم "
            "هنا لبطاقة تركيب «سائمة الغنم»، ولا يُملأ تعدادُ إسناداتها من "
            "شرحٍ بالمعنى. ويبقى خلاءُ التعداد على علّته المكتوبة في البطاقة "
            "نفسها حتى يُنقَل نصٌّ بحروفه وموضعه، ويُشترَط في كلّ اقتباسٍ أن "
            "يحتوي اسمَ سلطته نصًّا كما يُلزِم `LexicalAttribution`"
        ),
    }
)


def _assert_no_outcome_fields(markers: tuple[str, ...]) -> None:
    for declaring_type in (MarkerOutcomeRegistration, QaydMarkerPreregistration):
        for field in fields(declaring_type):
            for marker in markers:
                if marker in field.name.split("_"):  # pragma: no cover - guard
                    raise RuntimeError(
                        f"{declaring_type.__name__} يحمل حقلاً محظورًا: {field.name}"
                    )


_assert_no_outcome_fields(
    ("count", "total", "score", "rank", "verdict", "birth", "fractal")
)
