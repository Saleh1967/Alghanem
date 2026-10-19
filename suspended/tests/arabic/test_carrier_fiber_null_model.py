"""اختباراتُ النموذج الصفريّ: يُشغَّل فعلًا على نصٍّ مُودَعٍ وعلى نصوصٍ مصنوعة."""

from __future__ import annotations

from dataclasses import replace

import pytest

from alghanem.arabic.carrier_fiber_null_model import (
    CARRIER_FIBER_NULL_MODEL_NAMED_RESIDUALS,
    CarrierFiberNullModelError,
    ConditionalIndependenceReadout,
    assess_conditional_independence,
    run_null_model_on_the_deposited_fatiha,
)
from alghanem.arabic.carrier_fiber_preregistration import (
    FROZEN_CARRIER_FIBER_SPECIFICATION,
    CarrierFiberSpecificationContentBinding,
    FiberOutcome,
    PreEvidenceCarrierFiberSpecificationRegistry,
)
from alghanem.arabic.carrier_state_observed_fiber import (
    ObservedFiberTable,
    read_corpus_lines,
    tabulate_observed_fibers,
)
from alghanem.canonical_content import canonical_digest

_ALIF = "\u0627"
_FATHA = "\u064e"
_DAMMA = "\u064f"


def _fast_binding(**overrides: object) -> CarrierFiberSpecificationContentBinding:
    specification = replace(
        FROZEN_CARRIER_FIBER_SPECIFICATION,
        revision_id="probe-revision",
        revision_sequence=FROZEN_CARRIER_FIBER_SPECIFICATION.revision_sequence + 1,
        resampling_count=24,
        **overrides,  # type: ignore[arg-type]
    )
    registry = PreEvidenceCarrierFiberSpecificationRegistry()
    frozen = registry.freeze(specification)
    return CarrierFiberSpecificationContentBinding(
        specification=specification, frozen_manifest=frozen
    )


def _table_for(text: str) -> ObservedFiberTable:
    data = text.encode("utf-8")
    deposit, lines = read_corpus_lines(
        data, source_id="probe-corpus", expected_sha256=canonical_digest(data)
    )
    return tabulate_observed_fibers(lines, deposit=deposit)


@pytest.fixture(scope="module")
def deposited_readout() -> ConditionalIndependenceReadout:
    return run_null_model_on_the_deposited_fatiha()


# --- لا اختبارَ إلا بعد تجميدٍ سابقٍ للدليل -----------------------------------


def test_an_unbound_specification_may_not_drive_the_test() -> None:
    table = _table_for(f"ب{_FATHA} ت{_DAMMA}")
    with pytest.raises(CarrierFiberNullModelError):
        assess_conditional_independence(
            table,
            binding=FROZEN_CARRIER_FIBER_SPECIFICATION,  # type: ignore[arg-type]
        )


def test_a_table_measured_under_another_schema_is_refused() -> None:
    table = _table_for(f"ب{_FATHA} ت{_DAMMA}")
    other_schema = replace(
        FROZEN_CARRIER_FIBER_SPECIFICATION.state_schema, schema_id="another-schema"
    )
    binding = _fast_binding(state_schema=other_schema)
    with pytest.raises(CarrierFiberNullModelError):
        assess_conditional_independence(table, binding=binding)


def test_the_readout_carries_the_digest_of_the_specification_that_preceded_it(
    deposited_readout: ConditionalIndependenceReadout,
) -> None:
    assert len(deposited_readout.content_id_digest) == 64
    assert len(deposited_readout.source_sha256) == 64


# --- التكرارُ بالبذرة نفسِها -------------------------------------------------


def test_the_same_seed_over_the_same_table_returns_the_same_counts() -> None:
    table = _table_for(f"ب{_FATHA} ت{_DAMMA} ب{_FATHA} ت{_DAMMA}")
    binding = _fast_binding()
    first = assess_conditional_independence(table, binding=binding)
    second = assess_conditional_independence(table, binding=binding)
    assert first.rows == second.rows
    assert first.null_support_at_or_below_observed == (
        second.null_support_at_or_below_observed
    )


def test_another_seed_is_another_run_not_another_truth() -> None:
    table = _table_for(f"ب{_FATHA} ت{_DAMMA} ب{_FATHA} ت{_DAMMA}")
    first = assess_conditional_independence(table, binding=_fast_binding())
    second = assess_conditional_independence(
        table, binding=_fast_binding(resampling_seed=99)
    )
    assert first.observed_support_size == second.observed_support_size


# --- الضبطُ محفوظٌ بالبناء ----------------------------------------------------


def test_carrier_frequency_is_preserved_by_construction(
    deposited_readout: ConditionalIndependenceReadout,
) -> None:
    from alghanem.arabic.carrier_state_observed_fiber import (
        run_observed_fiber_on_the_deposited_fatiha,
    )

    table = run_observed_fiber_on_the_deposited_fatiha()
    for fiber in table.fibers:
        assert deposited_readout.reading_for(fiber.carrier).frequency == (
            fiber.frequency
        )


def test_the_observed_capacity_of_each_row_matches_the_measured_fiber(
    deposited_readout: ConditionalIndependenceReadout,
) -> None:
    from alghanem.arabic.carrier_state_observed_fiber import (
        run_observed_fiber_on_the_deposited_fatiha,
    )

    table = run_observed_fiber_on_the_deposited_fatiha()
    for fiber in table.fibers:
        assert deposited_readout.reading_for(fiber.carrier).observed_capacity == (
            fiber.capacity
        )


# --- الندرةُ لا تُقرأ نتيجةً ---------------------------------------------------


def test_a_carrier_below_the_frozen_support_threshold_is_left_undetermined() -> None:
    table = _table_for(f"ب{_FATHA} ت{_DAMMA}")
    readout = assess_conditional_independence(table, binding=_fast_binding())
    assert set(readout.carriers_below_support_threshold) == {"ب", "ت"}
    for row in readout.rows:
        assert row.capacity_outcome is FiberOutcome.UNDETERMINED
        assert row.composition_outcome is FiberOutcome.UNDETERMINED


def test_lowering_the_frozen_threshold_lets_a_reading_be_decided() -> None:
    table = _table_for(f"ب{_FATHA} ت{_DAMMA}")
    readout = assess_conditional_independence(
        table, binding=_fast_binding(minimum_carrier_support=1)
    )
    assert readout.carriers_below_support_threshold == ()
    for row in readout.rows:
        assert row.capacity_outcome is not FiberOutcome.UNDETERMINED


# --- مقياسان في حقلين، لا مقياسٌ مدموج ----------------------------------------


def test_capacity_and_composition_are_reported_in_two_separate_fields(
    deposited_readout: ConditionalIndependenceReadout,
) -> None:
    row = deposited_readout.reading_for(_ALIF)
    assert hasattr(row, "capacity_outcome")
    assert hasattr(row, "composition_outcome")
    fields = set(ConditionalIndependenceReadout.__slots__)
    for marker in ("verdict", "overall", "merged", "final", "combined"):
        assert not [name for name in fields if marker in name]


def test_a_probability_is_never_read_as_zero_in_a_finite_sample(
    deposited_readout: ConditionalIndependenceReadout,
) -> None:
    for row in deposited_readout.rows:
        assert row.capacity_p_value_permille >= 1
        assert row.composition_p_value_permille >= 1


# --- المعايرةُ على النصّ المُودَع ---------------------------------------------


def test_alif_stays_narrower_than_chance_after_the_frozen_controls(
    deposited_readout: ConditionalIndependenceReadout,
) -> None:
    row = deposited_readout.reading_for(_ALIF)
    assert row.capacity_outcome is FiberOutcome.NARROWER_THAN_CHANCE
    assert row.composition_outcome is FiberOutcome.NARROWER_THAN_CHANCE
    assert _ALIF in deposited_readout.carriers_narrower_than_chance
    assert _ALIF in deposited_readout.carriers_with_distinctive_composition


def test_not_every_carrier_is_narrower_than_chance(
    deposited_readout: ConditionalIndependenceReadout,
) -> None:
    outcomes = {row.capacity_outcome for row in deposited_readout.rows}
    assert FiberOutcome.INDISTINGUISHABLE_FROM_CHANCE in outcomes


def test_a_carrier_absent_from_the_run_is_refused_by_name(
    deposited_readout: ConditionalIndependenceReadout,
) -> None:
    with pytest.raises(CarrierFiberNullModelError):
        deposited_readout.reading_for("ﭖ")


# --- ما لا يحسمه هذا الاختبار، مكتوبٌ لا مطويّ --------------------------------


def test_every_named_residual_is_keyed_by_its_own_name() -> None:
    for name, text in CARRIER_FIBER_NULL_MODEL_NAMED_RESIDUALS.items():
        assert text.startswith(f"{name}:")


def test_the_named_residuals_refuse_the_licensed_fiber_reading() -> None:
    joined = " ".join(CARRIER_FIBER_NULL_MODEL_NAMED_RESIDUALS)
    assert "NARROWER_THAN_CHANCE_IS_NOT_A_LICENSED_FIBER" in joined
    assert "THREE_CONTROLS_ARE_NOT_ALL_CONTROLS" in joined


# --- سلطة: هذا الاختبار خاملٌ في النواة ---------------------------------------


def test_no_kernel_module_reads_this_null_model() -> None:
    import pkgutil

    import alghanem.kernel as kernel_package

    for module in pkgutil.walk_packages(
        kernel_package.__path__, prefix="alghanem.kernel."
    ):
        source = module.module_finder.find_spec(  # type: ignore[union-attr]
            module.name
        )
        assert source is not None and source.origin is not None
        with open(source.origin, encoding="utf-8") as handle:
            text = handle.read()
        assert "carrier_fiber_null_model" not in text, module.name
        assert "ConditionalIndependenceReadout" not in text, module.name
