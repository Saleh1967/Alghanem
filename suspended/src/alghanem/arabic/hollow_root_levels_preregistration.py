"""تجميدُ سُلَّمِ المستويات على الجذر الأجوف قبل قياسه: صورٌ، وإسقاطاتٌ، وتوقّع.

**السؤالُ الذي وُضِعت هذه الوحدةُ لأجله**: وصلت من محادثةٍ خارجية دعوى «بناءٍ
هرميٍّ» على الجذر الأجوف، مؤدّاها أنّ كلَّ مستوًى يحلّ ما عجز عنه سابقُه. والدعوى
غيرُ قابلةٍ للفحص ما دام «المستوى» عبارةً نثرية؛ فتُجمَّد هنا **إسقاطاتٌ مُسمّاةٌ
مُنفَّذةٌ فعلًا في هذه الشجرة**، ثمّ يقع القياسُ عليها في
`hollow_root_levels_measurement` لا هنا.

`FREEZE_BEFORE_MEASUREMENT`: ليس في هذه الوحدة دالّةُ قياسٍ ولا حقلُ نتيجة،
وحارسٌ عند الاستيراد يمنع تسلُّلَهما لاحقًا — على منوال
`morphological_necessity_probe`. فاختبارٌ يُصاغ هدفُه بعد رؤية أوّل نتيجةٍ
اختبارٌ بُني لينجح.

`A_HAND_BUILT_EXAMPLE_IS_NOT_A_CORPUS_OCCURRENCE`: الصورُ الأربعُ والعشرون
**مُنشأةٌ يدويًّا بصيغٍ كلاسيكيةٍ معروفة**، ولم تُستخرَج من مدوّنةٍ مُبصَّمة. وجنسُ
إسنادها مُصرَّحٌ به في `ExampleProvenance` ولا يُترَك صمتًا، على منوال ما يفصله
`encoding/provenance_genus` بين المرصود والمُصطنَع. ومن قرأ هذه الصورَ شواهدَ
مدوّنيّةً قرأ مُصطنَعًا مرصودًا.

`TWENTY_FOUR_HAND_PICKED_FORMS_ARE_NOT_A_CENSUS`: نطاقُ كلّ ما يُشتَقّ من هذه
الوحدة أربعٌ وعشرون صورةً بأعيانها. وتصادمٌ يقع فيها تصادمٌ واقعٌ فعلًا لا
يُنقَض بعدّ، أمّا **انتفاءُ** التصادم فلا يُقرأ خاصّيّةً في العربية ولا في فئة
الأجوف: عيّنةٌ مُصمَّمةٌ لإظهار تصادمٍ بعينه لا تُقرأ إحصاءً على منوال
`ExhaustedSourceIsNotAnExhaustedWorld`.

`A_LEVEL_EARNS_ITS_PLACE_ONLY_WHERE_ITS_PREDECESSOR_COLLIDES`: لا يُنسَب لمستوًى
فضلُ حسمٍ إلا على زوجٍ **تصادم فيه سابقُه فعلًا**. والقاعدةُ مُجمَّدةٌ هنا قبل
القياس لأنّها هي التي تُسقِط أكثرَ ما وصل من دعاوى: مستوًى يفصل ما كان مفصولًا
سلفًا لم يُثبت لنفسه ضرورة.

`THE_PROJECTIONS_ARE_NAMED_BECAUSE_THEIR_RESULTS_INVERT`: «إسقاطُ الحركات» في
النصّ الوارد غيرُ مُسمًّى، ونتيجتُه **تنقلب** بحسب أيّهما قُصِد: `HARAKAT_STRIPPED`
(وهو `text_key.comparison_key` القائم) يُبقي حرفَ المدّ فلا يتصادم قَالَ وقُلْ،
و`MADD_ALSO_DROPPED` يُسقطه فيتصادمان. فيُجمَّد الاثنان معًا بأسمائهما، ولا
يُطوى أحدُهما في الآخر.

`THIS_IS_REGISTRATION_NOT_AUTHORITY`: لا ولادةَ هنا، ولا حكمَ ولادة، ولا تجميدَ
`E0`، ولا استيرادَ من `kernel/`، ولا تُرفَع بهذه الوحدة حجبٌ عن
`DictionaryLayer.SYLLABLES_AND_WAZN` ولا عن غيرها.
"""

from __future__ import annotations

from dataclasses import dataclass, fields
from enum import Enum
from typing import Final

from ..canonical_content import canonical_bytes, canonical_digest

__all__ = [
    "A_HAND_BUILT_EXAMPLE_IS_NOT_A_CORPUS_OCCURRENCE_NOTE",
    "A_LEVEL_EARNS_ITS_PLACE_ONLY_WHERE_ITS_PREDECESSOR_COLLIDES_NOTE",
    "FREEZE_BEFORE_MEASUREMENT_NOTE",
    "FROZEN_SURFACES",
    "LEVEL_ORDER",
    "NAMED_RESIDUALS",
    "PRE_REGISTERED_EXPECTATION",
    "SURFACE_SET_DIGEST",
    "THE_PROJECTIONS_ARE_NAMED_BECAUSE_THEIR_RESULTS_INVERT_NOTE",
    "THIS_IS_REGISTRATION_NOT_AUTHORITY_NOTE",
    "TWENTY_FOUR_HAND_PICKED_FORMS_ARE_NOT_A_CENSUS_NOTE",
    "ExampleProvenance",
    "FrozenSurface",
    "HollowRootLevel",
    "HollowRootPreregistrationError",
    "surface_set_digest",
]


class HollowRootPreregistrationError(ValueError):
    """رفضٌ عند الإنشاء: صورةٌ بلا جنسِ إسناد، أو جذرٌ خارجَ المُجمَّد."""


class ExampleProvenance(Enum):
    """جنسُ إسناد الصورة. مفردةٌ مغلقةٌ ثنائية، ولا ثالثَ بينهما هنا.

    ولا يُفتَح فيها عضوٌ ثالث: من احتاج جنسًا ليس فيها فقد احتاج تسجيلًا
    قبْليًّا آخر لا عضوًا يُضاف إلى هذه المفردة.
    """

    MANUALLY_CONSTRUCTED_EXAMPLE = "مُنشأةٌ يدويًّا بصيغةٍ كلاسيكيةٍ معروفة"
    MEASURED_CORPUS_OCCURRENCE = "مرصودةٌ في مدوّنةٍ مُبصَّمةٍ بسجلِّ رصد"


class HollowRootLevel(Enum):
    """المستوياتُ الأربعة، كلٌّ منها **إسقاطٌ مُسمًّى مُنفَّذٌ في هذه الشجرة**.

    وقيمةُ كلّ عضوٍ نصُّ الإسقاط لا وصفُ فضله: الفضلُ يُقاس ولا يُعلَن هنا.
    """

    HARAKAT_STRIPPED = "إسقاطُ العلامات وحدها، وهو `text_key.comparison_key` بعينه"
    MADD_ALSO_DROPPED = "إسقاطُ العلامات مع استبعاد حاملِ دور `MADD_EXTENSION`"
    SYLLABLE_TEMPLATE_SEQUENCE = (
        "تتابعُ قوالب المقاطع من `syllabifier.syllabify_surface`"
    )
    CARRIER_STATE_SEQUENCE = "تتابعُ حالات الحامل من `p_extractor.read_surface`"


LEVEL_ORDER: Final[tuple[HollowRootLevel, ...]] = (
    HollowRootLevel.HARAKAT_STRIPPED,
    HollowRootLevel.MADD_ALSO_DROPPED,
    HollowRootLevel.SYLLABLE_TEMPLATE_SEQUENCE,
    HollowRootLevel.CARRIER_STATE_SEQUENCE,
)
"""ترتيبُ المستويات مُجمَّدٌ قبل القياس؛ فترتيبٌ يُعاد بعد النتيجة يصنع الفضل."""


@dataclass(frozen=True, slots=True)
class FrozenSurface:
    """صورةٌ واحدةٌ مُجمَّدة: حروفُها، وجذرُها المُعلَن، وجنسُ إسنادها."""

    surface: str
    declared_root: str
    provenance: ExampleProvenance

    def __post_init__(self) -> None:
        for name in ("surface", "declared_root"):
            value = getattr(self, name)
            if not isinstance(value, str) or not value.strip():
                raise HollowRootPreregistrationError(
                    f"{name} نصٌّ غير فارغ؛ ولا يُترَك صمتًا."
                )
        if not isinstance(self.provenance, ExampleProvenance):
            raise HollowRootPreregistrationError(
                "جنسُ الإسناد عضوٌ من `ExampleProvenance` لا نصٌّ يُكتَب. "
                + A_HAND_BUILT_EXAMPLE_IS_NOT_A_CORPUS_OCCURRENCE_NOTE
            )
        if self.provenance is ExampleProvenance.MEASURED_CORPUS_OCCURRENCE:
            raise HollowRootPreregistrationError(
                "لم تصل إلى هذه الشجرة مدوّنةٌ مُبصَّمةٌ ولا سجلُّ رصدٍ يُطابَق "
                "عليه، فلا تُوسَم صورةٌ هنا مرصودةً. "
                + A_HAND_BUILT_EXAMPLE_IS_NOT_A_CORPUS_OCCURRENCE_NOTE
            )

    def encoded(self) -> dict[str, str]:
        """الصورةُ المُعمَّاة، وهي وحدُها ما تُبصَم عليه البصمةُ المُجمَّدة."""

        return {
            "surface": self.surface,
            "declared_root": self.declared_root,
            "provenance": self.provenance.name,
        }


def _hand_built(surface: str, declared_root: str) -> FrozenSurface:
    return FrozenSurface(
        surface=surface,
        declared_root=declared_root,
        provenance=ExampleProvenance.MANUALLY_CONSTRUCTED_EXAMPLE,
    )


FROZEN_SURFACES: Final[tuple[FrozenSurface, ...]] = (
    _hand_built("قَالَ", "قول"),
    _hand_built("قِيلَ", "قول"),
    _hand_built("يَقُولُ", "قول"),
    _hand_built("يُقَالُ", "قول"),
    _hand_built("قَوْلٌ", "قول"),
    _hand_built("قَائِلٌ", "قول"),
    _hand_built("قُلْ", "قول"),
    _hand_built("بَاعَ", "بيع"),
    _hand_built("بِيعَ", "بيع"),
    _hand_built("يَبِيعُ", "بيع"),
    _hand_built("يُبَاعُ", "بيع"),
    _hand_built("بَيْعٌ", "بيع"),
    _hand_built("بَائِعٌ", "بيع"),
    _hand_built("بِعْ", "بيع"),
    _hand_built("خَافَ", "خوف"),
    _hand_built("يَخَافُ", "خوف"),
    _hand_built("خَوْفٌ", "خوف"),
    _hand_built("خَائِفٌ", "خوف"),
    _hand_built("نَامَ", "نوم"),
    _hand_built("يَنَامُ", "نوم"),
    _hand_built("نَوْمٌ", "نوم"),
    _hand_built("نَائِمٌ", "نوم"),
    _hand_built("هَابَ", "هيب"),
    _hand_built("يَهَابُ", "هيب"),
)
"""الصورُ المُجمَّدة: عشرون من المجموعة الواردة، وصورتا `هيب` للزوج الأدنى.

وصورتا `هَابَ`/`يَهَابُ` مُضافتان عمدًا وبسببٍ مكتوب: `يَخَافُ` (جذرُه واويّ)
و`يَهَابُ` (جذرُه يائيّ) يتطابقان تطابقًا سطحيًّا تامًّا، فهما وحدَهما ما يفصل
«تطابقُ صدفةِ جذرين متشابهين» عن «عمى المستوى عن هويّة العلّة».
"""


def surface_set_digest(surfaces: tuple[FrozenSurface, ...] | None = None) -> str:
    """بصمةُ مجموعة الصور، مُعادةَ الاشتقاق منها لا مُعلَنةً في حقل."""

    frozen = FROZEN_SURFACES if surfaces is None else surfaces
    if not isinstance(frozen, tuple):
        raise HollowRootPreregistrationError("مجموعةُ الصور تعدادٌ مُجمَّد.")
    for surface in frozen:
        if not isinstance(surface, FrozenSurface):
            raise HollowRootPreregistrationError("كلُّ عنصرٍ صورةٌ مُجمَّدةٌ مُصاغة.")
    return canonical_digest(canonical_bytes([item.encoded() for item in frozen]))


SURFACE_SET_DIGEST: Final[str] = (
    "97793356d061eeda4d131e3d11f2c9377ae310ae4cb909bd9651948b793af355"
)
"""البصمةُ المُجمَّدة؛ تُطابَق عند الاستيراد فصورةٌ تُزاد بعدها تُسقِط القراءة."""


FREEZE_BEFORE_MEASUREMENT_NOTE: Final[str] = (
    "FreezeBeforeMeasurement: الصورُ والإسقاطاتُ والتوقّعُ مُجمَّدةٌ قبل أن "
    "تُكتَب دالّةُ قياسٍ واحدة؛ ومن جمّد بأثرٍ رجعيّ برّر ولم يفحص"
)

A_HAND_BUILT_EXAMPLE_IS_NOT_A_CORPUS_OCCURRENCE_NOTE: Final[str] = (
    "AHandBuiltExampleIsNotACorpusOccurrence: الصورُ مُنشأةٌ يدويًّا بصيغٍ "
    "كلاسيكيةٍ معروفة، لا مُستخرَجةٌ من مدوّنةٍ مُبصَّمة؛ فلا يُقرأ منها تردُّدٌ "
    "ولا نسبةٌ ولا غيابُ شاهد"
)

TWENTY_FOUR_HAND_PICKED_FORMS_ARE_NOT_A_CENSUS_NOTE: Final[str] = (
    "TwentyFourHandPickedFormsAreNotACensus: نطاقُ الدعوى هذه الصورُ بأعيانها؛ "
    "وتصادمٌ فيها واقعٌ فعلًا، أمّا انتفاءُ التصادم فخاصّيّةُ العيّنة لا خاصّيّةُ "
    "فئة الأجوف ولا خاصّيّةُ العربية"
)

A_LEVEL_EARNS_ITS_PLACE_ONLY_WHERE_ITS_PREDECESSOR_COLLIDES_NOTE: Final[str] = (
    "ALevelEarnsItsPlaceOnlyWhereItsPredecessorCollides: لا يُنسَب لمستوًى فضلُ "
    "حسمٍ على زوجٍ لم يتصادم فيه سابقُه؛ فمن فصل ما كان مفصولًا سلفًا لم يُثبت "
    "لنفسه ضرورة"
)

THE_PROJECTIONS_ARE_NAMED_BECAUSE_THEIR_RESULTS_INVERT_NOTE: Final[str] = (
    "TheProjectionsAreNamedBecauseTheirResultsInvert: «إسقاطُ الحركات» عبارةٌ "
    "تحتمل إسقاطين تنقلب نتيجتُهما؛ فيُجمَّد الاثنان بأسمائهما ولا يُطوى أحدُهما "
    "في الآخر"
)

THIS_IS_REGISTRATION_NOT_AUTHORITY_NOTE: Final[str] = (
    "ThisIsRegistrationNotAuthority: تجميدٌ قبل القياس بلا حكمٍ ولا ولادةٍ ولا "
    "تجميدِ `E0` ولا رفعِ حجبٍ عن طبقةٍ في قاموس بنية الكلمة"
)

NAMED_RESIDUALS: Final[dict[str, str]] = {
    "FREEZE_BEFORE_MEASUREMENT": FREEZE_BEFORE_MEASUREMENT_NOTE,
    "A_HAND_BUILT_EXAMPLE_IS_NOT_A_CORPUS_OCCURRENCE": (
        A_HAND_BUILT_EXAMPLE_IS_NOT_A_CORPUS_OCCURRENCE_NOTE
    ),
    "TWENTY_FOUR_HAND_PICKED_FORMS_ARE_NOT_A_CENSUS": (
        TWENTY_FOUR_HAND_PICKED_FORMS_ARE_NOT_A_CENSUS_NOTE
    ),
    "A_LEVEL_EARNS_ITS_PLACE_ONLY_WHERE_ITS_PREDECESSOR_COLLIDES": (
        A_LEVEL_EARNS_ITS_PLACE_ONLY_WHERE_ITS_PREDECESSOR_COLLIDES_NOTE
    ),
    "THE_PROJECTIONS_ARE_NAMED_BECAUSE_THEIR_RESULTS_INVERT": (
        THE_PROJECTIONS_ARE_NAMED_BECAUSE_THEIR_RESULTS_INVERT_NOTE
    ),
    "THE_WEAK_RADICAL_IS_NOT_READ_FROM_THE_SURFACE": (
        "TheWeakRadicalIsNotReadFromTheSurface: هويّةُ العلّة (و أم ي) لا "
        "تُشتَقّ في هذه الوحدة من صورةٍ سطحية؛ و`declared_root` حقلٌ **مُعلَنٌ** "
        "مع الصورة لا مُستخرَجٌ منها، ولا تملك هذه الشجرة مستخرِجَ جذورٍ من "
        "الصور أصلًا"
    ),
    "THIS_IS_REGISTRATION_NOT_AUTHORITY": THIS_IS_REGISTRATION_NOT_AUTHORITY_NOTE,
}


PRE_REGISTERED_EXPECTATION: Final[str] = (
    "PreRegisteredExpectation: المُتوقَّعُ قبل القياس أربعةُ أمور، كُتِبت قبل أن "
    "تُكتَب دالّةُ قياسٍ واحدة. **أوّلًا**: يفترق الإسقاطان في المستوى صفر — "
    "`قَالَ` و`قُلْ` لا يتصادمان تحت `HARAKAT_STRIPPED` ويتصادمان تحت "
    "`MADD_ALSO_DROPPED`. **ثانيًا**: يتصادم تتابعُ القوالب عبر جذورٍ مختلفة لا "
    "داخلَ الجذر الواحد وحده. **ثالثًا**: لا يرفع تتابعُ حالات الحامل كلَّ "
    "تصادمٍ يقع في القوالب؛ ويبقى منه ما يبقى. **رابعًا**: يعمى السُّلَّمُ كلُّه "
    "عن هويّة العلّة في `يَخَافُ` و`يَهَابُ` رغم اختلافها، وهذا موافقٌ لحدٍّ "
    "مكتوبٍ في `docs/reference/gflk_arabic_letter_specification.md` **قبل** "
    "طرح هذا السؤال: «فتحة ما قبل مدّ المضارع عمياء بنيويًّا لهوية العلة». "
    "ومطابقةُ التوقّع تأكيدٌ ومخالفتُه مفاجأةٌ تُوثَّق، ولا يُصاغ أحدُهما بعد "
    "وقوعه"
)


_FORBIDDEN_FIELD_MARKERS: Final[tuple[str, ...]] = (
    "outcome",
    "result",
    "verdict",
    "collision",
    "fingerprint",
    "birth",
    "freeze",
    "rank",
)


def _assert_no_outcome_field() -> None:
    """احرسْ خلوَّ وحدة التجميد من حقلِ مُخرَجٍ أو نتيجة؛ فالقياسُ لم يقع بعد."""

    for field in fields(FrozenSurface):
        lowered = field.name.lower()
        for marker in _FORBIDDEN_FIELD_MARKERS:
            if marker in lowered:
                raise RuntimeError(
                    f"FrozenSurface.{field.name} حقلٌ ممنوع: هذه وحدةُ تجميدٍ "
                    "قبل القياس ولا مُخرَج فيها. " + FREEZE_BEFORE_MEASUREMENT_NOTE
                )


def _assert_the_surface_set_is_frozen() -> None:
    """احرسْ مجموعةَ الصور ببصمةٍ مُعادةِ الاشتقاق؛ فصورةٌ تُزاد بعدها تُرَدّ."""

    if len(FROZEN_SURFACES) != 24:  # pragma: no cover - حارسُ بناء
        raise RuntimeError("مجموعةُ الصور أربعٌ وعشرون صورةً مُجمَّدةً لا غير")
    if len({item.surface for item in FROZEN_SURFACES}) != len(FROZEN_SURFACES):
        raise RuntimeError("صورةٌ مكرَّرةٌ في المجموعة تُضاعِف وزنَها في التصادم")
    if len(LEVEL_ORDER) != len(HollowRootLevel):
        raise RuntimeError("ترتيبُ المستويات يستوعب المفردةَ كلَّها لا بعضَها")
    recomputed = surface_set_digest()
    if recomputed != SURFACE_SET_DIGEST:
        raise RuntimeError(
            "مجموعةُ الصور تغيّرت بعد تجميدها: البصمةُ المُعادُ اشتقاقُها "
            f"{recomputed} تخالف المُجمَّدة {SURFACE_SET_DIGEST}. "
            + FREEZE_BEFORE_MEASUREMENT_NOTE
        )


_assert_no_outcome_field()
_assert_the_surface_set_is_frozen()
