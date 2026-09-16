"""Re-derive the stem-denominator coverage, its residue and the operator pairs.

MASAQ's ``Syntactic_Role`` is filled in 76.36% of **segments** — a figure that
reads as a gap in the annotation. Restricted to **stems** alone, the same
column is filled in 99.68%. The two are not rival numbers; they are two
ratios with two denominators, and ``ADenominatorIsDeclaredNotAssumed`` is why
every ratio printed here carries its denominator with it. Prefixes and
suffixes have no i'rab case to begin with, so counting them in the denominator
lowers a ratio that never fell.

    ALGHANEM_MASAQ_PATH=/path/to/MASAQ.csv \\
        python examples/arabic/measure_irab_operators.py

The bytes are read from ``corpora/MASAQ.csv`` when they are there; the
variable above is for bytes held elsewhere. Either way the byte length and the
SHA-256 are matched before a single record is parsed, and no figure is printed
if they are not.

The residue is 246 stems, and it is **named before it is excused**: 190 verses
at 1.29 stems each, in two distinct patterns — a verse whose other stems are
annotated and one is not, and a verse left wholly unannotated, the largest
being 2:13 with thirteen stems. What did not arrive is how the remaining 82
stems split between the second and third patterns, so that place is left
declared and empty rather than filled with a zero.

Coverage is not correctness. 99.68% counts the stems that **were** annotated,
not the stems annotated **rightly**: in that same 2:13, "آمَنَ" — a perfect
verb — is tagged ``مجزوم``.

The relation measured here is a **neighbourhood inside one verse**, never
across a verse boundary, and it is not a proven government: the corpus has no
column binding an operator to its own dependent, so each dependent gets one of
three named standings — an operator before it, an operator after it, or no
operator observed — and the distance to the nearest one is printed in words.

This script adopts no figure, issues no verdict, joins no corpus to another,
reads the ``Phrase`` column not at all, and imports nothing from
``alghanem.kernel``.
"""

from __future__ import annotations

import sys

from alghanem.arabic.irab_operator_census import (
    ARRIVING_RESIDUE_STEMS,
    ARRIVING_RESIDUE_VERSES,
    DependentStanding,
    IrabOperatorCensusError,
    measure_relations,
    measure_residue,
    read_stem_coverage,
)
from alghanem.arabic.irab_operator_preregistration import (
    ACCEPTANCE_THRESHOLD_PERCENTAGE,
    ARRIVING_RESIDUE_ACCOUNT,
    ARRIVING_STEM_TOTAL,
    DEPENDENT_ROLE_VALUES,
    IRAB_OPERATOR_PREREGISTRATION_DIGEST,
    IRAB_OPERATOR_PREREGISTRATION_NAMED_RESIDUALS,
    NEUTRAL_ROLE_VALUES,
    OPERATOR_ROLE_VALUES,
    PRE_MEASUREMENT_EXPECTATION,
    STEM_DENOMINATOR,
    ResiduePattern,
)
from alghanem.arabic.masaq_corpus_deposit import (
    MASAQ_ATTRIBUTION,
    MASAQ_PATH_VARIABLE,
    MASAQ_RELATIVE_PATH,
    MasaqDepositError,
    masaq_records,
    read_masaq_bytes,
)


def main() -> int:
    print(MASAQ_ATTRIBUTION)
    print(f"preregistration digest: {IRAB_OPERATOR_PREREGISTRATION_DIGEST}")
    print(f"denominator: {STEM_DENOMINATOR.name} — {STEM_DENOMINATOR.counting_rule}")

    try:
        records = masaq_records(read_masaq_bytes())
    except (MasaqDepositError, IrabOperatorCensusError) as error:
        print(f"error: {error}", file=sys.stderr)
        print(
            f"deposit the bytes at {MASAQ_RELATIVE_PATH} or declare "
            f"{MASAQ_PATH_VARIABLE}; no figure is printed without them",
            file=sys.stderr,
        )
        return 1

    coverage = read_stem_coverage(records)
    residue = measure_residue(records)
    relations = measure_relations(records)

    print(
        f"[coverage] column={coverage.column} denominator={STEM_DENOMINATOR.name} "
        f"stems={coverage.denominator_count} (claimed {ARRIVING_STEM_TOTAL}) "
        f"covered={coverage.covered_count} "
        f"measured={coverage.measured_percentage:.4f}% "
        f"claimed={coverage.declared_percentage}% "
        f"threshold={ACCEPTANCE_THRESHOLD_PERCENTAGE}% "
        f"meets_threshold={coverage.meets_threshold}"
    )
    print(
        f"[residue] stems={residue.residue_stems} (claimed {ARRIVING_RESIDUE_STEMS}) "
        f"verses={residue.residue_verses} (claimed {ARRIVING_RESIDUE_VERSES}) "
        f"stems_per_verse={residue.stems_per_verse:.2f}"
    )
    claimed_verses = {
        account.pattern: account.verses for account in ARRIVING_RESIDUE_ACCOUNT
    }
    claimed_stems = {
        account.pattern: account.stems for account in ARRIVING_RESIDUE_ACCOUNT
    }
    for pattern in ResiduePattern:
        stems = claimed_stems[pattern]
        print(
            f"    {pattern.name}: verses={residue.verses_by_pattern[pattern.name]} "
            f"(claimed {claimed_verses[pattern]}) "
            f"stems={residue.stems_by_pattern[pattern.name]} "
            f"(claimed {stems if stems is not None else 'لم يصل'})"
        )
    print(
        f"[relations] operators={relations.operators} "
        f"dependents={relations.dependents} "
        f"unreadable_word_keys={relations.unreadable_word_keys}"
    )
    for standing in DependentStanding:
        print(f"    {standing.value}: {relations.standings[standing.name]}")
    print(
        f"    preceding_share_of_decided="
        f"{relations.preceding_share_of_decided:.4f} "
        f"most_common_distance={relations.most_common_distance}"
    )
    for distance in sorted(relations.distances)[:8]:
        print(f"    distance={distance} words: {relations.distances[distance]}")
    print(f"operators: {', '.join(OPERATOR_ROLE_VALUES)}")
    print(f"dependents: {', '.join(DEPENDENT_ROLE_VALUES)}")
    print(f"neutral: {', '.join(NEUTRAL_ROLE_VALUES)}")
    print(PRE_MEASUREMENT_EXPECTATION)
    for name, note in sorted(IRAB_OPERATOR_PREREGISTRATION_NAMED_RESIDUALS.items()):
        print(f"    {name}: {note}")

    outcomes = (
        coverage.denominator_count == ARRIVING_STEM_TOTAL,
        coverage.agrees_with_the_declared,
        coverage.residue_count == ARRIVING_RESIDUE_STEMS,
        residue.residue_stems == coverage.residue_count,
        residue.residue_verses == ARRIVING_RESIDUE_VERSES,
    )
    if all(outcomes):
        print("the arriving coverage and residue re-derive from the bytes")
        return 0
    print(
        "error: a derived figure differs from the arriving record; the record "
        "is not edited to match it",
        file=sys.stderr,
    )
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
