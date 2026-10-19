"""قياسُ سُلَّمِ المستويات على الجذر الأجوف: بصماتٌ تُشتَقّ، وتصادماتٌ تُجمَع.

هذه وحدةُ **القياس** وحدها. الصورُ والإسقاطاتُ والتوقّعُ مُجمَّدةٌ قبلها في
`hollow_root_levels_preregistration`، وتُطابَق بصمتُها عند الاستيراد؛ فصورةٌ
تُزاد بعد التجميد تُسقِط هذه القراءةَ ولا تمرّ بصمت.

`A_COLLISION_IS_FOUND_BY_GROUPING_NOT_BY_PAIRWISE_COMPARISON`: التصادمُ يُكشَف
بتجميع الصور تحت بصمتها الواحدة، لا بمقارنة كلّ صورةٍ بسابقتها. وهذا ليس
تفضيلَ أسلوب: السكربتُ الوارد من المحادثة الخارجية قارَن كلَّ صورةٍ **بآخر
صورةٍ وحدها** وكان يشترط لإعلان التصادم **اختلافَ الحالات** — فمرّ أشدُّ ما في
عيّنته صامتًا (`قَوْلٌ`/`بَيْعٌ`/`خَوْفٌ`/`نَوْمٌ` متطابقةً تطابقًا تامًّا)، وقُرِئ
تصادمٌ رباعيٌّ ثنائيًّا. والتجميعُ يُخرِج الطبقةَ كاملةً بأعضائها.

`A_TOTAL_COLLISION_IS_THE_STRONGEST_ONE_NOT_THE_INVISIBLE_ONE`: تطابقُ القالب
**والحالة معًا** أشدُّ التصادم لا أخفُّه؛ فمن اشترط اختلافَ الحالة ليُبلِّغ عن
تصادمٍ أخفى أقواه.

`A_LEVEL_EARNS_ITS_PLACE_ONLY_WHERE_ITS_PREDECESSOR_COLLIDES`: لا تُصدِر هذه
الوحدةُ لمستوًى فضلَ حسمٍ إلا على زوجٍ تصادم فيه سابقُه فعلًا، والقاعدةُ مُجمَّدةٌ
في وحدة التسجيل قبل القياس. ومن سأل عن فضلِ مستوًى على زوجٍ لم يتصادم فيه سابقُه
رُفِع له استثناءٌ ولم تُخترَع له قيمة.

`A_LATER_LEVEL_IS_NOT_NECESSARILY_A_FINER_ONE`: ترتيبُ المستويات ترتيبُ
تسميةٍ لا ترتيبُ دقّةٍ متزايدة. وقد أظهر القياسُ على هذه العيّنة أنّ عددَ
البصمات المتمايزة **ينخفض** كلّما تقدّمنا في السُّلَّم لا يرتفع؛ فالمستوى
المتأخِّرُ هنا يتصادم أكثرَ من المتقدِّم، لا أقلّ. ومن راكَم المستوياتِ من
أوّلها تلقائيًّا أخفى هذا الانقلابَ بجمعٍ لم يُطلَب منه؛ ولذلك تُقرأ
المستوياتُ هنا مفردةً، ولا يُركَّب منها إلا ما ذُكر بعينه.

`AN_UNSEGMENTABLE_WORD_IS_A_NAMED_REFUSAL_NOT_A_NULL`: الصورةُ التي يتعذّر
تقطيعُها تخرج ببصمةٍ متعذّرةٍ باسم سببها، ولا تُقرَّب إلى أقرب قالب ولا تُطوى
صمتًا — وهو نصُّ الحدّ نفسِه في `syllabifier`.

`THE_WEAK_RADICAL_IS_DECLARED_NOT_EXTRACTED`: هويّةُ العلّة تُقرأ من
`FrozenSurface.declared_root` المُعلَن مع الصورة، ولا تُستخرَج من الصورة: لا
مستخرِجَ جذورٍ في هذه الشجرة. فمطابقةُ الجذر المُعلَن بمدخلٍ في جدول المقاييس
المُبصَّم **عدٌّ لما في الجدول**، لا حسمٌ لهويّة علّةِ هذه الصورة بعينها.

`TWENTY_FOUR_HAND_PICKED_FORMS_ARE_NOT_A_CENSUS`: كلُّ ما يخرج من هنا مقصورٌ
على الصور المُجمَّدة بأعيانها. والتصادمُ الواقعُ فيها واقعٌ فعلًا، أمّا انتفاؤه
فخاصّيّةُ العيّنة لا خاصّيّةُ اللغة.

`THIS_IS_A_READING_NOT_A_BIRTH`: لا ولادةَ هنا، ولا حكمَ ولادة، ولا تجميدَ
`E0`، ولا استيرادَ من `kernel/`، ولا تُرفَع بهذه القراءةِ حجبٌ عن طبقة.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Final

from .hollow_root_levels_preregistration import (
    A_LEVEL_EARNS_ITS_PLACE_ONLY_WHERE_ITS_PREDECESSOR_COLLIDES_NOTE,
    FROZEN_SURFACES,
    LEVEL_ORDER,
    SURFACE_SET_DIGEST,
    FrozenSurface,
    HollowRootLevel,
    surface_set_digest,
)
from .p_extractor import PhoneticRole, read_surface
from .syllabifier import SyllabifierError, syllabify_surface
from .text_key import comparison_key

__all__ = [
    "AN_UNSEGMENTABLE_WORD_IS_A_NAMED_REFUSAL_NOT_A_NULL_NOTE",
    "A_COLLISION_IS_FOUND_BY_GROUPING_NOT_BY_PAIRWISE_COMPARISON_NOTE",
    "A_LATER_LEVEL_IS_NOT_NECESSARILY_A_FINER_ONE_NOTE",
    "A_TOTAL_COLLISION_IS_THE_STRONGEST_ONE_NOT_THE_INVISIBLE_ONE_NOTE",
    "MEASUREMENT_NAMED_RESIDUALS",
    "THE_WEAK_RADICAL_IS_DECLARED_NOT_EXTRACTED_NOTE",
    "THIS_IS_A_READING_NOT_A_BIRTH_NOTE",
    "CollisionClass",
    "HollowRootLevelsMeasurementError",
    "LevelReading",
    "collision_classes",
    "combined_fingerprint",
    "TEMPLATE_AND_STATE",
    "template_and_state_collisions",
    "level_fingerprint",
    "read_level",
    "read_all_levels",
    "surfaces_the_level_separates",
]


class HollowRootLevelsMeasurementError(ValueError):
    """رفضٌ عند القراءة: صورةٌ خارج المُجمَّد، أو فضلٌ يُسأل عنه بلا تصادمٍ سابق."""


_UNSEGMENTABLE_PREFIX: Final[str] = "متعذّر:"


def _frozen_surface_of(surface: str) -> FrozenSurface:
    for item in FROZEN_SURFACES:
        if item.surface == surface:
            return item
    raise HollowRootLevelsMeasurementError(
        f"الصورةُ «{surface}» خارجَ المجموعة المُجمَّدة؛ وقياسٌ يُوسِّع عيّنتَه "
        "أثناءه ليس قياسًا للمُجمَّد."
    )


def _harakat_stripped(surface: str) -> str:
    """المستوى صفر-أ: إسقاطُ العلامات وحدها، بمفتاح المقارنة القائم استيرادًا."""

    return comparison_key(surface)


def _madd_also_dropped(surface: str) -> str:
    """المستوى صفر-ب: الإسقاطُ نفسُه مع استبعاد حاملِ دور المدّ من قراءة P."""

    reading = read_surface(surface)
    return "".join(
        letter.unit.carrier
        for letter in reading.letters
        if PhoneticRole.MADD_EXTENSION not in letter.roles
    )


def _syllable_template_sequence(surface: str) -> str:
    """تتابعُ القوالب؛ والمتعذّرُ يخرج باسم سببه ولا يُقرَّب إلى أقرب قالب."""

    try:
        syllabified = syllabify_surface(surface)
    except SyllabifierError as refusal:
        return f"{_UNSEGMENTABLE_PREFIX}{refusal}"
    if not syllabified.syllables:
        reasons = (
            "،".join(item.reason for item in syllabified.wazn_unresolved)
            or "بلا سببٍ مُسمًّى"
        )
        return f"{_UNSEGMENTABLE_PREFIX}{reasons}"
    return "-".join(syllable.template.name for syllable in syllabified.syllables)


def _carrier_state_sequence(surface: str) -> str:
    """تتابعُ حالات الحامل كما وردت من المرماز، بلا طيِّ حالةٍ في أخرى."""

    reading = read_surface(surface)
    return "-".join(
        letter.unit.state.value if letter.unit.state is not None else "بلا_حالة"
        for letter in reading.letters
    )


_PROJECTIONS: Final[dict[HollowRootLevel, object]] = {
    HollowRootLevel.HARAKAT_STRIPPED: _harakat_stripped,
    HollowRootLevel.MADD_ALSO_DROPPED: _madd_also_dropped,
    HollowRootLevel.SYLLABLE_TEMPLATE_SEQUENCE: _syllable_template_sequence,
    HollowRootLevel.CARRIER_STATE_SEQUENCE: _carrier_state_sequence,
}


def level_fingerprint(surface: str, level: HollowRootLevel) -> str:
    """بصمةُ صورةٍ مُجمَّدةٍ عند مستوًى واحد، مُشتقّةً بأدوات الشجرة استيرادًا."""

    _frozen_surface_of(surface)
    if not isinstance(level, HollowRootLevel):
        raise HollowRootLevelsMeasurementError(
            "المستوى عضوٌ من `HollowRootLevel` لا نصٌّ يُكتَب."
        )
    projection = _PROJECTIONS[level]
    assert callable(projection)
    projected = projection(surface)
    assert isinstance(projected, str)
    return projected


def combined_fingerprint(
    surface: str, levels: tuple[HollowRootLevel, ...]
) -> tuple[str, ...]:
    """بصمةٌ مركَّبةٌ من مستويات مذكورةٍ بأعيانها، بترتيبِ `LEVEL_ORDER` لا بترتيبِ
    ذِكرِها.

    ولا تُقرأ المستوياتُ متراكمةً من أوّلها تلقائيًّا: الترتيبُ المُجمَّد ترتيبُ
    **تسمية** لا ترتيبُ دقّةٍ متزايدة، وقد تبيّن بالقياس أنّ المتأخِّر يتصادم
    أكثرَ من المتقدِّم (`A_LATER_LEVEL_IS_NOT_NECESSARILY_A_FINER_ONE`). فمن
    راكَم من الأوّل تلقائيًّا أخفى هذا الانقلابَ بجمعٍ لم يُطلَب منه.
    """

    for level in levels:
        if level not in LEVEL_ORDER:
            raise HollowRootLevelsMeasurementError(
                "المستوى عضوٌ من الترتيب المُجمَّد لا خارجَه."
            )
    ordered = tuple(level for level in LEVEL_ORDER if level in set(levels))
    return tuple(level_fingerprint(surface, level) for level in ordered)


TEMPLATE_AND_STATE: Final[tuple[HollowRootLevel, ...]] = (
    HollowRootLevel.SYLLABLE_TEMPLATE_SEQUENCE,
    HollowRootLevel.CARRIER_STATE_SEQUENCE,
)


@dataclass(frozen=True, slots=True)
class CollisionClass:
    """طبقةُ تصادمٍ واحدة: مستوياتُها، وبصمتُها، وصورُها كلُّها لا آخرُها."""

    levels: tuple[HollowRootLevel, ...]
    fingerprint: tuple[str, ...]
    surfaces: tuple[str, ...]

    def __post_init__(self) -> None:
        if len(self.surfaces) < 2:
            raise HollowRootLevelsMeasurementError(
                "طبقةُ تصادمٍ بأقلَّ من صورتين ليست تصادمًا. "
                + A_COLLISION_IS_FOUND_BY_GROUPING_NOT_BY_PAIRWISE_COMPARISON_NOTE
            )

    @property
    def declared_roots(self) -> tuple[str, ...]:
        """الجذورُ المُعلَنةُ للصور المتصادمة، مرتَّبةً بلا تكرار.

        وطبقةٌ تجمع جذورًا مُعلَنةً مختلفةً تصادمٌ **عبر الجذور** لا داخلَ
        الجذر الواحد؛ والجذرُ هنا مُعلَنٌ لا مُستخرَج.
        """

        return tuple(
            sorted(
                {_frozen_surface_of(surface).declared_root for surface in self.surfaces}
            )
        )


def collision_classes(
    levels: HollowRootLevel | tuple[HollowRootLevel, ...],
    surfaces: tuple[str, ...] | None = None,
) -> tuple[CollisionClass, ...]:
    """طبقاتُ التصادم عند مستوًى أو تركيبِ مستويات، **بالتجميع** لا بمقارنة
    كلّ صورةٍ بسابقتها."""

    requested = (levels,) if isinstance(levels, HollowRootLevel) else levels
    pool = (
        tuple(item.surface for item in FROZEN_SURFACES)
        if surfaces is None
        else surfaces
    )
    grouped: dict[tuple[str, ...], list[str]] = {}
    for surface in pool:
        grouped.setdefault(combined_fingerprint(surface, requested), []).append(surface)
    return tuple(
        CollisionClass(
            levels=requested, fingerprint=fingerprint, surfaces=tuple(members)
        )
        for fingerprint, members in grouped.items()
        if len(members) > 1
    )


def template_and_state_collisions() -> tuple[CollisionClass, ...]:
    """طبقاتُ التصادم تحت البصمة المركَّبة «قالبٌ + حالة» التي جاء بها السؤال.

    وهذه هي البصمةُ التي ادُّعي أنّها «تحسم الصيغةَ السطحيةَ كاملةً بلا تصادمٍ
    واحد». والقياسُ يقلبها: تحتها تقع أشدُّ طبقات هذه العيّنة تصادمًا.
    """

    return collision_classes(TEMPLATE_AND_STATE)


@dataclass(frozen=True, slots=True)
class LevelReading:
    """قراءةُ مستوًى واحد على المجموعة المُجمَّدة: بصماتُه، وتصادماتُه."""

    level: HollowRootLevel
    fingerprints: tuple[tuple[str, tuple[str, ...]], ...]
    collisions: tuple[CollisionClass, ...]

    @property
    def distinct_fingerprint_count(self) -> int:
        """عددُ البصمات المتمايزة؛ نتيجةٌ تُعَدّ لا رقمٌ يُعلَن."""

        return len({fingerprint for _, fingerprint in self.fingerprints})

    @property
    def collided_surfaces(self) -> frozenset[str]:
        """الصورُ الواقعةُ في تصادمٍ عند هذا المستوى، مجموعةً لا قائمة."""

        return frozenset(
            surface for collision in self.collisions for surface in collision.surfaces
        )


def read_level(level: HollowRootLevel) -> LevelReading:
    """اقرأ مستوًى واحدًا على المجموعة المُجمَّدة كلِّها، بلا انتقاءٍ أثناء القراءة."""

    fingerprints = tuple(
        (item.surface, (level_fingerprint(item.surface, level),))
        for item in FROZEN_SURFACES
    )
    return LevelReading(
        level=level,
        fingerprints=fingerprints,
        collisions=collision_classes(level),
    )


def read_all_levels() -> tuple[LevelReading, ...]:
    """اقرأ المستوياتِ الأربعةَ بترتيبها المُجمَّد، ولا يُعاد ترتيبٌ بعد النتيجة."""

    return tuple(read_level(level) for level in LEVEL_ORDER)


def surfaces_the_level_separates(level: HollowRootLevel) -> tuple[tuple[str, str], ...]:
    """الأزواجُ التي فصلها هذا المستوى **بعد أن تصادم فيها سابقُه فعلًا**.

    وهذا هو تنفيذُ `A_LEVEL_EARNS_ITS_PLACE_ONLY_WHERE_ITS_PREDECESSOR_COLLIDES`
    بنيويًّا: مستوًى أوّلُ لا سابقَ له فلا يُنسَب إليه فضلٌ أصلًا، ويُرَدّ السؤالُ
    عنه استثناءً لا يُجاب بتعدادٍ فارغ — فالفارغُ يُقرأ «قِيس فلم يفصل»، والحقُّ
    أنّه «لا يُقاس فضلُه أصلًا».
    """

    if level not in LEVEL_ORDER:
        raise HollowRootLevelsMeasurementError(
            "المستوى عضوٌ من الترتيب المُجمَّد لا خارجَه."
        )
    index = LEVEL_ORDER.index(level)
    if index == 0:
        raise HollowRootLevelsMeasurementError(
            "المستوى الأوّلُ لا سابقَ له، فلا يُنسَب إليه فضلُ حسمٍ على أحد. "
            + A_LEVEL_EARNS_ITS_PLACE_ONLY_WHERE_ITS_PREDECESSOR_COLLIDES_NOTE
        )
    previous = LEVEL_ORDER[index - 1]
    separated: list[tuple[str, str]] = []
    for collision in collision_classes(previous):
        members = collision.surfaces
        for first_index, first in enumerate(members):
            for second in members[first_index + 1 :]:
                if level_fingerprint(first, level) != level_fingerprint(second, level):
                    separated.append((first, second))
    return tuple(separated)


A_LATER_LEVEL_IS_NOT_NECESSARILY_A_FINER_ONE_NOTE: Final[str] = (
    "ALaterLevelIsNotNecessarilyAFinerOne: ترتيبُ المستويات ترتيبُ تسميةٍ لا "
    "ترتيبُ دقّة؛ وعلى هذه العيّنة ينخفض عددُ البصمات المتمايزة كلّما تقدّمنا "
    "في السُّلَّم، فالمتأخِّرُ يتصادم أكثرَ من المتقدِّم لا أقلّ"
)

A_COLLISION_IS_FOUND_BY_GROUPING_NOT_BY_PAIRWISE_COMPARISON_NOTE: Final[str] = (
    "ACollisionIsFoundByGroupingNotByPairwiseComparison: تُجمَع الصورُ تحت "
    "بصمتها الواحدة فتخرج الطبقةُ بأعضائها كلِّهم؛ ومقارنةُ كلّ صورةٍ بآخر "
    "صورةٍ وحدها تقرأ تصادمًا رباعيًّا ثنائيًّا أو تُفوِّته"
)

A_TOTAL_COLLISION_IS_THE_STRONGEST_ONE_NOT_THE_INVISIBLE_ONE_NOTE: Final[str] = (
    "ATotalCollisionIsTheStrongestOneNotTheInvisibleOne: تطابقُ القالب والحالة "
    "معًا أشدُّ التصادم؛ ومن اشترط اختلافَ الحالة ليُبلِّغ عن تصادمٍ أخفى أقواه"
)

AN_UNSEGMENTABLE_WORD_IS_A_NAMED_REFUSAL_NOT_A_NULL_NOTE: Final[str] = (
    "AnUnsegmentableWordIsANamedRefusalNotANull: المتعذّرُ تقطيعُه يخرج ببصمةٍ "
    "تحمل اسمَ سببه، ولا يُقرَّب إلى أقرب قالبٍ ولا يُطوى صمتًا"
)

THE_WEAK_RADICAL_IS_DECLARED_NOT_EXTRACTED_NOTE: Final[str] = (
    "TheWeakRadicalIsDeclaredNotExtracted: الجذرُ حقلٌ مُعلَنٌ مع الصورة لا "
    "مُستخرَجٌ منها؛ ولا يملك هذا المستودعُ مستخرِجَ جذورٍ من الصور السطحية"
)

THIS_IS_A_READING_NOT_A_BIRTH_NOTE: Final[str] = (
    "ThisIsAReadingNotABirth: لا ولادةَ ولا حكمَ ولادةٍ ولا تجميدَ `E0`، ولا "
    "استيرادَ من `kernel/`، ولا رفعَ حجبٍ عن طبقة"
)

MEASUREMENT_NAMED_RESIDUALS: Final[tuple[str, ...]] = (
    AN_UNSEGMENTABLE_WORD_IS_A_NAMED_REFUSAL_NOT_A_NULL_NOTE,
    A_LATER_LEVEL_IS_NOT_NECESSARILY_A_FINER_ONE_NOTE,
    A_COLLISION_IS_FOUND_BY_GROUPING_NOT_BY_PAIRWISE_COMPARISON_NOTE,
    A_TOTAL_COLLISION_IS_THE_STRONGEST_ONE_NOT_THE_INVISIBLE_ONE_NOTE,
    THE_WEAK_RADICAL_IS_DECLARED_NOT_EXTRACTED_NOTE,
    THIS_IS_A_READING_NOT_A_BIRTH_NOTE,
)


def _assert_the_frozen_set_is_unchanged() -> None:
    """طابِقْ بصمةَ المجموعة عند الاستيراد؛ فقياسٌ على عيّنةٍ تغيّرت لا يُقرأ."""

    recomputed = surface_set_digest()
    if recomputed != SURFACE_SET_DIGEST:
        raise RuntimeError(
            "مجموعةُ الصور تغيّرت بعد تجميدها: البصمةُ المُعادُ اشتقاقُها "
            f"{recomputed} تخالف المُجمَّدة {SURFACE_SET_DIGEST}؛ وهذه القراءةُ "
            "تسقط ولا تمرّ بصمت."
        )
    if set(_PROJECTIONS) != set(HollowRootLevel):
        raise RuntimeError(
            "لكلّ مستوًى مُجمَّدٍ إسقاطٌ مُنفَّذ، ولا مستوى بلا إسقاطٍ ولا "
            "إسقاطَ بلا مستوًى مُسجَّل."
        )


_assert_the_frozen_set_is_unchanged()
