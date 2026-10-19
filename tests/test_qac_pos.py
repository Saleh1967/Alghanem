"""أقسامُ الكلم في QAC مودَعًا لـSLGE (ADR ٥١): المواقعُ والقطعُ كما قرأتُها باليد، والطفرات.

التوقّعاتُ باليد من سطور `quranic-corpus-morphology-0.4.txt` ومن سطور المدوّنة المختومة، لا من الأداة:
الفاتحةُ سبعةُ أسطرٍ رموزُها 4، 4، 2، 3، 4، 3، 9 = 29، وسطرُ (2:1) خمسةُ رموزٍ أربعةٌ منها بسملةٌ لا يعدّها
QAC؛ فـ«الم» (2:1:1، ‎INL‎) الموقعُ 33، و«ذَلِكَ» (2:2:1، ‎DEM‎) 34، و«فِيهِ» (2:2:5، ‎fiy P‎ + ‎hi PRON
SUFFIX‎) 38 — و`<sel>` بعده ليس موقعًا. الطفراتُ بأسمائها: `MUTANT_SEL_IS_A_TOKEN`،
`MUTANT_JOINED_FIRST_KEPT`، `MUTANT_STEM_IS_FIRST_SEGMENT`.
"""

from __future__ import annotations

import gzip
import importlib.util
import sys
from typing import Any

import pytest
from conftest import ROOT

SPEC = importlib.util.spec_from_file_location("gen_qac_pos", ROOT / "tools" / "gen_qac_pos.py")
assert SPEC and SPEC.loader
MOD: Any = importlib.util.module_from_spec(SPEC)
sys.modules["gen_qac_pos"] = MOD
SPEC.loader.exec_module(MOD)

SNIPPET = (
    "(1:1:1:1)\tAl^m^\tINL\tSTEM|POS:INL\n"
    "(1:1:2:1)\tyA\tVOC\tPREFIX|yA\n"
    "(1:1:2:2)\t>ay~u\tN\tSTEM|POS:N|LEM:>ay~\n"
    "(1:1:2:3)\thaA\tVOC\tSUFFIX|VOC\n"
    "(1:1:3:1)\tfiy\tP\tSTEM|POS:P|LEM:fiY\n"
    "(1:1:3:2)\thi\tPRON\tSUFFIX|PRON:3MS\n"
)
CORPUS = "الم يَا أَيُّهَا <sel> فِيهِ\n"


def test_hand_rows_on_a_snippet() -> None:
    rs, rules = MOD.rows(SNIPPET.encode("utf-8"), CORPUS)
    assert rs == [("0", "1:1:1", "STEM:INL", "INL"),
                  ("2", "1:1:2", "PREFIX:VOC+STEM:N+SUFFIX:VOC", "N"),
                  ("3", "1:1:3", "STEM:P+SUFFIX:PRON", "P")]
    assert rules["YA_JOINED_FIRST"] == 1 and rules["ALIGN_RESIDUAL"] == 0


def test_hand_rows_on_the_sealed_text() -> None:
    blob, rules, n = MOD.generate()
    rows = {r.split("\t")[0]: r.split("\t")
            for r in gzip.decompress(blob).decode("utf-8").splitlines()[1:]}
    assert rows["33"][1:] == ["2:1:1", "STEM:INL", "INL"]
    assert rows["34"][1:] == ["2:2:1", "STEM:DEM", "DEM"]
    assert rows["38"][1:] == ["2:2:5", "STEM:P+SUFFIX:PRON", "P"]
    assert not {"29", "30", "31", "32"} & set(rows)  # البسملةُ في (2:1) لا يعدّها QAC
    assert rules["BASMALA"] == 112 and blob == MOD.generate()[0]  # بلا طابع زمن


def _mutant(old: str, new: str) -> Any:
    src = (ROOT / "tools" / "gen_qac_pos.py").read_text(encoding="utf-8")
    assert old in src
    ns: dict[str, Any] = {"__name__": "qac_pos_mutant", "__file__": str(ROOT / "tools" / "x.py")}
    exec(compile(src.replace(old, new, 1), "qac_pos_mutant", "exec"), ns)  # noqa: S102
    return ns


def test_named_mutants_are_caught() -> None:
    m = _mutant('if t != "<sel>")}', "if True)}")
    with pytest.raises(AssertionError):  # SEL_IS_A_TOKEN: عدُّ المواقع يخالف تيّارَ الشهادات
        m["rows"](SNIPPET.encode("utf-8"), CORPUS)
    m = _mutant("str(tok[g[-1]])", "str(tok[g[0]])")
    assert m["rows"](SNIPPET.encode("utf-8"), CORPUS)[0][1][0] == "1"  # JOINED_FIRST_KEPT
    m = _mutant('if x.startswith("STEM:")', "")
    assert m["rows"](SNIPPET.encode("utf-8"), CORPUS)[0][1][3] == "VOC"  # STEM_IS_FIRST_SEGMENT
