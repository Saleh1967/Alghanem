"""العمومُ والخصوص: تخصيصُ العام بالمفهوم بلا إهمال الدليل الأوّل (الحلقة ١٠).

تسجيلٌ لا شهادة: لا مصدرَ مسمًّى ولا شاهدَ منقولًا بنصّه لكل فرعٍ هنا، فالمُخرَج
«تسجيل» على منوال `qiyas_rabt_registration` و`riwaya_diraya_registration`، لا
«شهادة» على منوال `word_class_formal` وأخواتها. وادّعاءُ عنوان الشهادة بلا نصٍّ
مصدريٍّ مُثبَتٍ هو بعينه ما تمنعه تلك الوحدات.

**القاعدةُ المُنفَّذة: يُخصَّص العامُّ بالمفهوم دون إهمال الدليل الأوّل**::

    Takhsis != Ihmal
    التخصيص  != الإهمال

فالتخصيصُ إعمالُ الدليلين معًا: يبقى العامُّ حجّةً فيما وراء موضع التخصيص،
ويعمل الخاصُّ في موضعه. وإسقاطُ أحدهما ليس تخصيصًا بل إهمالًا لدليلٍ قائم،
فيفشل عنده **الإنشاء** ولا يصدر عنه تحذير: لا حقلَ في هذه الوحدة يُكتَب فيه
«المُهمَل»، ويُفحَص ذلك عند الاستيراد على حقول الأصناف نفسها.

**وقناةُ التخصيص مستوردةٌ لا منسوخة**: `DalalaChannel` من `mantuq_mafhum_ifada`
هي مفردةُ المنطوق والمفهوم، فلا تُكتَب هنا مفردةٌ ثانيةٌ بالأسماء نفسها —
والازدواجُ يُنشئ مفهومَين باسمٍ واحد، وهو ما نبّهت عليه تلك الوحدةُ نفسها في
اشتراك لفظ «مفهوم» بين طبقتين.

**والتعارضُ دعوًى تحتاج إثباتًا لا حالةٌ افتراضية**، على نصّ
`DEFAULT_IS_DIFFERENCE_NOT_CONTRADICTION_NOTE` في `apparent_conflict`: فلا
يُسجَّل تخصيصٌ إلا ببيان موضع التعارض بالاسم، لأن تخصيصًا بلا تعارضٍ مُبيَّن
يُضيّق عامًّا لم يُعارِضه شيء.

**والقاعدةُ العامةُ تُفرَّع على أفرادٍ، والقاعدةُ الكلّيةُ تُفرَّع على جزئيات،
ولا تُخلَطان.** والموضوعُ مجاورٌ لـ`kulli_juzi_formal` لا مندمجٌ فيه، ولذلك لم
تُستورَد مفردةُ `Universality` منها: تلك تُصنِّف **اللفظَ المفرد** كلّيًّا أو
جزئيًّا بشواهدَ مُثبَتةٍ من مصدرٍ مُسمًّى، وهذه تُسجِّل **جنسَ قاعدةٍ** ومسارَ
تفريعها. و`جزئي` هناك ليس مقابلَ `قاعدة_عامة` هنا بحال، فاستيرادُ تلك المفردة
لأجل هذا الاشتقاق يُقابِل الجزئيَّ بالعامّ وهو خلطٌ في الجنس نفسه — وهو بعينه
ما تمنعه هذه الحلقة. فمفردةُ `RuleGenus` مستقلّةٌ هنا، والمسارُ يُشتَقّ منها
ولا يُكتَب حرًّا.

**وهذه الوحدة تسجيلٌ لا سلطة**: لا تُصدر ولادةً ولا تجميدًا ولا `E0`، ولا
تستورد من `kernel/` شيئًا، ولا تقرؤها وحدةٌ فيه.
"""

from __future__ import annotations

from dataclasses import dataclass, fields
from enum import Enum
from typing import Final

from .mantuq_mafhum_ifada import DalalaChannel

__all__ = [
    "CONFLICT_MUST_BE_NAMED_NOTE",
    "GENERAL_REMAINS_AUTHORITATIVE_OUTSIDE_NOTE",
    "TAFRI_PATHS_ARE_NOT_MIXED_NOTE",
    "TAKHSIS_IS_NOT_IHMAL_NOTE",
    "UMUM_KHUSUS_IS_NOT_A_GATE_NOTE",
    "DalilRegistration",
    "DalilScope",
    "RuleGenus",
    "TafriPath",
    "TafriRegistration",
    "TakhsisChannel",
    "TakhsisRegistration",
    "UmumKhususError",
    "derive_takhsis_channel",
    "tafri_path_of",
]


class UmumKhususError(ValueError):
    """رفضٌ صريحٌ في تسجيل العموم والخصوص؛ لا يُحمَل على أقرب حالةٍ مقبولة."""


class DalilScope(Enum):
    """سعةُ الدليل في لفظه؛ مفردةٌ ثنائيةٌ مغلقةٌ لا درجةَ بينهما."""

    عام = "عام"
    خاص = "خاص"


class TakhsisChannel(Enum):
    """قناةُ المُخصِّص، مُشتَقّةً من قناة دلالته لا مكتوبةً في حقل.

    والعضوُ الثالث `لا_تخصيص` تصريحٌ لا صمت، على منهج `MafhumKind.لا_ينطبق`:
    التصريحُ بأن التخصيص لم يقع جزءٌ من البنية، لا فراغٌ يُقرأ كما يشاء قارئه.
    """

    تخصيص_بمنطوق = "تخصيص_بمنطوق"
    تخصيص_بمفهوم = "تخصيص_بمفهوم"
    لا_تخصيص = "لا_تخصيص"


class RuleGenus(Enum):
    """جنسُ القاعدة؛ مفردةٌ ثنائيةٌ مغلقةٌ مستقلّةٌ عن تصنيف اللفظ المفرد.

    و«عامّة» هنا وصفُ **قاعدةٍ** يشمل لفظُها أفرادًا، لا وصفُ لفظٍ مفردٍ في
    `kulli_juzi_formal`؛ والموضوعان متجاوران لا مندمجان.
    """

    قاعدة_عامة = "قاعدة_عامة"
    قاعدة_كلية = "قاعدة_كلية"


class TafriPath(Enum):
    """مسارُ التفريع؛ مفردةٌ ثنائيةٌ مغلقة، والمساران لا يُخلَطان."""

    قاعدة_عامة_على_أفراد = "قاعدة_عامة_على_أفراد"
    قاعدة_كلية_على_جزئيات = "قاعدة_كلية_على_جزئيات"


TAKHSIS_IS_NOT_IHMAL_NOTE: Final[str] = (
    "التخصيصُ إعمالُ الدليلين معًا لا إسقاطُ أحدهما: يعمل الخاصُّ في موضعه، "
    "ويبقى العامُّ حجّةً فيما وراءه. ومن أسقط العامَّ لأجل الخاصّ فقد أهمل "
    "دليلًا قائمًا وسمّاه تخصيصًا؛ ولذلك لا حقلَ «مُهمَل» في هذه الوحدة، "
    "والدليلان يبقيان معًا في كل تسجيل."
)

GENERAL_REMAINS_AUTHORITATIVE_OUTSIDE_NOTE: Final[str] = (
    "بقاءُ العامّ حجّةً فيما وراء موضع التخصيص حالٌ مُشتَقّةٌ من بنية التسجيل "
    "نفسها لا دعوى تُكتَب: ما دام الدليلُ العامُّ محفوظًا في التسجيل بموضعه "
    "المُسمّى، فموضعُ التخصيص وحده هو المستثنى، وما عداه على عمومه."
)

CONFLICT_MUST_BE_NAMED_NOTE: Final[str] = (
    "الأصلُ عدمُ التعارض، والتعارضُ دعوًى تحتاج إثباتًا لا حالةٌ افتراضيةٌ "
    "تُقبَل بمجرّد التشابه (`DEFAULT_IS_DIFFERENCE_NOT_CONTRADICTION_NOTE`). "
    "فتسجيلُ تخصيصٍ يلزمه بيانُ موضع التعارض بالاسم، وتخصيصٌ بلا تعارضٍ "
    "مُبيَّنٍ يُضيّق عامًّا لم يُعارِضه شيء."
)

TAFRI_PATHS_ARE_NOT_MIXED_NOTE: Final[str] = (
    "القاعدةُ العامّةُ تُفرَّع على أفرادها، والقاعدةُ الكلّيةُ تُفرَّع على "
    "جزئياتها، والمساران متغايران لا مترادفان: الأفرادُ أعيانٌ يشملها لفظُ "
    "العامّ، والجزئياتُ حصصٌ من معنى الكلّي. وخلطُهما يُفرِّع كلّيًّا على أعيانٍ "
    "لم يشملها لفظُه، أو يُفرِّع عامًّا على حصصٍ ليست أفرادَه."
)

UMUM_KHUSUS_IS_NOT_A_GATE_NOTE: Final[str] = (
    "تسجيلٌ لا سلطة: لا تُصدر هذه الوحدة ولادةً ولا حكمَ ولادة ولا تجميدًا ولا "
    "`E0`، ولا تستورد من `kernel/` شيئًا، ولا تقرؤها وحدةٌ فيه."
)

_CHANNEL_BY_DALALA: Final[dict[DalalaChannel, TakhsisChannel]] = {
    DalalaChannel.منطوق: TakhsisChannel.تخصيص_بمنطوق,
    DalalaChannel.مفهوم: TakhsisChannel.تخصيص_بمفهوم,
}

_PATH_BY_RULE_GENUS: Final[dict[RuleGenus, TafriPath]] = {
    RuleGenus.قاعدة_عامة: TafriPath.قاعدة_عامة_على_أفراد,
    RuleGenus.قاعدة_كلية: TafriPath.قاعدة_كلية_على_جزئيات,
}

_FORBIDDEN_FIELD_MARKERS: Final[tuple[str, ...]] = (
    "count",
    "number",
    "total",
    "verdict",
    "birth",
    "freeze",
    "rank",
    "dropped",
    "ignored",
    "مهمل",
    "مُهمَل",
)


def _require_non_blank(value: str, label: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise UmumKhususError(f"{label} نصٌّ غير فارغ.")
    return value


def derive_takhsis_channel(channel: DalalaChannel) -> TakhsisChannel:
    """اشتقّ قناةَ التخصيص من قناة دلالة المُخصِّص؛ ولا موضعَ تُكتَب فيه."""

    if not isinstance(channel, DalalaChannel):
        raise UmumKhususError(
            "قناةُ الدلالة من مفردة `DalalaChannel` وحدها، مستورَدةً لا منسوخة."
        )
    return _CHANNEL_BY_DALALA[channel]


def tafri_path_of(genus: RuleGenus) -> TafriPath:
    """اشتقّ مسارَ التفريع من جنس القاعدة؛ فالمسارُ لا يُكتَب حرًّا."""

    if not isinstance(genus, RuleGenus):
        raise UmumKhususError(
            "جنسُ القاعدة من مفردته المغلقة الثنائية، لا من تصنيف اللفظ المفرد."
        )
    return _PATH_BY_RULE_GENUS[genus]


@dataclass(frozen=True, slots=True)
class DalilRegistration:
    """دليلٌ مُسجَّل: موضعُه، ونصُّه المقروء، وسعتُه، وقناةُ دلالته."""

    reference: str
    wording: str
    scope: DalilScope
    channel: DalalaChannel

    def __post_init__(self) -> None:
        _require_non_blank(self.reference, "موضعُ الدليل")
        _require_non_blank(self.wording, "نصُّ الدليل المقروء")
        if not isinstance(self.scope, DalilScope):
            raise UmumKhususError("سعةُ الدليل من مفردتها المغلقة الثنائية.")
        if not isinstance(self.channel, DalalaChannel):
            raise UmumKhususError(
                "قناةُ الدليل من مفردة `DalalaChannel` وحدها، مستورَدةً لا منسوخة."
            )

    @property
    def is_general(self) -> bool:
        return self.scope is DalilScope.عام


@dataclass(frozen=True, slots=True)
class TakhsisRegistration:
    """تخصيصٌ مُسجَّل: دليلان يبقيان معًا، وموضعُ تعارضٍ مُسمًّى.

    لا حقلَ هنا لدليلٍ مُهمَل ولا لدليلٍ راجح: التسجيلُ يحمل العامَّ والخاصَّ
    كليهما، وقناةُ التخصيص تُشتَقّ من قناة الخاصّ وحدها.
    """

    general: DalilRegistration
    specializer: DalilRegistration
    conflict_locus: str

    def __post_init__(self) -> None:
        for value, label in (
            (self.general, "الدليلُ العام"),
            (self.specializer, "الدليلُ المُخصِّص"),
        ):
            if not isinstance(value, DalilRegistration):
                raise UmumKhususError(f"{label} دليلٌ مُسجَّلٌ مُصاغ، لا نصٌّ حرّ.")
        if self.general.scope is not DalilScope.عام:
            raise UmumKhususError(
                "المُخصَّصُ دليلٌ عامٌّ في لفظه؛ وتخصيصُ خاصٍّ بخاصٍّ ليس تخصيصًا."
            )
        if self.specializer.scope is not DalilScope.خاص:
            raise UmumKhususError("المُخصِّصُ دليلٌ خاصٌّ في لفظه؛ وعامٌّ لا يُخصِّص عامًّا مثلَه.")
        if self.general.reference == self.specializer.reference:
            raise UmumKhususError("دليلٌ يُخصِّص نفسَه ليس تخصيصًا بل إعادةَ قراءةٍ لنصٍّ واحد.")
        _require_non_blank(self.conflict_locus, "موضعُ التعارض")

    @property
    def channel(self) -> TakhsisChannel:
        """قناةُ التخصيص مُشتَقّةً من قناة المُخصِّص، لا مكتوبةً في حقل."""

        return derive_takhsis_channel(self.specializer.channel)

    @property
    def retained(self) -> tuple[DalilRegistration, DalilRegistration]:
        """الدليلان معًا: `Takhsis != Ihmal`، فلا يسقط أحدُهما بالتسجيل."""

        return (self.general, self.specializer)

    @property
    def general_remains_authoritative_outside_locus(self) -> bool:
        """العامُّ حجّةٌ فيما وراء موضع التخصيص؛ حالٌ بنيويةٌ لا دعوى تُكتَب."""

        return True

    @property
    def specialized_by_mafhum(self) -> bool:
        """أوقع التخصيصُ بمفهومٍ لا بمنطوق؟ سؤالُ الحلقة العاشرة بعينه."""

        return self.channel is TakhsisChannel.تخصيص_بمفهوم


@dataclass(frozen=True, slots=True)
class TafriRegistration:
    """تفريعٌ مُسجَّل: قاعدةٌ بجنسها، وما فُرِّعت عليه، ومسارٌ مُشتَقّ لا مكتوب."""

    rule_reference: str
    rule_genus: RuleGenus
    branched_onto: tuple[str, ...]
    declared_path: TafriPath

    def __post_init__(self) -> None:
        _require_non_blank(self.rule_reference, "موضعُ القاعدة")
        if not isinstance(self.rule_genus, RuleGenus):
            raise UmumKhususError(
                "جنسُ القاعدة من مفردته المغلقة الثنائية، لا من تصنيف اللفظ المفرد."
            )
        if not isinstance(self.branched_onto, tuple) or not self.branched_onto:
            raise UmumKhususError(
                "التفريعُ يقع على شيءٍ مُسمًّى؛ وتفريعٌ على لا شيء ليس تفريعًا."
            )
        for item in self.branched_onto:
            _require_non_blank(item, "ما فُرِّعت عليه القاعدة")
        if len(set(self.branched_onto)) != len(self.branched_onto):
            raise UmumKhususError("عنصرٌ مُعادٌ باسمه نفسه ليس عنصرًا ثانيًا.")
        if not isinstance(self.declared_path, TafriPath):
            raise UmumKhususError("مسارُ التفريع من مفردته المغلقة الثنائية.")
        if self.declared_path is not self.path:
            raise UmumKhususError(
                "المسارُ المكتوب يخالف المُشتَقّ من جنس القاعدة: "
                f"{TAFRI_PATHS_ARE_NOT_MIXED_NOTE}"
            )

    @property
    def path(self) -> TafriPath:
        """المسارُ مُشتَقًّا من جنس القاعدة وحده."""

        return tafri_path_of(self.rule_genus)


def _assert_no_fields_matching(markers: tuple[str, ...]) -> None:
    for declaring_type in (
        DalilRegistration,
        TakhsisRegistration,
        TafriRegistration,
    ):
        for field in fields(declaring_type):
            for marker in markers:
                if marker in field.name.lower():
                    raise RuntimeError(
                        f"{declaring_type.__name__} يحمل حقلاً محظورًا: {field.name}"
                    )


if len(DalilScope) != 2:  # pragma: no cover - guard
    raise RuntimeError("سعةُ الدليل ثنائيةٌ مغلقة: عامٌّ أو خاصّ.")
if len(TakhsisChannel) != 3:  # pragma: no cover - guard
    raise RuntimeError("قناةُ التخصيص ثلاثيةٌ مغلقة، و«لا_تخصيص» عضوٌ مُسمًّى فيها.")
if len(TafriPath) != 2:  # pragma: no cover - guard
    raise RuntimeError("مسارا التفريع اثنان لا يُخلَطان.")
if set(_CHANNEL_BY_DALALA) != set(DalalaChannel):  # pragma: no cover - guard
    raise RuntimeError("اشتقاقُ قناة التخصيص غيرُ تامٍّ على قناتَي الدلالة.")
if len(RuleGenus) != 2:  # pragma: no cover - guard
    raise RuntimeError("جنسُ القاعدة ثنائيٌّ مغلق: عامّةٌ أو كلّية.")
if set(_PATH_BY_RULE_GENUS) != set(RuleGenus):  # pragma: no cover - guard
    raise RuntimeError("اشتقاقُ مسار التفريع غيرُ تامٍّ على جنسَي القاعدة.")
if TakhsisChannel.لا_تخصيص in _CHANNEL_BY_DALALA.values():  # pragma: no cover - guard
    raise RuntimeError("«لا_تخصيص» لا تُشتَقّ من قناةِ مُخصِّصٍ قائم.")
_assert_no_fields_matching(_FORBIDDEN_FIELD_MARKERS)
