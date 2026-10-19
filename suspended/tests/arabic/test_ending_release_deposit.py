"""اختباراتُ إيداع مولِّدات الخاتمة: القياسُ يُعاد، والحكمُ لا يُكتَب."""

from __future__ import annotations

from dataclasses import fields, replace
from pathlib import Path

import pytest

from alghanem.arabic.ending_release_deposit import (
    ENDING_RELEASE_NAMED_RESIDUALS,
    THE_ABSENT_IDENTIFIERS,
    THE_ENDING_FIGURES,
    CorpusFigures,
    EndingReleaseError,
    FigureGenus,
    FigureStanding,
    FormKey,
    KeyLadderRow,
    TranscribedFigure,
    contradicting_figures,
    identifier_is_present_in_this_tree,
    measure_the_sealed_corpus,
    the_corpus_gate_is_untouched,
    the_key_ladder,
)


def test_the_five_ending_classes_partition_every_token() -> None:
    """القسمةُ خمسًا مُستغرِقةٌ: مجموعُها عددُ التوكنات بلا فضلةٍ ولا نقص."""

    figures = measure_the_sealed_corpus()
    assert figures.ending_total == figures.token_count


def test_the_two_structural_laws_hold_without_a_single_exception() -> None:
    """السكونان المتجاوران صفرٌ مطلق، والسكونُ الأوّل اثنان لا غير."""

    figures = measure_the_sealed_corpus()
    assert figures.adjacent_written_sukun_inside_a_word == 0
    assert figures.word_initial_written_sukun == 2


def test_the_separated_lam_is_a_spacing_habit_and_not_a_breach() -> None:
    """لامُ الأمر الموصولةُ أكثرُ بمراتبَ من المفصولة، فالفصلُ عُرفُ رسم."""

    figures = measure_the_sealed_corpus()
    assert figures.joined_lam_of_command_tokens > 100
    assert (
        figures.joined_lam_of_command_tokens > figures.word_initial_written_sukun * 50
    )


def test_the_release_zero_belongs_to_the_connecting_hamza_alone() -> None:
    """الصفرُ يزول إن وُسِّع الشرطُ إلى كلّ صورة ألف؛ فهو صفرُ الوصل وحدَه."""

    figures = measure_the_sealed_corpus()
    assert figures.sukun_before_the_connecting_alif == 0
    assert figures.sukun_before_any_alif_shape > 0
    assert figures.the_release_zero_survives_only_the_connecting_alif


def test_the_pause_is_absent_from_this_pointing() -> None:
    """فواصلُ الآي الساكنةُ قلّةٌ، فالنصُّ مشكولٌ للوصل ولا يُقاس فيه وقف."""

    figures = measure_the_sealed_corpus()
    assert figures.ayah_final_written_sukun * 10 < figures.ayah_count


def test_the_form_key_moves_the_figure_more_than_the_phenomenon() -> None:
    """درجاتُ السلّم الثلاث تنقص بانتقاء المفتاح، ولا يتبدّل في النصّ حرف."""

    ladder = the_key_ladder()
    assert tuple(rung.key for rung in ladder) == tuple(FormKey)
    forms = [rung.alternating_forms for rung in ladder]
    releases = [rung.fatha_releases for rung in ladder]
    assert forms == sorted(forms, reverse=True)
    assert releases == sorted(releases, reverse=True)
    assert releases[0] > releases[-1] * 2


def test_the_generous_key_merges_more_than_half_of_its_own_forms() -> None:
    """أكثرُ من نصف «المتناوبات» تحت المفتاح السخيّ أكثرُ من جذعٍ واحد."""

    figures = measure_the_sealed_corpus()
    assert (
        figures.multi_stem_forms_under_the_dropping_key * 2
        > figures.forms_marks_dropped
    )


def test_the_fatha_after_bare_inna_dominates_and_the_attachment_splits() -> None:
    """الفتحُ بعد إنّ المجرّدة غالبٌ، ويسقط غلبتَه انضمامُ لاحقةٍ إليها."""

    figures = measure_the_sealed_corpus()
    bare = figures.bare_inna_next_is_fatha / figures.bare_inna_readable_next
    attached = figures.attached_inna_next_is_fatha / figures.attached_inna_readable_next
    assert bare > 0.9
    assert attached < 0.5


def test_every_transcribed_figure_is_recomputed_not_believed() -> None:
    """كلُّ رقمٍ منقولٍ يُقابَل بقياسٍ حيّ، ولا يُقبَل بذاته."""

    for figure in THE_ENDING_FIGURES:
        if figure.genus is not FigureGenus.MEASURED_ON_THE_SEALED_BYTES:
            continue
        assert figure.measured is not None
        expected = (
            FigureStanding.AGREES
            if figure.measured == figure.transcribed
            else FigureStanding.CONTRADICTS
        )
        assert figure.standing is expected


def test_the_deposit_carries_contradictions_and_agreements_both() -> None:
    """إيداعٌ كلُّه موافقةٌ يُتّهَم؛ وههنا الطرفان معًا."""

    agreeing = [
        figure
        for figure in THE_ENDING_FIGURES
        if figure.standing is FigureStanding.AGREES
    ]
    assert len(agreeing) > 5
    assert len(contradicting_figures()) > 0


def test_a_bumped_transcription_flips_its_own_standing() -> None:
    """الحكمُ يتبع الطرفَين فعلًا: يُزاد المنقولُ واحدًا فينقلب الحكم."""

    agreeing = next(
        figure
        for figure in THE_ENDING_FIGURES
        if figure.standing is FigureStanding.AGREES
    )
    assert agreeing.transcribed is not None
    bumped = replace(agreeing, transcribed=agreeing.transcribed + 1)
    assert bumped.standing is FigureStanding.CONTRADICTS


def test_no_refused_or_unmeasurable_figure_carries_a_number() -> None:
    """ما منعته البوّابةُ وما امتنع قياسُه لا رقمَ له ههنا البتّة."""

    withheld = [
        figure
        for figure in THE_ENDING_FIGURES
        if figure.genus is not FigureGenus.MEASURED_ON_THE_SEALED_BYTES
    ]
    assert len(withheld) == 4
    for figure in withheld:
        assert figure.transcribed is None
        assert figure.measured is None
        assert figure.standing is FigureStanding.NOT_ISSUED_HERE


def test_a_withheld_figure_cannot_be_given_a_number() -> None:
    """محاولةُ تهريب رقمٍ إلى الخانة الممنوعة تُرفَض بالبناء."""

    with pytest.raises(EndingReleaseError):
        TranscribedFigure(
            name="ربحٌ مهرَّب",
            genus=FigureGenus.REFUSED_BY_THE_TOKEN_MARKOV_GATE,
            attribute=None,
            transcribed=52,
        )


def test_a_measured_figure_must_name_an_attribute_we_actually_measure() -> None:
    """لا يُقبَل رقمٌ مقيسٌ يُسنَد إلى حقلٍ لا نقيسه."""

    with pytest.raises(EndingReleaseError):
        TranscribedFigure(
            name="رقمٌ بلا باب",
            genus=FigureGenus.MEASURED_ON_THE_SEALED_BYTES,
            attribute="a_field_we_do_not_measure",
            transcribed=1,
        )


def test_no_deposit_type_carries_a_hand_written_verdict_field() -> None:
    """لا حقلَ حكمٍ في أنواع هذا الإيداع؛ فالحكمُ مشتقٌّ دائمًا."""

    for declared in (TranscribedFigure, CorpusFigures, KeyLadderRow):
        for field in fields(declared):
            assert "standing" not in field.name
            assert "verdict" not in field.name


def test_the_absent_identifiers_are_absent_and_the_probe_can_find_one() -> None:
    """المعرِّفانِ غائبان فعلًا، والمِسبارُ يجد ما هو موجودٌ فلا يُتّهَم بالعمى."""

    for identifier in THE_ABSENT_IDENTIFIERS:
        assert not identifier_is_present_in_this_tree(identifier)
    assert identifier_is_present_in_this_tree("AIM-T3")
    assert identifier_is_present_in_this_tree("measure_the_sealed_corpus")
    assert not identifier_is_present_in_this_tree("NO-SUCH-IDENTIFIER-HERE")


def test_the_markov_gate_is_untouched_by_this_deposit() -> None:
    """لا يزحزح هذا الإيداعُ بوّابةَ ماركوف عمّا كانت عليه عند الاستيراد."""

    assert the_corpus_gate_is_untouched()


def test_every_named_residual_carries_its_own_name() -> None:
    """كلُّ قيدٍ يُصدِّر اسمَه في نصّه، فلا يُقتطَع عن معرِّفه."""

    assert len(ENDING_RELEASE_NAMED_RESIDUALS) == 8
    for name, residual in ENDING_RELEASE_NAMED_RESIDUALS.items():
        assert residual.split(":")[0].isupper()
        assert name.islower()


def test_the_deposit_imports_no_authority_module() -> None:
    """خمولٌ سلطويّ: لا استيرادَ من النواة ولا من البرنامج في هذا الملفّ."""

    lines = (
        Path("src/alghanem/arabic/ending_release_deposit.py")
        .read_text(encoding="utf-8")
        .splitlines()
    )
    statements = [line for line in lines if line.startswith(("import ", "from "))]
    assert statements
    for statement in statements:
        assert "kernel" not in statement
        assert "program" not in statement


def test_the_corpus_is_never_read_outside_the_sealed_door() -> None:
    """لا يُقرأ المسارُ مباشرةً؛ البابُ المختومُ وحدَه هو المدخل."""

    source = Path("src/alghanem/arabic/ending_release_deposit.py").read_text(
        encoding="utf-8"
    )
    assert "read_quran_corpus_bytes" in source
    assert "corpora/" not in source.replace("corpora/quran-simple-enhanced.txt", "")


def test_an_empty_measurement_is_refused_by_construction() -> None:
    """قياسٌ فارغٌ أو قسمةٌ غيرُ مستغرِقةٍ تُرفَض عند البناء لا بعده."""

    figures = measure_the_sealed_corpus()
    with pytest.raises(EndingReleaseError):
        replace(figures, ending_tanwin=figures.ending_tanwin + 1)
    with pytest.raises(EndingReleaseError):
        replace(figures, token_count=0)
