"""تحضيرُ جولةٍ ثانيةٍ لم تُشغَّل: أجناسٌ تُولَد مُعلَنة، ووقفٌ يُسمّى نوعَه.

تُثبِّت هذه الشواهدُ ستّة أمور: الأجناسُ الثلاثةُ مواليدُ مُعلَنةٌ لا نسخٌ
للقالب، ولا شيءَ ههنا يدّعي تشغيلًا فـ`was_run` `False` بالبنية، ووقفُ
البايتات غيرُ وقفِ الختم غيرِ المُعلَن فلا يُجمَعان ولا يرفع أحدَهما رافعُ
الآخر، وأرقامُ ما قبل الاختبار تدخل واردةً ولا تُوسَم مولَّدةً من قرصنا،
ومدوّنةُ التدقيق المُودَعةُ ليست بايتاتِ أيٍّ من الطبقات الثلاث، والشرطُ
الانتظاريُّ مُسجَّلٌ مسبقًا وموضعُ فتحه طلبٌ مستقلّ.
"""

from dataclasses import fields, replace

import pytest

from alghanem.arabic.audit_corpus_deposit import (
    THE_AUDIT_CORPUS,
    DepositedFigure,
    FigureProvenance,
    vendored_audit_corpus_path,
)
from alghanem.arabic.hamil_round_two_preregistration import (
    A_BLOCK_ON_BYTES_IS_NOT_A_BLOCK_ON_AN_UNDECLARED_SEAL,
    A_PRE_TEST_DECLARATION_IS_NOT_A_MEASUREMENT_HERE,
    A_PREPARED_AUDIT_IS_NOT_A_RUN_AUDIT,
    ROUND_TWO_NAMED_RESIDUALS,
    THE_CARRIER_STATE_BIRTH_WAITING_CONDITION,
    THE_ROUND_TWO_BIRTHS,
    AuditGenus,
    BlockingKind,
    DeclaredGenusBirth,
    RoundTwoError,
    WaitingCondition,
)


def test_each_declared_genus_is_born_exactly_once() -> None:
    """ثلاثةُ أجناسٍ وثلاثةُ مواليد، والقالبُ يُوسَّع جنسًا لا يُنسَخ نسخًا."""

    born = [birth.genus for birth in THE_ROUND_TWO_BIRTHS]
    assert len(born) == len(set(born)) == len(AuditGenus) == 3
    assert set(born) == set(AuditGenus)


def test_nothing_here_declares_itself_run() -> None:
    """التحضيرُ ليس تشغيلًا: `was_run` مُشتَقٌّ ثابتٌ لا حقلٌ يُكتَب."""

    for birth in THE_ROUND_TWO_BIRTHS:
        assert birth.was_run is False
    assert THE_CARRIER_STATE_BIRTH_WAITING_CONDITION.is_run_here is False
    names = {field.name for field in fields(DeclaredGenusBirth)}
    assert "was_run" not in names


def test_no_prepared_type_carries_a_verdict_or_result_field() -> None:
    """الحكمُ مُشتَقٌّ لا مكتوب، ولا نتيجةَ في وديعةٍ لم تُشغَّل بعد."""

    for datatype in (DeclaredGenusBirth, WaitingCondition):
        names = {field.name for field in fields(datatype)}
        assert not any(
            token in name
            for name in names
            for token in ("verdict", "result", "outcome", "verified")
        )


def test_only_the_waqf_layer_is_blocked_on_bytes_alone() -> None:
    """وقفُ البايتات واحدٌ، ووقفُ الختم غيرِ المُعلَن اثنان؛ ولا يُجمَعان."""

    by_genus = {birth.genus: birth for birth in THE_ROUND_TWO_BIRTHS}
    waqf = by_genus[AuditGenus.UTHMANI_WAQF_LAYER]
    assert waqf.blocking is BlockingKind.BYTES_NOT_DEPOSITED_HERE
    assert waqf.bytes_would_suffice is True
    assert waqf.seal == "16d65358"
    for genus in (AuditGenus.ILAL_LAYER, AuditGenus.FIELD_112_LAWS):
        birth = by_genus[genus]
        assert birth.blocking is BlockingKind.SEAL_NOT_YET_DECLARED
        assert birth.bytes_would_suffice is False
        assert birth.seal is None


def test_a_seal_and_its_blocking_kind_may_not_disagree() -> None:
    """ختمٌ مُعلَنٌ مع وقفِ ختمٍ غيرِ مُعلَنٍ تناقضٌ يُرفَض عند الإنشاء."""

    waqf = next(
        birth
        for birth in THE_ROUND_TWO_BIRTHS
        if birth.genus is AuditGenus.UTHMANI_WAQF_LAYER
    )
    with pytest.raises(RoundTwoError):
        replace(waqf, blocking=BlockingKind.SEAL_NOT_YET_DECLARED)
    with pytest.raises(RoundTwoError):
        replace(waqf, seal=None)
    ilal = next(
        birth for birth in THE_ROUND_TWO_BIRTHS if birth.genus is AuditGenus.ILAL_LAYER
    )
    with pytest.raises(RoundTwoError):
        replace(ilal, seal="deadbeef")


def test_a_pre_test_figure_may_not_be_marked_generated_from_our_disk() -> None:
    """رقمُ ما قبل الاختبار واردٌ من إعلانهم، ووسمُه مولَّدًا يُرفَض ههنا."""

    waqf = next(
        birth
        for birth in THE_ROUND_TWO_BIRTHS
        if birth.genus is AuditGenus.UTHMANI_WAQF_LAYER
    )
    with pytest.raises(RoundTwoError):
        replace(
            waqf,
            declared_figures=(
                DepositedFigure(
                    name="نسبةُ المواءمة",
                    value="99.03%",
                    provenance=FigureProvenance.GENERATED_FROM_THE_DISK_AT_DEPOSIT,
                ),
            ),
        )


def test_every_declared_figure_entered_as_quoted_incoming() -> None:
    """أربعةُ أرقامٍ مُعلَنةٍ قبل الاختبار، كلُّها واردةٌ لا مولَّدة."""

    figures = [
        figure for birth in THE_ROUND_TWO_BIRTHS for figure in birth.declared_figures
    ]
    assert len(figures) == 4
    assert all(figure.is_generated is False for figure in figures)
    values = {figure.value for figure in figures}
    assert {"99.03%", "754", "86.6%"} <= values


def test_what_would_lift_each_block_is_named_and_not_left_blank() -> None:
    """لكلّ وقفٍ رافعٌ مُسمًّى؛ ووقفٌ بلا رافعٍ مُسمًّى وقفٌ بلا باب."""

    for birth in THE_ROUND_TWO_BIRTHS:
        assert birth.what_would_lift_it.strip()
        with pytest.raises(RoundTwoError):
            replace(birth, what_would_lift_it="   ")


def test_the_audit_corpus_is_not_mistaken_for_a_round_two_layer() -> None:
    """المُودَعُ اليومَ مدوّنةُ تدقيقٍ واحدة، وليست بايتاتِ أيّ طبقةٍ من الثلاث."""

    for birth in THE_ROUND_TWO_BIRTHS:
        if birth.seal is not None:
            assert not THE_AUDIT_CORPUS.sha256_hex.startswith(birth.seal)


def test_the_carrier_state_condition_is_preregistered_and_opened_elsewhere() -> None:
    """الشرطُ سُجِّل قبل التشغيل، وما أنهى الانتظارَ مُسمًّى، والفتحُ في طلبٍ آخر."""

    condition = THE_CARRIER_STATE_BIRTH_WAITING_CONDITION
    assert "حامل" in condition.subject
    assert condition.the_condition.strip()
    assert "بوّابة" in condition.what_discharged_it
    assert "طلبٌ مستقلٌّ" in condition.opens_where
    assert condition.is_run_here is False
    with pytest.raises(RoundTwoError):
        replace(condition, what_discharged_it=" ")


def test_the_named_residuals_open_with_their_own_key() -> None:
    """ثلاثةُ بواقٍ مُسمّاةٍ، كلٌّ يفتتح نصَّه باسمه، وأرقامُها في نصوصها."""

    assert set(ROUND_TWO_NAMED_RESIDUALS) == {
        "A_PREPARED_AUDIT_IS_NOT_A_RUN_AUDIT",
        "A_BLOCK_ON_BYTES_IS_NOT_A_BLOCK_ON_AN_UNDECLARED_SEAL",
        "A_PRE_TEST_DECLARATION_IS_NOT_A_MEASUREMENT_HERE",
    }
    for key, text in ROUND_TWO_NAMED_RESIDUALS.items():
        assert text.startswith(f"{key}: ")
    assert "was_run" in A_PREPARED_AUDIT_IS_NOT_A_RUN_AUDIT
    assert "16d65358" in A_BLOCK_ON_BYTES_IS_NOT_A_BLOCK_ON_AN_UNDECLARED_SEAL
    assert "86.6%" in A_PRE_TEST_DECLARATION_IS_NOT_A_MEASUREMENT_HERE


def test_the_module_reads_no_bytes_and_imports_neither_kernel_nor_program() -> None:
    """لا قراءةَ بايتاتٍ ههنا، ولا استيرادَ من `kernel/` ولا من `program/`."""

    source = (
        vendored_audit_corpus_path().parent.parent
        / "src"
        / "alghanem"
        / "arabic"
        / "hamil_round_two_preregistration.py"
    ).read_text(encoding="utf-8")
    assert "alghanem.kernel" not in source
    assert "alghanem.program" not in source
    assert "read_bytes" not in source
    assert "read_audit_corpus_bytes" not in source
