"""هويّةُ النتيجة: نواةٌ تُبصَم، وغلافٌ يحمل البصمةَ والتصريحَ الذي حكم به.

    ExecutionResultCore   →  execution_digest
    ExecutionResultEnvelope  =  declaration_document + core + execution_digest

**والبصمةُ لا تبصم نفسَها** (`ADigestDoesNotContainItself`): لو وُضِع
`execution_digest` حقلًا في النواة لصار المحتوى المبصومُ متضمّنًا بصمتَه، وهذا
دورٌ لا يُغلَق. فالنواةُ محتوًى خالص، والبصمةُ عنها في الغلاف.

**وإعادةُ التشغيل من التصريح لا من البصمة** (`AReplayNeedsTheDeclarationNotItsDigest`):
البصمةُ لا تُعكَس، فلا يُعاد منها تنفيذ. لذلك يحمل الغلافُ **وثيقةَ التصريح
كاملةً** خارج النواة، وتُشَدّ إليها بشرطٍ لازم:

    Digest(declaration_document) == core.input_digest

تسجيلٌ لا سلطة: لا ولادةَ ولا حكمَ ولادةٍ ولا تجميدَ `E0`.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Final

from ..canonical_content import canonical_bytes, canonical_digest
from .outcome import CheckStanding, ExecutionOutcome, Identity, LawCheckEntry, Violation
from .requirement import UnresolvedRequirement

__all__ = [
    "A_DIGEST_DOES_NOT_CONTAIN_ITSELF",
    "A_REPLAY_NEEDS_THE_DECLARATION_NOT_ITS_DIGEST",
    "EXECUTION_RESULT_SCHEMA",
    "ExecutionResultCore",
    "ExecutionResultEnvelope",
    "ExecutionResultError",
    "LineageIdentity",
]


EXECUTION_RESULT_SCHEMA: Final[str] = "alghanem.execution.result.v1"

A_DIGEST_DOES_NOT_CONTAIN_ITSELF: Final[str] = (
    "البصمةُ لا تبصم نفسَها: محتوًى يتضمّن بصمتَه دورٌ لا يُغلَق؛ فالنواةُ محتوًى "
    "خالصٌ والبصمةُ عنها في الغلاف لا فيها"
)

A_REPLAY_NEEDS_THE_DECLARATION_NOT_ITS_DIGEST: Final[str] = (
    "إعادةُ التشغيل تحتاج التصريحَ لا بصمتَه: البصمةُ لا تُعكَس، فيحمل الغلافُ "
    "وثيقةَ التصريح كاملةً وتُشَدّ إليها ببصمة الإدخال"
)


class ExecutionResultError(ValueError):
    """رفضٌ عند تكوين نتيجةٍ أو غلافها؛ لا حملَ على أقرب حالةٍ مقبولة."""


@dataclass(frozen=True, slots=True)
class LineageIdentity:
    """هويّةُ السلسلة الثلاثيّة؛ ثلاثُ هويّاتٍ وبصمةٌ واحدةٌ تجمعها."""

    base: Identity
    general_ontology: Identity
    linguistic_ontology: Identity
    content_id: str

    def __post_init__(self) -> None:
        for value in (self.base, self.general_ontology, self.linguistic_ontology):
            if not isinstance(value, Identity):
                raise ExecutionResultError("مستوى السلسلة هويّةٌ كاملةٌ لا اسمٌ حرّ")
        if not isinstance(self.content_id, str) or not self.content_id.strip():
            raise ExecutionResultError("بصمةُ السلسلة نصٌّ غير فارغ")

    def as_canonical_content(self) -> dict[str, object]:
        """محتوى هويّة السلسلة للبصمة."""

        return {
            "base": self.base.as_canonical_content(),
            "general_ontology": self.general_ontology.as_canonical_content(),
            "linguistic_ontology": self.linguistic_ontology.as_canonical_content(),
            "content_id": self.content_id,
        }


@dataclass(frozen=True, slots=True)
class ExecutionResultCore:
    """نواةُ النتيجة: الحكمُ وأثرُه وهويّاتُه؛ ولا بصمةَ لنفسها فيها."""

    schema: str
    nisbah_schema: str
    input_digest: str
    law_set_id: str
    law_set_digest: str
    outcome: ExecutionOutcome
    trace: tuple[LawCheckEntry, ...]
    violations: tuple[Violation, ...]
    residuals: tuple[UnresolvedRequirement, ...]
    lineage_identity: LineageIdentity | None
    materialized_identity: Identity | None

    def __post_init__(self) -> None:
        if not isinstance(self.outcome, ExecutionOutcome):
            raise ExecutionResultError("الحكمُ عضوٌ في مفردته المغلقة")
        for value, label in (
            (self.schema, "مِخطاطُ النتيجة"),
            (self.nisbah_schema, "مِخطاطُ النسبة"),
            (self.input_digest, "بصمةُ الإدخال"),
            (self.law_set_id, "مُعرِّفُ قائمة القوانين"),
            (self.law_set_digest, "بصمةُ قائمة القوانين"),
        ):
            if not isinstance(value, str) or not value.strip():
                raise ExecutionResultError(f"{label} نصٌّ غير فارغ")
        if not isinstance(self.trace, tuple) or not self.trace:
            raise ExecutionResultError("الأثرُ سطرٌ فأكثر؛ وحكمٌ بلا أثرٍ غيرُ مقروء")
        for entry in self.trace:
            if not isinstance(entry, LawCheckEntry):
                raise ExecutionResultError("عضوٌ في الأثر خارج نوعه")
        violated = tuple(
            entry for entry in self.trace if entry.standing is CheckStanding.VIOLATED
        )
        if len(violated) != len(self.violations):
            raise ExecutionResultError(
                "المخالفاتُ هي سطورُ الأثر الثابتةُ نفسُها لا قائمةٌ تُكتَب بجانبها"
            )
        if (self.outcome is ExecutionOutcome.BLOCK) != bool(violated):
            raise ExecutionResultError(
                "الحجبُ مخالفةٌ ثابتةٌ في الأثر؛ ولا حجبَ بلا مخالفةٍ ولا مخالفةَ بلا حجب"
            )
        if self.outcome is ExecutionOutcome.DEFER and not self.residuals:
            raise ExecutionResultError("التأجيلُ بقيّةٌ مُسمّاةٌ لا صمت")
        if self.outcome is not ExecutionOutcome.PASS and (
            self.materialized_identity is not None
        ):
            raise ExecutionResultError(
                "المادّةُ السلطويّةُ لا تُنشَأ إلّا بعد النجاح؛ والحكمُ يسبق الإنشاء"
            )

    @property
    def not_evaluated(self) -> tuple[LawCheckEntry, ...]:
        """السطورُ التي حجب شرطٌ سابقٌ تقييمَها؛ وليست من البقايا."""

        return tuple(
            entry
            for entry in self.trace
            if entry.standing is CheckStanding.NOT_EVALUATED_BY_PREREQUISITE
        )

    def as_canonical_content(self) -> dict[str, object]:
        """محتوى النواة للبصمة؛ ولا بصمةَ نتيجةٍ داخله."""

        return {
            "schema": self.schema,
            "nisbah_schema": self.nisbah_schema,
            "input_digest": self.input_digest,
            "law_set_id": self.law_set_id,
            "law_set_digest": self.law_set_digest,
            "outcome": self.outcome.value,
            "trace": [entry.as_canonical_content() for entry in self.trace],
            "violations": [item.as_canonical_content() for item in self.violations],
            "residuals": [item.as_canonical_content() for item in self.residuals],
            "lineage_identity": (
                None
                if self.lineage_identity is None
                else self.lineage_identity.as_canonical_content()
            ),
            "materialized_identity": (
                None
                if self.materialized_identity is None
                else self.materialized_identity.as_canonical_content()
            ),
        }


@dataclass(frozen=True, slots=True)
class ExecutionResultEnvelope:
    """الغلاف: التصريحُ الذي حكم به، ونواةُ الحكم، وبصمتُها عنها لا فيها."""

    declaration_document: dict[str, object]
    core: ExecutionResultCore
    execution_digest: str

    def __post_init__(self) -> None:
        if not isinstance(self.core, ExecutionResultCore):
            raise ExecutionResultError("نواةُ النتيجة من نوعها لا من وصفٍ حرّ")
        if not isinstance(self.declaration_document, dict):
            raise ExecutionResultError(A_REPLAY_NEEDS_THE_DECLARATION_NOT_ITS_DIGEST)
        recomputed_input = canonical_digest(canonical_bytes(self.declaration_document))
        if recomputed_input != self.core.input_digest:
            raise ExecutionResultError(
                "وثيقةُ التصريح في الغلاف مشدودةٌ إلى بصمة الإدخال؛ و"
                + A_REPLAY_NEEDS_THE_DECLARATION_NOT_ITS_DIGEST
            )
        recomputed = canonical_digest(canonical_bytes(self.core.as_canonical_content()))
        if recomputed != self.execution_digest:
            raise ExecutionResultError(
                "بصمةُ التنفيذ مُشتَقّةٌ من النواة لا مكتوبةٌ بجانبها؛ و"
                + A_DIGEST_DOES_NOT_CONTAIN_ITSELF
            )

    @classmethod
    def sealing(
        cls, declaration_document: dict[str, object], core: ExecutionResultCore
    ) -> ExecutionResultEnvelope:
        """اختم نتيجةً ببصمتها المُشتَقّة؛ ولا تُكتَب البصمةُ من خارجها."""

        return cls(
            declaration_document=declaration_document,
            core=core,
            execution_digest=canonical_digest(
                canonical_bytes(core.as_canonical_content())
            ),
        )

    def as_canonical_content(self) -> dict[str, object]:
        """محتوى الغلاف للحفظ؛ وهو الصيغةُ التي يُعاد منها التشغيل."""

        return {
            "declaration": self.declaration_document,
            "result": self.core.as_canonical_content(),
            "execution_digest": self.execution_digest,
        }
