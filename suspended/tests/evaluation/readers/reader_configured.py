"""قارئٌ صوريٌّ يُصنِّف بإعداده المُسلَّم: فالإعدادُ يُنفَّذ لا يُهوَّى وحده."""

from __future__ import annotations

import json
from collections.abc import Mapping


def read(
    payload_bytes: bytes, configuration: Mapping[str, str]
) -> tuple[tuple[str, str], ...]:
    """اقرأ موضعَ المدخل المرصود من الإعداد، ولا تُخمِّنه ولا تُثبِّته."""

    index = int(configuration["observed_input_index"])
    payload = json.loads(payload_bytes.decode("utf-8"))
    return tuple(
        (member["member_id"], member["observed_inputs"][index][1])
        for member in payload["members"]
    )
