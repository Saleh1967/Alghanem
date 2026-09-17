"""`Σ_M` — لغةُ الميتا-جبر نفسُها، لا نظريّةً مكتوبةً بها.

هذه الوحدةُ تُجمّد **ما معنى** أن يكون الشيءُ طبقةً، و**ما معنى** أن يكون
انتقالًا، و**ما معنى** أن يكون تحقيقًا؛ ولا تحمل طبقةً واحدةً ولا انتقالًا
واحدًا:

    Σ_M = MetaAlgebraSchema      ← لغةُ الجبر، صفرُ طبقات
    Σ_A = AbstractSystemSpecification  ← نظريّةٌ معيّنةٌ مكتوبةٌ بتلك اللغة

والفرقُ بينهما هو الذي يمنع أن تتحوّل مجموعةُ الطبقات المبنيّة اليوم إلى تعريفٍ
للميتا-جبر بتراكمها (`A_SCHEMA_IS_NOT_A_SPECIFICATION`).

**ومصدرُ أسماء المكوّنات واحدٌ لا نسخةٌ ثانية:** `LAYER_COMPONENT_NAMES` من
`layer`، و`TRANSITION_COMPONENT_NAMES` و`REQUIRED_AUDIT_CERTIFICATE_FACTS` من
`transition`. ونسختان من قائمةٍ واحدةٍ قائمتان تنحرفان بلا أن تُخفق إحداهما.

تسجيلٌ لا سلطة: لا حكمَ في صنفٍ هنا، ولا استيرادَ من `kernel/` ولا من `arabic/`
ولا من حزمة التوليد.
"""

from __future__ import annotations

from dataclasses import dataclass, fields
from typing import Final

from ..canonical_content import canonical_bytes, canonical_digest
from .composition import (
    BACKWARD_AUDITABILITY_OBLIGATION,
    COMPOSITION_LAW,
    THEOREM_VALIDITY_IS_NOT_INSTANTIATION_COVERAGE,
)
from .layer import (
    CARRIER_IS_NOT_STATE,
    LAYER_COMPONENT_NAMES,
    LayerSignature,
)
from .transition import (
    CLOSURE_IS_NOT_A_RIGHT_OF_EXIT,
    HANDOFF_LAW,
    NO_JUMP_LAW,
    REQUIRED_AUDIT_CERTIFICATE_FACTS,
    TRANSITION_COMPONENT_NAMES,
    TransitionSignature,
)

__all__ = [
    "A_SCHEMA_IS_NOT_A_SPECIFICATION",
    "META_ALGEBRA_SCHEMA",
    "NO_CONCRETE_STRUCTURE_IN_THE_SCHEMA",
    "REALIZATION_COMPONENT_NAMES",
    "SCHEMA_VERSION",
    "MetaAlgebraSchema",
    "MetaAlgebraSchemaError",
    "SchemaLaw",
    "SortDeclaration",
]


class MetaAlgebraSchemaError(ValueError):
    """رفضٌ عند الإنشاء: صنفٌ في المخطّط يحمل بنيةً معيّنةً لا تعريفَ بنية."""


A_SCHEMA_IS_NOT_A_SPECIFICATION: Final[str] = (
    "لغةُ الجبر ليست نظريّةً مكتوبةً بها: `Σ_M` تقول ما معنى الطبقةِ والانتقال، "
    "و`Σ_A` تحمل طبقاتٍ وانتقالاتٍ بعينها؛ ومجموعةُ الطبقات لا تصير تعريفًا "
    "للميتا-جبر بتراكمها"
)

NO_CONCRETE_STRUCTURE_IN_THE_SCHEMA: Final[str] = (
    "لا طبقةَ ولا انتقالَ داخل المخطّط: مخطّطٌ يحمل مثيلًا واحدًا مخطّطٌ انقلب "
    "نظريّةً، وصارت بنيتُه قيدًا على كلّ نظريّةٍ تُكتَب بعدُ"
)

SCHEMA_VERSION: Final[str] = "meta-algebra.schema.v1"
"""إصدارُ لغة الجبر؛ وتغيّرُه حدثٌ دستوريٌّ لا تفصيلُ تحرير."""


def _require_text(value: object, label: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise MetaAlgebraSchemaError(f"{label} نصٌّ غير فارغ")
    return value


def _require_text_tuple(value: object, label: str) -> tuple[str, ...]:
    if not isinstance(value, tuple) or not value:
        raise MetaAlgebraSchemaError(f"{label} مجموعةٌ غير فارغة")
    for item in value:
        _require_text(item, f"عنصرٌ في {label}")
    if len(set(value)) != len(value):
        raise MetaAlgebraSchemaError(f"{label} بلا تكرار؛ والمكرّرُ يُرفَض لا يُطوى")
    return value


@dataclass(frozen=True, slots=True)
class SortDeclaration:
    """صنفٌ نحويٌّ في لغة الجبر: اسمُه، ومكوّناتُه بأسمائها، وما يُعرّفه.

    `component_names` أسماءُ المواضع لا مثيلاتُها؛ فإعلانُ `Layer` بثمانية مواضعَ
    ليس دعوى أنّ في العالم ثماني طبقاتٍ ولا طبقةً واحدةً مبنيّة.
    """

    sort_id: str
    component_names: tuple[str, ...]
    meaning: str

    def __post_init__(self) -> None:
        _require_text(self.sort_id, "اسمُ الصنف النحويّ")
        _require_text_tuple(self.component_names, f"مواضعُ `{self.sort_id}`")
        _require_text(self.meaning, f"معنى `{self.sort_id}`")

    def as_canonical_content(self) -> dict[str, object]:
        """محتوى الصنف النحويّ للبصمة."""

        return {
            "sort_id": self.sort_id,
            "component_names": list(self.component_names),
            "meaning": self.meaning,
        }


@dataclass(frozen=True, slots=True)
class SchemaLaw:
    """قانونٌ من قوانين اللغة، بنصّه المُجمَّد وما يمنعه.

    والنصُّ مأخوذٌ من موضعه الأصليّ لا معادٌ كتابتُه هنا، فلا نسختان لقانونٍ
    واحدٍ تنحرفان.
    """

    law_id: str
    statement: str
    what_it_forbids: str

    def __post_init__(self) -> None:
        _require_text(self.law_id, "اسمُ القانون")
        _require_text(self.statement, f"نصُّ `{self.law_id}`")
        _require_text(self.what_it_forbids, f"ما يمنعه `{self.law_id}`")

    def as_canonical_content(self) -> dict[str, object]:
        """محتوى القانون للبصمة."""

        return {
            "law_id": self.law_id,
            "statement": self.statement,
            "what_it_forbids": self.what_it_forbids,
        }


@dataclass(frozen=True, slots=True)
class MetaAlgebraSchema:
    """`Σ_M`: لغةُ الجبر — أصنافُها النحويّة وقوانينُها، بصفر بنيةٍ معيّنة."""

    schema_version: str
    sorts: tuple[SortDeclaration, ...]
    laws: tuple[SchemaLaw, ...]

    def __post_init__(self) -> None:
        _require_text(self.schema_version, "إصدارُ اللغة")
        if not isinstance(self.sorts, tuple) or not self.sorts:
            raise MetaAlgebraSchemaError("اللغةُ صنفٌ نحويٌّ فأكثر")
        if not isinstance(self.laws, tuple) or not self.laws:
            raise MetaAlgebraSchemaError("لغةٌ بلا قانونٍ واحدٍ ليست لغةَ جبر")
        for sort in self.sorts:
            if not isinstance(sort, SortDeclaration):
                raise MetaAlgebraSchemaError("عضوٌ في الأصناف النحويّة خارج نوعه")
        for law in self.laws:
            if not isinstance(law, SchemaLaw):
                raise MetaAlgebraSchemaError("عضوٌ في القوانين خارج نوعه")
        for value in (self.sorts, self.laws):
            for member in value:
                if isinstance(member, LayerSignature | TransitionSignature):
                    raise MetaAlgebraSchemaError(NO_CONCRETE_STRUCTURE_IN_THE_SCHEMA)
        _require_text_tuple(
            tuple(sort.sort_id for sort in self.sorts), "أسماءُ الأصناف النحويّة"
        )
        _require_text_tuple(tuple(law.law_id for law in self.laws), "أسماءُ القوانين")

    def sort(self, sort_id: str) -> SortDeclaration:
        """الصنفُ النحويُّ باسمه؛ والغيابُ رفضٌ لا `None` يُقرأ صمتًا."""

        for declared in self.sorts:
            if declared.sort_id == sort_id:
                return declared
        raise MetaAlgebraSchemaError(f"لا صنفَ نحويًّا في اللغة اسمُه `{sort_id}`")

    @property
    def sort_ids(self) -> tuple[str, ...]:
        """أسماءُ الأصناف؛ خاصّيّةٌ تُشتَقّ لا حقلٌ يُكتَب."""

        return tuple(sort.sort_id for sort in self.sorts)

    @property
    def law_ids(self) -> tuple[str, ...]:
        """أسماءُ القوانين؛ خاصّيّةٌ تُشتَقّ كذلك."""

        return tuple(law.law_id for law in self.laws)

    def as_canonical_content(self) -> dict[str, object]:
        """محتوى اللغة للبصمة."""

        return {
            "schema_version": self.schema_version,
            "sorts": [sort.as_canonical_content() for sort in self.sorts],
            "laws": [law.as_canonical_content() for law in self.laws],
        }

    @property
    def content_id(self) -> str:
        """بصمةُ لغة الجبر؛ ونظريّةٌ مبنيّةٌ على بصمةٍ غيرِها نظريّةٌ بلغةٍ أخرى."""

        return canonical_digest(canonical_bytes(self.as_canonical_content()))


REALIZATION_COMPONENT_NAMES: Final[tuple[str, ...]] = (
    "domain",
    "layer_realizations",
    "transition_realizations",
)
"""مواضعُ التحقيق الثلاثة؛ ميدانٌ، وتحقيقُ طبقاتٍ، وتحقيقُ انتقالات."""


META_ALGEBRA_SCHEMA: Final[MetaAlgebraSchema] = MetaAlgebraSchema(
    schema_version=SCHEMA_VERSION,
    sorts=(
        SortDeclaration(
            sort_id="Layer",
            component_names=LAYER_COMPONENT_NAMES,
            meaning="𝒜 = (C, S, Ω, Rel, Inv, Cl, Tr, R): ما يجعل الشيءَ طبقةً",
        ),
        SortDeclaration(
            sort_id="Transition",
            component_names=TRANSITION_COMPONENT_NAMES + ("handoff",),
            meaning="𝒯 = (D, G, T, P, τ, ρ) مع شرط التسليم: ما يجعل الشيءَ انتقالًا",
        ),
        SortDeclaration(
            sort_id="AuditCertificate",
            component_names=REQUIRED_AUDIT_CERTIFICATE_FACTS,
            meaning="ما تستردُّه شهادةُ التدقيق الرجعيّ؛ خمسةٌ مجتمعةٌ لا بديلَ لواحدها",
        ),
        SortDeclaration(
            sort_id="Realization",
            component_names=REALIZATION_COMPONENT_NAMES,
            meaning="تحقيقُ نظريّةٍ في ميدانٍ مُسمًّى، بتغطيةٍ تامّةٍ لمواضع كلّ طبقةٍ وانتقال",
        ),
    ),
    laws=(
        SchemaLaw(
            law_id="NoJump",
            statement=NO_JUMP_LAW,
            what_it_forbids="شهادةَ نجاحٍ عند عدم الترخيص",
        ),
        SchemaLaw(
            law_id="Handoff",
            statement=HANDOFF_LAW,
            what_it_forbids=CLOSURE_IS_NOT_A_RIGHT_OF_EXIT,
        ),
        SchemaLaw(
            law_id="CarrierIsNotState",
            statement=CARRIER_IS_NOT_STATE,
            what_it_forbids="دفنَ فضاء الحالة حقلًا داخل الحامل",
        ),
        SchemaLaw(
            law_id="Composition",
            statement=COMPOSITION_LAW,
            what_it_forbids="قراءةَ سلسلةٍ صحيحةِ التجاور سلسلةً مُبرهَنةً أو مُشغَّلة",
        ),
        SchemaLaw(
            law_id="BackwardAuditability",
            statement=BACKWARD_AUDITABILITY_OBLIGATION,
            what_it_forbids="طلبَ معكوسِ التحويل بدل شهادةِ سببِ الترخيص",
        ),
        SchemaLaw(
            law_id="ValidityIsNotCoverage",
            statement=THEOREM_VALIDITY_IS_NOT_INSTANTIATION_COVERAGE,
            what_it_forbids="قراءةَ عدد البنى المبنيّة برهانًا أو عيبًا في البرهان",
        ),
        SchemaLaw(
            law_id="SchemaIsNotSpecification",
            statement=A_SCHEMA_IS_NOT_A_SPECIFICATION,
            what_it_forbids=NO_CONCRETE_STRUCTURE_IN_THE_SCHEMA,
        ),
    ),
)
"""لغةُ الجبر المُجمَّدة؛ مثيلٌ واحدٌ تُنسَب إليه كلُّ نظريّةٍ تُكتَب بها."""


_CONCRETE_FIELD_MARKERS: Final[tuple[str, ...]] = (
    "layer_signature",
    "transition_signature",
    "layers",
    "transitions",
    "chain",
)

_SCHEMA_TYPES: Final[tuple[type, ...]] = (
    MetaAlgebraSchema,
    SchemaLaw,
    SortDeclaration,
)

for _declaring_type in _SCHEMA_TYPES:  # pragma: no cover - import guard
    for _field in fields(_declaring_type):
        if any(marker in _field.name for marker in _CONCRETE_FIELD_MARKERS):
            raise RuntimeError(NO_CONCRETE_STRUCTURE_IN_THE_SCHEMA)
