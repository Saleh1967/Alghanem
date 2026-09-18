"""قارئٌ صوريٌّ يرفع خطأً: يُوصَل حدثُه بإيصالٍ ولا يُرقّى إلى تشغيلٍ مرجعيّ."""

from __future__ import annotations


def read(payload_bytes: bytes) -> tuple[tuple[str, str], ...]:
    """يرفع خطأً بدل أن يُصنِّف، فيُسمّى حالُ خروجه ولا يُطوى."""

    raise RuntimeError("قارئٌ لم يُكمِل قراءتَه")
