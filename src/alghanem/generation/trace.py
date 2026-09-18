"""أثرُ الإنتاج: كلُّ انتقالٍ يُسمّي مدخلَه وقاعدتَه ومخرجَه وما لم يُحسَم فيه.

    GenerationStep  =  stage + input_content_id + rule_id + output_content_id

**والأثرُ متّصلٌ بالبصمات** (`AChainIsReadFromItsDigestsNotItsOrder`): مخرجُ
خطوةٍ هو مدخلُ التالية بعينه، فلا تُركَّب مرحلةٌ فوق مرحلةٍ لم تُنتَج، ولا يُقرأ
الترتيبُ وحدَه دليلًا على الاتّصال.

**والبقايا مرصودةٌ لا مكتوبة** (`ResidualsAreObservedNotAuthored`): كلُّ بقيّةٍ
تُسمّي الخطوةَ التي رصدتها، فلا تُملى بقيّةٌ في مدخلٍ ولا تُنسَب إلى انتقالٍ لم
يجرِ. وجنسُها من مفردةٍ مغلقة، فلا وصفَ حرًّا يُخفي تحته حجبًا غيرَ مُسمًّى.

**ولا مدخلَ خفيّ** (`SameSpecificationSameRulesSameTrace`): لا وقتٌ ولا عشوائيٌّ
ولا بيئةٌ ولا مسارُ ملفّ؛ فما لم يُصرَّح به لا يدخل في الأثر ولا في بصمته.

تسجيلٌ لا سلطة: لا ولادةَ، ولا حكمَ ولادةٍ، ولا تجميدَ `E0`.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Final

from ..canonical_content import canonical_bytes, canonical_digest, is_canonical_digest
from .laws import RESIDUALS_ARE_OBSERVED_NOT_AUTHORED

__all__ = [
    "A_CHAIN_IS_READ_FROM_ITS_DIGESTS_NOT_ITS_ORDER",
    "GenerationResidual",
    "GenerationResidualKind",
    "GenerationStage",
    "GenerationStep",
    "GenerationTrace",
    "GenerationTraceError",
    "SAME_SPECIFICATION_SAME_RULES_SAME_TRACE",
]


A_CHAIN_IS_READ_FROM_ITS_DIGESTS_NOT_ITS_ORDER: Final[str] = (
    "السلسلةُ تُقرأ من بصماتها لا من ترتيبها: مخرجُ الخطوة هو مدخلُ التالية "
    "بعينه، وترتيبٌ بلا اتّصالِ بصماتٍ جوارٌ لا اشتقاق"
)

SAME_SPECIFICATION_SAME_RULES_SAME_TRACE: Final[str] = (
    "المواصفةُ نفسُها بالقواعد نفسِها تُعطي الأثرَ نفسَه: لا وقتَ ولا عشوائيَّ ولا "
    "بيئةَ ولا مسارَ ملفٍّ يدخل في خطوةٍ أو في بصمتها"
)


class GenerationTraceError(ValueError):
    """رفضٌ عند تكوين خطوةٍ أو أثرٍ أو بقيّة."""


class GenerationStage(Enum):
    """مراحلُ الإنتاج المُسمّاة؛ والإسقاطان أخوان بعد التكوين لا سلسلةٌ واحدة.

    و`SPECIFICATION_CONFORMANCE` مرحلةُ **حكمٍ** لا مرحلةُ إنتاج: لا تُخرِج
    محتوًى ولا تدخل في سلسلة البصمات، وإنّما تُنسَب إليها بقايا بوّابةِ المطابقة.
    """

    LEXICAL_SELECTION = "lexical_selection"
    WORD_FORM = "word_form"
    RELATION_SLOT_ASSIGNMENT = "relation_slot_assignment"
    COMPOSITION = "composition"
    CASE_EFFECT = "case_effect"
    PHONOLOGICAL_PROJECTION = "phonological_projection"
    ORTHOGRAPHIC_PROJECTION = "orthographic_projection"
    UTTERANCE = "utterance"
    SPECIFICATION_CONFORMANCE = "specification_conformance"


class GenerationResidualKind(Enum):
    """أجناسُ البقايا؛ مفردةٌ مغلقةٌ لا نصٌّ حرٌّ يُخفي حجبًا غيرَ مُسمًّى."""

    UNMEASURED_PROSODIC_LAYER = "unmeasured_prosodic_layer"
    UNDERIVED_MORPHOLOGICAL_FORM = "underived_morphological_form"
    UNEXPRESSED_CASE_EFFECT = "unexpressed_case_effect"
    UNRESOLVED_LEXICAL_CHOICE = "unresolved_lexical_choice"
    UNCERTIFIED_ROUND_TRIP = "uncertified_round_trip"
    UNLICENSED_SYNTACTIC_FUNCTION_ASSIGNMENT = (
        "unlicensed_syntactic_function_assignment"
    )
    UNATTESTED_LEXICAL_REFERENCE = "unattested_lexical_reference"


@dataclass(frozen=True, slots=True)
class GenerationResidual:
    """بقيّةٌ مرصودة: جنسُها، وموضعُها، والخطوةُ التي رصدتها، وسببُها المُسمّى."""

    kind: GenerationResidualKind
    stage: GenerationStage
    subject_id: str
    reason: str

    def __post_init__(self) -> None:
        if not isinstance(self.kind, GenerationResidualKind):
            raise GenerationTraceError("جنسُ البقيّة عضوٌ في مفردته المغلقة")
        if not isinstance(self.stage, GenerationStage):
            raise GenerationTraceError(
                "البقيّةُ تُسمّي المرحلةَ التي رصدتها؛ و"
                + RESIDUALS_ARE_OBSERVED_NOT_AUTHORED
            )
        for value, label in ((self.subject_id, "موضوعُ البقيّة"), (self.reason, "سببُها")):
            if not isinstance(value, str) or not value.strip():
                raise GenerationTraceError(f"{label} نصٌّ غير فارغ")

    def as_canonical_content(self) -> dict[str, object]:
        """محتوى البقيّة للبصمة."""

        return {
            "kind": self.kind.value,
            "stage": self.stage.value,
            "subject_id": self.subject_id,
            "reason": self.reason,
        }


@dataclass(frozen=True, slots=True)
class GenerationStep:
    """خطوةُ انتقالٍ واحدة: مرحلتُها، ومدخلُها وقاعدتُها ومخرجُها، وبقاياها."""

    stage: GenerationStage
    rule_id: str
    input_content_id: str
    output_content_id: str | None
    residuals: tuple[GenerationResidual, ...]

    def __post_init__(self) -> None:
        if not isinstance(self.stage, GenerationStage):
            raise GenerationTraceError("مرحلةُ الخطوة عضوٌ في مفردتها المغلقة")
        if not isinstance(self.rule_id, str) or not self.rule_id.strip():
            raise GenerationTraceError("مُعرِّفُ القاعدة المُطبَّقة نصٌّ غير فارغ")
        if not is_canonical_digest(self.input_content_id):
            raise GenerationTraceError("مدخلُ الخطوة بصمةٌ قانونيّةٌ لا وصفٌ حرّ")
        if self.output_content_id is not None and not is_canonical_digest(
            self.output_content_id
        ):
            raise GenerationTraceError("مخرجُ الخطوة بصمةٌ قانونيّةٌ أو غيابٌ مُسبَّب")
        if not isinstance(self.residuals, tuple):
            raise GenerationTraceError("بقايا الخطوة مجموعةٌ مُصرَّحٌ بها")
        for residual in self.residuals:
            if not isinstance(residual, GenerationResidual):
                raise GenerationTraceError("عضوٌ في البقايا خارج نوعه")
            if residual.stage is not self.stage:
                raise GenerationTraceError(
                    "بقيّةٌ تُنسَب إلى مرحلةٍ غير مرحلتها؛ و"
                    + RESIDUALS_ARE_OBSERVED_NOT_AUTHORED
                )
        if self.output_content_id is None and not self.residuals:
            raise GenerationTraceError("خطوةٌ بلا مخرجٍ تُسمّي بقيّتها؛ والحجبُ لا يكون صمتًا")

    def as_canonical_content(self) -> dict[str, object]:
        """محتوى الخطوة للبصمة."""

        return {
            "stage": self.stage.value,
            "rule_id": self.rule_id,
            "input_content_id": self.input_content_id,
            "output_content_id": self.output_content_id,
            "residuals": [
                residual.as_canonical_content() for residual in self.residuals
            ],
        }


@dataclass(frozen=True, slots=True)
class GenerationTrace:
    """أثرُ إنتاجٍ متّصل: خطوةٌ فأكثر، ومخرجُ كلِّ خطوةٍ مدخلُ تاليتها بعينه."""

    steps: tuple[GenerationStep, ...]

    def __post_init__(self) -> None:
        if not isinstance(self.steps, tuple) or not self.steps:
            raise GenerationTraceError("الأثرُ خطوةٌ فأكثر؛ وإنتاجٌ بلا أثرٍ غيرُ مقروء")
        previous: GenerationStep | None = None
        for step in self.steps:
            if not isinstance(step, GenerationStep):
                raise GenerationTraceError("عضوٌ في الأثر خارج نوعه")
            if previous is not None:
                if previous.output_content_id is None:
                    raise GenerationTraceError(
                        "لا خطوةَ بعد خطوةٍ لم تُخرِج شيئًا؛ و"
                        + A_CHAIN_IS_READ_FROM_ITS_DIGESTS_NOT_ITS_ORDER
                    )
                if previous.output_content_id != step.input_content_id:
                    raise GenerationTraceError(
                        A_CHAIN_IS_READ_FROM_ITS_DIGESTS_NOT_ITS_ORDER
                    )
            previous = step

    @property
    def residuals(self) -> tuple[GenerationResidual, ...]:
        """بقايا الأثر كلُّها مرصودةً من خطواتها؛ ولا قائمةَ تُكتَب بجانبها."""

        return tuple(residual for step in self.steps for residual in step.residuals)

    @property
    def input_content_id(self) -> str:
        """مدخلُ الأثر: مدخلُ أوّل خطوةٍ فيه."""

        return self.steps[0].input_content_id

    @property
    def output_content_id(self) -> str | None:
        """مخرجُ الأثر: مخرجُ آخر خطوةٍ فيه، وقد يكون غيابًا مُسبَّبًا."""

        return self.steps[-1].output_content_id

    def as_canonical_content(self) -> dict[str, object]:
        """محتوى الأثر للبصمة."""

        return {"steps": [step.as_canonical_content() for step in self.steps]}

    @property
    def content_id(self) -> str:
        """بصمةُ الأثر مُشتَقّةً من محتواه؛ ولا تُكتَب من خارجه."""

        return canonical_digest(canonical_bytes(self.as_canonical_content()))
