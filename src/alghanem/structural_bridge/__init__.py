"""`G0.SBR-0`: جسرٌ يصل بايتاتٍ حقيقيّةً بخانتين بنيويّتين، ولا يتجاوزهما.

    source: bytes  --موضعا بتٍّ مُصرَّحان-->  StructuralWhole ذو خانتين

وهذا الجسرُ يُثبِت شيئًا واحدًا: أنّ قيمتَي الخانتين مستخرجتان من هذا المصدر
بعينه في موضعين مُسمّيين، وأنّ الشاهدَ مربوطٌ ببصمة المصدر وطولِه وموضعيه.

ولا يُثبِت شيئًا وراء ذلك. فهذه الأربعةُ ممنوعةٌ بقانونٍ ومقيسةٌ باختبار:

    BitSlot  !=  LinguisticRole
    BitSlot  !=  RootCandidate
    BitSlot  !=  WeightCandidate
    ByteSlotBridge  ↛  الإفادة

والجسرُ لا يدخل في توليد الإفادة ولا يُغيّرها: يُقاس السَّوقُ قبلَه وبعدَه
على البايتات عينِها، ويُقارَن الحكمُ والطبقةُ والمانعُ والأثرُ كلُّه.

تسجيلٌ لا سلطة: لا شهادةَ ولادةٍ، ولا حكمَ مطابقةٍ للواقع، ولا ترقيةَ دور.
"""

from __future__ import annotations

from .byte_slot_bridge import (
    A_BIT_SLOT_IS_NOT_A_LINGUISTIC_ROLE,
    A_BIT_VALUE_IS_NOT_A_STRUCTURAL_SCALE,
    A_REPEATED_VALUE_IS_NOT_A_PRESERVED_OCCURRENCE,
    DECLARED_SLOT_COUNT,
    STRUCTURAL_BRIDGE_NAMED_LAWS,
    THE_BRIDGE_DOES_NOT_TOUCH_THE_BENEFIT,
    THE_WITNESS_IS_BOUND_TO_ITS_SOURCE_AND_POSITIONS,
    BitPosition,
    BitSlotReading,
    ByteSlotBridge,
    PathComparison,
    StructuralBridgeError,
    bridge_two_bits,
    compare_with_the_path,
    render_bridge,
)

__all__ = [
    "A_BIT_SLOT_IS_NOT_A_LINGUISTIC_ROLE",
    "A_BIT_VALUE_IS_NOT_A_STRUCTURAL_SCALE",
    "A_REPEATED_VALUE_IS_NOT_A_PRESERVED_OCCURRENCE",
    "DECLARED_SLOT_COUNT",
    "STRUCTURAL_BRIDGE_NAMED_LAWS",
    "THE_BRIDGE_DOES_NOT_TOUCH_THE_BENEFIT",
    "THE_WITNESS_IS_BOUND_TO_ITS_SOURCE_AND_POSITIONS",
    "BitPosition",
    "BitSlotReading",
    "ByteSlotBridge",
    "PathComparison",
    "StructuralBridgeError",
    "bridge_two_bits",
    "compare_with_the_path",
    "render_bridge",
]
