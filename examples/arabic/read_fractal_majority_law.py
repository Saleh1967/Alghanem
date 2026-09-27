"""يعرض الجدولَ الفراكتاليَّ قانونًا غالبًا: كسورُه الأربعة، وشرطاه بمصدريهما."""

from __future__ import annotations

from alghanem.arabic.fractal_majority_law_deposit import (
    FRACTAL_MAJORITY_LAW_NAMED_RESIDUALS,
    THE_FIRST_CONDITION,
    THE_FOUR_BREAKS,
    THE_LEVELS,
    THE_QUOTED_FIRST_POSITION_DENOMINATOR,
    THE_SECOND_CONDITION,
    THE_THREE_SIGNATURES,
    Verdict,
    measured_share_of_the_table,
    the_corpus_gate_is_untouched,
    the_direction_holds_on_every_key,
    the_marked_word_count,
    the_measured_ladder,
    the_transcription_verdicts,
)


def main() -> None:
    """أطبع الجدولَ ومنازلَه، ثمّ المقيسَ من البايتات، ثمّ أحكامَ المنقول."""

    print("الجدولُ الفراكتاليُّ — قانونُ غالبٍ لا تام:")
    for row in THE_LEVELS:
        print(f"  {row.level}: {row.standing.value}")
        print(f"    وصلٌ: {row.joining} · قطعٌ: {row.cutting}")
        print(f"    إعادةُ تركيبٍ: {row.recomposition}")
        print(f"    السند: {row.where}")
    print(f"  حصّةُ الصفوف المقيسة: {measured_share_of_the_table():.3f}")

    print("\nالكسورُ الأربعة، مسمّاةً بمواضعها:")
    for a_break in THE_FOUR_BREAKS:
        print(f"  [{a_break.level}] {a_break.name} — {a_break.genus.value}")
        print(f"    موضعُ الكسر: {a_break.where_it_breaks}")
        print(f"    المصدر: {a_break.source}")

    print("\nالتوقيعاتُ الثلاث:")
    for signature in THE_THREE_SIGNATURES:
        print(f"  {signature.name}: {signature.what_it_says}")
        print(f"    تُغيِّر: {signature.what_it_changes}")

    print("\nالمقيسُ من البايتات المختومة، على مفتاحَي الخاتمة:")
    for reading in the_measured_ladder():
        print(f"  {reading.key.value}:")
        for census in (reading.interior, reading.ending):
            fatha, kasra, damma = census.three_vowel_shares
            print(
                f"    {census.where}: فتحة {fatha:.3f} · كسرة {kasra:.3f} · "
                f"ضمّة {damma:.3f} · H {census.three_vowel_entropy:.4f} · "
                f"سكون+تنوين {census.sukun_and_tanwin_share:.4f}"
            )
        print(
            f"    هبوطُ الفتحة {reading.fatha_collapse:.3f} · "
            f"ارتفاعُ الإنتروبيا {reading.entropy_rise:.4f}"
        )
    print(f"  الاتّجاهُ يثبت على المفتاحين: {the_direction_holds_on_every_key()}")

    print("\nأحكامُ الأرقام المنقولة، مُشتَقّةً بالحساب:")
    for comparison in the_transcription_verdicts():
        print(
            f"  [{comparison.key.value}] {comparison.name}: "
            f"نُقِل {comparison.quoted:.4f} وقِيس {comparison.measured:.4f} "
            f"→ {comparison.verdict.value}"
        )

    print("\nتقاطعُ التنفيذين:")
    print(
        f"  الكلماتُ المشكولة ههنا {the_marked_word_count()} "
        f"ومقامُهم المنقول {THE_QUOTED_FIRST_POSITION_DENOMINATOR}"
    )

    print("\nالشرطان، مُقيَّدَين بمصدريهما:")
    for condition in (THE_FIRST_CONDITION, THE_SECOND_CONDITION):
        genus = condition.verdict_genus
        name = genus.value if isinstance(genus, Verdict) else "حكمُه مقابلةٌ لا وسم"
        print(f"  {condition.question} — {condition.standing.value} ({name})")
        print(f"    مربوطٌ بـ: {condition.bound_to}")
        print(f"    القراءة: {condition.reading}")

    print(f"\nبوّابةُ ماركوف كما كانت: {the_corpus_gate_is_untouched()}")
    print("\nالبقايا المسمّاة:")
    for token in FRACTAL_MAJORITY_LAW_NAMED_RESIDUALS:
        print(f"  {token}")


if __name__ == "__main__":
    main()
