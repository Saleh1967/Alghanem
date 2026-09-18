"""المطلبُ غير المحسوم: سلطةٌ لازمةٌ لم تثبت، ولم يُختلَق لها مرجع.

    UnresolvedRequirement = (RequiredAuthority, subject_id, UNRESOLVED)

**والدليلُ غيرُ المكتمل ليس بطلانَ إدخال**
(`UnresolvedEvidenceIsNotInvalidInput`): حقلٌ مطلوبٌ غائبٌ من الوثيقة عجزٌ عن
تكوين القضيّة، أمّا موضعٌ يُصرِّح قانونيًّا بأنّ سلطتَه لم تُحسَم بعد فقضيّةٌ
صحيحةُ التكوين دليلُها ناقص. والفرقُ بينهما هو الفرقُ بين «لا نعرف ما طُلِب»
و«نعرف ما طُلِب ولا نملك رخصته بعد».

**والمطلبُ غيرُ المحسوم ليس مرجعًا مُزوَّرًا**
(`AnUnresolvedRequirementIsNotAForgedReference`): هذا النوعُ لا سلطةَ له،
ولا يُقرَأ `PriorConditionRef` ولا `LicensedRoleRefV3`، ولا يحمل نصًّا حرًّا
يفسّر سببَ التأجيل؛ فالتعليلُ النثريُّ بابٌ يدخل منه المعنى المخترَع.

تسجيلٌ لا سلطة: لا ولادةَ ولا حكمَ ولادةٍ ولا تجميدَ `E0`.
"""

from __future__ import annotations

from dataclasses import dataclass, fields
from enum import Enum
from typing import Final

__all__ = [
    "AN_UNRESOLVED_REQUIREMENT_IS_NOT_A_FORGED_REFERENCE",
    "UNRESOLVED_EVIDENCE_IS_NOT_INVALID_INPUT",
    "RequiredAuthority",
    "RequirementStanding",
    "UnresolvedRequirement",
]


UNRESOLVED_EVIDENCE_IS_NOT_INVALID_INPUT: Final[str] = (
    "الدليلُ غيرُ المكتمل ليس بطلانَ إدخال: الحقلُ المطلوبُ الغائبُ يمنع تكوينَ "
    "القضيّة، والتصريحُ بأنّ سلطةً لازمةً لم تُحسَم قضيّةٌ صحيحةُ التكوين "
    "دليلُها ناقص"
)

AN_UNRESOLVED_REQUIREMENT_IS_NOT_A_FORGED_REFERENCE: Final[str] = (
    "المطلبُ غيرُ المحسوم ليس مرجعًا مُزوَّرًا: مفردةٌ مغلقةٌ بلا سلطةٍ ولا نصٍّ "
    "حرّ؛ ومرجعٌ يُصطنَع ليسدّ فراغًا يُحوِّل النقصَ المُعلَن إلى رخصةٍ لم تُمنَح"
)


class RequiredAuthority(Enum):
    """أجناسُ السلطة التي قد تبقى غيرَ محسومة؛ مفردةٌ مغلقة."""

    PRIOR_CONDITION_REFERENCE = "prior_condition_reference"
    ROLE_LICENSE = "role_license"
    GENERAL_ONTOLOGY_FOUNDATION = "general_ontology_foundation"
    LINGUISTIC_ONTOLOGY_FOUNDATION = "linguistic_ontology_foundation"
    EXISTENCE_LINEAGE = "existence_lineage"


REQUIRED_AUTHORITY_NAMES: Final[tuple[str, ...]] = tuple(
    authority.value for authority in RequiredAuthority
)
"""أسماءُ الأجناس مُشتَقّةٌ من المفردة نفسِها؛ ولا نسخةَ ثانيةً تنحرف عنها."""


class RequirementStanding(Enum):
    """منزلةُ المطلب؛ وليس في هذا المستوى إلّا عدمُ الحسم مُصرَّحًا به."""

    UNRESOLVED = "unresolved"


@dataclass(frozen=True, slots=True)
class UnresolvedRequirement:
    """سلطةٌ لازمةٌ مُصرَّحٌ بأنّها لم تُحسَم؛ موضوعُها مُسمًّى وجنسُها مغلق."""

    required_authority: RequiredAuthority
    subject_id: str
    standing: RequirementStanding = RequirementStanding.UNRESOLVED

    def __post_init__(self) -> None:
        if not isinstance(self.required_authority, RequiredAuthority):
            raise TypeError(
                "جنسُ السلطة المطلوبة عضوٌ في مفردته المغلقة؛ و"
                + AN_UNRESOLVED_REQUIREMENT_IS_NOT_A_FORGED_REFERENCE
            )
        if not isinstance(self.subject_id, str) or not self.subject_id.strip():
            raise TypeError("موضوعُ المطلب نصٌّ غير فارغ")
        if self.standing is not RequirementStanding.UNRESOLVED:
            raise TypeError("منزلةُ المطلب في هذا المستوى عدمُ الحسم وحدَه")

    def as_canonical_content(self) -> dict[str, object]:
        """محتوى المطلب للبصمة."""

        return {
            "required_authority": self.required_authority.value,
            "subject_id": self.subject_id,
            "standing": self.standing.value,
        }


def _refuse_a_prose_field_in_a_requirement() -> None:
    """لا حقلَ تعليلٍ نثريٍّ في المطلب؛ والتأجيلُ يُسمّى ولا يُفسَّر بنصٍّ حرّ."""

    for owner_field in fields(UnresolvedRequirement):
        lowered = owner_field.name.lower()
        for marker in ("reason", "note", "statement", "description", "prose"):
            if marker in lowered:  # pragma: no cover - import guard
                raise RuntimeError(AN_UNRESOLVED_REQUIREMENT_IS_NOT_A_FORGED_REFERENCE)


_refuse_a_prose_field_in_a_requirement()
