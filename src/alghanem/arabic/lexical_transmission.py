"""بنيةُ الاستشهاد المعجميّ، مُشتَقّةً من واصفٍ يُفحَص لا من عنوانٍ يُصدَّق.

ثلاثُ بطاقاتٍ مستقلّة (قُروء، وأنّى، ومَلِك) وقفت عند الحلقة الرابعة نفسها،
وسببُ وقوفها واحدٌ مُسمًّى: البطاقةُ تُسمّي مصدرًا («لسان العرب لابن منظور، مادة
كذا») ولا تصف **طريقَ ورود** المدلول. وهذه الوحدةُ تحسم جنسَ ذلك الوقوف بالمنهج
المُختبَر في `transmission_standing` نفسه — واصفٌ تُعاد بصمتُه، واشتقاقٌ غيرُ
متناظر، وبقيّةٌ ثالثةٌ لمن لم يقم عليه برهان — لا بافتراضٍ ولا بانتظار.

**والفرضيةُ المُختبَرة**: لسان العرب ليس مصدرًا متزامنًا بحقّ، إذ جمعه ابنُ منظور
من معاجمَ متعاقبةٍ مُسنَدةٍ بالاسم داخل نصّه (الخليل، والأزهريّ، والجوهريّ، وابن
سيده...). فإن **نُقِل** ذلك الإسنادُ الداخليُّ بنصّه في بطاقةٍ بعينها صارت بنيةُ
استشهادها `إسناد_داخلي_متعاقب_مُسمّى`؛ وإن اقتُصِر على العنوان بقيت
`عنوان_واحد_مسطَّح`، **وهذا خطأٌ فئويٌّ دائم** لا حجزٌ لغياب سلطة::

    FlatTitleCitation != TransmissionChain

**والإسنادُ الداخليُّ لا يُثبِت استقلالَ المصادر بحال**: كلُّه منقولٌ داخل نصّ
مُجمِّعٍ واحد، والنقلُ عن كتابٍ عينُ ما ينفي استحالةَ التواطؤ. فحاملُ الاستقلال
هنا `NOT_ESTABLISHED` بنيويًّا لا بحقلٍ يُكتَب، ولذلك **يبقى `متواتر` عضوًا بلا
مدخل** في هذا الطريق أيضًا، ويبقى `NO_IMPORT_ENTRY_FOR_A_FOREIGN_RECURRENCE_CLAIM_NOTE`
صادقًا على حاله.

**والوحدةُ تسجيلٌ وفحصٌ لا سلطة**: لا تُصدر ولادةً ولا حكمًا ولا تجميدًا ولا
`E0`، ولا تقرؤها وحدةٌ في `kernel/`.
"""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass, fields
from enum import Enum
from types import MappingProxyType
from typing import Any, Final

from alghanem.canonical_content import (
    canonical_bytes,
    canonical_digest,
    is_canonical_digest,
)

from .text_key import comparison_key
from .transmission_standing import (
    KnowledgeBasis,
    RepetitionPattern,
    SourceIndependence,
    TawaturQuestionStanding,
    TransmissionStanding,
    UnconstructibilityGenus,
    derive_standing,
)

_FORBIDDEN_COUNT_FIELD_MARKERS: Final = (
    "count",
    "number",
    "size",
    "total",
    "verdict",
    "birth",
)


class LexicalTransmissionError(ValueError):
    """رفضٌ صريحٌ في وحدة النقل المعجميّ؛ لا يُحمَل على أقرب حالةٍ مقبولة."""


class AttributionContentKind(Enum):
    """جنسُ محتوى الإسناد: أقولٌ منقولٌ عن سلطته، أم وصفُ استعمالٍ مُلخَّص؟"""

    نقل_قول_منسوب = "نقل_قول_منسوب"
    وصف_استعمال_ملخص = "وصف_استعمال_ملخص"


class LexicalCitationStructure(Enum):
    """بنيةُ الاستشهاد المعجميّ، مُشتَقّةً لا مُمرَّرة، باشتقاقٍ غير متناظر.

    `عنوان_واحد_مسطَّح` يُبرهَن بإعادة اشتقاق بصمة سلسلةٍ خاليةٍ (أو مفردةٍ لا
    تعاقبَ فيها): من أعلن أنّه لم ينقل إسنادًا داخليًّا أثبت على نفسه مسطَّحيّة
    استشهاده. و`إسناد_داخلي_متعاقب_مُسمّى` يُبرهَن بإعادة اشتقاق بصمة سلسلةٍ
    مُعدَّدةٍ مرتَّبة. أمّا من لم يُعلِن بصمةً أصلًا فبنيتُه غيرُ محسومة، ولا
    تُقرأ سالبةُ أحد الطرفين إثباتًا للآخر.
    """

    عنوان_واحد_مسطح = "عنوان_واحد_مسطح"
    إسناد_داخلي_متعاقب_مسمى = "إسناد_داخلي_متعاقب_مسمى"
    بنية_الاستشهاد_غير_محسومة = "بنية_الاستشهاد_غير_محسومة"


if len(AttributionContentKind) != 2:  # pragma: no cover - guard
    raise RuntimeError("an attribution is a transcribed saying or a summary")
if len(LexicalCitationStructure) != 3:  # pragma: no cover - guard
    raise RuntimeError(
        "a citation is provably flat, provably chained, or unsettled: a "
        "two-valued vocabulary would let exclusion alone prove a chain"
    )


LEXICAL_CHAIN_SCHEMA_VERSION: Final = "lexical-attribution-chain.v1"

CARD_LEXICAL_PATH_KEY: Final = "طريق_النقل_المعجمي"

ALLOWED_LEXICAL_PATH_KEYS: Final = ("المصدر", "المادة", "الإسنادات")

ALLOWED_ATTRIBUTION_KEYS: Final = (
    "السلطة",
    "الاقتباس_المنقول",
    "الموضع",
    "جنس_المحتوى",
)

FLAT_TITLE_CITATION_IS_NOT_A_TRANSMISSION_CHAIN_NOTE: Final = (
    "FlatTitleCitationIsNotATransmissionChain: الاستشهادُ بعنوان كتابٍ ومادّةٍ "
    "فيه تسميةُ موضعٍ لا وصفُ طريق ورود؛ فلا سلسلةَ فيه يقع فيها تعاقبٌ أصلًا، "
    "وسؤالُ التواتر عليه غيرُ مستقيم الوضع لا سؤالٌ بلا جوابٍ بعدُ ترفعه سلطةٌ "
    "تُبنى غدًا. وهذا خطأٌ فئويٌّ دائمٌ من جنس "
    "`TawaturRequiresDiachronicSuccession` لا حجزٌ لغياب أداة"
)

INTERNAL_ATTRIBUTION_IS_NOT_SOURCE_INDEPENDENCE_NOTE: Final = (
    "الإسنادُ الداخليُّ واقعةُ احتواءٍ في نصّ مُجمِّعٍ واحد لا برهانٌ على استقلال "
    "المصادر: ابنُ منظور ناقلٌ عن كتب، والنقلُ عن كتابٍ عينُ ما ينفي استحالةَ "
    "التواطؤ. فحاملُ الاستقلال `غير_مُثبَت` بنيويًّا، ولا حقلَ هنا يرفعه"
)

SUCCESSION_CARRIER_DOES_NOT_RAISE_A_STANDING_ALONE_NOTE: Final = (
    "بلوغُ `دورات_مستقلة_متعاقبة` بهذا الطريق لا يرفع درجةً بمفرده: الدرجةُ "
    "تُشتَقّ من الحوامل الثلاثة معًا، واستقلالُ المصادر غيرُ مُثبَتٍ هنا "
    "بنيويًّا؛ فمُخرَجُ هذا الطريق `آحاد` أو `فرض` لا غير"
)

MUTAWATIR_HAS_NO_ENTRY_ON_THIS_PATH_NOTE: Final = (
    "`متواتر` عضوٌ بلا مدخلٍ في هذا الطريق أيضًا، ومنعُه بنيويٌّ لا شرطيّ: "
    "اشتقاقُ الدرجة يمرّ بحاملٍ استقلالُه `غير_مُثبَت` دائمًا، فلا فرعَ يُخرِجه"
)

CHAIN_IS_REDERIVED_NOT_TRUSTED_NOTE: Final = (
    "بصمةُ السلسلة تُعاد اشتقاقها من تعداد الإسنادات نفسه ولا تُصدَّق مُعلَنةً: "
    "من لم يُعدّد إسناداته لم يُثبت بنيةَ استشهاده، ومن عدّدها أُلزِم بتعدادٍ "
    "مُعيَّنٍ لا يقبل واردًا صامتًا"
)

ORDER_IS_LOAD_BEARING_NOTE: Final = (
    "ترتيبُ الإسنادات دالٌّ هنا فلا يُفرَز قبل البصم، بخلاف تعداد "
    "`EvidenceBaseDescriptor`: الدعوى المُختبَرة تعاقبٌ، وتعاقبٌ مفروزٌ أبجديًّا "
    "ليس التعاقبَ المُدَّعى بل مجموعةٌ بلا ترتيب"
)

EMPTY_CHAIN_IS_A_CLAIM_NOT_A_CLOSURE_NOTE: Final = (
    "تعدادٌ خالٍ ببصمةٍ مُعادةِ الاشتقاق مقبولٌ هنا ومرفوضٌ في "
    "`EvidenceBaseDescriptor`، والفارقُ في جهة الدعوى: هناك يُدَّعى إغلاقٌ لا "
    "يُثبته خلاءٌ، وهنا يُدَّعى **انتفاءُ** سلسلةٍ منقولة، وهو ما يُثبته الخلاءُ "
    "نفسه مطابقةً بالبايت"
)

NEGATION_IS_NOT_PROOF_OF_THE_CONTRARY_NOTE: Final = (
    "«ليست سلسلةَ إسنادٍ متعاقبة» لا تُنتج «إذن عنوانٌ مسطَّح»، ولا العكس: "
    "بطاقةٌ لم تُعلن طريقَها المعجميَّ أصلًا بنيتُها غيرُ محسومة، ولا يُحمَل "
    "سكوتُها على أحد الطرفين"
)

LEXICAL_TRANSMISSION_IS_NOT_A_GATE_NOTE: Final = (
    "تسجيلٌ وفحصٌ فقط: لا تُصدر هذه الوحدة ولادةً ولا حكمًا ولا تجميدًا ولا "
    "`E0`، ولا تقرؤها أيّ بوّابةٍ في النواة"
)

LISAN_TEXT_IS_NOT_VENDORED_HERE: Final = "LISAN_TEXT_IS_NOT_VENDORED_HERE"

COMPILER_SYNCHRONY_IS_NOT_DECIDED_HERE: Final = "COMPILER_SYNCHRONY_IS_NOT_DECIDED_HERE"

NAMED_RESIDUALS: Final[Mapping[str, str]] = MappingProxyType(
    {
        LISAN_TEXT_IS_NOT_VENDORED_HERE: (
            "لا متنَ لسان العرب في هذا المستودع، فالإسناداتُ تبقى مُعلَنةً من "
            "المستدعي ولا شيءَ هنا يقابلها بنصّ المعجم — نظير "
            "`CLOSURE_ENUMERATION_IS_DECLARED_BY_ITS_CALLER`. والمتبدِّلُ أنّ "
            "المُعلَن صار دعوى بنيويّةً تُعاد مطابقتُها بالبايت، ويُلزَم كلُّ "
            "إسنادٍ باقتباسٍ يحتوي اسمَ سلطته، بدل عنوانٍ يُمرَّر بلا ما يفحصه"
        ),
        COMPILER_SYNCHRONY_IS_NOT_DECIDED_HERE: (
            "أمُعجَمُ ابن منظور في نفسه مقطعٌ متزامنٌ مُجمَّد أم لا؟ سؤالٌ لا "
            "تحسمه هذه الوحدة ولا تحتاج حسمَه: المفحوصُ هنا بنيةُ **الاستشهاد** "
            "في بطاقةٍ بعينها، لا بنيةُ المصدر في ذاته؛ وحسمُ الثاني يحتاج "
            "السلطةَ الزمنيّة الغائبة نفسها"
        ),
    }
)


def _require_non_blank(value: object, field_name: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise LexicalTransmissionError(f"{field_name} نصٌّ غير فارغ")
    return value


@dataclass(frozen=True, slots=True)
class LexicalAttribution:
    """إسنادٌ داخليٌّ واحد: سلطتُه المُسمّاة، واقتباسُه المنقول، وموضعُه."""

    attributed_authority: str
    verbatim_excerpt: str
    locus: str
    content_kind: AttributionContentKind = AttributionContentKind.نقل_قول_منسوب

    def __post_init__(self) -> None:
        _require_non_blank(self.attributed_authority, "سلطةُ الإسناد")
        _require_non_blank(self.verbatim_excerpt, "الاقتباسُ المنقول")
        _require_non_blank(self.locus, "موضعُ الإسناد")
        if not isinstance(self.content_kind, AttributionContentKind):
            raise LexicalTransmissionError("جنسُ محتوى الإسناد من مفردته المغلقة")
        if comparison_key(self.attributed_authority.strip()) not in comparison_key(
            self.verbatim_excerpt
        ):
            raise LexicalTransmissionError(
                "الاقتباسُ المنقول يحتوي اسمَ سلطته نصًّا وإلا فهو إحالةٌ مبهمة: "
                "إسنادٌ لا يُقرأ فيه المُسنَد إليه لا يُفحَص بالاحتواء أصلًا"
            )

    @property
    def encoded(self) -> list[str]:
        """ترميزُ الإسناد للبصم؛ حقولُه كلُّها ولا شيءَ سواها."""

        return [
            self.attributed_authority.strip(),
            self.verbatim_excerpt.strip(),
            self.locus.strip(),
            self.content_kind.value,
        ]


def lexical_chain_digest(
    entry_id: str, entry_locus: str, attributions: tuple[LexicalAttribution, ...]
) -> str:
    """اشتقّ بصمةَ سلسلة الإسناد من المدخل وموضعه وتعداده **مرتَّبًا**."""

    identifier = _require_non_blank(entry_id, "معرّف المدخل المعجميّ").strip()
    locus = _require_non_blank(entry_locus, "مادّةُ المدخل").strip()
    if not isinstance(attributions, tuple):
        raise LexicalTransmissionError("تعدادُ الإسنادات مجموعةٌ مرتَّبة")
    encoded: list[object] = [LEXICAL_CHAIN_SCHEMA_VERSION, identifier, locus]
    for attribution in attributions:
        if not isinstance(attribution, LexicalAttribution):
            raise LexicalTransmissionError("كلُّ إسنادٍ من نوع `LexicalAttribution`")
        encoded.append(attribution.encoded)
    return canonical_digest(canonical_bytes(encoded))


@dataclass(frozen=True, slots=True)
class LexicalTransmissionDescriptor:
    """واصفُ استشهادٍ معجميٍّ ببصمة سلسلته، يُفحَص ولا يُصدَّق."""

    entry_id: str
    compiler_source: str
    entry_locus: str
    attributions: tuple[LexicalAttribution, ...] = ()
    declared_chain_digest: str | None = None

    def __post_init__(self) -> None:
        _require_non_blank(self.entry_id, "معرّف المدخل المعجميّ")
        _require_non_blank(self.compiler_source, "المصدرُ المُجمِّع")
        _require_non_blank(self.entry_locus, "مادّةُ المدخل")
        if not isinstance(self.attributions, tuple):
            raise LexicalTransmissionError("تعدادُ الإسنادات مجموعةٌ مرتَّبة")
        encoded = []
        for attribution in self.attributions:
            if not isinstance(attribution, LexicalAttribution):
                raise LexicalTransmissionError("كلُّ إسنادٍ من نوع `LexicalAttribution`")
            encoded.append(tuple(attribution.encoded))
        if len(set(encoded)) != len(encoded):
            raise LexicalTransmissionError(
                "إسنادٌ مكرَّرٌ في السلسلة: تكرارُ النقل ليس تعاقبَ سلطتين، "
                "وعدّه سلسلتين يُنتج تعاقبًا موهومًا من نقلٍ واحد"
            )
        if self.declared_chain_digest is None:
            return
        if not is_canonical_digest(self.declared_chain_digest):
            raise LexicalTransmissionError(
                "بصمةُ السلسلة المُعلَنة على شكل البصمة القانونيّة أو لا تكون"
            )
        if self.declared_chain_digest != lexical_chain_digest(
            self.entry_id, self.entry_locus, self.attributions
        ):
            raise LexicalTransmissionError(CHAIN_IS_REDERIVED_NOT_TRUSTED_NOTE)

    @property
    def chain_is_rederived(self) -> bool:
        """أأُعيد اشتقاقُ بصمة السلسلة فعلًا؟ مُشتَقٌّ من نجاح الإنشاء نفسه."""

        return self.declared_chain_digest is not None

    @property
    def naql_source(self) -> str:
        """مصدرُ النقل كما يُكتَب في `WadRecord`: المُجمِّعُ ومادّتُه معًا."""

        return f"{self.compiler_source.strip()}، {self.entry_locus.strip()}"


def flat_title_citation(
    entry_id: str, compiler_source: str, entry_locus: str
) -> LexicalTransmissionDescriptor:
    """ابنِ واصفًا يُعلِن انتفاءَ سلسلةٍ منقولة، ببصمته المُشتَقّة."""

    return LexicalTransmissionDescriptor(
        entry_id=entry_id,
        compiler_source=compiler_source,
        entry_locus=entry_locus,
        attributions=(),
        declared_chain_digest=lexical_chain_digest(entry_id, entry_locus, ()),
    )


def attested_lexical_chain(
    entry_id: str,
    compiler_source: str,
    entry_locus: str,
    attributions: tuple[LexicalAttribution, ...],
) -> LexicalTransmissionDescriptor:
    """ابنِ واصفًا بسلسلةٍ مُعدَّدةٍ مرتَّبة، ببصمتها المُشتَقّة."""

    return LexicalTransmissionDescriptor(
        entry_id=entry_id,
        compiler_source=compiler_source,
        entry_locus=entry_locus,
        attributions=attributions,
        declared_chain_digest=lexical_chain_digest(entry_id, entry_locus, attributions),
    )


def derive_lexical_citation_structure(
    descriptor: LexicalTransmissionDescriptor,
) -> LexicalCitationStructure:
    """اشتقّ بنيةَ الاستشهاد؛ دالّةٌ تامّةٌ لا تُنتج طرفًا من سالبة الآخر."""

    if not isinstance(descriptor, LexicalTransmissionDescriptor):
        raise LexicalTransmissionError("بنيةُ الاستشهاد تُشتَقّ من واصفها")
    if not descriptor.chain_is_rederived:
        return LexicalCitationStructure.بنية_الاستشهاد_غير_محسومة
    if len(descriptor.attributions) >= 2:
        return LexicalCitationStructure.إسناد_داخلي_متعاقب_مسمى
    return LexicalCitationStructure.عنوان_واحد_مسطح


def _genus_of_lexical_structure(
    structure: LexicalCitationStructure,
) -> UnconstructibilityGenus:
    """صِلْ كلَّ بنيةٍ بجنس امتناعها؛ دالّةٌ تامّة بلا فرعٍ افتراضيّ."""

    if structure is LexicalCitationStructure.عنوان_واحد_مسطح:
        return UnconstructibilityGenus.REFUSED_BY_STRUCTURAL_CATEGORY_MISMATCH
    if structure is LexicalCitationStructure.إسناد_داخلي_متعاقب_مسمى:
        return UnconstructibilityGenus.HELD_BY_MISSING_AUTHORITY_TODAY
    return UnconstructibilityGenus.GENUS_NOT_SETTLED


def lexical_unconstructibility_genus(
    descriptor: LexicalTransmissionDescriptor,
) -> UnconstructibilityGenus:
    """اشتقّ جنسَ امتناع `متواتر` على هذا الاستشهاد من واصفه لا من تصنيفٍ مُمرَّر."""

    return _genus_of_lexical_structure(derive_lexical_citation_structure(descriptor))


def lexical_tawatur_question_standing(
    descriptor: LexicalTransmissionDescriptor,
) -> TawaturQuestionStanding:
    """أمستقيمُ الوضع سؤالُ التواتر على هذا الاستشهاد؟ مُشتَقٌّ لا مكتوب."""

    genus = lexical_unconstructibility_genus(descriptor)
    if genus is UnconstructibilityGenus.REFUSED_BY_STRUCTURAL_CATEGORY_MISMATCH:
        return TawaturQuestionStanding.ILL_POSED_ON_THIS_STRUCTURE
    if genus is UnconstructibilityGenus.HELD_BY_MISSING_AUTHORITY_TODAY:
        return TawaturQuestionStanding.WELL_POSED_AND_UNVERIFIED_HERE
    return TawaturQuestionStanding.STANDING_NOT_SETTLED_ON_THIS_STRUCTURE


def derive_lexical_carriers(
    descriptor: LexicalTransmissionDescriptor,
) -> tuple[KnowledgeBasis, SourceIndependence, RepetitionPattern]:
    """اشتقّ حواملَ الدرجة الثلاثة من سلسلةٍ مُعدَّدةٍ مُعادةِ الاشتقاق وحدها.

    ولا حواملَ لاستشهادٍ مسطَّحٍ ولا لغير محسوم: الأوّلُ ممتنعٌ فئويًّا فحواملُه
    تصنعُ طريقًا حيث لا طريق، والثاني لم يُعلِن ما يُشتَقّ منه أصلًا.
    """

    structure = derive_lexical_citation_structure(descriptor)
    if structure is not LexicalCitationStructure.إسناد_داخلي_متعاقب_مسمى:
        raise LexicalTransmissionError(
            "لا حواملَ تُشتَقّ من هذه البنية. "
            + FLAT_TITLE_CITATION_IS_NOT_A_TRANSMISSION_CHAIN_NOTE
        )
    basis = (
        KnowledgeBasis.DIRECT_OBSERVATION
        if all(
            attribution.content_kind is AttributionContentKind.نقل_قول_منسوب
            for attribution in descriptor.attributions
        )
        else KnowledgeBasis.INFERENCE
    )
    return (
        basis,
        SourceIndependence.NOT_ESTABLISHED,
        RepetitionPattern.SUCCESSIVE_GENERATIONS,
    )


@dataclass(frozen=True, slots=True)
class LexicalWadPath:
    """جسرٌ رقيق: يُخرِج درجةَ النقل المُشتَقّة ليُبنى منها `WadRecord` هناك."""

    descriptor: LexicalTransmissionDescriptor

    def __post_init__(self) -> None:
        if not isinstance(self.descriptor, LexicalTransmissionDescriptor):
            raise LexicalTransmissionError("طريقُ الوضع يقوم على واصفٍ معجميّ")

    @property
    def structure(self) -> LexicalCitationStructure:
        return derive_lexical_citation_structure(self.descriptor)

    @property
    def genus(self) -> UnconstructibilityGenus:
        return lexical_unconstructibility_genus(self.descriptor)

    @property
    def question_standing(self) -> TawaturQuestionStanding:
        return lexical_tawatur_question_standing(self.descriptor)

    @property
    def standing(self) -> TransmissionStanding | None:
        """درجةُ النقل المُشتَقّة، أو لا شيءَ حين لا طريقَ أصلًا."""

        if self.structure is not LexicalCitationStructure.إسناد_داخلي_متعاقب_مسمى:
            return None
        derived = derive_standing(*derive_lexical_carriers(self.descriptor))
        if derived is TransmissionStanding.MUTAWATIR:  # pragma: no cover - guard
            raise RuntimeError(MUTAWATIR_HAS_NO_ENTRY_ON_THIS_PATH_NOTE)
        return derived

    @property
    def naql_source(self) -> str:
        return self.descriptor.naql_source


def _canonical_content_kind(value: object) -> AttributionContentKind:
    key = comparison_key(_require_non_blank(value, "الإسنادات[].جنس_المحتوى"))
    for member in AttributionContentKind:
        if comparison_key(member.value) == key:
            return member
    allowed = "، ".join(member.value for member in AttributionContentKind)
    raise LexicalTransmissionError(
        "الإسنادات[].جنس_المحتوى يجب أن يكون أحد: " + allowed
    )


def read_lexical_transmission(
    card: Mapping[str, Any],
) -> LexicalTransmissionDescriptor | None:
    """اقرأ طريقَ النقل المعجميّ من البطاقة، أو لا شيءَ إن لم تُعلِنه.

    وبطاقةٌ لم تُعلِن الحقلَ أصلًا لا يُقرأ سكوتُها تسطيحًا ولا تعاقبًا: تُنتج
    `None`، وبنيتُها عند الاشتقاق `بنية_الاستشهاد_غير_محسومة`.
    """

    if not isinstance(card, Mapping):
        raise LexicalTransmissionError("البطاقةُ كائنٌ يُقرأ بمفاتيحه")
    raw = card.get(CARD_LEXICAL_PATH_KEY)
    if raw is None:
        return None
    if not isinstance(raw, Mapping):
        raise LexicalTransmissionError(f"{CARD_LEXICAL_PATH_KEY} كائنٌ لا نصّ")
    allowed = {comparison_key(name) for name in ALLOWED_LEXICAL_PATH_KEYS}
    if {comparison_key(str(key)) for key in raw} - allowed:
        raise LexicalTransmissionError(
            f"{CARD_LEXICAL_PATH_KEY} لا يقبل إلا: "
            + "، ".join(ALLOWED_LEXICAL_PATH_KEYS)
        )
    compiler_source = _require_non_blank(raw.get("المصدر"), "المصدر")
    entry_locus = _require_non_blank(raw.get("المادة"), "المادة")
    entries = raw.get("الإسنادات")
    if not isinstance(entries, list):
        raise LexicalTransmissionError(
            "الإسنادات قائمةٌ تُعدَّد ولو خالية؛ وغيابُها إعلانٌ ناقصٌ لا تسطيحٌ " "مُثبَت"
        )
    allowed_attribution = {comparison_key(name) for name in ALLOWED_ATTRIBUTION_KEYS}
    attributions: list[LexicalAttribution] = []
    for entry in entries:
        if not isinstance(entry, Mapping):
            raise LexicalTransmissionError("كلُّ إسنادٍ كائنٌ يُقرأ بمفاتيحه")
        if {comparison_key(str(key)) for key in entry} - allowed_attribution:
            raise LexicalTransmissionError(
                "الإسنادات[] لا تقبل إلا: " + "، ".join(ALLOWED_ATTRIBUTION_KEYS)
            )
        declared_kind = entry.get("جنس_المحتوى")
        attributions.append(
            LexicalAttribution(
                attributed_authority=_require_non_blank(
                    entry.get("السلطة"), "الإسنادات[].السلطة"
                ),
                verbatim_excerpt=_require_non_blank(
                    entry.get("الاقتباس_المنقول"), "الإسنادات[].الاقتباس_المنقول"
                ),
                locus=_require_non_blank(entry.get("الموضع"), "الإسنادات[].الموضع"),
                content_kind=(
                    AttributionContentKind.نقل_قول_منسوب
                    if declared_kind is None
                    else _canonical_content_kind(declared_kind)
                ),
            )
        )
    entry_id = _require_non_blank(card.get("معرف_السؤال"), "معرف_السؤال")
    return attested_lexical_chain(
        entry_id=entry_id,
        compiler_source=compiler_source,
        entry_locus=entry_locus,
        attributions=tuple(attributions),
    )


def card_lexical_wad_path(card: Mapping[str, Any]) -> LexicalWadPath | None:
    """طريقُ الوضع المعجميُّ لبطاقةٍ بعينها، أو لا شيءَ إن لم تُعلِنه."""

    descriptor = read_lexical_transmission(card)
    return None if descriptor is None else LexicalWadPath(descriptor)


def card_lexical_citation_structure(
    card: Mapping[str, Any],
) -> LexicalCitationStructure:
    """بنيةُ الاستشهاد المعجميّ لبطاقةٍ بعينها؛ وغيابُ الإعلان لا يُحسَم."""

    descriptor = read_lexical_transmission(card)
    if descriptor is None:
        return LexicalCitationStructure.بنية_الاستشهاد_غير_محسومة
    return derive_lexical_citation_structure(descriptor)


def card_transmission_standing(
    card: Mapping[str, Any],
) -> TransmissionStanding | None:
    """درجةُ النقل المُشتَقّة لبطاقةٍ بعينها، أو لا شيءَ حين لا طريقَ لها."""

    path = card_lexical_wad_path(card)
    return None if path is None else path.standing


def _assert_no_fields_matching(
    declaring_type: type, markers: tuple[str, ...], message: str
) -> None:
    for item in fields(declaring_type):
        if any(marker in item.name for marker in markers):
            raise RuntimeError(message)


for _declaring_type in (
    LexicalAttribution,
    LexicalTransmissionDescriptor,
    LexicalWadPath,
):
    _assert_no_fields_matching(
        _declaring_type,
        _FORBIDDEN_COUNT_FIELD_MARKERS,
        "no type here may carry a count, size, verdict, or birth field",
    )


__all__ = [
    "ALLOWED_ATTRIBUTION_KEYS",
    "ALLOWED_LEXICAL_PATH_KEYS",
    "CARD_LEXICAL_PATH_KEY",
    "CHAIN_IS_REDERIVED_NOT_TRUSTED_NOTE",
    "COMPILER_SYNCHRONY_IS_NOT_DECIDED_HERE",
    "EMPTY_CHAIN_IS_A_CLAIM_NOT_A_CLOSURE_NOTE",
    "FLAT_TITLE_CITATION_IS_NOT_A_TRANSMISSION_CHAIN_NOTE",
    "INTERNAL_ATTRIBUTION_IS_NOT_SOURCE_INDEPENDENCE_NOTE",
    "LEXICAL_CHAIN_SCHEMA_VERSION",
    "LEXICAL_TRANSMISSION_IS_NOT_A_GATE_NOTE",
    "LISAN_TEXT_IS_NOT_VENDORED_HERE",
    "MUTAWATIR_HAS_NO_ENTRY_ON_THIS_PATH_NOTE",
    "NAMED_RESIDUALS",
    "NEGATION_IS_NOT_PROOF_OF_THE_CONTRARY_NOTE",
    "ORDER_IS_LOAD_BEARING_NOTE",
    "SUCCESSION_CARRIER_DOES_NOT_RAISE_A_STANDING_ALONE_NOTE",
    "AttributionContentKind",
    "LexicalAttribution",
    "LexicalCitationStructure",
    "LexicalTransmissionDescriptor",
    "LexicalTransmissionError",
    "LexicalWadPath",
    "attested_lexical_chain",
    "card_lexical_citation_structure",
    "card_lexical_wad_path",
    "card_transmission_standing",
    "derive_lexical_carriers",
    "derive_lexical_citation_structure",
    "flat_title_citation",
    "lexical_chain_digest",
    "lexical_tawatur_question_standing",
    "lexical_unconstructibility_genus",
    "read_lexical_transmission",
]
