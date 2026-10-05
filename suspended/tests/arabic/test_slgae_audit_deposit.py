"""إيداعُ تدقيق SLGAE: تسجيلٌ بقيدٍ لا تصديق.

تُثبِّت هذه الشواهدُ ستّة أمور: المفرداتُ مغلقةٌ تُرفَض القيمةُ خارجها عند
الإنشاء، والعددُ مكتملٌ فلا صامدَ بلا مقياسٍ مستقلّ ولا ساقطَ بلا نوعٍ مُسمًّى،
وكلُّ رقمٍ منقولٍ له نظيرٌ في السجلّ الواحد `REPORTED_UNVERIFIED_FIGURES`،
وما يُقاس من هذه الشجرة يُقاس عند القراءة ولا يُجمَّد، والسندُ الساقطُ جنسٌ
ثالثٌ لا يُقرأ نقضًا للنتيجة، والوحدةُ خاملةٌ سلطويًّا لا تقرؤها بوّابةٌ في
`kernel/` ولا تستورد منه شيئًا.
"""

import ast
import pkgutil
from dataclasses import fields, replace
from pathlib import Path

import pytest

import alghanem.kernel as kernel_package
from alghanem.arabic.slgae_audit_deposit import (
    A_COUNT_FROM_ANOTHER_TREE_IS_NOT_A_MEASUREMENT_HERE,
    A_DEPOSITED_AUDIT_IS_NOT_A_RERUN_EXPERIMENT,
    A_NAMED_CRITERION_IS_NOT_A_BUILT_GATE,
    A_NAMED_FAILURE_IS_DEPOSITED_AS_ONE,
    A_WITHDRAWN_SUPPORT_IS_NOT_A_REFUTED_RESULT,
    SLGAE_AUDIT_DEPOSIT,
    SLGAE_NAMED_RESIDUALS,
    THE_FIGURES_LIVE_IN_THE_ONE_REGISTER_NOT_IN_A_SECOND_STORE,
    BuildStanding,
    FailureGenus,
    IndependentMeasure,
    OwnBuildRecord,
    QuotedAgainstMeasured,
    QuotedFigure,
    ReDerivability,
    SlgaeAuditDeposit,
    SlgaeDepositError,
    SlgaeDiscrepancy,
    SlgaeFinding,
    SlgaeOutcome,
    SlgaeSection,
    SupportDefect,
    SupportStanding,
    WithdrawnSupportRecord,
    counted_test_functions,
    source_module_count,
    the_quoted_build_counts_against_disk,
)
from alghanem.program.direct_certainty import (
    REPORTED_UNVERIFIED_FIGURES,
    CertaintySourceGenus,
    FigureConstraint,
    figures_by_constraint,
)

_QUOTED = ReDerivability.NOT_RE_DERIVABLE_IN_THIS_TREE


def _figure(subject: str = "موضوع", text: str = "رقم") -> QuotedFigure:
    return QuotedFigure(subject=subject, figure_text=text, rederivability=_QUOTED)


# --- انغلاقُ المفردات -----------------------------------------------------------


def test_a_figure_without_a_subject_or_a_constraint_is_refused() -> None:
    with pytest.raises(SlgaeDepositError, match="موضوعُ الرقم"):
        QuotedFigure(subject="  ", figure_text="رقم", rederivability=_QUOTED)
    with pytest.raises(SlgaeDepositError, match="نصُّ الرقم"):
        QuotedFigure(subject="موضوع", figure_text=" ", rederivability=_QUOTED)
    with pytest.raises(SlgaeDepositError, match="ReDerivability"):
        QuotedFigure(
            subject="موضوع",
            figure_text="رقم",
            rederivability="غير_قابل",  # type: ignore[arg-type]
        )


def test_a_held_finding_without_an_independent_measure_is_refused() -> None:
    with pytest.raises(SlgaeDepositError, match="لا صمودَ بلا مقياسٍ"):
        SlgaeFinding(
            experiment="تجربة",
            section=SlgaeSection.GROSS_STRUCTURE,
            statement="دعوى",
            figure=_figure(),
            outcome=SlgaeOutcome.HELD_WITH_INDEPENDENT_MEASURE,
            independent_measure=None,
            failure_genus=None,
        )


def test_a_failed_finding_without_a_named_genus_is_refused() -> None:
    with pytest.raises(SlgaeDepositError, match="لا سقوطَ بلا نوعٍ"):
        SlgaeFinding(
            experiment="تجربة",
            section=SlgaeSection.MARKOV_FIVE_YA,
            statement="دعوى",
            figure=_figure(),
            outcome=SlgaeOutcome.FAILED_NAMED,
            independent_measure=None,
            failure_genus=None,
        )


def test_a_finding_may_not_carry_both_a_measure_and_a_failure_genus() -> None:
    with pytest.raises(SlgaeDepositError, match="لا يحمل نوعَ سقوط"):
        SlgaeFinding(
            experiment="تجربة",
            section=SlgaeSection.GROSS_STRUCTURE,
            statement="دعوى",
            figure=_figure(),
            outcome=SlgaeOutcome.HELD_WITH_INDEPENDENT_MEASURE,
            independent_measure=IndependentMeasure.PREREGISTERED_PREDICTION,
            failure_genus=FailureGenus.FELL_STATISTICALLY,
        )
    with pytest.raises(SlgaeDepositError, match="لا يحمل مقياسَ صمود"):
        SlgaeFinding(
            experiment="تجربة",
            section=SlgaeSection.GROSS_STRUCTURE,
            statement="دعوى",
            figure=_figure(),
            outcome=SlgaeOutcome.FAILED_NAMED,
            independent_measure=IndependentMeasure.MEASURED_OFF_THE_RULE,
            failure_genus=FailureGenus.FELL_STATISTICALLY,
        )


def test_our_own_build_is_not_filed_as_a_finding_of_the_external_research() -> None:
    with pytest.raises(SlgaeDepositError, match="بناؤنا نحن لا يُسجَّل"):
        SlgaeFinding(
            experiment="تجربة",
            section=SlgaeSection.OUR_OWN_BUILD,
            statement="دعوى",
            figure=_figure(),
            outcome=SlgaeOutcome.FAILED_NAMED,
            independent_measure=None,
            failure_genus=FailureGenus.FELL_STATISTICALLY,
        )


def test_no_standing_other_than_withdrawn_support_enters_that_door() -> None:
    with pytest.raises(SlgaeDepositError, match="RESULT_STANDS_SUPPORT_WITHDRAWN"):
        WithdrawnSupportRecord(
            subject="موضوع",
            statement="بيان",
            standing="قائم",  # type: ignore[arg-type]
            defect=SupportDefect.CIRCULAR_ON_THE_TAGS,
        )


def test_a_discrepancy_without_a_figure_is_refused() -> None:
    with pytest.raises(SlgaeDepositError, match="بلا رقمٍ مُسجَّلٍ"):
        SlgaeDiscrepancy(
            name="اسم",
            statement="بيان",
            figures=(),
            checkable_if_bytes_were_deposited=False,
        )


def test_a_discrepancy_may_not_claim_a_figure_re_derivable_here() -> None:
    with pytest.raises(SlgaeDepositError, match="وصلت سردًا"):
        SlgaeDiscrepancy(
            name="اسم",
            statement="بيان",
            figures=(
                QuotedFigure(
                    subject="موضوع",
                    figure_text="رقم",
                    rederivability=ReDerivability.RE_DERIVABLE_FROM_THIS_TREE,
                ),
            ),
            checkable_if_bytes_were_deposited=False,
        )


def test_a_comparison_below_one_is_refused() -> None:
    with pytest.raises(SlgaeDepositError, match="دون الواحد"):
        QuotedAgainstMeasured(subject="موضوع", quoted=0, measured=1)


# --- اكتمالُ العدد وتغطيتُه ------------------------------------------------------


def test_the_deposit_names_thirteen_failures_and_four_discrepancies() -> None:
    assert SLGAE_AUDIT_DEPOSIT.failure_count == 13
    assert len(SLGAE_AUDIT_DEPOSIT.failures) == 13
    assert len(SLGAE_AUDIT_DEPOSIT.discrepancies) == 4
    assert len(SLGAE_AUDIT_DEPOSIT.held) == 10


def test_no_held_finding_lacks_a_named_independent_measure() -> None:
    for finding in SLGAE_AUDIT_DEPOSIT.held:
        assert finding.held
        assert isinstance(finding.independent_measure, IndependentMeasure)
        assert finding.failure_genus is None


def test_every_failure_carries_its_genus_and_the_genera_are_not_one() -> None:
    genera = {finding.failure_genus for finding in SLGAE_AUDIT_DEPOSIT.failures}
    assert None not in genera
    assert len(genera) > 1
    split = SLGAE_AUDIT_DEPOSIT.failures_by_genus
    assert set(split) == set(FailureGenus)
    assert sum(len(findings) for findings in split.values()) == 13


def test_the_five_named_failure_genera_of_the_report_are_all_present() -> None:
    split = SLGAE_AUDIT_DEPOSIT.failures_by_genus
    for genus in (
        FailureGenus.BEATEN_BY_A_RIVAL,
        FailureGenus.CONTRADICTED_BY_THE_COUNT,
        FailureGenus.FELL_STATISTICALLY,
        FailureGenus.DIRECTION_REVERSED,
        FailureGenus.FRAGILE_UNDER_SCOPE_CHANGE,
        FailureGenus.METHOD_COLLAPSED,
    ):
        assert split[genus], f"نوعُ سقوطٍ بلا سجلٍّ واحد: {genus}"


def test_the_three_research_sections_each_carry_a_record() -> None:
    covered = {
        finding.section
        for finding in (*SLGAE_AUDIT_DEPOSIT.held, *SLGAE_AUDIT_DEPOSIT.failures)
    }
    assert covered == {
        SlgaeSection.GROSS_STRUCTURE,
        SlgaeSection.MARKOV_FIVE_YA,
        SlgaeSection.VOWEL_FIRST_FIVE_KAF,
    }


def test_a_deposit_missing_a_named_section_is_refused() -> None:
    with pytest.raises(SlgaeDepositError, match="موضعٌ مُسمًّى بلا سجلٍّ"):
        SlgaeAuditDeposit(
            held=tuple(
                finding
                for finding in SLGAE_AUDIT_DEPOSIT.held
                if finding.section is not SlgaeSection.MARKOV_FIVE_YA
            ),
            failures=tuple(
                finding
                for finding in SLGAE_AUDIT_DEPOSIT.failures
                if finding.section is not SlgaeSection.MARKOV_FIVE_YA
            ),
            withdrawn_supports=SLGAE_AUDIT_DEPOSIT.withdrawn_supports,
            discrepancies=SLGAE_AUDIT_DEPOSIT.discrepancies,
            own_build=SLGAE_AUDIT_DEPOSIT.own_build,
        )


def test_a_duplicated_experiment_is_refused() -> None:
    with pytest.raises(SlgaeDepositError, match="تجربةٌ مكرّرة"):
        SlgaeAuditDeposit(
            held=SLGAE_AUDIT_DEPOSIT.held,
            failures=(*SLGAE_AUDIT_DEPOSIT.failures, SLGAE_AUDIT_DEPOSIT.failures[0]),
            withdrawn_supports=SLGAE_AUDIT_DEPOSIT.withdrawn_supports,
            discrepancies=SLGAE_AUDIT_DEPOSIT.discrepancies,
            own_build=SLGAE_AUDIT_DEPOSIT.own_build,
        )


def test_a_held_finding_may_not_be_filed_among_the_failures() -> None:
    with pytest.raises(SlgaeDepositError, match="سجلٌّ صامدٌ في باب الساقط"):
        SlgaeAuditDeposit(
            held=SLGAE_AUDIT_DEPOSIT.held,
            failures=(SLGAE_AUDIT_DEPOSIT.held[0],),
            withdrawn_supports=SLGAE_AUDIT_DEPOSIT.withdrawn_supports,
            discrepancies=SLGAE_AUDIT_DEPOSIT.discrepancies,
            own_build=SLGAE_AUDIT_DEPOSIT.own_build,
        )


# --- السندُ الساقطُ جنسٌ ثالث ------------------------------------------------------


def test_the_withdrawn_supports_name_five_distinct_defects() -> None:
    supports = SLGAE_AUDIT_DEPOSIT.withdrawn_supports
    assert len(supports) == 5
    assert {record.defect for record in supports} == set(SupportDefect)
    for record in supports:
        assert record.standing is SupportStanding.RESULT_STANDS_SUPPORT_WITHDRAWN
        assert not record.result_is_refuted


def test_a_withdrawn_support_is_neither_a_held_nor_a_failed_finding() -> None:
    subjects = {record.subject for record in SLGAE_AUDIT_DEPOSIT.withdrawn_supports}
    experiments = {
        finding.experiment
        for finding in (*SLGAE_AUDIT_DEPOSIT.held, *SLGAE_AUDIT_DEPOSIT.failures)
    }
    assert not (subjects & experiments)


# --- التناقضاتُ وقيدُ فحصها ------------------------------------------------------


def test_the_two_arithmetic_discrepancies_wait_on_bytes_never_deposited() -> None:
    by_name = {item.name: item for item in SLGAE_AUDIT_DEPOSIT.discrepancies}
    assert by_name["LambdaIsNotRebuiltFromTheColumn"].checkable_if_bytes_were_deposited
    assert by_name["TheGammaBetaRatioCannotBeChecked"].checkable_if_bytes_were_deposited
    for discrepancy in SLGAE_AUDIT_DEPOSIT.discrepancies:
        assert not discrepancy.was_checked_in_this_tree


def test_no_figure_in_the_deposit_claims_to_be_measured_here() -> None:
    assert not SLGAE_AUDIT_DEPOSIT.any_figure_is_measured_here
    for figure in SLGAE_AUDIT_DEPOSIT.quoted_figures:
        assert figure.rederivability is _QUOTED
        assert not figure.is_measured_in_this_tree


# --- الأرقامُ تسكن السجلَّ الواحد ---------------------------------------------------


def test_every_quoted_figure_has_its_twin_in_the_one_register() -> None:
    registered = {
        (record.subject, record.figure_text) for record in REPORTED_UNVERIFIED_FIGURES
    }
    for figure in SLGAE_AUDIT_DEPOSIT.quoted_figures:
        assert (figure.subject, figure.figure_text) in registered


def test_the_registered_twins_arrived_as_prose_and_none_is_a_measurement() -> None:
    subjects = {figure.subject for figure in SLGAE_AUDIT_DEPOSIT.quoted_figures}
    for record in REPORTED_UNVERIFIED_FIGURES:
        if record.subject in subjects:
            assert record.source_genus is (
                CertaintySourceGenus.PROSE_FROM_ANOTHER_CONVERSATION
            )
            assert not record.source_genus.supports_freeze


def test_the_post_hoc_level_selection_constraint_is_populated_by_this_report() -> None:
    records = figures_by_constraint()[FigureConstraint.POST_HOC_LEVEL_SELECTION]
    assert records
    subjects = {figure.subject for figure in SLGAE_AUDIT_DEPOSIT.quoted_figures}
    for record in records:
        assert record.subject in subjects


def test_the_deposit_opens_no_second_store_of_its_own() -> None:
    source = (
        Path(str(Path(__file__).resolve().parents[2]))
        / "src/alghanem/arabic/slgae_audit_deposit.py"
    )
    text = source.read_text(encoding="utf-8")
    tree = ast.parse(text)
    imported: set[str] = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.ImportFrom) and node.module:
            imported.add(node.module)
        elif isinstance(node, ast.Import):
            imported.update(alias.name for alias in node.names)
    assert not any(name.startswith("alghanem.program") for name in imported)
    assert not any(name.startswith("alghanem.kernel") for name in imported)


# --- ما يُقاس هنا يُقاس ولا يُجمَّد --------------------------------------------------


def test_the_quoted_build_counts_are_compared_with_what_disk_measures() -> None:
    comparisons = the_quoted_build_counts_against_disk()
    assert len(comparisons) == 2
    for comparison in comparisons:
        assert comparison.agrees == (comparison.quoted == comparison.measured)


def test_the_measured_side_is_read_from_disk_at_every_call() -> None:
    first = the_quoted_build_counts_against_disk()
    assert first[0].measured == source_module_count()
    assert first[1].measured == counted_test_functions()


def test_the_measured_counts_are_positive_and_count_this_very_module() -> None:
    assert source_module_count() > 0
    assert counted_test_functions() > 0
    names = {
        path.name
        for path in (
            Path(__file__).resolve().parents[2] / "src" / "alghanem" / "arabic"
        ).glob("*.py")
    }
    assert "slgae_audit_deposit.py" in names


def test_a_disagreeing_comparison_is_reported_and_not_smoothed_over() -> None:
    comparison = QuotedAgainstMeasured(subject="موضوع", quoted=1, measured=2)
    assert not comparison.agrees
    assert replace(comparison, quoted=2).agrees


# --- بناؤنا نحن: الفشلُ المُسمّى يُودَع فشلًا -------------------------------------------


def test_the_undecided_axes_are_deposited_as_block_or_defer_not_as_progress() -> None:
    standings = {record.standing for record in SLGAE_AUDIT_DEPOSIT.own_build}
    assert BuildStanding.BLOCKED_BY_A_MEASURED_ZERO in standings
    assert BuildStanding.DEFERRED_UNDECIDED in standings
    for record in SLGAE_AUDIT_DEPOSIT.own_build:
        assert not record.is_work_in_progress


def test_the_vowel_axis_zero_is_written_as_a_measured_zero() -> None:
    blocked = [
        record
        for record in SLGAE_AUDIT_DEPOSIT.own_build
        if record.standing is BuildStanding.BLOCKED_BY_A_MEASURED_ZERO
    ]
    assert blocked
    assert any("صفر" in record.figure.figure_text for record in blocked)


def test_an_own_build_record_without_a_figure_is_refused() -> None:
    with pytest.raises(SlgaeDepositError, match="مقرونٌ برقمٍ"):
        OwnBuildRecord(
            subject="موضوع",
            statement="بيان",
            standing=BuildStanding.DEFERRED_UNDECIDED,
            figure="رقم",  # type: ignore[arg-type]
        )


# --- السلطة: هذا الإيداع خامل ------------------------------------------------------


def test_the_deposit_declares_itself_inoperative() -> None:
    assert not SLGAE_AUDIT_DEPOSIT.deposit_is_operative


def test_no_type_in_the_deposit_carries_a_verdict_or_a_birth_field() -> None:
    for dataclass_type in (
        QuotedFigure,
        SlgaeFinding,
        WithdrawnSupportRecord,
        SlgaeDiscrepancy,
        OwnBuildRecord,
        QuotedAgainstMeasured,
        SlgaeAuditDeposit,
    ):
        for field in fields(dataclass_type):
            for token in ("verdict", "birth", "certificate", "proof", "freeze"):
                assert token not in field.name


def test_no_kernel_module_reads_this_deposit() -> None:
    for module in pkgutil.iter_modules(kernel_package.__path__):
        path = f"{kernel_package.__path__[0]}/{module.name}.py"
        try:
            with open(path, encoding="utf-8") as handle:
                source = handle.read()
        except OSError:
            continue
        assert "slgae_audit_deposit" not in source


def test_every_residual_is_named_by_its_own_key() -> None:
    for key, text in SLGAE_NAMED_RESIDUALS.items():
        assert text.startswith(key)
    assert set(SLGAE_NAMED_RESIDUALS.values()) == {
        A_DEPOSITED_AUDIT_IS_NOT_A_RERUN_EXPERIMENT,
        THE_FIGURES_LIVE_IN_THE_ONE_REGISTER_NOT_IN_A_SECOND_STORE,
        A_WITHDRAWN_SUPPORT_IS_NOT_A_REFUTED_RESULT,
        A_NAMED_CRITERION_IS_NOT_A_BUILT_GATE,
        A_COUNT_FROM_ANOTHER_TREE_IS_NOT_A_MEASUREMENT_HERE,
        A_NAMED_FAILURE_IS_DEPOSITED_AS_ONE,
    }
