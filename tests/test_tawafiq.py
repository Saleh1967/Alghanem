"""توافيقُ الخانات (`A116.Tawafiq`، ADR ٦٣): عددُ المرخَّص من كلّ سلاسل الشبكة (113) بطولٍ معلوم.

١. `tawafiq.csv` (يطبعه Lean المترجَم، ويطابقه CI): أعدادُ الطولين الأوّل والثاني مكتوبةٌ هنا باليد
   من البنية — 84 = 28 × 3، و9,492 = 84 × 84 + 84 × 29، و56 = 28 × 2 — وأعدادُ الطول الثالث تُعاد
   بمرآة البوّابة المستقلّة (`gate.licence`) لا بـLean (`-m slow`: ‎1.44 مليون سلسلة‎).
٢. الثغرةُ المسمّاة `ALIF_CLOSER_NOT_REFUSED`: كُاْ مرخَّصٌ وصلًا في المرآة أيضًا، والألفُ فيه مُغلِق.
٣. الفضاءُ المولَّد (ADR ٦٩): أبنيةُ الاسم الثلاثيّ على الشاهد ك ت ب — الأعمى 64، والقانونُ 45 وصلًا
   و48 وقفًا (بالمرآة)، والاثنا عشر كلُّها مرخَّصة، والعشرةُ **نقلٌ** (`TEN_OF_TWELVE_IS_NAQL`): مراسيها
   أسطرُ الكتاب المختوم بأعيانها (`corpora/sibawayh/kitab-anchors.tsv`) تُطابَق على الكتاب المختوم
   هنا (`corpora/kitab/`، ADR ٦٨).
الطفرات: `MUTANT_ALIF_ONSET` (29 × 3 = 87)، `MUTANT_BINARY_COUNT` (‎U(2) = 10,092‎)، `MUTANT_3364`،
`MUTANT_LAW_GIVES_TEN` (نسبةُ العشرة إلى القانون)، `MUTANT_ANCHOR_LINE_SHIFTED`.
"""

from __future__ import annotations

import gzip
import hashlib
import itertools
from pathlib import Path

import pytest

from gate.licence import kind_of, licensable_atom, strict_licensed, strict_pause_licensed

ROOT = Path(__file__).resolve().parents[1]
TABLE = ROOT / "formal" / "a116" / "tawafiq.csv"
LICENSABLE = ROOT / "formal" / "a116" / "licensable.csv"


ANCHORS = ROOT / "corpora" / "sibawayh" / "kitab-anchors.tsv"
KITAB = ROOT / "corpora" / "kitab" / "0180Sibawayhi.KitabSibawayhi.JK006989-ara1.gz"
KITAB_SHA256 = "a160f940bb194e6fe7e6655d2c7f28e41f1fc648c4c5e340cc4e42306d5cb625"


def _lines() -> list[str]:
    return TABLE.read_text(encoding="utf-8").splitlines()[1:]


def _rows() -> dict[int, tuple[int, int, int, int]]:
    out: dict[int, tuple[int, int, int, int]] = {}
    for ln in _lines():
        n, *rest = ln.split(",")
        if n.isdigit():
            out[int(n)] = tuple(int(x) for x in rest)  # type: ignore[assignment]
    return out


def _anchors() -> list[dict[str, str]]:
    head, *body = ANCHORS.read_text(encoding="utf-8").splitlines()
    keys = head.split("\t")
    return [dict(zip(keys, ln.split("\t"))) for ln in body]


def _cells() -> list[str]:
    cells = [ln.split(",")[0] for ln in LICENSABLE.read_text(encoding="utf-8").splitlines()
             if ln.strip()]
    assert len(cells) == 113 and all(licensable_atom(c) for c in cells)
    return cells


def _count(n: int) -> tuple[int, int, int, int]:
    total = wasl = waqf = closers = 0
    for seq in itertools.product(_cells(), repeat=n):
        a = list(seq)
        total += 1
        if strict_licensed(a):
            wasl += 1
            if a[-1] == "اْ" and kind_of(a)[-1] == "c":
                closers += 1
        if strict_pause_licensed(a):
            waqf += 1
    return total, wasl, waqf, closers


def test_lengths_one_and_two_by_hand() -> None:
    rows = _rows()
    assert rows[1] == (113, 28 * 3, 28 * 3, 0)
    assert rows[2] == (113 ** 2, 84 * 84 + 84 * 29, 84 * 84 + 84 * 29, 28 * 2)
    assert _count(1) == rows[1] and _count(2) == rows[2]


@pytest.mark.slow
def test_length_three_by_independent_mirror() -> None:
    rows = _rows()
    assert rows[3][0] == 113 ** 3 and rows[3][2] == 84 * 113 ** 2 and rows[3][3] == 56 * 84
    assert _count(3) == rows[3]


def test_alif_closer_not_refused() -> None:
    """`ALIF_CLOSER_NOT_REFUSED`: الألفُ الساكنة بعد ضمّةٍ مُغلِقٌ مرخَّص، وبعد فتحةٍ مدّ."""

    assert strict_licensed(["كُ", "اْ"]) and kind_of(["كُ", "اْ"]) == ["cv", "c"]
    assert kind_of(["كَ", "اْ"]) == ["cv", "v"]
    assert strict_pause_licensed(["كَ", "اْ", "اْ"]) and not strict_licensed(["كَ", "اْ", "اْ"])


def test_mutants_rejected() -> None:
    rows = _rows()
    assert 29 * 3 != rows[1][1]                    # MUTANT_ALIF_ONSET: الألفُ حاملَ ابتداء
    assert 87 * 87 + 87 * 29 != rows[2][1]         # MUTANT_BINARY_COUNT: U(2) الثنائيّ على الـ116
    assert 29 * 4 * 29 not in rows[1] + rows[2]    # MUTANT_3364


# العشرةُ باليد من الكتاب (س18621–18641): البناءُ ومثالُه وسطرُه؛ والحركةُ من المثال لأنّ الكتاب غيرُ مشكول
NAQL_TEN = [("فَعْل", "صقر", 18625), ("فِعْل", "عكم", 18626), ("فُعْل", "برد", 18628),
            ("فَعَل", "جبل", 18630), ("فَعِل", "كتف", 18631), ("فَعُل", "رجل", 18632),
            ("فُعَل", "صرد", 18633), ("فُعُل", "طنب", 18635), ("فِعَل", "ضلع", 18637),
            ("فِعِل", "إبل", 18640)]


def _shapes(root: str = "كتب") -> dict[str, list[str]]:
    marks = "َُِْ"
    return {a + b + c: [root[0] + a, root[1] + b, root[2] + c]
            for a in marks for b in marks for c in marks}


def test_generated_space_row_by_hand() -> None:
    g = [ln for ln in _lines() if ln.startswith("g,ism3")]
    assert g == ["g,ism3,64,45,48,12,10"]
    shapes = _shapes()
    assert len(shapes) == 64
    assert sum(strict_licensed(v) for v in shapes.values()) == 45
    assert sum(strict_pause_licensed(v) for v in shapes.values()) == 48
    twelve = [(a, b) for a in "َُِ" for b in "َُِْ"]
    assert all(strict_licensed(["ك" + a, "ت" + b, "بُ"]) for a, b in twelve)
    assert all(strict_pause_licensed(["ك" + a, "ت" + b, "بْ"]) for a, b in twelve)


def test_higher_degree_rows_by_hand() -> None:
    """ADR ٧٠: الفعلُ 12 بالقانون و4 بالنقل (ثلاثةُ أبواب وفُعِلَ س18641)، والرباعيُّ 48/45/1،
    والزوائدُ 31."""

    g = {ln.split(",")[1]: ln.split(",")[2:] for ln in _lines() if ln.startswith("g,")}
    assert g["fil3"] == ["12", "12", "-", "12", "4"]
    assert g["rubai4"] == ["48", "45", "-", "-", "1"]
    assert g["zawaid"] == ["31", "31", "-", "-", "31"]
    marks = "َُِْ"
    assert sum(strict_licensed(["د" + a, "ح" + b, "ر" + c, "جَ"])
               for a in marks[:3] for b in marks for c in marks) == 45


def test_naql_ten_is_subset_and_two_are_left() -> None:
    naql = [ln.split(",") for ln in _lines() if ln.startswith("naql,")]
    assert [(r[2], r[3]) for r in naql] == [(str(ln), ex) for _, ex, ln in NAQL_TEN]
    patterns = {(b[1], b[3]) for b, _, _ in NAQL_TEN}
    assert len(patterns) == 10
    twelve = {(a, b) for a in "َُِ" for b in "َُِْ"}
    assert patterns < twelve and twelve - patterns == {("ُ", "ِ"), ("ِ", "ُ")}   # فُعِل، فِعُل (س18641)
    assert 10 != 12                                                           # MUTANT_LAW_GIVES_TEN


def test_anchors_are_verbatim_lines_of_the_sealed_kitab() -> None:
    raw = gzip.decompress(KITAB.read_bytes())
    assert hashlib.sha256(raw).hexdigest() == KITAB_SHA256
    lines = raw.decode("utf-8").split("\n")
    rows = _anchors()
    assert len(rows) == 17
    for r in rows:
        assert lines[int(r["line"]) - 1] == r["text"], r["line"]
    for b, ex, ln in NAQL_TEN:
        row = next(r for r in rows if r["line"] == str(ln))
        assert row["binaa"] == b and ex in row["text"]
    assert any(r["line"] == "235" and "لا يغنى واحد منهما عن الآخر" in r["text"] for r in rows)


def test_mutant_anchor_line_shifted() -> None:
    rows = _anchors()
    texts = [r["text"] for r in rows]
    assert all(texts[i] != texts[i + 1] for i in range(len(texts) - 1))
