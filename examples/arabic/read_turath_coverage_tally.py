"""قراءةُ جدول تغطية عقد الدال بالتراث: إحصاؤه ومقاماتُه وبقاياه.

python examples/arabic/read_turath_coverage_tally.py
"""

from __future__ import annotations

from alghanem.arabic.turath_coverage_tally import (
    THE_COVERAGE_CRITERION_IS_ABSENT,
    THE_QUOTED_HEADER,
    THE_QUOTED_NODE_COUNT,
    THE_ROWS,
    THE_TURATH_TEXTS_NAMED_IN_THE_TABLE,
    TURATH_COVERAGE_NAMED_RESIDUALS,
    Ground,
    deposited_corpora,
    falsifiable_rows,
    ground_census,
    hedged_rows,
    mark_census,
    no_turath_bytes_are_deposited,
    rows_by_ground,
    tally,
    the_header_overstates_the_covered_rows_by,
    the_title_is_unreached_even_by_the_header,
    unnamed_nodes,
)


def main() -> None:
    current = tally()
    print("المجاميعُ الثلاثة:")
    print(f"  صفوفُ الجدول المعدودة: {current.rows}")
    print(
        f"  جمعُ الترويسة: {THE_QUOTED_HEADER.covered} + "
        f"{THE_QUOTED_HEADER.absent} = {THE_QUOTED_HEADER.total}"
    )
    print(f"  عنوانُ الجدول: {THE_QUOTED_NODE_COUNT}")
    print(f"  تُفرِط الترويسةُ في المغطّاة بـ{the_header_overstates_the_covered_rows_by()}")
    print(f"  ولا يسمّي الجدولُ من العنوان {unnamed_nodes()} عقدة")
    gap = the_title_is_unreached_even_by_the_header()
    print(f"  ولا تبلغ الترويسةُ عنوانَها بـ{gap}")

    print("\nالأحكامُ على أربعتها (والترويسةُ تعدّها ثنتين):")
    for mark, count in mark_census().items():
        print(f"  {mark.value}: {count}")
    print("  المتحفَّظُ عليه:", ", ".join(row.measured_node for row in hedged_rows()))

    print("\nمقاماتُ العمود الأيسر:")
    for ground, count in ground_census().items():
        print(f"  {ground.value}: {count}")
        for row in rows_by_ground(ground):
            if ground is not Ground.NO_FIGURE:
                print(f"    — {row.measured_node}")

    print("\nالمعيار:")
    print(f"  {THE_COVERAGE_CRITERION_IS_ABSENT}")
    print(f"  الصفوفُ القابلةُ للفحص ههنا: {len(falsifiable_rows())} من {len(THE_ROWS)}")

    print("\nالتراثُ المُحال إليه:")
    for name in THE_TURATH_TEXTS_NAMED_IN_THE_TABLE:
        print(f"  — {name}")
    print("  مدوّناتُ الشجرة:", ", ".join(deposited_corpora()))
    print("  لا بايتَ تراثيًّا مُودَعًا:", no_turath_bytes_are_deposited())

    print("\nالبقايا المسمّاة:")
    for text in TURATH_COVERAGE_NAMED_RESIDUALS.values():
        print(f"  — {text}")


if __name__ == "__main__":
    main()
