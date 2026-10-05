"""Tests for the enforced AIM.1 aim record layer."""

from __future__ import annotations

import pkgutil
from dataclasses import fields, replace

import pytest

import alghanem.kernel as kernel_package
from alghanem.program import (
    AIM_ATTAINMENT_REFUSAL_GENERA,
    AIM_RECORDS,
    AIM_TERMINATION_DESCRIPTORS,
    ATTAINMENT_DEFERRAL_NOTE,
    DESIGN_SOURCE_OPEN_QUESTION,
    FOREIGN_DECLARED_AIMS,
    AimAttainmentRefusalGenus,
    AimEngagement,
    AimId,
    AimRecord,
    AimRecordError,
    AimTerminationDescriptor,
    AimTerminationStructure,
    AttainmentStanding,
    ForeignDeclaredAim,
    TerminationProofSite,
)
from alghanem.program import aims as aims_module

_ANSWER_MARKERS = (
    "answer",
    "verdict",
    "conclusion",
    "resolution",
    "decision",
    "result",
    "outcome",
    "birth",
    "promotion",
    "indicator",
    "score",
    "percent",
    "estimate",
    "priority",
)


def record(**overrides: object) -> AimRecord:
    base: dict[str, object] = dict(
        aim_id=AimId.K1,
        question="متى يصير الانتقال مُرخَّصًا؟",
        what_counts_as_reaching="سلطةٌ تُصدر انتقالًا مُرخَّصًا",
        what_does_not_count="القبول البنيوي مهما كَمُلت فحوصه",
        citation="docs/CONSTITUTION.md، صفّ القبول البنيوي",
        engagement=AimEngagement.UNCLASSIFIED_IN_RECORD,
        attainment=AttainmentStanding.NOT_REACHED,
    )
    base.update(overrides)
    return AimRecord(**base)  # type: ignore[arg-type]


def test_the_two_axes_are_independent_vocabularies() -> None:
    assert len(AimEngagement) == 3
    assert len(AttainmentStanding) == 3
    members = [*AimEngagement, *AttainmentStanding]
    assert len({member.value for member in members}) == len(members)


def test_every_declared_aim_id_carries_exactly_one_record() -> None:
    assert set(AIM_RECORDS) == set(AimId)
    assert len(AIM_RECORDS) == len(AimId) == 13
    for aim_id, aim in AIM_RECORDS.items():
        assert aim.aim_id is aim_id


def test_attainment_is_declared_and_not_constructible_today() -> None:
    assert AttainmentStanding.REACHED in AttainmentStanding
    with pytest.raises(AimRecordError, match="غير قابل للبناء"):
        record(attainment=AttainmentStanding.REACHED)


def test_no_recorded_aim_claims_attainment() -> None:
    assert all(aim.remains_unattained for aim in AIM_RECORDS.values())


def test_a_named_obstacle_is_required_exactly_when_blocked() -> None:
    with pytest.raises(AimRecordError, match="الحاجز المُسمّى"):
        record(engagement=AimEngagement.BLOCKED_BY_NAMED_OBSTACLE)
    with pytest.raises(AimRecordError, match="يبقى فارغًا"):
        record(named_obstacle="حاجزٌ بلا انسداد مُسجَّل")
    blocked = record(
        engagement=AimEngagement.BLOCKED_BY_NAMED_OBSTACLE,
        named_obstacle="غيابُ سلطة تقويم محتوى الدليل",
    )
    assert blocked.obstacle_is_named


def test_a_named_remainder_is_required_exactly_when_partially_reached() -> None:
    partial = AttainmentStanding.PARTIALLY_REACHED_WITH_NAMED_REMAINDER
    with pytest.raises(AimRecordError, match="البقيّة المُسمّاة"):
        record(attainment=partial)
    with pytest.raises(AimRecordError, match="يبقى فارغًا"):
        record(named_remainder="بقيّةٌ بلا بلوغٍ جزئيّ مُسجَّل")
    reached = record(attainment=partial, named_remainder="مفردتان لم تُصدَّرا بعد")
    assert reached.remains_unattained


def test_an_aim_that_has_not_started_carries_no_partial_attainment() -> None:
    with pytest.raises(AimRecordError, match="لم تبدأ"):
        record(
            engagement=AimEngagement.NOT_STARTED,
            attainment=AttainmentStanding.PARTIALLY_REACHED_WITH_NAMED_REMAINDER,
            named_remainder="بقيّةٌ مُسمّاة",
        )


@pytest.mark.parametrize(
    "field_name",
    ("question", "what_counts_as_reaching", "what_does_not_count", "citation"),
)
def test_every_aim_text_must_be_non_blank(field_name: str) -> None:
    with pytest.raises(AimRecordError):
        record(**{field_name: "   "})


def test_closed_vocabularies_reject_foreign_values() -> None:
    with pytest.raises(AimRecordError, match="معرّف الغاية"):
        record(aim_id="AIM-K1")
    with pytest.raises(AimRecordError, match="رتبة الانشغال"):
        record(engagement="لم_تبدأ")
    with pytest.raises(AimRecordError, match="رتبة البلوغ"):
        record(attainment="لم_تُبلَغ")


@pytest.mark.parametrize("marker", _ANSWER_MARKERS)
def test_no_record_type_carries_an_answer_bearing_field(marker: str) -> None:
    for declaring_type in (AimRecord, ForeignDeclaredAim):
        declared = {item.name for item in fields(declaring_type)}
        assert not any(marker in name for name in declared), declaring_type


def test_an_aim_record_is_frozen_and_replacement_is_revalidated() -> None:
    with pytest.raises(AimRecordError, match="غير قابل للبناء"):
        replace(AIM_RECORDS[AimId.K2], attainment=AttainmentStanding.REACHED)


def test_the_recorded_blocked_aims_are_exactly_those_named_in_the_document() -> None:
    blocked = {aim_id for aim_id, aim in AIM_RECORDS.items() if aim.obstacle_is_named}
    assert blocked == {AimId.K2, AimId.K3, AimId.A2}
    not_started = {
        aim_id
        for aim_id, aim in AIM_RECORDS.items()
        if aim.engagement is AimEngagement.NOT_STARTED
    }
    assert not_started == {AimId.K4, AimId.E1, AimId.E2}


def test_unclassified_aims_are_recorded_and_not_folded_into_not_started() -> None:
    unclassified = {
        aim_id
        for aim_id, aim in AIM_RECORDS.items()
        if aim.engagement is AimEngagement.UNCLASSIFIED_IN_RECORD
    }
    assert unclassified == {
        AimId.K1,
        AimId.A1,
        AimId.A3,
        AimId.X1,
        AimId.T1,
        AimId.T2,
        AimId.T3,
    }


def test_foreign_declared_aims_are_a_separate_type_outside_derivation() -> None:
    assert len(FOREIGN_DECLARED_AIMS) == 2
    local_ids = {member.value for member in AimId}
    for foreign in FOREIGN_DECLARED_AIMS:
        assert not isinstance(foreign, AimRecord)
        assert foreign.foreign_aim_id not in local_ids
        assert foreign.enters_local_derivation is False


def test_this_milestone_declares_no_indicator_value() -> None:
    for aim in AIM_RECORDS.values():
        assert not any(
            isinstance(getattr(aim, item.name), int | float)
            and not isinstance(getattr(aim, item.name), bool)
            for item in fields(aim)
        )


def test_the_module_cites_its_direct_design_source() -> None:
    assert aims_module.__doc__ is not None
    assert DESIGN_SOURCE_OPEN_QUESTION in aims_module.__doc__


def test_no_kernel_module_reads_the_aim_record_layer() -> None:
    for module in pkgutil.walk_packages(
        kernel_package.__path__, prefix="alghanem.kernel."
    ):
        source = module.module_finder.find_spec(  # type: ignore[union-attr]
            module.name
        )
        assert source is not None and source.origin is not None
        with open(source.origin, encoding="utf-8") as handle:
            text = handle.read()
        assert "alghanem.program" not in text, module.name
        assert "AimRecord" not in text, module.name
        assert "AIM_RECORDS" not in text, module.name


# --- the ninth milestone: the refusal genus is derived, not declared ---


def test_the_termination_and_genus_vocabularies_are_three_valued() -> None:
    assert len(AimTerminationStructure) == 3
    assert len(AimAttainmentRefusalGenus) == 3
    members = [*AimTerminationStructure, *AimAttainmentRefusalGenus]
    assert len({member.value for member in members}) == len(members)


def test_no_aim_carries_a_proved_termination_structure_today() -> None:
    for aim_id, descriptor in AIM_TERMINATION_DESCRIPTORS.items():
        assert descriptor.aim_id is aim_id
        assert descriptor.proved_sites == frozenset()
        assert (
            aims_module.derive_aim_termination_structure(descriptor)
            is AimTerminationStructure.TERMINATION_STRUCTURE_NOT_SETTLED
        )


def test_the_refusal_genus_is_unsettled_for_every_aim_today() -> None:
    assert set(AIM_ATTAINMENT_REFUSAL_GENERA) == set(AimId)
    assert set(AIM_ATTAINMENT_REFUSAL_GENERA.values()) == {
        AimAttainmentRefusalGenus.GENUS_NOT_SETTLED
    }


def test_a_descriptor_may_not_carry_a_proof_no_authority_issued() -> None:
    site = TerminationProofSite.CONSTITUTION_ROW_ESTABLISHING_A_TERMINAL_ARTEFACT
    with pytest.raises(AimRecordError, match="لا موضعَ برهانٍ قائمًا"):
        AimTerminationDescriptor(aim_id=AimId.K4, proved_sites=frozenset({site}))


def test_the_structure_reader_is_total_over_its_proof_sites() -> None:
    open_ended = (
        TerminationProofSite.CONSTITUTION_ROW_ESTABLISHING_FRACTAL_OPEN_ENDEDNESS
    )
    terminal = TerminationProofSite.CONSTITUTION_ROW_ESTABLISHING_A_TERMINAL_ARTEFACT
    read = aims_module._structure_of_proved_sites
    assert (
        read(frozenset({open_ended}))
        is AimTerminationStructure.OPEN_ENDED_BY_FRACTAL_RECURSION
    )
    assert (
        read(frozenset({terminal}))
        is AimTerminationStructure.TERMINAL_ON_A_NAMED_ARTEFACT
    )
    assert (
        read(frozenset()) is AimTerminationStructure.TERMINATION_STRUCTURE_NOT_SETTLED
    )
    with pytest.raises(AimRecordError, match="موضعا برهانٍ متناقضان"):
        read(frozenset({open_ended, terminal}))


def test_each_structure_carries_its_own_refusal_genus() -> None:
    genus = aims_module._genus_of_structure
    assert (
        genus(AimTerminationStructure.OPEN_ENDED_BY_FRACTAL_RECURSION)
        is AimAttainmentRefusalGenus.REFUSED_BY_STRUCTURAL_CATEGORY_MISMATCH
    )
    assert (
        genus(AimTerminationStructure.TERMINAL_ON_A_NAMED_ARTEFACT)
        is AimAttainmentRefusalGenus.HELD_BY_MISSING_AUTHORITY_TODAY
    )
    assert (
        genus(AimTerminationStructure.TERMINATION_STRUCTURE_NOT_SETTLED)
        is AimAttainmentRefusalGenus.GENUS_NOT_SETTLED
    )


def test_the_deferral_note_no_longer_declares_one_genus_for_all_aims() -> None:
    assert "لا سلطة هنا تُصدر بلوغَ غاية" not in ATTAINMENT_DEFERRAL_NOTE
    assert "يُشتَقّ" in ATTAINMENT_DEFERRAL_NOTE


def test_the_descriptor_carries_no_declared_structure_field() -> None:
    names = {item.name for item in fields(AimTerminationDescriptor)}
    assert names == {"aim_id", "proved_sites"}
    for marker in _ANSWER_MARKERS:
        assert not any(marker in name for name in names)
