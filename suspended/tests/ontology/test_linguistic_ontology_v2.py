"""شواهدُ `O_L²`: أصلُ الرخصة مرجعٌ مبصوم، والرخصةُ وشرطُها من قاعدةٍ واحدة."""

from __future__ import annotations

from dataclasses import fields

import pytest

from alghanem.ontology.general import (
    GeneralOntology,
    OntologicalCandidate,
    OntologicalKind,
)
from alghanem.ontology.linguistic import LinguisticFunction, LinguisticFunctionRef
from alghanem.ontology.linguistic_v2 import (
    LinguisticOntologyV2,
    LinguisticOntologyV2Error,
    ReferencedFunctionalLicense,
)
from alghanem.prior.conditions import (
    PriorCondition,
    PriorConditionKind,
    PriorInformationBase,
    PriorLicenseGenus,
)
from alghanem.prior.references import PriorConditionRef


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


def _candidate(kind: OntologicalKind = OntologicalKind.THING) -> OntologicalCandidate:
    return OntologicalCandidate(
        candidate_id=f"cand-{kind.value}",
        kind=kind,
        necessity_claim=f"لا يُستغنى عن {kind.value}",
        irreducibility_claim=f"لا يُرَدّ {kind.value} إلى غيره",
        licensing_condition=PriorConditionKind.IDENTITY_CRITERION,
    )


def _general(base: PriorInformationBase | None = None) -> GeneralOntology:
    return GeneralOntology.founded_on(
        "o0-test",
        base if base is not None else _base(),
        (_candidate(), _candidate(OntologicalKind.RELATION)),
    )


def _license(
    license_id: str,
    *,
    base: PriorInformationBase,
    kind: OntologicalKind = OntologicalKind.THING,
    function: LinguisticFunction = LinguisticFunction.TERM_ANCHOR_ROLE,
    place: PriorConditionKind = PriorConditionKind.DOMAIN,
) -> ReferencedFunctionalLicense:
    return ReferencedFunctionalLicense.granted(
        license_id,
        _candidate(kind),
        function,
        "قراءةٌ صوريّة",
        base,
        place,
    )


def test_a_license_names_the_very_condition_that_licensed_it() -> None:
    base = _base()
    granted = _license("lic-1", base=base)
    assert granted.condition_ref.condition_id == "pk0-test-domain"
    assert granted.condition_ref.base_content_id == base.content_id
    assert granted.licensing_place is PriorConditionKind.DOMAIN


def test_no_free_text_survives_in_the_origin_of_a_license() -> None:
    field_names = {item.name for item in fields(ReferencedFunctionalLicense)}
    assert "condition_statement" not in field_names
    assert "licensing_condition" not in field_names
    content = _license("lic-1", base=_base()).as_canonical_content()
    assert set(content) == {
        "license_id",
        "candidate_ref",
        "function_ref",
        "condition_ref",
    }


def test_a_prose_statement_cannot_stand_where_a_reference_belongs() -> None:
    with pytest.raises(LinguisticOntologyV2Error):
        ReferencedFunctionalLicense(
            license_id="lic-1",
            candidate_ref=_license("x", base=_base()).candidate_ref,
            function_ref=LinguisticFunctionRef(
                function=LinguisticFunction.TERM_ANCHOR_ROLE, read_from="قراءة"
            ),
            condition_ref="شرطٌ مذكورٌ نثرًا",  # type: ignore[arg-type]
        )


def test_a_license_whose_condition_comes_from_another_base_is_refused() -> None:
    general = _general()
    stranger = _base("pk0-other")
    with pytest.raises(LinguisticOntologyV2Error) as refusal:
        LinguisticOntologyV2.founded_on(
            "ol2-test", general, (_license("lic-foreign", base=stranger),)
        )
    assert "lic-foreign" in str(refusal.value)


def test_a_base_of_the_same_name_and_another_digest_is_another_base() -> None:
    base = _base()
    twin = _base(domain_note="مجالٌ آخر")
    assert twin.base_id == base.base_id
    assert twin.content_id != base.content_id
    with pytest.raises(LinguisticOntologyV2Error):
        LinguisticOntologyV2.founded_on(
            "ol2-test", _general(base), (_license("lic-twin", base=twin),)
        )


def test_every_offending_license_is_named_not_only_the_first() -> None:
    stranger = _base("pk0-other")
    with pytest.raises(LinguisticOntologyV2Error) as refusal:
        LinguisticOntologyV2.founded_on(
            "ol2-test",
            _general(),
            (
                _license("lic-a", base=stranger),
                _license("lic-b", base=stranger),
            ),
        )
    message = str(refusal.value)
    assert "lic-a" in message and "lic-b" in message


def test_a_license_for_an_unregistered_candidate_is_refused() -> None:
    base = _base()
    granted = ReferencedFunctionalLicense(
        license_id="lic-ghost",
        candidate_ref=_license("x", base=base).candidate_ref.__class__(
            candidate_id="cand-ghost", kind_name="thing"
        ),
        function_ref=LinguisticFunctionRef(
            function=LinguisticFunction.TERM_ANCHOR_ROLE, read_from="قراءة"
        ),
        condition_ref=PriorConditionRef.of(base, PriorConditionKind.DOMAIN),
    )
    with pytest.raises(LinguisticOntologyV2Error) as refusal:
        LinguisticOntologyV2.founded_on("ol2-test", _general(base), (granted,))
    assert "lic-ghost" in str(refusal.value)


def test_a_license_disagreeing_with_the_registered_kind_is_refused() -> None:
    base = _base()
    granted = ReferencedFunctionalLicense(
        license_id="lic-mismatch",
        candidate_ref=_license("x", base=base).candidate_ref.__class__(
            candidate_id="cand-thing", kind_name="relation"
        ),
        function_ref=LinguisticFunctionRef(
            function=LinguisticFunction.TERM_ANCHOR_ROLE, read_from="قراءة"
        ),
        condition_ref=PriorConditionRef.of(base, PriorConditionKind.DOMAIN),
    )
    with pytest.raises(LinguisticOntologyV2Error) as refusal:
        LinguisticOntologyV2.founded_on("ol2-test", _general(base), (granted,))
    assert "lic-mismatch" in str(refusal.value)


def test_the_new_ontology_carries_the_base_of_its_general_ontology() -> None:
    base = _base()
    general = _general(base)
    ontology = LinguisticOntologyV2.founded_on(
        "ol2-test", general, (_license("lic-1", base=base),)
    )
    assert ontology.prior_base_ref == general.prior_base_ref
    assert ontology.general_content_id == general.content_id
    assert ontology.content_id != general.content_id


def test_a_duplicated_license_identifier_is_refused() -> None:
    base = _base()
    with pytest.raises(LinguisticOntologyV2Error):
        LinguisticOntologyV2.founded_on(
            "ol2-test",
            _general(base),
            (_license("lic-1", base=base), _license("lic-1", base=base)),
        )


def test_licenses_are_readable_by_function_and_by_identifier() -> None:
    base = _base()
    anchor = _license("lic-anchor", base=base)
    predicate = _license(
        "lic-pred",
        base=base,
        kind=OntologicalKind.RELATION,
        function=LinguisticFunction.PREDICATE_ROLE,
    )
    ontology = LinguisticOntologyV2.founded_on(
        "ol2-test", _general(base), (anchor, predicate)
    )
    assert ontology.licenses_for(LinguisticFunction.PREDICATE_ROLE) == (predicate,)
    assert ontology.license("lic-anchor") is anchor
    with pytest.raises(LinguisticOntologyV2Error):
        ontology.license("lic-absent")


def test_the_first_linguistic_ontology_is_untouched_by_this_module() -> None:
    from alghanem.ontology import linguistic as first

    assert "condition_statement" in {
        item.name for item in fields(first.FunctionalLicense)
    }
    assert "prior_base_ref" not in {
        item.name for item in fields(first.LinguisticOntology)
    }
