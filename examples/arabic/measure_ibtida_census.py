"""Re-derive the inchoative denominator, its four classes and the mubtadaʾ standings.

The inchoative is **not measured over the stems**. 77,797 stems and 157,677
segments are two other denominators, and most of what they count cannot begin
a nominal sentence at all. The denominator declared here is the **positions
that admit inchoativity**: the eight ``Syntactic_Role`` values of mubtadaʾ and
khabar together, 11,349 positions. ``ADenominatorIsDeclaredNotAssumed`` is why
every ratio printed below carries that denominator with it, and why the stem
and segment totals are printed beside it — three denominators, not three rival
figures.

    ALGHANEM_MASAQ_PATH=/path/to/MASAQ.csv \\
        python examples/arabic/measure_ibtida_census.py

The bytes are read from ``corpora/MASAQ.csv`` when they are there; the
variable above is for bytes held elsewhere. Either way the byte length and the
SHA-256 are matched before a single record is parsed, and no figure is printed
if they are not.

A role tag is not a link. "khabar" says *this is a predicate*, never *this is
the predicate of that mubtadaʾ*: the corpus has no column binding the two, so
each inchoative gets one of three named standings inside **its own verse** —
one tagged predicate, no tagged predicate (named by its place, not summed into
a zero), or more than one candidate. No accuracy is reported and none can be:
there is no gold for this link.

Four residues are named before they are excused: three accusative mubtadaʾ
(printed position by position, because three is a number to inspect one by one
and not to summarise), an arriving 187-difference whose two terms did not
arrive, the two nasikh differences derived by subtraction rather than written
as third numbers, and a fronted predicate that carries no tag at all.

This script adopts no figure, issues no verdict, joins no corpus to another,
reads the ``Phrasal_Function`` column not at all, and imports nothing from
``alghanem.kernel``.
"""

from __future__ import annotations

import sys

from alghanem.arabic.ibtida_census import (
    IBTIDA_CENSUS_NAMED_RESIDUALS,
    GovernorStanding,
    IbtidaCensusError,
    MubtadaStanding,
    classify_positions,
    measure_accusative_mubtada,
    measure_governors,
    measure_inchoative_relations,
    read_inchoative_denominator,
)
from alghanem.arabic.ibtida_preregistration import (
    ARRIVING_INCHOATIVE_POSITIONS,
    ARRIVING_MUBTADA_BREAKDOWN,
    IBTIDA_PREREGISTRATION_DIGEST,
    IBTIDA_PREREGISTRATION_NAMED_RESIDUALS,
    INCHOATIVE_POSITION_DENOMINATOR,
    INCHOATIVE_POSITION_TOTAL,
    NAMED_RESIDUES,
    PRE_MEASUREMENT_EXPECTATION,
    THE_RETRACTED_TOTAL_DENIAL,
    SentenceClass,
    figures_of_class,
)
from alghanem.arabic.irab_operator_preregistration import ARRIVING_STEM_TOTAL
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
    print(f"preregistration digest: {IBTIDA_PREREGISTRATION_DIGEST}")
    print(
        f"denominator: {INCHOATIVE_POSITION_DENOMINATOR.name} "
        f"({INCHOATIVE_POSITION_TOTAL} positions) — "
        f"{INCHOATIVE_POSITION_DENOMINATOR.counting_rule}"
    )

    try:
        records = masaq_records(read_masaq_bytes())
    except (MasaqDepositError, IbtidaCensusError) as error:
        print(f"error: {error}", file=sys.stderr)
        print(
            f"deposit the bytes at {MASAQ_RELATIVE_PATH} or declare "
            f"{MASAQ_PATH_VARIABLE}; no figure is printed without them",
            file=sys.stderr,
        )
        return 1

    reading = read_inchoative_denominator(records)
    classes = classify_positions(records)
    relations = measure_inchoative_relations(records)
    governors = measure_governors(records)
    accusative = measure_accusative_mubtada(records)

    print(
        f"[denominator] inchoative_positions={reading.denominator_count} "
        f"(claimed {INCHOATIVE_POSITION_TOTAL}) "
        f"stems={reading.stem_count} (claimed {ARRIVING_STEM_TOTAL}) "
        f"segments={reading.segment_count}"
    )
    for figure in ARRIVING_INCHOATIVE_POSITIONS:
        measured = reading.counts_by_value.get(figure.value)
        print(
            f"    {figure.value}: measured="
            f"{measured if measured is not None else 'ليست من قيم هذا العمود'} "
            f"claimed={figure.claimed_segment_count} "
            f"class={figure.sentence_class.name} side={figure.side.value}"
        )
    for sentence_class in SentenceClass:
        claimed = sum(
            figure.claimed_segment_count for figure in figures_of_class(sentence_class)
        )
        measured_class = classes.positions_by_class[sentence_class.name]
        share = reading.share_of_the_denominator(measured_class)
        print(
            f"    [{sentence_class.name}] measured={measured_class} "
            f"(claimed {claimed}) share_of_the_denominator={share:.4f}"
        )
    print(
        f"[conservation] four_classes={classes.positions_in_the_four_classes} "
        f"denominator={classes.denominator_count} "
        f"conserved={classes.conserves_the_denominator} "
        f"stems_outside={classes.stems_outside_the_denominator}"
    )
    print(
        f"[relations] inchoatives={relations.inchoatives} "
        f"predicates={relations.predicates} "
        f"unreadable_word_keys={relations.unreadable_word_keys} "
        f"no_predicate_value_for_their_class="
        f"{relations.inchoatives_whose_class_has_no_predicate_value}"
    )
    for standing in MubtadaStanding:
        print(f"    {standing.value}: {relations.standings[standing.name]}")
    for reference in relations.positions_without_a_predicate[:8]:
        print(f"    بلا خبرٍ موسوم: {reference}")
    print(
        f"[governors] by_value={governors.governors_by_value} "
        f"absent_values={governors.absent_values or 'لا شيء'}"
    )
    for standing in GovernorStanding:
        print(f"    {standing.value}: {governors.standings[standing.name]}")
    for reference in governors.governors_without_a_name[:8]:
        print(f"    ناسخٌ بلا اسمٍ موسوم: {reference}")
    print(f"[accusative mubtadaʾ] count={accusative.count} (claimed 3)")
    for reference, marker in zip(accusative.references, accusative.markers):
        print(f"    {reference} — علامتُه {marker or 'بلا علامةٍ موسومة'}")
    print(
        f"[mubtadaʾ breakdown] positions={ARRIVING_MUBTADA_BREAKDOWN.positions} "
        f"top_marker={ARRIVING_MUBTADA_BREAKDOWN.top_marker_label} "
        f"share={ARRIVING_MUBTADA_BREAKDOWN.top_marker_share:.4f} "
        f"unaccounted_by_build={ARRIVING_MUBTADA_BREAKDOWN.unaccounted_by_build}"
    )
    for residue in NAMED_RESIDUES:
        size = residue.claimed_size if residue.claimed_size is not None else "لا عددَ له"
        print(f"    [residue] {residue.name}: {size} — {residue.derivation.name}")
    print(PRE_MEASUREMENT_EXPECTATION)
    print(THE_RETRACTED_TOTAL_DENIAL)
    for name, note in sorted(IBTIDA_PREREGISTRATION_NAMED_RESIDUALS.items()):
        print(f"    {name}: {note}")
    for name, note in sorted(IBTIDA_CENSUS_NAMED_RESIDUALS.items()):
        print(f"    {name}: {note}")

    outcomes = (
        reading.denominator_count == INCHOATIVE_POSITION_TOTAL,
        reading.stem_count == ARRIVING_STEM_TOTAL,
        classes.conserves_the_denominator,
        all(
            reading.counts_by_value.get(figure.value) == figure.claimed_segment_count
            for figure in ARRIVING_INCHOATIVE_POSITIONS
        ),
    )
    if all(outcomes):
        print("the arriving denominator and its eight figures re-derive from the bytes")
        return 0
    print(
        "error: a derived figure differs from the arriving record; the record "
        "is not edited to match it",
        file=sys.stderr,
    )
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
