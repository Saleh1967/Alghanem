"""إيداعُ تدقيق «حلقة ث/ع» الأولى: حكمٌ يُعاد حسابًا، لا نقلٌ يُصدَّق.

تُثبِّت هذه الشواهدُ ستّة أمور: المفرداتُ مغلقةٌ تُرفَض القيمةُ خارجها عند
الإنشاء، وحكمُ كلّ فحصٍ مُشتَقٌّ من طرفَيه فينقلب وحدَه إذا بُدِّل رقمٌ، وسترلنج
وبِلّ يُعادان من تنفيذ هذه الشجرة فيكونان تقاطعَ تنفيذين لا نقلًا، والمخالفاتُ
الخمسُ قائمةٌ بالحساب لا موصوفةٌ في نثر، وما وقف على بايتاتٍ لم تُودَع لا يحمل
طرفَين فيُوهِمَ فحصًا لم يقع، والوحدةُ خاملةٌ سلطويًّا لا تستورد `kernel/` ولا
`program/` ولا تقرؤها بوّابة.
"""

import pkgutil
from dataclasses import fields, replace
from pathlib import Path

import pytest

import alghanem.kernel as kernel_package
from alghanem.arabic.hamil_phase1_audit_deposit import (
    A_CONTRADICTION_IS_NAMED_NOT_SOFTENED,
    A_SEAL_FROM_ANOTHER_REPOSITORY_IS_NOT_A_MISSING_OBJECT_HERE,
    A_VERDICT_HERE_IS_RECOMPUTED_NOT_TRANSCRIBED,
    AN_INTERNAL_IDENTITY_IS_NOT_AN_EXTERNAL_CONFIRMATION,
    HAMIL_PHASE1_AUDIT_DEPOSIT,
    HAMIL_PHASE1_NAMED_RESIDUALS,
    ONLY_A_SECOND_IMPLEMENTATION_MAKES_A_CROSS_CHECK,
    READING_A_PASTED_LISTING_IS_NOT_RUNNING_IT,
    THE_CHECKS,
    THE_CLASS_COUNTS,
    THE_CODE_DEFECTS,
    THE_CORPUS_IS_NOT_OURS,
    THE_MARGINALS,
    THE_QAF_ENDINGS,
    THE_TRANSITIONS,
    ArithmeticCheck,
    CheckGenus,
    CheckVerdict,
    CodeDefect,
    DefectGenus,
    ForeignCorpusNote,
    HamilPhase1AuditDeposit,
    HamilPhase1DepositError,
    the_chain_rule_gap,
    the_rate_denominators,
    the_stirling_cross_check,
)
from alghanem.arabic.letter_haraka_partition import bell_number, stirling_second_kind
from alghanem.program.direct_certainty import REPORTED_UNVERIFIED_FIGURES


def _check(left: float, right: float, tolerance: float = 0.0) -> ArithmeticCheck:
    return ArithmeticCheck(
        name="فحصٌ للاختبار",
        statement="بيانٌ للاختبار",
        genus=CheckGenus.RECOMPUTED_FROM_THE_QUOTED_FIGURES,
        left=left,
        right=right,
        tolerance=tolerance,
    )


class TestTheVocabularyIsClosed:
    """المفرداتُ مغلقةٌ، والرفضُ عند الإنشاء لا عند القراءة."""

    def test_a_check_without_a_name_is_refused(self) -> None:
        with pytest.raises(HamilPhase1DepositError):
            replace(_check(1.0, 1.0), name="   ")

    def test_a_genus_outside_the_enumeration_is_refused(self) -> None:
        with pytest.raises(HamilPhase1DepositError):
            replace(_check(1.0, 1.0), genus="مُعادٌ_من_الأرقام_المنقولة_وحدَها")

    def test_a_negative_tolerance_is_refused(self) -> None:
        with pytest.raises(HamilPhase1DepositError):
            replace(_check(1.0, 1.0), tolerance=-0.1)

    def test_a_computable_check_without_two_sides_is_refused(self) -> None:
        with pytest.raises(HamilPhase1DepositError):
            replace(_check(1.0, 1.0), left=None)

    def test_an_uncheckable_check_may_not_carry_sides(self) -> None:
        with pytest.raises(HamilPhase1DepositError):
            replace(_check(1.0, 1.0), genus=CheckGenus.REQUIRES_BYTES_NOT_DEPOSITED)

    def test_a_defect_genus_outside_the_enumeration_is_refused(self) -> None:
        with pytest.raises(HamilPhase1DepositError):
            replace(THE_CODE_DEFECTS[0], genus="قاعدةٌ_معلَنةٌ_لا_تُنفَّذ")

    def test_a_defect_without_a_locus_is_refused(self) -> None:
        with pytest.raises(HamilPhase1DepositError):
            replace(THE_CODE_DEFECTS[0], locus="")

    def test_a_corpus_note_with_a_zero_length_is_refused(self) -> None:
        with pytest.raises(HamilPhase1DepositError):
            replace(HAMIL_PHASE1_AUDIT_DEPOSIT.corpus, their_length=0)


class TestTheVerdictIsRecomputed:
    """الحكمُ يتبع الطرفَين حتمًا؛ ولا حقلَ حكمٍ يُكتَب باليد."""

    def test_no_dataclass_here_carries_a_verdict_field(self) -> None:
        for dataclass_type in (ArithmeticCheck, CodeDefect, ForeignCorpusNote):
            names = {field.name for field in fields(dataclass_type)}
            assert not any("verdict" in name for name in names)

    def test_equal_sides_agree_and_unequal_sides_contradict(self) -> None:
        assert _check(3.0, 3.0).verdict is CheckVerdict.AGREES
        assert _check(3.0, 4.0).verdict is CheckVerdict.CONTRADICTS

    def test_moving_one_side_flips_the_verdict_by_itself(self) -> None:
        agreeing = THE_CHECKS[0]
        assert agreeing.verdict is CheckVerdict.AGREES
        assert replace(agreeing, left=agreeing.left + 1.0).verdict is (
            CheckVerdict.CONTRADICTS
        )

    def test_the_tolerance_is_honoured_in_both_directions(self) -> None:
        assert _check(1.0, 1.05, tolerance=0.1).verdict is CheckVerdict.AGREES
        assert _check(1.0, 0.95, tolerance=0.1).verdict is CheckVerdict.AGREES
        assert _check(1.0, 1.2, tolerance=0.1).verdict is CheckVerdict.CONTRADICTS

    def test_an_uncheckable_check_reports_neither_agreement_nor_contradiction(
        self,
    ) -> None:
        uncheckable = HAMIL_PHASE1_AUDIT_DEPOSIT.by_verdict(
            CheckVerdict.NOT_CHECKABLE_HERE
        )
        assert uncheckable
        for check in uncheckable:
            assert check.genus is CheckGenus.REQUIRES_BYTES_NOT_DEPOSITED
            assert check.gap is None

    def test_the_gap_is_never_zeroed_for_politeness(self) -> None:
        for check in HAMIL_PHASE1_AUDIT_DEPOSIT.by_verdict(CheckVerdict.CONTRADICTS):
            assert check.gap is not None
            assert abs(check.gap) > check.tolerance


class TestTheQuotedIdentitiesAreRecomputed:
    """المتطابقاتُ المُعادةُ من النقل وحدَه، كلُّ واحدةٍ بحسابها."""

    def test_the_four_classes_sum_to_the_quoted_word_total(self) -> None:
        assert sum(THE_CLASS_COUNTS.values()) == 77801

    def test_the_twenty_endings_sum_to_the_qaf_class(self) -> None:
        assert sum(THE_QAF_ENDINGS.values()) == THE_CLASS_COUNTS["ق"]
        assert len(THE_QAF_ENDINGS) == 20

    def test_the_five_marginals_sum_to_the_gate_total(self) -> None:
        assert sum(THE_MARGINALS.values()) == 6236

    def test_the_transition_table_sums_to_the_training_half(self) -> None:
        assert sum(THE_TRANSITIONS.values()) == 3118
        assert len(THE_TRANSITIONS) == len(THE_MARGINALS) ** 2

    def test_the_reconciliation_closes_to_the_letter(self) -> None:
        assert 223611 + 20186 == 243797
        assert 16082 + 5831 - 1727 == 20186


class TestTheCrossCheckIsASecondImplementation:
    """سترلنج وبِلّ وحدَهما تقاطعُ تنفيذين؛ وما سواهما اتّساقٌ داخليّ."""

    def test_every_stirling_figure_is_reproduced_here(self) -> None:
        for check in the_stirling_cross_check():
            assert check.verdict is CheckVerdict.AGREES
            assert check.is_an_external_confirmation

    def test_the_seventeen_digit_figure_matches_this_tree(self) -> None:
        assert stirling_second_kind(28, 4) == 2998587019946701

    def test_the_two_ceilings_match_this_tree(self) -> None:
        assert int(bell_number(112).bit_length()) - 1 in (443, 444)
        assert bell_number(28) > 0

    def test_an_internal_identity_is_not_marked_a_cross_check(self) -> None:
        internal = tuple(
            check
            for check in THE_CHECKS
            if check.genus is CheckGenus.RECOMPUTED_FROM_THE_QUOTED_FIGURES
        )
        assert internal
        for check in internal:
            assert not check.is_an_external_confirmation


class TestTheContradictionsStand:
    """المخالفاتُ الخمسُ قائمةٌ بالحساب، ولا واحدةَ منها موصوفةٌ في نثرٍ فقط."""

    def test_the_chain_rule_is_broken_beyond_the_printed_precision(self) -> None:
        gap = the_chain_rule_gap()
        assert abs(gap) > 0.0001
        assert round(gap, 4) == 0.0316

    def test_no_declared_denominator_yields_the_quoted_rate(self) -> None:
        for value in the_rate_denominators().values():
            assert abs(value - 0.2133) > 0.05

    def test_the_held_out_gain_is_not_the_quoted_one(self) -> None:
        check = next(c for c in THE_CHECKS if c.name == "ربحُ خارج العيّنة")
        assert check.verdict is CheckVerdict.CONTRADICTS
        assert check.right is not None
        assert round(check.right, 2) == 49.89

    def test_the_partition_costs_more_than_no_partition(self) -> None:
        check = next(c for c in THE_CHECKS if c.name == "التقسيمُ بإزاء اللاتقسيم")
        assert check.verdict is CheckVerdict.CONTRADICTS
        assert check.gap is not None
        assert check.gap > 0.0

    def test_the_two_quoted_marginals_disagree_on_t_and_agree_on_c(self) -> None:
        t_check = next(c for c in THE_CHECKS if c.name == "الهامشُ T بين نقلين")
        c_check = next(c for c in THE_CHECKS if c.name == "الهامشُ C بين نقلين")
        assert t_check.verdict is CheckVerdict.CONTRADICTS
        assert c_check.verdict is CheckVerdict.AGREES

    def test_the_deposit_counts_its_contradictions_from_the_checks(self) -> None:
        assert HAMIL_PHASE1_AUDIT_DEPOSIT.contradiction_count == len(
            HAMIL_PHASE1_AUDIT_DEPOSIT.by_verdict(CheckVerdict.CONTRADICTS)
        )
        assert HAMIL_PHASE1_AUDIT_DEPOSIT.contradiction_count >= 5


class TestTheDepositIsComplete:
    """الإيداعُ يغطّي الأجناسَ الثلاثة، ولا يقبل فحصًا مكرّرًا."""

    def test_all_three_check_genera_carry_a_record(self) -> None:
        genera = {check.genus for check in HAMIL_PHASE1_AUDIT_DEPOSIT.checks}
        assert genera == set(CheckGenus)

    def test_all_five_defect_genera_carry_a_record(self) -> None:
        genera = {defect.genus for defect in THE_CODE_DEFECTS}
        assert genera == set(DefectGenus)

    def test_a_duplicate_check_name_is_refused(self) -> None:
        with pytest.raises(HamilPhase1DepositError):
            HamilPhase1AuditDeposit(
                checks=(THE_CHECKS[0], THE_CHECKS[0]),
                defects=THE_CODE_DEFECTS,
                corpus=HAMIL_PHASE1_AUDIT_DEPOSIT.corpus,
            )

    def test_a_deposit_missing_a_genus_is_refused(self) -> None:
        only_internal = tuple(
            check
            for check in THE_CHECKS
            if check.genus is CheckGenus.RECOMPUTED_FROM_THE_QUOTED_FIGURES
        )
        with pytest.raises(HamilPhase1DepositError):
            HamilPhase1AuditDeposit(
                checks=only_internal,
                defects=THE_CODE_DEFECTS,
                corpus=HAMIL_PHASE1_AUDIT_DEPOSIT.corpus,
            )

    def test_a_deposit_without_a_defect_is_refused(self) -> None:
        with pytest.raises(HamilPhase1DepositError):
            HamilPhase1AuditDeposit(
                checks=THE_CHECKS,
                defects=(),
                corpus=HAMIL_PHASE1_AUDIT_DEPOSIT.corpus,
            )

    def test_the_named_residuals_are_seven_and_each_names_itself(self) -> None:
        assert len(HAMIL_PHASE1_NAMED_RESIDUALS) == 7
        for name, note in HAMIL_PHASE1_NAMED_RESIDUALS.items():
            assert note.startswith(f"{name}: ")

    def test_each_residual_constant_is_in_the_register(self) -> None:
        for note in (
            A_VERDICT_HERE_IS_RECOMPUTED_NOT_TRANSCRIBED,
            AN_INTERNAL_IDENTITY_IS_NOT_AN_EXTERNAL_CONFIRMATION,
            ONLY_A_SECOND_IMPLEMENTATION_MAKES_A_CROSS_CHECK,
            A_CONTRADICTION_IS_NAMED_NOT_SOFTENED,
            A_SEAL_FROM_ANOTHER_REPOSITORY_IS_NOT_A_MISSING_OBJECT_HERE,
            READING_A_PASTED_LISTING_IS_NOT_RUNNING_IT,
            THE_CORPUS_IS_NOT_OURS,
        ):
            assert note in HAMIL_PHASE1_NAMED_RESIDUALS.values()


class TestTheForeignCorpusIsNotOurs:
    """مدوّنتُهم ليست مدوّنتنا، والفرقُ مُشتَقٌّ لا مكتوب."""

    def test_the_two_corpora_differ_and_say_so(self) -> None:
        corpus = HAMIL_PHASE1_AUDIT_DEPOSIT.corpus
        assert not corpus.are_the_same_corpus
        assert corpus.byte_gap == 13131

    def test_the_gap_follows_the_lengths_and_is_not_a_field(self) -> None:
        widened = replace(HAMIL_PHASE1_AUDIT_DEPOSIT.corpus, their_length=1_000_000)
        assert widened.byte_gap == 1319901 - 1_000_000

    def test_no_check_claims_to_measure_the_foreign_corpus(self) -> None:
        assert not HAMIL_PHASE1_AUDIT_DEPOSIT.any_check_measures_the_foreign_corpus

    def test_no_defect_claims_to_have_been_run_here(self) -> None:
        for defect in THE_CODE_DEFECTS:
            assert not defect.was_run_in_this_tree


class TestTheUncheckableFiguresAreInTheOneRegister:
    """ما لم يُفحَص ههنا له نظيرٌ في السجلّ الواحد، ولا مخزنَ ثانيَ للأرقام."""

    def test_the_uncheckable_subjects_are_registered(self) -> None:
        subjects = {record.subject for record in REPORTED_UNVERIFIED_FIGURES}
        for check in HAMIL_PHASE1_AUDIT_DEPOSIT.by_verdict(
            CheckVerdict.NOT_CHECKABLE_HERE
        ):
            assert any(check.name in subject for subject in subjects), check.name


class TestTheDepositIsInert:
    """خمولٌ سلطويّ: لا استيرادَ من النواة ولا من البرنامج، ولا قارئَ في النواة."""

    def test_the_module_imports_neither_kernel_nor_program(self) -> None:
        source = Path("src/alghanem/arabic/hamil_phase1_audit_deposit.py").read_text(
            encoding="utf-8"
        )
        assert "alghanem.kernel" not in source
        assert "alghanem.program" not in source
        assert "from ..kernel" not in source
        assert "from ..program" not in source

    def test_no_kernel_module_reads_this_deposit(self) -> None:
        for module in pkgutil.iter_modules(kernel_package.__path__):
            path = Path(kernel_package.__path__[0]) / f"{module.name}.py"
            if not path.is_file():
                continue
            assert "hamil_phase1_audit_deposit" not in path.read_text(encoding="utf-8")

    def test_the_deposit_declares_itself_inoperative(self) -> None:
        assert not HAMIL_PHASE1_AUDIT_DEPOSIT.deposit_is_operative
