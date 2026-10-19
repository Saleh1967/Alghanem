"""اقرأ «لا صامتَ بلا صائتٍ رياضيًّا» قراءاتِها الأربعَ على الإيداع المُبصَّم."""

from __future__ import annotations

from alghanem.arabic.no_consonant_without_a_vowel import (
    NO_CONSONANT_WITHOUT_A_VOWEL_NAMED_RESIDUALS,
    THE_CLAIM,
    read_the_claim,
    take_syllable_census,
)


def main() -> None:
    census = take_syllable_census()

    print(f"الدعوى: «{THE_CLAIM}»")
    print(f"الإيداع: {census.deposit_sha256}")
    print(
        f"الكلمات: {census.word_total} "
        f"(مُقطَّعة {census.segmented_words}، متعذّرة {census.unsegmented_words})"
    )
    print(
        f"المقاطع: {census.syllable_total} "
        f"(بلا نواة {census.syllables_without_a_nucleus}، "
        f"إغلاقات {census.coda_consonants})"
    )
    print(
        f"الحوامل في الرسم: {census.surface_carriers} "
        f"(متحرّكة {census.surface_carriers_bearing_a_vowel}، "
        f"ساكنة {census.surface_carriers_bearing_a_sukun})"
    )
    print(
        "القوالب: "
        + "، ".join(f"{name}×{count}" for name, count in census.templates_seen)
    )

    for verdict in read_the_claim(census):
        print()
        print(f"— {verdict.reading.value} ← {verdict.verdict.value}")
        print(f"  المُقرِّر: {verdict.what_decided_it}")
        print(f"  الشواهد: {verdict.witness_count}")
        for note in verdict.residuals:
            print(f"  بقيّة: {note}")

    print()
    print("الحدودُ المُسمّاة:")
    for note in NO_CONSONANT_WITHOUT_A_VOWEL_NAMED_RESIDUALS:
        print(f"  - {note}")


if __name__ == "__main__":
    main()
