"""نصوصٌ مصدريةٌ **زُوِّدت** لمراحل طبقة المركّب، بحروفها وبجنس تحقُّق موضعها.

`compound_layer_preregistration` جمَّد المراحلَ الأربعَ قبل مصادرها، ووقفت كلُّها
عند `مصدر_غير_مُقدَّم` بدعوى صريحةٍ عن حال الشجرة: «لم يُقدَّم لهذه المرحلة نصٌّ
مصدريّ **في هذا المستودع**». وهذه الوحدةُ موضعُ ما زُوِّد منها فعلًا؛ وتزويدُه
يُبطِل تلك الدعوى في المرحلة المُزوَّدة وحدها، ولا يُبطِلها في غيرها.

**ووحدةُ النقل هذه مستقلّةٌ عن `sentence_card_source_texts` بجنسها لا بترتيبها**
(`CompoundStageIsNotACardItem`): تلك تُزوِّد **بندَ بطاقةٍ** (`CardItem`) من
**مفردة مراجعَ ثلاثيةٍ مُجمَّدة**، وهذه تُزوِّد **مرحلةَ طبقةٍ** (`CompoundStage`)
من كتبٍ ليست أعضاءً في تلك المفردة أصلًا. فحشرُ هذه النصوص هناك توسيعٌ لمفردةٍ
مُجمَّدةٍ **بعد رؤية نصّها**، وهو ما يمنعه `MarkerVocabularyIsFrozenBeforeItsText`
بعينه. وتُعاد هنا الأدواتُ المشتركةُ استيرادًا لا نسخًا: مرتبةُ تحقُّق الموضع،
والشاهدُ الرقميّ، وحدُّ الاقتباس بالاحتواء.

**ومفردةُ مراجع هذه الوحدة فُتِحت لحالةٍ وقعت، وتُسجَّل بقيّتُها**
(`REFERENCE_VOCABULARY_OPENED_AFTER_ITS_TEXT_WAS_SEEN`): الكتابان لم يُختارا قبل
النصّ ثم زُوِّدا، بل وُجِد النصُّ أوّلًا فسُمِّي الكتابان بعده. وهذا ترتيبٌ
معكوسٌ عن المُشتهى، **ويُسجَّل بقيّةً مُسمّاةً ولا يُطوى**؛ وإنما احتُمِل لأنّ
هذه الوحدة لا تحمل مفردةَ مخرجاتٍ ولا دالّةَ قرارٍ يُفصَّل مقاسُها على النصّ،
ومفرداتُ المراحل في `compound_layer_preregistration` بقيت **بحروفها كما جُمِّدت**.

**والتزويدُ يرفع نقصَ النقل وحده** (`SuppliedTextIsNotAFormalCertificate`): لا
مجالَ مُجمَّدًا ينشأ به، ولا دالّةَ قرار، ولا حاملًا يُشتَقّ منه، ولا شاهدَ لكلّ
فرع. و`شاهد_لكل_فرع` تبقى **مُعلَنةً غير قابلة للبناء** بقانونها هناك: لا سلطةَ
في هذا المستودع تتحقّق من إسناد فرعٍ إلى نصّه، ولا يرفع ذلك تزويدٌ ولا عشرة.

**ولا سلطةَ لهذه الوحدة**: لا ولادةَ، ولا حكمَ ولادةٍ، ولا تجميد، ولا `E0`، ولا
تقرؤها بوّابةٌ في `kernel/`، ولا تدخل في `BirthExperimentSpecification`.
"""

from __future__ import annotations

from dataclasses import dataclass, fields
from enum import Enum
from types import MappingProxyType
from typing import Final

from .compound_layer_preregistration import CompoundStage
from .sentence_card_source_texts import (
    DIGITAL_WITNESS_TAGGING_IS_NOT_QUOTED_WHOLESALE_NOTE,
    DigitalWitness,
    LocusVerification,
    SourceTextError,
)
from .text_key import comparison_key

__all__ = [
    "AMIL_MAMUL_IBN_AQIL_ISHTIGHAL",
    "AMIL_MAMUL_MUGHNI_FASL",
    "COMPOUND_STAGE_IS_NOT_A_CARD_ITEM_NOTE",
    "COMPOUND_SUPPLIED_SOURCE_TEXTS",
    "IBN_AQIL_DIGITAL_WITNESS",
    "MUGHNI_DIGITAL_WITNESS",
    "REFERENCE_VOCABULARY_OPENED_AFTER_ITS_TEXT_NOTE",
    "TERM_IS_USED_NOT_DEFINED_NOTE",
    "CompoundSourceReference",
    "CompoundSuppliedSourceText",
    "compound_texts_for_stage",
    "require_attested_compound_excerpt",
    "supplied_compound_text_for",
]


class CompoundSourceReference(Enum):
    """مراجعُ طبقة المركّب المُزوَّدة؛ عضوان، وكلاهما نحويٌّ تراثيٌّ مُسمّى."""

    SHARH_IBN_AQIL = "شرح_ابن_عقيل_على_ألفية_ابن_مالك"
    MUGHNI_AL_LABIB = "مغني_اللبيب_عن_كتب_الأعاريب"


COMPOUND_STAGE_IS_NOT_A_CARD_ITEM_NOTE: Final[str] = (
    "CompoundStageIsNotACardItem: مرحلةُ طبقة المركّب ليست بندًا في بطاقة "
    "الجملة، ومرجعُها ليس عضوًا في مفردة مراجع البطاقة الثلاثية المُجمَّدة؛ "
    "فتزويدُها هنا نقلٌ في موضعها، وحشرُه هناك توسيعُ مفردةٍ مُجمَّدةٍ بعد "
    "رؤية نصّها"
)

REFERENCE_VOCABULARY_OPENED_AFTER_ITS_TEXT_NOTE: Final[str] = (
    "REFERENCE_VOCABULARY_OPENED_AFTER_ITS_TEXT_WAS_SEEN: مفردةُ مراجع هذه "
    "الوحدة سُمّيت **بعد** وقوع نصّها لا قبله، فالترتيبُ معكوسٌ عن المُشتهى "
    "ويُسجَّل بقيّةً؛ وإنما احتُمِل لأنّها لا تحمل مفردةَ مخرجاتٍ ولا دالّةَ "
    "قرارٍ يُفصَّل مقاسُها على النصّ، ومفرداتُ المراحل بقيت بحروفها كما جُمِّدت"
)

TERM_IS_USED_NOT_DEFINED_NOTE: Final[str] = (
    "TERM_IS_USED_NOT_DEFINED_IN_THE_SUPPLIED_TEXT: المنقولُ يستعمل «العامل» "
    "و«المعمول» في مسألةٍ بعينها ويفترض حدَّهما مفروغًا منه، ولا يَحُدّهما ولا "
    "يقسم اللفظَ إليهما قسمةً حاصرة؛ فاستعمالُ مصطلحٍ ليس تعريفَه، ولا يقوم "
    "مقامَ شاهدٍ مُثبَتٍ لكلّ فرعٍ من فروع المفردة"
)


IBN_AQIL_DIGITAL_WITNESS: Final[DigitalWitness] = DigitalWitness(
    corpus="OpenITI (Open Islamicate Texts Initiative)",
    repository="github.com/OpenITI/RELEASE",
    path=(
        "data/0769IbnCaqilBahaDinMisri/0769IbnCaqilBahaDinMisri.SharhCalaAlfiyya/"
        "0769IbnCaqilBahaDinMisri.SharhCalaAlfiyya.Shamela0009904-ara1"
    ),
    print_edition=(
        "شرح ابن عقيل على ألفية ابن مالك، بهاء الدين عبد الله بن عقيل (ت٧٦٩هـ)، "
        "تحقيق محمد محيي الدين عبد الحميد، دار التراث - القاهرة، ٤ أجزاء"
    ),
    tagging_note=(
        "ترويسةُ الملفّ تُصرّح بالمحقِّق والدار، وعلاماتُ الصفحات المُضمَّنة في "
        "المتن (`PageV02P128` وما حولها، وهي ألفٌ وثلاثُ مئةٍ وثلاثون علامةً في "
        "أربعة أجزاء) ترقيمٌ على طبعةٍ ورقيةٍ مُسمّاة لا تقسيمُ عرضٍ إلكترونيّ؛ "
        "ولم تُقابَل هذه الحروفُ بنسخةٍ ورقيةٍ في اليد، فالموضعُ "
        "`ترقيم_طبعة_مرمز_رقميا_غير_مقابل` لا `مقابل_بنسخة_ورقية_محققة`. "
        "ولا مِلفَّ ترخيصٍ في المستودع المذكور، فاقتُصِر على اقتباساتٍ قصيرةٍ "
        "من المتن دون نسخ جهد التوسيم. "
        + DIGITAL_WITNESS_TAGGING_IS_NOT_QUOTED_WHOLESALE_NOTE
    ),
)

MUGHNI_DIGITAL_WITNESS: Final[DigitalWitness] = DigitalWitness(
    corpus="OpenITI (Open Islamicate Texts Initiative)",
    repository="github.com/OpenITI/RELEASE",
    path=(
        "data/0761JamalDinIbnHisham/0761JamalDinIbnHisham.MughniLabib/"
        "0761JamalDinIbnHisham.MughniLabib.JK001131-ara1"
    ),
    print_edition=(
        "مغني اللبيب عن كتب الأعاريب، ابن هشام الأنصاري (ت٧٦١هـ)، تحقيق مازن "
        "المبارك ومحمد علي حمد الله، دار الفكر - دمشق، ١٩٨٥م"
    ),
    tagging_note=(
        "ترويسةُ الملفّ تُصرّح بالمحقِّقَين والدار والمكان والسنة، وعلاماتُ "
        "الصفحات المُضمَّنة (`PageV01P084` وما حولها، وهي تسعُ مئةٍ وسبعُ "
        "علاماتٍ في جزأين) ترقيمٌ على تلك الطبعة لا تقسيمُ عرضٍ إلكترونيّ؛ ولم "
        "تُقابَل بنسخةٍ ورقيةٍ في اليد. **والمحقِّقان هنا غيرُ محقِّق شرح ابن "
        "عقيل**، فلا تُقرأ «استمراريةُ محقِّقٍ واحد» عبر المصدرين. "
        + DIGITAL_WITNESS_TAGGING_IS_NOT_QUOTED_WHOLESALE_NOTE
    ),
)


@dataclass(frozen=True, slots=True)
class CompoundSuppliedSourceText:
    """نصٌّ مُزوَّدٌ لمرحلةٍ واحدة: حروفُه، وموضعُه، وجنسُ تحقّقه، وبقاياه."""

    key: str
    stage: CompoundStage
    reference: CompoundSourceReference
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
        if not isinstance(self.stage, CompoundStage):
            raise SourceTextError("المرحلةُ عضوٌ في مفردتها المغلقة.")
        if not isinstance(self.reference, CompoundSourceReference):
            raise SourceTextError("المرجعُ عضوٌ في مفردة مراجع هذه الوحدة.")
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
        if "REFERENCE_VOCABULARY_OPENED_AFTER_ITS_TEXT_WAS_SEEN" not in (
            self.named_residuals
        ):
            raise SourceTextError(
                f"نصُّ {self.key} لا يحمل بقيّةَ فتحِ المفردة بعد نصّها؛ "
                "والترتيبُ المعكوسُ يُكتَب في كلّ نصٍّ من هذه الوحدة لا مرّةً "
                "في صدرها ثمّ يُنسى."
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

    @property
    def attests_every_branch(self) -> bool:
        """`False` دائمًا: النقلُ يرفع نقصَ النقل ولا يُقيم شاهدًا لكلّ فرع."""

        return False


AMIL_MAMUL_IBN_AQIL_ISHTIGHAL: Final[CompoundSuppliedSourceText] = (
    CompoundSuppliedSourceText(
        key="AMIL_MAMUL_IBN_AQIL_ISHTIGHAL",
        stage=CompoundStage.AMIL_MAMUL,
        reference=CompoundSourceReference.SHARH_IBN_AQIL,
        locus_statement=(
            "شرح ابن عقيل، باب «اشتغال العامل عن المعمول»، ج٢/١٢٨ بترقيم طبعة "
            "دار التراث المُصرَّح بها في ترويسة الشاهد الرقميّ؛ والمقطعُ واقعٌ "
            "بين علامتَي `PageV02P128` و`PageV02P129` في المتن نفسه"
        ),
        locus_verification=LocusVerification.ترقيم_طبعة_مرمز_رقميا_غير_مقابل,
        verbatim_text=(
            "الاشتغال: أن يتقدم اسم ويتأخر عنه فعل قد عمل في ضمير ذلك الاسم أو "
            "في سبيبه وهو المضاف إلى ضمير الاسم السابق فمثال المشتغل بالضمير "
            "زيدا ضربته وزيدا مررت به ومثال المشتغل بالسببي زيدا ضربت غلامه"
        ),
        internal_authorities=(),
        named_residuals=(
            "REFERENCE_VOCABULARY_OPENED_AFTER_ITS_TEXT_WAS_SEEN",
            "DIGITALLY_ENCODED_PRINT_PAGINATION_UNCOLLATED",
            "MATN_IS_QUOTED_NOT_VENDORED_WHOLESALE",
            "TERM_IS_USED_NOT_DEFINED_IN_THE_SUPPLIED_TEXT",
            "CHAPTER_TITLE_IS_THE_EDITORS_NOT_NECESSARILY_THE_AUTHORS",
        ),
        digital_witness=IBN_AQIL_DIGITAL_WITNESS,
    )
)

AMIL_MAMUL_MUGHNI_FASL: Final[CompoundSuppliedSourceText] = CompoundSuppliedSourceText(
    key="AMIL_MAMUL_MUGHNI_FASL",
    stage=CompoundStage.AMIL_MAMUL,
    reference=CompoundSourceReference.MUGHNI_AL_LABIB,
    locus_statement=(
        "مغني اللبيب، الكلام على «إمّا»، ج١/٨٤ بترقيم طبعة دار الفكر ١٩٨٥ "
        "المُصرَّح بها في ترويسة الشاهد الرقميّ؛ والمقطعُ واقعٌ بين علامتَي "
        "`PageV01P084` و`PageV01P085` في المتن نفسه"
    ),
    locus_verification=LocusVerification.ترقيم_طبعة_مرمز_رقميا_غير_مقابل,
    verbatim_text=(
        "ولا خلاف أن إما الأولى غير عاطفة لاعتراضها بين العامل والمعمول في نحو "
        "قام إما زيد وإما عمرو وبين أحد معمولي العامل ومعموله الآخر"
    ),
    internal_authorities=(),
    named_residuals=(
        "REFERENCE_VOCABULARY_OPENED_AFTER_ITS_TEXT_WAS_SEEN",
        "DIGITALLY_ENCODED_PRINT_PAGINATION_UNCOLLATED",
        "MATN_IS_QUOTED_NOT_VENDORED_WHOLESALE",
        "TERM_IS_USED_NOT_DEFINED_IN_THE_SUPPLIED_TEXT",
        "ONE_OPERATOR_MAY_HAVE_TWO_MAMULS_AND_THE_VOCABULARY_IS_NOT_WIDENED",
    ),
    digital_witness=MUGHNI_DIGITAL_WITNESS,
)


COMPOUND_SUPPLIED_SOURCE_TEXTS: Final[
    MappingProxyType[str, CompoundSuppliedSourceText]
] = MappingProxyType(
    {
        supplied.key: supplied
        for supplied in (AMIL_MAMUL_IBN_AQIL_ISHTIGHAL, AMIL_MAMUL_MUGHNI_FASL)
    }
)


def supplied_compound_text_for(key: str) -> CompoundSuppliedSourceText:
    """النصُّ المُزوَّدُ بمفتاحه؛ ومفتاحٌ غيرُ مُسجَّلٍ يُرَدّ ولا يُحمَل على غيره."""

    if not isinstance(key, str) or key not in COMPOUND_SUPPLIED_SOURCE_TEXTS:
        raise SourceTextError(
            f"لا نصَّ مُزوَّدًا بهذا المفتاح: {key!r}؛ والمفاتيحُ مُسجَّلةٌ مغلقة."
        )
    return COMPOUND_SUPPLIED_SOURCE_TEXTS[key]


def compound_texts_for_stage(
    stage: CompoundStage,
) -> tuple[CompoundSuppliedSourceText, ...]:
    """نصوصُ مرحلةٍ بعينها بترتيب تسجيلها؛ ومرحلةٌ بلا نصٍّ تُرجِع تعدادًا فارغًا."""

    if not isinstance(stage, CompoundStage):
        raise SourceTextError("المرحلةُ عضوٌ في مفردتها المغلقة.")
    return tuple(
        supplied
        for supplied in COMPOUND_SUPPLIED_SOURCE_TEXTS.values()
        if supplied.stage is stage
    )


def require_attested_compound_excerpt(key: str, excerpt: str) -> str:
    """رُدَّ الاقتباسَ إن لم يكن حرفُه واقعًا في النصّ المُزوَّد نفسه."""

    supplied = supplied_compound_text_for(key)
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

    for declared in fields(CompoundSuppliedSourceText):
        lowered = declared.name.lower()
        for token in _FORBIDDEN_FIELD_TOKENS:
            if token in lowered:
                raise SourceTextError(
                    "حقلٌ يحمل نتيجة تسلّل إلى CompoundSuppliedSourceText: "
                    f"{declared.name}؛ والنقلُ لا نتيجة فيه."
                )


_assert_no_result_field()


def _assert_registry_matches_preregistration() -> None:
    """حارسُ استيراد: التسجيلُ والنقلُ يتطابقان في المفاتيح ولا ينفرد أحدهما.

    مفتاحٌ مُعلَنٌ في مرحلةٍ بلا نصٍّ هنا دعوى تزويدٍ بلا مُزوَّد، ونصٌّ هنا
    بلا مفتاحٍ في مرحلته نقلٌ لا يُغيّر موقفَ شيءٍ وهو يدّعي أنه يُغيّره.
    """

    from .compound_layer_preregistration import COMPOUND_LAYER_PREREGISTRATION

    for registration in COMPOUND_LAYER_PREREGISTRATION.registrations:
        declared = set(registration.supplied_text_keys)
        registered = {
            supplied.key for supplied in compound_texts_for_stage(registration.stage)
        }
        if declared != registered:
            raise SourceTextError(
                f"مفاتيحُ مرحلة {registration.stage.value} في التسجيل تخالف "
                "النصوصَ المُسجَّلة هنا؛ والتطابقُ شرطُ الاستيراد لا تعليقٌ "
                "يُصحَّح لاحقًا."
            )


_assert_registry_matches_preregistration()
