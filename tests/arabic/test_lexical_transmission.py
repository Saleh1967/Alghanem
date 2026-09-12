"""اختبارُ بنية الاستشهاد المعجميّ، وسَوقُ البطاقات الثلاث على الفرع نفسه.

والمقصودُ حسمُ سؤالٍ واحد: أوقوفُ البطاقات عند الحلقة الرابعة خطأٌ فئويٌّ دائم
أم فجوةٌ مؤقّتة؟ فيُشتَقّ الجوابُ من واصفٍ يُفحَص، ويُسجَّل لكلّ بطاقةٍ ما جرى
فعلًا: بنيتُها، وجنسُ امتناعها، وحالُ سؤال التواتر عليها، ودرجتُها إن قامت.
"""

import json
from pathlib import Path
from typing import Any, Final

import pytest
from card_traversal import first_stop, traverse

from alghanem.arabic.lexical_transmission import (
    CARD_LEXICAL_PATH_KEY,
    LEXICAL_CHAIN_SCHEMA_VERSION,
    NAMED_RESIDUALS,
    AttributionContentKind,
    LexicalAttribution,
    LexicalCitationStructure,
    LexicalTransmissionDescriptor,
    LexicalTransmissionError,
    LexicalWadPath,
    attested_lexical_chain,
    card_lexical_citation_structure,
    card_lexical_wad_path,
    card_transmission_standing,
    derive_lexical_carriers,
    derive_lexical_citation_structure,
    flat_title_citation,
    lexical_chain_digest,
    lexical_tawatur_question_standing,
    lexical_unconstructibility_genus,
    read_lexical_transmission,
)
from alghanem.arabic.transmission_standing import (
    KnowledgeBasis,
    RepetitionPattern,
    SourceIndependence,
    TawaturQuestionStanding,
    TransmissionStanding,
    UnconstructibilityGenus,
)
from alghanem.arabic.wad_naql import WadRecord

_EXAMPLES: Final = Path(__file__).resolve().parents[2] / "examples" / "external_audit"
_CARDS: Final = ("quru_2_228.yaml", "anna_2_223.yaml", "malik_114_2.yaml")

_COMPILER: Final = "لسان العرب لابن منظور"


def _card(name: str) -> dict[str, Any]:
    payload = json.loads((_EXAMPLES / name).read_text(encoding="utf-8"))
    assert isinstance(payload, dict)
    return payload


def _chain() -> tuple[LexicalAttribution, ...]:
    return (
        LexicalAttribution(
            attributed_authority="الأزهري",
            verbatim_excerpt="قال الأزهري: كذا وكذا في هذه المادّة",
            locus="مادّةٌ مُسمّاة",
        ),
        LexicalAttribution(
            attributed_authority="الجوهري",
            verbatim_excerpt="وقال الجوهري: كذا وكذا في هذه المادّة",
            locus="مادّةٌ مُسمّاة",
        ),
    )


def test_an_attribution_whose_excerpt_omits_its_authority_is_refused() -> None:
    """إسنادٌ لا يُقرأ فيه المُسنَد إليه إحالةٌ مبهمة لا إسناد."""

    with pytest.raises(LexicalTransmissionError):
        LexicalAttribution(
            attributed_authority="الخليل",
            verbatim_excerpt="قال بعضهم: كذا",
            locus="مادّةٌ مُسمّاة",
        )


def test_a_declared_chain_digest_is_rederived_not_trusted() -> None:
    """البصمةُ المخالفة رفضٌ عند الإنشاء، لا حالٌ «غير محسومة»."""

    attributions = _chain()
    with pytest.raises(LexicalTransmissionError):
        LexicalTransmissionDescriptor(
            entry_id="e",
            compiler_source=_COMPILER,
            entry_locus="م ل ك",
            attributions=attributions,
            declared_chain_digest="0" * 64,
        )
    descriptor = attested_lexical_chain("e", _COMPILER, "م ل ك", attributions)
    assert descriptor.declared_chain_digest == lexical_chain_digest(
        "e", "م ل ك", attributions
    )
    assert descriptor.chain_is_rederived is True


def test_the_order_of_attributions_is_load_bearing() -> None:
    """الترتيبُ دالٌّ فلا يُفرَز قبل البصم: سلسلتان مختلفتان بصمتان."""

    first, second = _chain()
    assert lexical_chain_digest("e", "م ل ك", (first, second)) != lexical_chain_digest(
        "e", "م ل ك", (second, first)
    )
    assert LEXICAL_CHAIN_SCHEMA_VERSION == "lexical-attribution-chain.v1"


def test_a_repeated_attribution_is_refused() -> None:
    """تكرارُ النقل ليس تعاقبَ سلطتين، فلا يُعدُّ سلسلتين."""

    first, _ = _chain()
    with pytest.raises(LexicalTransmissionError):
        attested_lexical_chain("e", _COMPILER, "م ل ك", (first, first))


def test_the_three_structures_are_derived_each_from_its_own_proof() -> None:
    """المسطَّحُ والمتعاقبُ يُبرهَنان، وغيرُ المُعلِن يبقى غيرَ محسوم."""

    flat = flat_title_citation("e", _COMPILER, "م ل ك")
    chained = attested_lexical_chain("e", _COMPILER, "م ل ك", _chain())
    undeclared = LexicalTransmissionDescriptor(
        entry_id="e", compiler_source=_COMPILER, entry_locus="م ل ك"
    )

    assert (
        derive_lexical_citation_structure(flat)
        is LexicalCitationStructure.عنوان_واحد_مسطح
    )
    assert (
        derive_lexical_citation_structure(chained)
        is LexicalCitationStructure.إسناد_داخلي_متعاقب_مسمى
    )
    assert (
        derive_lexical_citation_structure(undeclared)
        is LexicalCitationStructure.بنية_الاستشهاد_غير_محسومة
    )


def test_a_single_attribution_is_not_a_succession() -> None:
    """إسنادٌ واحدٌ موضعٌ مُسمًّى لا سلسلةٌ متعاقبة، فيبقى الاستشهادُ مسطَّحًا."""

    first, _ = _chain()
    descriptor = attested_lexical_chain("e", _COMPILER, "م ل ك", (first,))

    assert (
        derive_lexical_citation_structure(descriptor)
        is LexicalCitationStructure.عنوان_واحد_مسطح
    )


def test_the_genus_and_the_question_standing_follow_the_structure() -> None:
    """المسطَّحُ خطأٌ فئويٌّ دائم، والمتعاقبُ حجزٌ لغياب سلطة، والباقي غيرُ محسوم."""

    flat = flat_title_citation("e", _COMPILER, "م ل ك")
    chained = attested_lexical_chain("e", _COMPILER, "م ل ك", _chain())
    undeclared = LexicalTransmissionDescriptor(
        entry_id="e", compiler_source=_COMPILER, entry_locus="م ل ك"
    )

    assert lexical_unconstructibility_genus(flat) is (
        UnconstructibilityGenus.REFUSED_BY_STRUCTURAL_CATEGORY_MISMATCH
    )
    assert lexical_tawatur_question_standing(flat) is (
        TawaturQuestionStanding.ILL_POSED_ON_THIS_STRUCTURE
    )
    assert lexical_unconstructibility_genus(chained) is (
        UnconstructibilityGenus.HELD_BY_MISSING_AUTHORITY_TODAY
    )
    assert lexical_tawatur_question_standing(chained) is (
        TawaturQuestionStanding.WELL_POSED_AND_UNVERIFIED_HERE
    )
    assert lexical_unconstructibility_genus(undeclared) is (
        UnconstructibilityGenus.GENUS_NOT_SETTLED
    )
    assert lexical_tawatur_question_standing(undeclared) is (
        TawaturQuestionStanding.STANDING_NOT_SETTLED_ON_THIS_STRUCTURE
    )


def test_source_independence_is_never_established_on_this_path() -> None:
    """النقلُ عن كتابٍ عينُ ما ينفي استحالةَ التواطؤ، فلا حقلَ يرفعه."""

    descriptor = attested_lexical_chain("e", _COMPILER, "م ل ك", _chain())
    basis, independence, repetition = derive_lexical_carriers(descriptor)

    assert basis is KnowledgeBasis.DIRECT_OBSERVATION
    assert independence is SourceIndependence.NOT_ESTABLISHED
    assert repetition is RepetitionPattern.SUCCESSIVE_GENERATIONS
    assert LexicalWadPath(descriptor).standing is TransmissionStanding.AHAD


def test_a_summarized_attribution_yields_fard_not_ahad() -> None:
    """وصفُ الاستعمال المُلخَّص استنتاجٌ لا مشاهدة، فدرجتُه `فرض`."""

    first, second = _chain()
    summarized = LexicalAttribution(
        attributed_authority=second.attributed_authority,
        verbatim_excerpt=second.verbatim_excerpt,
        locus=second.locus,
        content_kind=AttributionContentKind.وصف_استعمال_ملخص,
    )
    descriptor = attested_lexical_chain("e", _COMPILER, "م ل ك", (first, summarized))

    assert derive_lexical_carriers(descriptor)[0] is KnowledgeBasis.INFERENCE
    assert LexicalWadPath(descriptor).standing is TransmissionStanding.FARD


def test_mutawatir_has_no_entry_on_this_path() -> None:
    """`متواتر` عضوٌ بلا مدخل، ومنعُه بنيويٌّ في كلّ فرعٍ من فروع الاشتقاق."""

    descriptors = (
        attested_lexical_chain("e", _COMPILER, "م ل ك", _chain()),
        attested_lexical_chain("e", _COMPILER, "م ل ك", _chain()[:1]),
        flat_title_citation("e", _COMPILER, "م ل ك"),
        LexicalTransmissionDescriptor("e", _COMPILER, "م ل ك"),
    )

    assert all(
        LexicalWadPath(descriptor).standing is not TransmissionStanding.MUTAWATIR
        for descriptor in descriptors
    )


def test_no_carriers_are_derived_from_a_flat_or_unsettled_citation() -> None:
    """لا حواملَ حيث لا طريق: اشتقاقُها هناك يصنع طريقًا لا يوجد."""

    for descriptor in (
        flat_title_citation("e", _COMPILER, "م ل ك"),
        LexicalTransmissionDescriptor("e", _COMPILER, "م ل ك"),
    ):
        with pytest.raises(LexicalTransmissionError):
            derive_lexical_carriers(descriptor)
        assert LexicalWadPath(descriptor).standing is None


def test_a_derived_standing_records_a_wad_without_touching_wad_naql() -> None:
    """الجسرُ يُخرِج الدرجةَ فيُبنى منها `WadRecord` كما هو بلا تعديل."""

    path = LexicalWadPath(attested_lexical_chain("e", _COMPILER, "م ل ك", _chain()))
    standing = path.standing
    assert standing is not None

    record = WadRecord(
        lafz="مَلِك",
        madlul="ذو سلطان",
        naql_source=path.naql_source,
        transmission=standing,
    )

    assert record.transmission is TransmissionStanding.AHAD
    assert record.naql_source == f"{_COMPILER}، م ل ك"


def test_a_card_without_the_declaration_is_not_read_as_flat() -> None:
    """سكوتُ البطاقة لا يُحمَل على أحد الطرفين، بل يبقى غيرَ محسوم."""

    assert read_lexical_transmission({}) is None
    assert card_lexical_wad_path({}) is None
    assert (
        card_lexical_citation_structure({})
        is LexicalCitationStructure.بنية_الاستشهاد_غير_محسومة
    )


def test_a_card_path_with_an_unknown_key_is_refused() -> None:
    """المفتاحُ غيرُ المُسمّى يُسقِط القراءة بدل أن يُهمَل صامتًا."""

    card = {
        "معرف_السؤال": "q",
        CARD_LEXICAL_PATH_KEY: {
            "المصدر": _COMPILER,
            "المادة": "م ل ك",
            "الإسنادات": [],
            "درجة": "متواتر",
        },
    }

    with pytest.raises(LexicalTransmissionError):
        read_lexical_transmission(card)


def test_a_card_path_without_an_attribution_list_is_refused() -> None:
    """غيابُ التعداد إعلانٌ ناقصٌ لا تسطيحٌ مُثبَت."""

    card = {
        "معرف_السؤال": "q",
        CARD_LEXICAL_PATH_KEY: {"المصدر": _COMPILER, "المادة": "م ل ك"},
    }

    with pytest.raises(LexicalTransmissionError):
        read_lexical_transmission(card)


@pytest.mark.parametrize("name", _CARDS)
def test_each_card_declares_a_flat_title_citation_today(name: str) -> None:
    """المُخرَجُ الفعليُّ للاختبار: البطاقاتُ الثلاث مسطَّحةٌ لا متعاقبة."""

    card = _card(name)
    path = card_lexical_wad_path(card)

    assert path is not None
    assert path.structure is LexicalCitationStructure.عنوان_واحد_مسطح
    assert path.genus is (
        UnconstructibilityGenus.REFUSED_BY_STRUCTURAL_CATEGORY_MISMATCH
    )
    assert path.question_standing is TawaturQuestionStanding.ILL_POSED_ON_THIS_STRUCTURE
    assert path.standing is None
    assert card_transmission_standing(card) is None


@pytest.mark.parametrize("name", _CARDS)
def test_every_card_still_stops_at_the_fourth_link_by_a_named_genus(name: str) -> None:
    """الوقوفُ واحدٌ في البطاقات الثلاث، ومُعلَّلٌ ببنيةٍ مُشتَقّة لا بانتظار."""

    stop = first_stop(traverse(_card(name)))

    assert stop is not None
    assert stop.label == "٤"
    assert stop.module_relative_path == "wad_naql.py"
    assert "عنوان_واحد_مسطح" in stop.missing_declaration
    assert "ممتنعة_بخطأ_فئوي_بنيوي" in stop.missing_declaration


def test_the_unraised_residuals_are_named_not_silent() -> None:
    """ما لم يُرفَع مُسمًّى: لا متنَ للمعجم هنا، ولا حسمَ لتزامن المُجمِّع."""

    assert set(NAMED_RESIDUALS) == {
        "LISAN_TEXT_IS_NOT_VENDORED_HERE",
        "COMPILER_SYNCHRONY_IS_NOT_DECIDED_HERE",
    }
    assert all(text.strip() for text in NAMED_RESIDUALS.values())


def test_this_module_issues_no_verdict_and_carries_no_count() -> None:
    """فحصٌ وتسجيلٌ لا سلطة: لا حقلَ عددٍ ولا حكمٍ ولا ولادةٍ في أنواعها."""

    forbidden = ("count", "number", "size", "total", "verdict", "birth", "rank")

    for declaring_type in (
        LexicalAttribution,
        LexicalTransmissionDescriptor,
        LexicalWadPath,
    ):
        assert all(
            marker not in name
            for name in declaring_type.__slots__
            for marker in forbidden
        )
