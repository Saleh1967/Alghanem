"""قارئٌ صوريٌّ يُصنِّف عضوًا ويتركه بقيّةً معًا؛ والجمعُ بينهما يُرفَض."""

from __future__ import annotations

import json
from collections.abc import Mapping


def read(payload_bytes: bytes, configuration: Mapping[str, str]) -> dict[str, object]:
    """يُصنِّف كلَّ عضوٍ ثمّ يترك أوّلَهم بقيّةً في الوقت نفسه."""

    payload = json.loads(payload_bytes.decode("utf-8"))
    members = payload["members"]
    return {
        "outputs": [
            [member["member_id"], member["observed_inputs"][0][1]] for member in members
        ],
        "residuals": [
            {
                "member_id": members[0]["member_id"],
                "residual_code": "unclassified_by_reader",
                "blocking": False,
                "reason": "صنَّفتُه وتركتُه معًا",
                "evidence_ref": "stdout:residuals[0]",
            }
        ],
    }
