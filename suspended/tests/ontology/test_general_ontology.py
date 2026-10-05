"""شواهدُ `O_0`: ضرورةٌ وعدمُ اختزالٍ معًا، وبناءٌ على بصمة `PK_0` لا على اسمها."""

from __future__ import annotations

import pytest

from alghanem.ontology.general import (
    ONTOLOGICAL_CANDIDATE_NAMES,
    GeneralOntology,
    OntologicalCandidate,
    OntologicalKind,
    OntologyError,
    PriorBaseRef,
)
from alghanem.prior.conditions import (
    PriorCondition,
    PriorConditionKind,
    PriorInformationBase,
    PriorLicenseGenus,
)


def _base(
    licensed_by: PriorLicenseGenus = PriorLicenseGenus.STIPULATED_FOR_THE_DOMAIN,
) -> PriorInformationBase:
    return PriorInformationBase(
        base_id="pk0-test",
        domain_note="مجالٌ صوريٌّ للاختبار",
        conditions=tuple(
            PriorCondition(
                condition_id=f"c-{kind.value}",
                kind=kind,
                statement=f"شرطُ {kind.value}",
                what_it_forbids=f"ما يخالف {kind.value}",
                licensed_by=licensed_by,
            )
            for kind in PriorConditionKind
        ),
    )


def _candidate(
    kind: OntologicalKind = OntologicalKind.EVENT,
    licensing_condition: PriorConditionKind = PriorConditionKind.IDENTITY_CRITERION,
) -> OntologicalCandidate:
    return OntologicalCandidate(
        candidate_id=f"cand-{kind.value}",
        kind=kind,
        necessity_claim=f"لا يُستغنى عن {kind.value} في وصف المجال",
        irreducibility_claim=f"لا يُرَدّ {kind.value} إلى غيره من المرشَّحين",
        licensing_condition=licensing_condition,
    )


def test_the_candidate_vocabulary_declares_an_unread_member() -> None:
    assert "unread" in ONTOLOGICAL_CANDIDATE_NAMES


def test_a_candidate_without_a_necessity_claim_is_refused() -> None:
    with pytest.raises(OntologyError):
        OntologicalCandidate(
            candidate_id="cand-x",
            kind=OntologicalKind.THING,
            necessity_claim="  ",
            irreducibility_claim="لا يُرَدّ إلى غيره",
            licensing_condition=PriorConditionKind.DOMAIN,
        )


def test_a_candidate_without_an_irreducibility_claim_is_refused() -> None:
    with pytest.raises(OntologyError):
        OntologicalCandidate(
            candidate_id="cand-x",
            kind=OntologicalKind.THING,
            necessity_claim="لا يُستغنى عنه",
            irreducibility_claim="",
            licensing_condition=PriorConditionKind.DOMAIN,
        )


def test_an_ontology_is_founded_on_the_digest_of_its_prior_base() -> None:
    base = _base()
    ontology = GeneralOntology.founded_on("o0-test", base, (_candidate(),))
    assert ontology.prior_base_ref == PriorBaseRef.of(base)
    assert ontology.prior_base_ref.content_id == base.content_id
    assert ontology.candidate_ids == ("cand-event",)


def test_an_ontology_refuses_a_base_that_carries_an_unlicensed_condition() -> None:
    base = _base(PriorLicenseGenus.DERIVED_FROM_THE_ONTOLOGY_IT_LICENSES)
    with pytest.raises(OntologyError):
        GeneralOntology.founded_on("o0-test", base, (_candidate(),))


def test_a_candidate_naming_a_place_absent_from_the_base_is_refused() -> None:
    base = _base()
    partial = PriorInformationBase.__new__(PriorInformationBase)
    object.__setattr__(partial, "base_id", base.base_id)
    object.__setattr__(partial, "domain_note", base.domain_note)
    object.__setattr__(
        partial,
        "conditions",
        tuple(
            condition
            for condition in base.conditions
            if condition.kind is not PriorConditionKind.PRESERVED_TRACE
        ),
    )
    with pytest.raises(OntologyError):
        GeneralOntology.founded_on(
            "o0-test",
            partial,
            (_candidate(licensing_condition=PriorConditionKind.PRESERVED_TRACE),),
        )


def test_a_duplicated_candidate_id_is_refused_rather_than_folded() -> None:
    base = _base()
    with pytest.raises(OntologyError):
        GeneralOntology.founded_on("o0-test", base, (_candidate(), _candidate()))


def test_an_absent_candidate_is_refused_rather_than_returned_as_none() -> None:
    ontology = GeneralOntology.founded_on("o0-test", _base(), (_candidate(),))
    with pytest.raises(OntologyError):
        ontology.candidate("cand-absent")


def test_the_digest_is_independent_of_the_candidate_order() -> None:
    base = _base()
    first = _candidate(OntologicalKind.EVENT)
    second = _candidate(OntologicalKind.QUANTITY)
    forward = GeneralOntology.founded_on("o0-test", base, (first, second))
    backward = GeneralOntology.founded_on("o0-test", base, (second, first))
    assert forward.content_id == backward.content_id


def test_a_reference_is_derived_from_a_standing_base_not_from_a_free_name() -> None:
    with pytest.raises(OntologyError):
        PriorBaseRef.of("pk0-test")  # type: ignore[arg-type]
