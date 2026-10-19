"""معلومة ومفهوم: الثالوث الأنطولوجي للدلالة (§3 من G0.N).

الفهم البنيوي/النحوي الصحيح للنص **معلومةٌ فقط**؛ ولا يصير مفهومًا إلا بواقعٍ
مُدرَكٍ في الذهن: حسًّا مباشرًا، أو تسليمًا مسنَدًا بسلسلةٍ تنتهي بحسّ — على
منوال سلسلة التفويض في `SealedInvariantExtractorRegistry`.
"""

from __future__ import annotations

from dataclasses import dataclass, fields
from enum import Enum
from typing import Final

__all__ = [
    "EXCLUDED_TARGET_NOTES",
    "ONLY_LEGITIMATE_TARGET_NOTE",
    "SANAD_MUST_TERMINATE_NOTE",
    "STRUCTURAL_UNDERSTANDING_IS_NOT_A_CONCEPT_NOTE",
    "ContentStanding",
    "MalumaMafhumError",
    "SanadLink",
    "SanadOrigin",
    "SemanticTarget",
    "UnderstandingRecord",
]


class MalumaMafhumError(ValueError):
    """رفضٌ صريحٌ في تمييز المعلومة عن المفهوم."""


class ContentStanding(Enum):
    """حالُ المحتوى: معلومةٌ مُمثَّلة، أو مفهومٌ مُسنَد إلى حسّ."""

    معلومة = "معلومة"
    مفهوم = "مفهوم"


class SemanticTarget(Enum):
    """أهدافُ «الدلالة» الثلاثة؛ اثنان مستبعَدان بنيويًّا لا عمليًّا."""

    استرجاع_الوضع = "استرجاع_الوضع"
    المطابقة_للخارج = "المطابقة_للخارج"
    قصد_المتكلم_الفردي = "قصد_المتكلم_الفردي"


class SanadOrigin(Enum):
    """منشأُ حلقة السند: حسٌّ مباشر، أو تسليمٌ عن حلقةٍ سابقة."""

    حسّ_مباشر = "حسّ_مباشر"
    تسليم_عن_سابق = "تسليم_عن_سابق"


ONLY_LEGITIMATE_TARGET_NOTE: Final[str] = (
    "هدفُ الدلالة المشروع الوحيد استرجاعُ الوضع: انتظامٌ توزيعيٌّ مستقرٌّ عبر "
    "مجتمعٍ لغوي، قابلٌ للرصد إحصائيًّا في كوربصٍ كبير."
)

EXCLUDED_TARGET_NOTES: Final[dict[SemanticTarget, str]] = {
    SemanticTarget.المطابقة_للخارج: (
        "المطابقةُ للخارج (صدقُ المحتوى) مستبعَدةٌ بنيويًّا لا عمليًّا: تحتاج "
        "دليلاً خارج اللغة كليًّا، ولا شيءَ في هذا الأنبوب يخرج عن اللغة."
    ),
    SemanticTarget.قصد_المتكلم_الفردي: (
        "قصدُ المتكلم الفردي (نيةٌ نفسية) مستبعَدٌ منهجيًّا بنصٍّ صريح تحت "
        "`NoIntentProjection`، لا لصعوبة الوصول إليه فحسب."
    ),
}

STRUCTURAL_UNDERSTANDING_IS_NOT_A_CONCEPT_NOTE: Final[str] = (
    "فهمٌ بنيويٌّ/نحويٌّ صحيحٌ للنص معلومةٌ فقط؛ وترقيتُه إلى مفهومٍ بلا واقعٍ "
    "مُدرَكٍ في الذهن هي بعينها المصادرةُ التي يمنعها هذا التمييز."
)

SANAD_MUST_TERMINATE_NOTE: Final[str] = (
    "سلسلةُ التسليم التي لا تنتهي بحسٍّ مباشرٍ لا تُنتج مفهومًا مهما طالت؛ "
    "والطولُ ليس بديلاً عن الانتهاء."
)


def _require_non_blank(value: str, label: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise MalumaMafhumError(f"{label} نصٌّ غير فارغ.")
    return value


@dataclass(frozen=True, slots=True)
class SanadLink:
    """حلقةٌ واحدةٌ في سلسلة التفويض المنتهية إلى حسّ."""

    link_id: str
    origin: SanadOrigin
    delegated_from: str | None

    def __post_init__(self) -> None:
        _require_non_blank(self.link_id, "معرّف الحلقة")
        if not isinstance(self.origin, SanadOrigin):
            raise MalumaMafhumError("منشأُ الحلقة من مفردته المغلقة.")
        if self.origin is SanadOrigin.حسّ_مباشر:
            if self.delegated_from is not None:
                raise MalumaMafhumError(
                    "الحسُّ المباشر منشأٌ لا تسليم؛ فلا حلقةَ سابقةَ له."
                )
            return
        if self.delegated_from is None:
            raise MalumaMafhumError(
                "التسليمُ عن سابقٍ يلزمه تسميةُ الحلقة السابقة بالاسم."
            )
        _require_non_blank(self.delegated_from, "الحلقة السابقة")
        if self.delegated_from == self.link_id:
            raise MalumaMafhumError("حلقةٌ تُسنِد إلى نفسها ليست سندًا.")


def _validate_sanad(chain: tuple[SanadLink, ...]) -> None:
    """تحقّق أن السلسلة متّصلةٌ وتنتهي بحسٍّ مباشرٍ عند طرفها الأخير."""

    if not isinstance(chain, tuple) or not chain:
        raise MalumaMafhumError("السندُ سلسلةٌ غير فارغةٍ من الحلقات.")
    seen: set[str] = set()
    for link in chain:
        if not isinstance(link, SanadLink):
            raise MalumaMafhumError("كلُّ حلقةٍ في السند حلقةٌ مُصاغة، لا نصٌّ حرّ.")
        if link.link_id in seen:
            raise MalumaMafhumError("حلقةٌ مُعادةٌ بمعرّفها نفسه ليست حلقةً ثانية.")
        seen.add(link.link_id)
    for link in chain[1:]:
        if link.origin is not SanadOrigin.تسليم_عن_سابق:
            raise MalumaMafhumError(
                "حسٌّ مباشرٌ في وسط السلسلة يقطعها؛ الطرفُ المنتهي واحدٌ لا غير."
            )
    for earlier, later in zip(chain, chain[1:], strict=False):
        if later.delegated_from != earlier.link_id:
            raise MalumaMafhumError(
                "السلسلةُ مقطوعة: حلقةٌ لا تُسنِد إلى الحلقة التي تسبقها."
            )
    if chain[0].origin is not SanadOrigin.حسّ_مباشر:
        raise MalumaMafhumError("سلسلةٌ لا تنتهي بحسٍّ مباشرٍ لا تُنتج مفهومًا مهما طالت.")


@dataclass(frozen=True, slots=True)
class UnderstandingRecord:
    """قراءةٌ واحدة: أهي معلومةٌ فقط أم مفهومٌ مُسنَد؟ والحالُ تُشتَقّ."""

    content_id: str
    target: SemanticTarget
    structurally_admissible: bool
    sanad: tuple[SanadLink, ...]
    declared_standing: ContentStanding

    def __post_init__(self) -> None:
        _require_non_blank(self.content_id, "معرّف المحتوى")
        if not isinstance(self.target, SemanticTarget):
            raise MalumaMafhumError("هدفُ الدلالة من مفردته المغلقة.")
        if self.target in EXCLUDED_TARGET_NOTES:
            raise MalumaMafhumError(EXCLUDED_TARGET_NOTES[self.target])
        if not isinstance(self.structurally_admissible, bool):
            raise MalumaMafhumError("القبولُ البنيوي قيمةٌ ثنائية.")
        if not self.structurally_admissible:
            raise MalumaMafhumError("ما لم يُمثَّل بنيويًّا ليس معلومةً أصلاً، فلا يُسجَّل هنا.")
        if not isinstance(self.sanad, tuple):
            raise MalumaMafhumError("السندُ سلسلةُ حلقاتٍ مُصاغة.")
        if self.sanad:
            _validate_sanad(self.sanad)
        if not isinstance(self.declared_standing, ContentStanding):
            raise MalumaMafhumError("حالُ المحتوى من مفردتها المغلقة.")
        if self.declared_standing is not self.standing:
            raise MalumaMafhumError(
                "الحالُ المكتوبة تخالف المُشتَقّة من السند؛ والحالُ تُشتَقّ " "ولا تُكتَب."
            )

    @property
    def standing(self) -> ContentStanding:
        """الحالُ مُشتقّةً من وجود سندٍ منتهٍ إلى حسٍّ وحده."""

        if self.sanad:
            return ContentStanding.مفهوم
        return ContentStanding.معلومة

    @property
    def is_concept(self) -> bool:
        return self.standing is ContentStanding.مفهوم


def _assert_no_fields_matching(markers: tuple[str, ...]) -> None:
    for declaring_type in (SanadLink, UnderstandingRecord):
        for field in fields(declaring_type):
            for marker in markers:
                if marker in field.name:
                    raise RuntimeError(
                        f"{declaring_type.__name__} يحمل حقلاً محظورًا: {field.name}"
                    )


if len(ContentStanding) != 2:
    raise RuntimeError("حالُ المحتوى ثنائيةٌ مغلقة.")
if len(SemanticTarget) != 3:
    raise RuntimeError("أهدافُ الدلالة ثلاثةٌ لا غير.")
if len(SanadOrigin) != 2:
    raise RuntimeError("منشأُ الحلقة ثنائيٌّ مغلق.")
if set(EXCLUDED_TARGET_NOTES) | {SemanticTarget.استرجاع_الوضع} != set(SemanticTarget):
    raise RuntimeError("المستبعَدان بنيويًّا لا يُغطّيان ما عدا الهدف المشروع.")
_assert_no_fields_matching(("count", "number", "total", "verdict", "birth", "intent"))
