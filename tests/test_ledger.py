"""الدفترُ مملوءًا من الأوزان (`A116.Ledger`، ADR ١٩): كلُّ وزنٍ صفٌّ في جدول درجته بعدده n.

التوقّعاتُ مستقلّةٌ عن `Ledger.waznRows`: الدرجةُ والعدد يُحسبان هنا باليد من مقاطع الوصل في `wazn.csv`
(مولَّدٌ من `Wazn.thulathi` ومودَعٌ قبل هذا الدفتر) بعدِّ جدول الوصل — ‎n = 3·I(t) + d(u)‎ و‎I‎ بالأساس 4 —
ثمّ يُطابَق بهما `lake exe a116-table ledger`. وشواهدُ مكتوبةٌ باليد من التقطيع:
كَتَبَ ← CV-CV-CV = (3، 0)؛ اِفْعَلْ ← ءِفْ | عَلْ = CVC-CVC: ‎3·2 + 2 = 8‎؛ فَاعِلْ ← CVV-CVC: ‎3·1 + 2 = 5‎؛
اِسْتَفْعَلَ ← ءِسْ | تَفْ | عَ | لَ = CVC-CVC-CV-CV: ‎I = 4·(4·2 + 2) + 0 = 40‎ ← ‎3·40 + 0 = 120‎.
والطفرة: عدٌّ بالأساس 6 (عددُ الوقف) على صفوف الوصل يخالف الجدول (`MUTANT_PAUSE_BASE`).
"""

from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
WAZN = ROOT / "formal" / "a116" / "wazn.csv"
LEDGER = ROOT / "formal" / "a116" / "ledger.csv"

INNER = ("CV", "CVV", "CVC", "CVVC")


def _n(ss: list[str], width: int = 3) -> int:
    i = 0
    for s in ss[:-1]:
        i = 4 * i + INNER.index(s)
    return width * i + INNER.index(ss[-1])


def _ledger() -> list[tuple[int, int, int]]:
    out = []
    for line in LEDGER.open(encoding="utf-8"):
        i, d, n = line.rstrip("\n").split(",")
        out.append((int(i), int(d), int(n)))
    return out


def _from_wazn(width: int = 3) -> list[tuple[int, int, int]]:
    out = []
    for line in WAZN.open(encoding="utf-8"):
        i, _, cont, _ = line.rstrip("\n").split(",")
        ss = cont.split("-")
        assert ss[-1] in INNER[:3]  # طرفُ الوصل
        out.append((int(i), len(ss), _n(ss, width)))
    return out


def test_ledger_matches_hand_count() -> None:
    rows = _ledger()
    assert len(rows) == 31
    assert rows == _from_wazn()
    assert [sum(1 for r in rows if r[1] == d) for d in (2, 3, 4)] == [6, 15, 10]


def test_hand_witnesses() -> None:
    rows = {i: (d, n) for i, d, n in _ledger()}
    assert rows[0] == (3, 0)  # كَتَبَ
    assert rows[20] == (2, 8)  # اِفْعَلْ
    assert rows[24] == (2, 5)  # فَاعِلْ
    assert rows[10] == (4, 120)  # اِسْتَفْعَلَ


def test_mutant_pause_base_is_refused() -> None:
    assert _from_wazn(width=6) != _ledger()  # MUTANT_PAUSE_BASE
