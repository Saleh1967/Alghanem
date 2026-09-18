"""منزلةُ الإدخال: أصالحةٌ القضيّةُ لأن تُحكَم أصلًا؟

    InputStanding  =  VALID | INVALID

**وفسادُ الإدخال ليس حجبًا** (`InvalidInputIsNotABlock`): وثيقةٌ مفتاحُها
مجهولٌ، أو حقلُها المطلوبُ غائب، أو نوعُها غيرُ قانونيّ، أو بصمتُها المُعلَنة
تخالف بصمةَ محتواها المُعاد حسابُه — كلُّ ذلك عجزٌ عن تكوين قضيّةٍ قابلةٍ
للحكم، لا مخالفةٌ ثبتت بعد أن أصبح الحكمُ ممكنًا. ولذلك لا يحمل هذا النوعُ
حقلَ `ExecutionOutcome` أصلًا: الخلطُ غيرُ قابلٍ للقول لا مرفوضٌ بعد وقوعه.

تسجيلٌ لا سلطة: لا ولادةَ ولا حكمَ ولادةٍ ولا تجميدَ `E0`.
"""

from __future__ import annotations

from dataclasses import dataclass, fields
from enum import Enum
from typing import Final

__all__ = [
    "INVALID_INPUT_IS_NOT_A_BLOCK",
    "InputFault",
    "InputFaultKind",
    "InputStanding",
    "InputValidation",
]


INVALID_INPUT_IS_NOT_A_BLOCK: Final[str] = (
    "فسادُ الإدخال ليس حجبًا: الأوّلُ عجزٌ عن تكوين قضيّةٍ قابلةٍ للحكم، "
    "والثاني مخالفةٌ ثبتت بعد أن أصبح الحكمُ ممكنًا؛ ومن جمعهما أصدر حكمًا "
    "على ما لم يستطع أن يقرأه"
)


class InputStanding(Enum):
    """منزلةُ الوثيقة قبل الحكم؛ مفردةٌ مغلقةٌ لا ثالثَ لها."""

    VALID = "valid"
    INVALID = "invalid"


class InputFaultKind(Enum):
    """أجناسُ فساد الإدخال؛ مفردةٌ مغلقةٌ، ولا واحدَ منها يُقرَأ حكمًا."""

    UNKNOWN_KEY = "unknown_key"
    MISSING_REQUIRED_FIELD = "missing_required_field"
    ILLEGAL_TYPE = "illegal_type"
    UNKNOWN_SCHEMA = "unknown_schema"
    UNKNOWN_VOCABULARY_MEMBER = "unknown_vocabulary_member"
    DUPLICATE_DECLARED_ID = "duplicate_declared_id"
    UNRESOLVABLE_INTERNAL_REFERENCE = "unresolvable_internal_reference"
    DECLARED_CONTENT_ID_DISAGREES = "declared_content_id_disagrees"
    UNDECLARED_ABSENT_SITE = "undeclared_absent_site"
    MALFORMED_DECLARED_CONTENT = "malformed_declared_content"


@dataclass(frozen=True, slots=True)
class InputFault:
    """عيبُ إدخالٍ واحد: جنسُه، وموضعُه؛ ولا نصَّ حرًّا يفسّره."""

    kind: InputFaultKind
    site: str

    def __post_init__(self) -> None:
        if not isinstance(self.kind, InputFaultKind):
            raise TypeError("جنسُ العيب عضوٌ في مفردته المغلقة")
        if not isinstance(self.site, str) or not self.site.strip():
            raise TypeError("موضعُ العيب نصٌّ غير فارغ")

    def as_canonical_content(self) -> dict[str, object]:
        """محتوى العيب للبصمة."""

        return {"kind": self.kind.value, "site": self.site}


@dataclass(frozen=True, slots=True)
class InputValidation:
    """نتيجةُ عقد الإدخال؛ ولا حقلَ حكمٍ فيها ألبتّة."""

    standing: InputStanding
    faults: tuple[InputFault, ...]

    def __post_init__(self) -> None:
        if not isinstance(self.standing, InputStanding):
            raise TypeError("منزلةُ الإدخال عضوٌ في مفردتها المغلقة")
        if not isinstance(self.faults, tuple):
            raise TypeError("عيوبُ الإدخال مجموعةٌ مُصرَّحٌ بها")
        for fault in self.faults:
            if not isinstance(fault, InputFault):
                raise TypeError("عضوٌ في عيوب الإدخال خارج نوعه")
        if (self.standing is InputStanding.INVALID) != bool(self.faults):
            raise TypeError(
                "الفسادُ يُسمّي عيوبَه، والصحّةُ لا عيبَ فيها؛ و"
                + INVALID_INPUT_IS_NOT_A_BLOCK
            )

    @property
    def is_valid(self) -> bool:
        """أصالحةٌ القضيّةُ لأن تُحكَم؟ خاصّيّةٌ تُشتَقّ لا حقلٌ يُكتَب."""

        return self.standing is InputStanding.VALID

    def as_canonical_content(self) -> dict[str, object]:
        """محتوى التحقّق للبصمة؛ والعيوبُ مرتَّبةٌ ترتيبًا لا يتبع مصادفةً."""

        return {
            "standing": self.standing.value,
            "faults": [
                fault.as_canonical_content()
                for fault in sorted(
                    self.faults, key=lambda item: (item.kind.value, item.site)
                )
            ],
        }


def _refuse_an_outcome_field_in_the_input_stage() -> None:
    """لا حقلَ حكمٍ في طبقة الإدخال؛ فالخلطُ يُمنَع بالنوع لا بالانتباه."""

    for owner in (InputFault, InputValidation):
        for owner_field in fields(owner):
            lowered = owner_field.name.lower()
            for marker in ("outcome", "verdict", "block", "defer"):
                if marker in lowered:  # pragma: no cover - import guard
                    raise RuntimeError(INVALID_INPUT_IS_NOT_A_BLOCK)


_refuse_an_outcome_field_in_the_input_stage()
