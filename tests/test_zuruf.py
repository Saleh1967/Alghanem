"""ظروفُ المكان: القطعُ والجرُّ والإضافةُ على الخانة الأخيرة، والقياسُ على MASAQ."""

from __future__ import annotations

from slge.cells import STATES, licensed
from slge.zuruf import CONSTANTS, STEMS, hukm, jarr, mudaf, qat, set_last

_A, _I, _U, SUKUN = STATES
BY = {z.name: z.stem for z in STEMS}


def test_three_operations_read_back() -> None:
    for z in STEMS:
        assert hukm(mudaf(z.stem)) == "منصوب مضاف"
        assert hukm(jarr(z.stem)) == "مجرور"
        assert hukm(qat(z.stem)).startswith("مقطوع")
        for op in (mudaf, jarr, qat):
            assert licensed(op(z.stem)) and len(op(z.stem)) == len(z.stem)


def test_gate_witnesses() -> None:
    assert qat(BY["قَبْل"]) == (("ق", _A), ("ب", SUKUN), ("ل", _U))  # قَبْلُ
    assert jarr(BY["بَعْد"]) == (("ب", _A), ("ع", SUKUN), ("د", _I))  # بَعْدِ
    assert mudaf(BY["فَوْق"]) == (("ف", _A), ("و", SUKUN), ("ق", _A))  # فَوْقَ
    assert CONSTANTS["حَيْثُ"] == (("ح", _A), ("ي", SUKUN), ("ث", _U))
    assert hukm(CONSTANTS["حَيْثُ"]).startswith("مقطوع")
    assert hukm(CONSTANTS["لَدَى"]) == "لا تقرؤه الخانة"


def test_mutation_sukun_breaks_licence_not_the_reader() -> None:
    w = set_last(BY["فَوْق"], SUKUN)
    assert not licensed(w) and hukm(w) == "لا تقرؤه الخانة"
    assert set_last((), _A) == ()


def test_masaq_measurement_and_index() -> None:
    import importlib.util
    import sys
    from pathlib import Path

    root = Path(__file__).resolve().parent.parent
    tool = root / "tools" / "gen_zuruf_index.py"
    spec = importlib.util.spec_from_file_location("gen_zuruf_index", tool)
    assert spec and spec.loader
    mod = importlib.util.module_from_spec(spec)
    sys.modules["gen_zuruf_index"] = mod
    spec.loader.exec_module(mod)
    table, total = mod.measure()
    assert total == 1493
    damm_cut = sum(v for (a, _, c), v in table.items() if a == "ضم" and c == "غير مضاف")
    assert damm_cut == 82
    fath_free = sum(v for (a, b, c), v in table.items()
                    if a == "فتح" and b == "—" and c == "غير مضاف")
    assert fath_free == 4
    assert mod.render() == (root / "ZURUF_INDEX.md").read_text(encoding="utf-8")


def test_constants_agree_with_ishara() -> None:
    from slge.ishara import HUNA, THAMMA

    assert CONSTANTS["ثَمَّ"] == THAMMA and CONSTANTS["هُنَا"] == HUNA
