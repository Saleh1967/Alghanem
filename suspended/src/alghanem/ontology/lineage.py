"""سلسلةُ الأصل الوجوديّة: `PK_0 → O_0 → O_L²` مرجعًا واحدًا مبصومًا.

    ExistenceLineageRef = (BaseId, BaseDigest,
                           GeneralId, GeneralDigest,
                           LinguisticId, LinguisticDigest)

**واتّحادُ الأنطولوجيا ليس اتّحادَ الأصل** (`OriginUnityIsNotOntologyUnity`):
`v2` تشدّ النسبةَ إلى بصمة `O_L` واحدة، فتمنع خلطَ رخصتين من أنطولوجيتين. لكنّ
رخصةً من مسارٍ وجوديٍّ وشرطًا من مسارٍ آخر يمرّان معًا، لأنّ شرطَ الهويّة يأتي
من قاعدةٍ سابقةٍ ولا شيءَ يوجب أن تكون هي القاعدةَ التي تأسّست عليها الأنطولوجيا
التي أصدرت رخصةَ الدور. فلا يُغلَق محورُ الأصل إلّا باتّحاد السلسلة كلِّها.

**والسلسلةُ تُشتَقّ ولا تُكتَب** (`AReferenceIsDerivedNotConstructed`): ستّةُ
حقولٍ صحيحةٍ شكلًا لا تُثبِت أنّها اشتُقّت من مستوياتٍ قائمة، فلا يُصدِر النداءُ
المباشرُ سلسلةً أصلًا؛ ومع ذلك يبقى `verify_against` موضعَ إعادةِ اشتقاقٍ من
المستويات الحيّة.

**والسلسلةُ تُمَدّ ولا تُعدَّل** (`ALineageIsNotEditedItIsExtended`): متى قام
مستوًى فوق `O_L²` فامتدادُه نوعٌ جديدٌ يُبنى على بصمة هذه السلسلة، لا حقلٌ
يُضاف إليها بأثرٍ رجعيّ؛ فتعديلُ سلسلةٍ مُسجَّلةٍ يمحو ما كانت تشهد به.

تسجيلٌ لا سلطة: لا ولادةَ ولا حكمَ ولادةٍ ولا تجميدَ `E0`.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Final

from ..canonical_content import canonical_bytes, canonical_digest
from .general import GeneralOntology
from .linguistic_v2 import LinguisticOntologyV2

__all__ = [
    "A_LINEAGE_IS_NOT_EDITED_IT_IS_EXTENDED",
    "A_REFERENCE_IS_DERIVED_NOT_CONSTRUCTED",
    "ORIGIN_UNITY_IS_NOT_ONTOLOGY_UNITY",
    "ExistenceLineageError",
    "ExistenceLineageRef",
]


class ExistenceLineageError(ValueError):
    """رفضٌ عند اشتقاق سلسلة الأصل؛ لا حملَ على أقرب حالةٍ مقبولة."""


ORIGIN_UNITY_IS_NOT_ONTOLOGY_UNITY: Final[str] = (
    "اتّحادُ الأنطولوجيا ليس اتّحادَ الأصل: بصمةُ `O_L` وحدَها تمنع خلطَ رخصتين "
    "من أنطولوجيتين، ولا تمنع رخصةً من مسارٍ وجوديٍّ وشرطًا من مسارٍ آخر؛ "
    "وإغلاقُ المحور اتّحادُ السلسلة من `PK_0` إلى `O_0` إلى `O_L²`"
)

A_REFERENCE_IS_DERIVED_NOT_CONSTRUCTED: Final[str] = (
    "السلسلةُ تُشتَقّ ولا تُكتَب: ستّةُ حقولٍ صحيحةٍ شكلًا لا تُثبِت أنّها "
    "اشتُقّت من مستوياتٍ قائمة، فالنداءُ المباشرُ لا يُصدِر سلسلةً أصلًا"
)

A_LINEAGE_IS_NOT_EDITED_IT_IS_EXTENDED: Final[str] = (
    "السلسلةُ تُمَدّ ولا تُعدَّل: مستوًى يقوم فوقها يمتدّ بنوعٍ جديدٍ مبنيٍّ على "
    "بصمتها، وحقلٌ يُضاف إليها بأثرٍ رجعيٍّ يمحو ما كانت تشهد به"
)


class _LineageWitness:
    """شاهدُ اشتقاقٍ واحدٌ لا يُنشَأ ثانيةً؛ يُوصَد بابُه عند تمام الاستيراد."""

    __slots__ = ()

    def __init__(self) -> None:
        if _WITNESS_IS_ISSUED:
            raise ExistenceLineageError(A_REFERENCE_IS_DERIVED_NOT_CONSTRUCTED)


_WITNESS_IS_ISSUED: bool = False
_LINEAGE_WITNESS: Final[_LineageWitness] = _LineageWitness()
_WITNESS_IS_ISSUED = True


def _require_text(value: object, label: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise ExistenceLineageError(f"{label} نصٌّ غير فارغ")
    return value


@dataclass(frozen=True, slots=True)
class ExistenceLineageRef:
    """السلسلةُ الوجوديّةُ الثلاثيّة: قاعدةٌ سابقة، فأنطولوجيا عامّة، فلغويّة."""

    base_id: str
    base_content_id: str
    general_ontology_id: str
    general_content_id: str
    linguistic_ontology_id: str
    linguistic_content_id: str
    derivation_witness: object = field(default=None, repr=False, compare=False)

    def __post_init__(self) -> None:
        if self.derivation_witness is not _LINEAGE_WITNESS:
            raise ExistenceLineageError(A_REFERENCE_IS_DERIVED_NOT_CONSTRUCTED)
        for value, label in (
            (self.base_id, "مُعرِّفُ القاعدة السابقة"),
            (self.base_content_id, "بصمةُ القاعدة السابقة"),
            (self.general_ontology_id, "مُعرِّفُ الأنطولوجيا العامّة"),
            (self.general_content_id, "بصمةُ الأنطولوجيا العامّة"),
            (self.linguistic_ontology_id, "مُعرِّفُ الأنطولوجيا اللغويّة"),
            (self.linguistic_content_id, "بصمةُ الأنطولوجيا اللغويّة"),
        ):
            _require_text(value, label)

    @classmethod
    def of(
        cls, general: GeneralOntology, linguistic: LinguisticOntologyV2
    ) -> ExistenceLineageRef:
        """اشتقّ السلسلةَ من مستويين قائمين؛ وانفصالُ أحدهما عن الآخر رفضٌ."""

        if not isinstance(general, GeneralOntology):
            raise ExistenceLineageError(
                "السلسلةُ تُشتَقّ من أنطولوجيا عامّةٍ قائمةٍ لا من اسمٍ حرّ"
            )
        if not isinstance(linguistic, LinguisticOntologyV2):
            raise ExistenceLineageError(
                "السلسلةُ تُشتَقّ من أنطولوجيا لغويّةٍ قائمةٍ لا من اسمٍ حرّ"
            )
        broken: list[str] = []
        if linguistic.general_ontology_id != general.ontology_id:
            broken.append("مُعرِّفُ الأنطولوجيا العامّة")
        if linguistic.general_content_id != general.content_id:
            broken.append("بصمةُ الأنطولوجيا العامّة")
        if linguistic.prior_base_ref != general.prior_base_ref:
            broken.append("مرجعُ القاعدة السابقة")
        if broken:
            raise ExistenceLineageError(
                "أنطولوجيا لغويّةٌ مؤسَّسةٌ على غير هذه العامّة لا تصل سلسلةً؛ "
                "والمواضعُ المنقطعة: " + "، ".join(broken)
            )
        return cls(
            base_id=general.prior_base_ref.base_id,
            base_content_id=general.prior_base_ref.content_id,
            general_ontology_id=general.ontology_id,
            general_content_id=general.content_id,
            linguistic_ontology_id=linguistic.ontology_id,
            linguistic_content_id=linguistic.content_id,
            derivation_witness=_LINEAGE_WITNESS,
        )

    def verify_against(
        self, general: GeneralOntology, linguistic: LinguisticOntologyV2
    ) -> bool:
        """أعِد اشتقاقَ السلسلة من المستويات الحيّة وقارنها حقلًا حقلًا."""

        try:
            rederived = ExistenceLineageRef.of(general, linguistic)
        except ExistenceLineageError:
            return False
        return rederived == self

    def as_canonical_content(self) -> dict[str, object]:
        """محتوى السلسلة للبصمة؛ وشاهدُ الاشتقاق ليس محتوًى يُنقَل."""

        return {
            "base_id": self.base_id,
            "base_content_id": self.base_content_id,
            "general_ontology_id": self.general_ontology_id,
            "general_content_id": self.general_content_id,
            "linguistic_ontology_id": self.linguistic_ontology_id,
            "linguistic_content_id": self.linguistic_content_id,
        }

    @property
    def content_id(self) -> str:
        """بصمةُ السلسلة؛ وسلسلتان بمستوياتٍ مختلفةٍ بصمتاهما مختلفتان."""

        return canonical_digest(canonical_bytes(self.as_canonical_content()))


def _refuse_a_second_witness() -> None:  # pragma: no cover - import guard
    try:
        _LineageWitness()
    except ExistenceLineageError:
        return
    raise RuntimeError(A_REFERENCE_IS_DERIVED_NOT_CONSTRUCTED)


_refuse_a_second_witness()
