"""Measure the Maqāyīs/QAC root overlap at every declared normalisation stage.

This script is reference material, not part of the kernel or the Arabic layer.
It derives no kernel object, licenses no transition, and asserts no Arabic
cardinality. It prints each arriving figure beside the counting rule that would
produce it and the number this tree actually derives, and exits non-zero on any
drift.

The Maqāyīs side is measured from bytes already in this tree
(``maqayis_by_root_csv_999.csv``, length and digest re-checked on every read).
The corpus side is deliberately **not** vendored: the Quranic Arabic Corpus is
GPL-licensed and the Tanzil Uthmani text it embeds is CC BY-ND, and both forbid
modification. Obtain the exact file named in
``alghanem.arabic.irab_corpus_witness.QURANIC_ARABIC_CORPUS_WITNESS``, then::

    python examples/irab/measure_maqayis_qac_root_overlap.py path/to/morphology-0.4.txt

Two things are printed that no single number can carry. First the **root
alphabet of the corpus's own ``ROOT`` field, untransliterated**: whether the six
Buckwalter hamza characters occur there at all is the observation that decides
between the two frozen diagnoses of the 328-root reverse gap — a broken
transliteration in the sender's tool, or a corpus convention that unifies hamza
before we ever see it. Second, **all six stages together**, with the fusions each
stage caused: normalisation changes the number, and a number printed only after
normalisation hides the rule that made it.

Source: the Quranic Arabic Corpus, http://corpus.quran.com — built on the
Tanzil Quran text, http://tanzil.info. Both attributions are conditions of the
licences above, not courtesies.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from alghanem.arabic.hollow_root_root_census import HollowRootCensusError
from alghanem.arabic.irab_corpus_witness import QURANIC_ARABIC_CORPUS_WITNESS
from alghanem.arabic.maqayis_qac_root_overlap_census import (
    OverlapCensusError,
    OverlapReadout,
    maqayis_roots,
    maqayis_trilateral_roots,
    overlap_readouts,
    qac_root_alphabet,
    qac_roots,
    readout_at,
    stage_fusions,
)
from alghanem.arabic.maqayis_qac_root_overlap_preregistration import (
    ARRIVING_OVERLAP_FIGURES,
    HAMZA_DIAGNOSIS_HYPOTHESES,
    OVERLAP_PREREGISTRATION_DIGEST,
    OVERLAP_STAGES,
    STANDING,
    FigureStanding,
    figure_by_label,
)
from alghanem.arabic.maqayis_root_table_deposit import MaqayisRootTableError

ALPHABET_PREVIEW = 12


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "corpus",
        type=Path,
        help="path to the exact quranic-corpus-morphology-0.4.txt bytes",
    )
    arguments = parser.parse_args(argv)

    witness = QURANIC_ARABIC_CORPUS_WITNESS
    print(f"preregistration digest: {OVERLAP_PREREGISTRATION_DIGEST}")
    print(f"standing: {STANDING.value}")
    print(f"corpus: {witness.corpus} {witness.version}")
    print(f"sha256: {witness.sha256}")
    print("source: http://corpus.quran.com — text: http://tanzil.info")
    print()

    try:
        maqayis = maqayis_roots()
        trilateral = maqayis_trilateral_roots()
        corpus = qac_roots(arguments.corpus)
        alphabet = qac_root_alphabet(corpus)
        readouts = overlap_readouts(maqayis, corpus)
        trilateral_readouts = overlap_readouts(trilateral, corpus)
        fusions = stage_fusions(maqayis, corpus)
    except (MaqayisRootTableError, HollowRootCensusError, OverlapCensusError) as error:
        print(f"refused: {error}", file=sys.stderr)
        return 2

    print("ROOT field alphabet as it is, before any transliteration:")
    for character, count in alphabet.characters[:ALPHABET_PREVIEW]:
        print(f"  {character!r} in {count} roots")
    present = alphabet.hamza_characters_present
    print(f"  hamza characters present: {present if present else 'none'}")
    for hypothesis in HAMZA_DIAGNOSIS_HYPOTHESES:
        print(f"  hypothesis {hypothesis.label}: {hypothesis.what_would_refute_it}")
    print()

    print("stage-by-stage, all six together:")
    for readout in readouts:
        print(
            f"  {readout.stage_name}: maqayis={readout.maqayis_size} "
            f"qac={readout.qac_size} shared={readout.intersection} "
            f"uncovered={readout.maqayis_only} ({readout.uncovered_share:.1%}) "
            f"reverse={readout.qac_only} ({readout.reverse_uncovered_share:.1%})"
        )
    print()

    print("the price each stage charged (distinctions destroyed):")
    for record in fusions:
        print(
            f"  {record.stage_name}: maqayis={record.maqayis_distinctions_lost} "
            f"qac={record.qac_distinctions_lost}"
        )
    print()

    print("arriving figures beside what this tree derives:")
    drifted = False
    derived: dict[str, int] = {
        "جذور_مقاييس": len(maqayis),
        "جذور_مقاييس_الثلاثية": len(trilateral),
        "جذور_المدوَّنة": len(corpus),
    }
    for figure in ARRIVING_OVERLAP_FIGURES:
        value = derived.get(figure.label)
        if value is None:
            matches = sorted(
                stage.name
                for stage in OVERLAP_STAGES
                if _stage_value(
                    trilateral_readouts
                    if figure.label == "غير_المغطّى_الثلاثي"
                    else readouts,
                    stage.name,
                    figure.label,
                )
                == figure.claimed_value
            )
            print(
                f"  {figure.label}: claimed {figure.claimed_value}; "
                f"matched at stages {matches if matches else 'none'}"
            )
            if not matches:
                drifted = True
            continue
        mark = "=" if value == figure.claimed_value else "DRIFT"
        print(
            f"  {figure.label}: claimed {figure.claimed_value}, "
            f"derived {value} {mark}"
        )
        if value != figure.claimed_value:
            drifted = True
    print()

    for label in ("جذور_مقاييس", "جذور_المدوَّنة"):
        figure = figure_by_label(label)
        if figure.standing is FigureStanding.AWAITING_BYTES_NOT_IN_THE_TREE:
            print(f"note: {label} was not checkable from this tree's bytes alone")

    if drifted:
        print(
            "DRIFT: an arriving figure matched no stage under any frozen rule",
            file=sys.stderr,
        )
        return 1

    print("every arriving figure matched at a named stage under its written rule")
    return 0


def _stage_value(
    readouts: tuple[OverlapReadout, ...], stage_name: str, label: str
) -> int:
    """The value a stage gives for one arriving figure, under that figure's rule.

    The trilateral figure is read from a run over the trilateral roots only, not
    sliced out of the all-types run: ``root_type`` is a column in the file, and a
    subset taken after the fact is not the same counting rule.
    """

    readout = readout_at(readouts, stage_name)
    if label == "التقاطع":
        return readout.intersection
    if label in {"غير_المغطّى", "غير_المغطّى_الثلاثي"}:
        return readout.maqayis_only
    return readout.qac_only


if __name__ == "__main__":
    raise SystemExit(main())
