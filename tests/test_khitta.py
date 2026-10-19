"""خطّةُ المهامّ مودَعةً بلفظها (STEP-0004).

* النصُّ بين العلامتين بصمتُه بصمةُ القسم في سجلّ الجلسة الخام
  (حُسبت بأداةٍ في الجلسة؛ السجلُّ ليس في المستودع).
* جدولُ الحال معلن؛ والمفحوصُ منه أنّ لكلّ مهمّةٍ صفًّا، وأنّ كلَّ دَينٍ يذكره موجودٌ باسمه
  في ADR ١١١ أو ١١٢ أو ١١٤ أو ١١٥.
"""

from __future__ import annotations

import hashlib
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
KHITTA = (ROOT / "docs" / "protocol" / "khitta.md").read_text(encoding="utf-8")
# بصمةُ القسم في سجلّ الجلسة الخام.
SHA = "5566aa132502896be735763c54ebce0bebf05aa676b11faa0b42e06d711d16a9"


def block() -> str:
    a = "<!-- نصّ الخطّة: بدء -->\n"
    b = "<!-- نصّ الخطّة: نهاية -->"
    return KHITTA[KHITTA.index(a) + len(a):KHITTA.index(b)]


def test_block_verbatim() -> None:
    assert hashlib.sha256(block().encode("utf-8")).hexdigest() == SHA
    assert SHA in KHITTA


def test_block_edit_refused() -> None:
    """ختمٌ لا مطابقة: تغييرُ حرفٍ في النصّ المودَع يُسقط `test_block_verbatim`.

    وهذا تحصيلُ خاصّيّة البصمة (معلن)، لا طفرةٌ على شيفرة.
    """
    b = block().replace("مهمّةٌ واحدة", "مهمّتان", 1)
    assert hashlib.sha256(b.encode("utf-8")).hexdigest() != SHA


def test_status_rows() -> None:
    status = KHITTA[KHITTA.index("## حالُ كلّ مهمّة"):]
    for n in range(1, 8):
        assert f"\n| {n} |" in status, n
    adrs = "".join((ROOT / "docs" / "adr" / f).read_text(encoding="utf-8")
                   for f in ("0111-protocol-tafrat.md", "0112-mantuq-mafhum.md",
                             "0114-silsila.md", "0115-silsila-furu.md"))
    debts = re.findall(r"`([A-Z][A-Z_]{5,})`", status)
    assert len(debts) >= 8
    for d in debts:
        assert f"`{d}`" in adrs, d
