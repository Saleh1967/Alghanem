"""سلّمُ رفع الالتباس: خمسُ طبقاتٍ مرتَّبة، ولا واحدةٌ ترقى بسلطة التالية.

**ترتيبُ التنفيذ مُعلَنٌ ههنا مرّةً واحدة**، ورتبةُ كلّ طبقةٍ **مُشتقّةٌ من موضعها
في الإعلان** لا مكتوبةٌ بجانبها:

1. `CARRIER_IDENTITY` — حفظُ هويّة الحامل.
2. `RASM_VERSUS_SOUND` — فصلُ الرسم عن الصوت.
3. `LICENSED_FEATURES` — اختبارُ السمات المرخّصة.
4. `SYLLABIC_AND_MORPHOLOGICAL_RELATIONS` — العلاقاتُ المقطعيّة والصرفيّة.
5. `IFADA` — الإفادةُ في طبقتها الخاصّة.

**والقانونُ المركزيُّ**: لا تكتسب طبقةٌ سلطةَ الطبقة التالية لمجرّد أنّها فصلت
حالتين. فـ`authority_after_separating` تردّ الطبقةَ نفسَها مهما كثر ما فصلته،
و`claim_is_licensed_at` لا ترخّص دعوى طبقةٍ أعلى لعاملٍ في طبقةٍ أدنى
(`SEPARATING_TWO_STATES_GRANTS_NO_UPPER_AUTHORITY`).

**ورفعُ الالتباس لا يكون باختلاق فروق**: كلُّ طبقةٍ تستشهد بأسماء حقولٍ
**مُسجَّلةٍ في القطعة نفسها بمصادرٍ مكتوبة**، فإن استشهدت بما ليس مُسجَّلًا
رُفِض السلّمُ رفضًا صريحًا؛ وكلُّ فرقٍ يظهر في السلّم مردودٌ إلى حقلٍ مُسجَّلٍ
بسنده (`A_DISTINCTION_WITHOUT_A_RECORDED_FIELD_IS_AN_INVENTION`). ولا يُستشهَد
بحقلٍ واحدٍ في طبقتين، فذلك تمريرُ فرقٍ من طبقةٍ إلى أخرى باسمٍ جديد
(`A_FIELD_BELONGS_TO_EXACTLY_ONE_LAYER`).

**ولا يُفسَد القياسُ الأصليّ**: قاعُ السلّم يُقابَل بالقياس الأصليّ المحفوظ في
القطعة، فإن لم يُسترجَع منه رُدَّ `the_original_measurement_is_recoverable`
كاذبًا بالقياس لا بالإعلان (`THE_LADDER_ADDS_AND_DOES_NOT_REPLACE`).

**ولا تُعلَن ولادةُ المقطع قبل برهانها**: `refuse_syllable_birth_claim` ترفض
دعوى الولادة من أيّ طبقة، والرابعةُ داخلةٌ في ذلك؛ فقياسُ العلاقات المقطعيّة
ليس ولادةً لها (`SYLLABLE_BIRTH_IS_NOT_DECLARED_BY_ANY_LAYER`).

وليست هذه الوحدةُ بوّابةً: لا ولادةَ، ولا حكمَ ولادة، ولا تجميدَ، ولا استيرادَ
من `kernel/`.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from itertools import combinations
from typing import Final

from .hamza_contract import THE_DECLARED_OCCURRENCES, codec_projection

__all__ = [
    "AN_UNRESOLVED_PAIR_IS_NOT_LIFTED_BY_INVENTING_A_FIELD_NOTE",
    "A_DISTINCTION_WITHOUT_A_RECORDED_FIELD_IS_AN_INVENTION_NOTE",
    "A_FIELD_BELONGS_TO_EXACTLY_ONE_LAYER_NOTE",
    "A_SEPARATION_IS_A_ROW_NOT_A_RANK_NOTE",
    "DISAMBIGUATION_LAYER_ORDER_NAMED_RESIDUALS",
    "SEPARATING_TWO_STATES_GRANTS_NO_UPPER_AUTHORITY_NOTE",
    "SYLLABLE_BIRTH_IS_NOT_DECLARED_BY_ANY_LAYER_NOTE",
    "THE_DECLARED_HAMZA_LADDER",
    "THE_DECLARED_HAMZA_ITEMS",
    "THE_DECLARED_ORDER",
    "THE_LADDER_ADDS_AND_DOES_NOT_REPLACE_NOTE",
    "THE_ORDER_IS_DECLARED_NOT_MEASURED_NOTE",
    "THE_PLACEMENT_OF_A_FIELD_IN_A_LAYER_IS_DECLARED_NOT_DERIVED_NOTE",
    "DisambiguationLayer",
    "LadderReport",
    "LayerOrderError",
    "LayerReading",
    "LayerSeparations",
    "ObservedItem",
    "OrderedLadder",
    "RecordedField",
    "authority_after_separating",
    "claim_is_licensed_at",
    "rank_of",
    "refuse_syllable_birth_claim",
    "run_ladder",
    "syllable_birth_is_declared",
    "value_at",
]


class LayerOrderError(ValueError):
    """رفضٌ صريح: سلّمٌ مختلُّ الترتيب، أو استشهادٌ بما ليس مُسجَّلًا."""


class DisambiguationLayer(Enum):
    """الطبقاتُ الخمس؛ وأسماؤها لا تحمل رتبتَها، والرتبةُ من الترتيب المُعلَن."""

    CARRIER_IDENTITY = "هويّةُ_الحامل"
    RASM_VERSUS_SOUND = "فصلُ_الرسم_عن_الصوت"
    LICENSED_FEATURES = "السماتُ_المرخّصة"
    SYLLABIC_AND_MORPHOLOGICAL_RELATIONS = "العلاقاتُ_المقطعيّةُ_والصرفيّة"
    IFADA = "الإفادة"


THE_DECLARED_ORDER: Final[tuple[DisambiguationLayer, ...]] = (
    DisambiguationLayer.CARRIER_IDENTITY,
    DisambiguationLayer.RASM_VERSUS_SOUND,
    DisambiguationLayer.LICENSED_FEATURES,
    DisambiguationLayer.SYLLABIC_AND_MORPHOLOGICAL_RELATIONS,
    DisambiguationLayer.IFADA,
)
"""ترتيبُ التنفيذ المُعلَن؛ وهو منهجٌ مُختار، لا نتيجةَ قياسٍ على مدوّنة."""


def rank_of(layer: DisambiguationLayer) -> int:
    """رتبةُ الطبقة، مُشتقّةً من موضعها في الترتيب المُعلَن لا مكتوبةً."""

    if not isinstance(layer, DisambiguationLayer):
        raise LayerOrderError("طبقةٌ غيرُ مُسمّاةٍ لا رتبةَ لها")
    return THE_DECLARED_ORDER.index(layer)


def authority_after_separating(
    layer: DisambiguationLayer, separated_pairs: int
) -> DisambiguationLayer:
    """أيُّ سلطةٍ تُكتسَب بعد فصل حالتين؟ سلطةُ الطبقة نفسِها، وكم فصلت لا يغيّر.

    والدالّةُ تأخذ عددَ ما فصلته لتُظهر أنّها **لا تقرؤه**؛ فلو كان الفصلُ
    يرقّي لظهر أثرُه ههنا.
    """

    if separated_pairs < 0:
        raise LayerOrderError("عددُ ما فُصِل لا يكون سالبًا")
    return layer


def claim_is_licensed_at(
    claim_layer: DisambiguationLayer, working_layer: DisambiguationLayer
) -> bool:
    """أتُرخَّص دعوى طبقةٍ لعاملٍ في طبقة؟ لا ترتفع الدعوى فوق رتبة العامل."""

    return rank_of(claim_layer) <= rank_of(working_layer)


def syllable_birth_is_declared() -> bool:
    """أأُعلِنت ولادةُ المقطع؟ لا — وقياسُ العلاقات المقطعيّة ليس ولادةً لها."""

    return False


def refuse_syllable_birth_claim(layer: DisambiguationLayer) -> None:
    """ارفض دعوى ولادة المقطع من أيّ طبقة، والرابعةُ ليست مستثناة."""

    raise LayerOrderError(
        f"ولادةُ المقطع غيرُ مُعلَنةٍ، ولا تُدَّعى من طبقة «{rank_of(layer)}»؛ "
        "وفصلُ العلاقات المقطعيّة قياسٌ لها لا ولادةٌ"
    )


# --- القطعةُ وسجلُّ حقولها ----------------------------------------------------


@dataclass(frozen=True, slots=True)
class RecordedField:
    """حقلٌ مُسجَّلٌ في القطعة: اسمُه، وقيمتُه، ومصدرُه المكتوب."""

    name: str
    value: str
    declared_source: str

    def __post_init__(self) -> None:
        if not self.name.strip():
            raise LayerOrderError("حقلٌ بلا اسمٍ لا يُستشهَد به")
        if not self.value.strip():
            raise LayerOrderError("حقلٌ بلا قيمةٍ لا يفصل شيئًا")
        if not self.declared_source.strip():
            raise LayerOrderError(
                "حقلٌ بلا مصدرٍ مكتوب؛ والفرقُ المبنيُّ عليه اختلاقٌ لا سندَ له"
            )


@dataclass(frozen=True, slots=True)
class ObservedItem:
    """قطعةٌ مرصودة: قياسُها الأصليُّ المحفوظ، وحقولُها المُسجَّلةُ بمصادرها."""

    item_id: str
    original_measurement: str
    recorded: tuple[RecordedField, ...]

    def __post_init__(self) -> None:
        if not self.item_id.strip():
            raise LayerOrderError("قطعةٌ بلا مُعرِّفٍ لا تُقابَل بغيرها")
        if not self.original_measurement.strip():
            raise LayerOrderError("قطعةٌ بلا قياسٍ أصليٍّ محفوظٍ لا يُفحَص استرجاعُه")
        names = [item.name for item in self.recorded]
        if len(names) != len(set(names)):
            raise LayerOrderError("حقلٌ مُسجَّلٌ مرّتين في قطعةٍ واحدة؛ وأيُّهما يُقرَأ؟")
        if not self.recorded:
            raise LayerOrderError("قطعةٌ بلا حقلٍ مُسجَّلٍ لا تدخل سلّمًا")

    @property
    def recorded_names(self) -> frozenset[str]:
        """أسماءُ الحقول المُسجَّلة، مُشتقّةً من السجلّ لا مكتوبةً بجانبه."""

        return frozenset(item.name for item in self.recorded)

    def value_of(self, name: str) -> str:
        """قيمةُ حقلٍ مُسجَّل؛ وطلبُ غيرِ المُسجَّل رفضٌ لا قيمةٌ خالية."""

        for item in self.recorded:
            if item.name == name:
                return item.value
        raise LayerOrderError(
            f"استُشهِد بحقل «{name}» وليس مُسجَّلًا في «{self.item_id}»؛ "
            "والفرقُ المبنيُّ عليه اختلاقٌ لا رفعَ التباس"
        )


@dataclass(frozen=True, slots=True)
class LayerReading:
    """قراءةُ طبقةٍ واحدة: الطبقةُ، والحقولُ المُسجَّلةُ التي تستشهد بها."""

    layer: DisambiguationLayer
    cited_fields: tuple[str, ...]

    def __post_init__(self) -> None:
        if not isinstance(self.layer, DisambiguationLayer):
            raise LayerOrderError("طبقةٌ غيرُ مُسمّاةٍ لا تقرأ")
        if not self.cited_fields:
            raise LayerOrderError(
                "طبقةٌ لا تستشهد بحقلٍ واحدٍ لا تضيف شيئًا؛ ووجودُها في السلّم لغوٌ"
            )
        if len(self.cited_fields) != len(set(self.cited_fields)):
            raise LayerOrderError("حقلٌ مُستشهَدٌ به مرّتين في طبقةٍ واحدة")


def value_at(
    item: ObservedItem, ladder: OrderedLadder, layer: DisambiguationLayer
) -> tuple[tuple[str, str], ...]:
    """قيمةُ القطعة عند طبقة: حقولُ هذه الطبقة وما دونها، مُراكَمةً لا مُستبدَلة."""

    ceiling = rank_of(layer)
    return tuple(
        (name, item.value_of(name))
        for reading in ladder.readings
        if rank_of(reading.layer) <= ceiling
        for name in reading.cited_fields
    )


# --- السلّمُ المرتَّب ----------------------------------------------------------


@dataclass(frozen=True, slots=True)
class OrderedLadder:
    """سلّمٌ مرتَّب: قراءاتُ الطبقات بترتيبها المُعلَن، لا بترتيبٍ حرّ."""

    readings: tuple[LayerReading, ...]

    def __post_init__(self) -> None:
        if not self.readings:
            raise LayerOrderError("سلّمٌ بلا قراءةٍ واحدةٍ لا يرفع التباسًا")
        layers = [reading.layer for reading in self.readings]
        if len(layers) != len(set(layers)):
            raise LayerOrderError("طبقةٌ مقروءةٌ مرّتين في سلّمٍ واحد")
        ranks = [rank_of(layer) for layer in layers]
        if ranks != sorted(ranks):
            raise LayerOrderError(
                "قراءاتُ السلّم على غير الترتيب المُعلَن؛ ولا تُقرأ طبقةٌ قبل ما دونها"
            )
        if ranks != list(range(len(ranks))):
            raise LayerOrderError(
                "السلّمُ يبدأ من قاع الترتيب ويتّصل؛ وتخطّي طبقةٍ تخطٍّ لسلطتها"
            )
        cited: list[str] = [
            name for reading in self.readings for name in reading.cited_fields
        ]
        if len(cited) != len(set(cited)):
            raise LayerOrderError("حقلٌ مُستشهَدٌ به في طبقتين؛ وذلك تمريرُ فرقٍ باسمٍ جديد")

    @property
    def highest_layer(self) -> DisambiguationLayer:
        """أعلى طبقةٍ بلغها السلّم، مُشتقّةً من قراءاته."""

        return self.readings[-1].layer

    @property
    def cited_fields(self) -> tuple[str, ...]:
        """كلُّ الحقول المُستشهَد بها، بترتيب طبقاتها."""

        return tuple(name for reading in self.readings for name in reading.cited_fields)


@dataclass(frozen=True, slots=True)
class LayerSeparations:
    """ما فصلته طبقةٌ بعينها: أزواجُ القطع، صفوفًا بأسمائها لا عددًا مجرّدًا."""

    layer: DisambiguationLayer
    newly_separated: tuple[tuple[str, str], ...]

    @property
    def separated_count(self) -> int:
        """عددُ ما فصلته، معدودًا من الصفوف لا مكتوبًا بجانبها."""

        return len(self.newly_separated)

    @property
    def granted_authority(self) -> DisambiguationLayer:
        """السلطةُ المكتسَبةُ بهذا الفصل: طبقتُه، لا التي تليها."""

        return authority_after_separating(self.layer, self.separated_count)


@dataclass(frozen=True, slots=True)
class LadderReport:
    """حصادُ تشغيل السلّم على قطعٍ مرصودة؛ كلُّه مُشتَقٌّ بالتشغيل."""

    separations: tuple[LayerSeparations, ...]
    unresolved_pairs: tuple[tuple[str, str], ...]
    original_measurement_mismatches: tuple[str, ...]

    @property
    def the_original_measurement_is_recoverable(self) -> bool:
        """أيُسترجَع القياسُ الأصليُّ من قاع السلّم؟ يُقرأ من صفوف الخُلف."""

        return not self.original_measurement_mismatches

    @property
    def every_layer_separated_something(self) -> bool:
        """أأضافت كلُّ طبقةٍ فرقًا؟ طبقةٌ لا تفصل شيئًا لا تُرقَّى بذلك ولا تُحذَف."""

        return all(item.separated_count > 0 for item in self.separations)

    @property
    def the_ambiguity_is_fully_lifted(self) -> bool:
        """أارتفع الالتباسُ كلُّه على هذه القطع؟ يُقرأ من الأزواج الباقية."""

        return not self.unresolved_pairs

    @property
    def no_layer_gained_upper_authority(self) -> bool:
        """أبقيت كلُّ طبقةٍ على سلطتها بعد فصلها؟ يُشتَقّ بالمقابلة لا بالإعلان."""

        return all(item.granted_authority is item.layer for item in self.separations)


def run_ladder(ladder: OrderedLadder, items: tuple[ObservedItem, ...]) -> LadderReport:
    """شغِّل السلّمَ على القطع: أحصِ ما فصلته كلُّ طبقة، وافحص استرجاعَ الأصل."""

    if not items:
        raise LayerOrderError("قطعٌ خاليةٌ يُثبَت عليها كلُّ شيء")
    identifiers = [item.item_id for item in items]
    if len(identifiers) != len(set(identifiers)):
        raise LayerOrderError("مُعرِّفٌ مكرَّرٌ بين القطع؛ ولا تُقابَل قطعةٌ بنفسها")
    for name in ladder.cited_fields:
        for item in items:
            item.value_of(name)

    bottom = THE_DECLARED_ORDER[0]
    mismatches = tuple(
        item.item_id
        for item in items
        if tuple(value for _, value in value_at(item, ladder, bottom))
        != (item.original_measurement,)
    )

    separations: list[LayerSeparations] = []
    pending = list(combinations(items, 2))
    for reading in ladder.readings:
        newly: list[tuple[str, str]] = []
        still: list[tuple[ObservedItem, ObservedItem]] = []
        for left, right in pending:
            if value_at(left, ladder, reading.layer) != value_at(
                right, ladder, reading.layer
            ):
                newly.append((left.item_id, right.item_id))
            else:
                still.append((left, right))
        pending = still
        separations.append(
            LayerSeparations(layer=reading.layer, newly_separated=tuple(newly))
        )

    return LadderReport(
        separations=tuple(separations),
        unresolved_pairs=tuple(
            (left.item_id, right.item_id) for left, right in pending
        ),
        original_measurement_mismatches=mismatches,
    )


# --- السلّمُ المُعلَنُ على وقوعات الهمزة ----------------------------------------


_CODEC_SOURCE: Final[str] = "تشغيلُ المِرماز على سطح الوقوع"
_DECLARED_SOURCE: Final[str] = "إعلانُ الوقوع بمصدره المكتوب في عقد الهمزة"

_CARRIER_FIELD: Final[str] = "الحاملُ_المِرمازيّ"
_SEAT_FIELD: Final[str] = "الكرسيُّ_المِرمازيّ"
_IDENTITY_FIELD: Final[str] = "الهويّةُ_المُعلَنة"
_FUNCTION_FIELD: Final[str] = "الوظيفةُ_المُعلَنة"
_REALIZATION_FIELD: Final[str] = "التحقّقُ_السياقيّ"
_CONTENT_FIELD: Final[str] = "المضمونُ_المُفاد"


def _hamza_items() -> tuple[ObservedItem, ...]:
    items: list[ObservedItem] = []
    for position, occurrence in enumerate(THE_DECLARED_OCCURRENCES):
        carrier, seat = codec_projection(occurrence)
        items.append(
            ObservedItem(
                item_id=f"وقوع_{position}",
                original_measurement=carrier,
                recorded=(
                    RecordedField(_CARRIER_FIELD, carrier, _CODEC_SOURCE),
                    RecordedField(
                        _SEAT_FIELD, "بلا_كرسيّ" if seat is None else seat, _CODEC_SOURCE
                    ),
                    RecordedField(
                        _IDENTITY_FIELD,
                        occurrence.identity.value,
                        occurrence.declared_source,
                    ),
                    RecordedField(
                        _FUNCTION_FIELD,
                        occurrence.function.value,
                        occurrence.declared_source,
                    ),
                    RecordedField(
                        _REALIZATION_FIELD,
                        occurrence.realization.value,
                        occurrence.declared_source,
                    ),
                    RecordedField(_CONTENT_FIELD, occurrence.content, _DECLARED_SOURCE),
                ),
            )
        )
    return tuple(items)


THE_DECLARED_HAMZA_ITEMS: Final[tuple[ObservedItem, ...]] = _hamza_items()
"""قطعُ الشاهد: وقوعاتُ الهمزة المُعلَنة، بحقولها المُسجَّلةِ بمصادرها."""

THE_DECLARED_HAMZA_LADDER: Final[OrderedLadder] = OrderedLadder(
    readings=(
        LayerReading(DisambiguationLayer.CARRIER_IDENTITY, (_CARRIER_FIELD,)),
        LayerReading(DisambiguationLayer.RASM_VERSUS_SOUND, (_SEAT_FIELD,)),
        LayerReading(
            DisambiguationLayer.LICENSED_FEATURES,
            (_IDENTITY_FIELD, _FUNCTION_FIELD),
        ),
        LayerReading(
            DisambiguationLayer.SYLLABIC_AND_MORPHOLOGICAL_RELATIONS,
            (_REALIZATION_FIELD,),
        ),
        LayerReading(DisambiguationLayer.IFADA, (_CONTENT_FIELD,)),
    )
)
"""سلّمٌ مُعلَنٌ يوزّع حقولَ عقد الهمزة على الطبقات الخمس؛ والتوزيعُ اختيار."""


# --- البواقي المُسمّاة --------------------------------------------------------


A_DISTINCTION_WITHOUT_A_RECORDED_FIELD_IS_AN_INVENTION_NOTE: Final[str] = (
    "ADistinctionWithoutARecordedFieldIsAnInvention: كلُّ فرقٍ في السلّم مردودٌ "
    "إلى حقلٍ مُسجَّلٍ في القطعة بمصدرٍ مكتوب؛ والاستشهادُ بغير المُسجَّل رفضٌ "
    "صريح، لأنّ رفعَ الالتباس باختلاق فرقٍ ليس رفعًا له بل إزاحةٌ لموضعه"
)

AN_UNRESOLVED_PAIR_IS_NOT_LIFTED_BY_INVENTING_A_FIELD_NOTE: Final[str] = (
    "AnUnresolvedPairIsNotLiftedByInventingAField: يبقى في شاهد الهمزة زوجٌ لم "
    "يفصله السلّم، لأنّ مضمونَيه المُسجَّلَين سواء؛ ورفعُه يلزمه حقلٌ مُسجَّلٌ "
    "جديدٌ بمصدره — وذلك قياسٌ جديد، لا فرقٌ يُختلَق في طبقةٍ قائمة"
)

A_FIELD_BELONGS_TO_EXACTLY_ONE_LAYER_NOTE: Final[str] = (
    "AFieldBelongsToExactlyOneLayer: لا يُستشهَد بحقلٍ واحدٍ في طبقتين، وإلّا "
    "مُرِّر فرقُ طبقةٍ إلى أخرى باسمٍ جديد فبدت الثانيةُ فاصلةً وهي مُعيدةٌ"
)

A_SEPARATION_IS_A_ROW_NOT_A_RANK_NOTE: Final[str] = (
    "ASeparationIsARowNotARank: ما فصلته الطبقةُ محفوظٌ أزواجًا بأسماء قطعها في "
    "`newly_separated`، وعددُه معدودٌ منها؛ ولا يُقرَأ العددُ رتبةً ولا قدرةً، "
    "ولا تُرقَّى طبقةٌ بكثرة ما فصلت"
)

SEPARATING_TWO_STATES_GRANTS_NO_UPPER_AUTHORITY_NOTE: Final[str] = (
    "SeparatingTwoStatesGrantsNoUpperAuthority: `authority_after_separating` "
    "تأخذ عددَ ما فُصِل ولا تقرؤه، فتردّ الطبقةَ نفسَها؛ وفصلُ الرسم لا يرخّص "
    "دعوى سمةٍ، وفصلُ السمة لا يرخّص دعوى علاقةٍ مقطعيّة، وهكذا صُعُدًا"
)

SYLLABLE_BIRTH_IS_NOT_DECLARED_BY_ANY_LAYER_NOTE: Final[str] = (
    "SyllableBirthIsNotDeclaredByAnyLayer: الطبقةُ الرابعةُ تقيس العلاقات "
    "المقطعيّة ولا تلد المقطع؛ و`refuse_syllable_birth_claim` ترفض الدعوى من "
    "كلّ طبقةٍ بلا استثناء، ولا يُغلَق البابُ بحياد الألف ولا بفصلٍ ناجح"
)

THE_LADDER_ADDS_AND_DOES_NOT_REPLACE_NOTE: Final[str] = (
    "TheLadderAddsAndDoesNotReplace: قيمةُ القطعة عند طبقةٍ مراكمةٌ لحقول ما "
    "دونها، فلا تُفسِد طبقةٌ عُليا قياسَ من تحتها؛ واسترجاعُ القياس الأصليّ من "
    "قاع السلّم **مفحوصٌ** بالمقابلة، لا مُعلَنٌ بالبناء"
)

THE_ORDER_IS_DECLARED_NOT_MEASURED_NOTE: Final[str] = (
    "TheOrderIsDeclaredNotMeasured: ترتيبُ الطبقات الخمس منهجٌ مُختارٌ مُعلَنٌ "
    "ههنا، ولم يُقَس على مدوّنةٍ ولم يُبرهَن أنّه الترتيبُ الوحيدُ الممكن؛ "
    "والرتبُ مُشتقّةٌ من الترتيب، فإن نُقِض الترتيبُ نُقِضت معه"
)

THE_PLACEMENT_OF_A_FIELD_IN_A_LAYER_IS_DECLARED_NOT_DERIVED_NOTE: Final[str] = (
    "ThePlacementOfAFieldInALayerIsDeclaredNotDerived: وضعُ «الوظيفة» في "
    "السمات المرخّصة و«التحقّق» في العلاقات المقطعيّة اختيارٌ مُعلَنٌ في هذا "
    "السلّم؛ وسلّمٌ آخرُ قد يوزّعها غيرَ هذا التوزيع، فتتغيّر أرقامُ ما فصلته "
    "كلُّ طبقةٍ دون أن يتغيّر ما ارتفع من الالتباس جملةً"
)

DISAMBIGUATION_LAYER_ORDER_NAMED_RESIDUALS: Final[tuple[str, ...]] = (
    THE_ORDER_IS_DECLARED_NOT_MEASURED_NOTE,
    SEPARATING_TWO_STATES_GRANTS_NO_UPPER_AUTHORITY_NOTE,
    A_DISTINCTION_WITHOUT_A_RECORDED_FIELD_IS_AN_INVENTION_NOTE,
    A_FIELD_BELONGS_TO_EXACTLY_ONE_LAYER_NOTE,
    AN_UNRESOLVED_PAIR_IS_NOT_LIFTED_BY_INVENTING_A_FIELD_NOTE,
    THE_LADDER_ADDS_AND_DOES_NOT_REPLACE_NOTE,
    A_SEPARATION_IS_A_ROW_NOT_A_RANK_NOTE,
    THE_PLACEMENT_OF_A_FIELD_IN_A_LAYER_IS_DECLARED_NOT_DERIVED_NOTE,
    SYLLABLE_BIRTH_IS_NOT_DECLARED_BY_ANY_LAYER_NOTE,
)
"""البواقي المُسمّاة؛ تُعَدّ في الاختبار ولا يُكتَب عددُها بجانبها."""
