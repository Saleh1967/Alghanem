"""Tests for the mantūq/mafhūm/ifāda vocabularies and their derived standings."""

from __future__ import annotations

import pkgutil
from dataclasses import fields
from pathlib import Path

import pytest

import alghanem.kernel as kernel_package
from alghanem.arabic import (
    ContentStanding,
    DalalaCensus,
    DalalaChannel,
    DalalaRecord,
    IfadaStanding,
    MafhumKind,
    MantuqMafhumIfadaError,
)


def record(**overrides: object) -> DalalaRecord:
    base: dict[str, object] = {
        "lafz": "لفظٌ مقروء",
        "madlul": "مدلولٌ مقروء",
        "carried_by_the_wording": True,
        "agrees_with_the_uttered_ruling": None,
        "composition_benefits": True,
        "benefit_witness": "شاهدُ إفادةٍ مقروء",
        "declared_channel": DalalaChannel.منطوق,
        "declared_mafhum_kind": MafhumKind.لا_ينطبق,
        "declared_ifada": IfadaStanding.مُفيد,
    }
    base.update(overrides)
    return DalalaRecord(**base)  # type: ignore[arg-type]


def understood(**overrides: object) -> DalalaRecord:
    base: dict[str, object] = {
        "carried_by_the_wording": False,
        "agrees_with_the_uttered_ruling": True,
        "declared_channel": DalalaChannel.مفهوم,
        "declared_mafhum_kind": MafhumKind.موافقة,
    }
    base.update(overrides)
    return record(**base)


# --- the three standings are derived from carriers, never written ---


def test_the_channel_is_derived_from_its_carrier_alone() -> None:
    assert record().channel is DalalaChannel.منطوق
    assert understood().channel is DalalaChannel.مفهوم


def test_the_mafhum_kind_is_derived_and_opposition_is_readable() -> None:
    assert understood().mafhum_kind is MafhumKind.موافقة
    opposed = understood(
        agrees_with_the_uttered_ruling=False,
        declared_mafhum_kind=MafhumKind.مخالفة,
    )
    assert opposed.mafhum_kind is MafhumKind.مخالفة


def test_the_ifada_standing_is_derived_and_unread_is_a_member_not_a_blank() -> None:
    unread = record(
        composition_benefits=None,
        benefit_witness="",
        declared_ifada=IfadaStanding.غير_مقروء,
    )
    assert unread.ifada is IfadaStanding.غير_مقروء
    assert unread.ifada.is_read is False
    without_benefit = record(
        composition_benefits=False,
        declared_ifada=IfadaStanding.غير_مُفيد,
    )
    assert without_benefit.ifada is IfadaStanding.غير_مُفيد
    assert without_benefit.ifada.is_read is True


@pytest.mark.parametrize(
    "overrides",
    [
        {"declared_channel": DalalaChannel.مفهوم},
        {"declared_mafhum_kind": MafhumKind.موافقة},
        {"declared_ifada": IfadaStanding.غير_مُفيد},
    ],
)
def test_a_declared_standing_that_contradicts_its_carrier_is_refused(
    overrides: dict[str, object],
) -> None:
    with pytest.raises(MantuqMafhumIfadaError, match="تخالف المُشتَقّة"):
        record(**overrides)


# --- the three vocabularies are kept apart, and the parts are not raised ---


def test_the_agreement_carrier_is_refused_on_an_uttered_signification() -> None:
    with pytest.raises(MantuqMafhumIfadaError, match="قسمٌ إلى مقام قسيمه|قسيمه"):
        record(agrees_with_the_uttered_ruling=True)


def test_an_understood_signification_without_its_part_carrier_is_refused() -> None:
    with pytest.raises(MantuqMafhumIfadaError, match="يلزمه حاملُ قسمه"):
        record(
            carried_by_the_wording=False,
            declared_channel=DalalaChannel.مفهوم,
            declared_mafhum_kind=MafhumKind.لا_ينطبق,
        )


def test_a_witness_is_required_when_benefit_is_read_and_refused_when_it_is_not() -> (
    None
):
    with pytest.raises(MantuqMafhumIfadaError, match="شاهد الإفادة"):
        record(benefit_witness="")
    with pytest.raises(MantuqMafhumIfadaError, match="شاهد الإفادة"):
        record(
            composition_benefits=None,
            declared_ifada=IfadaStanding.غير_مقروء,
        )


def test_this_mafhum_is_not_the_content_standing_of_maluma_mafhum() -> None:
    assert DalalaChannel.مفهوم is not ContentStanding.مفهوم
    assert DalalaChannel.مفهوم.value == ContentStanding.مفهوم.value


# --- every member is present in every census, zero included ---


def test_every_member_of_every_vocabulary_is_counted_even_at_zero() -> None:
    census = DalalaCensus(records=(record(),))
    assert set(census.channel_counts) == set(DalalaChannel)
    assert set(census.mafhum_kind_counts) == set(MafhumKind)
    assert set(census.ifada_counts) == set(IfadaStanding)
    assert census.channel_counts[DalalaChannel.مفهوم] == 0
    assert census.mafhum_kind_counts[MafhumKind.مخالفة] == 0
    assert census.ifada_counts[IfadaStanding.غير_مقروء] == 0


def test_an_empty_census_still_names_every_member_at_zero() -> None:
    census = DalalaCensus(records=())
    assert sum(census.channel_counts.values()) == 0
    assert set(census.ifada_counts) == set(IfadaStanding)


def test_the_census_refuses_free_text_instead_of_a_read_record() -> None:
    with pytest.raises(MantuqMafhumIfadaError, match="قراءةٌ مُصاغة"):
        DalalaCensus(records=("قراءة",))  # type: ignore[arg-type]


# --- no answer-bearing field, and no kernel authority ---


def test_no_type_here_carries_a_count_rank_or_verdict_field() -> None:
    for declaring_type in (DalalaRecord, DalalaCensus):
        declared = {item.name for item in fields(declaring_type)}
        for marker in ("count", "total", "score", "rank", "progress", "verdict"):
            assert not any(marker in name for name in declared), marker


def test_the_module_reads_no_kernel_authority() -> None:
    source = (
        Path(__file__).resolve().parents[2]
        / "src"
        / "alghanem"
        / "arabic"
        / "mantuq_mafhum_ifada.py"
    ).read_text(encoding="utf-8")
    imports = tuple(
        line for line in source.splitlines() if line.startswith(("import ", "from "))
    )
    assert imports
    assert not any("kernel" in line for line in imports)
    assert not any("program" in line for line in imports)


def test_no_kernel_module_reads_these_vocabularies() -> None:
    for module in pkgutil.walk_packages(
        kernel_package.__path__, prefix="alghanem.kernel."
    ):
        spec = module.module_finder.find_spec(module.name)  # type: ignore[union-attr]
        assert spec is not None and spec.origin is not None
        text = Path(spec.origin).read_text(encoding="utf-8")
        for name in ("mantuq_mafhum_ifada", "DalalaChannel", "IfadaStanding"):
            assert name not in text, (module.name, name)
