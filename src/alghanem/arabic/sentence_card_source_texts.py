"""نصوصٌ مصدريةٌ **زُوِّدت** لبنودٍ من بطاقة الجملة، بحروفها وبجنس تحقُّق موضعها.

التسجيلُ المسبق في `sentence_card_preregistration` جمَّد بطاقةَ الأسئلة وسجَّل
عشرةَ بنودٍ تنتظر نصًّا مصدريًّا. وهذه الوحدةُ **موضعُ ما زُوِّد منها فعلًا**، لا
موضعُ جوابها: تَنقُل الحروفَ وتُسمّي موضعَها وتُعلِن **جنسَ التحقّق من ذلك
الموضع**، ولا تُصنِّف ولا تُقرِّر ولا تُصدِر شهادة::

    SuppliedText  != FormalCertificate
    NamedLocus    != CollatedLocus

**ومرتبةُ تحقُّق الموضع ثلاثيةٌ مغلقة، وأوسطُها هو الجديد** الذي أوجبه هذا
النقل: موضعٌ لم يُقابَل بشيء (`موضع_غير_متحقق`)، وموضعٌ **ترقيمُه ترقيمُ طبعةٍ
ورقيةٍ مُسمّاةٍ مُضمَّنٌ في شاهدٍ رقميّ ولم يُقابَل باليد**
(`ترقيم_طبعة_مرمز_رقميا_غير_مقابل`)، وموضعٌ قوبل بنسخةٍ ورقيةٍ محقَّقةٍ في اليد
(`مقابل_بنسخة_ورقية_محققة`). **والثالثُ عضوٌ بلا مدخلٍ اليوم**، على منوال بقاء
`متواتر` عضوًا بلا مدخلٍ في `transmission_standing`؛ وبقاؤه مُسمًّى هو ما يجعل
الوسطَ مرتبةً وسطى لا سقفًا.

**والنقلُ اقتباساتٌ قصيرةٌ مُسنَدة لا نسخُ مادةٍ بجهد توسيمها**
(`DigitalWitnessTaggingIsNotQuotedWholesale`): متنُ «لسان العرب» لابن منظور
(ت٧١١هـ) مِلكٌ عامٌّ في نفسه، والذي قد يحمل جهدًا محميًّا هو **التوسيمُ والترقيمُ
الرقميّان** في الشاهد المُعتمَد؛ فتُنقَل هنا مقاطعُ قصيرةٌ يحمل كلٌّ منها اسمَ
سلطته نصًّا، ولا تُنسَخ المادةُ كاملةً ببنيتها المُوسَّمة.

**ولا سلطةَ لهذه الوحدة**: لا ولادةَ، ولا حكمَ ولادةٍ، ولا تجميد، ولا `E0`، ولا
تقرؤها بوّابةٌ في `kernel/`، ولا تدخل في `BirthExperimentSpecification`.
"""

from __future__ import annotations

from dataclasses import dataclass, fields
from enum import Enum
from types import MappingProxyType
from typing import Final

from .sentence_card_preregistration import CardItem, FrozenReference
from .text_key import comparison_key

__all__ = [
    "DIGITAL_WITNESS_TAGGING_IS_NOT_QUOTED_WHOLESALE_NOTE",
    "ISHTIQAQ_SARF_LISAN_NUR",
    "KHABAR_INSHA_SHAKHSIYYA_THREE",
    "LISAN_DIGITAL_WITNESS",
    "MUTABAQA_TADAMMUN_ILTIZAM_SHAKHSIYYA_THREE",
    "PUBLIC_DOMAIN_MATN_IS_NOT_AN_OPEN_LICENCE_NOTE",
    "SUPPLIED_SOURCE_TEXTS",
    "SUPPLIED_TEXT_IS_NOT_A_CERTIFICATE_NOTE",
    "WAZN_LISAN_NUR",
    "DigitalWitness",
    "LocusVerification",
    "SourceTextError",
    "SuppliedSourceText",
    "require_attested_excerpt",
    "supplied_text_for",
]


class SourceTextError(ValueError):
    """رُفض نقلٌ خارج شرطه؛ ولا يُحمَل على أقرب حالةٍ مقبولة."""


class LocusVerification(Enum):
    """جنسُ التحقّق من الموضع؛ ثلاثيٌّ مغلق، وأعلاه عضوٌ بلا مدخلٍ اليوم."""

    موضع_غير_متحقق = "موضع_غير_متحقق"
    ترقيم_طبعة_مرمز_رقميا_غير_مقابل = "ترقيم_طبعة_مرمز_رقميا_غير_مقابل"
    مقابل_بنسخة_ورقية_محققة = "مقابل_بنسخة_ورقية_محققة"


SUPPLIED_TEXT_IS_NOT_A_CERTIFICATE_NOTE: Final[str] = (
    "SuppliedTextIsNotAFormalCertificate: تزويدُ النصّ يرفع نقصَ النقل وحده، "
    "ولا يُنشئ مجالًا مُجمَّدًا ولا دالّةَ قرارٍ ولا حاملًا يُشتَقّ منه؛ فالبندُ "
    "المُزوَّدُ نصُّه يبقى غيرَ مُشتَقٍّ حتى تقوم له شهادةٌ صوريةٌ في موضعها"
)

PUBLIC_DOMAIN_MATN_IS_NOT_AN_OPEN_LICENCE_NOTE: Final[str] = (
    "PublicDomainMatnIsNotAnOpenLicence: كونُ المتن تراثيًّا مِلكًا عامًّا لا "
    "يجعل كلَّ شاهدٍ رقميٍّ له مُرخَّصًا بإطلاق؛ فالمتنُ شيءٌ وجهدُ التوسيم "
    "والترقيم الرقميَّين شيءٌ آخر، والفرقُ يُسجَّل ولا يُطوى"
)

DIGITAL_WITNESS_TAGGING_IS_NOT_QUOTED_WHOLESALE_NOTE: Final[str] = (
    "DigitalWitnessTaggingIsNotQuotedWholesale: يُنقَل من الشاهد الرقميّ ما "
    "يحتاجه البندُ من حروف المتن مُسنَدًا، ولا تُنسَخ المادةُ كاملةً ببنيتها "
    "المُوسَّمة وعلاماتها؛ فالمطلوبُ نصُّ السلطة لا جهدُ الترميز"
)


@dataclass(frozen=True, slots=True)
class DigitalWitness:
    """شاهدٌ رقميٌّ مُسمًّى بمستودعه ومساره وبيانات الطبعة التي يُرقِّم عليها."""

    corpus: str
    repository: str
    path: str
    print_edition: str
    tagging_note: str

    def __post_init__(self) -> None:
        for value, label in (
            (self.corpus, "الكوربص"),
            (self.repository, "المستودع"),
            (self.path, "المسار"),
            (self.print_edition, "بياناتُ الطبعة"),
            (self.tagging_note, "بيانُ التوسيم"),
        ):
            if not isinstance(value, str) or not value.strip():
                raise SourceTextError(f"{label} نصٌّ غير فارغ؛ ولا يُترَك صمتًا.")


LISAN_DIGITAL_WITNESS: Final[DigitalWitness] = DigitalWitness(
    corpus="OpenITI (Open Islamicate Texts Initiative)",
    repository="github.com/OpenITI/RELEASE",
    path=(
        "data/0711IbnManzurIfriqi/0711IbnManzurIfriqi.LisanCarab/"
        "0711IbnManzurIfriqi.LisanCarab.Shamela0001687-ara1.mARkdown"
    ),
    print_edition=(
        "لسان العرب، ابن منظور (ت٧١١هـ)، دار صادر - بيروت، الطبعة الثالثة "
        "١٤١٤هـ، ١٥ مجلدًا"
    ),
    tagging_note=(
        "ترويسةُ الملفّ تُصرّح ببيانات هذه الطبعة، وعلاماتُ الصفحات المُضمَّنة "
        "(`PageV05P240` وما بعدها) ترقيمٌ على طبعةٍ ورقيةٍ مُسمّاة لا ترقيمُ "
        "موقعٍ إلكترونيّ؛ ولم تُقابَل هذه الحروفُ بنسخةٍ ورقيةٍ في اليد، فالموضعُ "
        "`ترقيم_طبعة_مرمز_رقميا_غير_مقابل` لا `مقابل_بنسخة_ورقية_محققة`. "
        "ولا مِلفَّ ترخيصٍ في المستودع المذكور، فاقتُصِر على اقتباساتٍ قصيرةٍ "
        "مُسنَدةٍ من المتن دون نسخ جهد التوسيم. "
        + DIGITAL_WITNESS_TAGGING_IS_NOT_QUOTED_WHOLESALE_NOTE
    ),
)


@dataclass(frozen=True, slots=True)
class SuppliedSourceText:
    """نصٌّ مُزوَّدٌ لبندٍ واحد: حروفُه، وموضعُه، وجنسُ التحقّق منه، وبقاياه."""

    key: str
    item: CardItem
    reference: FrozenReference
    locus_statement: str
    locus_verification: LocusVerification
    verbatim_text: str
    internal_authorities: tuple[str, ...]
    named_residuals: tuple[str, ...]
    digital_witness: DigitalWitness | None = None

    def __post_init__(self) -> None:
        for value, label in (
            (self.key, "مفتاحُ النصّ"),
            (self.locus_statement, "بيانُ الموضع"),
            (self.verbatim_text, "النصُّ المنقول"),
        ):
            if not isinstance(value, str) or not value.strip():
                raise SourceTextError(f"{label} نصٌّ غير فارغ؛ ولا يُترَك صمتًا.")
        if not isinstance(self.item, CardItem):
            raise SourceTextError("البند عضوٌ في مفردته المغلقة.")
        if not isinstance(self.reference, FrozenReference):
            raise SourceTextError("المرجعُ عضوٌ في مفردته الثلاثية المغلقة.")
        if not isinstance(self.locus_verification, LocusVerification):
            raise SourceTextError("جنسُ التحقّق من الموضع عضوٌ في مفردته المغلقة.")
        if not isinstance(self.internal_authorities, tuple):
            raise SourceTextError("سلطاتُ النصّ الداخلية تعدادٌ مرتَّب.")
        haystack = comparison_key(self.verbatim_text)
        for authority in self.internal_authorities:
            if not isinstance(authority, str) or not authority.strip():
                raise SourceTextError("كلُّ سلطةٍ داخليةٍ اسمٌ غيرُ فارغ.")
            if comparison_key(authority.strip()) not in haystack:
                raise SourceTextError(
                    f"السلطةُ «{authority}» غيرُ واقعةٍ في النصّ المنقول نصًّا؛ "
                    "وإسنادٌ لا يُقرأ فيه المُسنَد إليه إحالةٌ مبهمة."
                )
        if not isinstance(self.named_residuals, tuple) or not self.named_residuals:
            raise SourceTextError(
                f"نصُّ {self.key} بلا بقيّةٍ مُسمّاةٍ واحدة؛ وحدودُ النقل تُسمّى "
                "ولا تُترَك للقارئ."
            )
        for residual in self.named_residuals:
            if not isinstance(residual, str) or not residual.strip():
                raise SourceTextError("كلُّ بقيّةٍ مُسمّاةٍ مفتاحٌ غيرُ فارغ.")
        if self.digital_witness is not None and not isinstance(
            self.digital_witness, DigitalWitness
        ):
            raise SourceTextError("الشاهدُ الرقميُّ `DigitalWitness` أو لا شيء.")

    @property
    def locus_is_collated_by_hand(self) -> bool:
        """`True` فقط حين قوبل الموضعُ بنسخةٍ ورقيةٍ محقَّقة؛ ولا مدخلَ له اليوم."""

        return self.locus_verification is LocusVerification.مقابل_بنسخة_ورقية_محققة


MUTABAQA_TADAMMUN_ILTIZAM_SHAKHSIYYA_THREE: Final[SuppliedSourceText] = (
    SuppliedSourceText(
        key="MUTABAQA_TADAMMUN_ILTIZAM_SHAKHSIYYA_THREE",
        item=CardItem.MUTABAQA_TADAMMUN_ILTIZAM,
        reference=FrozenReference.SHAKHSIYYA_THREE,
        locus_statement=(
            "الشخصية الإسلامية، الجزء الثالث؛ نسخةُ `.docx` مرفوعةٌ بلا بياناتِ "
            "دارٍ وسنةٍ وطبعةٍ مؤكَّدة، وأرقامُ «السطور» المذكورةُ في الطلب "
            "ترقيمُ استخراجٍ آليٍّ من ذلك الملفّ لا ترقيمُ صفحاتِ طبعة"
        ),
        locus_verification=LocusVerification.موضع_غير_متحقق,
        verbatim_text=(
            "فما دل عليه اللفظ مطابقة أو تضمناً هو المنطوق... فدلالة اللفظ على "
            "تمام معناه مطابقة فهي من المنطوق، ودلالة اللفظ على جزء المسمى تضمن "
            "وهي كذلك من المنطوق... أما دلالة الالتزام فهي دلالة اللفظ على لازم "
            "معناه"
        ),
        internal_authorities=(),
        named_residuals=(
            "PRINT_EDITION_LOCUS_NOT_VERIFIED",
            "EXTRACTED_LINE_NUMBERS_ARE_NOT_PRINT_PAGINATION",
        ),
    )
)

KHABAR_INSHA_SHAKHSIYYA_THREE: Final[SuppliedSourceText] = SuppliedSourceText(
    key="KHABAR_INSHA_SHAKHSIYYA_THREE",
    item=CardItem.KHABAR_INSHA,
    reference=FrozenReference.SHAKHSIYYA_THREE,
    locus_statement=(
        "الشخصية الإسلامية، الجزء الثالث؛ النسخةُ والتحفّظُ نفسهما: ملفُّ "
        "`.docx` بلا بيانات طبعةٍ مؤكَّدة، وترقيمُ سطوره ترقيمُ استخراجٍ آليّ"
    ),
    locus_verification=LocusVerification.موضع_غير_متحقق,
    verbatim_text=(
        "والفرق بين الإنشاء والخبر، أن الإنشاء لا يحتمل التصديق والتكذيب، بخلاف "
        "الخبر. والإنشاء لا يكون معناه إلا مقارناً للفظ، بخلاف الخبر فقد يتقدم "
        "وقد يتأخر"
    ),
    internal_authorities=(),
    named_residuals=(
        "PRINT_EDITION_LOCUS_NOT_VERIFIED",
        "EXTRACTED_LINE_NUMBERS_ARE_NOT_PRINT_PAGINATION",
    ),
)

WAZN_LISAN_NUR: Final[SuppliedSourceText] = SuppliedSourceText(
    key="WAZN_LISAN_NUR",
    item=CardItem.WAZN,
    reference=FrozenReference.LISAN_AL_ARAB,
    locus_statement="لسان العرب، مادة (ن و ر)، ج٥/٢٤١ بترقيم دار صادر ط٣ ١٤١٤هـ",
    locus_verification=LocusVerification.ترقيم_طبعة_مرمز_رقميا_غير_مقابل,
    verbatim_text=(
        "قال ثعلب: إنما ذلك لأن العرب تشبه الحرف بالحرف فشبهوا منارة وهي مفعلة "
        "من النور، بفتح الميم، بفعالة فكسروها تكسيرها"
    ),
    internal_authorities=("ثعلب",),
    named_residuals=(
        "DIGITALLY_ENCODED_PRINT_PAGINATION_UNCOLLATED",
        "LISAN_MATN_IS_QUOTED_NOT_VENDORED_WHOLESALE",
    ),
    digital_witness=LISAN_DIGITAL_WITNESS,
)

ISHTIQAQ_SARF_LISAN_NUR: Final[SuppliedSourceText] = SuppliedSourceText(
    key="ISHTIQAQ_SARF_LISAN_NUR",
    item=CardItem.ISHTIQAQ_SARF,
    reference=FrozenReference.LISAN_AL_ARAB,
    locus_statement="لسان العرب، مادة (ن و ر)، ج٥/٢٤١ بترقيم دار صادر ط٣ ١٤١٤هـ",
    locus_verification=LocusVerification.ترقيم_طبعة_مرمز_رقميا_غير_مقابل,
    verbatim_text=(
        "الجوهري: الجمع مناور، بالواو، لأنه من النور، ومن قال منائر وهمز فقد شبه "
        "الأصلي بالزائد كما قالوا مصائب وأصله مصاوب"
    ),
    internal_authorities=("الجوهري",),
    named_residuals=(
        "DIGITALLY_ENCODED_PRINT_PAGINATION_UNCOLLATED",
        "LISAN_MATN_IS_QUOTED_NOT_VENDORED_WHOLESALE",
    ),
    digital_witness=LISAN_DIGITAL_WITNESS,
)


SUPPLIED_SOURCE_TEXTS: Final[MappingProxyType[str, SuppliedSourceText]] = (
    MappingProxyType(
        {
            supplied.key: supplied
            for supplied in (
                MUTABAQA_TADAMMUN_ILTIZAM_SHAKHSIYYA_THREE,
                KHABAR_INSHA_SHAKHSIYYA_THREE,
                WAZN_LISAN_NUR,
                ISHTIQAQ_SARF_LISAN_NUR,
            )
        }
    )
)


def supplied_text_for(key: str) -> SuppliedSourceText:
    """النصُّ المُزوَّدُ بمفتاحه؛ ومفتاحٌ غيرُ مُسجَّلٍ يُرَدّ ولا يُحمَل على غيره."""

    if not isinstance(key, str) or key not in SUPPLIED_SOURCE_TEXTS:
        raise SourceTextError(
            f"لا نصَّ مُزوَّدًا بهذا المفتاح: {key!r}؛ والمفاتيحُ مُسجَّلةٌ مغلقة."
        )
    return SUPPLIED_SOURCE_TEXTS[key]


def require_attested_excerpt(key: str, excerpt: str) -> str:
    """رُدَّ الاقتباسَ إن لم يكن حرفُه واقعًا في النصّ المُزوَّد نفسه."""

    supplied = supplied_text_for(key)
    if not isinstance(excerpt, str) or not excerpt.strip():
        raise SourceTextError("الاقتباسُ نصٌّ غير فارغ.")
    if comparison_key(excerpt) not in comparison_key(supplied.verbatim_text):
        raise SourceTextError(
            f"اقتباسٌ لا يقع حرفُه في نصّ {key}: والتحقّقُ بالاحتواء لا "
            "بالتصديق، وحكايةُ المعنى ليست نقلًا."
        )
    return excerpt


_FORBIDDEN_FIELD_TOKENS: Final[tuple[str, ...]] = (
    "result",
    "outcome",
    "verdict",
    "birth",
    "certificate",
    "classification",
    "proof",
    "score",
    "fractal",
)


def _assert_no_result_field() -> None:
    """حارسُ استيراد: لا حقلَ نتيجةٍ يتسلّل إلى وحدة النقل لاحقًا."""

    for declaring_type in (SuppliedSourceText, DigitalWitness):
        for declared in fields(declaring_type):
            lowered = declared.name.lower()
            for token in _FORBIDDEN_FIELD_TOKENS:
                if token in lowered:
                    raise SourceTextError(
                        f"حقلٌ يحمل نتيجة تسلّل إلى {declaring_type.__name__}: "
                        f"{declared.name}؛ والنقلُ لا نتيجة فيه."
                    )


if len(LocusVerification) != 3:  # pragma: no cover - guard
    raise RuntimeError(
        "locus verification is unverified, digitally encoded print pagination, "
        "or hand-collated: dropping the middle member would equate an encoded "
        "print edition with a source that names no edition at all"
    )

_assert_no_result_field()
