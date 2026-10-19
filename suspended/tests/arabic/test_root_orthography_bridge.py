"""اختباراتُ جسر رسم الجذور: قاعدةُ التحويل وقواعدُ التطبيع، بلا عدٍّ مقيس.

والأمثلةُ هنا **مُصطنَعةٌ مُصرَّحٌ بجنسها** إلّا ما نُصَّ على أنّه مقيسٌ من
بايتاتٍ في الشجرة: `test_ta_marbuta_never_fires_on_the_maqayis_root_column`
يفتح جدولَ «مقاييس» المُبصَّم لأنّ دعوى «أثرُ القاعدة صفرٌ» دعوى عن البايتات
لا عن قاعدةٍ، فلا تُثبَت بمثالٍ مصنوع.
"""

from __future__ import annotations

import pytest

from alghanem.arabic import root_orthography_bridge as bridge
from alghanem.arabic.maqayis_root_table_deposit import root_table_rows
from alghanem.arabic.root_orthography_bridge import (
    ALIF_MAQSURA_RULE,
    BUCKWALTER_TO_ARABIC,
    HAMZA_CHARACTERS_IN_BUCKWALTER,
    HAMZA_TO_BARE_ALIF_RULE,
    HAMZA_TO_CARRIED_ALIF_RULE,
    NORMALISATION_RULES,
    REFUSED_RULES,
    ROOT_ORTHOGRAPHY_BRIDGE_NAMED_RESIDUALS,
    TA_MARBUTA_RULE,
    NormalisationReadout,
    NormalisationRule,
    RootOrthographyBridgeError,
    fusions_under,
    normalise_root,
    rule_by_name,
    transliterate_root,
)


def test_the_table_distinguishes_bare_alif_from_every_hamza_carrier() -> None:
    assert BUCKWALTER_TO_ARABIC["A"] == "ا"
    assert BUCKWALTER_TO_ARABIC[">"] == "أ"
    assert BUCKWALTER_TO_ARABIC["<"] == "إ"
    assert BUCKWALTER_TO_ARABIC["|"] == "آ"
    assert BUCKWALTER_TO_ARABIC["'"] == "ء"
    assert BUCKWALTER_TO_ARABIC["}"] == "ئ"
    assert BUCKWALTER_TO_ARABIC["&"] == "ؤ"
    assert len(set(BUCKWALTER_TO_ARABIC.values())) == len(BUCKWALTER_TO_ARABIC)


def test_transliteration_of_a_bare_alif_root_introduces_no_hamza() -> None:
    assert transliterate_root("Abd") == "ابد"
    assert transliterate_root(">bd") == "أبد"
    assert transliterate_root("qwl") == "قول"


def test_a_character_outside_the_table_is_refused_not_passed_through() -> None:
    with pytest.raises(RootOrthographyBridgeError):
        transliterate_root("qw1")
    with pytest.raises(RootOrthographyBridgeError):
        transliterate_root("")


def test_a_rule_without_a_written_text_is_refused() -> None:
    with pytest.raises(RootOrthographyBridgeError):
        NormalisationRule(
            name="بلا_نصّ",
            statement="   ",
            mapping=(("ى", "ي"),),
            what_it_destroys="تمييزًا",
        )
    with pytest.raises(RootOrthographyBridgeError):
        NormalisationRule(
            name="بلا_حدّ",
            statement="قاعدة",
            mapping=(("ى", "ي"),),
            what_it_destroys="",
        )
    with pytest.raises(RootOrthographyBridgeError):
        NormalisationRule(
            name="بلا_خريطة",
            statement="قاعدة",
            mapping=(),
            what_it_destroys="تمييزًا",
        )
    with pytest.raises(RootOrthographyBridgeError):
        NormalisationRule(
            name="محرف_إلى_نفسه",
            statement="قاعدة",
            mapping=(("ى", "ى"),),
            what_it_destroys="تمييزًا",
        )


def test_normalisation_returns_both_forms_and_the_rules_that_fired() -> None:
    readout = normalise_root("أبد", (HAMZA_TO_BARE_ALIF_RULE,))

    assert readout.before == "أبد"
    assert readout.after == "ابد"
    assert readout.applied_rules == (HAMZA_TO_BARE_ALIF_RULE.name,)
    assert readout.offered_rules == (HAMZA_TO_BARE_ALIF_RULE.name,)
    assert readout.was_changed is True


def test_an_offered_rule_that_changed_nothing_is_not_recorded_as_applied() -> None:
    readout = normalise_root("قول", (HAMZA_TO_BARE_ALIF_RULE, ALIF_MAQSURA_RULE))

    assert readout.after == "قول"
    assert readout.applied_rules == ()
    assert readout.offered_rules == (
        HAMZA_TO_BARE_ALIF_RULE.name,
        ALIF_MAQSURA_RULE.name,
    )
    assert readout.was_changed is False


def test_a_readout_claiming_a_change_without_a_rule_is_refused() -> None:
    with pytest.raises(RootOrthographyBridgeError):
        NormalisationReadout(
            before="أبد", after="ابد", offered_rules=("همزة",), applied_rules=()
        )
    with pytest.raises(RootOrthographyBridgeError):
        NormalisationReadout(
            before="قول", after="قول", offered_rules=("همزة",), applied_rules=("همزة",)
        )
    with pytest.raises(RootOrthographyBridgeError):
        NormalisationReadout(
            before="أبد", after="ابد", offered_rules=("همزة",), applied_rules=("ياء",)
        )


def test_the_two_hamza_rules_are_refused_in_one_chain() -> None:
    with pytest.raises(RootOrthographyBridgeError):
        normalise_root("أبد", (HAMZA_TO_BARE_ALIF_RULE, HAMZA_TO_CARRIED_ALIF_RULE))


def test_the_two_hamza_targets_give_two_different_forms() -> None:
    bare = normalise_root("إبد", (HAMZA_TO_BARE_ALIF_RULE,))
    carried = normalise_root("إبد", (HAMZA_TO_CARRIED_ALIF_RULE,))

    assert bare.after == "ابد"
    assert carried.after == "أبد"
    assert bare.after != carried.after


def test_fusions_name_the_roots_that_were_merged_not_only_their_number() -> None:
    fusions = fusions_under(("سأل", "سال", "قول"), (HAMZA_TO_BARE_ALIF_RULE,))

    assert len(fusions) == 1
    assert fusions[0].normalised == "سال"
    assert fusions[0].sources == ("سأل", "سال")
    assert fusions[0].lost_distinctions == 1


def test_the_carried_alif_rule_does_not_fuse_a_hamza_with_a_bare_alif() -> None:
    assert fusions_under(("سأل", "سال"), (HAMZA_TO_CARRIED_ALIF_RULE,)) == ()
    assert len(fusions_under(("سأل", "سئل"), (HAMZA_TO_CARRIED_ALIF_RULE,))) == 1


def test_normalisation_is_not_invertible_and_no_inverse_is_offered() -> None:
    for name in dir(bridge):
        if name == "NORMALISATION_IS_NOT_INVERTIBLE_NOTE":
            continue
        lowered = name.lower()
        assert "denormalise" not in lowered
        assert "invert" not in lowered
        assert "to_buckwalter" not in lowered
    assert (
        normalise_root("سأل", (HAMZA_TO_BARE_ALIF_RULE,)).after
        == normalise_root("سال", (HAMZA_TO_BARE_ALIF_RULE,)).after
    )


def test_the_morphological_rule_is_refused_by_name_not_forgotten() -> None:
    labels = {rule.name for rule in REFUSED_RULES}

    assert "ألف_إلى_واو_أو_ياء" in labels
    assert all(rule.why_it_is_refused.strip() for rule in REFUSED_RULES)
    assert all(rule.what_would_admit_it.strip() for rule in REFUSED_RULES)
    assert labels.isdisjoint({rule.name for rule in NORMALISATION_RULES})


def test_rule_by_name_refuses_an_invented_rule() -> None:
    assert rule_by_name(TA_MARBUTA_RULE.name) is TA_MARBUTA_RULE
    with pytest.raises(RootOrthographyBridgeError):
        rule_by_name("قاعدة_لم_تُسَنّ")


def test_every_rule_names_what_it_destroys() -> None:
    for rule in NORMALISATION_RULES:
        assert rule.what_it_destroys.strip()
        assert rule.statement.strip()


def test_the_named_residuals_carry_the_notes_verbatim() -> None:
    assert (
        ROOT_ORTHOGRAPHY_BRIDGE_NAMED_RESIDUALS["NormalisationIsNotInvertible"]
        == bridge.NORMALISATION_IS_NOT_INVERTIBLE_NOTE
    )
    assert len(ROOT_ORTHOGRAPHY_BRIDGE_NAMED_RESIDUALS) == 7


def test_the_six_hamza_characters_are_named_for_the_alphabet_check() -> None:
    assert set(HAMZA_CHARACTERS_IN_BUCKWALTER) == {"'", "|", ">", "&", "<", "}"}
    assert all(
        character in BUCKWALTER_TO_ARABIC
        for character in HAMZA_CHARACTERS_IN_BUCKWALTER
    )


def test_ta_marbuta_never_fires_on_the_maqayis_root_column() -> None:
    """واقعةٌ مقيسةٌ من بايتاتٍ في الشجرة: «ة» لا ترد في `root_full` البتّة.

    فأثرُ `TA_MARBUTA_RULE` على هذا الجدول صفرٌ **مقيسٌ لا مفترَض**، والقاعدةُ
    تبقى مسنونةً لأنّ سكوتَها عن جدولٍ ليس سكوتًا عن كلّ جدول.
    """

    roots = {row["root_full"] for row in root_table_rows()}

    assert roots
    assert not any("ة" in root for root in roots)
    assert fusions_under(roots, (TA_MARBUTA_RULE,)) == ()
    assert any("ى" in root for root in roots)
