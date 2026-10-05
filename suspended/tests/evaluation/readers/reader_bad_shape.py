"""قارئٌ صوريٌّ يُعيد شكلًا خارج القناة المغلقة؛ يُرفَض ولا يُحمَل على أقربه."""

from __future__ import annotations

from collections.abc import Mapping


def read(payload_bytes: bytes, configuration: Mapping[str, str]) -> str:
    """يُعيد نصًّا حرًّا بدل أزواج التصنيف، وهو شكلٌ لا تنقله القناة."""

    return "صنّفتُ كلَّ شيءٍ على ما أظنّ"
