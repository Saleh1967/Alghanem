"""شواهدُ مرجع الشرط: المرجعُ يُشتَقّ ولا يُنشَأ، وملكُه المعلوماتُ السابقة."""

from __future__ import annotations

import pytest

from alghanem.prior.conditions import (
    PriorCondition,
    PriorConditionKind,
    PriorInformationBase,
    PriorInformationError,
    PriorLicenseGenus,
)
from alghanem.prior.references import PriorConditionRef


def _base(
    base_id: str = "pk0-test",
    *,
    domain_note: str = "مجالٌ صوريٌّ للاختبار",
    licensed_by: PriorLicenseGenus = PriorLicenseGenus.STIPULATED_FOR_THE_DOMAIN,
) -> PriorInformationBase:
    return PriorInformationBase(
        base_id=base_id,
        domain_note=domain_note,
        conditions=tuple(
            PriorCondition(
                condition_id=f"{base_id}-{kind.value}",
                kind=kind,
                statement=f"شرطُ {kind.value}",
                what_it_forbids=f"ما يخالف {kind.value}",
                licensed_by=licensed_by,
            )
            for kind in PriorConditionKind
        ),
    )


def test_a_reference_is_derived_from_a_standing_base() -> None:
    base = _base()
    ref = PriorConditionRef.of(base, PriorConditionKind.IDENTITY_CRITERION)
    assert ref.condition_id == "pk0-test-identity_criterion"
    assert ref.place is PriorConditionKind.IDENTITY_CRITERION
    assert ref.base_id == base.base_id
    assert ref.base_content_id == base.content_id


def test_direct_construction_issues_no_reference_at_all() -> None:
    with pytest.raises(PriorInformationError):
        PriorConditionRef(
            condition_id="مُصطنَع",
            place=PriorConditionKind.DOMAIN,
            base_id="قاعدةٌ مزعومة",
            base_content_id="بصمةٌ مكتوبة",
        )


def test_a_forged_witness_cannot_be_constructed() -> None:
    from alghanem.prior import references

    with pytest.raises(PriorInformationError):
        references._DerivationWitness()
    assert "_DerivationWitness" not in references.__all__
    assert "_DERIVATION_WITNESS" not in references.__all__


def test_a_reference_is_not_derived_from_a_free_name() -> None:
    with pytest.raises(PriorInformationError):
        PriorConditionRef.of("pk0-test", PriorConditionKind.DOMAIN)  # type: ignore[arg-type]


def test_a_place_outside_the_closed_vocabulary_is_refused() -> None:
    with pytest.raises(PriorInformationError):
        PriorConditionRef.of(_base(), "domain")  # type: ignore[arg-type]


@pytest.mark.parametrize(
    "genus",
    (
        PriorLicenseGenus.UNREAD,
        PriorLicenseGenus.DERIVED_FROM_THE_ONTOLOGY_IT_LICENSES,
    ),
)
def test_an_unusable_condition_is_not_referenced(genus: PriorLicenseGenus) -> None:
    base = _base(licensed_by=genus)
    with pytest.raises(PriorInformationError):
        PriorConditionRef.of(base, PriorConditionKind.DOMAIN)


def test_verification_rederives_from_the_living_base() -> None:
    base = _base()
    ref = PriorConditionRef.of(base, PriorConditionKind.DOMAIN)
    assert ref.verify_against(base) is True
    moved = _base(domain_note="مجالٌ آخر")
    assert moved.base_id == base.base_id
    assert moved.content_id != base.content_id
    assert ref.verify_against(moved) is False


def test_a_reference_of_another_base_is_another_reference() -> None:
    first = PriorConditionRef.of(_base(), PriorConditionKind.DOMAIN)
    second = PriorConditionRef.of(_base("pk0-other"), PriorConditionKind.DOMAIN)
    assert first != second


def test_the_witness_is_not_canonical_content() -> None:
    content = PriorConditionRef.of(_base(), PriorConditionKind.DOMAIN)
    assert set(content.as_canonical_content()) == {
        "condition_id",
        "place",
        "base_id",
        "base_content_id",
    }


def test_a_condition_is_standing_not_described_as_born() -> None:
    """الشرطُ قائمٌ مُسجَّلٌ مُرخَّص؛ ولا يُوصَف بما هو فوق رتبة التسجيل."""

    from pathlib import Path

    source = (
        Path(__file__).resolve().parents[2]
        / "src"
        / "alghanem"
        / "prior"
        / "references.py"
    ).read_text(encoding="utf-8")
    for forbidden in ("شرطٍ مولودٍ", "شرط مولود", "born condition", "is born"):
        assert forbidden not in source, forbidden
    assert "قائمٍ مُرخَّصٍ" in source
