"""اختباراتُ `G0.FIBER-0`: العقدةُ الليفيّة، والتوازي، وحيادُ العقد، وختمُ الجواب."""

from __future__ import annotations

import pytest

from alghanem.prior import (
    PriorCondition,
    PriorConditionKind,
    PriorInformationBase,
    PriorLicenseGenus,
)
from alghanem.prior_fiber import (
    PRIOR_FIBER_LAWS,
    PRIOR_FIBER_NODE_POSITIONS,
    AdmissibleDistinction,
    DomainMember,
    ExternalRankReference,
    FiberAxis,
    FiberContract,
    ParallelFiberBundle,
    PriorFiberError,
    PriorFiberNode,
    SlotStanding,
    SuccessCriterion,
    fiber_import_isolation_audit,
    fiber_vocabulary_audit,
    project_all_fibers,
    project_fiber,
    seal_gold,
)
from alghanem.prior_fiber import audit as audit_module
from alghanem.prior_fiber import contract as contract_module
from alghanem.prior_fiber import fibers as fibers_module
from alghanem.prior_fiber import node as node_module


def _condition(kind: PriorConditionKind, *, licensed: bool = True) -> PriorCondition:
    return PriorCondition(
        condition_id=f"c.{kind.value}",
        kind=kind,
        statement=f"نصُّ الشرط في موضع {kind.value}",
        what_it_forbids=f"يمنع ما خالف موضع {kind.value}",
        licensed_by=(
            PriorLicenseGenus.STIPULATED_FOR_THE_DOMAIN
            if licensed
            else PriorLicenseGenus.UNREAD
        ),
    )


def _base(*, licensed: bool = True) -> PriorInformationBase:
    return PriorInformationBase(
        base_id="base.test",
        domain_note="مجالٌ صوريٌّ للاختبار",
        conditions=tuple(
            _condition(kind, licensed=licensed or kind is not PriorConditionKind.DOMAIN)
            for kind in PriorConditionKind
        ),
    )


def _distinction(distinction_id: str = "d.one") -> AdmissibleDistinction:
    return AdmissibleDistinction(
        distinction_id=distinction_id,
        question="سؤالُ الفرق؟",
        options=("أ", "ب"),
        asked_when="تُطرَح دائمًا",
    )


def _node(**overrides: object) -> PriorFiberNode:
    fields: dict[str, object] = {
        "origin_id": "origin.test",
        "instance_id": "instance.test",
        "prior_base": _base(),
        "slot_geometry": ("d.one",),
        "admissible_distinctions": (_distinction(),),
        "relations": (),
        "capabilities": ("قدرةٌ مُعلَنة",),
        "evidence_requirements": ("دليلٌ مُسمًّى لكلِّ إسناد",),
        "gates": ("بوّابةٌ مُعلَنة",),
        "rank_reference": ExternalRankReference(
            evidence_ref="ref.evidence",
            rank_ceiling_ref="ref.ceiling",
            issuing_authority="سلطةٌ خارج الليف",
        ),
        "residual_policy": "كلُّ متروكٍ بقيّةٌ حاجبة",
        "trace": ("أثرٌ مُسجَّل",),
    }
    fields.update(overrides)
    return PriorFiberNode(**fields)  # type: ignore[arg-type]


def _contract(**overrides: object) -> FiberContract:
    node = _node()
    members = (
        DomainMember(member_id="member.one", observed_inputs=(("d.one", "أ"),)),
        DomainMember(member_id="member.two", observed_inputs=(("d.one", "ب"),)),
    )
    fields: dict[str, object] = {
        "contract_id": "contract.test",
        "node": node,
        "members": members,
        "success_criteria": tuple(SuccessCriterion),
        "gold_seal": seal_gold(
            {"member.one": "جوابٌ أوّل", "member.two": "جوابٌ ثانٍ"},
            gold_scheme="جوابٌ مختومٌ للاختبار",
        ),
        "authored_by": "author.neutral",
        "reading_systems": ("system.one", "system.two"),
    }
    fields.update(overrides)
    return FiberContract(**fields)  # type: ignore[arg-type]


def test_the_node_declares_its_twelve_positions_as_its_own_fields() -> None:
    assert tuple(PriorFiberNode.__dataclass_fields__) == PRIOR_FIBER_NODE_POSITIONS


def test_the_node_starts_neutral_and_assigns_no_positive_role() -> None:
    node = _node()

    assert node.assigns_no_positive_role
    assert all(
        standing is SlotStanding.UNASSIGNED for _, standing in node.neutral_slot_state
    )
    assert not SlotStanding.UNASSIGNED.is_positive


def test_an_unlicensed_prior_base_cannot_found_a_fiber_node() -> None:
    unlicensed = PriorInformationBase(
        base_id="base.unlicensed",
        domain_note="قاعدةٌ فيها شرطٌ غيرُ مقروء",
        conditions=tuple(
            _condition(kind, licensed=kind is not PriorConditionKind.DOMAIN)
            for kind in PriorConditionKind
        ),
    )

    with pytest.raises(PriorFiberError, match="هندسةٌ مُرخَّصة"):
        _node(prior_base=unlicensed)


def test_the_origin_and_the_instance_are_distinct_identities() -> None:
    with pytest.raises(PriorFiberError, match="متمايزان"):
        _node(instance_id="origin.test")


def test_a_missing_distinction_is_refused_not_answered_with_none() -> None:
    with pytest.raises(PriorFiberError, match="لا فرقَ في العقدة"):
        _node().distinction("d.absent")


def test_the_three_fibers_are_projected_from_one_node_in_parallel() -> None:
    node = _node()

    bundle = project_all_fibers(node)

    assert bundle.is_parallel
    assert {fiber.axis for fiber in bundle.fibers} == set(FiberAxis)
    assert all(fiber.node_content_id == node.content_id for fiber in bundle.fibers)


def test_a_fiber_derived_from_another_fiber_is_refused() -> None:
    node = _node()
    fiber = project_fiber(node, FiberAxis.CARRIER_ALONE)

    with pytest.raises(PriorFiberError, match="ThreeFibersAreParallelNotSequential"):
        type(fiber)(
            axis=FiberAxis.CONTENT_ALONE,
            node_content_id=node.content_id,
            origin_id=node.origin_id,
            instance_id=node.instance_id,
            slot_geometry=node.slot_geometry,
            admissible_distinction_ids=("d.one",),
            derived_from_fiber=FiberAxis.CARRIER_ALONE,
        )


def test_a_bundle_missing_an_axis_is_refused() -> None:
    node = _node()

    with pytest.raises(PriorFiberError, match="تغطيةُ المحاور تامّة"):
        ParallelFiberBundle(
            node_content_id=node.content_id,
            fibers=(project_fiber(node, FiberAxis.CARRIER_ALONE),),
        )


def test_each_axis_declares_what_it_reads() -> None:
    assert FiberAxis.CARRIER_ALONE.reads_the_carrier
    assert not FiberAxis.CARRIER_ALONE.reads_the_content
    assert FiberAxis.CONTENT_ALONE.reads_the_content
    assert not FiberAxis.CONTENT_ALONE.reads_the_carrier
    assert FiberAxis.CARRIER_AND_CONTENT_TOGETHER.reads_the_carrier
    assert FiberAxis.CARRIER_AND_CONTENT_TOGETHER.reads_the_content


def test_a_system_may_not_author_the_contract_it_is_read_by() -> None:
    with pytest.raises(PriorFiberError, match="NoSystemDefinesTheContractItIsReadBy"):
        _contract(authored_by="system.one")


def test_a_contract_read_by_one_system_alone_is_refused() -> None:
    with pytest.raises(PriorFiberError, match="بنظامين فأكثر"):
        _contract(reading_systems=("system.one",))


def test_the_contract_covers_every_success_criterion_exactly() -> None:
    partial = tuple(
        criterion
        for criterion in SuccessCriterion
        if criterion is not SuccessCriterion.NO_JUMP
    )

    with pytest.raises(PriorFiberError, match="تغطيةً تامّةً"):
        _contract(success_criteria=partial)


def test_a_member_input_outside_the_declared_options_is_refused() -> None:
    stray = (
        DomainMember(member_id="member.one", observed_inputs=(("d.one", "ج"),)),
        DomainMember(member_id="member.two", observed_inputs=(("d.one", "ب"),)),
    )

    with pytest.raises(PriorFiberError, match="خارج قيم الفرق"):
        _contract(members=stray)


def test_the_gold_is_sealed_as_a_digest_and_withheld_from_the_contract() -> None:
    contract = _contract()

    assert contract.gold_is_sealed_by_digest_only
    assert contract.withholds("جوابٌ أوّل")
    assert contract.withholds("جوابٌ ثانٍ")
    assert contract.gold_seal.sealed_member_count == len(contract.members)


def test_the_seal_changes_when_the_withheld_answer_changes() -> None:
    first = seal_gold({"member.one": "أ"}, gold_scheme="صيغة")
    second = seal_gold({"member.one": "ب"}, gold_scheme="صيغة")

    assert first.gold_digest != second.gold_digest


def test_a_seal_that_does_not_cover_the_domain_is_refused() -> None:
    with pytest.raises(PriorFiberError, match="عددُ الأعضاء المختومة"):
        _contract(gold_seal=seal_gold({"member.one": "جوابٌ أوّل"}, gold_scheme="صيغة"))


def test_the_preregistration_digest_is_derived_from_the_frozen_content() -> None:
    contract = _contract()

    assert contract.preregistration_digest == _contract().preregistration_digest
    assert (
        contract.preregistration_digest
        != _contract(contract_id="contract.other").preregistration_digest
    )


def test_the_contract_ceiling_is_dominance_within_a_frozen_domain() -> None:
    assert "ObservedDominanceWithinFrozenDomain" in _contract().strength_claim_ceiling


def test_the_layer_is_import_isolated_from_domains_and_systems() -> None:
    report = fiber_import_isolation_audit()

    assert report.is_isolated, report.violations
    assert report.alghanem_imports
    for reached in report.alghanem_imports:
        head = reached.split(".")[1]
        assert head in {"canonical_content", "prior", "prior_fiber"}


def test_the_layer_names_stay_neutral_between_domains() -> None:
    report = fiber_vocabulary_audit(
        audit_module, contract_module, fibers_module, node_module
    )

    assert report.is_neutral, report.violations
    assert report.inspected_names


def test_every_law_is_distinct_and_non_blank() -> None:
    assert len(set(PRIOR_FIBER_LAWS)) == len(PRIOR_FIBER_LAWS)
    assert all(law.strip() for law in PRIOR_FIBER_LAWS)
