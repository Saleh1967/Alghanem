"""اختبارُ البوّابة نفسِها: أتصادِم فعلًا، وتُسمّي، ولا تحمل نسخةً ثانية؟"""

from __future__ import annotations

import importlib.util
import sys
from pathlib import Path
from types import ModuleType

from alghanem.seals import SealGenus

REPO_ROOT = Path(__file__).resolve().parents[2]
GATE_PATH = REPO_ROOT / "tools" / "regen_all.py"


def _load_gate() -> ModuleType:
    spec = importlib.util.spec_from_file_location("regen_all", GATE_PATH)
    if spec is None or spec.loader is None:
        raise RuntimeError("لا تُحمَّل البوّابةُ من مسارها.")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


gate = _load_gate()


def test_no_guarded_figure_has_drifted_from_its_generator() -> None:
    drifted = [
        (verdict.seal.name, reading.field, reading.transcribed, reading.measured)
        for verdict in gate.the_registry().collide_all()
        for reading in verdict.discrepancies
    ]
    assert drifted == []


def test_the_gate_returns_zero_only_when_nothing_drifted() -> None:
    assert gate.main(["--check"]) == 0


def test_every_seal_is_named_by_one_of_the_three_genera() -> None:
    tally = gate.the_registry().genera()
    assert tally[SealGenus.GENERATED] >= 1
    assert tally[SealGenus.TRANSCRIBED] >= 1
    assert tally[SealGenus.QUOTED] >= 1


def test_a_quoted_witness_is_listed_and_never_collided() -> None:
    quoted = [
        verdict
        for verdict in gate.the_registry().collide_all()
        if verdict.seal.genus is SealGenus.QUOTED
    ]
    assert quoted
    for verdict in quoted:
        assert verdict.readings
        assert verdict.discrepancies == ()


def test_the_gate_carries_no_second_copy_of_any_guarded_figure() -> None:
    text = GATE_PATH.read_text(encoding="utf-8")
    for figure in ("82,427", "17,864", "8114640", "1.465"):
        assert figure not in text


def test_a_named_difference_is_rendered_and_not_swallowed() -> None:
    from alghanem.seals import Seal, SealVerdict

    seal = Seal(
        name="فارقٌ مُصطنَع",
        genus=SealGenus.GENERATED,
        origin="اختبار",
        generate=lambda: {"حقل": "2"},
        transcription=lambda: {"حقل": "1"},
    )
    verdict = SealVerdict(seal=seal, readings=seal.collide())
    rendered = "\n".join(gate.render((verdict,)))
    assert "حقل" in rendered
    assert "1" in rendered and "2" in rendered
    assert verdict.discrepancies
