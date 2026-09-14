"""Re-derive the frozen `irab_case_readout` measurements from the corpus itself.

This script is reference material, not part of the kernel or the Arabic layer.
It derives no kernel object, licenses no transition, and asserts no Arabic
cardinality. It only recomputes the numbers frozen in
``src/alghanem/arabic/irab_case_readout.py`` and fails loudly if they drift.

The corpus is deliberately **not** vendored: the Quranic Arabic Corpus is
GPL-licensed and the Tanzil Uthmani text it embeds is CC BY-ND, and both forbid
modification. Obtain the exact file named in
``alghanem.arabic.irab_corpus_witness.QURANIC_ARABIC_CORPUS_WITNESS``, then::

    python examples/irab/measure_case_readout.py path/to/morphology-0.4.txt

The script verifies the recorded SHA-256 and byte length first and refuses to
report numbers for any other file, so a silently updated corpus cannot be
mistaken for the frozen measurement.

Source: the Quranic Arabic Corpus, http://corpus.quran.com — built on the
Tanzil Quran text, http://tanzil.info. Both attributions are conditions of the
licences above, not courtesies.
"""

from __future__ import annotations

import argparse
import hashlib
import sys
import unicodedata
from collections import Counter, OrderedDict
from pathlib import Path

from alghanem.arabic.irab_case_readout import (
    AS_STATED_HYPOTHESIS_BASELINE,
    DEVELOPMENT_SPLIT_MEASUREMENT,
    HELD_OUT_SPLIT_MEASUREMENT,
    NORMALIZATION_FORM,
    WHOLE_CORPUS_MEASUREMENT,
    CaseReadout,
    CaseReadoutMeasurement,
    development_split_contains,
    read_surface_case,
)
from alghanem.arabic.irab_corpus_witness import QURANIC_ARABIC_CORPUS_WITNESS

# The corpus ships Buckwalter transliteration. This table is declared here, not
# derived from any property of Arabic; the trailing entries are the Quranic
# recitation marks the corpus encodes with ASCII punctuation.
BUCKWALTER: dict[str, str] = {
    "'": "\u0621",
    "|": "\u0622",
    ">": "\u0623",
    "&": "\u0624",
    "<": "\u0625",
    "}": "\u0626",
    "A": "\u0627",
    "b": "\u0628",
    "p": "\u0629",
    "t": "\u062a",
    "v": "\u062b",
    "j": "\u062c",
    "H": "\u062d",
    "x": "\u062e",
    "d": "\u062f",
    "*": "\u0630",
    "r": "\u0631",
    "z": "\u0632",
    "s": "\u0633",
    "$": "\u0634",
    "S": "\u0635",
    "D": "\u0636",
    "T": "\u0637",
    "Z": "\u0638",
    "E": "\u0639",
    "g": "\u063a",
    "_": "\u0640",
    "f": "\u0641",
    "q": "\u0642",
    "k": "\u0643",
    "l": "\u0644",
    "m": "\u0645",
    "n": "\u0646",
    "h": "\u0647",
    "w": "\u0648",
    "Y": "\u0649",
    "y": "\u064a",
    "F": "\u064b",
    "N": "\u064c",
    "K": "\u064d",
    "a": "\u064e",
    "u": "\u064f",
    "i": "\u0650",
    "~": "\u0651",
    "o": "\u0652",
    "`": "\u0670",
    "{": "\u0671",
    "^": "\u0653",
    "#": "\u0654",
    "@": "\u06df",
    ":": "\u06dc",
    '"': "\u06e2",
    "[": "\u06e3",
    "]": "\u06ed",
    ",": "\u06d6",
    ".": "\u06d7",
    "-": "\u06d8",
    "+": "\u06d9",
    "!": "\u06da",
}

GOLD_CASE_READOUT: dict[str, CaseReadout] = {
    "NOM": CaseReadout.مرفوع,
    "ACC": CaseReadout.منصوب,
    "GEN": CaseReadout.مجرور,
}

FATHA = "\u064e"
FATHATAN = "\u064b"
SUKUN = "\u0652"
SHORT_VOWELS = frozenset("\u064b\u064c\u064d\u064e\u064f\u0650")

Key = tuple[int, int, int]
Row = tuple[Key, str, str]


def to_arabic(buckwalter: str) -> str:
    """Transliterate one corpus form and canonicalize it once, at the border."""

    return unicodedata.normalize(
        NORMALIZATION_FORM,
        "".join(BUCKWALTER.get(character, character) for character in buckwalter),
    )


def load_words(path: Path) -> OrderedDict[Key, tuple[str, tuple[str, ...]]]:
    """Join the corpus's morphological segments back into whole words."""

    forms: OrderedDict[Key, str] = OrderedDict()
    features: dict[Key, list[str]] = {}
    with path.open(encoding="utf-8") as handle:
        for line in handle:
            if not line.startswith("("):
                continue
            location, form, _tag, feature = line.rstrip("\n").split("\t")
            sura, aya, word, _segment = (
                int(part) for part in location.strip("()").split(":")
            )
            key: Key = (sura, aya, word)
            forms[key] = forms.get(key, "") + to_arabic(form)
            features.setdefault(key, []).append(feature)
    return OrderedDict(
        (key, (form, tuple(features[key]))) for key, form in forms.items()
    )


def gold_case(features: tuple[str, ...]) -> str | None:
    """Read the corpus's own case tag; this is its annotation, not our reading."""

    for feature in features:
        for case in ("NOM", "ACC", "GEN"):
            if feature.endswith("|" + case) or ("|" + case + "|") in feature:
                return case
    return None


def is_perfect_verb(features: tuple[str, ...]) -> bool:
    return any("POS:V" in feature and "PERF" in feature for feature in features)


def final_short_vowel(surface: str) -> str | None:
    """The naive readout the original hypothesis used, kept for the baseline."""

    for character in reversed(surface):
        if character in SHORT_VOWELS:
            return character
        if character == SUKUN:
            return SUKUN
    return None


def measure(
    population: list[Row], split: str
) -> tuple[CaseReadoutMeasurement, Counter[str]]:
    correct = wrong = untestable = 0
    genera: Counter[str] = Counter()
    for _key, surface, case in population:
        reading = read_surface_case(surface)
        if reading.readout is CaseReadout.متعذّر_القياس:
            untestable += 1
            genera["untestable:" + reading.genus.value] += 1
            continue
        if reading.readout is GOLD_CASE_READOUT[case]:
            correct += 1
        else:
            wrong += 1
            genera["wrong:" + reading.genus.value + "->" + case] += 1
    measurement = CaseReadoutMeasurement(
        witness=QURANIC_ARABIC_CORPUS_WITNESS,
        split=split,
        normalization_form=NORMALIZATION_FORM,
        unicode_database_version=unicodedata.unidata_version,
        population=len(population),
        correct=correct,
        wrong=wrong,
        untestable=untestable,
    )
    return measurement, genera


def report(measurement: CaseReadoutMeasurement, genera: Counter[str]) -> None:
    print(
        f"[{measurement.split}] population={measurement.population} "
        f"decided={measurement.decided} untestable={measurement.untestable} "
        f"accuracy_on_decided={measurement.accuracy_on_decided:.4f} "
        f"untestable_share={measurement.untestable_share:.4f}"
    )
    for name, count in genera.most_common(8):
        print(f"    {name}: {count}")


def matches(left: CaseReadoutMeasurement, right: CaseReadoutMeasurement) -> bool:
    return (
        left.population == right.population
        and left.correct == right.correct
        and left.wrong == right.wrong
        and left.untestable == right.untestable
    )


def collect(
    words: OrderedDict[Key, tuple[str, tuple[str, ...]]],
) -> tuple[list[Row], int, int]:
    """Return the cased next-words, and the as-stated hypothesis's own counts."""

    keys = list(words)
    following: list[Row] = []
    predicted = matched = 0
    for index, key in enumerate(keys):
        _form, features = words[key]
        if not is_perfect_verb(features) or index + 1 >= len(keys):
            continue
        next_key = keys[index + 1]
        if next_key[:2] != key[:2]:
            continue
        surface, next_features = words[next_key]
        case = gold_case(next_features)
        if final_short_vowel(surface) in {FATHA, FATHATAN}:
            predicted += 1
            if case == "ACC":
                matched += 1
        if case is not None:
            following.append((next_key, surface, case))
    return following, predicted, matched


def main() -> int:
    parser = argparse.ArgumentParser(description="re-derive the frozen numbers")
    parser.add_argument("corpus_path", type=Path)
    parser.add_argument("--allow-unfrozen-input", action="store_true")
    args = parser.parse_args()

    raw = args.corpus_path.read_bytes()
    digest = hashlib.sha256(raw).hexdigest()
    witness = QURANIC_ARABIC_CORPUS_WITNESS
    if digest != witness.sha256 or len(raw) != witness.byte_length:
        message = (
            f"{args.corpus_path} has sha256 {digest} and {len(raw)} bytes; the "
            f"frozen witness is {witness.sha256} with {witness.byte_length} bytes"
        )
        if not args.allow_unfrozen_input:
            print(f"error: {message}", file=sys.stderr)
            return 1
        print(f"warning: {message}", file=sys.stderr)

    following, predicted, matched = collect(load_words(args.corpus_path))
    print(
        f"[as-stated hypothesis] predicted={predicted} accusative_in_gold="
        f"{matched} precision={matched / max(1, predicted):.4f}"
    )
    outcomes = [
        predicted == AS_STATED_HYPOTHESIS_BASELINE.predicted_positive
        and matched == AS_STATED_HYPOTHESIS_BASELINE.accusative_in_gold
    ]
    development = [row for row in following if development_split_contains(row[0][0])]
    held_out = [row for row in following if not development_split_contains(row[0][0])]
    for population, frozen in (
        (development, DEVELOPMENT_SPLIT_MEASUREMENT),
        (held_out, HELD_OUT_SPLIT_MEASUREMENT),
        (following, WHOLE_CORPUS_MEASUREMENT),
    ):
        measurement, genera = measure(population, frozen.split)
        report(measurement, genera)
        outcomes.append(matches(measurement, frozen))

    if all(outcomes):
        print("all frozen numbers re-derived from the corpus")
        return 0
    print("error: re-derived numbers differ from the frozen record", file=sys.stderr)
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
