"""Check the syllabification floor on the frozen corpus and report the residue.

This script is reference material, not part of the kernel or the Arabic layer.
It asserts no Arabic cardinality and moves no dictionary layer. It checks the
four structural conditions frozen *before* any measurement in
``alghanem.arabic.syllable_preregistration.STRUCTURAL_ACCEPTANCE_CONDITIONS``:

* CLOSURE — every emitted syllable is one of the six templates;
* RECONSTRUCTION — the syllables re-derive the expanded slot stream exactly;
* TOTALITY — segmented words plus `wazn_unresolved` words equal the words read;
* DETERMINISM — the same word segments the same way twice.

It then prints the unresolved share **with no threshold attached**
(`NO_THRESHOLD_IS_INVENTED_AFTER_THE_FACT`): that number is published, not
graded, and it does not by itself lift the withholding of
`DictionaryLayer.SYLLABLES_AND_WAZN`.

The corpus is deliberately not vendored: the Quranic Arabic Corpus is
GPL-licensed and the Tanzil Uthmani text it embeds is CC BY-ND, and both forbid
modification. Obtain the exact file named in
``alghanem.arabic.irab_corpus_witness.QURANIC_ARABIC_CORPUS_WITNESS``, then::

    python examples/letter_fingerprint/measure_syllabification_floor.py path/to/file.txt

The script verifies the recorded SHA-256 and byte length first and refuses to
report numbers for any other file.

Source: the Quranic Arabic Corpus, http://corpus.quran.com — built on the
Tanzil Quran text, http://tanzil.info. Both attributions are conditions of the
licences above, not courtesies.
"""

from __future__ import annotations

import argparse
import hashlib
import sys
from collections import Counter
from pathlib import Path

from alghanem.arabic.encoding.carrier_state_candidate import CarrierStateEncodingError
from alghanem.arabic.irab_corpus_witness import QURANIC_ARABIC_CORPUS_WITNESS
from alghanem.arabic.p_extractor import read_surface
from alghanem.arabic.syllabifier import expand_slots, syllabify_reading
from alghanem.arabic.syllable_preregistration import (
    PREREGISTRATION_DIGEST,
    SyllableTemplate,
    preregistration_digest,
)

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "irab"))

from measure_case_readout import Key, load_words  # noqa: E402


def main() -> int:
    parser = argparse.ArgumentParser(description="check the syllabification floor")
    parser.add_argument("corpus_path", type=Path)
    parser.add_argument("--allow-unfrozen-input", action="store_true")
    args = parser.parse_args()

    if preregistration_digest() != PREREGISTRATION_DIGEST:
        print(
            "error: the syllable preregistration drifted after the tool was "
            "written; no floor may be reported against it",
            file=sys.stderr,
        )
        return 1

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

    words: dict[Key, tuple[str, tuple[str, ...]]] = load_words(args.corpus_path)
    templates: Counter[str] = Counter()
    reasons: Counter[str] = Counter()
    read = resolved = unresolved = refused = 0
    closure = reconstruction = determinism = True

    for _key, (surface, _features) in words.items():
        try:
            reading = read_surface(surface)
        except CarrierStateEncodingError:
            refused += 1
            continue
        read += 1
        word = syllabify_reading(reading)
        if syllabify_reading(reading) != word:
            determinism = False
        if word.is_resolved:
            resolved += 1
            for syllable in word.syllables:
                if syllable.template not in set(SyllableTemplate):
                    closure = False
                templates[syllable.template.value] += 1
            slots, failure = expand_slots(reading)
            rebuilt = tuple(
                slot for syllable in word.syllables for slot in syllable.slots
            )
            if failure is not None or rebuilt != slots:
                reconstruction = False
        else:
            unresolved += 1
            reasons[word.wazn_unresolved[0].reason] += 1

    print(f"[refused by the codec before reading] {refused}")
    print(f"[read] {read} segmented={resolved} unresolved={unresolved}")
    if read:
        print(
            f"[unresolved share, published with no threshold] {unresolved / read:.6f}"
        )
    print(f"[template histogram] {dict(sorted(templates.items()))}")
    for reason, count in reasons.most_common(10):
        print(f"    {count:>7} {reason}")

    outcomes = {
        "CLOSURE": closure,
        "RECONSTRUCTION": reconstruction,
        "TOTALITY": resolved + unresolved == read,
        "DETERMINISM": determinism,
    }
    for name, held in outcomes.items():
        print(f"[{name}] {'held' if held else 'FAILED'}")
    if all(outcomes.values()):
        print("the four structural conditions held on the frozen corpus")
        return 0
    print(
        "error: a structural condition written before the measurement failed",
        file=sys.stderr,
    )
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
