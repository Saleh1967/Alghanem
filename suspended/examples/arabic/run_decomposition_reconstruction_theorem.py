"""أغلِق مبرهنةَ التفكيك وإعادة البناء، واعرض المفردتين والآلتين منفصلتين."""

from __future__ import annotations

from alghanem.arabic.decomposition_reconstruction_theorem import (
    DECOMPOSITION_THEOREM_NAMED_RESIDUALS,
    INSTRUMENT_DIVERGENCES,
    census_of_declared_population,
    census_of_observed_population,
    prove_decomposition_reconstructs,
    prove_the_residue_is_necessary,
)


def main() -> None:
    observed = census_of_observed_population()
    declared = census_of_declared_population()

    print("المفردةُ المرصودة (بآلةِ المِرماز):")
    print("  المصدر:", observed.source_id)
    print("  كلماتٌ:", observed.word_count, "| مواضعُ:", observed.unit_count)
    print("  حواملُ متمايزة:", observed.distinct_carriers)
    print("  سعاتٌ مقيسة:", observed.observed_capacities)
    print("  أمدى السعات متّصل؟", observed.capacity_range_is_contiguous)
    print()

    print("المفردةُ المُعلَنة (مكتوبةٌ في الشجرة):")
    print("  حواملُ مُعلَنة:", declared.carrier_count)
    print("  حالاتٌ مُعلَنة:", declared.state_count)
    print("  حدٌّ أعلى (جداءٌ لا إحصاء):", declared.upper_bound)
    print()

    print("فوارقُ الآلتين على الإيداع نفسِه — تُسمّى ولا تُسوّى:")
    for divergence in INSTRUMENT_DIVERGENCES:
        print(
            f"  {divergence.quantity}: المِرماز {divergence.codec_value} "
            f"↔ الليف {divergence.fiber_value}"
        )
        print(f"    لماذا: {divergence.why_they_differ}")
    print()

    closed = prove_decomposition_reconstructs()
    print("المبرهنة — تفكيكٌ ثمّ إعادةُ بناءٍ بالبقيّة:")
    print(f"  عاد تامًّا: {closed.exact_rebuilds}/{closed.word_count}")
    print("  أتُغلَق؟", closed.closes)
    print()

    broken = prove_the_residue_is_necessary()
    print("الشاهدُ المضادّ — إسقاطُ البقيّة:")
    print(f"  عاد تامًّا: {broken.exact_rebuilds}/{broken.word_count}")
    print("  انكسر:", len(broken.broken_words), "كلمة")
    print("  منها:", ", ".join(broken.broken_words[:4]))
    print()

    print("الحدودُ مُسمّاةً:")
    for note in DECOMPOSITION_THEOREM_NAMED_RESIDUALS:
        print(" -", note)


if __name__ == "__main__":
    main()
