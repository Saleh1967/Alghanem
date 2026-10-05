"""بروتوكولُ الأصل العربيِّ المعياريِّ القابل للعدّ — A116-CANONICAL-TXT-1.0.

الجسرُ المرجعيُّ في `canonical116.bridge`، وبوّابةُ العدّ الوحيدة
`canonical116.count_atoms`. والمقصودُ بالأصل ههنا تمثيلٌ نصّيٌّ مُفكَّكٌ مع
سجلِّ الهويّة والأدوار، لا الجذرُ الصرفيُّ ولا استعادةُ صورةٍ تاريخيّةٍ مجهولة.
"""

from __future__ import annotations

from .bridge import (
    A116,
    ALPHABET,
    HARAKAT,
    PROTOCOL_VERSION,
    BridgeStatus,
    bridge,
    count_atoms,
    verify,
)

__all__ = [
    "A116",
    "ALPHABET",
    "HARAKAT",
    "PROTOCOL_VERSION",
    "BridgeStatus",
    "bridge",
    "count_atoms",
    "verify",
]
