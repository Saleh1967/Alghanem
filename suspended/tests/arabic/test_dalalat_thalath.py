"""اختباراتُ الدلالاتِ الثلاث: مطابقةٌ وتضمّنٌ والتزام، مفردةً مستقلّة."""

from __future__ import annotations

import pkgutil
from pathlib import Path

import pytest

import alghanem.kernel as kernel_package
from alghanem.arabic import (
    CHANNEL_DOES_NOT_DETERMINE_DALALA_NOTE,
    DALALAT_BY_CHANNEL,
    DALALAT_THALATH_IS_NOT_A_GATE_NOTE,
    ENUMERATIVE_CLOSURE_IS_NOT_A_STATED_COUNT,
    ILTIZAM_CONDITION_IS_NOT_ITS_CAUSE_NOTE,
    THREE_DALALAT_ARE_NOT_THE_CHANNEL_PAIR_NOTE,
    DalalaChannel,
    DalalaKind,
    DalalatThalathError,
    SignificationReading,
    channel_of_dalala,
    dalalat_of_channel,
)

_MODULE = (
    Path(__file__).resolve().parents[2]
    / "src"
    / "alghanem"
    / "arabic"
    / "dalalat_thalath.py"
)


def test_the_three_dalalat_are_their_own_closed_vocabulary() -> None:
    assert len(DalalaKind) == 3
    assert {kind.value for kind in DalalaKind} == {"مطابقة", "تضمن", "التزام"}


def test_the_channel_pair_was_not_widened() -> None:
    assert len(DalalaChannel) == 2
    assert {channel.value for channel in DalalaChannel} == {"منطوق", "مفهوم"}
    assert "ولا تُوسَّع" in THREE_DALALAT_ARE_NOT_THE_CHANNEL_PAIR_NOTE


def test_the_channel_is_derived_from_the_dalala_one_way() -> None:
    assert channel_of_dalala(DalalaKind.مطابقة) is DalalaChannel.منطوق
    assert channel_of_dalala(DalalaKind.تضمن) is DalalaChannel.منطوق
    assert channel_of_dalala(DalalaKind.التزام) is DalalaChannel.مفهوم


def test_the_channel_does_not_determine_a_single_dalala() -> None:
    assert set(dalalat_of_channel(DalalaChannel.منطوق)) == {
        DalalaKind.مطابقة,
        DalalaKind.تضمن,
    }
    assert set(dalalat_of_channel(DalalaChannel.مفهوم)) == {DalalaKind.التزام}
    assert "ولا تختار منه" in CHANNEL_DOES_NOT_DETERMINE_DALALA_NOTE


def test_the_by_channel_map_covers_the_pair_and_the_three() -> None:
    assert set(DALALAT_BY_CHANNEL) == set(DalalaChannel)
    assert sum(len(kinds) for kinds in DALALAT_BY_CHANNEL.values()) == len(DalalaKind)


def test_a_reading_carries_no_channel_field_of_its_own() -> None:
    reading = SignificationReading(
        lafz="البيت",
        read_meaning="الجدارُ والسقف",
        kind=DalalaKind.مطابقة,
    )
    assert reading.channel is DalalaChannel.منطوق
    with pytest.raises(DalalatThalathError):
        SignificationReading(
            lafz="",
            read_meaning="معنًى",
            kind=DalalaKind.مطابقة,
        )


def test_the_necessity_condition_is_a_named_refusal_not_a_logical_flag() -> None:
    assert "شرطٌ وليس بموجِب" in ILTIZAM_CONDITION_IS_NOT_ITS_CAUSE_NOTE
    assert "ENUMERATIVE_CLOSURE_IS_NOT_A_STATED_COUNT" in (
        ENUMERATIVE_CLOSURE_IS_NOT_A_STATED_COUNT
    )


def test_the_module_declares_its_own_limits_by_name() -> None:
    assert "لا سلطة" in DALALAT_THALATH_IS_NOT_A_GATE_NOTE


def test_the_module_imports_no_kernel_authority() -> None:
    source = _MODULE.read_text(encoding="utf-8")
    imports = tuple(
        line for line in source.splitlines() if line.startswith(("import ", "from "))
    )
    assert imports
    assert not any("kernel" in line for line in imports)


def test_no_kernel_module_reads_this_registration() -> None:
    for module in pkgutil.walk_packages(
        kernel_package.__path__, prefix="alghanem.kernel."
    ):
        spec = module.module_finder.find_spec(module.name)  # type: ignore[union-attr]
        assert spec is not None and spec.origin is not None
        text = Path(spec.origin).read_text(encoding="utf-8")
        for name in ("dalalat_thalath", "DalalaKind", "SignificationReading"):
            assert name not in text, (module.name, name)
