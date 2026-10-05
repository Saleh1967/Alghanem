"""شواهدُ `PK_0`: تغطيةٌ تامّةٌ للمواضع التسعة، وشرطٌ بلا ترخيصٍ لا يؤسِّس."""

from __future__ import annotations

import pytest

from alghanem.prior.conditions import (
    PRIOR_CONDITION_NAMES,
    PriorCondition,
    PriorConditionKind,
    PriorInformationBase,
    PriorInformationError,
    PriorLicenseGenus,
)


def _condition(
    kind: PriorConditionKind,
    licensed_by: PriorLicenseGenus = PriorLicenseGenus.STIPULATED_FOR_THE_DOMAIN,
) -> PriorCondition:
    return PriorCondition(
        condition_id=f"c-{kind.value}",
        kind=kind,
        statement=f"شرطُ الإمكان في موضع {kind.value}",
        what_it_forbids=f"ما يُخالف {kind.value} من دعاوى",
        licensed_by=licensed_by,
    )


def _complete_conditions() -> tuple[PriorCondition, ...]:
    return tuple(_condition(kind) for kind in PriorConditionKind)


def _base(conditions: tuple[PriorCondition, ...] | None = None) -> PriorInformationBase:
    return PriorInformationBase(
        base_id="pk0-test",
        domain_note="مجالٌ صوريٌّ للاختبار، بلا لغةٍ مخصوصة",
        conditions=_complete_conditions() if conditions is None else conditions,
    )


def test_the_vocabulary_holds_exactly_nine_places() -> None:
    assert len(PRIOR_CONDITION_NAMES) == 9
    assert len(set(PRIOR_CONDITION_NAMES)) == 9


def test_a_complete_base_is_constructible_and_fit_to_found_an_ontology() -> None:
    base = _base()
    assert base.is_fit_to_found_an_ontology
    assert base.unusable_condition_ids == ()
    assert base.condition(PriorConditionKind.DOMAIN).kind is PriorConditionKind.DOMAIN


def test_a_missing_place_is_refused_rather_than_read_as_complete() -> None:
    partial = tuple(
        condition
        for condition in _complete_conditions()
        if condition.kind is not PriorConditionKind.PRESERVED_TRACE
    )
    with pytest.raises(PriorInformationError) as refusal:
        _base(partial)
    assert "preserved_trace" in str(refusal.value)


def test_a_duplicated_place_is_refused_rather_than_folded() -> None:
    doubled = _complete_conditions() + (
        PriorCondition(
            condition_id="c-domain-again",
            kind=PriorConditionKind.DOMAIN,
            statement="صياغةٌ ثانيةٌ للمجال",
            what_it_forbids="لا شيءَ زائد",
            licensed_by=PriorLicenseGenus.PRIOR_PROOF,
        ),
    )
    with pytest.raises(PriorInformationError):
        _base(doubled)


def test_a_condition_that_forbids_nothing_is_refused_at_construction() -> None:
    with pytest.raises(PriorInformationError):
        PriorCondition(
            condition_id="c-empty",
            kind=PriorConditionKind.DOMAIN,
            statement="وصفٌ عامّ",
            what_it_forbids="  ",
            licensed_by=PriorLicenseGenus.PRIOR_PROOF,
        )


def test_a_condition_licensed_by_what_it_licenses_is_not_usable() -> None:
    circular = PriorLicenseGenus.DERIVED_FROM_THE_ONTOLOGY_IT_LICENSES
    assert not circular.licenses_use
    condition = _condition(PriorConditionKind.IDENTITY_CRITERION, circular)
    assert not condition.is_usable


def test_an_unread_condition_is_not_a_satisfied_one() -> None:
    assert not PriorLicenseGenus.UNREAD.licenses_use
    conditions = tuple(
        _condition(kind, PriorLicenseGenus.UNREAD)
        if kind is PriorConditionKind.UNIT_CRITERION
        else _condition(kind)
        for kind in PriorConditionKind
    )
    base = _base(conditions)
    assert base.unusable_condition_ids == ("c-unit_criterion",)
    assert not base.is_fit_to_found_an_ontology


def test_every_unusable_condition_is_named_and_evaluation_does_not_stop_early() -> None:
    conditions = tuple(
        _condition(kind, PriorLicenseGenus.UNREAD)
        if kind
        in (PriorConditionKind.DOMAIN, PriorConditionKind.CLOSURE_BLOCKING_REMAINDER)
        else _condition(kind)
        for kind in PriorConditionKind
    )
    base = _base(conditions)
    assert set(base.unusable_condition_ids) == {
        "c-domain",
        "c-closure_blocking_remainder",
    }


def test_the_digest_is_independent_of_the_declaration_order() -> None:
    forward = _base()
    backward = PriorInformationBase(
        base_id=forward.base_id,
        domain_note=forward.domain_note,
        conditions=tuple(reversed(forward.conditions)),
    )
    assert forward.content_id == backward.content_id


def test_a_changed_statement_changes_the_digest() -> None:
    base = _base()
    altered = PriorInformationBase(
        base_id=base.base_id,
        domain_note="مجالٌ آخر",
        conditions=base.conditions,
    )
    assert altered.content_id != base.content_id


def test_an_absent_place_is_refused_rather_than_returned_as_none() -> None:
    conditions = tuple(
        condition
        for condition in _complete_conditions()
        if condition.kind is not PriorConditionKind.DOMAIN
    )
    base = PriorInformationBase.__new__(PriorInformationBase)
    object.__setattr__(base, "base_id", "pk0-partial")
    object.__setattr__(base, "domain_note", "مجالٌ ناقصُ التغطية، أُنشئ لفحص الغياب")
    object.__setattr__(base, "conditions", conditions)
    with pytest.raises(PriorInformationError):
        base.condition(PriorConditionKind.DOMAIN)
