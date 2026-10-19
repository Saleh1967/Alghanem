"""القراءةُ الثانية على بايتاتٍ نزلت: حكمٌ يُعاد قياسًا، وتحوُّلٌ يُسمّى نوعَه.

تُثبِّت هذه الشواهدُ ستّة أمور: القياسُ يجري على بايتاتٍ مطابَقةِ الختم لا على
ملفٍّ في موضعٍ، وحكمُ كلّ فحصٍ مُشتَقٌّ من طرفَيه فينقلب وحدَه إذا بُدِّل رقمٌ،
وما بقي موقوفًا لا يحمل طرفًا مقيسًا فيُوهِمَ فحصًا وقع، والتحوُّلُ إلى «مقيسٍ»
لا يصحّ بلا رافعٍ مُسمًّى كما لا تصحّ إعادةُ التجنيس برافع، وقواعدُ العدّ
الأربعُ كلُّها معروضةٌ فلا تُنتقى واحدةٌ لموافقتها، والوحدةُ خاملةٌ سلطويًّا لا
تستورد `kernel/` ولا `program/`.
"""

from dataclasses import fields, replace
from pathlib import Path

import pytest

from alghanem.arabic.audit_corpus_deposit import (
    AUDIT_CORPUS_PATH_VARIABLE,
    vendored_audit_corpus_path,
)
from alghanem.arabic.hamil_audit_second_reading import (
    A_GAP_UNDER_OUR_RULE_DOES_NOT_ATTRIBUTE_ITSELF,
    ARRIVING_BYTES_DO_NOT_LIFT_A_BLOCK_ON_THEIR_MODEL,
    SECOND_READING_NAMED_RESIDUALS,
    THE_COUNTS_AT_MEASUREMENT,
    THE_DENOMINATOR_SWALLOWS_THE_METADATA_FOOTER,
    THE_QUOTED_FIGURES,
    THE_RECORDING_DATE,
    THE_TRANSITIONS_RECORDED,
    AuditCounts,
    BlockedGenus,
    CountingRule,
    SecondReadingCheck,
    SecondReadingError,
    SecondReadingGenus,
    SecondReadingVerdict,
    TransitionRecord,
    count_by_rule,
    measure_the_audit_corpus,
    second_reading_checks,
    the_counts_have_drifted,
    the_measurement_is_possible,
)


@pytest.mark.skipif(
    not the_measurement_is_possible(),
    reason="بايتاتُ مدوّنة التدقيق غيرُ محلولةٍ في هذه البيئة",
)
def test_the_counts_have_not_drifted_from_what_was_recorded() -> None:
    """المُدوَّنُ يُعاد توليدُه من القرص في كلّ نداء، فتُكشَف الزحزحةُ ولا تُخفى."""

    assert the_counts_have_drifted() is False
    assert measure_the_audit_corpus() == THE_COUNTS_AT_MEASUREMENT


@pytest.mark.skipif(
    not the_measurement_is_possible(),
    reason="بايتاتُ مدوّنة التدقيق غيرُ محلولةٍ في هذه البيئة",
)
def test_the_metadata_footer_is_twenty_seven_tokens_inside_their_denominator() -> None:
    """الفرقُ بين المقامين مُشتَقٌّ لا مكتوبٌ في حقلٍ ثالث، وهو 27 رمزًا."""

    counts = measure_the_audit_corpus()
    assert counts.comment_block_tokens == 27
    assert counts.whole_file_tokens == THE_QUOTED_FIGURES["raw_words"]
    assert counts.tokens_outside_the_comment_block < counts.whole_file_tokens


def test_the_derived_footer_count_follows_its_two_sides() -> None:
    """لا حقلَ ثالثًا: تبديلُ طرفٍ يُبدِّل المُشتَقَّ وحدَه بلا كتابة."""

    moved = replace(THE_COUNTS_AT_MEASUREMENT, whole_file_tokens=82_400)
    assert moved.comment_block_tokens == 21
    names = {field.name for field in fields(AuditCounts)}
    assert "comment_block_tokens" not in names


def test_a_count_below_one_is_refused_at_construction() -> None:
    """عددٌ دون الواحد لا يخرج من قياس، والرفضُ عند الإنشاء."""

    with pytest.raises(SecondReadingError):
        replace(THE_COUNTS_AT_MEASUREMENT, distinct_tokens=0)


@pytest.mark.skipif(
    not the_measurement_is_possible(),
    reason="بايتاتُ مدوّنة التدقيق غيرُ محلولةٍ في هذه البيئة",
)
def test_every_declared_rule_is_measured_and_none_is_picked_for_agreeing() -> None:
    """القواعدُ الأربعُ معروضةٌ كلُّها، ولا واحدةَ تُنتقى لأنّها وافقت."""

    text = vendored_audit_corpus_path().read_bytes().decode("utf-8")
    by_rule = {rule: count_by_rule(text, rule) for rule in CountingRule}
    assert len(by_rule) == 4
    assert by_rule[CountingRule.WHITESPACE_TOKENS_IN_THE_WHOLE_FILE] == 82_406
    assert by_rule[CountingRule.WHITESPACE_TOKENS_OUTSIDE_THE_COMMENT_BLOCK] == 82_379
    assert by_rule[CountingRule.DISTINCT_TOKENS_OUTSIDE_THE_COMMENT_BLOCK] == 18_254
    assert by_rule[CountingRule.DISTINCT_MARK_STRIPPED_TOKENS] == 14_873


def test_the_byte_order_mark_is_not_counted_as_a_token() -> None:
    """صدرُ الملفّ يحمل علامةَ ترتيبٍ، وإسقاطُها قاعدةٌ مُعلَنةٌ لا تنظيفٌ صامت."""

    with_mark = "\ufeffبِسْمِ ٱللَّهِ"
    without = "بِسْمِ ٱللَّهِ"
    rule = CountingRule.WHITESPACE_TOKENS_IN_THE_WHOLE_FILE
    assert count_by_rule(with_mark, rule) == count_by_rule(without, rule) == 2


def test_the_comment_block_rule_drops_whole_lines_not_trailing_text() -> None:
    """يُسقَط السطرُ الذي أوّلُ غيرِ بياضه `#`، ولا يُقتطَع من داخل سطر."""

    text = "أ ب\n# وسمٌ في الذيل\nج # ليست بادئة\n"
    outside = CountingRule.WHITESPACE_TOKENS_OUTSIDE_THE_COMMENT_BLOCK
    assert count_by_rule(text, CountingRule.WHITESPACE_TOKENS_IN_THE_WHOLE_FILE) == 10
    assert count_by_rule(text, outside) == 6


@pytest.mark.skipif(
    not the_measurement_is_possible(),
    reason="بايتاتُ مدوّنة التدقيق غيرُ محلولةٍ في هذه البيئة",
)
def test_the_second_reading_names_one_agreement_and_three_contradictions() -> None:
    """الأحكامُ تخرج من الطرفَين: تطابقٌ واحد، ومخالفاتٌ ثلاث، ووقفان."""

    checks = {check.name: check for check in second_reading_checks()}
    assert len(checks) == 6
    verdicts = [check.verdict for check in checks.values()]
    assert verdicts.count(SecondReadingVerdict.AGREES) == 1
    assert verdicts.count(SecondReadingVerdict.CONTRADICTS) == 3
    assert verdicts.count(SecondReadingVerdict.STILL_BLOCKED) == 2
    assert checks["raw_words على الملفّ كلِّه"].gap == 0.0
    assert checks["raw_words خارج كتلة الوسم"].gap == -27.0
    assert checks["بصمةُ الهياكل 14,870"].gap == 3.0
    assert checks["فرقُ المقامين 4,605"].gap == -27.0


@pytest.mark.skipif(
    not the_measurement_is_possible(),
    reason="بايتاتُ مدوّنة التدقيق غيرُ محلولةٍ في هذه البيئة",
)
def test_each_verdict_flips_alone_when_one_side_is_moved() -> None:
    """الحكمُ تابعٌ لا حقل: تحريكُ طرفٍ يقلبه، ولا يُكتَب حكمٌ يخالف طرفَيه."""

    agreeing = next(
        check
        for check in second_reading_checks()
        if check.verdict is SecondReadingVerdict.AGREES
    )
    assert replace(agreeing, measured=agreeing.measured or 0.0 + 1.0).verdict in {
        SecondReadingVerdict.AGREES,
        SecondReadingVerdict.CONTRADICTS,
    }
    moved = replace(agreeing, quoted=(agreeing.quoted or 0.0) + 1.0)
    assert moved.verdict is SecondReadingVerdict.CONTRADICTS
    assert moved.gap == -1.0
    names = {field.name for field in fields(SecondReadingCheck)}
    assert "verdict" not in names and "gap" not in names


@pytest.mark.skipif(
    not the_measurement_is_possible(),
    reason="بايتاتُ مدوّنة التدقيق غيرُ محلولةٍ في هذه البيئة",
)
def test_a_check_blocked_on_their_model_carries_no_measured_side() -> None:
    """ما وقف على نموذجهم لا يتنكّر فحصًا وقع: لا طرفَ مقيسًا ولا فرقًا."""

    blocked = [
        check
        for check in second_reading_checks()
        if check.genus
        is SecondReadingGenus.REQUIRES_THEIR_MODEL_WHICH_BYTES_DO_NOT_LIFT
    ]
    assert len(blocked) == 2
    for check in blocked:
        assert check.measured is None
        assert check.gap is None
        assert check.verdict is SecondReadingVerdict.STILL_BLOCKED


def test_a_blocked_check_refuses_to_carry_a_measured_side() -> None:
    """الرفضُ عند الإنشاء لا عند القراءة؛ فلا يُبنى موقوفٌ ذو طرفَين أصلًا."""

    with pytest.raises(SecondReadingError):
        SecondReadingCheck(
            name="موقوفٌ يتنكّر",
            statement="موقوفٌ على نموذجهم، وقد حُمِّل طرفًا مقيسًا",
            genus=SecondReadingGenus.REQUIRES_THEIR_MODEL_WHICH_BYTES_DO_NOT_LIFT,
            rule=None,
            quoted=5.83,
            measured=5.83,
        )


def test_an_unblocked_check_without_two_sides_or_a_rule_is_refused() -> None:
    """فحصٌ غيرُ موقوفٍ بلا طرفَين ليس فحصًا، وقياسٌ بلا قاعدةٍ ليس قياسًا."""

    with pytest.raises(SecondReadingError):
        SecondReadingCheck(
            name="بلا طرفَين",
            statement="أُعلن مقيسًا ثمّ خلا من طرفٍ",
            genus=SecondReadingGenus.MEASURED_ON_THE_AUDIT_CORPUS,
            rule=CountingRule.WHITESPACE_TOKENS_IN_THE_WHOLE_FILE,
            quoted=1.0,
            measured=None,
        )
    with pytest.raises(SecondReadingError):
        SecondReadingCheck(
            name="بلا قاعدة",
            statement="أُعلن مقيسًا على المدوّنة بلا قاعدةٍ مُعلَنة",
            genus=SecondReadingGenus.MEASURED_ON_THE_AUDIT_CORPUS,
            rule=None,
            quoted=1.0,
            measured=1.0,
        )


def test_the_two_transitions_are_recorded_with_their_date_and_kind() -> None:
    """تحوُّلان: واحدٌ رُفِع وقفُه برافعٍ مُسمًّى، وآخرُ أُعيد تجنيسُه بلا رافع."""

    assert len(THE_TRANSITIONS_RECORDED) == 2
    lifted = [
        record for record in THE_TRANSITIONS_RECORDED if record.the_bytes_lifted_it
    ]
    regenused = [
        record for record in THE_TRANSITIONS_RECORDED if not record.the_bytes_lifted_it
    ]
    assert len(lifted) == len(regenused) == 1
    assert lifted[0].lifted_by is not None
    assert regenused[0].lifted_by is None
    assert regenused[0].became is (
        BlockedGenus.REQUIRES_THEIR_MODEL_WHICH_BYTES_DO_NOT_LIFT
    )
    for record in THE_TRANSITIONS_RECORDED:
        assert record.on_date == THE_RECORDING_DATE
        assert record.was is BlockedGenus.REQUIRES_BYTES_NOT_DEPOSITED
    assert "verdict" not in {field.name for field in fields(TransitionRecord)}


def test_a_lift_without_a_lifter_and_a_regenusing_with_one_are_both_refused() -> None:
    """لا قياسَ بلا رافعٍ مُسمًّى، ولا رافعَ لإعادة تجنيسٍ لم ترفع شيئًا."""

    with pytest.raises(SecondReadingError):
        TransitionRecord(
            check_name="قياسٌ بلا رافع",
            was=BlockedGenus.REQUIRES_BYTES_NOT_DEPOSITED,
            became=BlockedGenus.MEASURED_ON_THE_AUDIT_CORPUS,
            on_date=THE_RECORDING_DATE,
            lifted_by=None,
            note="ادُّعي القياسُ ولم يُسمَّ ما رفع الوقف",
        )
    with pytest.raises(SecondReadingError):
        TransitionRecord(
            check_name="تجنيسٌ برافع",
            was=BlockedGenus.REQUIRES_BYTES_NOT_DEPOSITED,
            became=BlockedGenus.REQUIRES_THEIR_MODEL_WHICH_BYTES_DO_NOT_LIFT,
            on_date=THE_RECORDING_DATE,
            lifted_by="بايتاتٌ نزلت",
            note="نُسب الرفعُ إلى ما لم يرفع",
        )
    with pytest.raises(SecondReadingError):
        TransitionRecord(
            check_name="إلى الجنس نفسِه",
            was=BlockedGenus.REQUIRES_BYTES_NOT_DEPOSITED,
            became=BlockedGenus.REQUIRES_BYTES_NOT_DEPOSITED,
            on_date=THE_RECORDING_DATE,
            lifted_by=None,
            note="لا تحوُّلَ ههنا",
        )


def test_every_transition_names_a_check_that_the_reading_carries() -> None:
    """أسماءُ المتحوِّلَين مذكورةٌ في فحوص القراءة نفسِها لا في نثرٍ منفصل."""

    recorded = {record.check_name for record in THE_TRANSITIONS_RECORDED}
    assert recorded == {"بصمةُ الهياكل 14,870", "ربحُ الزوجيّ المشترك"}


def test_the_measurement_is_a_refusal_when_the_bytes_are_absent(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """غيابُ البايتات يمنع الإخراجَ ولا يُخرِج صفرًا ولا يُسكِت فحصًا."""

    monkeypatch.setenv(AUDIT_CORPUS_PATH_VARIABLE, str(tmp_path / "ليس-هنا.txt"))
    assert the_measurement_is_possible() is False
    with pytest.raises(ValueError):
        second_reading_checks()


def test_the_named_residuals_open_with_their_own_key() -> None:
    """ثلاثةُ بواقٍ مُسمّاةٍ، كلٌّ يفتتح نصَّه باسمه، وأرقامُها في نصوصها."""

    assert set(SECOND_READING_NAMED_RESIDUALS) == {
        "ARRIVING_BYTES_DO_NOT_LIFT_A_BLOCK_ON_THEIR_MODEL",
        "A_GAP_UNDER_OUR_RULE_DOES_NOT_ATTRIBUTE_ITSELF",
        "THE_DENOMINATOR_SWALLOWS_THE_METADATA_FOOTER",
    }
    for key, text in SECOND_READING_NAMED_RESIDUALS.items():
        assert text.startswith(f"{key}: ")
    assert "14,873" in A_GAP_UNDER_OUR_RULE_DOES_NOT_ATTRIBUTE_ITSELF
    assert "4,578" in THE_DENOMINATOR_SWALLOWS_THE_METADATA_FOOTER
    assert "إعادةُ تجنيسٍ" in ARRIVING_BYTES_DO_NOT_LIFT_A_BLOCK_ON_THEIR_MODEL


def test_the_module_imports_neither_kernel_nor_program() -> None:
    """الوحدةُ خاملةٌ سلطويًّا: لا تستورد `kernel/` ولا `program/`."""

    source = (
        vendored_audit_corpus_path().parent.parent
        / "src"
        / "alghanem"
        / "arabic"
        / "hamil_audit_second_reading.py"
    ).read_text(encoding="utf-8")
    assert "alghanem.kernel" not in source
    assert "alghanem.program" not in source
