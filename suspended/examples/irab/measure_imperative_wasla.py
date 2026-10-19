"""Re-derive the frozen `imperative_wasla_census` numbers from the corpus itself.

This script is reference material, not part of the kernel or the Arabic layer.
It derives no kernel object, licenses no transition, and issues no grammatical
judgement about any root. It recomputes the numbers frozen in
``src/alghanem/arabic/imperative_wasla_census.py`` and fails loudly if they
drift.

The corpus is deliberately **not** vendored: the Quranic Arabic Corpus is
GPL-licensed and the Tanzil Uthmani text it embeds is CC BY-ND, and both forbid
modification. Obtain the exact file named in
``alghanem.arabic.irab_corpus_witness.QURANIC_ARABIC_CORPUS_WITNESS``, then::

    python examples/irab/measure_imperative_wasla.py path/to/morphology-0.4.txt

The script verifies the recorded SHA-256 and byte length first and refuses to
report numbers for any other file.

What a match does establish: that under each of the four declared weakness
rules, the hollow root takes no hamzat al-waṣl at all, and that inside the
doubled root the assimilation itself predicts the waṣl in 21 of 22 positions.
What it does not establish: the single figure of 96.9% for the sound root,
which appears under no rule; the sound rate moves between 84.4% and 100.0%
depending on whether hamza is counted as a weak letter and whether the doubled
root is separated. The specification is marked `مُصاغة_بعد_الرقم` — formulated
after the number — because it was, and the four rules are printed together so
that no single one can be quoted without its assumption.

Source: the Quranic Arabic Corpus, http://corpus.quran.com — built on the
Tanzil Quran text, http://tanzil.info. Both attributions are conditions of the
licences above, not courtesies.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from alghanem.arabic.hollow_root_root_census import corpus_lines, parse_segment_line
from alghanem.arabic.imperative_wasla_census import (
    ARRIVING_IMPERATIVE_DIVERGENCES,
    BARE_IMPERATIVE_SEGMENTS,
    DOUBLED_ROOT_RESIDUAL,
    IMPERATIVE_WASLA_CENSUS_NAMED_RESIDUALS,
    NAQIS_RESIDUAL,
    REDERIVED_IDGHAM_AGREEMENT,
    REDERIVED_IMPERFECT_COEXISTENCE,
    REDERIVED_SALIM_AJWAF_TEST,
    REDERIVED_SHAPE_TABLES,
    classify_root,
    idgham_agreement,
    imperfect_coexistence,
    permutation_test,
    read_imperative,
    shape_table,
)
from alghanem.arabic.imperative_wasla_specification import (
    IMPERATIVE_WASL_NAMED_RESIDUALS,
    STANDING,
    WEAKNESS_RULES,
    RootShape,
)
from alghanem.arabic.irab_corpus_witness import QURANIC_ARABIC_CORPUS_WITNESS


def _compare(label: str, measured: object, frozen: object) -> bool:
    matched = measured == frozen
    mark = "=" if matched else "!"
    print(f"  [{mark}] {label}: measured={measured!r} frozen={frozen!r}")
    return matched


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("corpus", type=Path, help="path to the morphology file")
    arguments = parser.parse_args(argv)

    records = [
        record
        for record in (
            parse_segment_line(line) for line in corpus_lines(arguments.corpus)
        )
        if record is not None
    ]
    readings = tuple(
        reading
        for reading in (read_imperative(record) for record in records)
        if reading is not None
    )
    bare = tuple(reading for reading in readings if reading.is_bare)

    print(f"witness: {QURANIC_ARABIC_CORPUS_WITNESS.measured_path}")
    print(f"  sha256={QURANIC_ARABIC_CORPUS_WITNESS.sha256}")
    print(f"specification standing: {STANDING.value}")

    checks = [_compare("bare imperative segments", len(bare), BARE_IMPERATIVE_SEGMENTS)]

    print("the table under every declared rule:")
    for rule in WEAKNESS_RULES:
        print(f"  rule «{rule.name}» — assumes: {rule.what_it_assumes}")
        measured = {
            count.shape.value: (count.with_wasla, count.segments)
            for count in shape_table(bare, rule)
        }
        checks.append(
            _compare(
                f"    table[{rule.name}]", measured, REDERIVED_SHAPE_TABLES[rule.name]
            )
        )

    print("the permutation test, at the narrowest rule and the widest:")
    for rule_name, frozen in REDERIVED_SALIM_AJWAF_TEST.items():
        rule = next(item for item in WEAKNESS_RULES if item.name == rule_name)
        sound = [
            reading.has_wasla
            for reading in bare
            if classify_root(reading.root, rule) is RootShape.SALIM
        ]
        hollow = [
            reading.has_wasla
            for reading in bare
            if classify_root(reading.root, rule) is RootShape.AJWAF
        ]
        checks.append(
            _compare(
                f"  test[{rule_name}]",
                permutation_test(frozen.label, sound, hollow),
                frozen,
            )
        )

    print("the mechanism tested inside the doubled root alone:")
    checks.append(
        _compare(
            "  idgham agreement", idgham_agreement(bare), REDERIVED_IDGHAM_AGREEMENT
        )
    )
    print(
        f"  agreeing {REDERIVED_IDGHAM_AGREEMENT.agreeing} of "
        f"{REDERIVED_IDGHAM_AGREEMENT.total}"
    )

    print("the imperfect as a precondition, counted and not settled:")
    checks.append(
        _compare(
            "  coexistence",
            imperfect_coexistence(records),
            REDERIVED_IMPERFECT_COEXISTENCE,
        )
    )

    print("named residual positions, kept rather than dropped:")
    for residual in (DOUBLED_ROOT_RESIDUAL, NAQIS_RESIDUAL):
        print(
            f"  ({residual.sura}:{residual.aya}:{residual.word}:{residual.segment}) "
            f"{residual.form} ROOT:{residual.root}"
        )
        print(f"    {residual.why_it_is_named}")

    print("the arriving figures, each against what the bytes gave:")
    matched = 0
    for divergence in ARRIVING_IMPERATIVE_DIVERGENCES:
        if divergence.matched:
            matched += 1
        print(
            f"  [{'=' if divergence.matched else '!'}] {divergence.figure.label}: "
            f"arrived={divergence.figure.claimed_value} "
            f"rederived={divergence.rederived_value} "
            f"(under {divergence.under_rule})"
        )
    print(f"  matched {matched} of {len(ARRIVING_IMPERATIVE_DIVERGENCES)}")

    print("named residuals:")
    for name, note in {
        **IMPERATIVE_WASL_NAMED_RESIDUALS,
        **IMPERATIVE_WASLA_CENSUS_NAMED_RESIDUALS,
    }.items():
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
