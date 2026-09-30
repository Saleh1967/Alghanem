"""قراءةُ دعاوى ورقة Powers على البايتات المختومة.

python examples/arabic/read_powers_two_regime.py
"""

from __future__ import annotations

from alghanem.arabic.powers_two_regime_measure import (
    POWERS_NAMED_RESIDUALS,
    THE_PENDING_LAWS,
    Law,
    TokenRule,
    band_lengths,
    head_fit,
    tail_fit,
    the_ayah_field_rule_is_silent_on_these_bytes,
    the_length_ladder_is_monotone,
    the_markup_drop_lands_on_the_surveyed_total,
    the_publisher_markup_census,
    the_quoted_figures_against_ours,
    the_tail_prefers_the_corrected_law,
    token_census,
)


def main() -> None:
    markup = the_publisher_markup_census()
    print("علاماتُ الناشر:", ", ".join(markup.forms))
    print(f"  وقوعاتُها {markup.occurrences:,} · رتبةُ أكثرها {markup.top_rank}")
    for rule in TokenRule:
        census = token_census(rule)
        print(f"{rule.value}: {census.tokens:,} توكنًا · {census.types:,} نوعًا")
    print(
        "  إسقاطُها يبلغ 78,245:",
        the_markup_drop_lands_on_the_surveyed_total(),
        "· وقاعدةُ حقل الآية صامتةٌ ههنا:",
        the_ayah_field_rule_is_silent_on_these_bytes(),
    )

    print("\nالنظامان:")
    for rule in TokenRule:
        for law in Law:
            head = head_fit(rule, law)
            tail = tail_fit(rule, law)
            print(
                f"  {rule.value} · {law.value}: "
                f"رأس {head.r_squared:.4f} ({head.slope:+.4f}) · "
                f"ذيل {tail.r_squared:.4f} ({tail.slope:+.4f})"
            )
        print("  الذيلُ يُؤثِر المصحَّح:", the_tail_prefers_the_corrected_law(rule))

    print("\nسُلَّمُ الطول (المفتاح المختوم):")
    for band in band_lengths():
        ceiling = "بلا سقف" if not band.high else str(band.high)
        print(
            f"  {band.low}–{ceiling}: {band.types:,} نوعًا · "
            f"{band.mean_length:.4f} حرفًا"
        )
    print("  صعودٌ أحاديّ:", the_length_ladder_is_monotone())

    print("\nالمنقولُ مقابَلًا:")
    for row in the_quoted_figures_against_ours():
        print(
            f"  {row.name}: منقولٌ {row.quoted} · مقيسٌ {row.measured:.4f} · "
            f"فارقٌ {row.gap:+.4f} → {row.standing.value}"
        )

    print("\nبندان ينتظران مادّتَهما:")
    for law in THE_PENDING_LAWS:
        print(f"  {law.name}: {law.what_it_needs}")

    print("\nالبقايا المسمّاة:")
    for text in POWERS_NAMED_RESIDUALS.values():
        print(f"  — {text}")


if __name__ == "__main__":
    main()
