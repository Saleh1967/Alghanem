"""المنطوق والمفهوم والإفادة: ثلاثُ مفرداتٍ مغلقةٍ منفصلة، وحالٌ تُشتَقّ لا تُكتَب.

هذه الوحدة مفردةُ دلالةٍ في الطبقة العربية، تقوم إلى جانب `maluma_mafhum` و
`madlul_alone_formal` و`comprehension_defect` ولا تُدمَج في أيٍّ منها::

    DalalaChannel != ContentStanding
    Ifada         != Attainment
    Classification!= Verdict

**اشتراكُ لفظِ «مفهوم» بين طبقتين يُسمّى هنا صراحةً ولا يُطوى.** `ContentStanding.مفهوم`
في `maluma_mafhum.py` حالُ **محتوًى** أُسنِد إلى حسٍّ فصار واقعًا مُدرَكًا في الذهن،
ومقابلُه `معلومة`. و`DalalaChannel.مفهوم` هنا **قناةُ دلالةٍ** في لفظٍ: ما دلّ عليه
اللفظُ لا بمنطوقه، ومقابلُه `منطوق`. فهما اسمان متّفقان لفظًا مختلفان موضوعًا،
ودمجُهما — أو استيرادُ أحدهما مكان الآخر — يُسقط الفارق بين «أسُنِد إلى حسّ؟» و
«أحُمِل على اللفظ نفسه؟». ولذلك لا تستورد هذه الوحدة `ContentStanding` ولا تُحوّل
إليها.

**مفرداتٌ ثلاث لا مقياسٌ واحد، مع تعليل كلّ دمجٍ مرفوض:**

* `DalalaChannel` و`MafhumKind` لا تُدمَجان في مفردةٍ رباعية: قسمةُ الموافقة
  والمخالفة قسمةٌ **داخل** المفهوم وحده، ورفعُها إلى مستوى القناة يجعل «موافقة»
  بديلًا عن «منطوق» وهو ليس بديلًا عنه بل قسمًا من قسيمه.
* `IfadaStanding` لا تُدمَج فيهما ولا تصير درجةً في سُلَّم: الإفادةُ وصفُ ما بلغه
  التركيبُ من فائدةٍ مقروءة، لا وصفٌ لقناة الدلالة؛ فمنطوقٌ غيرُ مُفيد ومفهومٌ مُفيد
  كلاهما قائم، ولا يُشتَقّ أحدُهما من الآخر.
* ولا تُستحدَث رتبةٌ رابعة ولا نسبةٌ ولا ترتيبٌ بين لفظين: التقديرُ حكمٌ لا سلطةَ
  لهذه الطبقة به، ويُفحَص منعُه على أسماء حقول كلّ صنفٍ هنا عند الاستيراد.

**الجهلُ عضوٌ مُصرَّحٌ به لا فراغٌ يُطوى**: `IfadaStanding.غير_مقروء` عضوٌ في
المفردة على مثال `لا_ينطبق` في `comprehension_defect`، فغيابُ قراءةِ الفائدة لا
يُقرَأ انتفاءً لها.

**المصدر النصّي للإفادة، مُستشهَدًا به لا مُعادًا اشتقاقه.** الفارقُ بين «موجود»
و«مُفيد» منقولٌ عن النصّ المُثبَت في `madlul_alone_formal.py` في القسم الخامس
(الهذيان): "هذا القسم غير موضوع، أي لم تضعه العرب؛ لأن الغرض من التركيب الإفادة،
وهذا لا يفيد؛ ولكنه موجود." فـ`غير_مُفيد` حالٌ لتركيبٍ **قائم** لا لتركيبٍ معدوم،
وهذا هو بعينه ما يمنع قراءةَ عدم الإفادة غيابًا.

**الحالُ تُشتَقّ من حواملها ولا تُكتَب** (على منهج `UnderstandingRecord.standing`):
كلّ سجلٍّ يحمل حواملَه — حاملَ القناة، وحاملَ قسم المفهوم، وحاملَ الإفادة مع شاهده
— وتُشتَقّ الأحوالُ الثلاثة منها، وتُرفَض الحالُ المُعلَنة المخالفة عند الإنشاء.

**خمولٌ سلطويّ**: لا ولادةَ هنا ولا حكمَ ولادة ولا تجميد ولا `E0`، ولا تقرأ هذه
المخرجاتِ بوّابةٌ في `kernel/`، ولا تدخل `BirthExperimentSpecification`.
"""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass, fields
from enum import Enum
from types import MappingProxyType
from typing import Final

__all__ = [
    "BENEFIT_IS_READ_NOT_ASSUMED_NOTE",
    "IFADA_SOURCE_TEXT_NOTE",
    "MAFHUM_IS_NOT_CONTENT_STANDING_NOTE",
    "MANTUQ_MAFHUM_IFADA_AUTHORITY_NOTE",
    "STANDING_IS_DERIVED_NOT_WRITTEN_NOTE",
    "DalalaCensus",
    "DalalaChannel",
    "DalalaRecord",
    "IfadaStanding",
    "MafhumKind",
    "MantuqMafhumIfadaError",
]


MANTUQ_MAFHUM_IFADA_AUTHORITY_NOTE: Final[str] = (
    "تصنيفٌ وتوثيقٌ فقط: لا تُنتج هذه الوحدة ولادةً ولا حكمَ ولادة، ولا "
    "تُجمِّد، ولا تُصدر `E0`، ولا تقرؤها بوّابةٌ في النواة"
)

MAFHUM_IS_NOT_CONTENT_STANDING_NOTE: Final[str] = (
    "`DalalaChannel.مفهوم` قناةُ دلالةٍ في لفظ، و`ContentStanding.مفهوم` حالُ "
    "محتوًى أُسنِد إلى حسّ؛ اسمان متّفقان لفظًا مختلفان موضوعًا، وحملُ أحدهما "
    "على الآخر يُسقط الفارق بين الإسناد إلى حسٍّ والحملِ على اللفظ"
)

IFADA_SOURCE_TEXT_NOTE: Final[str] = (
    "الغرض من التركيب الإفادة، وهذا لا يفيد؛ ولكنه موجود — نصٌّ مُثبَتٌ في "
    "`madlul_alone_formal.py`، وبه تُفرَّق حالُ `غير_مُفيد` عن الغياب: هي حالُ "
    "تركيبٍ قائمٍ لا تركيبٍ معدوم"
)

BENEFIT_IS_READ_NOT_ASSUMED_NOTE: Final[str] = (
    "`غير_مقروء` عضوٌ مُصرَّحٌ به في المفردة لا فراغٌ يُطوى: ما لم تُقرَأ "
    "فائدتُه لا يُقرَأ غيرَ مُفيد، ولا مُفيدًا"
)

STANDING_IS_DERIVED_NOT_WRITTEN_NOTE: Final[str] = (
    "الأحوالُ الثلاثة تُشتَقّ من حواملها، والحالُ المُعلَنة المخالفة تُرفَض عند "
    "الإنشاء ولا تُقرَّر"
)

_FORBIDDEN_FIELD_MARKERS: Final[tuple[str, ...]] = (
    "count",
    "total",
    "score",
    "rank",
    "percent",
    "ratio",
    "progress",
    "priority",
    "verdict",
    "birth",
    "attainment",
)


class MantuqMafhumIfadaError(ValueError):
    """رفضٌ صريحٌ في قراءة القناة أو قسم المفهوم أو الإفادة."""


class DalalaChannel(Enum):
    """قناةُ الدلالة: أدلّ اللفظُ بمنطوقه أم بما يُفهَم منه؟

    ليست سُلَّمًا ولا تقديرَ قوّة: المنطوق ليس «أعلى» من المفهوم ولا أقربَ إلى
    أيّ بلوغ، وإنما هما موضعان مختلفان للدلالة من اللفظ نفسه.
    """

    منطوق = "منطوق"
    مفهوم = "مفهوم"


class MafhumKind(Enum):
    """قسمةُ المفهوم وحده: موافقةٌ لحكم المنطوق أم مخالفةٌ له، أو لا ينطبق.

    `لا_ينطبق` قيمةٌ مصرَّحٌ بها لا `None` صامتة، على منهج `comprehension_defect`:
    التصريحُ بأن القسمة لم تُطرَح أصلًا — لأن القناة منطوق — جزءٌ من البنية.
    """

    موافقة = "موافقة"
    مخالفة = "مخالفة"
    لا_ينطبق = "لا_ينطبق"


class IfadaStanding(Enum):
    """حالُ الإفادة: أبلغ التركيبُ فائدةً مقروءة، أم لم يُفِد، أم لم تُقرَأ؟"""

    مُفيد = "مُفيد"
    غير_مُفيد = "غير_مُفيد"
    غير_مقروء = "غير_مقروء"

    @property
    def is_read(self) -> bool:
        """أقُرئت الفائدةُ أصلًا؟ فعدمُ القراءة ليس عدمَ إفادة."""

        return self is not IfadaStanding.غير_مقروء


if len(DalalaChannel) != 2:  # pragma: no cover - guard
    raise RuntimeError("قناةُ الدلالة ثنائيةٌ مغلقة.")
if len(MafhumKind) != 3:  # pragma: no cover - guard
    raise RuntimeError("قسمةُ المفهوم ثلاثيةٌ مغلقة، وعدمُ الانطباق عضوٌ فيها.")
if len(IfadaStanding) != 3:  # pragma: no cover - guard
    raise RuntimeError("حالُ الإفادة ثلاثيةٌ مغلقة، والجهلُ عضوٌ فيها.")


def _require_non_blank(value: str, label: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise MantuqMafhumIfadaError(f"{label} نصٌّ غير فارغ.")
    return value


def _require_blank(value: str, label: str, reason: str) -> str:
    if not isinstance(value, str) or value:
        raise MantuqMafhumIfadaError(f"{label} يبقى فارغًا: {reason}")
    return value


@dataclass(frozen=True, slots=True)
class DalalaRecord:
    """قراءةُ لفظٍ واحد: قناتُه، وقسمُ مفهومه، وحالُ إفادته — كلُّها مُشتَقّة.

    الحواملُ ثلاثة، واحدٌ لكلّ حالٍ مُشتَقّة:

    * `carried_by_the_wording` حاملُ القناة: أحُمِلت الدلالةُ على اللفظ نفسه؟
    * `agrees_with_the_uttered_ruling` حاملُ قسم المفهوم، ولا يُملأ إلا للمفهوم.
    * `composition_benefits` حاملُ الإفادة، و`None` فيه قراءةٌ لم تقع لا انتفاء.

    و`benefit_witness` شاهدُ الإفادة المقروء: يلزم متى قُرئت الفائدة — إفادةً أو
    عدمَها — ويبقى فارغًا متى لم تُقرَأ، فلا يُسنَد حكمٌ إلى شاهدٍ لم يُذكَر.
    """

    lafz: str
    madlul: str
    carried_by_the_wording: bool
    agrees_with_the_uttered_ruling: bool | None
    composition_benefits: bool | None
    benefit_witness: str
    declared_channel: DalalaChannel
    declared_mafhum_kind: MafhumKind
    declared_ifada: IfadaStanding

    def __post_init__(self) -> None:
        _require_non_blank(self.lafz, "اللفظ")
        _require_non_blank(self.madlul, "المدلول المقروء")

        if not isinstance(self.carried_by_the_wording, bool):
            raise MantuqMafhumIfadaError("حاملُ القناة قيمةٌ ثنائية.")

        if self.carried_by_the_wording:
            if self.agrees_with_the_uttered_ruling is not None:
                raise MantuqMafhumIfadaError(
                    "قسمةُ الموافقة والمخالفة قسمةٌ داخل المفهوم وحده؛ "
                    "وملؤها على منطوقٍ يرفع قسمًا إلى مقام قسيمه."
                )
        elif not isinstance(self.agrees_with_the_uttered_ruling, bool):
            raise MantuqMafhumIfadaError(
                "المفهومُ يلزمه حاملُ قسمه: موافقٌ لحكم المنطوق أم مخالفٌ له."
            )

        if self.composition_benefits is None:
            _require_blank(
                self.benefit_witness,
                "شاهد الإفادة",
                "ما لم تُقرَأ فائدتُه لا شاهدَ له يُكتَب",
            )
        elif not isinstance(self.composition_benefits, bool):
            raise MantuqMafhumIfadaError("حاملُ الإفادة قيمةٌ ثنائيةٌ أو غيرُ مقروء.")
        else:
            _require_non_blank(self.benefit_witness, "شاهد الإفادة")

        for declared, derived, label in (
            (self.declared_channel, self.channel, "قناةُ الدلالة"),
            (self.declared_mafhum_kind, self.mafhum_kind, "قسمُ المفهوم"),
            (self.declared_ifada, self.ifada, "حالُ الإفادة"),
        ):
            if not isinstance(declared, type(derived)):
                raise MantuqMafhumIfadaError(f"{label} من مفردتها المغلقة.")
            if declared is not derived:
                raise MantuqMafhumIfadaError(
                    f"{label} المكتوبة تخالف المُشتَقّة من حاملها: "
                    f"{STANDING_IS_DERIVED_NOT_WRITTEN_NOTE}"
                )

    @property
    def channel(self) -> DalalaChannel:
        """القناةُ مُشتقّةً من حاملها وحده."""

        if self.carried_by_the_wording:
            return DalalaChannel.منطوق
        return DalalaChannel.مفهوم

    @property
    def mafhum_kind(self) -> MafhumKind:
        """قسمُ المفهوم مُشتقًّا، و`لا_ينطبق` تصريحٌ بأن القسمة لم تُطرَح."""

        if self.carried_by_the_wording:
            return MafhumKind.لا_ينطبق
        if self.agrees_with_the_uttered_ruling:
            return MafhumKind.موافقة
        return MafhumKind.مخالفة

    @property
    def ifada(self) -> IfadaStanding:
        """حالُ الإفادة مُشتقّةً من حاملها، وعدمُ القراءة عضوٌ لا فراغ."""

        if self.composition_benefits is None:
            return IfadaStanding.غير_مقروء
        if self.composition_benefits:
            return IfadaStanding.مُفيد
        return IfadaStanding.غير_مُفيد


@dataclass(frozen=True, slots=True)
class DalalaCensus:
    """إحصاءُ قراءاتٍ مُصاغة: تعدادٌ بكلّ مفردةٍ من الثلاث، بلا حقل عدد.

    وكلّ عضوٍ في كلّ مفردةٍ حاضرٌ في التعداد ولو بصفر، فالصفرُ المقروء لا يُطوى
    ولا يُقرَأ غيابًا للعضو من المفردة.
    """

    records: tuple[DalalaRecord, ...]

    def __post_init__(self) -> None:
        if not isinstance(self.records, tuple):
            raise MantuqMafhumIfadaError("الإحصاءُ مجموعةٌ من القراءات المُصاغة.")
        for record in self.records:
            if not isinstance(record, DalalaRecord):
                raise MantuqMafhumIfadaError("كلُّ عنصرٍ قراءةٌ مُصاغة، لا نصٌّ حرّ.")

    @property
    def channel_counts(self) -> Mapping[DalalaChannel, int]:
        """تعدادُ القراءات بحسب قناتها، وكلُّ عضوٍ حاضرٌ ولو بصفر."""

        counts = dict.fromkeys(DalalaChannel, 0)
        for record in self.records:
            counts[record.channel] += 1
        return MappingProxyType(counts)

    @property
    def mafhum_kind_counts(self) -> Mapping[MafhumKind, int]:
        """تعدادُ القراءات بحسب قسم مفهومها، وكلُّ عضوٍ حاضرٌ ولو بصفر."""

        counts = dict.fromkeys(MafhumKind, 0)
        for record in self.records:
            counts[record.mafhum_kind] += 1
        return MappingProxyType(counts)

    @property
    def ifada_counts(self) -> Mapping[IfadaStanding, int]:
        """تعدادُ القراءات بحسب حال إفادتها، وكلُّ عضوٍ حاضرٌ ولو بصفر."""

        counts = dict.fromkeys(IfadaStanding, 0)
        for record in self.records:
            counts[record.ifada] += 1
        return MappingProxyType(counts)


def _assert_no_fields_matching(markers: tuple[str, ...]) -> None:
    for declaring_type in (DalalaRecord, DalalaCensus):
        for field in fields(declaring_type):
            for marker in markers:
                if marker in field.name:  # pragma: no cover - guard
                    raise RuntimeError(
                        f"{declaring_type.__name__} يحمل حقلاً محظورًا: {field.name}"
                    )


_assert_no_fields_matching(_FORBIDDEN_FIELD_MARKERS)
