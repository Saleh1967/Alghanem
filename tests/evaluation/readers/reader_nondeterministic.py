"""قارئٌ صوريٌّ غيرُ حتميّ: يُصنِّف بما يقرؤه من ساعةِ العمليّة لا من الحمولة."""

from __future__ import annotations

import json
import time


def read(payload_bytes: bytes) -> tuple[tuple[str, str], ...]:
    """يُصنِّف كلَّ عضوٍ بقيمةٍ تتغيّر بين تشغيلين."""

    payload = json.loads(payload_bytes.decode("utf-8"))
    stamp = str(time.time_ns())
    return tuple((member["member_id"], stamp) for member in payload["members"])
