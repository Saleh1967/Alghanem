"""اختباراتُ قراءة P-EXTRACTOR: أدوارٌ مغلقة، وغموضٌ خارج المفردة، وأرضيّةٌ محفوظة."""

from __future__ import annotations

import ast
from dataclasses import fields
from pathlib import Path

import pytest

from alghanem.arabic.encoding.carrier_state_candidate import (
    EMBEDDED_ROUND_TRIP_CASES,
    CarrierState,
    CarrierStateCodec,
    GeminationRole,
)
from alghanem.arabic.gflk_codec_revision_audit import SILENT_OVERWRITE_LOCATIONS
from alghanem.arabic.gflk_state_machine_registration import (
    P_EXTRACTOR_ACCEPTANCE_CONDITION,
    UNRESOLVABLE_PROPOSALS,
)
from alghanem.arabic.p_extractor import (
    AMBIGUOUS_PROPOSAL,
    SILENCING_ROLES,
    AmbiguityRecord,
    LetterReading,
    PExtractorError,
    PExtractorReading,
    PhoneticRole,
    UndecidedSite,
    read_surface,
    reading_preserves_the_round_trip,
    retrieve_surface,
)
from alghanem.arabic.p_extractor_preregistration import (
    PASS_TWO_RULES,
    PREREGISTRATION_DIGEST,
    RuleDecidability,
    RuleEmission,
    acceptance_condition,
    floor_named_cases,
    preregistration_digest,
    rule_named,
)

_SOURCE_ROOT = Path(__file__).resolve().parents[2] / "src"


def test_the_role_vocabulary_is_closed_at_five() -> None:
    assert len(PhoneticRole) == 5
    assert {role.name for role in PhoneticRole} == {
        "ASSIMILATED_SILENT",
        "MADD_EXTENSION",
        "SHADDA_PAIR_START",
        "SILENT_DIFFERENTIATING_ALIF",
        "TANWEEN_ALIF_CARRIER",
    }


def test_the_state_vocabulary_was_not_enlarged_by_the_reading() -> None:
    assert len(CarrierState) == 7


def test_the_preregistration_digest_did_not_drift() -> None:
    assert preregistration_digest() == PREREGISTRATION_DIGEST


def test_the_frozen_rule_order_is_contiguous_and_named_once() -> None:
    orders = [rule.order for rule in PASS_TWO_RULES]
    assert orders == list(range(1, len(PASS_TWO_RULES) + 1))
    names = [rule.name for rule in PASS_TWO_RULES]
    assert len(set(names)) == len(names)
    assert rule_named("IDGHAM").order == 1


def test_undecidable_rules_emit_no_role() -> None:
    for rule in PASS_TWO_RULES:
        if rule.decidability is RuleDecidability.UNDECIDABLE_FROM_THE_WRITTEN_MARKS:
            assert rule.emission is not RuleEmission.ROLE_OVER_AN_EXISTING_UNIT
            assert rule.emitted_role_name is None


def test_the_acceptance_floor_is_read_not_restated() -> None:
    assert acceptance_condition() is P_EXTRACTOR_ACCEPTANCE_CONDITION
    assert floor_named_cases() == tuple(
        token.location for token in SILENT_OVERWRITE_LOCATIONS
    )
    assert P_EXTRACTOR_ACCEPTANCE_CONDITION.explicit_test_cases.strip()


def test_the_reading_touches_no_unit_on_the_embedded_cases() -> None:
    codec = CarrierStateCodec()
    for surface in EMBEDDED_ROUND_TRIP_CASES:
        reading = read_surface(surface)
        assert reading.units == codec.generate(surface)
        assert retrieve_surface(reading) == codec.retrieve(codec.generate(surface))
        assert reading_preserves_the_round_trip(surface)


def test_the_six_named_locations_are_still_the_only_named_cases() -> None:
    locations = floor_named_cases()
    assert len(locations) == 6
    assert len(set(locations)) == 6
    assert locations == tuple(sorted(locations))


def test_madd_is_read_where_a_matching_short_vowel_precedes() -> None:
    reading = read_surface("\u0642\u064e\u0627\u0644\u064f\u0648\u0627")
    assert reading.roles_at(1) == (PhoneticRole.MADD_EXTENSION,)
    assert reading.roles_at(3) == (PhoneticRole.MADD_EXTENSION,)
    assert reading.roles_at(4) == (PhoneticRole.SILENT_DIFFERENTIATING_ALIF,)


def test_the_tanween_seat_is_read_in_both_written_orders() -> None:
    marked_first = read_surface("\u0643\u0650\u062a\u064e\u0627\u0628\u064b\u0627")
    assert marked_first.letters[-1].has_role(PhoneticRole.TANWEEN_ALIF_CARRIER)
    assert not marked_first.letters[-1].has_role(PhoneticRole.MADD_EXTENSION)
    alif_first = read_surface("\u0633\u0650\u064a\u064e\u0627\u0642\u0627\u064b")
    assert alif_first.letters[-1].has_role(PhoneticRole.TANWEEN_ALIF_CARRIER)
    assert alif_first.letters[-1].unit.tanwin_alif_seat


def test_idgham_silences_the_first_of_two_unlike_letters() -> None:
    reading = read_surface(
        "\u0627\u0644\u0631\u064e\u0651\u062d\u0650\u064a\u0645\u0650"
    )
    assert reading.letters[1].has_role(PhoneticRole.ASSIMILATED_SILENT)
    assert reading.letters[2].has_role(PhoneticRole.SHADDA_PAIR_START)
    assert reading.letters[2].unit.gemination is GeminationRole.PAIR_START


def test_haraka_bearing_is_derived_and_not_stored() -> None:
    stored = {field.name for field in fields(LetterReading)}
    assert stored == {"index", "unit", "roles"}
    assert "is_haraka_bearing" not in stored
    reading = read_surface(
        "\u0627\u0644\u0631\u064e\u0651\u062d\u0650\u064a\u0645\u0650"
    )
    bearing = reading.haraka_bearing
    assert all(
        not any(role in SILENCING_ROLES for role in letter.roles) for letter in bearing
    )
    assert all(
        letter.unit.state is not CarrierState.SUKUN_IMPLICIT for letter in bearing
    )


def test_the_ambiguity_is_a_separate_record_reading_its_own_registration() -> None:
    reading = read_surface("\u0633\u0650\u064a\u064e\u0627\u0642\u0627\u064b")
    assert len(reading.ambiguities) == 1
    record = reading.ambiguities[0]
    assert isinstance(record, AmbiguityRecord)
    assert record.proposal is UNRESOLVABLE_PROPOSALS[0]
    assert record.proposed_name == "AMBIGUOUS_MADD_OR_TANWEEN_ROOT"
    assert record.proposal is AMBIGUOUS_PROPOSAL


def test_the_ambiguity_name_is_a_member_of_no_enum_in_the_tree() -> None:
    forbidden = "AMBIGUOUS_MADD_OR_TANWEEN_ROOT"
    offenders: list[str] = []
    for path in _SOURCE_ROOT.rglob("*.py"):
        tree = ast.parse(path.read_text(encoding="utf-8"))
        for node in ast.walk(tree):
            if not isinstance(node, ast.ClassDef):
                continue
            bases = {
                base.id if isinstance(base, ast.Name) else getattr(base, "attr", "")
                for base in node.bases
            }
            if not bases & {"Enum", "StrEnum", "IntEnum"}:
                continue
            for statement in node.body:
                if isinstance(statement, ast.Assign):
                    for target in statement.targets:
                        if isinstance(target, ast.Name) and target.id == forbidden:
                            offenders.append(f"{path}:{node.name}")
    assert offenders == []


def test_the_undecided_wasl_site_is_recorded_not_guessed() -> None:
    reading = read_surface(
        "\u0627\u0644\u0631\u064e\u0651\u062d\u0650\u064a\u0645\u0650"
    )
    assert len(reading.undecided) == 1
    site = reading.undecided[0]
    assert isinstance(site, UndecidedSite)
    assert site.rule_name == "WASL_LAM"
    assert site.why_it_is_undecided.strip()
    assert site.tree_reference.strip()


def test_no_reading_carries_a_resolution_field() -> None:
    for record in (LetterReading, AmbiguityRecord, UndecidedSite, PExtractorReading):
        names = {field.name for field in fields(record)}
        assert not names & {"resolution", "resolved", "verdict", "outcome", "decision"}


def test_a_reading_refuses_a_foreign_preregistration_digest() -> None:
    with pytest.raises(PExtractorError):
        PExtractorReading(surface="", letters=(), preregistration_digest="0" * 64)


def test_a_reading_refuses_a_gap_in_the_unit_positions() -> None:
    units = CarrierStateCodec().generate("\u0628\u064e")
    with pytest.raises(PExtractorError):
        PExtractorReading(surface="\u0628\u064e", letters=(LetterReading(1, units[0]),))


def test_a_role_may_not_be_hung_twice_on_one_unit() -> None:
    units = CarrierStateCodec().generate("\u0628\u064e")
    with pytest.raises(PExtractorError):
        LetterReading(
            0,
            units[0],
            (PhoneticRole.MADD_EXTENSION, PhoneticRole.MADD_EXTENSION),
        )
