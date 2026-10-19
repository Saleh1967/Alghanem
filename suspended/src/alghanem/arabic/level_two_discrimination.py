"""الاختبارُ الفارق للمستوى الثاني: تسجيلٌ مسبقٌ قبل نقل أيّ نصّ، وحارسٌ يمنع
قراءةَ تطابق أجناس الوقوف فركتاليًّا ما دام أحدُها وقوفَ روايةٍ لا وقوفَ دراية.

**الاكتشافُ الذي وُضِعت هذه الوحدة لأجله**: `derive_lexical_citation_structure`
يشترط عتبةَ عددٍ مُسمّاةً الآن (`LEXICAL_CHAIN_MINIMUM_ATTRIBUTIONS == 2`)،
فاستشهادٌ بإسنادٍ **واحدٍ حقيقيٍّ تمامًا** يُشتَقّ منه `عنوان_واحد_مسطح` بجنس
امتناعٍ واحدٍ مع من لم يَنقُل إسنادًا أصلًا. ولازمُ ذلك أنّ الوقوفَ المُسجَّل في
بطاقة «سائمة الغنم» **لم يكن قابلًا للتفنيد بإسنادٍ واحدٍ حقيقيّ**: سلبيّةٌ
واحدةٌ ممتنعةُ القراءة بنيويًّا، لا بياناتٌ ناقصةٌ وحسب.

**وهذا نمطٌ متكرّرٌ يُسمّى هنا ولا يُنتظَر اكتشافُه بعد كلّ بناء**
(`STRUCTURALLY_UNFALSIFIABLE_NEGATIVE_IS_A_RECURRING_PATTERN_NOTE`): اشتراطُ
`متواتر` باسمه جعل الحلقةَ الرابعة ممتنعةً أبدًا لا واقفةً بعارض، ثمّ تكرّر
الجنسُ نفسُه في عتبة العدد هنا. فلكلّ بوّابةٍ جديدةٍ سؤالٌ استباقيّ واحد: **أيّ
مدخلٍ واقعيٍّ يُفنّد وقوفَها؟** فإن لم يوجد فالوقوفُ قيدُ أداةٍ لا نتيجة.

**والتسجيلُ هنا تمهيديٌّ بسيط** على منوال `COMPOUND_LAYER_PREREGISTRATION`، لا
بصمةَ فيه ولا مَسجَل: المُجمَّد قبل النصّ هو المتغيّرُ الوحيد المسموحُ بتغييره،
والثوابتُ التي لا تُمَسّ، وفروعُ النتيجة وما يُرخّصه كلُّ فرعٍ وما يمنعه.
والثقلُ الأعلى يُدَّخر للحظة تشغيل التجربة على بياناتٍ حقيقيةٍ فعلًا.

**ومجالُ الاختبار الفارق مقصورٌ على (الغنم) و(سائمة)** وحدهما كما صُمِّم؛ أمّا
حارسُ التطابق فعامٌّ يُقرأ على أيّ عددٍ من الحالات، لأنّ تحذيرَه لا يخصّ زوجًا
بعينه: تطابقُ جنس الوقوف عبر أيّ عددٍ من الحالات لا يعني فركتاليّةً ما دام
أحدُها وقوفَ رواية.

**ولا حكمَ فركتاليًّا هنا (Φ)**: هذه الوحدة تُسمّي **جنسَ التطابق المؤهَّل
للقراءة** ولا تُصدر حكمًا بوقوع فركتاليّةٍ ولا بانتفائها؛ وذلك بعينه
`FRACTAL_VERDICT_IS_NOT_ISSUED_HERE_NOTE` في `level_two_manat.py`.

**خمولٌ سلطويّ**: لا ولادةَ ولا حكمَ ولادةٍ ولا تجميدَ ولا `E0`، ولا تقرأ هذه
المخرجاتِ بوّابةٌ في `kernel/`.
"""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass, fields
from enum import Enum
from typing import Any, Final

from .compound_layer_preregistration import NamedRefusal
from .level_two_manat import (
    LevelTwoStopGenus,
    TaqyeedLinkAttempt,
)
from .lexical_transmission import (
    LEXICAL_CHAIN_MINIMUM_ATTRIBUTIONS,
    lexical_unconstructibility_genus,
    read_lexical_transmission,
)
from .text_key import comparison_key
from .transmission_standing import UnconstructibilityGenus

__all__ = [
    "ARITY_IS_NOT_A_LINGUISTIC_STRUCTURE_NOTE",
    "DISCRIMINATION_AUTHORITY_NOTE",
    "DISCRIMINATION_SCOPE_NOTE",
    "IDENTICAL_STOP_GENUS_IS_NOT_FRACTAL_EVIDENCE_NOTE",
    "LEVEL_TWO_DISCRIMINATION_PREREGISTRATION",
    "SINGLE_ATTRIBUTION_STOP_IS_AN_ARITY_ARTIFACT_NOTE",
    "STRUCTURALLY_UNFALSIFIABLE_NEGATIVE_IS_A_RECURRING_PATTERN_NOTE",
    "DiscriminationBranch",
    "DiscriminationBranchRegistration",
    "LevelTwoDiscriminationError",
    "LevelTwoDiscriminationPreregistration",
    "StopDataStanding",
    "StopMatchGenus",
    "StopReading",
    "card_stop_data_standing",
    "card_stop_reading",
    "discrimination_branch",
    "stop_match_genus",
]


DISCRIMINATION_AUTHORITY_NOTE: Final[str] = (
    "تسجيلٌ واشتقاقٌ فقط: لا تُنتج هذه الوحدة ولادةً ولا حكمَ ولادة، ولا "
    "تُجمِّد، ولا تُصدر `E0`، ولا تقرؤها بوّابةٌ في النواة"
)

DISCRIMINATION_SCOPE_NOTE: Final[str] = (
    "DiscriminationScopeIsTheGhanamSaimaPairAlone: الاختبارُ الفارق مقصورٌ على "
    "بطاقتي (الغنم) و(سائمة) وبطاقة تركيبهما، فهو اختبارٌ محدَّدُ الغرض؛ "
    "وحارسُ التطابق وحده عامٌّ يُقرأ على أيّ عددٍ من الحالات"
)

SINGLE_ATTRIBUTION_STOP_IS_AN_ARITY_ARTIFACT_NOTE: Final[str] = (
    "SingleAttributionStopIsAnArityArtifact: وقوفٌ على إسنادٍ واحدٍ — ولو كان "
    f"منقولًا بنصّه حقيقةً — أثرُ عتبة العدد ({LEXICAL_CHAIN_MINIMUM_ATTRIBUTIONS}) "
    "لا نتيجةَ الاختبار الفارق؛ فلا يُقرأ تفنيدًا ولا تأييدًا، ولا يُبنى عليه "
    "ادّعاءُ تطابقٍ عبر المستويين"
)

ARITY_IS_NOT_A_LINGUISTIC_STRUCTURE_NOTE: Final[str] = (
    "ArityIsNotALinguisticStructure: تطابقُ جنس الامتناع بين استشهادٍ بإسنادٍ "
    "واحدٍ واستشهادٍ بلا إسنادٍ أصلًا تطابقُ قيدٍ في الأداة، لا بنيةٌ لغويةٌ "
    "تكرّرت؛ وقراءتُه بنيةً تنقل حدَّ الأداة إلى العالم"
)

IDENTICAL_STOP_GENUS_IS_NOT_FRACTAL_EVIDENCE_NOTE: Final[str] = (
    "IdenticalStopGenusIsNotFractalEvidenceWhileDataIsAbsent: تطابقُ جنس "
    "الوقوف عبر مستويين — أو عبر أيّ عددٍ من الحالات — لا يُقرأ شهادةً على "
    "تكرار بنيةٍ ما دام أحدُ الطرفين واقفًا لأنّه لم يُنقَل عنه إسنادٌ بعد: "
    "ذلك تطابقُ روايةٍ (لم يُكتَب النقلُ بعد) لا تطابقُ دراية (بنيةٌ فُحِصت "
    "فتكرّرت)، وخلطُهما يُلبِس غيابَ البيانات ثوبَ النجاح"
)

STRUCTURALLY_UNFALSIFIABLE_NEGATIVE_IS_A_RECURRING_PATTERN_NOTE: Final[str] = (
    "StructurallyUnfalsifiableNegativeIsARecurringPattern: وقعت هذه العلّةُ "
    "مرّاتٍ بأثوابٍ مختلفة — اشتراطُ `متواتر` باسمه جعل الحلقة الرابعة ممتنعةً "
    "أبدًا لا واقفةً بعارض، ثمّ عتبةُ عدد الإسنادات جعلت السلبيّة بإسنادٍ واحدٍ "
    "حقيقيٍّ غيرَ قابلةٍ للقراءة. فلكلّ بوّابةٍ جديدةٍ سؤالٌ استباقيٌّ يُطرَح قبل "
    "بنائها لا بعده: أيُّ مدخلٍ واقعيٍّ يُفنّد وقوفَها؟ فإن لم يوجد فوقوفُها "
    "قيدُ أداةٍ لا نتيجةَ فحص"
)


class LevelTwoDiscriminationError(ValueError):
    """رفضٌ صريحٌ في وحدة الاختبار الفارق؛ لا يُحمَل على أقرب حالةٍ مقبولة."""


class StopDataStanding(Enum):
    """حالُ البيانات المنقولة في الطريق المفحوص، مُشتَقّةً من تعداده لا مكتوبة."""

    لا_إسناد_منقول = "لا_إسناد_منقول"
    إسناد_واحد_منقول = "إسناد_واحد_منقول"
    إسناد_متعاقب_منقول = "إسناد_متعاقب_منقول"


class DiscriminationBranch(Enum):
    """فروعُ الاختبار الفارق، مُسمّاةٌ كلُّها قبل نقل أيّ نصّ."""

    الرابط_قام = "الرابط_قام"
    وقف_بإسناد_متعاقب_منقول = "وقف_بإسناد_متعاقب_منقول"
    وقف_لتعارض_منقول = "وقف_لتعارض_منقول"
    وقف_بإسناد_واحد_منقول = "وقف_بإسناد_واحد_منقول"
    لم_يُزوَّد_بإسناد_بعد = "لم_يُزوَّد_بإسناد_بعد"
    وقف_مدخل_خارج_الاختبار = "وقف_مدخل_خارج_الاختبار"


class StopMatchGenus(Enum):
    """جنسُ تطابق أجناس الوقوف: أتطابقُ روايةٍ هو أم تطابقُ درايةٍ مرشَّح؟"""

    لا_تطابق = "لا_تطابق"
    تطابق_رواية = "تطابق_رواية"
    تطابق_دراية_مرشح = "تطابق_دراية_مرشح"
    تطابق_غير_محسوم = "تطابق_غير_محسوم"


if len(StopDataStanding) != 3:  # pragma: no cover - guard
    raise RuntimeError(
        "حالُ البيانات ثلاثيةٌ مغلقة: لا إسناد، أو واحدٌ دون العتبة، أو متعاقبٌ "
        "بالغُها؛ وطيُّ الأوسط يُخفي أثرَ العتبة الذي وُضِعت هذه الوحدة لكشفه"
    )
if len(DiscriminationBranch) != 6:  # pragma: no cover - guard
    raise RuntimeError("فروعُ الاختبار الفارق سداسيةٌ مغلقةٌ مُسمّاةٌ قبل النصّ")
if len(StopMatchGenus) != 4:  # pragma: no cover - guard
    raise RuntimeError(
        "جنسُ التطابق رباعيٌّ مغلق: ونفيُ تطابق الرواية ليس إثباتًا لتطابق الدراية"
    )


_FORBIDDEN_FIELD_MARKERS: Final[tuple[str, ...]] = (
    "count",
    "total",
    "score",
    "rank",
    "percent",
    "ratio",
    "verdict",
    "birth",
    "fractal",
    "attainment",
)


def _require_text(value: str, label: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise LevelTwoDiscriminationError(f"{label} نصٌّ غير فارغ")
    return value


@dataclass(frozen=True, slots=True)
class DiscriminationBranchRegistration:
    """فرعٌ واحدٌ مُسجَّلٌ قبل النصّ: ما يُرخّصه، وما يمنعه، كلاهما بنصّه."""

    branch: DiscriminationBranch
    licensed_reading: str
    refused_reading: str

    def __post_init__(self) -> None:
        if not isinstance(self.branch, DiscriminationBranch):
            raise LevelTwoDiscriminationError("الفرعُ من مفردته المغلقة")
        _require_text(self.licensed_reading, f"ما يُرخّصه {self.branch.value}")
        _require_text(self.refused_reading, f"ما يمنعه {self.branch.value}")


@dataclass(frozen=True, slots=True)
class LevelTwoDiscriminationPreregistration:
    """التسجيلُ المسبقُ للاختبار الفارق: متغيّرٌ واحد، وثوابتُه، وفروعُه كلُّها."""

    controlled_variable: str
    fixed_elements: tuple[str, ...]
    branches: tuple[DiscriminationBranchRegistration, ...]
    refusals: tuple[NamedRefusal, ...]

    def __post_init__(self) -> None:
        _require_text(self.controlled_variable, "المتغيّرُ الوحيد")
        if len(self.fixed_elements) < 2:
            raise LevelTwoDiscriminationError(
                "الثوابتُ تُسمّى اثنين فأكثر، وإلّا فلا عزلَ لمتغيّرٍ أصلًا"
            )
        seen_fixed: set[str] = set()
        for element in self.fixed_elements:
            _require_text(element, "ثابتٌ في التسجيل")
            key = comparison_key(element)
            if key in seen_fixed:
                raise LevelTwoDiscriminationError(f"ثابتٌ مكرَّرٌ في التسجيل: {element}")
            seen_fixed.add(key)

        registered: list[DiscriminationBranch] = []
        for registration in self.branches:
            if not isinstance(registration, DiscriminationBranchRegistration):
                raise LevelTwoDiscriminationError(
                    "كلُّ فرعٍ `DiscriminationBranchRegistration` بنصَّيه"
                )
            if registration.branch in registered:
                raise LevelTwoDiscriminationError(
                    f"فرعٌ مكرَّرٌ في التسجيل: {registration.branch.value}"
                )
            registered.append(registration.branch)
        missing = tuple(
            branch for branch in DiscriminationBranch if branch not in registered
        )
        if missing:
            raise LevelTwoDiscriminationError(
                "فرعٌ غيرُ مُسجَّلٍ قبل النصّ: "
                + "، ".join(branch.value for branch in missing)
                + "؛ والتغطيةُ تسبق القراءة، وفرعٌ لم يُسجَّل يُقرأ بعد وقوعه "
                "بما يشتهيه قارئه"
            )

        if not self.refusals:
            raise LevelTwoDiscriminationError(
                "تسجيلٌ بلا رفضٍ مُسمًّى واحد: حدودُ الاختبار تُسمّى ولا تُترَك للقارئ"
            )
        refusal_names: set[str] = set()
        for refusal in self.refusals:
            if not isinstance(refusal, NamedRefusal):
                raise LevelTwoDiscriminationError("كلُّ رفضٍ `NamedRefusal` باسمه وبيانه")
            if refusal.name in refusal_names:
                raise LevelTwoDiscriminationError(f"رفضٌ مكرَّر: {refusal.name}")
            refusal_names.add(refusal.name)

    @property
    def registered_branches(self) -> tuple[DiscriminationBranch, ...]:
        """الفروعُ بترتيب تسجيلها، مُشتَقّةً من التسجيلات نفسها."""

        return tuple(registration.branch for registration in self.branches)

    def registration_for(
        self, branch: DiscriminationBranch
    ) -> DiscriminationBranchRegistration:
        """تسجيلُ فرعٍ بعينه؛ والفرعُ موجودٌ بحكم التغطية المفحوصة عند الإنشاء."""

        for registration in self.branches:
            if registration.branch is branch:
                return registration
        raise LevelTwoDiscriminationError(f"لا تسجيلَ للفرع {branch.value}")


LEVEL_TWO_DISCRIMINATION_PREREGISTRATION: Final[
    LevelTwoDiscriminationPreregistration
] = LevelTwoDiscriminationPreregistration(
    controlled_variable=(
        "تعدادُ `الإسنادات` في بطاقة تركيب (سائمة الغنم) وحده: يُزوَّد بنقلٍ "
        "مُسنَدٍ منقولٍ بنصّه أو يبقى خاليًا، ولا يُمَسّ شيءٌ سواه"
    ),
    fixed_elements=(
        "بطاقتا المستوى الأول (الغنم) و(سائمة) بنصّهما وقرائنهما، وحالُ إغلاقهما "
        "الصادرة عن بوّابة G0.EA.1",
        "نسبةُ التركيب المُعلَنة `تقييدية` ومصدرُها المُسمّى في بطاقة التركيب",
        "معيارُ قيام الرابط في `TaqyeedManatGate` وحروفُ `lexical_transmission` "
        "و`transmission_standing` كما هي",
        "علاماتُ التخصيص والطرديّة المُجمَّدة في `level_two_manat.py` قبل القراءة",
    ),
    branches=(
        DiscriminationBranchRegistration(
            branch=DiscriminationBranch.الرابط_قام,
            licensed_reading=(
                "قام الرابطُ بإسنادٍ حقيقيّ: يُقرأ أنّ المستوى الأول وقف لإجمالٍ "
                "لغويٍّ حقيقيّ وأنّ المستوى الثاني كان واقفًا لغياب بياناتٍ وحدها، "
                "فاستقلالُ آلة المستويين مرشَّحٌ للبناء عليه"
            ),
            refused_reading=(
                "ولا يُقرأ حكمًا بفركتاليّةٍ ولا بانتفائها، ولا شهادةً لمرحلة "
                "`التضمين_والتقييد` المُجمَّدة"
            ),
        ),
        DiscriminationBranchRegistration(
            branch=DiscriminationBranch.وقف_بإسناد_متعاقب_منقول,
            licensed_reading=(
                "وقف الرابطُ رغم إسنادٍ متعاقبٍ منقولٍ بنصّه بالغِ العتبة: عندئذٍ "
                "فقط يصير تطابقُ جنس الوقوف عبر المستويين تطابقَ درايةٍ مرشَّحًا "
                "يُفحَص، لا مصادفةَ رواية"
            ),
            refused_reading=(
                "ولا يُقرأ إثباتًا لفركتاليّةٍ بنفسه: التطابقُ يصير عندها أهلًا "
                "للفحص، والحكمُ يُترَك لقراءةٍ خارج هذه الوحدة"
            ),
        ),
        DiscriminationBranchRegistration(
            branch=DiscriminationBranch.وقف_لتعارض_منقول,
            licensed_reading=(
                "نُقِل في الطريق تخصيصٌ وطرديّةٌ معًا: تُقرأ حالُ خلافٍ منقولةً "
                "بجنس وقوفٍ مُسمًّى، وهي نتيجةٌ تُسجَّل لا عطلٌ في الأداة"
            ),
            refused_reading=(
                "ولا يُحمَل التعارضُ على أحد طرفيه، ولا يُقرأ تفنيدًا للاختبار "
                "الفارق ولا تأييدًا له"
            ),
        ),
        DiscriminationBranchRegistration(
            branch=DiscriminationBranch.وقف_بإسناد_واحد_منقول,
            licensed_reading=(
                "لا يُقرأ من هذا الفرع شيءٌ سوى أنّ العتبةَ لم تُبلَغ: "
                + SINGLE_ATTRIBUTION_STOP_IS_AN_ARITY_ARTIFACT_NOTE
            ),
            refused_reading=(
                "ويمتنع قطعًا أن يُقرأ سلبيّةً حقيقيةً أو تطابقًا عبر المستويين: "
                + ARITY_IS_NOT_A_LINGUISTIC_STRUCTURE_NOTE
            ),
        ),
        DiscriminationBranchRegistration(
            branch=DiscriminationBranch.لم_يُزوَّد_بإسناد_بعد,
            licensed_reading=(
                "لم يُنقَل إسنادٌ بعد: يُقرأ أنّ الاختبار الفارق **لم يُجرَ**، "
                "وأنّ الوقوفَ القائم وقوفُ روايةٍ لا يخبر عن التركيب شيئًا"
            ),
            refused_reading=(
                "ويمتنع أيُّ ادّعاء تطابقٍ عبر المستويين على هذا الفرع: "
                + IDENTICAL_STOP_GENUS_IS_NOT_FRACTAL_EVIDENCE_NOTE
            ),
        ),
        DiscriminationBranchRegistration(
            branch=DiscriminationBranch.وقف_مدخل_خارج_الاختبار,
            licensed_reading=(
                "وقف المدخلُ قبل أن تُختبَر الآلةُ أصلًا: يُقرأ خروجًا من مجال "
                "الاختبار الفارق، لا نتيجةً فيه"
            ),
            refused_reading=(
                "ولا يُقرأ فشلًا للآلة، ولا يدخل في مقارنة أجناس الوقوف عبر " "المستويين"
            ),
        ),
    ),
    refusals=(
        NamedRefusal(
            name="SingleAttributionStopIsAnArityArtifact",
            statement=SINGLE_ATTRIBUTION_STOP_IS_AN_ARITY_ARTIFACT_NOTE,
        ),
        NamedRefusal(
            name="IdenticalStopGenusIsNotFractalEvidenceWhileDataIsAbsent",
            statement=IDENTICAL_STOP_GENUS_IS_NOT_FRACTAL_EVIDENCE_NOTE,
        ),
        NamedRefusal(
            name="ArityIsNotALinguisticStructure",
            statement=ARITY_IS_NOT_A_LINGUISTIC_STRUCTURE_NOTE,
        ),
        NamedRefusal(
            name="StructurallyUnfalsifiableNegativeIsARecurringPattern",
            statement=STRUCTURALLY_UNFALSIFIABLE_NEGATIVE_IS_A_RECURRING_PATTERN_NOTE,
        ),
        NamedRefusal(
            name="DiscriminationScopeIsTheGhanamSaimaPairAlone",
            statement=DISCRIMINATION_SCOPE_NOTE,
        ),
    ),
)


def card_stop_data_standing(card: Mapping[str, Any]) -> StopDataStanding:
    """حالُ البيانات المنقولة في طريق هذه البطاقة، مُشتَقّةً من تعداده وحده.

    وبطاقةٌ لم تُعلِن طريقَها وبطاقةٌ أعلنته بتعدادٍ خالٍ كلتاهما `لا_إسناد_منقول`:
    الفارقُ بينهما بنيةُ إعلانٍ لا بياناتٌ منقولة، والمقروءُ هنا البياناتُ.
    """

    descriptor = read_lexical_transmission(card)
    if descriptor is None or not descriptor.attributions:
        return StopDataStanding.لا_إسناد_منقول
    if len(descriptor.attributions) < LEXICAL_CHAIN_MINIMUM_ATTRIBUTIONS:
        return StopDataStanding.إسناد_واحد_منقول
    return StopDataStanding.إسناد_متعاقب_منقول


@dataclass(frozen=True, slots=True)
class StopReading:
    """قراءةُ موقفٍ واحد: موضعُه، وجنسُ امتناعه، وحالُ بياناته المنقولة."""

    label: str
    genus: UnconstructibilityGenus
    data: StopDataStanding

    def __post_init__(self) -> None:
        _require_text(self.label, "موضعُ القراءة")
        if not isinstance(self.genus, UnconstructibilityGenus):
            raise LevelTwoDiscriminationError("جنسُ الامتناع من مفردته المغلقة")
        if not isinstance(self.data, StopDataStanding):
            raise LevelTwoDiscriminationError("حالُ البيانات من مفردتها المغلقة")


def card_stop_reading(label: str, card: Mapping[str, Any]) -> StopReading:
    """اقرأ موقفَ بطاقةٍ بعينها: جنسَ امتناعها وحالَ بياناتها معًا، لا أحدَهما."""

    if not isinstance(card, Mapping):
        raise LevelTwoDiscriminationError("البطاقةُ كائنٌ يُقرأ بمفاتيحه")
    descriptor = read_lexical_transmission(card)
    genus = (
        UnconstructibilityGenus.GENUS_NOT_SETTLED
        if descriptor is None
        else lexical_unconstructibility_genus(descriptor)
    )
    return StopReading(label=label, genus=genus, data=card_stop_data_standing(card))


def stop_match_genus(readings: tuple[StopReading, ...]) -> StopMatchGenus:
    """اشتقّ جنسَ تطابق أجناس الوقوف، ولا تُصدر به حكمًا فركتاليًّا.

    ولا يقوم `تطابق_دراية_مرشح` إلّا إذا بلغ **كلُّ** طرفٍ عتبةَ التعاقب: فطرفٌ
    بلا إسنادٍ يجعل التطابقَ تطابقَ روايةٍ، وطرفٌ بإسنادٍ واحدٍ يجعله غيرَ محسوم
    لأنّ جنسَه أثرُ عتبةٍ (`ARITY_IS_NOT_A_LINGUISTIC_STRUCTURE_NOTE`).
    """

    if not isinstance(readings, tuple):
        raise LevelTwoDiscriminationError("القراءاتُ مجموعةٌ مرتَّبة")
    if len(readings) < 2:
        raise LevelTwoDiscriminationError(
            "التطابقُ نسبةٌ بين قراءتين فأكثر، وقراءةٌ واحدةٌ لا تُطابق نفسها"
        )
    for reading in readings:
        if not isinstance(reading, StopReading):
            raise LevelTwoDiscriminationError("كلُّ قراءةٍ من نوع `StopReading`")
    genera = {reading.genus for reading in readings}
    if len(genera) != 1:
        return StopMatchGenus.لا_تطابق
    if any(reading.data is StopDataStanding.لا_إسناد_منقول for reading in readings):
        return StopMatchGenus.تطابق_رواية
    if all(reading.data is StopDataStanding.إسناد_متعاقب_منقول for reading in readings):
        return StopMatchGenus.تطابق_دراية_مرشح
    return StopMatchGenus.تطابق_غير_محسوم


def discrimination_branch(
    attempt: TaqyeedLinkAttempt, composition_card: Mapping[str, Any]
) -> DiscriminationBranch:
    """اشتقّ فرعَ الاختبار الفارق من محاولة الرابط وبطاقة تركيبها معًا."""

    if not isinstance(attempt, TaqyeedLinkAttempt):
        raise LevelTwoDiscriminationError("الفرعُ يُشتَقّ من محاولة رابطٍ مُصاغة")
    if not isinstance(composition_card, Mapping):
        raise LevelTwoDiscriminationError("بطاقةُ التركيب كائنٌ يُقرأ بمفاتيحه")
    if attempt.stood_up:
        return DiscriminationBranch.الرابط_قام
    if attempt.stop_genus is LevelTwoStopGenus.وقوف_مدخل_قبل_اختبار_الآلة:
        return DiscriminationBranch.وقف_مدخل_خارج_الاختبار
    if attempt.stop_genus is LevelTwoStopGenus.وقوف_آلة_لتعارض_منقول_في_دلالة_القيد:
        return DiscriminationBranch.وقف_لتعارض_منقول
    data = card_stop_data_standing(composition_card)
    if data is StopDataStanding.لا_إسناد_منقول:
        return DiscriminationBranch.لم_يُزوَّد_بإسناد_بعد
    if data is StopDataStanding.إسناد_واحد_منقول:
        return DiscriminationBranch.وقف_بإسناد_واحد_منقول
    return DiscriminationBranch.وقف_بإسناد_متعاقب_منقول


def _bears_marker(name: str, marker: str) -> bool:
    """أيحمل اسمُ الحقل هذه العلامةَ كلمةً قائمةً لا جزءًا من كلمةٍ أخرى؟"""

    return marker in name.split("_")


def _assert_no_fields_matching(markers: tuple[str, ...]) -> None:
    for declaring_type in (
        DiscriminationBranchRegistration,
        LevelTwoDiscriminationPreregistration,
        StopReading,
    ):
        for field in fields(declaring_type):
            for marker in markers:
                if _bears_marker(field.name, marker):  # pragma: no cover - guard
                    raise RuntimeError(
                        f"{declaring_type.__name__} يحمل حقلاً محظورًا: {field.name}"
                    )


_assert_no_fields_matching(_FORBIDDEN_FIELD_MARKERS)
