"""Re-derive every frozen compression figure from the corpus bytes themselves.

This script is reference material, not part of the kernel or the Arabic layer.
It derives no kernel object, licenses no transition, and asserts nothing about
Arabic. It prints the SHA-256 of the bytes it was handed before anything else,
refuses to report a single number for any other bytes, and exits non-zero if
any frozen figure drifts.

The corpus bytes are deliberately not vendored: what is frozen in
``src/alghanem/arabic/compression_model_preregistration.py`` is their length
and digest, so a third party can re-derive the numbers from their own copy
without this tree claiming custody of the text. Run::

    python examples/compression/measure_compression_model.py path/to/corpus.txt

Both sizes are always printed together — the encoded payload and the total
that is actually decodable from scratch, tables included — because the payload
alone is not a file size. The tie-break rule is printed with every table size,
since the payload is invariant under the rule and the table is not.
"""

from __future__ import annotations

import argparse
import hashlib
import sys
import zlib
from pathlib import Path

from alghanem.arabic.compression_model_measurement import (
    FROZEN_ORDER_ONE_MEASUREMENT,
    FROZEN_ORDER_ZERO_MEASUREMENT,
    FROZEN_ZLIB_REFERENCE_BYTES,
    ModelMeasurement,
    measure_order_one,
    measure_order_zero,
)
from alghanem.arabic.compression_model_preregistration import (
    FROZEN_CORPUS,
    PREREGISTRATION_DIGEST,
    TieBreakRule,
)
from alghanem.arabic.compression_model_revision_audit import (
    SUPERSEDED_COMPRESSION_CLAIMS,
)


def _report(measured: ModelMeasurement, frozen: ModelMeasurement) -> bool:
    payload_line, total_line = measured.as_two_sizes()
    print(f"  {measured.model} [{measured.tie_break.name}]")
    print(f"    {payload_line}")
    print(f"    {total_line}")
    print(f"    table {measured.table_bits:,} bits, alphabet {measured.alphabet_size}")
    drift = (
        measured.payload_bits != frozen.payload_bits
        or measured.table_bits != frozen.table_bits
        or measured.alphabet_size != frozen.alphabet_size
    )
    if drift:
        print(
            f"    DRIFT: frozen payload {frozen.payload_bits:,} bits, "
            f"table {frozen.table_bits:,} bits, alphabet {frozen.alphabet_size}"
        )
    return drift


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("corpus", type=Path, help="the frozen corpus file")
    arguments = parser.parse_args(argv)

    data = arguments.corpus.read_bytes()
    print("SHA-256 (raw bytes) :", hashlib.sha256(data).hexdigest())
    print("byte length         :", len(data))
    print("frozen digest       :", FROZEN_CORPUS.sha256_hex)
    print("preregistration     :", PREREGISTRATION_DIGEST)
    print()

    if hashlib.sha256(data).hexdigest() != FROZEN_CORPUS.sha256_hex:
        print(
            "refused: these are not the frozen bytes, and a number reported for "
            "other bytes is a number about something else"
        )
        return 2

    drifted = False
    print("frozen tie-break rule:")
    drifted |= _report(measure_order_zero(data), FROZEN_ORDER_ZERO_MEASUREMENT)
    drifted |= _report(measure_order_one(data), FROZEN_ORDER_ONE_MEASUREMENT)

    print()
    print("minimal-table tie-break rule (payload must be identical):")
    for measure, frozen in (
        (measure_order_zero, FROZEN_ORDER_ZERO_MEASUREMENT),
        (measure_order_one, FROZEN_ORDER_ONE_MEASUREMENT),
    ):
        minimal = measure(data, TieBreakRule.MINIMAL_TABLE)
        payload_line, total_line = minimal.as_two_sizes()
        print(f"  {minimal.model} [{minimal.tie_break.name}]")
        print(f"    {payload_line}")
        print(f"    {total_line}")
        print(f"    table {minimal.table_bits:,} bits")
        if minimal.payload_bits != frozen.payload_bits:
            print("    DRIFT: the payload is not invariant under the tie-break")
            drifted = True
        if minimal.table_bits > frozen.table_bits:
            print("    DRIFT: the minimal-table rule produced a larger table")
            drifted = True

    reference = len(zlib.compress(data, 9))
    print()
    print(
        f"external reference zlib -9: {reference:,} bytes = "
        f"{100.0 * (1.0 - reference / len(data)):.4f}% (a ceiling, not a model here)"
    )
    if reference != FROZEN_ZLIB_REFERENCE_BYTES:
        print(f"    DRIFT: frozen reference {FROZEN_ZLIB_REFERENCE_BYTES:,} bytes")
        drifted = True

    print()
    print("superseded figures kept on the record:")
    for claim in SUPERSEDED_COMPRESSION_CLAIMS:
        print(f"  {claim.superseded_figure} -> {claim.corrected_figure}")

    return 1 if drifted else 0


if __name__ == "__main__":
    sys.exit(main())
