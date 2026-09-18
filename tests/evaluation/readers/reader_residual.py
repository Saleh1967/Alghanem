"""قارئٌ صوريٌّ يترك عضوًا ويُسمّي بقيّتَه برمزٍ وسببٍ وشاهد، لا بنصٍّ حرّ."""

from __future__ import annotations

import json


def read(payload_bytes: bytes) -> dict[str, object]:
    """صنِّف ما عدا أوّلَ عضو، واترك الأوّلَ بقيّةً مُعيقةً مُسمّاة."""

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
                "blocking": True,
                "reason": "مدخلاتُه المرصودةُ لا تُميِّز قسمًا واحدًا",
                "evidence_ref": "payload:members[0].observed_inputs",
            }
        ],
    }
