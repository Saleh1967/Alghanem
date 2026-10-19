"""الاختباراتُ تُشغَّل من جذر الشجرة؛ والبوّابةُ تُبنى مرّةً لكلّ الجلسة."""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
