"""تجميد مواصفة التحقيق القادم قبل دليله، وتسجيل سؤال الطور الثاني مفتوحًا.

`distributional_probe_report.py` سجّل نتيجةً **ماضية** بمواصفتها، وأعلن نثرًا أن
أي تجربة تالية تحتاج مواصفةً مُجمَّدة قبل دليلها. والفارق الذي تُغلقه هذه الوحدة
هو بالضبط الفارق بين النثر والبنية:

    FrozenProbeSpecification (تجربة ماضية مسجَّلة)
        != EnforcedPreEvidenceSpecification (تجربة قادمة مُلزِمة)

فالمواصفة المسجَّلة هناك تصف ما جرى، ولا تمنع أحدًا من كتابة سماته **بعد** رؤية
عناقيده. أما هنا فلا يمكن بناء نتيجةٍ أصلًا إلا مربوطةً بمواصفةٍ سبقتها زمنيًّا
(بتجميدها في سجلّ) ومحتوًى (ببصمة مُعاد حسابها تطابق المُجمَّد). فمن غيّر حرفًا
واحدًا في المواصفة بعد التجميد، أو أدخل سمةً خارج المُجمَّد، أو بدّل معيار الحسم
أو قاعدة التوقّف — فشل عنده **الإنشاء**، لا صدر عنه تحذير يُقرأ أو يُهمَل.

`ما تمنعه هذه الوحدة بنيويًّا:`

* مواصفةٌ تحمل نتيجةً: `FrozenFollowupProbeSpecification` لا حقل نتيجة فيه
  البتّة، وحارسٌ عند الاستيراد يمنع تسلّل حقلٍ كهذا لاحقًا.
* نتيجةٌ بلا مواصفة سابقة: `ProbeResultAttachment` يلزمه ربطُ محتوًى مُتحقَّق منه.
* انزياح المواصفة بعد التجميد: البصمة تُعاد حسابها من المواصفة الحيّة وتُقارَن
  بايتيًّا بالمُجمَّدة.
* اختيار السمات بعد رؤية العناقيد: سمات النتيجة يجب أن تكون جزءًا من السمات
  المُجمَّدة، لا زيادةً عليها.

`جنس الدليل` مفردةٌ ثنائية عمدًا: `توزيعي` و`صرفي_وظيفي`، ولا ثالث `مختلط`.
فالجمع بين جنسين ليس قيمةً في مفردة، بل تركيبٌ صريح `(دليل_توزيعي، دليل_صرفي،
عقد_التركيب)` يحتاج عقدًا مُبرهَنًا لم يُبنَ بعد؛ وإدخال `مختلط` الآن منفذٌ
لخلط الجنسين قبل برهان عقدهما. والجنس الصرفي-الوظيفي **مُعلَن غير قابل للبناء**
في هذه المرحلة: لا مفردة سمات صرفية مجمَّدة بعد، فمن أعلنه رُدَّ تصريحًا بأن
مفرداته لم تُولَد، لا بادّعاء أنه غير مشروع.

`سؤال الطور الثاني` مسجَّل بلا جواب، وبثلاثة احتمالات لا احتمالين، لأن الثنائية
هنا ثنائية كاذبة: قد يكون التقسيم مستردًّا توزيعيًّا لكن بعد ولادة متغيّرات
بنيوية أدنى (حدّ، وموضع، وتحوّل صرفي) تصير حواملَ مرخَّصة — وهو ما يوافق قانون
الطبقات: `إغلاق طبقة ← تسليم ← ولادة الطبقة الأعلى`. ولا تُجيب هذه الوحدة عن
أيٍّ من الثلاثة.

نطاق الوحدة وحدودها — تسجيل صريح، لا اعتذار لاحق:

* لا أنبوب قياس هنا، ولا مدوَّنة، ولا سمات جديدة، ولا تجربة طور ثانٍ مُنشأة:
  المُنشأ هنا **البنية التي تمنع تزوير الترتيب الزمني**، لا التجربة نفسها.
* سلطويًّا: `ProbeResultAttachment != BirthVerdict`، و
  `FrozenFollowupProbeSpecification != BirthExperimentSpecification`، و
  `PreEvidenceProbeSpecificationRegistry != PreEvidenceSpecificationRegistry`.
  لا نوع في `kernel/`، ولا `Freeze` نواةً، ولا `E0`، ولا بوّابة نواة تقرأ شيئًا
  من هذه الوحدة. وسجلّ التجميد هنا سجلٌّ محلّي لطبقة التوثيق، لا سلطة نواة.
* والمشترك مع النواة شيءٌ واحد لا يحمل سلطة: بدائية الترميز القانوني والبصمة في
  `alghanem.canonical_content`. فاستعمال ترميزٍ واحد يمنع انحراف نسختين، ولا
  ينقل من النواة أي إذن.
"""

from __future__ import annotations

from dataclasses import dataclass, field, fields
from enum import Enum
from typing import Final

from alghanem.canonical_content import (
    CANONICAL_HASH_ALGORITHM,
    canonical_bytes,
    canonical_digest,
    is_canonical_digest,
)

from .distributional_probe_report import ProbeFeature, SelectionCriterion

_PREREGISTRATION_TOKEN = object()
_CANONICALIZATION_VERSION: Final = "followup-probe-specification-manifest-v1"


class ProbePreregistrationError(ValueError):
    """رُفض مدخلٌ خارج المجال المُجمَّد؛ لا يُحمَل على أقرب حالة."""


class EvidenceGenus(Enum):
    """جنس الدليل المغلق؛ قيمتان لا ثالثة، ولا قيمة `مختلط` تخفي التركيب."""

    DISTRIBUTIONAL = "توزيعي"
    MORPHO_FUNCTIONAL = "صرفي_وظيفي"


class StoppingRule(Enum):
    """قاعدة التوقّف المغلقة؛ تُعلَن قبل الدليل لا تُختار بعد رؤيته."""

    EXHAUSTIVE_DECLARED_K_SCAN = "مسح_شامل_لمدى_k_المُعلَن"


class Phase2Hypothesis(Enum):
    """احتمالات الطور الثاني الثلاثة المفتوحة؛ لا ثنائية كاذبة بينها."""

    CURRENT_FEATURES_INSUFFICIENT = "السمات_الخمس_الحالية_وحدها_غير_كافية"
    DIVISION_IS_NOT_SURFACE_DISTRIBUTIONAL = "التقسيم_ليس_توزيعيًّا_سطحيًّا"
    NEEDS_LOWER_BORN_VARIABLES = "التقسيم_يحتاج_متغيّرات_بنيوية_أدنى_مولودة"


COMPOSITION_DEFERRAL_NOTE: Final = (
    "الجمع بين جنسي الدليل مؤجَّل: لا يُعلَن جنسٌ `مختلط` في المفردة، وإنما "
    "يحتاج تركيبًا صريحًا (دليل توزيعي، ودليل صرفي وظيفي، وعقد تركيب مُبرهَن) "
    "لم يُبنَ بعد"
)

MORPHO_FUNCTIONAL_VOCABULARY_DEFERRAL_NOTE: Final = (
    "الجنس الصرفي الوظيفي مُعلَن ولا مفردة سمات مجمَّدة له بعد، فلا تُبنى به "
    "مواصفة حتى تُولَد مفرداته؛ وإعلانه بلا مفردات ادّعاءُ نطاق غير مبرهَن"
)

PREREGISTRATION_AUTHORITY_NOTE: Final = (
    "تجميد وتوثيق فقط: لا يُنتج ولادةً ولا حكم ولادة، ولا يُجمَّد في النواة، "
    "ولا تقرأه أيّ بوّابة فيها"
)

PHASE2_QUESTION_REMAINS_OPEN_NOTE: Final = (
    "سؤال الطور الثاني مسجَّل مفتوحًا بثلاثة احتمالات، ولا جواب له في هذه "
    "المرحلة؛ فحسمه يحتاج تجربةً مُجمَّدة قبل دليلها لم تُنشأ بعد"
)

_RESULT_BEARING_FIELD_MARKERS: Final = (
    "result",
    "outcome",
    "cluster",
    "partition",
    "layer",
    "silhouette",
    "selected",
    "answer",
    "verdict",
)

_ANSWER_BEARING_FIELD_MARKERS: Final = (
    "answer",
    "verdict",
    "conclusion",
    "resolution",
    "decision",
    "selected",
    "preferred",
)

if len(EvidenceGenus) != 2:  # pragma: no cover - guard
    raise RuntimeError("evidence genus is deliberately two-valued in this milestone")


def _require_non_blank(value: str, field_name: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise ProbePreregistrationError(f"{field_name} must be non-blank text")
    return value


def _require_positive(value: int, field_name: str) -> int:
    if not isinstance(value, int) or isinstance(value, bool) or value <= 0:
        raise ProbePreregistrationError(f"{field_name} must be a positive integer")
    return value


@dataclass(frozen=True, slots=True)
class FrozenFollowupProbeSpecification:
    """مواصفة تحقيق قادم، مُعلَنة قبل دليلها بالكامل، وبلا أي حقل نتيجة."""

    experiment_id: str
    revision_id: str
    revision_sequence: int
    evidence_genus: EvidenceGenus
    features: tuple[ProbeFeature, ...]
    minimum_support: int
    smallest_scanned_k: int
    largest_scanned_k: int
    selection_criterion: SelectionCriterion
    stopping_rule: StoppingRule
    evaluation_criterion_id: str
    evaluation_criterion: str

    def __post_init__(self) -> None:
        _require_non_blank(self.experiment_id, "معرّف التجربة")
        _require_non_blank(self.revision_id, "معرّف المراجعة")
        _require_non_blank(self.evaluation_criterion_id, "معرّف معيار التقويم")
        _require_non_blank(self.evaluation_criterion, "معيار التقويم")
        if (
            not isinstance(self.revision_sequence, int)
            or isinstance(self.revision_sequence, bool)
            or self.revision_sequence < 0
        ):
            raise ProbePreregistrationError("ترتيب المراجعة عددٌ صحيح غير سالب")
        if not isinstance(self.evidence_genus, EvidenceGenus):
            raise ProbePreregistrationError(
                "جنس الدليل must come from the closed vocabulary"
            )
        if self.evidence_genus is not EvidenceGenus.DISTRIBUTIONAL:
            raise ProbePreregistrationError(MORPHO_FUNCTIONAL_VOCABULARY_DEFERRAL_NOTE)
        if not isinstance(self.features, tuple) or not self.features:
            raise ProbePreregistrationError("السمات تُعلَن مجموعةً غير فارغة")
        for feature in self.features:
            if not isinstance(feature, ProbeFeature):
                raise ProbePreregistrationError(
                    "كل سمة must come from the closed vocabulary"
                )
        if len(set(self.features)) != len(self.features):
            raise ProbePreregistrationError("تكرّرت سمة واحدة في المواصفة")
        if not isinstance(self.selection_criterion, SelectionCriterion):
            raise ProbePreregistrationError(
                "معيار الاختيار must come from the closed vocabulary"
            )
        if not isinstance(self.stopping_rule, StoppingRule):
            raise ProbePreregistrationError(
                "قاعدة التوقّف must come from the closed vocabulary"
            )
        _require_positive(self.minimum_support, "شرط الدعم")
        _require_positive(self.smallest_scanned_k, "أصغر k مفحوص")
        _require_positive(self.largest_scanned_k, "أكبر k مفحوص")
        if self.smallest_scanned_k < 2:
            raise ProbePreregistrationError("مسح k يبدأ من ٢ فصاعدًا، فلا عنقدة بواحد")
        if self.largest_scanned_k <= self.smallest_scanned_k:
            raise ProbePreregistrationError("أكبر k المفحوص يجب أن يتجاوز أصغره")

    @property
    def scanned_k_values(self) -> tuple[int, ...]:
        """قيم k المُجمَّدة كاملةً، من أصغرها إلى أكبرها بلا ثغرة."""

        return tuple(range(self.smallest_scanned_k, self.largest_scanned_k + 1))

    @property
    def freeze_key(self) -> tuple[str, str, int]:
        """هوية التجميد: التجربة، ومراجعتها، وترتيبها."""

        return (self.experiment_id, self.revision_id, self.revision_sequence)


@dataclass(frozen=True, slots=True)
class FollowupProbeSpecificationContentIdentity:
    """بصمةٌ لمحتوى مواصفة، لا تصدر إلا عن المُرمِّز."""

    algorithm: str
    canonicalization_version: str
    digest: str
    _token: object | None = field(default=None, repr=False, compare=False)

    def __post_init__(self) -> None:
        if self._token is not _PREREGISTRATION_TOKEN:
            raise ProbePreregistrationError(
                "بصمة المحتوى لا تصدر إلا عن CanonicalFollowupProbeSpecificationEncoder"
            )
        if (
            self.algorithm != CANONICAL_HASH_ALGORITHM
            or self.canonicalization_version != _CANONICALIZATION_VERSION
            or not is_canonical_digest(self.digest)
        ):
            raise ProbePreregistrationError("بصمة محتوى المواصفة غير سليمة")


@dataclass(frozen=True, slots=True)
class CanonicalFollowupProbeSpecificationManifest:
    """المحتوى القانوني الكامل لمواصفة واحدة، ببصمته."""

    content_bytes: bytes
    content_id: FollowupProbeSpecificationContentIdentity
    _token: object | None = field(default=None, repr=False, compare=False)

    def __post_init__(self) -> None:
        if self._token is not _PREREGISTRATION_TOKEN:
            raise ProbePreregistrationError("البيان القانوني لا يصدر إلا عن المُرمِّز")
        if canonical_digest(self.content_bytes) != self.content_id.digest:
            raise ProbePreregistrationError("بايتات البيان تخالف بصمته")


class CanonicalFollowupProbeSpecificationEncoder:
    """المُصدِر الوحيد للبيانات القانونية لمواصفات التحقيق القادم."""

    COVERAGE: Final = (
        "experiment_id",
        "revision_id",
        "revision_sequence",
        "evidence_genus",
        "features",
        "minimum_support",
        "smallest_scanned_k",
        "largest_scanned_k",
        "selection_criterion",
        "stopping_rule",
        "evaluation_criterion_id",
        "evaluation_criterion",
    )

    @classmethod
    def encode(
        cls, specification: FrozenFollowupProbeSpecification
    ) -> CanonicalFollowupProbeSpecificationManifest:
        if type(specification) is not FrozenFollowupProbeSpecification:
            raise ProbePreregistrationError("الترميز القانوني يلزمه مواصفة تحقيق قادم")
        cls._assert_schema_coverage()
        encoded = {
            "evaluation_criterion": specification.evaluation_criterion,
            "evaluation_criterion_id": specification.evaluation_criterion_id,
            "evidence_genus": specification.evidence_genus.name,
            "experiment_id": specification.experiment_id,
            "features": [feature.name for feature in specification.features],
            "largest_scanned_k": specification.largest_scanned_k,
            "minimum_support": specification.minimum_support,
            "revision_id": specification.revision_id,
            "revision_sequence": specification.revision_sequence,
            "selection_criterion": specification.selection_criterion.name,
            "smallest_scanned_k": specification.smallest_scanned_k,
            "stopping_rule": specification.stopping_rule.name,
            "version": _CANONICALIZATION_VERSION,
        }
        content = canonical_bytes(encoded)
        content_id = FollowupProbeSpecificationContentIdentity(
            algorithm=CANONICAL_HASH_ALGORITHM,
            canonicalization_version=_CANONICALIZATION_VERSION,
            digest=canonical_digest(content),
            _token=_PREREGISTRATION_TOKEN,
        )
        return CanonicalFollowupProbeSpecificationManifest(
            content_bytes=content,
            content_id=content_id,
            _token=_PREREGISTRATION_TOKEN,
        )

    @classmethod
    def _assert_schema_coverage(cls) -> None:
        declared = {item.name for item in fields(FrozenFollowupProbeSpecification)}
        if declared != set(cls.COVERAGE):
            raise RuntimeError(
                "canonical follow-up manifest coverage must explicitly account "
                "for every frozen specification field"
            )


@dataclass(frozen=True, slots=True)
class FrozenPreEvidenceProbeManifest:
    """محتوى مواصفة مُجمَّد قبل دليله؛ لا يصدر إلا عن سجلّ التجميد."""

    canonical_manifest: CanonicalFollowupProbeSpecificationManifest
    _token: object | None = field(default=None, repr=False, compare=False)

    def __post_init__(self) -> None:
        if self._token is not _PREREGISTRATION_TOKEN:
            raise ProbePreregistrationError(
                "البيان المُجمَّد قبل الدليل لا يصدر إلا عن سجلّ التجميد"
            )

    @property
    def content_id(self) -> FollowupProbeSpecificationContentIdentity:
        """بصمة المحتوى المُجمَّد."""

        return self.canonical_manifest.content_id


class PreEvidenceProbeSpecificationRegistry:
    """سجلّ تجميد محلّي لطبقة التوثيق؛ ليس سلطة نواة ولا يشبهها في المفعول."""

    def __init__(self) -> None:
        self._frozen: dict[tuple[str, str, int], FrozenPreEvidenceProbeManifest] = {}

    def freeze(
        self, specification: FrozenFollowupProbeSpecification
    ) -> FrozenPreEvidenceProbeManifest:
        """جمِّد محتوى مواصفة قبل دليلها، وارفض تغييرًا لاحقًا تحت هويتها."""

        if type(specification) is not FrozenFollowupProbeSpecification:
            raise ProbePreregistrationError("التجميد يلزمه مواصفة تحقيق قادم")
        manifest = CanonicalFollowupProbeSpecificationEncoder.encode(specification)
        key = specification.freeze_key
        existing = self._frozen.get(key)
        if existing is not None:
            if existing.canonical_manifest.content_bytes != manifest.content_bytes:
                raise ProbePreregistrationError(
                    "محتوى المواصفة يخالف ما جُمِّد تحت هذه الهوية؛ فالتغيير بعد "
                    "التجميد يحتاج مراجعةً جديدة لا كتابةً فوق القديمة"
                )
            return existing
        frozen = FrozenPreEvidenceProbeManifest(
            canonical_manifest=manifest, _token=_PREREGISTRATION_TOKEN
        )
        self._frozen[key] = frozen
        return frozen


@dataclass(frozen=True, slots=True)
class FollowupProbeSpecificationContentBinding:
    """يُثبِت أن مواصفةً حيّة تُعيد إنتاج محتوًى مُجمَّدًا قبل دليله بعينه."""

    specification: FrozenFollowupProbeSpecification
    frozen_manifest: FrozenPreEvidenceProbeManifest
    content_id: FollowupProbeSpecificationContentIdentity = field(init=False)

    def __post_init__(self) -> None:
        if type(self.specification) is not FrozenFollowupProbeSpecification:
            raise ProbePreregistrationError("الربط يلزمه مواصفة تحقيق قادم")
        if type(self.frozen_manifest) is not FrozenPreEvidenceProbeManifest:
            raise ProbePreregistrationError("الربط يلزمه بيانًا مُجمَّدًا قبل الدليل")
        runtime = CanonicalFollowupProbeSpecificationEncoder.encode(self.specification)
        if (
            runtime.content_bytes
            != self.frozen_manifest.canonical_manifest.content_bytes
        ):
            raise ProbePreregistrationError(
                "محتوى المواصفة الحيّة لا يطابق المحتوى المُجمَّد قبل الدليل"
            )
        object.__setattr__(self, "content_id", self.frozen_manifest.content_id)


@dataclass(frozen=True, slots=True)
class ProbeResultAttachment:
    """نتيجةٌ لا تُبنى إلا مربوطةً بمواصفةٍ سبقتها زمنيًّا ومحتوًى."""

    binding: FollowupProbeSpecificationContentBinding
    used_features: tuple[ProbeFeature, ...]
    used_selection_criterion: SelectionCriterion
    used_stopping_rule: StoppingRule
    selected_k: int

    def __post_init__(self) -> None:
        if type(self.binding) is not FollowupProbeSpecificationContentBinding:
            raise ProbePreregistrationError(
                "النتيجة لا تُبنى إلا بربط محتوًى متحقَّق منه بمواصفة مُجمَّدة قبل دليلها"
            )
        specification = self.binding.specification
        if not isinstance(self.used_features, tuple) or not self.used_features:
            raise ProbePreregistrationError("سمات النتيجة تُعلَن مجموعةً غير فارغة")
        for feature in self.used_features:
            if not isinstance(feature, ProbeFeature):
                raise ProbePreregistrationError(
                    "كل سمة must come from the closed vocabulary"
                )
        if len(set(self.used_features)) != len(self.used_features):
            raise ProbePreregistrationError("تكرّرت سمة واحدة في النتيجة")
        frozen_features = set(specification.features)
        if not set(self.used_features) <= frozen_features:
            raise ProbePreregistrationError(
                "سمةٌ في النتيجة خارج السمات المُجمَّدة؛ واختيار السمات بعد رؤية "
                "العناقيد هو عين ما تمنعه بوّابة ما قبل الدليل"
            )
        if self.used_selection_criterion is not specification.selection_criterion:
            raise ProbePreregistrationError(
                "معيار الحسم المستعمَل يخالف المُجمَّد في المواصفة"
            )
        if self.used_stopping_rule is not specification.stopping_rule:
            raise ProbePreregistrationError(
                "قاعدة التوقّف المستعمَلة تخالف المُجمَّدة في المواصفة"
            )
        if self.selected_k not in specification.scanned_k_values:
            raise ProbePreregistrationError("k المختار خارج المدى المُجمَّد قبل الدليل")

    @property
    def content_id(self) -> FollowupProbeSpecificationContentIdentity:
        """بصمة المواصفة التي سبقت هذه النتيجة."""

        return self.binding.content_id


@dataclass(frozen=True, slots=True)
class Phase2OpenQuestion:
    """سؤالٌ مسجَّل مفتوحًا: احتمالاته كلّها، وسبب بقائه، ولا جواب فيه."""

    question_id: str
    hypotheses: tuple[Phase2Hypothesis, ...]
    why_open: str

    def __post_init__(self) -> None:
        _require_non_blank(self.question_id, "معرّف السؤال")
        _require_non_blank(self.why_open, "سبب بقاء السؤال مفتوحًا")
        if not isinstance(self.hypotheses, tuple):
            raise ProbePreregistrationError("الاحتمالات تُعلَن مجموعةً مرتَّبة")
        for hypothesis in self.hypotheses:
            if not isinstance(hypothesis, Phase2Hypothesis):
                raise ProbePreregistrationError(
                    "كل احتمال must come from the closed vocabulary"
                )
        if set(self.hypotheses) != set(Phase2Hypothesis) or len(self.hypotheses) != len(
            Phase2Hypothesis
        ):
            raise ProbePreregistrationError(
                "السؤال المفتوح يُعلِن احتمالاته كلّها بلا تكرار؛ وإسقاط احتمال "
                "منها يصنع ثنائيةً كاذبة"
            )

    @property
    def remains_open(self) -> bool:
        """هل بقي السؤال بلا جواب؟ نعم دائمًا في هذه المرحلة، بنيويًّا."""

        return True


def _assert_no_fields_matching(
    specification_type: type, markers: tuple[str, ...], message: str
) -> None:
    declared = {item.name for item in fields(specification_type)}
    for name in declared:
        if any(marker in name for marker in markers):
            raise RuntimeError(message)


_assert_no_fields_matching(
    FrozenFollowupProbeSpecification,
    _RESULT_BEARING_FIELD_MARKERS,
    "a pre-evidence specification may not carry any result field",
)
_assert_no_fields_matching(
    Phase2OpenQuestion,
    _ANSWER_BEARING_FIELD_MARKERS,
    "an open question may not carry any answer or verdict field",
)


PHASE2_OPEN_QUESTION: Final = Phase2OpenQuestion(
    question_id="phase2-identity-level-of-the-ism-fil-harf-division",
    hypotheses=(
        Phase2Hypothesis.CURRENT_FEATURES_INSUFFICIENT,
        Phase2Hypothesis.DIVISION_IS_NOT_SURFACE_DISTRIBUTIONAL,
        Phase2Hypothesis.NEEDS_LOWER_BORN_VARIABLES,
    ),
    why_open=(
        "النتيجة السلبية المسجَّلة تنفي استرجاع التقسيم بالسمات الخمس بعينها، "
        "ولا تفصل بين ثلاثة احتمالات: أن تكون السمات وحدها غير كافية، أو أن "
        "يكون التقسيم ليس نوعًا توزيعيًّا سطحيًّا أصلًا فلا يستعيده أي عدد من "
        "سمات هذا الجنس، أو أن يكون استرجاعه موقوفًا على ولادة متغيّرات بنيوية "
        "أدنى (حدّ، وموضع، وتحوّل صرفي) تصير حواملَ مرخَّصة أولًا. وحسم ذلك "
        "يحتاج تجربةً مُجمَّدة قبل دليلها لم تُنشأ بعد، فالجواب هنا تزوير"
    ),
)

if not PHASE2_OPEN_QUESTION.remains_open:  # pragma: no cover - guard
    raise RuntimeError("the recorded phase-2 question is an open one")


__all__ = [
    "COMPOSITION_DEFERRAL_NOTE",
    "CanonicalFollowupProbeSpecificationEncoder",
    "CanonicalFollowupProbeSpecificationManifest",
    "EvidenceGenus",
    "FollowupProbeSpecificationContentBinding",
    "FollowupProbeSpecificationContentIdentity",
    "FrozenFollowupProbeSpecification",
    "FrozenPreEvidenceProbeManifest",
    "MORPHO_FUNCTIONAL_VOCABULARY_DEFERRAL_NOTE",
    "PHASE2_OPEN_QUESTION",
    "PHASE2_QUESTION_REMAINS_OPEN_NOTE",
    "PREREGISTRATION_AUTHORITY_NOTE",
    "Phase2Hypothesis",
    "Phase2OpenQuestion",
    "PreEvidenceProbeSpecificationRegistry",
    "ProbePreregistrationError",
    "ProbeResultAttachment",
    "StoppingRule",
]
