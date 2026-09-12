"""Reproduce the lisan345 same-cluster adjacency measurement.

This script is reference material, not part of the kernel or the Arabic layer.
It derives no kernel object, licenses no transition, and asserts no Arabic
cardinality; it only recomputes the frozen numbers recorded in
``docs/reference/lisan345_cluster_adjacency.md``.

The dataset is not vendored into this repository: ``git85hub/lisan345``
publishes no licence file, so only derived counts are stored here. Obtain
``data/lisan3.csv`` yourself at the frozen commit named in the record, then::

    python examples/reference/lisan345_cluster_adjacency.py path/to/lisan3.csv

The script verifies the recorded SHA-256 of the input and refuses to report
numbers for any other file, so a silently updated dataset cannot be mistaken
for the frozen measurement.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import sys
from collections import Counter, defaultdict
from collections.abc import Mapping, Sequence
from pathlib import Path

FROZEN_SOURCE_COMMIT = "67ae8a60c7cb7d05fc92cd85f2eda908b05b9bbb"
FROZEN_INPUT_SHA256 = "bbcfb084e424f61f7647d4a60220cb91d90dfc5d3af517c04b07e61405d0b97e"
FROZEN_ROOT_COUNT = 6529

# ``LAB1``/``LAB2``/``LAB3`` hold the transliterated root consonants. The
# dataset's own ``P``/``M`` columns follow Watson (2002) and are deliberately
# unused: the clusters below are the traditional Arabic places of articulation
# supplied for this measurement, not the dataset's classification.
TRANSLITERATION: Mapping[str, str] = {
    "ʾ": "ء",
    "B": "ب",
    "T": "ت",
    "Ṯ": "ث",
    "Ǧ": "ج",
    "Ḥ": "ح",
    "Ḫ": "خ",
    "D": "د",
    "Ḏ": "ذ",
    "R": "ر",
    "Z": "ز",
    "S": "س",
    "Š": "ش",
    "Ṣ": "ص",
    "Ḍ": "ض",
    "Ṭ": "ط",
    "Ẓ": "ظ",
    "ʿ": "ع",
    "Ġ": "غ",
    "F": "ف",
    "Q": "ق",
    "K": "ك",
    "L": "ل",
    "M": "م",
    "N": "ن",
    "H": "ه",
    "W": "و",
    "Y": "ي",
}

CLUSTERS: Mapping[str, tuple[str, ...]] = {
    "أسلي": ("س", "ص", "ز"),
    "لثوي": ("ث", "ذ", "ظ"),
    "نطعي": ("ت", "د", "ط"),
    "حلقي_أقصى": ("ء", "ه"),
    "حلقي_وسط": ("ع", "ح"),
    "حلقي_أدنى": ("غ", "خ"),
    "شجري": ("ج", "ش"),
    "ذلقي": ("ل", "ن", "ر"),
    "شفهي": ("ب", "م", "و"),
}


def load_roots(path: Path) -> list[tuple[str, str, str]]:
    """Read the triliteral roots as Arabic consonant triples."""
    with path.open(encoding="utf-8-sig", newline="") as handle:
        rows = list(csv.DictReader(handle))
    roots: list[tuple[str, str, str]] = []
    for row in rows:
        first, middle, last = (
            TRANSLITERATION[row[column]] for column in ("LAB1", "LAB2", "LAB3")
        )
        roots.append((first, middle, last))
    return roots


def report(roots: Sequence[tuple[str, str, str]]) -> None:
    """Print the same-cluster adjacency table and the middle-slot check."""
    unigrams = Counter(letter for root in roots for letter in root)
    slots = 3 * len(roots)
    frequency = {letter: count / slots for letter, count in unigrams.items()}
    # Adjacency means R1-R2 or R2-R3; R1-R3 is not adjacent and is excluded.
    bigrams = [(root[0], root[1]) for root in roots]
    bigrams += [(root[1], root[2]) for root in roots]
    trials = len(bigrams)

    print(f"roots={len(roots)} adjacent_bigrams={trials}")
    header = (
        f"{'cluster':<12}{'observed':>10}{'expected':>10}{'ratio':>8}"
        f"{'same_obs':>10}{'same_exp':>10}{'same_ratio':>12}"
    )
    print(header)
    for name, letters in CLUSTERS.items():
        members = set(letters)
        distinct_observed = sum(
            1
            for left, right in bigrams
            if left in members and right in members and left != right
        )
        distinct_expected = trials * sum(
            frequency[x] * frequency[y] for x in letters for y in letters if x != y
        )
        # Gemination is reported separately: folding it into the distinct-pair
        # count would hide that repetition is not what the constraint blocks.
        same_observed = sum(
            1
            for left, right in bigrams
            if left in members and right in members and left == right
        )
        same_expected = trials * sum(frequency[x] * frequency[x] for x in letters)
        print(
            f"{name:<12}{distinct_observed:>10}{distinct_expected:>10.1f}"
            f"{distinct_observed / distinct_expected:>8.2f}"
            f"{same_observed:>10}{same_expected:>10.1f}"
            f"{same_observed / same_expected:>12.2f}"
        )

    middles: defaultdict[tuple[str, str], set[str]] = defaultdict(set)
    for first, middle, last in roots:
        middles[(first, last)].add(middle)
    sizes = [len(values) for values in middles.values()]
    print(
        f"\nouter_pairs={len(sizes)} "
        f"mean_middles={sum(sizes) / len(sizes):.2f} "
        f"max_middles={max(sizes)} "
        f"pairs_with_at_least_20_middles={sum(1 for size in sizes if size >= 20)}"
    )


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="lisan345 cluster adjacency")
    parser.add_argument("csv_path", type=Path, help="path to lisan345 data/lisan3.csv")
    parser.add_argument(
        "--allow-unfrozen-input",
        action="store_true",
        help="report numbers even if the input differs from the frozen dataset",
    )
    args = parser.parse_args(argv)

    digest = hashlib.sha256(args.csv_path.read_bytes()).hexdigest()
    if digest != FROZEN_INPUT_SHA256:
        message = (
            f"input sha256 {digest} does not match the frozen dataset "
            f"{FROZEN_INPUT_SHA256} (commit {FROZEN_SOURCE_COMMIT})"
        )
        if not args.allow_unfrozen_input:
            print(f"error: {message}", file=sys.stderr)
            return 1
        print(f"warning: {message}", file=sys.stderr)

    roots = load_roots(args.csv_path)
    if len(roots) != FROZEN_ROOT_COUNT and not args.allow_unfrozen_input:
        print(
            f"error: expected {FROZEN_ROOT_COUNT} roots, read {len(roots)}",
            file=sys.stderr,
        )
        return 1
    report(roots)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
