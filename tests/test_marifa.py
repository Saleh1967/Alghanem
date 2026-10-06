"""المعارف: أل والإدغامُ الشمسيّ، الإضافةُ تُسقط التنوين، والقانونُ المقيس على MASAQ."""

from __future__ import annotations

from slge.cells import STATES, licensed
from slge.marifa import MAWSUL, SUN, al, drop_tanwin, has_al, idafa, kind_of, shamsi
from slge.nida import has_tanwin

_A, _I, _U, SUKUN = STATES
KITAB = (("ك", _I), ("ت", _A), ("ا", SUKUN), ("ب", _U))
RAHMAN = (("ر", _A), ("ح", SUKUN), ("م", _A), ("ن", _I))
SHAMS = (("ش", _A), ("م", SUKUN), ("س", _U))


def test_al_and_shamsi_match_gate() -> None:
    assert al(KITAB) == (("ء", _A), ("ل", SUKUN), *KITAB)  # ءَلْكِتَاْبُ
    assert al(RAHMAN) == (("ء", _A), ("ر", SUKUN), *RAHMAN)  # ءَرْرَحْمَنِ
    assert al(SHAMS) == (("ء", _A), ("ش", SUKUN), *SHAMS)  # ءَشْشَمْسُ
    for w in (KITAB, RAHMAN, SHAMS):
        assert has_al(al(w)) and licensed(al(w)) and not has_al(w)
    assert len(SUN) == 14 and shamsi(KITAB) == KITAB


def test_idafa_drops_tanwin() -> None:
    kitabun = (*KITAB, ("ن", SUKUN))
    assert has_tanwin(kitabun) and drop_tanwin(kitabun) == KITAB
    w = idafa(kitabun, (("ك", _A),))
    assert w == (*KITAB, ("ك", _A)) and not has_tanwin(w) and licensed(w)
    assert kind_of(w) == "مضاف إلى ضمير" and kind_of(al(KITAB)) == "معرَّف بأل"
    assert kind_of(MAWSUL["الَّذِينَ"]) == "اسم موصول" and kind_of(KITAB) == "لا تقرؤه الخانة"


def test_mawsul_witnesses() -> None:
    assert MAWSUL["الَّذِي"] == (("ء", _A), ("ل", SUKUN), ("ل", _A), ("ذ", _I), ("ي", SUKUN))
    assert MAWSUL["الَّذِينَ"][-1] == ("ن", _A) and MAWSUL["اللَّذَيْنِ"][-2:] == (("ي", SUKUN), ("ن", _I))
    assert len(MAWSUL) == 14 and len(set(MAWSUL.values())) == 14
    assert all(has_al(w) for name, w in MAWSUL.items() if name.startswith("ال"))
    assert has_tanwin(MAWSUL["مَنْ"])  # تشابهٌ مسمًّى


def test_masaq_measurement_and_index() -> None:
    import importlib.util
    import sys
    from pathlib import Path

    root = Path(__file__).resolve().parent.parent
    tool = root / "tools" / "gen_marifa_index.py"
    spec = importlib.util.spec_from_file_location("gen_marifa_index", tool)
    assert spec and spec.loader
    mod = importlib.util.module_from_spec(spec)
    sys.modules["gen_marifa_index"] = mod
    spec.loader.exec_module(mod)
    table, total = mod.measure()
    assert total == 6544
    assert table[("معرَّف بأل", True)] == 1 and table[("معرَّف بأل", False)] == 1884
    assert table[("مضاف", True)] + table[("مضاف إلى ضمير", True)] == 12
    assert table[("علم", True)] == 35
    assert mod.render() == (root / "MARIFA_INDEX.md").read_text(encoding="utf-8")
