"""تقييمُ القوانين: من المادّة المُشتَقّة إلى أثرٍ مرتَّبٍ ثمّ إلى حكم.

    PartialAuthorityDerivation  →  (LawCheckEntry, …)  →  PASS | BLOCK | DEFER

**وكلُّ قانونٍ يُقيَّم ولا يُوقَف عند أوّل مخالفة** على منهج
`PriorCoverageIsExactNotBestEffort`؛ فإن تعذّر تقييمُ قانونٍ تابعٍ لأنّ قانونًا
سابقًا حجب مادّتَه، سُجِّل `NOT_EVALUATED_BY_PREREQUISITE` **مسمّى حاجبَه**، ولم
يُقرأ نقصَ دليل. وإن لم تُعلَن دعوى هويّةٍ أصلًا سُجِّل
`NOT_APPLICABLE_NO_CLAIM`، ولم يُقرأ غيابُ الدعوى تصديقًا لها.

    BLOCK  >  DEFER  >  PASS

تسجيلٌ لا سلطة: لا ولادةَ ولا حكمَ ولادةٍ ولا تجميدَ `E0`.
"""

from __future__ import annotations

from typing import Final

from ..linguistic.nisbah import DEFERRED_ARGUMENT_ROLE_NAMES, ArityLicenseGenus
from ..ontology.linguistic_v2 import LinguisticOntologyV2
from ..prior.conditions import PriorConditionKind, PriorLicenseGenus
from .declaration import (
    CaseDeclaration,
    ConditionSiteDeclaration,
    LinguisticOntologyDeclaration,
    RoleSiteDeclaration,
)
from .derivation import (
    DerivedSite,
    PartialAuthorityDerivation,
    RefusalKind,
    SiteStanding,
)
from .lawset import ExecutionLaw
from .outcome import CheckStanding, ExecutionOutcome, Identity, LawCheckEntry, Violation
from .requirement import RequiredAuthority, RequirementStanding, UnresolvedRequirement

__all__ = [
    "EVERY_LAW_IS_EVALUATED",
    "aggregate_outcome",
    "evaluate_laws",
    "residuals_of",
    "violations_of",
]


EVERY_LAW_IS_EVALUATED: Final[str] = (
    "كلُّ قانونٍ يُقيَّم: لا يُوقَف عند أوّل مخالفةٍ ولا يُسقَط قانونٌ من الأثر؛ "
    "والقانونُ الذي حُجِبت مادّتُه يُسجَّل محجوبًا مسمًّى حاجبُه لا مؤجَّلًا"
)


_BLOCKER_OF_REFUSAL: Final[dict[RefusalKind, ExecutionLaw]] = {
    RefusalKind.CONDITION_IS_SELF_DERIVED: (
        ExecutionLaw.NO_SELF_DERIVED_LICENSING_GENUS
    ),
    RefusalKind.CONDITION_IS_NOT_LICENSED_FOR_USE: (
        ExecutionLaw.CONDITION_SITES_ARE_LICENSED_FOR_USE
    ),
    RefusalKind.CANDIDATE_IS_NOT_REGISTERED: (
        ExecutionLaw.LINGUISTIC_LICENSES_NAME_REGISTERED_CANDIDATES
    ),
    RefusalKind.LICENSE_BASE_DIFFERS_FROM_THE_FOUNDING_BASE: (
        ExecutionLaw.LINGUISTIC_LICENSES_SHARE_THE_FOUNDING_BASE
    ),
    RefusalKind.LICENSE_IS_ABSENT: (
        ExecutionLaw.ROLE_LICENSE_GRANTED_FOR_THE_FUNCTION_READ
    ),
    RefusalKind.LICENSE_IS_FOR_ANOTHER_FUNCTION: (
        ExecutionLaw.ROLE_LICENSE_GRANTED_FOR_THE_FUNCTION_READ
    ),
    RefusalKind.LICENSE_IS_NOT_OPERATIVE: ExecutionLaw.ROLE_LICENSE_IS_OPERATIVE,
    RefusalKind.FOUNDATION_WAS_REFUSED: (
        ExecutionLaw.LINGUISTIC_ONTOLOGY_FOUNDED_ON_THE_LINEAGE_GENERAL
    ),
    RefusalKind.LINEAGE_DID_NOT_DERIVE: ExecutionLaw.EXISTENCE_LINEAGE_REDERIVES,
}

_AUTHORITY_OF_LAW: Final[dict[ExecutionLaw, RequiredAuthority]] = {
    ExecutionLaw.NO_SELF_DERIVED_LICENSING_GENUS: (
        RequiredAuthority.PRIOR_CONDITION_REFERENCE
    ),
    ExecutionLaw.NO_UNREAD_CONDITION_IN_THE_FOUNDING_BASE: (
        RequiredAuthority.PRIOR_CONDITION_REFERENCE
    ),
    ExecutionLaw.GENERAL_ONTOLOGY_FOUNDED_ON_THE_LINEAGE_BASE: (
        RequiredAuthority.GENERAL_ONTOLOGY_FOUNDATION
    ),
    ExecutionLaw.LINGUISTIC_LICENSES_NAME_REGISTERED_CANDIDATES: (
        RequiredAuthority.LINGUISTIC_ONTOLOGY_FOUNDATION
    ),
    ExecutionLaw.LINGUISTIC_LICENSES_SHARE_THE_FOUNDING_BASE: (
        RequiredAuthority.LINGUISTIC_ONTOLOGY_FOUNDATION
    ),
    ExecutionLaw.LINGUISTIC_ONTOLOGY_FOUNDED_ON_THE_LINEAGE_GENERAL: (
        RequiredAuthority.LINGUISTIC_ONTOLOGY_FOUNDATION
    ),
    ExecutionLaw.EXISTENCE_LINEAGE_REDERIVES: RequiredAuthority.EXISTENCE_LINEAGE,
    ExecutionLaw.CONDITION_SITES_SHARE_THE_LINEAGE_BASE: (
        RequiredAuthority.PRIOR_CONDITION_REFERENCE
    ),
    ExecutionLaw.CONDITION_SITES_ARE_LICENSED_FOR_USE: (
        RequiredAuthority.PRIOR_CONDITION_REFERENCE
    ),
    ExecutionLaw.ROLE_SITES_SHARE_THE_LINEAGE_ONTOLOGY: RequiredAuthority.ROLE_LICENSE,
    ExecutionLaw.ROLE_LICENSE_GRANTED_FOR_THE_FUNCTION_READ: (
        RequiredAuthority.ROLE_LICENSE
    ),
    ExecutionLaw.ROLE_LICENSE_IS_OPERATIVE: RequiredAuthority.ROLE_LICENSE,
    ExecutionLaw.PREDICATE_ARITY_LICENSE_PERMITS_USE: RequiredAuthority.ROLE_LICENSE,
    ExecutionLaw.PREDICATE_ARITY_MATCHES_ITS_SLOTS: RequiredAuthority.ROLE_LICENSE,
    ExecutionLaw.ARGUMENT_SLOT_IDS_ARE_NOT_DEFERRED_ROLE_NAMES: (
        RequiredAuthority.ROLE_LICENSE
    ),
    ExecutionLaw.ANCHORS_DO_NOT_EXCEED_ARITY: RequiredAuthority.ROLE_LICENSE,
    ExecutionLaw.DECLARED_LINGUISTIC_IDENTITY_AGREES: (
        RequiredAuthority.LINGUISTIC_ONTOLOGY_FOUNDATION
    ),
    ExecutionLaw.MATERIALIZED_IDENTITY_AGREES: (
        RequiredAuthority.LINGUISTIC_ONTOLOGY_FOUNDATION
    ),
}


def _entry(
    law: ExecutionLaw,
    standing: CheckStanding,
    subject_id: str | None = None,
    expected: Identity | None = None,
    observed: Identity | None = None,
    blocked_by: ExecutionLaw | None = None,
) -> LawCheckEntry:
    return LawCheckEntry(
        law=law.value,
        standing=standing,
        subject_id=subject_id,
        expected=expected,
        observed=observed,
        blocked_by=None if blocked_by is None else blocked_by.value,
    )


def _blocker_of(attempt: DerivedSite[LinguisticOntologyV2]) -> ExecutionLaw:
    if attempt.refusal is None:
        return ExecutionLaw.LINGUISTIC_ONTOLOGY_FOUNDED_ON_THE_LINEAGE_GENERAL
    return _BLOCKER_OF_REFUSAL[attempt.refusal]


def _lineage_ontology(
    declaration: CaseDeclaration,
) -> LinguisticOntologyDeclaration | None:
    for declared in declaration.linguistic_ontologies:
        if declared.ontology_id == declaration.lineage.linguistic_ontology_id:
            return declared
    return None


def _condition_genus(
    derivation: PartialAuthorityDerivation, base_id: str, place_name: str
) -> PriorLicenseGenus | None:
    base = derivation.bases.get(base_id)
    if base is None:
        return None
    return base.condition(PriorConditionKind(place_name)).licensed_by


def _base_identity(
    derivation: PartialAuthorityDerivation, base_id: str
) -> Identity | None:
    base = derivation.bases.get(base_id)
    if base is None:
        return None
    return Identity(id=base.base_id, content_id=base.content_id)


def _evaluate_licensing_genus(
    declaration: CaseDeclaration, derivation: PartialAuthorityDerivation
) -> tuple[list[LawCheckEntry], list[LawCheckEntry]]:
    """قانونا الجنس المُرخِّص للرخص اللغويّة: المنتزعُ مخالفةٌ وغيرُ المقروء نقص."""

    self_derived: list[LawCheckEntry] = []
    unread: list[LawCheckEntry] = []
    declared = _lineage_ontology(declaration)
    if declared is None:
        return self_derived, unread
    for granted in declared.licenses:
        genus = _condition_genus(
            derivation, granted.condition_base_id, granted.condition_place_name
        )
        if genus is None:
            self_derived.append(
                _entry(
                    ExecutionLaw.NO_SELF_DERIVED_LICENSING_GENUS,
                    CheckStanding.UNRESOLVED,
                    granted.license_id,
                )
            )
            unread.append(
                _entry(
                    ExecutionLaw.NO_UNREAD_CONDITION_IN_THE_FOUNDING_BASE,
                    CheckStanding.UNRESOLVED,
                    granted.license_id,
                )
            )
            continue
        self_derived.append(
            _entry(
                ExecutionLaw.NO_SELF_DERIVED_LICENSING_GENUS,
                CheckStanding.VIOLATED
                if genus is PriorLicenseGenus.DERIVED_FROM_THE_ONTOLOGY_IT_LICENSES
                else CheckStanding.SATISFIED,
                granted.license_id,
            )
        )
        unread.append(
            _entry(
                ExecutionLaw.NO_UNREAD_CONDITION_IN_THE_FOUNDING_BASE,
                CheckStanding.UNRESOLVED
                if genus is PriorLicenseGenus.UNREAD
                else CheckStanding.SATISFIED,
                granted.license_id,
            )
        )
    return self_derived, unread


def _evaluate_general_foundation(
    declaration: CaseDeclaration, derivation: PartialAuthorityDerivation
) -> list[LawCheckEntry]:
    lineage = declaration.lineage
    general = derivation.generals.get(lineage.general_ontology_id)
    expected = _base_identity(derivation, lineage.base_id)
    if general is None or expected is None:
        return [
            _entry(
                ExecutionLaw.GENERAL_ONTOLOGY_FOUNDED_ON_THE_LINEAGE_BASE,
                CheckStanding.UNRESOLVED,
                lineage.general_ontology_id,
                expected,
            )
        ]
    observed = Identity(
        id=general.prior_base_ref.base_id,
        content_id=general.prior_base_ref.content_id,
    )
    return [
        _entry(
            ExecutionLaw.GENERAL_ONTOLOGY_FOUNDED_ON_THE_LINEAGE_BASE,
            CheckStanding.SATISFIED if observed == expected else CheckStanding.VIOLATED,
            lineage.general_ontology_id,
            expected,
            observed,
        )
    ]


def _evaluate_license_origins(
    declaration: CaseDeclaration, derivation: PartialAuthorityDerivation
) -> tuple[list[LawCheckEntry], list[LawCheckEntry]]:
    """قانونا الرخص: أهي لمرشَّحين مُسجَّلين؟ وأشرطُها من قاعدة التأسيس نفسِها؟"""

    registered: list[LawCheckEntry] = []
    shared: list[LawCheckEntry] = []
    declared = _lineage_ontology(declaration)
    if declared is None:
        return registered, shared
    general = derivation.generals.get(declared.founded_on_general_id)
    for granted in declared.licenses:
        if general is None:
            registered.append(
                _entry(
                    ExecutionLaw.LINGUISTIC_LICENSES_NAME_REGISTERED_CANDIDATES,
                    CheckStanding.UNRESOLVED,
                    granted.license_id,
                )
            )
            shared.append(
                _entry(
                    ExecutionLaw.LINGUISTIC_LICENSES_SHARE_THE_FOUNDING_BASE,
                    CheckStanding.UNRESOLVED,
                    granted.license_id,
                )
            )
            continue
        try:
            general.candidate(granted.candidate_id)
        except ValueError:
            registered.append(
                _entry(
                    ExecutionLaw.LINGUISTIC_LICENSES_NAME_REGISTERED_CANDIDATES,
                    CheckStanding.VIOLATED,
                    granted.license_id,
                )
            )
        else:
            registered.append(
                _entry(
                    ExecutionLaw.LINGUISTIC_LICENSES_NAME_REGISTERED_CANDIDATES,
                    CheckStanding.SATISFIED,
                    granted.license_id,
                )
            )
        expected = Identity(
            id=general.prior_base_ref.base_id,
            content_id=general.prior_base_ref.content_id,
        )
        observed = _base_identity(derivation, granted.condition_base_id)
        shared.append(
            _entry(
                ExecutionLaw.LINGUISTIC_LICENSES_SHARE_THE_FOUNDING_BASE,
                CheckStanding.UNRESOLVED
                if observed is None
                else (
                    CheckStanding.SATISFIED
                    if observed == expected
                    else CheckStanding.VIOLATED
                ),
                granted.license_id,
                expected,
                observed,
            )
        )
    return registered, shared


def _evaluate_linguistic_foundation(
    declaration: CaseDeclaration, derivation: PartialAuthorityDerivation
) -> list[LawCheckEntry]:
    lineage = declaration.lineage
    declared = _lineage_ontology(declaration)
    law = ExecutionLaw.LINGUISTIC_ONTOLOGY_FOUNDED_ON_THE_LINEAGE_GENERAL
    if declared is None:
        return [_entry(law, CheckStanding.UNRESOLVED, lineage.linguistic_ontology_id)]
    general = derivation.generals.get(lineage.general_ontology_id)
    expected = (
        None
        if general is None
        else Identity(id=general.ontology_id, content_id=general.content_id)
    )
    if general is None:
        return [_entry(law, CheckStanding.UNRESOLVED, declared.ontology_id, expected)]
    if declared.founded_on_general_id != general.ontology_id:
        observed_general = derivation.generals.get(declared.founded_on_general_id)
        observed = (
            None
            if observed_general is None
            else Identity(
                id=observed_general.ontology_id,
                content_id=observed_general.content_id,
            )
        )
        return [
            _entry(
                law, CheckStanding.VIOLATED, declared.ontology_id, expected, observed
            )
        ]
    attempt = derivation.linguistics.get(declared.ontology_id)
    if attempt is None or attempt.standing is SiteStanding.NOT_ATTEMPTED:
        return [_entry(law, CheckStanding.UNRESOLVED, declared.ontology_id, expected)]
    if attempt.standing is SiteStanding.UNRESOLVED:
        return [_entry(law, CheckStanding.UNRESOLVED, declared.ontology_id, expected)]
    if attempt.standing is SiteStanding.REFUSED:
        blocker = _blocker_of(attempt)
        if blocker is law:
            return [_entry(law, CheckStanding.VIOLATED, declared.ontology_id, expected)]
        return [
            _entry(
                law,
                CheckStanding.NOT_EVALUATED_BY_PREREQUISITE,
                declared.ontology_id,
                expected,
                blocked_by=blocker,
            )
        ]
    return [_entry(law, CheckStanding.SATISFIED, declared.ontology_id, expected)]


def _evaluate_lineage(
    declaration: CaseDeclaration, derivation: PartialAuthorityDerivation
) -> list[LawCheckEntry]:
    law = ExecutionLaw.EXISTENCE_LINEAGE_REDERIVES
    subject = declaration.lineage.linguistic_ontology_id
    attempt = derivation.lineage
    if attempt.standing is SiteStanding.DERIVED:
        return [_entry(law, CheckStanding.SATISFIED, subject)]
    if attempt.standing is SiteStanding.REFUSED:
        return [_entry(law, CheckStanding.VIOLATED, subject)]
    linguistic = derivation.linguistics.get(subject)
    if linguistic is not None and linguistic.standing is SiteStanding.REFUSED:
        return [
            _entry(
                law,
                CheckStanding.NOT_EVALUATED_BY_PREREQUISITE,
                subject,
                blocked_by=_blocker_of(linguistic),
            )
        ]
    return [_entry(law, CheckStanding.UNRESOLVED, subject)]


def _condition_sites(
    declaration: CaseDeclaration,
) -> tuple[tuple[str, ConditionSiteDeclaration | None], ...]:
    sites: list[tuple[str, ConditionSiteDeclaration | None]] = [
        (slot.slot_id, slot.condition_site)
        for slot in declaration.nisbah.predicate.slots
    ]
    sites.extend(
        (anchor.anchor_id, anchor.condition_site)
        for anchor in declaration.nisbah.anchors
    )
    return tuple(sites)


def _role_sites(
    declaration: CaseDeclaration,
) -> tuple[tuple[str, RoleSiteDeclaration | None], ...]:
    predicate = declaration.nisbah.predicate
    sites: list[tuple[str, RoleSiteDeclaration | None]] = [
        (predicate.predicate_id, predicate.role_site)
    ]
    sites.extend(
        (anchor.anchor_id, anchor.role_site) for anchor in declaration.nisbah.anchors
    )
    return tuple(sites)


def _evaluate_condition_sites(
    declaration: CaseDeclaration, derivation: PartialAuthorityDerivation
) -> tuple[list[LawCheckEntry], list[LawCheckEntry]]:
    shared: list[LawCheckEntry] = []
    licensed: list[LawCheckEntry] = []
    expected = _base_identity(derivation, declaration.lineage.base_id)
    for owner_id, site in _condition_sites(declaration):
        if site is None:
            shared.append(
                _entry(
                    ExecutionLaw.CONDITION_SITES_SHARE_THE_LINEAGE_BASE,
                    CheckStanding.UNRESOLVED,
                    owner_id,
                    expected,
                )
            )
            licensed.append(
                _entry(
                    ExecutionLaw.CONDITION_SITES_ARE_LICENSED_FOR_USE,
                    CheckStanding.UNRESOLVED,
                    owner_id,
                )
            )
            continue
        observed = _base_identity(derivation, site.base_id)
        shared.append(
            _entry(
                ExecutionLaw.CONDITION_SITES_SHARE_THE_LINEAGE_BASE,
                CheckStanding.UNRESOLVED
                if observed is None or expected is None
                else (
                    CheckStanding.SATISFIED
                    if observed == expected
                    else CheckStanding.VIOLATED
                ),
                owner_id,
                expected,
                observed,
            )
        )
        genus = _condition_genus(derivation, site.base_id, site.place_name)
        if genus is None:
            standing = CheckStanding.UNRESOLVED
        elif genus is PriorLicenseGenus.UNREAD:
            standing = CheckStanding.UNRESOLVED
        elif genus.licenses_use:
            standing = CheckStanding.SATISFIED
        else:
            standing = CheckStanding.VIOLATED
        licensed.append(
            _entry(
                ExecutionLaw.CONDITION_SITES_ARE_LICENSED_FOR_USE,
                standing,
                owner_id,
            )
        )
    return shared, licensed


def _evaluate_role_sites(
    declaration: CaseDeclaration, derivation: PartialAuthorityDerivation
) -> tuple[list[LawCheckEntry], list[LawCheckEntry], list[LawCheckEntry]]:
    lineage = declaration.lineage
    shared: list[LawCheckEntry] = []
    granted_for: list[LawCheckEntry] = []
    operative: list[LawCheckEntry] = []
    for owner_id, site in _role_sites(declaration):
        if site is None:
            shared.append(
                _entry(
                    ExecutionLaw.ROLE_SITES_SHARE_THE_LINEAGE_ONTOLOGY,
                    CheckStanding.UNRESOLVED,
                    owner_id,
                )
            )
            granted_for.append(
                _entry(
                    ExecutionLaw.ROLE_LICENSE_GRANTED_FOR_THE_FUNCTION_READ,
                    CheckStanding.UNRESOLVED,
                    owner_id,
                )
            )
            operative.append(
                _entry(
                    ExecutionLaw.ROLE_LICENSE_IS_OPERATIVE,
                    CheckStanding.UNRESOLVED,
                    owner_id,
                )
            )
            continue
        foreign = site.linguistic_ontology_id != lineage.linguistic_ontology_id
        shared.append(
            _entry(
                ExecutionLaw.ROLE_SITES_SHARE_THE_LINEAGE_ONTOLOGY,
                CheckStanding.VIOLATED if foreign else CheckStanding.SATISFIED,
                owner_id,
            )
        )
        attempt = derivation.linguistics.get(site.linguistic_ontology_id)
        if attempt is None or attempt.subject is None:
            blocker = (
                None
                if attempt is None or attempt.standing is not SiteStanding.REFUSED
                else _blocker_of(attempt)
            )
            standing = (
                CheckStanding.UNRESOLVED
                if blocker is None
                else CheckStanding.NOT_EVALUATED_BY_PREREQUISITE
            )
            granted_for.append(
                _entry(
                    ExecutionLaw.ROLE_LICENSE_GRANTED_FOR_THE_FUNCTION_READ,
                    standing,
                    owner_id,
                    blocked_by=blocker,
                )
            )
            operative.append(
                _entry(
                    ExecutionLaw.ROLE_LICENSE_IS_OPERATIVE,
                    standing,
                    owner_id,
                    blocked_by=blocker,
                )
            )
            continue
        ontology = attempt.subject
        try:
            granted = ontology.license(site.license_id)
        except ValueError:
            granted_for.append(
                _entry(
                    ExecutionLaw.ROLE_LICENSE_GRANTED_FOR_THE_FUNCTION_READ,
                    CheckStanding.VIOLATED,
                    owner_id,
                )
            )
            operative.append(
                _entry(
                    ExecutionLaw.ROLE_LICENSE_IS_OPERATIVE,
                    CheckStanding.NOT_EVALUATED_BY_PREREQUISITE,
                    owner_id,
                    blocked_by=(
                        ExecutionLaw.ROLE_LICENSE_GRANTED_FOR_THE_FUNCTION_READ
                    ),
                )
            )
            continue
        matches = granted.function_ref.function.value == site.function_name
        granted_for.append(
            _entry(
                ExecutionLaw.ROLE_LICENSE_GRANTED_FOR_THE_FUNCTION_READ,
                CheckStanding.SATISFIED if matches else CheckStanding.VIOLATED,
                owner_id,
            )
        )
        if not matches:
            operative.append(
                _entry(
                    ExecutionLaw.ROLE_LICENSE_IS_OPERATIVE,
                    CheckStanding.NOT_EVALUATED_BY_PREREQUISITE,
                    owner_id,
                    blocked_by=(
                        ExecutionLaw.ROLE_LICENSE_GRANTED_FOR_THE_FUNCTION_READ
                    ),
                )
            )
            continue
        operative.append(
            _entry(
                ExecutionLaw.ROLE_LICENSE_IS_OPERATIVE,
                CheckStanding.SATISFIED
                if granted.is_operative
                else CheckStanding.VIOLATED,
                owner_id,
            )
        )
    return shared, granted_for, operative


def _evaluate_predicate_shape(
    declaration: CaseDeclaration,
) -> tuple[
    list[LawCheckEntry], list[LawCheckEntry], list[LawCheckEntry], list[LawCheckEntry]
]:
    predicate = declaration.nisbah.predicate
    genus = ArityLicenseGenus(predicate.arity_license_name)
    permits = [
        _entry(
            ExecutionLaw.PREDICATE_ARITY_LICENSE_PERMITS_USE,
            CheckStanding.SATISFIED if genus.licenses_use else CheckStanding.VIOLATED,
            predicate.predicate_id,
        )
    ]
    positions = sorted(slot.position for slot in predicate.slots)
    slot_ids = tuple(slot.slot_id for slot in predicate.slots)
    shaped = (
        len(predicate.slots) == predicate.arity
        and positions == list(range(1, predicate.arity + 1))
        and len(set(slot_ids)) == len(slot_ids)
    )
    matches = [
        _entry(
            ExecutionLaw.PREDICATE_ARITY_MATCHES_ITS_SLOTS,
            CheckStanding.SATISFIED if shaped else CheckStanding.VIOLATED,
            predicate.predicate_id,
        )
    ]
    deferred: list[LawCheckEntry] = []
    for slot in predicate.slots:
        lowered = slot.slot_id.casefold()
        named = any(name in lowered for name in DEFERRED_ARGUMENT_ROLE_NAMES)
        deferred.append(
            _entry(
                ExecutionLaw.ARGUMENT_SLOT_IDS_ARE_NOT_DEFERRED_ROLE_NAMES,
                CheckStanding.VIOLATED if named else CheckStanding.SATISFIED,
                slot.slot_id,
            )
        )
    anchor_ids = tuple(anchor.anchor_id for anchor in declaration.nisbah.anchors)
    within = len(anchor_ids) <= predicate.arity and len(set(anchor_ids)) == len(
        anchor_ids
    )
    anchors = [
        _entry(
            ExecutionLaw.ANCHORS_DO_NOT_EXCEED_ARITY,
            CheckStanding.SATISFIED if within else CheckStanding.VIOLATED,
            declaration.nisbah.nisbah_id,
        )
    ]
    return permits, matches, deferred, anchors


def _evaluate_declared_linguistic_identity(
    declaration: CaseDeclaration, derivation: PartialAuthorityDerivation
) -> list[LawCheckEntry]:
    law = ExecutionLaw.DECLARED_LINGUISTIC_IDENTITY_AGREES
    declared = _lineage_ontology(declaration)
    if declared is None:
        return [
            _entry(
                law,
                CheckStanding.UNRESOLVED,
                declaration.lineage.linguistic_ontology_id,
            )
        ]
    if declared.declared_content_id is None:
        return [
            _entry(law, CheckStanding.NOT_APPLICABLE_NO_CLAIM, declared.ontology_id)
        ]
    expected = Identity(
        id=declared.ontology_id, content_id=declared.declared_content_id
    )
    attempt = derivation.linguistics.get(declared.ontology_id)
    if attempt is None or attempt.subject is None:
        blocker = (
            None
            if attempt is None or attempt.standing is not SiteStanding.REFUSED
            else _blocker_of(attempt)
        )
        return [
            _entry(
                law,
                CheckStanding.UNRESOLVED
                if blocker is None
                else CheckStanding.NOT_EVALUATED_BY_PREREQUISITE,
                declared.ontology_id,
                expected,
                blocked_by=blocker,
            )
        ]
    observed = Identity(
        id=attempt.subject.ontology_id, content_id=attempt.subject.content_id
    )
    return [
        _entry(
            law,
            CheckStanding.SATISFIED if observed == expected else CheckStanding.VIOLATED,
            declared.ontology_id,
            expected,
            observed,
        )
    ]


def evaluate_laws(
    declaration: CaseDeclaration, derivation: PartialAuthorityDerivation
) -> tuple[LawCheckEntry, ...]:
    """قيِّم القوانينَ من الأولى إلى السابعةَ عشرةَ على ترتيب القائمة المجمَّدة."""

    self_derived, unread = _evaluate_licensing_genus(declaration, derivation)
    registered, shared_bases = _evaluate_license_origins(declaration, derivation)
    shared_conditions, licensed_conditions = _evaluate_condition_sites(
        declaration, derivation
    )
    shared_roles, granted_roles, operative_roles = _evaluate_role_sites(
        declaration, derivation
    )
    permits, matches, deferred, anchors = _evaluate_predicate_shape(declaration)
    trace: list[LawCheckEntry] = []
    trace.extend(self_derived)
    trace.extend(unread)
    trace.extend(_evaluate_general_foundation(declaration, derivation))
    trace.extend(registered)
    trace.extend(shared_bases)
    trace.extend(_evaluate_linguistic_foundation(declaration, derivation))
    trace.extend(_evaluate_lineage(declaration, derivation))
    trace.extend(shared_conditions)
    trace.extend(licensed_conditions)
    trace.extend(shared_roles)
    trace.extend(granted_roles)
    trace.extend(operative_roles)
    trace.extend(permits)
    trace.extend(matches)
    trace.extend(deferred)
    trace.extend(anchors)
    trace.extend(_evaluate_declared_linguistic_identity(declaration, derivation))
    return tuple(trace)


def aggregate_outcome(trace: tuple[LawCheckEntry, ...]) -> ExecutionOutcome:
    """اجمع الحكمَ من المنازل المُسجَّلة وحدَها: مخالفةٌ تحجب، ونقصٌ يؤجِّل."""

    if any(entry.standing is CheckStanding.VIOLATED for entry in trace):
        return ExecutionOutcome.BLOCK
    if any(entry.standing is CheckStanding.UNRESOLVED for entry in trace):
        return ExecutionOutcome.DEFER
    return ExecutionOutcome.PASS


def violations_of(trace: tuple[LawCheckEntry, ...]) -> tuple[Violation, ...]:
    """المخالفاتُ الثابتةُ وحدَها؛ ولا تُصنَع مخالفةٌ من منزلةٍ غيرِ ثابتة."""

    return tuple(
        Violation(
            law=entry.law,
            subject_id=entry.subject_id,
            expected=entry.expected,
            observed=entry.observed,
        )
        for entry in trace
        if entry.standing is CheckStanding.VIOLATED
    )


def residuals_of(
    declaration: CaseDeclaration, trace: tuple[LawCheckEntry, ...]
) -> tuple[UnresolvedRequirement, ...]:
    """البقايا: مطالبُ غيرُ محسومةٍ مُسمّاةٌ بسلطتها؛ والمحجوبُ ليس منها."""

    collected: dict[tuple[str, str], UnresolvedRequirement] = {}
    for requirement in declaration.unresolved_requirements:
        key = (requirement.required_authority.value, requirement.subject_id)
        collected[key] = requirement
    for entry in trace:
        if entry.standing is not CheckStanding.UNRESOLVED:
            continue
        law = ExecutionLaw(entry.law)
        authority = _AUTHORITY_OF_LAW[law]
        subject = entry.subject_id or declaration.nisbah.nisbah_id
        key = (authority.value, subject)
        if key in collected:
            continue
        collected[key] = UnresolvedRequirement(
            required_authority=authority,
            subject_id=subject,
            standing=RequirementStanding.UNRESOLVED,
        )
    return tuple(collected[key] for key in sorted(collected))
