"""Re-derive the frozen `transitivity_corpus_census` numbers from the corpus itself.

This script is reference material, not part of the kernel or the Arabic layer.
It derives no kernel object, licenses no transition, and issues no grammatical
judgement about any root. It only recomputes the numbers frozen in
``src/alghanem/arabic/transitivity_corpus_census.py`` and fails loudly if they
drift.

The corpus is deliberately **not** vendored: the Quranic Arabic Corpus is
GPL-licensed and the Tanzil Uthmani text it embeds is CC BY-ND, and both forbid
modification. Obtain the exact file named in
``alghanem.arabic.irab_corpus_witness.QURANIC_ARABIC_CORPUS_WITNESS``, then::

    python examples/irab/measure_transitivity_census.py path/to/morphology-0.4.txt

The script verifies the recorded SHA-256 and byte length first and refuses to
report numbers for any other file.

What a match does establish: the four results hold *in this corpus*, under the
counting rules frozen in ``transitivity_probe_preregistration``. What it does
not establish: that the figures which arrived in the originating text are
reproducible — none of the fifteen matched, and the divergence table is printed
here rather than hidden. Nor does it establish anything about the maṣdar, the
morphological noun of place or time, the noun of instrument, or tamyīz: the
corpus does not tag them, so they are left without a number rather than with a
zero.

Source: the Quranic Arabic Corpus, http://corpus.quran.com — built on the
Tanzil Quran text, http://tanzil.info. Both attributions are conditions of the
licences above, not courtesies.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from alghanem.arabic.hollow_root_root_census import corpus_lines, parse_segment_line
from alghanem.arabic.irab_corpus_witness import QURANIC_ARABIC_CORPUS_WITNESS
from alghanem.arabic.transitivity_corpus_census import (
    ARRIVING_FIGURE_DIVERGENCES,
    AUGMENTED_PASSIVE_EXAMPLES,
    REDERIVED_ACTIVE_PARTICIPLE_TEST,
    REDERIVED_AUGMENTED_PASSIVE_TEST,
    REDERIVED_BARE_PERFECT_ACTIVE_ROOTS,
    REDERIVED_CONFIRMED_TRANSITIVE,
    REDERIVED_INTRANSITIVE_CANDIDATES,
    REDERIVED_PARTICIPLE_RATES,
    REDERIVED_PASSIVE_PARTICIPLE_TEST,
    REDERIVED_TAGGED_ROOTS,
    REDERIVED_TENSE_SPLIT,
    REDERIVED_VERB_TAGGED_ROOTS,
    PermutationOutcome,
    RootProfile,
    Tense,
    TransitivityCensusError,
    Voice,
    participle_rates,
    partition_roots,
    permutation_test,
    root_profiles,
    tense_split,
)
from alghanem.arabic.transitivity_probe_preregistration import (
    PERMUTATION_PROTOCOL,
    TRANSITIVITY_PROBE_NAMED_RESIDUALS,
    UNTAGGED_CATEGORIES,
    TransitivityClass,
)


def _check(label: str, expected: object, actual: object) -> bool:
    status = "MATCH" if expected == actual else "DRIFT"
    print(f"  {status:5}  {label}: expected {expected!r}, rederived {actual!r}")
    return expected == actual


def _report_test(outcome: PermutationOutcome, frozen: PermutationOutcome) -> bool:
    print(f"  {outcome.label}:")
    ok = _check(
        "observed gap (points)", frozen.observed_gap_points, outcome.observed_gap_points
    )
    ok &= _check(
        "maximum null gap (points)",
        frozen.maximum_null_gap_points,
        outcome.maximum_null_gap_points,
    )
    ok &= _check(
        "permutations at least as extreme",
        frozen.at_least_as_extreme,
        outcome.at_least_as_extreme,
    )
    floor = PERMUTATION_PROTOCOL.p_value_floor
    print(f"         p = {outcome.p_value:.6f} (floor {floor:.6f})")
    return ok


def _verb_tagged(profiles: dict[str, RootProfile]) -> int:
    return sum(
        1
        for profile in profiles.values()
        if profile.bare_verb_shapes or profile.augmented_verb_shapes
    )


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "corpus",
        type=Path,
        help="path to the exact fingerprinted morphology file, never vendored here",
    )
    arguments = parser.parse_args(argv)
    try:
        lines = corpus_lines(arguments.corpus)
    except Exception as error:  # noqa: BLE001 - the refusal is the message
        print(f"refused: {error}", file=sys.stderr)
        return 2
    witness = QURANIC_ARABIC_CORPUS_WITNESS
    print(f"corpus: {witness.corpus} {witness.version}")
    print(f"sha256 verified: {witness.sha256}")

    records = [
        record
        for record in (parse_segment_line(line) for line in lines)
        if record is not None
    ]
    try:
        profiles = root_profiles(records)
    except TransitivityCensusError as error:
        print(f"refused: {error}", file=sys.stderr)
        return 2
    partition = partition_roots(profiles)

    print("\nresult 1 — the central partition")
    ok = _check("tagged roots", REDERIVED_TAGGED_ROOTS, len(profiles))
    ok &= _check(
        "verb-tagged roots", REDERIVED_VERB_TAGGED_ROOTS, _verb_tagged(profiles)
    )
    ok &= _check(
        "roots with a bare active perfect",
        REDERIVED_BARE_PERFECT_ACTIVE_ROOTS,
        len(partition.confirmed_transitive) + len(partition.intransitive_candidates),
    )
    ok &= _check(
        "confirmed transitive",
        REDERIVED_CONFIRMED_TRANSITIVE,
        len(partition.confirmed_transitive),
    )
    ok &= _check(
        "intransitive candidates",
        REDERIVED_INTRANSITIVE_CANDIDATES,
        len(partition.intransitive_candidates),
    )

    print("\nresult 2 — the passive across the two tenses")
    split = tense_split(profiles)
    ok &= _check(
        "bare imperfect passive only",
        REDERIVED_TENSE_SPLIT.imperfect_passive_only,
        split.imperfect_passive_only,
    )
    ok &= _check(
        "both tenses passive",
        REDERIVED_TENSE_SPLIT.both_tenses_passive,
        split.both_tenses_passive,
    )
    ok &= _check(
        "bare perfect passive only",
        REDERIVED_TENSE_SPLIT.perfect_passive_only,
        split.perfect_passive_only,
    )

    print("\nresult 3 — participles, by root")
    for frozen in REDERIVED_PARTICIPLE_RATES:
        rates = participle_rates(
            profiles,
            partition.roots_of(frozen.transitivity_class),
            frozen.transitivity_class,
        )
        ok &= _check(
            f"{frozen.transitivity_class.name} group size",
            frozen.group_size,
            rates.group_size,
        )
        ok &= _check(
            f"{frozen.transitivity_class.name} active participle roots",
            frozen.active_participle_roots,
            rates.active_participle_roots,
        )
        ok &= _check(
            f"{frozen.transitivity_class.name} passive participle roots",
            frozen.passive_participle_roots,
            rates.passive_participle_roots,
        )
        print(
            f"         active {rates.active_percentage:.1f}% | "
            f"passive {rates.passive_percentage:.1f}%"
        )

    transitive = partition.roots_of(TransitivityClass.CONFIRMED_TRANSITIVE)
    intransitive = partition.roots_of(TransitivityClass.INTRANSITIVE_CANDIDATE)
    for frozen, voice in (
        (REDERIVED_PASSIVE_PARTICIPLE_TEST, Voice.PASSIVE),
        (REDERIVED_ACTIVE_PARTICIPLE_TEST, Voice.ACTIVE),
    ):
        ok &= _report_test(
            permutation_test(
                frozen.label,
                [profiles[root].has_participle(voice) for root in transitive],
                [profiles[root].has_participle(voice) for root in intransitive],
            ),
            frozen,
        )

    print("\nresult 4 — does augmentation turn the intransitive transitive?")
    augmented = REDERIVED_AUGMENTED_PASSIVE_TEST
    ok &= _report_test(
        permutation_test(
            augmented.label,
            [profiles[root].has_augmented_passive() for root in transitive],
            [profiles[root].has_augmented_passive() for root in intransitive],
        ),
        augmented,
    )
    for example in AUGMENTED_PASSIVE_EXAMPLES:
        profile = profiles[example.root_buckwalter]
        present = example.form in profile.augmented_passive_forms()
        in_group = example.root_buckwalter in intransitive
        ok &= _check(
            f"{example.root_arabic} ({example.root_buckwalter}) form {example.form} "
            f"passive at {example.location}",
            (True, True),
            (present, in_group),
        )

    print("\nthe arriving figures against the rederived ones")
    for divergence in ARRIVING_FIGURE_DIVERGENCES:
        status = "MATCH" if divergence.matched else "DIVERGED"
        print(
            f"  {status:9} {divergence.figure.label}: "
            f"arrived {divergence.figure.claimed_value}, "
            f"rederived {divergence.rederived_value} "
            f"[{divergence.figure.counting_rule.name}]"
        )

    print("\nnot measured here, and left without a number")
    for category in UNTAGGED_CATEGORIES:
        print(
            f"  {category.arabic_name}: {category.why_it_is_not_measurable_here} "
            f"(nearest tag {category.nearest_available_tag} — "
            f"{category.why_the_nearest_tag_is_not_it})"
        )

    print("\nnamed residuals that travel with every number above")
    for name in sorted(TRANSITIVITY_PROBE_NAMED_RESIDUALS):
        print(f"  {name}")

    if not ok:
        print(
            "\nthe frozen numbers drifted; nothing is rewritten here", file=sys.stderr
        )
        return 1
    print("\nevery frozen number rederived exactly")
    print(
        f"a bare perfect is a {Tense.PERFECT.value} with no form tag; "
        "a tense tag alone is never a voice"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
