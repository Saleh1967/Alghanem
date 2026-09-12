"""تحقيق المناط على كلمة عربية واحدة: تشغيل بوّابة G0.EA.1 على بطاقة حقيقية.

هذه الوحدة **لا تضع قانونًا جديدًا**. البوّابة مبنيّة منذ `G0.EA.1`
(`alghanem.kernel.applicability`)، وظلّت حتى اليوم بلا تطبيقٍ واحد على مادّة
لغوية. وهذا أوّل تطبيقٍ لها على كلمةٍ بعينها: **(قُرُوء)** في البقرة:228،
عبر البطاقة `examples/external_audit/quru_2_228.yaml`.

`ExternalAuditor != KernelAuthority` محفوظٌ كما في `test_hadhan_*`: البطاقة
تُقدِّم قرائنَ ونصًّا وعلاقاتٍ مُعلَنة، ولا يدخل شيءٌ منها البوّابةَ إلا مشتقًّا
بدالّة هنا. ولا تُصدر هذه الوحدة حكمًا ولا ولادةً ولا معرفة.

`جنس البيان` مفردةٌ ثنائية مغلقة عمدًا ولا ثالث لها:

* `بيان_بالقول` — قرينةٌ **نصّية**: نصُّ الآية نفسها، أو نقلٌ مُسنَدٌ في مصدر
  تفسيرٍ مُسمّى.
* `بيان_بالفعل` — إشارةٌ **استعمالية معجمية**: ورود المادّة في معجمٍ مُسمّى.

والمصطلحان مأخوذان هنا بالمعنى الذي صرّح به طالبُ العمل (قولٌ منصوص مقابل
استعمالٍ مشهود)، لا بتمام معناهما الأصولي في بيان الشارع؛ ولا صفَّ في
`docs/CONSTITUTION.md` يُرخِّص التوسّع بهما إلى ما وراء هذا الحدّ
(`BAYAN_TERMS_ARE_USED_IN_THE_DECLARED_NARROW_SENSE_NOTE`).

**الترتيب مُشتَقٌّ من الجنس ولا يُكتَب**: لا حقلَ رتبةٍ ولا أولويةٍ في أيّ
قرينة، ويُرفَض عند القراءة أيُّ مفتاحٍ من هذا الجنس بدل أن يمضي صامتًا. وموضعُ
القول في ترتيب البوّابة يحتاج تصريحًا دقيقًا لئلا يُقرأ مقلوبًا: بوّابة
`G0.EA.1` تحسم **بأضعف نموذجٍ يُغلِق**، و«نموذجٌ أقوى غير محسوم لا يَنقُض
الأضعف». فالموضع غير القابل للنقض في هذا الترتيب هو **موضع الأضعف**، ولذلك
يُوضَع `بيان_بالقول` فيه، ويُعلَن `بيان_بالفعل` **أقوى منه** فلا يَنقُضه أبدًا.
وهذا هو بعينه المطلوب أصوليًّا — تقدُّمُ القول على الفعل — مُعبَّرًا عنه بترتيب
هذه البوّابة لا بترتيبٍ آخر
(`QAWL_OCCUPIES_THE_NON_OVERRIDABLE_POSITION_NOTE`).

**ولا يستقلّ بيان الفعل بالحسم بنيويًّا**: بطاقةٌ فيها قرينةُ فعلٍ بلا قرينةِ
قولٍ واحدةٍ تُرفَض عند القراءة، فلا تُتصوَّر حالةٌ يكون فيها النموذج المعجمي
هو الأضعف فيحسم وحده (`FIL_NEVER_DECIDES_ALONE_NOTE`).

**ما تقرؤه هذه الوحدة شهادةٌ لا قياس**: المصادر المُسمّاة (جامع البيان، لسان
العرب) تُذكَر بأسمائها في البطاقة، ولا تُقرأ هنا مدوَّنةٌ ولا يُعاد اشتقاق
بصمةِ ملفّ. فليس في هذه الوحدة قياسٌ على معجم، والفارق هو نفسه الذي يُقرِّره
`docs/reference/arabic_identity_confusion_catalog.md` بين القياس والشهادة
(`NAMED_SOURCE_IS_TESTIMONY_NOT_MEASUREMENT_NOTE`).

**ولا مسار `BLOCK` في هذه الطبقة**، وغيابه مُصرَّحٌ به لا مُغطّى: ليس في
البطاقة قرينةٌ تُكذِّب النموذج المختبَر تكذيبًا بنيويًّا. والقرينة المُقصِية
المضافة هنا تُقصي **قراءةً منافسة** ولا تُكذِّب النموذج المختبَر، فالمُقيِّمان
ما زالا يُنتجان `PASS` أو `DEFER` فقط (`NO_BLOCK_PATH_IN_THIS_LAYER_NOTE`).

**ووظيفة القرينة جنسٌ مستقلٌّ يُضاف بجانب جنس البيان لا بديلًا عنه**: مفردة
`QarinaFunction` ثنائية مغلقة ولا ثالث لها — `قرينة_مؤيِّدة` تُرجِّح قراءةً
دون إلغاء الأخرى، و`قرينة_مُقصِية` تُبطِل انطباق قراءةٍ منافسةٍ مُسمّاةٍ
بالكلّية على هذا الموضع بعينه. وجنس البيان (قول/فعل) وترتيبه المُشتقّ لم
يتغيّرا بحرف.

**والإقصاء نوعٌ لا درجة**: تُرفَض عند الإنشاء كلُّ قرينةٍ تُصنَّف `مُقصِية`
ولا يُصرِّح نصُّها باستحالة القراءة المُقصاة على هذا الموضع، أو يُصرِّح بأنها
«أرجح» فحسب؛ فالفارق بين الإقصاء والترجيح ليس شدّةً في العبارة
(`ELIMINATION_IS_A_KIND_NOT_A_DEGREE_NOTE`). والقرينة الواحدة تُقصي قراءةً
واحدةً مُسمّاةً لا قائمة، ولا دالّةَ تُحوِّل تراكمَ المؤيِّدات إلى إقصاء
(`ONE_SOUND_ELIMINATION_SUFFICES_NOTE`).

**ولا يُقصي بيان الفعل وحده**، امتدادًا لنفس علّة `FIL_NEVER_DECIDES_ALONE`
لا افتراضًا لتشابهٍ فئويّ: القرائن المُقصِية لا تُسقِط قراءةً منافسةً إلا
إذا كان جنس بيانها `بيان_بالقول`، فيبقى الإقصاء صادرًا من موضع الأضعف الذي
لا يُنقَض (`FIL_NEGATION_NEVER_ELIMINATES_ALONE_NOTE`).

وبطاقة «أنّى» في البقرة:223 (`examples/external_audit/anna_2_223.yaml`) هي
تطبيق هذا الجنس: «حرثكم» في الآية نفسها تُقصي قراءة «من أين»، فتُغلِق البوّابة
بـ`PASS` بقرينةٍ مُقصِيةٍ واحدة، دون تراكم مؤيِّدات.

والنتيجة المتوقَّعة على بطاقة (قُرُوء) `DEFER` بفضلةٍ مُسمّاة، وهي **نجاح**
لا نقص: القراءة المنافسة (طهر) مُعلَنةٌ `غير_متعينة`، والقرائن القولية نفسها
تَنقُل المعنيين معًا عن مصدرٍ واحدٍ مُسمّى، فلا تُعيِّن واحدًا منهما. وأيّ
هندسةٍ تُجبر النتيجة على `PASS` تُلغي قيمة التطبيق كلّه.
"""

from __future__ import annotations

import hashlib
import json
from collections.abc import Callable, Mapping
from dataclasses import dataclass, fields
from enum import Enum
from typing import Any, Final

from alghanem.kernel import AuthenticatedObservationBinding
from alghanem.kernel.anchor import Anchor
from alghanem.kernel.applicability import (
    ApplicabilityAssessmentGate,
    ApplicabilityAssessmentSpecification,
    ApplicabilityAssessmentStatus,
    ApplicabilityEvaluatorRegistry,
    ApplicabilityModelResult,
    EvidenceApplicabilityAssessment,
    FrozenApplicabilityModel,
    SealedApplicabilityEvaluatorRegistry,
)
from alghanem.kernel.claim_constitution import (
    CanonicalClaimContentEncoder,
    ClaimCandidate,
    ClaimContentManifest,
    ClaimCore,
    ClaimOccurrenceRef,
    ClaimPolarity,
    ClaimScopeRef,
    PredicateRef,
)
from alghanem.kernel.evidence_role import EvidenceRoleCandidate, EvidenceRoleRef
from alghanem.kernel.residual import Residual
from alghanem.kernel.trace import Trace

from .external_audit import ExternalAuditError, canonical_relation
from .text_key import comparison_key

__all__ = [
    "BAYAN_TERMS_ARE_USED_IN_THE_DECLARED_NARROW_SENSE_NOTE",
    "CLOSED_BAYAN_VOCABULARY",
    "CLOSED_QARINA_FUNCTION_VOCABULARY",
    "ELIMINATION_IS_A_KIND_NOT_A_DEGREE_NOTE",
    "FIL_MODEL_ID",
    "FIL_NEGATION_NEVER_ELIMINATES_ALONE_NOTE",
    "FIL_NEVER_DECIDES_ALONE_NOTE",
    "FORBIDDEN_QARINA_KEYS",
    "IMPOSSIBILITY_MARKERS",
    "MANAT_ROLE_IDENTIFIER",
    "NAMED_SOURCE_IS_TESTIMONY_NOT_MEASUREMENT_NOTE",
    "NO_BLOCK_PATH_IN_THIS_LAYER_NOTE",
    "ONE_SOUND_ELIMINATION_SUFFICES_NOTE",
    "PREFERENCE_MARKERS",
    "QAWL_MODEL_ID",
    "QAWL_OCCUPIES_THE_NON_OVERRIDABLE_POSITION_NOTE",
    "BayanKind",
    "ManatQarina",
    "ManatVerificationError",
    "QarinaFunction",
    "assess_manat_from_card",
    "build_manat_candidate",
    "derive_bayan_models",
    "eliminated_competing_readings",
    "manat_claim_anchor",
    "manat_claim_scope",
    "read_manat_qarain",
    "seal_bayan_evaluators",
    "undetermined_competing_readings",
]


class ManatVerificationError(ValueError):
    """بطاقةٌ لا تصلح لتحقيق المناط بهذا العقد."""


class BayanKind(Enum):
    """مفردة جنس البيان المغلقة: قولٌ وفعل، ولا ثالث."""

    QAWL = "بيان_بالقول"
    FIL = "بيان_بالفعل"


CLOSED_BAYAN_VOCABULARY: Final = tuple(kind.value for kind in BayanKind)


class QarinaFunction(Enum):
    """مفردة وظيفة القرينة المغلقة: مؤيِّدةٌ ومُقصِية، ولا ثالث ولا مختلط."""

    SUPPORTING = "قرينة_مؤيِّدة"
    NEGATING = "قرينة_مُقصِية"


CLOSED_QARINA_FUNCTION_VOCABULARY: Final = tuple(
    function.value for function in QarinaFunction
)

IMPOSSIBILITY_MARKERS: Final = (
    "يستحيل",
    "مستحيل",
    "استحالة",
    "يمتنع",
    "امتناع",
    "لا يتصور",
    "لا يصح",
    "منتف",
)
PREFERENCE_MARKERS: Final = (
    "أرجح",
    "راجح",
    "ترجيح",
    "أظهر",
    "أقوى",
    "أولى",
    "أضعف",
    "الأكثر",
    "الأشهر",
)

QAWL_MODEL_ID: Final = "نموذج_بيان_بالقول"
FIL_MODEL_ID: Final = "نموذج_بيان_بالفعل"
MANAT_ROLE_IDENTIFIER: Final = "قرينة_تحقيق_المناط"

ALLOWED_QARINA_KEYS: Final = (
    "معرف",
    "القرينة",
    "جنس_البيان",
    "وظيفة_القرينة",
    "القراءة_المُقصاة",
    "المصدر_المُسمّى",
)
FORBIDDEN_QARINA_KEYS: Final = (
    "رتبة",
    "ترتيب",
    "أولوية",
    "وزن",
    "حكم",
    "نتيجة",
    "الحالة",
    "قرار",
)

QAWL_OCCUPIES_THE_NON_OVERRIDABLE_POSITION_NOTE: Final = (
    "QawlOccupiesTheNonOverridablePosition: بوّابة G0.EA.1 تحسم بأضعف نموذجٍ "
    "يُغلِق، والأقوى غير المحسوم لا يَنقُضه؛ فيُوضَع بيان القول في موضع الأضعف "
    "لأنه الموضع الذي لا يُنقَض، ويُعلَن بيان الفعل أقوى منه فلا يَنقُضه"
)
FIL_NEVER_DECIDES_ALONE_NOTE: Final = (
    "FilNeverDecidesAlone: بطاقةٌ تُعلن قرينةَ بيانٍ بالفعل بلا قرينةِ بيانٍ "
    "بالقول تُرفَض عند القراءة، فلا تُتصوَّر حالةٌ يستقلّ فيها المعجمي بالحسم"
)
NO_BLOCK_PATH_IN_THIS_LAYER_NOTE: Final = (
    "NoBlockPathInThisLayer: القرينة المُقصِية تُقصي قراءةً منافسةً ولا تُكذِّب "
    "النموذج المختبَر، فالمُقيِّمان يُنتجان PASS أو DEFER فقط، وغيابُ BLOCK "
    "مُصرَّحٌ به لا مُغطّى"
)
ELIMINATION_IS_A_KIND_NOT_A_DEGREE_NOTE: Final = (
    "EliminationIsAKindNotADegree: القرينة المُقصِية يجب أن يُصرِّح نصُّها "
    "باستحالة القراءة المُقصاة على هذا الموضع بعينه؛ ونصٌّ يصفها بأنها أرجح "
    "أو أظهر يُرفَض عند الإنشاء، فالفارق نوعٌ لا درجة"
)
ONE_SOUND_ELIMINATION_SUFFICES_NOTE: Final = (
    "OneSoundEliminationSuffices: الإقصاء فعلٌ نوعيٌّ لقرينةٍ واحدة تُسمّي "
    "قراءةً واحدةً مُقصاة، فلا قائمةَ إقصاءاتٍ في القرينة ولا تراكمَ مؤيِّداتٍ "
    "يُعامَل إقصاءً، وقرينةٌ مُقصِيةٌ واحدةٌ تكفي لإغلاق البوّابة بلا تعزيز"
)
FIL_NEGATION_NEVER_ELIMINATES_ALONE_NOTE: Final = (
    "FilNegationNeverEliminatesAlone: امتدادٌ مُصرَّحٌ لأصله "
    "FIL_NEVER_DECIDES_ALONE_NOTE بنفس العلّة لا بتشابهٍ فئويّ صامت: لا يستقلّ "
    "المعجمي بالحسم، فكذلك لا يُسقِط قرينةً منافسةً وحده؛ ولا يُقصي إلا ما "
    "كان جنس بيانه بيانًا بالقول"
)
NAMED_SOURCE_IS_TESTIMONY_NOT_MEASUREMENT_NOTE: Final = (
    "NamedSourceIsTestimonyNotMeasurement: المصادر المُسمّاة تُذكَر بأسمائها "
    "ولا تُقرأ هنا مدوَّنةٌ ولا تُعاد بصمةُ ملفّ، فهذه شهادةٌ لا قياس"
)
BAYAN_TERMS_ARE_USED_IN_THE_DECLARED_NARROW_SENSE_NOTE: Final = (
    "BayanTermsAreUsedInTheDeclaredNarrowSense: القول والفعل هنا نصٌّ منقول "
    "مقابل استعمالٍ معجميّ مشهود، لا تمامُ معناهما في بيان الشارع"
)

_KIND_BY_KEY: Final = {comparison_key(kind.value): kind for kind in BayanKind}
if len(_KIND_BY_KEY) != len(BayanKind):  # pragma: no cover - guard
    raise RuntimeError("two bayan kinds collapse onto one comparison key")

_FUNCTION_BY_KEY: Final = {
    comparison_key(function.value): function for function in QarinaFunction
}
if len(_FUNCTION_BY_KEY) != len(QarinaFunction):  # pragma: no cover - guard
    raise RuntimeError("two qarina functions collapse onto one comparison key")

_IMPOSSIBILITY_KEYS: Final = tuple(
    comparison_key(marker) for marker in IMPOSSIBILITY_MARKERS
)
_PREFERENCE_KEYS: Final = tuple(comparison_key(marker) for marker in PREFERENCE_MARKERS)

_FORBIDDEN_KEY_KEYS: Final = frozenset(
    comparison_key(name) for name in FORBIDDEN_QARINA_KEYS
)
_ALLOWED_KEY_KEYS: Final = frozenset(
    comparison_key(name) for name in ALLOWED_QARINA_KEYS
)


@dataclass(frozen=True, slots=True)
class ManatQarina:
    """قرينةٌ واحدة بجنس بيانها ووظيفتها ومصدرها؛ لا رتبةَ فيها ولا نتيجة."""

    identifier: str
    statement: str
    kind: BayanKind
    named_source: str
    function: QarinaFunction = QarinaFunction.SUPPORTING
    excluded_reading: str | None = None

    def __post_init__(self) -> None:
        for value, name in (
            (self.identifier, "معرف"),
            (self.statement, "القرينة"),
            (self.named_source, "المصدر_المُسمّى"),
        ):
            if type(value) is not str or not value.strip():
                raise ManatVerificationError(f"قرائن_المناط[].{name} نصٌّ غير فارغ")
        if not isinstance(self.kind, BayanKind):
            raise ManatVerificationError("قرائن_المناط[].جنس_البيان من المفردة المغلقة")
        if not isinstance(self.function, QarinaFunction):
            raise ManatVerificationError(
                "قرائن_المناط[].وظيفة_القرينة من المفردة المغلقة"
            )
        if self.function is QarinaFunction.SUPPORTING:
            if self.excluded_reading is not None:
                raise ManatVerificationError(
                    "قرائن_المناط[].القراءة_المُقصاة لا تُعلَن إلا في قرينةٍ "
                    "وظيفتها " + QarinaFunction.NEGATING.value
                )
            return
        if type(self.excluded_reading) is not str or not self.excluded_reading.strip():
            raise ManatVerificationError(
                "قرائن_المناط[].القراءة_المُقصاة نصٌّ غير فارغ يُسمّي قراءةً "
                "منافسةً واحدة؛ " + ONE_SOUND_ELIMINATION_SUFFICES_NOTE
            )
        statement_key = comparison_key(self.statement)
        if any(marker in statement_key for marker in _PREFERENCE_KEYS):
            raise ManatVerificationError(ELIMINATION_IS_A_KIND_NOT_A_DEGREE_NOTE)
        if not any(marker in statement_key for marker in _IMPOSSIBILITY_KEYS):
            raise ManatVerificationError(ELIMINATION_IS_A_KIND_NOT_A_DEGREE_NOTE)


def _assert_no_verdict_fields() -> None:
    """يمنع تسلّل حقلِ رتبةٍ أو نتيجةٍ إلى القرينة لاحقًا."""

    declared = {comparison_key(item.name) for item in fields(ManatQarina)}
    forbidden = {
        comparison_key(name)
        for name in (
            *FORBIDDEN_QARINA_KEYS,
            "rank",
            "order",
            "status",
            "verdict",
            "weight",
            "score",
            "count",
        )
    }
    if declared & forbidden:  # pragma: no cover - import guard
        raise RuntimeError("لا يجوز أن تحمل قرينةُ المناط رتبةً ولا نتيجة")


_assert_no_verdict_fields()


def _require_text(value: Any, field_name: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise ManatVerificationError(f"{field_name} نصٌّ غير فارغ")
    return value


def _canonical_kind(value: str) -> BayanKind:
    kind = _KIND_BY_KEY.get(comparison_key(value))
    if kind is None:
        allowed = "، ".join(CLOSED_BAYAN_VOCABULARY)
        raise ManatVerificationError(
            "قرائن_المناط[].جنس_البيان يجب أن يكون أحد: " + allowed
        )
    return kind


def _canonical_function(value: str) -> QarinaFunction:
    function = _FUNCTION_BY_KEY.get(comparison_key(value))
    if function is None:
        allowed = "، ".join(CLOSED_QARINA_FUNCTION_VOCABULARY)
        raise ManatVerificationError(
            "قرائن_المناط[].وظيفة_القرينة يجب أن يكون أحد: " + allowed
        )
    return function


def _competing_reading_names(card: Mapping[str, Any]) -> tuple[str, ...]:
    """أسماء القراءات المنافسة كما أُعلِنت في البطاقة، بلا تأويل."""

    alternatives = card.get("القراءات_المنافسة")
    if not isinstance(alternatives, list):
        raise ManatVerificationError("القراءات_المنافسة قائمة")
    names: list[str] = []
    for item in alternatives:
        if not isinstance(item, dict):
            raise ManatVerificationError("كل قراءة منافسة يجب أن تكون كائنًا")
        names.append(_require_text(item.get("قراءة"), "القراءات_المنافسة[].قراءة"))
    return tuple(names)


def read_manat_qarain(card: Mapping[str, Any]) -> tuple[ManatQarina, ...]:
    """يقرأ قرائن المناط المُعلَنة، ويرفض كلَّ رتبةٍ مكتوبة.

    الجنس مُعلَنٌ في البطاقة، والترتيب مُشتَقٌّ منه في `derive_bayan_models`؛
    فأيّ مفتاحٍ يُسمّي رتبةً أو أولويةً أو نتيجةً يُسقِط القراءة بدل أن يُهمَل.

    ووظيفة القرينة اختيارية الإعلان لأن الحالة الافتراضية يجب أن تكون الأضعف
    ادّعاءً: غيابُ التصريح يُقرَأ `قرينة_مؤيِّدة`، إذ الإقصاء ادّعاءٌ أقوى لا
    يقوم إلا بتصريحٍ إيجابيّ صارم.
    """

    raw = card.get("قرائن_المناط")
    if not isinstance(raw, list) or not raw:
        raise ManatVerificationError("قرائن_المناط قائمةٌ غير فارغة")
    qarain: list[ManatQarina] = []
    for entry in raw:
        if not isinstance(entry, dict):
            raise ManatVerificationError("كل قرينة مناطٍ يجب أن تكون كائنًا")
        entry_keys = {comparison_key(str(key)) for key in entry}
        if entry_keys & _FORBIDDEN_KEY_KEYS:
            raise ManatVerificationError(
                "قرائن_المناط لا تحمل رتبةً ولا أولويةً ولا نتيجة؛ الترتيب مُشتَقٌّ "
                "من جنس البيان"
            )
        if not entry_keys <= _ALLOWED_KEY_KEYS:
            raise ManatVerificationError(
                "قرائن_المناط[] لا تقبل إلا: " + "، ".join(ALLOWED_QARINA_KEYS)
            )
        declared_function = entry.get("وظيفة_القرينة")
        function = (
            QarinaFunction.SUPPORTING
            if declared_function is None
            else _canonical_function(
                _require_text(declared_function, "قرائن_المناط[].وظيفة_القرينة")
            )
        )
        declared_excluded = entry.get("القراءة_المُقصاة")
        qarain.append(
            ManatQarina(
                identifier=_require_text(entry.get("معرف"), "قرائن_المناط[].معرف"),
                statement=_require_text(entry.get("القرينة"), "قرائن_المناط[].القرينة"),
                kind=_canonical_kind(
                    _require_text(entry.get("جنس_البيان"), "قرائن_المناط[].جنس_البيان")
                ),
                named_source=_require_text(
                    entry.get("المصدر_المُسمّى"), "قرائن_المناط[].المصدر_المُسمّى"
                ),
                function=function,
                excluded_reading=(
                    None
                    if declared_excluded is None
                    else _require_text(
                        declared_excluded, "قرائن_المناط[].القراءة_المُقصاة"
                    )
                ),
            )
        )
    identifiers = [item.identifier for item in qarain]
    if len(set(identifiers)) != len(identifiers):
        raise ManatVerificationError("معرّفات قرائن المناط لا تتكرّر")
    if not any(item.kind is BayanKind.QAWL for item in qarain):
        raise ManatVerificationError(FIL_NEVER_DECIDES_ALONE_NOTE)
    declared_readings = {
        comparison_key(name) for name in _competing_reading_names(card)
    }
    for item in qarain:
        if item.excluded_reading is None:
            continue
        if comparison_key(item.excluded_reading) not in declared_readings:
            raise ManatVerificationError(
                "قرائن_المناط[].القراءة_المُقصاة تُسمّي قراءةً غير مُعلَنةٍ في "
                "القراءات_المنافسة"
            )
    return tuple(qarain)


def derive_bayan_models(
    qarain: tuple[ManatQarina, ...],
) -> tuple[FrozenApplicabilityModel, ...]:
    """يشتقّ ترتيب النماذج من أجناس القرائن وحدها، ولا يقرأ رتبةً مكتوبة.

    نموذج القول يُوضَع في موضع الأضعف — الموضع الذي لا يَنقُضه أقوى — ويُعلَن
    نموذج الفعل أقوى منه بذكره في `weaker_model_ids`.
    """

    if type(qarain) is not tuple or not qarain:
        raise ManatVerificationError("اشتقاق الترتيب يحتاج قرائن مناطٍ مقروءة")
    if not any(item.kind is BayanKind.QAWL for item in qarain):
        raise ManatVerificationError(FIL_NEVER_DECIDES_ALONE_NOTE)
    models = [FrozenApplicabilityModel(QAWL_MODEL_ID, QAWL_MODEL_ID)]
    if any(item.kind is BayanKind.FIL for item in qarain):
        models.append(
            FrozenApplicabilityModel(FIL_MODEL_ID, FIL_MODEL_ID, (QAWL_MODEL_ID,))
        )
    return tuple(models)


def undetermined_competing_readings(card: Mapping[str, Any]) -> tuple[str, ...]:
    """يعيد القراءات المنافسة التي ما زالت علاقتها بالنموذج المختبَر غير متعينة."""

    alternatives = card.get("القراءات_المنافسة")
    if not isinstance(alternatives, list):
        raise ManatVerificationError("القراءات_المنافسة قائمة")
    unresolved: list[str] = []
    for item in alternatives:
        if not isinstance(item, dict):
            raise ManatVerificationError("كل قراءة منافسة يجب أن تكون كائنًا")
        reading = _require_text(item.get("قراءة"), "القراءات_المنافسة[].قراءة")
        declared = _require_text(
            item.get("علاقة_بالنموذج_المختبر"),
            "القراءات_المنافسة[].علاقة_بالنموذج_المختبر",
        )
        try:
            relation = canonical_relation(declared)
        except ExternalAuditError as exc:
            raise ManatVerificationError(str(exc)) from exc
        if relation == "غير_متعينة":
            unresolved.append(reading)
    return tuple(unresolved)


def eliminated_competing_readings(
    card: Mapping[str, Any], qarain: tuple[ManatQarina, ...]
) -> tuple[str, ...]:
    """يعيد القراءات المنافسة التي أُقصيت بقرينةٍ مُقصِيةٍ جنسُ بيانها قول.

    القرينة المُقصِية من `بيان_بالفعل` تُقرَأ وتُذكَر ولا تُسقِط شيئًا وحدها
    (`FIL_NEGATION_NEVER_ELIMINATES_ALONE_NOTE`)، والقرينة الواحدة تُسقِط
    قراءةً واحدةً مُسمّاة لا قائمة (`ONE_SOUND_ELIMINATION_SUFFICES_NOTE`).
    """

    declared = _competing_reading_names(card)
    eliminated_keys = {
        comparison_key(item.excluded_reading)
        for item in qarain
        if item.function is QarinaFunction.NEGATING
        and item.kind is BayanKind.QAWL
        and item.excluded_reading is not None
    }
    return tuple(
        reading for reading in declared if comparison_key(reading) in eliminated_keys
    )


def _card_word_reference(card: Mapping[str, Any]) -> str:
    position = _require_text(card.get("الموضع"), "الموضع")
    word = _require_text(card.get("الكلمة_المدروسة"), "الكلمة_المدروسة")
    return f"{position}:{word}"


def _card_domain(card: Mapping[str, Any]) -> str:
    trial = card.get("تعريف_التجربة")
    if not isinstance(trial, dict):
        raise ManatVerificationError("تعريف_التجربة كائن")
    return _require_text(trial.get("domain"), "تعريف_التجربة.domain")


def manat_claim_scope(card: Mapping[str, Any]) -> ClaimScopeRef:
    """نطاق الدعوى مُشتَقٌّ من موضع الكلمة في البطاقة، لا مكتوبٌ فيها."""

    return ClaimScopeRef("كلمة_في_آية", _card_word_reference(card))


def manat_claim_anchor(card: Mapping[str, Any]) -> Anchor:
    """مرساة الدعوى: الكلمة في موضعها، ضمن مجال التجربة المُعلَن."""

    return Anchor(_card_word_reference(card), _card_domain(card))


def build_manat_candidate(
    card: Mapping[str, Any], binding: AuthenticatedObservationBinding
) -> EvidenceRoleCandidate:
    """يبني مُرشَّح دور الدليل من البطاقة ومن ربطٍ صادرٍ عن سلطة مصدر.

    الوحدة لا تُصدر ربطًا موثَّقًا ولا تدّعي سلطةَ مصدر؛ تستقبله وحسب.
    """

    if type(binding) is not AuthenticatedObservationBinding:
        raise ManatVerificationError(
            "تحقيق المناط يحتاج ربطَ مشاهدةٍ موثَّقًا صادرًا عن سلطة مصدر"
        )
    test_model = _require_text(card.get("النموذج_المختبر"), "النموذج_المختبر")
    content = ClaimContentManifest(
        core=ClaimCore(
            anchor=manat_claim_anchor(card),
            predicate=PredicateRef(f"مدلول_اللفظ_هو_{test_model}"),
            polarity=ClaimPolarity.AFFIRM,
            scope=manat_claim_scope(card),
        )
    )
    return EvidenceRoleCandidate(
        binding,
        ClaimCandidate(
            ClaimOccurrenceRef(_require_text(card.get("معرف_السؤال"), "معرف_السؤال")),
            content,
            CanonicalClaimContentEncoder.encode(content),
        ),
        EvidenceRoleRef(MANAT_ROLE_IDENTIFIER),
    )


def _implementation_identity(kind: BayanKind, qarain: tuple[ManatQarina, ...]) -> str:
    encoded = json.dumps(
        {
            "جنس_البيان": kind.value,
            "القرائن": [
                {
                    "المصدر_المُسمّى": item.named_source,
                    "معرف": item.identifier,
                    "وظيفة_القرينة": item.function.value,
                    "القراءة_المُقصاة": item.excluded_reading,
                }
                for item in qarain
            ],
        },
        ensure_ascii=False,
        separators=(",", ":"),
        sort_keys=True,
    ).encode("utf-8")
    return f"manat-bayan-evaluator-{hashlib.sha256(encoded).hexdigest()}"


def _bayan_evaluator(
    kind: BayanKind,
    qarain: tuple[ManatQarina, ...],
    unresolved_readings: tuple[str, ...],
    eliminated_readings: tuple[str, ...] = (),
) -> Callable[[EvidenceRoleCandidate], ApplicabilityModelResult]:
    """مُقيِّمٌ كلّيٌّ على مُدخَلات البطاقة: يُغلِق فقط إذا لم تبقَ قراءةٌ غير متعينة.

    لا `BLOCK` هنا (`NO_BLOCK_PATH_IN_THIS_LAYER_NOTE`)، ولا تُقرأ نتيجةٌ من
    البطاقة: القرائن تُثبِت أن في الطبقة ما يُنظَر فيه، وبقاءُ قراءةٍ منافسةٍ
    غير متعينة ولا مُقصاة يُبقي مدلول اللفظ غير معيَّن في نطاق الدعوى.
    """

    named = "، ".join(item.identifier for item in qarain)
    events = tuple(
        f"{kind.value}: {item.identifier} — {item.function.value}"
        + (
            f" — تُقصي ({item.excluded_reading})"
            if item.excluded_reading is not None
            else ""
        )
        + f" — {item.named_source}"
        for item in qarain
    ) + tuple(
        f"{kind.value}: القراءة المنافسة ({reading}) مُقصاةٌ بقرينةٍ مُقصِيةٍ "
        "واحدةٍ من بيان القول"
        for reading in eliminated_readings
    )

    def evaluate(candidate: EvidenceRoleCandidate) -> ApplicabilityModelResult:
        scope = candidate.claim.content.core.scope.reference
        if unresolved_readings:
            return ApplicabilityModelResult(
                status=ApplicabilityAssessmentStatus.DEFER,
                reason=(
                    f"قرائن {kind.value} ({named}) لا تُعيِّن مدلول اللفظ في "
                    f"{scope}: قراءةٌ منافسةٌ واحدة على الأقل ما زالت غير متعينة"
                ),
                trace=Trace(events),
                residuals=tuple(
                    Residual(
                        f"{kind.value}: القراءة المنافسة ({reading}) في {scope} "
                        "ما زالت غير متعينة بعد هذه القرائن"
                    )
                    for reading in unresolved_readings
                ),
            )
        return ApplicabilityModelResult(
            status=ApplicabilityAssessmentStatus.PASS,
            reason=(
                f"قرائن {kind.value} ({named}) تنطبق في {scope}: لا قراءةَ "
                "منافسةٍ غير متعينة"
                + (
                    "، والقراءات المُقصاة: " + "، ".join(eliminated_readings)
                    if eliminated_readings
                    else ""
                )
            ),
            trace=Trace(events),
        )

    return evaluate


def seal_bayan_evaluators(
    card: Mapping[str, Any], qarain: tuple[ManatQarina, ...]
) -> SealedApplicabilityEvaluatorRegistry:
    """يُسجِّل مُقيِّمًا لكل جنسِ بيانٍ حاضر، ثم يختم السجلّ.

    السجلّ المختوم وحده هو ما تقبله البوّابة؛ والمُقيِّم مربوطٌ بنطاق الدعوى
    وبدور الدليل معًا، فلا يُقرأ في نطاقٍ آخر.
    """

    models = derive_bayan_models(qarain)
    undetermined = undetermined_competing_readings(card)
    eliminated = eliminated_competing_readings(card, qarain)
    eliminated_keys = {comparison_key(reading) for reading in eliminated}
    unresolved = tuple(
        reading
        for reading in undetermined
        if comparison_key(reading) not in eliminated_keys
    )
    scope = manat_claim_scope(card)
    registry = ApplicabilityEvaluatorRegistry()
    for model in models:
        kind = BayanKind.QAWL if model.model_id == QAWL_MODEL_ID else BayanKind.FIL
        group = tuple(item for item in qarain if item.kind is kind)
        registry.register(
            evaluator_id=model.evaluator_id,
            implementation_identity=_implementation_identity(kind, group),
            role_identifier=MANAT_ROLE_IDENTIFIER,
            scope=scope,
            evaluator=_bayan_evaluator(kind, group, unresolved, eliminated),
        )
    return registry.seal(f"manat-{_card_word_reference(card)}")


def assess_manat_from_card(
    card: Mapping[str, Any], binding: AuthenticatedObservationBinding
) -> EvidenceApplicabilityAssessment:
    """يُشغِّل بوّابة G0.EA.1 على البطاقة، ويعيد ما أصدرته البوّابة كما هو.

    لا تُعدَّل الحالة الصادرة ولا تُلطَّف: `DEFER` بفضلةٍ مُسمّاة نتيجةٌ
    مقبولة، وهي المتوقَّعة على بطاقة (قُرُوء).
    """

    qarain = read_manat_qarain(card)
    registry = seal_bayan_evaluators(card, qarain)
    specification = ApplicabilityAssessmentSpecification(derive_bayan_models(qarain))
    return ApplicabilityAssessmentGate.assess(
        build_manat_candidate(card, binding), specification, registry
    )
