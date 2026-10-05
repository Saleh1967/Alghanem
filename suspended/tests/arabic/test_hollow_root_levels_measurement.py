"""اختبارُ قياسِ السُّلَّم: الطبقاتُ الستّ بأعيانها، وانقلابُ ترتيب الدقّة."""

from __future__ import annotations

import pytest

from alghanem.arabic.hollow_root_levels_measurement import (
    MEASUREMENT_NAMED_RESIDUALS,
    TEMPLATE_AND_STATE,
    CollisionClass,
    HollowRootLevelsMeasurementError,
    collision_classes,
    combined_fingerprint,
    level_fingerprint,
    read_all_levels,
    read_level,
    surfaces_the_level_separates,
    template_and_state_collisions,
)
from alghanem.arabic.hollow_root_levels_preregistration import (
    FROZEN_SURFACES,
    LEVEL_ORDER,
    HollowRootLevel,
)

_EXPECTED_TEMPLATE_AND_STATE_CLASSES: tuple[
    tuple[tuple[str, str], tuple[str, ...]], ...
] = (
    (
        ("CVV-CV", "fatha-sukun_implicit-fatha"),
        ("قَالَ", "بَاعَ", "خَافَ", "نَامَ", "هَابَ"),
    ),
    (("CVV-CV", "kasra-sukun_implicit-fatha"), ("قِيلَ", "بِيعَ")),
    (
        ("CV-CVV-CV", "damma-fatha-sukun_implicit-damma"),
        ("يُقَالُ", "يُبَاعُ"),
    ),
    (
        ("CVC-CVC", "fatha-sukun_explicit-damma"),
        ("قَوْلٌ", "بَيْعٌ", "خَوْفٌ", "نَوْمٌ"),
    ),
    (
        ("CVV-CV-CVC", "fatha-sukun_implicit-kasra-damma"),
        ("قَائِلٌ", "بَائِعٌ", "خَائِفٌ", "نَائِمٌ"),
    ),
    (
        ("CV-CVV-CV", "fatha-fatha-sukun_implicit-damma"),
        ("يَخَافُ", "يَنَامُ", "يَهَابُ"),
    ),
)


def test_the_six_collision_classes_are_pinned_by_value() -> None:
    measured = {
        collision.fingerprint: collision.surfaces
        for collision in template_and_state_collisions()
    }
    expected = {
        fingerprint: surfaces
        for fingerprint, surfaces in _EXPECTED_TEMPLATE_AND_STATE_CLASSES
    }
    assert measured == expected


def test_the_claim_of_no_collision_under_template_and_state_inverts() -> None:
    assert len(template_and_state_collisions()) == 6
    distinct = {
        combined_fingerprint(item.surface, TEMPLATE_AND_STATE)
        for item in FROZEN_SURFACES
    }
    assert len(FROZEN_SURFACES) == 24
    assert len(distinct) == 10


def test_the_strongest_collision_keeps_waw_and_ya_visible_yet_unread() -> None:
    """قَوْلٌ/بَيْعٌ/خَوْفٌ/نَوْمٌ: و/ي ظاهرتان في الرسم، والبصمةُ لا تفرّق."""

    classes = {
        collision.fingerprint: collision
        for collision in template_and_state_collisions()
    }
    strongest = classes[("CVC-CVC", "fatha-sukun_explicit-damma")]
    assert strongest.surfaces == ("قَوْلٌ", "بَيْعٌ", "خَوْفٌ", "نَوْمٌ")
    assert strongest.declared_roots == ("بيع", "خوف", "قول", "نوم")


def test_the_mudari_fatha_pattern_is_blind_to_the_weak_radical() -> None:
    """يَخَافُ (واويّ) و يَهَابُ (يائيّ) بصمةٌ واحدة: حدٌّ مُسجَّلٌ هنا قبل الدعوى."""

    assert combined_fingerprint("يَخَافُ", TEMPLATE_AND_STATE) == combined_fingerprint(
        "يَهَابُ", TEMPLATE_AND_STATE
    )
    roots = {item.surface: item.declared_root for item in FROZEN_SURFACES}
    assert roots["يَخَافُ"] != roots["يَهَابُ"]


def test_level_zero_inverts_between_its_two_named_projections() -> None:
    """بإسقاط العلامات وحدها لا تصادم، وبإسقاط حامل المدّ معها يقع."""

    stripped = HollowRootLevel.HARAKAT_STRIPPED
    madd_dropped = HollowRootLevel.MADD_ALSO_DROPPED
    assert level_fingerprint("قَالَ", stripped) != level_fingerprint("قُلْ", stripped)
    assert level_fingerprint("قَالَ", madd_dropped) == level_fingerprint(
        "قُلْ", madd_dropped
    )


def test_a_later_level_is_not_necessarily_a_finer_one() -> None:
    """عددُ البصمات المتمايزة ينخفض مع تقدّم السُّلَّم، فالترتيبُ ترتيبُ تسميةٍ."""

    counts = [reading.distinct_fingerprint_count for reading in read_all_levels()]
    assert counts == [23, 18, 5, 10]
    assert counts[-1] < counts[0]


def test_collisions_are_grouped_not_compared_pairwise() -> None:
    """طبقةٌ خماسيّةٌ تخرج بأعضائها الخمسة، لا ثنائيّةً كما يُخرِجها الدهس."""

    quintet = next(
        collision
        for collision in template_and_state_collisions()
        if "قَالَ" in collision.surfaces
    )
    assert len(quintet.surfaces) == 5


def test_a_collision_class_of_one_is_refused() -> None:
    with pytest.raises(HollowRootLevelsMeasurementError):
        CollisionClass(
            levels=TEMPLATE_AND_STATE,
            fingerprint=("CVV-CV", "fatha-sukun_implicit-fatha"),
            surfaces=("قَالَ",),
        )


def test_a_surface_outside_the_frozen_set_is_refused() -> None:
    with pytest.raises(HollowRootLevelsMeasurementError):
        level_fingerprint("سَارَ", HollowRootLevel.SYLLABLE_TEMPLATE_SEQUENCE)


def test_the_first_level_is_credited_with_no_separation_at_all() -> None:
    with pytest.raises(HollowRootLevelsMeasurementError):
        surfaces_the_level_separates(LEVEL_ORDER[0])


def test_a_level_separates_only_where_its_predecessor_collided() -> None:
    separated = surfaces_the_level_separates(HollowRootLevel.MADD_ALSO_DROPPED)
    collided = {
        surface
        for collision in collision_classes(HollowRootLevel.HARAKAT_STRIPPED)
        for surface in collision.surfaces
    }
    for first, second in separated:
        assert first in collided and second in collided


def test_every_reading_covers_the_whole_frozen_set() -> None:
    for reading in read_all_levels():
        assert len(reading.fingerprints) == len(FROZEN_SURFACES)


def test_reading_a_level_needs_a_level_member_not_a_string() -> None:
    with pytest.raises(HollowRootLevelsMeasurementError):
        combined_fingerprint("قَالَ", ("SYLLABLE_TEMPLATE_SEQUENCE",))  # type: ignore[arg-type]


def test_the_combined_fingerprint_follows_the_frozen_order() -> None:
    forward = combined_fingerprint("قَالَ", TEMPLATE_AND_STATE)
    backward = tuple(reversed(TEMPLATE_AND_STATE))
    reversed_request = combined_fingerprint("قَالَ", backward)
    assert forward == reversed_request


def test_the_named_residuals_are_present() -> None:
    assert MEASUREMENT_NAMED_RESIDUALS
    assert all(note.strip() for note in MEASUREMENT_NAMED_RESIDUALS)


def test_a_single_level_reading_is_not_cumulative() -> None:
    reading = read_level(HollowRootLevel.CARRIER_STATE_SEQUENCE)
    for _, fingerprint in reading.fingerprints:
        assert len(fingerprint) == 1
