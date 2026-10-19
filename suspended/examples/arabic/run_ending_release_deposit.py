"""يعرض إيداعَ مولِّدات الخاتمة: ما وافق، وما خالف، وما لم يُنشَر ههنا."""

from __future__ import annotations

from alghanem.arabic.ending_release_deposit import (
    ENDING_RELEASE_NAMED_RESIDUALS,
    THE_ABSENT_IDENTIFIERS,
    THE_ENDING_FIGURES,
    FigureStanding,
    contradicting_figures,
    identifier_is_present_in_this_tree,
    measure_the_sealed_corpus,
    the_corpus_gate_is_untouched,
    the_key_ladder,
)


def main() -> None:
    """أطبع ما يُعاد قياسُه، ثمّ ما يمتنع نشرُه ولماذا."""

    figures = measure_the_sealed_corpus()
    print("المدوّنةُ المختومة:")
    print(f"  آيات: {figures.ayah_count}؛ توكنات: {figures.token_count}")
    print(f"  أعلى صنفِ خاتمةٍ حصّةً: {figures.dominant_ending_share:.4f}")

    print("\nالقانونان البنيويّان:")
    print(f"  سكونٌ في أوّل الكلمة: {figures.word_initial_written_sukun}")
    adjacent = figures.adjacent_written_sukun_inside_a_word
    print(f"  سكونان متجاوران داخلها: {adjacent}")
    print(f"  لامُ الأمر موصولةً: {figures.joined_lam_of_command_tokens}")

    print("\nجدولُ ق-تخلّص على الصيغ المتناوبة:")
    print(f"  ساكنٌ قبل ألفِ الوصل: {figures.sukun_before_the_connecting_alif}")
    print(f"  ساكنٌ قبل سواها: {figures.sukun_before_anything_else}")
    voweled_wasl = figures.voweled_before_the_connecting_alif
    print(f"  متحرّكٌ قبل ألفِ الوصل: {voweled_wasl}")
    print(f"  متحرّكٌ قبل سواها: {figures.voweled_before_anything_else}")
    print(f"  لو وُسِّع الشرطُ إلى كلّ ألف: {figures.sukun_before_any_alif_shape}")

    print("\nسلّمُ المفاتيح الثلاثة:")
    for rung in the_key_ladder():
        print(
            f"  {rung.key.value}: {rung.alternating_forms} صيغةً، "
            f"{rung.fatha_releases} فتحة"
        )

    print("\nأحكامُ الأرقام المنقولة:")
    for standing in FigureStanding:
        count = sum(1 for figure in THE_ENDING_FIGURES if figure.standing is standing)
        print(f"  {standing.value}: {count}")
    for figure in contradicting_figures():
        print(f"  خالف: {figure.name} — نُقِل {figure.transcribed}")
        print(f"    وقِيس {figure.measured}")

    print("\nالمعرِّفانِ المسنَدان إلى موضعٍ خالٍ:")
    for identifier in THE_ABSENT_IDENTIFIERS:
        print(f"  {identifier}: {identifier_is_present_in_this_tree(identifier)}")

    print(f"\nبوّابةُ ماركوف كما كانت: {the_corpus_gate_is_untouched()}")
    print("\nالقيودُ المسمّاة:")
    for key in ENDING_RELEASE_NAMED_RESIDUALS:
        print(f"  - {key}")


if __name__ == "__main__":
    main()
