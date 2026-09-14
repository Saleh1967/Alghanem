"""Tests for the two-sukun adjacency scan over carrier/state units."""

from __future__ import annotations

import hashlib

import pytest

from alghanem.arabic.encoding.carrier_state_candidate import (
    CarrierState,
    CarrierStateCodec,
    CarrierStateUnit,
    GeminationRole,
)
from alghanem.arabic.encoding.sakin_adjacency import (
    ARTICLE_DERIVATION_CASES,
    DECLARED_ARTIFACT_CODEPOINTS,
    DECLARED_EXTENSION_CARRIERS,
    DECLARED_RARE_READING_MARKS,
    EMBEDDED_ADJACENCY_CASES,
    HA_DERIVATION_CASES,
    MEASURED_SAKIN_CLASH_SOURCES,
    MUQATTAAT_OPENINGS,
    SAKIN_ADJACENCY_NAMED_RESIDUALS,
    AdjacentSakinPair,
    SakinAdjacencyError,
    SakinClashExclusion,
    SakinClashScan,
    derive_article_gemination_offsets,
    derive_ha_and_ta_marbuta_units,
    holds_sukun,
    is_extension_unit,
    scan_surface,
    scan_units,
)

_CODEC = CarrierStateCodec()

_SUN_WORD = "\u0671\u0644\u0634\u0651\u064e\u0645\u0652\u0633\u0650"  # ٱلشَّمْسِ
_LAM_WORD = "\u0671\u0644\u0651\u064e\u0630\u0650\u064a\u0646\u064e"  # ٱلَّذِينَ
_MOON_WORD = "\u0671\u0644\u0652\u0642\u064e\u0645\u064e\u0631\u0650"  # ٱلْقَمَرِ


# --- the derivation that decides where the article's mark sits -------------


def test_the_article_mark_sits_on_the_sun_letter_not_on_the_lam() -> None:
    offsets = derive_article_gemination_offsets()
    assert offsets[_SUN_WORD] == (2,)
    assert offsets[_LAM_WORD] == (1,)
    assert offsets[_MOON_WORD] == ()


def test_the_pair_before_a_sun_letter_carries_no_gemination_on_either_member() -> None:
    units = _CODEC.generate(_SUN_WORD)
    assert units[0].gemination is None
    assert units[1].gemination is None
    assert units[2].gemination is GeminationRole.PAIR_START
    report = scan_surface(_SUN_WORD)
    first, second = report.pairs
    assert first.exclusion is SakinClashExclusion.EXTENSION_CARRIER_FIRST
    assert second.exclusion is SakinClashExclusion.ASSIMILATION_PAIR


def test_a_gemination_check_of_one_member_alone_would_miss_a_case() -> None:
    sun = _CODEC.generate(_SUN_WORD)
    lam = _CODEC.generate(_LAM_WORD)
    assert sun[1].gemination is None and sun[2].gemination is GeminationRole.PAIR_START
    assert lam[1].gemination is GeminationRole.PAIR_START
    assert scan_surface(_LAM_WORD).pairs[0].exclusion is (
        SakinClashExclusion.ASSIMILATION_PAIR
    )


# --- the haa and the tied taa ----------------------------------------------


def test_the_connecting_vowel_after_a_haa_is_a_passthrough_unit() -> None:
    rows = derive_ha_and_ta_marbuta_units()
    small = [row for row in rows if row[1] in {"\u06e5", "\u06e6"}]
    assert small
    assert all(row[4] for row in small)
    assert all(row[2] == "passthrough" for row in small)


def test_the_tied_taa_reports_taa_and_never_haa() -> None:
    rows = derive_ha_and_ta_marbuta_units()
    seated = [row for row in rows if row[3] == "ta_marbuta"]
    assert seated
    assert all(row[1] == "\u062a" for row in seated)
    assert not any(row[1] == "\u0647" and row[3] == "ta_marbuta" for row in rows)


def test_a_passthrough_unit_is_read_through_rather_than_breaking_adjacency() -> None:
    report = scan_surface("\u0645\u064f\u062d\u0652 \u0635\u0652")  # مُحْ صْ
    assert len(report.pairs) == 1
    pair = report.pairs[0]
    assert pair.skipped_passthrough == 1
    assert pair.is_counted


def test_the_haa_cases_hold_no_adjacency_pair() -> None:
    for surface in HA_DERIVATION_CASES:
        assert scan_surface(surface).pairs == () or scan_surface(surface).counted == ()


# --- the sukun-bearing nun and the stop marks ------------------------------


def test_a_sukun_bearing_nun_before_a_vowelled_consonant_poses_no_pair() -> None:
    assert scan_surface("\u0645\u0650\u0646\u0652\u0647\u064f\u0645\u0652").pairs == ()
    assert scan_surface("\u0645\u064e\u0646\u0652 \u064a\u064e\u0642\u064f").pairs == ()


def test_a_stop_mark_is_only_a_passthrough_unit() -> None:
    units = _CODEC.generate("\u0645\u064e\u0646\u0652\u06d6")  # مَنْۖ
    assert units[-1].state is CarrierState.PASSTHROUGH
    assert units[-1].carrier == "\u06d6"


# --- the extension carriers -------------------------------------------------


def test_an_extension_carrier_is_never_the_first_member_of_a_counted_pair() -> None:
    for carrier in DECLARED_EXTENSION_CARRIERS:
        unit = CarrierStateUnit(carrier, CarrierState.SUKUN_IMPLICIT)
        assert is_extension_unit(unit)


def test_the_dagger_alef_is_excluded_under_its_own_name() -> None:
    units = (
        CarrierStateUnit("\u0628", CarrierState.SUKUN_IMPLICIT),
        CarrierStateUnit("\u0627", CarrierState.DAGGER),
        CarrierStateUnit("\u062f", CarrierState.SUKUN_EXPLICIT),
    )
    pairs = scan_units(units)
    assert [pair.exclusion for pair in pairs] == [SakinClashExclusion.DAGGER_ALIF]
    assert pairs[0].skipped_passthrough == 1


def test_the_silent_zero_is_carried_on_its_unit_and_not_as_a_stray_unit() -> None:
    units = _CODEC.generate("\u0642\u064e\u0627\u0644\u064f\u0648\u0627\u06df")
    assert len(units) == 5
    assert units[-1].silent
    assert (
        scan_surface("\u0642\u064e\u0627\u0644\u064f\u0648\u0627\u06df").counted == ()
    )


# --- the letter openings ----------------------------------------------------


def test_the_letter_openings_are_placed_outside_the_scope_by_name() -> None:
    report = scan_surface("\u0643\u0647\u064a\u0639\u0635")  # كهيعص
    assert report.treated_as_letter_names
    assert report.counted == ()
    assert all(
        pair.exclusion is SakinClashExclusion.DISCONNECTED_LETTER_NAMES
        for pair in report.pairs
    )


def test_an_opening_exclusion_is_marked_as_residue_defined() -> None:
    report = scan_surface("\u0637\u0647")  # طه
    assert report.pairs
    assert all(pair.is_residue_defined_exclusion for pair in report.pairs)


def test_every_opening_is_a_written_member_of_the_declared_list() -> None:
    assert len(MUQATTAAT_OPENINGS) == 14
    assert "\u0643\u0647\u064a\u0639\u0635" in MUQATTAAT_OPENINGS


# --- artifacts and rare marks ----------------------------------------------


def test_a_latin_letter_between_two_sukuns_names_the_artifact_exclusion() -> None:
    units = (
        CarrierStateUnit("\u0628", CarrierState.SUKUN_EXPLICIT),
        CarrierStateUnit("i", CarrierState.PASSTHROUGH),
        CarrierStateUnit("\u062f", CarrierState.SUKUN_EXPLICIT),
    )
    assert scan_units(units)[0].exclusion is SakinClashExclusion.NON_ARABIC_ARTIFACT


def test_a_rare_reading_mark_between_two_sukuns_names_its_own_exclusion() -> None:
    mark = next(iter(sorted(DECLARED_RARE_READING_MARKS)))
    units = (
        CarrierStateUnit("\u0628", CarrierState.SUKUN_EXPLICIT),
        CarrierStateUnit(mark, CarrierState.PASSTHROUGH),
        CarrierStateUnit("\u062f", CarrierState.SUKUN_EXPLICIT),
    )
    assert scan_units(units)[0].exclusion is SakinClashExclusion.RARE_READING_MARK


def test_the_artifact_codepoints_are_declared_and_hold_the_drawn_line() -> None:
    assert "\u0640" in DECLARED_ARTIFACT_CODEPOINTS


# --- what the predicate still counts ---------------------------------------


def test_two_ordinary_consonants_both_sukun_are_counted_across_a_space() -> None:
    report = scan_surface("\u062f\u0652 \u0635\u0652")  # دْ صْ
    assert len(report.counted) == 1
    assert report.excluded == ()


def test_the_scan_keeps_the_excluded_rows_rather_than_subtracting_them() -> None:
    report = scan_surface(_SUN_WORD)
    assert len(report.pairs) == 2
    assert report.counted == ()
    assert len(report.excluded) == 2
    assert len(report.excluded_by(SakinClashExclusion.ASSIMILATION_PAIR)) == 1


def test_every_embedded_case_is_scannable() -> None:
    for surface in EMBEDDED_ADJACENCY_CASES:
        report = scan_surface(surface)
        assert report.surface == surface
        for pair in report.pairs:
            assert holds_sukun(pair.first) and holds_sukun(pair.second)


# --- pair invariants --------------------------------------------------------


def test_a_pair_runs_forward_and_both_members_hold_a_sukun() -> None:
    sukun = CarrierStateUnit("\u0628", CarrierState.SUKUN_EXPLICIT)
    vowelled = CarrierStateUnit("\u0628", CarrierState.FATHA)
    with pytest.raises(SakinAdjacencyError):
        AdjacentSakinPair(2, 1, sukun, sukun, None, 0)
    with pytest.raises(SakinAdjacencyError):
        AdjacentSakinPair(0, 1, vowelled, sukun, None, 0)
    with pytest.raises(SakinAdjacencyError):
        AdjacentSakinPair(0, 2, sukun, sukun, None, 0)


def test_a_scan_refuses_anything_that_is_not_a_unit() -> None:
    with pytest.raises(SakinAdjacencyError):
        scan_units(["\u0628"])  # type: ignore[list-item]
    with pytest.raises(SakinAdjacencyError):
        scan_surface(7)  # type: ignore[arg-type]


# --- the measurement withheld until a digest arrives ------------------------


def test_no_rate_is_recorded_because_no_source_was_supplied() -> None:
    assert MEASURED_SAKIN_CLASH_SOURCES == ()


def test_a_scan_record_requires_a_digest_of_the_right_shape() -> None:
    digest = hashlib.sha256("\u0628".encode()).hexdigest()
    good = SakinClashScan.measure(
        source_id="probe",
        source_sha256=digest,
        source_byte_length=4,
        normalization_form="NFC",
        unicode_database_version="15.0.0",
        surfaces=ARTICLE_DERIVATION_CASES,
    )
    assert good.pair_total == 6
    assert good.counted_total == 0
    assert good.excluded_total == 6
    assert good.counted_fraction == 0.0
    with pytest.raises(SakinAdjacencyError):
        SakinClashScan(
            source_id="probe",
            source_sha256="short",
            source_byte_length=4,
            normalization_form="NFC",
            unicode_database_version="15.0.0",
            pair_total=1,
            counted_total=0,
            residue_defined_exclusion_total=0,
        )


def test_a_scan_record_holds_no_percentage_field() -> None:
    fields = set(SakinClashScan.__dataclass_fields__)
    assert not any("percent" in name or "fraction" in name for name in fields)


def test_a_scan_record_refuses_more_counted_than_found() -> None:
    digest = "0" * 64
    with pytest.raises(SakinAdjacencyError):
        SakinClashScan(
            source_id="probe",
            source_sha256=digest,
            source_byte_length=4,
            normalization_form="NFC",
            unicode_database_version="15.0.0",
            pair_total=1,
            counted_total=2,
            residue_defined_exclusion_total=0,
        )


# --- the named residuals ----------------------------------------------------


def test_every_named_residual_is_present_and_non_blank() -> None:
    expected = {
        "CLOSURE_IS_A_PREDICATE_NOT_A_MEASURED_RATE",
        "RESIDUE_DEFINED_EXCLUSIONS_ARE_NOT_INDEPENDENT_EVIDENCE",
        "DECLARED_EXTENSION_CARRIERS_ARE_NOT_DERIVED",
        "MUQATTAAT_ARE_EXCLUDED_BY_DEFINITION_NOT_MEASURED",
        "PAUSAL_SUKUN_IS_NOT_DISTINGUISHED_FROM_CONNECTED_SUKUN",
        "TA_MARBUTA_PAUSAL_HA_IS_NOT_ENCODED",
        "NUN_SAKINA_RULINGS_ARE_NOT_MODELLED_HERE",
        "NO_CORPUS_IS_VENDORED_SO_NO_RATE_IS_RECORDED",
        "PHONETIC_ECONOMY_IS_AN_INDUCTION_NOT_A_LICENCE",
    }
    assert set(SAKIN_ADJACENCY_NAMED_RESIDUALS) == expected
    assert all(text.strip() for text in SAKIN_ADJACENCY_NAMED_RESIDUALS.values())


def test_the_residue_defined_exclusions_are_exactly_the_three_named() -> None:
    residue = {member for member in SakinClashExclusion if member.is_residue_defined}
    assert residue == {
        SakinClashExclusion.DISCONNECTED_LETTER_NAMES,
        SakinClashExclusion.NON_ARABIC_ARTIFACT,
        SakinClashExclusion.RARE_READING_MARK,
    }


def test_the_module_imports_nothing_from_the_kernel() -> None:
    import pathlib

    import alghanem.arabic.encoding.sakin_adjacency as module

    source = pathlib.Path(module.__file__ or "").read_text(encoding="utf-8")
    assert "alghanem.kernel" not in source
    assert "from alghanem.kernel" not in source


def test_every_exclusion_is_reachable_by_some_scanned_unit_sequence() -> None:
    """No exclusion may name a case no pair can reach.

    The dagger exclusion was exactly such a dead branch before this test: a
    dagger unit holds no sukun, so it could never be a member of a pair, and the
    name sat in the enum unreadable. The guard is the genus, not that instance.
    """
    reached: set[SakinClashExclusion] = set()
    probes: tuple[tuple[CarrierStateUnit, ...], ...] = (
        _CODEC.generate(_SUN_WORD),
        _CODEC.generate("\u0628\u0652\u0627\u0652"),  # بْاْ
        _CODEC.generate("\u0642\u064e\u0627\u0644\u064f\u0648\u0627\u06df"),
        (
            CarrierStateUnit("\u0628", CarrierState.SUKUN_IMPLICIT),
            CarrierStateUnit("\u0627", CarrierState.DAGGER),
            CarrierStateUnit("\u062f", CarrierState.SUKUN_EXPLICIT),
        ),
        (
            CarrierStateUnit("\u0628", CarrierState.SUKUN_EXPLICIT),
            CarrierStateUnit("i", CarrierState.PASSTHROUGH),
            CarrierStateUnit("\u062f", CarrierState.SUKUN_EXPLICIT),
        ),
        (
            CarrierStateUnit("\u0628", CarrierState.SUKUN_EXPLICIT),
            CarrierStateUnit("\u06dc", CarrierState.PASSTHROUGH),
            CarrierStateUnit("\u062f", CarrierState.SUKUN_EXPLICIT),
        ),
    )
    for units in probes:
        for pair in scan_units(units):
            if pair.exclusion is not None:
                reached.add(pair.exclusion)
    for pair in scan_surface("\u0643\u0647\u064a\u0639\u0635").pairs:
        assert pair.exclusion is not None
        reached.add(pair.exclusion)
    assert reached == set(SakinClashExclusion)
