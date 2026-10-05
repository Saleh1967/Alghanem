"""الطبقاتُ الثلاث المستقلّة، مُشتَقّةً من جنس القطعة لا مكتوبةً عليها.

ثلاثُ طبقاتٍ لا واحدة، وخلطُها هو الخطأ المتكرّر تاريخيًّا لا خطأً عارضًا:

* **الوجود الفيزيائيّ** (الصوت نفسه): فيزياءٌ تُدرَك بالحسّ المباشر، حالتُها
  يقينٌ متواتر، ومصدرُها **خارج هذا الأنبوب بالكلّية**. بيانات هذا المستودع
  نقاطُ ترميز Unicode، لا صوتٌ مُسجَّل، فلا قطعةَ هنا تقيسها.
* **العقدةُ الوضعيّة** (الحرف بوصفه اصطلاحًا كتابيًّا): اصطلاحٌ جمعيٌّ مستقرّ،
  حالتُه وضعيّةٌ تواتريّة، وهي **نقطةُ الدخول الفعليّة** لـ
  `RawSurfaceObservation` و`SurfaceNormalization`.
* **تحليلُ الصفات الإحصائيّ**: استدلالٌ من عيّنة، ظنّيٌّ دومًا مهما علت رتبته،
  وهو وحده ما تملكه هذه الطبقة العربية فعلًا (نتاجُ
  `distributional_probe_report`).

الشكلُ المُتَّبَع هنا مأخوذٌ من `encoding/provenance_genus.py` بعينه، لا مُبتكَرًا:

    DeclaredLayerLabel != DerivedOntologicalLayer

فلا حقلَ في أيّ صنفٍ هنا يكتب فيه حاملُ القطعة طبقتَها؛ الطبقةُ تُشتَقّ من نوع
القطعة نفسها، فالتسميةُ الكاذبة ليست مرفوضةً بعد وقوعها بل **غيرُ قابلةٍ
للقول**. والبوّابة هي المُصدِر الوحيد لتصنيفٍ أصلًا.

**الطبقةُ الفيزيائية مُعلَنةٌ وغيرُ قابلةٍ للبناء من أيّ قطعةٍ في هذا المستودع**،
بالانضباط نفسه الذي مُنع به `شاهد_لكل_فرع` و`CLOSED_BY_FROZEN_EXPERIMENT`: لا
قطعةَ هنا صوتٌ مُسجَّل، وإصدارُ تصنيفٍ فيزيائيّ ادّعاءُ قياسٍ لم يجرِ
(`UnicodeIsNotRecordedSound`). وإسقاطُها من المفردة أسوأ من إعلانها ممتنعة: فإنّ
حذفها يُوهم أنّ الطبقتين الباقيتين كلُّ ما هنالك، وهو بعينه الخلطُ المُتَّقى.

**الربطُ بين الطبقة (ج) والطبقة (أ) استدلالٌ مستورَد لا نتاجُ الأنبوب**
(`CrossLayerInferenceIsImported`): تجمُّعٌ إحصائيّ في تحليل الصفات لا يعكس
تجانسًا في الفيزياء إلا بدليلٍ مستقلٍّ يربط الطبقتين، فكلُّ ربطٍ هنا يلزمه
استشهادٌ خارجيٌّ مُصرَّح به، ويُسجَّل `مُصرَّح_غير_مُتحقَّق` على منوال
`ForeignFrozenExport != LocalFreeze`؛ لا سلطةَ هنا ترفعه عن ذلك، ولا يدخل أيّ
بنيةٍ في `kernel/`.

**خمولٌ سلطويّ**: `OntologicalLayerClassification != BirthVerdict` و
`CrossLayerInferenceRecord != AssessedEvidence`؛ لا ولادةَ ولا تجميدَ ولا `E0`،
ولا تقرأ هذه الوحدةَ أيّ بوّابةٍ في `kernel/`، وهو ما يفحصه اختبارٌ يمسح كلّ
وحداتها. وحقولُ التدقيق الخارجيّ تبقى متطابقةً بايتًا بعد هذه المرحلة.
"""

from __future__ import annotations

from dataclasses import dataclass, field, fields
from enum import Enum
from typing import Final

from .distributional_probe_report import DiscoveredLayer, DistributionalProbeReport
from .encoding.normalization import NormalizationAudit
from .encoding.observation import RawSurfaceObservation

_GATE_TOKEN = object()

_FORBIDDEN_LAYER_FIELD_MARKERS: Final = (
    "declared_layer",
    "verdict",
    "birth",
    "rank",
    "certified",
    "promotion",
)


class EpistemicLayerError(ValueError):
    """طبقةٌ مرفوضة؛ لا تُحمَل القطعة على أقرب طبقةٍ مقبولة."""


class OntologicalLayer(Enum):
    """الطبقات الثلاث، مفردةً مغلقة؛ والثالثةُ ليست أعلى الأولى بل غيرُها."""

    PHYSICAL_EXISTENCE = "وجود_فيزيائي"
    CONVENTIONAL_KNOT = "عقدة_وضعية"
    STATISTICAL_ATTRIBUTE_ANALYSIS = "تحليل_صفات_إحصائي"


class EpistemicStanding(Enum):
    """حالةُ كلّ طبقةٍ معرفيًّا، مُشتَقّةً من الطبقة لا مكتوبةً معها."""

    CERTAIN_BY_RECURRENT_TRANSMISSION = "يقين_متواتر"
    CONVENTIONAL_TRANSMITTED = "وضعي_تواتري"
    PRESUMPTIVE_ALWAYS = "ظنّي_دومًا"


class ImportedInferenceStanding(Enum):
    """موقفُ الاستشهاد الخارجيّ: مُصرَّحٌ به، ولا ثانيَ له يُبنى هنا.

    القيمةُ الثانية `مُتحقَّق_محليًّا` مُعلَنةٌ وغيرُ قابلةٍ للبناء، إذ لا سلطةَ
    هنا تتحقّق من دليلٍ خارج اللغة أصلًا؛ وإسقاطُها يُوهم أنّ الأولى هي كلُّ
    الممكن، وإتاحتُها ادّعاءُ فحصٍ لم يجرِ.
    """

    DECLARED_NOT_VERIFIED = "مُصرَّح_غير_مُتحقَّق"
    VERIFIED_LOCALLY = "مُتحقَّق_محليًّا"


if len(OntologicalLayer) != 3:  # pragma: no cover - guard
    raise RuntimeError("the ontological layers are deliberately three")
if len(EpistemicStanding) != 3:  # pragma: no cover - guard
    raise RuntimeError("each declared layer carries exactly one epistemic standing")
if len(ImportedInferenceStanding) != 2:  # pragma: no cover - guard
    raise RuntimeError("imported inference standing is deliberately two-valued")


UNICODE_IS_NOT_RECORDED_SOUND_NOTE: Final = (
    "UnicodeIsNotRecordedSound: لا قطعةَ في هذا المستودع صوتٌ مُسجَّل، فبياناتُه "
    "نقاطُ ترميزٍ لا مادّةٌ صوتيّة؛ وإصدارُ تصنيفٍ في الطبقة الفيزيائية من قطعةٍ "
    "هنا ادّعاءُ قياسٍ لم يجرِ، لا تقريبٌ مقبول"
)

CROSS_LAYER_INFERENCE_IS_IMPORTED_NOTE: Final = (
    "CrossLayerInferenceIsImported: ربطُ نتيجةٍ إحصائية بتفسيرٍ فيزيائيّ-صوتيّ "
    "استدلالٌ مستورَد من خارج الأنبوب، لا نتاجٌ له؛ فيلزمه استشهادٌ خارجيٌّ "
    "مُصرَّح به، ويبقى مُصرَّحًا غيرَ مُتحقَّق"
)

LAYER_CONFUSION_IS_THE_RECURRING_ERROR_NOTE: Final = (
    "افتراضُ أنّ تجمّعًا في تحليل الصفات يعكس تجانسًا في الوجود الفيزيائيّ دون "
    "دليلٍ مستقلٍّ يربط الطبقتين هو الخطأ المتكرّر تاريخيًّا؛ وهو خطأُ خلطِ "
    "طبقاتٍ لا خطأُ قياسٍ يُصلَح بتشديد الإحصاء"
)

EPISTEMIC_LAYERS_AUTHORITY_NOTE: Final = (
    "تصنيفٌ فقط: لا تُصدر هذه الوحدة ولادةً ولا حكمًا ولا تجميدًا ولا `E0`، ولا "
    "تقرؤها أيّ بوّابةٍ في النواة"
)


_STANDING_BY_LAYER: Final[dict[OntologicalLayer, EpistemicStanding]] = {
    OntologicalLayer.PHYSICAL_EXISTENCE: (
        EpistemicStanding.CERTAIN_BY_RECURRENT_TRANSMISSION
    ),
    OntologicalLayer.CONVENTIONAL_KNOT: EpistemicStanding.CONVENTIONAL_TRANSMITTED,
    OntologicalLayer.STATISTICAL_ATTRIBUTE_ANALYSIS: (
        EpistemicStanding.PRESUMPTIVE_ALWAYS
    ),
}

if set(_STANDING_BY_LAYER) != set(OntologicalLayer):  # pragma: no cover - guard
    raise RuntimeError("every declared layer must declare its epistemic standing")
if len(set(_STANDING_BY_LAYER.values())) != len(
    EpistemicStanding
):  # pragma: no cover - guard
    raise RuntimeError("two layers must not share one epistemic standing")


def _require_non_blank(value: str, field_name: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise EpistemicLayerError(f"{field_name} نصٌّ غير فارغ")
    return value


@dataclass(frozen=True, slots=True)
class OntologicalLayerClassification:
    """طبقةُ قطعةٍ واحدة، مُشتَقّةً من نوعها ومُصدَرةً من البوّابة وحدها."""

    layer: OntologicalLayer
    artifact_kind: str
    _token: object | None = field(default=None, repr=False, compare=False)

    def __post_init__(self) -> None:
        if self._token is not _GATE_TOKEN:
            raise EpistemicLayerError(
                "التصنيفُ لا يُنشَأ إلا من `OntologicalLayerGate`؛ والكتابةُ "
                "المباشرة إعلانُ طبقةٍ لا اشتقاقُها"
            )
        if not isinstance(self.layer, OntologicalLayer):
            raise EpistemicLayerError("الطبقةُ من مفردتها المغلقة")
        if self.layer is OntologicalLayer.PHYSICAL_EXISTENCE:
            raise EpistemicLayerError(UNICODE_IS_NOT_RECORDED_SOUND_NOTE)
        _require_non_blank(self.artifact_kind, "جنس القطعة")

    @property
    def standing(self) -> EpistemicStanding:
        """الحالةُ المعرفيّة، مُشتَقّةً من الطبقة لا مكتوبةً بجانبها."""

        return _STANDING_BY_LAYER[self.layer]

    @property
    def is_measured_by_this_pipeline(self) -> bool:
        """أقاسَ هذا الأنبوبُ الطبقةَ الفيزيائية؟ `False` بنيويًّا لا اختيارًا."""

        return self.layer is not OntologicalLayer.PHYSICAL_EXISTENCE


class OntologicalLayerGate:
    """المُصدِر الوحيد لتصنيفِ طبقة، مُشتقًّا من نوع القطعة وحده."""

    @staticmethod
    def classify(
        artifact: RawSurfaceObservation
        | NormalizationAudit
        | DistributionalProbeReport
        | DiscoveredLayer,
    ) -> OntologicalLayerClassification:
        """اشتقّ طبقةَ القطعة من نوعها؛ ولا يُقبَل من حاملها وسمٌ ولا تفضيل."""

        if isinstance(artifact, RawSurfaceObservation | NormalizationAudit):
            return OntologicalLayerClassification(
                layer=OntologicalLayer.CONVENTIONAL_KNOT,
                artifact_kind=type(artifact).__name__,
                _token=_GATE_TOKEN,
            )
        if isinstance(artifact, DistributionalProbeReport | DiscoveredLayer):
            return OntologicalLayerClassification(
                layer=OntologicalLayer.STATISTICAL_ATTRIBUTE_ANALYSIS,
                artifact_kind=type(artifact).__name__,
                _token=_GATE_TOKEN,
            )
        raise EpistemicLayerError(
            "قطعةٌ من جنسٍ لا تعرفه هذه البوّابة تُرفَض باسم نوعها ولا تُحمَل "
            f"على أقرب طبقة: {type(artifact).__name__}"
        )


@dataclass(frozen=True, slots=True)
class CrossLayerInferenceRecord:
    """ربطٌ مُعلَنٌ بين طبقتين، بمصدرٍ خارجيٍّ مُسمّى وموقفٍ لا يُرفَع هنا."""

    inference_id: str
    from_layer: OntologicalLayer
    to_layer: OntologicalLayer
    external_citation: str
    standing: ImportedInferenceStanding = (
        ImportedInferenceStanding.DECLARED_NOT_VERIFIED
    )

    def __post_init__(self) -> None:
        _require_non_blank(self.inference_id, "معرّف الاستدلال")
        _require_non_blank(self.external_citation, "الاستشهاد الخارجيّ")
        for value, name in (
            (self.from_layer, "الطبقة المصدر"),
            (self.to_layer, "الطبقة الهدف"),
        ):
            if not isinstance(value, OntologicalLayer):
                raise EpistemicLayerError(f"{name} من مفردتها المغلقة")
        if self.from_layer is self.to_layer:
            raise EpistemicLayerError(
                "ربطُ الطبقة بنفسها ليس عبورَ طبقتين؛ وتسجيلُه هنا يُخفي أنّ لا "
                "عبورَ وقع أصلًا"
            )
        if not isinstance(self.standing, ImportedInferenceStanding):
            raise EpistemicLayerError("موقفُ الاستدلال من مفردته المغلقة")
        if self.standing is ImportedInferenceStanding.VERIFIED_LOCALLY:
            raise EpistemicLayerError(
                "التحقّقُ المحلّيّ مُعلَنٌ وغيرُ قابلٍ للبناء: لا سلطةَ هنا تفحص "
                f"دليلًا خارج اللغة. {CROSS_LAYER_INFERENCE_IS_IMPORTED_NOTE}"
            )

    @property
    def crosses_into_the_physical_layer(self) -> bool:
        """أيعبُر هذا الاستدلالُ إلى الطبقة الفيزيائية؟ مُشتَقٌّ لا مكتوب."""

        return OntologicalLayer.PHYSICAL_EXISTENCE in (self.from_layer, self.to_layer)

    @property
    def is_produced_by_this_pipeline(self) -> bool:
        """`False` بنيويًّا: الاستدلالُ عبرَ الطبقات مستورَدٌ لا نتاجُ أنبوب."""

        return False


def _assert_no_fields_matching(
    declaring_type: type, markers: tuple[str, ...], message: str
) -> None:
    for item in fields(declaring_type):
        if any(marker in item.name for marker in markers):
            raise RuntimeError(message)


for _declaring_type in (OntologicalLayerClassification, CrossLayerInferenceRecord):
    _assert_no_fields_matching(
        _declaring_type,
        _FORBIDDEN_LAYER_FIELD_MARKERS,
        "no type here may carry a written layer label, verdict, birth, or rank field",
    )


__all__ = [
    "CROSS_LAYER_INFERENCE_IS_IMPORTED_NOTE",
    "EPISTEMIC_LAYERS_AUTHORITY_NOTE",
    "LAYER_CONFUSION_IS_THE_RECURRING_ERROR_NOTE",
    "UNICODE_IS_NOT_RECORDED_SOUND_NOTE",
    "CrossLayerInferenceRecord",
    "EpistemicLayerError",
    "EpistemicStanding",
    "ImportedInferenceStanding",
    "OntologicalLayer",
    "OntologicalLayerClassification",
    "OntologicalLayerGate",
]
