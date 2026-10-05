"""تسجيلُ القياس والربط (§10 من G0.N).

تسجيلٌ لا شهادة: لا مصدرَ مسمّى ولا شاهدَ لكل فرعٍ هنا، فالمُخرَج «تسجيل» على
منوال `compound_layer_preregistration` و`convergence_claim_register`.
"""

from __future__ import annotations

from dataclasses import dataclass, fields
from enum import Enum
from typing import Final

from .kulli_juzi_formal import FROZEN_KULLI_JUZI_DOMAIN
from .lafz_madlul_relation_formal import FROZEN_RELATION_DOMAIN
from .madlul_alone_formal import FROZEN_MADLUL_DOMAIN
from .word_class_formal import FROZEN_FORMAL_DOMAIN

__all__ = [
    "ASL_MUST_BE_FROZEN_NOTE",
    "FOREIGN_CASE_NOTE",
    "FROZEN_ASL_REFERENCES",
    "INVALID_FROM_ORIGIN_IS_NOT_WEAK_NOTE",
    "RABT_IS_UNCONSTRUCTIBLE_NOTE",
    "ForeignDeclaredCase",
    "IllaApplication",
    "LinkStanding",
    "QiyasRegistration",
    "QiyasRabtRegistrationError",
    "QiyasStanding",
    "RabtRegistration",
    "frozen_asl_references",
]


class QiyasRabtRegistrationError(ValueError):
    """رفضٌ صريحٌ في تسجيل القياس والربط."""


class IllaApplication(Enum):
    """انطباقُ العلة على الفرع؛ مفردةٌ مغلقةٌ لا تدرّجَ فيها."""

    منطبقة_فعلاً = "منطبقة_فعلاً"
    تشابه_فئوي_فقط = "تشابه_فئوي_فقط"
    لا_علة_في_النص = "لا_علة_في_النص"


class QiyasStanding(Enum):
    """حالُ القياس: صحيحٌ من أصله، أو باطلٌ من أصله. ولا «ضعيف» بينهما."""

    صحيح_من_أصله = "صحيح_من_أصله"
    باطل_من_أصله = "باطل_من_أصله"


class LinkStanding(Enum):
    """حالُ الرابط المستورَد: استرجاعٌ حتى يُعمَّم على وقائع محجوزة."""

    استرجاع = "استرجاع"
    ربط = "ربط"


INVALID_FROM_ORIGIN_IS_NOT_WEAK_NOTE: Final[str] = (
    "التشابهُ الفئوي وحده، وغيابُ العلة من النص، يُنتجان قياسًا باطلاً من "
    "أصله لا قياسًا «ضعيفًا»: الضعفُ درجةٌ في قياسٍ قائم، والبطلانُ من الأصل "
    "نفيٌ لقيامه. ولذلك لا درجةَ بين طرفَي `QiyasStanding`."
)

RABT_IS_UNCONSTRUCTIBLE_NOTE: Final[str] = (
    "«ربط» مُصرَّحٌ به وغيرُ قابلٍ للإنشاء اليوم: لا يرتقي الرابطُ المستورَد "
    "من «استرجاع» إلى «ربط» إلا بتعميمٍ ناجحٍ على وقائع مستقلةٍ لم تدخل في "
    "تكوين الشهادة (عيّنةٌ محجوزة)، ولا عيّنةَ محجوزةَ تُسلَّم هنا؛ فإصدارُه "
    "ادّعاءُ تعميمٍ لم يجرِ."
)

FOREIGN_CASE_NOTE: Final[str] = (
    "الوقائعُ المُستشهَد بها في وثيقة G0.N (مثل `prefixes ⊂ ziyada` و"
    "`SUN-MOON-LETTERS-AR-1`) غيرُ موجودةٍ في هذا المستودع، فتُسجَّل حالاتٍ "
    "أجنبيةً مُصرَّحةً غيرَ مُتحقَّقة، على منوال `ForeignDeclaredAim`."
)

ASL_MUST_BE_FROZEN_NOTE: Final[str] = (
    "أصلُ القياس إشارةٌ إلى مجالٍ صوريٍّ مُجمَّدٍ فعلاً في هذا المستودع، "
    "يُتحقَّق منه بالاستيراد لا بالكتابة؛ والاسمُ الحرُّ لا يصلح أصلاً."
)


def frozen_asl_references() -> tuple[str, ...]:
    """أعِد أسماءَ المجالات المُجمَّدة، مُشتقّةً بالاستيراد لا مكتوبةً هنا."""

    return tuple(
        sorted(
            type(domain).__name__
            for domain in (
                FROZEN_FORMAL_DOMAIN,
                FROZEN_KULLI_JUZI_DOMAIN,
                FROZEN_MADLUL_DOMAIN,
                FROZEN_RELATION_DOMAIN,
            )
        )
    )


FROZEN_ASL_REFERENCES: Final[tuple[str, ...]] = frozen_asl_references()

_STANDING_BY_ILLA_APPLICATION: Final[dict[IllaApplication, QiyasStanding]] = {
    IllaApplication.منطبقة_فعلاً: QiyasStanding.صحيح_من_أصله,
    IllaApplication.تشابه_فئوي_فقط: QiyasStanding.باطل_من_أصله,
    IllaApplication.لا_علة_في_النص: QiyasStanding.باطل_من_أصله,
}


def _require_non_blank(value: str, label: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise QiyasRabtRegistrationError(f"{label} نصٌّ غير فارغ.")
    return value


@dataclass(frozen=True, slots=True)
class QiyasRegistration:
    """قياسٌ مُسجَّل بأركانه الأربعة: أصلٌ مُجمَّد، وفرع، وعلة، وحكم."""

    asl_reference: str
    far_reference: str
    illa: str
    hukm: str
    illa_application: IllaApplication

    def __post_init__(self) -> None:
        _require_non_blank(self.asl_reference, "الأصل")
        if self.asl_reference not in FROZEN_ASL_REFERENCES:
            raise QiyasRabtRegistrationError(
                "الأصلُ إشارةٌ إلى مجالٍ صوريٍّ مُجمَّدٍ فعلاً في المستودع "
                f"({', '.join(FROZEN_ASL_REFERENCES)})، لا اسمٌ حرّ."
            )
        _require_non_blank(self.far_reference, "الفرع")
        _require_non_blank(self.illa, "العلة")
        _require_non_blank(self.hukm, "الحكم")
        if self.far_reference == self.asl_reference:
            raise QiyasRabtRegistrationError("فرعٌ هو الأصلُ نفسه ليس قياسًا بل إعادةَ نصّ.")
        if not isinstance(self.illa_application, IllaApplication):
            raise QiyasRabtRegistrationError("انطباقُ العلة من مفردته المغلقة الثلاثية.")

    @property
    def standing(self) -> QiyasStanding:
        """الحالُ مُشتقّةً من انطباق العلة وحده؛ ولا «ضعيف» في المفردة."""

        return _STANDING_BY_ILLA_APPLICATION[self.illa_application]

    @property
    def is_invalid_from_origin(self) -> bool:
        return self.standing is QiyasStanding.باطل_من_أصله


@dataclass(frozen=True, slots=True)
class RabtRegistration:
    """رابطٌ مستورَد: استرجاعٌ ما لم تُسلَّم عيّنةٌ محجوزةٌ يُعمَّم عليها."""

    link_id: str
    imported_from: str
    certificate_reference: str
    held_out_cases: tuple[str, ...]
    declared_standing: LinkStanding

    def __post_init__(self) -> None:
        _require_non_blank(self.link_id, "معرّف الرابط")
        _require_non_blank(self.imported_from, "مصدرُ الاستيراد")
        _require_non_blank(self.certificate_reference, "مرجعُ الشهادة")
        if not isinstance(self.held_out_cases, tuple):
            raise QiyasRabtRegistrationError("العيّنةُ المحجوزة سلسلةُ وقائع مُسمّاة.")
        for case in self.held_out_cases:
            _require_non_blank(case, "واقعةٌ محجوزة")
        if not isinstance(self.declared_standing, LinkStanding):
            raise QiyasRabtRegistrationError("حالُ الرابط من مفردتها المغلقة.")
        if len(set(self.held_out_cases)) != len(self.held_out_cases):
            raise QiyasRabtRegistrationError(
                "واقعةٌ محجوزةٌ مُعادةٌ باسمها نفسه ليست واقعةً ثانية."
            )
        if self.declared_standing is LinkStanding.ربط:
            if not self.held_out_cases:
                raise QiyasRabtRegistrationError(
                    "«ربط» بلا عيّنةٍ محجوزةٍ تُعمَّم عليها ليس ربطًا بل "
                    "استرجاعًا مُسمّى باسمٍ أعلى منه."
                )
            raise QiyasRabtRegistrationError(RABT_IS_UNCONSTRUCTIBLE_NOTE)

    @property
    def standing(self) -> LinkStanding:
        """الحالُ الوحيدةُ القابلةُ للإنشاء اليوم: استرجاع."""

        return LinkStanding.استرجاع


@dataclass(frozen=True, slots=True)
class ForeignDeclaredCase:
    """واقعةٌ من خارج هذا المستودع: مُصرَّحةٌ لا مُتحقَّقة."""

    case_id: str
    declared_in: str
    why_not_verifiable_here: str

    def __post_init__(self) -> None:
        _require_non_blank(self.case_id, "معرّف الواقعة")
        _require_non_blank(self.declared_in, "موضعُ التصريح")
        _require_non_blank(self.why_not_verifiable_here, "سببُ تعذّر التحقّق")

    @property
    def verified_here(self) -> bool:
        """لا تُتحقَّق واقعةٌ أجنبيةٌ في هذا المستودع بحال."""

        return False


def _assert_no_fields_matching(markers: tuple[str, ...]) -> None:
    for declaring_type in (QiyasRegistration, RabtRegistration, ForeignDeclaredCase):
        for field in fields(declaring_type):
            for marker in markers:
                if marker in field.name:
                    raise RuntimeError(
                        f"{declaring_type.__name__} يحمل حقلاً محظورًا: {field.name}"
                    )


if len(IllaApplication) != 3:
    raise RuntimeError("انطباقُ العلة ثلاثيٌّ مغلق.")
if len(QiyasStanding) != 2:
    raise RuntimeError("حالُ القياس ثنائيةٌ لا درجةَ بينها.")
if len(LinkStanding) != 2:
    raise RuntimeError("حالُ الرابط ثنائيةٌ مغلقة.")
if set(_STANDING_BY_ILLA_APPLICATION) != set(IllaApplication):
    raise RuntimeError("اشتقاقُ حال القياس غيرُ تامٍّ على انطباقات العلة.")
if len(FROZEN_ASL_REFERENCES) != 4:
    raise RuntimeError("المجالاتُ المُجمَّدة في المستودع أربعةٌ تُقرأ بالاستيراد.")
_assert_no_fields_matching(
    ("count", "number", "total", "verdict", "birth", "weak", "ضعيف")
)
