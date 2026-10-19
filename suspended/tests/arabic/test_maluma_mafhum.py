"""Tests for the information/concept distinction and its sanad chain."""

from __future__ import annotations

import json
import pkgutil
from dataclasses import fields
from pathlib import Path

import pytest

import alghanem.kernel as kernel_package
from alghanem.arabic import (
    ContentStanding,
    MalumaMafhumError,
    SanadLink,
    SanadOrigin,
    SemanticTarget,
    UnderstandingRecord,
)
from alghanem.arabic.external_audit import audit_card

_EXAMPLES = Path(__file__).resolve().parents[2] / "examples" / "external_audit"
_CARDS = (
    "man_2_255.yaml",
    "maa_2_197.yaml",
    "imran_3_33.yaml",
    "hadhan_20_63.yaml",
)

SENSE = SanadLink(link_id="link-0", origin=SanadOrigin.حسّ_مباشر, delegated_from=None)
RELAY = SanadLink(
    link_id="link-1",
    origin=SanadOrigin.تسليم_عن_سابق,
    delegated_from="link-0",
)


def record(**overrides: object) -> UnderstandingRecord:
    base: dict[str, object] = {
        "content_id": "content-1",
        "target": SemanticTarget.استرجاع_الوضع,
        "structurally_admissible": True,
        "sanad": (),
        "declared_standing": ContentStanding.معلومة,
    }
    base.update(overrides)
    return UnderstandingRecord(**base)  # type: ignore[arg-type]


def test_correct_structural_understanding_alone_is_information_not_concept() -> None:
    only_structural = record()
    assert only_structural.standing is ContentStanding.معلومة
    assert only_structural.is_concept is False


def test_a_sanad_terminating_in_direct_sense_yields_a_concept() -> None:
    grounded = record(sanad=(SENSE, RELAY), declared_standing=ContentStanding.مفهوم)
    assert grounded.standing is ContentStanding.مفهوم
    assert grounded.is_concept is True


def test_promoting_information_to_concept_by_writing_it_is_refused() -> None:
    with pytest.raises(MalumaMafhumError, match="تُشتَقّ"):
        record(declared_standing=ContentStanding.مفهوم)


def test_a_chain_that_never_reaches_sense_produces_no_concept() -> None:
    with pytest.raises(MalumaMafhumError, match="لا تنتهي بحسٍّ مباشر"):
        record(
            sanad=(
                SanadLink(
                    link_id="link-1",
                    origin=SanadOrigin.تسليم_عن_سابق,
                    delegated_from="link-0",
                ),
            ),
            declared_standing=ContentStanding.مفهوم,
        )


def test_a_long_chain_is_no_substitute_for_termination() -> None:
    long_chain = tuple(
        SanadLink(
            link_id=f"link-{index}",
            origin=SanadOrigin.تسليم_عن_سابق,
            delegated_from=f"link-{index - 1}",
        )
        for index in range(1, 12)
    )
    with pytest.raises(MalumaMafhumError, match="لا تنتهي بحسٍّ مباشر"):
        record(sanad=long_chain, declared_standing=ContentStanding.مفهوم)


def test_a_broken_delegation_chain_is_refused() -> None:
    with pytest.raises(MalumaMafhumError, match="مقطوعة"):
        record(
            sanad=(
                SENSE,
                SanadLink(
                    link_id="link-2",
                    origin=SanadOrigin.تسليم_عن_سابق,
                    delegated_from="link-9",
                ),
            ),
            declared_standing=ContentStanding.مفهوم,
        )


def test_a_link_delegating_to_itself_is_not_a_sanad() -> None:
    with pytest.raises(MalumaMafhumError, match="تُسنِد إلى نفسها"):
        SanadLink(
            link_id="link-1",
            origin=SanadOrigin.تسليم_عن_سابق,
            delegated_from="link-1",
        )


def test_direct_sense_has_no_earlier_link() -> None:
    with pytest.raises(MalumaMafhumError, match="فلا حلقةَ سابقةَ له"):
        SanadLink(
            link_id="link-0",
            origin=SanadOrigin.حسّ_مباشر,
            delegated_from="link-9",
        )


def test_a_second_direct_sense_inside_the_chain_breaks_it() -> None:
    with pytest.raises(MalumaMafhumError, match="يقطعها"):
        record(
            sanad=(
                SENSE,
                SanadLink(
                    link_id="link-1",
                    origin=SanadOrigin.حسّ_مباشر,
                    delegated_from=None,
                ),
            ),
            declared_standing=ContentStanding.مفهوم,
        )


@pytest.mark.parametrize(
    "target",
    (SemanticTarget.المطابقة_للخارج, SemanticTarget.قصد_المتكلم_الفردي),
)
def test_the_two_other_targets_are_structurally_excluded_at_construction(
    target: SemanticTarget,
) -> None:
    with pytest.raises(MalumaMafhumError, match="مستبعَد"):
        record(target=target)


def test_the_only_legitimate_target_is_retrieval_of_convention() -> None:
    assert len(SemanticTarget) == 3
    assert record().target is SemanticTarget.استرجاع_الوضع


def test_content_that_is_not_structurally_representable_is_not_information() -> None:
    with pytest.raises(MalumaMafhumError, match="ليس معلومةً أصلاً"):
        record(structurally_admissible=False)


def test_no_type_here_carries_a_count_or_intent_field() -> None:
    for declaring_type in (SanadLink, UnderstandingRecord):
        declared = {item.name for item in fields(declaring_type)}
        for marker in ("count", "number", "total", "verdict", "birth", "intent"):
            assert not any(marker in name for name in declared), marker


def test_the_module_reads_no_kernel_authority() -> None:
    source = (
        Path(__file__).resolve().parents[2]
        / "src"
        / "alghanem"
        / "arabic"
        / "maluma_mafhum.py"
    ).read_text(encoding="utf-8")
    imports = tuple(
        line for line in source.splitlines() if line.startswith(("import ", "from "))
    )
    assert imports
    assert not any("kernel" in line for line in imports)


def test_no_kernel_module_reads_this_distinction() -> None:
    for module in pkgutil.walk_packages(
        kernel_package.__path__, prefix="alghanem.kernel."
    ):
        spec = module.module_finder.find_spec(module.name)  # type: ignore[union-attr]
        assert spec is not None and spec.origin is not None
        text = Path(spec.origin).read_text(encoding="utf-8")
        for name in ("maluma_mafhum", "UnderstandingRecord", "SanadLink"):
            assert name not in text, (module.name, name)


@pytest.mark.parametrize("card", _CARDS)
def test_this_distinction_changes_no_external_audit_field(card: str) -> None:
    before = json.dumps(
        audit_card(_EXAMPLES / card).to_dict(), ensure_ascii=False, sort_keys=True
    )
    record()
    record(sanad=(SENSE, RELAY), declared_standing=ContentStanding.مفهوم)
    after = json.dumps(
        audit_card(_EXAMPLES / card).to_dict(), ensure_ascii=False, sort_keys=True
    )
    assert before == after
