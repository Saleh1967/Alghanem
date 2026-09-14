"""Re-derive the UD objecthood measurement from the PADT files themselves.

This script is reference material, not part of the kernel or the Arabic layer.
It derives no kernel object, licenses no transition, and asserts no Arabic
cardinality. It runs the claim exactly as the frozen pre-registration in
``src/alghanem/arabic/ud_objecthood_preregistration.py`` states it — a word
immediately following a perfect verb whose last short vowel is a fatḥa is
predicted to be a direct object — and compares that prediction against the
treebank's own ``obj`` relation.

Every number frozen in ``src/alghanem/arabic/ud_objecthood_measurement.py`` is
recomputed here and any drift exits non-zero: the population, the four
positional counts, the objects present in the population, and the split of the
errors into function words and content words. The reading of the vowel and the
decision threshold are imported, never re-implemented, so this script cannot
quietly measure a different claim than the one that was pre-registered.

The treebank bytes are deliberately not vendored. UD_Arabic-PADT is
CC BY-NC-SA 3.0; that non-commercial condition follows the bytes. Obtain the
exact files named in the pre-registration, put them in one directory under
their recorded file names, then::

    python examples/irab/measure_ud_objecthood.py path/to/directory

Each file's recorded SHA-256 and byte length are verified first, and the script
refuses to report numbers for any other bytes.

Sources: Universal Dependencies, https://github.com/UniversalDependencies —
UD_Arabic-PADT derives from the Prague Arabic Dependency Treebank,
http://ufal.mff.cuni.cz/padt/. These attributions are conditions of the licence
above, not courtesies.
"""

from __future__ import annotations

import argparse
import hashlib
import sys
from dataclasses import dataclass
from pathlib import Path

from alghanem.arabic.ud_objecthood_measurement import (
    DEVELOPMENT_SPLIT_OBJECTHOOD_MEASUREMENT,
    FUNCTION_WORD_UPOS_TAGS,
    HELD_OUT_SPLIT_OBJECTHOOD_MEASUREMENT,
    ObjecthoodMeasurement,
    predicts_object,
)
from alghanem.arabic.ud_objecthood_preregistration import OBJECTHOOD_PREREGISTRATION

_PERFECT_ASPECT = "Aspect=Perf"
_VERB_UPOS = "VERB"
_VFORM_KEY = "Vform="


@dataclass(frozen=True, slots=True)
class PositionCensus:
    """What the bytes say about the positions the claim speaks about."""

    population: int
    predicted_and_is_object: int
    predicted_and_is_not_object: int
    unreadable_positions: int
    readable_but_not_predicted: int
    objects_in_population: int
    function_word_errors: int
    content_word_errors: int


def _sentences(text: str) -> list[list[list[str]]]:
    sentences: list[list[list[str]]] = []
    current: list[list[str]] = []
    for raw_line in text.split("\n"):
        line = raw_line.rstrip("\r")
        if not line:
            if current:
                sentences.append(current)
                current = []
            continue
        if line.startswith("#"):
            continue
        columns = line.split("\t")
        if len(columns) != 10:
            continue
        token_id = columns[0]
        if "-" in token_id or "." in token_id:
            continue
        current.append(columns)
    if current:
        sentences.append(current)
    return sentences


def _vocalized_form(misc: str) -> str | None:
    for part in misc.split("|"):
        if part.startswith(_VFORM_KEY):
            return part[len(_VFORM_KEY) :]
    return None


def census_positions(text: str) -> PositionCensus:
    """Count the pre-registered positions without adding a rule to the claim."""

    population = 0
    hit = miss = unreadable = not_predicted = objects = 0
    function_errors = content_errors = 0
    for sentence in _sentences(text):
        for index in range(1, len(sentence)):
            previous = sentence[index - 1]
            if previous[3] != _VERB_UPOS:
                continue
            if _PERFECT_ASPECT not in previous[5].split("|"):
                continue
            columns = sentence[index]
            population += 1
            is_object = (
                columns[7].split(":")[0] == OBJECTHOOD_PREREGISTRATION.gold_relation
            )
            objects += int(is_object)
            vocalized = _vocalized_form(columns[9])
            predicted = predicts_object(vocalized) if vocalized is not None else None
            if predicted is None:
                unreadable += 1
            elif not predicted:
                not_predicted += 1
            elif is_object:
                hit += 1
            else:
                miss += 1
                if columns[3] in FUNCTION_WORD_UPOS_TAGS:
                    function_errors += 1
                else:
                    content_errors += 1
    return PositionCensus(
        population=population,
        predicted_and_is_object=hit,
        predicted_and_is_not_object=miss,
        unreadable_positions=unreadable,
        readable_but_not_predicted=not_predicted,
        objects_in_population=objects,
        function_word_errors=function_errors,
        content_word_errors=content_errors,
    )


def _compare(frozen: ObjecthoodMeasurement, measured: PositionCensus) -> list[str]:
    drifts: list[str] = []
    for label in (
        "population",
        "predicted_and_is_object",
        "predicted_and_is_not_object",
        "unreadable_positions",
        "readable_but_not_predicted",
        "objects_in_population",
        "function_word_errors",
        "content_word_errors",
    ):
        recorded = getattr(frozen, label)
        found = getattr(measured, label)
        if recorded != found:
            drifts.append(f"{label}: recorded {recorded}, measured {found}")
    return drifts


def main() -> int:
    parser = argparse.ArgumentParser(
        description="re-derive the pre-registered objecthood measurement"
    )
    parser.add_argument("treebank_directory", type=Path)
    parser.add_argument("--allow-unfrozen-input", action="store_true")
    args = parser.parse_args()

    print(f"pre-registration digest: {OBJECTHOOD_PREREGISTRATION.content_digest}")
    ok = True
    for frozen in (
        DEVELOPMENT_SPLIT_OBJECTHOOD_MEASUREMENT,
        HELD_OUT_SPLIT_OBJECTHOOD_MEASUREMENT,
    ):
        path = args.treebank_directory / frozen.witness.measured_path
        if not path.is_file():
            print(f"error: {path} is missing", file=sys.stderr)
            ok = False
            continue
        raw = path.read_bytes()
        digest = hashlib.sha256(raw).hexdigest()
        if digest != frozen.witness.sha256 or len(raw) != frozen.witness.byte_length:
            message = (
                f"{path} has sha256 {digest} and {len(raw)} bytes; the frozen "
                f"witness is {frozen.witness.sha256} with "
                f"{frozen.witness.byte_length} bytes"
            )
            if not args.allow_unfrozen_input:
                print(f"error: {message}", file=sys.stderr)
                ok = False
                continue
            print(f"warning: {message}", file=sys.stderr)

        measured = census_positions(raw.decode("utf-8"))
        print(
            f"[{frozen.split}] population={measured.population} "
            f"hit={measured.predicted_and_is_object} "
            f"miss={measured.predicted_and_is_not_object} "
            f"unreadable={measured.unreadable_positions} "
            f"not_predicted={measured.readable_but_not_predicted} "
            f"objects={measured.objects_in_population} "
            f"function_word_errors={measured.function_word_errors} "
            f"content_word_errors={measured.content_word_errors} "
            f"precision={frozen.precision_on_decided:.4f} "
            f"recall={frozen.recall_over_objects:.4f} "
            f"decision={frozen.decision.value}"
        )
        drifts = _compare(frozen, measured)
        for drift in drifts:
            print(f"    drift: {drift}", file=sys.stderr)
        ok = ok and not drifts

    if ok:
        print("all frozen objecthood numbers re-derived from the treebank files")
        return 0
    print("error: re-derived numbers differ from the frozen record", file=sys.stderr)
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
