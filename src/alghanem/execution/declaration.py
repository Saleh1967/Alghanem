"""التصريحُ المرشَّح: وصفٌ خاملٌ يُعاد منه الاشتقاق، لا سلطةٌ تُفكّ من نصّ.

    Declaration  →  Validation  →  PartialDerivation  →  LawEvaluation

**والتصريحُ ليس سلطة** (`ADeclarationIsNotAnAuthority`): أنواعُ هذه الوحدة
حقولُها نصوصٌ وأعدادٌ وأعضاءُ مفرداتٍ مغلقة، وليس فيها شاهدُ اشتقاقٍ ولا
`PriorConditionRef` ولا `LicensedRoleRefV3` ولا بصمةٌ ذاتُ سلطة. فقولُ
التصريح «شرطُ هذه المرساة في الموضع الفلانيّ من القاعدة الفلانيّة» دعوى عن
**أين يُنظَر**، لا مرجعٌ مُرخِّص.

**والحكمُ سابقٌ على البناء** (`JudgmentPrecedesConstruction`): لهذا يجوز أن
يُصرَّح بأكثر من قاعدةٍ سابقةٍ وأكثر من أنطولوجيا في الوثيقة الواحدة، وكلُّ
موضعٍ يُسمّي أصلَه بنفسه. وهذا وحدَه ما يجعل خلطَ الأصلين قابلًا للقول، فيراه
المحرّكُ ويحكم عليه، بدل أن يرفضه بانٍ سلطويٌّ قبل أن يصل إليه الحكم.

تسجيلٌ لا سلطة: لا ولادةَ ولا حكمَ ولادةٍ ولا تجميدَ `E0`.
"""

from __future__ import annotations

from dataclasses import dataclass, fields
from typing import Final

from ..canonical_content import canonical_bytes, canonical_digest
from .requirement import UnresolvedRequirement

__all__ = [
    "A_DECLARATION_IS_NOT_AN_AUTHORITY",
    "EXECUTION_DOCUMENT_SCHEMA",
    "JUDGMENT_PRECEDES_CONSTRUCTION",
    "AnchorDeclaration",
    "CandidateDeclaration",
    "CaseDeclaration",
    "ConditionSiteDeclaration",
    "GeneralOntologyDeclaration",
    "LicenseDeclaration",
    "LineageDeclaration",
    "LinguisticOntologyDeclaration",
    "NisbahDeclaration",
    "PredicateDeclaration",
    "PriorBaseDeclaration",
    "PriorConditionDeclaration",
    "RoleSiteDeclaration",
    "SlotDeclaration",
]


EXECUTION_DOCUMENT_SCHEMA: Final[str] = "alghanem.execution.v1"
"""اسمُ عقد الإدخال؛ وثيقةٌ بعقدٍ آخر لا تُقرَأ بهذا العقد بالسهو."""

A_DECLARATION_IS_NOT_AN_AUTHORITY: Final[str] = (
    "التصريحُ ليس سلطة: حقولُه دعاوى عن مواضعِ النظر، والسلطةُ تُشتَقّ بعدَه من "
    "الأبواب القائمة؛ ووثيقةٌ تُفَكّ مراجعَ سلطويّةً مباشرةً تمنح رخصةً لم تُمنَح"
)

JUDGMENT_PRECEDES_CONSTRUCTION: Final[str] = (
    "الحكمُ سابقٌ على البناء: لو أُنشئ الكائنُ السلطويُّ النهائيُّ قبل الحكم "
    "لرفض حُرّاسُه الحالةَ المختلطة، فلا يكون المحرّكُ هو الذي أثبت الحجب، "
    "ويعود التنفيذُ آلةَ قبولٍ لما نجا أصلًا من كلّ الحُرّاس"
)


def _require_text(value: object, label: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise TypeError(f"{label} نصٌّ غير فارغ")
    return value


def _require_optional_text(value: object, label: str) -> str | None:
    if value is None:
        return None
    return _require_text(value, label)


@dataclass(frozen=True, slots=True)
class PriorConditionDeclaration:
    """تصريحُ شرطٍ سابق: أسماءُ مواضعَ وأجناسٍ نصًّا، لا أعضاءُ مفرداتٍ سلطويّة."""

    condition_id: str
    kind_name: str
    statement: str
    what_it_forbids: str
    licensed_by_name: str

    def __post_init__(self) -> None:
        _require_text(self.condition_id, "مُعرِّفُ الشرط المُصرَّح به")
        _require_text(self.kind_name, "اسمُ موضع الشرط")
        _require_text(self.statement, "نصُّ الشرط")
        _require_text(self.what_it_forbids, "ما يمنعه الشرط")
        _require_text(self.licensed_by_name, "اسمُ جنس ترخيص الشرط")

    def as_canonical_content(self) -> dict[str, object]:
        """محتوى التصريح للبصمة."""

        return {
            "condition_id": self.condition_id,
            "kind": self.kind_name,
            "statement": self.statement,
            "what_it_forbids": self.what_it_forbids,
            "licensed_by": self.licensed_by_name,
        }


@dataclass(frozen=True, slots=True)
class PriorBaseDeclaration:
    """تصريحُ قاعدةٍ سابقة، ببصمةٍ مُعلَنةٍ تُفحَص قبل الحكم لا بعده."""

    base_id: str
    domain_note: str
    declared_content_id: str
    conditions: tuple[PriorConditionDeclaration, ...]

    def __post_init__(self) -> None:
        _require_text(self.base_id, "مُعرِّفُ القاعدة المُصرَّح بها")
        _require_text(self.domain_note, "بيانُ مجال القاعدة")
        _require_text(self.declared_content_id, "البصمةُ المُعلَنة للقاعدة")
        if not isinstance(self.conditions, tuple):
            raise TypeError("شروطُ القاعدة مجموعةٌ مُصرَّحٌ بها")

    def as_canonical_content(self) -> dict[str, object]:
        """محتوى التصريح للبصمة."""

        return {
            "base_id": self.base_id,
            "domain_note": self.domain_note,
            "declared_content_id": self.declared_content_id,
            "conditions": [
                condition.as_canonical_content() for condition in self.conditions
            ],
        }


@dataclass(frozen=True, slots=True)
class CandidateDeclaration:
    """تصريحُ مرشَّحٍ أنطولوجيّ؛ نوعُه وموضعُ ترخيصه اسمان لا عضوان."""

    candidate_id: str
    kind_name: str
    necessity_claim: str
    irreducibility_claim: str
    licensing_condition_name: str

    def __post_init__(self) -> None:
        _require_text(self.candidate_id, "مُعرِّفُ المرشَّح المُصرَّح به")
        _require_text(self.kind_name, "اسمُ نوع المرشَّح")
        _require_text(self.necessity_claim, "دعوى ضرورة المرشَّح")
        _require_text(self.irreducibility_claim, "دعوى عدم اختزال المرشَّح")
        _require_text(self.licensing_condition_name, "اسمُ موضع الشرط المُرخِّص")

    def as_canonical_content(self) -> dict[str, object]:
        """محتوى التصريح للبصمة."""

        return {
            "candidate_id": self.candidate_id,
            "kind": self.kind_name,
            "necessity_claim": self.necessity_claim,
            "irreducibility_claim": self.irreducibility_claim,
            "licensing_condition": self.licensing_condition_name,
        }


@dataclass(frozen=True, slots=True)
class GeneralOntologyDeclaration:
    """تصريحُ `O_0`: أصلُها مُسمًّى، وبصمتُها مُعلَنةٌ تُفحَص قبل الحكم."""

    ontology_id: str
    founded_on_base_id: str
    declared_content_id: str
    candidates: tuple[CandidateDeclaration, ...]

    def __post_init__(self) -> None:
        _require_text(self.ontology_id, "مُعرِّفُ الأنطولوجيا العامّة")
        _require_text(self.founded_on_base_id, "مُعرِّفُ القاعدة المؤسِّسة")
        _require_text(self.declared_content_id, "البصمةُ المُعلَنة للأنطولوجيا العامّة")
        if not isinstance(self.candidates, tuple):
            raise TypeError("مرشَّحو الأنطولوجيا مجموعةٌ مُصرَّحٌ بها")

    def as_canonical_content(self) -> dict[str, object]:
        """محتوى التصريح للبصمة."""

        return {
            "ontology_id": self.ontology_id,
            "founded_on_base_id": self.founded_on_base_id,
            "declared_content_id": self.declared_content_id,
            "candidates": [
                candidate.as_canonical_content() for candidate in self.candidates
            ],
        }


@dataclass(frozen=True, slots=True)
class LicenseDeclaration:
    """تصريحُ رخصةٍ وظيفيّة؛ وشرطُها موضعٌ في قاعدةٍ **يُسمّيها بنفسه**."""

    license_id: str
    candidate_id: str
    function_name: str
    read_from: str
    condition_base_id: str
    condition_place_name: str

    def __post_init__(self) -> None:
        _require_text(self.license_id, "مُعرِّفُ الرخصة المُصرَّح بها")
        _require_text(self.candidate_id, "مُعرِّفُ المرشَّح المُرخَّص")
        _require_text(self.function_name, "اسمُ الوظيفة")
        _require_text(self.read_from, "حاملُ قراءة الوظيفة")
        _require_text(self.condition_base_id, "مُعرِّفُ قاعدة شرط الرخصة")
        _require_text(self.condition_place_name, "اسمُ موضع شرط الرخصة")

    def as_canonical_content(self) -> dict[str, object]:
        """محتوى التصريح للبصمة."""

        return {
            "license_id": self.license_id,
            "candidate_id": self.candidate_id,
            "function": self.function_name,
            "read_from": self.read_from,
            "condition_base_id": self.condition_base_id,
            "condition_place": self.condition_place_name,
        }


@dataclass(frozen=True, slots=True)
class LinguisticOntologyDeclaration:
    """تصريحُ `O_L²`؛ وبصمتُها المُعلَنةُ دعوًى تُفحَص في طبقة القوانين لا قبلها."""

    ontology_id: str
    founded_on_general_id: str
    declared_content_id: str | None
    licenses: tuple[LicenseDeclaration, ...]

    def __post_init__(self) -> None:
        _require_text(self.ontology_id, "مُعرِّفُ الأنطولوجيا اللغويّة")
        _require_text(self.founded_on_general_id, "مُعرِّفُ الأنطولوجيا العامّة المؤسِّسة")
        _require_optional_text(
            self.declared_content_id, "البصمةُ المُعلَنة للأنطولوجيا اللغويّة"
        )
        if not isinstance(self.licenses, tuple):
            raise TypeError("رخصُ الأنطولوجيا مجموعةٌ مُصرَّحٌ بها")

    def as_canonical_content(self) -> dict[str, object]:
        """محتوى التصريح للبصمة."""

        return {
            "ontology_id": self.ontology_id,
            "founded_on_general_id": self.founded_on_general_id,
            "declared_content_id": self.declared_content_id,
            "licenses": [granted.as_canonical_content() for granted in self.licenses],
        }


@dataclass(frozen=True, slots=True)
class LineageDeclaration:
    """تصريحُ السلسلة: ثلاثةُ مُعرِّفاتٍ تُسمّي مستوياتٍ مُصرَّحًا بها في الوثيقة."""

    base_id: str
    general_ontology_id: str
    linguistic_ontology_id: str

    def __post_init__(self) -> None:
        _require_text(self.base_id, "مُعرِّفُ قاعدة السلسلة")
        _require_text(self.general_ontology_id, "مُعرِّفُ أنطولوجيا السلسلة العامّة")
        _require_text(self.linguistic_ontology_id, "مُعرِّفُ أنطولوجيا السلسلة اللغويّة")

    def as_canonical_content(self) -> dict[str, object]:
        """محتوى التصريح للبصمة."""

        return {
            "base_id": self.base_id,
            "general_ontology_id": self.general_ontology_id,
            "linguistic_ontology_id": self.linguistic_ontology_id,
        }


@dataclass(frozen=True, slots=True)
class RoleSiteDeclaration:
    """موضعُ دورٍ: أنطولوجيا مُسمّاةٌ ورخصةٌ فيها ووظيفةٌ تُقرأ لها."""

    linguistic_ontology_id: str
    license_id: str
    function_name: str

    def __post_init__(self) -> None:
        _require_text(self.linguistic_ontology_id, "مُعرِّفُ أنطولوجيا موضع الدور")
        _require_text(self.license_id, "مُعرِّفُ رخصة موضع الدور")
        _require_text(self.function_name, "اسمُ وظيفة موضع الدور")

    def as_canonical_content(self) -> dict[str, object]:
        """محتوى الموضع للبصمة."""

        return {
            "linguistic_ontology_id": self.linguistic_ontology_id,
            "license_id": self.license_id,
            "function": self.function_name,
        }


@dataclass(frozen=True, slots=True)
class ConditionSiteDeclaration:
    """موضعُ شرطٍ: قاعدةٌ مُسمّاةٌ وموضعٌ فيها؛ دعوى نظرٍ لا مرجعٌ مُرخِّص."""

    base_id: str
    place_name: str

    def __post_init__(self) -> None:
        _require_text(self.base_id, "مُعرِّفُ قاعدة موضع الشرط")
        _require_text(self.place_name, "اسمُ موضع الشرط")

    def as_canonical_content(self) -> dict[str, object]:
        """محتوى الموضع للبصمة."""

        return {"base_id": self.base_id, "place": self.place_name}


@dataclass(frozen=True, slots=True)
class SlotDeclaration:
    """تصريحُ موضعِ حجّة؛ وغيابُ شرطه يلزمه مطلبٌ غيرُ محسومٍ يُسمّيه."""

    slot_id: str
    position: int
    condition_site: ConditionSiteDeclaration | None

    def __post_init__(self) -> None:
        _require_text(self.slot_id, "مُعرِّفُ الموضع المُصرَّح به")
        if type(self.position) is not int:
            raise TypeError("رتبةُ الموضع عددٌ صحيح")
        if self.condition_site is not None and not isinstance(
            self.condition_site, ConditionSiteDeclaration
        ):
            raise TypeError("موضعُ شرط الحجّة من نوعه أو غائبٌ مُصرَّحٌ بغيابه")

    def as_canonical_content(self) -> dict[str, object]:
        """محتوى التصريح للبصمة."""

        return {
            "slot_id": self.slot_id,
            "position": self.position,
            "condition_site": (
                None
                if self.condition_site is None
                else self.condition_site.as_canonical_content()
            ),
        }


@dataclass(frozen=True, slots=True)
class PredicateDeclaration:
    """تصريحُ محمول: رتبتُه وجنسُ ترخيصها ومواضعُ حججه ودورُه."""

    predicate_id: str
    arity: int
    arity_license_name: str
    role_site: RoleSiteDeclaration | None
    slots: tuple[SlotDeclaration, ...]

    def __post_init__(self) -> None:
        _require_text(self.predicate_id, "مُعرِّفُ المحمول المُصرَّح به")
        if type(self.arity) is not int:
            raise TypeError("رتبةُ المحمول عددٌ صحيح")
        _require_text(self.arity_license_name, "اسمُ جنس ترخيص الرتبة")
        if self.role_site is not None and not isinstance(
            self.role_site, RoleSiteDeclaration
        ):
            raise TypeError("موضعُ دور المحمول من نوعه أو غائبٌ مُصرَّحٌ بغيابه")
        if not isinstance(self.slots, tuple):
            raise TypeError("مواضعُ الحجج مجموعةٌ مُصرَّحٌ بها")

    def as_canonical_content(self) -> dict[str, object]:
        """محتوى التصريح للبصمة."""

        return {
            "predicate_id": self.predicate_id,
            "arity": self.arity,
            "arity_license": self.arity_license_name,
            "role_site": (
                None
                if self.role_site is None
                else self.role_site.as_canonical_content()
            ),
            "slots": [slot.as_canonical_content() for slot in self.slots],
        }


@dataclass(frozen=True, slots=True)
class AnchorDeclaration:
    """تصريحُ مرساةِ طرف: دورُها وشرطُ هويّتها، وكلٌّ منهما يُسمّي أصلَه."""

    anchor_id: str
    role_site: RoleSiteDeclaration | None
    condition_site: ConditionSiteDeclaration | None

    def __post_init__(self) -> None:
        _require_text(self.anchor_id, "مُعرِّفُ المرساة المُصرَّح بها")
        if self.role_site is not None and not isinstance(
            self.role_site, RoleSiteDeclaration
        ):
            raise TypeError("موضعُ دور المرساة من نوعه أو غائبٌ مُصرَّحٌ بغيابه")
        if self.condition_site is not None and not isinstance(
            self.condition_site, ConditionSiteDeclaration
        ):
            raise TypeError("موضعُ شرط المرساة من نوعه أو غائبٌ مُصرَّحٌ بغيابه")

    def as_canonical_content(self) -> dict[str, object]:
        """محتوى التصريح للبصمة."""

        return {
            "anchor_id": self.anchor_id,
            "role_site": (
                None
                if self.role_site is None
                else self.role_site.as_canonical_content()
            ),
            "condition_site": (
                None
                if self.condition_site is None
                else self.condition_site.as_canonical_content()
            ),
        }


@dataclass(frozen=True, slots=True)
class NisbahDeclaration:
    """تصريحُ النسبة؛ وبصمتُها المُعلَنةُ دعوًى **اختياريّة** عن ناتجٍ لم يُنشَأ بعد."""

    nisbah_id: str
    declared_content_id: str | None
    predicate: PredicateDeclaration
    anchors: tuple[AnchorDeclaration, ...]

    def __post_init__(self) -> None:
        _require_text(self.nisbah_id, "مُعرِّفُ النسبة المُصرَّح بها")
        _require_optional_text(self.declared_content_id, "البصمةُ المُعلَنة للنسبة")
        if not isinstance(self.predicate, PredicateDeclaration):
            raise TypeError("محمولُ النسبة تصريحٌ من نوعه")
        if not isinstance(self.anchors, tuple):
            raise TypeError("مراسي النسبة مجموعةٌ مُصرَّحٌ بها")

    def as_canonical_content(self) -> dict[str, object]:
        """محتوى التصريح للبصمة."""

        return {
            "nisbah_id": self.nisbah_id,
            "declared_content_id": self.declared_content_id,
            "predicate": self.predicate.as_canonical_content(),
            "anchors": [anchor.as_canonical_content() for anchor in self.anchors],
        }


@dataclass(frozen=True, slots=True)
class CaseDeclaration:
    """وثيقةُ حالةٍ كاملة؛ تصريحٌ مرشَّحٌ يُعاد منه الاشتقاق ولا يُقرَأ سلطةً."""

    schema: str
    nisbah_schema: str
    prior_bases: tuple[PriorBaseDeclaration, ...]
    general_ontologies: tuple[GeneralOntologyDeclaration, ...]
    linguistic_ontologies: tuple[LinguisticOntologyDeclaration, ...]
    lineage: LineageDeclaration
    nisbah: NisbahDeclaration
    unresolved_requirements: tuple[UnresolvedRequirement, ...]

    def __post_init__(self) -> None:
        _require_text(self.schema, "اسمُ عقد الوثيقة")
        _require_text(self.nisbah_schema, "اسمُ مخطَّط النسبة")
        for value, label in (
            (self.prior_bases, "القواعدُ السابقة"),
            (self.general_ontologies, "الأنطولوجيات العامّة"),
            (self.linguistic_ontologies, "الأنطولوجيات اللغويّة"),
            (self.unresolved_requirements, "المطالبُ غيرُ المحسومة"),
        ):
            if not isinstance(value, tuple):
                raise TypeError(f"{label} مجموعةٌ مُصرَّحٌ بها")
        if not isinstance(self.lineage, LineageDeclaration):
            raise TypeError("سلسلةُ الوثيقة تصريحٌ من نوعه")
        if not isinstance(self.nisbah, NisbahDeclaration):
            raise TypeError("نسبةُ الوثيقة تصريحٌ من نوعه")

    def as_canonical_content(self) -> dict[str, object]:
        """وثيقةُ التصريح كاملةً؛ وهي نفسُها صورةُ `JSON` المحفوظة."""

        return {
            "schema": self.schema,
            "nisbah_schema": self.nisbah_schema,
            "prior_bases": [base.as_canonical_content() for base in self.prior_bases],
            "general_ontologies": [
                general.as_canonical_content() for general in self.general_ontologies
            ],
            "linguistic_ontologies": [
                linguistic.as_canonical_content()
                for linguistic in self.linguistic_ontologies
            ],
            "lineage": self.lineage.as_canonical_content(),
            "nisbah": self.nisbah.as_canonical_content(),
            "unresolved_requirements": [
                requirement.as_canonical_content()
                for requirement in self.unresolved_requirements
            ],
        }

    @property
    def input_digest(self) -> str:
        """بصمةُ التصريح؛ وهي هويّةُ المدخل في الأثر وفي إعادة التشغيل."""

        return canonical_digest(canonical_bytes(self.as_canonical_content()))

    def requirement_for(
        self, required_authority: object, subject_id: str
    ) -> UnresolvedRequirement | None:
        """المطلبُ المُصرَّحُ به لموضوعٍ بعينه؛ والغيابُ `None` يُقرَأ غيابًا لا رخصة."""

        for requirement in self.unresolved_requirements:
            if (
                requirement.required_authority is required_authority
                and requirement.subject_id == subject_id
            ):
                return requirement
        return None


_AUTHORITATIVE_TYPE_MARKERS: Final[tuple[str, ...]] = (
    "PriorConditionRef",
    "LicensedRoleRefV3",
    "ExistenceLineageRef",
    "ReferencedFunctionalLicense",
    "AnchoredNisbahSignatureV3",
    "derivation_witness",
)

_DECLARING_TYPES: Final[tuple[type, ...]] = (
    PriorConditionDeclaration,
    PriorBaseDeclaration,
    CandidateDeclaration,
    GeneralOntologyDeclaration,
    LicenseDeclaration,
    LinguisticOntologyDeclaration,
    LineageDeclaration,
    RoleSiteDeclaration,
    ConditionSiteDeclaration,
    SlotDeclaration,
    PredicateDeclaration,
    AnchorDeclaration,
    NisbahDeclaration,
    CaseDeclaration,
)


def _refuse_an_authoritative_field_in_a_declaration() -> None:
    """لا حقلَ سلطويٍّ في التصريح؛ فخمولُه مفحوصٌ على الأنواع لا على النيّة."""

    for owner in _DECLARING_TYPES:
        for owner_field in fields(owner):
            annotation = str(owner_field.type)
            for marker in _AUTHORITATIVE_TYPE_MARKERS:
                if marker in annotation:  # pragma: no cover - import guard
                    raise RuntimeError(A_DECLARATION_IS_NOT_AN_AUTHORITY)


_refuse_an_authoritative_field_in_a_declaration()
