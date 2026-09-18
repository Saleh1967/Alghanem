"""`G0.CASE-0.MATRIX` تُقرَأ مطلبًا لا وصفًا: تغطيةٌ تامّة، وامتناعٌ مُعلَّل.

وهذه الاختباراتُ لا تُشغِّل المحرّكَ ولا تحكم على قضيّة؛ إنّما تُحاسِب المصفوفةَ
على شرطها هي: أن تُسمّي المطلوبَ قبل الحالات، وألّا تُسمّي حالةً ولا بصمةَ تنفيذ.

تسجيلٌ لا سلطة: لا ولادةَ ولا حكمَ ولادةٍ ولا تجميدَ `E0`.
"""

from __future__ import annotations

import ast
from dataclasses import replace
from pathlib import Path

import pytest

from alghanem.execution.coverage import (
    COVERAGE_MATRIX,
    COVERAGE_MATRIX_DIGEST,
    COVERAGE_MATRIX_ID,
    EVALUATION_SCOPE_OF_LAW,
    CaseDisposition,
    CoverageAxis,
    CoverageMatrix,
    CoverageMatrixError,
    CoverageRequirement,
    EvaluationScope,
    VerdictEffect,
)
from alghanem.execution.laws import aggregate_outcome
from alghanem.execution.lawset import LAW_SET, ExecutionLaw
from alghanem.execution.outcome import (
    CheckStanding,
    ExecutionOutcome,
    Identity,
    LawCheckEntry,
)

_SOURCE_ROOT = Path(__file__).resolve().parents[2] / "src" / "alghanem"

_VERDICT_EFFECT_OF_STANDING = {
    CheckStanding.SATISFIED: VerdictEffect.NO_VERDICT_EFFECT,
    CheckStanding.VIOLATED: VerdictEffect.FORCES_BLOCK,
    CheckStanding.UNRESOLVED: VerdictEffect.FORCES_DEFER_UNLESS_BLOCKED,
    CheckStanding.NOT_EVALUATED_BY_PREREQUISITE: VerdictEffect.NO_VERDICT_EFFECT,
    CheckStanding.NOT_APPLICABLE_NO_CLAIM: VerdictEffect.NO_VERDICT_EFFECT,
}


def _entry(
    law: ExecutionLaw, standing: CheckStanding, subject_id: str
) -> LawCheckEntry:
    blocked = standing is CheckStanding.NOT_EVALUATED_BY_PREREQUISITE
    return LawCheckEntry(
        law=law.value,
        standing=standing,
        subject_id=subject_id,
        expected=None
        if standing is CheckStanding.NOT_APPLICABLE_NO_CLAIM
        else Identity(id=subject_id, content_id="content"),
        observed=None,
        blocked_by=ExecutionLaw.EXISTENCE_LINEAGE_REDERIVES.value if blocked else None,
    )


def _law_standing_cells() -> tuple[CoverageRequirement, ...]:
    return COVERAGE_MATRIX.of_axis(CoverageAxis.LAW_STANDING)


def test_every_law_is_read_in_every_standing_exactly_once() -> None:
    seen: set[tuple[ExecutionLaw, CheckStanding]] = set()
    for cell in _law_standing_cells():
        assert cell.law is not None and cell.target_standing is not None
        key = (cell.law, cell.target_standing)
        assert key not in seen, key
        seen.add(key)
    assert seen == {(law, standing) for law in LAW_SET for standing in CheckStanding}
    assert len(seen) == len(LAW_SET) * len(CheckStanding)


def test_the_matrix_names_no_case_and_carries_unique_identifiers() -> None:
    identifiers = [item.requirement_id for item in COVERAGE_MATRIX.requirements]
    assert len(identifiers) == len(set(identifiers))
    for item in COVERAGE_MATRIX.requirements:
        assert item.case_id is None


def test_a_required_cell_is_reachable_and_an_unreachable_cell_is_justified() -> None:
    for item in COVERAGE_MATRIX.requirements:
        if item.reachable:
            assert item.justification_if_unreachable is None
        else:
            assert item.required is False
            assert item.justification_if_unreachable
            assert item.verdict_effect is None
            assert item.expected_disposition is None
            assert item.prerequisite_laws == ()
            assert item.forbidden_co_standings == ()


def test_a_reachable_law_standing_cell_forbids_every_other_standing() -> None:
    for cell in _law_standing_cells():
        if not cell.reachable:
            continue
        assert set(cell.forbidden_co_standings) == {
            standing
            for standing in CheckStanding
            if standing is not cell.target_standing
        }


def test_a_standing_declares_its_effect_on_the_verdict_not_the_verdict() -> None:
    for cell in _law_standing_cells():
        assert cell.expected_disposition is None, cell.requirement_id
        if not cell.reachable:
            continue
        assert cell.target_standing is not None
        assert cell.verdict_effect is _VERDICT_EFFECT_OF_STANDING[cell.target_standing]


def test_a_satisfied_law_does_not_force_a_passing_case() -> None:
    cell = COVERAGE_MATRIX.cell(
        ExecutionLaw.ANCHORS_DO_NOT_EXCEED_ARITY, CheckStanding.SATISFIED
    )
    assert cell is not None
    assert cell.verdict_effect is VerdictEffect.NO_VERDICT_EFFECT
    assert cell.expected_disposition is None
    trace = (
        _entry(
            ExecutionLaw.ANCHORS_DO_NOT_EXCEED_ARITY,
            CheckStanding.SATISFIED,
            "nisbah-1",
        ),
        _entry(
            ExecutionLaw.ROLE_LICENSE_IS_OPERATIVE,
            CheckStanding.VIOLATED,
            "role-1",
        ),
    )
    assert aggregate_outcome(trace) is ExecutionOutcome.BLOCK


def test_an_unresolved_law_does_not_defer_a_case_that_holds_a_violation() -> None:
    cell = COVERAGE_MATRIX.cell(
        ExecutionLaw.EXISTENCE_LINEAGE_REDERIVES, CheckStanding.UNRESOLVED
    )
    assert cell is not None
    assert cell.verdict_effect is VerdictEffect.FORCES_DEFER_UNLESS_BLOCKED
    unresolved = _entry(
        ExecutionLaw.EXISTENCE_LINEAGE_REDERIVES,
        CheckStanding.UNRESOLVED,
        "ontology-1",
    )
    assert aggregate_outcome((unresolved,)) is ExecutionOutcome.DEFER
    violated = _entry(
        ExecutionLaw.ROLE_LICENSE_IS_OPERATIVE, CheckStanding.VIOLATED, "role-1"
    )
    assert aggregate_outcome((unresolved, violated)) is ExecutionOutcome.BLOCK
    assert aggregate_outcome((violated, unresolved)) is ExecutionOutcome.BLOCK


def test_a_violation_alone_forces_a_block_whatever_the_other_standings_are() -> None:
    violated = _entry(
        ExecutionLaw.ROLE_LICENSE_IS_OPERATIVE, CheckStanding.VIOLATED, "role-1"
    )
    for standing in CheckStanding:
        if standing is CheckStanding.VIOLATED:
            continue
        other = _entry(
            ExecutionLaw.DECLARED_LINGUISTIC_IDENTITY_AGREES, standing, "ontology-1"
        )
        assert aggregate_outcome((other, violated)) is ExecutionOutcome.BLOCK, standing
        cell = COVERAGE_MATRIX.cell(
            ExecutionLaw.DECLARED_LINGUISTIC_IDENTITY_AGREES, standing
        )
        assert cell is not None
        if cell.reachable:
            assert cell.verdict_effect is not VerdictEffect.FORCES_BLOCK


def test_every_law_carries_the_frozen_scope_its_judgement_is_borne_on() -> None:
    assert set(EVALUATION_SCOPE_OF_LAW) == set(LAW_SET)
    for cell in _law_standing_cells():
        assert cell.law is not None
        assert cell.evaluation_scope is EVALUATION_SCOPE_OF_LAW[cell.law]
    assert (
        EVALUATION_SCOPE_OF_LAW[ExecutionLaw.ROLE_LICENSE_IS_OPERATIVE]
        is EvaluationScope.SUBJECT
    )
    assert (
        EVALUATION_SCOPE_OF_LAW[ExecutionLaw.PREDICATE_ARITY_MATCHES_ITS_SLOTS]
        is EvaluationScope.CASE
    )
    assert (
        EVALUATION_SCOPE_OF_LAW[ExecutionLaw.MATERIALIZED_IDENTITY_AGREES]
        is EvaluationScope.CASE
    )


def test_a_cell_may_not_redefine_the_scope_its_law_is_judged_on() -> None:
    cell = COVERAGE_MATRIX.cell(
        ExecutionLaw.ROLE_LICENSE_IS_OPERATIVE, CheckStanding.SATISFIED
    )
    assert cell is not None
    with pytest.raises(CoverageMatrixError):
        replace(cell, evaluation_scope=EvaluationScope.CASE)


def test_a_first_axis_cell_that_claims_a_case_disposition_is_refused() -> None:
    cell = COVERAGE_MATRIX.cell(
        ExecutionLaw.ANCHORS_DO_NOT_EXCEED_ARITY, CheckStanding.SATISFIED
    )
    assert cell is not None
    with pytest.raises(CoverageMatrixError):
        replace(cell, expected_disposition=CaseDisposition.PASS)


def test_a_whole_case_requirement_carries_no_verdict_effect() -> None:
    witness = COVERAGE_MATRIX.of_axis(CoverageAxis.OUTCOME_REACHABILITY)[0]
    assert witness.verdict_effect is None
    with pytest.raises(CoverageMatrixError):
        replace(witness, verdict_effect=VerdictEffect.FORCES_BLOCK)


def test_a_prohibition_on_a_subject_scoped_law_binds_that_subject_alone() -> None:
    law = ExecutionLaw.CONDITION_SITES_ARE_LICENSED_FOR_USE
    assert EVALUATION_SCOPE_OF_LAW[law] is EvaluationScope.SUBJECT
    satisfied = COVERAGE_MATRIX.cell(law, CheckStanding.SATISFIED)
    assert satisfied is not None
    assert satisfied.evaluation_scope is EvaluationScope.SUBJECT
    assert CheckStanding.VIOLATED in satisfied.forbidden_co_standings
    on_a = _entry(law, CheckStanding.SATISFIED, "site-A")
    on_b = _entry(law, CheckStanding.VIOLATED, "site-B")
    assert {(on_a.law, on_a.subject_id), (on_b.law, on_b.subject_id)} == {
        (law.value, "site-A"),
        (law.value, "site-B"),
    }
    assert aggregate_outcome((on_a, on_b)) is ExecutionOutcome.BLOCK
    same_subject = _entry(law, CheckStanding.VIOLATED, "site-A")
    assert (on_a.law, on_a.subject_id) == (same_subject.law, same_subject.subject_id)
    assert same_subject.standing in satisfied.forbidden_co_standings


def test_prerequisite_laws_are_named_only_where_a_prior_law_blocks() -> None:
    for cell in _law_standing_cells():
        if cell.prerequisite_laws:
            assert (
                cell.target_standing is CheckStanding.NOT_EVALUATED_BY_PREREQUISITE
            ), cell.requirement_id
        for law in cell.prerequisite_laws:
            assert law in LAW_SET
            assert law is not cell.law
            assert LAW_SET.index(law) < LAW_SET.index(cell.law)
        if (
            cell.reachable
            and cell.target_standing is CheckStanding.NOT_EVALUATED_BY_PREREQUISITE
        ):
            assert cell.prerequisite_laws, cell.requirement_id


def test_an_unread_condition_and_a_nisbah_identity_are_refused_with_reasons() -> None:
    unread = COVERAGE_MATRIX.cell(
        ExecutionLaw.NO_UNREAD_CONDITION_IN_THE_FOUNDING_BASE,
        CheckStanding.VIOLATED,
    )
    assert unread is not None and unread.reachable is False
    identity = COVERAGE_MATRIX.cell(
        ExecutionLaw.MATERIALIZED_IDENTITY_AGREES, CheckStanding.UNRESOLVED
    )
    assert identity is not None and identity.reachable is False
    materialized_violated = COVERAGE_MATRIX.cell(
        ExecutionLaw.MATERIALIZED_IDENTITY_AGREES, CheckStanding.VIOLATED
    )
    assert materialized_violated is not None
    assert materialized_violated.reachable is True
    assert materialized_violated.verdict_effect is VerdictEffect.FORCES_BLOCK


def test_every_outcome_including_the_internal_failure_has_a_reachability_witness() -> (
    None
):
    axis = COVERAGE_MATRIX.of_axis(CoverageAxis.OUTCOME_REACHABILITY)
    assert {item.expected_disposition for item in axis} == {
        CaseDisposition.PASS,
        CaseDisposition.BLOCK,
        CaseDisposition.DEFER,
        CaseDisposition.INVALID_INPUT,
        CaseDisposition.INVARIANT_ERROR,
    }
    for item in axis:
        assert item.required is True
        assert item.claim


def test_the_separations_between_the_stages_are_named_in_the_third_axis() -> None:
    axis = COVERAGE_MATRIX.of_axis(CoverageAxis.CROSS_STAGE_SEPARATION)
    assert {item.requirement_id for item in axis} == {
        "XS.invalid_input_has_no_envelope",
        "XS.block_has_no_materialized_identity",
        "XS.defer_has_no_materialized_identity",
        "XS.pass_has_a_materialized_identity",
        "XS.invariant_error_has_no_verdict_and_no_envelope",
        "XS.blocked_dependent_has_no_residual",
        "XS.no_claim_is_not_read_as_satisfied",
    }


def test_a_separation_that_binds_no_case_verdict_constrains_none() -> None:
    axis = {
        item.requirement_id: item
        for item in COVERAGE_MATRIX.of_axis(CoverageAxis.CROSS_STAGE_SEPARATION)
    }
    blocked = axis["XS.blocked_dependent_has_no_residual"]
    assert blocked.expected_disposition is None
    assert blocked.evaluation_scope is EvaluationScope.SUBJECT
    no_claim = axis["XS.no_claim_is_not_read_as_satisfied"]
    assert no_claim.expected_disposition is None
    assert no_claim.evaluation_scope is EvaluationScope.SUBJECT
    assert no_claim.forbidden_co_standings == (CheckStanding.SATISFIED,)
    for identifier in (
        "XS.block_has_no_materialized_identity",
        "XS.defer_has_no_materialized_identity",
        "XS.pass_has_a_materialized_identity",
    ):
        assert axis[identifier].expected_disposition is not None
        assert axis[identifier].evaluation_scope is EvaluationScope.CASE


def test_the_three_axes_exhaust_the_matrix() -> None:
    counted = sum(len(COVERAGE_MATRIX.of_axis(axis)) for axis in CoverageAxis)
    assert counted == len(COVERAGE_MATRIX.requirements)


def test_a_cell_that_names_a_case_is_refused() -> None:
    with pytest.raises(CoverageMatrixError):
        CoverageRequirement(
            requirement_id="LS.forged",
            axis=CoverageAxis.LAW_STANDING,
            law=ExecutionLaw.ANCHORS_DO_NOT_EXCEED_ARITY,
            target_standing=CheckStanding.SATISFIED,
            claim=None,
            required=True,
            reachable=True,
            evaluation_scope=EvaluationScope.CASE,
            prerequisite_laws=(),
            forbidden_co_standings=(),
            verdict_effect=VerdictEffect.NO_VERDICT_EFFECT,
            expected_disposition=None,
            case_id="case-0001",  # type: ignore[arg-type]
            justification_if_unreachable=None,
        )


def test_an_unreachable_cell_that_is_required_is_refused() -> None:
    refused = COVERAGE_MATRIX.cell(
        ExecutionLaw.MATERIALIZED_IDENTITY_AGREES, CheckStanding.UNRESOLVED
    )
    assert refused is not None
    with pytest.raises(CoverageMatrixError):
        replace(refused, required=True)


def test_an_unreachable_cell_without_a_justification_is_refused() -> None:
    refused = COVERAGE_MATRIX.cell(
        ExecutionLaw.MATERIALIZED_IDENTITY_AGREES, CheckStanding.UNRESOLVED
    )
    assert refused is not None
    with pytest.raises(CoverageMatrixError):
        replace(refused, justification_if_unreachable="   ")


def test_a_law_is_not_a_prerequisite_of_itself() -> None:
    cell = COVERAGE_MATRIX.cell(
        ExecutionLaw.ROLE_LICENSE_IS_OPERATIVE,
        CheckStanding.NOT_EVALUATED_BY_PREREQUISITE,
    )
    assert cell is not None
    with pytest.raises(CoverageMatrixError):
        replace(
            cell,
            prerequisite_laws=cell.prerequisite_laws
            + (ExecutionLaw.ROLE_LICENSE_IS_OPERATIVE,),
        )


def test_a_standing_is_not_forbidden_alongside_itself() -> None:
    cell = COVERAGE_MATRIX.cell(
        ExecutionLaw.ANCHORS_DO_NOT_EXCEED_ARITY, CheckStanding.VIOLATED
    )
    assert cell is not None
    with pytest.raises(CoverageMatrixError):
        replace(cell, forbidden_co_standings=(CheckStanding.VIOLATED,))


def test_a_first_axis_cell_that_repeats_itself_in_prose_is_refused() -> None:
    cell = COVERAGE_MATRIX.cell(
        ExecutionLaw.ANCHORS_DO_NOT_EXCEED_ARITY, CheckStanding.VIOLATED
    )
    assert cell is not None
    with pytest.raises(CoverageMatrixError):
        replace(cell, claim="خرقٌ ظاهر")


def test_a_later_axis_requirement_is_not_a_law_in_a_standing() -> None:
    witness = COVERAGE_MATRIX.of_axis(CoverageAxis.OUTCOME_REACHABILITY)[0]
    with pytest.raises(CoverageMatrixError):
        replace(witness, law=ExecutionLaw.ANCHORS_DO_NOT_EXCEED_ARITY)
    with pytest.raises(CoverageMatrixError):
        replace(witness, claim="")


def test_a_repeated_identifier_hides_a_requirement() -> None:
    first = COVERAGE_MATRIX.requirements[0]
    with pytest.raises(CoverageMatrixError):
        CoverageMatrix(matrix_id=COVERAGE_MATRIX_ID, requirements=(first, first))


def test_an_empty_matrix_is_not_a_standard() -> None:
    with pytest.raises(CoverageMatrixError):
        CoverageMatrix(matrix_id=COVERAGE_MATRIX_ID, requirements=())


def test_the_digest_moves_when_a_requirement_moves() -> None:
    assert COVERAGE_MATRIX_DIGEST
    reordered = CoverageMatrix(
        matrix_id=COVERAGE_MATRIX_ID,
        requirements=tuple(reversed(COVERAGE_MATRIX.requirements)),
    )
    assert reordered.as_canonical_content() != COVERAGE_MATRIX.as_canonical_content()


def test_the_matrix_is_read_by_no_engine_module() -> None:
    for path in sorted((_SOURCE_ROOT / "execution").glob("*.py")):
        if path.name in {"coverage.py", "__init__.py"}:
            continue
        tree = ast.parse(path.read_text(encoding="utf-8"))
        for node in ast.walk(tree):
            if isinstance(node, ast.ImportFrom):
                assert node.module != "coverage", path.name
            elif isinstance(node, ast.Import):
                for alias in node.names:
                    assert "coverage" not in alias.name.split("."), path.name
