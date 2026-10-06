"""العدد: المخالفةُ تاءٌ، التركيبُ فتح، العقودُ واوٌ وياء، والتمييزُ مقيس."""

from __future__ import annotations

from slge.adad import (
    STEMS,
    TEN_FEM,
    TEN_MASC,
    UQUD,
    compound,
    fem,
    gender_of,
    masc,
    tamyiz_state,
    twelve,
    twelve_case,
    uqud,
    uqud_case,
)
from slge.cells import STATES, licensed

_A, _I, _U, SUKUN = STATES


def test_gate_witnesses() -> None:
    assert masc(STEMS[3], _A) == (("ث", _A), ("ل", _A), ("ا", SUKUN), ("ث", _A), ("ت", _A))  # ثَلَاثَةَ
    assert fem(STEMS[3], _U) == (("ث", _A), ("ل", _A), ("ا", SUKUN), ("ث", _U))  # ثَلَاثُ
    assert fem(STEMS[7], _A) == (("س", _A), ("ب", SUKUN), ("ع", _A))  # سَبْعَ
    thamaniya = (("ث", _A), ("م", _A), ("ا", SUKUN), ("ن", _I), ("ي", _A), ("ت", _A))
    assert masc(STEMS[8], _A) == thamaniya  # ثَمَانِيَةَ
    assert compound(STEMS[9], True) == (("ت", _I), ("س", SUKUN), ("ع", _A), *TEN_MASC)  # تِسْعَ عَشَرَ
    ishrin = (("ع", _I), ("ش", SUKUN), ("ر", _I), ("ي", SUKUN), ("ن", _A))
    assert uqud(UQUD[20], False) == ishrin  # عِشْرِينَ
    ithnata = (("ء", _I), ("ث", SUKUN), ("ن", _A), ("ت", _A), ("ا", SUKUN), *TEN_FEM)
    assert twelve(True, False) == ithnata  # اثْنَتَا عَشْرَةَ


def test_gender_is_one_ta_and_six_is_radical() -> None:
    for n, stem in STEMS.items():
        for case in (_U, _A, _I):
            assert gender_of(masc(stem, case)) == "مذكّر" and gender_of(fem(stem, case)) == "مؤنّث", n
            assert fem(stem, case) == (*masc(stem, case)[:-2], (stem[-1][0], case))
    assert gender_of(fem(STEMS[6], _U)) == "مؤنّث"  # سِتُّ: التاءُ أصل بعد ساكن


def test_compound_shin_twelve_uqud() -> None:
    assert TEN_MASC[1] == ("ش", _A) and TEN_FEM[1] == ("ش", SUKUN)
    for n in range(3, 10):
        for m in (True, False):
            w = compound(STEMS[n], m)
            assert w[-1][1] == _A and licensed(w)
    assert {twelve_case(twelve(r, m)) for r in (True,) for m in (True, False)} == {"رفع"}
    assert {twelve_case(twelve(False, m)) for m in (True, False)} == {"نصب/جرّ"}
    for stem in UQUD.values():
        assert uqud_case(uqud(stem, True)) == "رفع" and uqud_case(uqud(stem, False)) == "نصب/جرّ"
    assert uqud_case((("ب", _A),)) is None


def test_tamyiz_function_and_masaq() -> None:
    assert tamyiz_state(7) == (_I, False, True) and tamyiz_state(11) == (_A, True, False)
    assert tamyiz_state(100) == (_I, False, False) and tamyiz_state(2) == (_A, False, False)

    import importlib.util
    import sys
    from pathlib import Path

    root = Path(__file__).resolve().parent.parent
    tool = root / "tools" / "gen_adad_index.py"
    spec = importlib.util.spec_from_file_location("gen_adad_index", tool)
    assert spec and spec.loader
    mod = importlib.util.module_from_spec(spec)
    sys.modules["gen_adad_index"] = mod
    spec.loader.exec_module(mod)
    table, counted, total = mod.measure()
    assert (counted, total) == (72, 112)
    assert sum(v for (_, _, o), v in table.items() if o) == 71
    assert mod.render() == (root / "ADAD_INDEX.md").read_text(encoding="utf-8")
