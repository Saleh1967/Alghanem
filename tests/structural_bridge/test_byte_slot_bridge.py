"""اختباراتُ جسر البتّين: من بايتاتٍ حقيقيّةٍ إلى خانتين بنيويّتين لا غير."""

from __future__ import annotations

import ast
from pathlib import Path

import pytest

from alghanem.arabic.composition_ifada_path import IfadaStanding, PathStage, run_bytes
from alghanem.structural_bridge import (
    A_BIT_SLOT_IS_NOT_A_LINGUISTIC_ROLE,
    STRUCTURAL_BRIDGE_NAMED_LAWS,
    THE_BRIDGE_DOES_NOT_TOUCH_THE_BENEFIT,
    THE_WITNESS_IS_BOUND_TO_ITS_SOURCE_AND_POSITIONS,
    BitPosition,
    BitSlotReading,
    ByteSlotBridge,
    StructuralBridgeError,
    bridge_two_bits,
    compare_with_the_path,
    render_bridge,
)

_ISNAD = "اللَّهُ نُورٌ".encode()
_IDAFA = "بيتُ اللَّهِ".encode()
_FIRST = BitPosition(byte_index=0, bit_index=0)
_SECOND = BitPosition(byte_index=1, bit_index=7)


def _flip(source: bytes, position: BitPosition) -> bytes:
    """ابدِل بتًّا واحدًا في مصدرٍ بايتيّ، والطولُ باقٍ على حاله."""

    mutable = bytearray(source)
    mutable[position.byte_index] ^= position.mask
    return bytes(mutable)


# ————— الخانتان مستخرجتان من هذا المصدر بعينه —————


def test_each_slot_value_is_extracted_from_the_declared_source() -> None:
    """قيمةُ كلِّ خانةٍ مقروءةٌ من المصدر عند موضعها، لا مُصرَّحةٌ مع الجسر."""

    bridge = bridge_two_bits(_ISNAD, _FIRST, _SECOND)

    assert bridge.source == _ISNAD
    assert bridge.values == (
        _FIRST.read_from(_ISNAD),
        _SECOND.read_from(_ISNAD),
    )
    for reading in bridge.readings:
        assert reading.agrees_with(_ISNAD)
        assert reading.token.endswith(f"={reading.value}")


def test_the_bridge_carries_exactly_two_slots_in_a_structural_whole() -> None:
    """الجسرُ خانتان في كلٍّ بنيويّ، ورموزُ الكلّ هي رموزُ القراءتين بترتيبهما."""

    bridge = bridge_two_bits(_ISNAD, _FIRST, _SECOND)

    assert len(bridge.readings) == 2
    assert bridge.whole.slot_count == 2
    assert bridge.whole.tokens == tuple(r.token for r in bridge.readings)
    assert bridge.hypotheses.count > 1
    assert bridge.hypotheses.forced_winner is None


def test_the_witness_is_bound_to_its_digest_length_and_positions() -> None:
    """هويّةُ الشاهد مشدودةٌ إلى بصمة المصدر وطولِه وموضعيه، وتتغيّر بتغيّر أيّها."""

    bridge = bridge_two_bits(_ISNAD, _FIRST, _SECOND)
    other_positions = bridge_two_bits(
        _ISNAD, _FIRST, BitPosition(byte_index=1, bit_index=6)
    )
    other_source = bridge_two_bits(_IDAFA, _FIRST, _SECOND)

    assert len(bridge.witness_id) == 64
    assert bridge.witness_id != other_positions.witness_id
    assert bridge.witness_id != other_source.witness_id
    assert bridge.source_digest != other_source.source_digest
    assert bridge.byte_length == len(_ISNAD)


def test_the_bridge_rebuilds_its_readings_from_its_own_source() -> None:
    """إعادةُ القراءة من المصدر نفسِه تُطابق الشاهد، ومن غيره لا تُلزِم."""

    bridge = bridge_two_bits(_ISNAD, _FIRST, _SECOND)

    assert bridge.rebuilds_from(_ISNAD)
    assert bridge_two_bits(_IDAFA, _FIRST, _SECOND).rebuilds_from(_IDAFA)


# ————— تبديلُ البتّ —————


def test_flipping_a_declared_bit_changes_the_slot_value_and_the_whole() -> None:
    """تبديلُ بتٍّ مُصرَّحٍ فرقٌ قادح: القيمةُ تنقلب والبصمةُ تتغيّر والطولُ باقٍ."""

    original = bridge_two_bits(_ISNAD, _FIRST, _SECOND)
    mutated_source = _flip(_ISNAD, _FIRST)
    mutated = bridge_two_bits(mutated_source, _FIRST, _SECOND)

    assert len(mutated_source) == len(_ISNAD)
    assert mutated_source != _ISNAD
    assert mutated.values[0] == 1 - original.values[0]
    assert mutated.values[1] == original.values[1]
    assert mutated.whole.content_id != original.whole.content_id
    assert mutated.witness_id != original.witness_id


def test_a_witness_of_the_original_does_not_rebuild_from_the_flipped_source() -> None:
    """شاهدُ الأصل لا يُعاد بناؤه من مصدرٍ بُدِّل بتُّه، وهذا هو موضع الكشف."""

    original = bridge_two_bits(_ISNAD, _FIRST, _SECOND)

    assert not original.rebuilds_from(_flip(_ISNAD, _FIRST))


def test_a_reading_that_contradicts_its_source_is_refused() -> None:
    """قراءةٌ تخالف مصدرَها مردودةٌ باسم قانونها، ولا تُصحَّح ولا تُبتلَع."""

    bridge = bridge_two_bits(_ISNAD, _FIRST, _SECOND)
    lying = BitSlotReading(position=_FIRST, value=1 - bridge.values[0])

    with pytest.raises(StructuralBridgeError):
        ByteSlotBridge(
            source=_ISNAD,
            readings=(lying, bridge.readings[1]),
            whole=bridge.whole,
        )


def test_flipping_an_undeclared_bit_leaves_the_slot_values_alone() -> None:
    """تبديلُ بتٍّ خارج الموضعين لا يُغيّر القيمتين، ويُغيّر بصمةَ المصدر وحدَها."""

    elsewhere = BitPosition(byte_index=4, bit_index=3)
    original = bridge_two_bits(_ISNAD, _FIRST, _SECOND)
    mutated = bridge_two_bits(_flip(_ISNAD, elsewhere), _FIRST, _SECOND)

    assert mutated.values == original.values
    assert mutated.source_digest != original.source_digest
    assert mutated.witness_id != original.witness_id


# ————— إسقاطُ البتّ —————


def test_a_position_past_the_end_of_the_source_is_refused() -> None:
    """موضعٌ خارج طول المصدر مردودٌ باسمه، ولا يُقرَأ صفرًا ضمنيًّا."""

    short = _ISNAD[:2]

    with pytest.raises(StructuralBridgeError):
        bridge_two_bits(short, _FIRST, BitPosition(byte_index=9, bit_index=0))
    with pytest.raises(StructuralBridgeError):
        BitPosition(byte_index=9, bit_index=0).read_from(short)


def test_dropping_the_trailing_bytes_can_drop_a_declared_position() -> None:
    """إسقاطُ بايتاتٍ من الذيل قد يُسقِط موضعًا مُصرَّحًا، فيقف الجسرُ ولا يُقدّر."""

    tail = BitPosition(byte_index=len(_ISNAD) - 1, bit_index=0)
    full = bridge_two_bits(_ISNAD, _FIRST, tail)

    assert full.rebuilds_from(_ISNAD)
    assert not full.rebuilds_from(_ISNAD[:-1])
    with pytest.raises(StructuralBridgeError):
        bridge_two_bits(_ISNAD[:-1], _FIRST, tail)


def test_a_ninth_bit_in_a_byte_is_refused() -> None:
    """لا بتَّ تاسعٌ في بايت؛ والموضعُ فوق السابع مردودٌ عند بنائه."""

    with pytest.raises(StructuralBridgeError):
        BitPosition(byte_index=0, bit_index=8)
    with pytest.raises(StructuralBridgeError):
        BitPosition(byte_index=0, bit_index=-1)


def test_an_empty_source_is_not_bridged() -> None:
    """مصدرٌ فارغٌ لا يُجسَر، فلا بتَّ فيه يُستخرَج."""

    with pytest.raises(StructuralBridgeError):
        bridge_two_bits(b"", _FIRST, _SECOND)


def test_one_position_declared_twice_is_not_two_slots() -> None:
    """موضعٌ واحدٌ مُصرَّحٌ مرّتين ليس خانتين، ولا يُعدُّ تقسيمًا ثنائيًّا."""

    bridge = bridge_two_bits(_ISNAD, _FIRST, _SECOND)
    doubled = (bridge.readings[0], bridge.readings[0])

    with pytest.raises(StructuralBridgeError):
        ByteSlotBridge(source=_ISNAD, readings=doubled, whole=bridge.whole)


def test_a_bridge_of_one_or_three_slots_is_refused() -> None:
    """الجسرُ خانتان لا أقلَّ ولا أكثر؛ وما خالف مردودٌ عند بنائه."""

    bridge = bridge_two_bits(_ISNAD, _FIRST, _SECOND)
    third = BitSlotReading(
        position=(extra := BitPosition(byte_index=2, bit_index=1)),
        value=extra.read_from(_ISNAD),
    )

    with pytest.raises(StructuralBridgeError):
        ByteSlotBridge(
            source=_ISNAD, readings=(bridge.readings[0],), whole=bridge.whole
        )
    with pytest.raises(StructuralBridgeError):
        ByteSlotBridge(
            source=_ISNAD, readings=(*bridge.readings, third), whole=bridge.whole
        )


# ————— تبادلُ شاهدِ مصدرين —————


def test_a_witness_of_one_source_is_refused_over_another() -> None:
    """شاهدُ مصدرٍ لا يُركَّب على مصدرٍ آخر ولو صحّت صورتُه، فالقرانُ ببصمته."""

    first = bridge_two_bits(_ISNAD, _FIRST, _SECOND)

    with pytest.raises(StructuralBridgeError):
        ByteSlotBridge(source=_IDAFA, readings=first.readings, whole=first.whole)


def test_two_sources_that_agree_on_two_bits_keep_distinct_witnesses() -> None:
    """مصدران يتّفقان في البتّين لا يتّحد شاهداهما؛ فالبصمةُ داخلةٌ في الهويّة."""

    twin = _flip(_ISNAD, BitPosition(byte_index=4, bit_index=3))
    left = bridge_two_bits(_ISNAD, _FIRST, _SECOND)
    right = bridge_two_bits(twin, _FIRST, _SECOND)

    assert left.values == right.values
    assert left.whole.tokens == right.whole.tokens
    assert left.source_digest != right.source_digest
    assert left.witness_id != right.witness_id
    assert left.as_canonical_content() != right.as_canonical_content()


def test_a_comparison_is_refused_over_a_run_of_another_source() -> None:
    """المقارنةُ لا تقبل سَوقًا على بايتاتٍ غير بايتات جسرها."""

    bridge = bridge_two_bits(_ISNAD, _FIRST, _SECOND)
    comparison = compare_with_the_path(bridge)

    with pytest.raises(StructuralBridgeError):
        type(comparison)(
            bridge=bridge, before=comparison.before, after=run_bytes(_IDAFA)
        )


# ————— الجسرُ لا يُغيّر الإفادة —————


def test_the_run_is_unchanged_before_and_after_the_bridge() -> None:
    """السَّوقُ قبل الجسر وبعده واحدٌ: طبقةً وحكمًا ومانعًا وأثرًا وإفادة."""

    bridge = bridge_two_bits(_ISNAD, _FIRST, _SECOND)
    comparison = compare_with_the_path(bridge)

    assert comparison.the_benefit_is_unchanged
    assert comparison.the_whole_run_is_unchanged
    assert comparison.before.trace.events == comparison.after.trace.events
    assert comparison.refusal == THE_BRIDGE_DOES_NOT_TOUCH_THE_BENEFIT


def test_the_benefit_of_a_bridged_source_equals_the_benefit_without_it() -> None:
    """إفادةُ مصدرٍ جُسِر هي إفادتُه غيرَ مجسور، فالجسرُ خارج اشتقاقها."""

    standalone = run_bytes(_ISNAD)
    bridged = compare_with_the_path(bridge_two_bits(_ISNAD, _FIRST, _SECOND))

    assert standalone.ifada is bridged.after.ifada
    assert standalone.reached is bridged.after.reached
    assert standalone.trace.events == bridged.after.trace.events
    assert standalone.ifada is IfadaStanding.مُفيد
    assert standalone.reached is PathStage.IFADA


def test_a_bridge_over_an_unreadable_source_still_changes_nothing() -> None:
    """مصدرٌ لا تُقرأ إفادتُه يُجسَر ولا تتحرّك حالُه: غيرُ مقروءٍ قبلُ وبعدُ."""

    single = "كلمة".encode()
    comparison = compare_with_the_path(bridge_two_bits(single, _FIRST, _SECOND))

    assert comparison.before.ifada is IfadaStanding.غير_مقروء
    assert comparison.the_whole_run_is_unchanged


def test_the_bridge_exposes_no_benefit_and_no_certificate() -> None:
    """الجسرُ لا يحمل إفادةً ولا شهادةً ولا حكمَ مطابقةٍ للواقع."""

    bridge = bridge_two_bits(_ISNAD, _FIRST, _SECOND)

    for field_name in ("ifada", "benefit", "certificate", "verdict", "role"):
        assert not hasattr(bridge, field_name)
    for reading in bridge.readings:
        assert not hasattr(reading, "role")


# ————— ما لا يُثبِته الجسر —————


def test_the_bridge_names_the_five_genera_it_does_not_reach() -> None:
    """الجسرُ يُسمّي ما لا يبلغه: دورًا لغويًّا، وجذرًا، ووزنًا، ومدلولًا، وإفادة."""

    bridge = bridge_two_bits(_ISNAD, _FIRST, _SECOND)
    refusals = bridge.what_it_is_not

    assert refusals[0] == A_BIT_SLOT_IS_NOT_A_LINGUISTIC_ROLE
    assert len(refusals) == 5
    assert len(set(refusals)) == 5
    for refusal in refusals:
        assert refusal.strip()


def test_every_named_law_carries_a_single_name_in_its_head() -> None:
    """كلُّ قانونٍ مُسمًّى يصدّر باسمٍ مفردٍ ثمّ شرحِه، ولا قانونَ مُكرَّر."""

    assert STRUCTURAL_BRIDGE_NAMED_LAWS
    for law in STRUCTURAL_BRIDGE_NAMED_LAWS:
        head = law.split(":", 1)[0]
        assert head[0].isupper()
        assert " " not in head
    assert THE_WITNESS_IS_BOUND_TO_ITS_SOURCE_AND_POSITIONS in (
        STRUCTURAL_BRIDGE_NAMED_LAWS
    )


def test_the_rendered_bridge_publishes_its_bindings_and_its_limits() -> None:
    """العرضُ يُظهر البصمةَ والموضعين وهويّةَ الشاهد وما لا يُثبِته، بلا حكمٍ زائد."""

    bridge = bridge_two_bits(_ISNAD, _FIRST, _SECOND)
    rendered = render_bridge(bridge)

    assert bridge.source_digest in rendered
    assert bridge.witness_id in rendered
    assert bridge.whole.content_id in rendered
    for reading in bridge.readings:
        assert reading.position.position_id in rendered
    for refusal in bridge.what_it_is_not:
        assert refusal in rendered


def test_the_bridge_is_the_only_module_joining_the_algebra_to_the_path() -> None:
    """الجسرُ وحدَه يجمع الجبرَ بالمسار؛ ولا وحدةَ أخرى تفعل ذلك في الشجرة."""

    source = Path("src/alghanem").resolve()
    bridge_dir = source / "structural_bridge"
    joiners = sorted(
        str(path.relative_to(source))
        for path in source.rglob("*.py")
        if "structural_dal" in (text := path.read_text(encoding="utf-8"))
        and "composition_ifada_path" in text
    )

    assert joiners
    for joiner in joiners:
        assert (source / joiner).parent == bridge_dir


def test_the_arabic_path_still_reads_nothing_from_the_bridge() -> None:
    """المسارُ العربيُّ لا يستورد الجسرَ ولا الجبر؛ فالاتّجاهُ واحدٌ لا يُعكَس."""

    arabic = Path("src/alghanem/arabic").resolve()
    readers = sorted(
        path.name
        for path in arabic.rglob("*.py")
        for node in ast.walk(ast.parse(path.read_text(encoding="utf-8")))
        if isinstance(node, ast.ImportFrom)
        and (node.module or "").startswith(
            ("alghanem.structural_dal", "alghanem.structural_bridge")
        )
    )

    assert readers == []


def test_the_structural_whole_is_anchored_in_the_source_digest() -> None:
    """مِرساةُ الكلّ مُشتَقّةٌ من بصمة المصدر، فلا تُعار لمصدرٍ يوافقه في البتّين."""

    twin = _flip(_ISNAD, BitPosition(byte_index=4, bit_index=3))
    left = bridge_two_bits(_ISNAD, _FIRST, _SECOND)
    right = bridge_two_bits(twin, _FIRST, _SECOND)

    assert left.whole.tokens == right.whole.tokens
    assert left.whole.anchor_id != right.whole.anchor_id
    assert left.source_digest[:16] in left.whole.anchor_id
    with pytest.raises(StructuralBridgeError):
        ByteSlotBridge(source=twin, readings=right.readings, whole=left.whole)
