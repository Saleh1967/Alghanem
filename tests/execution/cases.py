"""بُناةُ حالاتٍ للاختبار: وثائقُ تصريحٍ كاملةٌ تُبنى من مفرداتٍ مغلقة.

هذه الوحدةُ **مادّةُ اختبارٍ لا جزءٌ من المحرّك**: تُنتِج وثيقةَ `JSON` صالحةً
ثمّ تُغيَّر فيها قيمةٌ واحدةٌ في الاختبارات المضادّة، ليُعرَف بالضبط أيُّ تغييرٍ
يُنتِج أيَّ حكم.

تسجيلٌ لا سلطة: لا ولادةَ ولا حكمَ ولادةٍ ولا تجميدَ `E0`.
"""

from __future__ import annotations

import copy
from typing import Any

from alghanem.linguistic.anchored_v3 import ANCHORED_V3_SCHEMA_VERSION
from alghanem.ontology.general import GeneralOntology, OntologicalKind, PriorBaseRef
from alghanem.prior.conditions import (
    PriorCondition,
    PriorConditionKind,
    PriorInformationBase,
    PriorLicenseGenus,
)

Document = dict[str, Any]

USABLE_GENUS = PriorLicenseGenus.STIPULATED_FOR_THE_DOMAIN


def condition_declaration(
    base_id: str,
    kind: PriorConditionKind,
    genus: PriorLicenseGenus = USABLE_GENUS,
) -> Document:
    """شرطٌ مُصرَّحٌ به في موضعٍ واحدٍ من مواضع `PK_0` التسعة."""

    return {
        "condition_id": f"{base_id}.{kind.value}",
        "kind": kind.value,
        "statement": f"بيانُ {kind.value} في {base_id}",
        "what_it_forbids": f"ما يمنعه {kind.value} في {base_id}",
        "licensed_by": genus.value,
    }


def _base_object(
    base_id: str, overrides: dict[PriorConditionKind, PriorLicenseGenus]
) -> PriorInformationBase:
    return PriorInformationBase(
        base_id=base_id,
        domain_note=f"مجالُ {base_id}",
        conditions=tuple(
            PriorCondition(
                condition_id=f"{base_id}.{kind.value}",
                kind=kind,
                statement=f"بيانُ {kind.value} في {base_id}",
                what_it_forbids=f"ما يمنعه {kind.value} في {base_id}",
                licensed_by=overrides.get(kind, USABLE_GENUS),
            )
            for kind in PriorConditionKind
        ),
    )


def base_declaration(
    base_id: str,
    overrides: dict[PriorConditionKind, PriorLicenseGenus] | None = None,
) -> Document:
    """قاعدةٌ سابقةٌ مُصرَّحٌ بها، مبصومةٌ ببصمتها المُعاد حسابُها."""

    resolved = overrides or {}
    base = _base_object(base_id, resolved)
    return {
        "base_id": base_id,
        "domain_note": f"مجالُ {base_id}",
        "declared_content_id": base.content_id,
        "conditions": [
            condition_declaration(base_id, kind, resolved.get(kind, USABLE_GENUS))
            for kind in PriorConditionKind
        ],
    }


def candidate_declaration(candidate_id: str, kind: OntologicalKind) -> Document:
    """مرشَّحٌ أنطولوجيٌّ مُصرَّحٌ به في `O_0`."""

    return {
        "candidate_id": candidate_id,
        "kind": kind.value,
        "necessity_claim": f"دعوى لزوم {candidate_id}",
        "irreducibility_claim": f"دعوى عدم ارتداد {candidate_id}",
        "licensing_condition": PriorConditionKind.DOMAIN.value,
    }


def general_declaration(
    ontology_id: str,
    base_id: str,
    overrides: dict[PriorConditionKind, PriorLicenseGenus] | None = None,
) -> Document:
    """أنطولوجيا عامّةٌ مُصرَّحٌ بها، مبصومةٌ ببصمتها المُعاد حسابُها."""

    resolved = overrides or {}
    base = _base_object(base_id, resolved)
    candidates = (
        ("cand.predicate", OntologicalKind.RELATION),
        ("cand.term", OntologicalKind.THING),
    )
    general = GeneralOntology(
        ontology_id=ontology_id,
        prior_base_ref=PriorBaseRef.of(base),
        candidates=tuple(
            _candidate_object(candidate_id, kind) for candidate_id, kind in candidates
        ),
    )
    return {
        "ontology_id": ontology_id,
        "founded_on_base_id": base_id,
        "declared_content_id": general.content_id,
        "candidates": [
            candidate_declaration(candidate_id, kind)
            for candidate_id, kind in candidates
        ],
    }


def _candidate_object(candidate_id: str, kind: OntologicalKind) -> Any:
    from alghanem.ontology.general import OntologicalCandidate

    return OntologicalCandidate(
        candidate_id=candidate_id,
        kind=kind,
        necessity_claim=f"دعوى لزوم {candidate_id}",
        irreducibility_claim=f"دعوى عدم ارتداد {candidate_id}",
        licensing_condition=PriorConditionKind.DOMAIN,
    )


def valid_document(base_id: str = "base.A", general_id: str = "general.A") -> Document:
    """حالةٌ واحدةُ الأصل، كاملةُ العناصر، يُتوقَّع منها `PASS`."""

    return {
        "schema": "alghanem.execution.v1",
        "nisbah_schema": ANCHORED_V3_SCHEMA_VERSION,
        "prior_bases": [base_declaration(base_id)],
        "general_ontologies": [general_declaration(general_id, base_id)],
        "linguistic_ontologies": [
            {
                "ontology_id": "linguistic.A",
                "founded_on_general_id": general_id,
                "declared_content_id": None,
                "licenses": [
                    {
                        "license_id": "license.predicate",
                        "candidate_id": "cand.predicate",
                        "function": "predicate_role",
                        "read_from": "قراءةٌ مُسجَّلة",
                        "condition_base_id": base_id,
                        "condition_place": PriorConditionKind.RELATION_POSSIBILITY.value,
                    },
                    {
                        "license_id": "license.term",
                        "candidate_id": "cand.term",
                        "function": "term_anchor_role",
                        "read_from": "قراءةٌ مُسجَّلة",
                        "condition_base_id": base_id,
                        "condition_place": PriorConditionKind.UNIT_CRITERION.value,
                    },
                ],
            }
        ],
        "lineage": {
            "base_id": base_id,
            "general_ontology_id": general_id,
            "linguistic_ontology_id": "linguistic.A",
        },
        "nisbah": {
            "nisbah_id": "nisbah.A",
            "declared_content_id": None,
            "predicate": {
                "predicate_id": "predicate.A",
                "arity": 2,
                "arity_license": "prior_specification",
                "role_site": {
                    "linguistic_ontology_id": "linguistic.A",
                    "license_id": "license.predicate",
                    "function": "predicate_role",
                },
                "slots": [
                    {
                        "slot_id": "site.first",
                        "position": 1,
                        "condition_site": {
                            "base_id": base_id,
                            "place": (
                                PriorConditionKind.ATTRIBUTE_POSSIBILITY.value
                            ),
                        },
                    },
                    {
                        "slot_id": "site.second",
                        "position": 2,
                        "condition_site": {
                            "base_id": base_id,
                            "place": (
                                PriorConditionKind.CONDITIONS_AND_PREVENTERS.value
                            ),
                        },
                    },
                ],
            },
            "anchors": [
                {
                    "anchor_id": "anchor.first",
                    "role_site": {
                        "linguistic_ontology_id": "linguistic.A",
                        "license_id": "license.term",
                        "function": "term_anchor_role",
                    },
                    "condition_site": {
                        "base_id": base_id,
                        "place": PriorConditionKind.IDENTITY_CRITERION.value,
                    },
                }
            ],
        },
        "unresolved_requirements": [],
    }


def mutate(document: Document) -> Document:
    """نسخةٌ عميقةٌ تُغيَّر فيها قيمةٌ واحدةٌ دون أن تُمَسّ الأصل."""

    return copy.deepcopy(document)
