"""إلزامُ بروتوكول شرط العدّ قبل أيّ اختبارٍ في هذه الشجرة.

هذا الملفُّ هو **موضعُ الإلزام**: يُشغَّل مرّةً واحدةً عند بدء الجلسة، قبل أن
يُجمَع اختبارٌ أو يُنفَّذ. فإن لم ينفُذ البروتوكول — أي إن غاب موقعُ دالّة
التأسيس أو كُسر ختمُه — وقفت الجلسةُ كلُّها ولم يُعَدّ موضعٌ واحد.

ولا يُقرأ وقوفُ الجلسة حكمًا على العدّ: شرطُ الإمكان **غيرُ مستوفًى** اليوم
ومع ذلك تمرّ الجلسة، لأنّ الإلزامَ على الإجراء لا على المادّة
(`A_BINDING_PROTOCOL_IS_NOT_A_MET_PRECONDITION`).
"""

from __future__ import annotations

import sys
from pathlib import Path
from typing import Any

# حزمةُ canonical116 في جذر المستودع، وليست من الوحدات المُنصَّبة (`where = ["src"]`)؛
# فمن استوردها من داخل الشجرة لم يجدها، لأنّ pytest يُقحم مجلّدَ ملفّ الاختبار لا
# الجذر. فيُقحَم الجذرُ ههنا مرّةً واحدة، ولا يُقرأ ذلك تنصيبًا: الحزمةُ تبقى خارج
# `testpaths` وتُشغَّل اختباراتُها بـ`python -m unittest` كما كانت.
_REPO_ROOT = Path(__file__).resolve().parent.parent
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))

from alghanem.arabic.counting_precondition_protocol import (  # noqa: E402
    require_the_protocol,
)


def pytest_sessionstart(session: Any) -> None:
    """يسبق كلَّ اختبارٍ في الجلسة؛ ويرفع خطأَ البروتوكول ولا يبتلعه."""

    del session
    require_the_protocol()
