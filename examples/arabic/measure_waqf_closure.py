"""Re-derive the waqf closure census: three clause kinds, three standings.

The waqf measured here is **syntactic, not phonetic**: the point at which a
predicative unit closes, not a place to stop in recitation. The phonetic law
registered in ``ibtida_wasl_waqf_registration`` is a different subject that
shares a word, and neither is measured by the other.

The proposed law is one sentence: *a predicative unit closes when both of its
terms are present, and a prepositional phrase never closes by itself.* Every
key therefore gets exactly one of three named standings — closed, open, or
dependent — and their sum is the declared denominator exactly.

    ALGHANEM_MASAQ_PATH=/path/to/MASAQ.csv \\
        python examples/arabic/measure_waqf_closure.py

The bytes are read from ``corpora/MASAQ.csv`` when they are there; the variable
above is for bytes held elsewhere. Either way the byte length and the SHA-256
are matched before a single record is parsed, and no figure is printed if they
are not.

The denominator is **the keys** — stems carrying a frozen opening-term value —
not verses, not all stems, and not "the sentences of the Quran". Reading this
count as a census of Quranic sentences reads a figure without its denominator.

The sharpest limit is printed with every nominal figure. The two terms of a
nominal clause are read from two columns of very different coverage:
``Syntactic_Role`` at 76.3631% of segments holds مبتدأ, while
``Phrasal_Function`` at 1.79% holds خبر and its kinds. So the count of *open*
nominal units reads first as an empty column, not as an unclosed clause — the
same objection that excluded ``Phrase`` (1.80%), which is not read here at all.

Every detector is a **pair of (column, value)**, never a value alone: فاعل in
``Syntactic_Role`` is 10,483 and فاعل in ``Phrasal_Function`` is 1, and those
are two values, not one value with two numbers. Values that arrived with a
count but no named column — ظرف زمان, ظرف مكان, a second نائب فاعل, اسم ناسخ —
are registered suspended by name and enter no count, because a guessed spelling
turns "not among this column's values" into a silent zero.

A verse boundary is not a sentence boundary. Every relation here is measured
inside one verse, so a unit called open may well close in the next verse; that
is the instrument's limit, not a statement about Arabic.

This script adopts no figure, issues no verdict, joins no corpus to another,
reads the ``Phrase`` column not at all, and imports nothing from
``alghanem.kernel``.
"""

from __future__ import annotations

import sys

from alghanem.arabic.masaq_corpus_deposit import (
    MASAQ_ATTRIBUTION,
    MASAQ_PATH_VARIABLE,
    MASAQ_RELATIVE_PATH,
    MasaqDepositError,
    masaq_records,
    read_masaq_bytes,
)
from alghanem.arabic.waqf_closure_census import (
    CLAIMED_KEYS_BY_KIND,
    CLOSURE_SCANNED_COLUMNS,
    WAQF_CLOSURE_CENSUS_NAMED_RESIDUALS,
    WaqfClosureCensusError,
    closing_values_absent_from_their_columns,
    measure_closure,
    scan_column_values,
)
from alghanem.arabic.waqf_closure_preregistration import (
    CLOSURE_DETECTORS,
    KEY_DENOMINATOR,
    NOMINAL_TERM_COVERAGE_GAP,
    PRE_MEASUREMENT_EXPECTATION,
    SUSPENDED_ARRIVING_VALUES,
    WAQF_CLOSURE_PREREGISTRATION_DIGEST,
    WAQF_CLOSURE_PREREGISTRATION_NAMED_RESIDUALS,
    ClauseKind,
    ClosureStanding,
)


def _print_frozen_side() -> None:
    print(MASAQ_ATTRIBUTION)
    print(f"preregistration digest: {WAQF_CLOSURE_PREREGISTRATION_DIGEST}")
    print(f"denominator: {KEY_DENOMINATOR.name} — {KEY_DENOMINATOR.counting_rule}")
    print()
    print("detectors — each a (column, value) pair, count imported not restated:")
    for detector in CLOSURE_DETECTORS:
        print(
            f"  {detector.kind.value} / {detector.side.value}: "
            f"{detector.column} = {detector.value} "
            f"({detector.claimed_segment_count})"
        )
    print()
    print("keys claimed per kind (a sum of the frozen figures, not a fourth number):")
    for kind_name, total in CLAIMED_KEYS_BY_KIND.items():
        print(f"  {kind_name}: {total}")
    print()
    print("suspended arriving values — registered by name, entering no count:")
    for value in SUSPENDED_ARRIVING_VALUES:
        arrived = value.claimed_count if value.claimed_count else "لم يصل"
        print(f"  {value.name} ({arrived}): {value.reason}")
    print()
    print(
        "nominal term coverage gap: "
        f"{NOMINAL_TERM_COVERAGE_GAP.opening_column} "
        f"{NOMINAL_TERM_COVERAGE_GAP.opening_percentage}% vs "
        f"{NOMINAL_TERM_COVERAGE_GAP.closing_column} "
        f"{NOMINAL_TERM_COVERAGE_GAP.closing_percentage}%"
    )
    print()
    print(PRE_MEASUREMENT_EXPECTATION)
    print()
    for name, note in sorted(WAQF_CLOSURE_PREREGISTRATION_NAMED_RESIDUALS.items()):
        print(f"  [{name}] {note}")
    print()


def main() -> int:
    _print_frozen_side()

    try:
        records = masaq_records(read_masaq_bytes())
    except MasaqDepositError as error:
        print(f"no figure without the fingerprinted bytes: {error}")
        print(
            f"place them at {MASAQ_RELATIVE_PATH} or set {MASAQ_PATH_VARIABLE}; "
            "nothing is estimated in their absence."
        )
        return 0

    try:
        census = measure_closure(records)
    except WaqfClosureCensusError as error:
        print(f"the count stopped rather than zeroing itself: {error}")
        return 1

    print("measured on the fingerprinted bytes:")
    for kind in ClauseKind:
        if kind is ClauseKind.OUTSIDE_THE_DETECTORS:
            continue
        print(f"  {kind.value}: {census.keys_of(kind)} keys")
        for standing in ClosureStanding:
            print(f"    {standing.value}: {census.count(kind, standing)}")
        observed = census.attachments_observed[kind.name]
        print(f"    attachment/closure observed: {observed}")
    print(f"  keys in total: {census.keys_total}")
    print(f"  unreadable word keys: {census.unreadable_word_keys}")
    print()

    for column in CLOSURE_SCANNED_COLUMNS:
        scan = scan_column_values(records, column)
        print(f"  total scan of {column}: {scan.distinct_values} distinct values")
    absent = closing_values_absent_from_their_columns(records)
    print(
        "  closing pairs absent from their columns after a total scan: "
        f"{len(absent)}"
    )
    for column, value in absent:
        print(f"    {column} = {value} — a spelling absent, not a category denied")
    print()

    for name, note in sorted(WAQF_CLOSURE_CENSUS_NAMED_RESIDUALS.items()):
        print(f"  [{name}] {note}")
    print()

    failures: list[str] = []
    if not census.conserves_the_denominator:
        failures.append(
            "the three standings do not sum to the keys: the denominator is not "
            "conserved, and the gap is printed rather than closed by adjustment"
        )
    if not census.no_phrase_is_closed:
        failures.append(
            "a prepositional phrase was counted closed; APhraseIsNotAClause is "
            "a definition, so this is an implementation defect, not a finding"
        )
    verbal = census.keys_of(ClauseKind.VERBAL)
    nominal = census.keys_of(ClauseKind.NOMINAL)
    print(
        "expectation one — verbal keys exceed nominal keys: "
        f"{verbal} vs {nominal} — "
        + ("held" if verbal > nominal else "FALSIFIED, and left as measured")
    )
    print(
        "expectation two — the open share of nominal exceeds that of verbal: "
        f"{census.open_share(ClauseKind.NOMINAL):.4f} vs "
        f"{census.open_share(ClauseKind.VERBAL):.4f} — read first as the "
        "emptiness of Phrasal_Function, never as a structure of Arabic"
    )

    for failure in failures:
        print(f"drift: {failure}")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
