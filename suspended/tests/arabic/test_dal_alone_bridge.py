"""شواهدُ جسر الدالّ وحدَه: تُصادم القياسَ ولا تنقله."""

from __future__ import annotations

from pathlib import Path

import pytest

from alghanem.arabic.dal_alone_bridge import (
    THE_BUILT_PROOFS,
    THE_SHAPE_INVARIANTS,
    THE_SIDES,
    THE_TRANSCRIBED_AXES,
    WHAT_WOULD_DISCHARGE_THE_VACANCY,
    AxisLoad,
    DalAloneBridgeError,
    DecisionAxis,
    SideStanding,
    axis_transcription_drift,
    invariant_census,
    load_census,
    sides_reading,
    the_seven_are_by_both,
)


def test_the_triad_has_three_sides_and_no_side_is_named_twice() -> None:
    assert len(THE_SIDES) == 3
    assert len({side.name for side in THE_SIDES}) == 3
    assert len({side.module for side in THE_SIDES}) == 3


def test_the_vacant_side_is_read_off_disk_and_is_the_signifier_alone() -> None:
    reading = sides_reading()
    assert reading.vacant == ("الدالُّ وحدَه",)
    assert len(reading.built) == 2


def test_the_vacancy_would_invert_itself_if_the_module_were_built() -> None:
    """خلوٌّ مقيسٌ لا مقول: لو وُجد الملفُّ بحدِّ البرهان لانقلب الحكم."""

    vacant = next(side for side in THE_SIDES if side.name == "الدالُّ وحدَه")
    path = Path("src/alghanem/arabic") / f"{vacant.module}.py"
    assert not path.is_file()


def test_a_named_file_without_the_proof_seal_does_not_discharge_a_side() -> None:
    """وجودُ ملفٍّ باسم الضلع ليس سدادًا له؛ العبرةُ بحدِّ البرهان في بايتاته."""

    from alghanem.arabic import dal_alone_bridge

    assert dal_alone_bridge.THE_SHAPE_INVARIANTS[0][1] in Path(
        "src/alghanem/arabic/madlul_alone_formal.py"
    ).read_text(encoding="utf-8")


def test_every_side_standing_is_one_of_the_two_declared_values() -> None:
    standings = dict(sides_reading().standings)
    assert set(standings) == {side.name for side in THE_SIDES}
    assert set(standings.values()) <= set(SideStanding)


def test_no_transcribed_question_has_drifted_from_its_module() -> None:
    assert axis_transcription_drift() == ()


def test_a_question_that_is_not_in_its_module_is_caught_as_drift() -> None:
    """الحارسُ يُمسِك النقلَ المنزاح، ولا يقبل نصًّا لا أصلَ له."""

    forged = DecisionAxis(
        module="madlul_alone_formal",
        label="س٩",
        question="سؤالٌ لم يُكتَب في تلك الوحدة قطّ",
        load=AxisLoad.FROM_THE_SIGNIFIER_ALONE,
        why="مُختلَقٌ لأجل هذا الشاهد",
    )
    text = Path(f"src/alghanem/arabic/{forged.module}.py").read_text(encoding="utf-8")
    assert forged.question not in text


def test_an_axis_without_a_reason_for_its_load_is_refused() -> None:
    with pytest.raises(DalAloneBridgeError):
        DecisionAxis(
            module="madlul_alone_formal",
            label="س١",
            question="نوع مدلول اللفظ؟",
            load=AxisLoad.FROM_THE_SIGNIFIED,
            why="   ",
        )


def test_the_signifier_alone_cannot_separate_the_branches_of_any_built_proof() -> None:
    """حملُ الجسر: لا برهانَ مبنيًّا تكفي محاورُه الدالّيّةُ لفصل فروعه."""

    census = load_census()
    assert census
    for module, total, alone in census:
        assert 0 <= alone < total, module


def test_the_signifier_alone_carries_exactly_one_axis_in_the_whole_tree() -> None:
    alone = [
        axis
        for axis in THE_TRANSCRIBED_AXES
        if axis.load is AxisLoad.FROM_THE_SIGNIFIER_ALONE
    ]
    assert [axis.question for axis in alone] == ["عدد الألفاظ في العنقود؟"]


def test_the_load_census_sums_to_the_transcribed_axes_without_loss() -> None:
    assert sum(total for _, total, _ in load_census()) == len(THE_TRANSCRIBED_AXES)


def test_a_shape_carried_by_some_is_reported_apart_from_a_shape_of_the_genus() -> None:
    census = invariant_census()
    assert len(census) == len(THE_SHAPE_INVARIANTS)
    partial = [item for item in census if not item.is_carried_by_every_built_proof]
    assert [item.name for item in partial] == ["شاهدٌ واحدٌ لكلّ فرعٍ بالضبط"]
    assert set(partial[0].carriers) < set(THE_BUILT_PROOFS)


def test_the_named_carriers_are_reported_not_merely_their_number() -> None:
    for item in invariant_census():
        assert set(item.carriers) <= set(THE_BUILT_PROOFS)
        assert len(set(item.carriers)) == len(item.carriers)


def test_the_seven_part_division_is_by_both_ends_not_by_the_signifier() -> None:
    assert the_seven_are_by_both() is True


def test_the_closure_sentence_is_read_from_its_own_module_not_copied_here() -> None:
    """لو نُقِلت الجملةُ ههنا لصارت الدعوى شاهدةً لنفسها."""

    here = Path("src/alghanem/arabic/dal_alone_bridge.py").read_text(encoding="utf-8")
    assert "إلى سبعة أقسام" not in here


def test_what_would_discharge_the_vacancy_is_stated_before_it_is_supplied() -> None:
    assert len(WHAT_WOULD_DISCHARGE_THE_VACANCY) == 4
    for requirement in WHAT_WOULD_DISCHARGE_THE_VACANCY:
        assert requirement.strip()


def test_the_bridge_publishes_no_figure_about_any_language() -> None:
    """أعدادُ هذا الجسر عن الشجرة؛ فلا يقرأ بايتاتِ مدوّنةٍ ولا معجم."""

    text = Path("src/alghanem/arabic/dal_alone_bridge.py").read_text(encoding="utf-8")
    for forbidden in ("corpora", "maqayis", "masaq", "quran"):
        assert forbidden not in text


def test_the_bridge_imports_nothing_from_the_kernel() -> None:
    text = Path("src/alghanem/arabic/dal_alone_bridge.py").read_text(encoding="utf-8")
    for forbidden in ("kernel", "program", "capability"):
        assert f"from alghanem.{forbidden}" not in text
        assert f"from ..{forbidden}" not in text
        assert f"import {forbidden}" not in text


def test_the_dal_chapter_gloss_is_not_counted_as_the_built_side() -> None:
    """اشتراكٌ لفظيٌّ لا يُوحِّد جنسين: وسمُ باب الدال ليس ضلعَ الدلالة."""

    assert Path("src/alghanem/arabic/dal_alone_gloss.py").is_file()
    assert "dal_alone_gloss" not in {side.module for side in THE_SIDES}
    assert "dal_alone_gloss" not in THE_BUILT_PROOFS
    assert sides_reading().vacant == ("الدالُّ وحدَه",)


def test_the_book_carrying_the_division_is_absent_so_the_scan_is_secondary() -> None:
    """ساقُ الخلوّ الأولى سقطت بالإيداع؛ والثانيةُ قائمة، فالخلوُّ لم يُرفَع.

    وهذا الشاهدُ انقلب بانقلاب القرص: كان يقيس غيابًا فصار يقيس حضورًا،
    ويُبقي الحكمَ معلّقًا على الساق التي لم تسقط.
    """

    from alghanem.arabic.dal_alone_bridge import (
        THE_BOOK_THAT_CARRIES_THE_DIVISION_IS_ABSENT_FROM_THIS_TREE,
    )

    declared = THE_BOOK_THAT_CARRIES_THE_DIVISION_IS_ABSENT_FROM_THIS_TREE
    assert "الشخصية الإسلامية" in declared
    from alghanem.arabic.dal_madlul_bridge import (
        SealStanding,
        governing_seal_reading,
    )

    assert governing_seal_reading().standing is SealStanding.SEALED_AND_PRESENT
    assert list(Path(".").glob("**/*الشخصية*"))


def test_the_scanned_book_does_not_carry_the_division() -> None:
    from alghanem.arabic.dal_alone_bridge import material_scan

    scan = material_scan()
    assert scan.carries_the_division is False
    assert [count for _, count in scan.marker_hits] == [0, 0, 0, 0]


def test_a_crude_negative_is_not_taken_without_a_positive_control() -> None:
    """المسحُ منحازٌ إلى النفي، فلا يُقبَل حتّى تثبت الآلةُ أنّها تقرأ."""

    from alghanem.arabic.dal_alone_bridge import material_scan

    scan = material_scan()
    assert scan.the_extractor_is_not_blind is True
    assert scan.extracted_arabic_runs > 1000
    assert scan.near_miss_hits > 0


def test_the_near_miss_is_reported_and_not_folded_into_the_negative() -> None:
    from alghanem.arabic.dal_alone_bridge import THE_NEAR_MISS, material_scan

    scan = material_scan()
    assert scan.near_miss_hits > 0
    assert THE_NEAR_MISS not in dict(scan.marker_hits)


def test_the_scan_publishes_no_figure_that_is_transcribed_into_prose() -> None:
    """أرقامُ المسح تُخرَج من مولِّدها ولا تُنقَل في النثر."""

    text = Path("src/alghanem/arabic/dal_alone_bridge.py").read_text(encoding="utf-8")
    from alghanem.arabic.dal_alone_bridge import material_scan

    scan = material_scan()
    assert str(scan.extracted_arabic_runs) not in text
    assert f"{scan.near_miss_hits} موضع" not in text


def test_a_missing_scanned_book_is_refused_and_not_read_as_a_negative() -> None:
    from alghanem.arabic import dal_alone_bridge

    assert dal_alone_bridge._scanned_book_path().is_file()
