"""اختباراتُ بروتوكول شرط العدّ: محفوظٌ بموقعه، ومُلزِمٌ قبل أيّ عدّ."""

from __future__ import annotations

import hashlib
import importlib.util
from pathlib import Path

import pytest

from alghanem.arabic.a116_bridge_licence import MaterialStanding
from alghanem.arabic.counting_precondition_protocol import (
    COUNTING_PROTOCOL_NAMED_RESIDUALS,
    THE_FOUNDING_SITE,
    THE_PROTOCOL_CLAUSES,
    ClauseForce,
    CountingProtocolError,
    CountingStanding,
    DeclaredCount,
    ProtocolBinding,
    count_under_the_protocol,
    importers_of_the_protocol,
    protocol_binding,
    require_the_protocol,
    site_seal_renderings,
    the_block_and_the_freeze_are_untouched,
)

REPO_ROOT = Path(__file__).resolve().parents[2]


def _tree_without_the_site(tmp_path: Path) -> Path:
    """شجرةٌ مُصطنَعةٌ لا موقعَ فيها، ليُفحَص وقوفُ الباب لا ليُعدَّل الأصل."""

    (tmp_path / "src" / "alghanem" / "arabic").mkdir(parents=True)
    return tmp_path


def _tree_with_a_broken_seal(tmp_path: Path) -> Path:
    """شجرةٌ فيها الموقعُ حاضرًا وقد حُرّر متنُه، فكُسر ختمُه."""

    root = _tree_without_the_site(tmp_path)
    site = root / THE_FOUNDING_SITE.relative_path
    site.write_text("# متنٌ محرَّرٌ لا يطابق ختمَه\n", encoding="utf-8")
    return root


# ---------------------------------------------------------------------------
# أوّلًا: الموقعُ محفوظٌ ومختوم
# ---------------------------------------------------------------------------


def test_the_founding_function_site_is_declared_by_path_and_seal() -> None:
    assert (
        THE_FOUNDING_SITE.relative_path
        == "src/alghanem/arabic/imla_founding_function.py"
    )
    assert THE_FOUNDING_SITE.declared_byte_length is not None
    assert THE_FOUNDING_SITE.declared_sha256 is not None


def test_the_declared_seal_is_what_the_disk_measures_now() -> None:
    """الختمُ يُعاد اشتقاقُه من القرص، ولا يُقرأ من حقلٍ مكتوب."""

    raw = (REPO_ROOT / THE_FOUNDING_SITE.relative_path).read_bytes()
    assert len(raw) == THE_FOUNDING_SITE.declared_byte_length
    assert hashlib.sha256(raw).hexdigest() == THE_FOUNDING_SITE.declared_sha256
    measured = site_seal_renderings()
    assert measured["الطول"] == str(THE_FOUNDING_SITE.declared_byte_length)
    assert measured["البصمة"] == THE_FOUNDING_SITE.declared_sha256


def test_an_absent_site_is_named_and_the_door_stops(tmp_path: Path) -> None:
    root = _tree_without_the_site(tmp_path)
    binding = protocol_binding(root)
    assert binding.site_standing is MaterialStanding.ABSENT_FROM_THE_TREE
    assert not binding.holds
    with pytest.raises(CountingProtocolError):
        require_the_protocol(root)


def test_an_edited_site_breaks_its_seal_and_the_door_stops(tmp_path: Path) -> None:
    root = _tree_with_a_broken_seal(tmp_path)
    binding = protocol_binding(root)
    assert binding.site_standing is MaterialStanding.PRESENT_BUT_BREAKS_ITS_SEAL
    assert not binding.holds
    with pytest.raises(CountingProtocolError):
        require_the_protocol(root)


def test_a_broken_site_is_readable_without_raising_so_it_can_be_named(
    tmp_path: Path,
) -> None:
    """القراءةُ لا ترفع خطأً، وإلّا لتعذّر فحصُ المكسور وتسميتُه."""

    reading = protocol_binding(_tree_without_the_site(tmp_path))
    assert isinstance(reading, ProtocolBinding)


# ---------------------------------------------------------------------------
# ثانيًا: الأسبقيّةُ بالبناء لا بالوعد
# ---------------------------------------------------------------------------


def test_the_counter_is_not_called_before_the_protocol_runs(tmp_path: Path) -> None:
    """البابُ الواقفُ لا يستدعي العادَّ ألبتّة؛ فلا يُنتَج رقمٌ قبل الشرط."""

    calls: list[int] = []

    def counter() -> int:
        calls.append(1)
        return 5

    with pytest.raises(CountingProtocolError):
        count_under_the_protocol("عدٌّ لا يمرّ", counter, _tree_without_the_site(tmp_path))
    assert calls == []


def test_the_counter_runs_after_the_protocol_when_the_door_holds() -> None:
    calls: list[int] = []

    def counter() -> int:
        calls.append(1)
        return 5

    declared = count_under_the_protocol("عدٌّ يمرّ", counter)
    assert calls == [1]
    assert declared.value == 5


def test_a_number_handed_in_place_of_a_counter_is_refused() -> None:
    """لو قُبِل الرقمُ لكان قد حُسب قبل البروتوكول، فصار البابُ ختمًا لاحقًا."""

    with pytest.raises(CountingProtocolError):
        count_under_the_protocol("رقمٌ سابق", 5)  # type: ignore[arg-type]


def test_a_counter_that_does_not_yield_an_integer_is_refused() -> None:
    with pytest.raises(CountingProtocolError):
        count_under_the_protocol("عادٌّ معيب", lambda: "سبعة")  # type: ignore[arg-type,return-value]


# ---------------------------------------------------------------------------
# ثالثًا: الإعلانُ مُلزِمٌ والترقيةُ ممنوعة
# ---------------------------------------------------------------------------


def test_a_count_today_comes_out_conditional_with_its_half_named() -> None:
    declared = count_under_the_protocol("وقوعاتٌ مقيسة", lambda: 82_532)
    assert declared.value == 82_532
    assert declared.standing is CountingStanding.CONDITIONAL_ON_A_NAMED_SUSPENSION
    assert not declared.is_licensed
    assert declared.unmet_halves
    assert any("الصوتيّ" in half for half in declared.unmet_halves)


def test_a_conditional_count_without_a_named_half_is_refused() -> None:
    with pytest.raises(CountingProtocolError):
        DeclaredCount(
            name="عددٌ معلَّقٌ بلا تسمية",
            value=1,
            standing=CountingStanding.CONDITIONAL_ON_A_NAMED_SUSPENSION,
            unmet_halves=(),
            site_standing=MaterialStanding.DEPOSITED_AND_SEALED,
        )


def test_a_count_written_licensed_while_a_half_is_suspended_is_refused() -> None:
    with pytest.raises(CountingProtocolError):
        DeclaredCount(
            name="ترقيةٌ ممنوعة",
            value=1,
            standing=CountingStanding.LICENSED_BY_A_MET_PRECONDITION,
            unmet_halves=("النصفُ الصوتيّ: موقوف",),
            site_standing=MaterialStanding.DEPOSITED_AND_SEALED,
        )


def test_a_count_cannot_be_built_while_the_site_is_unsealed() -> None:
    with pytest.raises(CountingProtocolError):
        DeclaredCount(
            name="عددٌ بلا موقعٍ مختوم",
            value=1,
            standing=CountingStanding.CONDITIONAL_ON_A_NAMED_SUSPENSION,
            unmet_halves=("النصفُ الصوتيّ: موقوف",),
            site_standing=MaterialStanding.ABSENT_FROM_THE_TREE,
        )


def test_a_nameless_or_negative_count_is_refused() -> None:
    for name, value in (("", 1), ("عددٌ سالب", -1)):
        with pytest.raises(CountingProtocolError):
            DeclaredCount(
                name=name,
                value=value,
                standing=CountingStanding.CONDITIONAL_ON_A_NAMED_SUSPENSION,
                unmet_halves=("النصفُ الصوتيّ: موقوف",),
                site_standing=MaterialStanding.DEPOSITED_AND_SEALED,
            )


# ---------------------------------------------------------------------------
# رابعًا: الإلزامُ غيرُ الاستيفاء
# ---------------------------------------------------------------------------


def test_the_protocol_binds_today_while_its_precondition_is_unmet() -> None:
    """نفاذُ الإجراء قائمٌ واستيفاءُ المادّة غيرُ قائم، ولا يُقرأ أحدُهما بالآخر."""

    binding = require_the_protocol()
    assert binding.holds
    assert not binding.precondition_is_met
    assert binding.unmet_halves


def test_a_reading_that_claims_a_met_condition_with_unmet_halves_is_refused() -> None:
    with pytest.raises(CountingProtocolError):
        ProtocolBinding(
            site_standing=MaterialStanding.DEPOSITED_AND_SEALED,
            precondition_is_met=True,
            unmet_halves=("النصفُ الصوتيّ: موقوف",),
        )


def test_an_unmet_condition_without_naming_its_halves_is_refused() -> None:
    with pytest.raises(CountingProtocolError):
        ProtocolBinding(
            site_standing=MaterialStanding.DEPOSITED_AND_SEALED,
            precondition_is_met=False,
            unmet_halves=(),
        )


# ---------------------------------------------------------------------------
# خامسًا: البنودُ والشاهد
# ---------------------------------------------------------------------------


def test_the_clauses_are_ordered_from_one_and_distinctly_named() -> None:
    ordinals = [clause.ordinal for clause in THE_PROTOCOL_CLAUSES]
    assert ordinals == list(range(1, len(THE_PROTOCOL_CLAUSES) + 1))
    assert len({clause.name for clause in THE_PROTOCOL_CLAUSES}) == len(ordinals)


def test_the_binding_clauses_are_separated_from_the_witness() -> None:
    binding = require_the_protocol().binding_clauses
    witnesses = [
        clause for clause in THE_PROTOCOL_CLAUSES if clause.force is ClauseForce.WITNESS
    ]
    assert len(binding) == 5
    assert len(witnesses) == 1
    assert set(binding).isdisjoint(witnesses)


def test_a_clause_without_a_rank_or_a_question_is_refused() -> None:
    clause = THE_PROTOCOL_CLAUSES[0]
    with pytest.raises(CountingProtocolError):
        type(clause)(
            ordinal=0, name=clause.name, question=clause.question, force=clause.force
        )
    with pytest.raises(CountingProtocolError):
        type(clause)(ordinal=1, name="  ", question=clause.question, force=clause.force)


def test_the_importers_witness_is_read_from_disk_and_not_frozen() -> None:
    """شاهدٌ يُقرأ ولا يُجمَّد؛ ولا يُقرأ عددُه امتثالًا."""

    importers = importers_of_the_protocol()
    assert isinstance(importers, tuple)
    assert "counting_precondition_protocol" not in importers


def test_an_import_is_not_a_passage_and_the_residual_names_it() -> None:
    joined = "\n".join(COUNTING_PROTOCOL_NAMED_RESIDUALS)
    assert "AN_IMPORT_IS_NOT_A_PASSAGE_THROUGH_THE_DOOR" in joined
    assert "A_BINDING_PROTOCOL_IS_NOT_A_MET_PRECONDITION" in joined


def test_the_session_hook_runs_the_protocol_before_any_test() -> None:
    """موضعُ الإلزام: `tests/conftest.py` يُشغّل البروتوكول عند بدء الجلسة."""

    spec = importlib.util.spec_from_file_location(
        "alghanem_root_conftest", REPO_ROOT / "tests" / "conftest.py"
    )
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    assert module.require_the_protocol is require_the_protocol
    module.pytest_sessionstart(None)


def test_the_session_hook_does_not_swallow_a_stopped_door(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """الخطأُ يُرفَع من الخطّاف ولا يُبتلَع، وإلّا لم يكن إلزامًا."""

    spec = importlib.util.spec_from_file_location(
        "alghanem_root_conftest_stopped", REPO_ROOT / "tests" / "conftest.py"
    )
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)

    def stopped() -> ProtocolBinding:
        raise CountingProtocolError("بابٌ واقفٌ مُصطنَعٌ للفحص")

    monkeypatch.setattr(module, "require_the_protocol", stopped)
    with pytest.raises(CountingProtocolError):
        module.pytest_sessionstart(None)


def test_the_module_claims_no_authority() -> None:
    assert "NO_PROTOCOL_HERE_LIFTS_A_BLOCK_OR_THAWS_A_FREEZE" in (
        the_block_and_the_freeze_are_untouched()
    )
