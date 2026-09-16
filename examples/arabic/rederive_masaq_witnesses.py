"""Re-derive, in one pass, every MASAQ figure deposited in this tree.

MASAQ is CC BY 3.0 — the first witness in this tree whose licence permits
vendoring, unlike the Quranic Arabic Corpus (GPL) and the Tanzil text it embeds
(CC BY-ND). The bytes are read from ``corpora/MASAQ.csv`` when they are there,
with the attribution its licence requires recorded in ``corpora/README.md``.
Bytes held elsewhere are passed instead::

    ALGHANEM_MASAQ_PATH=/path/to/MASAQ.csv \\
        python examples/arabic/rederive_masaq_witnesses.py

The resolution order is the explicit argument, then that variable, then the
tree; no fourth location is guessed.

Every figure is matched against the byte length and the SHA-256 **before** it
is produced, and every figure carries the counting rule that produced it. A
mismatch exits non-zero: a figure that drifts is printed as ``DRIFT``, not
quietly refreshed to whatever the bytes now say.

What this script does **not** do: it adopts no figure, issues no verdict, joins
no corpus to another, and imports nothing from ``alghanem.kernel``. MASAQ has
**no root column**, so linking it to QAC or to Maqāyīs is positional
``(sura, verse, word)``, not by root — and that is exactly where an alignment
measurement fell from 23.3% to 0.3% once. No cross-corpus figure is re-derived
here; every figure below is a count inside one corpus.

This script caught a real defect on its first run. ``embedded_newline_records``
re-derived as 0 against a deposited 154. The cause was in the re-derivation
function, not in the deposit: ``splitlines()`` had already split the embedded
newlines before ``csv.reader`` saw them, so no field contained one. It is read
through ``io.StringIO`` for that reason, and a named test prevents the return.
"""

from __future__ import annotations

import sys

from alghanem.arabic.masaq_corpus_deposit import (
    MASAQ_ATTRIBUTION,
    MASAQ_PATH_VARIABLE,
    MASAQ_REDERIVED_FIGURES,
    MASAQ_RELATIVE_PATH,
    MasaqDepositError,
    lines_are_conserved,
    read_masaq_bytes,
)


def main() -> int:
    try:
        data = read_masaq_bytes()
    except MasaqDepositError as error:
        print(f"error: {error}", file=sys.stderr)
        print(
            f"place the MASAQ.csv whose digest is deposited in "
            f"{MASAQ_RELATIVE_PATH}, or set {MASAQ_PATH_VARIABLE} to it",
            file=sys.stderr,
        )
        return 2

    print(MASAQ_ATTRIBUTION)
    print("(attribution is a licence condition, not a courtesy)")
    print()

    failures: list[str] = []
    for figure in MASAQ_REDERIVED_FIGURES:
        derived = figure.rederive(data)
        holds = derived == figure.deposited
        print(f"  [{'ok' if holds else 'DRIFT'}] {figure.name}: {derived!r}")
        print(f"         rule: {figure.counting_rule}")
        print(f"         limit: {figure.what_it_does_not_establish}")
        if not holds:
            failures.append(f"{figure.name}: deposited {figure.deposited!r}")
    print()

    conserved = lines_are_conserved(data)
    print(
        f"  [{'ok' if conserved else 'DRIFT'}] every line accounted for: "
        "1 header + records + embedded line breaks"
    )
    print(
        "         limit: a conservation audit proves every segment received an "
        "account, not that the account is right"
    )
    print()
    if not conserved:
        failures.append(
            "line conservation: the header, the records and the embedded line "
            "breaks no longer exhaust the lines"
        )

    if failures:
        print(f"error: {len(failures)} figure(s) drifted: {failures}", file=sys.stderr)
        return 1
    print(f"{len(MASAQ_REDERIVED_FIGURES)} figures re-derived from the deposited bytes")
    print("this script adopts nothing and deposits no cross-corpus figure")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
