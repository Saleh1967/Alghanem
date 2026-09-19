"""اختباراتُ الانتقال إلى المقطع: هدفٌ مقيسٌ، وقارئٌ أعمى، ونتيجةٌ سالبةٌ مقيسة."""

from __future__ import annotations

from pathlib import Path

import pytest

from alghanem.arabic import syllable_transition_experiment as transition_module
from alghanem.arabic.disambiguation_layer_order import (
    DisambiguationLayer,
    LayerOrderError,
    a_lookup_reader,
    run_ladder,
)
from alghanem.arabic.hamza_contract import (
    HamzaFunction,
    HamzaIdentity,
    HamzaOccurrence,
    HamzaRealization,
    HamzaSeat,
)
from alghanem.arabic.syllable_transition_experiment import (
    SYLLABLE_TRANSITION_NAMED_RESIDUALS,
    THE_DECLARED_HOSTED_ITEMS,
    THE_DECLARED_HOSTS,
    THE_HOSTED_LADDER,
    THE_SYLLABLE_SHAPE_TARGET,
    HostedOccurrence,
    SyllableTransitionError,
    hosted_item,
    measured_syllable_shape,
    refuse_a_syllable_birth_claim_from_this_run,
    run_syllable_transition_experiment,
    the_transition_to_the_syllable_is_established,
)
from alghanem.import_boundary import ImportBoundaryPolicy, audit_import_boundary


def _a_declared_occurrence() -> HamzaOccurrence:
    return HamzaOccurrence(
        surface="أَكَلَ",
        index=0,
        identity=HamzaIdentity.HAMZA,
        seat=HamzaSeat.ON_ALEF,
        function=HamzaFunction.QAT,
        realization=HamzaRealization.REALIZED,
        context="مقامٌ مُعلَنٌ في الاختبار",
        declared_source="إعلانُ الاختبار",
        content="مضمونٌ مُعلَن",
    )


# --- الحدودُ البنيويّة --------------------------------------------------------


def test_the_transition_module_reaches_no_kernel_module() -> None:
    reached = audit_import_boundary(
        (Path(str(transition_module.__file__)),),
        ImportBoundaryPolicy(
            policy_id="syllable-transition-experiment",
            permitted_modules=(),
            forbidden_packages=("alghanem.kernel",),
        ),
    )
    assert not [
        name for name in reached.reached_modules if name.startswith("alghanem.kernel")
    ]


def test_no_refine_slot_operation_is_exported_by_this_deposit() -> None:
    exported = set(transition_module.__all__)
    assert not [name for name in exported if "refine" in name.lower()]
    assert not [name for name in exported if "split" in name.lower()]
    assert not hasattr(transition_module, "RefineSlot")


def test_there_are_five_named_residuals_all_distinct_and_non_blank() -> None:
    assert len(SYLLABLE_TRANSITION_NAMED_RESIDUALS) == 5
    assert len(set(SYLLABLE_TRANSITION_NAMED_RESIDUALS)) == 5
    assert all(note.strip() for note in SYLLABLE_TRANSITION_NAMED_RESIDUALS)


# --- الهدفُ مقيسٌ لا مُعلَن ----------------------------------------------------


def test_the_shape_is_measured_by_the_syllabifier() -> None:
    assert measured_syllable_shape("أَكَلَ") == "CV-CV-CV"
    assert measured_syllable_shape("أُمٌّ") == "CVC-CVC"


def test_an_empty_or_unsegmentable_host_is_a_named_refusal() -> None:
    with pytest.raises(SyllableTransitionError):
        measured_syllable_shape("   ")
    with pytest.raises(SyllableTransitionError):
        measured_syllable_shape("ـ")


def test_the_target_is_recomputed_and_not_stored_beside_the_case() -> None:
    hosted = HostedOccurrence(
        occurrence=_a_declared_occurrence(), host_note="بيانٌ مكتوب"
    )
    assert hosted.measured_shape == measured_syllable_shape(hosted.host_surface)
    assert hosted.host_surface == hosted.occurrence.surface


def test_a_host_without_a_written_note_is_refused() -> None:
    with pytest.raises(SyllableTransitionError):
        HostedOccurrence(occurrence=_a_declared_occurrence(), host_note=" ")


def test_an_object_outside_the_hamza_contract_may_not_enter() -> None:
    with pytest.raises(SyllableTransitionError):
        HostedOccurrence(occurrence="أ", host_note="بيان")  # type: ignore[arg-type]


# --- الهدفُ محجوبٌ عن السلّم ---------------------------------------------------


def test_the_target_is_not_among_the_recorded_fields() -> None:
    for item in THE_DECLARED_HOSTED_ITEMS:
        assert item.target.name == THE_SYLLABLE_SHAPE_TARGET
        assert THE_SYLLABLE_SHAPE_TARGET not in item.recorded_names


def test_the_hosted_ladder_never_cites_the_target() -> None:
    assert THE_SYLLABLE_SHAPE_TARGET not in THE_HOSTED_LADDER.cited_fields


def test_the_ladder_stops_below_the_ifada_layer() -> None:
    layers = {reading.layer for reading in THE_HOSTED_LADDER.readings}
    assert DisambiguationLayer.IFADA not in layers
    assert (
        THE_HOSTED_LADDER.highest_layer
        is DisambiguationLayer.SYLLABIC_AND_MORPHOLOGICAL_RELATIONS
    )


def test_every_declared_host_becomes_exactly_one_item() -> None:
    assert len(THE_DECLARED_HOSTED_ITEMS) == len(THE_DECLARED_HOSTS)
    identifiers = [item.item_id for item in THE_DECLARED_HOSTED_ITEMS]
    assert len(identifiers) == len(set(identifiers))


def test_the_original_measurement_is_recovered_at_the_bottom() -> None:
    report = run_ladder(THE_HOSTED_LADDER, THE_DECLARED_HOSTED_ITEMS)
    assert report.the_original_measurement_is_recoverable


# --- نتيجةُ الانتقال ----------------------------------------------------------


def test_the_ladder_merges_words_of_different_syllable_shapes() -> None:
    report = run_syllable_transition_experiment(
        a_lookup_reader(THE_HOSTED_LADDER, THE_DECLARED_HOSTED_ITEMS)
    )
    assert report.merged_targets
    by_id = {item.item_id: item for item in THE_DECLARED_HOSTED_ITEMS}
    for left, right in report.merged_targets:
        assert by_id[left].target.value != by_id[right].target.value
        for name in THE_HOSTED_LADDER.cited_fields:
            assert by_id[left].value_of(name) == by_id[right].value_of(name)


def test_the_refutation_precedes_the_reader() -> None:
    def _never(value: tuple[tuple[str, str], ...]) -> str:
        raise AssertionError("سُئل القارئُ بعد الدمج")

    report = run_syllable_transition_experiment(_never)
    assert report.reader_calls == 0
    assert not report.the_reader_was_consulted


def test_the_transition_to_the_syllable_is_not_established() -> None:
    assert not the_transition_to_the_syllable_is_established()


def test_no_reader_however_strong_lifts_the_merge() -> None:
    report = run_syllable_transition_experiment(
        a_lookup_reader(THE_HOSTED_LADDER, THE_DECLARED_HOSTED_ITEMS)
    )
    assert not report.the_ladder_determines_the_target
    assert not report.is_a_linguistic_rule


def test_the_report_names_the_measured_target() -> None:
    report = run_syllable_transition_experiment(
        a_lookup_reader(THE_HOSTED_LADDER, THE_DECLARED_HOSTED_ITEMS)
    )
    assert report.target_name == THE_SYLLABLE_SHAPE_TARGET
    assert report.distinct_values < len(THE_DECLARED_HOSTED_ITEMS)


# --- ولادةُ المقطع لا تُقضى ههنا ----------------------------------------------


def test_this_run_may_not_be_read_as_a_syllable_birth_claim() -> None:
    with pytest.raises(LayerOrderError):
        refuse_a_syllable_birth_claim_from_this_run()


def test_the_item_builder_is_reusable_on_a_single_host() -> None:
    hosted = HostedOccurrence(
        occurrence=_a_declared_occurrence(), host_note="بيانٌ مكتوب"
    )
    item = hosted_item(hosted)
    assert item.target.value == "CV-CV-CV"
    assert item.original_measurement == item.value_of("الحاملُ_المِرمازيّ")
