"""أثرُ كلِّ تدخّلٍ مشتقًّا منه، وحكمُ تبادلِ كلِّ زوجٍ مُقابَلًا بمِرصادِه.

`intervention.py` يُطبِّق كلَّ تدخّلٍ على موقعه المُثبَت وحده، فلا يسأل ولا
يُجيب عن سؤالٍ واحدٍ بقي مفتوحًا من العمل السابق: إذا وقع تدخّلان على
**الموضع الواحد**، فهل يستوي ترتيبهما؟ وهذه الوحدة تُغلق ذلك السؤال على
بياناتٍ داخلية بالكامل: تعريفات التدخّلات نفسها، بلا مدوَّنةٍ ولا حمولةٍ
خارجية غائبة.

والحدُّ الذي تحرسه الوحدة كلُّها:

```
PredictedVerdict != ObservedVerdict   ← يُسجَّل ولا يُطوى
NamedCriticalPairs != GeneralizedLaw
DerivedFootprint   != DeclaredFootprint
agreed verdict     != granted authority
```

**١. الأثر مشتقٌّ لا مكتوب.** `InterventionFootprint` لا حقلَ فيه إلا
التدخّل نفسه؛ و`read_set` و`write_set` و`shift` خصائصُ تُحسَب منه. فلا
يمكن بنيويًّا بناءُ أثرٍ يناقض تدخّله، بنفس قاعدة `readiness_rank`
و`imported_feature_vocabulary`: لا حقلَ يُكتَب فيه الحكم مباشرةً.

**٢. الإزاحة مُنمذَجة لا مطويّة.** `delete` و`insert` و`repeat` تُزيح كلَّ
ما عن يمين موضعها، فتتعارض مع كلِّ إحداثيةٍ تقع عند مبدأ الإزاحة أو بعده
وإن لم تتقاطع مجموعتا الكتابة. وهذا بالضبط نوع الخطأ الذي لا يظهر في
الحالة النموذجية، فمصفوفة المرجع تُشغَّل على تكويناتٍ مسمّاة: متجاورتان،
ومتباعدتان، وعند الصفر، وعند الإحداثية نفسها، ونازلتان، وعند الحافة
القصوى، وعند حدّ الإلحاق، وتبديلٌ غيرُ متجاورٍ يكتنف مبدأ الإزاحة،
وتبديلٌ يشارك إحداثيةً واحدة لا أكثر. وتُشغَّل كذلك على تسلسلٍ أدنى من
ذرّتين وعلى تسلسلٍ ثانٍ متمايز الذرّات، فالأحكام تتبع الإحداثيات والطول
وحدهما لا قيمَ الذرّات.

**٣. `UNDEFINED` فرعٌ قائم لا قيمةٌ في مفردة.** إذا خرجت إحداثيةُ الثاني
عن المدى بعد تطبيق الأول (وهو ما تفعله الإزاحة السالبة عند الحافة)، فليس
الترتيبان مختلفَي النتيجة، بل أحدهما غير معرَّف أصلًا. ويُفحَص هذا الفرع
قبل التقاطع وقبل الإزاحة، ولمِرصاده اختبارُ عزلٍ خاصّ يتحقّق أن التطبيق
الفعلي يفشل بـ`InterventionCoordinateError` بعينه.

**٤. الحكم لا يُسمّى قانونًا قبل تمام المطابقة.** المُنتَج المُعلَن هنا
**قائمةُ أزواجٍ مسمّاة** بحكمها وسببها (`overlap` أو `shift` أو
`out_of_range`)، لا `Confluence` معمَّمة. و`law_status()` مشتقٌّ من
المصفوفة لا مكتوبٌ فيها: فمتى خالف المتوقَّعُ المرصودَ ولو في زوجٍ واحد،
سُجِّل باسمه `PREDICTION_ORACLE_MISMATCH(τᵢ,τⱼ)` وهبطت الحالة إلى
`PARTIAL_WITH_NAMED_RESIDUALS`. ولا يُعدَّل تعريفُ الأثر بأثرٍ رجعيّ ليوافق
ما رُصِد، ولا يُسقَط الزوج المخالف من القائمة — وهي قاعدة `NoLabelLeak`
عينها مرفوعةً إلى مستوى الحكم.

**٥. نطاق النموذج مُصرَّح به لا مسكوتٌ عنه: تسلسلاتٌ متمايزة الذرّات.**
الأثر بنيويٌّ يقرأ الإحداثيات لا القيم، فإذا تساوت ذرّتان في الموضع صار
`swap` عليهما هُويّةً، فيستوي الترتيبان **مصادفةً قيميّة** لا تبادلًا
بنيويًّا. فمصفوفة المرجع تُشغَّل على ذرّاتٍ متمايزة، وحالةُ المصادفة
مسجَّلةٌ باسمها في `VALUE_COINCIDENCE_NOTE` ومُبيَّنة باختبارٍ صريح، لا
مُعالَجةٌ بتوسيع التعريف حتى يبتلعها.

ونطاق الوحدة وحدودها — تسجيلٌ صريح لا اعتذارٌ لاحق:

* لا سلطةَ نواة: لا نوع في `kernel/`، ولا `Freeze`، ولا `E0`، ولا بوّابةَ
  ولادةٍ تقرأ من هنا شيئًا. اتّفاقُ المتوقَّع والمرصود يُثبت انضباط نموذجٍ
  على تدخّلاتٍ سطحية غير لغوية، ولا يمنح إذنًا البتّة. وهذا الغيابُ
  مفحوصٌ باختبارٍ يمسح الشجرة، لا مُصرَّحٌ به هنا وحسب.
* ولا دلالةَ لغوية: التدخّلات ذرّيةٌ غير مؤوَّلة كما وُلدت في
  `intervention.py`، ولا يُقرأ من تبادلها حكمٌ على حرفٍ ولا على معنًى.
* ولا مدوَّنةَ ولا سِمةَ جديدة ولا تجربةَ طورٍ ثانٍ: هذه الوحدة لا تمسّ
  `probe_preregistration` ولا `readiness_rank` ولا بايتًا من مسار الطور
  الثاني، ولا تنتظر حمولةً خارجية.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Final

from .intervention import (
    InterventionCoordinateError,
    InterventionType,
    SurfaceAtomIntervention,
    apply_intervention,
)

NO_KERNEL_MODULE_CONSUMES_INTERVENTION_FOOTPRINT_NOTE: Final = (
    "لا شيء في المسار الحالي يعتمد على صحّة هذا الحكم: لا وحدةَ نواة ولا "
    "بوّابة ولا وحدةَ عربية أخرى تستدعي شيئًا من هذا الملف، وتصديره من "
    "alghanem.arabic.encoding إتاحةٌ لا استهلاك. فلو انقلب حكمُ زوجٍ حين "
    "تتّسع المصفوفة، لا يوجد ما بُني على افتراضٍ ضمنيّ بصحّته يلزم تتبُّعه "
    "— وهذا الغياب مفحوصٌ باختبارٍ يمسح الشجرة، لا مُصرَّحٌ به هنا وحسب"
)

DERIVED_LAW_SCOPE_NOTE: Final = (
    "المُنتَج قائمةُ أزواجٍ مسمّاة على تكويناتٍ مسمّاة، لا قانونَ تبادلٍ "
    "معمَّمًا على جبر التدخّلات كلِّه: المصفوفة تشمل الأنواع الخمسة كاملةً "
    "بتسع تكوينات إحداثيات، وأزواجًا مرتَّبةً لا ثلاثيات، وما وراءها غيرُ "
    "مقيسٍ هنا فلا يُدَّعى"
)

VALUE_COINCIDENCE_NOTE: Final = (
    "نموذج الأثر بنيويٌّ يقرأ الإحداثيات لا القيم؛ فتساوي ذرّتين في الموضع "
    "قد يجعل الترتيبين متساويَي النتيجة مصادفةً قيميّة لا تبادلًا بنيويًّا. "
    "ولذلك نطاقُ المصفوفة تسلسلاتٌ متمايزة الذرّات، والمصادفة مُبيَّنةٌ "
    "باختبارٍ صريح لا مُبتلَعةٌ بتوسيع التعريف"
)

PREDICTION_ORACLE_MISMATCH_NOTE: Final = (
    "متى خالف المتوقَّعُ المرصودَ في زوجٍ واحد سُجِّل باسمه "
    "PREDICTION_ORACLE_MISMATCH(τᵢ,τⱼ) وبقي في القائمة، ولم يُعدَّل تعريفُ "
    "الأثر بأثرٍ رجعيّ ليوافقه، ولم تُرفَع حالةُ القانون إلى مؤكَّدة"
)

IDENTICAL_PAIR_EXCLUSION_NOTE: Final = (
    "تبادلُ تدخّلٍ مع نفسه حرفيًّا صحيحٌ بلا مضمون: الترتيبان تركيبٌ واحد. "
    "فالأزواج المتطابقة مستثناةٌ من المصفوفة تصريحًا، لا محذوفةٌ لأن حكمها "
    "خالف التوقّع"
)

ORDERED_TRIPLES_ABSENCE_NOTE: Final = (
    "المقيس أزواجٌ مرتَّبة وحدها، ولا ثلاثياتٍ هنا: وحكمُ الثلاثيّ لا يُشتَقّ "
    "من أحكام أزواجه، إذ قد يتبادل كلُّ زوجٍ على حدة ولا يستوي ترتيبُ "
    "الثلاثة. فالغياب مسجَّلٌ باسمه لا مُستنتَجٌ سكوتًا، ولا يُوسَّع القياسُ "
    "إليها قبل أن يوجد مستهلكٌ يطلبها"
)

PAYLOAD_INDEPENDENCE_NOTE: Final = (
    "الأحكام تتبع الإحداثيات والطول وحدهما لا قيمَ الذرّات: فتشغيلُ المصفوفة "
    "على تسلسلٍ ثانٍ متمايز الذرّات يعطي الأحكام نفسها بايتًا ببايت، وهذا "
    "مفحوصٌ باختبارٍ لا مُصرَّحٌ به وحسب"
)


class InterventionFootprintError(ValueError):
    """رُفض حسابُ أثرٍ أو حكمٍ خارج نطاقه؛ لا يُحمَل على أقرب حالةٍ مقبولة."""


class CommutationVerdict(Enum):
    """حكم تبادل زوجٍ من التدخّلات على موضعٍ واحد؛ ثلاث قيم لا اثنتان."""

    COMMUTES = "COMMUTES"
    CONFLICTS = "CONFLICTS"
    UNDEFINED = "UNDEFINED"


class ConflictReason(Enum):
    """سبب امتناع التبادل، مسمًّى لا موصوفًا نثرًا."""

    OVERLAP = "overlap"
    SHIFT = "shift"
    OUT_OF_RANGE = "out_of_range"


class PredictionOracleAgreement(Enum):
    """موقف الحكم المتوقَّع من الحكم المرصود؛ لا ثالثَ بينهما."""

    MATCH = "MATCH"
    PREDICTION_ORACLE_MISMATCH = "PREDICTION_ORACLE_MISMATCH"


class DerivedLawStatus(Enum):
    """حالة القانون، مشتقّةً من المصفوفة لا مكتوبةً فيها."""

    DERIVED_LAW_CONFIRMED = "DERIVED_LAW_CONFIRMED"
    PARTIAL_WITH_NAMED_RESIDUALS = "PARTIAL_WITH_NAMED_RESIDUALS"


if len(CommutationVerdict) != 3:  # pragma: no cover - guard
    raise RuntimeError("the commutation verdict vocabulary is three-valued")
if len(ConflictReason) != 3:  # pragma: no cover - guard
    raise RuntimeError("exactly three conflict reasons are declared here")


@dataclass(frozen=True)
class CoordinateShift:
    """إزاحةُ الإحداثيات الواقعة عند مبدأٍ أو بعده؛ صفرٌ يعني لا مبدأ."""

    delta: int
    origin: int | None

    def __post_init__(self) -> None:
        if self.delta == 0 and self.origin is not None:
            raise InterventionFootprintError("a zero shift declares no origin")
        if self.delta != 0 and self.origin is None:
            raise InterventionFootprintError("a non-zero shift requires an origin")

    def moves(self, coordinate: int) -> bool:
        return self.origin is not None and coordinate >= self.origin


@dataclass(frozen=True)
class InterventionFootprint:
    """أثر تدخّلٍ واحد: قراءةً وكتابةً وإزاحة، مشتقًّا منه لا مكتوبًا معه."""

    intervention: SurfaceAtomIntervention

    @property
    def intervention_type(self) -> InterventionType:
        return self.intervention.intervention_type

    @property
    def read_set(self) -> tuple[int, ...]:
        """الإحداثيات التي تعتمد النتيجةُ على **قيمها**."""
        if self.intervention_type == "repeat":
            return (self.intervention.coordinates[0],)
        if self.intervention_type == "swap":
            return tuple(sorted(self.intervention.coordinates))
        return ()

    @property
    def write_set(self) -> tuple[int, ...]:
        """الإحداثيات التي يُغيِّر التدخّلُ محتواها أو وجودها عندها."""
        return tuple(sorted(set(self.intervention.coordinates)))

    @property
    def shift(self) -> CoordinateShift:
        coordinate = self.intervention.coordinates[0]
        if self.intervention_type == "delete":
            return CoordinateShift(-1, coordinate + 1)
        if self.intervention_type == "repeat":
            return CoordinateShift(1, coordinate + 1)
        if self.intervention_type == "insert":
            return CoordinateShift(1, coordinate)
        return CoordinateShift(0, None)

    @property
    def touched(self) -> tuple[int, ...]:
        return tuple(sorted(set(self.read_set) | set(self.write_set)))

    @property
    def label(self) -> str:
        coordinates = ",".join(str(index) for index in self.intervention.coordinates)
        return f"{self.intervention_type}@{coordinates}"


@dataclass(frozen=True)
class CommutationAssessment:
    """حكمٌ متوقَّع على زوجٍ مرتَّب، مربوطٌ بطول التسلسل الذي حُسب عليه."""

    left: SurfaceAtomIntervention
    right: SurfaceAtomIntervention
    atom_count: int
    verdict: CommutationVerdict
    reason: ConflictReason | None

    def __post_init__(self) -> None:
        if self.verdict is CommutationVerdict.COMMUTES and self.reason is not None:
            raise InterventionFootprintError("a commuting pair declares no reason")
        if self.verdict is CommutationVerdict.CONFLICTS and self.reason not in {
            ConflictReason.OVERLAP,
            ConflictReason.SHIFT,
        }:
            raise InterventionFootprintError(
                "a conflicting pair declares an overlap or shift reason"
            )
        if (
            self.verdict is CommutationVerdict.UNDEFINED
            and self.reason is not ConflictReason.OUT_OF_RANGE
        ):
            raise InterventionFootprintError(
                "an undefined pair declares an out-of-range reason"
            )

    @property
    def pair_label(self) -> str:
        return (
            f"{InterventionFootprint(self.left).label}"
            f" × {InterventionFootprint(self.right).label}"
        )


@dataclass(frozen=True)
class CommutationCheck:
    """مقابلةُ حكمٍ متوقَّع بحكمٍ مرصود على تكوينٍ مسمًّى."""

    configuration: str
    assessment: CommutationAssessment
    observed: CommutationVerdict

    def __post_init__(self) -> None:
        if not isinstance(self.configuration, str) or not self.configuration:
            raise InterventionFootprintError(
                "a commutation check names its configuration"
            )

    @property
    def agreement(self) -> PredictionOracleAgreement:
        if self.assessment.verdict is self.observed:
            return PredictionOracleAgreement.MATCH
        return PredictionOracleAgreement.PREDICTION_ORACLE_MISMATCH

    @property
    def label(self) -> str:
        base = f"{self.assessment.pair_label} [{self.configuration}]"
        if self.agreement is PredictionOracleAgreement.MATCH:
            return base
        return f"PREDICTION_ORACLE_MISMATCH({base})"


def footprint(intervention: SurfaceAtomIntervention) -> InterventionFootprint:
    return InterventionFootprint(intervention)


def is_applicable(intervention: SurfaceAtomIntervention, atom_count: int) -> bool:
    """هل إحداثيات التدخّل داخل المدى على تسلسلٍ بهذا الطول؟"""
    if atom_count < 0:
        raise InterventionFootprintError("an atom count is never negative")
    upper_bound = (
        atom_count if intervention.intervention_type == "insert" else atom_count - 1
    )
    return all(0 <= index <= upper_bound for index in intervention.coordinates)


def predict_commutation(
    left: SurfaceAtomIntervention,
    right: SurfaceAtomIntervention,
    atom_count: int,
) -> CommutationAssessment:
    """الحكم المتوقَّع من الأثرين وحدهما، بلا تطبيقٍ ولا نظرٍ في القيم."""
    if not is_applicable(left, atom_count) or not is_applicable(right, atom_count):
        raise InterventionFootprintError(
            "both interventions must apply to the declared atom count"
        )
    left_footprint = footprint(left)
    right_footprint = footprint(right)
    if _order_is_undefined(left_footprint, right_footprint, atom_count) or (
        _order_is_undefined(right_footprint, left_footprint, atom_count)
    ):
        return CommutationAssessment(
            left,
            right,
            atom_count,
            CommutationVerdict.UNDEFINED,
            ConflictReason.OUT_OF_RANGE,
        )
    if set(left_footprint.touched) & set(right_footprint.touched):
        return CommutationAssessment(
            left,
            right,
            atom_count,
            CommutationVerdict.CONFLICTS,
            ConflictReason.OVERLAP,
        )
    if any(
        left_footprint.shift.moves(coordinate) for coordinate in right_footprint.touched
    ) or any(
        right_footprint.shift.moves(coordinate) for coordinate in left_footprint.touched
    ):
        return CommutationAssessment(
            left, right, atom_count, CommutationVerdict.CONFLICTS, ConflictReason.SHIFT
        )
    return CommutationAssessment(
        left, right, atom_count, CommutationVerdict.COMMUTES, None
    )


def observe_commutation(
    left: SurfaceAtomIntervention,
    right: SurfaceAtomIntervention,
    source_atoms: tuple[str, ...],
) -> CommutationVerdict:
    """الحكم المرصود بتطبيق الترتيبين فعلًا ومقارنة ذرّاتهما."""
    first = _compose(left, right, source_atoms)
    second = _compose(right, left, source_atoms)
    if first is None or second is None:
        return CommutationVerdict.UNDEFINED
    if first == second:
        return CommutationVerdict.COMMUTES
    return CommutationVerdict.CONFLICTS


def check_commutation(
    left: SurfaceAtomIntervention,
    right: SurfaceAtomIntervention,
    source_atoms: tuple[str, ...],
    configuration: str,
) -> CommutationCheck:
    assessment = predict_commutation(left, right, len(source_atoms))
    observed = observe_commutation(left, right, source_atoms)
    return CommutationCheck(configuration, assessment, observed)


def _compose(
    first: SurfaceAtomIntervention,
    second: SurfaceAtomIntervention,
    source_atoms: tuple[str, ...],
) -> tuple[str, ...] | None:
    try:
        intermediate = apply_intervention(first, source_atoms)
        return apply_intervention(second, intermediate)
    except InterventionCoordinateError:
        return None


def _order_is_undefined(
    first: InterventionFootprint, second: InterventionFootprint, atom_count: int
) -> bool:
    return not is_applicable(second.intervention, atom_count + first.shift.delta)


REFERENCE_ATOMS: Final[tuple[str, ...]] = (
    "\u0623",
    "\u0628",
    "\u062c",
    "\u062f",
    "\u0647",
    "\u0648",
)

REFERENCE_SOURCE_ID: Final = "reference-occurrence"
REFERENCE_OCCURRENCE_ID: Final = "0"

ALTERNATE_ATOMS: Final[tuple[str, ...]] = (
    "\u0642",
    "\u0643",
    "\u0644",
    "\u0645",
    "\u0646",
    "\u0649",
)

MINIMAL_ATOMS: Final[tuple[str, ...]] = ("\u0642", "\u0643")

LEFT_PAYLOAD: Final = "\u0632"
RIGHT_PAYLOAD: Final = "\u0637"

INTERVENTION_TYPES: Final[tuple[InterventionType, ...]] = (
    "delete",
    "substitute",
    "repeat",
    "swap",
    "insert",
)

COORDINATE_CONFIGURATIONS: Final[tuple[tuple[str, int, int, int], ...]] = (
    ("adjacent", 1, 2, 1),
    ("distant", 1, 4, 1),
    ("at_zero", 0, 3, 1),
    ("same_coordinate", 2, 2, 1),
    ("descending", 4, 1, 1),
    ("upper_edge", 4, 5, 1),
    ("append_edge", 5, 6, 1),
    ("straddling_swap", 2, 1, 3),
    ("swap_shares_one_coordinate", 1, 1, 2),
)


def _build(
    intervention_type: InterventionType,
    anchor: int,
    payload: str,
    atom_count: int,
    swap_span: int,
) -> SurfaceAtomIntervention | None:
    coordinates: tuple[int, ...]
    if intervention_type == "swap":
        if anchor + swap_span <= atom_count - 1:
            coordinates = (anchor, anchor + swap_span)
        elif anchor - swap_span >= 0 and anchor <= atom_count - 1:
            coordinates = (anchor - swap_span, anchor)
        else:
            return None
    else:
        coordinates = (anchor,)
    candidate = SurfaceAtomIntervention(
        REFERENCE_SOURCE_ID,
        REFERENCE_OCCURRENCE_ID,
        intervention_type,
        coordinates,
        payload if intervention_type in {"substitute", "insert"} else None,
    )
    if not is_applicable(candidate, atom_count):
        return None
    return candidate


def reference_matrix(
    source_atoms: tuple[str, ...] = REFERENCE_ATOMS,
) -> tuple[CommutationCheck, ...]:
    """المصفوفة الكاملة: خمسةُ أنواعٍ × خمسة × تكويناتُ الإحداثيات، بترتيبٍ حتميّ."""
    atom_count = len(source_atoms)
    checks: list[CommutationCheck] = []
    for (
        configuration,
        left_anchor,
        right_anchor,
        swap_span,
    ) in COORDINATE_CONFIGURATIONS:
        for left_type in INTERVENTION_TYPES:
            for right_type in INTERVENTION_TYPES:
                left = _build(
                    left_type, left_anchor, LEFT_PAYLOAD, atom_count, swap_span
                )
                right = _build(
                    right_type, right_anchor, RIGHT_PAYLOAD, atom_count, swap_span
                )
                if left is None or right is None or left == right:
                    continue
                checks.append(
                    check_commutation(left, right, source_atoms, configuration)
                )
    return tuple(checks)


def _select(
    checks: tuple[CommutationCheck, ...], verdict: CommutationVerdict
) -> tuple[str, ...]:
    return tuple(check.label for check in checks if check.assessment.verdict is verdict)


def commuting_pairs(checks: tuple[CommutationCheck, ...]) -> tuple[str, ...]:
    return _select(checks, CommutationVerdict.COMMUTES)


def critical_pairs(checks: tuple[CommutationCheck, ...]) -> tuple[str, ...]:
    return tuple(
        f"{check.label} :: {check.assessment.reason.value}"
        for check in checks
        if check.assessment.verdict is CommutationVerdict.CONFLICTS
        and check.assessment.reason is not None
    )


def undefined_pairs(checks: tuple[CommutationCheck, ...]) -> tuple[str, ...]:
    return _select(checks, CommutationVerdict.UNDEFINED)


def mismatched_pairs(checks: tuple[CommutationCheck, ...]) -> tuple[str, ...]:
    return tuple(
        check.label
        for check in checks
        if check.agreement is PredictionOracleAgreement.PREDICTION_ORACLE_MISMATCH
    )


def law_status(checks: tuple[CommutationCheck, ...]) -> DerivedLawStatus:
    """الحالة مشتقّةٌ من المصفوفة: مخالفةٌ واحدة تكفي لإسقاط التأكيد."""
    if not checks:
        raise InterventionFootprintError("an empty matrix confirms no law")
    if mismatched_pairs(checks):
        return DerivedLawStatus.PARTIAL_WITH_NAMED_RESIDUALS
    return DerivedLawStatus.DERIVED_LAW_CONFIRMED


__all__ = [
    "ALTERNATE_ATOMS",
    "COORDINATE_CONFIGURATIONS",
    "DERIVED_LAW_SCOPE_NOTE",
    "IDENTICAL_PAIR_EXCLUSION_NOTE",
    "INTERVENTION_TYPES",
    "MINIMAL_ATOMS",
    "NO_KERNEL_MODULE_CONSUMES_INTERVENTION_FOOTPRINT_NOTE",
    "ORDERED_TRIPLES_ABSENCE_NOTE",
    "PAYLOAD_INDEPENDENCE_NOTE",
    "PREDICTION_ORACLE_MISMATCH_NOTE",
    "REFERENCE_ATOMS",
    "VALUE_COINCIDENCE_NOTE",
    "CommutationAssessment",
    "CommutationCheck",
    "CommutationVerdict",
    "ConflictReason",
    "CoordinateShift",
    "DerivedLawStatus",
    "InterventionFootprint",
    "InterventionFootprintError",
    "PredictionOracleAgreement",
    "check_commutation",
    "commuting_pairs",
    "critical_pairs",
    "footprint",
    "is_applicable",
    "law_status",
    "mismatched_pairs",
    "observe_commutation",
    "predict_commutation",
    "reference_matrix",
    "undefined_pairs",
]
