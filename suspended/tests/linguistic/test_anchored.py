"""شواهدُ `v2`: الدورُ رخصةٌ لا أصلٌ، والشرطُ مرجعٌ لا نثرٌ حرّ، و`v1` قائم."""

from __future__ import annotations

from dataclasses import fields

import pytest

from alghanem.linguistic.anchored import (
    ANCHORED_NISBAH_SCHEMA,
    ANCHORED_SCHEMA_VERSION,
    AnchoredArgumentSlot,
    AnchoredLayerError,
    AnchoredNisbahSchema,
    AnchoredNisbahSignature,
    AnchoredPredicateSignature,
    AnchoredTermAnchor,
    BaseSchemaRef,
    LicensedConditionRef,
    LicensedRoleRef,
)
from alghanem.linguistic.nisbah import ArityLicenseGenus, TermAnchorKind
from alghanem.linguistic.schema import LINGUISTIC_NISBAH_SCHEMA, SCHEMA_VERSION
from alghanem.ontology.general import (
    GeneralOntology,
    OntologicalCandidate,
    OntologicalKind,
)
from alghanem.ontology.linguistic import (
    FunctionalLicense,
    LinguisticFunction,
    LinguisticFunctionRef,
    LinguisticOntology,
    OntologicalCandidateRef,
)
from alghanem.prior.conditions import (
    PriorCondition,
    PriorConditionKind,
    PriorInformationBase,
    PriorLicenseGenus,
)


def _base(
    unusable: PriorConditionKind | None = None,
) -> PriorInformationBase:
    return PriorInformationBase(
        base_id="pk0-anchored-test",
        domain_note="مجالٌ صوريٌّ للاختبار",
        conditions=tuple(
            PriorCondition(
                condition_id=f"c-{kind.value}",
                kind=kind,
                statement=f"شرطُ {kind.value}",
                what_it_forbids=f"ما يخالف {kind.value}",
                licensed_by=(
                    PriorLicenseGenus.UNREAD
                    if kind is unusable
                    else PriorLicenseGenus.STIPULATED_FOR_THE_DOMAIN
                ),
            )
            for kind in PriorConditionKind
        ),
    )


def _general(base: PriorInformationBase) -> GeneralOntology:
    return GeneralOntology.founded_on(
        ontology_id="o0-anchored-test",
        base=base,
        candidates=tuple(
            OntologicalCandidate(
                candidate_id=f"cand-{kind.value}",
                kind=kind,
                necessity_claim=f"لا يُستغنى عن {kind.value}",
                irreducibility_claim=f"لا يُرَدّ {kind.value} إلى غيره",
                licensing_condition=PriorConditionKind.IDENTITY_CRITERION,
            )
            for kind in (OntologicalKind.THING, OntologicalKind.EVENT)
        ),
    )


def _license(
    license_id: str,
    kind: OntologicalKind,
    function: LinguisticFunction,
    general: GeneralOntology,
) -> FunctionalLicense:
    return FunctionalLicense(
        license_id=license_id,
        candidate_ref=OntologicalCandidateRef.of(
            general.candidate(f"cand-{kind.value}")
        ),
        function_ref=LinguisticFunctionRef(function=function, read_from="شاهدٌ صوريّ"),
        licensing_condition=PriorConditionKind.IDENTITY_CRITERION,
        condition_statement=f"يؤدّي {kind.value} وظيفةَ {function.value} بشرطٍ ناقض",
    )


def _ontology(general: GeneralOntology) -> LinguisticOntology:
    return LinguisticOntology.founded_on(
        ontology_id="ol-anchored-test",
        general=general,
        licenses=(
            _license(
                "lic-anchor",
                OntologicalKind.THING,
                LinguisticFunction.TERM_ANCHOR_ROLE,
                general,
            ),
            _license(
                "lic-predicate",
                OntologicalKind.EVENT,
                LinguisticFunction.PREDICATE_ROLE,
                general,
            ),
            FunctionalLicense(
                license_id="lic-unread",
                candidate_ref=OntologicalCandidateRef.of(
                    general.candidate("cand-thing")
                ),
                function_ref=LinguisticFunctionRef(
                    function=LinguisticFunction.UNREAD, read_from="لم تُقرَأ بعد"
                ),
                licensing_condition=PriorConditionKind.DOMAIN,
                condition_statement="وظيفةٌ لم تُقرَأ، وتُسجَّل غيابًا لا استيفاءً",
            ),
        ),
    )


def _nisbah() -> AnchoredNisbahSignature:
    base = _base()
    ontology = _ontology(_general(base))
    slot = AnchoredArgumentSlot(
        slot_id="slot-1",
        position=1,
        admissibility_condition_ref=LicensedConditionRef.of(
            base, PriorConditionKind.RELATION_POSSIBILITY
        ),
    )
    predicate = AnchoredPredicateSignature(
        predicate_id="p-1",
        role_ref=LicensedRoleRef.of(
            ontology, "lic-predicate", LinguisticFunction.PREDICATE_ROLE
        ),
        arity=1,
        arity_license=ArityLicenseGenus.PRIOR_SPECIFICATION,
        slots=(slot,),
    )
    anchor = AnchoredTermAnchor(
        anchor_id="a-1",
        role_ref=LicensedRoleRef.of(
            ontology, "lic-anchor", LinguisticFunction.TERM_ANCHOR_ROLE
        ),
        identity_condition_ref=LicensedConditionRef.of(
            base, PriorConditionKind.IDENTITY_CRITERION
        ),
    )
    return AnchoredNisbahSignature.licensed_by(
        nisbah_id="n-1",
        ontology=ontology,
        predicate=predicate,
        anchors=(anchor,),
    )


def test_a_role_is_a_license_not_a_written_kind() -> None:
    for owner in (AnchoredTermAnchor, AnchoredPredicateSignature):
        annotations = {field.name: str(field.type) for field in fields(owner)}
        assert TermAnchorKind.__name__ not in " ".join(annotations.values())
        assert "LicensedRoleRef" in annotations["role_ref"]


def test_a_license_granted_for_another_function_is_refused() -> None:
    ontology = _ontology(_general(_base()))
    with pytest.raises(AnchoredLayerError):
        LicensedRoleRef.of(
            ontology, "lic-predicate", LinguisticFunction.TERM_ANCHOR_ROLE
        )


def test_an_unread_license_is_not_read_as_operative() -> None:
    ontology = _ontology(_general(_base()))
    with pytest.raises(AnchoredLayerError):
        LicensedRoleRef.of(ontology, "lic-unread", LinguisticFunction.UNREAD)


def test_an_absent_license_is_refused_not_silently_skipped() -> None:
    ontology = _ontology(_general(_base()))
    with pytest.raises(AnchoredLayerError):
        LicensedRoleRef.of(
            ontology, "lic-not-registered", LinguisticFunction.TERM_ANCHOR_ROLE
        )


def test_a_role_ref_is_derived_from_the_ontology_not_written_beside_it() -> None:
    ontology = _ontology(_general(_base()))
    role = LicensedRoleRef.of(
        ontology, "lic-anchor", LinguisticFunction.TERM_ANCHOR_ROLE
    )
    assert role.ontology_content_id == ontology.content_id
    assert role.candidate_id == "cand-thing"
    with pytest.raises(AnchoredLayerError):
        LicensedRoleRef.of(
            "ol-anchored-test",  # type: ignore[arg-type]
            "lic-anchor",
            LinguisticFunction.TERM_ANCHOR_ROLE,
        )


def test_a_condition_is_a_bound_reference_not_free_text() -> None:
    base = _base()
    ref = LicensedConditionRef.of(base, PriorConditionKind.IDENTITY_CRITERION)
    assert ref.condition_id == "c-identity_criterion"
    assert ref.base_content_id == base.content_id
    for owner in (AnchoredTermAnchor, AnchoredArgumentSlot):
        for field in fields(owner):
            if "condition" in field.name:
                assert "LicensedConditionRef" in str(field.type)


def test_an_unlicensed_condition_founds_no_anchor() -> None:
    base = _base(unusable=PriorConditionKind.IDENTITY_CRITERION)
    with pytest.raises(AnchoredLayerError):
        LicensedConditionRef.of(base, PriorConditionKind.IDENTITY_CRITERION)


def test_a_condition_reference_is_not_built_from_a_free_name() -> None:
    with pytest.raises(AnchoredLayerError):
        LicensedConditionRef.of(
            "pk0-anchored-test",  # type: ignore[arg-type]
            PriorConditionKind.DOMAIN,
        )


def test_a_free_text_condition_is_refused_at_construction() -> None:
    base = _base()
    ontology = _ontology(_general(base))
    role = LicensedRoleRef.of(
        ontology, "lic-anchor", LinguisticFunction.TERM_ANCHOR_ROLE
    )
    with pytest.raises(AnchoredLayerError):
        AnchoredTermAnchor(
            anchor_id="a-free",
            role_ref=role,
            identity_condition_ref="الطرفُ محفوظُ الهويّة",  # type: ignore[arg-type]
        )
    with pytest.raises(AnchoredLayerError):
        AnchoredArgumentSlot(
            slot_id="slot-free",
            position=1,
            admissibility_condition_ref="ما يقع في الموضع",  # type: ignore[arg-type]
        )


def test_deferred_argument_role_names_are_still_refused() -> None:
    base = _base()
    ref = LicensedConditionRef.of(base, PriorConditionKind.RELATION_POSSIBILITY)
    with pytest.raises(AnchoredLayerError):
        AnchoredArgumentSlot(
            slot_id="agent-slot", position=1, admissibility_condition_ref=ref
        )


def test_an_arity_read_off_the_target_state_does_not_license_use() -> None:
    base = _base()
    ontology = _ontology(_general(base))
    slot = AnchoredArgumentSlot(
        slot_id="slot-1",
        position=1,
        admissibility_condition_ref=LicensedConditionRef.of(
            base, PriorConditionKind.RELATION_POSSIBILITY
        ),
    )
    with pytest.raises(AnchoredLayerError):
        AnchoredPredicateSignature(
            predicate_id="p-bad",
            role_ref=LicensedRoleRef.of(
                ontology, "lic-predicate", LinguisticFunction.PREDICATE_ROLE
            ),
            arity=1,
            arity_license=ArityLicenseGenus.DERIVED_FROM_THE_TARGET_STATE,
            slots=(slot,),
        )


def test_a_license_of_another_ontology_is_refused() -> None:
    nisbah = _nisbah()
    with pytest.raises(AnchoredLayerError):
        AnchoredNisbahSignature(
            nisbah_id="n-mixed",
            ontology_content_id="بصمةٌ أخرى",
            predicate=nisbah.predicate,
            anchors=nisbah.anchors,
        )


def test_arguments_closed_is_one_component_not_the_closure() -> None:
    nisbah = _nisbah()
    assert nisbah.are_arguments_closed is True
    assert nisbah.unfilled_slot_count == 0
    assert "closure" not in nisbah.as_canonical_content()


def test_the_nisbah_digest_is_content_bound() -> None:
    first = _nisbah()
    second = _nisbah()
    assert first.content_id == second.content_id
    assert len(first.content_id) == 64


def test_more_anchors_than_arity_is_a_term_without_a_slot() -> None:
    nisbah = _nisbah()
    extra = AnchoredTermAnchor(
        anchor_id="a-2",
        role_ref=nisbah.anchors[0].role_ref,
        identity_condition_ref=nisbah.anchors[0].identity_condition_ref,
    )
    with pytest.raises(AnchoredLayerError):
        AnchoredNisbahSignature(
            nisbah_id="n-overfull",
            ontology_content_id=nisbah.ontology_content_id,
            predicate=nisbah.predicate,
            anchors=(nisbah.anchors[0], extra),
        )


def test_v2_stands_beside_v1_and_is_bound_to_its_digest() -> None:
    assert ANCHORED_SCHEMA_VERSION == "linguistic-nisbah.schema.v2"
    assert SCHEMA_VERSION == "linguistic-nisbah.schema.v1"
    assert ANCHORED_SCHEMA_VERSION != SCHEMA_VERSION
    assert ANCHORED_NISBAH_SCHEMA.base_schema_ref == BaseSchemaRef(
        schema_version=SCHEMA_VERSION,
        content_id=LINGUISTIC_NISBAH_SCHEMA.content_id,
    )
    assert ANCHORED_NISBAH_SCHEMA.content_id != LINGUISTIC_NISBAH_SCHEMA.content_id


def test_a_schema_bound_to_another_v1_digest_is_refused() -> None:
    with pytest.raises(AnchoredLayerError):
        AnchoredNisbahSchema(
            schema_version=ANCHORED_SCHEMA_VERSION,
            base_schema_ref=BaseSchemaRef(
                schema_version=SCHEMA_VERSION, content_id="بصمةٌ لم تَعُد قائمة"
            ),
            ontology_bound=True,
        )


def test_a_version_that_reuses_the_v1_name_is_refused() -> None:
    with pytest.raises(AnchoredLayerError):
        AnchoredNisbahSchema(
            schema_version=SCHEMA_VERSION,
            base_schema_ref=BaseSchemaRef.of(),
            ontology_bound=True,
        )


def test_an_unbound_schema_is_v1_under_another_name() -> None:
    with pytest.raises(AnchoredLayerError):
        AnchoredNisbahSchema(
            schema_version=ANCHORED_SCHEMA_VERSION,
            base_schema_ref=BaseSchemaRef.of(),
            ontology_bound=False,
        )


def test_the_anchored_layer_holds_no_concrete_arabic_nisbah() -> None:
    content = ANCHORED_NISBAH_SCHEMA.as_canonical_content()
    rendered = str(content)
    for forbidden in ("زيد", "قام", "arabic", "root"):
        assert forbidden not in rendered
