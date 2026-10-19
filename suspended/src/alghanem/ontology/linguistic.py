"""`O_L`: الأنطولوجيا اللغويّة — متى يستطيع الموجودُ أن يعمل طرفًا أو محمولًا.

    OntologicalKind  →  LinguisticFunction        (ترخيصٌ مُعلَّل)
    OntologicalKind  ⊄  LinguisticFunction        (لا احتواءَ أوّليًّا)

**والماهيّةُ غيرُ الوظيفة** (`OntologicalKindIsNotLinguisticRole`، على منوال
`RelationIsNotRepresentation` مستوًى فوق): «الحدث» نوعٌ أنطولوجيّ، و«مرساةُ
حدثٍ داخل نسبة» دورٌ لغويٌّ لذلك الموجود. والفصلُ مفحوصٌ على **أنواع** الحقول
لا على أسمائها: لا حقلَ من نوع المرشَّح الأنطولوجيّ داخل الوظيفة اللغويّة ولا
العكس، فدفنُ أحدهما في الآخر غيرُ قابلٍ للقول لا مرفوضٌ بعد الوقوع.

**والجهةُ ترخيصٌ لا احتواء** (`LicensingIsADirectionNotAContainment`):

    Genus → TermAnchorRole        لا        Genus ⊆ TermAnchor

فالرخصةُ تحمل المرشَّحَ الذي رُخِّص، والوظيفةَ التي رُخِّص لها، وشرطَ الترخيص،
ومصدرَه في `PK_0`؛ ورخصةٌ بلا شرطٍ دعوى احتواءٍ في ثوب ترخيص.

**والأنطولوجيا اللغويّة مبنيّةٌ على بصمة `O_0`** لا على اسمها: رخصةٌ تشير إلى
مرشَّحٍ ليس في الأنطولوجيا القائمة تُرفَض عند الإنشاء، فلا يُرخَّص ما لم يُسجَّل.

**وهذه الحزمةُ لا تُولِّد `Σ_L` ولا تُولَد منه** (`TheAlgebraDoesNotCreateItsObjects`):
لا تستورد من `linguistic/` حرفًا، ولا تكتب صنفًا باسم صنفٍ من أصناف `Σ_L`
السبعة؛ وإعادةُ إسناد `Σ_L` إلى هذه الطبقة خطوةٌ تاليةٌ مؤجَّلةٌ مُصرَّحٌ
بتأجيلها، لا تُقرَأ مُنجَزةً بوجود هذا الملفّ.

تسجيلٌ لا سلطة: لا ولادةَ ولا حكمَ ولادةٍ ولا تجميدَ `E0`.
"""

from __future__ import annotations

from dataclasses import dataclass, fields
from enum import Enum
from typing import Final

from ..canonical_content import canonical_bytes, canonical_digest
from ..prior.conditions import PriorConditionKind, PriorInformationBase
from .general import (
    GeneralOntology,
    OntologicalCandidate,
    OntologicalKind,
)

__all__ = [
    "AN_EVENT_IS_A_KIND_AN_EVENT_ANCHOR_IS_A_ROLE",
    "A_LICENSE_WITHOUT_A_CONDITION_IS_A_CONTAINMENT_CLAIM",
    "LICENSING_IS_A_DIRECTION_NOT_A_CONTAINMENT",
    "LINGUISTIC_FUNCTION_NAMES",
    "ONTOLOGICAL_KIND_IS_NOT_LINGUISTIC_ROLE",
    "THE_ALGEBRA_DOES_NOT_CREATE_ITS_OBJECTS",
    "FunctionalLicense",
    "LinguisticFunction",
    "LinguisticFunctionRef",
    "LinguisticOntology",
    "LinguisticOntologyError",
    "OntologicalCandidateRef",
]


class LinguisticOntologyError(ValueError):
    """رفضٌ عند الإنشاء في الأنطولوجيا اللغويّة؛ لا حملَ على أقرب حالة."""


ONTOLOGICAL_KIND_IS_NOT_LINGUISTIC_ROLE: Final[str] = (
    "ماهيّةُ الموجود غيرُ وظيفته اللغويّة: «الحدث» نوعٌ، و«مرساةُ حدثٍ في نسبة» "
    "دورٌ لذلك الموجود؛ ومن جمعهما في مفردةٍ واحدةٍ خلط ما الشيءُ بما يفعله"
)

LICENSING_IS_A_DIRECTION_NOT_A_CONTAINMENT: Final[str] = (
    "الترخيصُ جهةٌ لا احتواء: `Genus → TermAnchorRole` رخصةٌ مُعلَّلة، و"
    "`Genus ⊆ TermAnchor` مصادرةٌ تجعل الفرعَ أصلًا بلا برهان"
)

A_LICENSE_WITHOUT_A_CONDITION_IS_A_CONTAINMENT_CLAIM: Final[str] = (
    "رخصةٌ بلا شرطٍ دعوى احتواءٍ في ثوب ترخيص: الشرطُ هو ما يجعل الرخصةَ قابلةً "
    "للنقض، ورخصةٌ لا تُنقَض بشيءٍ ليست ترخيصًا بل تسميةً أخرى للاحتواء"
)

AN_EVENT_IS_A_KIND_AN_EVENT_ANCHOR_IS_A_ROLE: Final[str] = (
    "الحدثُ نوعٌ ومرساةُ الحدث دور: النوعُ يُسجَّل في `O_0`، والدورُ يُرخَّص في "
    "`O_L`؛ ومفردةٌ تجمعهما تُدخِل الوظيفةَ في الماهيّة بلا ترخيص"
)

THE_ALGEBRA_DOES_NOT_CREATE_ITS_OBJECTS: Final[str] = (
    "الجبرُ لا يخلق موجوداتِه: `Σ_L` يعمل على ما رخّصته `O_L`، وجبرٌ يُولِّد "
    "أنواعَه يُثبِت ما افترضه ولا يُقيم عليه برهانًا"
)


class LinguisticFunction(Enum):
    """الوظائفُ اللغويّةُ المرشَّحة؛ ما يستطيع الموجودُ أن يؤدّيَه في لغةٍ ما."""

    TERM_ANCHOR_ROLE = "term_anchor_role"
    PREDICATE_ROLE = "predicate_role"
    OPERATOR_ROLE = "operator_role"
    CONSTRAINT_ROLE = "constraint_role"
    UNREAD = "unread"


LINGUISTIC_FUNCTION_NAMES: Final[tuple[str, ...]] = tuple(
    function.value for function in LinguisticFunction
)
"""أسماءُ الوظائف مُشتَقّةٌ من المفردة نفسِها؛ ولا نسخةَ ثانيةً تنحرف عنها."""


def _require_text(value: object, label: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise LinguisticOntologyError(f"{label} نصٌّ غير فارغ")
    return value


@dataclass(frozen=True, slots=True)
class OntologicalCandidateRef:
    """إشارةٌ إلى مرشَّحٍ أنطولوجيٍّ مُسجَّل؛ ماهيّةٌ لا وظيفة، ولا حقلَ دورٍ فيها."""

    candidate_id: str
    kind_name: str

    def __post_init__(self) -> None:
        _require_text(self.candidate_id, "مُعرِّفُ المرشَّح المُشارِ إليه")
        _require_text(self.kind_name, "اسمُ نوع المرشَّح")

    @classmethod
    def of(cls, candidate: OntologicalCandidate) -> OntologicalCandidateRef:
        """اشتقّ الإشارةَ من مرشَّحٍ قائم؛ ولا تُصطنَع من اسمٍ حرّ."""

        if not isinstance(candidate, OntologicalCandidate):
            raise LinguisticOntologyError(
                "الإشارةُ تُشتَقّ من مرشَّحٍ مُسجَّلٍ في `O_0` لا من اسمٍ حرّ"
            )
        return cls(candidate_id=candidate.candidate_id, kind_name=candidate.kind.value)

    def as_canonical_content(self) -> dict[str, object]:
        """محتوى الإشارة للبصمة."""

        return {"candidate_id": self.candidate_id, "kind_name": self.kind_name}


@dataclass(frozen=True, slots=True)
class LinguisticFunctionRef:
    """إشارةٌ إلى وظيفةٍ لغويّة؛ وظيفةٌ لا ماهيّة، ولا حقلَ مرشَّحٍ فيها."""

    function: LinguisticFunction
    read_from: str

    def __post_init__(self) -> None:
        if not isinstance(self.function, LinguisticFunction):
            raise LinguisticOntologyError("الوظيفةُ عضوٌ في مفردتها المغلقة لا نصٌّ حرّ")
        _require_text(self.read_from, "حاملُ قراءة الوظيفة")

    @property
    def is_read(self) -> bool:
        """أقُرِئت الوظيفةُ؟ وغيابُ القراءة لا يُقرَأ غيابَ وظيفة."""

        return self.function is not LinguisticFunction.UNREAD

    def as_canonical_content(self) -> dict[str, object]:
        """محتوى الإشارة للبصمة."""

        return {"function": self.function.value, "read_from": self.read_from}


@dataclass(frozen=True, slots=True)
class FunctionalLicense:
    """رخصةٌ وظيفيّة: موجودٌ مُسجَّلٌ **يستطيع** أن يؤدّيَ وظيفةً، بشرطٍ مُسمًّى."""

    license_id: str
    candidate_ref: OntologicalCandidateRef
    function_ref: LinguisticFunctionRef
    licensing_condition: PriorConditionKind
    condition_statement: str

    def __post_init__(self) -> None:
        _require_text(self.license_id, "مُعرِّفُ الرخصة")
        if not isinstance(self.candidate_ref, OntologicalCandidateRef):
            raise LinguisticOntologyError(ONTOLOGICAL_KIND_IS_NOT_LINGUISTIC_ROLE)
        if not isinstance(self.function_ref, LinguisticFunctionRef):
            raise LinguisticOntologyError(ONTOLOGICAL_KIND_IS_NOT_LINGUISTIC_ROLE)
        if not isinstance(self.licensing_condition, PriorConditionKind):
            raise LinguisticOntologyError(
                "موضعُ الشرط المُرخِّص عضوٌ في مفردة المعلومات السابقة المغلقة"
            )
        if (
            not isinstance(self.condition_statement, str)
            or not self.condition_statement.strip()
        ):
            raise LinguisticOntologyError(
                A_LICENSE_WITHOUT_A_CONDITION_IS_A_CONTAINMENT_CLAIM
            )

    @property
    def is_operative(self) -> bool:
        """أرخصةٌ عاملة؟ رخصةٌ وظيفتُها غيرُ مقروءةٍ مُسجَّلةٌ ولا تُقرَأ عاملة."""

        return self.function_ref.is_read

    def as_canonical_content(self) -> dict[str, object]:
        """محتوى الرخصة للبصمة."""

        return {
            "license_id": self.license_id,
            "candidate_ref": self.candidate_ref.as_canonical_content(),
            "function_ref": self.function_ref.as_canonical_content(),
            "licensing_condition": self.licensing_condition.value,
            "condition_statement": self.condition_statement,
        }


@dataclass(frozen=True, slots=True)
class LinguisticOntology:
    """`O_L`: الرخصُ الوظيفيّة، مبنيّةً على بصمة `O_0` لا على أسماء مرشَّحيها."""

    ontology_id: str
    general_ontology_id: str
    general_content_id: str
    licenses: tuple[FunctionalLicense, ...]

    def __post_init__(self) -> None:
        _require_text(self.ontology_id, "مُعرِّفُ الأنطولوجيا اللغويّة")
        _require_text(self.general_ontology_id, "مُعرِّفُ الأنطولوجيا العامّة")
        _require_text(self.general_content_id, "بصمةُ الأنطولوجيا العامّة")
        if not isinstance(self.licenses, tuple) or not self.licenses:
            raise LinguisticOntologyError("الأنطولوجيا اللغويّةُ رخصةٌ فأكثر")
        for granted in self.licenses:
            if not isinstance(granted, FunctionalLicense):
                raise LinguisticOntologyError("عضوٌ في الرخص خارج نوعه")
        ids = tuple(granted.license_id for granted in self.licenses)
        if len(set(ids)) != len(ids):
            raise LinguisticOntologyError("مُعرِّفُ الرخصة لا يتكرّر؛ والمكرّرُ يُرفَض لا يُطوى")

    @classmethod
    def founded_on(
        cls,
        ontology_id: str,
        general: GeneralOntology,
        licenses: tuple[FunctionalLicense, ...],
    ) -> LinguisticOntology:
        """أسِّس رخصًا على أنطولوجيا قائمة؛ ورخصةٌ لمرشَّحٍ غيرِ مُسجَّلٍ رفضٌ."""

        if not isinstance(general, GeneralOntology):
            raise LinguisticOntologyError(
                "التأسيسُ على أنطولوجيا عامّةٍ قائمةٍ لا على اسمٍ حرّ"
            )
        for granted in licenses:
            if not isinstance(granted, FunctionalLicense):
                raise LinguisticOntologyError("عضوٌ في الرخص خارج نوعه")
            candidate = general.candidate(granted.candidate_ref.candidate_id)
            if candidate.kind.value != granted.candidate_ref.kind_name:
                raise LinguisticOntologyError(
                    "نوعُ المرشَّح في الرخصة يخالف نوعَه في `O_0`؛ ورخصةٌ على "
                    "نوعٍ لم يُسجَّل ترخيصٌ لغير موجود"
                )
        return cls(
            ontology_id=ontology_id,
            general_ontology_id=general.ontology_id,
            general_content_id=general.content_id,
            licenses=licenses,
        )

    def licenses_for(
        self, function: LinguisticFunction
    ) -> tuple[FunctionalLicense, ...]:
        """الرخصُ الممنوحةُ لوظيفةٍ بعينها؛ والفراغُ فراغٌ لا يُقرَأ منعًا."""

        if not isinstance(function, LinguisticFunction):
            raise LinguisticOntologyError("الوظيفةُ عضوٌ في مفردتها المغلقة")
        return tuple(
            granted
            for granted in self.licenses
            if granted.function_ref.function is function
        )

    def as_canonical_content(self) -> dict[str, object]:
        """محتوى الأنطولوجيا اللغويّة للبصمة."""

        return {
            "ontology_id": self.ontology_id,
            "general_ontology_id": self.general_ontology_id,
            "general_content_id": self.general_content_id,
            "licenses": [
                granted.as_canonical_content()
                for granted in sorted(self.licenses, key=lambda item: item.license_id)
            ],
        }

    @property
    def content_id(self) -> str:
        """بصمةُ الأنطولوجيا اللغويّة؛ وجبرٌ يُسنَد إلى بصمةٍ غيرِها جبرُ غيرِها."""

        return canonical_digest(canonical_bytes(self.as_canonical_content()))


def _refuse_a_buried_component() -> None:
    """افحص الفصلَ على **أنواع** الحقول لا على أسمائها، كما في مستوى النسبة."""

    pairs = (
        (OntologicalCandidateRef, LinguisticFunctionRef),
        (LinguisticFunctionRef, OntologicalCandidateRef),
    )
    for declaring, forbidden in pairs:
        for field in fields(declaring):
            annotation = field.type
            name = (
                annotation.__name__ if isinstance(annotation, type) else str(annotation)
            )
            if forbidden.__name__ in name:
                raise RuntimeError(ONTOLOGICAL_KIND_IS_NOT_LINGUISTIC_ROLE)
            if isinstance(annotation, type) and issubclass(annotation, forbidden):
                raise RuntimeError(ONTOLOGICAL_KIND_IS_NOT_LINGUISTIC_ROLE)


def _refuse_a_kind_that_is_also_a_function() -> None:
    """لا اسمَ مشتركًا بين مفردة الأنواع ومفردة الوظائف سوى عضو الجهل المُصرَّح."""

    kinds = {kind.value for kind in OntologicalKind}
    functions = {function.value for function in LinguisticFunction}
    shared = (kinds & functions) - {"unread"}
    if shared:
        raise RuntimeError(AN_EVENT_IS_A_KIND_AN_EVENT_ANCHOR_IS_A_ROLE)


def _refuse_an_unconditioned_prior_reference() -> None:
    """رخصةٌ تُسمّي موضعَ شرطٍ خارجَ مفردة `PK_0` رخصةٌ بلا مصدرِ ترخيص."""

    if not isinstance(
        PriorConditionKind.DOMAIN, PriorConditionKind
    ):  # pragma: no cover
        raise RuntimeError(A_LICENSE_WITHOUT_A_CONDITION_IS_A_CONTAINMENT_CLAIM)
    if not hasattr(PriorInformationBase, "condition"):  # pragma: no cover
        raise RuntimeError(A_LICENSE_WITHOUT_A_CONDITION_IS_A_CONTAINMENT_CLAIM)


_refuse_a_buried_component()
_refuse_a_kind_that_is_also_a_function()
_refuse_an_unconditioned_prior_reference()
