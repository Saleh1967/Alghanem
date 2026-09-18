"""شغِّل الفركتال تجريبيًّا على بايتات MASAQ الموثَّقة، وأخرِج شواهدَ لا ترخيصًا.

    ALGHANEM_MASAQ_PATH=/path/to/MASAQ.csv \\
        python examples/arabic/run_masaq_fractal_experiment.py --limit 200

تُقرأ البايتاتُ من ``corpora/MASAQ.csv`` إن كانت هناك، وإلّا فمن المتغيّر أعلاه؛
ويُطابَق الطولُ والبصمةُ قبل أن يُقرأ سجلٌّ واحد.

والمُولِّدُ لا يرى إلّا موضعَ الكلمة وصورَ مقاطعها؛ أمّا ``Morph_Tag`` وأخواتُه
فمحجوبةٌ عنه، تُقرأ بعد التشغيل ولا تدخل فيه. ولو نزلت في المدخل لكان المحرِّكُ
يُلقِّن نفسَه جوابَه.

وأقصى ما يُخرِجه هذا التشغيل حزمةُ شواهدَ بلا حكم: لا ``License`` ولا رتبةَ
دائمةٍ ولا ``NextScaleSeed``؛ والبذرةُ الصادرةُ تجريبيّةٌ ينتهي أثرُ سلطتها
بانتهاء التشغيل.
"""

from __future__ import annotations

import argparse
import sys

from alghanem.arabic.masaq_corpus_deposit import (
    MASAQ_ATTRIBUTION,
    MASAQ_PATH_VARIABLE,
    MASAQ_RELATIVE_PATH,
    MasaqDepositError,
)
from alghanem.arabic.masaq_fractal_experiment import (
    GENERATOR_VISIBLE_COLUMNS,
    HELD_OUT_READOUT_COLUMNS,
    MASAQ_PREREGISTRATION_CONTENT_ID,
    MASAQ_SUFFICIENCY_CONTRACT,
    MasaqExperimentError,
    read_masaq_word_inputs,
    run_masaq_fractal_experiment,
)
from alghanem.fractal_experiment import (
    EXPERIMENT_BEFORE_LICENSE,
    FRACTAL_EXPERIMENT_LAW_SET_DIGEST,
    SUFFICIENT_WITNESSES_OPEN_LICENSING_CANDIDATE_NOT_LICENSE,
    ExperimentalPermitState,
)
from alghanem.fractal_generation import (
    LiftError,
    NextScaleSeed,
    ScaleNecessityCertificate,
)


def main() -> int:
    """اقرأ البايتات، وشغِّل التجربة تحت إذنٍ مؤقّت، واطبع الشواهد."""

    parser = argparse.ArgumentParser(description="تشغيلٌ فراكتاليٌّ تجريبيٌّ على MASAQ")
    parser.add_argument(
        "--limit",
        type=int,
        default=200,
        help="عددُ الكلمات المُجمَّدة الداخلة في التشغيل بترتيب ورودها",
    )
    parser.add_argument(
        "--run-id",
        default="run.masaq.segment_accretion.1",
        help="مُعرِّفُ التشغيل؛ والإذنُ مربوطٌ به بعينه",
    )
    arguments = parser.parse_args()

    print(MASAQ_ATTRIBUTION)
    print(EXPERIMENT_BEFORE_LICENSE)
    print(f"law set digest: {FRACTAL_EXPERIMENT_LAW_SET_DIGEST}")
    print(f"preregistration digest: {MASAQ_PREREGISTRATION_CONTENT_ID}")
    print(
        "sufficiency contract (declaration only): "
        f"{MASAQ_SUFFICIENCY_CONTRACT.content_id}"
    )
    print(f"generator sees: {', '.join(GENERATOR_VISIBLE_COLUMNS)}")
    print(f"held out of the generator: {', '.join(HELD_OUT_READOUT_COLUMNS)}")

    try:
        words = read_masaq_word_inputs(limit=arguments.limit)
    except (MasaqDepositError, MasaqExperimentError) as error:
        print(f"error: {error}", file=sys.stderr)
        print(
            f"deposit the bytes at {MASAQ_RELATIVE_PATH} or declare "
            f"{MASAQ_PATH_VARIABLE}; no run is opened without them",
            file=sys.stderr,
        )
        return 1

    report = run_masaq_fractal_experiment(words, run_id=arguments.run_id)

    print(f"[binding] words={len(words)} content_id={report.binding.content_id}")
    print(f"[permit] content_id={report.permit.content_id}")
    print(f"[permit] final state={report.final_permit_state.value}")
    for standing, count in report.standings.items():
        print(f"    [{standing}] {count}")
    print(f"[experimental seeds] {len(report.experimental_seed_ids)}")
    for witness in report.witnesses[:8]:
        print(
            f"    {witness.witness_id}: {witness.standing.value} — "
            f"{witness.reconstruction_observation}"
        )
    print(f"[bundle] content_id={report.bundle.content_id}")
    print(f"[bundle] runs={sorted(report.bundle.independent_run_ids)}")
    print(f"[bundle] residuals={len(report.bundle.residual_union)}")
    for gap in report.bundle.authority_gaps:
        print(f"    [gap] {gap.gap_id}: {gap.statement}")
    print(SUFFICIENT_WITNESSES_OPEN_LICENSING_CANDIDATE_NOT_LICENSE)

    if report.final_permit_state is not ExperimentalPermitState.REVOKED:
        print("error: the temporary authority outlived its run", file=sys.stderr)
        return 1
    for name in ("license", "certify", "licence"):
        if hasattr(report.bundle, name) or hasattr(report.permit, name):
            print(f"error: a licensing member appeared: {name}", file=sys.stderr)
            return 1
    try:
        ScaleNecessityCertificate(  # type: ignore[call-arg]
            requirement=None,
            exhaustion=None,
            issuance=None,
        )
    except (LiftError, TypeError):
        pass
    else:
        print("error: the sealed scale necessity certificate issued", file=sys.stderr)
        return 1
    if any(isinstance(seed, NextScaleSeed) for seed in report.experimental_seed_ids):
        print("error: a permanent next scale seed appeared", file=sys.stderr)
        return 1
    print("the run produced witnesses under a temporary authority, and no license")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
