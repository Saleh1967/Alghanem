"""التسجيل البنيوي للنتيجة السلبية في التحقيق التوزيعي.

تُثبِّت هذه الاختبارات خمسة أمور: المواصفة مُجمَّدة وترفض ما خرج عنها،
والادّعاء المنفي مُلزَم على النتيجة السلبية ومرفوض على غيرها، وأحجام العناقيد
تُطابق عدد الأشكال المُعلَن ولا تُقرَّب، والطبقة المكتشَفة لا تُعلَن نحويّة
البتّة، والوحدة خاملة سلطويًّا لا تحرّك بوّابةً ولا تغيّر تدقيقًا خارجيًّا ولا
تحمل عنوان نجاح.
"""

import json
from pathlib import Path

import pytest

from alghanem.arabic import distributional_probe_report as module
from alghanem.arabic.distributional_probe_report import (
    PROBE_NOT_APPLICABLE_TEXT,
    RECORDED_PROBE_REPORT,
    RECORDED_PROBE_SPECIFICATION,
    RECORDED_REFUTED_CLAIM,
    DiscoveredLayer,
    DiscoveredLayerKind,
    DistributionalProbeError,
    DistributionalProbeReport,
    FrozenProbeSpecification,
    LayerNature,
    ProbeFeature,
    ProbeOutcome,
    ProbePartition,
    SelectionCriterion,
)
from alghanem.arabic.external_audit import audit_card

_EXAMPLES = Path(__file__).resolve().parents[2] / "examples" / "external_audit"

_CARDS = (
    "man_2_255.yaml",
    "maa_2_197.yaml",
    "imran_3_33.yaml",
    "hadhan_20_63.yaml",
)


def _specification(**overrides: object) -> FrozenProbeSpecification:
    fields: dict[str, object] = {
        "features": RECORDED_PROBE_SPECIFICATION.features,
        "minimum_support": RECORDED_PROBE_SPECIFICATION.minimum_support,
        "surface_form_count": RECORDED_PROBE_SPECIFICATION.surface_form_count,
        "smallest_scanned_k": RECORDED_PROBE_SPECIFICATION.smallest_scanned_k,
        "largest_scanned_k": RECORDED_PROBE_SPECIFICATION.largest_scanned_k,
        "selection_criterion": RECORDED_PROBE_SPECIFICATION.selection_criterion,
    }
    fields.update(overrides)
    return FrozenProbeSpecification(**fields)  # type: ignore[arg-type]


def _report(**overrides: object) -> DistributionalProbeReport:
    fields: dict[str, object] = {
        "specification": RECORDED_PROBE_REPORT.specification,
        "selected_k": RECORDED_PROBE_REPORT.selected_k,
        "partitions": RECORDED_PROBE_REPORT.partitions,
        "outcome": RECORDED_PROBE_REPORT.outcome,
        "discovered_layers": RECORDED_PROBE_REPORT.discovered_layers,
        "refuted_claim": RECORDED_PROBE_REPORT.refuted_claim,
    }
    fields.update(overrides)
    return DistributionalProbeReport(**fields)  # type: ignore[arg-type]


def test_the_outcome_vocabulary_is_exactly_the_three_declared_values() -> None:
    assert tuple(outcome.value for outcome in ProbeOutcome) == (
        "أعاد_اكتشاف_التقسيم",
        "اكتشف_طبقة_أخرى",
        "لم_يفصل",
    )


def test_the_feature_vocabulary_is_exactly_the_five_measured_features() -> None:
    assert tuple(feature.value for feature in ProbeFeature) == (
        "الطول",
        "نسبة_النهائية",
        "تنوّع_الخَلَف",
        "تنوّع_السلَف",
        "تنوّع_مضيف_الهيكل_الصامت",
    )
    assert RECORDED_PROBE_SPECIFICATION.feature_count == 5
    assert set(RECORDED_PROBE_SPECIFICATION.features) == set(ProbeFeature)


def test_a_repeated_feature_is_refused_rather_than_deduplicated() -> None:
    with pytest.raises(DistributionalProbeError):
        _specification(features=(ProbeFeature.LENGTH, ProbeFeature.LENGTH))


def test_a_criterion_outside_the_closed_vocabulary_is_refused() -> None:
    with pytest.raises(DistributionalProbeError):
        _specification(selection_criterion="silhouette")


def test_the_criterion_actually_used_is_silhouette_alone() -> None:
    assert tuple(SelectionCriterion) == (SelectionCriterion.SILHOUETTE,)
    assert (
        RECORDED_PROBE_SPECIFICATION.selection_criterion
        is SelectionCriterion.SILHOUETTE
    )


def test_the_scanned_range_is_two_to_eleven_without_a_gap() -> None:
    assert RECORDED_PROBE_SPECIFICATION.scanned_k_values == (
        2,
        3,
        4,
        5,
        6,
        7,
        8,
        9,
        10,
        11,
    )


def test_a_scan_starting_below_two_is_refused() -> None:
    with pytest.raises(DistributionalProbeError):
        _specification(smallest_scanned_k=1)


def test_a_scan_whose_largest_k_does_not_exceed_its_smallest_is_refused() -> None:
    with pytest.raises(DistributionalProbeError):
        _specification(smallest_scanned_k=4, largest_scanned_k=4)


def test_cluster_sizes_that_do_not_total_the_declared_form_count_are_refused() -> None:
    with pytest.raises(DistributionalProbeError):
        _report(
            partitions=(
                ProbePartition(k=2, cluster_sizes=(2159, 33)),
                ProbePartition(k=3, cluster_sizes=(1878, 289, 26)),
            ),
            discovered_layers=(),
            outcome=ProbeOutcome.NO_SEPARATION,
        )


def test_a_partition_whose_size_count_disagrees_with_k_is_refused() -> None:
    with pytest.raises(DistributionalProbeError):
        ProbePartition(k=3, cluster_sizes=(2159, 34))


def test_a_partition_outside_the_scanned_range_is_refused() -> None:
    with pytest.raises(DistributionalProbeError):
        _report(
            partitions=(ProbePartition(k=12, cluster_sizes=(2182, 11)),),
            selected_k=12,
            discovered_layers=(),
            outcome=ProbeOutcome.NO_SEPARATION,
        )


def test_a_selected_k_without_its_own_partition_is_refused() -> None:
    with pytest.raises(DistributionalProbeError):
        _report(selected_k=4)


def test_the_negative_outcome_without_a_refuted_claim_is_refused() -> None:
    with pytest.raises(DistributionalProbeError):
        _report(refuted_claim=PROBE_NOT_APPLICABLE_TEXT)


def test_the_no_separation_outcome_also_requires_a_refuted_claim() -> None:
    with pytest.raises(DistributionalProbeError):
        _report(
            outcome=ProbeOutcome.NO_SEPARATION,
            discovered_layers=(),
            refuted_claim=PROBE_NOT_APPLICABLE_TEXT,
        )


def test_a_rediscovery_outcome_carrying_a_refuted_claim_is_refused() -> None:
    with pytest.raises(DistributionalProbeError):
        _report(
            outcome=ProbeOutcome.REDISCOVERED_DIVISION,
            discovered_layers=(),
            refuted_claim=RECORDED_REFUTED_CLAIM,
        )


def test_a_rediscovery_outcome_declaring_a_discovered_layer_is_refused() -> None:
    with pytest.raises(DistributionalProbeError):
        _report(
            outcome=ProbeOutcome.REDISCOVERED_DIVISION,
            refuted_claim=PROBE_NOT_APPLICABLE_TEXT,
        )


def test_the_other_layer_outcome_without_a_named_layer_is_refused() -> None:
    with pytest.raises(DistributionalProbeError):
        _report(discovered_layers=())


def test_no_discovered_layer_may_be_declared_grammatical() -> None:
    with pytest.raises(DistributionalProbeError):
        DiscoveredLayer(
            kind=DiscoveredLayerKind.QURANIC_CADENCE,
            nature=LayerNature.GRAMMATICAL,
            at_k=3,
            member_count=289,
            distinguishing_feature="نسبة نهائية مرتفعة مع تنوّع خَلَف منخفض",
            member_examples=("يَعْلَمُونَ",),
        )


def test_the_cadence_layer_is_recorded_as_stylistic_not_grammatical() -> None:
    (cadence,) = (
        layer
        for layer in RECORDED_PROBE_REPORT.discovered_layers
        if layer.kind is DiscoveredLayerKind.QURANIC_CADENCE
    )
    assert cadence.nature is LayerNature.STYLISTIC_RHYTHMIC
    assert cadence.at_k == 3
    assert cadence.member_count == 289


def test_the_over_connectivity_layer_mixes_true_particles_with_content_words() -> None:
    (small,) = (
        layer
        for layer in RECORDED_PROBE_REPORT.discovered_layers
        if layer.layer_key == (DiscoveredLayerKind.OVER_CONNECTIVITY, 2)
    )
    assert small.nature is LayerNature.DISTRIBUTIONAL_FREQUENCY
    assert small.member_count == 34
    assert "في" in small.member_examples
    assert "الله" in small.member_examples
    assert "قال" in small.member_examples


def test_a_layer_size_that_is_no_cluster_of_its_own_partition_is_refused() -> None:
    with pytest.raises(DistributionalProbeError):
        _report(
            discovered_layers=(
                DiscoveredLayer(
                    kind=DiscoveredLayerKind.OVER_CONNECTIVITY,
                    nature=LayerNature.DISTRIBUTIONAL_FREQUENCY,
                    at_k=2,
                    member_count=33,
                    distinguishing_feature="تكرار هائل مع تنوّع اتصال مرتفع",
                    member_examples=("في",),
                ),
            )
        )


def test_more_membership_examples_than_members_are_refused() -> None:
    with pytest.raises(DistributionalProbeError):
        DiscoveredLayer(
            kind=DiscoveredLayerKind.OVER_CONNECTIVITY,
            nature=LayerNature.DISTRIBUTIONAL_FREQUENCY,
            at_k=2,
            member_count=2,
            distinguishing_feature="تكرار هائل مع تنوّع اتصال مرتفع",
            member_examples=("في", "من", "على"),
        )


def test_two_layers_of_one_kind_at_one_k_are_refused() -> None:
    layer = DiscoveredLayer(
        kind=DiscoveredLayerKind.OVER_CONNECTIVITY,
        nature=LayerNature.DISTRIBUTIONAL_FREQUENCY,
        at_k=2,
        member_count=34,
        distinguishing_feature="تكرار هائل مع تنوّع اتصال مرتفع",
        member_examples=("في",),
    )
    with pytest.raises(DistributionalProbeError):
        _report(discovered_layers=(layer, layer))


def test_the_recorded_result_selects_two_not_three_with_an_unbalanced_split() -> None:
    assert RECORDED_PROBE_REPORT.selected_k == 2
    assert RECORDED_PROBE_REPORT.selected_partition.cluster_sizes == (2159, 34)


def test_the_recorded_result_is_a_negative_one_and_carries_no_success_title() -> None:
    assert RECORDED_PROBE_REPORT.outcome is ProbeOutcome.DISCOVERED_OTHER_LAYER
    assert RECORDED_PROBE_REPORT.is_negative_result
    assert RECORDED_PROBE_REPORT.refuted_claim == RECORDED_REFUTED_CLAIM
    assert not hasattr(module, "SUCCESS_TITLE")
    assert not any(name.endswith("SUCCESS_TITLE") for name in vars(module))


def test_the_declared_layers_keep_their_declaration_order() -> None:
    assert RECORDED_PROBE_REPORT.layers_by_kind == (
        (DiscoveredLayerKind.OVER_CONNECTIVITY, 2),
        (DiscoveredLayerKind.OVER_CONNECTIVITY, 3),
        (DiscoveredLayerKind.QURANIC_CADENCE, 3),
    )


@pytest.mark.parametrize("card", _CARDS)
def test_recording_the_probe_leaves_the_external_audit_byte_identical(
    card: str,
) -> None:
    before = json.dumps(
        audit_card(_EXAMPLES / card).to_dict(), ensure_ascii=False, sort_keys=True
    )

    assert RECORDED_PROBE_REPORT.is_negative_result

    after = json.dumps(
        audit_card(_EXAMPLES / card).to_dict(), ensure_ascii=False, sort_keys=True
    )
    assert before == after
