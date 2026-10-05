"""التحقيقُ تغطيةٌ تامّةٌ بالضبط، بمُفنِّدٍ ومخرَجِ رفضٍ ومصائرِ بقايا أربعة."""

from __future__ import annotations

import ast
import importlib
import pathlib
from dataclasses import fields

import pytest
from builders import (
    component_realizations,
    layer_realization,
    realization,
    specification,
    transition_realization,
)

from alghanem.metaalgebra.clause import DeclarativeClause
from alghanem.metaalgebra.layer import LAYER_COMPONENT_NAMES
from alghanem.metaalgebra.realization import (
    REALIZED_TRANSITION_COMPONENT_NAMES,
    ComponentRealization,
    LayerRealization,
    Realization,
    RealizationCoverageError,
    RealizationDomainRef,
    RealizationError,
    ResidualDisposition,
    ResidualDispositionRealization,
    TransitionRealization,
)
from alghanem.metaalgebra.transition import TransitionOutcome


def _dispositions() -> tuple[ResidualDispositionRealization, ...]:
    return tuple(
        ResidualDispositionRealization(
            disposition=disposition, holds_when=f"شرطُ {disposition.value}"
        )
        for disposition in ResidualDisposition
    )


def test_a_layer_realization_covers_all_eight_components() -> None:
    realized = layer_realization("L0")
    assert set(realized.component_names) == set(LAYER_COMPONENT_NAMES)


def test_a_missing_component_is_a_silent_realization_and_is_refused() -> None:
    with pytest.raises(RealizationCoverageError):
        LayerRealization(
            layer_id="L0",
            components=component_realizations(LAYER_COMPONENT_NAMES[:-1]),
            residual_dispositions=_dispositions(),
        )


def test_an_extra_component_smuggles_domain_structure_and_is_refused() -> None:
    with pytest.raises(RealizationCoverageError):
        LayerRealization(
            layer_id="L0",
            components=component_realizations(
                LAYER_COMPONENT_NAMES + ("syllable_weight",)
            ),
            residual_dispositions=_dispositions(),
        )


def test_a_realization_without_a_falsifier_is_a_renaming() -> None:
    with pytest.raises(RealizationError):
        ComponentRealization(
            component_name="carrier",
            realized_as="Typed Object",
            realization_condition=DeclarativeClause(
                clause_id="c", clause_text="نصّ", why_not_executable="سبب"
            ),
            what_would_falsify_this_realization="   ",
        )


def test_a_falsifier_identical_to_the_realization_is_not_a_falsifier() -> None:
    with pytest.raises(RealizationError):
        ComponentRealization(
            component_name="carrier",
            realized_as="Typed Object",
            realization_condition=DeclarativeClause(
                clause_id="c", clause_text="نصّ", why_not_executable="سبب"
            ),
            what_would_falsify_this_realization="Typed Object",
        )


def test_a_realization_condition_is_a_clause_not_a_bare_string() -> None:
    with pytest.raises(Exception):
        ComponentRealization(
            component_name="carrier",
            realized_as="Typed Object",
            realization_condition="شرطٌ نصّيّ",  # type: ignore[arg-type]
            what_would_falsify_this_realization="مُفنِّد",
        )


def test_all_four_residual_dispositions_are_available() -> None:
    assert {member.value for member in ResidualDisposition} == {
        "CLOSE",
        "REFINE",
        "REVISE_DOMAIN",
        "DEFER",
    }
    assert layer_realization("L0").available_dispositions == frozenset(
        ResidualDisposition
    )


def test_a_realization_that_folds_residuals_away_is_refused() -> None:
    with pytest.raises(RealizationError):
        LayerRealization(
            layer_id="L0",
            components=component_realizations(LAYER_COMPONENT_NAMES),
            residual_dispositions=(),
        )


def test_a_domain_without_a_named_refusal_does_not_realize_a_gate() -> None:
    with pytest.raises(RealizationError):
        TransitionRealization(
            transition_id="alpha",
            components=component_realizations(REALIZED_TRANSITION_COMPONENT_NAMES),
            unlicensed_outcome_realizations=((TransitionOutcome.BLOCK, "منعٌ مُسمًّى"),),
        )


def test_a_success_outcome_is_not_a_refusal_realization() -> None:
    with pytest.raises(RealizationError):
        TransitionRealization(
            transition_id="alpha",
            components=component_realizations(REALIZED_TRANSITION_COMPONENT_NAMES),
            unlicensed_outcome_realizations=(
                (
                    TransitionOutcome.CONDITIONALLY_LICENSED_RELATIVE_TO_SIGMA,
                    "نجاحٌ",
                ),
                (TransitionOutcome.DEFER, "تأجيل"),
            ),
        )


def test_a_layer_left_silent_is_neither_realized_nor_deferred_and_is_refused() -> None:
    spec = specification()
    with pytest.raises(RealizationCoverageError):
        Realization(
            realization_id="R.partial",
            domain=RealizationDomainRef(
                domain_id="D0", description="وصف", what_is_not_this_domain="ما ليس منه"
            ),
            specification=spec,
            layer_realizations=(layer_realization("L0"),),
            transition_realizations=(transition_realization("alpha"),),
        )


def test_a_deferred_member_must_be_declared_explicitly() -> None:
    deferred = realization(realize_transitions=False)
    assert deferred.realized_transition_ids == ()
    assert deferred.deferred_transition_ids == ("alpha",)


def test_a_member_realized_and_deferred_at_once_is_contradictory() -> None:
    spec = specification()
    with pytest.raises(RealizationError):
        Realization(
            realization_id="R.contradictory",
            domain=RealizationDomainRef(
                domain_id="D0", description="وصف", what_is_not_this_domain="ما ليس منه"
            ),
            specification=spec,
            layer_realizations=(layer_realization("L0"), layer_realization("L1")),
            transition_realizations=(transition_realization("alpha"),),
            deferred_transition_ids=("alpha",),
        )


def test_a_name_outside_the_specification_is_neither_realized_nor_deferred() -> None:
    spec = specification()
    with pytest.raises(RealizationError):
        Realization(
            realization_id="R.foreign",
            domain=RealizationDomainRef(
                domain_id="D0", description="وصف", what_is_not_this_domain="ما ليس منه"
            ),
            specification=spec,
            layer_realizations=(
                layer_realization("L0"),
                layer_realization("L1"),
                layer_realization("L9"),
            ),
            transition_realizations=(transition_realization("alpha"),),
        )


def test_sigma_is_the_origin_its_digest_ignores_realizations() -> None:
    spec = specification()
    before = spec.content_id
    first = realization("R.a", domain_id="D0", spec=spec)
    second = realization("R.b", domain_id="D1", spec=spec)
    assert spec.content_id == before
    assert first.content_id != second.content_id
    assert first.specification.content_id == second.specification.content_id


def test_an_absent_layer_realization_is_refused_not_returned_as_none() -> None:
    built = realization()
    assert built.layer_realization("L0").layer_id == "L0"
    with pytest.raises(RealizationError):
        built.layer_realization("L9")


def test_no_realization_type_carries_a_standing_field() -> None:
    for declaring_type in (
        ComponentRealization,
        LayerRealization,
        Realization,
        TransitionRealization,
    ):
        for field in fields(declaring_type):
            assert "standing" not in field.name
            assert "verdict" not in field.name


def test_the_realization_module_imports_no_authority_layer() -> None:
    source = importlib.import_module("alghanem.metaalgebra.realization").__file__
    assert source is not None
    tree = ast.parse(pathlib.Path(source).read_text(encoding="utf-8"))
    imported: list[str] = []
    for node in ast.walk(tree):
        if isinstance(node, ast.ImportFrom) and node.module is not None:
            imported.append(node.module)
        elif isinstance(node, ast.Import):
            imported.extend(alias.name for alias in node.names)
    for module in imported:
        assert "kernel" not in module
        assert "arabic" not in module
        assert "realization." not in module
