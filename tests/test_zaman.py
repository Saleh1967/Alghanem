"""ظروفُ الزمان: خمسُ صورٍ للمتصرّف، صورةٌ للمبنيّ، والتنوينُ يفرّق المرفوعَ من المقطوع."""

from __future__ import annotations

from slge.cells import STATES, licensed
from slge.zaman import CONSTANTS, STEMS, forms_of, hukm, nasb_tanwin, raf_tanwin
from slge.zuruf import qat

_A, _I, _U, SUKUN = STATES


def test_five_forms_and_readers() -> None:
    for stem in STEMS.values():
        fs = forms_of(stem)
        assert len(set(fs)) == 5 and all(licensed(f) for f in fs)
        assert hukm(raf_tanwin(stem)).startswith("مرفوع") and hukm(qat(stem)).startswith("مقطوع")
        assert hukm(nasb_tanwin(stem)) == "منصوب منوَّن"
        assert raf_tanwin(stem) != qat(stem) and raf_tanwin(stem)[:-1] == qat(stem)


def test_gate_witnesses_for_yawm() -> None:
    yawm = STEMS["يَوْم"]
    assert raf_tanwin(yawm) == (("ي", _A), ("و", SUKUN), ("م", _U), ("ن", SUKUN))  # يَوْمٌ
    assert nasb_tanwin(yawm) == (("ي", _A), ("و", SUKUN), ("م", _A), ("ن", SUKUN))  # يَوْمًا
    assert qat(yawm) == (("ي", _A), ("و", SUKUN), ("م", _U))  # يَوْمُ


def test_constants_single_state() -> None:
    assert len(CONSTANTS) == 8
    for name, (cells, st) in CONSTANTS.items():
        assert cells[-1][1] == st and licensed(cells), name
    assert hukm(CONSTANTS["مُنْذُ"][0]).startswith("مقطوع")  # ضمٌّ عارٍ: تقرؤه الخانةُ قطعًا
    assert hukm(CONSTANTS["إِذْ"][0]) == "لا تقرؤه الخانة"


def test_masaq_measurement_and_index() -> None:
    import importlib.util
    import sys
    from pathlib import Path

    root = Path(__file__).resolve().parent.parent
    tool = root / "tools" / "gen_zaman_index.py"
    spec = importlib.util.spec_from_file_location("gen_zaman_index", tool)
    assert spec and spec.loader
    mod = importlib.util.module_from_spec(spec)
    sys.modules["gen_zaman_index"] = mod
    spec.loader.exec_module(mod)
    by_stem, _roles, used = mod.states()
    assert used == 1334
    assert len(by_stem["يوم"]) == 6 and len(by_stem["إذا"]) == 1 and len(by_stem["متى"]) == 1
    assert mod.render() == (root / "ZAMAN_INDEX.md").read_text(encoding="utf-8")
