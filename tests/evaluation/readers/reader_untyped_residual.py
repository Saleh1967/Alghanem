"""قارئٌ صوريٌّ يترك بقيّةً برمزٍ خارج المفردة المغلقة؛ تُرفَض ولا تُقبَل نصًّا."""

from __future__ import annotations

import json
from collections.abc import Mapping


def read(payload_bytes: bytes, configuration: Mapping[str, str]) -> dict[str, object]:
    """يترك عضوًا برمزِ بقيّةٍ غيرِ مُصنَّف."""

    payload = json.loads(payload_bytes.decode("utf-8"))
    members = payload["members"]
    return {
        "outputs": [
            [member["member_id"], member["observed_inputs"][0][1]]
            for member in members[1:]
        ],
        "residuals": [
            {
                "member_id": members[0]["member_id"],
                "residual_code": "لم يعجبني",
                "blocking": False,
                "reason": "سببٌ حرّ",
                "evidence_ref": "لا شاهد",
            }
        ],
    }
