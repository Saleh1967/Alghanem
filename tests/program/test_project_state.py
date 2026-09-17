"""Tests for the derived project state and its projection into `docs/VISION.md`."""

from __future__ import annotations

import ast
from dataclasses import FrozenInstanceError, replace
from pathlib import Path

import pytest

from alghanem.program import (
    A_DECLARED_STATUS_IS_READ_NOT_VERIFIED,
    A_MODULE_COUNT_IS_NOT_A_CAPABILITY,
    A_TEST_FUNCTION_COUNT_IS_NOT_A_PASSING_SUITE,
    AN_ABSENT_CORPUS_IS_NOT_A_REFUTED_ONE,
    NO_LINGUISTIC_FIGURE_IS_DERIVED_HERE,
    PROJECT_STATE_AUTHORITY_NOTE,
    PROJECT_STATE_NAMED_RESIDUALS,
    RENDERED_BLOCK_IS_NOT_EDITED_BY_HAND,
    STATE_BLOCK_BEGIN_MARKER,
    STATE_BLOCK_END_MARKER,
    VISION_RELATIVE_PATH,
    CorpusReadiness,
    DeclaredLawStatus,
    LawEnforcementGenus,
    LawStatusCensus,
    ProjectState,
    ProjectStateError,
    SourceTreeCensus,
    derive_project_state,
    read_document_state_block,
    render_state_block,
    vision_document_path,
)
from alghanem.program.project_state import _genus_of, repository_root_path


@pytest.fixture(scope="module")
def state() -> ProjectState:
    return derive_project_state()


def test_every_declared_status_has_a_genus() -> None:
    for status in DeclaredLawStatus:
        assert isinstance(_genus_of(status), LawEnforcementGenus)


def test_enforced_statuses_map_to_the_gate_genus() -> None:
    for status in DeclaredLawStatus:
        if status.name.startswith("ENFORCED"):
            assert _genus_of(status) is LawEnforcementGenus.ENFORCED_AT_A_NAMED_GATE


def test_genus_counts_partition_the_read_rows(state: ProjectState) -> None:
    counts = state.laws.counts_by_genus
    assert set(counts) == set(LawEnforcementGenus)
    assert sum(counts.values()) == state.laws.law_count


def test_enforcement_surface_count_is_bounded_by_the_gate_genus(
    state: ProjectState,
) -> None:
    gate_rows = state.laws.counts_by_genus[LawEnforcementGenus.ENFORCED_AT_A_NAMED_GATE]
    assert 0 < state.laws.enforcement_surface_count <= gate_rows


def test_counts_are_properties_not_written_fields(state: ProjectState) -> None:
    for owner in (state.laws, state.tree):
        for name in type(owner).__dataclass_fields__:
            assert not name.endswith("_count") or name == "test_function_count"
    assert state.laws.law_count > 0
    assert state.tree.source_module_count > 0


def test_state_is_frozen(state: ProjectState) -> None:
    with pytest.raises(FrozenInstanceError):
        state.declared_aim_count = 0  # type: ignore[misc]


def test_negative_or_boolean_scalars_are_refused(state: ProjectState) -> None:
    with pytest.raises(ProjectStateError):
        replace(state, declared_aim_count=-1)
    with pytest.raises(ProjectStateError):
        replace(state, unverified_figure_count=True)
    with pytest.raises(ProjectStateError):
        replace(state, corpus_readiness="مُتاحة")  # type: ignore[arg-type]


def test_census_refuses_unordered_duplicated_or_witnessless_trees() -> None:
    with pytest.raises(ProjectStateError):
        SourceTreeCensus(
            source_modules=("b.py", "a.py"),
            test_modules=("tests/test_a.py",),
            test_function_count=1,
        )
    with pytest.raises(ProjectStateError):
        SourceTreeCensus(
            source_modules=("a.py", "a.py"),
            test_modules=("tests/test_a.py",),
            test_function_count=1,
        )
    with pytest.raises(ProjectStateError):
        SourceTreeCensus(
            source_modules=("a.py",),
            test_modules=("tests/test_a.py", "tests/test_b.py"),
            test_function_count=1,
        )


def test_law_census_refuses_a_non_ledger() -> None:
    with pytest.raises(ProjectStateError):
        LawStatusCensus(ledger="146")  # type: ignore[arg-type]


def test_derivation_reads_a_missing_tree_as_a_refusal(tmp_path: Path) -> None:
    with pytest.raises(ProjectStateError):
        derive_project_state(tmp_path)


def test_corpus_readiness_is_a_closed_pair(state: ProjectState) -> None:
    assert state.corpus_readiness in set(CorpusReadiness)
    assert len(CorpusReadiness) == 2


def test_render_refuses_text_in_place_of_state() -> None:
    with pytest.raises(ProjectStateError):
        render_state_block("١٤٦ قانونًا")  # type: ignore[arg-type]


def test_rendered_block_is_delimited_and_deterministic(state: ProjectState) -> None:
    first = render_state_block(state)
    assert first == render_state_block(state)
    assert first.startswith(STATE_BLOCK_BEGIN_MARKER)
    assert first.endswith(STATE_BLOCK_END_MARKER)
    assert str(state.laws.law_count) in first
    assert state.corpus_readiness.value in first


def test_rendered_block_names_every_residual(state: ProjectState) -> None:
    block = render_state_block(state)
    for residual in (
        A_DECLARED_STATUS_IS_READ_NOT_VERIFIED,
        A_MODULE_COUNT_IS_NOT_A_CAPABILITY,
        A_TEST_FUNCTION_COUNT_IS_NOT_A_PASSING_SUITE,
        NO_LINGUISTIC_FIGURE_IS_DERIVED_HERE,
        AN_ABSENT_CORPUS_IS_NOT_A_REFUTED_ONE,
    ):
        assert residual in block


def test_named_residuals_are_described_and_immutable() -> None:
    for name, prose in PROJECT_STATE_NAMED_RESIDUALS.items():
        assert name == name.upper()
        assert prose.strip() and len(prose) > 40
    assert RENDERED_BLOCK_IS_NOT_EDITED_BY_HAND in PROJECT_STATE_NAMED_RESIDUALS
    with pytest.raises(TypeError):
        PROJECT_STATE_NAMED_RESIDUALS["x"] = "y"  # type: ignore[index]


def test_block_reader_refuses_missing_or_repeated_markers(state: ProjectState) -> None:
    block = render_state_block(state)
    with pytest.raises(ProjectStateError):
        read_document_state_block("   ")
    with pytest.raises(ProjectStateError):
        read_document_state_block("نصٌّ بلا علامات")
    with pytest.raises(ProjectStateError):
        read_document_state_block(block + "\n" + block)


def test_vision_document_carries_the_rendered_block_verbatim(
    state: ProjectState,
) -> None:
    document = vision_document_path().read_text(encoding="utf-8")
    assert read_document_state_block(document) == render_state_block(state)


def test_vision_thesis_carries_no_figure_of_its_own() -> None:
    document = vision_document_path().read_text(encoding="utf-8")
    thesis = document[: document.index(STATE_BLOCK_BEGIN_MARKER)]
    assert not any(character in "0123456789" for character in thesis)


def test_vision_document_is_named_where_the_module_says() -> None:
    assert vision_document_path() == repository_root_path() / VISION_RELATIVE_PATH
    assert VISION_RELATIVE_PATH == "docs/VISION.md"


def test_readme_points_at_the_vision_document() -> None:
    readme = (repository_root_path() / "README.md").read_text(encoding="utf-8")
    assert VISION_RELATIVE_PATH in readme


def test_no_unverified_figure_is_presented_as_an_achievement(
    state: ProjectState,
) -> None:
    from alghanem.program import REPORTED_UNVERIFIED_FIGURES

    document = vision_document_path().read_text(encoding="utf-8")
    for record in REPORTED_UNVERIFIED_FIGURES:
        assert record.figure_text not in document
    assert state.unverified_figure_count == len(REPORTED_UNVERIFIED_FIGURES)


def test_module_is_authority_inert_and_reads_no_kernel() -> None:
    assert "لا تُصدِر" in PROJECT_STATE_AUTHORITY_NOTE
    source = (
        repository_root_path() / "src" / "alghanem" / "program" / "project_state.py"
    ).read_text(encoding="utf-8")
    tree = ast.parse(source)
    for node in ast.walk(tree):
        if isinstance(node, ast.ImportFrom):
            assert "kernel" not in (node.module or "")
        if isinstance(node, ast.Import):
            for alias in node.names:
                assert "kernel" not in alias.name
