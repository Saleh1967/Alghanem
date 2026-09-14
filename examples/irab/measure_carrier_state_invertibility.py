"""Re-derive the carrier/state invertibility record from the corpus itself.

This script is reference material, not part of the kernel or the Arabic layer.
It derives no kernel object, licenses no transition, and asserts no Arabic
cardinality. It recomputes two things and fails loudly if either drifts:

* `QURANIC_CORPUS_INVERTIBILITY` in
  ``src/alghanem/arabic/encoding/carrier_state_candidate.py`` — what this
  tree's own `CarrierStateCodec` does over the corpus, including the tokens it
  refuses at construction rather than reading (`REFUSAL_IS_NOT_A_ROUND_TRIP`);
* `GFLK_CODEC_REVISION_AUDIT` in
  ``src/alghanem/arabic/gflk_codec_revision_audit.py`` — the six corpus words
  the externally deposited revision corrupts silently, by location and by
  surface.

The deposited revision is deliberately **not** vendored here. Its six
corruptions are recorded as the input and output surfaces of specific corpus
words, so a holder of the corpus bytes re-derives the input side from the
corpus and checks the output side against any copy of that revision.

The corpus is deliberately not vendored either: the Quranic Arabic Corpus is
GPL-licensed and the Tanzil Uthmani text it embeds is CC BY-ND, and both forbid
modification. Obtain the exact file named in
``alghanem.arabic.irab_corpus_witness.QURANIC_ARABIC_CORPUS_WITNESS``, then::

    python examples/irab/measure_carrier_state_invertibility.py path/to/file.txt

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
import unicodedata
from pathlib import Path

from alghanem.arabic.encoding.carrier_state_candidate import (
    QURANIC_CORPUS_INVERTIBILITY,
    CarrierStateEncodingError,
    InvertibilityMeasurement,
    round_trip_holds,
)
from alghanem.arabic.gflk_codec_revision_audit import (
    GFLK_CODEC_REVISION_AUDIT,
    AdoptionOutcome,
)
from alghanem.arabic.irab_corpus_witness import QURANIC_ARABIC_CORPUS_WITNESS

sys.path.insert(0, str(Path(__file__).resolve().parent))

from measure_case_readout import Key, load_words  # noqa: E402


def refused_locations(words: dict[Key, tuple[str, tuple[str, ...]]]) -> list[Key]:
    """The corpus words this tree's codec declines to read at all."""

    refused: list[Key] = []
    for key, (surface, _features) in words.items():
        try:
            round_trip_holds(surface)
        except CarrierStateEncodingError:
            refused.append(key)
    return refused


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

    words = load_words(args.corpus_path)
    measurement = InvertibilityMeasurement.measure(
        (surface for surface, _features in words.values()),
        source_id=QURANIC_CORPUS_INVERTIBILITY.source_id,
        source_sha256=digest,
        source_byte_length=len(raw),
    )
    print(
        f"[tree codec] tokens={measurement.token_total} "
        f"refused={measurement.token_refusals} "
        f"mismatched={measurement.token_mismatches} "
        f"accepted={measurement.accepted_tokens} "
        f"matched_fraction_over_accepted={measurement.matched_fraction:.6f}"
    )

    outcomes = [
        measurement.token_total == QURANIC_CORPUS_INVERTIBILITY.token_total,
        measurement.token_mismatches
        == QURANIC_CORPUS_INVERTIBILITY.token_mismatches,
        measurement.token_refusals == QURANIC_CORPUS_INVERTIBILITY.token_refusals,
        unicodedata.unidata_version
        == QURANIC_CORPUS_INVERTIBILITY.unicode_database_version,
    ]

    audit = GFLK_CODEC_REVISION_AUDIT
    print(
        f"[deposited revision] claimed={audit.claimed_round_trip_fraction:.6f} "
        f"over {audit.claimed_token_total} words; measured="
        f"{audit.measured_round_trip_fraction:.6f} over "
        f"{audit.measured_token_total} words; population_gap="
        f"{audit.token_total_gap}; outcome={audit.outcome.value}"
    )
    outcomes.append(audit.outcome is AdoptionOutcome.ADOPTION_REFUSED)
    outcomes.append(audit.measured_token_total == measurement.token_total)

    refused = refused_locations(words)
    recorded = [token.location for token in audit.corrupted_tokens]
    print(f"[refused at construction] {refused}")
    print(f"[recorded as corrupted by the revision] {recorded}")
    outcomes.append(sorted(refused) == sorted(recorded))

    for token in audit.corrupted_tokens:
        surface, _features = words[token.location]
        same = unicodedata.normalize("NFC", surface) == unicodedata.normalize(
            "NFC", token.surface_in
        )
        print(f"    {token.location} input_matches_corpus={same}")
        outcomes.append(same)

    if all(outcomes):
        print("all frozen numbers re-derived from the corpus")
        return 0
    print("error: re-derived numbers differ from the frozen record", file=sys.stderr)
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
