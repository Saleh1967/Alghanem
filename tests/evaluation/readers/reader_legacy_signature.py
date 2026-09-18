"""قارئٌ صوريٌّ بتوقيعٍ مهجور: يستلم البايتاتِ ولا يستلم الإعداد، فيُرفَض مُسمًّى."""

from __future__ import annotations

import json


def read(payload_bytes: bytes) -> tuple[tuple[str, str], ...]:
    """توقيعٌ برقمٍ واحد؛ ولا يُنادى بأقرب شكلٍ ولا يُقبَل طريقًا مهجورًا."""

    payload = json.loads(payload_bytes.decode("utf-8"))
    return tuple(
        (member["member_id"], member["observed_inputs"][0][1])
        for member in payload["members"]
    )
