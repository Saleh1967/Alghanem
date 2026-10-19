"""شاهدُ الدلالة جدولًا (`A116.Maqayis`، ADR ٣٥): صفوفُ Lean هي جذورُ الجدول المختوم بعينها.

`formal/a116/maqayis.csv` يطبعه Lean (`lake exe a116-table maqayis`) ويطابقه CI
بايتًا. والتوقّعُ يُعدّ هنا من بايتات `maqayis_by_root_csv_999.csv` المختومة بقاعدةٍ
معلنةٍ باليد (الكراسيُّ همزة، والمقصورةُ ياء، والآخرُ ثلاثةُ أصولٍ من الثمانية
والعشرين) — لا من شيفرة البوّابة ولا من Lean. والترتيبُ بالعدد n كما عرّفه
`RootGrade.num` (الفاءُ أدنى منزلة). والطفرات: إسقاطُ طيّ الكراسيّ، وإسقاطُ طيّ
المقصورة، وقلبُ المنازل.
"""

from __future__ import annotations

import csv
import hashlib
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TABLE = ROOT / "formal" / "a116" / "maqayis.csv"
SEALED = ROOT / "maqayis_by_root_csv_999.csv"
SEALED_SHA256 = "2c6000bd47797e183294b89da77df4ddfd27921ea595c6071ba52299c382ccb0"
CARRIERS = "ابتثجحخدذرزسشصضطظعغفقكلمنهويء"  # ترتيبُ الحوامل الـ29 (`Field112.carrierChar`) — باليد
RADICALS = set(CARRIERS[1:])
SEATS = {"أ": "ء", "إ": "ء", "ؤ": "ء", "ئ": "ء"}
MAQSURA = {"ى": "ي"}


def _sealed_roots(fold: dict[str, str]) -> set[str]:
    data = SEALED.read_bytes()
    assert hashlib.sha256(data).hexdigest() == SEALED_SHA256
    out: set[str] = set()
    for row in csv.DictReader(data.decode("utf-8").splitlines()):
        root = "".join(fold.get(c, c) for c in row["root_full"].replace("آ", "ءا"))
        if len(root) == 3 and set(root) <= RADICALS:
            out.add(root)
    return out


def _lean_rows() -> list[str]:
    return [line.strip() for line in TABLE.open(encoding="utf-8") if line.strip()]


def _n(root: str) -> int:
    d = [CARRIERS.index(c) - 1 for c in root]
    return d[0] + 28 * d[1] + 784 * d[2]


def test_lean_rows_are_the_sealed_roots() -> None:
    rows = _lean_rows()
    assert len(rows) == len(set(rows))
    assert set(rows) == _sealed_roots({**SEATS, **MAQSURA})


def test_rows_are_ordered_by_n() -> None:
    ns = [_n(r) for r in _lean_rows()]
    assert ns == sorted(ns) and len(set(ns)) == len(ns)


def test_mutant_without_seat_folding_is_caught() -> None:
    # MUTANT_NO_SEAT_FOLD: أ/إ/ؤ/ئ ليست من الثمانية والعشرين — فتسقط جذورُ الهمزة
    assert _sealed_roots(MAQSURA) < set(_lean_rows())


def test_mutant_without_maqsura_folding_is_caught() -> None:
    # MUTANT_NO_MAQSURA_FOLD: ى ليست من الثمانية والعشرين — فتسقط جذورُ الناقص اليائيّ المكتوب بها
    assert _sealed_roots(SEATS) != set(_lean_rows())


def test_mutant_big_endian_order_is_caught() -> None:
    # MUTANT_BIG_ENDIAN: الفاءُ أعلى منزلةً — ترتيبٌ غيرُ ترتيب Lean
    d = [[CARRIERS.index(c) - 1 for c in r] for r in _lean_rows()]
    ns = [784 * a + 28 * b + c for a, b, c in d]
    assert ns != sorted(ns)
