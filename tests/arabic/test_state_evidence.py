"""اختباراتُ الثلاثيّة (شرط/مانع/متعذِّر) وجنسِ السبب قبل توليد حاملِ الحالة."""

from __future__ import annotations

import unicodedata

import pytest

from alghanem.arabic.encoding.carrier_state_candidate import (
    EMBEDDED_ROUND_TRIP_CASES,
    CarrierState,
    CarrierStateCodec,
    CarrierStateEncodingError,
    CarrierStateUnit,
    GeminationRole,
    derive_alef_states,
    round_trip_holds,
)
from alghanem.arabic.encoding.state_evidence import (
    DECLARED_STATE_MARKS,
    REFUSAL_GENUS_REGISTRY,
    STATE_EVIDENCE_NAMED_RESIDUALS,
    EvidencedUnit,
    EvidencingReader,
    MarkObservation,
    RefusalGenus,
    RefusalSite,
    StateEvidence,
    StateEvidenceError,
    derive_mark_observations,
    derive_observed_capacities,
    derive_refusal_sites,
    derive_unclassified_refusal_sites,
)

ALEF = "\u0627"
BA = "\u0628"
FATHA = "\u064e"
DAMMA = "\u064f"
SHADDA = "\u0651"
SUKUN = "\u0652"
DAGGER_ALIF = "\u0670"
ALEF_WASLA = "\u0671"
AL_HAMD = "\u0627\u0644\u062d\u0645\u062f"


# --- الخطوة الأولى: تصنيفُ ما هو قائم ----------------------------------------


def test_every_existing_refusal_carries_a_named_genus() -> None:
    assert derive_unclassified_refusal_sites() == ()


def test_the_classification_covers_exactly_the_sites_that_exist() -> None:
    assert set(REFUSAL_GENUS_REGISTRY) == set(derive_refusal_sites())


def test_an_added_refusal_without_a_genus_is_reported_not_ignored() -> None:
    invented = RefusalSite("generate", "a refusal nobody classified")
    assert invented not in REFUSAL_GENUS_REGISTRY


def test_each_genus_has_at_least_one_existing_site() -> None:
    present = set(REFUSAL_GENUS_REGISTRY.values())
    assert present == set(RefusalGenus)


def test_a_condition_refusal_is_raised_by_the_deposited_module() -> None:
    site = RefusalSite("__post_init__", "a carrier is exactly one codepoint")
    assert REFUSAL_GENUS_REGISTRY[site] is RefusalGenus.CONDITION
    with pytest.raises(CarrierStateEncodingError, match="exactly one codepoint"):
        CarrierStateUnit("\u0628\u062a", CarrierState.FATHA)


def test_a_preventer_refusal_is_raised_by_the_deposited_module() -> None:
    site = RefusalSite(
        "_refuse_unheld_flags", "an explicit madda is read on the waw only"
    )
    assert REFUSAL_GENUS_REGISTRY[site] is RefusalGenus.PREVENTER
    with pytest.raises(CarrierStateEncodingError, match="madda"):
        CarrierStateUnit(BA, CarrierState.FATHA, waw_madda=True)


def test_an_undecidable_refusal_is_raised_by_the_deposited_module() -> None:
    site = RefusalSite(
        "_read_marks", "a second vowel mark writes over a state already read in"
    )
    assert REFUSAL_GENUS_REGISTRY[site] is RefusalGenus.UNDECIDABLE
    with pytest.raises(CarrierStateEncodingError, match="second vowel mark"):
        CarrierStateCodec().generate(BA + FATHA + DAMMA)


def test_the_two_undecidable_sites_are_the_double_writes_and_no_others() -> None:
    undecidable = {
        site
        for site, genus in REFUSAL_GENUS_REGISTRY.items()
        if genus is RefusalGenus.UNDECIDABLE
    }
    assert {site.function for site in undecidable} == {"_read_marks"}
    assert len(undecidable) == 2


def test_every_genus_carries_an_arabic_name() -> None:
    assert RefusalGenus.CONDITION.arabic_name == "شرط"
    assert RefusalGenus.PREVENTER.arabic_name == "مانع"
    assert RefusalGenus.UNDECIDABLE.arabic_name == "متعذِّر"


# --- الخطوة الثانية: السببُ بمعناه الضيّق -------------------------------------


def test_a_written_mark_is_read_as_a_written_mark() -> None:
    (read,) = EvidencingReader().read(BA + FATHA)
    assert read.evidence is StateEvidence.WRITTEN_MARK
    assert read.evidence.is_read_from_the_surface
    assert [mark.codepoint for mark in read.marks] == [FATHA]


def test_al_hamd_rests_on_no_written_mark_at_all() -> None:
    units = EvidencingReader().read(AL_HAMD)
    assert len(units) == 5
    assert all(item.unit.state is CarrierState.SUKUN_IMPLICIT for item in units)
    assert not any(
        item.evidence is StateEvidence.WRITTEN_MARK for item in units
    ), "not one of the five states is read off the surface"
    assert [item.evidence for item in units[1:]] == [
        StateEvidence.ABSENCE_ASSUMPTION
    ] * 4


def test_the_alef_of_al_hamd_is_undecidable_and_not_asserted_sakin() -> None:
    first = EvidencingReader().read(AL_HAMD)[0]
    assert first.unit.carrier == ALEF
    assert first.evidence is StateEvidence.UNDECIDABLE
    assert not first.evidence.is_read_from_the_surface
    assert first.marks == ()


def test_a_written_wasla_is_not_undecidable_because_its_writer_decided() -> None:
    (read,) = EvidencingReader().read(ALEF_WASLA)
    assert read.unit.carrier == ALEF_WASLA
    assert read.evidence is StateEvidence.ABSENCE_ASSUMPTION


def test_a_marked_word_initial_alef_is_not_undecidable() -> None:
    first = EvidencingReader().read(ALEF + FATHA + BA)[0]
    assert first.evidence is StateEvidence.WRITTEN_MARK


def test_undecidability_is_word_initial_and_not_a_property_of_the_alef() -> None:
    units = EvidencingReader().read(BA + ALEF)
    assert [item.evidence for item in units] == [
        StateEvidence.ABSENCE_ASSUMPTION,
        StateEvidence.ABSENCE_ASSUMPTION,
    ]


def test_a_word_after_a_space_starts_a_new_word() -> None:
    units = EvidencingReader().read(BA + " " + ALEF)
    assert units[1].evidence is None
    assert units[2].evidence is StateEvidence.UNDECIDABLE


def test_a_carrier_state_is_not_built_without_the_genus_of_its_sabab() -> None:
    with pytest.raises(StateEvidenceError, match="genus of its sabab"):
        EvidencedUnit(CarrierStateUnit(BA, CarrierState.FATHA), None)


def test_a_written_mark_genus_without_a_mark_is_refused() -> None:
    with pytest.raises(StateEvidenceError, match="names no mark"):
        EvidencedUnit(
            CarrierStateUnit(BA, CarrierState.FATHA), StateEvidence.WRITTEN_MARK
        )


def test_an_absence_assumption_carrying_a_mark_is_refused() -> None:
    with pytest.raises(StateEvidenceError, match="rests on no written mark"):
        EvidencedUnit(
            CarrierStateUnit(BA, CarrierState.SUKUN_IMPLICIT),
            StateEvidence.ABSENCE_ASSUMPTION,
            (MarkObservation(1, FATHA),),
        )


def test_a_passthrough_takes_no_state_evidence() -> None:
    with pytest.raises(StateEvidenceError, match="no state evidence"):
        EvidencedUnit(
            CarrierStateUnit("!", CarrierState.PASSTHROUGH),
            StateEvidence.ABSENCE_ASSUMPTION,
        )


def test_an_orphan_mark_is_carried_and_evidences_nothing() -> None:
    units = EvidencingReader().read(FATHA + BA)
    assert units[0].unit.state is CarrierState.PASSTHROUGH
    assert units[0].evidence is None
    assert [mark.codepoint for mark in units[0].marks] == [FATHA]


def test_a_dagger_alef_is_a_written_mark() -> None:
    units = EvidencingReader().read(BA + FATHA + DAGGER_ALIF)
    assert units[1].unit.state is CarrierState.DAGGER
    assert units[1].evidence is StateEvidence.WRITTEN_MARK


def test_the_shadda_evidences_no_state_for_either_half() -> None:
    units = EvidencingReader().read(BA + SHADDA)
    assert len(units) == 2
    assert units[0].unit.gemination is GeminationRole.PAIR_START
    assert [item.evidence for item in units] == [
        StateEvidence.ABSENCE_ASSUMPTION,
        StateEvidence.ABSENCE_ASSUMPTION,
    ]
    assert SHADDA not in DECLARED_STATE_MARKS


def test_the_second_half_of_a_pair_carries_the_mark_the_surface_wrote() -> None:
    units = EvidencingReader().read(BA + SHADDA + FATHA)
    assert units[0].marks == ()
    assert [mark.codepoint for mark in units[1].marks] == [FATHA]


def test_every_evidence_genus_carries_an_arabic_name() -> None:
    assert StateEvidence.WRITTEN_MARK.arabic_name == "علامةٌ مكتوبة"
    assert StateEvidence.ABSENCE_ASSUMPTION.arabic_name == "افتراضٌ عند الغياب"
    assert StateEvidence.UNDECIDABLE.arabic_name == "متعذِّر"


# --- الخطوة الثالثة: العلامةُ المرصودة ليست الحالةَ المشتقّة --------------------


def test_an_observed_mark_is_not_a_derived_state() -> None:
    surface = BA + FATHA + DAMMA
    assert len(derive_mark_observations(surface)) == 2
    with pytest.raises(CarrierStateEncodingError):
        CarrierStateCodec().generate(surface)


def test_an_observation_carries_its_codepoint_and_its_place() -> None:
    (observation,) = derive_mark_observations(BA + SUKUN)
    assert observation.offset == 1
    assert observation.codepoint == SUKUN
    assert observation.unicode_name == unicodedata.name(SUKUN)


def test_an_observation_outside_the_declared_marks_is_refused() -> None:
    with pytest.raises(StateEvidenceError, match="DECLARED_STATE_MARKS"):
        MarkObservation(0, BA)


def test_a_negative_offset_is_refused() -> None:
    with pytest.raises(StateEvidenceError, match="not negative"):
        MarkObservation(-1, FATHA)


def test_every_reported_offset_points_at_the_mark_it_names() -> None:
    reader = EvidencingReader()
    seen = 0
    for surface in EMBEDDED_ROUND_TRIP_CASES:
        text = unicodedata.normalize("NFC", surface)
        for item in reader.read(text):
            for mark in item.marks:
                seen += 1
                assert text[mark.offset] == mark.codepoint
    assert seen > 0


def test_no_observed_state_mark_is_dropped_by_the_reader() -> None:
    reader = EvidencingReader()
    for surface in EMBEDDED_ROUND_TRIP_CASES:
        text = unicodedata.normalize("NFC", surface)
        carried = sum(len(item.marks) for item in reader.read(text))
        assert carried == len(derive_mark_observations(text))


# --- الخطوة الرابعة: القابليّةُ مرصودةٌ لا مُعلَنة ------------------------------


def test_capacity_is_derived_from_what_was_observed() -> None:
    census = derive_observed_capacities([BA + FATHA, BA + DAMMA])
    assert census.surfaces_read == 2
    assert census.observed[BA] == frozenset({FATHA, DAMMA})


def test_an_unobserved_pair_is_unobserved_and_never_impossible() -> None:
    census = derive_observed_capacities([BA + FATHA])
    unobserved = set(census.unobserved_pairs())
    assert (BA, SUKUN) in unobserved
    assert (BA, FATHA) not in unobserved


def test_a_census_over_nothing_observes_nothing() -> None:
    census = derive_observed_capacities([])
    assert census.surfaces_read == 0
    assert census.observed == {}


# --- الخطوة الخامسة: لم يُكسَر شيء مِن المُودَع --------------------------------


def test_the_deposited_round_trip_still_holds_for_every_embedded_case() -> None:
    assert all(round_trip_holds(surface) for surface in EMBEDDED_ROUND_TRIP_CASES)


def test_the_deposited_alef_state_derivation_is_untouched() -> None:
    assert len(derive_alef_states()) > 1


def test_the_reader_returns_the_units_the_deposited_codec_returned() -> None:
    codec = CarrierStateCodec()
    for surface in EMBEDDED_ROUND_TRIP_CASES:
        text = unicodedata.normalize("NFC", surface)
        assert tuple(item.unit for item in EvidencingReader().read(text)) == (
            codec.generate(text)
        )


def test_the_named_residuals_are_non_empty_prose() -> None:
    assert STATE_EVIDENCE_NAMED_RESIDUALS
    assert all(value.strip() for value in STATE_EVIDENCE_NAMED_RESIDUALS.values())


def test_the_efficient_cause_is_recorded_as_omitted_by_decision() -> None:
    assert (
        "EFFICIENT_CAUSE_IS_OMITTED_BY_DECISION_NOT_BY_SILENCE"
        in STATE_EVIDENCE_NAMED_RESIDUALS
    )
