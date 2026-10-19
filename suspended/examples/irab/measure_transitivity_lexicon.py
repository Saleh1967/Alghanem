"""Re-derive the frozen `transitivity_lexicon_witness` census from the table itself.

This script is reference material, not part of the kernel or the Arabic layer.
It derives no kernel object, licenses no transition, and issues no grammatical
judgement about any verb. It recomputes the numbers frozen in
``src/alghanem/arabic/transitivity_lexicon_witness.py`` and fails loudly if they
drift.

The table is deliberately **not** vendored: it is GPL-licensed, and that licence
is not this repository's. Obtain the exact file named in
``alghanem.arabic.transitivity_lexicon_witness.QUTRUB_TRILATERAL_VERB_TABLE_WITNESS``
(or its identical second mirror), then::

    python examples/irab/measure_transitivity_lexicon.py path/to/triverbtable.py

The script verifies the recorded SHA-256 and byte length first and refuses to
report numbers for any other file. It reads the file as **text**, by declared
pattern match; it never executes it.

What a match does establish: that an externally authored, human-collected
lāzim/mutaʿaddin table of this exact content exists, and what is in it. What it
does not establish: anything about the Quranic partition frozen in
``transitivity_corpus_census`` — the two root vocabularies are written in
different scripts and their literal intersection is zero, measured. Joining
them would require a transliteration rule, and a rule is legislated, not read.

Source: Qutrub / Arramooz Alwaseet, T. Zerrouki, with verb data collected by
M. Kebdani — http://arramooz.sourceforge.net/ and
https://github.com/linuxscout/qutrub. Attribution is a condition of the GPL,
not a courtesy.
"""

from __future__ import annotations

import argparse
import hashlib
import sys
from collections import Counter
from pathlib import Path

from alghanem.arabic.transitivity_lexicon_witness import (
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
    THE_JOIN_WAS_NOT_TAKEN_NOTE,
    TRANSITIVITY_LEXICON_NAMED_RESIDUALS,
    TWO_MIRRORS_ONE_DIGEST_IS_NOT_TWO_WITNESSES_NOTE,
    WITNESS_ROOT_ALPHABET,
    TransitivityLexiconError,
    read_trilateral_entries,
    roots_by_mark,
)


def verified_table_text(path: Path) -> str:
    """Read the table only after its recorded digest and length both match."""
    witness = QUTRUB_TRILATERAL_VERB_TABLE_WITNESS
    if not path.is_file():
        raise TransitivityLexiconError(f"لا ملفَّ عند المسار: {path}")
    data = path.read_bytes()
    if len(data) != witness.byte_length:
        raise TransitivityLexiconError(
            f"طولُ الملفّ {len(data)} بايتة، والمُودَعُ {witness.byte_length}؛ "
            "فهذا ملفٌّ آخر، ولا يُنسَب إليه رقمٌ قِيس على غيره."
        )
    digest = hashlib.sha256(data).hexdigest()
    if digest != witness.sha256:
        raise TransitivityLexiconError(
            f"بصمةُ الملفّ {digest}، والمُودَعةُ {witness.sha256}؛ فهذا ملفٌّ آخر."
        )
    return data.decode("utf-8-sig")


def _compare(label: str, measured: object, frozen: object) -> bool:
    matched = measured == frozen
    mark = "=" if matched else "!"
    print(f"  [{mark}] {label}: measured={measured!r} frozen={frozen!r}")
    return matched


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("table", type=Path, help="path to triverbtable.py")
    arguments = parser.parse_args(argv)

    text = verified_table_text(arguments.table)
    entries = read_trilateral_entries(text)
    by_root = roots_by_mark(entries)

    print("witness (both mirrors carry one digest):")
    for witness in (
        QUTRUB_TRILATERAL_VERB_TABLE_WITNESS,
        QUTRUB_TRILATERAL_VERB_TABLE_WITNESS_SECOND_MIRROR,
    ):
        print(f"  {witness.measured_mirror}/{witness.measured_path}")
        print(f"    sha256={witness.sha256} bytes={witness.byte_length}")
    print(f"  {TWO_MIRRORS_ONE_DIGEST_IS_NOT_TWO_WITNESSES_NOTE}")

    print("census:")
    checks = [
        _compare("entries", len(entries), REDERIVED_ENTRIES),
        _compare(
            "distinct verbs",
            len({entry.verb for entry in entries}),
            REDERIVED_DISTINCT_VERBS,
        ),
        _compare("distinct roots", len(by_root), REDERIVED_DISTINCT_ROOTS),
        _compare(
            "mark counts",
            dict(Counter(entry.mark for entry in entries)),
            dict(REDERIVED_MARK_COUNTS),
        ),
        _compare(
            "bab counts",
            dict(sorted(Counter(entry.bab for entry in entries).items())),
            dict(sorted(REDERIVED_BAB_COUNTS.items())),
        ),
        _compare(
            "haraka counts",
            dict(Counter(entry.haraka for entry in entries)),
            dict(REDERIVED_HARAKA_COUNTS),
        ),
        _compare(
            "root-level mark combinations",
            dict(
                Counter(
                    tuple(sorted(mark.value for mark in marks))
                    for marks in by_root.values()
                )
            ),
            dict(REDERIVED_ROOT_LEVEL_COUNTS),
        ),
        _compare(
            "root alphabet",
            "".join(sorted({letter for root in by_root for letter in root})),
            WITNESS_ROOT_ALPHABET,
        ),
    ]

    print("the join that was not taken:")
    print(f"  witness root alphabet: {WITNESS_ROOT_ALPHABET}")
    print(f"  QAC root alphabet:     {QAC_ROOT_ALPHABET}")
    print(
        "  roots shared with the frozen partition, without a transliteration "
        f"rule: {REDERIVED_ROOTS_JOINING_THE_PARTITION_UNCHANGED}"
    )
    print(f"  {THE_JOIN_WAS_NOT_TAKEN_NOTE}")

    print("named residuals:")
    for name, note in TRANSITIVITY_LEXICON_NAMED_RESIDUALS.items():
        print(f"  {name}: {note}")

    if not all(checks):
        print(
            "\nat least one frozen number drifted; the deposit is wrong, not the file."
        )
        return 1
    print("\nevery frozen number rederived exactly.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
