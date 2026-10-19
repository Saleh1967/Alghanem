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

**والهدفُ محجوبٌ عن السلّم، والقارئُ أعمى عن الأصل**: المضمونُ المُفاد ليس حقلًا
من حقول القطعة بل `target` مستقلٌّ، و`ObservedItem` ترفض تسجيلَه في حقولها،
و`refuse_a_ladder_that_reads_its_target` ترفض سلّمًا يستشهد به. ثمّ
`run_target_recovery_experiment` تسأل: أيكفي ما بلغه السلّمُ لاسترجاعه؟ فتُعطي
القارئَ قيمةَ السلّم وحدها، وتسألُه **مرّةً واحدةً لكلّ قيمةٍ متمايزة**، وتردُّ
التجربةَ **قبل سؤاله** إن دمجت قيمةٌ واحدةٌ هدفين مختلفين
(`A_LADDER_THAT_CITES_ITS_TARGET_PROVES_NOTHING`,
`THE_READER_IS_ASKED_ONCE_PER_DISTINCT_VALUE`).

**ولا تُعلَن ولادةُ المقطع قبل برهانها**: `refuse_syllable_birth_claim` ترفض
دعوى الولادة من أيّ طبقة، والرابعةُ داخلةٌ في ذلك؛ فقياسُ العلاقات المقطعيّة
ليس ولادةً لها (`SYLLABLE_BIRTH_IS_NOT_DECLARED_BY_ANY_LAYER`).

وليست هذه الوحدةُ بوّابةً: لا ولادةَ، ولا حكمَ ولادة، ولا تجميدَ، ولا استيرادَ
من `kernel/`.
"""

from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass
from enum import Enum
from itertools import combinations
from typing import Final

from .hamza_contract import THE_DECLARED_OCCURRENCES, codec_projection

__all__ = [
    "AN_INDEPENDENT_READER_FAILED_WHERE_A_LOOKUP_SUCCEEDED_NOTE",
    "AN_UNRESOLVED_PAIR_IS_NOT_LIFTED_BY_INVENTING_A_FIELD_NOTE",
    "A_DISTINCTION_WITHOUT_A_RECORDED_FIELD_IS_AN_INVENTION_NOTE",
    "A_LADDER_THAT_CITES_ITS_TARGET_PROVES_NOTHING_NOTE",
    "A_LOOKUP_READER_IS_NOT_A_LINGUISTIC_RULE_NOTE",
    "A_FIELD_BELONGS_TO_EXACTLY_ONE_LAYER_NOTE",
    "A_SEPARATION_IS_A_ROW_NOT_A_RANK_NOTE",
    "DISAMBIGUATION_LAYER_ORDER_NAMED_RESIDUALS",
    "SEPARATING_TWO_STATES_GRANTS_NO_UPPER_AUTHORITY_NOTE",
    "SYLLABLE_BIRTH_IS_NOT_DECLARED_BY_ANY_LAYER_NOTE",
    "THE_DECLARED_FUNCTION_ONLY_TABLE",
    "THE_DECLARED_HAMZA_LADDER",
    "THE_DECLARED_HAMZA_ITEMS",
    "THE_DECLARED_ORDER",
    "THE_LADDER_ADDS_AND_DOES_NOT_REPLACE_NOTE",
    "THE_ORDER_IS_DECLARED_NOT_MEASURED_NOTE",
    "THE_PLACEMENT_OF_A_FIELD_IN_A_LAYER_IS_DECLARED_NOT_DERIVED_NOTE",
    "THE_READER_IS_ASKED_ONCE_PER_DISTINCT_VALUE_NOTE",
    "DisambiguationLayer",
    "LadderReader",
    "LadderReport",
    "LayerOrderError",
    "LayerReading",
    "LayerSeparations",
    "ObservedItem",
    "OrderedLadder",
    "RecordedField",
    "TargetRecoveryReport",
    "a_declared_function_only_reader",
    "a_lookup_reader",
    "authority_after_separating",
    "claim_is_licensed_at",
    "rank_of",
    "refuse_a_ladder_that_reads_its_target",
    "refuse_syllable_birth_claim",
    "run_ladder",
    "run_target_recovery_experiment",
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
    """قطعةٌ مرصودة: قياسُها الأصليُّ، وحقولُها المُسجَّلة، وهدفُها المحجوب عنها."""

    item_id: str
    original_measurement: str
    recorded: tuple[RecordedField, ...]
    target: RecordedField

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
        if self.target.name in names:
            raise LayerOrderError(
                f"الهدفُ «{self.target.name}» مُسجَّلٌ في حقول القطعة نفسِها؛ "
                "وسلّمٌ يقرأ هدفَه لا يرفع التباسًا بل ينقله"
            )

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


# --- تجربةُ استرجاع الهدف بدليلٍ وهدفٍ مستقلَّين -------------------------------


LadderReader = Callable[[tuple[tuple[str, str], ...]], str]
"""قارئٌ لا يرى إلّا قيمةَ السلّم: لا مُعرِّفَ القطعة، ولا هدفَها."""


def refuse_a_ladder_that_reads_its_target(
    ladder: OrderedLadder, items: tuple[ObservedItem, ...]
) -> None:
    """ارفض سلّمًا يستشهد بحقل الهدف؛ فذلك قراءةٌ للجواب لا استرجاعٌ له."""

    cited = frozenset(ladder.cited_fields)
    for item in items:
        if item.target.name in cited:
            raise LayerOrderError(
                f"السلّمُ يستشهد بحقل الهدف «{item.target.name}» في «{item.item_id}»؛ "
                "والاستشهادُ بالجواب ليس برهانًا على استرجاعه"
            )


@dataclass(frozen=True, slots=True)
class TargetRecoveryReport:
    """حصادُ التجربة: ما دُمِج، وكم سُئل القارئ، وأين أخطأ. كلُّه بالتشغيل."""

    target_name: str
    merged_targets: tuple[tuple[str, str], ...]
    distinct_values: int
    reader_calls: int
    mistaken_items: tuple[str, ...]

    def __post_init__(self) -> None:
        if not self.target_name.strip():
            raise LayerOrderError("تجربةٌ بلا هدفٍ مُسمًّى لا تُقرأ نتيجتُها")
        if self.reader_calls < 0 or self.distinct_values < 0:
            raise LayerOrderError("عددُ ما أُحصي لا يكون سالبًا")

    @property
    def the_reader_was_consulted(self) -> bool:
        """أسُئل القارئُ أصلًا؟ الدمجُ يُبطل التجربةَ قبل السؤال."""

        return self.reader_calls > 0

    @property
    def the_ladder_determines_the_target(self) -> bool:
        """أيُحدِّد السلّمُ الهدف؟ لا دمجَ، ولا خطأَ، وقد سُئل القارئُ فعلًا."""

        return (
            not self.merged_targets
            and not self.mistaken_items
            and self.the_reader_was_consulted
        )

    @property
    def is_a_linguistic_rule(self) -> bool:
        """أهذا حكمٌ لغويّ؟ لا — نجاحُ قارئٍ على قطعٍ مُعلَنةٍ ليس قاعدةً."""

        return False


def run_target_recovery_experiment(
    ladder: OrderedLadder,
    items: tuple[ObservedItem, ...],
    reader: LadderReader,
) -> TargetRecoveryReport:
    """اسأل: أيكفي ما بلغه السلّمُ لاسترجاع هدفٍ محجوبٍ عنه؟ بالتشغيل لا بالإعلان.

    والقارئُ **أعمى عن الأصل**: لا يُعطى إلّا قيمةَ السلّم، ويُسأل **مرّةً واحدةً
    لكلِّ قيمةٍ متمايزة**، ثمّ يُقابَل جوابُه بأهداف كلِّ القطع المشترِكة فيها.
    فإن دمجت القيمةُ الواحدةُ هدفين مختلفين رُدَّت التجربةُ **قبل سؤاله**.
    """

    if not items:
        raise LayerOrderError("قطعٌ خاليةٌ يُثبَت عليها كلُّ شيء")
    target_names = {item.target.name for item in items}
    if len(target_names) != 1:
        raise LayerOrderError("أهدافٌ بأسماءٍ مختلفةٍ في تجربةٍ واحدة؛ وأيُّها يُسترجَع؟")
    refuse_a_ladder_that_reads_its_target(ladder, items)

    top = ladder.highest_layer
    grouped: dict[tuple[tuple[str, str], ...], list[ObservedItem]] = {}
    for item in items:
        grouped.setdefault(value_at(item, ladder, top), []).append(item)

    merged = tuple(
        (left.item_id, right.item_id)
        for shared in grouped.values()
        for left, right in combinations(shared, 2)
        if left.target.value != right.target.value
    )
    if merged:
        return TargetRecoveryReport(
            target_name=target_names.pop(),
            merged_targets=merged,
            distinct_values=len(grouped),
            reader_calls=0,
            mistaken_items=(),
        )

    calls = 0
    mistaken: list[str] = []
    for value, shared in grouped.items():
        answer = reader(value)
        calls += 1
        mistaken.extend(item.item_id for item in shared if item.target.value != answer)

    return TargetRecoveryReport(
        target_name=target_names.pop(),
        merged_targets=(),
        distinct_values=len(grouped),
        reader_calls=calls,
        mistaken_items=tuple(mistaken),
    )


def a_lookup_reader(
    ladder: OrderedLadder, items: tuple[ObservedItem, ...]
) -> LadderReader:
    """قارئٌ بجدولٍ مبنيٍّ من القطع نفسِها: يُثبت التمايز، ولا يُثبت قاعدةً."""

    table: dict[tuple[tuple[str, str], ...], str] = {}
    top = ladder.highest_layer
    for item in items:
        table.setdefault(value_at(item, ladder, top), item.target.value)

    def read(value: tuple[tuple[str, str], ...]) -> str:
        if value not in table:
            raise LayerOrderError("قيمةٌ خارجَ الجدول؛ والقارئُ لا يخمّن")
        return table[value]

    return read


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
                ),
                target=RecordedField(
                    _CONTENT_FIELD, occurrence.content, _DECLARED_SOURCE
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
    )
)
"""سلّمٌ مُعلَنٌ يوزّع حقولَ عقد الهمزة على أربع طبقات؛ والإفادةُ هدفٌ محجوبٌ عنه."""

THE_DECLARED_FUNCTION_ONLY_TABLE: Final[tuple[tuple[str, str], ...]] = (
    ("قطع", "همزةُ قطعٍ محقَّقةٌ على كرسيّ الألف"),
    ("وصل", "همزةُ وصلٍ ساقطةٌ في الدرج"),
    ("لا_وظيفةَ_همزةٍ", "ألفُ مدٍّ لا همزَ فيها"),
)
"""قاعدةٌ مُعلَنةٌ قبل التشغيل: مضمونُ الوقوع من وظيفته وحدَها. تُختبَر ولا تُصدَّق."""


def a_declared_function_only_reader() -> LadderReader:
    """قارئٌ مستقلٌّ عن القطع: يقرأ الوظيفةَ وحدَها ويُجيب بجدولٍ مُعلَنٍ سلفًا."""

    table = dict(THE_DECLARED_FUNCTION_ONLY_TABLE)

    def read(value: tuple[tuple[str, str], ...]) -> str:
        for name, held in value:
            if name == _FUNCTION_FIELD:
                if held not in table:
                    raise LayerOrderError(
                        f"وظيفةٌ «{held}» خارجَ الجدول المُعلَن؛ والقارئُ لا يخمّن"
                    )
                return table[held]
        raise LayerOrderError("قيمةُ السلّم لا تبلغ حقلَ الوظيفة؛ ولا يقرأ هذا القارئ")

    return read


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

A_LADDER_THAT_CITES_ITS_TARGET_PROVES_NOTHING_NOTE: Final[str] = (
    "ALadderThatCitesItsTargetProvesNothing: كان السلّمُ يستشهد بحقل المضمون "
    "نفسِه في طبقة الإفادة، فكان يقرأ جوابَه ثمّ يُحسَب له استرجاعًا؛ والمضمونُ "
    "الآن هدفٌ محجوزٌ خارجَ حقول القطعة، و`ObservedItem` ترفض تسجيلَه فيها، "
    "و`refuse_a_ladder_that_reads_its_target` ترفض الاستشهادَ به"
)

A_LOOKUP_READER_IS_NOT_A_LINGUISTIC_RULE_NOTE: Final[str] = (
    "ALookupReaderIsNotALinguisticRule: `a_lookup_reader` جدولٌ مبنيٌّ من القطع "
    "المُعلَنة نفسِها؛ فنجاحُه يُثبت أنّ قيمةَ السلّم تُميّز هذه القطع، ولا "
    "يُثبت قاعدةً لغويّةً تستخرج المضمون — ولذلك `is_a_linguistic_rule` كاذبةٌ "
    "بالبناء لا بالقياس"
)

THE_READER_IS_ASKED_ONCE_PER_DISTINCT_VALUE_NOTE: Final[str] = (
    "TheReaderIsAskedOncePerDistinctValue: القارئُ لا يرى إلّا قيمةَ السلّم، "
    "ويُسأل مرّةً واحدةً لكلّ قيمةٍ متمايزة، ثمّ يُقابَل جوابُه بأهداف كلّ "
    "القطع المشترِكة فيها؛ فإن دمجت قيمةٌ هدفين مختلفين رُدَّت التجربةُ قبل "
    "سؤاله أصلًا، ولا يستطيع قارئٌ أن يميّز ما لم يُميَّز له"
)

AN_INDEPENDENT_READER_FAILED_WHERE_A_LOOKUP_SUCCEEDED_NOTE: Final[str] = (
    "AnIndependentReaderFailedWhereALookupSucceeded: قارئُ الجدول المبنيِّ من "
    "القطع يُصيب، وقارئُ القاعدة المُعلَنة سلفًا «المضمونُ من الوظيفة وحدَها» "
    "يُخطئ في قطعٍ مُحصاةٍ بالتشغيل؛ فالفرقُ بينهما قياسٌ لقدر ما أضافه الجدولُ "
    "لا لقدر ما أضافه السلّم، والقاعدةُ المُعلَنة مُفنَّدةٌ على هذه القطع"
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
    A_LADDER_THAT_CITES_ITS_TARGET_PROVES_NOTHING_NOTE,
    THE_READER_IS_ASKED_ONCE_PER_DISTINCT_VALUE_NOTE,
    A_LOOKUP_READER_IS_NOT_A_LINGUISTIC_RULE_NOTE,
    AN_INDEPENDENT_READER_FAILED_WHERE_A_LOOKUP_SUCCEEDED_NOTE,
)
"""البواقي المُسمّاة؛ تُعَدّ في الاختبار ولا يُكتَب عددُها بجانبها."""
