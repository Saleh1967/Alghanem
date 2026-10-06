"""أسماءُ الإشارة: العمليّاتُ الثلاث على النواة، الحالةُ من المدّ، والشواهدُ من البوّابة."""

from __future__ import annotations

from slge.cells import STATES, licensed
from slge.ishara import DUALS, FORMS, WITNESSED, bud, case_of, dual, tanbih, tier

_A, _I, _U, SUKUN = STATES
BY = {f.name: f.cells for f in FORMS}


def test_gate_witnesses_are_the_law_forms() -> None:
    gate = {
        "هَذَا": (("ه", _A), ("ذ", _A), ("ا", SUKUN)),
        "هَذِهِ": (("ه", _A), ("ذ", _I), ("ه", _I)),
        "هَذَانِ": (("ه", _A), ("ذ", _A), ("ا", SUKUN), ("ن", _I)),
        "هَاتَيْنِ": (("ه", _A), ("ا", SUKUN), ("ت", _A), ("ي", SUKUN), ("ن", _I)),
        "هَؤُلَاءِ": (("ه", _A), ("ء", _U), ("ل", _A), ("ا", SUKUN), ("ء", _I)),
        "ذَلِكَ": (("ذ", _A), ("ل", _I), ("ك", _A)),
        "تِلْكَ": (("ت", _I), ("ل", SUKUN), ("ك", _A)),
        "أُولَئِكَ": (("ء", _U), ("و", SUKUN), ("ل", _A), ("ء", _I), ("ك", _A)),
        "هُنَالِكَ": (("ه", _U), ("ن", _A), ("ا", SUKUN), ("ل", _I), ("ك", _A)),
        "ثَمَّ": (("ث", _A), ("م", SUKUN), ("م", _A)),
        "ذَا": (("ذ", _A), ("ا", SUKUN)),
        "ذِي": (("ذ", _I), ("ي", SUKUN)),
        "أُولَاءِ": (("ء", _U), ("و", SUKUN), ("ل", _A), ("ا", SUKUN), ("ء", _I)),
    }
    assert set(gate) == set(WITNESSED) and len(gate) == 13
    for name, cells in gate.items():
        assert BY[name] == cells, name


def test_three_operations_and_case_reading() -> None:
    core = (("ذ", _A),)
    assert tanbih(dual(core, "رفع")) == BY["هَذَانِ"] and bud(dual(core, "نصب")) == BY["ذَيْنِكَ"]
    assert case_of(BY["هَذَانِ"]) == "رفع" and case_of(BY["ذَيْنِكَ"]) == "نصب/جرّ"
    assert dual(core, "نصب") == dual(core, "جرّ")
    for f in FORMS:
        assert (case_of(f.cells) is not None) == (f.name in DUALS), f.name
        assert licensed(f.cells)


def test_mutation_breaks_the_dual_law() -> None:
    w = list(BY["هَذَانِ"])
    w[-1] = ("ن", _A)  # نونٌ مفتوحة: ليست نون المثنّى
    assert case_of(tuple(w)) is None
    w = list(BY["هَذَانِ"])
    w[-2] = ("و", SUKUN)
    assert case_of(tuple(w)) is None


def test_tiers_and_index() -> None:
    assert tier(FORMS[0]) == "د٨ الحدّ (تنبيهٌ أو بُعد)" and tier(FORMS[2]).startswith("د١٦")
    assert tier(FORMS[-1]).startswith("د٤")
    assert len({f.cells for f in FORMS}) == len(FORMS) == 25

    import importlib.util
    import sys
    from pathlib import Path

    root = Path(__file__).resolve().parent.parent
    tool = root / "tools" / "gen_ishara_index.py"
    spec = importlib.util.spec_from_file_location("gen_ishara_index", tool)
    assert spec and spec.loader
    mod = importlib.util.module_from_spec(spec)
    sys.modules["gen_ishara_index"] = mod
    spec.loader.exec_module(mod)
    assert mod.render() == (root / "ISHARA_INDEX.md").read_text(encoding="utf-8")
