"""قارئٌ صوريٌّ يترك عضوًا بلا بقيّةٍ؛ فالتغطيةُ تامّةٌ لا أحسنُ جهد."""

from __future__ import annotations

import json
from collections.abc import Mapping


def read(
    payload_bytes: bytes, configuration: Mapping[str, str]
) -> tuple[tuple[str, str], ...]:
    """يُصنِّف ما عدا أوّلَ عضو، ولا يُسمّي له بقيّة."""

    payload = json.loads(payload_bytes.decode("utf-8"))
    return tuple(
        (member["member_id"], member["observed_inputs"][0][1])
        for member in payload["members"][1:]
    )
