"""شواهدُ `O_L`: الماهيّةُ غيرُ الوظيفة، والترخيصُ جهةٌ لا احتواء."""

from __future__ import annotations

from dataclasses import fields

import pytest

from alghanem.ontology.general import (
    GeneralOntology,
    OntologicalCandidate,
    OntologicalKind,
    OntologyError,
)
from alghanem.ontology.linguistic import (
    LINGUISTIC_FUNCTION_NAMES,
    FunctionalLicense,
    LinguisticFunction,
    LinguisticFunctionRef,
    LinguisticOntology,
    LinguisticOntologyError,
    OntologicalCandidateRef,
)
from alghanem.prior.conditions import (
    PriorCondition,
    PriorConditionKind,
    PriorInformationBase,
    PriorLicenseGenus,
)


def _base() -> PriorInformationBase:
    return PriorInformationBase(
        base_id="pk0-test",
        domain_note="مجالٌ صوريٌّ للاختبار",
        conditions=tuple(
            PriorCondition(
                condition_id=f"c-{kind.value}",
                kind=kind,
                statement=f"شرطُ {kind.value}",
                what_it_forbids=f"ما يخالف {kind.value}",
                licensed_by=PriorLicenseGenus.STIPULATED_FOR_THE_DOMAIN,
            )
            for kind in PriorConditionKind
        ),
    )


def _candidate(kind: OntologicalKind) -> OntologicalCandidate:
    return OntologicalCandidate(
        candidate_id=f"cand-{kind.value}",
        kind=kind,
        necessity_claim=f"لا يُستغنى عن {kind.value}",
        irreducibility_claim=f"لا يُرَدّ {kind.value} إلى غيره",
        licensing_condition=PriorConditionKind.IDENTITY_CRITERION,
    )


def _general() -> GeneralOntology:
    return GeneralOntology.founded_on(
        "o0-test",
        _base(),
        (
            _candidate(OntologicalKind.THING),
            _candidate(OntologicalKind.EVENT),
            _candidate(OntologicalKind.QUANTITY),
        ),
    )


def _license(
    general: GeneralOntology,
    kind: OntologicalKind,
    function: LinguisticFunction = LinguisticFunction.TERM_ANCHOR_ROLE,
) -> FunctionalLicense:
    candidate = general.candidate(f"cand-{kind.value}")
    return FunctionalLicense(
        license_id=f"lic-{kind.value}-{function.value}",
        candidate_ref=OntologicalCandidateRef.of(candidate),
        function_ref=LinguisticFunctionRef(
            function=function, read_from="قراءةٌ صوريّةٌ للاختبار"
        ),
        licensing_condition=PriorConditionKind.IDENTITY_CRITERION,
        condition_statement="يُرخَّص متى حُفِظت هويّةُ الموجود عبر مواضع النسبة",
    )


def test_a_kind_name_is_never_also_a_function_name() -> None:
    kinds = {kind.value for kind in OntologicalKind}
    functions = set(LINGUISTIC_FUNCTION_NAMES)
    assert (kinds & functions) <= {"unread"}


def test_an_event_is_a_kind_while_its_anchor_is_a_role() -> None:
    assert OntologicalKind.EVENT.value == "event"
    assert "event_anchor" not in LINGUISTIC_FUNCTION_NAMES
    assert LinguisticFunction.TERM_ANCHOR_ROLE.value == "term_anchor_role"


def test_neither_reference_type_may_hold_a_field_of_the_other() -> None:
    pairs = (
        (OntologicalCandidateRef, LinguisticFunctionRef),
        (LinguisticFunctionRef, OntologicalCandidateRef),
    )
    for declaring, forbidden in pairs:
        for field in fields(declaring):
            assert forbidden.__name__ not in str(field.type)


def test_a_license_without_a_condition_is_refused_at_construction() -> None:
    general = _general()
    candidate = general.candidate("cand-event")
    with pytest.raises(LinguisticOntologyError):
        FunctionalLicense(
            license_id="lic-bare",
            candidate_ref=OntologicalCandidateRef.of(candidate),
            function_ref=LinguisticFunctionRef(
                function=LinguisticFunction.TERM_ANCHOR_ROLE, read_from="قراءة"
            ),
            licensing_condition=PriorConditionKind.IDENTITY_CRITERION,
            condition_statement="   ",
        )


def test_licensing_runs_from_a_registered_candidate_to_a_function() -> None:
    general = _general()
    ontology = LinguisticOntology.founded_on(
        "ol-test", general, (_license(general, OntologicalKind.EVENT),)
    )
    assert ontology.general_content_id == general.content_id
    granted = ontology.licenses_for(LinguisticFunction.TERM_ANCHOR_ROLE)
    assert len(granted) == 1
    assert granted[0].candidate_ref.kind_name == "event"
    assert granted[0].is_operative


def test_a_license_for_an_unregistered_candidate_is_refused() -> None:
    general = _general()
    stranger = FunctionalLicense(
        license_id="lic-stranger",
        candidate_ref=OntologicalCandidateRef(
            candidate_id="cand-absent", kind_name="thing"
        ),
        function_ref=LinguisticFunctionRef(
            function=LinguisticFunction.PREDICATE_ROLE, read_from="قراءة"
        ),
        licensing_condition=PriorConditionKind.RELATION_POSSIBILITY,
        condition_statement="شرطٌ مُسمًّى",
    )
    with pytest.raises(OntologyError):
        LinguisticOntology.founded_on("ol-test", general, (stranger,))


def test_a_license_whose_kind_disagrees_with_the_registry_is_refused() -> None:
    general = _general()
    mismatched = FunctionalLicense(
        license_id="lic-mismatch",
        candidate_ref=OntologicalCandidateRef(
            candidate_id="cand-event", kind_name="quantity"
        ),
        function_ref=LinguisticFunctionRef(
            function=LinguisticFunction.TERM_ANCHOR_ROLE, read_from="قراءة"
        ),
        licensing_condition=PriorConditionKind.IDENTITY_CRITERION,
        condition_statement="شرطٌ مُسمًّى",
    )
    with pytest.raises(LinguisticOntologyError):
        LinguisticOntology.founded_on("ol-test", general, (mismatched,))


def test_an_unread_function_is_recorded_and_not_read_as_operative() -> None:
    general = _general()
    granted = _license(general, OntologicalKind.THING, LinguisticFunction.UNREAD)
    ontology = LinguisticOntology.founded_on("ol-test", general, (granted,))
    assert not granted.is_operative
    assert ontology.licenses_for(LinguisticFunction.TERM_ANCHOR_ROLE) == ()


def test_the_digest_is_independent_of_the_license_order() -> None:
    general = _general()
    first = _license(general, OntologicalKind.EVENT)
    second = _license(general, OntologicalKind.QUANTITY)
    forward = LinguisticOntology.founded_on("ol-test", general, (first, second))
    backward = LinguisticOntology.founded_on("ol-test", general, (second, first))
    assert forward.content_id == backward.content_id


def test_a_duplicated_license_id_is_refused_rather_than_folded() -> None:
    general = _general()
    granted = _license(general, OntologicalKind.EVENT)
    with pytest.raises(LinguisticOntologyError):
        LinguisticOntology.founded_on("ol-test", general, (granted, granted))


def test_a_reference_is_derived_from_a_standing_candidate_not_a_free_name() -> None:
    with pytest.raises(LinguisticOntologyError):
        OntologicalCandidateRef.of("cand-event")  # type: ignore[arg-type]
