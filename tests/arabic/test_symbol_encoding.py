"""Tests for the symbolic Arabic encoding foundation."""

from __future__ import annotations

import pytest

from alghanem.arabic import ArabicSymbolEncodingV1


def surfaces() -> list[str]:
    carriers = [chr(0x0621 + offset) for offset in range(29)]
    states = ("\u064e", "\u064f", "\u0650", "\u0652")
    return [carrier + state for carrier in carriers for state in states]


def test_discovery_births_independent_identities_bindings_and_surfaces() -> None:
    encoding = ArabicSymbolEncodingV1()
    encoding.discover(surfaces())

    assert [carrier.identifier for carrier in encoding.carrier_identities] == [
        f"C_{index}" for index in range(29)
    ]
    assert [state.identifier for state in encoding.state_identities] == [
        f"S_{index}" for index in range(4)
    ]
    assert len(encoding.carrier_state_assignments) == 116
    assert len(encoding.canonical_surface_encodings) == 116


def test_normalization_precedes_canonical_surface_birth() -> None:
    encoding = ArabicSymbolEncodingV1()
    encoding.discover(["\u0628\u064e", "\u0628\u064e"])

    assert len(encoding.canonical_surface_encodings) == 1
    assert encoding.canonical_surface_encodings[0].normalized_surface == "\u0628\u064e"


def test_freeze_requires_the_declared_symbolic_cardinalities() -> None:
    encoding = ArabicSymbolEncodingV1()
    encoding.discover(["\u0628\u064e"])

    with pytest.raises(ValueError, match="exactly 29 carriers"):
        encoding.freeze()


@pytest.mark.parametrize("surface", ["\u0628", "\u064e", "\u0628\u064e\u064f", "\u0628\u062a\u064e"])
def test_discovery_rejects_surfaces_without_one_carrier_and_one_state(
    surface: str,
) -> None:
    with pytest.raises(ValueError, match="exactly one carrier and one combining state"):
        ArabicSymbolEncodingV1().discover([surface])
