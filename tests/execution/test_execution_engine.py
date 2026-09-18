"""شواهدُ `G0.RUN-0`: أربعُ حالاتٍ بلوغيّةٍ، واختباراتٌ مضادّةٌ بتغييرٍ واحد.

كلُّ اختبارٍ مضادٍّ هنا يغيّر **قيمةً واحدةً** في وثيقةٍ صحيحة، ويُثبِت مقدَّمًا
أيَّ حكمٍ ينبغي أن ينتج؛ فلا يُقرَأ الحكمُ ثمّ يُعدَّل المتوقَّعُ بعده.

تسجيلٌ لا سلطة: لا ولادةَ ولا حكمَ ولادةٍ ولا تجميدَ `E0`.
"""

from __future__ import annotations

import pytest
from execution_cases import (
    base_declaration,
    general_declaration,
    mutate,
    valid_document,
)

from alghanem.canonical_content import canonical_bytes, canonical_digest
from alghanem.execution import (
    LAW_SET,
    LAW_SET_DIGEST,
    CheckStanding,
    ExecutionLaw,
    ExecutionOutcome,
    ExecutionResultEnvelope,
    ExecutionResultError,
    InputFaultKind,
    InputStanding,
    RequiredAuthority,
    audit_lines,
    execute_document,
    is_reproducible,
    replay,
)
from alghanem.prior.conditions import PriorConditionKind, PriorLicenseGenus


def _standings(envelope: ExecutionResultEnvelope, law: ExecutionLaw) -> tuple[str, ...]:
    return tuple(
        entry.standing.value for entry in envelope.core.trace if entry.law == law.value
    )


def _entry(envelope: ExecutionResultEnvelope, law: ExecutionLaw) -> object:
    for entry in envelope.core.trace:
        if entry.law == law.value:
            return entry
    raise AssertionError(f"لا سطرَ في الأثر للقانون `{law.value}`")


def test_a_single_origin_case_passes() -> None:
    report = execute_document(valid_document())
    assert report.validation.standing is InputStanding.VALID
    assert report.envelope is not None
    assert report.envelope.core.outcome is ExecutionOutcome.PASS
    assert report.envelope.core.violations == ()
    assert report.envelope.core.residuals == ()
    assert report.envelope.core.materialized_identity is not None


def test_every_law_appears_in_the_trace_of_a_passing_case() -> None:
    report = execute_document(valid_document())
    assert report.envelope is not None
    named = {entry.law for entry in report.envelope.core.trace}
    assert named == {law.value for law in LAW_SET}


def test_a_welded_origin_blocks_and_leaves_no_residual() -> None:
    document = mutate(valid_document())
    document["prior_bases"].append(base_declaration("base.B"))
    document["nisbah"]["anchors"][0]["condition_site"]["base_id"] = "base.B"
    report = execute_document(document)
    assert report.envelope is not None
    core = report.envelope.core
    assert core.outcome is ExecutionOutcome.BLOCK
    assert core.residuals == ()
    assert core.materialized_identity is None
    assert ExecutionLaw.CONDITION_SITES_SHARE_THE_LINEAGE_BASE.value in {
        violation.law for violation in core.violations
    }


def test_a_declared_unresolved_role_defers_without_forging_a_reference() -> None:
    document = mutate(valid_document())
    document["nisbah"]["anchors"][0]["role_site"] = None
    document["unresolved_requirements"] = [
        {
            "required_authority": RequiredAuthority.ROLE_LICENSE.value,
            "subject_id": "anchor.first",
            "standing": "unresolved",
        }
    ]
    report = execute_document(document)
    assert report.validation.standing is InputStanding.VALID
    assert report.envelope is not None
    core = report.envelope.core
    assert core.outcome is ExecutionOutcome.DEFER
    assert core.violations == ()
    assert core.residuals
    assert core.materialized_identity is None


def test_an_unread_condition_defers_rather_than_blocking() -> None:
    document = mutate(valid_document())
    document["prior_bases"] = [
        base_declaration(
            "base.A",
            {PriorConditionKind.RELATION_POSSIBILITY: PriorLicenseGenus.UNREAD},
        )
    ]
    document["general_ontologies"] = [
        general_declaration(
            "general.A",
            "base.A",
            {PriorConditionKind.RELATION_POSSIBILITY: PriorLicenseGenus.UNREAD},
        )
    ]
    report = execute_document(document)
    assert report.envelope is not None
    assert report.envelope.core.outcome is ExecutionOutcome.DEFER
    assert CheckStanding.UNRESOLVED.value in _standings(
        report.envelope, ExecutionLaw.NO_UNREAD_CONDITION_IN_THE_FOUNDING_BASE
    )


def test_a_self_derived_licensing_genus_blocks() -> None:
    genus = PriorLicenseGenus.DERIVED_FROM_THE_ONTOLOGY_IT_LICENSES
    overrides = {PriorConditionKind.RELATION_POSSIBILITY: genus}
    document = mutate(valid_document())
    document["prior_bases"] = [base_declaration("base.A", overrides)]
    document["general_ontologies"] = [
        general_declaration("general.A", "base.A", overrides)
    ]
    report = execute_document(document)
    assert report.envelope is not None
    assert report.envelope.core.outcome is ExecutionOutcome.BLOCK
    assert CheckStanding.VIOLATED.value in _standings(
        report.envelope, ExecutionLaw.NO_SELF_DERIVED_LICENSING_GENUS
    )


def test_a_false_base_digest_is_invalid_input_and_never_a_block() -> None:
    document = mutate(valid_document())
    document["prior_bases"][0]["declared_content_id"] = "0" * 64
    report = execute_document(document)
    assert report.validation.standing is InputStanding.INVALID
    assert report.envelope is None
    assert InputFaultKind.DECLARED_CONTENT_ID_DISAGREES in {
        fault.kind for fault in report.validation.faults
    }


def test_a_false_general_digest_is_invalid_input() -> None:
    document = mutate(valid_document())
    document["general_ontologies"][0]["declared_content_id"] = "0" * 64
    report = execute_document(document)
    assert report.validation.standing is InputStanding.INVALID
    assert report.envelope is None


def test_a_missing_field_is_invalid_input_and_never_a_defer() -> None:
    document = mutate(valid_document())
    del document["nisbah"]["predicate"]["arity"]
    report = execute_document(document)
    assert report.validation.standing is InputStanding.INVALID
    assert report.envelope is None
    assert InputFaultKind.MISSING_REQUIRED_FIELD in {
        fault.kind for fault in report.validation.faults
    }


def test_an_unknown_key_is_invalid_input() -> None:
    document = mutate(valid_document())
    document["extra"] = "شيءٌ لم يُعرَّف"
    report = execute_document(document)
    assert report.validation.standing is InputStanding.INVALID
    assert InputFaultKind.UNKNOWN_KEY in {
        fault.kind for fault in report.validation.faults
    }


def test_an_absent_site_without_a_declared_requirement_is_invalid_input() -> None:
    document = mutate(valid_document())
    document["nisbah"]["anchors"][0]["role_site"] = None
    report = execute_document(document)
    assert report.validation.standing is InputStanding.INVALID
    assert InputFaultKind.UNDECLARED_ABSENT_SITE in {
        fault.kind for fault in report.validation.faults
    }


def test_a_requirement_for_a_present_site_is_a_contradiction() -> None:
    document = mutate(valid_document())
    document["unresolved_requirements"] = [
        {
            "required_authority": RequiredAuthority.ROLE_LICENSE.value,
            "subject_id": "anchor.first",
            "standing": "unresolved",
        }
    ]
    report = execute_document(document)
    assert report.validation.standing is InputStanding.INVALID


def test_a_version_two_schema_is_refused_at_the_door() -> None:
    document = mutate(valid_document())
    document["nisbah_schema"] = "linguistic-nisbah.schema.v2"
    report = execute_document(document)
    assert report.validation.standing is InputStanding.INVALID
    assert InputFaultKind.UNKNOWN_SCHEMA in {
        fault.kind for fault in report.validation.faults
    }


def test_a_role_license_read_for_another_function_blocks() -> None:
    document = mutate(valid_document())
    document["nisbah"]["anchors"][0]["role_site"]["license_id"] = "license.predicate"
    report = execute_document(document)
    assert report.envelope is not None
    assert report.envelope.core.outcome is ExecutionOutcome.BLOCK
    assert CheckStanding.VIOLATED.value in _standings(
        report.envelope, ExecutionLaw.ROLE_LICENSE_GRANTED_FOR_THE_FUNCTION_READ
    )


def test_a_non_operative_license_blocks() -> None:
    document = mutate(valid_document())
    document["linguistic_ontologies"][0]["licenses"][1]["function"] = "unread"
    document["nisbah"]["anchors"][0]["role_site"]["function"] = "unread"
    report = execute_document(document)
    assert report.envelope is not None
    assert report.envelope.core.outcome is ExecutionOutcome.BLOCK
    assert CheckStanding.VIOLATED.value in _standings(
        report.envelope, ExecutionLaw.ROLE_LICENSE_IS_OPERATIVE
    )


def test_a_role_site_from_another_ontology_blocks() -> None:
    document = mutate(valid_document())
    document["linguistic_ontologies"].append(
        {
            "ontology_id": "linguistic.B",
            "founded_on_general_id": "general.A",
            "declared_content_id": None,
            "licenses": [
                {
                    "license_id": "license.term",
                    "candidate_id": "cand.term",
                    "function": "term_anchor_role",
                    "read_from": "قراءةٌ مُسجَّلة",
                    "condition_base_id": "base.A",
                    "condition_place": PriorConditionKind.UNIT_CRITERION.value,
                }
            ],
        }
    )
    document["nisbah"]["anchors"][0]["role_site"]["linguistic_ontology_id"] = (
        "linguistic.B"
    )
    report = execute_document(document)
    assert report.envelope is not None
    assert report.envelope.core.outcome is ExecutionOutcome.BLOCK
    assert CheckStanding.VIOLATED.value in _standings(
        report.envelope, ExecutionLaw.ROLE_SITES_SHARE_THE_LINEAGE_ONTOLOGY
    )


def test_a_slot_order_change_does_not_pass_unnoticed() -> None:
    document = mutate(valid_document())
    document["nisbah"]["predicate"]["slots"][1]["position"] = 1
    report = execute_document(document)
    assert report.envelope is not None
    assert report.envelope.core.outcome is ExecutionOutcome.BLOCK
    assert CheckStanding.VIOLATED.value in _standings(
        report.envelope, ExecutionLaw.PREDICATE_ARITY_MATCHES_ITS_SLOTS
    )


def test_a_deferred_argument_role_name_blocks() -> None:
    document = mutate(valid_document())
    document["nisbah"]["predicate"]["slots"][0]["slot_id"] = "agent.site"
    report = execute_document(document)
    assert report.envelope is not None
    assert report.envelope.core.outcome is ExecutionOutcome.BLOCK
    assert CheckStanding.VIOLATED.value in _standings(
        report.envelope, ExecutionLaw.ARGUMENT_SLOT_IDS_ARE_NOT_DEFERRED_ROLE_NAMES
    )


def test_a_target_derived_arity_license_blocks() -> None:
    document = mutate(valid_document())
    document["nisbah"]["predicate"]["arity_license"] = "derived_from_the_target_state"
    report = execute_document(document)
    assert report.envelope is not None
    assert report.envelope.core.outcome is ExecutionOutcome.BLOCK
    assert CheckStanding.VIOLATED.value in _standings(
        report.envelope, ExecutionLaw.PREDICATE_ARITY_LICENSE_PERMITS_USE
    )


def test_an_unregistered_candidate_blocks() -> None:
    document = mutate(valid_document())
    document["linguistic_ontologies"][0]["licenses"][0]["candidate_id"] = "cand.absent"
    report = execute_document(document)
    assert report.envelope is not None
    assert report.envelope.core.outcome is ExecutionOutcome.BLOCK
    assert CheckStanding.VIOLATED.value in _standings(
        report.envelope, ExecutionLaw.LINGUISTIC_LICENSES_NAME_REGISTERED_CANDIDATES
    )


def test_a_license_from_another_base_blocks_the_linguistic_foundation() -> None:
    document = mutate(valid_document())
    document["prior_bases"].append(base_declaration("base.B"))
    document["linguistic_ontologies"][0]["licenses"][0]["condition_base_id"] = "base.B"
    report = execute_document(document)
    assert report.envelope is not None
    assert report.envelope.core.outcome is ExecutionOutcome.BLOCK
    assert CheckStanding.VIOLATED.value in _standings(
        report.envelope, ExecutionLaw.LINGUISTIC_LICENSES_SHARE_THE_FOUNDING_BASE
    )


def test_a_blocked_dependent_law_is_not_read_as_missing_evidence() -> None:
    document = mutate(valid_document())
    document["nisbah"]["declared_content_id"] = "0" * 64
    document["prior_bases"].append(base_declaration("base.B"))
    document["nisbah"]["anchors"][0]["condition_site"]["base_id"] = "base.B"
    report = execute_document(document)
    assert report.envelope is not None
    core = report.envelope.core
    assert core.outcome is ExecutionOutcome.BLOCK
    entry = _entry(report.envelope, ExecutionLaw.MATERIALIZED_IDENTITY_AGREES)
    assert entry.standing is CheckStanding.NOT_EVALUATED_BY_PREREQUISITE  # type: ignore[attr-defined]
    assert entry.blocked_by is not None  # type: ignore[attr-defined]
    assert core.residuals == ()


def test_an_absent_identity_claim_is_not_read_as_an_agreement() -> None:
    report = execute_document(valid_document())
    assert report.envelope is not None
    entry = _entry(report.envelope, ExecutionLaw.MATERIALIZED_IDENTITY_AGREES)
    assert entry.standing is CheckStanding.NOT_APPLICABLE_NO_CLAIM  # type: ignore[attr-defined]
    assert entry.expected is None  # type: ignore[attr-defined]
    assert entry.blocked_by is None  # type: ignore[attr-defined]


def test_a_no_claim_standing_is_causally_distinct_from_a_blocked_one() -> None:
    assert CheckStanding.NOT_APPLICABLE_NO_CLAIM is not (
        CheckStanding.NOT_EVALUATED_BY_PREREQUISITE
    )
    for standing in (
        CheckStanding.NOT_APPLICABLE_NO_CLAIM,
        CheckStanding.NOT_EVALUATED_BY_PREREQUISITE,
    ):
        assert not standing.bears_on_the_outcome


def test_a_true_identity_claim_is_satisfied_and_a_false_one_blocks() -> None:
    report = execute_document(valid_document())
    assert report.envelope is not None
    assert report.envelope.core.materialized_identity is not None
    truthful = mutate(valid_document())
    truthful["nisbah"]["declared_content_id"] = (
        report.envelope.core.materialized_identity.content_id
    )
    agreed = execute_document(truthful)
    assert agreed.envelope is not None
    assert agreed.envelope.core.outcome is ExecutionOutcome.PASS
    assert _standings(agreed.envelope, ExecutionLaw.MATERIALIZED_IDENTITY_AGREES) == (
        CheckStanding.SATISFIED.value,
    )
    lying = mutate(valid_document())
    lying["nisbah"]["declared_content_id"] = "0" * 64
    refused = execute_document(lying)
    assert refused.envelope is not None
    assert refused.envelope.core.outcome is ExecutionOutcome.BLOCK
    assert refused.envelope.core.materialized_identity is None


def test_a_declared_linguistic_identity_is_checked_after_the_licensing_act() -> None:
    report = execute_document(valid_document())
    assert report.envelope is not None
    assert report.envelope.core.lineage_identity is not None
    truthful = mutate(valid_document())
    truthful["linguistic_ontologies"][0]["declared_content_id"] = (
        report.envelope.core.lineage_identity.linguistic_ontology.content_id
    )
    agreed = execute_document(truthful)
    assert agreed.envelope is not None
    assert agreed.validation.standing is InputStanding.VALID
    assert agreed.envelope.core.outcome is ExecutionOutcome.PASS
    lying = mutate(valid_document())
    lying["linguistic_ontologies"][0]["declared_content_id"] = "0" * 64
    refused = execute_document(lying)
    assert refused.validation.standing is InputStanding.VALID
    assert refused.envelope is not None
    assert refused.envelope.core.outcome is ExecutionOutcome.BLOCK


def test_the_same_input_yields_the_same_result_and_the_same_trace() -> None:
    document = valid_document()
    first = execute_document(document)
    second = execute_document(document)
    assert first.envelope is not None
    assert second.envelope is not None
    assert first.envelope.execution_digest == second.envelope.execution_digest
    assert first.envelope.core.as_canonical_content() == (
        second.envelope.core.as_canonical_content()
    )


def test_a_replay_runs_from_the_stored_declaration() -> None:
    report = execute_document(valid_document())
    assert report.envelope is not None
    replayed = replay(report.envelope)
    assert replayed.envelope is not None
    assert replayed.envelope.execution_digest == report.envelope.execution_digest
    assert is_reproducible(report.envelope)


def test_an_envelope_is_bound_to_the_declaration_it_judged() -> None:
    report = execute_document(valid_document())
    assert report.envelope is not None
    tampered = mutate(report.envelope.declaration_document)
    tampered["schema"] = "alghanem.execution.v0"
    with pytest.raises(ExecutionResultError):
        ExecutionResultEnvelope(
            declaration_document=tampered,
            core=report.envelope.core,
            execution_digest=report.envelope.execution_digest,
        )


def test_an_execution_digest_is_derived_not_written() -> None:
    report = execute_document(valid_document())
    assert report.envelope is not None
    with pytest.raises(ExecutionResultError):
        ExecutionResultEnvelope(
            declaration_document=report.envelope.declaration_document,
            core=report.envelope.core,
            execution_digest="0" * 64,
        )
    assert "execution_digest" not in report.envelope.core.as_canonical_content()


def test_the_law_set_digest_changes_when_the_order_changes() -> None:
    reordered = list(law.value for law in LAW_SET)
    reordered[0], reordered[1] = reordered[1], reordered[0]
    assert (
        canonical_digest(
            canonical_bytes(
                {
                    "law_set_id": "alghanem.execution.laws.G0.RUN-0",
                    "laws": reordered,
                }
            )
        )
        != LAW_SET_DIGEST
    )


def test_an_audit_reads_the_trace_without_adding_a_line() -> None:
    report = execute_document(valid_document())
    assert report.envelope is not None
    lines = audit_lines(report.envelope)
    assert lines[0] == "outcome: pass"
    named = sum(1 for line in lines if line.startswith("  "))
    assert named >= len(report.envelope.core.trace)
