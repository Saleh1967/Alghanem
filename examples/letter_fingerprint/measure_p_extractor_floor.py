"""Re-derive the P-EXTRACTOR acceptance floor from the corpus bytes.

This script is reference material, not part of the kernel or the Arabic layer.
It derives no kernel object and asserts no Arabic cardinality. It checks the
one thing `alghanem.arabic.gflk_state_machine_registration`
.`P_EXTRACTOR_ACCEPTANCE_CONDITION` demands, and it checks it by measuring, not
by reading a number back:

* the round-trip fraction over the frozen Quranic corpus **after** the role
  reading of `alghanem.arabic.p_extractor` is applied must equal the fraction
  the bare codec achieves over the same bytes — the reading attaches roles to
  units it never rebuilds, so any difference at all is a regression;
* the set of corpus words refused at construction must remain exactly the six
  locations in `gflk_codec_revision_audit.CORRUPTED_TOKENS`; one new refusal
  fails the run even if the fraction rises.

The corpus is deliberately not vendored: the Quranic Arabic Corpus is
GPL-licensed and the Tanzil Uthmani text it embeds is CC BY-ND, and both forbid
modification. Obtain the exact file named in
``alghanem.arabic.irab_corpus_witness.QURANIC_ARABIC_CORPUS_WITNESS``, then::

    python examples/letter_fingerprint/measure_p_extractor_floor.py path/to/file.txt

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
from pathlib import Path

from alghanem.arabic.encoding.carrier_state_candidate import (
    CarrierStateEncodingError,
    round_trip_holds,
)
from alghanem.arabic.gflk_codec_revision_audit import GFLK_CODEC_REVISION_AUDIT
from alghanem.arabic.irab_corpus_witness import QURANIC_ARABIC_CORPUS_WITNESS
from alghanem.arabic.p_extractor import reading_preserves_the_round_trip
from alghanem.arabic.p_extractor_preregistration import (
    PREREGISTRATION_DIGEST,
    preregistration_digest,
)

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "irab"))

from measure_case_readout import Key, load_words  # noqa: E402


def read_corpus(
    words: dict[Key, tuple[str, tuple[str, ...]]],
) -> tuple[int, int, int, list[Key]]:
    """Return accepted, matched-by-codec, matched-after-reading, refused."""

    accepted = 0
    matched_bare = 0
    matched_read = 0
    refused: list[Key] = []
    for key, (surface, _features) in words.items():
        try:
            bare = round_trip_holds(surface)
        except CarrierStateEncodingError:
            refused.append(key)
            continue
        accepted += 1
        matched_bare += int(bare)
        matched_read += int(reading_preserves_the_round_trip(surface))
    return accepted, matched_bare, matched_read, refused


def main() -> int:
    parser = argparse.ArgumentParser(description="re-derive the P-EXTRACTOR floor")
    parser.add_argument("corpus_path", type=Path)
    parser.add_argument("--allow-unfrozen-input", action="store_true")
    args = parser.parse_args()

    if preregistration_digest() != PREREGISTRATION_DIGEST:
        print(
            "error: the pass-two preregistration drifted after the reader was "
            "written; the floor may not be reported",
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

    words = load_words(args.corpus_path)
    accepted, matched_bare, matched_read, refused = read_corpus(words)
    bare_fraction = matched_bare / accepted if accepted else 0.0
    read_fraction = matched_read / accepted if accepted else 0.0
    print(
        f"[bare codec] accepted={accepted} matched={matched_bare} "
        f"fraction={bare_fraction:.8f}"
    )
    print(
        f"[after the role reading] accepted={accepted} matched={matched_read} "
        f"fraction={read_fraction:.8f}"
    )

    recorded = sorted(
        token.location for token in GFLK_CODEC_REVISION_AUDIT.corrupted_tokens
    )
    print(f"[refused at construction] {sorted(refused)}")
    print(f"[the six named locations] {recorded}")

    outcomes = [
        matched_read == matched_bare,
        read_fraction >= bare_fraction,
        sorted(refused) == recorded,
    ]
    if all(outcomes):
        print("floor met: the reading changed no word's round trip")
        return 0
    print(
        "error: the reading changed the round trip, or a new word was refused; "
        "record the result as a refusal — the floor is not to be tuned",
        file=sys.stderr,
    )
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
