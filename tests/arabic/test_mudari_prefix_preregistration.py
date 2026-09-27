"""اختباراتُ ختمِ شرطِ حروف المضارعة — ولا بايتةَ مدوَّنةٍ تُقرأ ههنا."""

from __future__ import annotations

import re
from pathlib import Path

import pytest

from alghanem.arabic.mudari_prefix_preregistration import (
    MUDARI_PREFIX_NAMED_RESIDUALS,
    MUDARI_PREFIX_SPECIFICATION_DIGEST,
    STANDING,
    THE_ANCILLARY_LETTERS,
    THE_COUNTING_CONDITION,
    THE_DECLARED_CLAIMS,
    THE_DECLARED_DEFECT,
    THE_ENTAILED_EXPECTATION,
    THE_ENTAILED_EXPECTATION_FLOOR,
    THE_MINIMUM_SLOTS,
    THE_UNPREDICTED_QUESTION,
    THE_WIDE_HAMZA_CARRIERS,
    CarrierKey,
    ClaimGenus,
    DeclaredClaim,
    MudariPrefixSpecificationError,
    NounFilter,
    SpecificationStanding,
    specification_digest,
)

MODULE_PATH = (
    Path(__file__).resolve().parents[2]
    / "src"
    / "alghanem"
    / "arabic"
    / "mudari_prefix_preregistration.py"
)


def test_the_standing_is_prior_to_the_evidence() -> None:
    assert STANDING is SpecificationStanding.PRIOR_TO_THE_EVIDENCE


def test_the_frozen_digest_matches_what_the_content_yields() -> None:
    assert specification_digest() == MUDARI_PREFIX_SPECIFICATION_DIGEST


def test_changing_the_floor_changes_the_digest() -> None:
    import alghanem.arabic.mudari_prefix_preregistration as module

    before = specification_digest()
    original = module.THE_ENTAILED_EXPECTATION_FLOOR
    module.THE_ENTAILED_EXPECTATION_FLOOR = 0.80  # type: ignore[misc]
    try:
        assert specification_digest() != before
    finally:
        module.THE_ENTAILED_EXPECTATION_FLOOR = original  # type: ignore[misc]
    assert specification_digest() == before


def test_the_four_ancillary_letters_are_anyt_in_the_quoted_order() -> None:
    assert THE_ANCILLARY_LETTERS == ("\u0623", "\u0646", "\u064a", "\u062a")
    assert len(set(THE_ANCILLARY_LETTERS)) == 4


def test_the_narrow_carrier_is_a_strict_subset_of_the_wide_one() -> None:
    assert "\u0623" in THE_WIDE_HAMZA_CARRIERS
    assert set(THE_ANCILLARY_LETTERS) - set(THE_WIDE_HAMZA_CARRIERS) == {
        "\u0646",
        "\u064a",
        "\u062a",
    }
    assert len(THE_WIDE_HAMZA_CARRIERS) > 1


def test_both_carrier_keys_and_both_filters_are_declared() -> None:
    assert len(list(CarrierKey)) == 2
    assert len(list(NounFilter)) == 2


def test_the_three_source_genera_each_carry_at_least_one_claim() -> None:
    used = {claim.genus for claim in THE_DECLARED_CLAIMS}
    assert used == set(ClaimGenus)


def test_exactly_three_claims_are_textually_in_the_source() -> None:
    quoted = [
        claim
        for claim in THE_DECLARED_CLAIMS
        if claim.genus is ClaimGenus.TEXTUALLY_IN_THE_SOURCE
    ]
    assert len(quoted) == 3
    assert {claim.name for claim in quoted} == {
        "الزوائدُ الأربع",
        "تاءُ التأنيث الساكنة حرف",
        "الإسنادُ إلى غير من قام بالفعل مجاز",
    }


def test_the_two_inferences_are_named_as_the_speakers_own() -> None:
    inferred = [
        claim.name
        for claim in THE_DECLARED_CLAIMS
        if claim.genus is ClaimGenus.THE_SPEAKERS_OWN_INFERENCE
    ]
    assert len(inferred) == 2


def test_the_claim_names_are_distinct() -> None:
    names = [claim.name for claim in THE_DECLARED_CLAIMS]
    assert len(names) == len(set(names))


def test_some_declared_claims_are_beyond_the_surface() -> None:
    beyond = [claim for claim in THE_DECLARED_CLAIMS if not claim.surface_can_see_it]
    assert beyond, "فرزٌ لا يُخرج شيئًا عن سلطان السطح فرزٌ بلا أثر."
    assert any(
        claim.genus is ClaimGenus.TEXTUALLY_IN_THE_SOURCE for claim in beyond
    ), "ومن المنصوص ما لا يبلغه رسمٌ بلا وَسْم، فليُعلَن كذلك."


def test_an_empty_claim_is_refused() -> None:
    with pytest.raises(MudariPrefixSpecificationError):
        DeclaredClaim(
            name="   ",
            statement="نصّ",
            genus=ClaimGenus.FROM_THE_SCIENCE_OF_SARF,
            surface_can_see_it=True,
        )
    with pytest.raises(MudariPrefixSpecificationError):
        DeclaredClaim(
            name="اسم",
            statement="",
            genus=ClaimGenus.FROM_THE_SCIENCE_OF_SARF,
            surface_can_see_it=True,
        )


def test_a_claim_without_a_source_genus_is_refused() -> None:
    with pytest.raises(MudariPrefixSpecificationError):
        DeclaredClaim(
            name="اسم",
            statement="نصّ",
            genus="من_علم_الصرف",  # type: ignore[arg-type]
            surface_can_see_it=True,
        )


def test_the_expectation_floor_is_falsifiable() -> None:
    assert 0.5 < THE_ENTAILED_EXPECTATION_FLOOR < 1.0
    assert THE_ENTAILED_EXPECTATION_FLOOR == pytest.approx(0.90)


def test_the_minimum_slot_count_leaves_a_penultimate_slot() -> None:
    assert THE_MINIMUM_SLOTS >= 3


def test_the_condition_names_all_four_of_its_clauses() -> None:
    for clause in ("(١)", "(٢)", "(٣)", "(٤)"):
        assert clause in THE_COUNTING_CONDITION


def test_the_defect_names_the_three_quoted_nouns() -> None:
    for noun in ("أُمّ", "نُور", "تُراب"):
        assert noun in THE_DECLARED_DEFECT


def test_the_split_is_declared_unpredicted() -> None:
    assert "لا توقُّعَ" in THE_UNPREDICTED_QUESTION
    assert "تسعين" in THE_ENTAILED_EXPECTATION


def test_every_named_residual_carries_its_own_token() -> None:
    assert MUDARI_PREFIX_NAMED_RESIDUALS
    for token, text in MUDARI_PREFIX_NAMED_RESIDUALS.items():
        assert text.startswith(f"{token}:")


def test_the_module_reads_no_corpus_bytes_and_holds_no_measured_number() -> None:
    source = MODULE_PATH.read_text(encoding="utf-8")
    for forbidden in ("read_quran_corpus_bytes", "corpora/", "open("):
        assert (
            forbidden not in source
        ), "وحدةُ التجميد لا تقرأ مدوَّنةً؛ ولو قرأتها لَما صحّ أن تُسمّى سابقةً."
    for forbidden in ("from ..kernel", "from ..program"):
        assert forbidden not in source


def test_the_module_declares_no_percentage_of_its_own() -> None:
    source = MODULE_PATH.read_text(encoding="utf-8")
    body = source.split('"""', 2)[2]
    percentages = re.findall(r"\d+(?:\.\d+)?\s*٪", body)
    assert not percentages, (
        "رقمٌ بالمئة في وحدةٍ تُختَم قبل العدّ؛ وهو إمّا مقيسٌ فلا يجوز، أو "
        "متوقَّعٌ فموضعُه `THE_ENTAILED_EXPECTATION_FLOOR` وحدَه."
    )
