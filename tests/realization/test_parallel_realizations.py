"""ميدانان متوازيان لأصلٍ واحد: `Realizes(R_ar, Σ) ∧ Realizes(R_py, Σ)`."""

from __future__ import annotations

from alghanem.arabic.realization import (
    ARABIC_DOMAIN,
    NO_CARRIER_STATE_TO_SYLLABLE_BINDING_YET,
    arabic_realization,
)
from alghanem.metaalgebra.layer import LAYER_COMPONENT_NAMES
from alghanem.metaalgebra.realization import (
    REALIZED_TRANSITION_COMPONENT_NAMES,
    ResidualDisposition,
)
from alghanem.realization.python_realization import PYTHON_DOMAIN, python_realization
from alghanem.realization.reference_specification import REFERENCE_SPECIFICATION


def _pair() -> tuple[object, object]:
    return (
        arabic_realization(REFERENCE_SPECIFICATION),
        python_realization(REFERENCE_SPECIFICATION),
    )


def test_both_realizations_point_at_one_and_the_same_origin() -> None:
    arabic = arabic_realization(REFERENCE_SPECIFICATION)
    python = python_realization(REFERENCE_SPECIFICATION)
    assert arabic.specification.content_id == python.specification.content_id
    assert arabic.specification.content_id == REFERENCE_SPECIFICATION.content_id


def test_neither_realization_is_derived_from_the_other() -> None:
    arabic = arabic_realization(REFERENCE_SPECIFICATION)
    python = python_realization(REFERENCE_SPECIFICATION)
    assert arabic.content_id != python.content_id
    assert arabic.domain.domain_id != python.domain.domain_id
    arabic_names = {
        component.realized_as
        for layer in arabic.layer_realizations
        for component in layer.components
    }
    python_names = {
        component.realized_as
        for layer in python.layer_realizations
        for component in layer.components
    }
    assert arabic_names.isdisjoint(python_names)


def test_the_specification_digest_ignores_its_realizations() -> None:
    before = REFERENCE_SPECIFICATION.content_id
    arabic_realization(REFERENCE_SPECIFICATION)
    python_realization(REFERENCE_SPECIFICATION)
    assert REFERENCE_SPECIFICATION.content_id == before


def test_each_realization_covers_every_declared_component() -> None:
    for realization in (
        arabic_realization(REFERENCE_SPECIFICATION),
        python_realization(REFERENCE_SPECIFICATION),
    ):
        for layer in realization.layer_realizations:
            names = tuple(component.component_name for component in layer.components)
            assert set(names) == set(LAYER_COMPONENT_NAMES)
            dispositions = {item.disposition for item in layer.residual_dispositions}
            assert dispositions == set(ResidualDisposition)
        for transition in realization.transition_realizations:
            names = tuple(
                component.component_name for component in transition.components
            )
            assert set(names) == set(REALIZED_TRANSITION_COMPONENT_NAMES)


def test_every_component_realization_carries_its_own_falsifier() -> None:
    for realization in (
        arabic_realization(REFERENCE_SPECIFICATION),
        python_realization(REFERENCE_SPECIFICATION),
    ):
        for layer in realization.layer_realizations:
            for component in layer.components:
                falsifier = component.what_would_falsify_this_realization
                assert falsifier.strip()
                assert falsifier.strip() != component.realized_as.strip()


def test_the_arabic_realization_declares_that_it_binds_no_syllable() -> None:
    arabic = arabic_realization(REFERENCE_SPECIFICATION)
    rendered = " ".join(
        component.realized_as + component.realization_condition.clause_text
        for layer in arabic.layer_realizations
        for component in layer.components
    )
    assert "مقطع" not in rendered
    assert "وزن" not in rendered
    assert NO_CARRIER_STATE_TO_SYLLABLE_BINDING_YET.strip()


def test_no_realization_condition_is_executable_yet() -> None:
    for realization in (
        arabic_realization(REFERENCE_SPECIFICATION),
        python_realization(REFERENCE_SPECIFICATION),
    ):
        for layer in realization.layer_realizations:
            for component in layer.components:
                assert component.realization_condition.is_executable is False
                assert component.realization_condition.why_not_executable.strip()


def test_the_two_domains_are_named_and_bounded() -> None:
    for domain in (ARABIC_DOMAIN, PYTHON_DOMAIN):
        assert domain.description.strip()
        assert domain.what_is_not_this_domain.strip()
    assert ARABIC_DOMAIN.domain_id == "arabic"
    assert PYTHON_DOMAIN.domain_id == "python"
