"""شواهدُ `v3`: الدورُ وشرطُه من سلسلةٍ واحدة، و`v3` بجانب `v2` لا فوقها."""

from __future__ import annotations

from dataclasses import fields

import pytest

from alghanem.linguistic.anchored import ANCHORED_NISBAH_SCHEMA
from alghanem.linguistic.anchored_v3 import (
    ANCHORED_V3_NISBAH_SCHEMA,
    ANCHORED_V3_SCHEMA_VERSION,
    PARENT_SCHEMA_CONTENT_ID,
    AnchoredArgumentSlotV3,
    AnchoredNisbahSchemaV3,
    AnchoredNisbahSignatureV3,
    AnchoredPredicateSignatureV3,
    AnchoredTermAnchorV3,
    AnchoredV3Error,
    BaseSchemaRefV3,
    LicensedRoleRefV3,
)
from alghanem.linguistic.nisbah import (
    DEFERRED_ARGUMENT_ROLE_NAMES,
    ArityLicenseGenus,
    TermAnchorKind,
)
from alghanem.ontology.general import (
    GeneralOntology,
    OntologicalCandidate,
    OntologicalKind,
)
from alghanem.ontology.lineage import ExistenceLineageRef
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
from alghanem.prior.references import PriorConditionRef

_THING = OntologicalCandidate(
    candidate_id="cand-thing",
    kind=OntologicalKind.THING,
    necessity_claim="لا يُستغنى عن الشيء",
    irreducibility_claim="لا يُرَدّ الشيء إلى غيره",
    licensing_condition=PriorConditionKind.IDENTITY_CRITERION,
)
_RELATION = OntologicalCandidate(
    candidate_id="cand-relation",
    kind=OntologicalKind.RELATION,
    necessity_claim="لا يُستغنى عن النسبة",
    irreducibility_claim="لا تُرَدّ النسبة إلى غيرها",
    licensing_condition=PriorConditionKind.RELATION_POSSIBILITY,
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


def _general(base: PriorInformationBase) -> GeneralOntology:
    return GeneralOntology.founded_on("o0-test", base, (_THING, _RELATION))


def _linguistic(
    general: GeneralOntology, base: PriorInformationBase
) -> LinguisticOntologyV2:
    return LinguisticOntologyV2.founded_on(
        "ol2-test",
        general,
        (
            ReferencedFunctionalLicense.granted(
                "lic-anchor",
                _THING,
                LinguisticFunction.TERM_ANCHOR_ROLE,
                "قراءةٌ صوريّة",
                base,
                PriorConditionKind.DOMAIN,
            ),
            ReferencedFunctionalLicense.granted(
                "lic-pred",
                _RELATION,
                LinguisticFunction.PREDICATE_ROLE,
                "قراءةٌ صوريّة",
                base,
                PriorConditionKind.RELATION_POSSIBILITY,
            ),
        ),
    )


def _predicate(
    ontology: LinguisticOntologyV2, base: PriorInformationBase
) -> AnchoredPredicateSignatureV3:
    return AnchoredPredicateSignatureV3(
        predicate_id="pred-1",
        role_ref=LicensedRoleRefV3.of(
            ontology, "lic-pred", LinguisticFunction.PREDICATE_ROLE
        ),
        arity=1,
        arity_license=ArityLicenseGenus.LEXICAL_SOURCE,
        slots=(
            AnchoredArgumentSlotV3(
                slot_id="slot-1",
                position=1,
                admissibility_condition_ref=PriorConditionRef.of(
                    base, PriorConditionKind.UNIT_CRITERION
                ),
            ),
        ),
    )


def _anchor(
    ontology: LinguisticOntologyV2,
    base: PriorInformationBase,
    anchor_id: str = "anchor-1",
) -> AnchoredTermAnchorV3:
    return AnchoredTermAnchorV3(
        anchor_id=anchor_id,
        role_ref=LicensedRoleRefV3.of(
            ontology, "lic-anchor", LinguisticFunction.TERM_ANCHOR_ROLE
        ),
        identity_condition_ref=PriorConditionRef.of(
            base, PriorConditionKind.IDENTITY_CRITERION
        ),
    )


def test_a_nisbah_stands_when_role_and_condition_share_one_lineage() -> None:
    base = _base()
    general = _general(base)
    ontology = _linguistic(general, base)
    lineage = ExistenceLineageRef.of(general, ontology)
    nisbah = AnchoredNisbahSignatureV3.in_lineage(
        "nisbah-1", lineage, _predicate(ontology, base), (_anchor(ontology, base),)
    )
    assert nisbah.are_arguments_closed is True
    assert nisbah.unfilled_slot_count == 0
    assert nisbah.lineage_ref is lineage


def test_a_condition_from_another_existence_path_is_refused() -> None:
    base = _base()
    general = _general(base)
    ontology = _linguistic(general, base)
    lineage = ExistenceLineageRef.of(general, ontology)
    stranger = _base("pk0-other")
    foreign_anchor = AnchoredTermAnchorV3(
        anchor_id="anchor-foreign",
        role_ref=_anchor(ontology, base).role_ref,
        identity_condition_ref=PriorConditionRef.of(
            stranger, PriorConditionKind.IDENTITY_CRITERION
        ),
    )
    with pytest.raises(AnchoredV3Error) as refusal:
        AnchoredNisbahSignatureV3.in_lineage(
            "nisbah-1", lineage, _predicate(ontology, base), (foreign_anchor,)
        )
    assert "anchor-foreign" in str(refusal.value)


def test_every_foreign_role_and_every_foreign_condition_is_named() -> None:
    base = _base()
    general = _general(base)
    ontology = _linguistic(general, base)
    lineage = ExistenceLineageRef.of(general, ontology)
    stranger_base = _base("pk0-other")
    stranger_general = _general(stranger_base)
    stranger_ontology = _linguistic(stranger_general, stranger_base)
    foreign_predicate = _predicate(stranger_ontology, stranger_base)
    foreign_anchor = _anchor(stranger_ontology, stranger_base, "anchor-foreign")
    with pytest.raises(AnchoredV3Error) as refusal:
        AnchoredNisbahSignatureV3.in_lineage(
            "nisbah-1", lineage, foreign_predicate, (foreign_anchor,)
        )
    message = str(refusal.value)
    assert "pred-1" in message
    assert "anchor-foreign" in message
    assert "slot-1" in message


def test_the_second_version_admits_what_the_third_refuses() -> None:
    """الشاهدُ المزدوج: خلطُ المسارين يمرّ في `v2` ويُرفَض في `v3`."""

    from alghanem.linguistic.anchored import (
        AnchoredArgumentSlot as AnchoredArgumentSlotV2,
    )
    from alghanem.linguistic.anchored import (
        AnchoredNisbahSignature,
        AnchoredTermAnchor,
        LicensedConditionRef,
        LicensedRoleRef,
    )
    from alghanem.linguistic.anchored import (
        AnchoredPredicateSignature as AnchoredPredicateSignatureV2,
    )

    base = _base()
    general = _general(base)
    ontology = _linguistic(general, base)
    stranger = _base("pk0-other")
    first_ontology = _first_linguistic_ontology(general)
    predicate_v2 = AnchoredPredicateSignatureV2(
        predicate_id="pred-1",
        role_ref=LicensedRoleRef.of(
            first_ontology, "lic-pred", LinguisticFunction.PREDICATE_ROLE
        ),
        arity=1,
        arity_license=ArityLicenseGenus.LEXICAL_SOURCE,
        slots=(
            AnchoredArgumentSlotV2(
                slot_id="slot-1",
                position=1,
                admissibility_condition_ref=LicensedConditionRef.of(
                    base, PriorConditionKind.UNIT_CRITERION
                ),
            ),
        ),
    )
    anchor_v2 = AnchoredTermAnchor(
        anchor_id="anchor-1",
        role_ref=LicensedRoleRef.of(
            first_ontology, "lic-anchor", LinguisticFunction.TERM_ANCHOR_ROLE
        ),
        identity_condition_ref=LicensedConditionRef.of(
            stranger, PriorConditionKind.IDENTITY_CRITERION
        ),
    )
    admitted = AnchoredNisbahSignature(
        nisbah_id="nisbah-1",
        ontology_content_id=first_ontology.content_id,
        predicate=predicate_v2,
        anchors=(anchor_v2,),
    )
    assert admitted.are_arguments_closed is True

    lineage = ExistenceLineageRef.of(general, ontology)
    refused_anchor = AnchoredTermAnchorV3(
        anchor_id="anchor-1",
        role_ref=_anchor(ontology, base).role_ref,
        identity_condition_ref=PriorConditionRef.of(
            stranger, PriorConditionKind.IDENTITY_CRITERION
        ),
    )
    with pytest.raises(AnchoredV3Error):
        AnchoredNisbahSignatureV3.in_lineage(
            "nisbah-1", lineage, _predicate(ontology, base), (refused_anchor,)
        )


def _first_linguistic_ontology(general: GeneralOntology) -> object:
    from alghanem.ontology.linguistic import (
        FunctionalLicense,
        LinguisticFunctionRef,
        LinguisticOntology,
        OntologicalCandidateRef,
    )

    def _license(
        license_id: str,
        candidate: OntologicalCandidate,
        function: LinguisticFunction,
        place: PriorConditionKind,
    ) -> FunctionalLicense:
        return FunctionalLicense(
            license_id=license_id,
            candidate_ref=OntologicalCandidateRef(
                candidate_id=candidate.candidate_id, kind_name=candidate.kind.value
            ),
            function_ref=LinguisticFunctionRef(
                function=function, read_from="قراءةٌ صوريّة"
            ),
            licensing_condition=place,
            condition_statement="بيانُ الشرط نثرًا",
        )

    return LinguisticOntology.founded_on(
        "ol-first",
        general,
        (
            _license(
                "lic-anchor",
                _THING,
                LinguisticFunction.TERM_ANCHOR_ROLE,
                PriorConditionKind.DOMAIN,
            ),
            _license(
                "lic-pred",
                _RELATION,
                LinguisticFunction.PREDICATE_ROLE,
                PriorConditionKind.RELATION_POSSIBILITY,
            ),
        ),
    )


def test_a_lineage_written_by_hand_issues_no_nisbah() -> None:
    base = _base()
    general = _general(base)
    ontology = _linguistic(general, base)
    with pytest.raises(AnchoredV3Error):
        AnchoredNisbahSignatureV3(
            nisbah_id="nisbah-1",
            lineage_ref="سلسلةٌ مكتوبة",  # type: ignore[arg-type]
            predicate=_predicate(ontology, base),
            anchors=(_anchor(ontology, base),),
        )


def test_no_written_kind_and_no_free_text_condition_in_this_layer() -> None:
    anchor_fields = {item.name: item.type for item in fields(AnchoredTermAnchorV3)}
    assert "kind" not in anchor_fields
    assert "identity_condition" not in anchor_fields
    assert TermAnchorKind.__name__ not in " ".join(
        str(v) for v in anchor_fields.values()
    )
    slot_fields = {item.name for item in fields(AnchoredArgumentSlotV3)}
    assert "admissibility_condition" not in slot_fields


def test_a_deferred_role_name_is_still_refused() -> None:
    base = _base()
    deferred = next(iter(DEFERRED_ARGUMENT_ROLE_NAMES))
    with pytest.raises(AnchoredV3Error):
        AnchoredArgumentSlotV3(
            slot_id=deferred,
            position=1,
            admissibility_condition_ref=PriorConditionRef.of(
                base, PriorConditionKind.UNIT_CRITERION
            ),
        )


def test_a_role_reference_names_an_operative_license_only() -> None:
    base = _base()
    general = _general(base)
    ontology = _linguistic(general, base)
    with pytest.raises(AnchoredV3Error):
        LicensedRoleRefV3.of(ontology, "lic-anchor", LinguisticFunction.PREDICATE_ROLE)
    with pytest.raises(AnchoredV3Error):
        LicensedRoleRefV3.of(ontology, "lic-absent", LinguisticFunction.PREDICATE_ROLE)


def test_the_third_schema_reads_the_identity_of_the_second_not_its_name() -> None:
    assert ANCHORED_V3_NISBAH_SCHEMA.schema_version == ANCHORED_V3_SCHEMA_VERSION
    assert ANCHORED_V3_SCHEMA_VERSION != ANCHORED_NISBAH_SCHEMA.schema_version
    reference = ANCHORED_V3_NISBAH_SCHEMA.base_schema_ref
    assert reference.base_schema_id == ANCHORED_NISBAH_SCHEMA.schema_version
    assert reference.base_schema_content_id == ANCHORED_NISBAH_SCHEMA.content_id
    assert PARENT_SCHEMA_CONTENT_ID == ANCHORED_NISBAH_SCHEMA.content_id
    assert ANCHORED_V3_NISBAH_SCHEMA.content_id != ANCHORED_NISBAH_SCHEMA.content_id


def test_a_schema_that_carries_the_name_of_its_parent_is_refused() -> None:
    with pytest.raises(AnchoredV3Error):
        AnchoredNisbahSchemaV3(
            schema_version=ANCHORED_NISBAH_SCHEMA.schema_version,
            base_schema_ref=BaseSchemaRefV3.of(ANCHORED_NISBAH_SCHEMA),
            lineage_bound=True,
        )


def test_a_schema_not_bound_to_a_lineage_is_refused() -> None:
    with pytest.raises(AnchoredV3Error):
        AnchoredNisbahSchemaV3(
            schema_version=ANCHORED_V3_SCHEMA_VERSION,
            base_schema_ref=BaseSchemaRefV3.of(ANCHORED_NISBAH_SCHEMA),
            lineage_bound=False,
        )


def test_a_parent_reference_is_derived_from_a_living_parent_only() -> None:
    with pytest.raises(AnchoredV3Error):
        BaseSchemaRefV3.of(object())
    with pytest.raises(AnchoredV3Error):
        BaseSchemaRefV3(
            base_schema_id="linguistic-nisbah.schema.v2",
            base_schema_content_id="بصمةٌ مكتوبة",
        )
    from alghanem.linguistic import anchored_v3

    with pytest.raises(AnchoredV3Error):
        anchored_v3._ParentIdentityWitness()


def test_the_third_layer_issues_no_readout_either() -> None:
    from alghanem.linguistic import anchored_v3

    exported = set(anchored_v3.__all__)
    for forbidden in ("truth", "TruthValue", "readout", "Readout", "evaluate"):
        assert not any(
            forbidden.lower() in name.lower() for name in exported
        ), forbidden
