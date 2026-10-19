"""قارئٌ صوريٌّ أوّل: يقرأ بايتاتٍ مُسلسَلةً ولا يبلغ مادّةَ المجال ولا سلطةَ فتحه."""

from __future__ import annotations

import json
from collections.abc import Mapping


def read(
    payload_bytes: bytes, configuration: Mapping[str, str]
) -> tuple[tuple[str, str], ...]:
    """صنِّف أعضاءَ الحمولة بقراءة مدخلاتها المرصودة وحدها."""

    payload = json.loads(payload_bytes.decode("utf-8"))
    return tuple(
        (member["member_id"], member["observed_inputs"][0][1])
        for member in payload["members"]
    )
