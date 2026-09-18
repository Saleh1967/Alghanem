"""تشغيلُ MASAQ التجريبيّ: مدخلٌ مُجمَّدٌ بلا وَسْم، وشواهدُ بلا ترخيص.

    ALGHANEM_MASAQ_PATH → بايتاتٌ موثَّقة → تجريبٌ فراكتاليّ → شواهد

والوَسْمُ المُودَع لا ينزل في مدخل المُولِّد؛ وإن نزل رُفِض.

تسجيلٌ لا سلطة: لا ترخيصَ، ولا رتبةَ دائمة، ولا حكمَ كفاية.
"""

from __future__ import annotations

import pytest

from alghanem.arabic.masaq_corpus_deposit import (
    MORPH_TAG_COLUMN,
    masaq_bytes_are_resolvable,
)
from alghanem.arabic.masaq_fractal_experiment import (
    GENERATOR_VISIBLE_COLUMNS,
    HELD_OUT_MASAQ_COLUMN_ABSENT,
    HELD_OUT_READOUT_COLUMNS,
    LOCAL_SEGMENT_POSITION_FIELD,
    MASAQ_PREREGISTRATION_CONTENT_ID,
    MASAQ_SUFFICIENCY_CONTRACT,
    SEGMENT_INDEX_COLUMN,
    WEAKER_MODEL_TIES_FRACTAL_MODEL,
    MasaqExperimentError,
    StandingEvidence,
    build_frozen_binding,
    build_word_inputs,
    derive_standing,
    normalize_segment_surface,
    read_masaq_word_inputs,
    run_masaq_fractal_experiment,
)
from alghanem.fractal_experiment import (
    ExperimentalPermitState,
    ExperimentalStanding,
    FrozenExperimentBindingError,
)
from alghanem.fractal_generation import FractalResidualKind, NextScaleSeed

_ROWS = (
    {
        "Sura_No": "1",
        "Verse_No": "1",
        "Column5": "w1",
        "Word_No": "3",
        "Segmented_Word": "بِ",
        MORPH_TAG_COLUMN: "P",
        "Syntactic_Role": "jar",
    },
    {
        "Sura_No": "1",
        "Verse_No": "1",
        "Column5": "w1",
        "Word_No": "4",
        "Segmented_Word": "سْمِ",
        MORPH_TAG_COLUMN: "N",
        "Syntactic_Role": "majrur",
    },
    {
        "Sura_No": "1",
        "Verse_No": "1",
        "Column5": "w2",
        "Word_No": "5",
        "Segmented_Word": "ٱللَّهِ",
        MORPH_TAG_COLUMN: "PN",
        "Syntactic_Role": "mudaf_ilayh",
    },
)


def test_the_words_are_grouped_in_the_order_they_arrive() -> None:
    words = build_word_inputs(_ROWS)
    assert tuple(word.word_key for word in words) == ("w1", "w2")
    assert words[0].segments == ("ب", "سم")
    assert words[1].segments == ("ٱلله",)


def test_the_generator_sees_no_tag_column() -> None:
    words = build_word_inputs(_ROWS)
    projection = words[0].generator_projection()
    assert set(projection) <= set(GENERATOR_VISIBLE_COLUMNS)
    for column in HELD_OUT_READOUT_COLUMNS:
        assert column not in projection


def test_a_leaked_tag_in_the_generator_input_is_refused() -> None:
    words = build_word_inputs(_ROWS)
    binding = build_frozen_binding(
        words, binding_id="binding.test", source_id="source.test"
    )
    binding.refuse_held_out_fields(words[0].generator_projection())
    leaked = dict(words[0].generator_projection())
    leaked[MORPH_TAG_COLUMN] = "P"
    with pytest.raises(FrozenExperimentBindingError):
        binding.refuse_held_out_fields(leaked)


def test_the_frozen_word_still_carries_its_held_out_tags_for_readout() -> None:
    words = build_word_inputs(_ROWS)
    assert words[0].held_out_tags == ("P", "N")
    assert len(words[0].content_id) == 64


def test_an_empty_binding_is_refused() -> None:
    with pytest.raises(MasaqExperimentError):
        build_frozen_binding((), binding_id="binding.empty", source_id="source.test")


def test_a_synthetic_run_produces_witnesses_and_revokes_its_permit() -> None:
    words = build_word_inputs(_ROWS)
    report = run_masaq_fractal_experiment(words, run_id="run.test")
    assert report.final_permit_state is ExperimentalPermitState.REVOKED
    assert len(report.witnesses) == len(words)
    assert report.standings[ExperimentalStanding.OBSERVED_SUPPORT.value] == 0
    assert report.standings[ExperimentalStanding.UNDERPOWERED.value] == 2
    assert report.experimental_seed_ids
    assert report.bundle.preregistration_ref == MASAQ_PREREGISTRATION_CONTENT_ID


def test_the_run_is_reproducible_from_the_same_frozen_words() -> None:
    words = build_word_inputs(_ROWS)
    first = run_masaq_fractal_experiment(words, run_id="run.same")
    second = run_masaq_fractal_experiment(words, run_id="run.same")
    assert first.bundle.content_id == second.bundle.content_id


def test_the_run_yields_no_license_and_no_permanent_seed() -> None:
    words = build_word_inputs(_ROWS)
    report = run_masaq_fractal_experiment(words, run_id="run.test")
    for produced in (report.bundle, report.permit, *report.witnesses):
        assert not isinstance(produced, NextScaleSeed)
        for name in dir(produced):
            lowered = name.lower()
            assert "license" not in lowered
            assert "licence" not in lowered
            assert "verdict" not in lowered


def test_the_sufficiency_contract_precedes_any_measurement_of_it() -> None:
    assert len(MASAQ_SUFFICIENCY_CONTRACT.content_id) == 64
    assert MASAQ_SUFFICIENCY_CONTRACT.negative_controls
    for name in dir(MASAQ_SUFFICIENCY_CONTRACT):
        assert "assess" not in name.lower()
        assert "evaluate" not in name.lower()


@pytest.mark.skipif(
    not masaq_bytes_are_resolvable(),
    reason="بايتاتُ MASAQ ليست في هذه الشجرة ولا صُرِّح بمسارها",
)
def test_the_run_reads_the_deposited_bytes_when_they_are_there() -> None:
    words = read_masaq_word_inputs(limit=40)
    assert words
    report = run_masaq_fractal_experiment(words, run_id="run.masaq.real")
    assert report.final_permit_state is ExperimentalPermitState.REVOKED
    assert len(report.witnesses) == len(words)
    assert report.standings[ExperimentalStanding.RUN_FAILURE.value] == 0
    for witness in report.witnesses:
        assert witness.preregistration_content_id == MASAQ_PREREGISTRATION_CONTENT_ID
        assert witness.permit_content_id == report.permit.content_id


def test_a_tying_weaker_model_blocks_structural_support() -> None:
    words = build_word_inputs(_ROWS)
    report = run_masaq_fractal_experiment(words, run_id="run.tie")
    assert report.weaker_model_observations
    assert all(observation.ties for observation in report.weaker_model_observations)
    tied = report.witnesses[0]
    assert tied.standing is ExperimentalStanding.UNDERPOWERED
    assert any(
        WEAKER_MODEL_TIES_FRACTAL_MODEL in residual.reason
        for residual in tied.residuals
    )


def test_the_standing_law_refuses_support_on_closure_and_reconstruction_alone() -> None:
    tied = StandingEvidence(
        reconstruction_passed=True,
        closure_passed=True,
        negative_controls_behave_as_preregistered=True,
        weaker_model_ties=True,
        blocking_residual_present=False,
    )
    assert derive_standing(tied) is ExperimentalStanding.UNDERPOWERED
    discriminating = StandingEvidence(
        reconstruction_passed=True,
        closure_passed=True,
        negative_controls_behave_as_preregistered=True,
        weaker_model_ties=False,
        blocking_residual_present=False,
    )
    assert derive_standing(discriminating) is ExperimentalStanding.OBSERVED_SUPPORT
    refuted = StandingEvidence(
        reconstruction_passed=False,
        closure_passed=True,
        negative_controls_behave_as_preregistered=True,
        weaker_model_ties=False,
        blocking_residual_present=False,
    )
    assert derive_standing(refuted) is ExperimentalStanding.OBSERVED_REFUTATION
    failed = StandingEvidence(
        reconstruction_passed=True,
        closure_passed=True,
        negative_controls_behave_as_preregistered=True,
        weaker_model_ties=False,
        blocking_residual_present=False,
        run_failed=True,
    )
    assert derive_standing(failed) is ExperimentalStanding.RUN_FAILURE


def test_irreducibility_is_not_authored_merely_because_a_word_has_segments() -> None:
    words = build_word_inputs(_ROWS)
    report = run_masaq_fractal_experiment(words, run_id="run.irreducible")
    for witness in report.witnesses:
        for residual in witness.residuals:
            assert residual.kind is not FractalResidualKind.IRREDUCIBLE_AT_CURRENT_SCALE
    for residual in report.bundle.residual_union:
        assert residual.kind is not FractalResidualKind.IRREDUCIBLE_AT_CURRENT_SCALE


def test_the_source_word_no_survives_and_the_local_position_is_separate() -> None:
    words = build_word_inputs(_ROWS)
    assert words[0].source_word_numbers == ("3", "4")
    assert words[0].local_segment_positions == (0, 1)
    projection = words[0].generator_projection()
    assert projection[SEGMENT_INDEX_COLUMN] == ("3", "4")
    assert LOCAL_SEGMENT_POSITION_FIELD not in projection


def test_the_raw_surface_survives_its_normalization_with_a_replayable_trace() -> None:
    words = build_word_inputs(_ROWS)
    occurrence = words[0].occurrences[0]
    assert occurrence.raw_segment_surface == "بِ"
    assert occurrence.normalized_segment_surface == "ب"
    assert occurrence.normalization.replay() == occurrence.normalized_segment_surface
    assert occurrence.normalization.removed == ((1, "ِ"),)
    trace = normalize_segment_surface("سْمِ")
    assert trace.raw == "سْمِ"
    assert trace.replay() == trace.normalized == "سم"


def test_all_five_held_out_columns_are_frozen_and_absent_from_the_projection() -> None:
    words = build_word_inputs(_ROWS)
    held_out = words[0].occurrences[0].held_out
    assert tuple(name for name, _ in held_out.values) == HELD_OUT_READOUT_COLUMNS
    assert held_out.value_of(MORPH_TAG_COLUMN) == "P"
    assert held_out.value_of("Syntactic_Role") == "jar"
    assert held_out.value_of("Lemma") == HELD_OUT_MASAQ_COLUMN_ABSENT
    projection = words[0].generator_projection()
    for column in HELD_OUT_READOUT_COLUMNS:
        assert column not in projection
    content = words[0].as_canonical_content()
    frozen = content["occurrences"]
    assert isinstance(frozen, list)
    assert frozen[0]["held_out"][MORPH_TAG_COLUMN] == "P"


def test_the_negative_controls_run_through_the_declared_path() -> None:
    words = build_word_inputs(_ROWS)
    report = run_masaq_fractal_experiment(words, run_id="run.controls")
    transformations = {control.transformation for control in report.negative_controls}
    assert transformations == {"reversed_order", "dropped_segment"}
    for control in report.negative_controls:
        assert len(control.control_input_content_id) == 64
        assert control.output != control.reference_output
        assert control.discriminates
    controlled = report.witnesses[0]
    assert len(controlled.negative_control_observations) == 2


def test_an_experimental_seed_is_issued_while_the_standing_is_underpowered() -> None:
    words = build_word_inputs(_ROWS)
    report = run_masaq_fractal_experiment(words, run_id="run.lift")
    assert report.witnesses[0].standing is ExperimentalStanding.UNDERPOWERED
    assert report.experimental_seed_ids
    assert all(
        seed_id.startswith("experimental-seed.")
        for seed_id in report.experimental_seed_ids
    )
