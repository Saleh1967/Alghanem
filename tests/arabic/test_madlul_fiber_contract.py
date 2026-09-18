"""اختباراتُ مُحوِّل مجال المدلول إلى عقدٍ ليفيٍّ محايد: الاتّجاه، والحجب، والتغطية."""

from __future__ import annotations

import pytest

from alghanem.arabic.fiber_contracts import (
    MADLUL_CONTRACT_AUTHOR,
    build_madlul_fiber_contract,
    build_madlul_fiber_node,
    commit_madlul_gold,
    madlul_contract_body,
    madlul_domain_members,
    madlul_member_id,
    madlul_parallel_fibers,
    madlul_prior_base,
)
from alghanem.arabic.madlul_alone_formal import (
    ATTESTED_SIGNIFIED_WITNESSES,
    MADLUL_SOURCE,
    MadlulSection,
)
from alghanem.prior import PriorConditionKind
from alghanem.prior_fiber import FiberAxis, PriorFiberError, SuccessCriterion

_NONCE = bytes(range(32))


def _contract():  # type: ignore[no-untyped-def]
    return build_madlul_fiber_contract(commit_madlul_gold(_NONCE))


def test_the_prior_base_covers_the_nine_possibility_conditions_and_is_licensed() -> (
    None
):
    base = madlul_prior_base()

    assert {condition.kind for condition in base.conditions} == set(PriorConditionKind)
    assert base.is_fit_to_found_an_ontology
    assert not base.unusable_condition_ids


def test_the_node_is_built_over_the_prior_base_and_stays_neutral() -> None:
    node = build_madlul_fiber_node()

    assert node.prior_base == madlul_prior_base()
    assert node.assigns_no_positive_role
    assert MADLUL_SOURCE in node.trace
    assert node.rank_reference.issuing_authority


def test_the_three_fibers_are_projected_together_from_the_one_node() -> None:
    bundle = madlul_parallel_fibers()

    assert bundle.is_parallel
    assert {fiber.axis for fiber in bundle.fibers} == set(FiberAxis)
    assert bundle.node_content_id == build_madlul_fiber_node().content_id


def test_every_attested_witness_becomes_exactly_one_domain_member() -> None:
    members = madlul_domain_members()

    assert len(members) == len(ATTESTED_SIGNIFIED_WITNESSES)
    assert len({member.member_id for member in members}) == len(members)


def test_a_member_carries_its_observed_carriers_only() -> None:
    node = build_madlul_fiber_node()
    declared = {
        distinction.distinction_id for distinction in node.admissible_distinctions
    }

    for member in madlul_domain_members():
        assert {key for key, _ in member.observed_inputs} == declared


def test_the_member_identity_is_derived_from_its_witness_not_from_source_order() -> (
    None
):
    for witness in ATTESTED_SIGNIFIED_WITNESSES:
        member_id = madlul_member_id(witness)
        assert member_id.startswith("member.")
        assert witness.lexeme not in member_id
        assert witness.attested_section.value not in member_id


def test_the_contract_withholds_every_attested_section() -> None:
    contract = _contract()

    assert contract.gold_is_committed_not_shipped
    for section in MadlulSection:
        assert contract.withholds(section.value)
        assert madlul_contract_body().withholds(section.value)


def test_the_contract_body_is_frozen_before_any_reader_exists() -> None:
    body = madlul_contract_body()

    assert body.authored_by == MADLUL_CONTRACT_AUTHOR
    assert "reading_systems" not in tuple(type(body).__dataclass_fields__)
    assert _contract().carries_no_reader_identity
    assert body.body_digest == madlul_contract_body().body_digest


def test_the_contract_covers_every_criterion_and_commits_every_member() -> None:
    contract = _contract()

    assert set(contract.success_criteria) == set(SuccessCriterion)
    assert contract.gold_commitment.committed_member_count == len(contract.members)


def test_the_commitment_binds_the_body_and_moves_with_the_nonce() -> None:
    first = commit_madlul_gold(_NONCE)
    second = commit_madlul_gold(bytes(range(1, 33)))

    assert first.contract_body_digest == madlul_contract_body().body_digest
    assert first.commitment_digest != second.commitment_digest


def test_a_commitment_bound_to_another_body_is_refused_by_the_contract() -> None:
    from alghanem.prior_fiber import commit_gold

    stray = commit_gold(
        {"member.one": "جواب"},
        gold_scheme="صيغة",
        nonce=_NONCE,
        contract_body_digest="a" * 64,
    )

    with pytest.raises(PriorFiberError, match="جسم عقدٍ آخر"):
        build_madlul_fiber_contract(stray)


def test_the_contract_digest_is_stable_across_rebuilds() -> None:
    assert _contract().contract_digest == _contract().contract_digest


def test_the_fiber_layer_does_not_import_the_arabic_domain() -> None:
    from alghanem.prior_fiber import fiber_import_isolation_audit

    report = fiber_import_isolation_audit()

    assert report.is_isolated, report.violations
    assert not any("arabic" in reached for reached in report.alghanem_imports)
