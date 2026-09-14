"""اختباراتُ تسجيل قوانين الابتداء والوصل والوقف: تُشغِّل القراءةَ لا تصفُها."""

from __future__ import annotations

import pytest

from alghanem.arabic.alif_state_raw_count import SHORT_VOWELS
from alghanem.arabic.fatiha_source_text import FATIHA_LINES, FATIHA_SOURCE_ID
from alghanem.arabic.ibtida_wasl_waqf_registration import (
    IBTIDA_WASL_WAQF_NAMED_RESIDUALS,
    SHADDA,
    SUBMITTED_CLAIM_POPULATION_ID,
    SUBMITTED_FREEZE_IDENTIFIER,
    SUKUN,
    THE_THREE_LAWS,
    AdjacencyShape,
    FirstStateReading,
    IbtidaReadingTable,
    IbtidaWaslWaqfError,
    LawStanding,
    SubmittedFreezeStanding,
    SuppliedLaw,
    derive_submitted_freeze_standing,
    read_ibtida_on_the_deposited_fatiha,
    read_ibtida_positions,
    scan_quiescence_adjacency,
    scan_quiescence_adjacency_on_the_deposited_fatiha,
)
from alghanem.program import REPORTED_UNVERIFIED_FIGURES

_FATHA, _DAMMA, _KASRA = SHORT_VOWELS


# --- نصُّ القوانين: مُسجَّلٌ بمنزلته الدنيا، والأعلى غيرُ مبلوغة ----------------


def test_the_three_laws_are_registered_with_their_words_and_their_formal_text() -> None:
    assert len(THE_THREE_LAWS) == 3
    assert [law.key for law in THE_THREE_LAWS] == ["الابتداء", "الوصل", "الوقف"]
    for law in THE_THREE_LAWS:
        assert law.statement.strip()
        assert law.formal_text.strip()
        assert law.standing is LawStanding.MUWRADA_BILA_MASDARIN_MUSAMMA


def test_a_higher_standing_is_unreachable_because_no_source_was_named() -> None:
    assert len(LawStanding) == 3
    for standing in (
        LawStanding.MUQABALA_BI_TABA_MUSAMMAT,
        LawStanding.MIN_MASDARIN_MUSAMMAN_GHAYR_MUQABAL,
    ):
        with pytest.raises(IbtidaWaslWaqfError):
            SuppliedLaw(
                key="الابتداء",
                statement="نصٌّ",
                formal_text="صيغةٌ",
                standing=standing,
            )


# --- قراءةُ الابتداء: تُشغَّل الآن على النصّ المُودَع وحدَه --------------------


def test_the_reading_covers_every_written_word_of_the_deposited_text() -> None:
    table = read_ibtida_on_the_deposited_fatiha()
    assert table.source_id == FATIHA_SOURCE_ID
    assert len(table.rows) == sum(len(line.split()) for line in FATIHA_LINES)


def test_every_position_falls_in_exactly_one_of_the_four_readings() -> None:
    table = read_ibtida_on_the_deposited_fatiha()
    counted = sum(len(table.rows_read_as(reading)) for reading in FirstStateReading)
    assert counted == len(table.rows)
    assert len(FirstStateReading) == 4


def test_no_position_in_the_deposited_text_begins_with_a_written_sukun() -> None:
    table = read_ibtida_on_the_deposited_fatiha()
    assert table.positions_beginning_with_a_written_sukun == ()


def test_the_hamzat_wasl_positions_are_undecidable_not_admitted() -> None:
    """ألفُ «الْحَمْدُ» و«اهْدِنَا» لا حالةَ مكتوبةَ لها، فلا تُعَدّ موافقةً."""
    table = read_ibtida_on_the_deposited_fatiha()
    undecided = {row.word for row in table.positions_with_no_written_state}
    assert "الْحَمْدُ" in undecided
    assert "اهْدِنَا" in undecided
    assert len(table.decidable_positions) < len(table.rows)


def test_almost_half_the_positions_are_beyond_this_instrument() -> None:
    table = read_ibtida_on_the_deposited_fatiha()
    assert len(table.positions_with_no_written_state) == 14
    assert len(table.decidable_positions) == 15


def test_a_written_sukun_at_the_start_is_read_as_a_violation_shape() -> None:
    """لو ورد ابتداءٌ بسكونٍ مكتوبٍ لقُرئ مخالفةً، فالقراءةُ قابلةٌ للتكذيب."""
    table = read_ibtida_positions(["لْيَقْطَعْ"], source_id="سطرٌ-للاختبار")
    assert len(table.positions_beginning_with_a_written_sukun) == 1


def test_a_vowelled_first_carrier_is_read_as_compliant() -> None:
    table = read_ibtida_positions(["بِسْمِ"], source_id="سطرٌ-للاختبار")
    assert table.rows[0].reading is FirstStateReading.YABDA_BI_HARAKA


def test_the_reading_table_refuses_a_blank_source_id() -> None:
    with pytest.raises(IbtidaWaslWaqfError):
        IbtidaReadingTable(source_id="   ", rows=())


# --- مسحُ التجاور: ما تراه العلاماتُ لا ما يُقرأ في اللفظ ----------------------


def test_no_pair_of_written_sukuns_is_found_in_the_deposited_text() -> None:
    scan = scan_quiescence_adjacency_on_the_deposited_fatiha()
    assert scan.written_sukun_pairs == ()


def test_a_constructed_pair_of_written_sukuns_is_counted() -> None:
    """خلوُّ النصّ المُودَع ليس عجزًا في المسح، وهذا ما يُظهره."""
    word = "ب" + SUKUN + "ت" + SUKUN
    scan = scan_quiescence_adjacency([word], source_id="سطرٌ-للاختبار")
    assert len(scan.written_sukun_pairs) == 1


def test_the_madd_shape_also_catches_the_assimilated_article_lam() -> None:
    """الشكلُ لا يفصل ألفَ المدّ عن لام التعريف المُدغمة، والاختبارُ يُظهره."""
    scan = scan_quiescence_adjacency_on_the_deposited_fatiha()
    words = [row.word for row in scan.unmarked_before_shadda_positions]
    assert "الضَّالِّينَ" in words
    assert "اللَّهِ" in words
    assert len(AdjacencyShape) == 2


def test_the_scan_reads_marks_and_the_shadda_constant_is_the_written_one() -> None:
    assert SHADDA == "\u0651"
    assert SUKUN == "\u0652"


def test_adjacency_is_scanned_inside_a_word_never_across_its_boundary() -> None:
    word_one = "ب" + SUKUN
    word_two = "ت" + SUKUN
    scan = scan_quiescence_adjacency(
        [f"{word_one} {word_two}"], source_id="سطرٌ-للاختبار"
    )
    assert scan.written_sukun_pairs == ()


# --- التجميدُ الوارد: مرفوضٌ باشتقاقٍ من المصدر لا بإعلان ----------------------


def test_the_submitted_freeze_is_refused_because_its_population_is_not_deposited() -> (
    None
):
    table = read_ibtida_on_the_deposited_fatiha()
    assert (
        derive_submitted_freeze_standing(table)
        is SubmittedFreezeStanding.MARFUD_LI_ANNA_MUJTAMAAHU_GHAYR_MUWDA
    )


def test_the_acceptance_branch_exists_and_needs_the_claimed_population() -> None:
    """الرفضُ مشروطٌ لا مُطلَق: مصدرٌ بذلك الاسم يبلغ فرعَ القبول."""
    table = IbtidaReadingTable(source_id=SUBMITTED_CLAIM_POPULATION_ID, rows=())
    assert (
        derive_submitted_freeze_standing(table)
        is SubmittedFreezeStanding.MAQBUL_BI_ITADAT_TASHGHIL
    )
    assert len(SubmittedFreezeStanding) == 2


def test_no_deposited_text_in_this_tree_carries_the_claimed_population_id() -> None:
    assert FATIHA_SOURCE_ID != SUBMITTED_CLAIM_POPULATION_ID


def test_the_freeze_identifier_is_kept_verbatim_for_review() -> None:
    assert "99.9974PCT" in SUBMITTED_FREEZE_IDENTIFIER
    assert "100PCT-AFTER-NAMING-LAM-AMR-EXCEPTION" in SUBMITTED_FREEZE_IDENTIFIER


# --- الأرقامُ الواردة: مُسجَّلةٌ خبرًا بقيدها لا مقبولةً قياسًا ----------------


def test_the_submitted_figures_are_filed_as_reported_not_measured() -> None:
    figures = {record.figure_text for record in REPORTED_UNVERIFIED_FIGURES}
    assert "٩٩٫٩٩٧٤٪" in figures
    assert "١٠٠٫٠٠٠٠٪" in figures
    for record in REPORTED_UNVERIFIED_FIGURES:
        assert not record.source_genus.supports_freeze


# --- ما لا يحسمه التسجيل، مُسمًّى ولا يُترَك ليُفترَض -------------------------


def test_the_named_residuals_carry_their_own_names_in_their_text() -> None:
    assert len(IBTIDA_WASL_WAQF_NAMED_RESIDUALS) == 10
    for name, text in IBTIDA_WASL_WAQF_NAMED_RESIDUALS.items():
        assert text.startswith(f"{name}:")


def test_the_amendment_after_the_number_is_named_as_such() -> None:
    text = IBTIDA_WASL_WAQF_NAMED_RESIDUALS[
        "EXCLUDING_A_COUNTEREXAMPLE_AFTER_THE_NUMBER_IS_AN_AMENDMENT"
    ]
    assert "بعد الرقم" in text


def test_this_module_imports_no_kernel_and_no_program_module() -> None:
    from pathlib import Path

    from alghanem.arabic import ibtida_wasl_waqf_registration

    source = Path(ibtida_wasl_waqf_registration.__file__).read_text(encoding="utf-8")
    assert "from alghanem.kernel" not in source
    assert "from ..kernel" not in source
    assert "from alghanem.program" not in source
    assert "from ..program" not in source
