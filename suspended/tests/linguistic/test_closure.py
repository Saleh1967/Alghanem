"""الإغلاقُ خمسةُ مكوّناتٍ بتغطيةٍ تامّة، وناتجُه ما قبلَ الإفادة لا الإفادة."""

from __future__ import annotations

import pytest

from alghanem.linguistic.closure import (
    ClosureComponent,
    ClosureComponentReading,
    IfadaPrerequisite,
    RelationalClosureError,
    RelationalClosureStanding,
    assess_relational_closure,
)


def _readings(*unsatisfied: ClosureComponent) -> tuple[ClosureComponentReading, ...]:
    return tuple(
        ClosureComponentReading(
            component=component,
            is_satisfied=component not in unsatisfied,
            what_remains_open=(
                "ما بقي مفتوحًا مُسمًّى" if component in unsatisfied else "لا شيء"
            ),
        )
        for component in ClosureComponent
    )


def test_closure_is_five_components_not_one() -> None:
    assert len(tuple(ClosureComponent)) == 5


def test_a_complete_reading_reaches_pre_ifadah_closure_only() -> None:
    assessment = assess_relational_closure("nisbah-1", _readings())

    assert assessment.standing is RelationalClosureStanding.PRE_IFADAH_CLOSURE_REACHED
    assert assessment.unsatisfied_components == ()
    assert assessment.remaining_ifada_prerequisites == (
        IfadaPrerequisite.LICENSED_FORCE,
        IfadaPrerequisite.REQUIRED_CONTEXT,
    )


def test_filled_arguments_alone_do_not_close_the_nisbah() -> None:
    assessment = assess_relational_closure(
        "nisbah-1", _readings(ClosureComponent.REFERENCES_RESOLVED)
    )

    assert assessment.standing is RelationalClosureStanding.NOT_CLOSED
    assert not assessment.is_pre_ifadah_closed


def test_every_failing_component_is_named_not_only_the_first() -> None:
    assessment = assess_relational_closure(
        "nisbah-1",
        _readings(
            ClosureComponent.ARGUMENTS_CLOSED,
            ClosureComponent.OPERATORS_SCOPED,
            ClosureComponent.NO_CROSS_BOUNDARY_ACTIVE_RESIDUAL,
        ),
    )

    assert len(assessment.unsatisfied_components) == 3


def test_an_incomplete_coverage_is_refused_not_scored() -> None:
    partial = _readings()[:4]
    with pytest.raises(RelationalClosureError):
        assess_relational_closure("nisbah-1", partial)


def test_a_duplicated_component_is_refused() -> None:
    readings = _readings()
    with pytest.raises(RelationalClosureError):
        assess_relational_closure("nisbah-1", readings + (readings[0],))


def test_an_unclosed_nisbah_still_owes_all_three_ifada_prerequisites() -> None:
    assessment = assess_relational_closure(
        "nisbah-1", _readings(ClosureComponent.CONSTRAINTS_LICENSED)
    )

    assert assessment.remaining_ifada_prerequisites == tuple(IfadaPrerequisite)
