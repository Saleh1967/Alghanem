"""نصوصُ بطاقة الجملة المُزوَّدة: نقلٌ يُفحَص بالاحتواء، وموضعٌ بجنسِ تحقُّقه.

الاختبارُ هنا يُثبِت ثلاثةَ أشياء لا رابعَ لها: أنّ المنقولَ يقع حرفُه في نصّه،
وأنّ كلَّ سلطةٍ مُعلَنةٍ واقعةٌ في اقتباسها نصًّا، وأنّ مرتبةَ تحقُّق الموضع
الوسطى مُسمّاةٌ ولا تُقرأ مقابلةً باليد.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import pytest

from alghanem.arabic.lexical_transmission import (
    LexicalCitationStructure,
    card_lexical_citation_structure,
    read_lexical_transmission,
)
from alghanem.arabic.sentence_card_preregistration import (
    NAMED_RESIDUALS,
    SENTENCE_CARD_PREREGISTRATION,
    CardItem,
    ItemStanding,
)
from alghanem.arabic.sentence_card_source_texts import (
    LISAN_DIGITAL_WITNESS,
    SUPPLIED_SOURCE_TEXTS,
    DigitalWitness,
    LocusVerification,
    SourceTextError,
    SuppliedSourceText,
    require_attested_excerpt,
    supplied_text_for,
)

CARD_PATH = (
    Path(__file__).resolve().parents[2]
    / "examples"
    / "sentence_card"
    / "nur_24_35.yaml"
)


def _read_card() -> dict[str, Any]:
    payload = json.loads(CARD_PATH.read_text(encoding="utf-8"))
    assert isinstance(payload, dict)
    return payload


def test_every_supplied_text_belongs_to_the_item_that_names_it() -> None:
    supplied_items = SENTENCE_CARD_PREREGISTRATION.items_with_standing(
        ItemStanding.SOURCE_TEXT_SUPPLIED_WITHOUT_CERTIFICATE
    )
    assert len(supplied_items) == len(SUPPLIED_SOURCE_TEXTS)
    for item in supplied_items:
        registration = SENTENCE_CARD_PREREGISTRATION.registration_for(item)
        supplied = supplied_text_for(registration.supplied_text_key)
        assert supplied.item is item
        assert supplied.reference is registration.reference


def test_an_unregistered_key_is_refused_not_resolved_to_the_nearest() -> None:
    with pytest.raises(SourceTextError):
        supplied_text_for("WAZN_LISAN")


def test_excerpt_is_checked_by_containment_not_by_assent() -> None:
    require_attested_excerpt("WAZN_LISAN_NUR", "منارة وهي مفعلة من النور")
    with pytest.raises(SourceTextError):
        require_attested_excerpt("WAZN_LISAN_NUR", "وزن «نور» فعل")


def test_declared_authority_absent_from_its_excerpt_is_refused() -> None:
    with pytest.raises(SourceTextError):
        SuppliedSourceText(
            key="K",
            item=CardItem.WAZN,
            reference=SUPPLIED_SOURCE_TEXTS["WAZN_LISAN_NUR"].reference,
            locus_statement="موضعٌ مُسمًّى",
            locus_verification=LocusVerification.موضع_غير_متحقق,
            verbatim_text="الجمع مناور، بالواو، لأنه من النور",
            internal_authorities=("الجوهري",),
            named_residuals=("R",),
        )


def test_a_supplied_text_without_a_named_residual_is_refused() -> None:
    with pytest.raises(SourceTextError):
        SuppliedSourceText(
            key="K",
            item=CardItem.WAZN,
            reference=SUPPLIED_SOURCE_TEXTS["WAZN_LISAN_NUR"].reference,
            locus_statement="موضعٌ مُسمًّى",
            locus_verification=LocusVerification.موضع_غير_متحقق,
            verbatim_text="نصٌّ منقول",
            internal_authorities=(),
            named_residuals=(),
        )


def test_locus_verification_is_three_ranked_and_the_top_has_no_entry() -> None:
    assert len(LocusVerification) == 3
    for supplied in SUPPLIED_SOURCE_TEXTS.values():
        assert supplied.locus_is_collated_by_hand is False


def test_lisan_loci_are_encoded_print_pagination_and_shakhsiyya_loci_are_not() -> None:
    assert (
        SUPPLIED_SOURCE_TEXTS["WAZN_LISAN_NUR"].locus_verification
        is LocusVerification.ترقيم_طبعة_مرمز_رقميا_غير_مقابل
    )
    assert (
        SUPPLIED_SOURCE_TEXTS["KHABAR_INSHA_SHAKHSIYYA_THREE"].locus_verification
        is LocusVerification.موضع_غير_متحقق
    )


def test_every_named_residual_of_a_supplied_text_is_stated_somewhere() -> None:
    stated = set(NAMED_RESIDUALS) | {"PRINT_EDITION_LOCUS_NOT_VERIFIED"}
    for supplied in SUPPLIED_SOURCE_TEXTS.values():
        assert set(supplied.named_residuals) <= stated


def test_the_digital_witness_names_its_repository_path_and_print_edition() -> None:
    assert isinstance(LISAN_DIGITAL_WITNESS, DigitalWitness)
    assert "OpenITI/RELEASE" in LISAN_DIGITAL_WITNESS.repository
    assert "0711IbnManzurIfriqi.LisanCarab" in LISAN_DIGITAL_WITNESS.path
    assert "دار صادر" in LISAN_DIGITAL_WITNESS.print_edition
    with pytest.raises(SourceTextError):
        DigitalWitness(
            corpus="",
            repository="r",
            path="p",
            print_edition="e",
            tagging_note="n",
        )


def test_card_lexical_path_is_a_named_internal_chain_not_a_flat_title() -> None:
    card = _read_card()
    assert (
        card_lexical_citation_structure(card)
        is LexicalCitationStructure.إسناد_داخلي_متعاقب_مسمى
    )
    descriptor = read_lexical_transmission(card)
    assert descriptor is not None
    assert [
        attribution.attributed_authority for attribution in descriptor.attributions
    ] == ["ابن الأثير", "أبو منصور", "ثعلب", "الجوهري"]


def test_the_card_quotes_the_material_on_its_own_verse() -> None:
    """صدفةٌ نصّيةٌ تُسجَّل ولا تُقرأ حجّة: المادةُ تستشهد بآية البطاقة نفسها."""

    descriptor = read_lexical_transmission(_read_card())
    assert descriptor is not None
    quoting = [
        attribution
        for attribution in descriptor.attributions
        if "الله نور السماوات والأرض" in attribution.verbatim_excerpt
    ]
    assert len(quoting) == 1
    assert quoting[0].attributed_authority == "أبو منصور"
