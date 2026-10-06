"""أسماءُ الاستفهام: أَيّ وحدَه معرب، التركيبُ على الخانات، حذفُ ألف ما والإدغام، والصدارةُ مقيسة."""

from __future__ import annotations

from slge.cells import STATES, licensed
from slge.istifham import (
    AN,
    BI,
    FORMS,
    MA,
    MABNI,
    MAN,
    MIN,
    ayy,
    case_of,
    idgham_nm,
    ma_after_jarr,
    tier,
)

_A, _I, _U, SUKUN = STATES
BY = {f.name: f.cells for f in FORMS}


def test_gate_witnesses_are_the_law_forms() -> None:
    gate = {
        "أَيُّ": (("ء", _A), ("ي", SUKUN), ("ي", _U)), "أَيَّ": (("ء", _A), ("ي", SUKUN), ("ي", _A)),
        "أَيِّ": (("ء", _A), ("ي", SUKUN), ("ي", _I)),
        "مَاذَا": (("م", _A), ("ا", SUKUN), ("ذ", _A), ("ا", SUKUN)),
        "أَمَّنْ": (("ء", _A), ("م", SUKUN), ("م", _A), ("ن", SUKUN)),
        "بِمَ": (("ب", _I), ("م", _A)), "لِمَ": (("ل", _I), ("م", _A)),
        "فِيمَ": (("ف", _I), ("ي", SUKUN), ("م", _A)),
        "عَمَّ": (("ع", _A), ("م", SUKUN), ("م", _A)), "مِمَّ": (("م", _I), ("م", SUKUN), ("م", _A)),
        "لِأَيِّ": (("ل", _I), ("ء", _A), ("ي", SUKUN), ("ي", _I)),
        "أَنَّى": (("ء", _A), ("ن", SUKUN), ("ن", _A), ("ا", SUKUN)),
        "أَيَّانَ": (("ء", _A), ("ي", SUKUN), ("ي", _A), ("ا", SUKUN), ("ن", _A)),
    }
    for name, cells in gate.items():
        assert BY[name] == cells, name
    assert sum(f.witnessed for f in FORMS) == 21
    assert not next(f for f in FORMS if f.name == "مَنْ ذَا").witnessed


def test_ayy_is_the_only_declinable() -> None:
    assert [case_of(ayy(s)) for s in (_U, _A, _I)] == ["رفع", "نصب", "جرّ"]
    assert all(case_of(BY[n]) is None for n in MABNI)
    assert len({ayy(s)[:-1] for s in (_U, _A, _I)}) == 1
    assert case_of(BY["أَيْنَ"]) is None  # ليست أَيّ وإن شاركتها الصدر


def test_composition_and_ma_after_jarr() -> None:
    assert BY["مَاذَا"] == (*MA, *BY["ذَا"]) if "ذَا" in BY else BY["مَاذَا"][:2] == MA
    assert licensed((*MAN, ("ذ", _A), ("ا", SUKUN)))
    assert ma_after_jarr(BI) == (("ب", _I), ("م", _A))
    assert ma_after_jarr(AN) == (("ع", _A), ("م", SUKUN), ("م", _A))
    assert ma_after_jarr(MIN) == (("م", _I), ("م", SUKUN), ("م", _A))
    assert idgham_nm((("ع", _A), ("ن", SUKUN), ("ب", _A))) == (("ع", _A), ("ن", SUKUN), ("ب", _A))
    assert len(idgham_nm(BY["عَمَّ"])) == len(BY["عَمَّ"])


def test_tiers_and_index() -> None:
    assert tier(FORMS[8]).startswith("د١٦") and tier(FORMS[11]).startswith("د٨")
    assert tier(FORMS[0]).startswith("د٤") and tier(FORMS[14]).startswith("د٤")
    assert len({f.cells for f in FORMS}) == len(FORMS) == 22

    import importlib.util
    import sys
    from pathlib import Path

    root = Path(__file__).resolve().parent.parent
    tool = root / "tools" / "gen_istifham_index.py"
    spec = importlib.util.spec_from_file_location("gen_istifham_index", tool)
    assert spec and spec.loader
    mod = importlib.util.module_from_spec(spec)
    sys.modules["gen_istifham_index"] = mod
    spec.loader.exec_module(mod)
    front, other, total, _ = mod.precedence()
    assert (front, other, total) == (100, 151, 251)
    assert mod.render() == (root / "ISTIFHAM_INDEX.md").read_text(encoding="utf-8")
