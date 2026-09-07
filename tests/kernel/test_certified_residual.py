import pytest

from alghanem.kernel import (
    AuthenticatedObservationBinding,
    CertifiedResidual,
    ObservedDifference,
    ReconstructionSpec,
    Residual,
    ResidualCertificationError,
    ResidualComparatorSpec,
    Trace,
)
from alghanem.kernel._internal.authenticated_observation_bridge import (
    issue_from_source_authority,
)
from alghanem.kernel.fractal import FrozenFactorRef


def parent() -> FrozenFactorRef:
    return FrozenFactorRef(
        "factor", "factor-content", "freeze", "domain", "birth", "r1"
    )


def observation() -> AuthenticatedObservationBinding:
    return issue_from_source_authority("observation", "authentication")


def reconstruction() -> ReconstructionSpec:
    return ReconstructionSpec.register("reconstruction", "rebuild projection")


def comparator() -> ResidualComparatorSpec:
    return ResidualComparatorSpec.register("comparator", "exact projection equality")


def difference(
    comparator_spec: ResidualComparatorSpec | None = None,
    *,
    witness: str = "difference",
) -> ObservedDifference:
    spec = comparator_spec or comparator()
    return ObservedDifference(
        spec.spec_id, spec.content_id, "observed", "reconstructed", witness
    )


def certified() -> CertifiedResidual:
    return CertifiedResidual.certify(
        "residual",
        parent(),
        observation(),
        "scope",
        reconstruction(),
        comparator(),
        difference(),
        Trace(("observe", "reconstruct", "compare")),
    )


def test_certified_residual_binds_all_provenance() -> None:
    result = certified()

    assert result.parent_freeze_ref == parent()
    assert result.observation_ref == observation()
    assert result.reconstruction_spec_id == "reconstruction"
    assert result.comparator_spec_id == "comparator"
    assert result.observed_projection_id == "observed"
    assert result.reconstructed_projection_id == "reconstructed"
    assert result.difference_witness_id == "difference"
    assert result.residual_content_id


def test_legacy_residual_is_not_a_certified_residual() -> None:
    assert isinstance(Residual("legacy remainder"), Residual)
    assert not isinstance(Residual("legacy remainder"), CertifiedResidual)


def test_certification_requires_exact_frozen_parent() -> None:
    with pytest.raises(ResidualCertificationError):
        CertifiedResidual.certify(
            "residual",
            "factor-id",  # type: ignore[arg-type]
            observation(),
            "scope",
            reconstruction(),
            comparator(),
            difference(),
            Trace(("compare",)),
        )


def test_certification_requires_authenticated_observation() -> None:
    with pytest.raises(ResidualCertificationError):
        CertifiedResidual.certify(
            "residual",
            parent(),
            "observation",  # type: ignore[arg-type]
            "scope",
            reconstruction(),
            comparator(),
            difference(),
            Trace(("compare",)),
        )


def test_certification_rejects_no_difference() -> None:
    spec = comparator()
    no_difference = ObservedDifference(
        spec.spec_id, spec.content_id, "same", "same", ""
    )

    with pytest.raises(ResidualCertificationError):
        CertifiedResidual.certify(
            "residual",
            parent(),
            observation(),
            "scope",
            reconstruction(),
            spec,
            no_difference,
            Trace(("compare",)),
        )


def test_certification_rejects_posthoc_or_unregistered_specs() -> None:
    with pytest.raises(ResidualCertificationError):
        ReconstructionSpec("reconstruction", "posthoc")  # type: ignore[call-arg]
    with pytest.raises(ResidualCertificationError):
        ResidualComparatorSpec("comparator", "posthoc")  # type: ignore[call-arg]


def test_changing_provenance_changes_content_identity() -> None:
    first = certified()
    second = CertifiedResidual.certify(
        "residual",
        parent(),
        issue_from_source_authority("other-observation", "authentication"),
        "scope",
        reconstruction(),
        comparator(),
        difference(),
        Trace(("observe", "reconstruct", "compare")),
    )

    assert first != second
    assert first.residual_content_id != second.residual_content_id
