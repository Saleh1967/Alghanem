"""اختبارُ وثيقة الأصول: أبوابُها خمسةَ عشر، ومواضعُها تُفتَح، ولا رقمَ فيها."""

from __future__ import annotations

import importlib.util
import re
import sys
from pathlib import Path
from types import ModuleType

import pytest

from alghanem.seals import SealError, SealGenus

REPO_ROOT = Path(__file__).resolve().parents[2]
GATE_PATH = REPO_ROOT / "tools" / "regen_all.py"
DOCUMENT = REPO_ROOT / "docs" / "USOOL_AL-UNBOOB.md"
CODE_SPAN = re.compile(r"`[^`]*`")
ARABIC_INDIC = "٠١٢٣٤٥٦٧٨٩"


def _load_gate() -> ModuleType:
    spec = importlib.util.spec_from_file_location("regen_all", GATE_PATH)
    if spec is None or spec.loader is None:
        raise RuntimeError("لا تُحمَّل البوّابةُ من مسارها.")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


gate = _load_gate()


def test_the_fifteen_doors_are_read_and_each_site_is_on_disk() -> None:
    doors = gate._usool_doors()
    assert doors["الأبوابُ المقروءة"] == "15"
    sites = [value for key, value in doors.items() if key.startswith("باب: ")]
    assert len(sites) == 15
    for site in sites:
        assert (REPO_ROOT / site).is_file(), site


def test_a_vanished_site_is_named_and_not_swallowed(tmp_path: Path) -> None:
    forged = tmp_path / "USOOL_AL-UNBOOB.md"
    forged.write_text(
        "## بابٌ مُصطنَع\n\n> **موضعُه في الشجرة:** `src/alghanem/لا_وجودَ_له.py`\n",
        encoding="utf-8",
    )
    original = gate.USOOL_DOCUMENT
    gate.USOOL_DOCUMENT = forged
    try:
        doors = gate._usool_doors()
    finally:
        gate.USOOL_DOCUMENT = original
    assert doors["باب: بابٌ مُصطنَع"] == "موضعٌ غائبٌ عن الشجرة"


def test_a_document_without_a_single_door_is_refused(tmp_path: Path) -> None:
    empty = tmp_path / "USOOL_AL-UNBOOB.md"
    empty.write_text("نثرٌ بلا بابٍ يُسمّي موضعَه.\n", encoding="utf-8")
    original = gate.USOOL_DOCUMENT
    gate.USOOL_DOCUMENT = empty
    try:
        with pytest.raises(SealError):
            gate._usool_doors()
    finally:
        gate.USOOL_DOCUMENT = original


def test_the_document_carries_no_figure_that_could_be_transcribed() -> None:
    """وثيقةُ أصولٍ لا وديعة: ليس فيها عددٌ يُنقَل، فأعدادُها بحروفها."""

    prose = CODE_SPAN.sub("", DOCUMENT.read_text(encoding="utf-8"))
    stray = [mark for mark in prose if mark.isdigit() or mark in ARABIC_INDIC]
    assert stray == []


def test_a_code_span_that_is_only_digits_is_a_transcribed_figure_in_disguise() -> None:
    """ثغرةُ الحارس الأولى: الاستثناءُ للمسارات والمعرّفات لا للأعداد العارية."""

    spans = CODE_SPAN.findall(DOCUMENT.read_text(encoding="utf-8"))
    bare = [
        span
        for span in spans
        if span.strip("`").strip()
        and all(
            mark.isdigit() or mark in ARABIC_INDIC or mark in " ,_"
            for mark in span.strip("`")
        )
    ]
    assert bare == [], bare


def test_the_document_declares_itself_a_methodological_correspondence() -> None:
    text = DOCUMENT.read_text(encoding="utf-8")
    assert "مقابلةٌ منهجية" in text
    assert "لا تطبيقٌ فقهيّ" in text
    assert "جدولُ التشبيهاتِ المقيسة" in text


def test_the_table_claims_a_likeness_of_effect_and_never_an_identity() -> None:
    """حدُّ الباب الخامس عشر: يُدَّعى أثرُ الأصل لا ماهيتُه."""

    text = DOCUMENT.read_text(encoding="utf-8")
    assert "تشبيهٌ بالأثر" in text
    assert "أثرُه أثرُ" in text
    assert "التطابقُ حرفيّ" not in text
    assert "جدولُ المقابلات" not in text


def test_the_document_is_sealed_as_an_epistemic_witness_and_never_collided() -> None:
    verdicts = [
        verdict
        for verdict in gate.the_registry().collide_all()
        if verdict.seal.name == "usool_al_unboob.doors"
    ]
    assert len(verdicts) == 1
    verdict = verdicts[0]
    assert verdict.seal.genus is SealGenus.EPISTEMIC_WITNESS
    assert verdict.readings
    assert verdict.discrepancies == ()


def test_the_gate_carries_no_second_copy_of_the_document_fingerprint() -> None:
    fingerprint = gate._usool_doors()["بصمةُ الوثيقة"]
    assert fingerprint not in GATE_PATH.read_text(encoding="utf-8")
