"""`G0.SBR-0.BRIDGE`: استخراجُ بتّين مُصرَّحين من مصدرٍ بايتيّ، وحملُهما خانتين.

الترتيبُ المقصود: تُستخرَج القيمتان من المصدر بعينه، ثمّ يُبنى عليهما كلٌّ
بنيويٌّ بخانتين، ثمّ يُعدَّد تقسيمُه بلا فائزٍ مفروض. ولا يعود شيءٌ من ذلك
إلى المسار العربيّ، ولا يُقرَأ منه دورٌ لغويٌّ ولا إفادة.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Final

from alghanem.arabic.composition_ifada_path import PathRun, run_bytes
from alghanem.canonical_content import canonical_digest
from alghanem.structural_dal import (
    IdentityTransitionMode,
    PromotionStanding,
    ResidualReading,
    ScaleAscent,
    ShapePartitionHypothesisSet,
    StructuralDecomposition,
    StructuralWhole,
    ascend_one_slot,
    decompose,
    enumerate_shape_partitions,
    origin_whole,
)

__all__ = [
    "A_BIT_SLOT_IS_NOT_A_LINGUISTIC_ROLE",
    "A_BIT_VALUE_IS_NOT_A_STRUCTURAL_SCALE",
    "TWO_SLOTS_ARE_NOT_THE_SCALE_COMPOSITION",
    "UNPROVEN_SCALE_LADDER",
    "A_REPEATED_VALUE_IS_NOT_A_PRESERVED_OCCURRENCE",
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

BITS_IN_A_BYTE: Final[int] = 8
"""عددُ البتّات في البايت الواحد؛ حدُّ الموضع داخل البايت."""

DECLARED_SLOT_COUNT: Final[int] = 2
"""خانتان اثنتان لا أقلَّ ولا أكثر؛ وهو حدُّ ما بُرهِن في جبر `zero-one`."""


class StructuralBridgeError(ValueError):
    """رفضٌ مُسمًّى في الجسر نفسِه، لا حكمٌ على المصدر المقيس."""


THE_WITNESS_IS_BOUND_TO_ITS_SOURCE_AND_POSITIONS: Final[str] = (
    "TheWitnessIsBoundToItsSourceAndPositions: شاهدُ الجسر مقرونٌ ببصمةِ مصدره "
    "وطولِه وموضعَي بتّيه؛ فلا يُقرَأ على مصدرٍ آخر ولو تطابقت قيمتا الخانتين."
)

A_BIT_SLOT_IS_NOT_A_LINGUISTIC_ROLE: Final[str] = (
    "ABitSlotIsNotALinguisticRole: خانةُ البتّ موضعٌ وقيمةٌ في مصدرٍ بايتيّ، "
    "لا حرفًا ولا صوتًا ولا مقطعًا ولا جذرًا ولا وزنًا ولا مدلولًا."
)

THE_BRIDGE_DOES_NOT_TOUCH_THE_BENEFIT: Final[str] = (
    "TheBridgeDoesNotTouchTheBenefit: الجسرُ يقرأ المصدرَ ولا يُدخِل شيئًا في "
    "اشتقاق الإفادة؛ والسَّوقُ قبله وبعده واحدٌ حكمًا وطبقةً ومانعًا وأثرًا."
)

A_REPEATED_VALUE_IS_NOT_A_PRESERVED_OCCURRENCE: Final[str] = (
    "ARepeatedValueIsNotAPreservedOccurrence: القيمةُ قد تتكرّر مئاتِ المرّات، "
    "ولكلِّ وقوعٍ موضعُه المستقلّ؛ فتكرارُ القيمة ليس حفظًا لهويّة الوقوع. "
    "وثلاثُ هويّاتٍ لا تُخلَط: قيمةُ البتّ، وموضعُه، والكلُّ الذي ينتمي إليه."
)

A_BIT_VALUE_IS_NOT_A_STRUCTURAL_SCALE: Final[str] = (
    "ABitValueIsNotAStructuralScale: بتّا `0` و`1` قيمتان في مصدرٍ بايتيّ، "
    "ومقياسا `zero` و`one` عددُ خاناتٍ في جبرٍ بنيويّ؛ فلا يُساوى بينهما، "
    "ولا يُقرَأ بلوغُ المقياس من قيمة البتّ."
)

TWO_SLOTS_ARE_NOT_THE_SCALE_COMPOSITION: Final[str] = (
    "TwoSlotsAreNotTheScaleComposition: نجاحُ خانتين على مصدرٍ واحدٍ شاهدٌ في "
    "نطاق خانتين لا غير. ولا يُركَّب صعودًا إلى البايتات كلِّها ولا إلى الوحدات "
    "الكتابيّة ولا اللغويّة؛ فبرهانُ كلِّ مقياسٍ يُطلَب على حدته، ولا يُفترَض "
    "من نجاح الحالة الصغرى. فمن سمّى هذا الجسرَ اتّصالًا بين جبر التعقّل واللغة "
    "كلِّها فقد عبَر انتقالًا لم يُقَس هنا."
)

UNPROVEN_SCALE_LADDER: Final[tuple[str, ...]] = (
    "bits → octets",
    "octets → graphemes",
    "graphemes → linguistic_units",
    "linguistic_units → ifada",
)
"""مقاييسُ التركيب التي لم يُطلَب برهانُها بعد؛ تُعَدّ ولا يُفترَض قطعُها."""

STRUCTURAL_BRIDGE_NAMED_LAWS: Final[tuple[str, ...]] = (
    THE_WITNESS_IS_BOUND_TO_ITS_SOURCE_AND_POSITIONS,
    A_BIT_SLOT_IS_NOT_A_LINGUISTIC_ROLE,
    A_REPEATED_VALUE_IS_NOT_A_PRESERVED_OCCURRENCE,
    A_BIT_VALUE_IS_NOT_A_STRUCTURAL_SCALE,
    TWO_SLOTS_ARE_NOT_THE_SCALE_COMPOSITION,
    THE_BRIDGE_DOES_NOT_TOUCH_THE_BENEFIT,
)
"""قوانينُ هذا الطور المُسمّاةُ؛ وكلٌّ منها مقيسٌ باختبارٍ لا مُصرَّحٌ وحسب."""


def _source_stamp(source: bytes) -> str:
    """صدرُ بصمةِ المصدر؛ به تُشدُّ هويّةُ الكلّ إلى بايتاته لا إلى قيمتيه."""

    return canonical_digest(source)[:16]


def _whole_id(stamp: str) -> str:
    """مُعرِّفُ الكلّ؛ مُشتَقٌّ من بصمة المصدر لا مكتوبٌ مع الجسر."""

    return f"whole.bridge.{stamp}"


def _anchor_id(stamp: str) -> str:
    """مِرساةُ الكلّ؛ مُشتَقّةٌ من بصمة المصدر."""

    return f"anchor.bridge.{stamp}"


@dataclass(frozen=True, slots=True)
class BitPosition:
    """موضعُ بتٍّ: رقمُ البايت، ورقمُ البتّ داخله من الأدنى قيمةً إلى الأعلى."""

    byte_index: int
    bit_index: int

    def __post_init__(self) -> None:
        for value, subject in (
            (self.byte_index, "رقمُ البايت"),
            (self.bit_index, "رقمُ البتّ"),
        ):
            if type(value) is not int:
                raise StructuralBridgeError(f"{subject} عددٌ صحيح.")
            if value < 0:
                raise StructuralBridgeError(f"{subject} لا يسبق الصفر.")
        if self.bit_index >= BITS_IN_A_BYTE:
            raise StructuralBridgeError(
                f"رقمُ البتّ دون {BITS_IN_A_BYTE}؛ ولا بتَّ تاسعٌ في بايت."
            )

    @property
    def position_id(self) -> str:
        """اسمُ الموضع؛ مُشتَقٌّ لا مكتوب."""

        return f"bit.{self.byte_index}.{self.bit_index}"

    @property
    def bit_offset(self) -> int:
        """إزاحةُ البتّ في السلسلة كلِّها؛ مُشتَقّةٌ من البايت والبتّ معًا."""

        return self.byte_index * BITS_IN_A_BYTE + self.bit_index

    @property
    def mask(self) -> int:
        """قناعُ البتّ داخل بايته."""

        return 1 << self.bit_index

    def read_from(self, source: bytes) -> int:
        """اقرأ قيمةَ البتّ من مصدرٍ بعينه، أو ارفض موضعًا خارج طوله."""

        if type(source) is not bytes:
            raise StructuralBridgeError("المصدرُ بايتاتٌ لا نصّ.")
        if self.byte_index >= len(source):
            raise StructuralBridgeError(
                f"موضعٌ خارج المصدر: البايتُ {self.byte_index} وطولُ المصدر "
                f"{len(source)}؛ ولا يُقرَأ ما ليس فيه."
            )
        return 1 if source[self.byte_index] & self.mask else 0


@dataclass(frozen=True, slots=True)
class BitSlotReading:
    """قراءةُ خانةٍ واحدة: موضعُها، وقيمتُها المستخرجةُ من المصدر المُصرَّح."""

    position: BitPosition
    value: int

    def __post_init__(self) -> None:
        if type(self.position) is not BitPosition:
            raise StructuralBridgeError("موضعُ الخانة موضعُ بتٍّ من نوعه.")
        if self.value not in (0, 1):
            raise StructuralBridgeError("قيمةُ البتّ صفرٌ أو واحد.")

    @property
    def occurrence_id(self) -> str:
        """هويّةُ الوقوع؛ موضعٌ وحدَه لا قيمةَ فيه، فلا يُوحِّدها تكرارُ القيمة."""

        return f"occurrence@{self.position.bit_offset}"

    @property
    def token(self) -> str:
        """رمزُ الخانة البنيويّ؛ وقوعٌ وقيمةٌ مفصولان لا حرفَ فيهما."""

        return f"{self.occurrence_id}:{self.position.position_id}={self.value}"

    @property
    def value_is_not_a_scale(self) -> str:
        """قانونُ نفي مساواة قيمة البتّ بمقياسٍ بنيويّ."""

        return A_BIT_VALUE_IS_NOT_A_STRUCTURAL_SCALE

    @property
    def what_it_is_not(self) -> str:
        """ما لا تكونه خانةُ البتّ مهما صحّت قراءتُها."""

        return A_BIT_SLOT_IS_NOT_A_LINGUISTIC_ROLE

    def agrees_with(self, source: bytes) -> bool:
        """أتوافق هذه القراءةُ مصدرًا بعينه عند موضعها؟"""

        try:
            return self.position.read_from(source) == self.value
        except StructuralBridgeError:
            return False


@dataclass(frozen=True, slots=True)
class ByteSlotBridge:
    """جسرٌ مُقاس: مصدرٌ بايتيّ، وقراءتا بتّين، وكلٌّ بنيويٌّ بخانتين."""

    source: bytes
    readings: tuple[BitSlotReading, ...]
    ascent: ScaleAscent

    @property
    def whole(self) -> StructuralWhole:
        """الكلُّ البنيويُّ بعد الصعود؛ مُشتَقٌّ من الصعود لا مُصرَّحٌ بجانبه."""

        return self.ascent.after

    def __post_init__(self) -> None:
        if type(self.source) is not bytes or not self.source:
            raise StructuralBridgeError("مصدرُ الجسر بايتاتٌ غيرُ فارغة.")
        if type(self.readings) is not tuple or (
            len(self.readings) != DECLARED_SLOT_COUNT
        ):
            raise StructuralBridgeError(
                f"الجسرُ {DECLARED_SLOT_COUNT} خانتين لا أقلَّ ولا أكثر."
            )
        occurrences = [reading.occurrence_id for reading in self.readings]
        if len(set(occurrences)) != len(occurrences):
            raise StructuralBridgeError(
                "وقوعٌ واحدٌ مُصرَّحٌ مرّتين ليس خانتين؛ و"
                + A_REPEATED_VALUE_IS_NOT_A_PRESERVED_OCCURRENCE
            )
        for reading in self.readings:
            if not reading.agrees_with(self.source):
                raise StructuralBridgeError(
                    f"قيمةُ {reading.position.position_id} لا تُستخرَج من هذا "
                    "المصدر؛ و" + THE_WITNESS_IS_BOUND_TO_ITS_SOURCE_AND_POSITIONS
                )
        if type(self.ascent) is not ScaleAscent:
            raise StructuralBridgeError("كلُّ الجسر يُبنى بصعودٍ مقيسٍ من نوعه.")
        if self.ascent.before.tokens != (self.readings[0].token,):
            raise StructuralBridgeError("كلُّ ما قبل الصعود خانةُ الوقوع الأوّل.")
        if self.whole.tokens != tuple(reading.token for reading in self.readings):
            raise StructuralBridgeError("رموزُ الكلّ هي رموزُ قراءاته بترتيبها.")
        stamp = _source_stamp(self.source)
        if self.whole.anchor_id != _anchor_id(stamp) or (
            self.ascent.before.whole_id != _whole_id(stamp)
        ):
            raise StructuralBridgeError(
                "مِرساةُ الكلّ مشدودةٌ إلى بصمة مصدره؛ و"
                + THE_WITNESS_IS_BOUND_TO_ITS_SOURCE_AND_POSITIONS
            )

    @property
    def source_digest(self) -> str:
        """بصمةُ المصدر الخامّ كما ورد."""

        return canonical_digest(self.source)

    @property
    def byte_length(self) -> int:
        """طولُ المصدر بالبايت."""

        return len(self.source)

    @property
    def positions(self) -> tuple[BitPosition, ...]:
        """موضعا البتّين بترتيب تصريحهما."""

        return tuple(reading.position for reading in self.readings)

    @property
    def values(self) -> tuple[int, ...]:
        """قيمتا البتّين المستخرجتان."""

        return tuple(reading.value for reading in self.readings)

    @property
    def witness_id(self) -> str:
        """هويّةُ الشاهد: بصمةُ المصدر وطولُه وموضعاه؛ مُشتَقّةٌ لا مكتوبة."""

        return canonical_digest(
            "|".join(
                (
                    self.source_digest,
                    str(self.byte_length),
                    *(position.position_id for position in self.positions),
                )
            ).encode("utf-8")
        )

    @property
    def proven_scale_span(self) -> int:
        """مدى البرهان بالخانات؛ وهو حدُّ الطور لا اختيارَ هذا الجسر."""

        return self.whole.slot_count

    @property
    def unreached_scales(self) -> tuple[str, ...]:
        """المقاييسُ التي لم يبلغها هذا الشاهد؛ مُسمّاةً معدودةً لا مطويّة."""

        return UNPROVEN_SCALE_LADDER

    @property
    def reaches_the_whole_source(self) -> bool:
        """أيبلغ الشاهدُ بايتاتِ المصدر كلَّها؟ والجواب مقيسٌ لا مُصرَّح."""

        return self.proven_scale_span == len(self.source) * BITS_IN_A_BYTE

    @property
    def occurrence_ids(self) -> tuple[str, ...]:
        """هويّتا الوقوعين بترتيبهما؛ موضعان لا قيمتان."""

        return tuple(reading.occurrence_id for reading in self.readings)

    @property
    def preserves_instance_identity(self) -> bool:
        """أبقيت عينُ المِرساة عبر الصعود من خانةٍ إلى خانتين؟"""

        return self.ascent.preserves_instance_identity

    @property
    def trace_is_cumulative(self) -> bool:
        """أزاد أثرُ الصعود خطوةً واحدةً فوق سابقه بلا إعادة بناء؟"""

        return self.ascent.trace_is_cumulative

    @property
    def trace_steps(self) -> int:
        """عددُ خطوات أثر الكلّ بعد الصعود."""

        return self.whole.trace_steps

    @property
    def decompositions(self) -> tuple[StructuralDecomposition, ...]:
        """تفكيكُ الكلّ على كلِّ فرضيّاته؛ بلا ترجيحٍ ولا حذف."""

        return tuple(
            decompose(self.whole, hypothesis)
            for hypothesis in self.hypotheses.hypotheses
        )

    @property
    def residuals(self) -> tuple[ResidualReading, ...]:
        """بقايا التفكيكات مجموعةً؛ وهي التي تحجب كلَّ ترقية."""

        return tuple(
            reading
            for decomposition in self.decompositions
            for reading in decomposition.residuals
        )

    @property
    def every_partition_is_blocked(self) -> bool:
        """أمحجوبٌ كلُّ تقسيمٍ عن الترقية؟ فلا يُرفَع واحدٌ منها إلى دور."""

        return all(
            decomposition.promotion_standing is PromotionStanding.PROMOTION_BLOCKED
            for decomposition in self.decompositions
        )

    @property
    def hypotheses(self) -> ShapePartitionHypothesisSet:
        """تقسيماتُ الكلّ كاملةً بلا فائزٍ مفروض."""

        return enumerate_shape_partitions(self.whole)

    @property
    def what_it_is_not(self) -> tuple[str, ...]:
        """ما لا يُثبِته الجسرُ: دورٌ لغويّ، وتركيبُ المقاييس، وأجناسُ التقسيم."""

        return (
            A_BIT_SLOT_IS_NOT_A_LINGUISTIC_ROLE,
            TWO_SLOTS_ARE_NOT_THE_SCALE_COMPOSITION,
            *self.hypotheses.what_it_is_not,
        )

    def rebuilds_from(self, source: bytes) -> bool:
        """أتُعاد قراءةُ الخانتين من مصدرٍ بعينه فتُطابق هذا الشاهدَ كلَّه؟"""

        return all(reading.agrees_with(source) for reading in self.readings)

    def as_canonical_content(self) -> dict[str, object]:
        """محتوى الجسر للعرض والمقارنة."""

        return {
            "source_digest": self.source_digest,
            "byte_length": self.byte_length,
            "witness_id": self.witness_id,
            "readings": [
                [reading.position.position_id, reading.value]
                for reading in self.readings
            ],
            "occurrence_ids": list(self.occurrence_ids),
            "tokens": list(self.whole.tokens),
            "trace_steps": self.trace_steps,
            "content_id": self.whole.content_id,
            "hypothesis_count": self.hypotheses.count,
        }


def bridge_two_bits(
    source: bytes, first: BitPosition, second: BitPosition
) -> ByteSlotBridge:
    """ابنِ جسرًا على موضعَي بتٍّ مُصرَّحين من مصدرٍ بايتيٍّ بعينه."""

    if type(source) is not bytes or not source:
        raise StructuralBridgeError("مصدرُ الجسر بايتاتٌ غيرُ فارغة.")
    readings = tuple(
        BitSlotReading(position=position, value=position.read_from(source))
        for position in (first, second)
    )
    stamp = _source_stamp(source)
    zero = origin_whole(
        whole_id=_whole_id(stamp),
        anchor_id=_anchor_id(stamp),
        carrier_id=f"carrier.bridge.{stamp}",
        tokens=(readings[0].token,),
    )
    ascent = ascend_one_slot(
        zero,
        readings[1].token,
        mode=IdentityTransitionMode.SAME_ENTITY_RESCALING,
    )
    return ByteSlotBridge(source=source, readings=readings, ascent=ascent)


@dataclass(frozen=True, slots=True)
class PathComparison:
    """مقارنةُ سَوقِ المصدر قبل الجسر وبعده؛ والجسرُ لا يدخل بينهما."""

    bridge: ByteSlotBridge
    before: PathRun
    after: PathRun

    def __post_init__(self) -> None:
        if type(self.bridge) is not ByteSlotBridge:
            raise StructuralBridgeError("المقارنةُ تقع على جسرٍ من نوعه.")
        for run in (self.before, self.after):
            if type(run) is not PathRun:
                raise StructuralBridgeError("طرفا المقارنة سَوقان من نوعهما.")
            if run.source != self.bridge.source:
                raise StructuralBridgeError(
                    "طرفا المقارنة يُساقان على بايتات الجسر عينِها."
                )

    @property
    def the_benefit_is_unchanged(self) -> bool:
        """أبقيت الإفادةُ على حالها قبل الجسر وبعده؟"""

        return self.before.ifada is self.after.ifada

    @property
    def the_whole_run_is_unchanged(self) -> bool:
        """أبقي السَّوقُ كلُّه واحدًا: طبقةً وحكمًا ومانعًا وأثرًا؟"""

        return (
            self.before.reached is self.after.reached
            and self.before.outcome is self.after.outcome
            and self.before.stop is self.after.stop
            and self.before.trace.events == self.after.trace.events
            and self.the_benefit_is_unchanged
        )

    @property
    def refusal(self) -> str:
        """قانونُ امتناع الجسر عن الإفادة."""

        return THE_BRIDGE_DOES_NOT_TOUCH_THE_BENEFIT


def compare_with_the_path(bridge: ByteSlotBridge) -> PathComparison:
    """سُق بايتاتِ الجسر قبله وبعده، وقِس أنّ شيئًا لم يتغيّر."""

    if type(bridge) is not ByteSlotBridge:
        raise StructuralBridgeError("المقارنةُ تقع على جسرٍ من نوعه.")
    before = run_bytes(bridge.source)
    after = run_bytes(bridge.source)
    return PathComparison(bridge=bridge, before=before, after=after)


def render_bridge(bridge: ByteSlotBridge) -> str:
    """اعرض الجسرَ بهويّة شاهده وموضعيه وقيمتيه؛ ولا تعرض حكمًا لا يملكه."""

    if type(bridge) is not ByteSlotBridge:
        raise StructuralBridgeError("العرضُ يقع على جسرٍ من نوعه.")
    lines = [
        f"بصمةُ المصدر: {bridge.source_digest}",
        f"طولُ المصدر: {bridge.byte_length} بايتًا",
        f"هويّةُ الشاهد: {bridge.witness_id}",
        "",
        "| الموضع | القيمة | رمزُ الخانة |",
        "| --- | --- | --- |",
    ]
    lines.extend(
        f"| {reading.position.position_id} | {reading.value} | {reading.token} |"
        for reading in bridge.readings
    )
    lines.extend(
        [
            "",
            f"بصمةُ الكلّ البنيويّ: {bridge.whole.content_id}",
            f"خطواتُ الأثر: {bridge.trace_steps} — متراكمٌ: "
            f"{bridge.trace_is_cumulative}",
            f"البقايا الحاجبة: {len(bridge.residuals)} — كلُّ تقسيمٍ محجوب: "
            f"{bridge.every_partition_is_blocked}",
            f"عددُ التقسيمات: {bridge.hypotheses.count} بلا فائزٍ مفروض",
            f"مدى البرهان: {bridge.proven_scale_span} خانةً — يبلغ المصدرَ "
            f"كلَّه: {bridge.reaches_the_whole_source}",
            "مقاييسُ لم تُبلَغ: " + "، ".join(bridge.unreached_scales),
            "",
            "ما لا يُثبِته هذا الجسر:",
        ]
    )
    lines.extend(f"  - {refusal}" for refusal in bridge.what_it_is_not)
    return "\n".join(lines)


def _refuse_an_unnamed_law() -> None:
    """ارفض عند الاستيراد قانونًا بلا اسمٍ مُصدَّرٍ أو مُكرَّرًا في مجموعته."""

    if len(set(STRUCTURAL_BRIDGE_NAMED_LAWS)) != len(STRUCTURAL_BRIDGE_NAMED_LAWS):
        raise StructuralBridgeError("قانونٌ مُكرَّرٌ في مجموعة قوانين الجسر.")
    for law in STRUCTURAL_BRIDGE_NAMED_LAWS:
        head = law.split(":", 1)[0]
        if not head or not head[0].isupper() or " " in head:
            raise StructuralBridgeError(f"قانونٌ بلا اسمٍ مُفرَدٍ في صدره: {law[:40]}")


_refuse_an_unnamed_law()
