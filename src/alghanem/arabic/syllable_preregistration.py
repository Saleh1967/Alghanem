"""تجميدُ السيلبنة قبل إجرائها: قوالبُ ستّةٌ مغلقة، ووزنٌ إسقاطٌ لا كائن.

هذه الوحدةُ تُكتَب **قبل** وحدة القياس، على منوال
`compression_model_preregistration`: تُجمِّد ما سيُقاس وشرطَ قبوله، وتُخرِج
بصمةً تسقط بتغيّر بندٍ واحدٍ فيها فتسقط معها قراءةُ `syllabifier`.

`WAZN_IS_A_DERIVED_PROJECTION_NOT_A_BORN_OBJECT`: الوزنُ إسقاطٌ يُشتَقّ عند
السؤال من سلسلة المقاطع، ولا يُولَد كائنًا صرفيًّا له هويّةٌ مستقلّة. وهذا
شرطُ دخولِ الطبقة المكتوبُ قبلَ هذه الجلسة في
`word_structure_dictionary_preregistration`، لا شرطٌ يُبتكَر هنا.

`THE_TEMPLATES_ARE_SIX_AND_CLOSED`: القوالبُ CV, CVC, CVV, CVVC, CVCC, CVVCC
ولا سابعَ لها؛ ومقطعٌ لا يقع في واحدٍ منها لا يُقرَّب إلى أقربها، بل تُردّ
الكلمةُ كلُّها إلى حقل التعذّر.

`SHADDA_EXPANDS_INTO_TWO_SLOTS`: الشدّةُ شقّان — ساكنٌ يُغلق مقطعًا ومتحرّكٌ
يفتح ما بعده. والمرمازُ القائمُ يُخرِج الشقَّ الأوّلَ وحدةً مستقلّةً
(`GeminationRole.PAIR_START`)، فالتوسيعُ مقروءٌ من الوحدات لا مُنشأٌ فيها.

`AN_UNSEGMENTABLE_WORD_IS_A_NAMED_REFUSAL_NOT_A_NULL`: ما لم يُقطَّع يخرج في
`wazn_unresolved` باسم سببه، ولا يُخرَج `None` ولا مقطعٌ فارغ.

`NO_THRESHOLD_IS_INVENTED_AFTER_THE_FACT`: أرضيّةُ القبول هنا **بنيويّةٌ** لا
نسبةٌ مئويّة: شروطٌ أربعةٌ تُكتَب قبل القياس وتُفحَص على البايتات المُبصَّمة.
أمّا حصّةُ الكلمات المتعذّرة فرقمٌ يُنشَر كما خرج، ولا عتبةَ له في هذه الجلسة؛
ومن كتب عتبةً بعد رؤية الرقم كتب نتيجةً لا شرطًا.

`THE_WAQF_TRANSFORM_IS_A_STATED_INPUT_OPERATION`: إسقاطُ إعراب الآخِر عمليّةٌ
تُجرى على مُدخَلٍ **مُصرَّحٍ به** أنّه موقوفٌ عليه؛ وليست قراءةً للمدوّنة،
لأنّ الشجرةَ لا تُميّز السكونَ الوقفيَّ من الوصليّ
(`PAUSAL_SUKUN_IS_NOT_DISTINGUISHED_FROM_CONNECTED_SUKUN` في
`ibtida_wasl_waqf_registration`).

`THIS_IS_REGISTRATION_NOT_AUTHORITY`: لا ولادةَ هنا، ولا حكمَ ولادة، ولا تجميدَ
`E0`، ولا استيرادَ من `kernel/`، ولا يُرفَع بهذه الوحدة حجبُ طبقةٍ عن قاموس
بنية الكلمة.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Final

from alghanem.canonical_content import canonical_bytes, canonical_digest

from .word_structure_dictionary_preregistration import (
    DictionaryLayer,
    LayerRegistration,
)
from .word_structure_dictionary_preregistration import (
    layer_registration as _dictionary_layer_registration,
)

__all__ = [
    "AN_UNSEGMENTABLE_WORD_IS_A_NAMED_REFUSAL_NOT_A_NULL",
    "NO_THRESHOLD_IS_INVENTED_AFTER_THE_FACT",
    "PREREGISTRATION_DIGEST",
    "SHADDA_EXPANSION_RULE",
    "STRUCTURAL_ACCEPTANCE_CONDITIONS",
    "SYLLABLE_PREREGISTRATION_NAMED_RESIDUALS",
    "THE_TEMPLATES_ARE_SIX_AND_CLOSED",
    "THE_WAQF_TRANSFORM_IS_A_STATED_INPUT_OPERATION",
    "THIS_IS_REGISTRATION_NOT_AUTHORITY",
    "TANWEEN_IS_READ_AS_A_VOWEL_PLUS_A_CLOSING_NUN",
    "WAQF_TRANSFORM_RULES",
    "WAZN_IS_A_DERIVED_PROJECTION_NOT_A_BORN_OBJECT",
    "StructuralAcceptanceCondition",
    "SyllablePreregistrationError",
    "SyllableTemplate",
    "WaqfRule",
    "layer_registration",
    "preregistration_digest",
    "template_of",
]


class SyllablePreregistrationError(ValueError):
    """رفضٌ عند الإنشاء: قالبٌ خارج الستّة، أو شرطٌ بلا نصِّ فحصٍ مكتوب."""


class SyllableTemplate(Enum):
    """القوالبُ الستّة. مفردةٌ مغلقةٌ، وقيمتُها شكلُها الحرفيُّ لا وصفُها."""

    CV = "CV"
    CVC = "CVC"
    CVV = "CVV"
    CVVC = "CVVC"
    CVCC = "CVCC"
    CVVCC = "CVVCC"


def template_of(onset: int, nucleus_length: int, coda: int) -> SyllableTemplate:
    """القالبُ من شكله: صامتٌ مفتتِح، وطولُ الصائت، وعددُ الصوامت المُغلِقة.

    ولا تقريبَ إلى أقربِ قالب: شكلٌ خارجَ الستّة يُرفَع به استثناءٌ، فالكلمةُ
    تُردّ إلى حقل التعذّر ولا تُقرأ بقالبٍ لم تقع فيه.
    """

    if onset != 1:
        raise SyllablePreregistrationError(
            "المقطعُ يبدأ بصامتٍ متحرّكٍ واحدٍ بنصّ التعريف الصرفيّ المُعلَن؛ "
            "وهذا شرطٌ بالنسبة إليه لا بإطلاقٍ صوتيّ"
        )
    if nucleus_length not in (1, 2) or coda not in (0, 1, 2):
        raise SyllablePreregistrationError("طولُ الصائت ١ أو ٢، والإغلاقُ ٠ أو ١ أو ٢")
    name = "CV" + "V" * (nucleus_length - 1) + "C" * coda
    try:
        return SyllableTemplate(name)
    except ValueError as error:  # pragma: no cover - المفردةُ مغلقةٌ بالبناء
        raise SyllablePreregistrationError(
            f"الشكلُ {name!r} خارجَ القوالب الستّة، ولا يُقرَّب إلى أقربها"
        ) from error


@dataclass(frozen=True, slots=True)
class StructuralAcceptanceCondition:
    """شرطُ قبولٍ بنيويٌّ واحد: نصُّه، وكيف يُفحَص، وما يُسقطه."""

    name: str
    statement: str
    how_it_is_checked: str
    what_would_fail_it: str

    def __post_init__(self) -> None:
        for value, label in (
            (self.name, "اسمُ الشرط"),
            (self.statement, "نصُّ الشرط"),
            (self.how_it_is_checked, "طريقةُ الفحص"),
            (self.what_would_fail_it, "ما يُسقط الشرط"),
        ):
            if not isinstance(value, str) or not value.strip():
                raise SyllablePreregistrationError(f"{label} نصٌّ غير فارغ")

    def as_canonical_content(self) -> dict[str, str]:
        """محتوى الشرط للبصمة؛ الترتيبُ من المفتاح لا من الكتابة."""

        return {
            "name": self.name,
            "statement": self.statement,
            "how_it_is_checked": self.how_it_is_checked,
            "what_would_fail_it": self.what_would_fail_it,
        }


STRUCTURAL_ACCEPTANCE_CONDITIONS: Final[tuple[StructuralAcceptanceCondition, ...]] = (
    StructuralAcceptanceCondition(
        name="CLOSURE",
        statement="كلُّ مقطعٍ يخرج من الأداة عضوٌ في القوالب الستّة",
        how_it_is_checked=(
            "عضويّةُ `SyllableTemplate` مفحوصةٌ بالبناء في `template_of`، "
            "وتُعاد على المدوّنة المُبصَّمة كلمةً كلمة"
        ),
        what_would_fail_it="مقطعٌ واحدٌ بشكلٍ سابعَ يُقرَّب إلى أقرب قالب",
    ),
    StructuralAcceptanceCondition(
        name="RECONSTRUCTION",
        statement=(
            "تسلسلُ الشرائح المُقطَّعةِ يُعيد سلسلةَ الصوامت والصوائت التي "
            "دخلت، شريحةً بشريحةٍ وبالترتيب"
        ),
        how_it_is_checked=(
            "مقارنةُ ما يُخرِجه التقطيعُ بما أدخله التوسيعُ قبله، على كلّ كلمةٍ "
            "مقروءةٍ من البايتات المُبصَّمة"
        ),
        what_would_fail_it="شريحةٌ تُبتَلَع في التقطيع أو تُستحدَث فيه",
    ),
    StructuralAcceptanceCondition(
        name="TOTALITY",
        statement=(
            "مجموعُ الكلمات المُقطَّعة والكلمات في `wazn_unresolved` يساوي "
            "مجموعَ الكلمات المقروءة، بلا كلمةٍ تسقط بينهما"
        ),
        how_it_is_checked="عدٌّ ثلاثيٌّ يُطابَق على المدوّنة المُبصَّمة",
        what_would_fail_it="كلمةٌ لا تظهر في أيٍّ من العدَّين",
    ),
    StructuralAcceptanceCondition(
        name="DETERMINISM",
        statement="المُدخَلُ نفسُه يُخرِج التقطيعَ نفسَه في كلّ نداء",
        how_it_is_checked="ندءان متتاليان على المُدخَل الواحد وتطابقُ مُخرَجيهما",
        what_would_fail_it="حالٌ محفوظةٌ بين ندائين، أو ترتيبٌ يعتمد على مجموعة",
    ),
)
"""أرضيّةُ القبول البنيويّة، مكتوبةً قبل أن تُقاس على بايتةٍ واحدة."""


SHADDA_EXPANSION_RULE: Final[str] = (
    "الشدّةُ شقّان: الشقُّ الأوّلُ صامتٌ ساكنٌ يُغلق المقطعَ السابق، والثاني "
    "صامتٌ متحرّكٌ يفتح ما بعده. والمرمازُ القائمُ يُخرِج الشقَّ الأوّلَ وحدةً "
    "مستقلّةً بـ`GeminationRole.PAIR_START`، فالتوسيعُ قراءةٌ لا إنشاء"
)

TANWEEN_IS_READ_AS_A_VOWEL_PLUS_A_CLOSING_NUN: Final[str] = (
    "TanweenIsReadAsAVowelPlusAClosingNun: التنوينُ يُقطَّع صائتًا قصيرًا "
    "يليه صامتٌ مُغلِق (نونٌ ساكنةٌ غيرُ مكتوبة). وهذه **قراءةٌ مُعلَنة** لا "
    "مقيسة: الشجرةُ لا ترى نونًا في الرسم، وإنّما تقرأ العلامةَ على ما "
    "اصطُلح عليه؛ ومن عدّها بلا تصريحٍ أدخل حرفًا لم يُكتَب"
)


@dataclass(frozen=True, slots=True)
class WaqfRule:
    """قاعدةٌ من قواعد إسقاط إعراب الآخِر، على مُدخَلٍ مُصرَّحٍ بوقفه."""

    name: str
    applies_to: str
    becomes: str

    def __post_init__(self) -> None:
        for value, label in (
            (self.name, "اسمُ القاعدة"),
            (self.applies_to, "موضعُ التطبيق"),
            (self.becomes, "ما تصير إليه"),
        ):
            if not isinstance(value, str) or not value.strip():
                raise SyllablePreregistrationError(f"{label} نصٌّ غير فارغ")

    def as_canonical_content(self) -> dict[str, str]:
        """محتوى القاعدة للبصمة."""

        return {
            "name": self.name,
            "applies_to": self.applies_to,
            "becomes": self.becomes,
        }


WAQF_TRANSFORM_RULES: Final[tuple[WaqfRule, ...]] = (
    WaqfRule(
        name="TANWEEN_DAMM_OR_KASR",
        applies_to="آخرُ وحدةٍ حاملةٍ حركةً فعليّةً لا مدَّ بعدها، بتنوين ضمٍّ أو كسر",
        becomes="سكون",
    ),
    WaqfRule(
        name="TANWEEN_FATH",
        applies_to="الموضعُ نفسُه بتنوين فتح",
        becomes="فتحةٌ مجرّدةٌ يبقى مدُّها",
    ),
    WaqfRule(
        name="BARE_HARAKA",
        applies_to="الموضعُ نفسُه بحركةٍ بلا تنوين",
        becomes="سكون",
    ),
    WaqfRule(
        name="TAA_MARBUTA",
        applies_to="تاءٌ مربوطةٌ آخرَ الصورة",
        becomes="هاءٌ ساكنة",
    ),
)
"""قواعدُ الوقف الأربع، مُجمَّدةً بترتيبها قبل أن تُكتَب دالّةُ تحويلٍ واحدة."""


def layer_registration() -> LayerRegistration:
    """تسجيلُ طبقة المقطع والوزن، مقروءًا من موضعه السابق لا منسوخًا هنا."""

    return _dictionary_layer_registration(DictionaryLayer.SYLLABLES_AND_WAZN)


WAZN_IS_A_DERIVED_PROJECTION_NOT_A_BORN_OBJECT: Final[str] = (
    "WaznIsADerivedProjectionNotABornObject: الوزنُ يُشتَقّ من سلسلة المقاطع "
    "عند السؤال ولا يُخزَّن كائنًا؛ ومن جعله مولودًا أعطى الإسقاطَ هويّةً "
    "يُحتَجّ بها على ما أُسقِط عنه"
)

THE_TEMPLATES_ARE_SIX_AND_CLOSED: Final[str] = (
    "TheTemplatesAreSixAndClosed: ستّةُ قوالبَ لا سابعَ لها، ولا تقريبَ "
    "لمقطعٍ خارجها إلى أقربها؛ فالتقريبُ يُخفي الخارجَ في الداخل"
)

AN_UNSEGMENTABLE_WORD_IS_A_NAMED_REFUSAL_NOT_A_NULL: Final[str] = (
    "AnUnsegmentableWordIsANamedRefusalNotANull: المتعذّرُ يخرج باسم سببه في "
    "`wazn_unresolved`؛ و`None` يُسوّي «لم يُقطَّع» بـ«قُطِّع فكان لا شيء»"
)

NO_THRESHOLD_IS_INVENTED_AFTER_THE_FACT: Final[str] = (
    "NoThresholdIsInventedAfterTheFact: أرضيّةُ القبول بنيويّةٌ مكتوبةٌ قبل "
    "القياس؛ وحصّةُ المتعذّر رقمٌ يُنشَر بلا عتبةٍ في هذه الجلسة، ومن كتب "
    "العتبةَ بعد الرقم كتب النتيجةَ شرطًا"
)

THE_WAQF_TRANSFORM_IS_A_STATED_INPUT_OPERATION: Final[str] = (
    "TheWaqfTransformIsAStatedInputOperation: التحويلُ يُجرى على مُدخَلٍ "
    "مُصرَّحٍ بوقفه، ولا يُقرَأ الوقفُ من المدوّنة؛ فالسكونُ الوقفيُّ غيرُ "
    "مُميَّزٍ من الوصليّ في هذه الشجرة"
)

THIS_IS_REGISTRATION_NOT_AUTHORITY: Final[str] = (
    "ThisIsRegistrationNotAuthority: تجميدٌ قبل القياس بلا حكمٍ ولا ولادةٍ "
    "ولا رفعِ حجبٍ عن طبقةٍ في قاموس بنية الكلمة"
)

SYLLABLE_PREREGISTRATION_NAMED_RESIDUALS: Final[tuple[str, ...]] = (
    AN_UNSEGMENTABLE_WORD_IS_A_NAMED_REFUSAL_NOT_A_NULL,
    NO_THRESHOLD_IS_INVENTED_AFTER_THE_FACT,
    TANWEEN_IS_READ_AS_A_VOWEL_PLUS_A_CLOSING_NUN,
    THE_TEMPLATES_ARE_SIX_AND_CLOSED,
    THE_WAQF_TRANSFORM_IS_A_STATED_INPUT_OPERATION,
    THIS_IS_REGISTRATION_NOT_AUTHORITY,
    WAZN_IS_A_DERIVED_PROJECTION_NOT_A_BORN_OBJECT,
)
"""البواقي المُسمّاةُ لهذه الوحدة، مرتّبةً كما تُرتَّب في بقيّة الطبقة."""


def preregistration_digest() -> str:
    """بصمةُ المُجمَّد: يتغيّر بندٌ فيه فتتغيّر، فتسقط قراءةُ وحدة السيلبنة."""

    registration = layer_registration()
    return canonical_digest(
        canonical_bytes(
            {
                "templates": [template.value for template in SyllableTemplate],
                "structural_acceptance_conditions": [
                    condition.as_canonical_content()
                    for condition in STRUCTURAL_ACCEPTANCE_CONDITIONS
                ],
                "shadda_expansion_rule": SHADDA_EXPANSION_RULE,
                "tanween_reading": TANWEEN_IS_READ_AS_A_VOWEL_PLUS_A_CLOSING_NUN,
                "waqf_transform_rules": [
                    rule.as_canonical_content() for rule in WAQF_TRANSFORM_RULES
                ],
                "wazn_is_a_projection": (
                    WAZN_IS_A_DERIVED_PROJECTION_NOT_A_BORN_OBJECT
                ),
                "layer_entry_condition": registration.entry_condition,
                "layer_refusal_field_name": registration.refusal_field_name,
                "named_residuals": list(SYLLABLE_PREREGISTRATION_NAMED_RESIDUALS),
            }
        )
    )


PREREGISTRATION_DIGEST: Final[str] = preregistration_digest()
"""البصمةُ المُجمَّدة، محسوبةً عند الاستيراد لا مكتوبةً رقمًا في الشيفرة."""


def _refuse_a_template_outside_the_six() -> None:
    """حارسٌ عند الاستيراد: القوالبُ ستّةٌ بأسمائها، والشروطُ البنيويّةُ متمايزة."""

    if len(SyllableTemplate) != 6:
        raise SyllablePreregistrationError("القوالبُ ستّةٌ مغلقةٌ لا سابعَ لها")
    names = [condition.name for condition in STRUCTURAL_ACCEPTANCE_CONDITIONS]
    if len(set(names)) != len(names):
        raise SyllablePreregistrationError("شرطٌ بنيويٌّ تكرّر باسمه")
    rule_names = [rule.name for rule in WAQF_TRANSFORM_RULES]
    if len(set(rule_names)) != len(rule_names):
        raise SyllablePreregistrationError("قاعدةُ وقفٍ تكرّرت باسمها")


_refuse_a_template_outside_the_six()
