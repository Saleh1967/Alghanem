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
    GRADUATION_EXAM_ABSENCE_GUARDS_NOTE,
    GRADUATION_EXAM_MATERIAL_REFERENCE,
    OUT_OF_TREE_MARKER,
    THE_EXAM_KEEPS_ITS_DECISION_NUMBER_SO_LABELS_NO_LONGER_ASCEND_NOTE,
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


def test_the_chain_holds_exactly_sixteen_successive_positions() -> None:
    ledger = read_chain()
    assert len(ledger.readings) == 16
    assert [item.declaration.position for item in ledger.readings] == list(range(16))
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


def test_the_eleventh_link_is_coded_by_this_milestone() -> None:
    eleventh = next(
        item for item in read_chain().readings if item.declaration.label == "١١"
    )
    assert eleventh.declaration.module_relative_path == "umum_khusus.py"
    assert eleventh.coding is ChainLinkCoding.مُرمَّزة


def test_a_tree_without_the_eleventh_link_module_reads_it_as_uncoded_not_skipped(
    tmp_path: Path,
) -> None:
    package = tmp_path / ARABIC_PACKAGE_RELATIVE_PATH
    (package / "encoding").mkdir(parents=True)
    (package / "encoding" / "observation.py").write_text("", encoding="utf-8")
    ledger = read_chain(tmp_path)
    eleventh = next(item for item in ledger.readings if item.declaration.label == "١١")
    assert eleventh.coding is ChainLinkCoding.حلقة_غير_مُرمَّزة
    assert len(ledger.readings) == 16


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


def test_a_position_outside_the_sixteen_is_refused() -> None:
    with pytest.raises(DecisionChainError, match="ستةَ عشرَ موضعًا"):
        declaration(position=16)
    with pytest.raises(DecisionChainError, match="ستةَ عشرَ موضعًا"):
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


def test_the_governing_constraints_are_framework_not_links() -> None:
    assert len(GOVERNING_CONSTRAINTS) == 3
    assert [item.label for item in GOVERNING_CONSTRAINTS] == ["أ", "ب", "٧"]
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


def test_the_graduation_exam_sits_at_its_declared_position_and_shifts_no_position() -> (
    None
):
    """موضعُ الامتحان آخرَ السلسلة، ولم يُزِح موضعًا واحدًا؛ والمتحرّكُ الأرقام."""

    readings = read_chain().readings
    exam = readings[-1]

    assert exam.declaration.position == 15
    assert exam.declaration.label == "٧"
    assert exam.declaration.title.startswith("امتحانُ التخرّج")
    assert [item.declaration.label for item in readings[:15]] == [
        "٠",
        "١",
        "٢",
        "٣أ",
        "٣ب",
        "٤",
        "٥",
        "٦",
        "٨",
        "٩",
        "١٠",
        "١١",
        "١٢",
        "١٣",
        "١٤",
    ]


def test_the_exam_names_one_material_bound_outside_this_tree_and_only_one() -> None:
    """مادّتُه مُصدِّرُ hamil، وهو وحده الموصولُ خارجَ الشجرة."""

    bound = [
        item for item in read_chain().readings if item.declaration.is_bound_out_of_tree
    ]

    assert len(bound) == 1
    assert (
        bound[0].declaration.module_relative_path == GRADUATION_EXAM_MATERIAL_REFERENCE
    )
    assert "hamil" in GRADUATION_EXAM_MATERIAL_REFERENCE
    assert "induction/export_seals.py" in GRADUATION_EXAM_MATERIAL_REFERENCE


def test_the_bound_link_manufactures_no_dead_relative_path_in_this_tree() -> None:
    """العقدُ الارتباطُ بالمخرج، فلا يُنسَب المرجعُ إلى حزمة العربية."""

    exam = read_chain().readings[-1]
    path = exam.declaration.module_path

    assert path is not None
    assert path.startswith(OUT_OF_TREE_MARKER)
    assert not path.startswith(ARABIC_PACKAGE_RELATIVE_PATH)
    assert not (repository_root_path() / path).exists()


def test_a_bound_link_is_uncoded_by_its_mark_and_not_by_a_missing_file(
    tmp_path: Path,
) -> None:
    """ولو وُجد في الشجرة ملفٌّ بذلك الاسم لم يُقرأ الموصولُ مُرمَّزًا."""

    package = tmp_path / ARABIC_PACKAGE_RELATIVE_PATH
    package.mkdir(parents=True)
    forged = package / GRADUATION_EXAM_MATERIAL_REFERENCE.replace("/", "_")
    forged.write_text("", encoding="utf-8")

    exam = read_chain(tmp_path).readings[-1]

    assert exam.coding is ChainLinkCoding.حلقة_غير_مُرمَّزة
    assert exam.is_coded is False


def test_a_bound_reference_with_nothing_after_the_mark_is_refused() -> None:
    with pytest.raises(DecisionChainError, match="مرجعُ المُصدِّر الموصول"):
        declaration(module_relative_path=OUT_OF_TREE_MARKER + "   ")


def test_the_third_constraint_carries_the_three_absence_guards_as_prose() -> None:
    """ثلاثةُ شروط الغياب نصٌّ في `gap_note` لا عدّادٌ ولا حكم."""

    third = GOVERNING_CONSTRAINTS[2]

    assert third.label == "٧"
    assert third.is_in_the_chain is False
    assert third.standing is GoverningConstraintStanding.مُصرَّح_غير_مُرمَّز
    assert third.gap_note == GRADUATION_EXAM_ABSENCE_GUARDS_NOTE
    assert third.gap_note != GOVERNING_CONSTRAINTS[0].gap_note
    assert third.gap_note != GOVERNING_CONSTRAINTS[1].gap_note
    for fragment in ("**(١)**", "**(٢)**", "**(٣)**"):
        assert fragment in GRADUATION_EXAM_ABSENCE_GUARDS_NOTE
    assert "ast" in GRADUATION_EXAM_ABSENCE_GUARDS_NOTE
    assert "02_tariqa_aqliyya" in GRADUATION_EXAM_ABSENCE_GUARDS_NOTE


def test_the_third_constraint_asks_after_a_result_written_in_neither_end() -> None:
    third = GOVERNING_CONSTRAINTS[2]

    assert "لم تكن" in third.question and "مكتوبةً في طرفٍ منهما" in third.question
    assert "mirror.py" in third.question
    assert "deposit_law.verdict" in third.question


def test_the_exam_carries_its_decision_number_and_the_labels_stop_ascending() -> None:
    """الامتحانُ رقمُه `٧` في آخر المواضع، فالأرقامُ لم تعد تتصاعد مع المواضع."""

    labels = [item.declaration.label for item in read_chain().readings]

    assert labels[-1] == "٧"
    assert labels[8:15] == ["٨", "٩", "١٠", "١١", "١٢", "١٣", "١٤"]
    assert labels[:8] == ["٠", "١", "٢", "٣أ", "٣ب", "٤", "٥", "٦"]
    assert len(set(labels)) == len(labels)
    assert "الأرقامُ لم تعد تتصاعد" in (
        THE_EXAM_KEEPS_ITS_DECISION_NUMBER_SO_LABELS_NO_LONGER_ASCEND_NOTE
    )


def test_the_exam_and_its_governing_constraint_carry_one_number_not_two() -> None:
    """الرقمُ `٧` على الحلقة وعلى قيدها الحاكم معًا، مقصودًا ومحروسًا."""

    exam = read_chain().readings[-1]

    assert exam.declaration.label == GOVERNING_CONSTRAINTS[-1].label
    assert [item.label for item in GOVERNING_CONSTRAINTS].count("٧") == 1
    assert (
        sum(1 for item in read_chain().readings if item.declaration.label == "٧") == 1
    )
