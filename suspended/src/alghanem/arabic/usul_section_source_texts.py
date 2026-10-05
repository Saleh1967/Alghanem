"""موادُّ قسمٍ أصوليٍّ زُوِّدت في الطلب، مفروزةً بجنس تزويدها لا بموضوعها.

زُوِّد قسمٌ أصوليٌّ واحدٌ فيه خمسُ موادَّ تمسّ مواضعَ قائمةً في هذه الطبقة:
سلّمُ أولوية «الأمور المخلّة بفهم المراد»، وحدُّ أدوات التوليد اللفظيّ الثلاث،
وحكمٌ على ألفاظٍ محدَثةٍ بالخروج عن اللغة، وبرهانُ دورٍ على تصنيف الإنشاء،
وأمثلةٌ للمتواطئ والمشترك والمترادف. وهذه الوحدةُ **موضعُ ما زُوِّد منها**، لا
موضعُ الحكم به.

**والفرزُ الأول هنا فرزُ جنسِ التزويد لا فرزُ الموضوع** (`SectionMaterialStanding`):
بعضُ ما زُوِّد **حروفٌ بين قوسي اقتباس** تُفحَص بالاحتواء (`منقول_بحروفه`)،
وبعضُه **وصفٌ لحجّةٍ أو مثالٍ بلا حروفٍ منقولة** (`موصوف_بلا_نقل_حرفي`). وجمعُ
الجنسين تحت اسم «نصّ» يجعل الوصفَ نقلًا، وهو عينُ ما تمنعه الوحداتُ الأخرى في
`CASCADE_WORDING_IS_NOT_TRANSCRIBED`؛ فالموصوفُ يُسجَّل **مطلوبًا لا مُثبَتًا**،
ولا يُفحَص بالاحتواء، ولا يقوم مقامَ المنقول في موضعٍ يطلب حروفًا.

**وكتابُ القسم لم يُسَمَّ** (`SECTION_SOURCE_BOOK_IS_NOT_NAMED`): لم يُذكَر عنوانٌ
ولا مؤلّفٌ ولا سنةُ وفاةٍ ولا جزءٌ ولا صفحةٌ ولا دارٌ ولا طبعة، ولا شاهدَ رقميّ
يُقابَل عليه. فموضعُ كلّ مادّةٍ هنا `موضع_غير_متحقق` بلا استثناء، **وتسميةُ
الكتاب لاحقًا لا تُبدَّل بها المواضعُ المُسجَّلة بأثرٍ رجعيّ** إلا بتزويدٍ جديدٍ
يُسمّي موضعَه ابتداءً.

**وهذه المادّةُ مُعاضِدةٌ في كلّ حال، لا مرجعُ بندٍ ولا مفردةُ مخرجات**: مفردةُ
مراجع بطاقة الجملة ثلاثيةٌ مغلقة ولكلّ بندٍ منها واحدٌ لا أكثر، ومفرداتُ
`comprehension_defect` و`lafz_madlul_relation_formal` و`kulli_juzi_formal`
مُجمَّدةٌ قبل هذا النقل. فلا يُفتَح بهذا النقل عضوٌ في مفردة، ولا يُبدَّل به
مرجعٌ مُعلَن، ولا يتغيّر به موقفُ بندٍ واحد.

**ولا سلطةَ لهذه الوحدة**: لا ولادةَ، ولا حكمَ ولادةٍ، ولا تجميد، ولا `E0`، ولا
تقرؤها بوّابةٌ في `kernel/`، ولا تدخل في `BirthExperimentSpecification`.
"""

from __future__ import annotations

from dataclasses import dataclass, fields
from enum import Enum
from types import MappingProxyType
from typing import Final

from .comprehension_defect import ComprehensionDefectCause
from .sentence_card_source_texts import LocusVerification
from .text_key import comparison_key

__all__ = [
    "DAWR_PROOF_FOR_INSHA",
    "DESCRIBED_MATERIAL_IS_NOT_A_TRANSCRIPTION_NOTE",
    "DESCRIBED_SECTION_MATERIAL",
    "MURADIF_EXAMPLES_FARD_AND_HARAM",
    "MUSHTARAK_EXAMPLE_TAHUR",
    "MUTAWATI_EXAMPLE_HAJJ",
    "OUTSIDE_THE_LANGUAGE_EXCERPT",
    "PRIORITY_LADDER_EXCERPT",
    "SECTION_EXCERPTS",
    "SECTION_SOURCE_BOOK_IS_NOT_NAMED_NOTE",
    "SECTION_SOURCE_NAME",
    "SECTION_TEXTS_ARE_NOT_A_GATE_NOTE",
    "TAWLID_TOOLS_DOMAIN_EXCERPT",
    "DescribedSectionMaterial",
    "SectionExcerpt",
    "SectionMaterialStanding",
    "SectionTextError",
    "described_material_for",
    "require_attested_section_excerpt",
    "section_excerpt_for",
]


class SectionTextError(ValueError):
    """رُفض نقلٌ خارج شرطه؛ ولا يُحمَل على أقرب حالةٍ مقبولة."""


class SectionMaterialStanding(Enum):
    """جنسُ التزويد؛ ثنائيٌّ مغلق، ولا عضوَ فيه اسمُه «مُثبَت»."""

    منقول_بحروفه = "منقول_بحروفه"
    موصوف_بلا_نقل_حرفي = "موصوف_بلا_نقل_حرفي"


SECTION_SOURCE_NAME: Final[str] = (
    "قسمٌ أصوليٌّ زُوِّدت موادُّه في الطلب، لم يُسَمَّ كتابُه ولا مؤلّفُه ولا " "طبعتُه ولا موضعُه منها"
)

SECTION_SOURCE_BOOK_IS_NOT_NAMED_NOTE: Final[str] = (
    "SECTION_SOURCE_BOOK_IS_NOT_NAMED: القسمُ المُزوَّدُ بلا عنوانٍ ولا مؤلّفٍ "
    "ولا سنةِ وفاةٍ ولا جزءٍ ولا صفحةٍ ولا بيانات طبعةٍ ولا شاهدٍ رقميّ؛ "
    "فموضعُه `موضع_غير_متحقق` في كلّ مادّةٍ منه، وتسميةُ الكتاب لاحقًا لا "
    "تُبدَّل بها المواضعُ المُسجَّلة بأثرٍ رجعيّ"
)

DESCRIBED_MATERIAL_IS_NOT_A_TRANSCRIPTION_NOTE: Final[str] = (
    "DESCRIBED_MATERIAL_IS_NOT_A_TRANSCRIPTION: الموصوفُ بلا حروفٍ منقولةٍ "
    "مطلوبٌ لا مُثبَت؛ لا يُفحَص بالاحتواء، ولا يقوم مقامَ المنقول في موضعٍ "
    "يطلب حروفًا، ولا يُنقَل عنه بين قوسي اقتباسٍ كأنّه نصُّ سلطته"
)

SECTION_TEXTS_ARE_NOT_A_GATE_NOTE: Final[str] = (
    "SECTION_TEXTS_ARE_NOT_A_GATE: هذه الموادُّ نقلٌ وتسميةُ بقايا؛ لا تفتح "
    "عضوًا في مفردةٍ مُجمَّدة، ولا تُبدِّل مرجعًا مُعلَنًا، ولا تُغيِّر موقفَ "
    "بندٍ واحد، ولا تقرؤها بوّابةٌ في `kernel/`"
)


def _require_non_blank(value: object, label: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise SectionTextError(f"{label} نصٌّ غير فارغ؛ ولا يُترَك صمتًا.")
    return value


def _require_named_residuals(residuals: object, key: str) -> None:
    if not isinstance(residuals, tuple) or not residuals:
        raise SectionTextError(
            f"مادّةُ {key} بلا بقيّةٍ مُسمّاةٍ واحدة؛ وحدودُ النقل تُسمّى ولا " "تُترَك للقارئ."
        )
    for residual in residuals:
        _require_non_blank(residual, "البقيّةُ المُسمّاة")
    if "SECTION_SOURCE_BOOK_IS_NOT_NAMED" not in residuals:
        raise SectionTextError(
            f"مادّةُ {key} من قسمٍ لم يُسَمَّ كتابُه ولا تحمل بقيّةَ "
            "`SECTION_SOURCE_BOOK_IS_NOT_NAMED`؛ وحدُّ السند يُكتَب في البقايا "
            "لا يُترَك لحسن الظنّ."
        )


@dataclass(frozen=True, slots=True)
class SectionExcerpt:
    """حروفٌ منقولةٌ من القسم، ومواضعُ التصنيف التي تُعاضِدها، وبقاياها."""

    key: str
    verbatim_text: str
    corroborated_terms: tuple[str, ...]
    locus_statement: str
    locus_verification: LocusVerification
    named_residuals: tuple[str, ...]

    def __post_init__(self) -> None:
        _require_non_blank(self.key, "مفتاحُ المادّة")
        _require_non_blank(self.verbatim_text, "النصُّ المنقول")
        _require_non_blank(self.locus_statement, "بيانُ الموضع")
        if not isinstance(self.locus_verification, LocusVerification):
            raise SectionTextError("جنسُ التحقّق من الموضع عضوٌ في مفردته المغلقة.")
        if self.locus_verification is not LocusVerification.موضع_غير_متحقق:
            raise SectionTextError(
                f"موضعُ {self.key} لا يُرفَع عن `موضع_غير_متحقق` وكتابُ القسم "
                "لم يُسَمَّ؛ " + SECTION_SOURCE_BOOK_IS_NOT_NAMED_NOTE
            )
        terms = self.corroborated_terms
        if not isinstance(terms, tuple) or not terms:
            raise SectionTextError(
                f"نصُّ {self.key} لا يُعاضِد موضعًا واحدًا؛ ونقلٌ لا يُسمّي ما "
                "يُعاضِده منقولٌ بلا موضعٍ من هذه الطبقة."
            )
        seen: set[str] = set()
        for term in self.corroborated_terms:
            _require_non_blank(term, "الموضعُ المُعاضَد")
            if term in seen:
                raise SectionTextError(f"موضعٌ مكرَّرٌ في مُعاضَدات {self.key}: {term}.")
            seen.add(term)
        _require_named_residuals(self.named_residuals, self.key)

    @property
    def standing(self) -> SectionMaterialStanding:
        """`منقول_بحروفه` دائمًا؛ والجنسُ مُشتَقٌّ لا مُعلَنٌ في حقل."""

        return SectionMaterialStanding.منقول_بحروفه


@dataclass(frozen=True, slots=True)
class DescribedSectionMaterial:
    """مادّةٌ من القسم وُصِفت ولم تُنقَل بحروفها؛ مطلوبةٌ لا مُثبَتة."""

    key: str
    description: str
    related_terms: tuple[str, ...]
    named_residuals: tuple[str, ...]

    def __post_init__(self) -> None:
        _require_non_blank(self.key, "مفتاحُ المادّة")
        _require_non_blank(self.description, "وصفُ المادّة")
        if not isinstance(self.related_terms, tuple) or not self.related_terms:
            raise SectionTextError(
                f"مادّةُ {self.key} لا تُسمّي موضعًا واحدًا تتّصل به؛ ووصفٌ بلا "
                "موضعٍ لا يُقرأ."
            )
        seen: set[str] = set()
        for term in self.related_terms:
            _require_non_blank(term, "الموضعُ المُتّصل")
            if term in seen:
                raise SectionTextError(f"موضعٌ مكرَّرٌ في {self.key}: {term}.")
            seen.add(term)
        _require_named_residuals(self.named_residuals, self.key)
        if "MATERIAL_IS_DESCRIBED_NOT_TRANSCRIBED" not in self.named_residuals:
            raise SectionTextError(
                f"مادّةُ {self.key} موصوفةٌ ولا تحمل بقيّةَ "
                "`MATERIAL_IS_DESCRIBED_NOT_TRANSCRIBED`؛ "
                + DESCRIBED_MATERIAL_IS_NOT_A_TRANSCRIPTION_NOTE
            )

    @property
    def standing(self) -> SectionMaterialStanding:
        """`موصوف_بلا_نقل_حرفي` دائمًا؛ والجنسُ مُشتَقٌّ لا مُعلَنٌ في حقل."""

        return SectionMaterialStanding.موصوف_بلا_نقل_حرفي


_UNVERIFIED_LOCUS: Final[str] = (
    "قسمٌ أصوليٌّ زُوِّد في الطلب؛ لا عنوانَ كتابٍ ولا مؤلّفَ ولا جزءَ ولا "
    "صفحةَ ولا بياناتِ طبعةٍ ولا شاهدَ رقميّ يُقابَل عليه"
)


PRIORITY_LADDER_EXCERPT: Final[SectionExcerpt] = SectionExcerpt(
    key="PRIORITY_LADDER_EXCERPT",
    verbatim_text=(
        "الاشتراك أضعف الجميع... النقل أولى من الاشتراك؛ لأن المنقول مدلوله "
        "بمعنى واحد... بخلاف المشترك فمدلوله متعدد"
    ),
    corroborated_terms=(
        ComprehensionDefectCause.ISHTIRAK.value,
        ComprehensionDefectCause.NAQL.value,
    ),
    locus_statement=_UNVERIFIED_LOCUS,
    locus_verification=LocusVerification.موضع_غير_متحقق,
    named_residuals=(
        "SECTION_SOURCE_BOOK_IS_NOT_NAMED",
        "QUOTATION_CONTAINS_MARKED_ELISIONS",
        "ONLY_THE_NAQL_ISHTIRAK_COMPARISON_IS_TRANSCRIBED",
        "LADDER_ORDER_NOTATION_IS_THE_REQUESTER_WORDING",
    ),
)

TAWLID_TOOLS_DOMAIN_EXCERPT: Final[SectionExcerpt] = SectionExcerpt(
    key="TAWLID_TOOLS_DOMAIN_EXCERPT",
    verbatim_text=(
        "التعريب خاص بأسماء الأشياء... ولا يدخل الألفاظ الدالة على المعاني، ولا "
        "الجمل الدالة على الخيال"
    ),
    corroborated_terms=("تعريب", "اشتقاق", "مجاز"),
    locus_statement=_UNVERIFIED_LOCUS,
    locus_verification=LocusVerification.موضع_غير_متحقق,
    named_residuals=(
        "SECTION_SOURCE_BOOK_IS_NOT_NAMED",
        "QUOTATION_CONTAINS_MARKED_ELISIONS",
        "ISHTIQAQ_AND_MAJAZ_DOMAINS_ARE_NAMED_BY_EXCLUSION_NOT_BY_A_QUOTED_RULE",
        "TOOL_DOMAIN_TABLE_IS_THE_REQUESTER_WORDING",
    ),
)

OUTSIDE_THE_LANGUAGE_EXCERPT: Final[SectionExcerpt] = SectionExcerpt(
    key="OUTSIDE_THE_LANGUAGE_EXCERPT",
    verbatim_text=(
        "عمل كله خطأ، ويدل على الجمود الفكري، وعلى الجهل المطبق... هذه الألفاظ "
        "لا تُعتبر من ألفاظ اللغة العربية مطلقاً، أي ليست حقيقة لغوية، ولا "
        "حقيقة شرعية، ولا حقيقة عرفية، فلا تكون عربية على الإطلاق"
    ),
    corroborated_terms=("شرعية", "عرفية", "لغوية"),
    locus_statement=_UNVERIFIED_LOCUS,
    locus_verification=LocusVerification.موضع_غير_متحقق,
    named_residuals=(
        "SECTION_SOURCE_BOOK_IS_NOT_NAMED",
        "QUOTATION_CONTAINS_MARKED_ELISIONS",
        "THE_JUDGED_LEXEMES_ARE_NAMED_OUTSIDE_THE_QUOTED_SENTENCE",
        "NO_CRITERION_FOR_APPLYING_THE_JUDGEMENT_IS_INSIDE_THIS_QUOTATION",
    ),
)


DAWR_PROOF_FOR_INSHA: Final[DescribedSectionMaterial] = DescribedSectionMaterial(
    key="DAWR_PROOF_FOR_INSHA",
    description=(
        "وُصِف في الطلب برهانُ استحالةٍ دورانيةٍ على أنّ «طلقتك» إنشاءٌ لا خبر: "
        "لو كانت خبرًا لتوقّف صدقُها على وقوع الطلاق، وتوقّف وقوعُ الطلاق على "
        "صدق هذا الخبر نفسه، وهو دورٌ محال. ولم تُنقَل حروفُ هذا البرهان من "
        "كتابٍ مُسمًّى، وإنما وُصِفت حجّتُه وصفًا"
    ),
    related_terms=("خبري_إنشائي",),
    named_residuals=(
        "SECTION_SOURCE_BOOK_IS_NOT_NAMED",
        "MATERIAL_IS_DESCRIBED_NOT_TRANSCRIBED",
        "KHABAR_INSHA_ITEM_STANDING_IS_UNCHANGED_BY_THIS_MATERIAL",
        "CIRCULARITY_TEST_IS_NOT_A_DECISION_FUNCTION_HERE",
    ),
)

MUTAWATI_EXAMPLE_HAJJ: Final[DescribedSectionMaterial] = DescribedSectionMaterial(
    key="MUTAWATI_EXAMPLE_HAJJ",
    description=(
        "وُصِف «الحج» مثالًا للمتواطئ: يُطلَق على الإفراد والتمتّع والقِران، "
        "وهي مشتركةٌ في الماهية — إحرامٌ ووقوفٌ وطوافٌ وسعي. ولم تُنقَل حروفُ "
        "هذا المثال من كتابٍ مُسمًّى"
    ),
    related_terms=("متواطئ",),
    named_residuals=(
        "SECTION_SOURCE_BOOK_IS_NOT_NAMED",
        "MATERIAL_IS_DESCRIBED_NOT_TRANSCRIBED",
        "KULLI_JUZI_ATTESTED_WITNESSES_ARE_UNCHANGED_BY_THIS_MATERIAL",
    ),
)

MUSHTARAK_EXAMPLE_TAHUR: Final[DescribedSectionMaterial] = DescribedSectionMaterial(
    key="MUSHTARAK_EXAMPLE_TAHUR",
    description=(
        "وُصِف «الطهور» مثالًا للمشترك: يُطلَق على الماء وعلى التراب وعلى "
        "الدباغ، ثلاثةُ معانٍ للفظٍ واحد. ولم تُنقَل حروفُ هذا المثال من كتابٍ "
        "مُسمًّى، ولم يُنقَل دليلُ كونه وضعًا ابتدائيًّا لكلّ معنًى منها لا نقلًا "
        "ولا مجازًا"
    ),
    related_terms=("مشترك",),
    named_residuals=(
        "SECTION_SOURCE_BOOK_IS_NOT_NAMED",
        "MATERIAL_IS_DESCRIBED_NOT_TRANSCRIBED",
        "INITIAL_ASSIGNMENT_FOR_EACH_MEANING_IS_NOT_EVIDENCED_HERE",
        "SEVENFOLD_DECISION_DOMAIN_IS_UNCHANGED_BY_THIS_MATERIAL",
    ),
)

MURADIF_EXAMPLES_FARD_AND_HARAM: Final[DescribedSectionMaterial] = (
    DescribedSectionMaterial(
        key="MURADIF_EXAMPLES_FARD_AND_HARAM",
        description=(
            "وُصِف زوجان مثالًا للمترادف: الفرض والواجب، والحرام والمحظور. ولم "
            "تُنقَل حروفُ هذين المثالين من كتابٍ مُسمًّى، وهما يقعان في موضع "
            "قاعدةٍ مُسجَّلةٍ في `lafz_madlul_relation_formal` أنّ «الترادف خلاف "
            "الأصل»؛ فتوتّرُهما معها يُسجَّل ولا يُطوى، ولا يُرفَع بأحدهما"
        ),
        related_terms=("مترادف",),
        named_residuals=(
            "SECTION_SOURCE_BOOK_IS_NOT_NAMED",
            "MATERIAL_IS_DESCRIBED_NOT_TRANSCRIBED",
            "TENSION_WITH_MURADIF_PRESUMPTION_IS_RECORDED_NOT_RESOLVED",
            "FARD_WAJIB_SYNONYMY_IS_A_MADHHAB_DISPUTE_NOT_A_SETTLED_READING",
        ),
    )
)


SECTION_EXCERPTS: Final[MappingProxyType[str, SectionExcerpt]] = MappingProxyType(
    {
        excerpt.key: excerpt
        for excerpt in (
            PRIORITY_LADDER_EXCERPT,
            TAWLID_TOOLS_DOMAIN_EXCERPT,
            OUTSIDE_THE_LANGUAGE_EXCERPT,
        )
    }
)

DESCRIBED_SECTION_MATERIAL: Final[MappingProxyType[str, DescribedSectionMaterial]] = (
    MappingProxyType(
        {
            material.key: material
            for material in (
                DAWR_PROOF_FOR_INSHA,
                MUTAWATI_EXAMPLE_HAJJ,
                MUSHTARAK_EXAMPLE_TAHUR,
                MURADIF_EXAMPLES_FARD_AND_HARAM,
            )
        }
    )
)


def section_excerpt_for(key: str) -> SectionExcerpt:
    """النصُّ المنقولُ بمفتاحه؛ ومفتاحٌ غيرُ مُسجَّلٍ يُرَدّ ولا يُحمَل على غيره."""

    if not isinstance(key, str) or key not in SECTION_EXCERPTS:
        raise SectionTextError(
            f"لا نصَّ منقولًا بهذا المفتاح: {key!r}؛ والمفاتيحُ مُسجَّلةٌ مغلقة."
        )
    return SECTION_EXCERPTS[key]


def described_material_for(key: str) -> DescribedSectionMaterial:
    """المادّةُ الموصوفةُ بمفتاحها؛ ومفتاحٌ غيرُ مُسجَّلٍ يُرَدّ ولا يُحمَل على غيره."""

    if not isinstance(key, str) or key not in DESCRIBED_SECTION_MATERIAL:
        raise SectionTextError(
            f"لا مادّةَ موصوفةً بهذا المفتاح: {key!r}؛ والمفاتيحُ مُسجَّلةٌ مغلقة."
        )
    return DESCRIBED_SECTION_MATERIAL[key]


def require_attested_section_excerpt(key: str, excerpt: str) -> str:
    """رُدَّ الاقتباسَ إن لم يكن حرفُه واقعًا في النصّ المنقول نفسه.

    ولا نظيرَ لهذه الدالّة في الموادّ الموصوفة: الفحصُ بالاحتواء يفترض حروفًا
    منقولة، وإجراؤُه على وصفٍ يجعل الوصفَ نصًّا وهو عينُ ما مُنِع.
    """

    attested = section_excerpt_for(key)
    if not isinstance(excerpt, str) or not excerpt.strip():
        raise SectionTextError("الاقتباسُ نصٌّ غير فارغ.")
    if comparison_key(excerpt) not in comparison_key(attested.verbatim_text):
        raise SectionTextError(
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

    for declaring_type in (SectionExcerpt, DescribedSectionMaterial):
        for declared in fields(declaring_type):
            lowered = declared.name.lower()
            for token in _FORBIDDEN_FIELD_TOKENS:
                if token in lowered:
                    raise SectionTextError(
                        f"حقلٌ يحمل نتيجة تسلّل إلى {declaring_type.__name__}: "
                        f"{declared.name}؛ والنقلُ لا نتيجة فيه."
                    )


if len(SectionMaterialStanding) != 2:  # pragma: no cover - guard
    raise RuntimeError(
        "supplied section material is either transcribed verbatim or described "
        "without transcription: collapsing the pair would let a described "
        "argument be read as its source's own words"
    )

_assert_no_result_field()
