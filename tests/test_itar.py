"""الأطرُ الثلاثة (ADR ١٠٤، `A116/Itar.lean`): ترخيصُ الدالّ في شواهد Lean يُعاد بمُقطِّع البوّابة.

التوقّعاتُ مكتوبةٌ هنا باليد من قول الشواهد، والحكمُ على الخانات من `gate.licence` لا من Lean.
"""

from __future__ import annotations

import re
from pathlib import Path

from gate.licence import strict_joined

ROOT = Path(__file__).resolve().parents[1]
LEAN = ROOT / "formal/a116/A116/Itar.lean"
SUKUN = "ْ"

# (اليسار، اليمين، الموضع، الترخيص المتوقّع، الحكم المتوقّع) — من نصّ الشواهد.
SHAWAHID = [
    ("نَطَقَ", "لْوَلَدُ", "wasl", True, "haqiqa"),
    ("نَبَحَ", "لْكَلْبُ", "wasl", True, "majaz"),
    ("فِيْ", "دَاْرِ", "wasl", True, "laHukm"),
    ("نْطَقَ", "لْوَلَدُ", "ibtida", False, None),
]


def atoms(s: str) -> tuple[str, ...]:
    assert len(s) % 2 == 0, s
    return tuple(s[i:i + 2] for i in range(0, len(s), 2))


def dal(p: str, left: str, right: str, ibtida_open: bool = False) -> bool:
    a, b = atoms(left), atoms(right)
    if p == "ibtida":
        return ibtida_open or not a[0].endswith(SUKUN)
    assert p == "wasl"
    return strict_joined(a, b)


def test_shawahid_in_lean() -> None:
    text = LEAN.read_text(encoding="utf-8")
    for left, right, _, _, _ in SHAWAHID:
        assert f'k "{left}"' in text and f'k "{right}"' in text
    assert "⟨true, some .haqiqa⟩" in text and "⟨true, some .majaz⟩" in text
    assert "⟨false, none⟩" in text
    assert re.search(r"theorem shawahid\b", text)


def test_dal_by_gate() -> None:
    for left, right, p, tarkhis, _ in SHAWAHID:
        assert dal(p, left, right) is tarkhis, (left, right, p)


def test_mutant_ibtida_open() -> None:
    # MUTANT_IBTIDA_OPEN: الابتداءُ مفتوحٌ لكلّ شيء — يُكشف بـ«نْطَقَ».
    got = [dal(p, a, b, ibtida_open=True) for a, b, p, _, _ in SHAWAHID]
    assert got != [t for _, _, _, t, _ in SHAWAHID]
