"""قراءةُ قانون الودائع: البوّاباتُ ثمّ الشهود، كلٌّ بخرقه المقيس الآن.

    python examples/read_deposit_law.py

ولا رقمَ في هذا المثال مكتوبٌ سلفًا؛ كلُّه يُحسَب من الشجرة عند التشغيل.
"""

from __future__ import annotations

from alghanem.deposit_law import (
    LawStanding,
    Standing,
    assert_the_gates_hold,
    every_reading,
    module_paths,
    the_law_holds,
)


def main() -> None:
    print(f"وحداتُ الشجرة المقيسة: {len(module_paths())}\n")

    for standing, title in (
        (Standing.GATE, "البوّابات — تامّةٌ اليوم، وخرقُها يمنع الدمج"),
        (Standing.WITNESS, "الشهود — مقيسةٌ ومنشورة، ولا تمنع"),
    ):
        print(title)
        print("-" * len(title))
        for reading in every_reading():
            if reading.standing is not standing:
                continue
            print(f"  {reading.name}")
            print(f"    {reading.question}")
            print(
                f"    خرقٌ {reading.breach_count} من {reading.examined}"
                f" — امتثالٌ {reading.conformance:.1%} — {reading.law_standing.value}"
            )
            if reading.law_standing is not LawStanding.HELD:
                for breach in reading.breaches[:3]:
                    print(f"      · {breach.module}: {breach.detail}")
                if reading.breach_count > 3:
                    print(f"      · وغيرُها {reading.breach_count - 3}")
        print()

    assert_the_gates_hold()
    print(f"البوّاباتُ قائمةٌ كلُّها: {the_law_holds()}")


if __name__ == "__main__":
    main()
