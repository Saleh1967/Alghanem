"""جدولُ الغزاليّ بأسطره (ADR ٣٣): توقّعاتٌ مستقلّةٌ عن الشيفرة من المختومات — الخاناتُ الثماني كلٌّ بسطرها،
المنتِجُ من الأخصّ عينُ المقدَّم ونقيضُ التالي لا غير والمساوي يُنتج الأربع («إذا ثبت أن التالي مساو
للمقدم»)، خاناتُ المنطق رأيٌ ثانٍ بلا مرساةٍ في النبهانيّ، والقراءتان الأصوليّتان (مفهومُ الموافقة، مفهومُ
المخالفة بالشرط) مرساتان في المودَعَين معًا؛ وطفراتٌ مرفوضة باسمها."""

from __future__ import annotations

import gzip
import hashlib
import importlib.util
import sys
from pathlib import Path
from typing import Any

import pytest

from slge.ghazali_table import DEGREES, FORMS, GHAZALI, KINDS, NABHANI, ROWS
from slge.knowledge import Degree, Form, productive

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "tests" / "data"
SEALED = {"ج3": ("nabhani-shakhsiyya-3.txt.gz", "359bb553"),
          "التفكير": ("nabhani-tafkir.txt.gz", "b9b08eab"),
          "المستصفى": ("openiti-ghazali-mustasfa.txt.gz", "59cda7d5"),
          "محك النظر": ("openiti-ghazali-mihakk.txt.gz", "9e54d050"),
          "معيار العلم": ("openiti-ghazali-micyar.txt.gz", "2ddf9165")}


def _tool() -> Any:
    spec = importlib.util.spec_from_file_location("deposit_ghazali",
                                                  ROOT / "tools" / "deposit_ghazali.py")
    assert spec and spec.loader
    mod = importlib.util.module_from_spec(spec)
    sys.modules["deposit_ghazali"] = mod
    spec.loader.exec_module(mod)
    return mod


def _texts() -> dict[str, list[str]]:
    out = {}
    for src, (name, prefix) in SEALED.items():
        raw = gzip.decompress((DATA / name).read_bytes())
        assert hashlib.sha256(raw).hexdigest().startswith(prefix)
        out[src] = raw.decode("utf-8").split("\n")
    return out


def test_every_anchor_is_in_its_line_of_the_sealed_text() -> None:
    texts = _texts()
    assert len(ROWS) == 11 and [r[0] for r in ROWS] == list(range(11))
    for rid, _, _, _, _, ghazali, nabhani, _ in ROWS:
        for src, line, phrase in (*ghazali, *nabhani):
            assert phrase in texts[src][line - 1], (rid, src, line, phrase)
        assert all(src in GHAZALI for src, _, _ in ghazali) and GHAZALI == ("المستصفى", "محك النظر",
                                                                             "معيار العلم")
        assert all(src in NABHANI for src, _, _ in nabhani) and NABHANI == ("ج3", "التفكير")


def test_the_eight_cells_by_line_are_ghazalis_table_and_the_productive_one() -> None:
    """الأخصُّ: عينُ المقدَّم ونقيضُ التالي تُنتجان («والمنتج منه إثنان»)، والعقيمتان بشاهدٍ («ربما يكون
    فرسا»)؛ المساوي: الأربعُ («إذا ثبت أن التالي مساو للمقدم»، الشمسُ والنهار)."""

    cells = {(DEGREES[r[2]], FORMS[r[3]]): r[4] for r in ROWS if r[1] == 0}
    assert len(cells) == 8
    assert {f for (d, f), v in cells.items() if d == "akhass" and v} == {"aynMuqaddam", "naqidTali"}
    assert all(v for (d, _), v in cells.items() if d == "musawi")
    names = {"akhass": Degree.اخص, "musawi": Degree.مساو}
    forms = {"aynMuqaddam": Form.عين_المقدم, "naqidTali": Form.نقيض_التالي,
             "naqidMuqaddam": Form.نقيض_المقدم, "aynTali": Form.عين_التالي}
    for (d, f), v in cells.items():
        assert productive(names[d], forms[f]) == v, (d, f)
    # الشاهدُ على العقم بعينه، والمساوي بشرطه
    barren = next(r for r in ROWS if r[1] == 0 and r[2] == 0 and r[3] == 2)
    assert ("معيار العلم", 1517, "إذ ربما يكون فرسا") in barren[5]
    assert all(any(a[1] in (1524, 1525) for a in r[5]) for r in ROWS if r[1] == 0 and r[2] == 1)


def test_logic_is_a_second_opinion_and_usul_readings_agree_with_nabhani() -> None:
    assert KINDS[0].endswith("(رأي ثانٍ)") and "موافقة" in KINDS[1]
    logic = [r for r in ROWS if r[1] == 0]
    assert all(r[5] and not r[6] for r in logic)  # مرساةٌ عند الغزاليّ، لا مرساةَ لها في النبهانيّ
    usul = [r for r in ROWS if r[1] == 1]
    assert len(usul) == 2 and all(r[5] and r[6] and r[4] for r in usul)
    muwafaqa, mukhalafa = usul
    assert (DEGREES[muwafaqa[2]], FORMS[muwafaqa[3]]) == ("akhass", "aynMuqaddam")
    assert (DEGREES[mukhalafa[2]], FORMS[mukhalafa[3]]) == ("musawi", "naqidMuqaddam")
    assert ("ج3", 559, "ويسمى فحوى الخطاب") in muwafaqa[6]
    assert ("ج3", 567, "ويسمى دليل الخطاب") in mukhalafa[6]
    assert ("المستصفى", 10949, "وهذا قد يسمى مفهوم الموافقة") in muwafaqa[5]
    manhaj = [r for r in ROWS if r[1] == 2]
    assert len(manhaj) == 1 and not manhaj[0][5] and all(s == "التفكير" for s, _, _ in manhaj[0][6])


def test_mutations_are_refused_by_name() -> None:
    m = _tool()
    texts = _texts()
    m.verify(texts)
    rows = list(m.ROWS)

    def put(i: int, row: Any) -> None:
        m.ROWS = (*rows[:i], row, *rows[i + 1:])

    rid, kind, d, f, st, gh, nb, note = rows[2]
    put(2, (rid, kind, d, f, st, (("معيار العلم", 1517, "إذ ربما يكون جملا"),), nb, note))
    with pytest.raises(SystemExit, match="PHRASE_NOT_IN_LINE"):
        m.verify(texts)
    put(2, (rid, kind, d, 3, st, gh, nb, note))  # خانةٌ مكرّرة وأخرى مفقودة
    with pytest.raises(SystemExit, match="CELLS_NOT_COVERING"):
        m.verify(texts)
    put(2, (rid, kind, d, f, st, gh, (("التفكير", 67, "أما البحث المنطقي"),), note))  # ادّعاءُ موافقة
    with pytest.raises(SystemExit, match="LOGIC_CELL_IS_SECOND_OPINION"):
        m.verify(texts)
    rid, kind, d, f, st, gh, nb, note = rows[8]
    put(8, (rid, kind, d, f, st, gh, (), note))  # قراءةٌ أصوليّة بلا مرساةٍ في العمود
    with pytest.raises(SystemExit, match="USUL_READING_NOT_IN_BOTH"):
        m.verify(texts)
    put(8, (rid, kind, d, f, st, gh, (("المستصفى", 10949, "مفهوم الموافقة"),), note))
    with pytest.raises(SystemExit, match="NABHANI_ANCHOR_NOT_FROM_SPINE"):
        m.verify(texts)
    m.ROWS = tuple(rows)
    m.verify(texts)


def test_python_table_matches_the_lean_export() -> None:
    """`lake exe slge-table ghazali_table` (formal/out/ghazali_table.csv) يطبع الصفوفَ من
    `GhazaliTable.lean`؛ الجدولُ البايثونيُّ المولَّدُ من المودَع نفسِه يطابقه صفًّا صفًّا."""

    lean_forms = {"aynMuqaddam": "ayn_muqaddam", "naqidTali": "naqid_tali",
                  "naqidMuqaddam": "naqid_muqaddam", "aynTali": "ayn_tali"}
    rows = (ROOT / "formal" / "out" / "ghazali_table.csv").read_text(encoding="utf-8").splitlines()
    exported = [r.split(",") for r in rows if r.startswith("row,")]
    assert len(exported) == len(ROWS) == 11
    for (_, rid, kind, d, f, st, n_gh, n_nb), row in zip(exported, ROWS, strict=True):
        assert (int(rid), int(kind), d, f, st == "true", int(n_gh), int(n_nb)) == (
            row[0], row[1], DEGREES[row[2]], lean_forms[FORMS[row[3]]], row[4], len(row[5]),
            len(row[6]))
