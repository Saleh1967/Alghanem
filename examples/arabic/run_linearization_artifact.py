"""اقرأ دعوى الخطّيّة: أيحمل الترتيبُ بين الحامل وعلامته خبرًا، أم لا؟"""

from __future__ import annotations

from alghanem.arabic.carrier_state_observed_fiber import (
    run_observed_fiber_on_the_deposited_fatiha,
)
from alghanem.arabic.linearization_artifact import (
    LINEARIZATION_NAMED_RESIDUALS,
    THE_CLAIM,
    every_mark_follows_its_carrier_by_definition,
    measure_mark_order_freedom,
    measure_ordering_census,
    read_the_linearity_claim,
    round_trip_from_unordered_sets,
)


def main() -> None:
    table = run_observed_fiber_on_the_deposited_fatiha()

    print(f"الدعوى: «{THE_CLAIM}»")
    print(f"الإيداع: {table.deposit.sha256}")
    print()

    forced = every_mark_follows_its_carrier_by_definition()
    print(f"العلامةُ لاحقةٌ لحاملها بتعريف الترميز: {forced} — بلا حاجةٍ إلى عدّ")

    freedom = measure_mark_order_freedom()
    print(
        f"مجموعاتُ العلامات المفحوصة: {freedom.multisets_examined}، "
        f"ذاتُ صورةٍ قانونيّةٍ واحدة: "
        f"{freedom.multisets_with_a_single_canonical_form}، "
        f"أكان الترتيبُ حرًّا: {freedom.order_was_ever_free}"
    )

    audit = round_trip_from_unordered_sets(table)
    print(
        f"العكسُ من مجموعاتٍ غيرِ مرتَّبة: "
        f"{audit.words_reconstructed}/{audit.words_examined} "
        f"تامٌّ={audit.is_lossless}"
    )

    census = measure_ordering_census(table)
    print(
        f"ترتيباتٌ تدلّ على القراءة نفسِها: "
        f"{census.orderings_denoting_the_same_reading} "
        f"({census.bits_of_apparent_freedom:.0f} بتًّا) من "
        f"{census.carriers_bearing_more_than_one_mark} حاملًا ذي أكثرَ من علامة"
    )

    for reading in read_the_linearity_claim(table):
        print()
        print(f"— {reading.reading.value} ← {reading.verdict.value}")
        print(f"  المُقرِّر: {reading.what_decided_it}")
        for note in reading.residuals:
            print(f"  بقيّة: {note}")

    print()
    print("الحدودُ المُسمّاة:")
    for note in LINEARIZATION_NAMED_RESIDUALS:
        print(f"  - {note}")


if __name__ == "__main__":
    main()
