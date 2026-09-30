"""يعرض زِبف وإنتروبيا الكتل على البايتات المختومة، ثمّ منزلةَ المنقول."""

from __future__ import annotations

from alghanem.arabic.zipf_block_entropy_measure import (
    THE_BLOCK_SIZES,
    THE_QUOTED_BLOCK_ENTROPY,
    THE_QUOTED_ZIPF,
    ZIPF_BLOCK_ENTROPY_NAMED_RESIDUALS,
    SamplingRule,
    StreamKey,
    block_entropy_ladder,
    the_block_entropy_comparison,
    the_corpus_gate_is_untouched,
    the_folding_moves_the_exponent_by,
    the_quoted_pair_against_our_windows,
    the_stride_shift,
    the_window_that_hosts_the_quoted_pair,
    vocabulary_census,
)


def main() -> None:
    """أطبع سُلَّمَ النوافذ، ثمّ سُلَّمَي الكتل، ثمّ أحكامَ المقابلة."""

    census = vocabulary_census()
    print(
        f"المقام: {census.tokens:,} كلمةً · {census.types:,} لفظًا مميّزًا · "
        f"{census.hapax:,} منها مرّةً واحدة"
    )

    print("\nسُلَّمُ زِبف — الأسُّ دالّةٌ في النافذة:")
    for verdict in the_quoted_pair_against_our_windows():
        window = "كلُّ الرتب" if verdict.fit.window == 0 else f"{verdict.fit.window:,}"
        print(
            f"  {window:>12}: |α| = {verdict.fit.magnitude:.4f} · "
            f"R² = {verdict.fit.r_squared:.4f} · "
            f"الأسّ {verdict.exponent_standing.value} · "
            f"الربط {verdict.r_squared_standing.value}"
        )
    print(
        f"  المنقولُ ({THE_QUOTED_ZIPF.magnitude} · {THE_QUOTED_ZIPF.r_squared}) "
        f"عن `{THE_QUOTED_ZIPF.corpus}` يقع في: "
        f"{the_window_that_hosts_the_quoted_pair()}"
    )
    print(f"  ما حرّكه الطيُّ والفكُّ في الأسّ: {the_folding_moves_the_exponent_by():.6f}")

    print("\nسُلَّمُ إنتروبيا الكتل — بتٌّ في الحرف:")
    dense = block_entropy_ladder(StreamKey.AS_SEALED, SamplingRule.EVERY_POSITION)
    sparse = block_entropy_ladder(StreamKey.AS_SEALED, SamplingRule.EVERY_SEVENTH)
    for size, full, strided, shift in zip(
        THE_BLOCK_SIZES, dense.per_character, sparse.per_character, the_stride_shift()
    ):
        print(
            f"  k = {size}: كلُّ موضعٍ {full:.4f} · بخطوة سبعةٍ {strided:.4f} · "
            f"فرقُ الخطوة {shift:+.4f}"
        )

    print(f"\nمقابلةُ سُلَّمهم (خطوتُهم {THE_QUOTED_BLOCK_ENTROPY.declared_stride}):")
    for row in the_block_entropy_comparison():
        print(
            f"  k = {row.size}: المنقولُ {row.quoted:.3f} · المقيسُ "
            f"{row.measured:.4f} · {row.standing.value}"
        )

    print(f"\nبوّابةُ ماركوف لم تُزحزَح: {the_corpus_gate_is_untouched()}")
    print("\nالبقايا المسمّاة:")
    for name in ZIPF_BLOCK_ENTROPY_NAMED_RESIDUALS:
        print(f"  · {name}")


if __name__ == "__main__":
    main()
