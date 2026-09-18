"""إعادةُ التشغيل: من التصريح المحفوظ في الغلاف، لا من بصمةٍ يتعذّر عكسُها.

    ExecutionResultEnvelope  →  declaration_document  →  ExecutionReport

**ونفسُ المدخل ونفسُ القوانين نفسُ النتيجة** (`SameInputSameLawsSameResult`):
لا وقتَ ولا عشوائيَّ ولا بيئةَ في محتوى النتيجة؛ فبصمةُ التنفيذ تتكرّر بايتًا
بايت. واختلافُ البصمة عند إعادة التشغيل دليلٌ على تغيّر قانونٍ أو مدخل، لا
على «تقلّبٍ» مقبول.

تسجيلٌ لا سلطة: لا ولادةَ ولا حكمَ ولادةٍ ولا تجميدَ `E0`.
"""

from __future__ import annotations

from typing import Final

from .engine import ExecutionReport, execute_document
from .result import ExecutionResultEnvelope

__all__ = [
    "SAME_INPUT_SAME_LAWS_SAME_RESULT",
    "is_reproducible",
    "replay",
]


SAME_INPUT_SAME_LAWS_SAME_RESULT: Final[str] = (
    "نفسُ المدخل ونفسُ القوانين نفسُ النتيجة ونفسُ الأثر: لا وقتَ ولا عشوائيَّ "
    "ولا بيئةَ في محتوى النتيجة، واختلافُ البصمة دليلُ تغيُّرٍ لا تقلُّبٍ مقبول"
)


def replay(envelope: ExecutionResultEnvelope) -> ExecutionReport:
    """أعِد التنفيذَ من التصريح المحفوظ؛ ولا يُقرَأ الحكمُ السابقُ مدخلًا."""

    if not isinstance(envelope, ExecutionResultEnvelope):
        raise TypeError("إعادةُ التشغيل تكون من غلافٍ قائمٍ لا من وصفٍ حرّ")
    return execute_document(envelope.declaration_document)


def is_reproducible(envelope: ExecutionResultEnvelope) -> bool:
    """أتُعاد النتيجةُ نفسُها بأثرها؟ والمقارنةُ ببصمة التنفيذ لا بالحكم وحدَه."""

    replayed = replay(envelope).envelope
    if replayed is None:
        return False
    return replayed.execution_digest == envelope.execution_digest
