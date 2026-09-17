"""التسجيلُ المسبق لبنود الاختبار العشرة، قبل تشغيل أيّ طبقة.

نصُّ الفرضية مُجمَّدٌ في `fractal_transition_hypothesis`، وهو يشترط بنفسه أن
تُحدَّد عشرةُ بنودٍ **قبل تشغيل البيانات**: الطبقاتُ المُقارَنة، والحاملُ في
كلٍّ منها، والبوّابة، ومعنى حفظ الهوية، وتعريفُ البقية، وتعريفُ الإغلاق،
وتحويلُ تغيير المقياس `S`، ومعيارُ المطابقة، والنموذجُ الأضعف المنافس، وشروطُ
`PASS`/`FAIL`/`UNDERPOWERED`. هذه الوحدةُ هي تلك البنودُ العشرة مكتوبةً، وليس
فيها قراءةٌ واحدة ولا حكمٌ واحد:

    Preregistration != Readout

**وشاهدُ الترتيب في تاريخ المستودع لا في هذا النصّ**: هذه الوحدةُ ووحدةُ
النصّ المُجمَّد تُودَعان في دفعةٍ مستقلّةٍ **قبل أن توجد** وحدةُ القراءة
`fractal_transition_readout`؛ فمن أراد التحقّق من «قانون عدم القفز» قرأ
الترتيب من `git`، لا من دعوى الوحدة عن نفسها.

**والحقلُ لا يُعلَن باسمه بل بمُستخرِجه ومُفنِّده**: كلُّ حقلٍ من الحقول
الستّة يحمل هنا الشيءَ الذي يُقرأ منه، والعبارةَ التي يعنيها في تلك الطبقة
بعينها، و**المدخلَ الحقيقيَّ الذي يُكذّبه** (`what_would_fail_it`). وهذا تنفيذٌ
لقانون `StructurallyUnfalsifiableNegativeIsARecurringPattern` في
`docs/CONSTITUTION.md` §G0.L2.D: من بنى شرطًا لا يُكذّبه مدخلٌ قابلٌ للبناء فقد
سجّل حدَّ أداةٍ لا نتيجةً عن العالم. وحقلٌ بلا مُفنِّدٍ مكتوبٍ يُرَدّ عند
الإنشاء.

**والطبقةُ ولايةُ تجربةٍ لا عضوٌ في مفردةٍ تقليدية** (`NoTraditionalLayerEnum`):
لا يُعرَّف هنا نوعٌ مغلقٌ اسمُه `Layer` قيمُه «صوتيّ/صرفيّ/نحويّ»؛ الطبقةُ
مُعرَّفةٌ بمُعرِّفِ ولايتها ووحدتِها المُرمِّزة في هذا المستودع، وطبقتان
تشتركان في بنيةٍ لا يعني أن إحداهما حالةٌ من الأخرى.

**ومنزلةُ الطبقة مُعلَنةٌ قبل النتيجة لا بعدها**: طبقتا المركّب والجملة لا
تُخرِج أيُّ وحدةٍ في هذا المستودع منهما قراءةً لكلّ ورودٍ على حدة — نصوصُهما
مُزوَّدةٌ في `compound_layer_source_texts` و`sentence_card_source_texts`، ولا
حاملَ مُرمَّزًا يُشتَقّ منه توقيعُ انتقالٍ لصورةٍ بعينها. فالزوجان الثاني
والثالث يُقرآن `UNDERPOWERED` **بالبناء**، وهذا مُسجَّلٌ هنا قبل التشغيل حتى
لا يُقرأ بعده اعتذارًا.

**ولا زوجَ محجوزًا تحت السلّم المُجمَّد** (`NoPairIsHoldoutUnderTheFrozenLadder`):
شرطُ النجاح في النصّ يطلب طبقتين «لم تُستخدما في صياغة الفرضية»، والسلّمُ
المكتوبُ في النصّ نفسه يُسمّي الحرفَ والمقطعَ والقالبَ والكلمةَ والتركيبَ
والجملة. فكلُّ زوجٍ من هذه الطبقات مذكورٌ في نصّ الصياغة، وعضويّتُه
**مُشتَقّةٌ من النصّ لا مكتوبةٌ في حقل**. ولذلك `SUPPORTED` غيرُ بالغةٍ اليوم،
والمدخلُ الذي يرفع ذلك مُسمًّى ولا يُترَك مبهمًا: زوجُ ولايتين مُرمَّزتين
كلتاهما، لا يَرِد اسمُ أيٍّ منهما في `HYPOTHESIS_TEXT`.

**وحقلُ الأثر مُعلَنٌ غيرَ مُميِّزٍ قبل التشغيل**: `Trace` في الطبقتين
المُرمَّزتين صادقٌ بالبناء (كلُّ قراءةٍ تحمل بصمةَ تجميدها أو منزلةَ طبقتها)،
فلا يستطيع أن يقرأ كذبًا على أيّ مدخل، ولا يُميّز بنيةً عن نموذجٍ ثابت. وهذا
مكتوبٌ هنا **قبل** النتيجة، لأن كتابته بعدها تفسيرٌ لنتيجةٍ لا تسجيلٌ لتوقّع.

حدودُ الوحدة: لا بوّابة، ولا حكم، ولا ولادة، ولا `Freeze`، ولا `E0`، ولا وحدةَ
في `kernel/` تقرأ منها.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from pathlib import Path
from typing import Final

from ..canonical_content import canonical_bytes, canonical_digest
from .fractal_transition_hypothesis import (
    COMPARED_FIELDS,
    HYPOTHESIS_DIGEST,
    HYPOTHESIS_TEXT,
    require_compared_field,
)

__all__ = [
    "DECLARED_LAYERS",
    "DECLARED_PAIRS",
    "FROZEN_CASES",
    "MATCH_CRITERION",
    "NO_PAIR_IS_HOLDOUT_UNDER_THE_FROZEN_LADDER_NOTE",
    "PREREGISTRATION_DIGEST",
    "PREREGISTRATION_IS_NOT_A_READOUT_NOTE",
    "SCALE_TRANSPORT",
    "TRACE_IS_DECLARED_NON_DISCRIMINATING_NOTE",
    "WEAKER_MODEL",
    "FieldDeclaration",
    "FractalTransitionPreregistrationError",
    "LayerDeclaration",
    "LayerStanding",
    "MatchCriterion",
    "PairDeclaration",
    "ScaleTransport",
    "WeakerModel",
    "FrozenCase",
    "layer_named",
    "pair_named",
    "preregistration_digest",
]


class FractalTransitionPreregistrationError(ValueError):
    """رُفض تسجيلٌ ناقصٌ أو مُوسَّع؛ ولا يُقبَل حقلٌ بلا مُفنِّدٍ مكتوب."""


class LayerStanding(Enum):
    """منزلةُ الطبقة اليوم؛ ثنائيّةٌ مغلقةٌ لأن كلتا الحالتين واقعة."""

    CODED_AND_MEASURABLE = "مُرمَّزة_تُخرِج_قراءةً_لكلّ_ورود"
    SOURCE_SUPPLIED_NO_CODED_CARRIER = "مصدرٌ_مُقدَّمٌ_بلا_حاملٍ_مُرمَّز"


def _require_text(value: str, field_name: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise FractalTransitionPreregistrationError(
            f"{field_name} نصٌّ غير فارغ؛ ولا يُقبَل فيه الفراغ صمتًا"
        )
    return value


@dataclass(frozen=True, slots=True)
class FieldDeclaration:
    """حقلٌ واحدٌ من الستّة في طبقةٍ بعينها: ما يُقرأ، وما يعني، وما يُكذّبه."""

    field: str
    read_from: str
    statement: str
    what_would_fail_it: str

    def __post_init__(self) -> None:
        require_compared_field(self.field)
        _require_text(self.read_from, "موضعُ القراءة")
        _require_text(self.statement, "بيانُ الحقل")
        _require_text(self.what_would_fail_it, "المدخلُ الذي يُكذّب الحقل")

    def as_canonical_content(self) -> dict[str, str]:
        return {
            "field": self.field,
            "read_from": self.read_from,
            "statement": self.statement,
            "what_would_fail_it": self.what_would_fail_it,
        }


@dataclass(frozen=True, slots=True)
class LayerDeclaration:
    """ولايةُ طبقةٍ واحدة: وحدتُها المُرمِّزة، ومنزلتُها، وحقولُها الستّة."""

    jurisdiction: str
    ladder_name: str
    carrier_module: str
    standing: LayerStanding
    why_this_standing: str
    fields: tuple[FieldDeclaration, ...]

    def __post_init__(self) -> None:
        _require_text(self.jurisdiction, "مُعرِّفُ الولاية")
        _require_text(self.ladder_name, "اسمُ الطبقة في السلّم")
        _require_text(self.carrier_module, "مسارُ وحدة الحامل")
        _require_text(self.why_this_standing, "سببُ المنزلة")
        if not isinstance(self.standing, LayerStanding):
            raise FractalTransitionPreregistrationError(
                "منزلةُ الطبقة عضوٌ في مفردتها المغلقة"
            )
        declared = tuple(item.field for item in self.fields)
        if declared != COMPARED_FIELDS:
            raise FractalTransitionPreregistrationError(
                "حقولُ الطبقة هي الحقولُ الستّةُ بعينها وبترتيبها المُجمَّد؛ "
                "وإسقاطُ حقلٍ أو تكرارُه تغييرٌ للمعيار لا وصفٌ لطبقة"
            )
        module_path = Path(__file__).resolve().parent / self.carrier_module
        if not module_path.exists():
            raise FractalTransitionPreregistrationError(
                f"وحدةُ الحامل «{self.carrier_module}» غيرُ موجودةٍ في الشجرة؛ "
                "وإعلانُ حاملٍ بلا وحدةٍ تقرأه دعوى ترميزٍ بلا مُرمِّز"
            )

    @property
    def is_named_in_the_frozen_ladder(self) -> bool:
        """أوَرَد اسمُ الطبقة في نصّ الصياغة؟ مُشتَقٌّ من النصّ لا مكتوبٌ هنا."""

        return self.ladder_name in HYPOTHESIS_TEXT

    def field_named(self, field: str) -> FieldDeclaration:
        """إعلانُ حقلٍ بعينه في هذه الطبقة؛ وغيرُ المُعلَن يُرَدّ لا يُخترَع."""

        for item in self.fields:
            if item.field == field:
                return item
        raise FractalTransitionPreregistrationError(
            f"الحقل «{field}» غيرُ مُعلَنٍ في الولاية «{self.jurisdiction}»"
        )

    def as_canonical_content(self) -> dict[str, object]:
        return {
            "jurisdiction": self.jurisdiction,
            "ladder_name": self.ladder_name,
            "carrier_module": self.carrier_module,
            "standing": self.standing.value,
            "why_this_standing": self.why_this_standing,
            "fields": [item.as_canonical_content() for item in self.fields],
        }


@dataclass(frozen=True, slots=True)
class ScaleTransport:
    """تحويلُ تغيير المقياس `S_{n\\to m}` مُعرَّفًا قبل رؤية أيّ قراءة."""

    transport_id: str
    statement: str
    what_would_fail_it: str

    def __post_init__(self) -> None:
        _require_text(self.transport_id, "مُعرِّفُ التحويل")
        _require_text(self.statement, "بيانُ التحويل")
        _require_text(self.what_would_fail_it, "المدخلُ الذي يُكذّب التحويل")

    def as_canonical_content(self) -> dict[str, str]:
        return {
            "transport_id": self.transport_id,
            "statement": self.statement,
            "what_would_fail_it": self.what_would_fail_it,
        }


@dataclass(frozen=True, slots=True)
class MatchCriterion:
    """معيارُ المطابقة بين البنيتين، محصورًا بالحقول الستّة لا يتعدّاها."""

    criterion_id: str
    statement: str
    compared_fields: tuple[str, ...]
    refuting_fields: tuple[str, ...]

    def __post_init__(self) -> None:
        _require_text(self.criterion_id, "مُعرِّفُ المعيار")
        _require_text(self.statement, "بيانُ المعيار")
        for field in self.compared_fields:
            require_compared_field(field)
        if self.compared_fields != COMPARED_FIELDS:
            raise FractalTransitionPreregistrationError(
                "المعيارُ يقارن الحقولَ الستّةَ بعينها؛ ولا يُوسَّع ولا يُضيَّق"
            )
        for field in self.refuting_fields:
            require_compared_field(field)
        if set(self.refuting_fields) != {"Gate", "Identity", "Residual", "Closure"}:
            raise FractalTransitionPreregistrationError(
                "أسبابُ التفنيد الأربعةُ منصوصةٌ في الفرضية: البوّابة، وحفظُ "
                "الهوية، والبقية، والإغلاق"
            )

    def as_canonical_content(self) -> dict[str, object]:
        return {
            "criterion_id": self.criterion_id,
            "statement": self.statement,
            "compared_fields": list(self.compared_fields),
            "refuting_fields": list(self.refuting_fields),
        }


@dataclass(frozen=True, slots=True)
class WeakerModel:
    """النموذجُ الأضعفُ المنافس، مُعلَنًا قبل التشغيل لا مُختارًا بعده."""

    model_id: str
    statement: str
    what_it_reads: str
    how_it_could_lose: str

    def __post_init__(self) -> None:
        _require_text(self.model_id, "مُعرِّفُ النموذج")
        _require_text(self.statement, "بيانُ النموذج")
        _require_text(self.what_it_reads, "ما يقرأه النموذج")
        _require_text(self.how_it_could_lose, "الطريقُ الذي يخسر به النموذج")

    def as_canonical_content(self) -> dict[str, str]:
        return {
            "model_id": self.model_id,
            "statement": self.statement,
            "what_it_reads": self.what_it_reads,
            "how_it_could_lose": self.how_it_could_lose,
        }


@dataclass(frozen=True, slots=True)
class PairDeclaration:
    """زوجُ طبقتين مُسجَّلٌ قبل تشغيله، بشروط نجاحه وفشله وقصوره الثلاثة."""

    pair_id: str
    lower_jurisdiction: str
    upper_jurisdiction: str
    pass_condition: str
    fail_condition: str
    underpowered_condition: str
    what_would_lift_underpowered: str

    def __post_init__(self) -> None:
        _require_text(self.pair_id, "مُعرِّفُ الزوج")
        _require_text(self.pass_condition, "شرطُ PASS")
        _require_text(self.fail_condition, "شرطُ FAIL")
        _require_text(self.underpowered_condition, "شرطُ UNDERPOWERED")
        _require_text(self.what_would_lift_underpowered, "ما يرفع القصور")
        if self.lower_jurisdiction == self.upper_jurisdiction:
            raise FractalTransitionPreregistrationError(
                "زوجٌ طرفاه ولايةٌ واحدة يقيس الطبقةَ بنفسها لا بنيةً عبر مقياسين"
            )

    def as_canonical_content(self) -> dict[str, str]:
        return {
            "pair_id": self.pair_id,
            "lower_jurisdiction": self.lower_jurisdiction,
            "upper_jurisdiction": self.upper_jurisdiction,
            "pass_condition": self.pass_condition,
            "fail_condition": self.fail_condition,
            "underpowered_condition": self.underpowered_condition,
            "what_would_lift_underpowered": self.what_would_lift_underpowered,
        }


@dataclass(frozen=True, slots=True)
class FrozenCase:
    """صورةٌ مُجمَّدةٌ قبل القراءة، ومعها سببُ اختيارها المبدئيّ لا نتيجتُها."""

    surface: str
    why_chosen: str

    def __post_init__(self) -> None:
        _require_text(self.surface, "الصورة")
        _require_text(self.why_chosen, "سببُ الاختيار")

    def as_canonical_content(self) -> dict[str, str]:
        return {"surface": self.surface, "why_chosen": self.why_chosen}


_SYLLABLE_FIELDS: Final[tuple[FieldDeclaration, ...]] = (
    FieldDeclaration(
        field="Carrier",
        read_from="`syllabifier.syllabify_surface(x).syllables`",
        statement="حاملُ الطبقة مقطعٌ واحدٌ بقالبه وشرائحه؛ وقيامُ الحامل أن "
        "تخرج للصورة سلسلةُ مقاطعَ غيرُ خالية",
        what_would_fail_it="صورةٌ تخرج بـ`syllables=()` — كصورةٍ فيها رمزٌ "
        "مُمرَّرٌ لا حاملَ له",
    ),
    FieldDeclaration(
        field="Gate",
        read_from="`SyllabifiedWord.is_resolved` فوق `template_of`",
        statement="بوّابةُ الطبقة عضويّةُ القوالب الستّة المغلقة: لا يمرّ شكلٌ "
        "سابعٌ ولا يُقرَّب إلى أقرب قالب",
        what_would_fail_it="صورةٌ يقف تقطيعُها عند شكلٍ خارج الستّة فتُسجَّل في "
        "`wazn_unresolved`",
    ),
    FieldDeclaration(
        field="Identity",
        read_from="مواضعُ الحروف في شرائح المقاطع مقابلَ مواضع قراءة المرماز",
        statement="حفظُ الهوية أن تكون مواضعُ الحروف التي دخلت التقطيعَ هي "
        "بعينها مواضعَ الحروف التي خرجت في الشرائح، بلا موضعٍ سقط ولا موضعٍ "
        "زِيد",
        what_would_fail_it="صورةٌ يخرج تقطيعُها بشريحةٍ تشير إلى موضعِ حرفٍ لم "
        "يقرأه المرماز، أو يسقط منها موضعُ حرفٍ صائتٍ قُرِئ",
    ),
    FieldDeclaration(
        field="Trace",
        read_from="`SyllabifiedWord.preregistration_digest`",
        statement="الأثرُ أن تحمل القراءةُ بصمةَ التجميد الذي جرت تحته، فتُعرَف "
        "على أيّ قواعدَ قُرِئت",
        what_would_fail_it="قراءةٌ تحمل بصمةً غيرَ بصمة `syllable_preregistration` "
        "القائمة — وهي مرفوضةٌ عند الإنشاء في الوحدة نفسها",
    ),
    FieldDeclaration(
        field="Residual",
        read_from="`SyllabifiedWord.wazn_unresolved`",
        statement="البقيةُ ما لم يُحسَب في هذا الورود بعينه: تعذّرٌ مُسمًّى "
        "بموضعه وسببه. وخلوُّ البقية أن يكون الحقلُ فارغًا",
        what_would_fail_it="صورةٌ تخرج بتعذّرٍ غيرِ مُسمًّى، أو بمقاطعَ وتعذّرٍ "
        "معًا — وكلاهما مرفوضٌ عند الإنشاء",
    ),
    FieldDeclaration(
        field="Closure",
        read_from="قوالبُ المقاطع الخارجة مقابلَ `SyllableTemplate` الستّة",
        statement="الإغلاقُ أن يكون قالبُ كلّ مقطعٍ خارجٍ عضوًا في المفردة "
        "الستّية المغلقة، بلا عضوٍ سابعٍ ولا خانةٍ عامّةٍ يُلقى فيها الشاذّ",
        what_would_fail_it="مقطعٌ واحدٌ يخرج بقالبٍ خارج المفردة الستّية",
    ),
)

_WORD_FIELDS: Final[tuple[FieldDeclaration, ...]] = (
    FieldDeclaration(
        field="Carrier",
        read_from="`word_structure_dictionary.analyze_word(x).letters`",
        statement="حاملُ الطبقة حرفٌ مقروءةٌ حالتُه على المرماز؛ وقيامُ الحامل "
        "أن تخرج للصورة سلسلةُ حروفٍ غيرُ خالية",
        what_would_fail_it="صورةٌ كلُّ وحداتها `PASSTHROUGH` فتخرج بـ`letters=()`",
    ),
    FieldDeclaration(
        field="Gate",
        read_from="`WordStructureDictionary.unread`",
        statement="بوّابةُ الطبقة عضويّةُ الحوامل المُعلَنة: ما وقع خارجها "
        "يُسمّى مُمرَّرًا ولا يُقرأ حرفًا. ومرورُ الصورة كلِّها أن يخلو "
        "`unread`",
        what_would_fail_it="صورةٌ فيها رمزٌ خارج الحوامل المُعلَنة فيُسجَّل في "
        "`unread` بموضعه",
    ),
    FieldDeclaration(
        field="Identity",
        read_from="`WordStructureDictionary.surface_round_trips`",
        statement="حفظُ الهوية أن تُعاد الصورةُ من قراءتها حرفًا بحرفٍ كما "
        "دخلت، فلا تُبتَلع علامةٌ ولا تُستحدَث",
        what_would_fail_it="صورةٌ لا تُعاد من قراءتها كما دخلت فيقرأ الحقلُ " "`False`",
    ),
    FieldDeclaration(
        field="Trace",
        read_from="`WordStructureDictionary.standing_of` لكلّ طبقةٍ مُعلَنة",
        statement="الأثرُ أن تحمل القراءةُ منزلةَ كلّ طبقةٍ مُعلَنةٍ فيها، "
        "فيُعرَف المقيسُ من المحجوب ولا يُسوّى التجميعُ بينهما",
        what_would_fail_it="قراءةٌ تحجب طبقةً مقيسةً أو تُطلق طبقةً محجوبة — "
        "وكلاهما مرفوضٌ عند الإنشاء في الوحدة نفسها",
    ),
    FieldDeclaration(
        field="Residual",
        read_from="`WordStructureDictionary.unread` بوصفه بقيةَ الورود",
        statement="البقيةُ ما لم يُقرأ في هذا الورود بعينه: رمزٌ مُسمًّى "
        "بموضعه. والطبقاتُ المحجوبةُ في `withheld` تأجيلٌ مُعلَنٌ للطبقة "
        "كلِّها لا بقيةُ وُرودٍ، فلا تدخل في هذا الحقل",
        what_would_fail_it="صورةٌ فيها رمزٌ خارج الحوامل يخرج بلا موضعٍ مُسمًّى "
        "في `unread`",
    ),
    FieldDeclaration(
        field="Closure",
        read_from="مواضعُ `letters` و`unread` مجتمعةً مقابلَ مواضع وحدات المرماز",
        statement="الإغلاقُ أن يكون كلُّ موضعٍ في الصورة إمّا حرفًا مقروءًا "
        "وإمّا مُمرَّرًا مُسمًّى، بلا موضعٍ يسقط بينهما ولا موضعٍ يُعَدّ مرّتين",
        what_would_fail_it="موضعٌ واحدٌ لا يظهر في `letters` ولا في `unread`، أو "
        "موضعٌ يظهر فيهما معًا",
    ),
)

_COMPOUND_FIELDS: Final[tuple[FieldDeclaration, ...]] = (
    FieldDeclaration(
        field="Carrier",
        read_from="مرحلةُ «العامل والمعمول» في `compound_layer_preregistration`",
        statement="حاملُ الطبقة مركّبٌ يقوم بين عاملٍ ومعمول؛ ولا وحدةَ في "
        "الشجرة تُخرِج هذا الحامل لصورةٍ بعينها",
        what_would_fail_it="وحدةٌ تُخرِج لصورةٍ مُعطاةٍ عاملَها ومعمولَها "
        "مُشتقَّين من نصّها لا مكتوبين بيدٍ",
    ),
    FieldDeclaration(
        field="Gate",
        read_from="`AttestationStanding` في `compound_layer_preregistration`",
        statement="بوّابةُ الطبقة شاهدٌ مُثبَتٌ بنصّه لكلّ فرع؛ وقيمةُ "
        "`شاهد_لكل_فرع` مُعلَنةٌ غيرُ قابلةٍ للبناء اليوم",
        what_would_fail_it="سلطةُ تحقُّقٍ تُثبِت إسنادَ فرعٍ إلى نصّه، فتصير "
        "القيمةُ الثالثةُ قابلةً للبناء",
    ),
    FieldDeclaration(
        field="Identity",
        read_from="مراحلُ `CompoundStage` الأربع",
        statement="حفظُ الهوية أن تبقى الكلماتُ الداخلةُ في المركّب هي بعينها "
        "بعد التركيب، فلا تُبتَلع كلمةٌ ولا تُستحدَث",
        what_would_fail_it="قراءةُ مركّبٍ تُسقِط كلمةً وردت في نصّه أو تزيد " "كلمةً ليست فيه",
    ),
    FieldDeclaration(
        field="Trace",
        read_from="`compound_layer_source_texts` مفاتيحَ نصوصٍ مُزوَّدة",
        statement="الأثرُ أن تحمل القراءةُ مفتاحَ النصّ المصدريّ الذي جرت عليه",
        what_would_fail_it="قراءةُ مركّبٍ بلا مفتاحِ نصٍّ مُزوَّد",
    ),
    FieldDeclaration(
        field="Residual",
        read_from="`COMPOUND_UNDECIDED_TEXT` وقيمُ عدم الانطباق",
        statement="البقيةُ ما لم تُحسَم مرحلتُه في هذا المركّب بعينه",
        what_would_fail_it="مركّبٌ يخرج بعدم انطباقٍ بلا موضعٍ ولا سببٍ مُسمّى",
    ),
    FieldDeclaration(
        field="Closure",
        read_from="مفرداتُ المخرجات المُسجَّلة لكلّ مرحلة",
        statement="الإغلاقُ أن يقع مخرجُ كلّ مرحلةٍ في مفردتها المُسجَّلة، بلا "
        "عضوٍ يُضاف بعد رؤية النصّ",
        what_would_fail_it="مخرجٌ يقع خارج مفردة مرحلته فيُوسَّع لها عضوٌ جديد",
    ),
)

_SENTENCE_FIELDS: Final[tuple[FieldDeclaration, ...]] = (
    FieldDeclaration(
        field="Carrier",
        read_from="`CardItem` في `sentence_card_preregistration`",
        statement="حاملُ الطبقة جملةٌ تامّةٌ يُقرأ منها بندُ بطاقتها؛ ولا وحدةَ "
        "في الشجرة تُخرِج هذا الحامل لصورةٍ بعينها",
        what_would_fail_it="وحدةٌ تُخرِج لجملةٍ مُعطاةٍ بنودَ بطاقتها مُشتقّةً " "من نصّها",
    ),
    FieldDeclaration(
        field="Gate",
        read_from="`ItemStanding` في `sentence_card_preregistration`",
        statement="بوّابةُ الطبقة شهادةٌ قائمةٌ يُشتَقّ منها البند؛ و"
        "`مصدرٌ_مُزوَّدٌ_بلا_شهادة` موقفٌ لا يفتح البوّابة",
        what_would_fail_it="شهادةٌ صوريّةٌ قائمةٌ يُشتَقّ منها بندٌ فيصير موقفُه "
        "`مُشتَقّ_من_شهادة_قائمة`",
    ),
    FieldDeclaration(
        field="Identity",
        read_from="بنودُ البطاقة مقابلَ نصّ الجملة المُزوَّد",
        statement="حفظُ الهوية أن تبقى تراكيبُ الجملة الداخلةُ هي بعينها في "
        "بطاقتها، فلا يسقط تركيبٌ ولا يُستحدَث",
        what_would_fail_it="بطاقةٌ تُسقِط تركيبًا ورد في جملتها",
    ),
    FieldDeclaration(
        field="Trace",
        read_from="`sentence_card_source_texts` مفاتيحَ نصوصٍ مُزوَّدة",
        statement="الأثرُ أن تحمل البطاقةُ مفتاحَ النصّ المصدريّ وموضعَه",
        what_would_fail_it="بندٌ بلا مفتاحِ نصٍّ ولا موضع",
    ),
    FieldDeclaration(
        field="Residual",
        read_from="بنودُ البطاقة الموقوفةُ بقانونٍ مُسمّى",
        statement="البقيةُ بندٌ لم يُقرأ في هذه الجملة بعينها، موقوفًا بقانونٍ "
        "مُسمًّى لا بصمت",
        what_would_fail_it="بندٌ يسقط من البطاقة بلا قانونٍ يُسمّي وقفه",
    ),
    FieldDeclaration(
        field="Closure",
        read_from="مفردةُ `ItemStanding` الرباعية المغلقة",
        statement="الإغلاقُ أن يقع موقفُ كلّ بندٍ في المفردة الرباعية، بلا "
        "عضوٍ اسمُه «مُنجَز»",
        what_would_fail_it="بندٌ يخرج بموقفٍ خارج المفردة الرباعية",
    ),
)

DECLARED_LAYERS: Final[tuple[LayerDeclaration, ...]] = (
    LayerDeclaration(
        jurisdiction="syllable-segmentation",
        ladder_name="مقطع",
        carrier_module="syllabifier.py",
        standing=LayerStanding.CODED_AND_MEASURABLE,
        why_this_standing="الوحدةُ تُخرِج لصورةٍ مُعطاةٍ قراءةً كاملةً لكلّ "
        "ورودٍ على حدة، فوق تجميدٍ مُبصَّمٍ سابقٍ عليها",
        fields=_SYLLABLE_FIELDS,
    ),
    LayerDeclaration(
        jurisdiction="word-structure-dictionary",
        ladder_name="كلمة",
        carrier_module="word_structure_dictionary.py",
        standing=LayerStanding.CODED_AND_MEASURABLE,
        why_this_standing="الوحدةُ تُخرِج لصورةٍ مُعطاةٍ قاموسَ كلمةٍ بحقوله "
        "المقيسة وحقول تعذّرها المُسمّاة",
        fields=_WORD_FIELDS,
    ),
    LayerDeclaration(
        jurisdiction="compound-layer",
        ladder_name="تركيب",
        carrier_module="compound_layer_preregistration.py",
        standing=LayerStanding.SOURCE_SUPPLIED_NO_CODED_CARRIER,
        why_this_standing="نصوصُ المرحلة الأولى مُزوَّدةٌ في "
        "`compound_layer_source_texts`، ولا وحدةَ تُخرِج من صورةٍ مُعطاةٍ "
        "حاملَ مركّبٍ لكلّ ورودٍ على حدة؛ و`certificate_is_constructible` "
        "قائمةٌ على `False`",
        fields=_COMPOUND_FIELDS,
    ),
    LayerDeclaration(
        jurisdiction="sentence-card",
        ladder_name="جملة",
        carrier_module="sentence_card_preregistration.py",
        standing=LayerStanding.SOURCE_SUPPLIED_NO_CODED_CARRIER,
        why_this_standing="نصوصٌ مُزوَّدةٌ في `sentence_card_source_texts` بلا "
        "شهادةٍ يُشتَقّ منها بند، ولا وحدةَ تُخرِج من جملةٍ مُعطاةٍ بطاقتَها",
        fields=_SENTENCE_FIELDS,
    ),
)

SCALE_TRANSPORT: Final[ScaleTransport] = ScaleTransport(
    transport_id="same-occurrence-field-transport",
    statement="`S_{n→m}` يأخذ توقيعَ الطبقة الأدنى على الصورة نفسها، وينقله "
    "حقلًا بحقلٍ إلى إطار الطبقة الأعلى: المنقولُ هو **محمولُ الحقل** "
    "(أقام الحاملُ؟ أمرّت البوّابة؟ أحُفِظت الهوية؟ أخلَت البقية؟ أحُفِظ "
    "الأثر؟ أأُغلِقت المفردة؟) لا قيمتُه العددية ولا شكلُه السطحيّ. "
    "فتوقّعُ البنية أن يقرأ الحقلُ في الطبقة الأعلى على الصورة نفسها ما "
    "قرأه في الأدنى",
    what_would_fail_it="صورةٌ واحدةٌ يقرأ فيها حقلٌ من الأربعة المُفنِّدة "
    "محمولًا في الطبقة الأدنى ونقيضَه في الأعلى",
)

MATCH_CRITERION: Final[MatchCriterion] = MatchCriterion(
    criterion_id="field-wise-transport-agreement",
    statement="`S∘K_n ≅ K_m∘S` بالنسبة إلى الحقول الستّة وحدها: يتحقّق تناظرُ "
    "حقلٍ إذا وافق محمولُه في الطبقة الأعلى منقولَه من الأدنى على **كلّ** "
    "صورةٍ من الصور المُجمَّدة. وصورةٌ واحدةٌ تخالف تُسقِط تناظرَ ذلك الحقل، "
    "ولا يُقرأ الباقي أغلبيّةً",
    compared_fields=COMPARED_FIELDS,
    refuting_fields=("Gate", "Identity", "Residual", "Closure"),
)

WEAKER_MODEL: Final[WeakerModel] = WeakerModel(
    model_id="constant-admission",
    statement="نموذجٌ غيرُ فركتاليٍّ يتنبّأ بمحمولٍ صادقٍ لكلّ حقلٍ في الطبقة "
    "الأعلى على كلّ صورة، بلا أن يقرأ الطبقةَ الأدنى ولا أن يفترض بنيةَ "
    "انتقالٍ واحدة",
    what_it_reads="لا شيء: لا حاملَ ولا بوّابةَ ولا صورةً؛ مخرجُه ثابتٌ قبل " "المدخل",
    how_it_could_lose="صورةٌ يقرأ فيها حقلٌ في الطبقة الأعلى محمولًا كاذبًا "
    "ويقرأ في الأدنى كاذبًا مثلَه: تُصيبها البنيةُ بالنقل ويُخطئها الثابت. "
    "ولذلك أُدخِلت في الصور المُجمَّدة صورٌ يُتوقَّع أن يُردّ بعضُ حقولها",
)

DECLARED_PAIRS: Final[tuple[PairDeclaration, ...]] = (
    PairDeclaration(
        pair_id="syllable-to-word",
        lower_jurisdiction="syllable-segmentation",
        upper_jurisdiction="word-structure-dictionary",
        pass_condition="تناظرُ الحقول الأربعة المُفنِّدة على كلّ صورةٍ مُجمَّدة، "
        "مع `Reconstruct_K > Reconstruct_W` بالعدّ الصريح للإصابات",
        fail_condition="اختلالُ تناظرِ واحدٍ من: البوّابة، أو حفظ الهوية، أو "
        "البقية، أو الإغلاق، على صورةٍ واحدةٍ فأكثر",
        underpowered_condition="ألّا تكون إحدى الولايتين مُرمَّزةً تُخرِج قراءةً "
        "لكلّ ورود، أو ألّا تبلغ أزواجُ المطابقة شرطَ النجاح المنصوص "
        "(طبقتان لم تُستخدما في الصياغة ثمّ إعادةٌ على ثالثة)",
        what_would_lift_underpowered="زوجُ ولايتين مُرمَّزتين لا يَرِد اسمُ أيٍّ "
        "منهما في نصّ الفرضية المُجمَّد، يُعلَن قبل تشغيله",
    ),
    PairDeclaration(
        pair_id="word-to-compound",
        lower_jurisdiction="word-structure-dictionary",
        upper_jurisdiction="compound-layer",
        pass_condition="كشرط الزوج الأوّل بعينه، ولا يُخفَّف له",
        fail_condition="كشرط الزوج الأوّل بعينه",
        underpowered_condition="طبقةُ المركّب لا تُخرِج حاملًا لكلّ ورود، "
        "فالقراءةُ ممتنعةٌ بالبناء لا مُتعذّرةٌ بالبيانات",
        what_would_lift_underpowered="وحدةٌ تُخرِج من صورةٍ مُعطاةٍ عاملَها "
        "ومعمولَها مُشتقَّين من نصٍّ مصدريٍّ مُسمًّى، لا مكتوبَين بيد",
    ),
    PairDeclaration(
        pair_id="compound-to-sentence",
        lower_jurisdiction="compound-layer",
        upper_jurisdiction="sentence-card",
        pass_condition="كشرط الزوج الأوّل بعينه، ولا يُخفَّف له",
        fail_condition="كشرط الزوج الأوّل بعينه",
        underpowered_condition="كلتا الطبقتين لا تُخرِج حاملًا لكلّ ورود",
        what_would_lift_underpowered="وحدتان تُخرِجان الحاملين من نصوصٍ "
        "مصدريّةٍ مُسمّاة، ثمّ إعلانُ الزوج قبل تشغيله",
    ),
)

FROZEN_CASES: Final[tuple[FrozenCase, ...]] = (
    FrozenCase(
        surface="كَتَبَ",
        why_chosen="ثلاثيٌّ مفتوحُ الحروف كلُّه، لا مدَّ فيه ولا شدّةَ ولا "
        "تنوين: أبسطُ صورةٍ يُتوقَّع أن تمرّ في الطبقتين",
    ),
    FrozenCase(
        surface="قَالَ",
        why_chosen="فيه مدٌّ بالألف، فيمتحن فرعَ التطويل في التوسيع وفرعَ "
        "المَقعد في المرماز",
    ),
    FrozenCase(
        surface="مُحَمَّدٌ",
        why_chosen="فيه شدّةٌ وتنوين، فيمتحن فرعَي التضعيف والتنوين في " "الطبقتين معًا",
    ),
    FrozenCase(
        surface="كَتَبَZ",
        why_chosen="فيه رمزٌ خارج الحوامل المُعلَنة مُلحَقٌ بكلمةٍ سليمة: "
        "أُدخِل ليُتاح للبوّابة والبقية أن تقرآ محمولًا كاذبًا، إذ لا يخسر "
        "النموذجُ الثابت إلّا حيث يُقرأ الكذب",
    ),
    FrozenCase(
        surface="كتب",
        why_chosen="بلا علاماتٍ البتّة: حالةٌ حدّيّةٌ يُتوقَّع أن تختلف فيها "
        "الطبقتان أو تتّفقا، ولا يُعرَف أيُّهما قبل التشغيل",
    ),
)

PREREGISTRATION_IS_NOT_A_READOUT_NOTE: Final[str] = (
    "PreregistrationIsNotAReadout: ليس في هذه الوحدة قراءةٌ ولا حكمٌ ولا حقلُ "
    "نتيجة؛ وهي تُجمّد المطلوبَ قبل دليله لا تُنجزه"
)

NO_PAIR_IS_HOLDOUT_UNDER_THE_FROZEN_LADDER_NOTE: Final[str] = (
    "NoPairIsHoldoutUnderTheFrozenLadder: السلّمُ المكتوبُ في نصّ الفرضية "
    "يُسمّي الطبقاتِ الأربعَ المُعلَنةَ هنا، فلا زوجَ منها «لم يُستخدم في "
    "الصياغة»؛ وعضويّةُ الاسم في النصّ مُشتَقّةٌ لا مكتوبة، و`SUPPORTED` لا "
    "تبلغ حتى يُعلَن زوجٌ خارج السلّم"
)

TRACE_IS_DECLARED_NON_DISCRIMINATING_NOTE: Final[str] = (
    "TraceIsDeclaredNonDiscriminating: حقلُ الأثر في الطبقتين المُرمَّزتين "
    "صادقٌ بالبناء، فلا يقرأ كذبًا على أيّ مدخلٍ ولا يُميّز بنيةً عن نموذجٍ "
    "ثابت؛ وهذا مُسجَّلٌ قبل التشغيل لا مُفسَّرٌ بعده"
)

A_CONSTRUCTIONAL_AGREEMENT_IS_NOT_EVIDENCE_NOTE: Final[str] = (
    "AConstructionalAgreementIsNotEvidence: اتّفاقُ حقلٍ لا يستطيع أن يقرأ "
    "كذبًا في طبقتيه اتّفاقٌ عن بناء الأداة لا عن بنية اللغة، ويُعَدّ في "
    "حساب النموذج الأضعف كما يُعَدّ له"
)

PREREGISTRATION_NAMED_RESIDUALS: Final[tuple[str, ...]] = (
    PREREGISTRATION_IS_NOT_A_READOUT_NOTE,
    NO_PAIR_IS_HOLDOUT_UNDER_THE_FROZEN_LADDER_NOTE,
    TRACE_IS_DECLARED_NON_DISCRIMINATING_NOTE,
    A_CONSTRUCTIONAL_AGREEMENT_IS_NOT_EVIDENCE_NOTE,
)


def layer_named(jurisdiction: str) -> LayerDeclaration:
    """إعلانُ ولايةٍ بعينها؛ وغيرُ المُعلَنة تُرَدّ ولا تُقرأ أقربَ ولاية."""

    for layer in DECLARED_LAYERS:
        if layer.jurisdiction == jurisdiction:
            return layer
    raise FractalTransitionPreregistrationError(
        f"الولاية «{jurisdiction}» غيرُ مُعلَنةٍ في التسجيل المسبق"
    )


def pair_named(pair_id: str) -> PairDeclaration:
    """زوجٌ مُعلَنٌ بعينه؛ وزوجٌ غيرُ مُعلَنٍ لا يُقرأ بعد التشغيل."""

    for pair in DECLARED_PAIRS:
        if pair.pair_id == pair_id:
            return pair
    raise FractalTransitionPreregistrationError(
        f"الزوج «{pair_id}» غيرُ مُعلَنٍ قبل التشغيل، فلا يُقرأ بعده"
    )


def preregistration_digest() -> str:
    """بصمةُ التسجيل كلِّه، مُشتقّةً عند النداء لا منقولةً من ثابتٍ مكتوب."""

    return canonical_digest(
        canonical_bytes(
            {
                "canonicalization_version": "fractal-transition-preregistration-v1",
                "hypothesis_digest": HYPOTHESIS_DIGEST,
                "layers": [layer.as_canonical_content() for layer in DECLARED_LAYERS],
                "scale_transport": SCALE_TRANSPORT.as_canonical_content(),
                "match_criterion": MATCH_CRITERION.as_canonical_content(),
                "weaker_model": WEAKER_MODEL.as_canonical_content(),
                "pairs": [pair.as_canonical_content() for pair in DECLARED_PAIRS],
                "cases": [case.as_canonical_content() for case in FROZEN_CASES],
                "named_residuals": list(PREREGISTRATION_NAMED_RESIDUALS),
            }
        )
    )


PREREGISTRATION_DIGEST: Final[str] = preregistration_digest()


def _refuse_a_registration_that_does_not_close() -> None:
    jurisdictions = [layer.jurisdiction for layer in DECLARED_LAYERS]
    if len(set(jurisdictions)) != len(jurisdictions):
        raise FractalTransitionPreregistrationError("ولايةٌ تكرّرت بمُعرِّفها")
    ladder_names = [layer.ladder_name for layer in DECLARED_LAYERS]
    if len(set(ladder_names)) != len(ladder_names):
        raise FractalTransitionPreregistrationError("اسمُ طبقةٍ تكرّر في السلّم")
    for pair in DECLARED_PAIRS:
        layer_named(pair.lower_jurisdiction)
        layer_named(pair.upper_jurisdiction)
    pair_ids = [pair.pair_id for pair in DECLARED_PAIRS]
    if len(set(pair_ids)) != len(pair_ids):
        raise FractalTransitionPreregistrationError("زوجٌ تكرّر بمُعرِّفه")
    surfaces = [case.surface for case in FROZEN_CASES]
    if len(set(surfaces)) != len(surfaces):
        raise FractalTransitionPreregistrationError("صورةٌ تكرّرت في الصور المُجمَّدة")
    if not FROZEN_CASES:
        raise FractalTransitionPreregistrationError(
            "تسجيلٌ بلا صورةٍ واحدةٍ مُجمَّدةٍ يترك الحالاتِ تُختار بعد النتيجة"
        )
    if len(PREREGISTRATION_DIGEST) != 64:
        raise FractalTransitionPreregistrationError("بصمةُ التسجيل سلسلةٌ ستّينيّةٌ رباعية")


def _refuse_a_result_field() -> None:
    forbidden = ("verdict", "result", "outcome", "supported", "refuted", "score")
    for declared in (
        FieldDeclaration,
        LayerDeclaration,
        PairDeclaration,
        FrozenCase,
        MatchCriterion,
        WeakerModel,
        ScaleTransport,
    ):
        for name in getattr(declared, "__annotations__", {}):
            if any(token in name.lower() for token in forbidden):
                raise FractalTransitionPreregistrationError(
                    f"حقلٌ اسمُه «{name}» يفتح للتسجيل بابَ حملِ نتيجةٍ؛ "
                    f"{PREREGISTRATION_IS_NOT_A_READOUT_NOTE}"
                )


_refuse_a_registration_that_does_not_close()
_refuse_a_result_field()
