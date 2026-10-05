"""Check, before ``git add``, that this tree can actually receive MASAQ's bytes.

The deposit of ``corpora/MASAQ.csv`` has failed twice in this repository, each
time silently in its own way: once as an upload that landed under an unintended
name (``Masaq cor``), and once as a commit whose message announced a deposit it
did not carry. Both left the tree asserting a presence it did not hold.

This script asks the three questions that must all be answered before the bytes
are staged, and answers them from the tree itself rather than from prose::

    python examples/arabic/check_masaq_deposit_readiness.py /path/to/MASAQ.csv

With no argument it resolves the path exactly as ``masaq_path()`` does — the
argument, then ``ALGHANEM_MASAQ_PATH``, then the sanctioned in-tree place — so
this script introduces no fourth way of finding the file.

The three questions:

1. **Is the sanctioned place free?** ``corpora/`` may hold only ``README.md``
   and ``MASAQ.csv``; anything else is caught by ``unsanctioned_deposit_files``
   under ``AFailedUploadIsNotADeposit``.
2. **Can the path receive a file at all?** An ignore rule matching
   ``corpora/MASAQ.csv`` would make ``git add`` succeed while staging nothing.
   No such rule exists today, and a named test keeps it that way; this checks
   the working tree in front of you, which may not be that tree.
3. **Are these the deposited bytes?** The byte length and the SHA-256 are
   matched together by ``read_masaq_bytes``, which is the one authority for
   that rule — this script re-implements neither.

What a pass does **not** establish: that the bytes are correct Arabic, that any
figure re-derives, or that the deposit is licensed by anything other than the
CC BY 3.0 already recorded. It establishes that staging the file will do what
staging it appears to do. Re-deriving the figures is the separate job of
``rederive_masaq_witnesses.py``, and a pass here is not a substitute for it.
"""

from __future__ import annotations

import sys

from alghanem.arabic.masaq_corpus_deposit import (
    A_FAILED_UPLOAD_IS_NOT_A_DEPOSIT_NOTE,
    AN_IGNORED_PATH_CANNOT_RECEIVE_A_DEPOSIT_NOTE,
    MASAQ_ATTRIBUTION,
    MASAQ_BYTE_LENGTH,
    MASAQ_RELATIVE_PATH,
    MASAQ_SHA256,
    MasaqDepositError,
    deposit_path_ignore_rule,
    masaq_path,
    read_masaq_bytes,
    unsanctioned_deposit_files,
)


def main(argv: list[str] | None = None) -> int:
    arguments = sys.argv[1:] if argv is None else argv
    if len(arguments) > 1:
        print("usage: check_masaq_deposit_readiness.py [PATH]", file=sys.stderr)
        return 2
    candidate = arguments[0] if arguments else None

    print(MASAQ_ATTRIBUTION)
    print("(attribution is a licence condition, not a courtesy)")
    print()

    blocked: list[str] = []

    strangers = unsanctioned_deposit_files()
    if strangers:
        names = ", ".join(path.name for path in strangers)
        print(f"  [BLOCK] the deposit place holds unsanctioned files: {names}")
        print(f"          {A_FAILED_UPLOAD_IS_NOT_A_DEPOSIT_NOTE}")
        blocked.append("the deposit place is not clean")
    else:
        print("  [ok] the deposit place holds nothing unsanctioned")

    try:
        rule = deposit_path_ignore_rule()
    except MasaqDepositError as error:
        print(f"  [BLOCK] the ignore rules could not be read: {error}")
        blocked.append("the ignore rules could not be read")
    else:
        if rule is None:
            print(f"  [ok] no ignore rule matches {MASAQ_RELATIVE_PATH}")
        else:
            print(f"  [BLOCK] an ignore rule matches the deposit path: {rule}")
            print(f"          {AN_IGNORED_PATH_CANNOT_RECEIVE_A_DEPOSIT_NOTE}")
            blocked.append("the deposit path is ignored")

    resolved = None
    try:
        resolved = masaq_path(candidate)
        read_masaq_bytes(candidate)
    except MasaqDepositError as error:
        where = f"{resolved}: " if resolved is not None else ""
        print(f"  [BLOCK] {where}{error}")
        blocked.append(
            "the bytes do not match" if resolved is not None else "no path resolved"
        )
    else:
        print(f"  [ok] {resolved} matches the deposited length and digest")
        print(f"       length: {MASAQ_BYTE_LENGTH}")
        print(f"       sha256: {MASAQ_SHA256}")
    print()

    if blocked:
        print(f"error: not ready to deposit: {blocked}", file=sys.stderr)
        return 1
    print(f"ready: staging {MASAQ_RELATIVE_PATH} will deposit these exact bytes")
    print("this check adopts no figure and re-derives none")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
