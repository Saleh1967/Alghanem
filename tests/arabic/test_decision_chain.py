"""Tests for the fifteen-position decision chain read off the tree."""

from __future__ import annotations

import json
import pkgutil
from dataclasses import fields
from pathlib import Path

import pytest

import alghanem.kernel as kernel_package
from alghanem.arabic import (
    APPLICATION_STOPS_AT_THE_FOURTH_LINK_NOTE,
    ARABIC_PACKAGE_RELATIVE_PATH,
    GOVERNING_CONSTRAINTS,
    UNIVERSAL_IDEA_IS_ABSENT_NOTE,
    ChainLedger,
    ChainLinkCoding,
    ChainLinkDeclaration,
    ChainLinkReach,
    ChainLinkReading,
    DecisionChainError,
    GoverningConstraint,
    GoverningConstraintStanding,
    read_chain,
    repository_root_path,
)
from alghanem.arabic.external_audit import audit_card

_EXAMPLES = Path(__file__).resolve().parents[2] / "examples" / "external_audit"
_CARDS = ("quru_2_228.yaml", "man_2_255.yaml")


def declaration(**overrides: object) -> ChainLinkDeclaration:
    base: dict[str, object] = {
        "position": 5,
        "label": "٤",
        "title": "الوضع: الدالُّ والمدلولُ معًا، بالنقل وحده",
        "module_relative_path": "wad_naql.py",
        "deferral_law": None,
    }
    base.update(overrides)
    return ChainLinkDeclaration(**base)  # type: ignore[arg-type]


def test_the_chain_holds_exactly_fifteen_successive_positions() -> None:
    ledger = read_chain()
    assert len(ledger.readings) == 15
    assert [item.declaration.position for item in ledger.readings] == list(range(15))
    assert [item.declaration.label for item in ledger.readings][:6] == [
        "٠",
        "١",
        "٢",
        "٣أ",
        "٣ب",
        "٤",
    ]


def test_every_link_naming_a_module_is_read_from_the_tree() -> None:
    root = repository_root_path()
    for reading in read_chain().readings:
        path = reading.declaration.module_path
        if path is None:
            assert reading.coding is ChainLinkCoding.مؤجَّلة_بقانون
            continue
        exists = (root / path).is_file()
        assert reading.is_coded is exists


def test_the_fourth_link_is_coded_by_this_milestone() -> None:
    fourth = next(
        item for item in read_chain().readings if item.declaration.label == "٤"
    )
    assert fourth.declaration.module_relative_path == "wad_naql.py"
    assert fourth.coding is ChainLinkCoding.مُرمَّزة


def test_the_tenth_link_is_coded_by_this_milestone() -> None:
    tenth = next(
        item for item in read_chain().readings if item.declaration.label == "١٠"
    )
    assert tenth.declaration.module_relative_path == "umum_khusus.py"
    assert tenth.coding is ChainLinkCoding.مُرمَّزة


def test_a_tree_without_the_tenth_link_module_reads_it_as_uncoded_not_skipped(
    tmp_path: Path,
) -> None:
    package = tmp_path / ARABIC_PACKAGE_RELATIVE_PATH
    (package / "encoding").mkdir(parents=True)
    (package / "encoding" / "observation.py").write_text("", encoding="utf-8")
    ledger = read_chain(tmp_path)
    tenth = next(item for item in ledger.readings if item.declaration.label == "١٠")
    assert tenth.coding is ChainLinkCoding.حلقة_غير_مُرمَّزة
    assert len(ledger.readings) == 15


def test_the_first_two_links_stay_deferred_by_a_named_constitutional_law() -> None:
    deferred = [
        item
        for item in read_chain().readings
        if item.coding is ChainLinkCoding.مؤجَّلة_بقانون
    ]
    assert [item.declaration.label for item in deferred] == ["١", "٢"]
    assert {item.declaration.deferral_law for item in deferred} == {"KnotNotEssence"}
    constitution = (
        Path(__file__).resolve().parents[2] / "docs" / "CONSTITUTION.md"
    ).read_text(encoding="utf-8")
    assert "KnotNotEssence" in constitution


def test_reach_breaks_at_the_first_unreached_link_and_never_recovers() -> None:
    ledger = read_chain()
    reach = ledger.reach
    assert reach[0] is ChainLinkReach.بالغة
    assert reach[1] is ChainLinkReach.غير_بالغة_بذاتها
    assert all(item is ChainLinkReach.مسبوقة_بحلقة_غير_بالغة for item in reach[2:])
    assert ledger.is_fully_reached is False
    first = ledger.first_unreached
    assert first is not None and first.declaration.label == "١"


def test_a_coded_link_after_a_broken_one_is_not_read_as_reached() -> None:
    ledger = read_chain()
    coded_after_break = [
        (reading, reach)
        for reading, reach in zip(ledger.readings, ledger.reach)
        if reading.is_coded and reading.declaration.position > 1
    ]
    assert coded_after_break
    assert all(
        reach is ChainLinkReach.مسبوقة_بحلقة_غير_بالغة for _, reach in coded_after_break
    )


def test_reach_is_derived_and_is_not_a_field_on_any_type() -> None:
    for declaring_type in (ChainLinkDeclaration, ChainLinkReading, ChainLedger):
        declared = {item.name for item in fields(declaring_type)}
        assert "reach" not in declared


def test_a_link_declares_either_a_module_or_a_deferral_law_never_both() -> None:
    with pytest.raises(DecisionChainError, match="ولا يجتمعان ولا يرتفعان"):
        declaration(deferral_law="KnotNotEssence")
    with pytest.raises(DecisionChainError, match="ولا يجتمعان ولا يرتفعان"):
        declaration(module_relative_path=None)


def test_a_law_deferred_coding_may_not_be_pinned_on_a_link_naming_a_module() -> None:
    with pytest.raises(DecisionChainError, match="يقرأ التصريحَ مكان الشجرة"):
        ChainLinkReading(
            declaration=declaration(),
            coding=ChainLinkCoding.مؤجَّلة_بقانون,
        )


def test_a_module_naming_link_may_not_be_read_as_deferred_nor_the_reverse() -> None:
    with pytest.raises(DecisionChainError, match="يقرأ التصريحَ مكان الشجرة"):
        ChainLinkReading(
            declaration=declaration(module_relative_path=None, deferral_law="X"),
            coding=ChainLinkCoding.حلقة_غير_مُرمَّزة,
        )


def test_a_position_outside_the_fifteen_is_refused() -> None:
    with pytest.raises(DecisionChainError, match="خمسةَ عشرَ موضعًا"):
        declaration(position=15)
    with pytest.raises(DecisionChainError, match="خمسةَ عشرَ موضعًا"):
        declaration(position=-1)


def test_a_link_may_not_name_a_package_assembly_file() -> None:
    with pytest.raises(DecisionChainError, match="ملفَّ تجميعِ حزمة"):
        declaration(module_relative_path="encoding/__init__.py")


def test_a_ledger_with_a_gap_in_its_positions_is_refused() -> None:
    readings = read_chain().readings
    with pytest.raises(DecisionChainError, match="بلا فجوةٍ ولا تكرار"):
        ChainLedger(readings=(readings[0], readings[2]))


def test_one_module_may_serve_two_links() -> None:
    served = [
        item.declaration.module_relative_path
        for item in read_chain().readings
        if item.declaration.module_relative_path is not None
    ]
    assert served.count("manat_verification.py") == 2


def test_an_absent_arabic_package_is_refused_not_read_as_no_modules(
    tmp_path: Path,
) -> None:
    with pytest.raises(DecisionChainError, match="لم تُقرأ الشجرة لأجله"):
        read_chain(tmp_path)


def test_a_tree_without_the_fourth_link_module_reads_it_as_uncoded(
    tmp_path: Path,
) -> None:
    package = tmp_path / ARABIC_PACKAGE_RELATIVE_PATH
    (package / "encoding").mkdir(parents=True)
    (package / "encoding" / "observation.py").write_text("", encoding="utf-8")
    ledger = read_chain(tmp_path)
    fourth = next(item for item in ledger.readings if item.declaration.label == "٤")
    assert fourth.coding is ChainLinkCoding.حلقة_غير_مُرمَّزة
    assert ledger.reach[0] is ChainLinkReach.بالغة


def test_the_two_governing_constraints_are_framework_not_links() -> None:
    assert len(GOVERNING_CONSTRAINTS) == 2
    assert [item.label for item in GOVERNING_CONSTRAINTS] == ["أ", "ب"]
    assert all(item.is_in_the_chain is False for item in GOVERNING_CONSTRAINTS)
    assert all(
        item.standing is GoverningConstraintStanding.مُصرَّح_غير_مُرمَّز
        for item in GOVERNING_CONSTRAINTS
    )


def test_declaring_a_governing_constraint_coded_is_refused_today() -> None:
    with pytest.raises(DecisionChainError, match="ادّعاءُ بناءٍ لم يقع"):
        GoverningConstraint(
            label="أ",
            title="الفكرةُ والطريقةُ والوسيلة",
            question="أهي وسيلةٌ محايدة؟",
            standing=GoverningConstraintStanding.مُرمَّز,
            gap_note=UNIVERSAL_IDEA_IS_ABSENT_NOTE,
        )


def test_the_absent_universal_idea_is_recorded_structurally_not_written() -> None:
    first = GOVERNING_CONSTRAINTS[0]
    assert first.gap_note == UNIVERSAL_IDEA_IS_ABSENT_NOTE
    assert "GFLK" in UNIVERSAL_IDEA_IS_ABSENT_NOTE
    assert "مهمّةٌ مستقلّة" in UNIVERSAL_IDEA_IS_ABSENT_NOTE


def test_the_second_constraint_names_the_link_that_stopped_the_application() -> None:
    """غيابُ القيد (ب) ليس فراغًا نظريًّا كالقيد (أ) بل وقوفٌ عند موضعٍ مُسمًّى."""

    second = GOVERNING_CONSTRAINTS[1]

    assert second.gap_note == APPLICATION_STOPS_AT_THE_FOURTH_LINK_NOTE
    assert second.gap_note != GOVERNING_CONSTRAINTS[0].gap_note
    assert "الناس:٢" in APPLICATION_STOPS_AT_THE_FOURTH_LINK_NOTE
    assert "الحلقة الرابعة" in APPLICATION_STOPS_AT_THE_FOURTH_LINK_NOTE
    assert "TransmissionStanding" in APPLICATION_STOPS_AT_THE_FOURTH_LINK_NOTE
    assert "لا لفراغٍ نظريّ كالقيد (أ)" in APPLICATION_STOPS_AT_THE_FOURTH_LINK_NOTE


def test_no_type_here_carries_a_count_or_verdict_field() -> None:
    for declaring_type in (
        ChainLinkDeclaration,
        ChainLinkReading,
        ChainLedger,
        GoverningConstraint,
    ):
        declared = {item.name.lower() for item in fields(declaring_type)}
        for marker in ("count", "number", "total", "verdict", "birth", "freeze"):
            assert not any(marker in name for name in declared), marker


def test_the_module_reads_no_kernel_authority() -> None:
    source = (
        Path(__file__).resolve().parents[2]
        / "src"
        / "alghanem"
        / "arabic"
        / "decision_chain.py"
    ).read_text(encoding="utf-8")
    imports = tuple(
        line for line in source.splitlines() if line.startswith(("import ", "from "))
    )
    assert imports
    assert not any("kernel" in line for line in imports)


def test_no_kernel_module_reads_this_chain_ledger() -> None:
    for module in pkgutil.walk_packages(
        kernel_package.__path__, prefix="alghanem.kernel."
    ):
        spec = module.module_finder.find_spec(module.name)  # type: ignore[union-attr]
        assert spec is not None and spec.origin is not None
        text = Path(spec.origin).read_text(encoding="utf-8")
        for name in ("decision_chain", "ChainLedger", "read_chain"):
            assert name not in text, (module.name, name)


@pytest.mark.parametrize("card", _CARDS)
def test_this_ledger_changes_no_external_audit_field(card: str) -> None:
    before = json.dumps(
        audit_card(_EXAMPLES / card).to_dict(), ensure_ascii=False, sort_keys=True
    )
    read_chain()
    after = json.dumps(
        audit_card(_EXAMPLES / card).to_dict(), ensure_ascii=False, sort_keys=True
    )
    assert before == after
