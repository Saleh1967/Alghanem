"""اختبارُ سجلّ الأختام: أيُصادِم حيًّا، ويأبى الخزن، ويُفرِد الشاهد؟"""

from __future__ import annotations

from collections.abc import Mapping

import pytest

from alghanem.seals import (
    Seal,
    SealError,
    SealGenus,
    SealReading,
    SealRegistry,
    SealVerdict,
)


def _constant(value: str) -> object:
    def side() -> Mapping[str, str]:
        return {"حقل": value}

    return side


def _seal(name: str, transcribed: str, measured: str, genus: SealGenus) -> Seal:
    return Seal(
        name=name,
        genus=genus,
        origin="أمرُ توليدٍ مُعلَن",
        generate=_constant(measured),  # type: ignore[arg-type]
        transcription=_constant(transcribed),  # type: ignore[arg-type]
    )


def test_a_seal_that_agrees_reports_no_discrepancy() -> None:
    seal = _seal("متّفق", "1", "1", SealGenus.GENERATED)
    verdict = SealVerdict(seal=seal, readings=seal.collide())
    assert not verdict.has_drifted
    assert verdict.discrepancies == ()


def test_a_drifted_seal_names_its_field_and_both_sides() -> None:
    seal = _seal("منزاح", "1", "2", SealGenus.GENERATED)
    verdict = SealVerdict(seal=seal, readings=seal.collide())
    assert verdict.has_drifted
    (reading,) = verdict.discrepancies
    assert reading.field == "حقل"
    assert (reading.transcribed, reading.measured) == ("1", "2")


def test_a_quotation_is_listed_and_never_collided() -> None:
    seal = _seal("شاهد", "منقول", "لا يولَّد", SealGenus.QUOTED)
    verdict = SealVerdict(seal=seal, readings=seal.collide())
    assert verdict.is_quoted
    assert verdict.readings
    assert verdict.discrepancies == ()
    assert not verdict.has_drifted


def test_the_two_sides_are_called_at_every_collision_and_never_stored() -> None:
    calls: list[int] = []

    def generate() -> Mapping[str, str]:
        calls.append(1)
        return {"حقل": str(len(calls))}

    seal = Seal(
        name="حيٌّ لا مخزون",
        genus=SealGenus.GENERATED,
        origin="يُستدعى عند كلّ نداء",
        generate=generate,
        transcription=lambda: {"حقل": "ثابت"},
    )
    first = seal.collide()[0].measured
    second = seal.collide()[0].measured
    assert first != second
    assert len(calls) == 2


def test_a_seal_without_a_declared_generating_command_is_refused() -> None:
    with pytest.raises(SealError):
        Seal(
            name="قبرٌ لا ختم",
            genus=SealGenus.GENERATED,
            origin="   ",
            generate=lambda: {"حقل": "1"},
            transcription=lambda: {"حقل": "1"},
        )


def test_two_sides_naming_different_fields_do_not_collide() -> None:
    seal = Seal(
        name="جدولان",
        genus=SealGenus.GENERATED,
        origin="أمرُ توليدٍ مُعلَن",
        generate=lambda: {"ب": "1"},
        transcription=lambda: {"أ": "1"},
    )
    with pytest.raises(SealError):
        seal.collide()


def test_a_seal_guarding_nothing_is_refused() -> None:
    seal = Seal(
        name="خاوٍ",
        genus=SealGenus.GENERATED,
        origin="أمرُ توليدٍ مُعلَن",
        generate=lambda: {},
        transcription=lambda: {},
    )
    with pytest.raises(SealError):
        seal.collide()


def test_an_empty_registry_guards_nothing_and_is_refused() -> None:
    with pytest.raises(SealError):
        SealRegistry(seals=())


def test_two_seals_may_not_share_one_name() -> None:
    with pytest.raises(SealError):
        SealRegistry(
            seals=(
                _seal("مكرَّر", "1", "1", SealGenus.GENERATED),
                _seal("مكرَّر", "2", "2", SealGenus.GENERATED),
            )
        )


def test_the_registry_reports_only_the_drifted_seals() -> None:
    registry = SealRegistry(
        seals=(
            _seal("متّفق", "1", "1", SealGenus.GENERATED),
            _seal("منزاح", "1", "2", SealGenus.TRANSCRIBED),
            _seal("شاهد", "منقول", "لا يولَّد", SealGenus.QUOTED),
        )
    )
    assert len(registry.collide_all()) == 3
    drifted = registry.drifted()
    assert [verdict.seal.name for verdict in drifted] == ["منزاح"]


def test_the_genus_tally_is_derived_from_the_registry_and_not_transcribed() -> None:
    registry = SealRegistry(
        seals=(
            _seal("أ", "1", "1", SealGenus.GENERATED),
            _seal("ب", "1", "1", SealGenus.TRANSCRIBED),
            _seal("ج", "1", "1", SealGenus.TRANSCRIBED),
            _seal("د", "منقول", "لا يولَّد", SealGenus.QUOTED),
        )
    )
    tally = registry.genera()
    assert tally[SealGenus.GENERATED] == 1
    assert tally[SealGenus.TRANSCRIBED] == 2
    assert tally[SealGenus.QUOTED] == 1
    assert sum(tally.values()) == len(registry.seals)


def test_a_field_without_a_name_is_refused() -> None:
    with pytest.raises(SealError):
        SealReading(field="  ", transcribed="1", measured="1")
