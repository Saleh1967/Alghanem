"""تشغيلُ مربّع الاستقراء في رتبة ماركوف، وطبعُ طرفيه معًا.

    python examples/arabic/run_markov_order_induction.py

والغرضُ أن يُرى الطرفان في نفَسٍ واحد: ما تختاره الرتبةُ حين يُصعَد السلّمُ
على المادّة كلِّها، وما تختاره حين يُقسَم أوّلًا ثمّ يُصعَد داخل المرئيّ. وما
بينهما فرقٌ لا يُصلَح بمزيد حساب، لأنّه فرقٌ في ترتيب الاستقراء لا في البايتات.

ولا يُمسّ ههنا حجبُ ماركوف على المدوّنة: المقيسُ جدولُ الجذور المُبصَّم وحدَه.
"""

from __future__ import annotations

from alghanem.arabic.markov_order_induction import (
    THE_DECLARED_SMOOTHINGS,
    THE_LADDER_ORDER,
    THE_PREREGISTERED_COMMUTATION_CONDITION,
    THE_REQUIRED_DRAW_FLOOR,
    InductionDirection,
    degrees_of_freedom,
    information_criterion,
    measure_commutation,
    place_alphabet,
    place_sequences,
    rung_crossover_scan,
    the_corpus_gate_is_untouched,
)


def main() -> None:
    """يطبع السلّمَ، ثمّ طرفَي المربّع، ثمّ مسحَ عتبة الانقلاب."""

    material = place_sequences()
    alphabet = place_alphabet()
    print("الشرطُ المُودَع:")
    print(THE_PREREGISTERED_COMMUTATION_CONDITION)
    print()
    print(f"المادّة: {len(material)} جذرًا على {len(alphabet)} مخرجًا")
    print(f"بوّابةُ المدوّنة محجوبةٌ بعدُ: {the_corpus_gate_is_untouched()}")
    print()

    print("السلّم:")
    for rung in THE_LADDER_ORDER:
        freedom = degrees_of_freedom(rung, len(alphabet))
        reading = information_criterion(rung, material)
        print(f"  {rung.value}: حرّيّة {freedom}، معيار {reading:.2f}")
    print()

    reading = measure_commutation(draws=THE_REQUIRED_DRAW_FLOOR)
    ends = reading.rung_by_direction()
    print("طرفا المربّع:")
    for direction in InductionDirection:
        landed = ends[direction]
        print(f"  {direction.value}: {landed.value if landed else 'لا شيء'}")
    held_out = reading.held_out_rung
    print(
        f"  الفائزُ بالتنبّؤ على المحجوب: {held_out.value if held_out else 'مختلَفٌ فيه'}"
    )
    print(f"  نصيبُ الموافقة: {reading.agreement_share:.3f}")
    print(f"  الملساران المُعلَنان: {THE_DECLARED_SMOOTHINGS}")
    print(f"  المنزلة: {reading.standing.value}")
    print()

    print("مسحُ عتبة الانقلاب:")
    for row in rung_crossover_scan():
        chosen = sorted({rung.name for rung in row.rungs})
        mark = "بإجماع" if row.is_unanimous else "بانقسام"
        print(f"  عند {row.seen_count}: {'، '.join(chosen)} ({mark})")


if __name__ == "__main__":
    main()
