"""اختباراتُ نموذج الـ116: ما يُشتَقّ يُعاد اشتقاقُه، وما يُنقَل يُقابَل به.

ولا يُجمَّد ههنا مقدارٌ ينمو بنموّ الشجرة: المقيسُ مُودَعٌ مختومُ الطول
والبصمة، والمؤكَّدُ إمّا علاقةٌ بين مقدارَين، وإمّا بنيةُ قراءةٍ في شاهد،
وإمّا ردٌّ على مدخلٍ غيرِ مشهود.
"""

from __future__ import annotations

import pytest

from alghanem.arabic import a116_bridge_licence as a116
from alghanem.arabic import letter_haraka_partition as partition

# ---------------------------------------------------------------------------
# الجدولُ مشتقٌّ لا منقول
# ---------------------------------------------------------------------------


def test_the_hundred_and_sixteen_is_a_product_of_the_two_declarations() -> None:
    """الـ116 حاصلُ ضربٍ يُعاد اشتقاقُه، لا رقمٌ مكتوبٌ في حقل."""

    assert a116.THE_HUNDRED_AND_SIXTEEN == len(a116.THE_CARRIERS) * len(
        a116.THE_HARAKAT
    )
    assert len(a116.a116_cells()) == a116.THE_HUNDRED_AND_SIXTEEN
    assert len(set(a116.a116_cells())) == a116.THE_HUNDRED_AND_SIXTEEN


def test_the_difference_from_the_hundred_and_twelve_is_the_hamza_row_alone() -> None:
    """ما زاد على جدول `letter_haraka_partition` صفُّ الهمزة وحدَه لا غير."""

    row = a116.the_hamza_row()
    assert {cell[0] for cell in row} == {"ء"}
    assert len(row) == a116.THE_HUNDRED_AND_SIXTEEN - partition.THE_HUNDRED_AND_TWELVE


def test_a_cell_in_the_table_is_not_a_phonetic_licence() -> None:
    """الخانةُ مقعدٌ تمثيليّ؛ وخلوُّ صفٍّ كاملٍ في المُودَع لا يُقرأ منعًا."""

    absent = a116.census().absent_cells
    assert absent, "خانةٌ خاليةٌ واحدةٌ على الأقلّ مطلوبةٌ ليُقرأ الفرق."
    assert {cell[0] for cell in absent} == {"ا"}
    assert "A_CELL_IS_A_SEAT_NOT_A_PHONETIC_LICENCE" in "\n".join(
        a116.A116_BRIDGE_LICENCE_NAMED_RESIDUALS
    )


# ---------------------------------------------------------------------------
# قاعدةُ القراءة
# ---------------------------------------------------------------------------


def test_a_cluster_with_a_residue_is_not_a_completed_projection() -> None:
    """خانةٌ قائمةٌ مع بقيّةِ شدّةٍ ليست إسقاطًا مكتملًا؛ والفرقُ مقروءٌ لا مُلغًى."""

    clusters = a116.carrier_clusters("رَبِّ")
    final = clusters[-1]
    assert final.cell == ("ب", "\u0650")
    assert final.residue == ("\u0651",)
    assert not final.is_complete
    assert a116.projected_cells("رَبِّ") is None


def test_a_carrier_outside_the_vocabulary_has_no_cell() -> None:
    """حرفٌ خارجَ المفردة المُعلَنة لا خانةَ له، ولا يُفسَّر خانةً افتراضيّة."""

    cluster = a116.carrier_clusters("ةَ")[0]
    assert cluster.carrier == "ة"
    assert cluster.cell is None
    assert not cluster.is_complete


def test_a_cell_outside_the_table_is_refused_not_absorbed() -> None:
    """خانةٌ خارجَ الـ116 تُردّ باسمها، ولا تُنقَل حالةً صامتة."""

    with pytest.raises(a116.A116BridgeLicenceError):
        a116.step(a116.SyllableState.AWAITING_AN_ONSET, ("ة", "\u064e"))


# ---------------------------------------------------------------------------
# المنقولُ والمقيس
# ---------------------------------------------------------------------------


def test_the_transcribed_rows_are_internally_consistent_and_nothing_more() -> None:
    """الاتّساقُ الحسابيُّ في أرقام التقرير قائمٌ، وليس شهادةً من بايتات."""

    assert a116.the_report_is_internally_consistent()
    assert "AN_ARITHMETIC_IDENTITY_IS_NOT_A_CORROBORATION" in "\n".join(
        a116.A116_BRIDGE_LICENCE_NAMED_RESIDUALS
    )


def test_the_measured_census_splits_the_words_without_remainder() -> None:
    """المكتملُ والمحتاجُ للجسر يستغرقان الكلماتِ كلَّها، ولا بقيّةَ ثالثة."""

    measured = a116.census()
    assert measured.complete_words + measured.bridge_words == measured.words
    assert measured.attested_cells + len(measured.absent_cells) == (
        a116.THE_HUNDRED_AND_SIXTEEN
    )


def test_a_transcribed_figure_is_not_read_as_a_rederived_one() -> None:
    """كلُّ صفٍّ مقيسٍ يُقابَل فيخرج بمنزلته؛ وما لا مادّةَ له يُسمّى لا يُوافَق."""

    rows = a116.comparison_rows()
    assert len(rows) == len(a116.THE_REPORT_AT_TRANSCRIPTION)
    for row, value, standing in rows:
        if row.measured_key is None:
            assert value is None
            assert standing is a116.RowStanding.NOT_MEASURABLE_IN_THIS_TREE
            continue
        assert value == a116.census().value_of(row.measured_key)
        expected = (
            a116.RowStanding.AGREES_WITH_WHAT_DISK_GIVES
            if value == row.transcribed
            else a116.RowStanding.DIVERGES_FROM_WHAT_DISK_GIVES
        )
        assert standing is expected


def test_an_unknown_measured_key_is_refused_not_read_as_zero() -> None:
    """اسمُ حقلٍ مجهولٍ يُردّ؛ ولا يُفسَّر صفرًا فيُقرأ موافقةً كاذبة."""

    with pytest.raises(a116.A116BridgeLicenceError):
        a116.census().value_of("مقدارٌ لا وجودَ له")


# ---------------------------------------------------------------------------
# جسرُ الألف
# ---------------------------------------------------------------------------


def test_the_alif_bridge_moves_the_named_pair_and_leaves_groups_behind() -> None:
    """بالجسر يتمايز «مَلِكِ/مَالِكِ»، وببقاء مجموعاتٍ يبقى الاسترجاعُ بسجلّ الأصل."""

    reading = a116.collision_reading()
    assert reading.named_pair_collides_without_the_bridge
    assert not reading.named_pair_collides_with_the_bridge
    assert reading.the_bridge_moves_the_named_pair
    assert reading.groups_the_bridge_removes > 0
    assert reading.retrieval_rests_on_the_original_log


def test_the_named_pair_is_attested_in_the_sealed_deposit() -> None:
    """لا يُقاس جسرٌ بزوجٍ مختلَق؛ وصورتا الزوج مشهودتان في المُودَع."""

    attested = set(a116.deposited_words())
    for form in a116.THE_NAMED_COLLIDING_PAIR:
        assert form in attested


# ---------------------------------------------------------------------------
# النموذجُ ونقطةُ استقراره
# ---------------------------------------------------------------------------


def test_the_transition_is_total_on_every_cell_and_every_state() -> None:
    """لكلّ حالةٍ وخانةٍ صورةٌ؛ فلا موضعَ بلا انتقالٍ يُسَدّ باستثناء."""

    for state in a116.SyllableState:
        for cell in a116.a116_cells():
            assert isinstance(a116.step(state, cell), a116.SyllableState)


def test_the_fixpoint_closes_all_lengths_inside_the_declared_model() -> None:
    """عند ‎S(k+1) = S(k)‎ لا يخرج أثرُ أيّ كلمةٍ من ‎A₁₁₆*‎ عن المجموعة المستقرّة."""

    reading = a116.fixpoint_reading()
    assert reading.closes_all_lengths
    assert reading.rungs[-1] == len(reading.stable_set)
    cells = a116.a116_cells()
    probes = (
        (),
        (cells[0],),
        (cells[0], cells[3]),
        (cells[3], cells[0]),
        tuple(cells[index % len(cells)] for index in range(0, 40)),
    )
    for probe in probes:
        assert a116.run_declared_model(probe) in reading.stable_set


def test_a_sukun_seed_falls_out_of_the_model_and_that_is_not_a_prohibition() -> None:
    """البذرةُ الساكنةُ تُسقِط الكلمةَ عن النموذج، وهي حاجةُ وصلٍ لا امتناعُ صورة."""

    assert (
        a116.step(a116.SyllableState.AWAITING_AN_ONSET, ("ل", "\u0652"))
        is a116.SyllableState.FELL_OUT_OF_THE_MODEL
    )
    exits = a116.model_exit_reading()
    assert exits.outside_forms > 0
    assert exits.every_exit_needs_a_left_context
    assert exits.outside_forms <= exits.projected_forms
    assert "A_CASE_OUTSIDE_THE_MODEL_IS_NOT_A_FORM_FORBIDDEN_IN_ARABIC" in "\n".join(
        a116.A116_BRIDGE_LICENCE_NAMED_RESIDUALS
    )


# ---------------------------------------------------------------------------
# عقدُ التحقّق
# ---------------------------------------------------------------------------


def test_a_check_missing_a_clause_is_refused_before_it_runs() -> None:
    """عقدٌ ناقصُ بندٍ لا يُشغَّل أصلًا، ولا يُكمَّل بقيمةٍ افتراضيّة."""

    for kwargs in (
        {"scope": "   "},
        {"conditions": ()},
        {"minimum": 0},
    ):
        payload = {
            "scope": "مجالٌ مُعلَن",
            "conditions": ("شرطٌ مُعلَن",),
            "effect": "أثرٌ مُعلَن",
            "evidence": ("دليلٌ مقيس",),
            "minimum": 1,
            **kwargs,
        }
        with pytest.raises(a116.A116BridgeLicenceError):
            a116.LicenceCheck(**payload)  # type: ignore[arg-type]


def test_an_absent_material_suspends_and_a_short_evidence_refuses() -> None:
    """التعليقُ غيابُ المادّة، والرفضُ حضورُها دون الحدّ؛ ولا يُقرأ أحدُهما الآخر."""

    suspended = a116.LicenceCheck(
        scope="مادّةٌ غيرُ مُودَعة",
        conditions=("البايتاتُ في الشجرة",),
        effect="شهادةٌ تُعاد",
        evidence=(),
        minimum=1,
        material_is_deposited=False,
    )
    refused = a116.LicenceCheck(
        scope="مادّةٌ مُودَعة",
        conditions=("دليلان",),
        effect="أثرٌ مُعلَن",
        evidence=("دليلٌ واحد",),
        minimum=2,
    )
    licensed = a116.LicenceCheck(
        scope="مادّةٌ مُودَعة",
        conditions=("دليلان",),
        effect="أثرٌ مُعلَن",
        evidence=("أوّل", "ثانٍ"),
        minimum=2,
    )
    assert suspended.verdict is a116.Verdict.SUSPENDED
    assert refused.verdict is a116.Verdict.REFUSED_WITH_EVIDENCE
    assert licensed.verdict is a116.Verdict.LICENSED


def test_evidence_is_never_read_from_an_undeposited_material() -> None:
    """مادّةٌ غيرُ مُودَعةٍ لا يُعلَّق عليها دليل؛ والدعوى تُردّ لا تُسكَّت."""

    with pytest.raises(a116.A116BridgeLicenceError):
        a116.LicenceCheck(
            scope="مادّةٌ غيرُ مُودَعة",
            conditions=("شرطٌ مُعلَن",),
            effect="أثرٌ مُعلَن",
            evidence=("دليلٌ من غائب",),
            minimum=1,
            material_is_deposited=False,
        )


def test_the_report_rederivation_claim_is_refused_by_what_disk_gives() -> None:
    """دعوى إعادة اشتقاق أرقام التقرير مردودةٌ بدليلٍ مقيس، لا معلَّقةٌ بغياب."""

    ledger = dict(a116.the_ledger())
    claim = ledger["أرقامُ التقرير مُعادةُ الاشتقاق من هذه البايتات"]
    assert claim.verdict is a116.Verdict.REFUSED_WITH_EVIDENCE
    assert claim.material_is_deposited


def test_the_three_open_claims_stay_suspended_by_their_named_materials() -> None:
    """التغطيةُ ومطابقةُ حفصٍ وشهادةُ الأربعين معلَّقةٌ، ولا يُرقّيها نجاحُ غيرها."""

    suspended = set(a116.suspended_claims())
    assert "كلُّ انتقالٍ عربيٍّ إلى الوزن والتركيب مرخَّصٌ بهذه الدالّة" in suspended
    assert "مطابقةُ المتن لرواية حفص" in suspended
    assert "اجتيازُ أربعين اختبارًا من أربعين" in suspended
    for material in a116.THE_UNDEPOSITED_MATERIALS:
        assert material in a116.A_TRANSCRIBED_FIGURE_IS_NOT_A_REDERIVED_ONE


def test_the_ledger_runs_every_claim_through_one_procedure() -> None:
    """إجراءُ التحقّق واحدٌ لكلّ الدعاوى، وإنّما تختلف شروطُها لا خطواتُه."""

    for name, check in a116.the_ledger():
        assert name.strip()
        assert check.conditions
        assert check.verdict in set(a116.Verdict)


def test_no_licence_here_lifts_a_block_or_thaws_a_freeze() -> None:
    """لا سلطانَ لهذه الوحدة، وتُعاد الجملةُ ليُحتَجّ بها لا لتُزيَّن."""

    assert a116.the_block_and_the_freeze_are_untouched()
