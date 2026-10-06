"""الضمائر: قانونُ نا وقانونُ التاء على شهادات البوّابة، وإيّا حاملٌ، والفهرسُ مولَّد."""

from __future__ import annotations

from slge.cells import STATES, licensed
from slge.damair import (
    ATTACHED_NASB,
    ATTACHED_RAF,
    DETACHED_NASB,
    DETACHED_RAF,
    IYYA,
    WITNESS,
    attach,
    na_role,
    ta_person,
    tier,
)

_A, _I, _U, SUKUN = STATES


def test_na_law_on_gate_witnesses() -> None:
    assert na_role(WITNESS["قُلْنَا"]) == "رفع" and na_role(WITNESS["جِئْنَا"]) == "رفع"
    for w in ("جَاءَنَا", "لَنَا", "إِنَّنَا", "إِيَّانَا"):
        assert na_role(WITNESS[w]) == "نصب/جرّ", w
    assert na_role(WITNESS["كُنْتُ"]) is None
    # طفرة: تسكينُ ما قبل نا في جَاءَنَا يقلبه رفعًا
    mutant = list(WITNESS["جَاءَنَا"])
    mutant[2] = ("ء", SUKUN)
    assert na_role(tuple(mutant)) == "رفع"


def test_ta_law_on_gate_witnesses() -> None:
    assert ta_person(WITNESS["كُنْتُ"]) == "متكلم"
    assert ta_person(WITNESS["كُنْتَ"]) == "مخاطب"
    assert ta_person(WITNESS["كُنْتِ"]) == "مخاطبة"
    assert ta_person((("ب", _A), ("ت", _A))) is None  # بعد متحرّك ليست تاء الفاعل


def test_iyya_is_carrier_plus_attached() -> None:
    assert len(DETACHED_NASB) == len(ATTACHED_NASB) == 12
    for d, a in zip(DETACHED_NASB, ATTACHED_NASB, strict=True):
        assert d.cells == attach(IYYA, a.cells)
    assert WITNESS["إِيَّاكَ"] == DETACHED_NASB[2].cells and WITNESS["إِيَّاهُ"] == DETACHED_NASB[7].cells
    assert WITNESS["إِيَّانَا"] == DETACHED_NASB[1].cells


def test_counts_and_licence() -> None:
    assert len(DETACHED_RAF) == 12 and len(ATTACHED_RAF) == 11
    assert all(licensed(p.cells) for p in DETACHED_RAF + DETACHED_NASB)
    assert all(licensed(w) for w in WITNESS.values())
    assert {tier(p) for p in ATTACHED_RAF} == {"د١٦ الإعراب من الخانة", "د٨ الحدّ (إلحاق)"}
    assert all(tier(p) == "د٤ الخانة" for p in DETACHED_RAF + DETACHED_NASB)


def test_index_is_current() -> None:
    import importlib.util
    import sys
    from pathlib import Path

    root = Path(__file__).resolve().parent.parent
    tool = root / "tools" / "gen_damair_index.py"
    spec = importlib.util.spec_from_file_location("gen_damair_index", tool)
    assert spec and spec.loader
    mod = importlib.util.module_from_spec(spec)
    sys.modules["gen_damair_index"] = mod
    spec.loader.exec_module(mod)
    assert mod.render() == (root / "DAMAIR_INDEX.md").read_text(encoding="utf-8")
