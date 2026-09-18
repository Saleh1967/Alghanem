"""قارئٌ صوريٌّ يرفع خطأً: يُوصَل حدثُه بإيصالٍ ولا يُرقّى إلى تشغيلٍ مرجعيّ."""

from __future__ import annotations

from collections.abc import Mapping


def read(
    payload_bytes: bytes, configuration: Mapping[str, str]
) -> tuple[tuple[str, str], ...]:
    """يرفع خطأً بدل أن يُصنِّف، فيُسمّى حالُ خروجه ولا يُطوى."""

    raise RuntimeError("قارئٌ لم يُكمِل قراءتَه")
