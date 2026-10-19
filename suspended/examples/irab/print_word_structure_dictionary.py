"""اطبع القاموسَ البنيويَّ لكلماتٍ مُشكَّلة، مقيسَها ومحجوبَها على حدة.

هذا السكربت مادّةٌ مرجعيّة، لا جزءٌ من النواة ولا من طبقة العربية. لا يشتقّ
كائنًا في `kernel/`، ولا يُجيز انتقالًا، ولا يدّعي عددًا عربيًّا. وكلُّ ما
يفعله أنّه ينادي `analyze_word` ويعرض مخرجَها **بفصلِ الأجناس**: الطبقاتُ
الثلاثُ المقيسةُ تُطبَع قيمًا، والأربعُ المحجوبةُ تُطبَع بأسماء حقول تعذّرها
وشروط دخولها — لا بقيمةٍ خاليةٍ تُقرأ نتيجة.

    python examples/irab/print_word_structure_dictionary.py
"""

from __future__ import annotations

from alghanem.arabic.word_structure_dictionary import analyze_word

WORDS: tuple[str, ...] = (
    "الْحَمْدُ",
    "الرَّحْمَنِ",
    "كَتَبَ",
    "سَبَّحَ",
    "مَرَضاً",
    "كِتَابٌ",
)


def main() -> None:
    for word in WORDS:
        dictionary = analyze_word(word)
        print("=" * 68)
        print("الكلمة:", word, "| الذهاب والإياب:", dictionary.surface_round_trips)

        print("الحروف والحالات (مقيس):")
        for letter in dictionary.letters:
            marks = []
            if letter.gemination is not None:
                marks.append(f"تضعيف={letter.gemination.value}")
            if letter.tanwin:
                marks.append("تنوين")
            if letter.tanwin_alif_seat:
                marks.append("مقعد=ألف")
            if letter.seat is not None:
                marks.append(f"مقعد={letter.seat.value}")
            if letter.silent:
                marks.append("صامت")
            suffix = ("  " + " ".join(marks)) if marks else ""
            head = f"  {letter.position}: {letter.written_form}"
            print(f"{head} {letter.state_name}{suffix}")

        if dictionary.unread:
            print("رموز غير مقروءة حروفًا:")
            for segment in dictionary.unread:
                print(f"  {segment.position}: {segment.codepoint!r}")

        if dictionary.shadda_roles:
            print("دور الشدّة (مقيس، ومصدره متعذّر):")
            for role in dictionary.shadda_roles:
                print(f"  {role.position}: {role.carrier} — {role.source_undecided}")

        if dictionary.tanween_roles:
            print("دور التنوين (مقيس):")
            for role in dictionary.tanween_roles:
                seat = "على ألف" if role.seated_on_alif else "بلا مقعد ألف"
                print(f"  {role.position}: {role.carrier} {role.state.name} — {seat}")

        print("طبقات محجوبة (لا قيمة لها، ولكلٍّ حقل تعذّر مُسمًّى):")
        for entry in dictionary.withheld:
            print(f"  {entry.layer.value} [{entry.standing.value}]")
            print(f"    الحقل: {entry.refusal_field_name}")
            print(f"    يقول: {entry.what_the_refusal_field_says}")
            print(f"    شرط الدخول: {entry.entry_condition}")


if __name__ == "__main__":
    main()
