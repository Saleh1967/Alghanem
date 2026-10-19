"""عقدُ الإدخال: قراءةٌ صارمةٌ للوثيقة، رفضٌ لا ترميمٌ ولا أفضلُ جهد.

    JSON document  →  CaseDeclaration | InputFault…

لا يُرمَّم مفتاحٌ مجهول، ولا يُستنتَج حقلٌ غائب، ولا يُحوَّل نوعٌ إلى نوع. وكلُّ
عيبٍ يُسمّى بجنسه وموضعه، وتُجمَع العيوبُ كلُّها ولا يُوقَف عند أوّلها؛ فقارئٌ
يقف عند أوّل عيبٍ يُخفي عن صاحب الوثيقة بقيّةَ ما فيها.

**ولا سلطةَ تُفَكّ من نصّ**: ناتجُ هذه الوحدة تصريحٌ خامل، وليس فيه مرجعٌ
مُرخِّصٌ واحد؛ فالسلطةُ تُشتَقّ بعدَ التحقّق من الأبواب القائمة وحدَها.

تسجيلٌ لا سلطة: لا ولادةَ ولا حكمَ ولادةٍ ولا تجميدَ `E0`.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Final

from .declaration import (
    EXECUTION_DOCUMENT_SCHEMA,
    AnchorDeclaration,
    CandidateDeclaration,
    CaseDeclaration,
    ConditionSiteDeclaration,
    GeneralOntologyDeclaration,
    LicenseDeclaration,
    LineageDeclaration,
    LinguisticOntologyDeclaration,
    NisbahDeclaration,
    PredicateDeclaration,
    PriorBaseDeclaration,
    PriorConditionDeclaration,
    RoleSiteDeclaration,
    SlotDeclaration,
)
from .requirement import RequiredAuthority, RequirementStanding, UnresolvedRequirement
from .standing import InputFault, InputFaultKind

__all__ = ["DecodedDocument", "decode_document", "encode_declaration"]


_CASE_KEYS: Final[tuple[str, ...]] = (
    "schema",
    "nisbah_schema",
    "prior_bases",
    "general_ontologies",
    "linguistic_ontologies",
    "lineage",
    "nisbah",
    "unresolved_requirements",
)


@dataclass(frozen=True, slots=True)
class DecodedDocument:
    """ناتجُ القراءة: تصريحٌ إن تمّ، وعيوبٌ إن لم يتمّ؛ ولا حكمَ في الحالين."""

    declaration: CaseDeclaration | None
    faults: tuple[InputFault, ...]


class _Faults:
    """جامعُ عيوبٍ يُسمّي كلَّ ما وجد؛ ولا يقف عند أوّل عيبٍ فيُخفي ما بعده."""

    __slots__ = ("_collected",)

    def __init__(self) -> None:
        self._collected: list[InputFault] = []

    def add(self, kind: InputFaultKind, site: str) -> None:
        self._collected.append(InputFault(kind=kind, site=site))

    @property
    def collected(self) -> tuple[InputFault, ...]:
        return tuple(self._collected)

    def __bool__(self) -> bool:
        return bool(self._collected)


def _mapping(value: object, site: str, faults: _Faults) -> dict[str, object] | None:
    if not isinstance(value, dict):
        faults.add(InputFaultKind.ILLEGAL_TYPE, site)
        return None
    for key in value:
        if not isinstance(key, str):
            faults.add(InputFaultKind.ILLEGAL_TYPE, site)
            return None
    return dict(value)


def _keyed(
    value: object,
    site: str,
    required: tuple[str, ...],
    optional: tuple[str, ...],
    faults: _Faults,
) -> dict[str, object] | None:
    mapping = _mapping(value, site, faults)
    if mapping is None:
        return None
    known = set(required) | set(optional)
    complete = True
    for key in sorted(mapping):
        if key not in known:
            faults.add(InputFaultKind.UNKNOWN_KEY, f"{site}.{key}")
            complete = False
    for key in required:
        if key not in mapping:
            faults.add(InputFaultKind.MISSING_REQUIRED_FIELD, f"{site}.{key}")
            complete = False
    return mapping if complete else None


def _text(
    mapping: dict[str, object], key: str, site: str, faults: _Faults
) -> str | None:
    value = mapping.get(key)
    if not isinstance(value, str) or not value.strip():
        faults.add(InputFaultKind.ILLEGAL_TYPE, f"{site}.{key}")
        return None
    return value


def _optional_text(
    mapping: dict[str, object], key: str, site: str, faults: _Faults
) -> tuple[bool, str | None]:
    if key not in mapping or mapping[key] is None:
        return True, None
    value = mapping[key]
    if not isinstance(value, str) or not value.strip():
        faults.add(InputFaultKind.ILLEGAL_TYPE, f"{site}.{key}")
        return False, None
    return True, value


def _integer(
    mapping: dict[str, object], key: str, site: str, faults: _Faults
) -> int | None:
    value = mapping.get(key)
    if type(value) is not int:
        faults.add(InputFaultKind.ILLEGAL_TYPE, f"{site}.{key}")
        return None
    return value


def _sequence(
    mapping: dict[str, object], key: str, site: str, faults: _Faults
) -> list[object] | None:
    value = mapping.get(key)
    if not isinstance(value, list):
        faults.add(InputFaultKind.ILLEGAL_TYPE, f"{site}.{key}")
        return None
    return list(value)


def _condition(
    value: object, site: str, faults: _Faults
) -> PriorConditionDeclaration | None:
    mapping = _keyed(
        value,
        site,
        ("condition_id", "kind", "statement", "what_it_forbids", "licensed_by"),
        (),
        faults,
    )
    if mapping is None:
        return None
    condition_id = _text(mapping, "condition_id", site, faults)
    kind_name = _text(mapping, "kind", site, faults)
    statement = _text(mapping, "statement", site, faults)
    forbids = _text(mapping, "what_it_forbids", site, faults)
    licensed_by = _text(mapping, "licensed_by", site, faults)
    if None in (condition_id, kind_name, statement, forbids, licensed_by):
        return None
    assert condition_id is not None and kind_name is not None
    assert statement is not None and forbids is not None and licensed_by is not None
    return PriorConditionDeclaration(
        condition_id=condition_id,
        kind_name=kind_name,
        statement=statement,
        what_it_forbids=forbids,
        licensed_by_name=licensed_by,
    )


def _prior_base(
    value: object, site: str, faults: _Faults
) -> PriorBaseDeclaration | None:
    mapping = _keyed(
        value,
        site,
        ("base_id", "domain_note", "declared_content_id", "conditions"),
        (),
        faults,
    )
    if mapping is None:
        return None
    base_id = _text(mapping, "base_id", site, faults)
    domain_note = _text(mapping, "domain_note", site, faults)
    declared = _text(mapping, "declared_content_id", site, faults)
    raw_conditions = _sequence(mapping, "conditions", site, faults)
    if base_id is None or domain_note is None or declared is None:
        return None
    if raw_conditions is None:
        return None
    conditions: list[PriorConditionDeclaration] = []
    for index, raw in enumerate(raw_conditions):
        condition = _condition(raw, f"{site}.conditions[{index}]", faults)
        if condition is None:
            return None
        conditions.append(condition)
    return PriorBaseDeclaration(
        base_id=base_id,
        domain_note=domain_note,
        declared_content_id=declared,
        conditions=tuple(conditions),
    )


def _candidate(
    value: object, site: str, faults: _Faults
) -> CandidateDeclaration | None:
    mapping = _keyed(
        value,
        site,
        (
            "candidate_id",
            "kind",
            "necessity_claim",
            "irreducibility_claim",
            "licensing_condition",
        ),
        (),
        faults,
    )
    if mapping is None:
        return None
    candidate_id = _text(mapping, "candidate_id", site, faults)
    kind_name = _text(mapping, "kind", site, faults)
    necessity = _text(mapping, "necessity_claim", site, faults)
    irreducibility = _text(mapping, "irreducibility_claim", site, faults)
    licensing = _text(mapping, "licensing_condition", site, faults)
    if None in (candidate_id, kind_name, necessity, irreducibility, licensing):
        return None
    assert candidate_id is not None and kind_name is not None and necessity is not None
    assert irreducibility is not None and licensing is not None
    return CandidateDeclaration(
        candidate_id=candidate_id,
        kind_name=kind_name,
        necessity_claim=necessity,
        irreducibility_claim=irreducibility,
        licensing_condition_name=licensing,
    )


def _general(
    value: object, site: str, faults: _Faults
) -> GeneralOntologyDeclaration | None:
    mapping = _keyed(
        value,
        site,
        ("ontology_id", "founded_on_base_id", "declared_content_id", "candidates"),
        (),
        faults,
    )
    if mapping is None:
        return None
    ontology_id = _text(mapping, "ontology_id", site, faults)
    founded_on = _text(mapping, "founded_on_base_id", site, faults)
    declared = _text(mapping, "declared_content_id", site, faults)
    raw_candidates = _sequence(mapping, "candidates", site, faults)
    if ontology_id is None or founded_on is None or declared is None:
        return None
    if raw_candidates is None:
        return None
    candidates: list[CandidateDeclaration] = []
    for index, raw in enumerate(raw_candidates):
        candidate = _candidate(raw, f"{site}.candidates[{index}]", faults)
        if candidate is None:
            return None
        candidates.append(candidate)
    return GeneralOntologyDeclaration(
        ontology_id=ontology_id,
        founded_on_base_id=founded_on,
        declared_content_id=declared,
        candidates=tuple(candidates),
    )


def _license(value: object, site: str, faults: _Faults) -> LicenseDeclaration | None:
    mapping = _keyed(
        value,
        site,
        (
            "license_id",
            "candidate_id",
            "function",
            "read_from",
            "condition_base_id",
            "condition_place",
        ),
        (),
        faults,
    )
    if mapping is None:
        return None
    license_id = _text(mapping, "license_id", site, faults)
    candidate_id = _text(mapping, "candidate_id", site, faults)
    function_name = _text(mapping, "function", site, faults)
    read_from = _text(mapping, "read_from", site, faults)
    condition_base_id = _text(mapping, "condition_base_id", site, faults)
    condition_place = _text(mapping, "condition_place", site, faults)
    if None in (license_id, candidate_id, function_name, read_from):
        return None
    if condition_base_id is None or condition_place is None:
        return None
    assert license_id is not None and candidate_id is not None
    assert function_name is not None and read_from is not None
    return LicenseDeclaration(
        license_id=license_id,
        candidate_id=candidate_id,
        function_name=function_name,
        read_from=read_from,
        condition_base_id=condition_base_id,
        condition_place_name=condition_place,
    )


def _linguistic(
    value: object, site: str, faults: _Faults
) -> LinguisticOntologyDeclaration | None:
    mapping = _keyed(
        value,
        site,
        ("ontology_id", "founded_on_general_id", "declared_content_id", "licenses"),
        (),
        faults,
    )
    if mapping is None:
        return None
    ontology_id = _text(mapping, "ontology_id", site, faults)
    founded_on = _text(mapping, "founded_on_general_id", site, faults)
    read, declared = _optional_text(mapping, "declared_content_id", site, faults)
    raw_licenses = _sequence(mapping, "licenses", site, faults)
    if ontology_id is None or founded_on is None or not read or raw_licenses is None:
        return None
    licenses: list[LicenseDeclaration] = []
    for index, raw in enumerate(raw_licenses):
        granted = _license(raw, f"{site}.licenses[{index}]", faults)
        if granted is None:
            return None
        licenses.append(granted)
    return LinguisticOntologyDeclaration(
        ontology_id=ontology_id,
        founded_on_general_id=founded_on,
        declared_content_id=declared,
        licenses=tuple(licenses),
    )


def _lineage(value: object, site: str, faults: _Faults) -> LineageDeclaration | None:
    mapping = _keyed(
        value,
        site,
        ("base_id", "general_ontology_id", "linguistic_ontology_id"),
        (),
        faults,
    )
    if mapping is None:
        return None
    base_id = _text(mapping, "base_id", site, faults)
    general_id = _text(mapping, "general_ontology_id", site, faults)
    linguistic_id = _text(mapping, "linguistic_ontology_id", site, faults)
    if base_id is None or general_id is None or linguistic_id is None:
        return None
    return LineageDeclaration(
        base_id=base_id,
        general_ontology_id=general_id,
        linguistic_ontology_id=linguistic_id,
    )


def _role_site(
    value: object, site: str, faults: _Faults
) -> tuple[bool, RoleSiteDeclaration | None]:
    if value is None:
        return True, None
    mapping = _keyed(
        value, site, ("linguistic_ontology_id", "license_id", "function"), (), faults
    )
    if mapping is None:
        return False, None
    ontology_id = _text(mapping, "linguistic_ontology_id", site, faults)
    license_id = _text(mapping, "license_id", site, faults)
    function_name = _text(mapping, "function", site, faults)
    if ontology_id is None or license_id is None or function_name is None:
        return False, None
    return True, RoleSiteDeclaration(
        linguistic_ontology_id=ontology_id,
        license_id=license_id,
        function_name=function_name,
    )


def _condition_site(
    value: object, site: str, faults: _Faults
) -> tuple[bool, ConditionSiteDeclaration | None]:
    if value is None:
        return True, None
    mapping = _keyed(value, site, ("base_id", "place"), (), faults)
    if mapping is None:
        return False, None
    base_id = _text(mapping, "base_id", site, faults)
    place = _text(mapping, "place", site, faults)
    if base_id is None or place is None:
        return False, None
    return True, ConditionSiteDeclaration(base_id=base_id, place_name=place)


def _slot(value: object, site: str, faults: _Faults) -> SlotDeclaration | None:
    mapping = _keyed(value, site, ("slot_id", "position", "condition_site"), (), faults)
    if mapping is None:
        return None
    slot_id = _text(mapping, "slot_id", site, faults)
    position = _integer(mapping, "position", site, faults)
    read, condition_site = _condition_site(
        mapping.get("condition_site"), f"{site}.condition_site", faults
    )
    if slot_id is None or position is None or not read:
        return None
    return SlotDeclaration(
        slot_id=slot_id, position=position, condition_site=condition_site
    )


def _predicate(
    value: object, site: str, faults: _Faults
) -> PredicateDeclaration | None:
    mapping = _keyed(
        value,
        site,
        ("predicate_id", "arity", "arity_license", "role_site", "slots"),
        (),
        faults,
    )
    if mapping is None:
        return None
    predicate_id = _text(mapping, "predicate_id", site, faults)
    arity = _integer(mapping, "arity", site, faults)
    arity_license = _text(mapping, "arity_license", site, faults)
    read, role_site = _role_site(mapping.get("role_site"), f"{site}.role_site", faults)
    raw_slots = _sequence(mapping, "slots", site, faults)
    if predicate_id is None or arity is None or arity_license is None or not read:
        return None
    if raw_slots is None:
        return None
    slots: list[SlotDeclaration] = []
    for index, raw in enumerate(raw_slots):
        slot = _slot(raw, f"{site}.slots[{index}]", faults)
        if slot is None:
            return None
        slots.append(slot)
    return PredicateDeclaration(
        predicate_id=predicate_id,
        arity=arity,
        arity_license_name=arity_license,
        role_site=role_site,
        slots=tuple(slots),
    )


def _anchor(value: object, site: str, faults: _Faults) -> AnchorDeclaration | None:
    mapping = _keyed(
        value, site, ("anchor_id", "role_site", "condition_site"), (), faults
    )
    if mapping is None:
        return None
    anchor_id = _text(mapping, "anchor_id", site, faults)
    role_read, role_site = _role_site(
        mapping.get("role_site"), f"{site}.role_site", faults
    )
    condition_read, condition_site = _condition_site(
        mapping.get("condition_site"), f"{site}.condition_site", faults
    )
    if anchor_id is None or not role_read or not condition_read:
        return None
    return AnchorDeclaration(
        anchor_id=anchor_id, role_site=role_site, condition_site=condition_site
    )


def _nisbah(value: object, site: str, faults: _Faults) -> NisbahDeclaration | None:
    mapping = _keyed(
        value,
        site,
        ("nisbah_id", "declared_content_id", "predicate", "anchors"),
        (),
        faults,
    )
    if mapping is None:
        return None
    nisbah_id = _text(mapping, "nisbah_id", site, faults)
    read, declared = _optional_text(mapping, "declared_content_id", site, faults)
    predicate = _predicate(mapping.get("predicate"), f"{site}.predicate", faults)
    raw_anchors = _sequence(mapping, "anchors", site, faults)
    if nisbah_id is None or not read or predicate is None or raw_anchors is None:
        return None
    anchors: list[AnchorDeclaration] = []
    for index, raw in enumerate(raw_anchors):
        anchor = _anchor(raw, f"{site}.anchors[{index}]", faults)
        if anchor is None:
            return None
        anchors.append(anchor)
    return NisbahDeclaration(
        nisbah_id=nisbah_id,
        declared_content_id=declared,
        predicate=predicate,
        anchors=tuple(anchors),
    )


def _requirement(
    value: object, site: str, faults: _Faults
) -> UnresolvedRequirement | None:
    mapping = _keyed(
        value, site, ("required_authority", "subject_id", "standing"), (), faults
    )
    if mapping is None:
        return None
    authority_name = _text(mapping, "required_authority", site, faults)
    subject_id = _text(mapping, "subject_id", site, faults)
    standing_name = _text(mapping, "standing", site, faults)
    if authority_name is None or subject_id is None or standing_name is None:
        return None
    try:
        authority = RequiredAuthority(authority_name)
    except ValueError:
        faults.add(
            InputFaultKind.UNKNOWN_VOCABULARY_MEMBER, f"{site}.required_authority"
        )
        return None
    try:
        standing = RequirementStanding(standing_name)
    except ValueError:
        faults.add(InputFaultKind.UNKNOWN_VOCABULARY_MEMBER, f"{site}.standing")
        return None
    return UnresolvedRequirement(
        required_authority=authority, subject_id=subject_id, standing=standing
    )


def decode_document(document: object) -> DecodedDocument:
    """اقرأ وثيقةً بعقد `alghanem.execution.v1`؛ والعيوبُ تُجمَع ولا تُرمَّم."""

    faults = _Faults()
    mapping = _keyed(document, "document", _CASE_KEYS, (), faults)
    if mapping is None:
        return DecodedDocument(declaration=None, faults=faults.collected)
    schema = _text(mapping, "schema", "document", faults)
    nisbah_schema = _text(mapping, "nisbah_schema", "document", faults)
    if schema is not None and schema != EXECUTION_DOCUMENT_SCHEMA:
        faults.add(InputFaultKind.UNKNOWN_SCHEMA, "document.schema")
        schema = None
    raw_bases = _sequence(mapping, "prior_bases", "document", faults)
    raw_generals = _sequence(mapping, "general_ontologies", "document", faults)
    raw_linguistics = _sequence(mapping, "linguistic_ontologies", "document", faults)
    lineage = _lineage(mapping.get("lineage"), "document.lineage", faults)
    nisbah = _nisbah(mapping.get("nisbah"), "document.nisbah", faults)
    raw_requirements = _sequence(mapping, "unresolved_requirements", "document", faults)
    bases: list[PriorBaseDeclaration] = []
    if raw_bases is not None:
        for index, raw in enumerate(raw_bases):
            base = _prior_base(raw, f"document.prior_bases[{index}]", faults)
            if base is None:
                raw_bases = None
                break
            bases.append(base)
    generals: list[GeneralOntologyDeclaration] = []
    if raw_generals is not None:
        for index, raw in enumerate(raw_generals):
            general = _general(raw, f"document.general_ontologies[{index}]", faults)
            if general is None:
                raw_generals = None
                break
            generals.append(general)
    linguistics: list[LinguisticOntologyDeclaration] = []
    if raw_linguistics is not None:
        for index, raw in enumerate(raw_linguistics):
            linguistic = _linguistic(
                raw, f"document.linguistic_ontologies[{index}]", faults
            )
            if linguistic is None:
                raw_linguistics = None
                break
            linguistics.append(linguistic)
    requirements: list[UnresolvedRequirement] = []
    if raw_requirements is not None:
        for index, raw in enumerate(raw_requirements):
            requirement = _requirement(
                raw, f"document.unresolved_requirements[{index}]", faults
            )
            if requirement is None:
                raw_requirements = None
                break
            requirements.append(requirement)
    if (
        schema is None
        or nisbah_schema is None
        or raw_bases is None
        or raw_generals is None
        or raw_linguistics is None
        or lineage is None
        or nisbah is None
        or raw_requirements is None
    ):
        return DecodedDocument(declaration=None, faults=faults.collected)
    declaration = CaseDeclaration(
        schema=schema,
        nisbah_schema=nisbah_schema,
        prior_bases=tuple(bases),
        general_ontologies=tuple(generals),
        linguistic_ontologies=tuple(linguistics),
        lineage=lineage,
        nisbah=nisbah,
        unresolved_requirements=tuple(requirements),
    )
    return DecodedDocument(declaration=declaration, faults=faults.collected)


def encode_declaration(declaration: CaseDeclaration) -> dict[str, object]:
    """أعِد وثيقةَ التصريح؛ وقراءتُها ثانيةً تعطي التصريحَ نفسَه بلا فرق."""

    if not isinstance(declaration, CaseDeclaration):
        raise TypeError("الترميزُ يكون لتصريحٍ قائمٍ لا لاسمٍ حرّ")
    return declaration.as_canonical_content()
