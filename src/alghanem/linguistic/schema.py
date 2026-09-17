"""`Σ_L` — النواةُ اللغويّةُ العامّة: لغةُ النسبة، بين `Σ_M` و`Σ_{AR}`.

    Σ_M  →  Σ_L  →  Σ_AR

فـ`Σ_M` قانونُ التمثيل العامّ (حاملٌ وحالةٌ وانتقالٌ وإغلاقٌ وأثرٌ وبقايا)، ولا
`Term` فيه ولا `Predicate` ولا `Nisbah`. و`Σ_L` هذه تُولِّد سبعةَ أصنافٍ لغويّةٍ
عامّة:

    TermAnchor, Predicate, Operator, ArgumentSlot, Nisbah, Constraint,
    RelationalClosure

بلا اسمٍ عربيٍّ مخصوص، وبلا `Agent`/`Patient` سابقٍ لولادته. و`Σ_{AR}` — وهي
ليست هنا — تُحقّق هذه النواةَ في العربيّة.

**والمستوياتُ ثلاثةٌ لا مستويان** (`ThreeLevelsAreNotTwo`): سؤالُ «أفي `Σ_M` أم
في `Σ_A`؟» ثنائيٌّ زائف؛ لأنّ دعوى «اللغةُ نظامٌ لإقامة النِّسَب» أعمُّ من
العربيّة وأخصُّ من قانون التمثيل، فلا موضعَ لها في أحد الطرفين.

**والفصلُ بين المستويين مفحوصٌ لا موصوف** (`LinguisticSortsAreNotMetaSorts`):
لا صنفَ في `Σ_L` باسمِ صنفٍ في `Σ_M` ولا العكس، ويُفحَص ذلك عند الاستيراد؛
فاتّحادُ اسمٍ بين المستويين يُعيد الدمجَ الذي قام هذا المستوى لمنعه.

**و`Σ_L` مبنيّةٌ على بصمة `Σ_M`** لا على اسمها: نواةٌ تشير إلى بصمةِ لغةٍ غيرِ
القائمة نواةٌ بلغةٍ أخرى، وتُرفَض عند الإنشاء.

**ولا مثيلَ نسبةٍ واحدًا في هذه النواة** (`NoConcreteNisbahInTheNucleus`): هي
تقول **ما معنى** أن يكون الشيءُ طرفًا أو محمولًا أو نسبة، ولا تحمل طرفًا ولا
محمولًا ولا نسبةً بعينها؛ ومجموعةُ النِّسَب المبنيّة لا تصير تعريفًا للنواة
بتراكمها.

تسجيلٌ لا سلطة: لا حكمَ هنا، ولا استيرادَ من `kernel/` ولا من `arabic/`.
"""

from __future__ import annotations

from dataclasses import dataclass, fields
from typing import Final

from ..canonical_content import canonical_bytes, canonical_digest
from ..metaalgebra.schema import META_ALGEBRA_SCHEMA
from ..metaalgebra.specification import SchemaRef
from .closure import (
    ARGUMENT_FILLING_IS_NOT_CLOSURE,
    CLOSURE_COMPONENT_NAMES,
    IFADA_PREREQUISITE_NAMES,
    IFADA_VOCABULARY_IS_NOT_DUPLICATED,
    RELATIONAL_CLOSURE_IS_NOT_IFADAH,
)
from .hypothesis import THREE_LEVELS_ARE_NOT_TWO_NOTE
from .nisbah import (
    AN_OPERATOR_WITHOUT_SCOPE_IS_NOT_SCOPED,
    ARGUMENT_ROLES_ARE_DEFERRED_TO_THEIR_OWN_LAYER,
    ARITY_MUST_BE_LICENSED_BEFORE_USE,
    CANDIDATE_BRANCH_IS_NOT_A_BORN_KIND,
    NISBAH_COMPONENT_NAMES,
    PREDICATE_COMPONENT_NAMES,
    TERM_ANCHOR_IS_WIDER_THAN_GENUS,
    NisbahSignature,
    PredicateSignature,
)
from .role import RELATION_IS_NOT_REPRESENTATION

__all__ = [
    "LINGUISTIC_NISBAH_SCHEMA",
    "LINGUISTIC_SORTS_ARE_NOT_META_SORTS",
    "LINGUISTIC_SORT_IDS",
    "NO_CONCRETE_NISBAH_IN_THE_NUCLEUS",
    "SCHEMA_VERSION",
    "LinguisticLaw",
    "LinguisticNisbahSchema",
    "LinguisticNisbahSchemaError",
    "LinguisticSortDeclaration",
]


class LinguisticNisbahSchemaError(ValueError):
    """رفضٌ عند الإنشاء: بنيةٌ معيّنةٌ في النواة، أو بصمةُ `Σ_M` غيرُ مطابقة."""


SCHEMA_VERSION: Final[str] = "linguistic-nisbah.schema.v1"
"""إصدارُ النواة اللغويّة؛ وتغيّرُه حدثٌ دستوريٌّ لا تفصيلُ تحرير."""

LINGUISTIC_SORTS_ARE_NOT_META_SORTS: Final[str] = (
    "أصنافُ `Σ_L` ليست أصنافَ `Σ_M`: لا اسمَ مشتركًا بين المستويين، واتّحادُ "
    "الاسم يُعيد دمجَ قانون التمثيل بالوظيفة اللغويّة تحت لفظٍ واحد"
)

NO_CONCRETE_NISBAH_IN_THE_NUCLEUS: Final[str] = (
    "لا نسبةَ ولا محمولَ بعينه داخل النواة: نواةٌ تحمل مثيلًا واحدًا نواةٌ "
    "انقلبت نظريّةً، وصارت بنيتُها قيدًا على كلّ تحقيقٍ يُكتَب بعدُ"
)


def _require_text(value: object, label: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise LinguisticNisbahSchemaError(f"{label} نصٌّ غير فارغ")
    return value


def _require_text_tuple(value: object, label: str) -> tuple[str, ...]:
    if not isinstance(value, tuple) or not value:
        raise LinguisticNisbahSchemaError(f"{label} مجموعةٌ غير فارغة")
    for item in value:
        _require_text(item, f"عنصرٌ في {label}")
    if len(set(value)) != len(value):
        raise LinguisticNisbahSchemaError(f"{label} بلا تكرار؛ والمكرّرُ يُرفَض لا يُطوى")
    return value


@dataclass(frozen=True, slots=True)
class LinguisticSortDeclaration:
    """صنفٌ لغويٌّ في `Σ_L`: اسمُه، ومواضعُه بأسمائها، وما يُعرّفه."""

    sort_id: str
    component_names: tuple[str, ...]
    meaning: str

    def __post_init__(self) -> None:
        _require_text(self.sort_id, "اسمُ الصنف اللغويّ")
        _require_text_tuple(self.component_names, f"مواضعُ `{self.sort_id}`")
        _require_text(self.meaning, f"معنى `{self.sort_id}`")

    def as_canonical_content(self) -> dict[str, object]:
        """محتوى الصنف للبصمة."""

        return {
            "sort_id": self.sort_id,
            "component_names": list(self.component_names),
            "meaning": self.meaning,
        }


@dataclass(frozen=True, slots=True)
class LinguisticLaw:
    """قانونٌ من قوانين النواة، بنصّه المُجمَّد وما يمنعه."""

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
class LinguisticNisbahSchema:
    """`Σ_L`: أصنافُ النسبة وقوانينُها، مبنيّةً على بصمة `Σ_M`، بصفر نسبةٍ مبنيّة."""

    schema_version: str
    meta_schema_ref: SchemaRef
    sorts: tuple[LinguisticSortDeclaration, ...]
    laws: tuple[LinguisticLaw, ...]

    def __post_init__(self) -> None:
        _require_text(self.schema_version, "إصدارُ النواة اللغويّة")
        if not isinstance(self.meta_schema_ref, SchemaRef):
            raise LinguisticNisbahSchemaError(
                "النواةُ اللغويّةُ مبنيّةٌ على لغةٍ مُسمّاةٍ مبصومة"
            )
        if (
            self.meta_schema_ref.schema_version != META_ALGEBRA_SCHEMA.schema_version
            or self.meta_schema_ref.content_id != META_ALGEBRA_SCHEMA.content_id
        ):
            raise LinguisticNisbahSchemaError(
                "بصمةُ `Σ_M` غيرُ مطابقةٍ للقائمة: نواةٌ على لغةٍ لم تَعُد قائمة"
            )
        if not isinstance(self.sorts, tuple) or not self.sorts:
            raise LinguisticNisbahSchemaError("النواةُ صنفٌ لغويٌّ فأكثر")
        if not isinstance(self.laws, tuple) or not self.laws:
            raise LinguisticNisbahSchemaError("نواةٌ بلا قانونٍ واحدٍ ليست نواةً")
        for sort in self.sorts:
            if not isinstance(sort, LinguisticSortDeclaration):
                raise LinguisticNisbahSchemaError("عضوٌ في الأصناف خارج نوعه")
        for law in self.laws:
            if not isinstance(law, LinguisticLaw):
                raise LinguisticNisbahSchemaError("عضوٌ في القوانين خارج نوعه")
        for group in (self.sorts, self.laws):
            for member in group:
                if isinstance(member, NisbahSignature | PredicateSignature):
                    raise LinguisticNisbahSchemaError(
                        NO_CONCRETE_NISBAH_IN_THE_NUCLEUS
                    )
        sort_ids = _require_text_tuple(
            tuple(sort.sort_id for sort in self.sorts), "أسماءُ الأصناف"
        )
        _require_text_tuple(tuple(law.law_id for law in self.laws), "أسماءُ القوانين")
        shared = set(sort_ids) & set(META_ALGEBRA_SCHEMA.sort_ids)
        if shared:
            raise LinguisticNisbahSchemaError(LINGUISTIC_SORTS_ARE_NOT_META_SORTS)

    def sort(self, sort_id: str) -> LinguisticSortDeclaration:
        """الصنفُ باسمه؛ والغيابُ رفضٌ لا `None` يُقرأ صمتًا."""

        for declared in self.sorts:
            if declared.sort_id == sort_id:
                return declared
        raise LinguisticNisbahSchemaError(f"لا صنفَ في `Σ_L` اسمُه `{sort_id}`")

    @property
    def sort_ids(self) -> tuple[str, ...]:
        """أسماءُ الأصناف؛ خاصّيّةٌ تُشتَقّ لا حقلٌ يُكتَب."""

        return tuple(sort.sort_id for sort in self.sorts)

    @property
    def law_ids(self) -> tuple[str, ...]:
        """أسماءُ القوانين؛ خاصّيّةٌ تُشتَقّ كذلك."""

        return tuple(law.law_id for law in self.laws)

    def as_canonical_content(self) -> dict[str, object]:
        """محتوى النواة للبصمة."""

        return {
            "schema_version": self.schema_version,
            "meta_schema_ref": self.meta_schema_ref.as_canonical_content(),
            "sorts": [sort.as_canonical_content() for sort in self.sorts],
            "laws": [law.as_canonical_content() for law in self.laws],
        }

    @property
    def content_id(self) -> str:
        """بصمةُ النواة اللغويّة؛ وتحقيقٌ على بصمةٍ غيرِها تحقيقٌ لنواةٍ أخرى."""

        return canonical_digest(canonical_bytes(self.as_canonical_content()))


LINGUISTIC_NISBAH_SCHEMA: Final[LinguisticNisbahSchema] = LinguisticNisbahSchema(
    schema_version=SCHEMA_VERSION,
    meta_schema_ref=SchemaRef.of(),
    sorts=(
        LinguisticSortDeclaration(
            sort_id="TermAnchor",
            component_names=("anchor_id", "candidate_kind", "identity_condition"),
            meaning="ما يصحّ أن يكون طرفًا محفوظَ الهويّة في نسبة؛ والجنسُ فرعٌ منه",
        ),
        LinguisticSortDeclaration(
            sort_id="Predicate",
            component_names=PREDICATE_COMPONENT_NAMES,
            meaning="`Predicate_n(t_1,…,t_n)`: محمولٌ ذو رتبةٍ مُرخَّصةٍ ومواضعِ حجج",
        ),
        LinguisticSortDeclaration(
            sort_id="Operator",
            component_names=("operator_id", "scope_target"),
            meaning="مُشغِّلٌ يعمل على موضعٍ مُسمًّى من النسبة؛ ولا مُشغِّلَ بلا نطاق",
        ),
        LinguisticSortDeclaration(
            sort_id="ArgumentSlot",
            component_names=("slot_id", "position", "admissibility_condition"),
            meaning="موضعُ حجّةٍ داخلَ المحمول، أوّليٌّ بلا تسميةٍ دلاليّةٍ مسبقة",
        ),
        LinguisticSortDeclaration(
            sort_id="Nisbah",
            component_names=NISBAH_COMPONENT_NAMES,
            meaning="`P(t_1,…,t_n | Θ)`: ما يجعل الشيءَ نسبةً لا مجرّدَ طرفين",
        ),
        LinguisticSortDeclaration(
            sort_id="Constraint",
            component_names=("constraint_id", "kind", "licensed_by"),
            meaning="قيدٌ من `Θ` بجنسٍ مُجمَّدٍ ومصدرِ ترخيصٍ مُسمًّى",
        ),
        LinguisticSortDeclaration(
            sort_id="RelationalClosure",
            component_names=CLOSURE_COMPONENT_NAMES,
            meaning="خمسةٌ مجتمعةٌ ناتجُها `PreIfadahClosure` لا الإفادة",
        ),
    ),
    laws=(
        LinguisticLaw(
            law_id="ThreeLevelsAreNotTwo",
            statement=THREE_LEVELS_ARE_NOT_TWO_NOTE,
            what_it_forbids="قسمةَ الدعوى اللغويّة بين قانون التمثيل وتحقيقه العربيّ",
        ),
        LinguisticLaw(
            law_id="RelationIsNotRepresentation",
            statement=RELATION_IS_NOT_REPRESENTATION,
            what_it_forbids="دفنَ الدور النسبيّ داخل مرجع التمثيل أو العكس",
        ),
        LinguisticLaw(
            law_id="TermAnchorIsWiderThanGenus",
            statement=TERM_ANCHOR_IS_WIDER_THAN_GENUS,
            what_it_forbids="حصرَ طرف النسبة في الجنس المنطقيّ الضيّق",
        ),
        LinguisticLaw(
            law_id="CandidateBranchIsNotABornKind",
            statement=CANDIDATE_BRANCH_IS_NOT_A_BORN_KIND,
            what_it_forbids="قراءةَ فرعٍ مرشَّحٍ نمطًا مولودًا قبل تجربته",
        ),
        LinguisticLaw(
            law_id="ArityMustBeLicensedBeforeUse",
            statement=ARITY_MUST_BE_LICENSED_BEFORE_USE,
            what_it_forbids="انتزاعَ الرتبة من الحالة الهدف ثمّ إثباتَها بها",
        ),
        LinguisticLaw(
            law_id="ArgumentRolesAreDeferredToTheirOwnLayer",
            statement=ARGUMENT_ROLES_ARE_DEFERRED_TO_THEIR_OWN_LAYER,
            what_it_forbids="إدخالَ Agent/Patient/Cause/Result في النواة قبل ولادتها",
        ),
        LinguisticLaw(
            law_id="AnOperatorWithoutScopeIsNotScoped",
            statement=AN_OPERATOR_WITHOUT_SCOPE_IS_NOT_SCOPED,
            what_it_forbids="قراءةَ مُشغِّلٍ بلا نطاقٍ عامًّا بالسهو",
        ),
        LinguisticLaw(
            law_id="ArgumentFillingIsNotClosure",
            statement=ARGUMENT_FILLING_IS_NOT_CLOSURE,
            what_it_forbids="قراءةَ امتلاء الحجج إغلاقًا نسبيًّا",
        ),
        LinguisticLaw(
            law_id="RelationalClosureIsNotIfadah",
            statement=RELATIONAL_CLOSURE_IS_NOT_IFADAH,
            what_it_forbids="اشتقاقَ الإفادة من الإغلاق بلا قوّةٍ وسياق",
        ),
        LinguisticLaw(
            law_id="IfadaVocabularyIsNotDuplicated",
            statement=IFADA_VOCABULARY_IS_NOT_DUPLICATED,
            what_it_forbids="إنشاءَ مفردةِ إفادةٍ ثانيةٍ في هذه النواة",
        ),
        LinguisticLaw(
            law_id="NoConcreteNisbahInTheNucleus",
            statement=NO_CONCRETE_NISBAH_IN_THE_NUCLEUS,
            what_it_forbids="شحنَ النواة بنسبةٍ أو محمولٍ بعينه",
        ),
    ),
)
"""`Σ_L` المُجمَّدة؛ مثيلٌ واحدٌ يُنسَب إليه كلُّ تحقيقٍ لغويٍّ يُكتَب بها."""

LINGUISTIC_SORT_IDS: Final[tuple[str, ...]] = LINGUISTIC_NISBAH_SCHEMA.sort_ids
"""أسماءُ أصناف `Σ_L` السبعة، مُشتَقّةً من النواة لا مكتوبةً بجانبها."""


_CONCRETE_FIELD_MARKERS: Final[tuple[str, ...]] = (
    "nisbah_signature",
    "predicate_signature",
    "anchors",
    "nisab",
)

_SCHEMA_TYPES: Final[tuple[type, ...]] = (
    LinguisticNisbahSchema,
    LinguisticLaw,
    LinguisticSortDeclaration,
)

for _declaring_type in _SCHEMA_TYPES:  # pragma: no cover - import guard
    for _field in fields(_declaring_type):
        if any(marker in _field.name for marker in _CONCRETE_FIELD_MARKERS):
            raise RuntimeError(NO_CONCRETE_NISBAH_IN_THE_NUCLEUS)

if set(LINGUISTIC_SORT_IDS) & set(META_ALGEBRA_SCHEMA.sort_ids):  # pragma: no cover
    raise RuntimeError(LINGUISTIC_SORTS_ARE_NOT_META_SORTS)

if len(IFADA_PREREQUISITE_NAMES) != 3:  # pragma: no cover - import guard
    raise RuntimeError(RELATIONAL_CLOSURE_IS_NOT_IFADAH)
