"""اختباراتُ وحدة الحدّ: الدخولُ والخروجُ محوران، والشهادةُ تحمل الطرفين.

كلُّ رقمٍ ههنا **مقيسٌ على البايتات المختومة** في هذه الشجرة، ولا يُنقَل رقمٌ
من متن التقرير ليُمتَحَن به منتجُنا؛ فالمتنُ المنقولُ غائبٌ عن الشجرة.
"""

from __future__ import annotations

import pytest

from alghanem.arabic.a116_bridge_licence import MaterialStanding, Verdict
from alghanem.arabic.boundary116_entry_exit import (
    BOUNDARY116_NAMED_RESIDUALS,
    THE_DECLARED_WASL_NOUNS,
    THE_FOUR_MODES,
    THE_REPORT_AT_TRANSCRIPTION,
    THE_RULES,
    THE_SAHIHAYN_MATERIALS,
    THE_UNAPPLIED_READINGS,
    Atom,
    AtomOrigin,
    Boundary116Error,
    BoundaryMode,
    Entry,
    Exit,
    SeamCertificate,
    Status,
    TranscribedBookRow,
    axis_independence_reading,
    deposit_seam_census,
    deposit_word_census,
    project,
    rule_by_id,
    seam,
    the_ledger,
)

_IN_THE_HOUSE_LEFT = "\u0641\u0650\u064a"
_IN_THE_HOUSE_RIGHT = "\u0627\u0644\u0652\u0628\u064e\u064a\u0652\u062a\u0650"


def _rendered(atoms: tuple[Atom, ...]) -> list[str]:
    return [f"{atom.carrier}{atom.haraka}" for atom in atoms]


# ---------------------------------------------------------------------------
# أوّلًا: المحوران لا يُدمَجان في متغيّرٍ واحد
# ---------------------------------------------------------------------------


def test_the_four_modes_are_a_product_of_two_axes_not_three_values() -> None:
    assert len(THE_FOUR_MODES) == len(Entry) * len(Exit) == 4
    assert {(mode.entry, mode.exit) for mode in THE_FOUR_MODES} == {
        (entry, exit_) for entry in Entry for exit_ in Exit
    }


def test_one_word_may_be_started_and_paused_upon_at_once() -> None:
    """الابتداءُ والوقفُ ليسا متنافيين: الكلمةُ نفسُها تُبدَأ ويُوقَف عليها."""

    mode = BoundaryMode(Entry.START, Exit.PAUSE)
    assert mode.entry is Entry.START
    assert mode.exit is Exit.PAUSE
    assert mode in THE_FOUR_MODES


def test_both_axes_move_the_projection_on_the_sealed_bytes() -> None:
    """محورٌ لا يُحرّك شيئًا ليس محورًا؛ فاستقلالُهما مقيسٌ لا مُعلَن."""

    reading = axis_independence_reading()
    assert reading.occurrences == 82_532
    assert reading.moved_by_the_exit_axis == 34_203
    assert reading.moved_by_the_entry_axis == 10_397
    assert reading.both_axes_are_effective


# ---------------------------------------------------------------------------
# ثانيًا: الشهادةُ الزوجيّةُ تحمل أثرَين على جانبَي الحدّ
# ---------------------------------------------------------------------------


def test_the_declared_witness_is_rederived_on_both_sides_of_the_seam() -> None:
    certificate = seam(_IN_THE_HOUSE_LEFT, _IN_THE_HOUSE_RIGHT)
    assert _rendered(certificate.left_input) == ["\u0641\u0650", "\u064a\u0652"]
    assert _rendered(certificate.left_output) == ["\u0641\u0650"]
    assert _rendered(certificate.right_input)[0] == "\u0621\u064e"
    assert _rendered(certificate.right_output) == [
        "\u0644\u0652",
        "\u0628\u064e",
        "\u064a\u0652",
        "\u062a\u0650",
    ]
    assert certificate.applied == ("WASL_DROP_HAMZA", "SAKINAYN_DROP_MADD")
    assert certificate.status is Status.COMPLETE_CANDIDATE


def test_the_source_glyphs_survive_every_deletion_in_the_projection() -> None:
    """حذفُ همزة الوصل في الإسقاط لا يمحو ألفَها من أصل المصدر."""

    certificate = seam(_IN_THE_HOUSE_LEFT, _IN_THE_HOUSE_RIGHT)
    assert certificate.right_source == _IN_THE_HOUSE_RIGHT
    assert "\u0627" in certificate.right_source
    assert certificate.left_source == _IN_THE_HOUSE_LEFT


def test_applying_only_the_deletion_loses_the_left_side_repair() -> None:
    """تسليمُ كلِّ كلمةٍ مستقلّةً يُفقِد أثرَ إصلاح المدّ على الطرف الأيسر."""

    certificate = seam(_IN_THE_HOUSE_LEFT, _IN_THE_HOUSE_RIGHT)
    alone = project(_IN_THE_HOUSE_LEFT, BoundaryMode(Entry.START, Exit.CONTINUE))
    assert certificate.left_input == alone.atoms
    assert certificate.left_output != alone.atoms


# ---------------------------------------------------------------------------
# ثالثًا: الأثرُ المزوَّرُ مردودٌ بثلاثة حرّاس
# ---------------------------------------------------------------------------


def _atoms(*pairs: tuple[str, str]) -> tuple[Atom, ...]:
    return tuple(
        Atom(carrier=carrier, haraka=haraka, origin=AtomOrigin.WRITTEN)
        for carrier, haraka in pairs
    )


@pytest.mark.parametrize(
    "rule_id",
    ["WASL_DROP_HAMZA", "SAKINAYN_DROP_MADD", "SAKINAYN_TANWIN_KASR"],
)
def test_a_rule_claimed_without_its_effect_is_refused(rule_id: str) -> None:
    unchanged = _atoms(("\u0628", "\u064e"))
    with pytest.raises(Boundary116Error):
        SeamCertificate(
            left_source="\u0628\u064e",
            right_source="\u0628\u064e",
            left_exit=Exit.CONTINUE,
            right_entry=Entry.JOINED,
            left_input=unchanged,
            left_output=unchanged,
            right_input=unchanged,
            right_output=unchanged,
            applied=(rule_id,),
            status=Status.COMPLETE_CANDIDATE,
            deferral_reasons=(),
        )


def test_an_unknown_rule_identity_is_refused_not_read_as_a_general_rule() -> None:
    with pytest.raises(Boundary116Error):
        rule_by_id("WAQF_SOMETHING_UNDECLARED")


# ---------------------------------------------------------------------------
# رابعًا: بوّابةُ الابتداء
# ---------------------------------------------------------------------------


def test_starting_on_a_silent_seed_is_refused_and_never_patched() -> None:
    """لا تُضاف همزةُ إصلاحٍ مجهولةٌ إلى كلّ سلسلة؛ المنعُ يُسمّى ولا يُرقَّع."""

    assimilated = "\u0645\u0650\u0651\u0646\u064e"
    at_start = project(assimilated, BoundaryMode(Entry.START, Exit.CONTINUE))
    assert at_start.status is Status.REFUSED_START_ON_A_SILENT_SEED
    joined = project(assimilated, BoundaryMode(Entry.JOINED, Exit.CONTINUE))
    assert joined.status is not Status.REFUSED_START_ON_A_SILENT_SEED


def test_a_silent_seed_is_a_need_for_a_left_context_not_a_forbidden_form() -> None:
    reading = axis_independence_reading()
    assert reading.silent_seed_occurrences == 2_834
    assert reading.silent_seed_distinct_forms == 714
    assert "A_SILENT_SEED_NEEDS_A_LEFT_CONTEXT_IT_IS_NOT_A_FORBIDDEN_FORM" in "\n".join(
        BOUNDARY116_NAMED_RESIDUALS
    )


def test_the_wasl_hamza_of_the_article_is_proven_at_the_start() -> None:
    projection = project(_IN_THE_HOUSE_RIGHT, BoundaryMode(Entry.START, Exit.CONTINUE))
    assert _rendered(projection.atoms)[0] == "\u0621\u064e"
    assert "IBTIDA_WASL_HAMZA" in projection.applied


def test_a_verb_whose_wasl_vowel_is_undocumented_is_deferred_by_name() -> None:
    projection = project(
        "\u0627\u0636\u0652\u0631\u0650\u0628\u0652",
        BoundaryMode(Entry.START, Exit.CONTINUE),
    )
    assert projection.status is Status.DEFERRED
    assert projection.deferral_reasons


def test_the_declared_wasl_nouns_are_a_closed_named_list() -> None:
    assert "\u0633\u0645" in THE_DECLARED_WASL_NOUNS
    assert "\u0628\u0646" in THE_DECLARED_WASL_NOUNS


# ---------------------------------------------------------------------------
# خامسًا: الوصلُ وحفظُ همزة القطع وكرسيّها
# ---------------------------------------------------------------------------


def test_a_qat_hamza_is_kept_with_its_seat_when_joined() -> None:
    """حذفُ همزة الوصل لا يمسّ همزةَ القطع ولا كرسيَّها."""

    qat = "\u0623\u064e\u062d\u064e\u062f\u064c"
    joined = project(qat, BoundaryMode(Entry.JOINED, Exit.CONTINUE))
    assert "WASL_DROP_HAMZA" not in joined.applied
    assert joined.source == qat


# ---------------------------------------------------------------------------
# سادسًا: بوّابةُ الوقف
# ---------------------------------------------------------------------------


def test_the_final_short_haraka_becomes_a_sukun_at_a_pause() -> None:
    projection = project(
        "\u0627\u0644\u0652\u0628\u064e\u064a\u0652\u062a\u0650",
        BoundaryMode(Entry.JOINED, Exit.PAUSE),
    )
    assert _rendered(projection.atoms)[-1] == "\u062a\u0652"
    assert "WAQF_SHORT_HARAKA_TO_SUKUN" in projection.applied


def test_a_final_ta_marbuta_becomes_a_silent_ha_without_touching_the_glyph() -> None:
    word = "\u0631\u064e\u062d\u0652\u0645\u064e\u0629\u064c"
    projection = project(word, BoundaryMode(Entry.JOINED, Exit.PAUSE))
    assert _rendered(projection.atoms)[-1] == "\u0647\u0652"
    assert "WAQF_TA_MARBUTA_TO_HA" in projection.applied
    assert projection.source == word


def test_tanwin_at_a_pause_parts_by_its_vowel() -> None:
    damm = project(
        "\u0628\u064e\u064a\u0652\u062a\u064c", BoundaryMode(Entry.JOINED, Exit.PAUSE)
    )
    assert _rendered(damm.atoms)[-1] == "\u062a\u0652"
    fath = project(
        "\u0628\u064e\u064a\u0652\u062a\u064b\u0627",
        BoundaryMode(Entry.JOINED, Exit.PAUSE),
    )
    assert "WAQF_TANWIN" in fath.applied
    assert fath.atoms[-1].origin is AtomOrigin.WAQF_MADD_A


def test_a_shadda_keeps_two_slots_and_the_second_is_silenced_at_a_pause() -> None:
    word = "\u062d\u064e\u0642\u0651\u064c"
    projection = project(word, BoundaryMode(Entry.JOINED, Exit.PAUSE))
    rendered = _rendered(projection.atoms)
    assert rendered[-2:] == ["\u0642\u0652", "\u0642\u0652"]
    assert "WAQF_SHADDA_TWO_SLOTS" in projection.applied


# ---------------------------------------------------------------------------
# سابعًا: الحدودُ والفواصلُ غيرُ المصرَّحة
# ---------------------------------------------------------------------------


def test_a_map_that_pauses_the_left_then_joins_the_right_is_refused() -> None:
    with pytest.raises(Boundary116Error):
        seam(
            _IN_THE_HOUSE_LEFT,
            _IN_THE_HOUSE_RIGHT,
            left_exit=Exit.PAUSE,
            right_entry=Entry.JOINED,
        )


def test_a_declared_pause_then_a_fresh_start_applies_no_cross_seam_repair() -> None:
    """الحدُّ مُصرَّحٌ به: فإن وُقِف على الأيسر وابتُدئ بالأيمن فلا إصلاحَ عبره."""

    across = seam(
        _IN_THE_HOUSE_LEFT,
        _IN_THE_HOUSE_RIGHT,
        left_exit=Exit.PAUSE,
        right_entry=Entry.START,
    )
    assert "SAKINAYN_DROP_MADD" not in across.applied
    assert "WASL_DROP_HAMZA" not in across.applied
    assert across.left_output == across.left_input
    assert across.left_source == _IN_THE_HOUSE_LEFT


def test_an_undeclared_separator_blocks_a_seam_it_does_not_pause() -> None:
    census = deposit_seam_census()
    assert census.blocked_by_an_undeclared_separator == 8_574
    assert census.blocked_by_an_undeclared_separator < census.deferred


# ---------------------------------------------------------------------------
# ثامنًا: الإحصاءُ على المُودَع المختوم
# ---------------------------------------------------------------------------


@pytest.mark.parametrize(
    ("entry", "exit_", "complete", "refused"),
    [
        (Entry.START, Exit.CONTINUE, 52_146, 2_834),
        (Entry.START, Exit.PAUSE, 52_146, 2_834),
        (Entry.JOINED, Exit.CONTINUE, 54_980, 0),
        (Entry.JOINED, Exit.PAUSE, 54_980, 0),
    ],
)
def test_the_word_census_is_frozen_per_mode(
    entry: Entry, exit_: Exit, complete: int, refused: int
) -> None:
    census = deposit_word_census(entry, exit_)
    assert census.occurrences == 82_532
    assert census.complete == complete
    assert census.refused_start_on_a_silent_seed == refused
    assert census.out_of_profile == 4_287
    assert (
        census.complete
        + census.deferred
        + census.refused_start_on_a_silent_seed
        + census.out_of_profile
        == census.occurrences
    )


def test_the_seam_census_is_frozen_and_its_rules_are_not_summed_as_licences() -> None:
    census = deposit_seam_census()
    assert census.pairs == 76_296
    assert census.complete == 31_196
    assert census.deferred == 45_100
    assert census.wasl_hamza_deletions == 10_208
    assert census.madd_repairs == 2_105
    assert census.tanwin_nun_kasr == 1_896
    assert census.complete + census.deferred == census.pairs
    rule_operations = (
        census.wasl_hamza_deletions + census.madd_repairs + census.tanwin_nun_kasr
    )
    assert rule_operations != census.complete


# ---------------------------------------------------------------------------
# تاسعًا: النقلُ عن متنٍ غائبٍ يبقى نقلًا
# ---------------------------------------------------------------------------


def test_the_transcribed_rows_balance_their_own_occurrences() -> None:
    for row in THE_REPORT_AT_TRANSCRIPTION:
        assert (
            row.complete_start_continue + row.deferred_start_continue == row.occurrences
        )
        assert row.complete_start_pause + row.deferred_start_pause == row.occurrences


def test_an_inconsistent_transcription_is_refused_at_construction() -> None:
    with pytest.raises(Boundary116Error):
        TranscribedBookRow(
            book="متنٌ مُفتعَل",
            records=1,
            occurrences=100,
            complete_start_continue=50,
            complete_start_pause=50,
            deferred_start_continue=49,
            deferred_start_pause=50,
        )


def test_the_sahihayn_materials_are_absent_from_the_tree() -> None:
    for material in THE_SAHIHAYN_MATERIALS:
        assert material.standing() is MaterialStanding.ABSENT_FROM_THE_TREE


def test_the_unapplied_readings_are_named_not_silently_folded_in() -> None:
    assert len(THE_UNAPPLIED_READINGS) >= 5


# ---------------------------------------------------------------------------
# عاشرًا: عقدُ الترخيص
# ---------------------------------------------------------------------------


def test_every_rule_carries_a_guard_and_a_reference() -> None:
    assert len(THE_RULES) == 11
    for rule in THE_RULES:
        assert rule.guard.strip()
        assert rule.reference.strip()


def test_the_ledger_licenses_only_what_it_remeasures_here() -> None:
    ledger = dict(the_ledger())
    licensed = [
        name for name, check in ledger.items() if check.verdict is Verdict.LICENSED
    ]
    suspended = [
        name for name, check in ledger.items() if check.verdict is Verdict.SUSPENDED
    ]
    assert len(licensed) == 4
    assert len(suspended) == 4
    for name in suspended:
        assert not ledger[name].verdict.is_a_refusal


def test_the_sahihayn_figures_and_the_totality_claim_stay_suspended() -> None:
    ledger = dict(the_ledger())
    for name, check in ledger.items():
        if "الصحيحين" in name or "جامعيّة" in name or "كفاية" in name:
            assert check.verdict is Verdict.SUSPENDED
