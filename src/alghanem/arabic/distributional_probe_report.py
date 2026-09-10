"""تسجيل بنيوي لنتيجة سلبية: تحقيق توزيعي لم يُعِد اكتشاف اسم/فعل/حرف.

هذه الوحدة ليست شهادة رابعة. الشهادات الثلاث السابقة
(`word_class_formal.py`، و`lafz_madlul_relation_formal.py`،
و`madlul_alone_formal.py`) تُصنِّف شواهد مُثبَتة بنصّها بدالّة صورية كلّية،
وتنتهي إلى تطابق تامّ فتحمل عنوان النجاح. أمّا هذه الوحدة فتُسجِّل **نتيجة
قياس سلبية** بنفس انضباط تلك الشهادات: بمفردات مغلقة، وحقول مُلزَمة، ورَدٍّ
لكل حالة خارج المجال، حتى تصير النتيجة السلبية **مصنوعة بنيويًّا** لا فقرةً
في وصف طلب دمج تُنسى أو تُلطَّف لاحقًا.

ما جرى قياسه، بلا تجميل: على ٢١٩٣ شكلًا سطحيًّا (بشرط دعم ≥٥)، وبخمس سمات
توزيعية بحتة — الطول، ونسبة النهائية، وتنوّع الخَلَف، وتنوّع السلَف، وتنوّع
مضيف الهيكل الصامت — مُسِح k من ٢ إلى ١١ بمعيار `silhouette` وحده، فكان أفضل
k هو **٢ لا ٣**، وبتوزيع غير متوازن (٢١٥٩ مقابل ٣٤). ولم يُطابق التقسيم
الناتج تقسيم اللفظ المفرد إلى اسم وفعل وحرف.

والمكتشَف بدلًا من ذلك ظاهرتان بنيويتان تُسمَّيان هنا باسميهما لا بأقرب اسم
نحويّ إليهما:

* `فرط_اتصال` — العنقود الصغير (٣٤ عضوًا عند k=2، و٢٦ عند k=3): يضمّ حروفًا
  حقيقية بلا شكّ (في، من، على، لا، إلّا، إنّ، أن، ثمّ، إلى، أو) **مختلطةً**
  بكلمات محتوى فائقة التكرار (الله، الذين، ما، قال، كان). فسمته الفاصلة
  تكرارٌ هائل مع نسبة نهائية تقارب الصفر وتنوّع اتصال مرتفع جدًّا — أي
  فرط الاتصال، لا الحرفية بمعناها النحوي الدقيق.
* `فاصلة_قرآنية` — العنقود الثاني عند k=3 (٢٨٩ عضوًا): سمته الفاصلة نسبة
  نهائية مرتفعة (٠٫٥–١٫٠) مع تنوّع خَلَف يقارب الصفر، ويُفضِّل بنيويًّا
  مضارع الجمع بالواو والنون وصيغة `فعيل`. وهو أثر **أسلوبي إيقاعي**
  (السجع الختامي)، لا تصنيف نحويّ.

ولأن الخلط بين هاتين الطبقتين وبين التقسيم النحوي هو الخطأ الذي تحرسه هذه
الوحدة، فطبيعة كل طبقة حقلٌ مُلزَم مشتقّ من نوعها لا يُكتَب اعتباطًا: لا يجوز
لطبقة أن تُعلِن طبيعةً `نحوي`، لأن ذلك هو عين الادّعاء الذي لم يثبت.

وكذلك `الادّعاء_المنفي` حقلٌ مُلزَم على كل نتيجة سلبية، ومرفوض على نتيجة
`أعاد_اكتشاف_التقسيم` — بنفس نمط ملاحظة خروج الهذيان عن الوضع في الشهادة
الثالثة، وبنفس منطق `لا_ينطبق` في `comprehension_defect.py`: التصريح بعدم
الثبوت تصنيفٌ صادق، وإخفاؤه تزوير.

نطاق الوحدة وحدودها — تسجيل صريح، لا اعتذار لاحق:

* هذه الوحدة **تسجيل لنتيجة قياس، لا أنبوب قياس**: لا تقرأ مدوَّنة، ولا
  تحسب سمة، ولا تُشغِّل عنقدة، ولا تُعيد إنتاج الأرقام المسجَّلة فيها. أي
  ادّعاء بإعادة الإنتاج يحتاج أنبوبًا حتميًّا (مدوَّنة مُسمّاة بمصدرها،
  وبذرة مُجمَّدة، ومعيار توقّف مُعلَن) لم يُبنَ بعد، وإدخاله الآن ادّعاءُ
  نطاقٍ غير مبرهَن.
* ولا تُعلِن هذه الوحدة سمةً بديلة ولا تجربةً ثانية: اختيار سمات جديدة
  **بعد** رؤية العناقيد هو ما تمنعه بوّابة ما قبل الدليل في `kernel/`، فأي
  تجربة تالية تحتاج مواصفةً مُجمَّدة قبل دليلها.
* سلطويًّا: `ProbeOutcome != BirthVerdict`، و`DiscoveredCluster != BornOntology`.
  هذا توثيق وتسجيل فقط: لا نوع في `kernel/`، ولا `Freeze`، ولا `E0`، ولا
  بوّابة نواة تقرأ هذه المخرجات. لا تدخل نتيجة هذه الوحدة في
  `BirthExperimentSpecification`، ولا يقرأها `IndependentClosureGate` ولا
  `BirthVerdictGate`، ولا تغيّر نتيجة التدقيق الخارجي، ويبقى كل حقل فيه
  مطابقًا بايتيًّا.
* ولا عنوان نجاح في هذه الوحدة أصلًا: لا `SUCCESS_TITLE` ولا ما يقوم مقامه،
  لأن المسجَّل هنا نتيجة سلبية، وإلباسها عنوان الشهادات الثلاث تلبيسٌ لا
  تسجيل.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Final


class DistributionalProbeError(ValueError):
    """رُفض مدخلٌ خارج المجال المُجمَّد؛ لا يُحمَل على أقرب حالة."""


class ProbeFeature(Enum):
    """السمات التوزيعية الخمس المغلقة؛ لا سادسة لها في هذا التحقيق."""

    LENGTH = "الطول"
    FINAL_RATIO = "نسبة_النهائية"
    SUCCESSOR_DIVERSITY = "تنوّع_الخَلَف"
    PREDECESSOR_DIVERSITY = "تنوّع_السلَف"
    SILENT_SKELETON_HOST_DIVERSITY = "تنوّع_مضيف_الهيكل_الصامت"


class SelectionCriterion(Enum):
    """معيار اختيار k المغلق؛ المستعمَل فعلًا `silhouette` وحده."""

    SILHOUETTE = "silhouette"


class ProbeOutcome(Enum):
    """أحكام التحقيق المغلقة؛ لا رابع لها، ولا حكم صامت خارجها."""

    REDISCOVERED_DIVISION = "أعاد_اكتشاف_التقسيم"
    DISCOVERED_OTHER_LAYER = "اكتشف_طبقة_أخرى"
    NO_SEPARATION = "لم_يفصل"


class DiscoveredLayerKind(Enum):
    """أنواع الطبقات المكتشَفة المسمّاة بأعيانها، لا بأقرب اسم نحويّ إليها."""

    OVER_CONNECTIVITY = "فرط_اتصال"
    QURANIC_CADENCE = "فاصلة_قرآنية"


class LayerNature(Enum):
    """طبيعة الطبقة المغلقة؛ `نحوي` مُعلَنة لتُرفَض لا لتُستعمَل."""

    GRAMMATICAL = "نحوي"
    DISTRIBUTIONAL_FREQUENCY = "توزيعي_تكراري"
    STYLISTIC_RHYTHMIC = "أسلوبي_إيقاعي"


PROBE_NOT_APPLICABLE_TEXT: Final = "لا_ينطبق"

PROBE_SCOPE_NOTE: Final = (
    "هذه الوحدة تسجيل لنتيجة قياس لا أنبوب قياس: لا تقرأ مدوَّنة، ولا تحسب "
    "سمة، ولا تُشغِّل عنقدة، ولا تُعيد إنتاج أرقامها؛ وإعادة الإنتاج تحتاج "
    "أنبوبًا حتميًّا بمدوَّنة مُسمّاة وبذرة مُجمَّدة لم يُبنَ بعد"
)

PROBE_AUTHORITY_NOTE: Final = (
    "تسجيل وتوثيق فقط: لا يُنتج ولادةً ولا حكم ولادة، ولا يُجمَّد، ولا تقرأه "
    "أيّ بوّابة في النواة"
)

PROBE_PREREGISTRATION_NOTE: Final = (
    "أي تجربة تالية بسمات إضافية تحتاج مواصفةً مُجمَّدة قبل دليلها؛ فاختيار "
    "السمات بعد رؤية العناقيد هو عين ما تمنعه بوّابة ما قبل الدليل"
)

RECORDED_REFUTED_CLAIM: Final = (
    "السمات التوزيعية الخمس بصورتها الحالية لم تُعِد اكتشاف تقسيم اللفظ "
    "المفرد إلى اسم وفعل وحرف: أفضل k كان ٢ لا ٣، وبتوزيع غير متوازن، ولم "
    "يطابق أيّ عنقودٍ صنفًا من الأصناف الثلاثة"
)

_NATURE_BY_LAYER_KIND: Final[dict[DiscoveredLayerKind, LayerNature]] = {
    DiscoveredLayerKind.OVER_CONNECTIVITY: LayerNature.DISTRIBUTIONAL_FREQUENCY,
    DiscoveredLayerKind.QURANIC_CADENCE: LayerNature.STYLISTIC_RHYTHMIC,
}

_OUTCOMES_REQUIRING_REFUTED_CLAIM: Final = (
    ProbeOutcome.DISCOVERED_OTHER_LAYER,
    ProbeOutcome.NO_SEPARATION,
)

_OUTCOMES_REQUIRING_LAYERS: Final = (ProbeOutcome.DISCOVERED_OTHER_LAYER,)

if len(_NATURE_BY_LAYER_KIND) != len(DiscoveredLayerKind):  # pragma: no cover - guard
    raise RuntimeError("a declared layer kind derives no nature")
if LayerNature.GRAMMATICAL in set(
    _NATURE_BY_LAYER_KIND.values()
):  # pragma: no cover - guard
    raise RuntimeError("no discovered layer may be declared grammatical")


def _require_non_blank(value: str, field_name: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise DistributionalProbeError(f"{field_name} must be non-blank text")
    return value


def _require_positive(value: int, field_name: str) -> int:
    if not isinstance(value, int) or isinstance(value, bool) or value <= 0:
        raise DistributionalProbeError(f"{field_name} must be a positive integer")
    return value


@dataclass(frozen=True, slots=True)
class FrozenProbeSpecification:
    """مواصفة التحقيق المُجمَّدة: سماته، وشرط دعمه، وحجمه، ومدى k، ومعياره."""

    features: tuple[ProbeFeature, ...]
    minimum_support: int
    surface_form_count: int
    smallest_scanned_k: int
    largest_scanned_k: int
    selection_criterion: SelectionCriterion

    def __post_init__(self) -> None:
        if not isinstance(self.features, tuple) or not self.features:
            raise DistributionalProbeError("السمات تُعلَن مجموعةً غير فارغة")
        for feature in self.features:
            if not isinstance(feature, ProbeFeature):
                raise DistributionalProbeError(
                    "كل سمة must come from the closed vocabulary"
                )
        if len(set(self.features)) != len(self.features):
            raise DistributionalProbeError("تكرّرت سمة واحدة في المواصفة")
        if not isinstance(self.selection_criterion, SelectionCriterion):
            raise DistributionalProbeError(
                "معيار الاختيار must come from the closed vocabulary"
            )
        _require_positive(self.minimum_support, "شرط الدعم")
        _require_positive(self.surface_form_count, "عدد الأشكال السطحية")
        _require_positive(self.smallest_scanned_k, "أصغر k مفحوص")
        _require_positive(self.largest_scanned_k, "أكبر k مفحوص")
        if self.smallest_scanned_k < 2:
            raise DistributionalProbeError("مسح k يبدأ من ٢ فصاعدًا، فلا عنقدة بواحد")
        if self.largest_scanned_k <= self.smallest_scanned_k:
            raise DistributionalProbeError("أكبر k المفحوص يجب أن يتجاوز أصغره")
        if self.largest_scanned_k > self.surface_form_count:
            raise DistributionalProbeError("لا يُمسَح k أكبر من عدد الأشكال المعنقَدة")

    @property
    def feature_count(self) -> int:
        """عدد السمات المُعلَنة في المواصفة."""

        return len(self.features)

    @property
    def scanned_k_values(self) -> tuple[int, ...]:
        """قيم k المفحوصة كاملةً، من أصغرها إلى أكبرها بلا ثغرة."""

        return tuple(range(self.smallest_scanned_k, self.largest_scanned_k + 1))


@dataclass(frozen=True, slots=True)
class ProbePartition:
    """تقسيمٌ واحد عند k بعينه: أحجام عناقيده كما خرجت، لا كما تُشتهى."""

    k: int
    cluster_sizes: tuple[int, ...]

    def __post_init__(self) -> None:
        _require_positive(self.k, "k")
        if self.k < 2:
            raise DistributionalProbeError("لا تقسيم عند k أصغر من ٢")
        if not isinstance(self.cluster_sizes, tuple):
            raise DistributionalProbeError("أحجام العناقيد تُعلَن مجموعةً مرتَّبة")
        if len(self.cluster_sizes) != self.k:
            raise DistributionalProbeError("عدد أحجام العناقيد يخالف k المُعلَن")
        for size in self.cluster_sizes:
            _require_positive(size, "حجم العنقود")

    @property
    def member_total(self) -> int:
        """مجموع أعضاء العناقيد كلها في هذا التقسيم."""

        return sum(self.cluster_sizes)


@dataclass(frozen=True, slots=True)
class DiscoveredLayer:
    """طبقة مكتشَفة مسمّاة: نوعها، وطبيعتها، وحجمها، وسمتها الفاصلة، وشواهدها."""

    kind: DiscoveredLayerKind
    nature: LayerNature
    at_k: int
    member_count: int
    distinguishing_feature: str
    member_examples: tuple[str, ...]

    def __post_init__(self) -> None:
        if not isinstance(self.kind, DiscoveredLayerKind):
            raise DistributionalProbeError(
                "نوع الطبقة must come from the closed vocabulary"
            )
        if not isinstance(self.nature, LayerNature):
            raise DistributionalProbeError(
                "طبيعة الطبقة must come from the closed vocabulary"
            )
        if self.nature is not _NATURE_BY_LAYER_KIND[self.kind]:
            raise DistributionalProbeError(
                "طبيعة الطبقة تُشتَقّ من نوعها ولا تُكتَب اعتباطًا؛ ولا طبقة "
                "مكتشَفة تُعلَن نحويّة"
            )
        _require_positive(self.at_k, "k الطبقة")
        _require_positive(self.member_count, "عدد أعضاء الطبقة")
        _require_non_blank(self.distinguishing_feature, "السمة الفاصلة")
        if not isinstance(self.member_examples, tuple) or not self.member_examples:
            raise DistributionalProbeError("شواهد الطبقة تُعلَن مجموعةً غير فارغة")
        for example in self.member_examples:
            _require_non_blank(example, "شاهد العضوية")
        if len(set(self.member_examples)) != len(self.member_examples):
            raise DistributionalProbeError("تكرّر شاهد عضوية واحد بنصّه")
        if len(self.member_examples) > self.member_count:
            raise DistributionalProbeError(
                "شواهد الطبقة أكثر من أعضائها، فالشواهد عيّنة منهم لا زيادة عليهم"
            )

    @property
    def layer_key(self) -> tuple[DiscoveredLayerKind, int]:
        """هوية الطبقة: نوعها مع k الذي ظهرت عنده، لا نوعها وحده."""

        return (self.kind, self.at_k)


@dataclass(frozen=True, slots=True)
class DistributionalProbeReport:
    """تقرير التحقيق: مواصفته، وتقاسيمه، وحكمه، وطبقاته، وادّعاؤه المنفيّ."""

    specification: FrozenProbeSpecification
    selected_k: int
    partitions: tuple[ProbePartition, ...]
    outcome: ProbeOutcome
    discovered_layers: tuple[DiscoveredLayer, ...]
    refuted_claim: str

    def __post_init__(self) -> None:
        if not isinstance(self.specification, FrozenProbeSpecification):
            raise DistributionalProbeError("التقرير يلزمه مواصفة تحقيق مُجمَّدة")
        if not isinstance(self.outcome, ProbeOutcome):
            raise DistributionalProbeError("الحكم must come from the closed vocabulary")
        if not isinstance(self.partitions, tuple) or not self.partitions:
            raise DistributionalProbeError("التقاسيم تُعلَن مجموعةً غير فارغة")
        scanned = set(self.specification.scanned_k_values)
        declared_k: set[int] = set()
        for partition in self.partitions:
            if not isinstance(partition, ProbePartition):
                raise DistributionalProbeError("التقاسيم تُعلَن تقاسيمَ مبنيّة")
            if partition.k not in scanned:
                raise DistributionalProbeError("تقسيمٌ عند k خارج المدى المفحوص")
            if partition.k in declared_k:
                raise DistributionalProbeError("تقسيمان مُعلَنان عند k واحد")
            declared_k.add(partition.k)
            if partition.member_total != self.specification.surface_form_count:
                raise DistributionalProbeError(
                    "مجموع أحجام العناقيد يخالف عدد الأشكال المُعلَن في المواصفة"
                )
        if self.selected_k not in declared_k:
            raise DistributionalProbeError("k المختار بلا تقسيم مُعلَن يقابله")
        if not isinstance(self.discovered_layers, tuple):
            raise DistributionalProbeError("الطبقات تُعلَن مجموعةً مرتَّبة")
        layer_keys: set[tuple[DiscoveredLayerKind, int]] = set()
        sizes_by_k = {
            partition.k: partition.cluster_sizes for partition in self.partitions
        }
        for layer in self.discovered_layers:
            if not isinstance(layer, DiscoveredLayer):
                raise DistributionalProbeError("الطبقات تُعلَن طبقاتٍ مبنيّة")
            if layer.layer_key in layer_keys:
                raise DistributionalProbeError("طبقتان بنوع واحد عند k واحد")
            layer_keys.add(layer.layer_key)
            if layer.at_k not in sizes_by_k:
                raise DistributionalProbeError("طبقةٌ عند k بلا تقسيم مُعلَن يقابله")
            if layer.member_count not in sizes_by_k[layer.at_k]:
                raise DistributionalProbeError(
                    "حجم الطبقة ليس حجم عنقودٍ في تقسيم k الذي ظهرت عنده"
                )
        _require_non_blank(self.refuted_claim, "الادّعاء المنفي")
        declared_refutation = self.refuted_claim.strip() != PROBE_NOT_APPLICABLE_TEXT
        if self.outcome in _OUTCOMES_REQUIRING_REFUTED_CLAIM:
            if not declared_refutation:
                raise DistributionalProbeError(
                    "النتيجة السلبية يلزمها تصريحٌ بالادّعاء الذي لم يثبت"
                )
        elif declared_refutation:
            raise DistributionalProbeError(
                f"الادّعاء المنفي يُصرَّح على النتيجة السلبية وحدها، وعلى ما "
                f"عداها يكون {PROBE_NOT_APPLICABLE_TEXT}"
            )
        if self.outcome in _OUTCOMES_REQUIRING_LAYERS:
            if not self.discovered_layers:
                raise DistributionalProbeError(
                    "حكم اكتشاف طبقة أخرى يلزمه طبقةٌ مكتشَفة مسمّاة واحدة فأكثر"
                )
        elif self.discovered_layers:
            raise DistributionalProbeError(
                "لا تُعلَن طبقة مكتشَفة إلا مع حكم اكتشاف طبقة أخرى"
            )

    @property
    def is_negative_result(self) -> bool:
        """هل هذا تسجيلُ نتيجةٍ سلبية؟ نعم في كل حكم سوى إعادة الاكتشاف."""

        return self.outcome is not ProbeOutcome.REDISCOVERED_DIVISION

    @property
    def selected_partition(self) -> ProbePartition:
        """التقسيم عند k المختار بعينه، لا أوّل تقسيم مُعلَن."""

        (found,) = (
            partition for partition in self.partitions if partition.k == self.selected_k
        )
        return found

    @property
    def layers_by_kind(self) -> tuple[tuple[DiscoveredLayerKind, int], ...]:
        """هويات الطبقات المُعلَنة بترتيب إعلانها، بلا دمج ولا اختصار."""

        return tuple(layer.layer_key for layer in self.discovered_layers)


RECORDED_PROBE_SPECIFICATION: Final = FrozenProbeSpecification(
    features=(
        ProbeFeature.LENGTH,
        ProbeFeature.FINAL_RATIO,
        ProbeFeature.SUCCESSOR_DIVERSITY,
        ProbeFeature.PREDECESSOR_DIVERSITY,
        ProbeFeature.SILENT_SKELETON_HOST_DIVERSITY,
    ),
    minimum_support=5,
    surface_form_count=2193,
    smallest_scanned_k=2,
    largest_scanned_k=11,
    selection_criterion=SelectionCriterion.SILHOUETTE,
)

RECORDED_PROBE_REPORT: Final = DistributionalProbeReport(
    specification=RECORDED_PROBE_SPECIFICATION,
    selected_k=2,
    partitions=(
        ProbePartition(k=2, cluster_sizes=(2159, 34)),
        ProbePartition(k=3, cluster_sizes=(1878, 289, 26)),
    ),
    outcome=ProbeOutcome.DISCOVERED_OTHER_LAYER,
    discovered_layers=(
        DiscoveredLayer(
            kind=DiscoveredLayerKind.OVER_CONNECTIVITY,
            nature=LayerNature.DISTRIBUTIONAL_FREQUENCY,
            at_k=2,
            member_count=34,
            distinguishing_feature=(
                "تكرار هائل مع نسبة نهائية تقارب الصفر وتنوّع اتصال مرتفع جدًّا؛ "
                "فيُخلَط الحرف الحقيقي بكلمة المحتوى فائقة التكرار"
            ),
            member_examples=(
                "في",
                "من",
                "على",
                "لا",
                "إلّا",
                "إنّ",
                "أن",
                "ثمّ",
                "إلى",
                "أو",
                "الله",
                "الذين",
                "ما",
                "قال",
                "كان",
            ),
        ),
        DiscoveredLayer(
            kind=DiscoveredLayerKind.OVER_CONNECTIVITY,
            nature=LayerNature.DISTRIBUTIONAL_FREQUENCY,
            at_k=3,
            member_count=26,
            distinguishing_feature=(
                "الطبقة نفسها تظهر عند k=3 بعدد أقلّ، فثباتها عبر k دليل على "
                "أنها طبقة تكرار واتصال لا صنف نحويّ"
            ),
            member_examples=("في", "من", "على", "الله", "الذين"),
        ),
        DiscoveredLayer(
            kind=DiscoveredLayerKind.QURANIC_CADENCE,
            nature=LayerNature.STYLISTIC_RHYTHMIC,
            at_k=3,
            member_count=289,
            distinguishing_feature=(
                "نسبة نهائية مرتفعة جدًّا (٠٫٥–١٫٠) مع تنوّع خَلَف منخفض جدًّا "
                "يقارب الصفر؛ أثرٌ أسلوبي إيقاعي هو السجع الختامي، يُفضِّل "
                "بنيويًّا مضارع الجمع بالواو والنون وصيغة فعيل"
            ),
            member_examples=(
                "يُؤْمِنُونَ",
                "تَعْمَلُونَ",
                "يَعْلَمُونَ",
                "عَلِيمٌ",
                "رَّحِيمٌ",
                "الظَّالِمِينَ",
                "عَظِيمٌ",
            ),
        ),
    ),
    refuted_claim=RECORDED_REFUTED_CLAIM,
)

if not RECORDED_PROBE_REPORT.is_negative_result:  # pragma: no cover - guard
    raise RuntimeError("the recorded probe result is a negative one")
