"""المحورُ الأوّل: **الدالُّ وحدَه** — مطابقةٌ وتضمُّنٌ والتزام، إسقاطًا عن المرساة.

الأقسامُ الثلاثةُ مُبرهَنةٌ في `dalalat_thalath`، فتُستورَد `DalalaKind` مجالًا
مُغلَقًا ولا تُكتَب هنا ثانيةً. و`ProvenVocabularyIsNotProvenAssignment`: كونُ
المفردة مُبرهَنةً لا يجعل حملَ عضوٍ منها على وقوعٍ بعينه واقعةً مُبرهَنة؛ فما
هنا مُرشَّحاتٌ تحمل عضوًا، لا إسناداتٌ ثبتت.

**وثلاثةُ أنواعٍ لا نوعٌ بحقلٍ ثلاثيّ**: النوعُ الواحد يجعل القسمَ قيمةً تُكتَب
ثمّ تُبدَّل، والشرطُ يُفحَص مرّةً واحدةً لثلاثة أقسامٍ شروطُها مختلفة. وكلُّ
نوعٍ هنا يحمل قسمَه خاصّيّةً مُشتقَّةً لا حقلًا، فلا يخالف مُرشَّحٌ قسمَه.

**وشرطان لا موجِبان**: `PartOfMeaningIsConditionNotGenerativeAuthority` و
`LazimIsConditionNotMujib` مُنفَّذان حرفيًّا: التضمُّنُ والالتزامُ لا يُبنى
واحدٌ منهما إلّا عن `PrimarySignificationAnchor` مُرخَّصةٍ سابقةٍ عليه؛ فجزئيّةُ
المعنى واللزومُ الذهنيُّ شرطان يُشترَطان، ولا يولِّد واحدٌ منهما مُرشَّحًا.

هذا المحورُ **لا يستورد** محورَ المدلول ولا محورَ العلاقة: استقلالُ السلطة يمنع
الاستيراد، وإن كانت المادّةُ واحدةً في المرساة
(`AxesAreIndependentInAuthorityNotInData`).

تسجيلٌ لا سلطة.
"""

from __future__ import annotations

from dataclasses import dataclass

from .dalalat_thalath import (
    ILTIZAM_CONDITION_IS_NOT_ITS_CAUSE_NOTE,
    DalalaKind,
)
from .lexical_evidence_layer import PrimarySignificationAnchor
from .lexical_evidence_specification import (
    LAZIM_IS_CONDITION_NOT_MUJIB_NOTE,
    PART_OF_MEANING_IS_CONDITION_NOT_GENERATIVE_AUTHORITY_NOTE,
    PROVEN_VOCABULARY_IS_NOT_PROVEN_ASSIGNMENT_NOTE,
)

__all__ = [
    "IltizamCandidate",
    "MutabaqaCandidate",
    "SignifierAlgebraError",
    "TadammunCandidate",
    "refuse_lazim_without_anchor",
    "refuse_part_of_meaning_without_anchor",
]


class SignifierAlgebraError(ValueError):
    """رفضٌ في محور الدالّ وحدَه."""


def _require_anchor(anchor: PrimarySignificationAnchor) -> None:
    if not isinstance(anchor, PrimarySignificationAnchor):
        raise SignifierAlgebraError(
            "كلُّ مُرشَّحٍ في هذا المحور إسقاطٌ عن مرساةٍ مُرخَّصة؛ "
            + PROVEN_VOCABULARY_IS_NOT_PROVEN_ASSIGNMENT_NOTE
        )


def _require_text(value: str, label: str) -> None:
    if not isinstance(value, str) or not value.strip():
        raise SignifierAlgebraError(f"{label} نصٌّ غير فارغ.")


def refuse_part_of_meaning_without_anchor(anchor: object) -> None:
    """ارفض جزئيّةَ معنًى تُقدَّم مولِّدةً لتضمُّنٍ بلا مرساةٍ سابقة."""

    if not isinstance(anchor, PrimarySignificationAnchor):
        raise SignifierAlgebraError(
            PART_OF_MEANING_IS_CONDITION_NOT_GENERATIVE_AUTHORITY_NOTE
        )


def refuse_lazim_without_anchor(anchor: object) -> None:
    """ارفض لازمًا ذهنيًّا يُقدَّم مولِّدًا لالتزامٍ بلا مرساةٍ سابقة."""

    if not isinstance(anchor, PrimarySignificationAnchor):
        raise SignifierAlgebraError(LAZIM_IS_CONDITION_NOT_MUJIB_NOTE)


@dataclass(frozen=True, slots=True)
class MutabaqaCandidate:
    """مُرشَّحُ مطابقةٍ: الدالُّ على تمام ما وُضع له، إسقاطًا عن المرساة."""

    anchor: PrimarySignificationAnchor
    evidence_ref: str

    def __post_init__(self) -> None:
        _require_anchor(self.anchor)
        _require_text(self.evidence_ref, "مرجعُ الدليل")

    @property
    def proposed_kind(self) -> DalalaKind:
        return DalalaKind.مطابقة


@dataclass(frozen=True, slots=True)
class TadammunCandidate:
    """مُرشَّحُ تضمُّن: الجزءُ المُدَّعى مُسمًّى، والمرساةُ شرطٌ سابقٌ عليه.

    والجزءُ نصٌّ يُصرَّح به لا يُستنبَط، لأنّ استنباطه هنا جعلٌ للجزئيّة
    مولِّدةً، وهو عينُ ما يمنعه الشرط.
    """

    anchor: PrimarySignificationAnchor
    claimed_part: str
    evidence_ref: str

    def __post_init__(self) -> None:
        refuse_part_of_meaning_without_anchor(self.anchor)
        _require_text(self.claimed_part, "الجزءُ المُدَّعى")
        _require_text(self.evidence_ref, "مرجعُ الدليل")

    @property
    def proposed_kind(self) -> DalalaKind:
        return DalalaKind.تضمن

    @property
    def condition_note(self) -> str:
        return PART_OF_MEANING_IS_CONDITION_NOT_GENERATIVE_AUTHORITY_NOTE


@dataclass(frozen=True, slots=True)
class IltizamCandidate:
    """مُرشَّحُ التزام: اللازمُ الذهنيُّ مُسمًّى، والمرساةُ شرطٌ سابقٌ عليه.

    ولا يُقرَأ لزومًا منطقيًّا: `IltizamIsNotLogicalEntailment` مُقرَّرٌ في
    `dalalat_thalath`، ويُقرأ من هناك لا يُعاد تهجئته هنا.
    """

    anchor: PrimarySignificationAnchor
    claimed_lazim: str
    evidence_ref: str

    def __post_init__(self) -> None:
        refuse_lazim_without_anchor(self.anchor)
        _require_text(self.claimed_lazim, "اللازمُ المُدَّعى")
        _require_text(self.evidence_ref, "مرجعُ الدليل")

    @property
    def proposed_kind(self) -> DalalaKind:
        return DalalaKind.التزام

    @property
    def condition_note(self) -> str:
        return ILTIZAM_CONDITION_IS_NOT_ITS_CAUSE_NOTE
