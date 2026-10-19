"""G0.FLT-0: معايرةٌ تُسمّي عيوبَ الاختبار قبل أن يُنسَب حكمُه إلى الفرضية.

هذه الوحدةُ **لا تُصلح** النصَّ المُجمَّد ولا التسجيلَ القبليّ ولا المُستخرِجات،
ولا تُعيد تشغيلَ الصور الخمس بمعيارٍ جديد. وظيفتُها واحدة: أن تشتقّ — لا أن
تدّعي — أنّ التشغيلَ الأوّل لم يكن اختبارًا صالحًا للفرضية المطلوبة، ثمّ تحجُب
حكمَه عن أن يُقرأ حكمًا عليها.

**والانحرافُ الحرفيّ قاتلٌ للتسجيل لا حاشيةٌ عليه**
(`ADivergentFrozenTextIsAnInvalidPreregistration`): النصُّ المطلوب يجعل شرطَ
النجاح علاقةَ ترتيبٍ صريحةً بين `StructureMatch` و`BestWeakerReconstruction`،
والنصُّ المودَع في هذه الشجرة لا يحمل في ذلك الموضع علاقةً أصلًا. والوحدةُ
المُجمَّدة تُعلن في الوقت نفسه أنّ الترميزَ جزءٌ من النصّ. فبصمةُ
`HYPOTHESIS_DIGEST` تُثبت نصًّا آخر، ولو كان الفرقُ خطأَ نقلٍ لا قصدًا:

    H_frozen != H_requested  =>  INVALID_PREREGISTRATION

**والحجبُ ليس محوًا**: القراءةُ الأولى تبقى كما خرجت، وتُحمَل هنا بتمامها،
لأنّ إخفاءَ نتيجةٍ رآها صاحبُها هو عينُ ما يمنعه قانونُ عدم القفز. المحجوبُ
نسبتُها إلى الفرضية، لا وجودُها.

**وظرفُ القدرة يُعلَن قبل أن يُسأل عنه** (`AnUnreachableVerdictIsDeclaredNotDiscovered`):
هذا التسجيلُ لا يستطيع بلوغَ `SUPPORTED` بالبناء، لأنّ أسماءَ سلّمه الأربعة
كلَّها واردةٌ في النصّ المُجمَّد، فلا زوجَ فيه يصلح شاهدًا مؤجَّلًا. فاختبارٌ
يستطيع أن يُفنِّد ولا يستطيع أن يدعم اختبارُ تفنيدٍ، ولا يُسمّى اختبارًا
متوازنًا.

**والمقارنةُ الجارية ليست بعدُ نقلَ مقياس** (`BooleanAgreementIsNotScaleTransport`):
ما جرى هو مقارنةُ محمولٍ منطقيٍّ في طبقةٍ بمحمولٍ منطقيٍّ في أخرى على الصورة
نفسها، لا اختبارُ `S ∘ K_n ≅ K_m ∘ S` بتحويلٍ مستقلٍّ مُعرَّفٍ خارج المُستخرِجَين.
ولذلك كشفُ أنّ حقولًا منها صادقةٌ بالبناء تشخيصُ ضعفِ التوقيع، لا تفنيدٌ
للفراكتالية.

**وحفظُ الهويةِ هنا مُعلَنٌ لا مُتحقَّقٌ منه** (`DeclaredInvariant != VerifiedInvariant`):
حقلُ `Identity` بولٌ يخرج من مُرمِّز، ولا يمرّ ببوّابة التحقّق من الثوابت في
النواة. والواجبُ في التجربة القادمة أن يكون مُتحقَّقًا أو أن يجعل الزوجَ
قاصرًا، لا أن يُعَدّ إصابةً.

**ولا تُصلَح تجربةٌ ثمّ تُسمّى استباقيّة**
(`ARepairedRunOnSeenCasesIsNotProspective`): الصورُ الخمسُ والأزواجُ الثلاثةُ
قد قُرِئت، فلا تصلح شاهدًا قبليًّا بعد اليوم مهما أُحكِم المعيار. وشروطُ
`G0.FLT-1` مُعلَنةٌ هنا بالاسم، **غيرَ مُنفَّذةٍ في هذه الوحدة**.
"""

from __future__ import annotations

import importlib.util
from dataclasses import dataclass
from enum import Enum
from typing import Final

from . import fractal_transition_readout as readout_module
from .fractal_transition_hypothesis import (
    HYPOTHESIS_DIGEST,
    HYPOTHESIS_TEXT,
    FractalVerdict,
    hypothesis_digest,
)
from .fractal_transition_preregistration import (
    DECLARED_PAIRS,
    FROZEN_CASES,
    layer_named,
)
from .fractal_transition_readout import (
    FractalTransitionReadoutGate,
    HypothesisReadout,
    seal_preregistration,
)

__all__ = [
    "A_DIVERGENT_FROZEN_TEXT_IS_AN_INVALID_PREREGISTRATION_NOTE",
    "A_REPAIRED_RUN_ON_SEEN_CASES_IS_NOT_PROSPECTIVE_NOTE",
    "AN_UNREACHABLE_VERDICT_IS_DECLARED_NOT_DISCOVERED_NOTE",
    "BOOLEAN_AGREEMENT_IS_NOT_SCALE_TRANSPORT_NOTE",
    "CALIBRATION_NAMED_RESIDUALS",
    "CalibrationReading",
    "CalibrationStanding",
    "CapabilityEnvelope",
    "CapabilityLimit",
    "DECLARED_INVARIANT_IS_NOT_A_VERIFIED_ONE_NOTE",
    "FLT1_PREREQUISITES",
    "FractalCalibrationError",
    "G0_FLT_1_IS_NOT_ISSUED_HERE_NOTE",
    "REQUESTED_SUCCESS_CONDITION",
    "RequestedNotationSite",
    "VerbatimDivergence",
    "derive_capability_envelope",
    "derive_verbatim_divergences",
    "read_calibration",
]


class FractalCalibrationError(ValueError):
    """رفضٌ مُسمّى في وحدة المعايرة؛ لا تصحيحَ صامتًا ولا تخطّي."""


class CalibrationStanding(Enum):
    """منزلةُ التشغيل الأوّل؛ ثنائيّةٌ لأن الانحرافَ الحرفيّ إمّا وقع أو لم يقع."""

    INVALID_PREREGISTRATION = "تسجيلٌ_قبليٌّ_باطلٌ_لانحراف_نصّه_عن_المطلوب"
    VERBATIM_FIDELITY_HOLDS = "النصُّ_المُجمَّد_مطابقٌ_للمطلوب_في_المواضع_المفحوصة"


@dataclass(frozen=True, slots=True)
class RequestedNotationSite:
    """موضعٌ من النصّ المطلوب، بطرفيه والعلاقة الواجبة بينهما."""

    site_id: str
    left_operand: str
    required_relation: str
    right_operand: str
    what_it_decides: str

    def __post_init__(self) -> None:
        for value, name in (
            (self.site_id, "مُعرِّفُ الموضع"),
            (self.left_operand, "الطرفُ الأيسر"),
            (self.required_relation, "العلاقةُ الواجبة"),
            (self.right_operand, "الطرفُ الأيمن"),
            (self.what_it_decides, "ما يقرّره الموضع"),
        ):
            if not isinstance(value, str) or not value.strip():
                raise FractalCalibrationError(
                    f"{name} نصٌّ غيرُ فارغ؛ وموضعٌ بلا طرفٍ لا يُفحَص"
                )


REQUESTED_SUCCESS_CONDITION: Final[RequestedNotationSite] = RequestedNotationSite(
    site_id="success-condition-relation",
    left_operand=r"\operatorname{StructureMatch}",
    required_relation=">",
    right_operand=r"\operatorname{BestWeakerReconstruction}",
    what_it_decides=(
        "شرطُ النجاح نفسُه: أن تسبق إصابةُ البنية أفضلَ إعادةِ بناءٍ أضعف "
        "سبقًا صريحًا، لا أن تُقارَن بها بلا علاقةٍ منصوصة"
    ),
)


@dataclass(frozen=True, slots=True)
class VerbatimDivergence:
    """انحرافٌ مُشتَقٌّ بين النصّ المُجمَّد والنصّ المطلوب في موضعٍ مُسمّى."""

    site_id: str
    required_relation: str
    what_the_frozen_text_carries: str
    why_it_is_fatal: str


def _segment_between(text: str, opening: str, closing: str) -> str | None:
    start = text.find(opening)
    if start < 0:
        return None
    end = text.find(closing, start + len(opening))
    if end < 0:
        return None
    return text[start + len(opening) : end]


def derive_verbatim_divergences() -> tuple[VerbatimDivergence, ...]:
    """اشتقّ الانحرافَ من النصّ المودَع نفسِه؛ ولا تُصرِّح به تصريحًا منقولًا."""

    divergences: list[VerbatimDivergence] = []
    site = REQUESTED_SUCCESS_CONDITION
    segment = _segment_between(HYPOTHESIS_TEXT, site.left_operand, site.right_operand)
    if segment is None:
        raise FractalCalibrationError(
            "طرفا شرطِ النجاح غيرُ موجودين في النصّ المودَع، فلا يُفحَص ما "
            "بينهما؛ وغيابُ الطرفين انحرافٌ أشدُّ لا يُبتلَع صامتًا"
        )
    if site.required_relation not in segment:
        divergences.append(
            VerbatimDivergence(
                site_id=site.site_id,
                required_relation=site.required_relation,
                what_the_frozen_text_carries=segment.strip(),
                why_it_is_fatal=(
                    "الموضعُ يقرّر شرطَ النجاح، والنصُّ المودَع لا يحمل فيه "
                    "علاقةَ ترتيبٍ أصلًا؛ فالبصمةُ تُثبت نصًّا غيرَ المطلوب، "
                    "والوحدةُ تُعلن في الوقت نفسه أنّ الترميزَ جزءٌ من النصّ"
                ),
            )
        )
    return tuple(divergences)


@dataclass(frozen=True, slots=True)
class CapabilityLimit:
    """حدٌّ مُشتَقٌّ من بنية التسجيل، بما يمنعه وبما يرفعه."""

    limit_id: str
    holds: bool
    what_it_prevents: str
    how_it_was_derived: str
    what_would_lift_it: str


@dataclass(frozen=True, slots=True)
class CapabilityEnvelope:
    """ما يستطيعه هذا التسجيل وما لا يستطيعه، مُشتقًّا لا موصوفًا."""

    reachable_verdicts: tuple[FractalVerdict, ...]
    unreachable_verdicts: tuple[FractalVerdict, ...]
    limits: tuple[CapabilityLimit, ...]
    holdout_pair_count: int
    holdout_pairs_required_for_support: int

    @property
    def is_a_refutation_only_instrument(self) -> bool:
        """أداةُ تفنيدٍ فقط متى امتنع `SUPPORTED` بالبناء لا بالنتيجة."""

        return FractalVerdict.SUPPORTED in self.unreachable_verdicts


HOLDOUT_PAIRS_REQUIRED_FOR_SUPPORT: Final[int] = 3


def _holdout_pair_count() -> int:
    count = 0
    for pair in DECLARED_PAIRS:
        lower = layer_named(pair.lower_jurisdiction)
        upper = layer_named(pair.upper_jurisdiction)
        if not lower.is_named_in_the_frozen_ladder and (
            not upper.is_named_in_the_frozen_ladder
        ):
            count += 1
    return count


def _an_independent_scale_transport_is_absent() -> bool:
    try:
        return importlib.util.find_spec("alghanem.kernel.scale_transport") is None
    except ModuleNotFoundError:
        return True


def _identity_is_read_from_an_encoder_not_a_verification_gate() -> bool:
    return "InvariantVerificationGate" not in vars(readout_module)


def derive_capability_envelope() -> CapabilityEnvelope:
    """اشتقّ ظرفَ القدرة من التسجيل والشيفرة، لا من وصفٍ مكتوبٍ بجانبهما."""

    holdouts = _holdout_pair_count()
    support_is_reachable = holdouts >= HOLDOUT_PAIRS_REQUIRED_FOR_SUPPORT
    limits = (
        CapabilityLimit(
            limit_id="no-holdout-pair-under-the-frozen-ladder",
            holds=not support_is_reachable,
            what_it_prevents=(
                f"إصدارَ `SUPPORTED`؛ إذ يلزمه "
                f"{HOLDOUT_PAIRS_REQUIRED_FOR_SUPPORT} من الأزواج المؤجَّلة "
                f"والموجودُ منها {holdouts}"
            ),
            how_it_was_derived=(
                "بعدّ الأزواج المُعلَنة التي لا يَرِد اسمُ أيٍّ من طبقتيها في "
                "النصّ المُجمَّد؛ وأسماءُ السلّم الأربعة كلُّها واردةٌ فيه"
            ),
            what_would_lift_it=(
                "مقاييسُ لم تُستخدَم في صياغة `K`، تُعلَن قبل تشغيلها، ولا "
                "يَرِد اسمُها في النصّ المُجمَّد"
            ),
        ),
        CapabilityLimit(
            limit_id="boolean-agreement-is-not-scale-transport",
            holds=_an_independent_scale_transport_is_absent(),
            what_it_prevents=(
                "قراءةَ النتيجة اختبارًا لـ`S ∘ K_n ≅ K_m ∘ S`؛ فالمقيسُ توافقُ "
                "محمولين منطقيَّين على الصورة نفسها بين مُرمِّزَين"
            ),
            how_it_was_derived=(
                "بالبحث عن عقدِ نقلِ مقياسٍ مستقلٍّ في النواة "
                "(`alghanem.kernel.scale_transport`)؛ ولا وجودَ له"
            ),
            what_would_lift_it=(
                "عقدُ `S` مستقلٌّ مُعرَّفٌ خارج المُستخرِجَين، يُبرهَن تبديلُه "
                "مع الانتقال بدل أن يُفترَض"
            ),
        ),
        CapabilityLimit(
            limit_id="identity-is-declared-not-verified",
            holds=_identity_is_read_from_an_encoder_not_a_verification_gate(),
            what_it_prevents=(
                "عَدَّ حقلِ `Identity` شاهدًا على حفظ الهوية؛ فهو بولٌ يخرج من "
                "مُرمِّزٍ لا حكمٌ من بوّابة تحقّقٍ من الثوابت"
            ),
            how_it_was_derived=(
                "بفحص أسماء وحدة القراءة: لا ذكرَ لـ`InvariantVerificationGate` " "فيها"
            ),
            what_would_lift_it=(
                "أن يمرّ `I` ببوّابة التحقّق فيكون `VERIFIED`، أو أن يجعل "
                "الزوجَ `UNDERPOWERED` متى تعذّر التحقّق"
            ),
        ),
        CapabilityLimit(
            limit_id="frozen-cases-and-pairs-are-now-seen",
            holds=True,
            what_it_prevents=(
                f"إعادةَ استعمال الصور الـ{len(FROZEN_CASES)} والأزواج "
                f"الـ{len(DECLARED_PAIRS)} شاهدًا قبليًّا؛ نتائجُها معلومةٌ الآن"
            ),
            how_it_was_derived=(
                "من التاريخ نفسِه: القراءةُ الأولى جرت على هذه الصور بعينها "
                "وأُودِعت نتيجتُها"
            ),
            what_would_lift_it=(
                "صورٌ وأزواجٌ لم تُقرأ في G0.FLT-0، تُجمَّد في تسجيلٍ جديدٍ " "مستقلٍّ ببصمته"
            ),
        ),
    )
    reachable = tuple(
        verdict
        for verdict in FractalVerdict
        if verdict is not FractalVerdict.SUPPORTED or support_is_reachable
    )
    unreachable = tuple(
        verdict for verdict in FractalVerdict if verdict not in reachable
    )
    return CapabilityEnvelope(
        reachable_verdicts=reachable,
        unreachable_verdicts=unreachable,
        limits=limits,
        holdout_pair_count=holdouts,
        holdout_pairs_required_for_support=HOLDOUT_PAIRS_REQUIRED_FOR_SUPPORT,
    )


@dataclass(frozen=True, slots=True)
class CalibrationReading:
    """قراءةُ المعايرة: منزلةُ التشغيل، وانحرافاتُه، وظرفُه، ونتيجتُه محجوبةَ النسبة."""

    standing: CalibrationStanding
    divergences: tuple[VerbatimDivergence, ...]
    envelope: CapabilityEnvelope
    observed_readout: HypothesisReadout
    degenerate_fields: tuple[str, ...]
    withheld_judgment_reason: str

    @property
    def observed_verdict_is_a_hypothesis_judgment(self) -> bool:
        """هل تُنسَب النتيجةُ المرصودة إلى الفرضية؟ لا، ما دام التسجيلُ باطلًا."""

        return self.standing is CalibrationStanding.VERBATIM_FIDELITY_HOLDS


def read_calibration() -> CalibrationReading:
    """اقرأ التشغيلَ الأوّل معايرةً؛ ولا تُصدِر عنه حكمًا على الفرضية."""

    divergences = derive_verbatim_divergences()
    standing = (
        CalibrationStanding.INVALID_PREREGISTRATION
        if divergences
        else CalibrationStanding.VERBATIM_FIDELITY_HOLDS
    )
    observed = FractalTransitionReadoutGate.read_hypothesis(seal_preregistration())
    degenerate: list[str] = []
    for pair in observed.pairs:
        for field in pair.non_discriminating_fields:
            if field not in degenerate:
                degenerate.append(field)
    return CalibrationReading(
        standing=standing,
        divergences=divergences,
        envelope=derive_capability_envelope(),
        observed_readout=observed,
        degenerate_fields=tuple(degenerate),
        withheld_judgment_reason=(
            "النتيجةُ المرصودة "
            f"«{observed.verdict.value}» قراءةٌ صحيحةٌ لهذه الشيفرة على هذه "
            "الصور، ولا تُنسَب إلى الفرضية المطلوبة: النصُّ المُبصَّم يخالفها "
            "في موضعٍ يقرّر شرطَ النجاح، والمقيسُ توافقُ محمولاتٍ لا نقلُ "
            "مقياس، وحفظُ الهوية فيه مُعلَنٌ لا مُتحقَّقٌ منه"
        ),
    )


FLT1_PREREQUISITES: Final[tuple[str, ...]] = (
    "نصٌّ حرفيٌّ جديدٌ يُبصَّم بعد مقابلته موضعًا بموضعٍ بالنصّ الوارد، وفيه "
    "علاقةُ الترتيب في شرط النجاح صريحةً",
    "عقدُ `S` مستقلٌّ خارج المُستخرِجَين، يُختبَر تبديلُه مع الانتقال لا يُفترَض",
    "مقاييسُ لم تُستعمَل في صياغة `K` ولا يَرِد اسمُها في النصّ المُجمَّد، "
    "لتكون أزواجًا مؤجَّلةً حقيقيّةً يصير `SUPPORTED` عندها ممكنًا",
    "توقيعٌ مُميِّزٌ: حقلٌ يستطيع أن يقرأ كذبًا على مُدخَلٍ حقيقيّ، وإلّا "
    "أُعلِن غيرَ مُميِّزٍ قبل التشغيل لا بعده",
    "`Identity` مُتحقَّقٌ منه ببوّابة الثوابت، أو الزوجُ `UNDERPOWERED`",
    "صورٌ وأزواجٌ لم تُقرأ في G0.FLT-0",
)

A_DIVERGENT_FROZEN_TEXT_IS_AN_INVALID_PREREGISTRATION_NOTE: Final[str] = (
    "ADivergentFrozenTextIsAnInvalidPreregistration: بصمةٌ على نصٍّ يخالف "
    "النصَّ الوارد في موضعٍ يقرّر شرطَ النجاح تُثبت نصًّا آخر؛ فالقراءةُ "
    "معايرةٌ لا حكمٌ على الفرضية، ولو كان الفرقُ خطأَ نقل"
)

AN_UNREACHABLE_VERDICT_IS_DECLARED_NOT_DISCOVERED_NOTE: Final[str] = (
    "AnUnreachableVerdictIsDeclaredNotDiscovered: امتناعُ `SUPPORTED` بالبناء "
    "يُعلَن مع التسجيل لا بعد النتيجة؛ واختبارٌ يُفنِّد ولا يدعم أداةُ تفنيدٍ "
    "لا اختبارٌ متوازن"
)

BOOLEAN_AGREEMENT_IS_NOT_SCALE_TRANSPORT_NOTE: Final[str] = (
    "BooleanAgreementIsNotScaleTransport: توافقُ محمولين منطقيَّين على صورةٍ "
    "واحدةٍ بين مُرمِّزَين ليس اختبارًا لـ`S ∘ K_n ≅ K_m ∘ S`؛ وتدهورُ "
    "التوقيع تشخيصٌ للأداة لا تفنيدٌ للدعوى"
)

DECLARED_INVARIANT_IS_NOT_A_VERIFIED_ONE_NOTE: Final[str] = (
    "DeclaredInvariantIsNotAVerifiedOne: `Identity` المقروءُ من مُرمِّزٍ "
    "إعلانٌ؛ والشاهدُ على حفظ الهوية حكمُ بوّابة تحقّقٍ، وإلّا فالزوجُ قاصر"
)

A_REPAIRED_RUN_ON_SEEN_CASES_IS_NOT_PROSPECTIVE_NOTE: Final[str] = (
    "ARepairedRunOnSeenCasesIsNotProspective: إصلاحُ المعيار ثمّ إعادةُ "
    "تشغيله على الصور المقروءة نفسِها لا يُنتج شاهدًا استباقيًّا؛ و`G0.FLT-1` "
    "يلزمه نصٌّ جديدٌ وأزواجٌ لم تُقرأ"
)

G0_FLT_1_IS_NOT_ISSUED_HERE_NOTE: Final[str] = (
    "G0FLT1IsNotIssuedHere: شروطُ التجربة القادمة مُعلَنةٌ بالاسم في "
    "`FLT1_PREREQUISITES`، ولا تُنفَّذ في هذه الوحدة ولا في هذا الفرع؛ "
    "والإعلانُ ليس تنفيذًا"
)

CALIBRATION_NAMED_RESIDUALS: Final[tuple[str, ...]] = (
    A_DIVERGENT_FROZEN_TEXT_IS_AN_INVALID_PREREGISTRATION_NOTE,
    AN_UNREACHABLE_VERDICT_IS_DECLARED_NOT_DISCOVERED_NOTE,
    BOOLEAN_AGREEMENT_IS_NOT_SCALE_TRANSPORT_NOTE,
    DECLARED_INVARIANT_IS_NOT_A_VERIFIED_ONE_NOTE,
    A_REPAIRED_RUN_ON_SEEN_CASES_IS_NOT_PROSPECTIVE_NOTE,
    G0_FLT_1_IS_NOT_ISSUED_HERE_NOTE,
)


def _refuse_a_calibration_that_repairs_the_frozen_text() -> None:
    if hypothesis_digest(HYPOTHESIS_TEXT) != HYPOTHESIS_DIGEST:
        raise FractalCalibrationError(
            "النصُّ المُجمَّد تغيّر؛ والمعايرةُ تُسمّي انحرافَه ولا تُصلحه، "
            "فإصلاحُه بعد قراءته يمحو شاهدَ العيب نفسَه"
        )


def _refuse_an_unnamed_prerequisite() -> None:
    if len(FLT1_PREREQUISITES) != len(set(FLT1_PREREQUISITES)):
        raise FractalCalibrationError("شرطٌ مكرَّرٌ في شروط G0.FLT-1 يُنقص العدَّ ويُقرأ تمامًا")


_refuse_a_calibration_that_repairs_the_frozen_text()
_refuse_an_unnamed_prerequisite()
