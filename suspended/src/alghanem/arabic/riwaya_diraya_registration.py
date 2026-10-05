"""بوابتا القبول المنفصلتان: تسجيلُ الرواية وتسجيلُ الدراية (§4 من G0.N).

هذه الوحدة **تسجيلٌ لا بوابة**: لا تُصدر حكمًا، ولا يقرؤها `IndependentClosureGate`
ولا `BirthVerdictGate`، على منوال `DeclaredDefectCause != AssessedRelation`.
"""

from __future__ import annotations

from dataclasses import dataclass, fields
from enum import Enum
from typing import Final

__all__ = [
    "CATEGORY_REDEFINITION_IS_NOT_EVIDENCE_TIGHTENING_NOTE",
    "NOT_A_GATE_NOTE",
    "NO_BEDROCK_NOTE",
    "SEPARATION_NOTE",
    "DirayaBranch",
    "DirayaReading",
    "DirayaStanding",
    "IndependentApplication",
    "Remedy",
    "RiwayaDirayaRegistrationError",
    "RiwayaReading",
    "RiwayaStanding",
    "derive_remedy",
]


class RiwayaDirayaRegistrationError(ValueError):
    """رفضٌ صريحٌ في تسجيل الرواية والدراية."""


class RiwayaStanding(Enum):
    """حالُ القناة الناقلة نفسها، لا حالُ المتن."""

    قناة_سليمة = "قناة_سليمة"
    قناة_معطوبة = "قناة_معطوبة"


class DirayaBranch(Enum):
    """فرعا الدراية، مُميَّزان نوعًا لا بحقلٍ في صنفٍ واحد."""

    أنطولوجي = "أنطولوجي"
    ابستمولوجي = "ابستمولوجي"


class DirayaStanding(Enum):
    """حالُ المتن عند تطبيقٍ مستقلٍّ واحد."""

    لم_يُهزَم_بعد = "لم_يُهزَم_بعد"
    مهزوم = "مهزوم"


class Remedy(Enum):
    """العلاجات الثلاثة؛ كلٌّ منها مُشتقٌّ من نوع الفشل وحده."""

    إصلاح_الأداة = "إصلاح_الأداة"
    إعادة_تعريف_الفئات = "إعادة_تعريف_الفئات"
    تشديد_اختبار_الأدلة = "تشديد_اختبار_الأدلة"


SEPARATION_NOTE: Final[str] = (
    "الرواية تفحص سلامة القناة، والدراية تفحص المتن؛ وهما بوابتان منفصلتان "
    "تمامًا، فلا تُجمعان في صنفٍ واحدٍ بحقلَين."
)

CATEGORY_REDEFINITION_IS_NOT_EVIDENCE_TIGHTENING_NOTE: Final[str] = (
    "إعادةُ تعريف الفئات ليست تشديدًا لاختبار الأدلة: الأولى علاجُ فشلٍ "
    "أنطولوجي (المتن من غير جنسه)، والثانية علاجُ فشلٍ ابستمولوجي (المتن "
    "عارَض ما هو أقوى منه مُجمَّدًا). الخلط بينهما يُنجي المتن الباطل جنسًا "
    "بتشديدٍ لا يمسّه، أو يُهدر المتن الصحيح جنسًا بإعادة تصنيفٍ لا يحتاجها."
)

NO_BEDROCK_NOTE: Final[str] = (
    "الدرايةُ عمليةٌ مستمرةٌ لا بوابةٌ تُجتاز مرة: كل تطبيقٍ مستقلٍّ جديد "
    "(كوربص/أداة/نطاق) فرصةُ هزيمةٍ جديدة، ونجاحاتٌ متكررةٌ لا تعني «ثابت» "
    "بل «لم يُهزَم بعد»؛ ولذلك لا حقلَ «اجتيزت» هنا."
)

NOT_A_GATE_NOTE: Final[str] = (
    "تسجيلٌ لا بوابة: لا حكمَ يصدر عن هذه الوحدة، ولا سلطةَ كيرنل تقرؤها."
)

_REMEDY_BY_DIRAYA_BRANCH: Final[dict[DirayaBranch, Remedy]] = {
    DirayaBranch.أنطولوجي: Remedy.إعادة_تعريف_الفئات,
    DirayaBranch.ابستمولوجي: Remedy.تشديد_اختبار_الأدلة,
}


def derive_remedy(failure: RiwayaStanding | DirayaBranch) -> Remedy:
    """اشتقّ العلاج من نوع الفشل؛ لا موضعَ يُكتَب فيه العلاج حرًّا."""

    if isinstance(failure, RiwayaStanding):
        if failure is RiwayaStanding.قناة_سليمة:
            raise RiwayaDirayaRegistrationError(
                "لا علاجَ لقناةٍ سليمة؛ العلاج مُشتقٌّ من فشلٍ واقع."
            )
        return Remedy.إصلاح_الأداة
    if isinstance(failure, DirayaBranch):
        return _REMEDY_BY_DIRAYA_BRANCH[failure]
    raise RiwayaDirayaRegistrationError(
        "نوعُ الفشل من مفردتَيه المغلقتَين: رواية أو فرعُ دراية."
    )


def _require_non_blank(value: str, label: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise RiwayaDirayaRegistrationError(f"{label} نصٌّ غير فارغ.")
    return value


@dataclass(frozen=True, slots=True)
class RiwayaReading:
    """قراءةُ الرواية: هوية الأداة وبصمتها وسجلّ تغييراتها، لا المتن."""

    tool_identity: str
    tool_digest: str
    change_log_reference: str
    reproduced_independently: bool
    declared_standing: RiwayaStanding

    def __post_init__(self) -> None:
        _require_non_blank(self.tool_identity, "هوية الأداة")
        _require_non_blank(self.tool_digest, "بصمة الأداة")
        _require_non_blank(self.change_log_reference, "مرجع سجلّ التغييرات")
        if not isinstance(self.reproduced_independently, bool):
            raise RiwayaDirayaRegistrationError(
                "إعادةُ الإنتاج المستقلّة قيمةٌ ثنائية مرصودة."
            )
        if not isinstance(self.declared_standing, RiwayaStanding):
            raise RiwayaDirayaRegistrationError("حالُ الرواية من مفردتها المغلقة.")
        if self.declared_standing is not self.standing:
            raise RiwayaDirayaRegistrationError(
                "الحالُ المكتوبة تخالف المُشتَقّة من إعادة الإنتاج المستقلّة؛ "
                "والحالُ تُشتَقّ ولا تُكتَب."
            )

    @property
    def standing(self) -> RiwayaStanding:
        """حالُ القناة، مُشتقّةً من إعادة الإنتاج المستقلّة وحدها."""

        if self.reproduced_independently:
            return RiwayaStanding.قناة_سليمة
        return RiwayaStanding.قناة_معطوبة

    @property
    def remedy(self) -> Remedy | None:
        """علاجُ فشل الرواية: إصلاحُ الأداة، لا إعادةُ تعريف فئات."""

        if self.standing is RiwayaStanding.قناة_سليمة:
            return None
        return derive_remedy(self.standing)


@dataclass(frozen=True, slots=True)
class IndependentApplication:
    """تطبيقٌ مستقلٌّ واحد: كوربص/أداة/نطاق، وحالُ المتن عنده."""

    application_id: str
    independent_scope: str
    standing: DirayaStanding

    def __post_init__(self) -> None:
        _require_non_blank(self.application_id, "معرّف التطبيق")
        _require_non_blank(self.independent_scope, "نطاقُ التطبيق المستقلّ")
        if not isinstance(self.standing, DirayaStanding):
            raise RiwayaDirayaRegistrationError(
                "حالُ المتن عند التطبيق من مفردتها المغلقة."
            )


@dataclass(frozen=True, slots=True)
class DirayaReading:
    """قراءةُ الدراية على فرعٍ واحدٍ مُميَّز، عبر تطبيقاتٍ مستقلّةٍ متعدّدة."""

    matn_reference: str
    branch: DirayaBranch
    stronger_frozen_reference: str | None
    applications: tuple[IndependentApplication, ...]

    def __post_init__(self) -> None:
        _require_non_blank(self.matn_reference, "مرجع المتن")
        if not isinstance(self.branch, DirayaBranch):
            raise RiwayaDirayaRegistrationError(
                "فرعُ الدراية من مفردته المغلقة: أنطولوجي أو ابستمولوجي."
            )
        if not isinstance(self.applications, tuple) or not self.applications:
            raise RiwayaDirayaRegistrationError(
                "الدرايةُ عمليةٌ مستمرة، فيلزمها تطبيقٌ مستقلٌّ واحدٌ على الأقلّ."
            )
        seen: set[str] = set()
        for application in self.applications:
            if not isinstance(application, IndependentApplication):
                raise RiwayaDirayaRegistrationError(
                    "كلُّ تطبيقٍ قراءةٌ مستقلّةٌ مُصاغة، لا نصٌّ حرّ."
                )
            if application.application_id in seen:
                raise RiwayaDirayaRegistrationError(
                    "تطبيقٌ مستقلٌّ مُعاد بمعرّفه نفسه ليس تطبيقًا ثانيًا."
                )
            seen.add(application.application_id)
        if self.branch is DirayaBranch.ابستمولوجي:
            if self.stronger_frozen_reference is None:
                raise RiwayaDirayaRegistrationError(
                    "الدرايةُ الابستمولوجية تفحص المعارضة لما هو أقوى مُجمَّدًا "
                    "فعلاً، فيلزمها مرجعُ ذلك الأقوى بالاسم."
                )
            _require_non_blank(self.stronger_frozen_reference, "مرجعُ الأقوى المُجمَّد")
        elif self.stronger_frozen_reference is not None:
            raise RiwayaDirayaRegistrationError(
                "الدرايةُ الأنطولوجية سابقةٌ على أيّ دليل، فلا تُسنَد إلى "
                "مُجمَّدٍ أقوى؛ سؤالها تصنيفيٌّ عن الجنس."
            )

    @property
    def defeated(self) -> bool:
        """هُزم المتنُ إن هُزم عند تطبيقٍ مستقلٍّ واحد؛ ولا يُجبَر بتكرار النجاح."""

        return any(
            application.standing is DirayaStanding.مهزوم
            for application in self.applications
        )

    @property
    def reading(self) -> str:
        """قراءةُ السجل: «لم يُهزَم بعد» لا «ثابت»."""

        if self.defeated:
            return "مهزوم عند تطبيقٍ مستقلٍّ واحدٍ على الأقلّ"
        return "لم يُهزَم بعد؛ وكلُّ تطبيقٍ مستقلٍّ جديدٍ فرصةُ هزيمة"

    @property
    def remedy(self) -> Remedy | None:
        """علاجُ فشل الدراية، مُشتقًّا من فرعها لا مكتوبًا."""

        if not self.defeated:
            return None
        return derive_remedy(self.branch)


def _assert_no_fields_matching(markers: tuple[str, ...]) -> None:
    for declaring_type in (RiwayaReading, DirayaReading, IndependentApplication):
        for field in fields(declaring_type):
            for marker in markers:
                if marker in field.name:
                    raise RuntimeError(
                        f"{declaring_type.__name__} يحمل حقلاً محظورًا: {field.name}"
                    )


if len(RiwayaStanding) != 2:
    raise RuntimeError("حالُ الرواية ثنائيةٌ مغلقة.")
if len(DirayaBranch) != 2:
    raise RuntimeError("فرعا الدراية اثنان لا غير.")
if len(DirayaStanding) != 2:
    raise RuntimeError("حالُ المتن عند التطبيق ثنائيةٌ مغلقة.")
if len(Remedy) != 3:
    raise RuntimeError("العلاجات ثلاثةٌ لا غير.")
if set(_REMEDY_BY_DIRAYA_BRANCH) != set(DirayaBranch):
    raise RuntimeError("اشتقاقُ العلاج غيرُ تامٍّ على فرعَي الدراية.")
_assert_no_fields_matching(
    ("count", "number", "total", "verdict", "birth", "passed", "اجتيزت")
)
