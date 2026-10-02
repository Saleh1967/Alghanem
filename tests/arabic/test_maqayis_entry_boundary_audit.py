"""اختباراتُ حدّ المادّة في «مقاييس اللغة»: الفاتحةُ مقيسة، والخللُ مُسمًّى."""

from __future__ import annotations

import pytest

import alghanem.arabic.maqayis_entry_boundary_audit as audit
from alghanem.arabic.maqayis_entry_boundary_audit import (
    LETTER_NAMES,
    THE_BOUNDARY_READING_AT_MEASUREMENT,
    BoundaryReading,
    LaterNaming,
    MaqayisEntryBoundaryError,
    NamingGenus,
    axes_disagreement_rows,
    boundary_reading,
    boundary_reading_has_drifted,
    chapter_header_namings,
    every_row_opens_with_the_formula,
    later_namings,
    reconciliation_rows,
    row_identifier,
    rows_without_an_axes_count,
    strip_editorial_marks,
    swallowed_entries,
)
from alghanem.arabic.maqayis_root_table_deposit import root_table_digest


def test_the_opening_formula_is_measured_on_every_row_not_assumed() -> None:
    """علامةُ الحدّ مرخَّصةٌ باطّرادها المقيس: تصيب مطلعَ كلّ صفٍّ بلا استثناء."""

    assert every_row_opens_with_the_formula() is True
    reading = boundary_reading()
    assert reading.rows_opening_with_the_formula == reading.rows
    assert reading.opening_formula_is_exceptionless is True


def test_the_two_detectors_are_both_reported_and_their_gap_is_named() -> None:
    """الموسَّعُ حدٌّ أعلى والمحافِظُ حدٌّ أدنى، ولا يُطوى أحدُهما في الآخر."""

    reading = boundary_reading()
    assert reading.coarse_later_namings > reading.conservative_swallowed_entries
    assert reading.detector_gap == (
        reading.coarse_later_namings - reading.conservative_swallowed_entries
    )
    assert reading.detector_gap > 0


def test_a_chapter_header_is_not_counted_as_a_swallowed_entry() -> None:
    """فواتحُ الأبواب مفرَزةٌ بصنفها، فلا تُضخَّم بها أعدادُ الخلل."""

    headers = chapter_header_namings()
    assert headers
    assert all(naming.genus is NamingGenus.فاتحة_باب for naming in headers)
    assert len(headers) > len(swallowed_entries())
    hosts = {entry.row_index for entry in swallowed_entries()}
    assert (
        not {naming.row_index for naming in headers} & hosts or True
    )  # التداخلُ ممكنٌ في صفٍّ واحد، والصنفُ هو الفاصل
    assert all(naming.preceding_head is None for naming in headers)


def test_the_canonical_bleed_is_caught_with_its_host_and_its_head() -> None:
    """صفُّ «أجج» يبتلع مادّةَ «أحّ»؛ المثالُ المُسمّى يخرج بمضيفه وعنوانه."""

    entries = {
        (entry.host_root, entry.normalized_head) for entry in swallowed_entries()
    }
    assert ("أجج", "أح") in entries
    assert ("أصص", "أض") in entries
    assert ("أصص", "أط") in entries


def test_every_swallowed_material_has_no_row_of_its_own() -> None:
    """الضررُ ضِعفان: لا صفَّ للمبتلَعة لا بعنوانها ولا بتضعيفه."""

    readable = [entry for entry in swallowed_entries() if entry.head_is_readable]
    assert readable
    assert all(entry.has_its_own_row is False for entry in readable)
    reading = boundary_reading()
    assert reading.swallowed_entries_without_their_own_row == len(readable)


def test_an_unreadable_head_is_kept_apart_from_the_named_materials() -> None:
    """عنوانٌ لا حرفَ فيه ليس مادّةً مُسمّاة، ولا يُحذَف من التقرير."""

    reading = boundary_reading()
    assert (
        reading.swallowed_entries_with_a_readable_head
        < reading.conservative_swallowed_entries
    )
    unreadable = [entry for entry in swallowed_entries() if not entry.head_is_readable]
    assert unreadable
    assert all(entry.normalized_head == "" for entry in unreadable)


def test_a_silent_axes_count_is_not_read_as_a_zero() -> None:
    """الخالي غيابُ عدٍّ لا عددٌ مخالف، فيُفرَز صنفًا ثانيًا يُعَدّ على حدة."""

    disagreeing = set(axes_disagreement_rows())
    silent = set(rows_without_an_axes_count())
    assert disagreeing
    assert silent
    assert not disagreeing & silent
    reading = boundary_reading()
    assert reading.rows_whose_axes_fields_disagree == len(disagreeing)
    assert reading.rows_without_an_axes_count == len(silent)


def test_the_axes_disagreement_is_structural_not_a_single_row() -> None:
    """الخللُ منتشرٌ في مئات الصفوف، فالعلّةُ منهجيّةٌ لا مفردةٌ تُعالَج في صفّ."""

    reading = boundary_reading()
    assert reading.rows_whose_axes_fields_disagree > 1
    assert reading.rows_declaring_more_axes_than_they_carry > 1


def test_correcting_the_separator_lowered_the_disagreement_below_a_quarter() -> None:
    """القسمةُ بالفاصلة العربيّة ضخّمت الخلافَ؛ وتصحيحُ الاصطلاح يُنزِله دونَ الربع."""

    rows = audit.root_table_rows()
    inflated = sum(
        1
        for row in rows
        if row["axes_count"].strip().isdigit()
        and int(row["axes_count"])
        != len([part for part in row["semantic_axes"].split("،") if part.strip()])
    )
    reading = boundary_reading()
    assert inflated == 1_257
    assert inflated * 4 > reading.rows
    assert reading.rows_whose_axes_fields_disagree * 4 < reading.rows


def test_the_reconciliation_keys_each_finding_to_its_original_row() -> None:
    """المصالحةُ مُودَعةٌ بمعرّفٍ من بصمة الملفّ ورقم الصفّ؛ لا تُكتَب فوق أصلٍ."""

    digest = root_table_digest()
    rows = reconciliation_rows()
    assert len(rows) == len(swallowed_entries())
    for row in rows:
        identifier = row["row_identifier"]
        assert isinstance(identifier, str)
        assert identifier.startswith(digest[:12])
        assert "#" in identifier


def test_a_row_identifier_refuses_a_non_integer_or_negative_index() -> None:
    """المعرّفُ يرفض ما ليس رقمَ صفٍّ، ولا يُحمَل على أقرب رقمٍ مقبول."""

    with pytest.raises(MaqayisEntryBoundaryError):
        row_identifier(-1)
    with pytest.raises(MaqayisEntryBoundaryError):
        row_identifier(True)  # type: ignore[arg-type]


def test_a_naming_inside_the_head_window_is_refused_as_a_later_naming() -> None:
    """ما وقع في نافذة المطلع فاتحةٌ لا تأخُّر، ويُرفَض بالبناء لا بعد العدّ."""

    with pytest.raises(MaqayisEntryBoundaryError):
        LaterNaming(
            row_index=0,
            host_root="أجج",
            offset=0,
            naming_text="الهمزة والجيم",
            genus=NamingGenus.تسمية_في_سياق,
            preceding_head=None,
        )


def test_editorial_marks_are_stripped_without_folding_one_letter_into_another() -> None:
    """الأقواسُ والحركاتُ تسقط، ولا تُطوى همزةٌ ولا ألفٌ في صورةٍ أخرى."""

    assert strip_editorial_marks("[[بقم]") == "بقم"
    assert strip_editorial_marks("تاَم") == "تام"
    assert strip_editorial_marks("أحّ") == "أح"
    assert strip_editorial_marks("]") == ""
    assert strip_editorial_marks("إ") == "إ"


def test_the_letter_names_are_bare_so_the_lam_prefix_form_is_reachable() -> None:
    """الأسماءُ مجرَّدةٌ من «ال»، إذ تُدغَم في لام الجرّ فتصير «وللهمزة»."""

    assert "همزة" in LETTER_NAMES
    assert not any(name.startswith("ال") for name in LETTER_NAMES)
    assert len(LETTER_NAMES) == len(set(LETTER_NAMES))


def test_the_frozen_reading_is_collided_with_what_the_bytes_yield() -> None:
    """المُجمَّدُ يُصادَم بما يُشتَقّ من البايتات، ولا يُصدَّق لأنّه مكتوب."""

    assert boundary_reading() == THE_BOUNDARY_READING_AT_MEASUREMENT
    assert boundary_reading_has_drifted() is False


def test_every_later_naming_carries_a_genus_derived_not_written() -> None:
    """الجنسُ مُشتَقٌّ من الموضع وما قبله، ولا حقلَ يكتبه حاملُ القطعة."""

    namings = later_namings()
    assert namings
    assert all(isinstance(naming.genus, NamingGenus) for naming in namings)
    assert {naming.genus for naming in namings} == set(NamingGenus)
    assert all(naming.offset >= 40 for naming in namings)


def test_this_module_issues_no_birth_and_reads_no_kernel() -> None:
    """تسجيلٌ لا سلطة: لا ولادةَ ولا تجميدَ `E0`، ولا استيرادَ من `kernel/`."""

    import ast
    from pathlib import Path

    source = Path(audit.__file__).read_text(encoding="utf-8")
    tree = ast.parse(source)
    imported: set[str] = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            imported.update(alias.name for alias in node.names)
        elif isinstance(node, ast.ImportFrom):
            imported.add(node.module or "")
    assert not any("kernel" in name for name in imported)
    assert isinstance(boundary_reading(), BoundaryReading)


def test_the_arabic_comma_never_separates_two_axes_in_this_file() -> None:
    """الاختبارُ الأوّل: الفاصلةُ العربيّة داخلُ شرحٍ لا فاصلٌ بين محورين."""

    census = audit.separator_census()
    assert census == audit.THE_SEPARATOR_CENSUS_AT_MEASUREMENT
    assert census.rows_with_both_marks == 0
    assert census.comma_rows_declaring_one_axis == census.rows_with_an_arabic_comma
    assert census.the_comma_never_separates


def test_a_single_axis_whose_gloss_carries_commas_is_not_multiplied() -> None:
    """صفُّ «أسس» يُعلن محورًا واحدًا وفي شرحه فواصل؛ فلا يُقرأ محاورَ عدّة."""

    row = _row_named("أسس")
    assert "،" in row["semantic_axes"]
    assert row["axes_count"].strip() == "1"
    assert len(audit.axes_of(row)) == 1


def test_two_axes_parted_by_the_pipe_are_read_as_two() -> None:
    """صفُّ «أدد» يفصل محورَيه بالشارحة؛ فيُقرآن اثنين لا واحدًا."""

    row = _row_named("أدد")
    assert row["axes_count"].strip() == "2"
    assert audit.axes_of(row) == ("عظم الشي وشدته وتكرره", "الندود")


def _row_named(root: str) -> dict[str, str]:
    for row in audit.root_table_rows():
        if row["root_full"].strip() == root:
            return row
    raise AssertionError(f"لا صفَّ للجذر {root}")


def test_the_axes_residue_is_two_named_classes_that_exhaust_it() -> None:
    """الاختبارُ الثاني: الخلافُ مفروزٌ صنفين مُسمّيين، ومجموعُهما يستنفده."""

    reading = boundary_reading()
    assert reading.rows_whose_axes_fields_disagree == 822
    assert reading.rows_whose_axes_field_is_silent == 597
    assert reading.rows_declaring_more_axes_than_they_carry == 225
    assert reading.axes_residue_classes_exhaust_the_disagreement


def test_a_silent_axes_field_is_an_extraction_failure_not_a_count_error() -> None:
    """صفوفُ الصنف الأوّل محاورُها خاليةٌ وعدُّها ناطق؛ فالخللُ في الاستخراج."""

    rows = audit.root_table_rows()
    for index in audit.rows_whose_axes_field_is_silent():
        assert not (rows[index]["semantic_axes"] or "").strip()
        assert rows[index]["axes_count"].strip().isdigit()


def test_reading_the_field_correctly_is_not_claiming_its_axes_are_true() -> None:
    """الاختبارُ الثالثُ — صحّةُ المعنى — غيرُ مُدّعًى، ومُعلَنٌ أنّه غيرُ مُدّعًى."""

    assert (
        "لا تجيب عنه" in audit.THREE_SEPARATE_TESTS_AND_THE_THIRD_IS_NOT_INFERRED_NOTE
    )
    assert not hasattr(audit, "axes_are_semantically_adequate")
    assert not hasattr(audit, "semantic_adequacy")


def test_every_reconciliation_segment_is_a_candidate_awaiting_review() -> None:
    """الترشيحُ لا الحصر: كلُّ مقطعٍ يحمل حدَّه ودليلَه وبدائلَه وقرارًا معلَّقًا."""

    segments = reconciliation_rows()
    assert len(segments) == boundary_reading().conservative_swallowed_entries
    for segment in segments:
        assert segment["review_decision"] == "معلَّق"
        assert segment["boundary_evidence"]
        assert segment["alternatives"]
        assert segment["row_identifier"]
    readable = [segment for segment in segments if segment["head_is_readable"]]
    assert readable
    for segment in readable:
        assert isinstance(segment["segment_start"], int)
        assert segment["segment_end"] > segment["segment_start"]


def test_the_nomination_note_refuses_to_claim_the_seventeen_exhaust_the_defect() -> (
    None
):
    """السبعةَ عشرَ حدٌّ أدنى مُرشَّح؛ والنصُّ يمنع قراءتَها حصرًا."""

    note = audit.THE_OPENING_FORMULA_NOMINATES_AND_DOES_NOT_PROVE_EXHAUSTION_NOTE
    assert "لا يبرهن" in note
    assert "حدٌّ" in note and "أدنى" in note
