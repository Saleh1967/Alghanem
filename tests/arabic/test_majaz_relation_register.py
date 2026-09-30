"""شواهدُ سجلّ علاقات المجاز: تُصادم المنقولَ بما يولّده القرصُ الآن."""

from __future__ import annotations

import re

import pytest

from alghanem.arabic.majaz_relation_register import (
    A_BARE_ORDINAL_IS_NOT_A_SECTION_MARKER,
    A_KASHIDA_IS_A_SHAPE_NOT_A_LETTER,
    A_LICENSED_RELATION_IS_A_REGISTER_MEMBER_NOT_A_FELT_RESEMBLANCE,
    COUNTING_SUBDIVISIONS_IS_NOT_COUNTING_TYPES,
    THE_ELEVENTH_WEARS_NEITHER_MARKER_OF_THE_TEN,
    THE_KASHIDA,
    THE_MATN_PATH,
    THE_ORDINALS,
    THE_TRANSCRIBED_NAMES,
    MajazRelationEntry,
    MajazRelationRegisterError,
    MarkerGenus,
    bare_ordinal_hits_in_the_whole_matn,
    declared_subdivision_total,
    derive_register,
    entries_wearing,
    is_licensed,
    kashida_blind_eleventh_lines,
    licensed_relation_ref,
    matn_deposit,
    naw_ruler_yield,
    subdividing_entries,
)
from alghanem.arabic.owner_licensed_deposit import DepositStanding, standing_of


def test_the_register_is_derived_from_a_deposit_that_matches_its_seal() -> None:
    deposit = matn_deposit()
    assert deposit.path == THE_MATN_PATH
    assert standing_of(deposit) is DepositStanding.SIGNED_AND_SEALED


def test_the_deposit_yields_eleven_types_and_not_ten() -> None:
    assert len(derive_register()) == 11


def test_the_transcribed_names_are_collided_with_what_disk_produces() -> None:
    assert tuple(one.name for one in derive_register()) == THE_TRANSCRIBED_NAMES


def test_the_ordinals_ascend_without_a_gap() -> None:
    register = derive_register()
    assert tuple(one.ordinal for one in register) == THE_ORDINALS
    assert tuple(one.rank for one in register) == tuple(range(1, 12))


def test_the_naw_ruler_alone_yields_ten_so_its_ten_is_an_artefact() -> None:
    assert naw_ruler_yield() == 10
    assert len(derive_register()) == naw_ruler_yield() + 1
    assert "عشرةً" in THE_ELEVENTH_WEARS_NEITHER_MARKER_OF_THE_TEN


def test_the_eleventh_wears_the_other_marker_and_it_is_alone_in_it() -> None:
    prefixed = entries_wearing(MarkerGenus.PREFIXED_BY_NAW)
    bare = entries_wearing(MarkerGenus.BARE_ORDINAL)
    assert len(prefixed) == 10
    assert len(bare) == 1
    assert bare[0].ordinal == THE_ORDINALS[10]


def test_a_kashida_blind_reader_never_reaches_the_eleventh_type() -> None:
    eleventh = entries_wearing(MarkerGenus.BARE_ORDINAL)[0]
    blind = kashida_blind_eleventh_lines()
    assert blind, "المسطرةُ العمياءُ ليست فارغةً، وهذا ما يجعلها خادعة."
    assert eleventh.line_number not in blind
    assert "التطويل" in A_KASHIDA_IS_A_SHAPE_NOT_A_LETTER


def test_the_kashida_is_actually_written_in_that_line_on_this_deposit() -> None:
    from pathlib import Path

    import alghanem.arabic.majaz_relation_register as module

    root = Path(module.__file__).resolve().parents[3]
    lines = (root / THE_MATN_PATH).read_text(encoding="utf-8").split("\n")
    eleventh = entries_wearing(MarkerGenus.BARE_ORDINAL)[0]
    raw = lines[eleventh.line_number - 1]
    assert THE_KASHIDA in raw[: raw.index(":")]


def test_the_bare_ordinal_ruler_would_open_the_whole_matn() -> None:
    assert bare_ordinal_hits_in_the_whole_matn() > 11
    assert "أبوابٍ شتّى" in A_BARE_ORDINAL_IS_NOT_A_SECTION_MARKER


def test_the_eleventh_bare_ordinal_is_not_unique_in_the_deposit() -> None:
    assert len(kashida_blind_eleventh_lines()) >= 1
    eleventh = entries_wearing(MarkerGenus.BARE_ORDINAL)[0]
    others = [
        one
        for one in kashida_blind_eleventh_lines()
        if one != eleventh.line_number
    ]
    assert others, "لو كانت الرتبةُ المجرّدةُ فريدةً لجاز جعلُها حدًّا."


def test_the_types_are_contiguous_lines_so_the_scope_is_a_neighbourhood() -> None:
    numbers = [one.line_number for one in derive_register()]
    assert numbers == list(range(numbers[0], numbers[0] + 11))


def test_counting_subdivisions_is_not_counting_types() -> None:
    subdivided = subdividing_entries()
    assert len(subdivided) == 2
    assert declared_subdivision_total() != len(derive_register())
    assert declared_subdivision_total() == sum(
        one.declared_subdivisions or 0 for one in subdivided
    )
    assert "لا يُجمَع إليه" in COUNTING_SUBDIVISIONS_IS_NOT_COUNTING_TYPES


def test_the_subdivided_types_are_the_first_and_the_eleventh() -> None:
    assert tuple(one.rank for one in subdividing_entries()) == (1, 11)


def test_a_licensed_reference_is_a_register_member() -> None:
    for one in derive_register():
        assert is_licensed(licensed_relation_ref(one))


def test_a_felt_resemblance_is_not_a_licensed_reference() -> None:
    assert not is_licensed("مشابهةٌ ظاهرةٌ بين المعنيين")
    assert not is_licensed("المشابهة")
    assert not is_licensed("")
    assert not is_licensed("   ")
    assert "المُستشعَرةُ" in (
        A_LICENSED_RELATION_IS_A_REGISTER_MEMBER_NOT_A_FELT_RESEMBLANCE
    )


def test_a_reference_written_with_a_kashida_still_names_its_member() -> None:
    eleventh = entries_wearing(MarkerGenus.BARE_ORDINAL)[0]
    reference = licensed_relation_ref(eleventh)
    assert is_licensed(reference.replace("عشر", "عش" + THE_KASHIDA + "ر"))


def test_a_reference_that_is_not_text_is_refused_by_name() -> None:
    with pytest.raises(MajazRelationRegisterError):
        is_licensed(11)  # type: ignore[arg-type]


def test_the_reference_carries_both_the_deposit_and_the_ordinal() -> None:
    reference = licensed_relation_ref(derive_register()[0])
    assert reference.startswith(THE_MATN_PATH + "#")
    assert THE_ORDINALS[0] in reference


def test_a_reference_is_not_built_from_something_outside_the_register() -> None:
    with pytest.raises(MajazRelationRegisterError):
        licensed_relation_ref("السببية")  # type: ignore[arg-type]


def test_an_entry_outside_the_eleven_ordinals_is_refused() -> None:
    with pytest.raises(MajazRelationRegisterError):
        MajazRelationEntry(
            ordinal="الثاني عشر",
            name="نوعٌ مُختلَق",
            line_number=1,
            marker=MarkerGenus.BARE_ORDINAL,
            declared_subdivisions=None,
        )


def test_an_entry_without_a_name_or_a_line_is_refused() -> None:
    with pytest.raises(MajazRelationRegisterError):
        MajazRelationEntry(
            ordinal=THE_ORDINALS[0],
            name="   ",
            line_number=1,
            marker=MarkerGenus.BARE_ORDINAL,
            declared_subdivisions=None,
        )
    with pytest.raises(MajazRelationRegisterError):
        MajazRelationEntry(
            ordinal=THE_ORDINALS[0],
            name="السببية",
            line_number=0,
            marker=MarkerGenus.BARE_ORDINAL,
            declared_subdivisions=None,
        )


def test_a_marker_outside_the_two_genera_is_refused() -> None:
    with pytest.raises(MajazRelationRegisterError):
        entries_wearing("مُصدَّرٌ بلفظ «النوع»")  # type: ignore[arg-type]


def test_no_name_or_line_number_of_a_type_is_written_in_the_module() -> None:
    from pathlib import Path

    import alghanem.arabic.majaz_relation_register as module

    source = Path(module.__file__).read_text(encoding="utf-8")
    body = source.split('"""', 2)[2]
    for one in derive_register():
        assert str(one.line_number) not in body, (
            f"رقمُ سطرِ «{one.name}» مكتوبٌ في الوحدة، فالسجلُّ منقولٌ لا مُشتَقّ."
        )


def test_the_module_does_not_import_the_kernel() -> None:
    from pathlib import Path

    import alghanem.arabic.majaz_relation_register as module

    source = Path(module.__file__).read_text(encoding="utf-8")
    assert not re.search(r"^from \.\.kernel|^from alghanem\.kernel", source, re.M)
