"""شاهدُ سلسلة الأصل: اتحادُ البصمة ليس اتحادَ السلسلة، والسلسلةُ تُشتَقّ ولا تُنشَأ."""

from __future__ import annotations

import pytest

from alghanem.ontology.general import (
    GeneralOntology,
    OntologicalCandidate,
    OntologicalKind,
)
from alghanem.ontology.lineage import ExistenceLineageError, ExistenceLineageRef
from alghanem.ontology.linguistic import LinguisticFunction
from alghanem.ontology.linguistic_v2 import (
    LinguisticOntologyV2,
    ReferencedFunctionalLicense,
)
from alghanem.prior.conditions import (
    PriorCondition,
    PriorConditionKind,
    PriorInformationBase,
    PriorLicenseGenus,
)


def _base(
    base_id: str = "pk0-test", *, domain_note: str = "مجالٌ صوريٌّ للاختبار"
) -> PriorInformationBase:
    return PriorInformationBase(
        base_id=base_id,
        domain_note=domain_note,
        conditions=tuple(
            PriorCondition(
                condition_id=f"{base_id}-{kind.value}",
                kind=kind,
                statement=f"شرطُ {kind.value}",
                what_it_forbids=f"ما يخالف {kind.value}",
                licensed_by=PriorLicenseGenus.STIPULATED_FOR_THE_DOMAIN,
            )
            for kind in PriorConditionKind
        ),
    )


def _general(
    base: PriorInformationBase, ontology_id: str = "o0-test"
) -> GeneralOntology:
    return GeneralOntology.founded_on(
        ontology_id,
        base,
        (
            OntologicalCandidate(
                candidate_id="cand-thing",
                kind=OntologicalKind.THING,
                necessity_claim="لا يُستغنى عن الشيء",
                irreducibility_claim="لا يُرَدّ الشيء إلى غيره",
                licensing_condition=PriorConditionKind.IDENTITY_CRITERION,
            ),
        ),
    )


def _linguistic(
    general: GeneralOntology,
    base: PriorInformationBase,
    ontology_id: str = "ol2-test",
) -> LinguisticOntologyV2:
    return LinguisticOntologyV2.founded_on(
        ontology_id,
        general,
        (
            ReferencedFunctionalLicense.granted(
                "lic-anchor",
                OntologicalCandidate(
                    candidate_id="cand-thing",
                    kind=OntologicalKind.THING,
                    necessity_claim="لا يُستغنى عن الشيء",
                    irreducibility_claim="لا يُرَدّ الشيء إلى غيره",
                    licensing_condition=PriorConditionKind.IDENTITY_CRITERION,
                ),
                LinguisticFunction.TERM_ANCHOR_ROLE,
                "قراءةٌ صوريّة",
                base,
                PriorConditionKind.DOMAIN,
            ),
        ),
    )


def test_a_lineage_records_the_three_levels_it_passed_through() -> None:
    base = _base()
    general = _general(base)
    linguistic = _linguistic(general, base)
    lineage = ExistenceLineageRef.of(general, linguistic)
    assert lineage.base_id == base.base_id
    assert lineage.base_content_id == base.content_id
    assert lineage.general_ontology_id == general.ontology_id
    assert lineage.general_content_id == general.content_id
    assert lineage.linguistic_ontology_id == linguistic.ontology_id
    assert lineage.linguistic_content_id == linguistic.content_id


def test_direct_construction_issues_no_lineage_at_all() -> None:
    with pytest.raises(ExistenceLineageError):
        ExistenceLineageRef(
            base_id="قاعدةٌ مزعومة",
            base_content_id="بصمةٌ مكتوبة",
            general_ontology_id="أنطولوجيا مزعومة",
            general_content_id="بصمةٌ مكتوبة",
            linguistic_ontology_id="لغويّةٌ مزعومة",
            linguistic_content_id="بصمةٌ مكتوبة",
        )


def test_a_forged_witness_cannot_be_constructed() -> None:
    from alghanem.ontology import lineage

    with pytest.raises(ExistenceLineageError):
        lineage._LineageWitness()


def test_a_linguistic_ontology_of_another_general_ontology_is_refused() -> None:
    base = _base()
    general = _general(base)
    other = _general(base, ontology_id="o0-other")
    linguistic = _linguistic(other, base)
    with pytest.raises(ExistenceLineageError) as refusal:
        ExistenceLineageRef.of(general, linguistic)
    assert "مُعرِّفُ الأنطولوجيا العامّة" in str(refusal.value)


def test_every_broken_place_in_the_chain_is_named() -> None:
    base = _base()
    general = _general(base)
    stranger_base = _base("pk0-other")
    stranger_general = _general(stranger_base)
    linguistic = _linguistic(stranger_general, stranger_base)
    with pytest.raises(ExistenceLineageError) as refusal:
        ExistenceLineageRef.of(general, linguistic)
    message = str(refusal.value)
    assert "بصمةُ الأنطولوجيا العامّة" in message
    assert "مرجعُ القاعدة السابقة" in message


def test_verification_rederives_both_ends_of_the_chain() -> None:
    base = _base()
    general = _general(base)
    linguistic = _linguistic(general, base)
    lineage = ExistenceLineageRef.of(general, linguistic)
    assert lineage.verify_against(general, linguistic) is True
    moved_base = _base(domain_note="مجالٌ آخر")
    moved_general = _general(moved_base)
    moved_linguistic = _linguistic(moved_general, moved_base)
    assert lineage.verify_against(moved_general, moved_linguistic) is False


def test_two_chains_of_different_origins_are_two_identities() -> None:
    base = _base()
    first = ExistenceLineageRef.of(_general(base), _linguistic(_general(base), base))
    other_base = _base("pk0-other")
    other_general = _general(other_base)
    second = ExistenceLineageRef.of(
        other_general, _linguistic(other_general, other_base)
    )
    assert first.content_id != second.content_id


def test_a_lineage_is_a_new_object_beside_the_ontologies_not_inside_them() -> None:
    from dataclasses import fields

    base = _base()
    general = _general(base)
    linguistic = _linguistic(general, base)
    assert "lineage_ref" not in {item.name for item in fields(GeneralOntology)}
    assert "lineage_ref" not in {item.name for item in fields(LinguisticOntologyV2)}
    assert (
        ExistenceLineageRef.of(general, linguistic).content_id != linguistic.content_id
    )
