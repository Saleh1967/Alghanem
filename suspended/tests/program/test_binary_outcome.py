"""اختبارات قاعدة النتيجتين: لا فئةَ ثالثة، ولا رقمَ وسطٍ بلا تصنيف."""

from __future__ import annotations

import pkgutil

import pytest

import alghanem.kernel as kernel_package
from alghanem.program.binary_outcome import (
    BINARY_OUTCOME_NAMED_RESIDUALS,
    REFUSED_CLOSING_PHRASES,
    BinaryOutcomeError,
    ClassifiedAttempt,
    DeeperLayerRecord,
    GapClosureOutcome,
    MidFigureClassification,
    TotalCertaintyRecord,
    classify_attempt,
)
from alghanem.program.direct_certainty import (
    REPORTED_UNVERIFIED_FIGURES,
    CertaintySourceGenus,
    DirectCertaintyStep,
    ProtocolRun,
    StepRecord,
)

_GATE_MODULE = "alghanem.arabic.encoding.contamination_gate"
_GATE_CALLABLE = "derive_negative_filter_blind_spots"


def _run(
    genus: CertaintySourceGenus = CertaintySourceGenus.RERUN_NOW_IN_THIS_PROCESS,
    steps: tuple[DirectCertaintyStep, ...] = tuple(DirectCertaintyStep),
) -> ProtocolRun:
    return ProtocolRun(
        records=tuple(
            StepRecord(
                step=step,
                reproducer_module=_GATE_MODULE,
                reproducer_callable=_GATE_CALLABLE,
                source_genus=genus,
            )
            for step in steps
        )
    )


def _certainty(**overrides: object) -> TotalCertaintyRecord:
    fields: dict[str, object] = {
        "subject": "موضوعٌ مُسمًّى",
        "figure_text": "١٢/١٢",
        "run": _run(),
        "reason": "رقمٌ صريحٌ أُعيد تشغيلُ خطواته الستّ الآن",
    }
    fields.update(overrides)
    return TotalCertaintyRecord(**fields)  # type: ignore[arg-type]


def _deeper(**overrides: object) -> DeeperLayerRecord:
    fields: dict[str, object] = {
        "subject": "اختبارُ سكون الساكنين",
        "narrowed_unknown": "تلوّثٌ إنجليزيٌّ في الملفّ المصدر لم يكن مُسمًّى قبلها",
        "reason": "المحاولةُ لم تُغلِق الفجوة وسمَّت ملوِّثًا لم يكن معروفًا",
    }
    fields.update(overrides)
    return DeeperLayerRecord(**fields)  # type: ignore[arg-type]


# --- الفئتان، ولا ثالثةَ في المفردة ------------------------------------------


def test_the_outcome_vocabulary_holds_exactly_two_members() -> None:
    assert len(GapClosureOutcome) == 2
    assert set(GapClosureOutcome) == {
        GapClosureOutcome.TOTAL_CERTAINTY,
        GapClosureOutcome.DEEPER_LAYER_REVEALED,
    }


def test_both_mid_figure_classifications_are_of_the_second_outcome() -> None:
    assert len(MidFigureClassification) == 2
    for classification in MidFigureClassification:
        assert classification.outcome is GapClosureOutcome.DEEPER_LAYER_REVEALED


# --- الفئة الأولى: محسوبةٌ من المسار المربوط ----------------------------------


def test_a_total_certainty_bound_to_a_complete_rerun_is_admitted() -> None:
    record = _certainty()
    assert record.outcome is GapClosureOutcome.TOTAL_CERTAINTY


def test_a_total_certainty_bound_to_an_incomplete_run_is_refused() -> None:
    run = _run(steps=(DirectCertaintyStep.DATA_PURITY_CHECK,))
    with pytest.raises(BinaryOutcomeError, match="لم يُقبَل تجميدُه"):
        _certainty(run=run)


def test_a_total_certainty_quoted_from_prose_is_refused() -> None:
    run = _run(CertaintySourceGenus.PROSE_FROM_ANOTHER_CONVERSATION)
    with pytest.raises(BinaryOutcomeError, match="لم يُقبَل تجميدُه"):
        _certainty(run=run)


def test_a_total_certainty_without_a_bound_run_is_refused() -> None:
    with pytest.raises(BinaryOutcomeError, match="مربوطٌ بـ`ProtocolRun`"):
        _certainty(run="مسارٌ مذكورٌ في رسالة")


def test_a_total_certainty_without_an_explicit_figure_is_refused() -> None:
    with pytest.raises(BinaryOutcomeError, match="بلا رقمٍ مكتوبٍ"):
        _certainty(figure_text="  ")


def test_a_total_certainty_carrying_a_declared_exception_is_refused() -> None:
    with pytest.raises(BinaryOutcomeError, match="استثناءٍ يحتاج تبريرًا"):
        _certainty(declared_exceptions=("موضعٌ واحدٌ يحتاج تبريرًا",))


# --- الفئة الثانية: تسميةُ ما ضاق به المجهول ----------------------------------


def test_a_deeper_layer_record_names_what_narrowed_the_unknown() -> None:
    record = _deeper()
    assert record.outcome is GapClosureOutcome.DEEPER_LAYER_REVEALED


def test_a_deeper_layer_record_without_a_named_narrowing_is_refused() -> None:
    with pytest.raises(BinaryOutcomeError, match="ما ضاق به المجهول"):
        _deeper(narrowed_unknown="   ")


def test_a_deeper_layer_record_with_an_apologetic_reason_is_refused() -> None:
    with pytest.raises(BinaryOutcomeError, match="بعبارةٍ مُعلَّقة"):
        _deeper(reason="النتيجة جزئية وتحتاج نظرًا")


@pytest.mark.parametrize("phrase", REFUSED_CLOSING_PHRASES)
def test_every_declared_closing_phrase_is_refused(phrase: str) -> None:
    with pytest.raises(BinaryOutcomeError, match="بعبارةٍ مُعلَّقة"):
        _deeper(reason=f"المحاولةُ انتهت: {phrase}")


def test_a_refused_phrase_is_caught_through_its_diacritics() -> None:
    with pytest.raises(BinaryOutcomeError, match="بعبارةٍ مُعلَّقة"):
        _deeper(reason="إشارةٌ أوّليّةٌ تحتاج مزيدًا من العمل")


def test_an_evasive_first_outcome_reason_is_refused_too() -> None:
    with pytest.raises(BinaryOutcomeError, match="بعبارةٍ مُعلَّقة"):
        _certainty(reason="قريب من الهدف بلا استثناء")


# --- الرقمُ الوسط لا يبقى معلَّقًا ---------------------------------------------


def test_a_mid_figure_without_a_classification_is_refused() -> None:
    with pytest.raises(BinaryOutcomeError, match="رقمٌ وسطٌ بلا تصنيف"):
        _deeper(opening_mid_figure="٦٩٫٥٧٪")


def test_a_mid_figure_classified_as_a_wrong_question_is_admitted() -> None:
    record = _deeper(
        opening_mid_figure="٦٩٫٥٧٪",
        mid_figure_classification=(
            MidFigureClassification.CORRECT_MEASUREMENT_ON_A_WRONG_QUESTION
        ),
    )
    assert record.outcome is GapClosureOutcome.DEEPER_LAYER_REVEALED


def test_a_mid_figure_classified_as_missing_data_is_admitted() -> None:
    record = _deeper(
        opening_mid_figure="٦٩٫٥٧٪",
        mid_figure_classification=(
            MidFigureClassification.INCOMPLETE_MEASUREMENT_ON_A_RIGHT_QUESTION
        ),
    )
    assert record.outcome is GapClosureOutcome.DEEPER_LAYER_REVEALED


def test_a_classification_without_a_written_figure_is_refused() -> None:
    with pytest.raises(BinaryOutcomeError, match="بلا رقمٍ مكتوبٍ"):
        _deeper(
            mid_figure_classification=(
                MidFigureClassification.CORRECT_MEASUREMENT_ON_A_WRONG_QUESTION
            )
        )


# --- التصنيف: لا مخرجَ ثالثَ من الدالّة ---------------------------------------


def test_classifying_each_record_returns_its_own_outcome() -> None:
    first = classify_attempt(_certainty())
    second = classify_attempt(_deeper())
    assert first.outcome is GapClosureOutcome.TOTAL_CERTAINTY
    assert second.outcome is GapClosureOutcome.DEEPER_LAYER_REVEALED
    assert first.reason.strip() and second.reason.strip()


def test_an_attempt_of_neither_genus_raises_rather_than_returning() -> None:
    with pytest.raises(BinaryOutcomeError, match="ليست من الفئتين"):
        classify_attempt("نتيجةٌ قريبةٌ من الهدف")  # type: ignore[arg-type]


def test_a_classification_without_a_written_reason_is_refused() -> None:
    with pytest.raises(BinaryOutcomeError, match="بلا علّةٍ مكتوبة"):
        ClassifiedAttempt(outcome=GapClosureOutcome.TOTAL_CERTAINTY, reason="  ")


# --- أرقامُ نصّ القاعدة تخضع لقاعدة المرحلة قبلها ------------------------------


def test_the_figures_of_this_rule_are_filed_as_prose_in_the_one_register() -> None:
    subjects = {record.subject for record in REPORTED_UNVERIFIED_FIGURES}
    assert "تسلسلُ الانزلاق المذكور في قاعدة النتيجتين" in subjects
    assert "الرقمُ الوسط غيرُ المُفسَّر في اختبار CV+CV الأوّل" in subjects
    for record in REPORTED_UNVERIFIED_FIGURES:
        assert not record.source_genus.supports_freeze


# --- السلطة: هذه الوحدة خاملة ------------------------------------------------


def test_no_kernel_module_reads_this_rule() -> None:
    for module in pkgutil.iter_modules(kernel_package.__path__):
        path = f"{kernel_package.__path__[0]}/{module.name}.py"
        try:
            with open(path, encoding="utf-8") as handle:
                source = handle.read()
        except OSError:  # pragma: no cover - a package, not a module file
            continue
        assert "binary_outcome" not in source


def test_every_named_residual_is_reachable_and_says_something() -> None:
    assert len(BINARY_OUTCOME_NAMED_RESIDUALS) == 4
    for name, text in BINARY_OUTCOME_NAMED_RESIDUALS.items():
        assert name.isupper()
        assert name in text
