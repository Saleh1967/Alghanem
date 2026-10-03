"""مضمونُ الخطاب: ما ينسبه الكلامُ أو ينفيه أو يشترطه — منسوبًا إلى العبارة.

هذا **المستوى الثاني** من ثلاثة. ومخرجُه قولٌ منسوبٌ إلى عبارةٍ بعينها، لا
تقريرٌ عن الواقع: `AN_UTTERANCE_CONTENT_IS_NOT_A_CLAIM_ABOUT_THE_WORLD`.

**والمجهولُ غيرُ المنفيّ** (`AN_UNNAMED_PARTICIPANT_IS_NOT_A_DENIED_ONE`):
شاغلُ الدور إمّا مُعيَّنٌ بمرشَّحٍ أو أكثر، وإمّا **مجهولٌ مُصرَّحٌ به**، وإمّا
**منفيُّ الوجود بنصّ العبارة**. وثلاثتُها أعضاءٌ متمايزةٌ في مفردةٍ مغلقة؛
فـ«فُتح الباب» تُخرِج فاعلًا مجهولًا لا فاعلًا منفيًّا، و«انفتح الباب» لا
تُخرِج فاعلًا منفيًّا أصلًا بل تسكت عن موضع السبب.

**ونطاقُ النفي جزءٌ من المضمون** (`A_NEGATION_NAMES_ITS_SCOPE`): القطبيّةُ
وحدَها لا تكفي؛ `negation_scope` يُسمّي **ما الذي دخل تحت النفي** — أوقوعُ
الحدث كلِّه، أم شَغْلُ فردٍ بعينه لدورٍ بعينه — ونفيٌ بلا نطاقٍ مُسمًّى يُرفَض
عند الإنشاء.

**والجهةُ تُغيِّر التزامَ القول بالوقوع** (`A_CONDITIONAL_COMMITS_TO_NOTHING`):
`Modality.CONDITIONAL` تُخرِج `commits_to_occurrence = False` مع بقاء المضمون
كما هو؛ فتحويلُ النفي إلى شرطٍ يُغيِّر الالتزامَ ولا يُغيِّر الأطرافَ ولا
الأدوار، وهذا بعينه ما يُختبَر.

**وذِكرُ اسمٍ ليس إثباتًا لفرد** (`A_MENTION_IS_NOT_AN_EXISTENCE_CLAIM`):
`Designation` تحمل طريقةَ التعيين ومرشَّحي الإحالة، ولا تحمل حكمًا بوجود.

تسجيلٌ لا سلطة: لا ولادةَ ولا حكمَ ولادةٍ ولا تجميدَ `E0`.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Final

from ..canonical_content import canonical_bytes, canonical_digest
from .epistemics import Scope

__all__ = [
    "AN_UNNAMED_PARTICIPANT_IS_NOT_A_DENIED_ONE",
    "AN_UTTERANCE_CONTENT_IS_NOT_A_CLAIM_ABOUT_THE_WORLD",
    "A_CONDITIONAL_COMMITS_TO_NOTHING",
    "A_MENTION_IS_NOT_AN_EXISTENCE_CLAIM",
    "A_NEGATION_NAMES_ITS_SCOPE",
    "ContentError",
    "Designation",
    "DesignationMethod",
    "DiscourseContent",
    "EventContent",
    "FillerStanding",
    "Modality",
    "NegationScope",
    "Polarity",
    "RoleFilling",
]


class ContentError(ValueError):
    """رفضٌ بنيويٌّ في مضمون الخطاب؛ لا حملَ على أقرب حالة."""


AN_UTTERANCE_CONTENT_IS_NOT_A_CLAIM_ABOUT_THE_WORLD: Final[str] = (
    "مضمونُ العبارة منسوبٌ إليها لا تقريرٌ عن الواقع: من أودعه في سجلّ الوقائع "
    "بلا دليلٍ جعل الفهمَ تصديقًا، وأسقط الفرقَ بين أن تفهم قولًا وأن تقبله"
)

AN_UNNAMED_PARTICIPANT_IS_NOT_A_DENIED_ONE: Final[str] = (
    "المشاركُ غيرُ المُسمّى ليس مشاركًا منفيًّا: «فُتح الباب» تسكت عن الفاعل "
    "ولا تنفيه، و«انفتح الباب» لا تنفي وجودَ سببٍ بل لا تُسنِد إلى سببٍ معيَّن"
)

A_NEGATION_NAMES_ITS_SCOPE: Final[str] = (
    "النفيُ يُسمّي نطاقَه: نفيُ وقوعِ الحدث غيرُ نفيِ شَغْلِ فلانٍ دورَه، "
    "ونفيٌ بلا نطاقٍ مُسمًّى يُقرَأ على أوسع ما يحتمله قارئُه"
)

A_CONDITIONAL_COMMITS_TO_NOTHING: Final[str] = (
    "الشرطيُّ لا يلتزم بالوقوع: مضمونُه قائمٌ بأطرافه وأدواره، والتزامُ القائل "
    "بوقوعه ساقط؛ ومن أودعه واقعةً فكّ المضمونَ من شرطه بلا ترخيص"
)

A_MENTION_IS_NOT_AN_EXISTENCE_CLAIM: Final[str] = (
    "ورودُ الاسم في الخطاب ليس إثباتًا لوجود فردٍ في الواقع: التعيينُ طريقةٌ "
    "ومرشَّحون، وإثباتُ الوجود قضيّةٌ تحتاج دليلَها في سجلّ الوقائع"
)


class Polarity(Enum):
    """قطبيّةُ المضمون؛ عضوانِ لا ثالثَ لهما، ولا قيمةَ افتراضيّة."""

    AFFIRMED = "affirmed"
    NEGATED = "negated"

    @property
    def is_negated(self) -> bool:
        """أهي منفيّة؟ خاصّيّةٌ تُشتَقّ لا حقلٌ يُكتَب."""

        return self is Polarity.NEGATED


class NegationScope(Enum):
    """نطاقُ النفي؛ مُسمًّى دائمًا، وفيه عضوٌ للموجَب لا يُقرَأ نفيًا."""

    NOT_NEGATED = "not_negated"
    WHOLE_EVENT_OCCURRENCE = "whole_event_occurrence"
    ONE_ROLE_FILLING = "one_role_filling"


class Modality(Enum):
    """جهةُ القول؛ وفيها عضوُ جهلٍ مُصرَّحٌ به لا `None` صامتة."""

    ASSERTED = "asserted"
    CONDITIONAL = "conditional"
    INTERROGATED = "interrogated"
    UNREAD = "unread"

    @property
    def commits_to_occurrence(self) -> bool:
        """أيلتزم القائلُ بوقوع المضمون؟ الإخبارُ وحدَه، والمجهولُ لا يُقرَأ التزامًا."""

        return self is Modality.ASSERTED


class DesignationMethod(Enum):
    """طريقةُ تعيين الطرف؛ مفردةٌ مغلقةٌ فيها عضوُ جهل."""

    PROPER_NAME = "proper_name"
    DEFINITE_DESCRIPTION = "definite_description"
    INDEFINITE_DESCRIPTION = "indefinite_description"
    PRONOUN = "pronoun"
    UNREAD = "unread"


class FillerStanding(Enum):
    """منزلةُ شاغل الدور في المضمون؛ ثلاثةٌ متمايزةٌ لا يُبتلَع بعضُها في بعض."""

    DESIGNATED = "designated"
    UNNAMED_IN_THE_UTTERANCE = "unnamed_in_the_utterance"
    DENIED_BY_THE_UTTERANCE = "denied_by_the_utterance"
    ROLE_NOT_PROFILED = "role_not_profiled"


def _require_text(value: object, label: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise ContentError(f"{label} نصٌّ غير فارغ")
    return value


@dataclass(frozen=True, slots=True)
class Designation:
    """تعيينُ طرفٍ في الخطاب: لفظُه، وطريقتُه، ومرشَّحو إحالته — لا وجودُه."""

    surface: str
    method: DesignationMethod
    candidate_individual_ids: tuple[str, ...]

    def __post_init__(self) -> None:
        _require_text(self.surface, "لفظُ الطرف")
        if not isinstance(self.method, DesignationMethod):
            raise ContentError("طريقةُ التعيين عضوٌ في مفردتها المغلقة")
        if not isinstance(self.candidate_individual_ids, tuple):
            raise ContentError("مرشَّحو الإحالة صفٌّ مجمَّد")
        if len(set(self.candidate_individual_ids)) != len(
            self.candidate_individual_ids
        ):
            raise ContentError("مرشَّحٌ مكرَّرٌ في الإحالة يُرفَض لا يُطوى")

    @property
    def is_resolved(self) -> bool:
        """أانحصر التعيينُ في مرشَّحٍ واحد؟ والصفرُ والمتعدّدُ لا يُقرآنِ حصرًا."""

        return len(self.candidate_individual_ids) == 1

    def as_canonical_content(self) -> dict[str, object]:
        """محتوى التعيين للبصمة."""

        return {
            "surface": self.surface,
            "method": self.method.value,
            "candidate_individual_ids": list(self.candidate_individual_ids),
        }


@dataclass(frozen=True, slots=True)
class RoleFilling:
    """شَغْلُ دورٍ في مضمون حدث: الدورُ، ومنزلةُ شاغله، وتعيينُه إن كان مُعيَّنًا."""

    role_id: str
    standing: FillerStanding
    designation: Designation | None = None

    def __post_init__(self) -> None:
        _require_text(self.role_id, "مُعرِّفُ الدور")
        if not isinstance(self.standing, FillerStanding):
            raise ContentError(
                "منزلةُ الشاغل عضوٌ في مفردتها المغلقة؛ و"
                + AN_UNNAMED_PARTICIPANT_IS_NOT_A_DENIED_ONE
            )
        designated = self.standing is FillerStanding.DESIGNATED
        if designated and not isinstance(self.designation, Designation):
            raise ContentError("شاغلٌ مُعيَّنٌ بلا تعيينٍ مكتوب: منزلةٌ تُخالف حاملَها")
        if not designated and self.designation is not None:
            raise ContentError("تعيينٌ مكتوبٌ على شاغلٍ غيرِ مُعيَّن: حقلٌ لا يُقرأ")

    def as_canonical_content(self) -> dict[str, object]:
        """محتوى شَغْلِ الدور للبصمة."""

        return {
            "role_id": self.role_id,
            "standing": self.standing.value,
            "designation": (
                None
                if self.designation is None
                else self.designation.as_canonical_content()
            ),
        }


@dataclass(frozen=True, slots=True)
class EventContent:
    """مضمونُ حدثٍ كما تنسبه العبارة: نوعُه، وشاغلوه، وزمنُه، وقطبيّتُه، وجهتُه."""

    event_type_id: str
    role_fillings: tuple[RoleFilling, ...]
    time_scope: Scope
    polarity: Polarity
    negation_scope: NegationScope
    modality: Modality
    negated_role_id: str | None = None

    def __post_init__(self) -> None:
        _require_text(self.event_type_id, "نوعُ الحدث في المضمون")
        if not self.role_fillings:
            raise ContentError("مضمونُ الحدث شَغْلُ دورٍ فأكثر")
        seen: set[str] = set()
        for filling in self.role_fillings:
            if not isinstance(filling, RoleFilling):
                raise ContentError("عضوٌ في شواغل الأدوار خارج نوعه")
            if filling.role_id in seen:
                raise ContentError("دورٌ مكرَّرٌ في المضمون يُرفَض لا يُطوى")
            seen.add(filling.role_id)
        if not isinstance(self.time_scope, Scope):
            raise ContentError("زمنُ المضمون نطاقٌ قائم")
        for value, label, expected in (
            (self.polarity, "قطبيّةُ المضمون", Polarity),
            (self.negation_scope, "نطاقُ النفي", NegationScope),
            (self.modality, "جهةُ القول", Modality),
        ):
            if not isinstance(value, expected):
                raise ContentError(f"{label} عضوٌ في مفردته المغلقة")
        if self.polarity.is_negated:
            if self.negation_scope is NegationScope.NOT_NEGATED:
                raise ContentError(A_NEGATION_NAMES_ITS_SCOPE)
        elif self.negation_scope is not NegationScope.NOT_NEGATED:
            raise ContentError("نطاقُ نفيٍ على مضمونٍ موجَب: حقلٌ يُخالف قطبيّتَه")
        if self.negation_scope is NegationScope.ONE_ROLE_FILLING:
            _require_text(self.negated_role_id, "الدورُ الذي دخل تحت النفي")
            if self.negated_role_id not in seen:
                raise ContentError("نفيُ دورٍ ليس في المضمون: نطاقٌ بلا حامل")
        elif self.negated_role_id is not None:
            raise ContentError("دورٌ منفيٌّ مكتوبٌ خارج نطاقه: حقلٌ لا يُقرأ")

    def filling(self, role_id: str) -> RoleFilling:
        """شَغْلُ دورٍ بعينه؛ والغيابُ رفضٌ لا `None` يُقرأ سكوتًا."""

        for item in self.role_fillings:
            if item.role_id == role_id:
                return item
        raise ContentError(f"لا دورَ `{role_id}` في هذا المضمون")

    @property
    def commits_to_occurrence(self) -> bool:
        """أيلتزم القائلُ بوقوع هذا الحدث؟ إخبارٌ موجَبٌ لا شرطَ فيه ولا نفي."""

        return self.modality.commits_to_occurrence and not self.polarity.is_negated

    @property
    def commits_to_non_occurrence(self) -> bool:
        """أيلتزم القائلُ بعدم وقوعه كلِّه؟ نفيٌ إخباريٌّ نطاقُه الحدثُ كلُّه."""

        return (
            self.modality.commits_to_occurrence
            and self.polarity.is_negated
            and self.negation_scope is NegationScope.WHOLE_EVENT_OCCURRENCE
        )

    def as_canonical_content(self) -> dict[str, object]:
        """محتوى مضمون الحدث للبصمة."""

        return {
            "event_type_id": self.event_type_id,
            "role_fillings": [
                filling.as_canonical_content() for filling in self.role_fillings
            ],
            "time_scope": self.time_scope.as_canonical_content(),
            "polarity": self.polarity.value,
            "negation_scope": self.negation_scope.value,
            "modality": self.modality.value,
            "negated_role_id": self.negated_role_id,
        }


@dataclass(frozen=True, slots=True)
class DiscourseContent:
    """مضمونُ عبارةٍ بعينها، منسوبًا إليها ببصمة بايتاتها وبأثر جسرِه."""

    content_ref: str
    utterance_digest: str
    bridge_id: str
    event: EventContent

    def __post_init__(self) -> None:
        _require_text(self.content_ref, "مُعرِّفُ المضمون")
        _require_text(self.utterance_digest, "بصمةُ بايتات العبارة")
        _require_text(self.bridge_id, "مُعرِّفُ الجسر الذي بنى المضمون")
        if not isinstance(self.event, EventContent):
            raise ContentError("مضمونُ العبارة مضمونُ حدثٍ قائم")

    def as_canonical_content(self) -> dict[str, object]:
        """محتوى المضمون للبصمة."""

        return {
            "content_ref": self.content_ref,
            "utterance_digest": self.utterance_digest,
            "bridge_id": self.bridge_id,
            "event": self.event.as_canonical_content(),
        }

    @property
    def content_id(self) -> str:
        """بصمةُ المضمون؛ وتغييرُ العبارة أو الجسر يُغيِّرها."""

        return canonical_digest(canonical_bytes(self.as_canonical_content()))
