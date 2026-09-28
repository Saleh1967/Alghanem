"""شواهدُ حراسة امتحان التخرّج: شروطُ الغياب تجري فعلًا لا تُقال.

والمقصودُ ههنا أمران: أنّ النسخة المودَعة تُرفَض مادّةً باشتقاقٍ من بنيتها،
وأنّ حارسَ المسّ يُسمّي مسّةَ البانِي بموضعها؛ وأنّ شيئًا من ذلك لا يرفع
الحلقةَ `٧` من `حلقة_غير_مُرمَّزة`.
"""

import ast
from pathlib import Path

import pytest

from alghanem.arabic import read_chain
from alghanem.arabic.decision_chain import ChainLinkCoding
from alghanem.arabic.graduation_exam_readiness import (
    EXAM_MATERIAL_SEAL_CLASS,
    GRADUATION_EXAM_NAMED_RESIDUALS,
    THE_EXPORTER_OUTPUT_RELATIVE_PATH,
    THE_EXPORTING_REPOSITORY,
    THE_RUNG_ORDER,
    ExamRung,
    GraduationExamReadinessError,
    RungStanding,
    exporter_is_present_at_its_place,
    read_deposited_copy,
    repository_root_path,
    source_touches_in,
    the_first_unmet_rung,
    the_rung_readings,
)


def test_the_deposited_copy_carries_no_seal_of_the_material_class() -> None:
    """المودَعُ لا يحمل صنفَ المادّة، فامتناعُه مقروءٌ من بنيته لا مُدَّعًى."""

    reading = read_deposited_copy()

    assert EXAM_MATERIAL_SEAL_CLASS not in reading.classes_present
    assert reading.carries_the_material_class is False
    assert reading.is_refused_as_material is True


def test_the_refusal_names_the_shape_it_read_and_not_a_date() -> None:
    """الأصنافُ المقروءةُ تُسمّى، فالرفضُ مسنودٌ إلى بنيةٍ لا إلى يومِ أخذ."""

    reading = read_deposited_copy()

    assert reading.classes_present
    assert all(
        seal_class != EXAM_MATERIAL_SEAL_CLASS for seal_class in reading.classes_present
    )
    assert reading.relative_path.endswith("seals.json")


def test_a_deposit_that_did_carry_the_material_class_would_not_be_refused(
    tmp_path: Path,
) -> None:
    """والرفضُ مشروطٌ لا مطلق: وديعةٌ تحمل الصنفَ لا تُرفَض بهذا الحكم."""

    exhibit = tmp_path / "exhibits" / "hamil-induction"
    exhibit.mkdir(parents=True)
    (exhibit / "seals.json").write_text(
        '{"سجلُّ_الأختام": {"أختام": [{"صنف": "[بوّابة]"}]}}',
        encoding="utf-8",
    )

    reading = read_deposited_copy(tmp_path)

    assert reading.carries_the_material_class is True
    assert reading.is_refused_as_material is False


def test_a_deposit_absent_from_disk_is_named_and_not_read_as_empty(
    tmp_path: Path,
) -> None:
    """غيابُ المعروض يُسمّى رفضًا، ولا يُقرأ وديعةً فارغةً تجتاز صامتة."""

    with pytest.raises(GraduationExamReadinessError):
        read_deposited_copy(tmp_path)


def test_the_guard_names_every_touch_of_source_text_with_its_line() -> None:
    """حارسُ المسّ يُسمّي كلَّ مسّةٍ بموضعها من نصّ البانِي."""

    touches = source_touches_in(
        "import inspect\n"
        "def build(path):\n"
        "    inspect.getsource(build)\n"
        "    return open('induction/export_seals.py').read()\n"
    )

    assert [touch.call_name for touch in touches] == ["getsource", "open"]
    assert [touch.line for touch in touches] == [3, 4]
    assert all(touch.reason.strip() for touch in touches)


def test_a_builder_that_reads_only_the_output_is_not_flagged() -> None:
    """والبانِي الذي يقرأ المخرجَ وحدَه لا يُتَّهم: الحارسُ يفرّق ولا يعمّ."""

    touches = source_touches_in(
        "import json\n"
        "def build(path):\n"
        "    return json.loads((path / 'induction/seals.json').read_text())\n"
    )

    assert touches == ()


def test_the_exporter_is_not_present_and_it_is_the_first_unmet_rung() -> None:
    """الدرجةُ الأولى غيرُ مستوفاة، وهي وحدَها البابُ الذي يقف عنده البناء."""

    assert exporter_is_present_at_its_place() is False
    assert the_first_unmet_rung() is ExamRung.EXPORTER_PRESENT_AT_ITS_PLACE


def test_what_lies_past_the_stop_is_unexamined_and_never_read_as_met() -> None:
    """وما بعد الوقوف `غيرُ منظورٍ فيه`، فلا يُقرأ مستوفًى ولا غيرَ مستوفًى."""

    readings = the_rung_readings()

    assert [rung for rung, _ in readings] == list(THE_RUNG_ORDER)
    assert readings[0][1] is RungStanding.غير_مستوفاة
    assert all(standing is RungStanding.غير_منظور_فيها for _, standing in readings[1:])


def test_a_checkout_inside_this_tree_is_refused_as_a_copy_not_a_place(
    tmp_path: Path,
) -> None:
    """وموضعٌ داخلَ هذه الشجرة نسخةٌ لا موضع، فيُرفَض باسمه لا يُقبَل صامتًا."""

    del tmp_path

    with pytest.raises(GraduationExamReadinessError):
        exporter_is_present_at_its_place(repository_root_path() / "exhibits")


def test_an_outside_checkout_holding_the_output_meets_the_first_rung(
    tmp_path: Path,
) -> None:
    """والدرجةُ الأولى تُستوفى بمخرجٍ في موضعه، فالوقوفُ مشروطٌ لا مؤبَّد."""

    (tmp_path / "induction").mkdir()
    (tmp_path / THE_EXPORTER_OUTPUT_RELATIVE_PATH).write_text("{}", encoding="utf-8")

    assert exporter_is_present_at_its_place(tmp_path) is True
    assert the_first_unmet_rung(tmp_path) is (
        ExamRung.ABSENCE_GUARD_RUNS_OVER_THE_BUILDER
    )


def test_this_module_does_not_lift_the_exam_link_out_of_being_uncoded() -> None:
    """وجودُ الحارس لا يرفع الحلقةَ `٧`: الوصلُ الخارجيُّ حكمُها لا وجودُ ملفّ."""

    exam = read_chain().readings[-1]

    assert exam.declaration.label == "٧"
    assert exam.coding is ChainLinkCoding.حلقة_غير_مُرمَّزة
    assert exam.declaration.is_bound_out_of_tree is True


def test_no_figure_from_the_exporter_is_written_into_this_module() -> None:
    """ولا رقمَ يعبر: نصُّ الوحدة خالٍ من كلّ عددٍ منقولٍ عن ذاك المستودع."""

    source = (
        repository_root_path()
        / "src"
        / "alghanem"
        / "arabic"
        / "graduation_exam_readiness.py"
    ).read_text(encoding="utf-8")

    literals = {
        node.value
        for node in ast.walk(ast.parse(source))
        if isinstance(node, ast.Constant)
        and isinstance(node.value, int)
        and not isinstance(node.value, bool)
    }

    assert literals == {len(THE_RUNG_ORDER)}
    assert THE_EXPORTING_REPOSITORY in source


def test_every_named_residual_is_keyed_by_its_own_name() -> None:
    """البقايا تُقرأ بأسمائها، وكلُّ نصٍّ يبدأ باسمه فلا يُقتبَس مقطوعًا."""

    for name, text in GRADUATION_EXAM_NAMED_RESIDUALS.items():
        assert text.startswith(f"{name}: ")
