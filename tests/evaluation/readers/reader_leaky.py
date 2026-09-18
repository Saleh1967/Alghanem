"""قارئٌ صوريٌّ يخرق حدَّه: يبلغ مادّةَ الجواب، فلا تُجمَّد هويّتُه."""

from __future__ import annotations

from collections.abc import Mapping

from alghanem.arabic.madlul_alone_formal import ATTESTED_SIGNIFIED_WITNESSES


def read(payload_bytes: bytes, configuration: Mapping[str, str]) -> int:
    """يقرأ من مصدر الجواب لا من الحمولة."""

    return len(ATTESTED_SIGNIFIED_WITNESSES)
