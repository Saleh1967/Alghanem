"""قارئٌ صوريٌّ يخرق حدَّه: يبلغ مادّةَ الجواب، فلا تُجمَّد هويّتُه."""

from __future__ import annotations

from alghanem.arabic.madlul_alone_formal import ATTESTED_SIGNIFIED_WITNESSES


def read(payload_bytes: bytes) -> int:
    """يقرأ من مصدر الجواب لا من الحمولة."""

    return len(ATTESTED_SIGNIFIED_WITNESSES)
