import pytest

from alghanem.kernel import (
    AuthenticatedObservationBinding,
    Residual,
    ResidualCertificationCandidate,
    ResidualCertificationError,
    Trace,
)
from alghanem.kernel._internal.authenticated_observation_bridge import (
    issue_from_source_authority,
)
from alghanem.kernel.birth import ResidualDefinitionSpec
from alghanem.kernel.birth_content_identity import CanonicalBirthSemanticsEncoder
from alghanem.kernel.fractal import FrozenFactorRef


def parent() -> FrozenFactorRef:
    return FrozenFactorRef(
        "factor", "factor-content", "freeze", "domain", "birth", "r1"
    )


def observation() -> AuthenticatedObservationBinding:
    return issue_from_source_authority("observation", "authentication")


def residual_definition() -> ResidualDefinitionSpec:
    return ResidualDefinitionSpec(
        residual_id="residual",
        domain="domain",
        input_projection="projection",
        output_schema="schema",
        evaluator_id="declarative-evaluator",
        invariants=("coverage",),
        failure_semantics="defer malformed inputs",
    )


def candidate() -> ResidualCertificationCandidate:
    definition = residual_definition()
    manifest = CanonicalBirthSemanticsEncoder.encode_residual_definition(definition)
    return ResidualCertificationCandidate(
        residual_id="residual-occurrence",
        parent_freeze_ref=parent(),
        observation_ref=observation(),
        scope_ref="scope",
        residual_definition=definition,
        residual_definition_content_id=manifest.content_id,
        reconstruction_attempt_ref="attempt-ref",
        comparison_result_ref="comparison-ref",
        trace=Trace(("observe", "reconstruct", "compare")),
    )


def test_candidate_composes_existing_frozen_residual_definition() -> None:
    result = candidate()

    assert result.residual_definition is not None
    assert result.residual_definition_content_id.digest
    assert result.residual_id != result.residual_definition.residual_id


def test_legacy_residual_has_no_certification_authority() -> None:
    assert isinstance(Residual("legacy remainder"), Residual)
    assert not isinstance(Residual("legacy remainder"), ResidualCertificationCandidate)


def test_contract_does_not_claim_that_a_reference_proves_freeze() -> None:
    assert candidate().parent_freeze_ref == parent()

    # FrozenFactorRef remains caller-constructible until G0.FA.1.
    forged = FrozenFactorRef(
        "forged", "forged-content", "forged-certificate", "domain", "birth", "r1"
    )
    assert (
        ResidualCertificationCandidate(
            "occurrence",
            forged,
            observation(),
            "scope",
            residual_definition(),
            CanonicalBirthSemanticsEncoder.encode_residual_definition(
                residual_definition()
            ).content_id,
            "attempt",
            "comparison",
            Trace(("compare",)),
        ).parent_freeze_ref
        == forged
    )


def test_contract_rejects_missing_authenticated_observation() -> None:
    definition = residual_definition()
    manifest = CanonicalBirthSemanticsEncoder.encode_residual_definition(definition)
    with pytest.raises(ResidualCertificationError):
        ResidualCertificationCandidate(
            "occurrence",
            parent(),
            "observation",  # type: ignore[arg-type]
            "scope",
            definition,
            manifest.content_id,
            "attempt",
            "comparison",
            Trace(("compare",)),
        )


def test_contract_rejects_missing_reconstruction_or_comparison_reference() -> None:
    definition = residual_definition()
    manifest = CanonicalBirthSemanticsEncoder.encode_residual_definition(definition)
    with pytest.raises(ResidualCertificationError):
        ResidualCertificationCandidate(
            "occurrence",
            parent(),
            observation(),
            "scope",
            definition,
            manifest.content_id,
            "",
            "comparison",
            Trace(("compare",)),
        )
    with pytest.raises(ResidualCertificationError):
        ResidualCertificationCandidate(
            "occurrence",
            parent(),
            observation(),
            "scope",
            definition,
            manifest.content_id,
            "attempt",
            "",
            Trace(("compare",)),
        )
