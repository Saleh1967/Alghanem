"""اختباراتُ محاسبة البتّات: الإغلاق، والاشتقاق، والاستبعاد المُسجَّل."""

from __future__ import annotations

import math

import pytest

from alghanem.arabic.position_haraka_bit_account import (
    POSITION_HARAKA_BIT_ACCOUNT_NAMED_RESIDUALS,
    THE_DECLARED_EXCLUSIONS,
    THE_FIRST_POSITION_TABLE,
    THE_HARAKA_COLUMNS,
    THE_LAST_POSITION_TABLE,
    BitAccount,
    ClosureStanding,
    DepositedTable,
    PositionHarakaBitAccountError,
    TableStanding,
    bit_account,
    closure_of,
    entropy_of,
    letter_information,
    table_without_letter,
)


def test_the_last_position_table_closes_exactly() -> None:
    """جدولُ الوصل يغلق: صفوفُه وأعمدتُه ومجموعُه الكلّيُّ بلا باقٍ."""

    reading = closure_of(THE_LAST_POSITION_TABLE)
    assert reading.standing is ClosureStanding.CLOSES_EXACTLY
    assert reading.cell_sum == reading.stated_grand_total == 78_076
    assert reading.shortfall == 0
    assert reading.column_shortfalls == (0, 0, 0, 0)
    assert len(THE_LAST_POSITION_TABLE.rows) == 29


def test_the_first_position_table_does_not_close_and_says_by_how_much() -> None:
    """المجموعُ المُعلَنُ مكذوبٌ حسابًا: 12,139 وقعةً لا صفَّ لها."""

    reading = closure_of(THE_FIRST_POSITION_TABLE)
    assert reading.standing is ClosureStanding.CELLS_FALL_SHORT
    assert reading.stated_grand_total == 78_215
    assert reading.cell_sum == 66_076
    assert reading.shortfall == 12_139
    assert reading.shortfall_share == pytest.approx(15.520, abs=1e-3)
    assert THE_FIRST_POSITION_TABLE.stated_column_totals == (
        47_487,
        12_485,
        7_904,
        10_339,
    )
    assert reading.column_shortfalls == (7_231, 4_084, 667, 157)
    assert sum(reading.column_shortfalls) == reading.shortfall


def test_every_printed_row_agrees_with_its_own_total() -> None:
    """العجزُ صفٌّ ساقطٌ لا زلّةُ جمعٍ: كلُّ صفٍّ مطبوعٍ متّسقٌ مع مجموعه."""

    for table, expected in (
        (THE_FIRST_POSITION_TABLE, 66_076),
        (THE_LAST_POSITION_TABLE, 78_076),
    ):
        assert sum(sum(cells) for _, cells in table.rows) == expected
        for _, cells in table.rows:
            assert len(cells) == len(THE_HARAKA_COLUMNS)


def test_the_account_is_derived_from_the_cells_not_the_stated_total() -> None:
    """المحاسبةُ تقوم على الخلايا وحدَها، فمقامُ الأوّل 66,076 لا 78,215."""

    first = bit_account(THE_FIRST_POSITION_TABLE)
    assert first.occurrences == 66_076
    assert first.live_letters == 27
    last = bit_account(THE_LAST_POSITION_TABLE)
    assert last.occurrences == 78_076
    assert last.live_letters == 29


def test_the_bit_quantities_are_the_measured_ones() -> None:
    """البتّاتُ مشتقّةٌ عند القراءة، وهذه قيمُها على الجدولين المُودَعين."""

    first = bit_account(THE_FIRST_POSITION_TABLE)
    assert first.haraka_entropy == pytest.approx(1.579090, abs=1e-6)
    assert first.conditional_haraka_entropy == pytest.approx(1.282838, abs=1e-6)
    assert first.mutual_information == pytest.approx(0.296253, abs=1e-6)
    assert first.explained_share == pytest.approx(18.761, abs=1e-3)

    last = bit_account(THE_LAST_POSITION_TABLE)
    assert last.haraka_entropy == pytest.approx(1.876082, abs=1e-6)
    assert last.conditional_haraka_entropy == pytest.approx(1.682363, abs=1e-6)
    assert last.mutual_information == pytest.approx(0.193719, abs=1e-6)
    assert last.explained_share == pytest.approx(10.326, abs=1e-3)


def test_the_identities_hold_exactly() -> None:
    """I = H(ح)+H(ر)−H(ح,ر)، والشرطيّةُ متمِّمتُها، والفائضُ بُعدٌ عن بتَّين."""

    for table in (THE_FIRST_POSITION_TABLE, THE_LAST_POSITION_TABLE):
        account = bit_account(table)
        assert account.mutual_information == pytest.approx(
            account.haraka_entropy - account.conditional_haraka_entropy, abs=1e-12
        )
        assert account.uniform_haraka_slack == pytest.approx(
            2.0 - account.haraka_entropy, abs=1e-12
        )
        assert 0.0 <= account.mutual_information <= account.haraka_entropy
        assert account.haraka_entropy <= math.log2(len(THE_HARAKA_COLUMNS))
        assert account.letter_entropy <= math.log2(account.live_letters)
        assert account.bits_saved_by_the_letter() == pytest.approx(
            account.haraka_bits_unconditioned() - account.haraka_bits_conditioned(),
            abs=1e-6,
        )


def test_the_dependence_is_far_above_chance_and_still_small() -> None:
    """معنويّةٌ بمئات الأضعاف، وأثرٌ دون خُمس الإنتروبيا: مقداران لا واحد."""

    for table, floor_multiple in (
        (THE_FIRST_POSITION_TABLE, 300.0),
        (THE_LAST_POSITION_TABLE, 200.0),
    ):
        account = bit_account(table)
        assert account.times_chance_level > floor_multiple
        assert account.explained_share < 20.0


def test_excluding_the_seventeen_moves_the_haraka_account_by_under_4e_4() -> None:
    """مقاديرُ الحركة تتحرّك دون 4×10⁻⁴ بتٍّ، وهذا مقيسٌ لا مُطَمْأنٌ إليه."""

    whole = bit_account(THE_LAST_POSITION_TABLE)
    trimmed_table = table_without_letter(THE_LAST_POSITION_TABLE, "ا")
    trimmed = bit_account(trimmed_table)

    assert trimmed_table.stated_grand_total == 78_059
    assert trimmed.occurrences == 78_059
    assert trimmed.live_letters == 28
    for whole_value, trimmed_value in (
        (whole.haraka_entropy, trimmed.haraka_entropy),
        (whole.mutual_information, trimmed.mutual_information),
        (whole.conditional_haraka_entropy, trimmed.conditional_haraka_entropy),
    ):
        assert abs(trimmed_value - whole_value) < 4e-4
    assert trimmed.explained_share == pytest.approx(whole.explained_share, abs=2e-2)
    assert closure_of(trimmed_table).standing is ClosureStanding.CLOSES_EXACTLY


def test_excluding_the_seventeen_moves_the_letter_account_measurably() -> None:
    """ولا يُعَمَّم النفيُ: حذفُ صفٍّ يُغيّر إنتروبيا الحرف ألفَي جزءٍ من مليون."""

    whole = bit_account(THE_LAST_POSITION_TABLE)
    trimmed = bit_account(table_without_letter(THE_LAST_POSITION_TABLE, "ا"))

    assert abs(trimmed.letter_entropy - whole.letter_entropy) == pytest.approx(
        2.109e-3, rel=1e-2
    )
    assert abs(trimmed.joint_entropy - whole.joint_entropy) == pytest.approx(
        1.743e-3, rel=1e-2
    )
    assert abs(trimmed.letter_entropy - whole.letter_entropy) > 4e-4


def test_excluding_an_absent_row_is_refused() -> None:
    """استبعادُ صفٍّ غائبٍ وهمٌ يُرفَع، فلا يُظَنّ أنّ شيئًا أُخرِج."""

    with pytest.raises(PositionHarakaBitAccountError):
        table_without_letter(THE_FIRST_POSITION_TABLE, "ء")


def test_the_exclusions_are_recorded_with_their_counts_and_places() -> None:
    """ثلاثةُ استبعاداتٍ مُسمّاةٌ بعدّتها؛ والمحوُ ممنوعٌ والتسجيلُ لازم."""

    assert len(THE_DECLARED_EXCLUSIONS) == 3
    counts = {
        exclusion.exclusion_name: exclusion.excluded_occurrences
        for exclusion in THE_DECLARED_EXCLUSIONS
    }
    assert sorted(counts.values()) == [17, 139, 12_139]
    before = [
        exclusion
        for exclusion in THE_DECLARED_EXCLUSIONS
        if exclusion.excluded_before_deposit
    ]
    assert len(before) == 1
    assert before[0].excluded_occurrences == 139
    for exclusion in THE_DECLARED_EXCLUSIONS:
        assert exclusion.reason.strip()
        assert exclusion.table_name in {
            THE_FIRST_POSITION_TABLE.table_name,
            THE_LAST_POSITION_TABLE.table_name,
        }


def test_the_letter_contributions_sum_to_the_mutual_information() -> None:
    """تفكيكُ المعلومة إلى الحروف تامٌّ: مجموعُ الأنصبة هو I نفسُها."""

    for table in (THE_FIRST_POSITION_TABLE, THE_LAST_POSITION_TABLE):
        account = bit_account(table)
        readings = letter_information(table)
        assert len(readings) == account.live_letters
        assert sum(item.contribution for item in readings) == pytest.approx(
            account.mutual_information, abs=1e-12
        )
        assert [item.contribution for item in readings] == sorted(
            (item.contribution for item in readings), reverse=True
        )


def test_the_heaviest_carriers_are_not_the_commonest_letters() -> None:
    """أثقلُ الحروف معلومةً ليس أكثرَها ورودًا: الياءُ تتصدّر والميمُ أكثرُ عدّةً."""

    readings = letter_information(THE_LAST_POSITION_TABLE)
    assert readings[0].letter == "ي"
    heaviest = readings[0]
    commonest = max(readings, key=lambda item: item.occurrences)
    assert commonest.letter == "م"
    assert commonest.occurrences > heaviest.occurrences
    assert heaviest.contribution > commonest.contribution


def test_entropy_refuses_an_empty_or_negative_table() -> None:
    """إنتروبيا على مجموعٍ غيرِ موجبٍ أو عدّةٍ سالبةٍ تُرفَع لا تُسامَح."""

    with pytest.raises(PositionHarakaBitAccountError):
        entropy_of([0, 0])
    with pytest.raises(PositionHarakaBitAccountError):
        entropy_of([5, -1])
    assert entropy_of([1, 1, 1, 1]) == pytest.approx(2.0, abs=1e-12)
    assert entropy_of([7, 0, 0, 0]) == pytest.approx(0.0, abs=1e-12)


def test_a_malformed_deposit_is_refused_at_construction() -> None:
    """صفٌّ مكرَّرٌ أو ناقصُ الخلايا أو مقامٌ غيرُ موجبٍ يُرفَع عند الإنشاء."""

    good = (("ب", (1, 2, 3, 4)),)
    DepositedTable(
        table_name="تجربة",
        position="موضع",
        rows=good,
        stated_grand_total=10,
        stated_column_totals=(1, 2, 3, 4),
        standing=TableStanding.QUOTED_NOT_REDERIVED,
    )
    for rows, total, columns in (
        ((("ب", (1, 2, 3, 4)), ("ب", (1, 1, 1, 1))), 14, (2, 3, 4, 5)),
        ((("ب", (1, 2, 3)),), 6, (1, 2, 3, 0)),
        ((("ب", (1, 2, 3, -4)),), 2, (1, 2, 3, -4)),
        (good, 0, (1, 2, 3, 4)),
        ((), 10, (1, 2, 3, 4)),
        (good, 10, (1, 2, 3)),
    ):
        with pytest.raises(PositionHarakaBitAccountError):
            DepositedTable(
                table_name="تجربة",
                position="موضع",
                rows=rows,  # type: ignore[arg-type]
                stated_grand_total=total,
                stated_column_totals=columns,
                standing=TableStanding.QUOTED_NOT_REDERIVED,
            )


def test_an_account_on_no_occurrence_is_refused() -> None:
    """محاسبةٌ على صفرِ وقعاتٍ ليست محاسبةً، فتُرفَع."""

    with pytest.raises(PositionHarakaBitAccountError):
        BitAccount(
            table_name="تجربة",
            occurrences=0,
            live_letters=3,
            haraka_entropy=1.0,
            letter_entropy=1.0,
            joint_entropy=2.0,
        )


def test_both_tables_are_quoted_and_neither_is_rederived() -> None:
    """منزلةُ الأعداد منقولةٌ في الجدولين معًا، ولا مقامَ مشتركٌ بينهما."""

    for table in (THE_FIRST_POSITION_TABLE, THE_LAST_POSITION_TABLE):
        assert table.standing is TableStanding.QUOTED_NOT_REDERIVED
    assert THE_FIRST_POSITION_TABLE.stated_grand_total != (
        THE_LAST_POSITION_TABLE.stated_grand_total
    )
    assert bit_account(THE_FIRST_POSITION_TABLE).occurrences != (
        bit_account(THE_LAST_POSITION_TABLE).occurrences
    )


def test_each_named_residual_is_prefixed_by_its_own_key() -> None:
    """كلُّ بقيّةٍ مُسمّاةٍ تبدأ بمفتاحها، فلا يُنقَل نصٌّ عن موضعه بلا اسمه."""

    assert len(POSITION_HARAKA_BIT_ACCOUNT_NAMED_RESIDUALS) == 8
    for key, text in POSITION_HARAKA_BIT_ACCOUNT_NAMED_RESIDUALS.items():
        assert text.startswith(f"{key}: ")
