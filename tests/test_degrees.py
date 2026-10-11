"""جداولُ الدرجات (`A116.Exhaust`، ADR ١٥): الاستنفادُ درجةً درجة قبل الانتقال.

١. المطابقة: `gate.degrees.table` = `Exhaust.table` على جدول `lake exe a116-table degrees`
   (255 سطرًا مودَعًا يطابقه CI بايتًا بايتًا): الدرجةُ والعددُ والمقاطع.
٢. الطفرتان: مرآةٌ تقبل CVVC طرفًا (`MUTANT_CVVC_FINAL`) ومرآةٌ تعدّ الأحدثَ أعلى
   (`MUTANT_LITTLE_ENDIAN`) يُسقطهما الجدول.
٣. البوّابة: توقّعاتٌ محسوبةٌ باليد من التقطيع لا من الشيفرة — مِنْ ← (1، 2، CVC)؛ كَتَبَ ← (3، 0)؛
   عَلَيْهِمْ ← عَ | لَيْ | هِمْ = CV-CVC-CVC: داخليّةٌ [CV، CVC] عددُها ‎4·0 + 2 = 2‎، فالعدد ‎3·2 + 2 = 8‎.
"""

from __future__ import annotations

from pathlib import Path

from gate import Refusal, enter
from gate.degrees import FINAL, INNER, code_word, decode_word, degree_of, table

ROOT = Path(__file__).resolve().parents[1]
TABLE = ROOT / "formal" / "a116" / "degrees.csv"


def _rows() -> list[tuple[int, int, str]]:
    out = []
    for line in TABLE.open(encoding="utf-8"):
        d, n, ss = line.rstrip("\n").split(",")
        out.append((int(d), int(n), ss))
    return out


def _mirror() -> list[tuple[int, int, str]]:
    return [(d, n, "-".join(r)) for d in range(1, 5) for n, r in enumerate(table(d))]


def test_python_mirror_matches_lean_degree_table() -> None:
    rows = _rows()
    assert len(rows) == 255
    assert [sum(1 for r in rows if r[0] == d) for d in (1, 2, 3, 4)] == [3, 12, 48, 192]
    assert rows == _mirror()
    # العددُ تقابل: الفكُّ ثمّ العدّ يعيد العدد، ولا صفَّ يتكرّر في درجته
    for d, n, ss in rows:
        assert code_word(ss.split("-")) == n
    assert len({(d, ss) for d, _, ss in rows}) == 255


def test_lean_table_rejects_named_mutants() -> None:
    """`MUTANT_CVVC_FINAL` و`MUTANT_LITTLE_ENDIAN`."""

    rows = _rows()
    # مرآةٌ تقبل CVVC طرفًا: أربعةُ أطرافٍ لا ثلاثة، فتزيد صفوفًا ليست في جدول Lean
    mutant_final = {(1, "-".join(t + (f,))) for t in [()] for f in (*FINAL, "CVVC")}
    lean_deg1 = {(d, ss) for d, _, ss in rows if d == 1}
    assert mutant_final != lean_deg1 and (1, "CVVC") in mutant_final - lean_deg1
    # مرآةٌ تعدّ الأحدثَ أعلى: تخالف Lean في عدد CV-CVV
    def little(ss: list[str]) -> int:
        n = 0
        for s in reversed(ss[:-1]):
            n = 4 * n + INNER.index(s)
        return 3 * n + INNER.index(ss[-1])
    lean_n = {ss: n for d, n, ss in rows}
    assert any(little(ss.split("-")) != n for ss, n in lean_n.items())
    assert decode_word(2, lean_n["CVC-CV-CVV"]) == ["CVC", "CV", "CVV"]


def test_gate_certificates_by_hand() -> None:
    for word, want in (("مِنْ", (1, 2, ("CVC",))),
                       ("كَتَبَ", (3, 0, ("CV", "CV", "CV"))),
                       ("عَلَيْهِمْ", (3, 8, ("CV", "CVC", "CVC")))):
        cert = enter(word.encode("utf-8"))
        assert not isinstance(cert, Refusal), word
        assert degree_of(cert.atoms) == want, word
