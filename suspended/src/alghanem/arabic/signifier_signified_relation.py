"""المحورُ الثالث: **الدالُّ والمدلولُ معًا** — العلاقةُ السباعيّةُ المُبرهَنة.

التصنيفاتُ السبعةُ مُبرهَنةٌ في `lafz_madlul_relation_formal`، فيُستورَد
`LafzMadlulRelation` مجالًا مُغلَقًا ولا يُكتَب ثانيةً. وهذا المحورُ عن **حال
العلاقة**، لا عن تاريخ توليد اللفظ: `RelationStateIsNotGenerationHistory`، وذاك
في `lexical_path_candidate` وحده.

**والمجازُ يقتضي علاقةً مُرخَّصة**: `MajazRequiresLicensedRelation`. ولا يُبنى
مُرشَّحُ مجازٍ بغير مرجعِ علاقةٍ مُصرَّحٍ به؛ فالمشابهةُ المُستشعَرةُ ليست علاقةً
مُرخَّصة، وردُّها هنا بنيويٌّ لا تنبيهٌ يُكتَب.

**والحقيقةُ لا تُبهَم جنسُها**: `OriginalHaqiqahIsNotUrfiHaqiqah`. فمن ادّعى
حقيقةً صرّح بجنسها من `HaqiqaGenus`، ولا يُحمَل المسكوتُ عنه على «لغويّة».
وترتيبُ `HAQIQA_CASCADE_ORDER` مُسجَّلٌ غيرُ مُفعَّلٍ هناك، فلا يُفعَّل هنا.

**وشاهدُ الحرف علائقيّ**: `ParticleEvidenceIsRelationalNotIndependentLexicalMeaning`.
فمن حمل وقوعًا على `WordClass.HARF` لزمه مرجعُ ما تعلّق به الحرف، إذ معناه في
غيره لا في نفسه.

هذا المحورُ **لا يستورد** محورَ الدالّ ولا محورَ المدلول.

تسجيلٌ لا سلطة.
"""

from __future__ import annotations

from dataclasses import dataclass

from .lafz_madlul_relation_formal import HaqiqaGenus, LafzMadlulRelation
from .lexical_evidence_layer import PrimarySignificationAnchor
from .lexical_evidence_specification import (
    MAJAZ_REQUIRES_LICENSED_RELATION_NOTE,
    ORIGINAL_HAQIQAH_IS_NOT_URFI_HAQIQAH_NOTE,
    PARTICLE_EVIDENCE_IS_RELATIONAL_NOTE,
    PROVEN_VOCABULARY_IS_NOT_PROVEN_ASSIGNMENT_NOTE,
    RELATION_STATE_IS_NOT_GENERATION_HISTORY_NOTE,
)
from .word_class_formal import WordClass

__all__ = [
    "ParticleRelationalEvidence",
    "SignifierSignifiedRelationCandidate",
    "SignifierSignifiedRelationError",
]


class SignifierSignifiedRelationError(ValueError):
    """رفضٌ في محور العلاقة بين الدالّ والمدلول."""


def _require_text(value: str, label: str, note: str | None = None) -> None:
    if not isinstance(value, str) or not value.strip():
        message = f"{label} نصٌّ غير فارغ."
        raise SignifierSignifiedRelationError(
            message if note is None else f"{message} {note}"
        )


@dataclass(frozen=True, slots=True)
class SignifierSignifiedRelationCandidate:
    """مُرشَّحُ علاقةٍ: عضوٌ من السباعيّة، بشرطَي المجاز والحقيقة مُنفَّذَين."""

    anchor: PrimarySignificationAnchor
    relation: LafzMadlulRelation
    evidence_ref: str
    licensed_relation_ref: str | None = None
    haqiqa_genus: HaqiqaGenus | None = None

    def __post_init__(self) -> None:
        if not isinstance(self.anchor, PrimarySignificationAnchor):
            raise SignifierSignifiedRelationError(
                "مُرشَّحُ العلاقة إسقاطٌ عن مرساةٍ مُرخَّصة؛ "
                + PROVEN_VOCABULARY_IS_NOT_PROVEN_ASSIGNMENT_NOTE
            )
        if not isinstance(self.relation, LafzMadlulRelation):
            raise SignifierSignifiedRelationError("العلاقةُ عضوٌ في السباعيّة.")
        _require_text(self.evidence_ref, "مرجعُ الدليل")
        if self.relation is LafzMadlulRelation.MAJAZ:
            if self.licensed_relation_ref is None:
                raise SignifierSignifiedRelationError(
                    MAJAZ_REQUIRES_LICENSED_RELATION_NOTE
                )
            _require_text(
                self.licensed_relation_ref,
                "مرجعُ العلاقة المُرخَّصة",
                MAJAZ_REQUIRES_LICENSED_RELATION_NOTE,
            )
        elif self.licensed_relation_ref is not None:
            raise SignifierSignifiedRelationError(
                "مرجعُ العلاقة المُرخَّصة شرطُ المجاز وحدَه، فلا يُعلَّق بغيره."
            )
        if self.relation is LafzMadlulRelation.HAQIQA:
            if not isinstance(self.haqiqa_genus, HaqiqaGenus):
                raise SignifierSignifiedRelationError(
                    ORIGINAL_HAQIQAH_IS_NOT_URFI_HAQIQAH_NOTE
                )
        elif self.haqiqa_genus is not None:
            raise SignifierSignifiedRelationError(
                "جنسُ الحقيقة شرطُ الحقيقة وحدَها، فلا يُعلَّق بغيرها."
            )

    @property
    def is_generation_history(self) -> bool:
        """حالُ العلاقة ليس تاريخَ التوليد؛ الجوابُ ثابتٌ ومعه نصُّ فصله."""

        return False

    @property
    def separation_note(self) -> str:
        return RELATION_STATE_IS_NOT_GENERATION_HISTORY_NOTE


@dataclass(frozen=True, slots=True)
class ParticleRelationalEvidence:
    """شاهدُ الحرف: معناه في متعلَّقه، فمرجعُ المتعلَّق شرطٌ في بنيته."""

    anchor: PrimarySignificationAnchor
    attached_to_ref: str
    evidence_ref: str

    def __post_init__(self) -> None:
        if not isinstance(self.anchor, PrimarySignificationAnchor):
            raise SignifierSignifiedRelationError("شاهدُ الحرف إسقاطٌ عن مرساةٍ مُرخَّصة.")
        _require_text(
            self.attached_to_ref,
            "مرجعُ المتعلَّق",
            PARTICLE_EVIDENCE_IS_RELATIONAL_NOTE,
        )
        _require_text(self.evidence_ref, "مرجعُ الدليل")

    @property
    def word_class(self) -> WordClass:
        return WordClass.HARF

    @property
    def is_independent_lexical_meaning(self) -> bool:
        return False
