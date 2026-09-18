"""قارئٌ صوريٌّ تُقتَل عمليّتُه بإشارة؛ والقتلُ بإشارةٍ غيرُ الخروج برمزٍ غيرِ صفر."""

from __future__ import annotations

import os
import signal
from collections.abc import Mapping


def read(
    payload_bytes: bytes, configuration: Mapping[str, str]
) -> tuple[tuple[str, str], ...]:
    """يقتل عمليّتَه، فلا رمزَ خروجٍ عاديٌّ يُنسَب إليه."""

    os.kill(os.getpid(), signal.SIGKILL)
    return ()
