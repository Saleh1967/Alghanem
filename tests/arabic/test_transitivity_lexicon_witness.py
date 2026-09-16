"""اختباراتُ إيداعِ شاهد اللزوم والتعدّي المعجميِّ الخارجيِّ المُبصَّم.

والمداخلُ المكتوبةُ هنا **مُصطنَعةٌ مُصرَّحٌ بجنسها**، لا مقتطعةٌ من الجدول:
رخصتُه `GPL` وليست رخصةَ هذه الشجرة، فلا تُنسَخ بايتاتُه إليها. وبنيةُ السطر
وحدَها هي المُحاكاة.

وإعادةُ الاشتقاق من البايتات نفسِها اختبارٌ اختياريّ يُفعَّل بمتغيّر بيئةٍ
مُسمًّى، لأنّ البايتات ليست في الشجرة ولن تكون.
"""

from __future__ import annotations

import os
from collections import Counter
from pathlib import Path

import pytest

from alghanem.arabic.transitivity_lexicon_witness import (
    ARRAMOOZ_BRUT_VERB_DATA_WITNESS,
    QAC_ROOT_ALPHABET,
    QUTRUB_TRILATERAL_VERB_TABLE_WITNESS,
    QUTRUB_TRILATERAL_VERB_TABLE_WITNESS_SECOND_MIRROR,
    REDERIVED_BAB_COUNTS,
    REDERIVED_DISTINCT_ROOTS,
    REDERIVED_DISTINCT_VERBS,
    REDERIVED_ENTRIES,
    REDERIVED_HARAKA_COUNTS,
    REDERIVED_MARK_COUNTS,
    REDERIVED_ROOT_LEVEL_COUNTS,
    REDERIVED_ROOTS_JOINING_THE_PARTITION_UNCHANGED,
    TRANSITIVITY_LEXICON_NAMED_RESIDUALS,
    WITNESS_ROOT_ALPHABET,
    TransitivityLexiconError,
    TransitivityMark,
    TrilateralVerbEntry,
    read_trilateral_entries,
    roots_by_mark,
)

TABLE_PATH_VARIABLE = "ALGHANEM_TRIVERBTABLE_PATH"


def synthetic_entry_line(verb: str, root: str, bab: int, mark: str, haraka: str) -> str:
    return (
        f"u'{verb}{bab}':"
        f"{{'verb':u'{verb}','root':u'{root}','bab':{bab},"
        f"'transitive':u'{mark}','haraka':u'{haraka}'}},"
    )


SYNTHETIC_TABLE = (
    "TriVerbTable={\n"
    + "\n".join(
        (
            synthetic_entry_line("كَتَبَ", "كتب", 1, "م", "ضمة"),
            synthetic_entry_line("كَتِبَ", "كتب", 4, "ل", "فتحة"),
            synthetic_entry_line("ذَهَبَ", "ذهب", 3, "ل", "فتحة"),
            synthetic_entry_line("أَبَأَ", "ءبء", 3, "ك", "فتحة"),
        )
    )
    + "\n}\n"
)


def test_the_two_mirrors_carry_one_digest_and_two_places() -> None:
    first = QUTRUB_TRILATERAL_VERB_TABLE_WITNESS
    second = QUTRUB_TRILATERAL_VERB_TABLE_WITNESS_SECOND_MIRROR
    assert first.sha256 == second.sha256
    assert first.byte_length == second.byte_length
    assert first.measured_mirror != second.measured_mirror
    assert first.measured_path != second.measured_path


def test_every_deposited_witness_names_its_licence_and_attribution() -> None:
    for witness in (
        QUTRUB_TRILATERAL_VERB_TABLE_WITNESS,
        QUTRUB_TRILATERAL_VERB_TABLE_WITNESS_SECOND_MIRROR,
        ARRAMOOZ_BRUT_VERB_DATA_WITNESS,
    ):
        assert witness.licenses
        assert witness.required_attribution_links
        assert witness.attribution_requirement.strip()
        assert len(witness.sha256) == 64
        assert witness.byte_length > 0


def test_the_brut_csv_is_deposited_as_provenance_not_as_the_judgement() -> None:
    assert "ليس عمودًا فيه" in ARRAMOOZ_BRUT_VERB_DATA_WITNESS.annotation_note


def test_the_synthetic_table_is_read_by_pattern() -> None:
    entries = read_trilateral_entries(SYNTHETIC_TABLE)
    assert len(entries) == 4
    assert entries[0] == TrilateralVerbEntry(
        verb="كَتَبَ",
        root="كتب",
        bab=1,
        mark=TransitivityMark.TRANSITIVE,
        haraka="ضمة",
    )


def test_a_root_may_carry_more_than_one_mark() -> None:
    by_root = roots_by_mark(read_trilateral_entries(SYNTHETIC_TABLE))
    assert by_root["كتب"] == frozenset(
        {TransitivityMark.TRANSITIVE, TransitivityMark.INTRANSITIVE}
    )
    assert by_root["ذهب"] == frozenset({TransitivityMark.INTRANSITIVE})


def test_an_unknown_mark_is_refused_not_guessed() -> None:
    broken = SYNTHETIC_TABLE.replace("'transitive':u'ل'", "'transitive':u'ز'", 1)
    with pytest.raises(TransitivityLexiconError):
        read_trilateral_entries(broken)


def test_an_empty_table_is_not_a_witness() -> None:
    with pytest.raises(TransitivityLexiconError):
        read_trilateral_entries("TriVerbTable={}\n")


def test_bytes_are_refused_before_decoding() -> None:
    with pytest.raises(TransitivityLexiconError):
        read_trilateral_entries(SYNTHETIC_TABLE.encode("utf-8"))  # type: ignore[arg-type]


def test_an_entry_refuses_a_mark_outside_the_enumeration() -> None:
    with pytest.raises(TransitivityLexiconError):
        TrilateralVerbEntry(
            verb="كَتَبَ",
            root="كتب",
            bab=1,
            mark="م",
            haraka="ضمة",  # type: ignore[arg-type]
        )


def test_an_entry_refuses_a_non_positive_bab() -> None:
    with pytest.raises(TransitivityLexiconError):
        TrilateralVerbEntry(
            verb="كَتَبَ",
            root="كتب",
            bab=0,
            mark=TransitivityMark.TRANSITIVE,
            haraka="ضمة",
        )


def test_the_frozen_totals_agree_with_one_another() -> None:
    assert sum(REDERIVED_MARK_COUNTS.values()) == REDERIVED_ENTRIES
    assert sum(REDERIVED_BAB_COUNTS.values()) == REDERIVED_ENTRIES
    assert sum(REDERIVED_HARAKA_COUNTS.values()) == REDERIVED_ENTRIES
    assert sum(REDERIVED_ROOT_LEVEL_COUNTS.values()) == REDERIVED_DISTINCT_ROOTS
    assert REDERIVED_DISTINCT_VERBS <= REDERIVED_ENTRIES
    assert REDERIVED_DISTINCT_ROOTS <= REDERIVED_DISTINCT_VERBS


def test_the_two_root_alphabets_do_not_overlap_at_all() -> None:
    assert set(WITNESS_ROOT_ALPHABET) & set(QAC_ROOT_ALPHABET) == set()
    assert REDERIVED_ROOTS_JOINING_THE_PARTITION_UNCHANGED == 0


def test_the_hamza_is_not_unified_in_the_witness_alphabet() -> None:
    assert "ء" in WITNESS_ROOT_ALPHABET
    assert "أ" in WITNESS_ROOT_ALPHABET


def test_the_named_residuals_are_declared() -> None:
    assert set(TRANSITIVITY_LEXICON_NAMED_RESIDUALS) == {
        "TheMarksMeaningIsUpstreamsNotOurs",
        "TwoMirrorsOneDigestIsNotTwoWitnesses",
        "TheJoinWasNotTaken",
        "ALexiconIsNotACorpus",
        "TheTableIsTrilateralOnly",
    }
    for name, note in TRANSITIVITY_LEXICON_NAMED_RESIDUALS.items():
        assert note.startswith(f"{name}:")


@pytest.mark.skipif(
    TABLE_PATH_VARIABLE not in os.environ,
    reason=(
        f"يُفعَّل بوضع مسار `triverbtable.py` المُبصَّم في {TABLE_PATH_VARIABLE}؛ "
        "وبايتاتُ الجدول غيرُ منسوخةٍ إلى الشجرة."
    ),
)
def test_the_frozen_census_rederives_from_the_witness_bytes() -> None:
    path = Path(os.environ[TABLE_PATH_VARIABLE])
    data = path.read_bytes()
    assert len(data) == QUTRUB_TRILATERAL_VERB_TABLE_WITNESS.byte_length

    entries = read_trilateral_entries(data.decode("utf-8-sig"))
    by_root = roots_by_mark(entries)

    assert len(entries) == REDERIVED_ENTRIES
    assert len({entry.verb for entry in entries}) == REDERIVED_DISTINCT_VERBS
    assert len(by_root) == REDERIVED_DISTINCT_ROOTS
    assert dict(Counter(entry.mark for entry in entries)) == dict(REDERIVED_MARK_COUNTS)
    assert dict(Counter(entry.bab for entry in entries)) == dict(REDERIVED_BAB_COUNTS)
    assert dict(Counter(entry.haraka for entry in entries)) == dict(
        REDERIVED_HARAKA_COUNTS
    )
    assert dict(
        Counter(
            tuple(sorted(mark.value for mark in marks)) for marks in by_root.values()
        )
    ) == dict(REDERIVED_ROOT_LEVEL_COUNTS)
    assert (
        "".join(sorted({letter for root in by_root for letter in root}))
        == WITNESS_ROOT_ALPHABET
    )
