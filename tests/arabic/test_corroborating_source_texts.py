"""النصُّ المُعاضِدُ من «مقاييس اللغة»: نقلٌ يُفحَص بالاحتواء، وحدٌّ لا يُطوى.

الاختبارُ هنا يُثبِت أربعةَ أشياء لا خامسَ لها: أنّ المنقولَ يقع حرفُه في نصّه،
وأنّ المُعاضِدَ **لا يدخل خانةَ مرجعٍ ولا يُغيِّر موقفَ بند**، وأنّ موضعَه
`موضع_غير_متحقق` لأنّ رقمَ الإدخال ليس ترقيمَ طبعة، وأنّ بقيّةَ الفرق بين
الاشتقاق التسمويّ وحال اللفظ الصرفيّ مُسمّاةٌ في النصّ وفي بند «جامد/مشتق» معًا.
"""

from __future__ import annotations

import pytest

from alghanem.arabic.sentence_card_preregistration import (
    SENTENCE_CARD_PREREGISTRATION,
    CardItem,
    FrozenReference,
    ItemStanding,
)
from alghanem.arabic.sentence_card_source_texts import (
    CORROBORATING_SOURCE_TEXTS,
    CORROBORATION_IS_NOT_A_DECLARED_REFERENCE_NOTE,
    ETYMOLOGICAL_DERIVATION_IS_NOT_MORPHOLOGICAL_STATUS_NOTE,
    MAQAYIS_NUR_ENTRY,
    SUPPLIED_SOURCE_TEXTS,
    CorroboratingSourceText,
    LocusVerification,
    SourceTextError,
    corroborating_text_for,
    require_attested_corroborating_excerpt,
)


def _replacement(**changes: object) -> CorroboratingSourceText:
    base = {
        "key": "K",
        "source_name": "كتابٌ مُسمًّى",
        "locus_statement": "موضعٌ مُسمًّى",
        "locus_verification": LocusVerification.موضع_غير_متحقق,
        "verbatim_text": "حروفٌ منقولة",
        "corroborated_items": (CardItem.WAZN,),
        "internal_authorities": (),
        "named_residuals": ("CORROBORATION_IS_NOT_A_DECLARED_REFERENCE",),
    }
    base.update(changes)
    return CorroboratingSourceText(**base)  # type: ignore[arg-type]


def test_the_corroborating_registry_is_exactly_the_maqayis_entry() -> None:
    assert tuple(CORROBORATING_SOURCE_TEXTS) == ("MAQAYIS_NUR_ENTRY",)
    assert corroborating_text_for("MAQAYIS_NUR_ENTRY") is MAQAYIS_NUR_ENTRY
    assert "مقاييس اللغة" in MAQAYIS_NUR_ENTRY.source_name
    assert "ابن فارس" in MAQAYIS_NUR_ENTRY.source_name.replace("بن فارس", "ابن فارس")


def test_an_unregistered_corroborating_key_is_refused_not_coerced() -> None:
    with pytest.raises(SourceTextError, match="لا نصَّ مُعاضِدًا"):
        corroborating_text_for("MAQAYIS_NUR")


def test_the_corroborating_text_is_not_a_supplied_text_of_any_item() -> None:
    assert "MAQAYIS_NUR_ENTRY" not in SUPPLIED_SOURCE_TEXTS
    assert not hasattr(MAQAYIS_NUR_ENTRY, "reference")
    assert not hasattr(MAQAYIS_NUR_ENTRY, "item")
    assert MAQAYIS_NUR_ENTRY.changes_no_item_standing is True


def test_no_item_declares_the_corroborating_book_as_its_reference() -> None:
    for registration in SENTENCE_CARD_PREREGISTRATION.registrations:
        assert isinstance(registration.reference, FrozenReference)
        assert "مقاييس" not in registration.reference.value
    assert len(FrozenReference) == 3


def test_the_corroborated_items_keep_the_standings_they_had() -> None:
    standings = {
        item: SENTENCE_CARD_PREREGISTRATION.registration_for(item).standing
        for item in MAQAYIS_NUR_ENTRY.corroborated_items
    }
    assert standings == {
        CardItem.WAZN: ItemStanding.SOURCE_TEXT_SUPPLIED_WITHOUT_CERTIFICATE,
        CardItem.ISHTIQAQ_SARF: ItemStanding.SOURCE_TEXT_SUPPLIED_WITHOUT_CERTIFICATE,
        CardItem.JAMID_MUSHTAQ: ItemStanding.AWAITING_SOURCE_TEXT,
    }
    for item in MAQAYIS_NUR_ENTRY.corroborated_items:
        registration = SENTENCE_CARD_PREREGISTRATION.registration_for(item)
        assert registration.reference is FrozenReference.LISAN_AL_ARAB


def test_the_wazn_witness_is_read_verbatim_and_is_again_the_derivative() -> None:
    assert require_attested_corroborating_excerpt(
        "MAQAYIS_NUR_ENTRY", "والمنارة: مفعلة من الاستنارة، والأصل منورة"
    )
    assert (
        "WAZN_WITNESS_IS_AGAIN_THE_DERIVATIVE_NOT_THE_CARD_WORD"
        in MAQAYIS_NUR_ENTRY.named_residuals
    )
    wazn = SENTENCE_CARD_PREREGISTRATION.registration_for(CardItem.WAZN)
    assert any(
        refusal.name == "WaznOfADerivativeIsNotTheWaznOfTheCardWord"
        for refusal in wazn.refusals
    )


def test_a_narrated_excerpt_that_is_not_in_the_text_is_refused() -> None:
    with pytest.raises(SourceTextError, match="لا يقع حرفُه"):
        require_attested_corroborating_excerpt(
            "MAQAYIS_NUR_ENTRY", "ونور مصدر جامد لا اشتقاق فيه"
        )


def test_the_locus_is_unverified_because_an_entry_number_is_not_pagination() -> None:
    assert MAQAYIS_NUR_ENTRY.locus_verification is LocusVerification.موضع_غير_متحقق
    assert MAQAYIS_NUR_ENTRY.digital_witness is None
    for residual in (
        "PRINT_EDITION_NOT_NAMED",
        "ENTRY_NUMBER_IS_NOT_PRINT_PAGINATION",
        "QUOTATION_CONTAINS_MARKED_ELISIONS",
    ):
        assert residual in MAQAYIS_NUR_ENTRY.named_residuals


def test_the_etymological_residual_is_named_in_the_text_and_in_its_item() -> None:
    assert (
        "ETYMOLOGICAL_DERIVATION_IS_NOT_MORPHOLOGICAL_JUMUD_MUSHTAQ_STATUS"
        in MAQAYIS_NUR_ENTRY.named_residuals
    )
    assert "MORPHOLOGICAL_JUMUD_MUSHTAQ_STATUS" in (
        ETYMOLOGICAL_DERIVATION_IS_NOT_MORPHOLOGICAL_STATUS_NOTE
    )
    jamid = SENTENCE_CARD_PREREGISTRATION.registration_for(CardItem.JAMID_MUSHTAQ)
    refusal = next(
        item
        for item in jamid.refusals
        if item.name == "EtymologicalDerivationIsNotMorphologicalStatus"
    )
    assert "MORPHOLOGICAL_JUMUD_MUSHTAQ_STATUS" in refusal.statement
    assert "مقاييس اللغة" in jamid.note


def test_a_corroborating_text_without_its_own_boundary_residual_is_refused() -> None:
    assert CORROBORATION_IS_NOT_A_DECLARED_REFERENCE_NOTE.strip()
    with pytest.raises(SourceTextError, match="مُعاضِدٌ ولا يحمل"):
        _replacement(named_residuals=("PRINT_EDITION_NOT_NAMED",))


def test_a_corroborating_text_that_names_no_item_is_refused() -> None:
    with pytest.raises(SourceTextError, match="لا يُعاضِد بندًا"):
        _replacement(corroborated_items=())


def test_a_duplicated_corroborated_item_is_refused() -> None:
    with pytest.raises(SourceTextError, match="بندٌ مكرَّرٌ"):
        _replacement(corroborated_items=(CardItem.WAZN, CardItem.WAZN))


def test_an_authority_not_occurring_in_the_text_is_refused() -> None:
    with pytest.raises(SourceTextError, match="غيرُ واقعةٍ في النصّ"):
        _replacement(internal_authorities=("سيبويه",))


def test_a_blank_source_name_is_refused() -> None:
    with pytest.raises(SourceTextError, match="اسمُ الكتاب"):
        _replacement(source_name="  ")
