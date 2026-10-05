"""قارئٌ صوريٌّ يكتب صفةَ الإعاقة نصًّا؛ و`"false"` ليست `False` فيُرفَض."""

from __future__ import annotations

import json
from collections.abc import Mapping


def read(payload_bytes: bytes, configuration: Mapping[str, str]) -> dict[str, object]:
    """يُعيد بقيّةً بصفةِ إعاقةٍ نصّيّة، وهي نوعٌ خاطئٌ يُرفَض ولا يُحوَّل."""

    payload = json.loads(payload_bytes.decode("utf-8"))
    members = payload["members"]
    left = members[0]
    return {
        "outputs": [
            [member["member_id"], member["observed_inputs"][0][1]]
            for member in members[1:]
        ],
        "residuals": [
            {
                "member_id": left["member_id"],
                "residual_code": "unclassified_by_reader",
                "blocking": "false",
                "reason": "صفةُ إعاقةٍ مكتوبةٌ نصًّا",
                "evidence_ref": "payload:members[0]",
            }
        ],
    }
