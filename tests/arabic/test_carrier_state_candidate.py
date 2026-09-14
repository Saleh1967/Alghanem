"""Tests for the measured-invertible carrier/state candidate encoding."""

from __future__ import annotations

import pkgutil
import unicodedata
from dataclasses import fields

import pytest

import alghanem.kernel as kernel_package
from alghanem.arabic.encoding.carrier_state_candidate import (
    ALEF_STATE_EXCLUSIVITY_IS_DECLARED_NOT_ENFORCED,
    CARRIER_SET_IS_DECLARED_NOT_DERIVED,
    CARRIER_STATE_NAMED_RESIDUALS,
    DECLARED_CARRIERS,
    EMBEDDED_ROUND_TRIP_CASES,
    ENCODING_LAYER_REGISTRY,
    MEASURED_INVERTIBILITY_SOURCES,
    NO_WEAKER_MODEL_WAS_LICENSED_OR_FROZEN,
    ROUND_TRIP_IS_INVERTIBILITY_NOT_ATOMICITY,
    SOURCE_PERCENTAGES_ARE_UNMEASURED_HERE,
    THREE_SOURCES_ARE_CORPUS_BOUNDED,
    UTHMANI_RESIDUE_MIXES_PHENOMENA_WITH_DROPPED_SYMBOLS,
    CarrierSeat,
    CarrierState,
    CarrierStateCodec,
    CarrierStateEncodingError,
    CarrierStateUnit,
    EncodingLayer,
    GeminationRole,
    InvertibilityMeasurement,
    derive_alef_states,
    round_trip_holds,
)

CODEC = CarrierStateCodec()

SHADDA = "\u0651"
FATHA = "\u064e"
DAMMA = "\u064f"
KASRA = "\u0650"
TANWIN_FATHA = "\u064b"
TANWIN_DAMMA = "\u064c"
DAGGER_ALIF = "\u0670"
SILENT_ZERO = "\u06df"
WAW_MADDA = "\u0653"


# --- the round trip, and what it does and does not show --------------------


@pytest.mark.parametrize("surface", EMBEDDED_ROUND_TRIP_CASES)
def test_every_embedded_case_comes_back_identical(surface: str) -> None:
    assert round_trip_holds(surface)


@pytest.mark.parametrize(
    "surface",
    [
        "\u0647\u064e\u0670\u0630\u064e\u0627",
        "\u0671\u0644\u0652\u062d\u064e\u0645\u0652\u062f\u064f",
        "\u0634\u064e\u064a\u0652\u0621\u064c",
        "\u0631\u064e\u0623\u0652\u0633\u064c",
        "hello",
        "\u0661\u0662\u0663",
        "",
        "\u0628\u0640\u0645",
    ],
)
def test_surfaces_outside_the_embedded_set_come_back_identical_too(
    surface: str,
) -> None:
    assert round_trip_holds(surface)


def test_a_non_carrier_codepoint_is_carried_and_never_dropped() -> None:
    units = CODEC.generate("\u0627\u0644\u0639\u0631\u0628\u064a\u0629!")
    assert units[-1] == CarrierStateUnit("!", CarrierState.PASSTHROUGH)
    assert CODEC.retrieve(units) == "\u0627\u0644\u0639\u0631\u0628\u064a\u0629!"


def test_a_latin_word_is_passthrough_rather_than_a_run_of_carriers() -> None:
    units = CODEC.generate("hi")
    assert {unit.state for unit in units} == {CarrierState.PASSTHROUGH}


# --- the genus that is closed: a second write into a derived slot ----------


@pytest.mark.parametrize(
    "surface",
    [
        "\u0628" + FATHA + DAMMA,
        "\u0628" + FATHA + KASRA,
        "\u0628" + TANWIN_FATHA + TANWIN_DAMMA,
        "\u0628" + FATHA + TANWIN_DAMMA,
        "\u0628" + TANWIN_FATHA + FATHA,
    ],
)
def test_a_second_vowel_mark_is_refused_rather_than_silently_kept(
    surface: str,
) -> None:
    with pytest.raises(CarrierStateEncodingError, match="second vowel mark"):
        CODEC.generate(surface)


def test_a_second_shadda_is_refused_by_the_same_rule() -> None:
    with pytest.raises(CarrierStateEncodingError, match="second shadda"):
        CODEC.generate("\u0628" + SHADDA + SHADDA)


def test_one_mark_of_each_kind_is_not_a_second_write() -> None:
    assert round_trip_holds("\u0628" + FATHA + SHADDA)
    assert round_trip_holds("\u0628" + SHADDA + FATHA)
    assert round_trip_holds("\u0646" + SHADDA + TANWIN_FATHA)


# --- the madd seat: every field written is a field read --------------------


@pytest.mark.parametrize(
    "surface",
    [
        "\u0622",
        "\u0622" + FATHA,
        "\u0622" + DAMMA,
        "\u0622" + TANWIN_FATHA,
        "\u0622" + SILENT_ZERO,
        "\u0622" + SHADDA + FATHA,
        "\u0628\u0622" + KASRA,
    ],
)
def test_the_madd_carries_its_state_instead_of_swallowing_it(surface: str) -> None:
    assert round_trip_holds(surface)


def test_the_madd_is_a_seat_and_not_a_state_of_its_own() -> None:
    (unit,) = CODEC.generate("\u0622" + FATHA)
    assert unit.carrier == "\u0621"
    assert unit.seat is CarrierSeat.MADD
    assert unit.state is CarrierState.FATHA
    assert unit.written_form == "\u0622"
    assert not any(state.value == "madd_self" for state in CarrierState)


@pytest.mark.parametrize("state", [CarrierState.DAGGER, CarrierState.PASSTHROUGH])
def test_a_structural_state_refuses_every_field_it_would_never_read(
    state: CarrierState,
) -> None:
    assert state.is_structural_only
    carrier = "\u0627" if state is CarrierState.DAGGER else "!"
    assert CarrierStateUnit(carrier, state).state is state
    for extra in (
        {"tanwin": True},
        {"silent": True},
        {"waw_madda": True},
        {"seat": CarrierSeat.MADD},
        {"gemination": GeminationRole.PAIR_START},
        {"tanwin_alif_seat": True},
    ):
        with pytest.raises(CarrierStateEncodingError, match="would never be read"):
            CarrierStateUnit(carrier, state, **extra)  # type: ignore[arg-type]


def test_no_state_is_special_cased_out_of_the_retrieval_path() -> None:
    read_back = {
        CarrierState.PASSTHROUGH,
        CarrierState.DAGGER,
    }
    for state in CarrierState:
        if state in read_back:
            continue
        unit = CarrierStateUnit("\u0628", state)
        assert CODEC.retrieve([unit]).startswith("\u0628")


# --- the unit refuses structure it cannot hold ------------------------------


def test_a_seat_is_refused_on_a_carrier_that_does_not_host_it() -> None:
    with pytest.raises(CarrierStateEncodingError, match="is written on"):
        CarrierStateUnit("\u0628", CarrierState.FATHA, seat=CarrierSeat.MADD)


def test_an_alef_seat_is_refused_without_a_fatha_tanwin() -> None:
    with pytest.raises(CarrierStateEncodingError, match="alef seat is consumed"):
        CarrierStateUnit("\u0646", CarrierState.FATHA, tanwin_alif_seat=True)
    with pytest.raises(CarrierStateEncodingError, match="alef seat is consumed"):
        CarrierStateUnit(
            "\u0646", CarrierState.DAMMA, tanwin=True, tanwin_alif_seat=True
        )


def test_an_explicit_madda_is_refused_off_the_waw() -> None:
    with pytest.raises(CarrierStateEncodingError, match="read on the waw only"):
        CarrierStateUnit("\u0628", CarrierState.FATHA, waw_madda=True)


def test_a_pair_start_refuses_the_state_and_marks_of_its_own_second_half() -> None:
    with pytest.raises(CarrierStateEncodingError, match="holds sukun_implicit"):
        CarrierStateUnit("\u0628", CarrierState.FATHA, GeminationRole.PAIR_START)
    with pytest.raises(CarrierStateEncodingError, match="carries no tanwin or mark"):
        CarrierStateUnit(
            "\u0628",
            CarrierState.SUKUN_IMPLICIT,
            GeminationRole.PAIR_START,
            silent=True,
        )


def test_a_pair_start_without_its_own_second_half_is_refused_at_retrieval() -> None:
    start = CarrierStateUnit(
        "\u0628", CarrierState.SUKUN_IMPLICIT, GeminationRole.PAIR_START
    )
    with pytest.raises(CarrierStateEncodingError, match="not followed by its own"):
        CODEC.retrieve([start])
    with pytest.raises(CarrierStateEncodingError, match="not followed by its own"):
        CODEC.retrieve([start, CarrierStateUnit("\u062a", CarrierState.FATHA)])


def test_a_carrier_outside_the_declared_set_is_refused_off_the_passthrough() -> None:
    with pytest.raises(CarrierStateEncodingError, match="outside DECLARED_CARRIERS"):
        CarrierStateUnit("!", CarrierState.FATHA)
    with pytest.raises(CarrierStateEncodingError, match="exactly one codepoint"):
        CarrierStateUnit("\u0628\u062a", CarrierState.FATHA)
    with pytest.raises(CarrierStateEncodingError, match="a CarrierState member"):
        CarrierStateUnit("\u0628", "fatha")  # type: ignore[arg-type]
    with pytest.raises(CarrierStateEncodingError, match="a CarrierStateUnit"):
        CODEC.retrieve(["\u0628"])  # type: ignore[list-item]


# --- layer 1 is decided by derivation, not by wording ----------------------


def test_the_alef_exclusivity_claim_is_refuted_by_this_module_s_own_trace() -> None:
    held = derive_alef_states()
    assert CarrierState.SUKUN_IMPLICIT in held
    assert CarrierState.FATHA in held
    assert len(held) > 1
    assert derive_alef_states(["\u0642\u064e\u0627\u0644\u064e"]) == frozenset(
        {CarrierState.SUKUN_IMPLICIT}
    )


def test_the_refuted_claim_is_named_rather_than_quietly_reworded() -> None:
    layer_one = ENCODING_LAYER_REGISTRY[0]
    assert layer_one.order == 1
    assert "ALEF_STATE_EXCLUSIVITY_IS_DECLARED_NOT_ENFORCED" in layer_one.description
    assert "not enforced" in ALEF_STATE_EXCLUSIVITY_IS_DECLARED_NOT_ENFORCED


def test_the_layer_registry_is_ordered_and_names_every_claim() -> None:
    assert [layer.order for layer in ENCODING_LAYER_REGISTRY] == list(
        range(1, len(ENCODING_LAYER_REGISTRY) + 1)
    )
    with pytest.raises(CarrierStateEncodingError, match="positive integer"):
        EncodingLayer(0, "x", "y")
    with pytest.raises(CarrierStateEncodingError, match="names itself"):
        EncodingLayer(1, "x", "")


# --- the carrier set is declared, and says so ------------------------------


def test_the_carrier_set_is_declared_and_holds_no_foreign_letter() -> None:
    assert "h" not in DECLARED_CARRIERS
    assert "\u0628" in DECLARED_CARRIERS
    assert "\u0622" in DECLARED_CARRIERS
    assert "\u0671" in DECLARED_CARRIERS
    assert DAGGER_ALIF not in DECLARED_CARRIERS
    assert "not derived from any property" in CARRIER_SET_IS_DECLARED_NOT_DERIVED


# --- measurement over an external source -----------------------------------


def test_no_external_percentage_is_recorded_without_a_digest() -> None:
    assert MEASURED_INVERTIBILITY_SOURCES == ()
    assert "MEASURED_INVERTIBILITY_SOURCES is empty" in (
        SOURCE_PERCENTAGES_ARE_UNMEASURED_HERE
    )


def test_a_measurement_derives_its_counts_by_running_the_codec() -> None:
    measurement = InvertibilityMeasurement.measure(
        ["\u0628\u0650\u0633\u0652\u0645\u0650", "hello"],
        source_id="probe",
        source_sha256="a" * 64,
        source_byte_length=12,
    )
    assert measurement.token_total == 2
    assert measurement.token_mismatches == 0
    assert measurement.matched_tokens == 2
    assert measurement.matched_fraction == 1.0
    assert measurement.normalization_form == "NFC"
    assert measurement.unicode_database_version == unicodedata.unidata_version


def test_a_measurement_without_a_full_digest_or_a_length_is_refused() -> None:
    base = {
        "source_id": "probe",
        "source_sha256": "a" * 64,
        "source_byte_length": 12,
        "normalization_form": "NFC",
        "unicode_database_version": unicodedata.unidata_version,
        "token_total": 4,
        "token_mismatches": 1,
    }
    assert InvertibilityMeasurement(**base).matched_tokens == 3
    with pytest.raises(CarrierStateEncodingError, match="64 characters"):
        InvertibilityMeasurement(**{**base, "source_sha256": "a" * 40})
    with pytest.raises(CarrierStateEncodingError, match="positive integer"):
        InvertibilityMeasurement(**{**base, "source_byte_length": 0})
    with pytest.raises(CarrierStateEncodingError, match="non-empty string"):
        InvertibilityMeasurement(**{**base, "normalization_form": ""})
    with pytest.raises(CarrierStateEncodingError, match="not a measurement"):
        InvertibilityMeasurement(**{**base, "token_total": 0})
    with pytest.raises(CarrierStateEncodingError, match="contradictory claims"):
        InvertibilityMeasurement(**{**base, "token_mismatches": 5})


def test_a_measurement_carries_no_percentage_field_to_write_into() -> None:
    declared = {item.name for item in fields(InvertibilityMeasurement)}
    for forbidden in ("percent", "rate", "fraction", "score", "verdict", "standing"):
        assert not any(forbidden in name for name in declared), forbidden


# --- the named residuals ---------------------------------------------------


def test_the_residuals_left_by_this_encoding_are_named_not_hidden() -> None:
    assert set(CARRIER_STATE_NAMED_RESIDUALS) == {
        "ROUND_TRIP_IS_INVERTIBILITY_NOT_ATOMICITY",
        "NO_WEAKER_MODEL_WAS_LICENSED_OR_FROZEN",
        "THREE_SOURCES_ARE_CORPUS_BOUNDED",
        "CARRIER_SET_IS_DECLARED_NOT_DERIVED",
        "SOURCE_PERCENTAGES_ARE_UNMEASURED_HERE",
        "UTHMANI_RESIDUE_MIXES_PHENOMENA_WITH_DROPPED_SYMBOLS",
        "ALEF_STATE_EXCLUSIVITY_IS_DECLARED_NOT_ENFORCED",
    }
    assert all(text.strip() for text in CARRIER_STATE_NAMED_RESIDUALS.values())


def test_the_atomicity_claim_is_refused_rather_than_carried() -> None:
    assert "no evidence" in ROUND_TRIP_IS_INVERTIBILITY_NOT_ATOMICITY
    assert "atomic" in ROUND_TRIP_IS_INVERTIBILITY_NOT_ATOMICITY
    assert "no weaker model was licensed or frozen" in (
        NO_WEAKER_MODEL_WAS_LICENSED_OR_FROZEN
    )
    assert "presumptive beyond it" in THREE_SOURCES_ARE_CORPUS_BOUNDED
    assert "93.38%" in UTHMANI_RESIDUE_MIXES_PHENOMENA_WITH_DROPPED_SYMBOLS
    assert "95.76%" in UTHMANI_RESIDUE_MIXES_PHENOMENA_WITH_DROPPED_SYMBOLS


def test_nothing_here_is_named_an_atom_or_a_protocol() -> None:
    import alghanem.arabic.encoding.carrier_state_candidate as module

    text = open(module.__file__, encoding="utf-8").read()
    exported = set(module.__all__)
    assert not any("Atom" in name or "Protocol" in name for name in exported)
    assert "class Atom" not in text
    assert "CarrierStateEngine" not in text


# --- authority: this module is inert ---------------------------------------


def test_no_kernel_module_reads_the_carrier_state_candidate() -> None:
    for module in pkgutil.walk_packages(
        kernel_package.__path__, prefix="alghanem.kernel."
    ):
        source = module.module_finder.find_spec(  # type: ignore[union-attr]
            module.name
        )
        assert source is not None and source.origin is not None
        with open(source.origin, encoding="utf-8") as handle:
            text = handle.read()
        assert "carrier_state_candidate" not in text, module.name
        assert "CarrierStateUnit" not in text, module.name


def test_no_type_here_carries_a_verdict_birth_freeze_or_rank_field() -> None:
    for declaring in (
        CarrierStateUnit,
        EncodingLayer,
        InvertibilityMeasurement,
    ):
        declared = {item.name for item in fields(declaring)}
        for forbidden in ("verdict", "birth", "freeze", "rank", "reached", "aim"):
            assert not any(forbidden in name for name in declared), (
                declaring,
                forbidden,
            )


# --- a bounded injectivity probe, stated with its bound --------------------


def test_distinct_surfaces_do_not_share_one_unit_sequence_within_this_probe() -> None:
    carriers = ["\u0628", "\u0627", "\u0648", "\u064a", "\u0621", "\u0622", "!"]
    marks = [
        "",
        FATHA,
        DAMMA,
        TANWIN_FATHA,
        SHADDA,
        DAGGER_ALIF,
        SILENT_ZERO,
        WAW_MADDA,
    ]
    seen: dict[tuple[CarrierStateUnit, ...], str] = {}
    probed = 0
    for first in carriers:
        for first_mark in marks:
            for second in carriers:
                for second_mark in marks:
                    surface = first + first_mark + second + second_mark
                    try:
                        units = CODEC.generate(surface)
                    except CarrierStateEncodingError:
                        continue
                    probed += 1
                    normalized = unicodedata.normalize("NFC", surface)
                    assert (
                        unicodedata.normalize("NFC", CODEC.retrieve(units))
                        == normalized
                    )
                    assert seen.setdefault(units, normalized) == normalized
    assert probed > 2000
