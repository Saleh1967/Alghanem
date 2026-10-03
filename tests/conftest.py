"""إلزامُ بروتوكول شرط العدّ قبل أيّ اختبارٍ في هذه الشجرة.

هذا الملفُّ هو **موضعُ الإلزام**: يُشغَّل مرّةً واحدةً عند بدء الجلسة، قبل أن
يُجمَع اختبارٌ أو يُنفَّذ. فإن لم ينفُذ البروتوكول — أي إن غاب موقعُ دالّة
التأسيس أو كُسر ختمُه — وقفت الجلسةُ كلُّها ولم يُعَدّ موضعٌ واحد.

ولا يُقرأ وقوفُ الجلسة حكمًا على العدّ: شرطُ الإمكان **غيرُ مستوفًى** اليوم
ومع ذلك تمرّ الجلسة، لأنّ الإلزامَ على الإجراء لا على المادّة
(`A_BINDING_PROTOCOL_IS_NOT_A_MET_PRECONDITION`).

وفيه أيضًا **إقحامُ جذر الشجرة في `sys.path`**: حزمةُ `canonical116` في الجذر
خارجَ `where = ["src"]`، فلا يُنصِّبها `pip install -e .`. وكان استيرادُها
يعمل عرَضًا حين تُشغَّل الجلسةُ بـ`python -m pytest` — إذ يُقحِم المفسِّرُ
المجلّدَ الحاليَّ — ويسقط حين تُشغَّل بـ`pytest` كما في CI. فالإقحامُ ههنا
تصريحٌ بالشرط بدل الاتّكال على طريقة الاستدعاء، ولا تُحذَف أسطرُه.
"""

from __future__ import annotations

import sys
from pathlib import Path
from typing import Any

_REPO_ROOT = Path(__file__).resolve().parents[1]
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))

from alghanem.arabic.counting_precondition_protocol import (  # noqa: E402
    require_the_protocol,
)


def pytest_sessionstart(session: Any) -> None:
    """يسبق كلَّ اختبارٍ في الجلسة؛ ويرفع خطأَ البروتوكول ولا يبتلعه."""

    del session
    require_the_protocol()
