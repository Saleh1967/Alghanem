"""قارئٌ صوريٌّ يتجاوز السقفَ الزمنيّ؛ ويُسمّى حالُه ولا يُطوى في خروجٍ غيرِ صفر."""

from __future__ import annotations

import time
from collections.abc import Mapping


def read(
    payload_bytes: bytes, configuration: Mapping[str, str]
) -> tuple[tuple[str, str], ...]:
    """ينام فوق السقف المُعلَن، فلا يُنتِج ناتجًا ولا يخرج برمز."""

    time.sleep(float(configuration["sleep_seconds"]))
    return ()
