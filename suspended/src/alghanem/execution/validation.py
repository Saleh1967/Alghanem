"""التحقّقُ من عقد الإدخال: أتقوم قضيّةٌ قابلةٌ للحكم من هذه الوثيقة؟

    Declaration  →  InputValidation (VALID | INVALID)

وهنا تُفحَص الهويّاتُ **السابقةُ على الحكم** وحدَها: بصمةُ `PK_0` وبصمةُ `O_0`،
لأنّ محتواهما يتحدّد من التصريح نفسِه بلا فعلِ ترخيصٍ واحد. أمّا بصمةُ `O_L²`
فمحتواها يضمّ مراجعَ شرطٍ لا تتكوّن إلّا بفعل ترخيص، وبصمةُ النسبة لا تكون
إلّا بعد الإنشاء السلطويّ؛ فهاتان دعويان تُفحَصان في طبقة القوانين لا قبلها.
ولو طُولِبنا بمطابقتهما قبل الحكم لعدنا إلى الدور الذي قام هذا الفصلُ لمنعه.

تسجيلٌ لا سلطة: لا ولادةَ ولا حكمَ ولادةٍ ولا تجميدَ `E0`.
"""

from __future__ import annotations

from dataclasses import dataclass, field

from ..linguistic.anchored_v3 import ANCHORED_V3_SCHEMA_VERSION
from ..linguistic.nisbah import ArityLicenseGenus
from ..ontology.general import (
    GeneralOntology,
    OntologicalCandidate,
    OntologicalKind,
    OntologyError,
    PriorBaseRef,
)
from ..ontology.linguistic import LinguisticFunction
from ..prior.conditions import (
    PriorCondition,
    PriorConditionKind,
    PriorInformationBase,
    PriorInformationError,
    PriorLicenseGenus,
)
from .declaration import CaseDeclaration
from .requirement import RequiredAuthority
from .standing import InputFault, InputFaultKind, InputStanding, InputValidation

__all__ = ["DeclaredLevels", "validate_declaration"]


@dataclass(frozen=True, slots=True)
class DeclaredLevels:
    """المستوياتُ التي تحدَّد محتواها من التصريح وحدَه، مبنيّةً لا محكومًا عليها."""

    bases: dict[str, PriorInformationBase] = field(default_factory=dict)
    generals: dict[str, GeneralOntology] = field(default_factory=dict)


def _read_condition(
    declared: object, base_site: str, faults: list[InputFault]
) -> PriorCondition | None:
    from .declaration import PriorConditionDeclaration

    assert isinstance(declared, PriorConditionDeclaration)
    site = f"{base_site}.{declared.condition_id}"
    try:
        kind = PriorConditionKind(declared.kind_name)
    except ValueError:
        faults.append(
            InputFault(InputFaultKind.UNKNOWN_VOCABULARY_MEMBER, f"{site}.kind")
        )
        return None
    try:
        genus = PriorLicenseGenus(declared.licensed_by_name)
    except ValueError:
        faults.append(
            InputFault(InputFaultKind.UNKNOWN_VOCABULARY_MEMBER, f"{site}.licensed_by")
        )
        return None
    try:
        return PriorCondition(
            condition_id=declared.condition_id,
            kind=kind,
            statement=declared.statement,
            what_it_forbids=declared.what_it_forbids,
            licensed_by=genus,
        )
    except PriorInformationError:
        faults.append(InputFault(InputFaultKind.MALFORMED_DECLARED_CONTENT, site))
        return None


def _read_candidate(
    declared: object, ontology_site: str, faults: list[InputFault]
) -> OntologicalCandidate | None:
    from .declaration import CandidateDeclaration

    assert isinstance(declared, CandidateDeclaration)
    site = f"{ontology_site}.{declared.candidate_id}"
    try:
        kind = OntologicalKind(declared.kind_name)
    except ValueError:
        faults.append(
            InputFault(InputFaultKind.UNKNOWN_VOCABULARY_MEMBER, f"{site}.kind")
        )
        return None
    try:
        licensing = PriorConditionKind(declared.licensing_condition_name)
    except ValueError:
        faults.append(
            InputFault(
                InputFaultKind.UNKNOWN_VOCABULARY_MEMBER, f"{site}.licensing_condition"
            )
        )
        return None
    try:
        return OntologicalCandidate(
            candidate_id=declared.candidate_id,
            kind=kind,
            necessity_claim=declared.necessity_claim,
            irreducibility_claim=declared.irreducibility_claim,
            licensing_condition=licensing,
        )
    except OntologyError:
        faults.append(InputFault(InputFaultKind.MALFORMED_DECLARED_CONTENT, site))
        return None


def _read_bases(
    declaration: CaseDeclaration, faults: list[InputFault]
) -> dict[str, PriorInformationBase]:
    bases: dict[str, PriorInformationBase] = {}
    for declared in declaration.prior_bases:
        site = f"prior_bases.{declared.base_id}"
        if declared.base_id in bases:
            faults.append(InputFault(InputFaultKind.DUPLICATE_DECLARED_ID, site))
            continue
        conditions: list[PriorCondition] = []
        broken = False
        for raw in declared.conditions:
            condition = _read_condition(raw, site, faults)
            if condition is None:
                broken = True
                continue
            conditions.append(condition)
        if broken:
            continue
        try:
            base = PriorInformationBase(
                base_id=declared.base_id,
                domain_note=declared.domain_note,
                conditions=tuple(conditions),
            )
        except PriorInformationError:
            faults.append(InputFault(InputFaultKind.MALFORMED_DECLARED_CONTENT, site))
            continue
        if base.content_id != declared.declared_content_id:
            faults.append(
                InputFault(InputFaultKind.DECLARED_CONTENT_ID_DISAGREES, site)
            )
            continue
        bases[declared.base_id] = base
    return bases


def _read_generals(
    declaration: CaseDeclaration,
    bases: dict[str, PriorInformationBase],
    faults: list[InputFault],
) -> dict[str, GeneralOntology]:
    generals: dict[str, GeneralOntology] = {}
    for declared in declaration.general_ontologies:
        site = f"general_ontologies.{declared.ontology_id}"
        if declared.ontology_id in generals:
            faults.append(InputFault(InputFaultKind.DUPLICATE_DECLARED_ID, site))
            continue
        base = bases.get(declared.founded_on_base_id)
        if base is None:
            faults.append(
                InputFault(
                    InputFaultKind.UNRESOLVABLE_INTERNAL_REFERENCE,
                    f"{site}.founded_on_base_id",
                )
            )
            continue
        candidates: list[OntologicalCandidate] = []
        broken = False
        for raw in declared.candidates:
            candidate = _read_candidate(raw, site, faults)
            if candidate is None:
                broken = True
                continue
            candidates.append(candidate)
        if broken:
            continue
        try:
            general = GeneralOntology(
                ontology_id=declared.ontology_id,
                prior_base_ref=PriorBaseRef.of(base),
                candidates=tuple(candidates),
            )
        except OntologyError:
            faults.append(InputFault(InputFaultKind.MALFORMED_DECLARED_CONTENT, site))
            continue
        if general.content_id != declared.declared_content_id:
            faults.append(
                InputFault(InputFaultKind.DECLARED_CONTENT_ID_DISAGREES, site)
            )
            continue
        generals[declared.ontology_id] = general
    return generals


def _check_linguistic_references(
    declaration: CaseDeclaration,
    bases: dict[str, PriorInformationBase],
    generals: dict[str, GeneralOntology],
    faults: list[InputFault],
) -> set[str]:
    known: set[str] = set()
    for declared in declaration.linguistic_ontologies:
        site = f"linguistic_ontologies.{declared.ontology_id}"
        if declared.ontology_id in known:
            faults.append(InputFault(InputFaultKind.DUPLICATE_DECLARED_ID, site))
            continue
        known.add(declared.ontology_id)
        if declared.founded_on_general_id not in generals:
            faults.append(
                InputFault(
                    InputFaultKind.UNRESOLVABLE_INTERNAL_REFERENCE,
                    f"{site}.founded_on_general_id",
                )
            )
        seen: set[str] = set()
        for granted in declared.licenses:
            license_site = f"{site}.{granted.license_id}"
            if granted.license_id in seen:
                faults.append(
                    InputFault(InputFaultKind.DUPLICATE_DECLARED_ID, license_site)
                )
                continue
            seen.add(granted.license_id)
            if granted.condition_base_id not in bases:
                faults.append(
                    InputFault(
                        InputFaultKind.UNRESOLVABLE_INTERNAL_REFERENCE,
                        f"{license_site}.condition_base_id",
                    )
                )
            try:
                PriorConditionKind(granted.condition_place_name)
            except ValueError:
                faults.append(
                    InputFault(
                        InputFaultKind.UNKNOWN_VOCABULARY_MEMBER,
                        f"{license_site}.condition_place",
                    )
                )
            try:
                LinguisticFunction(granted.function_name)
            except ValueError:
                faults.append(
                    InputFault(
                        InputFaultKind.UNKNOWN_VOCABULARY_MEMBER,
                        f"{license_site}.function",
                    )
                )
    return known


def _check_site(
    role_site: object,
    condition_site: object,
    owner_id: str,
    owner_site: str,
    declaration: CaseDeclaration,
    bases: dict[str, PriorInformationBase],
    linguistic_ids: set[str],
    requires_role: bool,
    requires_condition: bool,
    faults: list[InputFault],
) -> None:
    from .declaration import ConditionSiteDeclaration, RoleSiteDeclaration

    if requires_role:
        if role_site is None:
            if (
                declaration.requirement_for(RequiredAuthority.ROLE_LICENSE, owner_id)
                is None
            ):
                faults.append(
                    InputFault(
                        InputFaultKind.UNDECLARED_ABSENT_SITE, f"{owner_site}.role_site"
                    )
                )
        else:
            assert isinstance(role_site, RoleSiteDeclaration)
            if role_site.linguistic_ontology_id not in linguistic_ids:
                faults.append(
                    InputFault(
                        InputFaultKind.UNRESOLVABLE_INTERNAL_REFERENCE,
                        f"{owner_site}.role_site.linguistic_ontology_id",
                    )
                )
            try:
                LinguisticFunction(role_site.function_name)
            except ValueError:
                faults.append(
                    InputFault(
                        InputFaultKind.UNKNOWN_VOCABULARY_MEMBER,
                        f"{owner_site}.role_site.function",
                    )
                )
    if not requires_condition:
        return
    if condition_site is None:
        if (
            declaration.requirement_for(
                RequiredAuthority.PRIOR_CONDITION_REFERENCE, owner_id
            )
            is None
        ):
            faults.append(
                InputFault(
                    InputFaultKind.UNDECLARED_ABSENT_SITE,
                    f"{owner_site}.condition_site",
                )
            )
    else:
        assert isinstance(condition_site, ConditionSiteDeclaration)
        if condition_site.base_id not in bases:
            faults.append(
                InputFault(
                    InputFaultKind.UNRESOLVABLE_INTERNAL_REFERENCE,
                    f"{owner_site}.condition_site.base_id",
                )
            )
        try:
            PriorConditionKind(condition_site.place_name)
        except ValueError:
            faults.append(
                InputFault(
                    InputFaultKind.UNKNOWN_VOCABULARY_MEMBER,
                    f"{owner_site}.condition_site.place",
                )
            )


def _check_requirement_subjects(
    declaration: CaseDeclaration, faults: list[InputFault]
) -> None:
    """مطلبٌ غيرُ محسومٍ لموضعٍ حاضرٍ تناقضٌ؛ والتناقضُ يمنع تكوينَ القضيّة."""

    present_roles: dict[str, bool] = {
        declaration.nisbah.predicate.predicate_id: (
            declaration.nisbah.predicate.role_site is not None
        )
    }
    present_conditions: dict[str, bool] = {}
    for slot in declaration.nisbah.predicate.slots:
        present_conditions[slot.slot_id] = slot.condition_site is not None
    for anchor in declaration.nisbah.anchors:
        present_roles[anchor.anchor_id] = anchor.role_site is not None
        present_conditions[anchor.anchor_id] = anchor.condition_site is not None
    for index, requirement in enumerate(declaration.unresolved_requirements):
        site = f"unresolved_requirements[{index}]"
        subject = requirement.subject_id
        if requirement.required_authority is RequiredAuthority.ROLE_LICENSE:
            if present_roles.get(subject, None) is not False:
                faults.append(
                    InputFault(InputFaultKind.UNRESOLVABLE_INTERNAL_REFERENCE, site)
                )
        elif (
            requirement.required_authority
            is RequiredAuthority.PRIOR_CONDITION_REFERENCE
        ):
            if present_conditions.get(subject, None) is not False:
                faults.append(
                    InputFault(InputFaultKind.UNRESOLVABLE_INTERNAL_REFERENCE, site)
                )


def validate_declaration(
    declaration: CaseDeclaration,
) -> tuple[InputValidation, DeclaredLevels]:
    """افحص عقدَ الإدخال؛ والعيوبُ تُجمَع كلُّها ولا يصدر معها حكمٌ ألبتّة."""

    faults: list[InputFault] = []
    if declaration.nisbah_schema != ANCHORED_V3_SCHEMA_VERSION:
        faults.append(
            InputFault(InputFaultKind.UNKNOWN_SCHEMA, "document.nisbah_schema")
        )
    bases = _read_bases(declaration, faults)
    generals = _read_generals(declaration, bases, faults)
    linguistic_ids = _check_linguistic_references(declaration, bases, generals, faults)
    lineage = declaration.lineage
    if lineage.base_id not in bases:
        faults.append(
            InputFault(
                InputFaultKind.UNRESOLVABLE_INTERNAL_REFERENCE, "lineage.base_id"
            )
        )
    if lineage.general_ontology_id not in generals:
        faults.append(
            InputFault(
                InputFaultKind.UNRESOLVABLE_INTERNAL_REFERENCE,
                "lineage.general_ontology_id",
            )
        )
    if lineage.linguistic_ontology_id not in linguistic_ids:
        faults.append(
            InputFault(
                InputFaultKind.UNRESOLVABLE_INTERNAL_REFERENCE,
                "lineage.linguistic_ontology_id",
            )
        )
    predicate = declaration.nisbah.predicate
    try:
        ArityLicenseGenus(predicate.arity_license_name)
    except ValueError:
        faults.append(
            InputFault(
                InputFaultKind.UNKNOWN_VOCABULARY_MEMBER,
                "nisbah.predicate.arity_license",
            )
        )
    _check_site(
        predicate.role_site,
        None,
        predicate.predicate_id,
        "nisbah.predicate",
        declaration,
        bases,
        linguistic_ids,
        True,
        False,
        faults,
    )
    for slot in predicate.slots:
        _check_site(
            None,
            slot.condition_site,
            slot.slot_id,
            f"nisbah.predicate.slots.{slot.slot_id}",
            declaration,
            bases,
            linguistic_ids,
            False,
            True,
            faults,
        )
    for anchor in declaration.nisbah.anchors:
        _check_site(
            anchor.role_site,
            anchor.condition_site,
            anchor.anchor_id,
            f"nisbah.anchors.{anchor.anchor_id}",
            declaration,
            bases,
            linguistic_ids,
            True,
            True,
            faults,
        )
    _check_requirement_subjects(declaration, faults)
    standing = InputStanding.INVALID if faults else InputStanding.VALID
    validation = InputValidation(standing=standing, faults=tuple(faults))
    return validation, DeclaredLevels(bases=bases, generals=generals)
