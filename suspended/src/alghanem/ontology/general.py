"""`O_0`: الأنطولوجيا العامّة — مرشَّحو الأنواع، وكلُّ مرشَّحٍ بضرورةٍ وعدمِ اختزال.

    OntologicalCandidate = Necessity + Irreducibility

**والمرشَّحُ ليس نمطًا مولودًا** (`AnOntologicalCandidateIsNotABornKind`، مُعادُ
الاستعمال لا مُعادُ الاختراع على منهج `CandidateBranchIsNotABornKind`): تسميةُ
الشيء والهويّة والصفة والحالة والحدث والعلاقة والدور والكمّيّة والإحالة والتحوّل
والشرط والمانع والأثر والبقيّة تسجيلُ ما يُختبَر، لا ولادةُ نمطٍ سبقت تجربتَه.

**والشرطانِ مجتمعانِ لا أحدُهما**: دعوى الضرورة تقول لماذا لا يُستغنى عن
المرشَّح، ودعوى عدمِ الاختزال تقول إلى أيّ مرشَّحٍ آخرَ لا يُرَدّ. ومرشَّحٌ
بأحدهما وحدَه مرشَّحٌ بلا ما يُسقِطه، فيُرفَض عند الإنشاء.

**والأنطولوجيا مبنيّةٌ على بصمة `PK_0`** لا على اسمها (على منهج بناء `Σ_L` على
بصمة `Σ_M`): أنطولوجيا تشير إلى معلوماتٍ سابقةٍ غيرِ القائمة أنطولوجيا قاعدةٍ
أخرى، وتُرفَض عند الإنشاء. وكلُّ مرشَّحٍ يُسمّي موضعَ الشرط الذي رخّص النظرَ
فيه، فلا يُولَد نوعٌ خارجَ مجال الإمكان المُسجَّل.

**ولا اسمَ لغويٍّ ولا عربيٍّ هنا** (`NoLinguisticRoleInTheGeneralOntology`): هذا
المستوى يقول ما الموجود، ولا يقول ما وظيفتُه في اللغة؛ وتلك مسألةُ الأنطولوجيا
اللغويّة، والفصلُ بينهما هو `OntologicalKind ≠ LinguisticRole`.

تسجيلٌ لا سلطة: لا ولادةَ ولا حكمَ ولادةٍ ولا تجميدَ `E0`، ولا استيرادَ من
`metaalgebra/` ولا `linguistic/` ولا `arabic/` ولا `kernel/`.
"""

from __future__ import annotations

from dataclasses import dataclass, fields
from enum import Enum
from typing import Final

from ..canonical_content import canonical_bytes, canonical_digest
from ..prior.conditions import (
    PriorConditionKind,
    PriorInformationBase,
    PriorInformationError,
)

__all__ = [
    "AN_ONTOLOGICAL_CANDIDATE_IS_NOT_A_BORN_KIND",
    "NECESSITY_AND_IRREDUCIBILITY_ARE_BOTH_REQUIRED",
    "NO_LINGUISTIC_ROLE_IN_THE_GENERAL_ONTOLOGY",
    "ONTOLOGICAL_CANDIDATE_NAMES",
    "GeneralOntology",
    "OntologicalCandidate",
    "OntologicalKind",
    "OntologyError",
    "PriorBaseRef",
]


class OntologyError(ValueError):
    """رفضٌ عند الإنشاء في الأنطولوجيا العامّة؛ لا حملَ على أقرب حالة."""


AN_ONTOLOGICAL_CANDIDATE_IS_NOT_A_BORN_KIND: Final[str] = (
    "المرشَّحُ الأنطولوجيُّ ليس نمطًا مولودًا: تسميتُه تسجيلُ ما يُختبَر، ولا "
    "تُقرَأ ولادةً سبقت تجربتَها ولا حكمًا صدر في حقّه"
)

NECESSITY_AND_IRREDUCIBILITY_ARE_BOTH_REQUIRED: Final[str] = (
    "المرشَّحُ ضرورةٌ وعدمُ اختزالٍ معًا: من قال لماذا يلزم ولم يقل إلى ماذا لا "
    "يُرَدّ أدخل مرشَّحًا يُغني عنه غيرُه، ومن عكس أدخل مرشَّحًا لا حاجةَ به"
)

NO_LINGUISTIC_ROLE_IN_THE_GENERAL_ONTOLOGY: Final[str] = (
    "لا دورَ لغويًّا في الأنطولوجيا العامّة: هذا المستوى يقول ما الموجود، "
    "ووظيفتُه في اللغة مسألةُ المستوى الذي فوقه؛ وجمعُهما خلطُ الماهيّة بالوظيفة"
)


class OntologicalKind(Enum):
    """مرشَّحو الأنواع العامّة؛ مُعلَنون لا مولودون، وفيهم عضوُ جهلٍ مُصرَّح."""

    THING = "thing"
    IDENTITY = "identity"
    ATTRIBUTE = "attribute"
    STATE = "state"
    EVENT = "event"
    RELATION = "relation"
    ROLE = "role"
    QUANTITY = "quantity"
    REFERENCE = "reference"
    TRANSFORMATION = "transformation"
    CONDITION = "condition"
    PREVENTER = "preventer"
    TRACE = "trace"
    REMAINDER = "remainder"
    UNREAD = "unread"


ONTOLOGICAL_CANDIDATE_NAMES: Final[tuple[str, ...]] = tuple(
    kind.value for kind in OntologicalKind
)
"""أسماءُ المرشَّحين مُشتَقّةٌ من المفردة نفسِها؛ ولا نسخةَ ثانيةً تنحرف عنها."""


def _require_text(value: object, label: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise OntologyError(f"{label} نصٌّ غير فارغ")
    return value


@dataclass(frozen=True, slots=True)
class PriorBaseRef:
    """إشارةٌ مبصومةٌ إلى قاعدة المعلومات السابقة التي رخّصت هذه الأنطولوجيا."""

    base_id: str
    content_id: str

    def __post_init__(self) -> None:
        _require_text(self.base_id, "مُعرِّفُ القاعدة المُشارِ إليها")
        _require_text(self.content_id, "بصمةُ القاعدة المُشارِ إليها")

    @classmethod
    def of(cls, base: PriorInformationBase) -> PriorBaseRef:
        """اشتقّ الإشارةَ من القاعدة نفسِها؛ ولا تُكتَب البصمةُ بجانبها يدويًّا."""

        if not isinstance(base, PriorInformationBase):
            raise OntologyError("الإشارةُ تُشتَقّ من قاعدةٍ قائمةٍ لا من اسمٍ حرّ")
        return cls(base_id=base.base_id, content_id=base.content_id)

    def as_canonical_content(self) -> dict[str, object]:
        """محتوى الإشارة للبصمة."""

        return {"base_id": self.base_id, "content_id": self.content_id}


@dataclass(frozen=True, slots=True)
class OntologicalCandidate:
    """مرشَّحُ نوعٍ عامّ: ضرورتُه، وعدمُ اختزاله، وموضعُ الشرط الذي رخّص النظرَ فيه."""

    candidate_id: str
    kind: OntologicalKind
    necessity_claim: str
    irreducibility_claim: str
    licensing_condition: PriorConditionKind

    def __post_init__(self) -> None:
        _require_text(self.candidate_id, "مُعرِّفُ المرشَّح")
        if not isinstance(self.kind, OntologicalKind):
            raise OntologyError(
                "نوعُ المرشَّح عضوٌ في مفردته المغلقة؛ و"
                + AN_ONTOLOGICAL_CANDIDATE_IS_NOT_A_BORN_KIND
            )
        for value, label in (
            (self.necessity_claim, "دعوى ضرورة المرشَّح"),
            (self.irreducibility_claim, "دعوى عدم اختزال المرشَّح"),
        ):
            if not isinstance(value, str) or not value.strip():
                raise OntologyError(
                    f"{label} نصٌّ غير فارغ؛ و"
                    + NECESSITY_AND_IRREDUCIBILITY_ARE_BOTH_REQUIRED
                )
        if not isinstance(self.licensing_condition, PriorConditionKind):
            raise OntologyError(
                "موضعُ الشرط المُرخِّص عضوٌ في مفردة المعلومات السابقة المغلقة"
            )

    def as_canonical_content(self) -> dict[str, object]:
        """محتوى المرشَّح للبصمة."""

        return {
            "candidate_id": self.candidate_id,
            "kind": self.kind.value,
            "necessity_claim": self.necessity_claim,
            "irreducibility_claim": self.irreducibility_claim,
            "licensing_condition": self.licensing_condition.value,
        }


@dataclass(frozen=True, slots=True)
class GeneralOntology:
    """`O_0`: مرشَّحو الأنواع، مبنيّين على بصمة قاعدةٍ سابقةٍ صالحةٍ للتأسيس."""

    ontology_id: str
    prior_base_ref: PriorBaseRef
    candidates: tuple[OntologicalCandidate, ...]

    def __post_init__(self) -> None:
        _require_text(self.ontology_id, "مُعرِّفُ الأنطولوجيا")
        if not isinstance(self.prior_base_ref, PriorBaseRef):
            raise OntologyError(
                "الأنطولوجيا مبنيّةٌ على قاعدةٍ مُسمّاةٍ مبصومة لا على اسمٍ حرّ"
            )
        if not isinstance(self.candidates, tuple) or not self.candidates:
            raise OntologyError("الأنطولوجيا مرشَّحٌ فأكثر")
        for candidate in self.candidates:
            if not isinstance(candidate, OntologicalCandidate):
                raise OntologyError("عضوٌ في المرشَّحين خارج نوعه")
        ids = tuple(candidate.candidate_id for candidate in self.candidates)
        if len(set(ids)) != len(ids):
            raise OntologyError("مُعرِّفُ المرشَّح لا يتكرّر؛ والمكرّرُ يُرفَض لا يُطوى")

    @classmethod
    def founded_on(
        cls,
        ontology_id: str,
        base: PriorInformationBase,
        candidates: tuple[OntologicalCandidate, ...],
    ) -> GeneralOntology:
        """أسِّس أنطولوجيا على قاعدةٍ قائمة؛ وقاعدةٌ غيرُ صالحةٍ للتأسيس رفضٌ."""

        if not isinstance(base, PriorInformationBase):
            raise OntologyError("التأسيسُ على قاعدةٍ قائمةٍ لا على اسمٍ حرّ")
        if not base.is_fit_to_found_an_ontology:
            raise OntologyError(
                "قاعدةٌ فيها شرطٌ غيرُ مُرخَّصٍ لا تؤسِّس أنطولوجيا؛ والشروطُ "
                "غيرُ الصالحة: " + "، ".join(base.unusable_condition_ids)
            )
        for candidate in candidates:
            if not isinstance(candidate, OntologicalCandidate):
                raise OntologyError("عضوٌ في المرشَّحين خارج نوعه")
            try:
                base.condition(candidate.licensing_condition)
            except PriorInformationError as absence:
                raise OntologyError(
                    "مرشَّحٌ يُسمّي موضعَ شرطٍ غيرَ مُسجَّلٍ في القاعدة مرشَّحٌ "
                    "خارجَ مجال الإمكان: " + str(absence)
                ) from absence
        return cls(
            ontology_id=ontology_id,
            prior_base_ref=PriorBaseRef.of(base),
            candidates=candidates,
        )

    def candidate(self, candidate_id: str) -> OntologicalCandidate:
        """المرشَّحُ بمُعرِّفه؛ والغيابُ رفضٌ لا `None` يُقرأ صمتًا."""

        for candidate in self.candidates:
            if candidate.candidate_id == candidate_id:
                return candidate
        raise OntologyError(f"لا مرشَّحَ في `O_0` مُعرِّفُه `{candidate_id}`")

    @property
    def candidate_ids(self) -> tuple[str, ...]:
        """مُعرِّفاتُ المرشَّحين؛ خاصّيّةٌ تُشتَقّ لا حقلٌ يُكتَب."""

        return tuple(candidate.candidate_id for candidate in self.candidates)

    def as_canonical_content(self) -> dict[str, object]:
        """محتوى الأنطولوجيا للبصمة."""

        return {
            "ontology_id": self.ontology_id,
            "prior_base_ref": self.prior_base_ref.as_canonical_content(),
            "candidates": [
                candidate.as_canonical_content()
                for candidate in sorted(
                    self.candidates, key=lambda item: item.candidate_id
                )
            ],
        }

    @property
    def content_id(self) -> str:
        """بصمةُ الأنطولوجيا؛ وأنطولوجيا لغويّةٌ على بصمةٍ غيرِها أنطولوجيا أخرى."""

        return canonical_digest(canonical_bytes(self.as_canonical_content()))


_FORBIDDEN_FIELD_MARKERS: Final[tuple[str, ...]] = (
    "role_ref",
    "linguistic",
    "term_anchor",
    "predicate",
    "nisbah",
    "arabic",
)
"""أسماءٌ لا تظهر حقلًا هنا؛ فالوظيفةُ اللغويّةُ مسألةُ المستوى الذي فوق."""

_DECLARING_TYPES: Final[tuple[type, ...]] = (
    OntologicalCandidate,
    GeneralOntology,
    PriorBaseRef,
)

for _declaring_type in _DECLARING_TYPES:  # pragma: no cover - import guard
    for _field in fields(_declaring_type):
        for _marker in _FORBIDDEN_FIELD_MARKERS:
            if _marker in _field.name.lower():
                raise RuntimeError(NO_LINGUISTIC_ROLE_IN_THE_GENERAL_ONTOLOGY)
