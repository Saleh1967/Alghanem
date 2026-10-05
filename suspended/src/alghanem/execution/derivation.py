"""الاشتقاقُ الجزئيّ: ما استطاع التصريحُ أن يُقيمَه من سلطةٍ حقيقيّةٍ قبل الحكم.

    CaseDeclaration  →  PartialAuthorityDerivation

وكلُّ موضعٍ هنا يمرّ من **بابه** لا من جانبه: `PriorConditionRef.of` و
`OntologicalCandidateRef.of` و`LicensedRoleRefV3.of` و`ExistenceLineageRef.of`.
فإذا ردَّ البابُ موضعًا **سُجِّل ردُّه ولم يُرمَ الاستثناءُ خارجًا**؛ لأنّ الردَّ
مادّةُ الحكم لا عطبٌ في المحرّك.

**والاشتقاقُ ليس حكمًا** (`ADerivationIsNotAVerdict`): هذه الطبقةُ لا تقول
`PASS` ولا `BLOCK` ولا `DEFER`؛ إنّما تقول ما قام وما رُدَّ وما بقي غيرَ محسوم،
ثمّ تتولّى طبقةُ القوانين وحدَها ترجمةَ ذلك إلى حكم.

**ولا تُنشَأ النسبةُ هنا** (`JudgmentPrecedesConstruction`): بناءُ
`AnchoredNisbahSignatureV3` نفسُه يرفض اختلاطَ الأصل، فلو أنشأناه قبل الحكم
لأصدر الباني الحكمَ بدل المحرّك، ولَما بقي أثرٌ يُقرأ.

تسجيلٌ لا سلطة: لا ولادةَ ولا حكمَ ولادةٍ ولا تجميدَ `E0`.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Final, Generic, TypeVar

from ..linguistic.anchored_v3 import AnchoredV3Error, LicensedRoleRefV3
from ..ontology.general import GeneralOntology
from ..ontology.lineage import ExistenceLineageError, ExistenceLineageRef
from ..ontology.linguistic import LinguisticFunction
from ..ontology.linguistic_v2 import (
    LinguisticOntologyV2,
    LinguisticOntologyV2Error,
    ReferencedFunctionalLicense,
)
from ..prior.conditions import (
    PriorConditionKind,
    PriorInformationBase,
    PriorInformationError,
    PriorLicenseGenus,
)
from ..prior.references import PriorConditionRef
from .declaration import (
    CaseDeclaration,
    ConditionSiteDeclaration,
    RoleSiteDeclaration,
)
from .validation import DeclaredLevels

__all__ = [
    "A_DERIVATION_IS_NOT_A_VERDICT",
    "DerivedSite",
    "PartialAuthorityDerivation",
    "RefusalKind",
    "SiteKey",
    "SiteOwnerKind",
    "SiteStanding",
    "derive_partial_authority",
]


A_DERIVATION_IS_NOT_A_VERDICT: Final[str] = (
    "الاشتقاقُ ليس حكمًا: هذه الطبقةُ تُقيم ما يمكن إقامتُه وتُسجّل ما رُدَّ، "
    "ولا تُصدِر `PASS` ولا `BLOCK` ولا `DEFER`؛ فالحكمُ لطبقة القوانين وحدَها"
)


class SiteStanding(Enum):
    """قيامُ الموضع: قام، أو رُدَّ ببابه، أو بقي غيرَ محسوم، أو لم يُحاوَل بعد."""

    DERIVED = "derived"
    REFUSED = "refused"
    UNRESOLVED = "unresolved"
    NOT_ATTEMPTED = "not_attempted"


class RefusalKind(Enum):
    """أسبابُ الردّ مفردةٌ مغلقة؛ ولا سببَ يُكتَب نثرًا خارجها."""

    CONDITION_IS_SELF_DERIVED = "condition_is_self_derived"
    CONDITION_IS_NOT_LICENSED_FOR_USE = "condition_is_not_licensed_for_use"
    CANDIDATE_IS_NOT_REGISTERED = "candidate_is_not_registered"
    LICENSE_IS_ABSENT = "license_is_absent"
    LICENSE_IS_FOR_ANOTHER_FUNCTION = "license_is_for_another_function"
    LICENSE_IS_NOT_OPERATIVE = "license_is_not_operative"
    LICENSE_BASE_DIFFERS_FROM_THE_FOUNDING_BASE = (
        "license_base_differs_from_the_founding_base"
    )
    FOUNDATION_WAS_REFUSED = "foundation_was_refused"
    LINEAGE_DID_NOT_DERIVE = "lineage_did_not_derive"


class SiteOwnerKind(Enum):
    """صاحبُ الموضع في النسبة؛ ولا يُخلَط محمولٌ بموضع حجّةٍ ولا بمرساة."""

    PREDICATE = "predicate"
    SLOT = "slot"
    ANCHOR = "anchor"


@dataclass(frozen=True, slots=True)
class SiteKey:
    """مفتاحُ الموضع: صنفُ صاحبه ومُعرِّفُه؛ ولا يُقرَأ مُعرِّفٌ وحدَه."""

    owner_kind: SiteOwnerKind
    owner_id: str

    def as_canonical_content(self) -> dict[str, object]:
        """محتوى المفتاح للأثر."""

        return {"owner_kind": self.owner_kind.value, "owner_id": self.owner_id}


_Subject = TypeVar("_Subject")


@dataclass(frozen=True)
class DerivedSite(Generic[_Subject]):
    """نتيجةُ محاولةٍ واحدةٍ عند باب: ما قام، أو سببُ ردِّه، بلا نثرٍ بينهما."""

    standing: SiteStanding
    subject: _Subject | None = None
    refusal: RefusalKind | None = None
    observed: str | None = None

    def __post_init__(self) -> None:
        if self.standing is SiteStanding.DERIVED:
            if self.subject is None or self.refusal is not None:
                raise ValueError("موضعٌ قائمٌ يحمل مُشتَقَّه ولا يحمل سببَ ردّ")
        elif self.standing is SiteStanding.REFUSED:
            if self.subject is not None or self.refusal is None:
                raise ValueError("موضعٌ مردودٌ يحمل سببَ ردِّه ولا يحمل مُشتَقًّا")
        elif self.subject is not None or self.refusal is not None:
            raise ValueError("موضعٌ غيرُ محسومٍ لا يحمل مُشتَقًّا ولا سببَ ردّ")

    @property
    def is_derived(self) -> bool:
        """أقام الموضعُ فعلًا؟ خاصّيّةٌ تُشتَقّ لا حقلٌ يُكتَب بجانبها."""

        return self.standing is SiteStanding.DERIVED

    def as_canonical_content(self) -> dict[str, object]:
        """محتوى المحاولة للأثر؛ والمُشتَقُّ نفسُه ليس أثرًا يُنسَخ هنا."""

        return {
            "standing": self.standing.value,
            "refusal": None if self.refusal is None else self.refusal.value,
            "observed": self.observed,
        }


def _unresolved(_kind: type[_Subject]) -> DerivedSite[_Subject]:
    return DerivedSite(SiteStanding.UNRESOLVED)


def _not_attempted(_kind: type[_Subject]) -> DerivedSite[_Subject]:
    return DerivedSite(SiteStanding.NOT_ATTEMPTED)


def _refused(
    _kind: type[_Subject], refusal: RefusalKind, observed: str | None = None
) -> DerivedSite[_Subject]:
    return DerivedSite(SiteStanding.REFUSED, refusal=refusal, observed=observed)


def _derive_condition_ref(
    base: PriorInformationBase, place: PriorConditionKind
) -> DerivedSite[PriorConditionRef]:
    """امرر الشرطَ من بابه؛ والشرطُ غيرُ المقروء نقصُ دليلٍ لا مخالفةُ أصل."""

    condition = base.condition(place)
    if condition.licensed_by is PriorLicenseGenus.UNREAD:
        return _unresolved(PriorConditionRef)
    if condition.licensed_by is PriorLicenseGenus.DERIVED_FROM_THE_ONTOLOGY_IT_LICENSES:
        return _refused(
            PriorConditionRef,
            RefusalKind.CONDITION_IS_SELF_DERIVED,
            condition.licensed_by.value,
        )
    try:
        return DerivedSite(
            SiteStanding.DERIVED, subject=PriorConditionRef.of(base, place)
        )
    except PriorInformationError:
        return _refused(
            PriorConditionRef,
            RefusalKind.CONDITION_IS_NOT_LICENSED_FOR_USE,
            condition.licensed_by.value,
        )


def _derive_license(
    declared: object,
    general: GeneralOntology,
    bases: dict[str, PriorInformationBase],
) -> DerivedSite[ReferencedFunctionalLicense]:
    """امنح رخصةً من مرشَّحٍ مُسجَّلٍ وشرطٍ قائم؛ وكلُّ ردٍّ يُسمَّى بسببه."""

    from .declaration import LicenseDeclaration

    if not isinstance(declared, LicenseDeclaration):  # pragma: no cover - guard
        raise TypeError("الرخصةُ المُصرَّحُ بها من نوعها")
    base = bases.get(declared.condition_base_id)
    if base is None:
        return _not_attempted(ReferencedFunctionalLicense)
    try:
        candidate = general.candidate(declared.candidate_id)
    except ValueError:
        return _refused(
            ReferencedFunctionalLicense,
            RefusalKind.CANDIDATE_IS_NOT_REGISTERED,
            declared.candidate_id,
        )
    place = PriorConditionKind(declared.condition_place_name)
    condition_site = _derive_condition_ref(base, place)
    if condition_site.standing is SiteStanding.UNRESOLVED:
        return _unresolved(ReferencedFunctionalLicense)
    if condition_site.refusal is not None:
        return _refused(
            ReferencedFunctionalLicense,
            condition_site.refusal,
            condition_site.observed,
        )
    try:
        granted = ReferencedFunctionalLicense.granted(
            license_id=declared.license_id,
            candidate=candidate,
            function=LinguisticFunction(declared.function_name),
            read_from=declared.read_from,
            base=base,
            place=place,
        )
    except (LinguisticOntologyV2Error, PriorInformationError):
        return _refused(ReferencedFunctionalLicense, RefusalKind.FOUNDATION_WAS_REFUSED)
    return DerivedSite(SiteStanding.DERIVED, subject=granted)


def _derive_role_ref(
    site: RoleSiteDeclaration,
    linguistics: dict[str, DerivedSite[LinguisticOntologyV2]],
) -> DerivedSite[LicensedRoleRefV3]:
    """امرر الدورَ من بابه في `O_L²`؛ ولكلِّ ردٍّ اسمُه المفرد."""

    derived = linguistics.get(site.linguistic_ontology_id)
    if derived is None or derived.subject is None:
        return _not_attempted(LicensedRoleRefV3)
    ontology = derived.subject
    function = LinguisticFunction(site.function_name)
    try:
        granted = ontology.license(site.license_id)
    except LinguisticOntologyV2Error:
        return _refused(
            LicensedRoleRefV3, RefusalKind.LICENSE_IS_ABSENT, site.license_id
        )
    if granted.function_ref.function is not function:
        return _refused(
            LicensedRoleRefV3,
            RefusalKind.LICENSE_IS_FOR_ANOTHER_FUNCTION,
            granted.function_ref.function.value,
        )
    if not granted.is_operative:
        return _refused(
            LicensedRoleRefV3,
            RefusalKind.LICENSE_IS_NOT_OPERATIVE,
            granted.function_ref.function.value,
        )
    try:
        role_ref = LicensedRoleRefV3.of(ontology, site.license_id, function)
    except AnchoredV3Error:
        return _refused(LicensedRoleRefV3, RefusalKind.FOUNDATION_WAS_REFUSED)
    return DerivedSite(SiteStanding.DERIVED, subject=role_ref)


def _derive_condition_site(
    site: ConditionSiteDeclaration, bases: dict[str, PriorInformationBase]
) -> DerivedSite[PriorConditionRef]:
    base = bases.get(site.base_id)
    if base is None:
        return _not_attempted(PriorConditionRef)
    return _derive_condition_ref(base, PriorConditionKind(site.place_name))


@dataclass(frozen=True, slots=True)
class PartialAuthorityDerivation:
    """ما قام من سلطةٍ وما رُدَّ؛ مادّةُ الحكم كلُّها ولا حكمَ فيها."""

    bases: dict[str, PriorInformationBase] = field(default_factory=dict)
    generals: dict[str, GeneralOntology] = field(default_factory=dict)
    licenses: dict[tuple[str, str], DerivedSite[ReferencedFunctionalLicense]] = field(
        default_factory=dict
    )
    linguistics: dict[str, DerivedSite[LinguisticOntologyV2]] = field(
        default_factory=dict
    )
    lineage: DerivedSite[ExistenceLineageRef] = field(
        default_factory=lambda: DerivedSite(SiteStanding.NOT_ATTEMPTED)
    )
    role_sites: dict[SiteKey, DerivedSite[LicensedRoleRefV3]] = field(
        default_factory=dict
    )
    condition_sites: dict[SiteKey, DerivedSite[PriorConditionRef]] = field(
        default_factory=dict
    )

    @property
    def lineage_subject(self) -> ExistenceLineageRef | None:
        """السلسلةُ إن قامت؛ والغيابُ غيابٌ لا يُقرَأ قيامًا."""

        return self.lineage.subject


def derive_partial_authority(
    declaration: CaseDeclaration, levels: DeclaredLevels
) -> PartialAuthorityDerivation:
    """أقِم ما يمكن إقامتُه من التصريح؛ ولا يخرج من هنا استثناءٌ ولا حكم."""

    bases = dict(levels.bases)
    generals = dict(levels.generals)
    licenses: dict[tuple[str, str], DerivedSite[ReferencedFunctionalLicense]] = {}
    linguistics: dict[str, DerivedSite[LinguisticOntologyV2]] = {}
    for declared in declaration.linguistic_ontologies:
        general = generals.get(declared.founded_on_general_id)
        if general is None:
            linguistics[declared.ontology_id] = _not_attempted(LinguisticOntologyV2)
            continue
        granted_licenses: list[ReferencedFunctionalLicense] = []
        unresolved = False
        refused = False
        for declared_license in declared.licenses:
            attempt = _derive_license(declared_license, general, bases)
            licenses[(declared.ontology_id, declared_license.license_id)] = attempt
            if attempt.subject is not None:
                granted_licenses.append(attempt.subject)
            elif attempt.standing is SiteStanding.UNRESOLVED:
                unresolved = True
            else:
                refused = True
        if refused:
            linguistics[declared.ontology_id] = _refused(
                LinguisticOntologyV2, RefusalKind.FOUNDATION_WAS_REFUSED
            )
            continue
        if unresolved or not granted_licenses:
            linguistics[declared.ontology_id] = _unresolved(LinguisticOntologyV2)
            continue
        foreign = tuple(
            granted.license_id
            for granted in granted_licenses
            if granted.condition_ref.base_id != general.prior_base_ref.base_id
            or granted.condition_ref.base_content_id
            != general.prior_base_ref.content_id
        )
        if foreign:
            linguistics[declared.ontology_id] = _refused(
                LinguisticOntologyV2,
                RefusalKind.LICENSE_BASE_DIFFERS_FROM_THE_FOUNDING_BASE,
                foreign[0],
            )
            continue
        try:
            ontology = LinguisticOntologyV2.founded_on(
                declared.ontology_id, general, tuple(granted_licenses)
            )
        except LinguisticOntologyV2Error:
            linguistics[declared.ontology_id] = _refused(
                LinguisticOntologyV2, RefusalKind.FOUNDATION_WAS_REFUSED
            )
            continue
        linguistics[declared.ontology_id] = DerivedSite(
            SiteStanding.DERIVED, subject=ontology
        )

    declared_lineage = declaration.lineage
    general = generals.get(declared_lineage.general_ontology_id)
    linguistic_attempt = linguistics.get(declared_lineage.linguistic_ontology_id)
    lineage: DerivedSite[ExistenceLineageRef] = _not_attempted(ExistenceLineageRef)
    if general is not None and linguistic_attempt is not None:
        if linguistic_attempt.standing is SiteStanding.UNRESOLVED:
            lineage = _unresolved(ExistenceLineageRef)
        elif linguistic_attempt.subject is not None:
            try:
                lineage = DerivedSite(
                    SiteStanding.DERIVED,
                    subject=ExistenceLineageRef.of(general, linguistic_attempt.subject),
                )
            except ExistenceLineageError:
                lineage = _refused(
                    ExistenceLineageRef, RefusalKind.LINEAGE_DID_NOT_DERIVE
                )

    role_sites: dict[SiteKey, DerivedSite[LicensedRoleRefV3]] = {}
    condition_sites: dict[SiteKey, DerivedSite[PriorConditionRef]] = {}
    predicate = declaration.nisbah.predicate
    predicate_key = SiteKey(SiteOwnerKind.PREDICATE, predicate.predicate_id)
    role_sites[predicate_key] = (
        _unresolved(LicensedRoleRefV3)
        if predicate.role_site is None
        else _derive_role_ref(predicate.role_site, linguistics)
    )
    for slot in predicate.slots:
        key = SiteKey(SiteOwnerKind.SLOT, slot.slot_id)
        condition_sites[key] = (
            _unresolved(PriorConditionRef)
            if slot.condition_site is None
            else _derive_condition_site(slot.condition_site, bases)
        )
    for anchor in declaration.nisbah.anchors:
        role_key = SiteKey(SiteOwnerKind.ANCHOR, anchor.anchor_id)
        role_sites[role_key] = (
            _unresolved(LicensedRoleRefV3)
            if anchor.role_site is None
            else _derive_role_ref(anchor.role_site, linguistics)
        )
        condition_sites[role_key] = (
            _unresolved(PriorConditionRef)
            if anchor.condition_site is None
            else _derive_condition_site(anchor.condition_site, bases)
        )
    return PartialAuthorityDerivation(
        bases=bases,
        generals=generals,
        licenses=licenses,
        linguistics=linguistics,
        lineage=lineage,
        role_sites=role_sites,
        condition_sites=condition_sites,
    )
