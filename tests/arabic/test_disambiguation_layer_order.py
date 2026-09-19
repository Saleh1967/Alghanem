"""اختباراتُ سلّم رفع الالتباس: ترتيبٌ مُعلَن، وسلطةٌ لا ترقى بالفصل."""

from __future__ import annotations

from pathlib import Path

import pytest

from alghanem.arabic import disambiguation_layer_order as ladder_module
from alghanem.arabic.disambiguation_layer_order import (
    DISAMBIGUATION_LAYER_ORDER_NAMED_RESIDUALS,
    THE_DECLARED_HAMZA_ITEMS,
    THE_DECLARED_HAMZA_LADDER,
    THE_DECLARED_ORDER,
    DisambiguationLayer,
    LayerOrderError,
    LayerReading,
    ObservedItem,
    OrderedLadder,
    RecordedField,
    authority_after_separating,
    claim_is_licensed_at,
    rank_of,
    refuse_syllable_birth_claim,
    run_ladder,
    syllable_birth_is_declared,
    value_at,
)
from alghanem.import_boundary import ImportBoundaryPolicy, audit_import_boundary


def _field(name: str, value: str) -> RecordedField:
    return RecordedField(name=name, value=value, declared_source="إعلانُ الاختبار")


def _item(item_id: str, carrier: str, mark: str) -> ObservedItem:
    return ObservedItem(
        item_id=item_id,
        original_measurement=carrier,
        recorded=(_field("حامل", carrier), _field("علامة", mark)),
    )


_TWO_LAYERS = OrderedLadder(
    readings=(
        LayerReading(DisambiguationLayer.CARRIER_IDENTITY, ("حامل",)),
        LayerReading(DisambiguationLayer.RASM_VERSUS_SOUND, ("علامة",)),
    )
)


# --- الحدودُ البنيويّة --------------------------------------------------------


def test_the_layer_order_module_reaches_no_kernel_module() -> None:
    report = audit_import_boundary(
        (Path(str(ladder_module.__file__)),),
        ImportBoundaryPolicy(
            policy_id="disambiguation-layer-order",
            permitted_modules=(),
            forbidden_packages=("alghanem.kernel",),
        ),
    )
    assert not [
        name for name in report.reached_modules if name.startswith("alghanem.kernel")
    ]


def test_no_refine_slot_operation_is_exported_by_this_deposit() -> None:
    assert not hasattr(ladder_module, "RefineSlot")
    for name in ladder_module.__all__:
        assert "refine" not in name.lower()
        assert "split" not in name.lower()


def test_there_are_nine_named_residuals_all_distinct_and_non_blank() -> None:
    assert len(DISAMBIGUATION_LAYER_ORDER_NAMED_RESIDUALS) == 9
    assert len(set(DISAMBIGUATION_LAYER_ORDER_NAMED_RESIDUALS)) == 9
    assert all(note.strip() for note in DISAMBIGUATION_LAYER_ORDER_NAMED_RESIDUALS)


# --- الترتيبُ والرتبة ---------------------------------------------------------


def test_the_declared_order_carries_every_layer_exactly_once() -> None:
    assert set(THE_DECLARED_ORDER) == set(DisambiguationLayer)
    assert len(THE_DECLARED_ORDER) == len(set(THE_DECLARED_ORDER))


def test_the_rank_is_derived_from_the_declared_order() -> None:
    ranks = [rank_of(layer) for layer in THE_DECLARED_ORDER]
    assert ranks == sorted(ranks)
    assert ranks == list(range(len(THE_DECLARED_ORDER)))


def test_the_order_runs_from_the_carrier_to_the_ifada() -> None:
    assert THE_DECLARED_ORDER[0] is DisambiguationLayer.CARRIER_IDENTITY
    assert THE_DECLARED_ORDER[-1] is DisambiguationLayer.IFADA
    assert rank_of(DisambiguationLayer.RASM_VERSUS_SOUND) < rank_of(
        DisambiguationLayer.LICENSED_FEATURES
    )
    assert rank_of(DisambiguationLayer.LICENSED_FEATURES) < rank_of(
        DisambiguationLayer.SYLLABIC_AND_MORPHOLOGICAL_RELATIONS
    )
    assert rank_of(DisambiguationLayer.SYLLABIC_AND_MORPHOLOGICAL_RELATIONS) < rank_of(
        DisambiguationLayer.IFADA
    )


def test_an_unnamed_layer_has_no_rank() -> None:
    with pytest.raises(LayerOrderError):
        rank_of("الإفادة")  # type: ignore[arg-type]


# --- القانونُ المركزيّ: الفصلُ لا يرقّي --------------------------------------


@pytest.mark.parametrize("separated", [0, 1, 2, 97])
def test_separating_any_number_of_states_grants_the_same_layer(
    separated: int,
) -> None:
    for layer in THE_DECLARED_ORDER:
        assert authority_after_separating(layer, separated) is layer


def test_a_negative_separation_count_is_refused() -> None:
    with pytest.raises(LayerOrderError):
        authority_after_separating(DisambiguationLayer.IFADA, -1)


def test_a_claim_may_not_rise_above_the_working_layer() -> None:
    for claim in THE_DECLARED_ORDER:
        for working in THE_DECLARED_ORDER:
            assert claim_is_licensed_at(claim, working) == (
                rank_of(claim) <= rank_of(working)
            )


def test_the_rasm_layer_licenses_no_feature_claim() -> None:
    assert not claim_is_licensed_at(
        DisambiguationLayer.LICENSED_FEATURES,
        DisambiguationLayer.RASM_VERSUS_SOUND,
    )
    assert not claim_is_licensed_at(
        DisambiguationLayer.IFADA,
        DisambiguationLayer.SYLLABIC_AND_MORPHOLOGICAL_RELATIONS,
    )


def test_no_layer_gained_upper_authority_on_the_declared_run() -> None:
    report = run_ladder(THE_DECLARED_HAMZA_LADDER, THE_DECLARED_HAMZA_ITEMS)
    assert report.no_layer_gained_upper_authority
    for separation in report.separations:
        assert separation.granted_authority is separation.layer


# --- ولادةُ المقطع -----------------------------------------------------------


def test_syllable_birth_is_not_declared() -> None:
    assert not syllable_birth_is_declared()


@pytest.mark.parametrize("layer", list(DisambiguationLayer))
def test_no_layer_may_claim_syllable_birth(layer: DisambiguationLayer) -> None:
    with pytest.raises(LayerOrderError):
        refuse_syllable_birth_claim(layer)


# --- الاختلاقُ مرفوض ---------------------------------------------------------


def test_a_field_without_a_written_source_is_refused() -> None:
    with pytest.raises(LayerOrderError):
        RecordedField(name="حامل", value="ء", declared_source="   ")


def test_a_field_without_a_name_or_a_value_is_refused() -> None:
    with pytest.raises(LayerOrderError):
        RecordedField(name=" ", value="ء", declared_source="إعلان")
    with pytest.raises(LayerOrderError):
        RecordedField(name="حامل", value="", declared_source="إعلان")


def test_citing_an_unrecorded_field_is_refused_as_an_invention() -> None:
    ladder = OrderedLadder(
        readings=(LayerReading(DisambiguationLayer.CARRIER_IDENTITY, ("مخرَج",)),)
    )
    with pytest.raises(LayerOrderError):
        run_ladder(ladder, (_item("أ", "ء", "فتحة"),))


def test_an_item_with_a_duplicated_recorded_field_is_refused() -> None:
    with pytest.raises(LayerOrderError):
        ObservedItem(
            item_id="أ",
            original_measurement="ء",
            recorded=(_field("حامل", "ء"), _field("حامل", "ا")),
        )


def test_an_item_without_an_identifier_or_a_record_is_refused() -> None:
    with pytest.raises(LayerOrderError):
        ObservedItem(
            item_id=" ", original_measurement="ء", recorded=(_field("حامل", "ء"),)
        )
    with pytest.raises(LayerOrderError):
        ObservedItem(item_id="أ", original_measurement="ء", recorded=())


def test_an_item_without_an_original_measurement_is_refused() -> None:
    with pytest.raises(LayerOrderError):
        ObservedItem(
            item_id="أ", original_measurement="", recorded=(_field("حامل", "ء"),)
        )


def test_asking_an_item_for_an_unrecorded_field_is_refused() -> None:
    with pytest.raises(LayerOrderError):
        _item("أ", "ء", "فتحة").value_of("مخرَج")


def test_duplicate_item_identifiers_are_refused() -> None:
    with pytest.raises(LayerOrderError):
        run_ladder(_TWO_LAYERS, (_item("أ", "ء", "فتحة"), _item("أ", "ا", "فتحة")))


def test_an_empty_domain_proves_nothing() -> None:
    with pytest.raises(LayerOrderError):
        run_ladder(_TWO_LAYERS, ())


# --- بناءُ السلّم ------------------------------------------------------------


def test_a_layer_that_cites_nothing_is_refused() -> None:
    with pytest.raises(LayerOrderError):
        LayerReading(DisambiguationLayer.IFADA, ())


def test_a_layer_that_cites_one_field_twice_is_refused() -> None:
    with pytest.raises(LayerOrderError):
        LayerReading(DisambiguationLayer.IFADA, ("مضمون", "مضمون"))


def test_an_unnamed_layer_may_not_read() -> None:
    with pytest.raises(LayerOrderError):
        LayerReading("الإفادة", ("مضمون",))  # type: ignore[arg-type]


def test_an_empty_ladder_is_refused() -> None:
    with pytest.raises(LayerOrderError):
        OrderedLadder(readings=())


def test_a_ladder_out_of_the_declared_order_is_refused() -> None:
    with pytest.raises(LayerOrderError):
        OrderedLadder(
            readings=(
                LayerReading(DisambiguationLayer.RASM_VERSUS_SOUND, ("علامة",)),
                LayerReading(DisambiguationLayer.CARRIER_IDENTITY, ("حامل",)),
            )
        )


def test_a_ladder_that_skips_the_bottom_layer_is_refused() -> None:
    with pytest.raises(LayerOrderError):
        OrderedLadder(
            readings=(LayerReading(DisambiguationLayer.RASM_VERSUS_SOUND, ("علامة",)),)
        )


def test_a_ladder_that_skips_an_intermediate_layer_is_refused() -> None:
    with pytest.raises(LayerOrderError):
        OrderedLadder(
            readings=(
                LayerReading(DisambiguationLayer.CARRIER_IDENTITY, ("حامل",)),
                LayerReading(DisambiguationLayer.LICENSED_FEATURES, ("سمة",)),
            )
        )


def test_a_ladder_that_reads_one_layer_twice_is_refused() -> None:
    with pytest.raises(LayerOrderError):
        OrderedLadder(
            readings=(
                LayerReading(DisambiguationLayer.CARRIER_IDENTITY, ("حامل",)),
                LayerReading(DisambiguationLayer.CARRIER_IDENTITY, ("علامة",)),
            )
        )


def test_one_field_may_not_be_cited_in_two_layers() -> None:
    with pytest.raises(LayerOrderError):
        OrderedLadder(
            readings=(
                LayerReading(DisambiguationLayer.CARRIER_IDENTITY, ("حامل",)),
                LayerReading(DisambiguationLayer.RASM_VERSUS_SOUND, ("حامل",)),
            )
        )


def test_the_ladder_derives_its_highest_layer_and_its_citations() -> None:
    assert THE_DECLARED_HAMZA_LADDER.highest_layer is DisambiguationLayer.IFADA
    cited = THE_DECLARED_HAMZA_LADDER.cited_fields
    assert len(cited) == len(set(cited))


# --- التراكمُ واسترجاعُ الأصل -------------------------------------------------


def test_a_layer_value_accumulates_the_lower_layers() -> None:
    item = _item("أ", "ء", "فتحة")
    bottom = value_at(item, _TWO_LAYERS, DisambiguationLayer.CARRIER_IDENTITY)
    upper = value_at(item, _TWO_LAYERS, DisambiguationLayer.RASM_VERSUS_SOUND)
    assert bottom == (("حامل", "ء"),)
    assert upper[: len(bottom)] == bottom
    assert len(upper) > len(bottom)


def test_the_original_measurement_is_recoverable_on_the_declared_run() -> None:
    report = run_ladder(THE_DECLARED_HAMZA_LADDER, THE_DECLARED_HAMZA_ITEMS)
    assert report.the_original_measurement_is_recoverable
    assert report.original_measurement_mismatches == ()


def test_a_bottom_layer_that_drops_the_original_measurement_is_detected() -> None:
    corrupting = OrderedLadder(
        readings=(
            LayerReading(DisambiguationLayer.CARRIER_IDENTITY, ("علامة",)),
            LayerReading(DisambiguationLayer.RASM_VERSUS_SOUND, ("حامل",)),
        )
    )
    report = run_ladder(corrupting, (_item("أ", "ء", "فتحة"),))
    assert not report.the_original_measurement_is_recoverable
    assert report.original_measurement_mismatches == ("أ",)


# --- التشغيلُ على وقوعات الهمزة ----------------------------------------------


def test_the_declared_items_match_the_declared_hamza_occurrences() -> None:
    from alghanem.arabic.hamza_contract import THE_DECLARED_OCCURRENCES

    assert len(THE_DECLARED_HAMZA_ITEMS) == len(THE_DECLARED_OCCURRENCES)
    identifiers = [item.item_id for item in THE_DECLARED_HAMZA_ITEMS]
    assert len(identifiers) == len(set(identifiers))


def test_every_declared_item_records_every_cited_field_with_a_source() -> None:
    for item in THE_DECLARED_HAMZA_ITEMS:
        for name in THE_DECLARED_HAMZA_LADDER.cited_fields:
            assert name in item.recorded_names
        assert all(field.declared_source.strip() for field in item.recorded)


def test_the_run_reports_one_separation_row_per_layer() -> None:
    report = run_ladder(THE_DECLARED_HAMZA_LADDER, THE_DECLARED_HAMZA_ITEMS)
    assert len(report.separations) == len(THE_DECLARED_HAMZA_LADDER.readings)
    assert tuple(item.layer for item in report.separations) == tuple(
        reading.layer for reading in THE_DECLARED_HAMZA_LADDER.readings
    )


def test_a_separation_count_is_counted_from_its_rows() -> None:
    report = run_ladder(THE_DECLARED_HAMZA_LADDER, THE_DECLARED_HAMZA_ITEMS)
    for separation in report.separations:
        assert separation.separated_count == len(separation.newly_separated)
        for left, right in separation.newly_separated:
            assert left != right


def test_no_pair_is_separated_at_two_layers() -> None:
    report = run_ladder(THE_DECLARED_HAMZA_LADDER, THE_DECLARED_HAMZA_ITEMS)
    seen: set[tuple[str, str]] = set()
    for separation in report.separations:
        for pair in separation.newly_separated:
            assert pair not in seen
            seen.add(pair)


def test_the_lower_layers_carry_the_bulk_of_the_separation() -> None:
    report = run_ladder(THE_DECLARED_HAMZA_LADDER, THE_DECLARED_HAMZA_ITEMS)
    counts = {item.layer: item.separated_count for item in report.separations}
    assert counts[DisambiguationLayer.CARRIER_IDENTITY] > 0
    assert counts[DisambiguationLayer.RASM_VERSUS_SOUND] > 0
    assert counts[DisambiguationLayer.LICENSED_FEATURES] > 0
    assert counts[DisambiguationLayer.SYLLABIC_AND_MORPHOLOGICAL_RELATIONS] > 0


def test_the_ifada_layer_separates_nothing_on_this_domain() -> None:
    report = run_ladder(THE_DECLARED_HAMZA_LADDER, THE_DECLARED_HAMZA_ITEMS)
    counts = {item.layer: item.separated_count for item in report.separations}
    assert counts[DisambiguationLayer.IFADA] == 0
    assert not report.every_layer_separated_something


def test_an_unresolved_pair_remains_and_is_not_lifted_by_invention() -> None:
    report = run_ladder(THE_DECLARED_HAMZA_LADDER, THE_DECLARED_HAMZA_ITEMS)
    assert not report.the_ambiguity_is_fully_lifted
    assert len(report.unresolved_pairs) == 1
    left, right = report.unresolved_pairs[0]
    by_id = {item.item_id: item for item in THE_DECLARED_HAMZA_ITEMS}
    for name in THE_DECLARED_HAMZA_LADDER.cited_fields:
        assert by_id[left].value_of(name) == by_id[right].value_of(name)


def test_the_ladder_lifts_every_other_pair() -> None:
    report = run_ladder(THE_DECLARED_HAMZA_LADDER, THE_DECLARED_HAMZA_ITEMS)
    total = len(THE_DECLARED_HAMZA_ITEMS) * (len(THE_DECLARED_HAMZA_ITEMS) - 1) // 2
    separated = sum(item.separated_count for item in report.separations)
    assert separated + len(report.unresolved_pairs) == total
