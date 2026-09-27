"""تشغيلُ الطبقات الأربع بعددِ تبديلاتٍ يكفي عتبتَها، وطبعُ ما يخرج.

والاختباراتُ تُشغّل الجبرَ بعددٍ صغيرٍ لتبقى سريعة، فيخرج فيها الحكمُ
`UNRESOLVABLE_AT_THIS_B` وهو الصوابُ عند ذلك العدد. وهذا المثالُ يرفع العدد
حتّى يصير حدُّ الوجهين `2/(B+1)` أدقَّ من العتبة، فتُقرَأ الأحكامُ مقروءةً.

    python examples/arabic/run_slot_rights_algebra.py

ولا يُمنح هنا وسمُ «مرخّص» لشيء: شرطُ القيد المكتوب قبل النظر منتفٍ، وبايتاتُ
المصدر الثاني ليست في هذه الشجرة.

والطبقةُ الرابعةُ أبطأُ الأربع: سلسلةُ «لا تفاعلَ ثلاثيّ» تقبل نحو أربعين خطوةً
في الثانية، فيأخذ تشغيلُها دقائق. وذلك ثمنُ مقترحٍ متناظرٍ لم يُستبدل بأسرعَ
منه موجَّهٍ يُخِلّ بالتوزيع.
"""

from __future__ import annotations

from alghanem.arabic.slot_rights_composition_algebra import (
    TernaryStatistic,
    VerdictStanding,
    algebra_substrate,
    fold_collapse_count,
    licence_standing,
    measure_closure,
    measure_triangle_closure,
    positional_asymmetry_locus,
    quoted_against_measured,
    second_source_is_resolvable,
    slot_birth_conditions,
    slot_rights,
    typed_cell_verdicts,
    verify_naive_null_breaks_distinctness,
    verify_witness_monotonicity,
)


def main() -> None:
    """يطبع الطبقاتِ الثلاثَ بالترتيب، ثمّ المنقولَ في وجه المقيس."""

    body = algebra_substrate()
    print(f"الجسم: {len(body):,} نوعًا مطويًّا، والطيُّ ألحم {fold_collapse_count()}.")
    print(f"منزلةُ الترخيص: {licence_standing().value}")
    print(f"بايتاتُ المصدر الثاني محلولة؟ {second_source_is_resolvable()}")

    print("\n— الطبقة الأولى: حقوقُ الخانة —")
    rights = slot_rights(body)
    witnessed = sum(1 for right in rights if right.witnesses > 0)
    print(f"الخلايا {len(rights)}، والمشهودُ منها {witnessed}.")
    print(f"مبرهنة ح١ مفحوصة: {verify_witness_monotonicity(body)}")
    for condition in slot_birth_conditions(body, draws=2000):
        print(
            f"  خانة {condition.slot + 1}: حاملون {condition.distinct_carriers}، "
            f"أزواجُ استبدال {condition.witnessed_substitution_pairs:,}، "
            f"p(M₀) = {condition.exchangeability_p:.5f}، وُلدت: {condition.is_born}"
        )

    print("\n— الطبقة الثانية: هندسةُ التركيب —")
    print(f"تزاحمُ النموذج الساذج (ت٢): {verify_naive_null_breaks_distinctness(body)}")
    closure = measure_closure(body, draws=2000, burn_in=200000, sweep=2000)
    print(
        f"  اجتماعُ الطرفين من مخرجٍ واحد: {closure.observed_same_place} بإزاء "
        f"{closure.null_mean_same_place:.1f} — نسبة {closure.same_place_ratio:.3f}"
    )
    print(
        f"  تماثلُ الطرفين: {closure.observed_identity} بإزاء "
        f"{closure.null_mean_identity:.1f} — نسبة {closure.identity_ratio:.3f}"
    )
    print(f"  أينغلق التركيب؟ {closure.closure_holds}")

    print("\n— الطبقة الثالثة: القيدُ مصنَّفًا بنوع العلاقة —")
    verdicts = typed_cell_verdicts(body, draws=3000, burn_in=200000, sweep=600)
    print(f"الخلايا المفحوصة {len(verdicts)}، والعتبة {verdicts[0].threshold:.3g}.")
    for verdict in verdicts:
        if verdict.standing is VerdictStanding.NEUTRAL:
            continue
        ratio = f"{verdict.ratio:.2f}" if verdict.ratio else "—"
        print(
            f"  {verdict.relation.value} · {verdict.place_class} · "
            f"{verdict.kind.value}: {verdict.observed} بإزاء "
            f"{verdict.null_mean:.1f} (نسبة {ratio}) — {verdict.standing.value}"
        )

    locus = positional_asymmetry_locus(body, draws=2000)
    print("\n— موضعُ الفرق بين العلاقتين المتجاورتين —")
    identity_p = f"{locus.identity_probability:.5f}"
    print(f"  في التماثل: {locus.identity_difference} (p = {identity_p})")
    print(f"  في التجانس: {locus.class_difference} (p = {locus.class_probability:.5f})")
    print(f"  الموضع: {locus.locus.value if locus.locus else 'غيرُ منفرد'}")

    print("\n— الطبقة الرابعة: المثلّثُ لا السلسلة —")
    print(f"  الشرطُ مكتوبٌ قبل العدّ، وعتبتُه {0.05 / 3:.5f}.")
    triangle = measure_triangle_closure(body)
    print(f"  الخطواتُ المقبولة: {triangle.accepted_moves:,} · خلطت: {triangle.mixed}")
    for statistic in TernaryStatistic:
        observed = triangle.observed[statistic]
        expected = triangle.null_mean[statistic]
        chance = triangle.probability[statistic]
        print(
            f"  {statistic.value}: {observed:,} بإزاء {expected:,.1f} "
            f"(p = {chance:.5f}، قيمٌ مختلفة {triangle.spread[statistic]})"
        )
    print(f"  منزلةُ المثلّث: {triangle.standing.value}")

    print("\n— المنقولُ في وجه المقيس —")
    for subject, quoted, measured, agrees in quoted_against_measured(body):
        print(f"  {subject}: منقولٌ «{quoted}» · مقيسٌ «{measured}» · تطابق: {agrees}")


if __name__ == "__main__":
    main()
