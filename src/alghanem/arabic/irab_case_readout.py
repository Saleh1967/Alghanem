"""قراءةُ الحالة الإعرابية من سطح الكلمة، مقيسةً على مدوَّنةٍ خارجيةٍ مُوسَّمة.

**الدعوى التي جاءت إلى هنا ورقمُها الكاذب**: «الكلمةُ التاليةُ للفعل الماضي،
إذا خُتِمت بفتحة، فهي مفعولٌ به»، بدقّةٍ مُعلَنةٍ ١٠٠٪. والرقمُ كان أثرًا من
أداة الفحص لا من اللغة: قورِن نصُّ المتوقَّع بنفسه لا بالحالة المقيسة. ثمّ
صُحِّح إلى ٤٨٪ بفحصٍ سطحيٍّ ثانٍ لم يُقَس على مدوَّنةٍ مُوسَّمة أصلًا.

**والرقمُ الأوّلُ الصادقُ هنا أخفضُ من كليهما**: تُشغَّل الدعوى كما نُطِق بها،
على ٤٢٦٥ موضعًا من مدوَّنةٍ خارجية، فتُصيب ١٤٤٤ — **٣٣٫٩٪**
(`AS_STATED_HYPOTHESIS_BASELINE`). لا ١٠٠٪، ولا ٤٨٪.

**ثمّ أُصلِح ما أمكن إصلاحُه، وسُمِّي ما لا يُصلَح**. والإصلاحاتُ لم تُستنبَط
من نظرٍ بل خرجت من الأمثلة التي طُبِعت عند التشغيل، وكلُّ واحدٍ منها عيبٌ في
الفاحص لا في اللغة:

* **الضميرُ المتّصل يحمل الحركةَ الأخيرة، لا الحالة**: «رَبُّكَ» مرفوعٌ وآخرُه
  فتحةٌ على الكاف. تُجرَّد اللواحقُ المُعلَنة ثمّ تُقرأ الحركة.
* **حرفُ الجرّ الملحق**: «لِلْكَٰفِرِينَ» و«بِـَٔايَٰتِنَا» مجروران، وفحصُ
  الحرف المفرد لا يبلغهما.
* **ما لا علامةَ ظاهرةَ له ليس خطأً بل متعذّر**: «مُوسَىٰ» و«ٱلنَّصَٰرَىٰ»
  مقصوران، و«ٱلصَّٰلِحَٰتِ» جمعُ مؤنّثٍ سالمٍ يُنصَب بالكسرة، و«ٱلْكَٰفِرِينَ»
  يُعلَم بالحرف لا بالحركة. فالمنزلةُ الثالثة (`متعذّر_القياس`) مفردةٌ مستقلّة
  لا تُجمَع أبدًا مع (`خطأ`) — على منوال `RefusalIsNotFailureToDiscriminate`
  في `morphological_necessity_measurement`. والخلطُ بين الغياب والتعذّر هو
  البابُ الوحيد الذي تُصنَع منه دقّةٌ زائفة، في الاتجاهين معًا.
* **ترتيبُ الشدّة والفتحة**: «ٱللَّهُ» قُرِئت منصوبةً لأنّ الشدّة سبقت الفتحة
  في بايتات المدوَّنة وتلتها في حروف هذه الشجرة. لا حيلةَ لفظيةَ هنا: يُطبَّق
  `NFC` قبل كلِّ مقارنة، ويُسجَّل إصدارُ قاعدة Unicode مع القياس —
  وهو عينُ ما تفرضه `arabic/encoding/measurement.py` على كلِّ مسارٍ مقيس.

**والرقمُ بعد الإصلاح ٩٧٫١٪ على قسمٍ محجوب، لا ٩٧٫٤٪ على الكلّ**
(`TUNED_ON_DEV_REPORTED_ON_HELD_OUT`): القواعدُ أعلاه اختيرت **بعد** رؤية أخطاء
المدوَّنة، فقياسُها على المواضع نفسِها ملاءمةٌ لا تنبّؤ. فقُسِّمت المدوَّنةُ
بقاعدةٍ لا علاقةَ لها بالجواب (زوجيّةُ رقم السورة)، وطُوِّرت القواعدُ على القسم
الزوجيّ وحده، ويُقرأ الرقمُ المُعلَنُ من القسم الفرديِّ المحجوب. والرقمان
مُودَعان كلاهما، لأنّ فرقهما هو مقدارُ الملاءمة، وإخفاءُ أحدهما إخفاءٌ له.

**وأخطرُ ما في هذه الوحدة أنّها لا تقيس الدعوى الأصلية أصلًا**
(`ACCUSATIVE_IS_NOT_OBJECTHOOD`): المدوَّنةُ المُوسَّمةُ المقيسُ عليها تُوسِّم
**الحالةَ** (`NOM`/`ACC`/`GEN`) لا **الوظيفةَ** (فاعل/مفعول به). فالنصبُ يقع
للمفعول به وللحال وللتمييز وللظرف ولاسم `إنّ` وللمفعول المطلق. فالمُثبَتُ هنا
أنّ قارئًا سطحيًّا يقرأ **علامةَ الإعراب** بدقّةٍ عالية، لا أنّ الفتحة تدلّ على
المفعولية. والدعوى الأصليةُ باقيةٌ غيرَ مقيسة، ولا يجوز أن يُقرأ ٩٧٫١٪ جوابًا
عنها؛ وقياسُها يحتاج شجرةَ الإعراب النحويّ لا ملفَّ الصرف.

**وما بقي خطأً سُمِّي ولم يُلطَّف** (`NAMED_RESIDUAL_ERROR_GENERA`): الممنوعُ
من الصرف يُجَرّ بالفتحة («جَهَنَّمَ»، «ثَمُودَ»)، والمنادى المضافُ المحذوفُ ياؤه
يُقرأ مجرورًا («رَبِّ»)، و«لِقَآءَ» لامُه من بنية الكلمة لا حرفَ جرّ. وهذه
ليست عيوبَ تنفيذٍ تُغلَق بسطر، بل حدودُ قارئٍ سطحيٍّ لا يعرف بنيةَ الكلمة.

**والمدى مُقيَّدٌ بالمدوَّنة** (`ACCURACY_IS_CORPUS_BOUNDED`): ٩٧٫١٪ على نصٍّ
مُبَصَّمٍ واحد، لا على العربية؛ واستنفادُ مدوَّنةٍ ليس استنفادَ لغةٍ، على منوال
`CompleteInductionIsCorpusBounded`.

وهذه الوحدة تسجيلٌ لا سلطة: لا ولادةَ فيها، ولا حكمَ ولادة، ولا تجميدَ `E0`،
ولا تستورد من `kernel/` شيئًا، ولا تقرؤها وحدةٌ فيه. وبايتاتُ المدوَّنة غيرُ
منسوخةٍ إلى الشجرة؛ انظر `irab_corpus_witness`.
"""

from __future__ import annotations

import unicodedata
from dataclasses import dataclass
from enum import Enum
from typing import Final, Literal

from .irab_corpus_witness import QURANIC_ARABIC_CORPUS_WITNESS, IrabCorpusWitness

__all__ = [
    "ACCURACY_IS_CORPUS_BOUNDED_NOTE",
    "ACCUSATIVE_IS_NOT_OBJECTHOOD_NOTE",
    "AS_STATED_HYPOTHESIS_BASELINE",
    "DEVELOPMENT_SPLIT_MEASUREMENT",
    "HELD_OUT_SPLIT_MEASUREMENT",
    "IRAB_CASE_READOUT_NAMED_RESIDUALS",
    "NAMED_RESIDUAL_ERROR_GENERA",
    "NORMALIZATION_FORM",
    "TUNED_ON_DEV_REPORTED_ON_HELD_OUT_NOTE",
    "UNICODE_DATABASE_VERSION",
    "UNTESTABLE_IS_NOT_WRONG_NOTE",
    "WHOLE_CORPUS_MEASUREMENT",
    "CaseReadout",
    "CaseReadoutError",
    "CaseReadoutMeasurement",
    "ReadoutGenus",
    "SurfaceCaseReading",
    "development_split_contains",
    "read_surface_case",
]


class CaseReadoutError(ValueError):
    """تُرفَع حين يُبنى قياسٌ لا تتّسق أعدادُه أو لا يُعاد به اشتقاقُ رقم."""


NORMALIZATION_FORM: Final[Literal["NFC"]] = "NFC"

UNICODE_DATABASE_VERSION: Final[str] = "15.0.0"


class CaseReadout(Enum):
    """منزلةُ القراءة السطحية: ثلاثُ حالاتٍ ورابعةٌ للتعذّر، لا ثنائية.

    والمنزلةُ الرابعةُ ليست حالةً إعرابيةً خامسة؛ هي تصريحٌ بأنّ السطحَ لا يحمل
    علامةً تُقرَأ أصلًا. وجمعُها مع `خطأ` يُنقِص الدقّةَ بغير وجه، وجمعُها مع
    `صواب` يرفعُها بغير وجه؛ فهي مفردةٌ مستقلّةٌ لا تُجمَع مع أيٍّ منهما.
    """

    منصوب = "منصوب"
    مرفوع = "مرفوع"
    مجرور = "مجرور"
    متعذّر_القياس = "متعذّر_القياس"


class ReadoutGenus(Enum):
    """جنسُ القاعدة التي أنتجت القراءة؛ يُسمّى ليُعرَف موضعُ الخطأ لا عددُه."""

    تنوين = "تنوين"
    فتحة = "فتحة"
    ضمة = "ضمة"
    كسرة = "كسرة"
    جمع_مذكر_سالم_بالواو = "جمع_مذكر_سالم_بالواو"
    مثنى_بالألف = "مثنى_بالألف"
    حرف_جر_ملحق = "حرف_جر_ملحق"
    لفظ_الجلالة = "لفظ_الجلالة"
    منادى_لا_علامة_له = "منادى_لا_علامة_له"
    جمع_مذكر_سالم_بالياء_ملتبس = "جمع_مذكر_سالم_بالياء_ملتبس"
    مثنى_بالياء_ملتبس = "مثنى_بالياء_ملتبس"
    جمع_مؤنث_سالم_ملتبس = "جمع_مؤنث_سالم_ملتبس"
    مقصور_لا_علامة_ظاهرة = "مقصور_لا_علامة_ظاهرة"
    منقوص_لا_علامة_ظاهرة = "منقوص_لا_علامة_ظاهرة"
    ساكن_موقوف = "ساكن_موقوف"
    لا_حركة_أخيرة = "لا_حركة_أخيرة"


# --- الحروف والمفردات المُعلَنة ---------------------------------------------
#
# `VOCABULARIES_ARE_DECLARED_NOT_DERIVED`: هذه المفرداتُ مكتوبةٌ بالاسم، لا
# مُشتَقّةٌ من خاصّيةٍ للعربية ولا من إحصاءٍ على المدوَّنة — على منوال
# `CARRIER_SET_IS_DECLARED_NOT_DERIVED` في `encoding/carrier_state_candidate`.
# فمن أراد توسيعَها وسَّعها بالاسم، ولا تتوسّع من نفسها بلا أثر.

_FATHA: Final[str] = "\u064e"
_DAMMA: Final[str] = "\u064f"
_KASRA: Final[str] = "\u0650"
_FATHATAN: Final[str] = "\u064b"
_DAMMATAN: Final[str] = "\u064c"
_KASRATAN: Final[str] = "\u064d"
_SUKUN: Final[str] = "\u0652"
_DAGGER_ALIF: Final[str] = "\u0670"

_SHORT_VOWELS: Final[frozenset[str]] = frozenset(
    {_FATHA, _DAMMA, _KASRA, _FATHATAN, _DAMMATAN, _KASRATAN}
)

_TANWIN_CASE: Final[dict[str, CaseReadout]] = {
    _FATHATAN: CaseReadout.منصوب,
    _DAMMATAN: CaseReadout.مرفوع,
    _KASRATAN: CaseReadout.مجرور,
}

_SHORT_VOWEL_CASE: Final[dict[str, CaseReadout]] = {
    _FATHA: CaseReadout.منصوب,
    _DAMMA: CaseReadout.مرفوع,
    _KASRA: CaseReadout.مجرور,
}

_RECITATION_MARKS: Final[frozenset[str]] = frozenset(
    chr(code) for code in range(0x06D6, 0x06EE)
) | frozenset({"\u0653", "\u0654", "\u0655"})

_ATTACHED_PRONOUNS: Final[tuple[str, ...]] = (
    "هُمَا",
    "هِمَا",
    "كُمَا",
    "هُنَّ",
    "هِنَّ",
    "كُنَّ",
    "هُمُ",
    "هِمُ",
    "كُمُ",
    "هُمْ",
    "هِمْ",
    "كُمْ",
    "هُم",
    "هِم",
    "كُم",
    "نَا",
    "نِي",
    "هَا",
    "كَ",
    "كِ",
    "هُ",
    "هِ",
)

_FIRST_PERSON_YA: Final[tuple[str, ...]] = ("ىَّ", "ِىَ", "ِيَ", "ىَ", "ىِ")

_LEADING_PARTICLES: Final[tuple[str, ...]] = ("وَ", "فَ", "أَ", "تَ", "لَ")

_BOUND_PREPOSITIONS: Final[tuple[str, ...]] = ("لِ", "بِ")

_DIVINE_NAME_FORMS: Final[dict[str, CaseReadout]] = {
    "ٱللَّهُ": CaseReadout.مرفوع,
    "ٱللَّهِ": CaseReadout.مجرور,
    "ٱللَّهَ": CaseReadout.منصوب,
    "اللَّهُ": CaseReadout.مرفوع,
    "اللَّهِ": CaseReadout.مجرور,
    "اللَّهَ": CaseReadout.منصوب,
}

_VOCATIVE_PREFIX: Final[str] = "يَٰ"

_MINIMUM_STEM_LENGTH: Final[int] = 3


@dataclass(frozen=True, slots=True)
class SurfaceCaseReading:
    """قراءةٌ واحدة: منزلتُها، وجنسُ القاعدة التي أنتجتها، والصورةُ المقروءة."""

    surface: str
    readout: CaseReadout
    genus: ReadoutGenus

    def __post_init__(self) -> None:
        if not isinstance(self.surface, str) or not self.surface:
            raise CaseReadoutError("الصورةُ المقروءةُ نصٌّ غير فارغ.")
        if not isinstance(self.readout, CaseReadout):
            raise CaseReadoutError("المنزلةُ عضوٌ في `CaseReadout` لا نصٌّ حرّ.")
        if not isinstance(self.genus, ReadoutGenus):
            raise CaseReadoutError("جنسُ القاعدة عضوٌ في `ReadoutGenus` لا نصٌّ حرّ.")


def _strip_recitation_marks(surface: str) -> str:
    return "".join(
        character for character in surface if character not in _RECITATION_MARKS
    )


def _strip_leading_particle(surface: str) -> str:
    for particle in _LEADING_PARTICLES:
        if surface.startswith(particle):
            return surface[len(particle) :]
    return surface


def _strip_attached_pronoun(surface: str) -> str:
    for suffix in _FIRST_PERSON_YA:
        if surface.endswith(suffix) and len(surface) - len(suffix) >= (
            _MINIMUM_STEM_LENGTH
        ):
            return surface[: -len(suffix)]
    for suffix in _ATTACHED_PRONOUNS:
        if surface.endswith(suffix) and len(surface) - len(suffix) >= (
            _MINIMUM_STEM_LENGTH
        ):
            return surface[: -len(suffix)]
    return surface


def _final_short_vowel(surface: str) -> str | None:
    for character in reversed(surface):
        if character in _SHORT_VOWELS:
            return character
        if character == _SUKUN:
            return _SUKUN
    return None


def _trailing_tanwin(surface: str) -> str | None:
    for character in reversed(surface):
        if character in _TANWIN_CASE:
            return character
        if character in _SHORT_VOWELS or character == _SUKUN:
            return None
    return None


def read_surface_case(surface: str) -> SurfaceCaseReading:
    """اقرأ الحالةَ الإعرابيةَ من سطح الكلمة وحده، بلا معجمٍ ولا وَسْمٍ مسبق.

    والترتيبُ أدناه جزءٌ من القاعدة لا تفصيلُ تنفيذ: العلامةُ بالحرف تسبق
    العلامةَ بالحركة، والمُلتبِسُ يُصرَّح بالتعذّر قبل أن تُقرَأ حركتُه، وإلّا
    قُرِئت كسرةُ «ٱلصَّٰلِحَٰتِ» جرًّا وهي نصب.
    """

    if not isinstance(surface, str) or not surface.strip():
        raise CaseReadoutError("الكلمةُ المقروءةُ نصٌّ غير فارغ؛ ولا تُقرَأ من صمت.")
    normalized = unicodedata.normalize(NORMALIZATION_FORM, surface)
    tail = _strip_recitation_marks(normalized)
    bare = _strip_leading_particle(tail)
    divine = _DIVINE_NAME_FORMS.get(bare)
    if divine is not None:
        return SurfaceCaseReading(surface, divine, ReadoutGenus.لفظ_الجلالة)
    if tail.startswith(_VOCATIVE_PREFIX) or bare.startswith(_VOCATIVE_PREFIX):
        return SurfaceCaseReading(
            surface, CaseReadout.متعذّر_القياس, ReadoutGenus.منادى_لا_علامة_له
        )
    stem = _strip_attached_pronoun(tail).rstrip(_SUKUN)
    for ending, readout, genus in (
        ("ونَ", CaseReadout.مرفوع, ReadoutGenus.جمع_مذكر_سالم_بالواو),
        ("ينَ", CaseReadout.متعذّر_القياس, ReadoutGenus.جمع_مذكر_سالم_بالياء_ملتبس),
        ("انِ", CaseReadout.مرفوع, ReadoutGenus.مثنى_بالألف),
        ("يْنِ", CaseReadout.متعذّر_القياس, ReadoutGenus.مثنى_بالياء_ملتبس),
    ):
        if stem.endswith(ending):
            return SurfaceCaseReading(surface, readout, genus)
    if len(stem) >= 2 and stem[-1] in {_KASRA, _KASRATAN, _FATHA, _FATHATAN}:
        if stem[-2] == "ت" and len(stem) >= 3 and stem[-3] in {"ا", "ٰ", _DAGGER_ALIF}:
            return SurfaceCaseReading(
                surface, CaseReadout.متعذّر_القياس, ReadoutGenus.جمع_مؤنث_سالم_ملتبس
            )
    # ألفُ تنوين النصب («كَثِيرًا») ليست ألفَ المقصور («مُوسَىٰ»): يفرّق بينهما
    # التنوينُ الذي يسبقها، وقراءتُها مقصورًا تُسقِط المنصوبَ الصريحَ كلَّه في
    # خانة المتعذّر فتُجمِّل النسبةَ بإخفاء المقام.
    if len(stem) >= 2 and stem[-1] == "ا" and stem[-2] == _FATHATAN:
        return SurfaceCaseReading(surface, CaseReadout.منصوب, ReadoutGenus.تنوين)
    if stem and stem[-1] in {"ى", "ا", "ٰ", _DAGGER_ALIF}:
        return SurfaceCaseReading(
            surface, CaseReadout.متعذّر_القياس, ReadoutGenus.مقصور_لا_علامة_ظاهرة
        )
    if (
        len(stem) >= 2
        and stem[-1] in _TANWIN_CASE
        and stem[-2] in {"ى", "ا", "ٰ", _DAGGER_ALIF}
    ):
        return SurfaceCaseReading(
            surface, CaseReadout.متعذّر_القياس, ReadoutGenus.مقصور_لا_علامة_ظاهرة
        )
    tanwin = _trailing_tanwin(stem)
    if tanwin is not None:
        return SurfaceCaseReading(surface, _TANWIN_CASE[tanwin], ReadoutGenus.تنوين)
    if stem.endswith("ي"):
        return SurfaceCaseReading(
            surface, CaseReadout.متعذّر_القياس, ReadoutGenus.منقوص_لا_علامة_ظاهرة
        )
    body = _strip_leading_particle(stem)
    if body.startswith(_BOUND_PREPOSITIONS):
        return SurfaceCaseReading(surface, CaseReadout.مجرور, ReadoutGenus.حرف_جر_ملحق)
    vowel = _final_short_vowel(stem)
    if vowel is None:
        return SurfaceCaseReading(
            surface, CaseReadout.متعذّر_القياس, ReadoutGenus.لا_حركة_أخيرة
        )
    if vowel == _SUKUN:
        return SurfaceCaseReading(
            surface, CaseReadout.متعذّر_القياس, ReadoutGenus.ساكن_موقوف
        )
    genus = {
        _FATHA: ReadoutGenus.فتحة,
        _DAMMA: ReadoutGenus.ضمة,
        _KASRA: ReadoutGenus.كسرة,
    }[vowel]
    return SurfaceCaseReading(surface, _SHORT_VOWEL_CASE[vowel], genus)


def development_split_contains(sura_number: int) -> bool:
    """أفي قسمِ التطوير هذه السورة؟ القاعدةُ زوجيةُ رقمها، لا شيءَ سواها.

    وقاعدةُ القسمة مكتوبةٌ هنا مرّةً واحدة ولا علاقةَ لها بجواب القياس، فلا
    تُنتقى بعد رؤيته؛ ومن قسّم بقاعدةٍ تعتمد على النتيجة قسَّم ليَربح.
    """

    if not isinstance(sura_number, int) or sura_number < 1:
        raise CaseReadoutError("رقمُ السورة عددٌ صحيحٌ موجب.")
    return sura_number % 2 == 0


@dataclass(frozen=True, slots=True)
class CaseReadoutMeasurement:
    """قياسٌ مُجمَّدٌ على شاهدٍ مُبَصَّم؛ نسبتُه مُشتَقّةٌ من أعداده لا مكتوبة."""

    witness: IrabCorpusWitness
    split: str
    normalization_form: str
    unicode_database_version: str
    population: int
    correct: int
    wrong: int
    untestable: int

    def __post_init__(self) -> None:
        if not isinstance(self.witness, IrabCorpusWitness):
            raise CaseReadoutError("الشاهدُ عضوٌ في نوعه لا نصٌّ حرّ.")
        if not isinstance(self.split, str) or not self.split.strip():
            raise CaseReadoutError("اسمُ القسم نصٌّ غير فارغ؛ وقياسٌ بلا قسمٍ مُبهَم.")
        if self.normalization_form != NORMALIZATION_FORM:
            raise CaseReadoutError(
                "صيغةُ التطبيع تُطابق صيغةَ الوحدة؛ وقياسٌ بصيغةٍ أخرى قياسٌ "
                "على حروفٍ أخرى."
            )
        if (
            not isinstance(self.unicode_database_version, str)
            or not self.unicode_database_version.strip()
        ):
            raise CaseReadoutError("إصدارُ قاعدة Unicode نصٌّ غير فارغ.")
        for value, label in (
            (self.population, "حجمُ المجتمع"),
            (self.correct, "عددُ الصواب"),
            (self.wrong, "عددُ الخطأ"),
            (self.untestable, "عددُ المتعذّر"),
        ):
            if not isinstance(value, int) or value < 0:
                raise CaseReadoutError(f"{label} عددٌ صحيحٌ غيرُ سالب.")
        if self.correct + self.wrong + self.untestable != self.population:
            raise CaseReadoutError(
                "الصوابُ والخطأُ والمتعذّرُ يستغرقون المجتمعَ كلَّه؛ وفرقٌ بينهما "
                "وبينه يعني موضعًا سقط من العدّ بلا منزلة."
            )
        if self.correct + self.wrong == 0:
            raise CaseReadoutError(
                "قياسٌ لم يُحسَم فيه موضعٌ واحد لا تُشتَقّ منه نسبة؛ ونسبةٌ من "
                "صفرٍ رقمٌ مصنوع."
            )

    @property
    def decided(self) -> int:
        """عددُ المواضع التي حُسِمت؛ والمتعذّرُ ليس منها."""

        return self.correct + self.wrong

    @property
    def accuracy_on_decided(self) -> float:
        """نسبةُ الصواب من المحسوم وحده؛ مُشتَقّةٌ لا مكتوبة."""

        return self.correct / self.decided

    @property
    def untestable_share(self) -> float:
        """حصّةُ المتعذّر من المجتمع؛ تُعلَن مع النسبة ولا تُطوى تحتها.

        فدقّةٌ عاليةٌ على محسومٍ ضئيلٍ دقّةٌ على قليل، وإخفاءُ المقام يُوهِم
        بشمولٍ لم يُقَس.
        """

        return self.untestable / self.population


ACCUSATIVE_IS_NOT_OBJECTHOOD_NOTE: Final[str] = (
    "AccusativeIsNotObjecthood: المدوَّنةُ المقيسُ عليها تُوسِّم الحالةَ "
    "(`NOM`/`ACC`/`GEN`) لا الوظيفةَ النحوية؛ والنصبُ يقع للمفعول به وللحال "
    "وللتمييز وللظرف ولاسم `إنّ` وللمفعول المطلق. فالمقيسُ هنا قراءةُ علامة "
    "الإعراب، والدعوى الأصلية «الفتحةُ تدلّ على المفعولية» باقيةٌ غيرَ مقيسة"
)

TUNED_ON_DEV_REPORTED_ON_HELD_OUT_NOTE: Final[str] = (
    "TunedOnDevReportedOnHeldOut: قواعدُ القراءة اختيرت بعد رؤية أخطاء القسم "
    "الزوجيّ، فرقمُه ملاءمةٌ لا تنبّؤ؛ والرقمُ المُعلَنُ من القسم الفرديِّ "
    "المحجوب، والفرقُ بينهما مقدارُ الملاءمة فيُودَعان معًا"
)

UNTESTABLE_IS_NOT_WRONG_NOTE: Final[str] = (
    "UntestableIsNotWrong: ما لا علامةَ ظاهرةَ له — مقصورٌ، ومنقوصٌ، وجمعُ "
    "مؤنّثٍ سالم، وجمعُ مذكّرٍ سالمٍ بالياء — لا يُحسَب خطأً ولا صوابًا؛ "
    "وجمعُه مع أحدهما يُحرّك النسبةَ في اتجاهٍ مُختار"
)

ACCURACY_IS_CORPUS_BOUNDED_NOTE: Final[str] = (
    "AccuracyIsCorpusBounded: النسبةُ على نصٍّ مُبَصَّمٍ واحدٍ مُغلَق، لا على "
    "العربية؛ واستنفادُ مدوَّنةٍ ليس استنفادَ لغة"
)

NAMED_RESIDUAL_ERROR_GENERA: Final[dict[str, str]] = {
    "ممنوع_من_الصرف": (
        "«جَهَنَّمَ» و«ثَمُودَ» و«دَاوُۥدَ» تُجَرّ بالفتحة، فيقرؤها القارئُ "
        "السطحيُّ منصوبةً. وهذا حدُّ قارئٍ لا يعرف بنيةَ الكلمة، لا عيبُ سطر"
    ),
    "منادى_مضاف_محذوف_الياء": (
        "«رَبِّ» في النداء آخرُها كسرةٌ وهي منصوبةٌ بالإضافة؛ ولا تُميَّز عن "
        "المجرور بالسطح وحده"
    ),
    "لام_من_بنية_الكلمة": (
        "«لِقَآءَ» لامُها من حروف الكلمة لا حرفَ جرّ؛ وقاعدةُ الحرف الملحق "
        "تقرؤها جرًّا. ولا يُغلَق هذا إلا بمعجمٍ أو تحليلٍ صرفيٍّ غيرِ قائمٍ هنا"
    ),
}

IRAB_CASE_READOUT_NAMED_RESIDUALS: Final[dict[str, str]] = {
    "AccusativeIsNotObjecthood": ACCUSATIVE_IS_NOT_OBJECTHOOD_NOTE,
    "TunedOnDevReportedOnHeldOut": TUNED_ON_DEV_REPORTED_ON_HELD_OUT_NOTE,
    "UntestableIsNotWrong": UNTESTABLE_IS_NOT_WRONG_NOTE,
    "AccuracyIsCorpusBounded": ACCURACY_IS_CORPUS_BOUNDED_NOTE,
}


@dataclass(frozen=True, slots=True)
class AsStatedHypothesisBaseline:
    """تشغيلُ الدعوى كما نُطِق بها، بلا استثناءٍ ولا منزلةٍ ثالثة.

    وهذا هو الرقمُ الذي تستحقّه الدعوى الأصلية: كلُّ كلمةٍ تلي فعلًا ماضيًا
    وآخرُ حركةٍ فيها فتحةٌ تُحسَب مفعولًا به، ويُقابَل ذلك بوَسْم المدوَّنة.
    """

    witness: IrabCorpusWitness
    predicted_positive: int
    accusative_in_gold: int
    claimed_accuracy_before_measurement: str

    def __post_init__(self) -> None:
        if not isinstance(self.witness, IrabCorpusWitness):
            raise CaseReadoutError("الشاهدُ عضوٌ في نوعه لا نصٌّ حرّ.")
        for value, label in (
            (self.predicted_positive, "عددُ المواضع المتوقَّعة"),
            (self.accusative_in_gold, "عددُ الموافق منها للوَسْم"),
        ):
            if not isinstance(value, int) or value < 0:
                raise CaseReadoutError(f"{label} عددٌ صحيحٌ غيرُ سالب.")
        if self.predicted_positive == 0:
            raise CaseReadoutError("دعوى لم تتنبّأ بموضعٍ واحد لا تُقاس.")
        if self.accusative_in_gold > self.predicted_positive:
            raise CaseReadoutError("الموافقُ لا يتجاوز المتوقَّع؛ وهذان تصريحان متناقضان.")
        if (
            not isinstance(self.claimed_accuracy_before_measurement, str)
            or not self.claimed_accuracy_before_measurement.strip()
        ):
            raise CaseReadoutError(
                "الدقّةُ المُدّعاةُ قبل القياس تُنقَل بحروفها؛ وطيُّها يُخفي "
                "الفرقَ بين ما ادُّعي وما قِيس."
            )

    @property
    def measured_precision(self) -> float:
        """الدقّةُ المقيسةُ على ما تنبّأت به الدعوى؛ مُشتَقّةٌ لا مكتوبة."""

        return self.accusative_in_gold / self.predicted_positive


AS_STATED_HYPOTHESIS_BASELINE: Final[AsStatedHypothesisBaseline] = (
    AsStatedHypothesisBaseline(
        witness=QURANIC_ARABIC_CORPUS_WITNESS,
        predicted_positive=4265,
        accusative_in_gold=1444,
        claimed_accuracy_before_measurement=(
            "ادُّعيت ١٠٠٪ أوّلًا، وهو أثرُ أداةِ فحصٍ قارنت نصَّ المتوقَّع بنفسه؛ "
            "ثمّ ٤٨٪ بفحصٍ سطحيٍّ ثانٍ لم يُقَس على مدوَّنةٍ مُوسَّمة. والمقيسُ "
            "على مدوَّنةٍ مُوسَّمةٍ أخفضُ من كليهما"
        ),
    )
)

DEVELOPMENT_SPLIT_MEASUREMENT: Final[CaseReadoutMeasurement] = CaseReadoutMeasurement(
    witness=QURANIC_ARABIC_CORPUS_WITNESS,
    split="سور_زوجية_قسم_التطوير",
    normalization_form=NORMALIZATION_FORM,
    unicode_database_version=UNICODE_DATABASE_VERSION,
    population=2045,
    correct=1609,
    wrong=38,
    untestable=398,
)

HELD_OUT_SPLIT_MEASUREMENT: Final[CaseReadoutMeasurement] = CaseReadoutMeasurement(
    witness=QURANIC_ARABIC_CORPUS_WITNESS,
    split="سور_فردية_قسم_محجوب",
    normalization_form=NORMALIZATION_FORM,
    unicode_database_version=UNICODE_DATABASE_VERSION,
    population=2025,
    correct=1609,
    wrong=48,
    untestable=368,
)

WHOLE_CORPUS_MEASUREMENT: Final[CaseReadoutMeasurement] = CaseReadoutMeasurement(
    witness=QURANIC_ARABIC_CORPUS_WITNESS,
    split="المدونة_كلها",
    normalization_form=NORMALIZATION_FORM,
    unicode_database_version=UNICODE_DATABASE_VERSION,
    population=4070,
    correct=3218,
    wrong=86,
    untestable=766,
)
