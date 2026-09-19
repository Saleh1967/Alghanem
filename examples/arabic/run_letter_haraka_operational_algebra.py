"""أجرِ الجبرَ التشغيليّ للحرف والحركة على الفاتحة المُودَعة، واعرض المداخل."""

from __future__ import annotations

from alghanem.arabic.letter_haraka_operational_algebra import (
    ALGEBRA_NAMED_RESIDUALS,
    JoinInputStatus,
    build_licensed_inputs,
)


def main() -> None:
    bundle = build_licensed_inputs()

    print("المصدر:", bundle.source_id)
    print("بصمةُ الحزمة:", bundle.content_digest)
    print()

    print("وحداتُ (حامل، حالة) المقسومة:", len(bundle.inputs))
    print("  مقبولةٌ مدخلًا لـ`J`:", len(bundle.admissible))
    print("  غيرُ معرَّفةٍ بعلّةٍ مسمّاة:", len(bundle.undefined))
    print(
        "  ليست عنصرًا في `X_C` ولا `X_V`:",
        sum(1 for i in bundle.inputs if i.status is JoinInputStatus.NOT_AN_ELEMENT),
    )
    print()

    print("توزيعُ الكمّيّة على المقبول (مُشتَقٌّ لا مكتوب):")
    for quantity, count in bundle.quantity_census:
        print(f"  كمّيّة {quantity}: {count}")
    print("  تعذّرت كمّيّتُها لمحورِ المدّ المؤجَّل:", len(bundle.quantity_undefined))
    print("  أشقاءُ شدّةٍ أُوَل، ولا صائتَ في وحدتها:", len(bundle.gemination_pair_starts))
    print()

    print("عيّنةٌ من المقبول:")
    for item in bundle.admissible[:5]:
        assert item.vowel is not None
        print(
            f"  كلمة {item.word_index} موضع {item.unit_index}: "
            f"{item.vowel.carrier} / {item.vowel.identity.value} / "
            f"كمّيّة {item.vowel.quantity}"
        )
    print()

    print("عيّنةٌ ممّا تعذّر:")
    for item in bundle.quantity_undefined:
        print(f"  كلمة {item.word_index} موضع {item.unit_index}: {item.reason}")
    print()

    print("الحدودُ مُسمّاةً:")
    for note in ALGEBRA_NAMED_RESIDUALS:
        print(" -", note)


if __name__ == "__main__":
    main()
