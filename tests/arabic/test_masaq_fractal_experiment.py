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
    HELD_OUT_READOUT_COLUMNS,
    MASAQ_PREREGISTRATION_CONTENT_ID,
    MASAQ_SUFFICIENCY_CONTRACT,
    MasaqExperimentError,
    build_frozen_binding,
    build_word_inputs,
    read_masaq_word_inputs,
    run_masaq_fractal_experiment,
)
from alghanem.fractal_experiment import (
    ExperimentalPermitState,
    ExperimentalStanding,
    FrozenExperimentBindingError,
)
from alghanem.fractal_generation import NextScaleSeed

_ROWS = (
    {
        "Sura_No": "1",
        "Verse_No": "1",
        "Column5": "w1",
        "Word_No": "1",
        "Segmented_Word": "بِ",
        MORPH_TAG_COLUMN: "P",
        "Syntactic_Role": "jar",
    },
    {
        "Sura_No": "1",
        "Verse_No": "1",
        "Column5": "w1",
        "Word_No": "2",
        "Segmented_Word": "سْمِ",
        MORPH_TAG_COLUMN: "N",
        "Syntactic_Role": "majrur",
    },
    {
        "Sura_No": "1",
        "Verse_No": "1",
        "Column5": "w2",
        "Word_No": "1",
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
    assert report.standings[ExperimentalStanding.OBSERVED_SUPPORT.value] == 1
    assert report.standings[ExperimentalStanding.UNDERPOWERED.value] == 1
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
