"""Re-derive the maṣdar-priority census from MASAQ bytes the holder declares.

This script is reference material, not part of the kernel or the Arabic layer.
It derives no kernel object, licenses no transition, and issues no grammatical
judgement about any root.

Unlike the other scripts in this directory, it cannot verify a witness that is
already deposited in the tree, because **no MASAQ witness is deposited**: only
a SHA-256 arrived, with no byte length, mirror, path, licence or attribution
requirement, and no column binding. Those facts are legislated declarations,
not readings, so the holder of the bytes must supply them on the command line;
they are then printed next to every number, together with the digest of the
binding they came from. See ``MASAQ_DEPOSIT_BARRIERS``.

    python examples/irab/measure_masdar_priority.py MASAQ.csv \\
        --byte-length 12345678 --mirror example.org/mirror \\
        --path-in-mirror MASAQ.csv --version 3 \\
        --upstream https://data.mendeley.com/datasets/9yvrzxktmr \\
        --license "the licence as the file states it" \\
        --attribution-link https://example.org/cite \\
        --declared-by "who read the header" \\
        --location-column ... --form-column ... --tag-column ... \\
        --root-column ... --lemma-column ... --verb-form-column ...

The script verifies the recorded SHA-256 and the declared byte length first and
refuses to report numbers for any other file.

What a run establishes: what this tagging says about maṣdar/form pairs in this
corpus, under the counting rules frozen in
``masdar_priority_preregistration``. What it does not establish: claim (ج).
Both of its barriers are open — the join between two corpora is not
legislated, and no rule turns a tagged maṣdar into a measured transitivity —
so the script prints the barriers instead of a number.

Source: MASAQ, as named by the holder of the bytes on the command line. The
attribution links given are printed as licence conditions, not courtesies.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from alghanem.arabic.masaq_corpus_witness import (
    MASAQ_DEPOSIT_BARRIERS,
    MasaqColumnBinding,
    MasaqWitnessError,
    binding_digest,
    deposit_masaq_witness,
    read_masaq_rows,
)
from alghanem.arabic.masdar_priority_census import (
    MASDAR_CENSUS_NAMED_RESIDUALS,
    MasdarPriorityCensusError,
    discrimination_table,
    masdar_records,
    permutation_test,
    single_root_witness,
)
from alghanem.arabic.masdar_priority_preregistration import (
    ARRIVING_MASDAR_FIGURES,
    LEGISLATION_BARRIERS,
    MASDAR_CLAIMS,
    MASDAR_PRIORITY_PREREGISTRATION_DIGEST,
    STANDING,
)


def _parse_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("corpus", type=Path, help="path to the MASAQ csv file")
    parser.add_argument("--byte-length", type=int, required=True)
    parser.add_argument("--version", required=True)
    parser.add_argument("--upstream", required=True)
    parser.add_argument("--mirror", required=True)
    parser.add_argument("--path-in-mirror", required=True)
    parser.add_argument("--license", action="append", required=True)
    parser.add_argument("--attribution-link", action="append", required=True)
    parser.add_argument(
        "--attribution-requirement",
        default="attribution as the file's own licence states it",
    )
    parser.add_argument(
        "--annotation-note",
        default="one row per morphological segment, tagged by its authors",
    )
    parser.add_argument("--declared-by", required=True)
    parser.add_argument(
        "--binding-assumes",
        default="the column names were read from the file's own header row",
    )
    parser.add_argument("--location-column", required=True)
    parser.add_argument("--form-column", required=True)
    parser.add_argument("--tag-column", required=True)
    parser.add_argument("--root-column", required=True)
    parser.add_argument("--lemma-column", required=True)
    parser.add_argument("--verb-form-column", required=True)
    parser.add_argument("--masdar-tag", action="append", default=None)
    parser.add_argument("--meemi-masdar-tag", action="append", default=None)
    parser.add_argument("--witness-root", default="قوم")
    return parser.parse_args()


def _print_registration() -> None:
    print("التسجيلُ القبْليُّ المُجمَّد")
    print(f"  البصمة: {MASDAR_PRIORITY_PREREGISTRATION_DIGEST}")
    print(f"  المنزلة: {STANDING.value}")
    for claim in MASDAR_CLAIMS:
        print(f"  الدعوى {claim.label}: {claim.statement}")
    print()
    print("الأرقامُ الواردةُ كما وصلت")
    for figure in ARRIVING_MASDAR_FIGURES:
        print(f"  {figure.label}: {figure.claimed_value}  [{figure.corpus}]")
    print()


def _print_barriers() -> None:
    print("الموانعُ القائمة")
    for deposit_barrier in MASAQ_DEPOSIT_BARRIERS:
        print(f"  {deposit_barrier.what_is_blocked}: {deposit_barrier.standing.value}")
    for barrier in LEGISLATION_BARRIERS:
        print(f"  {barrier.what_is_blocked}")
        print(f"    القاعدةُ الناقصة: {barrier.the_rule_that_is_missing}")
        print(f"    ما يرفعها: {barrier.what_lifts_it}")
    print()


def main() -> int:
    arguments = _parse_arguments()
    _print_registration()
    _print_barriers()
    binding = MasaqColumnBinding(
        declared_by=arguments.declared_by,
        what_it_assumes=arguments.binding_assumes,
        location_column=arguments.location_column,
        form_column=arguments.form_column,
        morphological_tag_column=arguments.tag_column,
        root_column=arguments.root_column,
        lemma_column=arguments.lemma_column,
        verb_form_column=arguments.verb_form_column,
        masdar_tag_values=tuple(arguments.masdar_tag or ("GERUND",)),
        meemi_masdar_tag_values=tuple(arguments.meemi_masdar_tag or ("GERUND_MEEM",)),
    )
    witness = deposit_masaq_witness(
        version=arguments.version,
        upstream=arguments.upstream,
        measured_mirror=arguments.mirror,
        measured_path=arguments.path_in_mirror,
        byte_length=arguments.byte_length,
        licenses=arguments.license,
        required_attribution_links=arguments.attribution_link,
        attribution_requirement=arguments.attribution_requirement,
        annotation_note=arguments.annotation_note,
    )
    rows = read_masaq_rows(arguments.corpus, witness, binding)
    records = masdar_records(rows, binding)
    table = discrimination_table(records, binding)
    print("الدعوى (أ) — قوّةُ تمييز المصدر للوزن")
    print(f"  بصمةُ ربط الأعمدة: {binding_digest(binding)}")
    print(f"  جذورٌ لها مصدر: {table.masdar_roots}")
    print(f"  جذورٌ لها أكثرُ من مصدر: {table.roots_with_more_than_one_masdar}")
    print(f"  مصادرُ متمايزة: {table.distinct_masdars}")
    print(f"  منها موسومةُ الوزن: {table.masdars_with_a_tagged_form}")
    print(f"    فصلت وزنًا واحدًا: {table.masdars_separating_one_form}")
    print(f"    اشتركت بين وزنين فأكثر: {table.masdars_shared_between_forms}")
    print(f"  نسبةُ الفصل: {table.separation_rate:.2f}%")
    outcome = permutation_test(records, "فصلُ المصدر للوزن")
    print(
        f"  التبديل: p = {outcome.p_value:.4f}، "
        f"أقصى العدميّ {outcome.maximum_null_rate:.2f}%، "
        f"حجمُ العيّنة {outcome.sample_size}"
    )
    print()
    print(f"الدعوى (ب) — شاهدُ جذرٍ واحدٍ مُسمًّى: {arguments.witness_root}")
    profile = single_root_witness(records, arguments.witness_root)
    for lemma, forms in profile.forms_by_lemma:
        print(f"  {lemma}: {', '.join(forms)}")
    print()
    print("الدعوى (ج) — بلا رقم؛ ومانعاها مطبوعان أعلاه.")
    print()
    print("المُخلَّفاتُ المُسمّاة")
    for name, note in MASDAR_CENSUS_NAMED_RESIDUALS.items():
        print(f"  {name}: {note}")
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except (MasaqWitnessError, MasdarPriorityCensusError) as error:
        print(f"رُفِض القياس: {error}", file=sys.stderr)
        sys.exit(1)
