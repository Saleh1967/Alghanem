"""شهودٌ على الجبر التشغيليّ للحرف والحركة."""

from __future__ import annotations

import inspect
from pathlib import Path

import pytest

from alghanem.arabic import letter_haraka_operational_algebra as algebra
from alghanem.arabic.encoding.carrier_state_candidate import (
    CarrierState,
    CarrierStateCodec,
    CarrierStateUnit,
    GeminationRole,
)
from alghanem.arabic.letter_haraka_operational_algebra import (
    ALGEBRA_NAMED_RESIDUALS,
    BANNED_PROXY_FIELDS,
    ConsonantPosition,
    JoinInputStatus,
    LicensedInputBundle,
    LicensedJoinInput,
    OperationalAlgebraError,
    VowelIdentity,
    VowelPosition,
    build_licensed_inputs,
    decompose_word,
    quantity_of,
)
from alghanem.import_boundary import ImportBoundaryPolicy, audit_import_boundary


@pytest.fixture(scope="module")
def bundle() -> LicensedInputBundle:
    return build_licensed_inputs()


# --- الحدودُ البنيويّة ------------------------------------------------------------


def test_the_algebra_reaches_no_kernel_module() -> None:
    report = audit_import_boundary(
        (Path(str(algebra.__file__)),),
        ImportBoundaryPolicy(
            policy_id="letter-haraka-operational-algebra",
            permitted_modules=(),
            forbidden_packages=("alghanem.kernel",),
        ),
    )
    assert not [
        name for name in report.reached_modules if name.startswith("alghanem.kernel")
    ]


def test_the_algebra_does_not_reach_the_excluded_syllabifier() -> None:
    report = audit_import_boundary(
        (Path(str(algebra.__file__)),),
        ImportBoundaryPolicy(
            policy_id="letter-haraka-operational-algebra-syllabifier",
            permitted_modules=(),
            forbidden_packages=("alghanem.kernel",),
        ),
    )
    assert "alghanem.arabic.syllabifier" not in report.reached_modules
    assert "alghanem.arabic.p_extractor" not in report.reached_modules


def test_the_module_source_names_no_banned_identity_proxy_as_a_reader() -> None:
    source = Path(str(algebra.__file__)).read_text(encoding="utf-8")
    body = source.split("BANNED_PROXY_FIELDS", 1)[1].split('"""', 2)[-1]
    for proxy in BANNED_PROXY_FIELDS:
        assert f".{proxy}" not in body


def test_the_banned_proxy_list_is_the_frozen_one() -> None:
    assert BANNED_PROXY_FIELDS == (
        "carrier_codepoint",
        "letter_index",
        "slot_position",
        "surface_offset",
    )


def test_no_join_is_applied_and_no_syllable_element_is_produced() -> None:
    exported = set(algebra.__all__)
    assert not {name for name in exported if "syllable" in name.lower()}
    assert not {name for name in exported if name.lower().startswith("join_")}


def test_there_are_exactly_five_named_residuals_and_none_is_blank() -> None:
    assert len(ALGEBRA_NAMED_RESIDUALS) == 5
    assert len(set(ALGEBRA_NAMED_RESIDUALS)) == 5
    assert all(note.strip() for note in ALGEBRA_NAMED_RESIDUALS)


def test_the_residuals_name_the_construction_debt_and_the_birth_ceiling() -> None:
    joined = "\n".join(ALGEBRA_NAMED_RESIDUALS)
    assert "بالبناء" in joined
    assert "لا ولادةَ" in joined
    assert "CONDITIONAL_STRUCTURAL_BIRTH" in joined


# --- الجوداتُ الثلاث --------------------------------------------------------------


def test_the_vowel_identity_is_closed_at_three_qualities() -> None:
    assert {member.value for member in VowelIdentity} == {"fatha", "damma", "kasra"}


def test_the_status_kinds_are_three_and_distinct() -> None:
    assert len({member.value for member in JoinInputStatus}) == 3


# --- `π_Q` ----------------------------------------------------------------------


def _unit(carrier: str, state: CarrierState, **kwargs: object) -> CarrierStateUnit:
    return CarrierStateUnit(
        carrier=carrier,
        state=state,
        **kwargs,  # type: ignore[arg-type]
    )


def test_quantity_is_one_when_no_position_follows() -> None:
    assert quantity_of(_unit("م", CarrierState.FATHA), None) == (1, None)


def test_quantity_is_two_for_a_matching_silent_extension_position() -> None:
    following = _unit("ا", CarrierState.SUKUN_IMPLICIT)
    assert quantity_of(_unit("م", CarrierState.FATHA), following) == (2, None)


def test_quantity_is_one_when_the_following_position_does_not_match_the_quality() -> (
    None
):
    following = _unit("و", CarrierState.SUKUN_IMPLICIT)
    quantity, reason = quantity_of(_unit("م", CarrierState.FATHA), following)
    assert quantity == 1
    assert reason is None


def test_a_geminated_extension_carrier_is_not_an_extension_position() -> None:
    following = _unit(
        "و", CarrierState.SUKUN_IMPLICIT, gemination=GeminationRole.PAIR_START
    )
    assert quantity_of(_unit("م", CarrierState.DAMMA), following)[0] == 1


def test_a_following_dagger_makes_the_quantity_undefined_not_one() -> None:
    following = _unit("ا", CarrierState.DAGGER)
    quantity, reason = quantity_of(_unit("م", CarrierState.FATHA), following)
    assert quantity is None
    assert reason is not None
    assert "المدّ" in reason


def test_quantity_refuses_a_non_vowel_unit() -> None:
    with pytest.raises(OperationalAlgebraError):
        quantity_of(_unit("م", CarrierState.SUKUN_EXPLICIT), None)


def test_quantity_reads_no_offset_or_index_argument() -> None:
    parameters = tuple(inspect.signature(quantity_of).parameters)
    assert parameters == ("unit", "following")


# --- العناصرُ المصنَّفة -------------------------------------------------------------


def test_a_consonant_position_refuses_a_blank_admission_reason() -> None:
    with pytest.raises(OperationalAlgebraError):
        ConsonantPosition(
            carrier="م",
            word_index=0,
            unit_index=0,
            is_gemination_pair_start=False,
            admitted_because="   ",
        )


def test_a_consonant_position_refuses_a_negative_position() -> None:
    with pytest.raises(OperationalAlgebraError):
        ConsonantPosition(
            carrier="م",
            word_index=-1,
            unit_index=0,
            is_gemination_pair_start=False,
            admitted_because="علّة",
        )


def test_a_consonant_position_refuses_a_multi_character_carrier() -> None:
    with pytest.raises(OperationalAlgebraError):
        ConsonantPosition(
            carrier="مم",
            word_index=0,
            unit_index=0,
            is_gemination_pair_start=False,
            admitted_because="علّة",
        )


def test_a_vowel_position_refuses_a_quantity_outside_one_and_two() -> None:
    with pytest.raises(OperationalAlgebraError):
        VowelPosition(
            carrier="م",
            word_index=0,
            unit_index=0,
            identity=VowelIdentity.FATHA,
            quantity=3,
            quantity_undefined_because=None,
        )


def test_a_vowel_position_refuses_an_undefined_quantity_with_no_reason() -> None:
    with pytest.raises(OperationalAlgebraError):
        VowelPosition(
            carrier="م",
            word_index=0,
            unit_index=0,
            identity=VowelIdentity.FATHA,
            quantity=None,
            quantity_undefined_because=None,
        )


def test_a_vowel_position_refuses_a_quantity_carrying_a_reason_for_its_absence() -> (
    None
):
    with pytest.raises(OperationalAlgebraError):
        VowelPosition(
            carrier="م",
            word_index=0,
            unit_index=0,
            identity=VowelIdentity.FATHA,
            quantity=1,
            quantity_undefined_because="علّة",
        )


# --- المداخلُ المرخَّصة ------------------------------------------------------------


def test_an_admissible_input_refuses_a_missing_side() -> None:
    with pytest.raises(OperationalAlgebraError):
        LicensedJoinInput(
            word_index=0,
            unit_index=0,
            status=JoinInputStatus.ADMISSIBLE,
            consonant=None,
            vowel=None,
            reason="علّة",
            conditions_true_by_construction=("شرط",),
        )


def test_an_admissible_input_refuses_an_underivable_quantity() -> None:
    consonant = ConsonantPosition(
        carrier="م",
        word_index=0,
        unit_index=0,
        is_gemination_pair_start=False,
        admitted_because="علّة",
    )
    vowel = VowelPosition(
        carrier="م",
        word_index=0,
        unit_index=0,
        identity=VowelIdentity.FATHA,
        quantity=None,
        quantity_undefined_because="محورُ المدّ مؤجَّل",
    )
    with pytest.raises(OperationalAlgebraError):
        LicensedJoinInput(
            word_index=0,
            unit_index=0,
            status=JoinInputStatus.ADMISSIBLE,
            consonant=consonant,
            vowel=vowel,
            reason="علّة",
            conditions_true_by_construction=("شرط",),
        )


def test_an_admissible_input_refuses_to_leave_its_construction_debt_unnamed() -> None:
    consonant = ConsonantPosition(
        carrier="م",
        word_index=0,
        unit_index=0,
        is_gemination_pair_start=False,
        admitted_because="علّة",
    )
    vowel = VowelPosition(
        carrier="م",
        word_index=0,
        unit_index=0,
        identity=VowelIdentity.FATHA,
        quantity=1,
        quantity_undefined_because=None,
    )
    with pytest.raises(OperationalAlgebraError):
        LicensedJoinInput(
            word_index=0,
            unit_index=0,
            status=JoinInputStatus.ADMISSIBLE,
            consonant=consonant,
            vowel=vowel,
            reason="علّة",
            conditions_true_by_construction=(),
        )


def test_every_input_carries_a_non_blank_reason() -> None:
    with pytest.raises(OperationalAlgebraError):
        LicensedJoinInput(
            word_index=0,
            unit_index=0,
            status=JoinInputStatus.UNDEFINED,
            consonant=None,
            vowel=None,
            reason="  ",
            conditions_true_by_construction=(),
        )


# --- القسمُ على كلمة --------------------------------------------------------------


def test_decomposition_splits_one_unit_into_two_co_located_positions() -> None:
    inputs = decompose_word("بَ", 0)
    admissible = [i for i in inputs if i.status is JoinInputStatus.ADMISSIBLE]
    assert len(admissible) == 1
    item = admissible[0]
    assert item.consonant is not None and item.vowel is not None
    assert item.consonant.unit_index == item.vowel.unit_index
    assert item.consonant.carrier == item.vowel.carrier


def test_a_vowel_less_consonant_is_undefined_and_keeps_its_element() -> None:
    inputs = decompose_word("بَحْ", 0)
    closing = inputs[-1]
    assert closing.status is JoinInputStatus.UNDEFINED
    assert closing.consonant is not None
    assert closing.vowel is None
    assert "صفريّ" in closing.reason


def test_an_undefined_input_names_no_condition_as_true_by_construction() -> None:
    inputs = decompose_word("بَحْ", 0)
    for item in inputs:
        if item.status is not JoinInputStatus.ADMISSIBLE:
            assert item.conditions_true_by_construction == ()


def test_every_admissible_input_names_the_adjacency_debt() -> None:
    inputs = decompose_word("بَ", 0)
    for item in inputs:
        if item.status is JoinInputStatus.ADMISSIBLE:
            assert any(
                "بالبناء" in condition
                for condition in item.conditions_true_by_construction
            )


def test_the_dagger_word_yields_an_undefined_quantity_at_its_fatha() -> None:
    inputs = decompose_word("الرَّحْمَٰنِ", 0)
    undefined_quantity = [
        item
        for item in inputs
        if item.vowel is not None and item.vowel.quantity is None
    ]
    assert len(undefined_quantity) == 1
    assert undefined_quantity[0].vowel is not None
    assert undefined_quantity[0].vowel.carrier == "م"


def test_the_dagger_unit_itself_is_not_an_element_of_either_space() -> None:
    inputs = decompose_word("الرَّحْمَٰنِ", 0)
    outside = [i for i in inputs if i.status is JoinInputStatus.NOT_AN_ELEMENT]
    assert len(outside) == 1
    assert outside[0].consonant is None and outside[0].vowel is None


def test_decomposition_covers_every_unit_exactly_once() -> None:
    codec = CarrierStateCodec()
    for word in ("الرَّحْمَٰنِ", "بِسْمِ", "نَسْتَعِينُ"):
        inputs = decompose_word(word, 0, codec=codec)
        assert len(inputs) == len(codec.generate(word))
        assert [item.unit_index for item in inputs] == list(range(len(inputs)))


# --- الحزمةُ المُبصَّمة -------------------------------------------------------------


def test_the_bundle_partitions_every_unit_into_exactly_one_status(
    bundle: LicensedInputBundle,
) -> None:
    counted = sum(
        len([i for i in bundle.inputs if i.status is status])
        for status in JoinInputStatus
    )
    assert counted == len(bundle.inputs)


def test_the_bundle_measures_the_deposit(bundle: LicensedInputBundle) -> None:
    assert len(bundle.inputs) == 159
    assert len(bundle.admissible) == 80
    assert len(bundle.undefined) == 77
    assert len(bundle.quantity_undefined) == 2
    assert len(bundle.gemination_pair_starts) == 14


def test_the_quantity_census_is_derived_not_written(
    bundle: LicensedInputBundle,
) -> None:
    assert bundle.quantity_census == ((1, 62), (2, 18))
    assert sum(count for _, count in bundle.quantity_census) == len(bundle.admissible)


def test_no_gemination_pair_start_is_ever_admissible(
    bundle: LicensedInputBundle,
) -> None:
    for item in bundle.gemination_pair_starts:
        assert item.status is JoinInputStatus.UNDEFINED


def test_the_bundle_refuses_a_forged_digest(bundle: LicensedInputBundle) -> None:
    with pytest.raises(OperationalAlgebraError):
        LicensedInputBundle(
            source_id=bundle.source_id,
            inputs=bundle.inputs,
            content_digest="0" * 64,
        )


def test_the_bundle_refuses_a_digest_borrowed_from_another_source(
    bundle: LicensedInputBundle,
) -> None:
    with pytest.raises(OperationalAlgebraError):
        LicensedInputBundle(
            source_id="another-source",
            inputs=bundle.inputs,
            content_digest=bundle.content_digest,
        )


def test_the_bundle_refuses_to_license_nothing() -> None:
    with pytest.raises(OperationalAlgebraError):
        LicensedInputBundle(source_id="x", inputs=(), content_digest="0" * 64)


def test_the_algebra_refuses_an_empty_text() -> None:
    with pytest.raises(OperationalAlgebraError):
        build_licensed_inputs(())


def test_the_digest_is_stable_across_runs(bundle: LicensedInputBundle) -> None:
    assert build_licensed_inputs().content_digest == bundle.content_digest


def test_the_digest_changes_when_the_measured_content_changes(
    bundle: LicensedInputBundle,
) -> None:
    other = build_licensed_inputs(("بِسْمِ",), source_id=bundle.source_id)
    assert other.content_digest != bundle.content_digest


def test_word_indices_run_across_lines_without_resetting(
    bundle: LicensedInputBundle,
) -> None:
    assert max(item.word_index for item in bundle.inputs) == 28


def test_no_admissible_input_carries_an_undefined_quantity(
    bundle: LicensedInputBundle,
) -> None:
    for item in bundle.admissible:
        assert item.vowel is not None
        assert item.vowel.quantity in (1, 2)
