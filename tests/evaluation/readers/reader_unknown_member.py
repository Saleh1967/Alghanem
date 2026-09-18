"""قارئٌ صوريٌّ يُصنِّف عضوًا خارج المجال؛ يُرفَض باسم حاله المُسمّى."""

from __future__ import annotations

import json
from collections.abc import Mapping


def read(
    payload_bytes: bytes, configuration: Mapping[str, str]
) -> tuple[tuple[str, str], ...]:
    """يُضيف عضوًا ليس في الحمولة إلى تصنيفاته."""

    payload = json.loads(payload_bytes.decode("utf-8"))
    classified = [
        (member["member_id"], member["observed_inputs"][0][1])
        for member in payload["members"]
    ]
    classified.append(("عضوٌ ليس في المجال", "تصنيفٌ لا مجالَ له"))
    return tuple(classified)
