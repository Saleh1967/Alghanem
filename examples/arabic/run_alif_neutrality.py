"""اقرأ دعوى «حيادِ الألف» على الإيداع المُبصَّم: ما انعقد، وما اختير، وما انتقض."""

from __future__ import annotations

from alghanem.arabic.alif_neutrality import (
    ALIF,
    ALIF_NEUTRALITY_NAMED_RESIDUALS,
    THE_CLAIM,
    identity_state,
    measure_constancies,
    measure_rectangle_fill,
    read_the_alif_claim,
)
from alghanem.arabic.carrier_state_observed_fiber import (
    run_observed_fiber_on_the_deposited_fatiha,
)


def main() -> None:
    table = run_observed_fiber_on_the_deposited_fatiha()

    print(f"الدعوى: «{THE_CLAIM}»")
    print(f"الإيداع: {table.deposit.sha256}")
    print(f"المحايد: {identity_state(table)}")
    print()

    print("الثباتُ مضبوطًا بالشُّح (ما سَعتُه واحدة):")
    for item in sorted(
        measure_constancies(table), key=lambda reading: reading.constancy_exponent
    ):
        if not item.is_constant:
            continue
        survived = "ينجو" if item.survives_the_scarcity_control else "لا ينجو"
        print(
            f"  {item.carrier}  وقعات={item.occurrences:3}  "
            f"احتمالُ الثبات={float(item.constancy_exponent):.2e}  {survived}"
        )

    whole = measure_rectangle_fill(table)
    without = measure_rectangle_fill(table, excluding=ALIF)
    print()
    print(
        f"المستطيل بالألف: {whole.realized_pairs}/{whole.rectangle} "
        f"سَعات={whole.capacity_spread}"
    )
    print(
        f"المستطيل بدونها: {without.realized_pairs}/{without.rectangle} "
        f"سَعات={without.capacity_spread}"
    )

    for reading in read_the_alif_claim(table):
        print()
        print(f"— {reading.reading.value} ← {reading.verdict.value}")
        print(f"  المُقرِّر: {reading.what_decided_it}")
        for note in reading.residuals:
            print(f"  بقيّة: {note}")

    print()
    print("الحدودُ المُسمّاة:")
    for note in ALIF_NEUTRALITY_NAMED_RESIDUALS:
        print(f"  - {note}")


if __name__ == "__main__":
    main()
