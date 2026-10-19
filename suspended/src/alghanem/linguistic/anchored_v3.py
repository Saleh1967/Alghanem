"""`v3`: النسبةُ المُسنَدةُ إلى سلسلة الأصل، بجانب `v2` لا فوقها.

    v2:  نسبةٌ مشدودةٌ إلى بصمة `O_L`
    v3:  نسبةٌ مشدودةٌ إلى `PK_0 → O_0 → O_L²` كلِّها

**واتّحادُ الأنطولوجيا ليس اتّحادَ الأصل** (`OriginUnityIsNotOntologyUnity`):
في `v2` تُفحَص بصمةُ `O_L` في مراجع الأدوار وحدَها، فتمرّ نسبةٌ دورُها مُرخَّصٌ
من أنطولوجيا تأسّست على قاعدةٍ وشرطُ هويّتها راجعٌ إلى قاعدةٍ أخرى. وهنا تُفحَص
السلسلةُ كلُّها: مرجعُ كلِّ دورٍ على بصمة `O_L²` التي فيها، ومرجعُ كلِّ شرطٍ على
مُعرِّف قاعدتها وبصمتها معًا. والمخالفاتُ تُسمَّى جميعًا ولا يُوقَف عند أوّلها.

**وقراءةُ هويّة `v2` ليست استعمالَ تنفيذها** (`V3StandsBesideV2NotOverIt`): تقرأ
هذه الوحدةُ من `anchored` مخطَّطَ `v2` **هويّةً** لتُثبِت الأبَ الذي امتدّت
عنه، ولا تبني بدوالّ `v2` شيئًا؛ فلو بَنَت بها لصارت دلالتُها متوقّفةً على
تنفيذ القديمة لا على نسبها التاريخيّ. والعقدُ ثلاثيّ: هويّةُ الأب، وهويّةٌ
مُجمَّدةٌ عند إنشاء `v3`، وإعادةُ اشتقاقٍ من الأب الحيّ عند الاستيراد.

**والشرطُ قائمٌ مُسجَّلٌ مُرخَّص، لا «مولود»** (`NoBirthLanguageAtThisStage`): لا
بوّابةَ ولادةٍ في هذه المرحلة، فلا يُوصَف تسجيلٌ بما هو فوق رتبته.

**والمفرداتُ مُعادةُ الاستعمال لا منسوخة**: `ArityLicenseGenus` و
`DEFERRED_ARGUMENT_ROLE_NAMES` من `v1`، و`PriorConditionRef` من `PK_0`.

تسجيلٌ لا سلطة: لا ولادةَ ولا حكمَ ولادةٍ ولا تجميدَ `E0`، ولا مدوّنةَ مُسمّاة.
"""

from __future__ import annotations

from dataclasses import dataclass, field, fields
from typing import Final

from ..canonical_content import canonical_bytes, canonical_digest
from ..ontology.lineage import ORIGIN_UNITY_IS_NOT_ONTOLOGY_UNITY, ExistenceLineageRef
from ..ontology.linguistic import LinguisticFunction
from ..ontology.linguistic_v2 import LinguisticOntologyV2, ReferencedFunctionalLicense
from ..prior.references import PriorConditionRef
from .anchored import ANCHORED_NISBAH_SCHEMA
from .nisbah import (
    ARGUMENT_ROLES_ARE_DEFERRED_TO_THEIR_OWN_LAYER,
    DEFERRED_ARGUMENT_ROLE_NAMES,
    ArityLicenseGenus,
    TermAnchorKind,
)

__all__ = [
    "ANCHORED_V3_NISBAH_SCHEMA",
    "ANCHORED_V3_SCHEMA_VERSION",
    "A_REFERENCE_IS_DERIVED_NOT_CONSTRUCTED",
    "A_ROLE_AND_A_CONDITION_SHARE_ONE_LINEAGE",
    "PARENT_SCHEMA_CONTENT_ID",
    "V3_STANDS_BESIDE_V2_NOT_OVER_IT",
    "AnchoredArgumentSlotV3",
    "AnchoredNisbahSchemaV3",
    "AnchoredNisbahSignatureV3",
    "AnchoredPredicateSignatureV3",
    "AnchoredTermAnchorV3",
    "AnchoredV3Error",
    "BaseSchemaRefV3",
    "LicensedRoleRefV3",
]


class AnchoredV3Error(ValueError):
    """رفضٌ عند الإنشاء في `v3`؛ لا حملَ على أقرب حالةٍ مقبولة."""


V3_STANDS_BESIDE_V2_NOT_OVER_IT: Final[str] = (
    "`v3` بجانب `v2` لا فوقها: `v2` إيداعٌ مُسجَّلٌ مبصومٌ في `G0.ONT-1`، "
    "وحفظُ تاريخ الحجّة يسري عليها كما سرى على `v1`؛ فالامتدادُ يُبنى على "
    "بصمتها ويُثبِتها أبًا، ولا يُعيد كتابتها ولا يبني بدوالّها"
)

A_ROLE_AND_A_CONDITION_SHARE_ONE_LINEAGE: Final[str] = (
    "الدورُ وشرطُه من سلسلةٍ واحدة: رخصةُ دورٍ من أنطولوجيا تأسّست على قاعدةٍ، "
    "وشرطُ هويّةٍ راجعٌ إلى قاعدةٍ أخرى، بناءٌ على أصلين؛ وكلُّ مرجعٍ في النسبة "
    "راجعٌ إلى السلسلة التي شُدّت إليها"
)

A_REFERENCE_IS_DERIVED_NOT_CONSTRUCTED: Final[str] = (
    "المرجعُ يُشتَقّ ولا يُنشَأ (`AReferenceIsDerivedNotConstructed`): السلطةُ شرطٌ في "
    "تكوّن المرجع، لا صفةٌ تُضاف إليه بعد وجوده"
)


ANCHORED_V3_SCHEMA_VERSION: Final[str] = "linguistic-nisbah.schema.v3"
"""إصدارُ الطبقة المشدودةِ إلى السلسلة؛ يقوم بجانب `v2` ولا يحلّ محلَّها."""

PARENT_SCHEMA_CONTENT_ID: Final[str] = ANCHORED_NISBAH_SCHEMA.content_id
"""هويّةُ الأب مقروءةً من `v2` القائمة؛ لا رقمًا مكتوبًا بلا مصدر."""


def _require_text(value: object, label: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise AnchoredV3Error(f"{label} نصٌّ غير فارغ")
    return value


@dataclass(frozen=True, slots=True)
class LicensedRoleRefV3:
    """مرجعُ رخصةٍ وظيفيّةٍ من `O_L²`؛ يحمل بصمةَ أنطولوجيته لا اسمَها وحدَه."""

    license_id: str
    candidate_id: str
    ontology_id: str
    ontology_content_id: str

    def __post_init__(self) -> None:
        _require_text(self.license_id, "مُعرِّفُ الرخصة")
        _require_text(self.candidate_id, "مُعرِّفُ المرشَّح المُرخَّص")
        _require_text(self.ontology_id, "مُعرِّفُ الأنطولوجيا اللغويّة")
        _require_text(self.ontology_content_id, "بصمةُ الأنطولوجيا اللغويّة")

    @classmethod
    def of(
        cls,
        ontology: LinguisticOntologyV2,
        license_id: str,
        function: LinguisticFunction,
    ) -> LicensedRoleRefV3:
        """اشتقّ المرجعَ من رخصةٍ قائمةٍ لوظيفةٍ بعينها؛ وما عداها رفضٌ."""

        if not isinstance(ontology, LinguisticOntologyV2):
            raise AnchoredV3Error("المرجعُ يُشتَقّ من أنطولوجيا لغويّةٍ قائمةٍ لا من اسمٍ حرّ")
        if not isinstance(function, LinguisticFunction):
            raise AnchoredV3Error("الوظيفةُ عضوٌ في مفردتها المغلقة لا نصٌّ حرّ")
        _require_text(license_id, "مُعرِّفُ الرخصة المطلوبة")
        try:
            granted: ReferencedFunctionalLicense = ontology.license(license_id)
        except ValueError as absence:
            raise AnchoredV3Error(
                f"لا رخصةَ في `O_L²` مُعرِّفُها `{license_id}`؛ والغيابُ رفضٌ لا صمت"
            ) from absence
        if granted.function_ref.function is not function:
            raise AnchoredV3Error(
                f"الرخصةُ `{license_id}` مُنِحت لوظيفة "
                f"`{granted.function_ref.function.value}` لا لـ`{function.value}`؛ "
                "ورخصةٌ لوظيفةٍ تُقرَأ لأخرى ترخيصٌ لم يُمنَح"
            )
        if not granted.is_operative:
            raise AnchoredV3Error(
                f"الرخصةُ `{license_id}` وظيفتُها غيرُ مقروءة، ورخصةٌ غيرُ عاملةٍ "
                "لا تُقرَأ عاملةً بالسهو"
            )
        return cls(
            license_id=granted.license_id,
            candidate_id=granted.candidate_ref.candidate_id,
            ontology_id=ontology.ontology_id,
            ontology_content_id=ontology.content_id,
        )

    def as_canonical_content(self) -> dict[str, object]:
        """محتوى المرجع للبصمة."""

        return {
            "license_id": self.license_id,
            "candidate_id": self.candidate_id,
            "ontology_id": self.ontology_id,
            "ontology_content_id": self.ontology_content_id,
        }


@dataclass(frozen=True, slots=True)
class AnchoredTermAnchorV3:
    """مرساةُ طرفٍ: رخصةٌ من `O_L²`، وشرطُ هويّةٍ مرجعُه `PK_0` مبصومًا بقاعدته."""

    anchor_id: str
    role_ref: LicensedRoleRefV3
    identity_condition_ref: PriorConditionRef

    def __post_init__(self) -> None:
        _require_text(self.anchor_id, "مُعرِّفُ المرساة")
        if not isinstance(self.role_ref, LicensedRoleRefV3):
            raise AnchoredV3Error("دورُ المرساة مرجعُ رخصةٍ لا نوعٌ يُكتَب")
        if not isinstance(self.identity_condition_ref, PriorConditionRef):
            raise AnchoredV3Error("شرطُ الهويّة مرجعٌ مبصومٌ إلى `PK_0` لا نصٌّ حرّ")

    def as_canonical_content(self) -> dict[str, object]:
        """محتوى المرساة للبصمة."""

        return {
            "anchor_id": self.anchor_id,
            "role_ref": self.role_ref.as_canonical_content(),
            "identity_condition_ref": (
                self.identity_condition_ref.as_canonical_content()
            ),
        }


@dataclass(frozen=True, slots=True)
class AnchoredArgumentSlotV3:
    """موضعُ حجّةٍ: رتبتُه، وشرطُ ما يقع فيه مرجعًا مبصومًا لا نثرًا حرًّا."""

    slot_id: str
    position: int
    admissibility_condition_ref: PriorConditionRef

    def __post_init__(self) -> None:
        _require_text(self.slot_id, "مُعرِّفُ الموضع")
        if type(self.position) is not int or self.position < 1:
            raise AnchoredV3Error("رتبةُ الموضع عددٌ صحيحٌ موجبٌ يبدأ من واحد")
        if not isinstance(self.admissibility_condition_ref, PriorConditionRef):
            raise AnchoredV3Error("شرطُ الموضع مرجعٌ مبصومٌ إلى `PK_0` لا نصٌّ حرّ")
        lowered = self.slot_id.casefold()
        for deferred in DEFERRED_ARGUMENT_ROLE_NAMES:
            if deferred in lowered:
                raise AnchoredV3Error(ARGUMENT_ROLES_ARE_DEFERRED_TO_THEIR_OWN_LAYER)

    def as_canonical_content(self) -> dict[str, object]:
        """محتوى الموضع للبصمة."""

        return {
            "slot_id": self.slot_id,
            "position": self.position,
            "admissibility_condition_ref": (
                self.admissibility_condition_ref.as_canonical_content()
            ),
        }


@dataclass(frozen=True, slots=True)
class AnchoredPredicateSignatureV3:
    """محمولٌ: رخصةُ محمولٍ من `O_L²`، ورتبةٌ مُرخَّصةٌ بجنسها المُعاد استعمالُه."""

    predicate_id: str
    role_ref: LicensedRoleRefV3
    arity: int
    arity_license: ArityLicenseGenus
    slots: tuple[AnchoredArgumentSlotV3, ...]

    def __post_init__(self) -> None:
        _require_text(self.predicate_id, "مُعرِّفُ المحمول")
        if not isinstance(self.role_ref, LicensedRoleRefV3):
            raise AnchoredV3Error("دورُ المحمول مرجعُ رخصةٍ لا نوعٌ يُكتَب")
        if type(self.arity) is not int or self.arity < 1:
            raise AnchoredV3Error("رتبةُ المحمول عددٌ صحيحٌ موجب")
        if not isinstance(self.arity_license, ArityLicenseGenus):
            raise AnchoredV3Error("ترخيصُ الرتبة عضوٌ في مفردته المغلقة")
        if not self.arity_license.licenses_use:
            raise AnchoredV3Error("رتبةٌ منتزعةٌ من الحالة المستهدَفة لا تُرخِّص استعمالَها")
        if not isinstance(self.slots, tuple) or not self.slots:
            raise AnchoredV3Error("المحمولُ موضعُ حجّةٍ فأكثر")
        for slot in self.slots:
            if not isinstance(slot, AnchoredArgumentSlotV3):
                raise AnchoredV3Error("عضوٌ في مواضع الحجج خارج نوعه")
        if len(self.slots) != self.arity:
            raise AnchoredV3Error(
                "عددُ مواضع الحجج هو الرتبةُ نفسُها؛ ورتبةٌ تخالف مواضعَها "
                "رتبةٌ مكتوبةٌ لا مُشتَقّة"
            )
        positions = tuple(slot.position for slot in self.slots)
        if sorted(positions) != list(range(1, self.arity + 1)):
            raise AnchoredV3Error("مواضعُ الحجج متتابعةٌ من واحدٍ إلى الرتبة بلا ثغرة")
        slot_ids = tuple(slot.slot_id for slot in self.slots)
        if len(set(slot_ids)) != len(slot_ids):
            raise AnchoredV3Error("أسماءُ المواضع بلا تكرار؛ والمكرّرُ يُخفي موضعًا")

    def as_canonical_content(self) -> dict[str, object]:
        """محتوى المحمول للبصمة."""

        return {
            "predicate_id": self.predicate_id,
            "role_ref": self.role_ref.as_canonical_content(),
            "arity": self.arity,
            "arity_license": self.arity_license.value,
            "slots": [slot.as_canonical_content() for slot in self.slots],
        }


@dataclass(frozen=True, slots=True)
class AnchoredNisbahSignatureV3:
    """نسبةٌ مشدودةٌ إلى سلسلةِ أصلٍ واحدة: كلُّ دورٍ وكلُّ شرطٍ راجعٌ إليها."""

    nisbah_id: str
    lineage_ref: ExistenceLineageRef
    predicate: AnchoredPredicateSignatureV3
    anchors: tuple[AnchoredTermAnchorV3, ...]

    def __post_init__(self) -> None:
        _require_text(self.nisbah_id, "مُعرِّفُ النسبة")
        if not isinstance(self.lineage_ref, ExistenceLineageRef):
            raise AnchoredV3Error(ORIGIN_UNITY_IS_NOT_ONTOLOGY_UNITY)
        if not isinstance(self.predicate, AnchoredPredicateSignatureV3):
            raise AnchoredV3Error("النسبةُ محمولٌ واحدٌ بنوعه لا نصٌّ يُسمّيه")
        if not isinstance(self.anchors, tuple):
            raise AnchoredV3Error("مراسي الأطراف مجموعةٌ مُصرَّحٌ بها")
        for anchor in self.anchors:
            if not isinstance(anchor, AnchoredTermAnchorV3):
                raise AnchoredV3Error("عضوٌ في مراسي الأطراف خارج نوعه")
        anchor_ids = tuple(anchor.anchor_id for anchor in self.anchors)
        if len(set(anchor_ids)) != len(anchor_ids):
            raise AnchoredV3Error("أسماءُ المراسي بلا تكرار في النسبة الواحدة")
        if len(self.anchors) > self.predicate.arity:
            raise AnchoredV3Error(
                "مراسي الأطراف لا تزيد على رتبة المحمول؛ وزيادتُها طرفٌ بلا موضع"
            )
        self._refuse_every_foreign_origin()

    def _refuse_every_foreign_origin(self) -> None:
        """اجمع المخالفاتِ كلَّها في محورَي الدور والشرط، ولا تقف عند أوّلها."""

        lineage = self.lineage_ref
        foreign_roles: list[str] = []
        foreign_conditions: list[str] = []
        roles = ((self.predicate.predicate_id, self.predicate.role_ref),) + tuple(
            (anchor.anchor_id, anchor.role_ref) for anchor in self.anchors
        )
        for owner_id, role_ref in roles:
            if (
                role_ref.ontology_content_id != lineage.linguistic_content_id
                or role_ref.ontology_id != lineage.linguistic_ontology_id
            ):
                foreign_roles.append(owner_id)
        conditions = tuple(
            (slot.slot_id, slot.admissibility_condition_ref)
            for slot in self.predicate.slots
        ) + tuple(
            (anchor.anchor_id, anchor.identity_condition_ref) for anchor in self.anchors
        )
        for owner_id, condition_ref in conditions:
            if (
                condition_ref.base_id != lineage.base_id
                or condition_ref.base_content_id != lineage.base_content_id
            ):
                foreign_conditions.append(owner_id)
        complaints: list[str] = []
        if foreign_roles:
            complaints.append(
                "مراجعُ أدوارٍ من أنطولوجيا غيرِ التي في السلسلة: "
                + "، ".join(foreign_roles)
            )
        if foreign_conditions:
            complaints.append(
                "مراجعُ شروطٍ من قاعدةٍ غيرِ التي في السلسلة: "
                + "، ".join(foreign_conditions)
            )
        if complaints:
            raise AnchoredV3Error(
                A_ROLE_AND_A_CONDITION_SHARE_ONE_LINEAGE
                + "؛ و"
                + "؛ و".join(complaints)
            )

    @classmethod
    def in_lineage(
        cls,
        nisbah_id: str,
        lineage: ExistenceLineageRef,
        predicate: AnchoredPredicateSignatureV3,
        anchors: tuple[AnchoredTermAnchorV3, ...],
    ) -> AnchoredNisbahSignatureV3:
        """ابنِ نسبةً على سلسلةٍ مُشتَقّة؛ وسلسلةٌ مكتوبةٌ لا تُصدِر نسبةً أصلًا."""

        return cls(
            nisbah_id=nisbah_id,
            lineage_ref=lineage,
            predicate=predicate,
            anchors=anchors,
        )

    @property
    def unfilled_slot_count(self) -> int:
        """كم موضعَ حجّةٍ بقي بلا مرساة؟ خاصّيّةٌ تُشتَقّ لا حقلٌ يُكتَب."""

        return self.predicate.arity - len(self.anchors)

    @property
    def are_arguments_closed(self) -> bool:
        """أامتلأت المواضع؟ **مكوّنٌ واحدٌ** من الإغلاق لا الإغلاقُ كلُّه."""

        return self.unfilled_slot_count == 0

    def as_canonical_content(self) -> dict[str, object]:
        """محتوى النسبة للبصمة؛ والسلسلةُ داخلةٌ فيه لا مجاورةٌ له."""

        return {
            "nisbah_id": self.nisbah_id,
            "lineage_ref": self.lineage_ref.as_canonical_content(),
            "predicate": self.predicate.as_canonical_content(),
            "anchors": [anchor.as_canonical_content() for anchor in self.anchors],
        }

    @property
    def content_id(self) -> str:
        """بصمةُ النسبة؛ ونسبتان بسلسلتين مختلفتين بصمتاهما مختلفتان."""

        return canonical_digest(canonical_bytes(self.as_canonical_content()))


class _ParentIdentityWitness:
    """شاهدُ قراءةٍ واحدٌ لا يُنشَأ ثانيةً؛ يُوصَد بابُه عند تمام الاستيراد."""

    __slots__ = ()

    def __init__(self) -> None:
        if _PARENT_WITNESS_IS_ISSUED:
            raise AnchoredV3Error(A_REFERENCE_IS_DERIVED_NOT_CONSTRUCTED)


_PARENT_WITNESS_IS_ISSUED: bool = False
_PARENT_IDENTITY_WITNESS: Final[_ParentIdentityWitness] = _ParentIdentityWitness()
_PARENT_WITNESS_IS_ISSUED = True


@dataclass(frozen=True, slots=True)
class BaseSchemaRefV3:
    """إشارةٌ إلى هويّة `v2`؛ تُقرَأ من المخطّط القائم ولا تُكتَب رقمًا بلا مصدر."""

    base_schema_id: str
    base_schema_content_id: str
    reading_witness: object = field(default=None, repr=False, compare=False)

    def __post_init__(self) -> None:
        if self.reading_witness is not _PARENT_IDENTITY_WITNESS:
            raise AnchoredV3Error(A_REFERENCE_IS_DERIVED_NOT_CONSTRUCTED)
        _require_text(self.base_schema_id, "إصدارُ المخطّط الأب")
        _require_text(self.base_schema_content_id, "بصمةُ المخطّط الأب")

    @classmethod
    def of(cls, parent: object) -> BaseSchemaRefV3:
        """اقرأ هويّةَ الأب من المخطّط نفسِه؛ قراءةَ هويّةٍ لا استعمالَ تنفيذ."""

        schema_version = getattr(parent, "schema_version", None)
        content_id = getattr(parent, "content_id", None)
        if not isinstance(schema_version, str) or not isinstance(content_id, str):
            raise AnchoredV3Error(
                "هويّةُ الأب تُقرَأ من مخطّطٍ قائمٍ يحمل إصدارَه وبصمتَه؛ و"
                + V3_STANDS_BESIDE_V2_NOT_OVER_IT
            )
        return cls(
            base_schema_id=schema_version,
            base_schema_content_id=content_id,
            reading_witness=_PARENT_IDENTITY_WITNESS,
        )

    def as_canonical_content(self) -> dict[str, object]:
        """محتوى الإشارة للبصمة."""

        return {
            "base_schema_id": self.base_schema_id,
            "base_schema_content_id": self.base_schema_content_id,
        }


@dataclass(frozen=True, slots=True)
class AnchoredNisbahSchemaV3:
    """`v3`: مخطّطٌ مشدودٌ إلى السلسلة، مبنيٌّ على هويّة `v2` وقائمٌ بجانبها."""

    schema_version: str
    base_schema_ref: BaseSchemaRefV3
    lineage_bound: bool

    def __post_init__(self) -> None:
        _require_text(self.schema_version, "إصدارُ المخطّط المشدود")
        if not isinstance(self.base_schema_ref, BaseSchemaRefV3):
            raise AnchoredV3Error(V3_STANDS_BESIDE_V2_NOT_OVER_IT)
        if self.base_schema_ref.base_schema_id == self.schema_version:
            raise AnchoredV3Error(
                "إصدارُ `v3` غيرُ إصدار `v2`؛ وإصدارٌ يحمل اسمَ سابقه نسخٌ فوقه"
            )
        if (
            self.base_schema_ref.base_schema_id != ANCHORED_NISBAH_SCHEMA.schema_version
            or self.base_schema_ref.base_schema_content_id != PARENT_SCHEMA_CONTENT_ID
        ):
            raise AnchoredV3Error(
                "هويّةُ `v2` غيرُ مطابقةٍ للقائم: مخطّطٌ مُسنَدٌ إلى أبٍ لم يَعُد قائمًا"
            )
        if self.lineage_bound is not True:
            raise AnchoredV3Error(
                "المخطّطُ مشدودٌ إلى سلسلة الأصل؛ ومخطّطٌ غيرُ مشدودٍ هو `v2` باسمٍ آخر"
            )

    def as_canonical_content(self) -> dict[str, object]:
        """محتوى المخطّط للبصمة."""

        return {
            "schema_version": self.schema_version,
            "base_schema_ref": self.base_schema_ref.as_canonical_content(),
            "lineage_bound": self.lineage_bound,
        }

    @property
    def content_id(self) -> str:
        """بصمةُ `v3`؛ وهي غيرُ بصمتَي `v1` و`v2` ولا تحلّ محلَّهما."""

        return canonical_digest(canonical_bytes(self.as_canonical_content()))


ANCHORED_V3_NISBAH_SCHEMA: Final[AnchoredNisbahSchemaV3] = AnchoredNisbahSchemaV3(
    schema_version=ANCHORED_V3_SCHEMA_VERSION,
    base_schema_ref=BaseSchemaRefV3.of(ANCHORED_NISBAH_SCHEMA),
    lineage_bound=True,
)
"""`v3` قائمًا بجانب `v2`، مبنيًّا على هويّتها لا على اسمها."""


def _refuse_a_written_kind_in_this_layer() -> None:
    """لا حقلَ من نوع `TermAnchorKind` هنا: الدورُ يُرخَّص ولا يُكتَب نوعًا."""

    declaring = (
        LicensedRoleRefV3,
        AnchoredTermAnchorV3,
        AnchoredArgumentSlotV3,
        AnchoredPredicateSignatureV3,
        AnchoredNisbahSignatureV3,
    )
    for owner in declaring:
        for owner_field in fields(owner):
            annotation = owner_field.type
            name = annotation.__name__ if isinstance(annotation, type) else annotation
            if TermAnchorKind.__name__ in str(name):  # pragma: no cover - guard
                raise RuntimeError("دورُ المرساة رخصةٌ لا أصلٌ لغويٌّ يُكتَب نوعًا")


def _refuse_a_free_text_condition_field() -> None:
    """لا حقلَ شرطٍ نصًّا حرًّا هنا؛ وكلُّ شرطٍ مرجعٌ مبصومٌ إلى `PK_0`."""

    for owner in (AnchoredTermAnchorV3, AnchoredArgumentSlotV3):
        for owner_field in fields(owner):
            if "condition" not in owner_field.name:
                continue
            annotation = owner_field.type
            name = annotation.__name__ if isinstance(annotation, type) else annotation
            if PriorConditionRef.__name__ not in str(name):  # pragma: no cover - guard
                raise RuntimeError("شرطُ هذه الطبقة مرجعٌ مبصومٌ لا نصٌّ حرّ")


def _refuse_a_parent_that_moved() -> None:
    """أعِد اشتقاقَ هويّة الأب الحيّ؛ وتحرُّكُها يُوقف هذه الطبقةَ لا يُطوى."""

    live = BaseSchemaRefV3.of(ANCHORED_NISBAH_SCHEMA)
    if live != ANCHORED_V3_NISBAH_SCHEMA.base_schema_ref:  # pragma: no cover - guard
        raise RuntimeError(V3_STANDS_BESIDE_V2_NOT_OVER_IT)
    if (
        ANCHORED_V3_SCHEMA_VERSION == ANCHORED_NISBAH_SCHEMA.schema_version
    ):  # pragma: no cover - guard
        raise RuntimeError(V3_STANDS_BESIDE_V2_NOT_OVER_IT)


_refuse_a_written_kind_in_this_layer()
_refuse_a_free_text_condition_field()
_refuse_a_parent_that_moved()


def _refuse_a_second_parent_witness() -> None:  # pragma: no cover - import guard
    try:
        _ParentIdentityWitness()
    except AnchoredV3Error:
        return
    raise RuntimeError(A_REFERENCE_IS_DERIVED_NOT_CONSTRUCTED)


_refuse_a_second_parent_witness()
