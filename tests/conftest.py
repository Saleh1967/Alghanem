"""إلزامُ بروتوكول شرط العدّ قبل أيّ اختبارٍ في هذه الشجرة.

هذا الملفُّ هو **موضعُ الإلزام**: يُشغَّل مرّةً واحدةً عند بدء الجلسة، قبل أن
يُجمَع اختبارٌ أو يُنفَّذ. فإن لم ينفُذ البروتوكول — أي إن غاب موقعُ دالّة
التأسيس أو كُسر ختمُه — وقفت الجلسةُ كلُّها ولم يُعَدّ موضعٌ واحد.

ولا يُقرأ وقوفُ الجلسة حكمًا على العدّ: شرطُ الإمكان **غيرُ مستوفًى** اليوم
ومع ذلك تمرّ الجلسة، لأنّ الإلزامَ على الإجراء لا على المادّة
(`A_BINDING_PROTOCOL_IS_NOT_A_MET_PRECONDITION`).
"""

from __future__ import annotations

from typing import Any

from alghanem.arabic.counting_precondition_protocol import require_the_protocol


def pytest_sessionstart(session: Any) -> None:
    """يسبق كلَّ اختبارٍ في الجلسة؛ ويرفع خطأَ البروتوكول ولا يبتلعه."""

    del session
    require_the_protocol()
