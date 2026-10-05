import pytest
from builders import layer, transition

from alghanem.metaalgebra.composition import (
    THEOREM_VALIDITY_IS_NOT_INSTANTIATION_COVERAGE,
    CompositionChain,
    CompositionChainError,
    StepObligation,
)


def chain_of_two() -> CompositionChain:
    return CompositionChain(
        chain_id="chain",
        layers=(layer("L0"), layer("L1")),
        transitions=(transition("alpha", source_layer_id="L0", target_layer_id="L1"),),
    )


def test_a_well_formed_chain_is_accepted() -> None:
    chain = chain_of_two()

    assert chain.layer_count == 2
    assert chain.instantiation_coverage == 1


def test_a_single_layer_chain_with_no_transition_is_accepted() -> None:
    chain = CompositionChain(chain_id="one", layers=(layer("L0"),), transitions=())

    assert chain.instantiation_coverage == 0
    assert chain.layer_count == 1


def test_the_transition_count_must_be_one_less_than_the_layer_count() -> None:
    with pytest.raises(CompositionChainError):
        CompositionChain(
            chain_id="gap",
            layers=(layer("L0"), layer("L1"), layer("L2")),
            transitions=(
                transition("alpha", source_layer_id="L0", target_layer_id="L1"),
            ),
        )


def test_a_transition_whose_source_is_not_the_previous_layer_is_refused() -> None:
    with pytest.raises(CompositionChainError):
        CompositionChain(
            chain_id="misaligned",
            layers=(layer("L0"), layer("L1")),
            transitions=(
                transition("alpha", source_layer_id="LX", target_layer_id="L1"),
            ),
        )


def test_a_transition_whose_target_is_not_the_next_layer_is_refused() -> None:
    with pytest.raises(CompositionChainError):
        CompositionChain(
            chain_id="misaligned",
            layers=(layer("L0"), layer("L1")),
            transitions=(
                transition("alpha", source_layer_id="L0", target_layer_id="LX"),
            ),
        )


def test_a_preserved_component_unknown_to_the_source_layer_is_refused() -> None:
    with pytest.raises(CompositionChainError):
        CompositionChain(
            chain_id="chain",
            layers=(layer("L0"), layer("L1", invariant_names=("identity", "rank"))),
            transitions=(
                transition(
                    "alpha",
                    source_layer_id="L0",
                    target_layer_id="L1",
                    preserved_components=("rank",),
                ),
            ),
        )


def test_a_preserved_component_unknown_to_the_target_layer_is_refused() -> None:
    with pytest.raises(CompositionChainError):
        CompositionChain(
            chain_id="chain",
            layers=(layer("L0", invariant_names=("identity", "rank")), layer("L1")),
            transitions=(
                transition(
                    "alpha",
                    source_layer_id="L0",
                    target_layer_id="L1",
                    preserved_components=("rank",),
                ),
            ),
        )


def test_a_repeated_layer_in_a_chain_is_refused() -> None:
    with pytest.raises(CompositionChainError):
        CompositionChain(
            chain_id="loop",
            layers=(layer("L0"), layer("L1"), layer("L0")),
            transitions=(
                transition("alpha", source_layer_id="L0", target_layer_id="L1"),
                transition("beta", source_layer_id="L1", target_layer_id="L0"),
            ),
        )


def test_coverage_is_derived_and_never_a_written_field() -> None:
    assert "instantiation_coverage" not in CompositionChain.__dataclass_fields__
    assert "layer_count" not in CompositionChain.__dataclass_fields__
    assert THEOREM_VALIDITY_IS_NOT_INSTANTIATION_COVERAGE.strip() != ""


def test_step_obligations_are_declared_not_measured() -> None:
    chain = chain_of_two()

    assert chain.step_obligations() == tuple(StepObligation)
    assert len(chain.step_obligations()) >= 5


def test_chain_content_id_is_content_sensitive() -> None:
    assert chain_of_two().content_id == chain_of_two().content_id
    single = CompositionChain(chain_id="one", layers=(layer("L0"),), transitions=())
    assert single.content_id != chain_of_two().content_id
