"""اختباراتُ قانون الودائع — تؤكّد **الخروقَ صفرًا** لا المقاديرَ أعدادًا.

ولا اختبارَ هنا يُجمّد عددًا من الشجرة، لأنّ الشجرةَ تنمو؛ فما يُؤكَّد إمّا
صفرُ خرقٍ في بوابة، وإمّا بنيةُ قراءةٍ في شاهد، وإمّا خاصّيّةٌ لا تتحرّك بالنموّ.
"""

from __future__ import annotations

import ast
import re
from dataclasses import FrozenInstanceError, fields
from pathlib import Path

import pytest

from alghanem import deposit_law
from alghanem.deposit_law import (
    DEPOSIT_LAW_NAMED_RESIDUALS,
    THE_CORPUS_DOOR,
    THE_GUARD_PREFIXES,
    THE_RESIDUAL_SUFFIX,
    Breach,
    DepositLawError,
    LawReading,
    LawStanding,
    Standing,
    assert_the_gates_hold,
    every_reading,
    gate_readings,
    law_source_root,
    module_paths,
    the_law_holds,
    witness_readings,
)

# ---------------------------------------------------------------------------
# البوّابات: صفرُ خرقٍ، وهو كلُّ ما يُؤكَّد
# ---------------------------------------------------------------------------


def test_every_gate_holds_with_zero_breaches_across_the_whole_tree() -> None:
    for reading in gate_readings():
        listed = [(b.module, b.detail) for b in reading.breaches]
        assert reading.breach_count == 0, f"{reading.name} مخروقة: {listed}"
        assert reading.law_standing is LawStanding.HELD


def test_the_law_holds_and_the_assertion_is_silent() -> None:
    assert the_law_holds() is True
    assert_the_gates_hold() is None


def test_a_gate_examines_something_so_a_zero_is_not_an_empty_sweep() -> None:
    """صفرُ خرقٍ لا يعني شيئًا إن لم يُفحَص شيء؛ فكلُّ بوابةٍ تفحص عددًا موجبًا."""

    for reading in gate_readings():
        assert reading.examined > 0
        assert reading.conformance == pytest.approx(1.0)


def test_there_are_three_gates_and_each_names_a_distinct_question() -> None:
    gates = gate_readings()
    assert len(gates) == 3
    assert len({g.question for g in gates}) == 3


# ---------------------------------------------------------------------------
# الشهود: يُنشَرون بخرقهم، ولا يمنعون
# ---------------------------------------------------------------------------


def test_every_witness_is_currently_uneven_which_is_why_it_is_not_a_gate() -> None:
    """الشاهدُ شاهدٌ لأنّه مخروق؛ ولو قام لوجب أن يُرقّى بوابةً بصراحةٍ في الفرق."""

    witnesses = witness_readings()
    assert witnesses
    for reading in witnesses:
        assert (
            reading.breach_count > 0
        ), f"{reading.name} صار تامًّا — فرقِّه بوابةً بدل تركه شاهدًا"
        assert reading.law_standing is LawStanding.UNEVEN


def test_a_breached_witness_does_not_block_the_law() -> None:
    assert any(r.law_standing is LawStanding.UNEVEN for r in every_reading())
    assert the_law_holds() is True


def test_every_witness_breach_names_its_module_and_its_detail() -> None:
    for reading in witness_readings():
        for breach in reading.breaches:
            assert breach.module.endswith(".py")
            assert breach.detail.strip()


def test_the_residual_dialect_witness_finds_both_dialects_not_one() -> None:
    """الشاهدُ يُعَدّ فرقًا لا عيبًا: اللهجتان كلتاهما مأهولتان اليوم."""

    reading = _named("A_RESIDUAL_CONTAINER_IS_A_MAPPING_FROM_TOKEN_TO_TEXT")
    assert 0 < reading.breach_count < reading.examined


def test_the_corpus_door_witness_is_about_mentions_not_about_reads() -> None:
    """الشاهدُ صريحٌ في أنّه يقيس ذكرَ المسار، لا فتحَ الملفّ؛ فلا يُقرأ أوسعَ منه."""

    reading = _named("THE_CORPUS_IS_REACHED_THROUGH_ITS_ONE_DOOR")
    assert THE_CORPUS_DOOR == "read_quran_corpus_bytes"
    assert reading.examined > 0


# ---------------------------------------------------------------------------
# القانونُ وديعةٌ عند نفسه
# ---------------------------------------------------------------------------


def test_the_law_file_is_inside_its_own_sweep() -> None:
    own = Path(deposit_law.__file__).resolve()
    assert own in {path.resolve() for path in module_paths()}


def test_the_sweep_carries_no_exemption_list_at_all() -> None:
    """قائمةُ الإعفاء هي الطريقُ إلى قانونٍ يصدق لأنّه استثنى مخالفيه."""

    source = Path(deposit_law.__file__).read_text(encoding="utf-8")
    body = source.split('"""', 2)[2]
    for marker in ("EXEMPT", "EXCLUDE", "SKIP_", "WHITELIST", "ALLOWLIST"):
        assert marker not in body


def test_the_law_freezes_no_integer_or_float_magnitude(
    tmp_path: Path,
) -> None:
    """ولا رقمَ مُجمَّدٌ: لا في النصّ، ولا يمرّ الحارسُ على ملفٍّ فيه رقمٌ مُجمَّد."""

    deposit_law._assert_the_law_freezes_no_magnitude()
    source = Path(deposit_law.__file__).read_text(encoding="utf-8")
    body = source.split('"""', 2)[2]
    assert not re.search(r":\s*Final\[(?:int|float)\]", body)
    _ = tmp_path


def test_the_law_stores_no_verdict_field_anywhere() -> None:
    forbidden = {"verdict", "passed", "failed", "ok", "valid", "conformance"}
    for dataclass_type in (Breach, LawReading):
        for field in fields(dataclass_type):
            assert not forbidden & set(field.name.split("_"))
    deposit_law._assert_no_written_verdict_field()


def test_the_verdict_is_derived_from_the_breaches_and_the_standing() -> None:
    held = LawReading("A", "؟", Standing.GATE, 3, ())
    breached = LawReading("B", "؟", Standing.GATE, 3, (Breach("m.py", "د"),))
    uneven = LawReading("C", "؟", Standing.WITNESS, 3, (Breach("m.py", "د"),))
    assert held.law_standing is LawStanding.HELD
    assert breached.law_standing is LawStanding.BREACHED
    assert uneven.law_standing is LawStanding.UNEVEN


def test_the_law_obeys_its_own_residual_gate() -> None:
    """أوّلُ ما يُفحَص به القانونُ نفسُه: بقاياه المسمّاة تسمّي أنفسَها وليست فارغة."""

    assert DEPOSIT_LAW_NAMED_RESIDUALS
    for token, text in DEPOSIT_LAW_NAMED_RESIDUALS.items():
        assert text.startswith(f"{token}:")
        assert len(text.strip()) > len(token) + 1


# ---------------------------------------------------------------------------
# بنيةُ القراءة وحدودُها
# ---------------------------------------------------------------------------


def test_readings_are_frozen_and_cannot_be_edited_after_measurement() -> None:
    reading = every_reading()[0]
    with pytest.raises(FrozenInstanceError):
        reading.examined = 0  # type: ignore[misc]


def test_two_calls_agree_because_nothing_is_cached_and_nothing_is_stored() -> None:
    first = {r.name: r.breach_count for r in every_reading()}
    second = {r.name: r.breach_count for r in every_reading()}
    assert first == second


def test_every_law_name_is_unique_and_every_question_is_arabic_prose() -> None:
    readings = every_reading()
    assert len({r.name for r in readings}) == len(readings)
    for reading in readings:
        assert reading.question.endswith("؟")


def test_a_breach_without_a_module_or_a_detail_is_refused() -> None:
    with pytest.raises(DepositLawError):
        Breach("", "د")
    with pytest.raises(DepositLawError):
        Breach("m.py", "   ")


def test_a_reading_with_more_breaches_than_examined_is_refused() -> None:
    with pytest.raises(DepositLawError):
        LawReading(
            "A", "؟", Standing.GATE, 1, (Breach("a.py", "د"), Breach("b.py", "د"))
        )


def test_conformance_refuses_to_divide_by_an_empty_sweep() -> None:
    with pytest.raises(DepositLawError):
        _ = LawReading("A", "؟", Standing.GATE, 0, ()).conformance


def test_both_standings_are_inhabited_so_the_distinction_is_not_decorative() -> None:
    deposit_law._assert_every_law_is_named_and_placed()
    assert {r.standing for r in every_reading()} == set(Standing)


# ---------------------------------------------------------------------------
# المسحُ نفسُه
# ---------------------------------------------------------------------------


def test_the_sweep_reaches_the_arabic_layer_and_the_kernel_alike() -> None:
    names = {p.relative_to(law_source_root()).as_posix() for p in module_paths()}
    assert any(n.startswith("arabic/") for n in names)
    assert any(n.startswith("kernel/") for n in names)
    assert not any(n.endswith("__init__.py") for n in names)


def test_the_guard_prefixes_are_the_ones_the_tree_actually_uses() -> None:
    """البادئتان مقيستان من الشجرة لا مُختارتان؛ ولو كانتا خطأً لخلا العدّ."""

    found = 0
    for path in module_paths():
        tree = ast.parse(path.read_text(encoding="utf-8"))
        found += sum(
            1
            for node in tree.body
            if isinstance(node, ast.FunctionDef)
            and node.name.startswith(THE_GUARD_PREFIXES)
        )
    assert found > 0


def test_the_residual_suffix_is_the_one_the_tree_actually_uses() -> None:
    carriers = [
        p
        for p in module_paths()
        if THE_RESIDUAL_SUFFIX in p.read_text(encoding="utf-8")
    ]
    assert len(carriers) > 1


def test_the_law_imports_no_authority_from_kernel_or_program() -> None:
    """خمولٌ سلطويّ: القانونُ يقرأ النصَّ ويعُدّ، ولا يستورد ولادةً ولا حكمًا."""

    source = Path(deposit_law.__file__).read_text(encoding="utf-8")
    tree = ast.parse(source)
    for node in ast.walk(tree):
        if isinstance(node, ast.ImportFrom) and node.module:
            assert not node.module.startswith(("alghanem.kernel", "alghanem.program"))
        if isinstance(node, ast.Import):
            for alias in node.names:
                assert not alias.name.startswith(
                    ("alghanem.kernel", "alghanem.program")
                )


def _named(name: str) -> LawReading:
    for reading in every_reading():
        if reading.name == name:
            return reading
    raise AssertionError(f"لا قانونَ باسم {name}")
