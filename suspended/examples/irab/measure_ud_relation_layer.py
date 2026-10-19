"""Re-derive the UD Arabic Step-0 census from the treebank files themselves.

This script is reference material, not part of the kernel or the Arabic layer.
It derives no kernel object, licenses no transition, and asserts no Arabic
cardinality. It is **not** a syntactic-function reader: it counts CoNLL-U
columns and nothing else (`STEP_ZERO_IS_NOT_A_READER`).

It recomputes every number frozen in
``src/alghanem/arabic/ud_relation_layer_step0.py`` and fails loudly on drift:
sentence and token totals, how many tokens actually carry a populated HEAD and
DEPREL (as opposed to the format spec merely declaring those columns), how many
carry a surface FORM at all, the ``obj``/``obl``/``nsubj`` totals, and the
accusative-versus-``obj`` split that measures `OBJ_VS_OBL_IS_PARTLY_CASE_DEFINED`
instead of assuming it.

The treebank bytes are deliberately not vendored. UD_Arabic-PADT is
CC BY-NC-SA 3.0, UD_Arabic-PUD is CC BY-SA 3.0, and UD_Arabic-NYUAD licenses
only its annotation, its surface forms having been removed because the
underlying Penn Arabic Treebank text is LDC-licensed. Obtain the exact files
named in ``alghanem.arabic.ud_relation_layer_step0.ARABIC_UD_CENSUSES``, put
them in one directory under their recorded file names, then::

    python examples/irab/measure_ud_relation_layer.py path/to/directory

Each file's recorded SHA-256 and byte length are verified first, and the script
refuses to report numbers for any other bytes.

Sources: Universal Dependencies,
https://github.com/UniversalDependencies — UD_Arabic-PADT derives from the
Prague Arabic Dependency Treebank, http://ufal.mff.cuni.cz/padt/. These
attributions are conditions of the licences above, not courtesies.
"""

from __future__ import annotations

import argparse
import hashlib
import sys
from dataclasses import dataclass
from pathlib import Path

from alghanem.arabic.ud_relation_layer_step0 import (
    ARABIC_UD_CENSUSES,
    UdRelationLayerCensus,
)

_EMPTY_COLUMN = "_"
_ACCUSATIVE_FEATURE = "Case=Acc"


@dataclass(frozen=True, slots=True)
class ColumnCensus:
    """What the bytes of one CoNLL-U file actually contain, column by column."""

    sentences: int
    tokens: int
    head_populated_tokens: int
    deprel_populated_tokens: int
    form_bearing_tokens: int
    obj_tokens: int
    obl_tokens: int
    nsubj_tokens: int
    accusative_tokens: int
    accusative_obj_tokens: int


def census_conllu(text: str) -> ColumnCensus:
    """Count CoNLL-U columns without interpreting a single relation."""

    sentences = tokens = 0
    head_populated = deprel_populated = form_bearing = 0
    obj = obl = nsubj = accusative = accusative_obj = 0
    inside_sentence = False
    for raw_line in text.split("\n"):
        line = raw_line.rstrip("\r")
        if not line:
            if inside_sentence:
                sentences += 1
                inside_sentence = False
            continue
        if line.startswith("#"):
            continue
        columns = line.split("\t")
        if len(columns) != 10:
            continue
        inside_sentence = True
        token_id = columns[0]
        if "-" in token_id or "." in token_id:
            continue
        tokens += 1
        if columns[6] != _EMPTY_COLUMN:
            head_populated += 1
        if columns[7] != _EMPTY_COLUMN:
            deprel_populated += 1
        if columns[1] != _EMPTY_COLUMN:
            form_bearing += 1
        relation = columns[7].split(":")[0]
        if relation == "obj":
            obj += 1
        elif relation == "obl":
            obl += 1
        elif relation == "nsubj":
            nsubj += 1
        if _ACCUSATIVE_FEATURE in columns[5].split("|"):
            accusative += 1
            if relation == "obj":
                accusative_obj += 1
    if inside_sentence:
        sentences += 1
    return ColumnCensus(
        sentences=sentences,
        tokens=tokens,
        head_populated_tokens=head_populated,
        deprel_populated_tokens=deprel_populated,
        form_bearing_tokens=form_bearing,
        obj_tokens=obj,
        obl_tokens=obl,
        nsubj_tokens=nsubj,
        accusative_tokens=accusative,
        accusative_obj_tokens=accusative_obj,
    )


def _compare(frozen: UdRelationLayerCensus, measured: ColumnCensus) -> list[str]:
    drifts: list[str] = []
    for label in (
        "sentences",
        "tokens",
        "head_populated_tokens",
        "deprel_populated_tokens",
        "form_bearing_tokens",
        "obj_tokens",
        "obl_tokens",
        "nsubj_tokens",
        "accusative_tokens",
        "accusative_obj_tokens",
    ):
        recorded = getattr(frozen, label)
        found = getattr(measured, label)
        if recorded != found:
            drifts.append(f"{label}: recorded {recorded}, measured {found}")
    return drifts


def main() -> int:
    parser = argparse.ArgumentParser(description="re-derive the Step-0 census")
    parser.add_argument("treebank_directory", type=Path)
    parser.add_argument("--allow-unfrozen-input", action="store_true")
    args = parser.parse_args()

    ok = True
    for frozen in ARABIC_UD_CENSUSES:
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

        measured = census_conllu(raw.decode("utf-8"))
        print(
            f"[{frozen.treebank}] sentences={measured.sentences} "
            f"tokens={measured.tokens} head={measured.head_populated_tokens} "
            f"deprel={measured.deprel_populated_tokens} "
            f"form={measured.form_bearing_tokens} obj={measured.obj_tokens} "
            f"obl={measured.obl_tokens} nsubj={measured.nsubj_tokens} "
            f"accusative={measured.accusative_tokens} "
            f"accusative_obj={measured.accusative_obj_tokens} "
            f"outcome={frozen.outcome.value}"
        )
        drifts = _compare(frozen, measured)
        for drift in drifts:
            print(f"    drift: {drift}", file=sys.stderr)
        ok = ok and not drifts

    if ok:
        print("all frozen Step-0 numbers re-derived from the treebank files")
        return 0
    print("error: re-derived numbers differ from the frozen record", file=sys.stderr)
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
