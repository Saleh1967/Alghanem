import pytest

from alghanem.canonical_content import canonical_bytes, canonical_digest
from alghanem.metaalgebra.standing import (
    DualStanding,
    EmpiricalStanding,
    ImplementationConformanceRecord,
    MetaAlgebraStandingError,
    SpecificationIndependenceGrade,
    SpecificationSetRef,
    StructuralStanding,
)


def sigma(sigma_id: str = "sigma-meta") -> SpecificationSetRef:
    return SpecificationSetRef(
        sigma_id=sigma_id,
        content_id=canonical_digest(canonical_bytes({"sigma": sigma_id})),
        scope="الميتا-جبر العامّ",
    )


def test_specification_ref_refuses_a_non_canonical_digest() -> None:
    with pytest.raises(MetaAlgebraStandingError):
        SpecificationSetRef(
            sigma_id="sigma",
            content_id="not-a-digest",
            scope="نطاق",
        )


def test_proved_relative_to_sigma_with_missing_target_is_admissible() -> None:
    standing = DualStanding(
        structural=StructuralStanding.STRUCTURALLY_PROVED_RELATIVE_TO_SIGMA,
        empirical=EmpiricalStanding.INDEPENDENT_TARGET_MISSING,
        specification=sigma(),
        independence_grade=(
            SpecificationIndependenceGrade.PROSPECTIVE_SPECIFICATION_INDEPENDENT
        ),
        reason="المحوران مستقلّان",
    )

    assert (
        standing.structural is StructuralStanding.STRUCTURALLY_PROVED_RELATIVE_TO_SIGMA
    )
    assert standing.empirical is EmpiricalStanding.INDEPENDENT_TARGET_MISSING


def test_structural_standing_requires_its_frozen_sigma() -> None:
    with pytest.raises(MetaAlgebraStandingError):
        DualStanding(
            structural=StructuralStanding.STRUCTURALLY_PROVED_RELATIVE_TO_SIGMA,
            empirical=EmpiricalStanding.NOT_TESTED,
            specification=None,
            independence_grade=(
                SpecificationIndependenceGrade.PROSPECTIVE_SPECIFICATION_INDEPENDENT
            ),
            reason="بلا مواصفة",
        )


def test_structural_standing_relative_to_sigma_requires_an_established_grade() -> None:
    with pytest.raises(MetaAlgebraStandingError):
        DualStanding(
            structural=StructuralStanding.STRUCTURALLY_PROVED_RELATIVE_TO_SIGMA,
            empirical=EmpiricalStanding.NOT_TESTED,
            specification=sigma(),
            independence_grade=SpecificationIndependenceGrade.NOT_ESTABLISHED,
            reason="بلا رتبة",
        )


def test_unassessed_structural_standing_does_not_require_sigma() -> None:
    standing = DualStanding(
        structural=StructuralStanding.NOT_ASSESSED,
        empirical=EmpiricalStanding.NOT_TESTED,
        specification=None,
        independence_grade=SpecificationIndependenceGrade.NOT_ESTABLISHED,
        reason="لم تُقيَّم بعد",
    )

    assert standing.specification is None


def test_no_standing_member_is_named_proved_without_its_sigma() -> None:
    assert "PROVED" not in {member.value for member in StructuralStanding}
    assert all(
        member.value.endswith("RELATIVE_TO_SIGMA")
        for member in StructuralStanding
        if member.requires_frozen_sigma
    )


def test_independent_target_missing_has_no_structural_counterpart() -> None:
    assert "INDEPENDENT_TARGET_MISSING" in {
        member.value for member in EmpiricalStanding
    }
    assert "INDEPENDENT_TARGET_MISSING" not in {
        member.value for member in StructuralStanding
    }


def test_dual_standing_exposes_two_fields_and_no_third_that_merges_them() -> None:
    content = DualStanding(
        structural=StructuralStanding.STRUCTURALLY_UNDERPOWERED,
        empirical=EmpiricalStanding.EMPIRICALLY_SUPPORTED_IN_SCOPE,
        specification=None,
        independence_grade=SpecificationIndependenceGrade.NOT_ESTABLISHED,
        reason="محوران",
    ).as_canonical_content()

    assert content["structural"] != content["empirical"]
    assert not any(
        marker in key
        for key in content
        for marker in ("combined", "overall", "merged", "verdict", "score")
    )


def test_an_implementation_predating_its_contract_cannot_be_prospective() -> None:
    with pytest.raises(MetaAlgebraStandingError):
        ImplementationConformanceRecord(
            implementation_id="arabic.carrier_state_candidate",
            specification=sigma(),
            implementation_predates_contract=True,
            grade=(
                SpecificationIndependenceGrade.PROSPECTIVE_SPECIFICATION_INDEPENDENT
            ),
            reason="محاولةُ ترقيةٍ رجعيّة",
        )


def test_an_implementation_predating_its_contract_may_be_retrospective() -> None:
    record = ImplementationConformanceRecord(
        implementation_id="arabic.syllabifier",
        specification=sigma(),
        implementation_predates_contract=True,
        grade=SpecificationIndependenceGrade.RETROSPECTIVE_CONFORMANCE,
        reason="الدالّةُ سابقةٌ للعقد، فأقصى ما تبلغ المطابقةُ الرجعيّة",
    )

    assert record.grade is SpecificationIndependenceGrade.RETROSPECTIVE_CONFORMANCE


def test_an_implementation_written_after_its_contract_may_be_prospective() -> None:
    record = ImplementationConformanceRecord(
        implementation_id="later.transition",
        specification=sigma(),
        implementation_predates_contract=False,
        grade=(SpecificationIndependenceGrade.PROSPECTIVE_SPECIFICATION_INDEPENDENT),
        reason="العقدُ سبق الدالّة",
    )

    assert record.implementation_predates_contract is False


def test_conformance_record_refuses_a_non_boolean_precedence_claim() -> None:
    with pytest.raises(MetaAlgebraStandingError):
        ImplementationConformanceRecord(
            implementation_id="impl",
            specification=sigma(),
            implementation_predates_contract=1,  # type: ignore[arg-type]
            grade=SpecificationIndependenceGrade.RETROSPECTIVE_CONFORMANCE,
            reason="قيمةٌ تُحمَل لا واقعةٌ مُصرَّحٌ بها",
        )
