"""Tests for the UD Arabic Step-0 relation-layer census."""

from __future__ import annotations

from dataclasses import replace

import pytest

from alghanem.arabic.irab_corpus_witness import QURANIC_ARABIC_CORPUS_WITNESS
from alghanem.arabic.ud_relation_layer_step0 import (
    ARABIC_UD_CENSUSES,
    OBJ_VS_OBL_IS_PARTLY_CASE_DEFINED_NOTE,
    UD_ARABIC_NYUAD_TEST_CENSUS,
    UD_ARABIC_PADT_TRAIN_CENSUS,
    UD_ARABIC_PUD_TEST_CENSUS,
    UD_RELATION_LAYER_NAMED_RESIDUALS,
    UdRelationLayerCensus,
    UdRelationLayerCensusError,
    UdRelationLayerOutcome,
)


def test_outcome_vocabulary_is_closed_at_three_values() -> None:
    assert len(UdRelationLayerOutcome) == 3


def test_populated_columns_yield_present() -> None:
    assert UD_ARABIC_PUD_TEST_CENSUS.outcome is (
        UdRelationLayerOutcome.RELATION_LAYER_PRESENT
    )
    assert UD_ARABIC_PADT_TRAIN_CENSUS.outcome is (
        UdRelationLayerOutcome.RELATION_LAYER_PRESENT
    )


def test_withheld_surfaces_yield_licence_blocked_not_present() -> None:
    assert UD_ARABIC_NYUAD_TEST_CENSUS.form_bearing_tokens == 0
    assert UD_ARABIC_NYUAD_TEST_CENSUS.head_populated_tokens > 0
    assert UD_ARABIC_NYUAD_TEST_CENSUS.outcome is (
        UdRelationLayerOutcome.RELATION_LAYER_PRESENT_BUT_LICENCE_BLOCKED
    )


def test_absent_outcome_is_reachable() -> None:
    absent = replace(
        UD_ARABIC_PUD_TEST_CENSUS,
        head_populated_tokens=0,
        deprel_populated_tokens=0,
        obj_tokens=0,
        obl_tokens=0,
        nsubj_tokens=0,
        accusative_obj_tokens=0,
    )
    assert absent.outcome is UdRelationLayerOutcome.RELATION_LAYER_ABSENT


def test_relation_layer_is_complete_not_merely_declared() -> None:
    for census in ARABIC_UD_CENSUSES:
        assert census.relation_layer_is_complete, census.treebank


def test_case_alone_over_predicts_objecthood_in_every_measured_treebank() -> None:
    """The negative control: accusative is not objecthood, counted not assumed."""

    for census in ARABIC_UD_CENSUSES:
        assert census.accusative_tokens > census.accusative_obj_tokens, census.treebank
        assert census.non_obj_accusative_tokens > 0, census.treebank


def test_padt_train_accusative_over_prediction_is_more_than_fourfold() -> None:
    census = UD_ARABIC_PADT_TRAIN_CENSUS
    assert census.accusative_tokens == 23_002
    assert census.accusative_obj_tokens == 5_449
    assert census.accusative_tokens > 4 * census.accusative_obj_tokens


def test_obl_outnumbers_obj_where_both_are_annotated() -> None:
    assert UD_ARABIC_PUD_TEST_CENSUS.obl_tokens > UD_ARABIC_PUD_TEST_CENSUS.obj_tokens
    assert (
        UD_ARABIC_PADT_TRAIN_CENSUS.obl_tokens > UD_ARABIC_PADT_TRAIN_CENSUS.obj_tokens
    )


def test_obj_vs_obl_case_dependence_is_named_before_any_reader() -> None:
    assert "ObjVsOblIsPartlyCaseDefined" in UD_RELATION_LAYER_NAMED_RESIDUALS
    assert "obl" in OBJ_VS_OBL_IS_PARTLY_CASE_DEFINED_NOTE


def test_named_residuals_are_all_non_empty() -> None:
    assert len(UD_RELATION_LAYER_NAMED_RESIDUALS) == 8
    for name, note in UD_RELATION_LAYER_NAMED_RESIDUALS.items():
        assert name and note.strip()


def test_witnesses_are_independent_of_the_quranic_witness() -> None:
    for census in ARABIC_UD_CENSUSES:
        assert census.witness is not QURANIC_ARABIC_CORPUS_WITNESS
        assert census.witness.sha256 != QURANIC_ARABIC_CORPUS_WITNESS.sha256
        assert census.witness.corpus != QURANIC_ARABIC_CORPUS_WITNESS.corpus


def test_every_witness_names_a_licence_and_an_attribution_link() -> None:
    for census in ARABIC_UD_CENSUSES:
        assert census.witness.licenses
        assert census.witness.required_attribution_links


def test_witness_digests_are_distinct_per_file() -> None:
    digests = {census.witness.sha256 for census in ARABIC_UD_CENSUSES}
    assert len(digests) == len(ARABIC_UD_CENSUSES)


def test_census_requires_a_witness() -> None:
    with pytest.raises(UdRelationLayerCensusError):
        replace(UD_ARABIC_PUD_TEST_CENSUS, witness="ar_pud")  # type: ignore[arg-type]


def test_census_rejects_negative_counts() -> None:
    with pytest.raises(UdRelationLayerCensusError):
        replace(UD_ARABIC_PUD_TEST_CENSUS, obj_tokens=-1)


def test_census_rejects_a_part_larger_than_the_whole() -> None:
    with pytest.raises(UdRelationLayerCensusError):
        replace(UD_ARABIC_PUD_TEST_CENSUS, head_populated_tokens=20_748)


def test_census_rejects_more_accusative_objects_than_objects() -> None:
    with pytest.raises(UdRelationLayerCensusError):
        replace(UD_ARABIC_PUD_TEST_CENSUS, accusative_obj_tokens=1_000)


def test_census_rejects_an_empty_file() -> None:
    with pytest.raises(UdRelationLayerCensusError):
        replace(
            UD_ARABIC_PUD_TEST_CENSUS,
            tokens=0,
            head_populated_tokens=0,
            deprel_populated_tokens=0,
            form_bearing_tokens=0,
            obj_tokens=0,
            obl_tokens=0,
            nsubj_tokens=0,
            accusative_tokens=0,
            accusative_obj_tokens=0,
        )


def test_no_field_carries_a_result() -> None:
    forbidden = {"outcome", "verdict", "decision", "usable", "adopted", "accepted"}
    for field_name in UdRelationLayerCensus.__dataclass_fields__:
        assert not forbidden & set(field_name.split("_"))


def test_module_imports_nothing_from_the_kernel() -> None:
    from pathlib import Path

    source = Path("src/alghanem/arabic/ud_relation_layer_step0.py").read_text(
        encoding="utf-8"
    )
    for line in source.splitlines():
        if line.startswith(("import ", "from ")):
            assert "kernel" not in line
