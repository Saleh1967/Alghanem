"""`PK_0`: تجميدُ نصّ فرضية «وجوب المعلومات السابقة المنظَّمة»، وفاحصُ أمانةٍ يقابله.

هذه فرضيةٌ **تأسيسيّةٌ مستقلّة**، لا تعديلٌ لنصّ `G0.NSB-0` ولا نقضٌ له
(`ALayerThatFoundALayerBeneathItIsNotARefutedLayer`): نصُّ النسبة يبقى بحرفه
وبصمته ومنزلته، وما يُضاف هنا طبقةٌ تحته اكتُشِف أنّها كانت مفقودة.

وهي — كسابقتها — **فرضيةٌ داخليّةٌ للمشروع لا قولٌ منقول**
(`AnInternalHypothesisIsNotATransmittedSource`): لا سندَ نقلٍ يُدّعى لها، ولا
تُقرَأ شاهدًا على أحد.

**والفحصُ يُشتَقّ ولا يُوعَد به** (`FidelityIsDerivedNotPromised`): تُسمَّى
مواضعُ الترميز الحاسمةُ واحدًا واحدًا، ويُشتَقّ حضورُها من النصّ المودَع نفسِه،
ويسقط الاستيرادُ عند غياب موضعٍ منها.

**ولا قراءةَ في هذا الإيداع** (`NoReadoutExistsForPK0Yet`): لا يُشغَّل الضبطُ
السلبيُّ للنسبة، ولا تُسمّى مدوّنةٌ محجوزة، حتى تستقرّ السلسلةُ
`PK_0 → O_0 → O_L`؛ لأنّ اختبارَ أنواعٍ مولودةٍ من طبقةٍ لم تَعُد الأسبقَ
اختبارٌ لغير ما يُدّعى.

تسجيلٌ لا سلطة: لا ولادةَ ولا حكمَ ولادةٍ ولا تجميدَ `E0`؛ ولا تستورد هذه
الحزمةُ من `metaalgebra/` ولا `linguistic/` ولا `arabic/` ولا `kernel/` حرفًا،
فهي أسبقُ منها جميعًا في محور الموجودات.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Final

from ..canonical_content import canonical_bytes, canonical_digest

__all__ = [
    "AN_EVENT_IS_A_KIND_AN_EVENT_ANCHOR_IS_A_ROLE_NOTE",
    "AN_INTERNAL_HYPOTHESIS_IS_NOT_A_TRANSMITTED_SOURCE_NOTE",
    "A_LAYER_THAT_FOUND_A_LAYER_BENEATH_IT_IS_NOT_REFUTED_NOTE",
    "FIDELITY_IS_DERIVED_NOT_PROMISED_NOTE",
    "FREE_TEXT_CONDITION_IS_NOT_A_LICENSED_CONDITION_NOTE",
    "NO_READOUT_EXISTS_FOR_PK0_YET_NOTE",
    "ONTOLOGICAL_KIND_IS_NOT_LINGUISTIC_ROLE_NOTE",
    "PRIOR_HYPOTHESIS_NAMED_RESIDUALS",
    "PRIOR_HYPOTHESIS_TEXT",
    "PRIOR_INFORMATION_ORDERS_POSSIBILITY_NOT_RESULT_NOTE",
    "PRIOR_TEXT_DIGEST",
    "REQUIRED_NOTATION_SITES",
    "THE_ALGEBRA_DOES_NOT_CREATE_ITS_OBJECTS_NOTE",
    "FidelityReport",
    "FidelitySiteReading",
    "FidelityStanding",
    "NotationSite",
    "PriorHypothesisError",
    "derive_fidelity_report",
    "prior_text_digest",
]


class PriorHypothesisError(ValueError):
    """رفضٌ مُسمّى في وحدة نصّ `G0.PK-0`؛ لا تصحيحَ صامتًا ولا تخطّي."""


PRIOR_HYPOTHESIS_TEXT: Final[
    str
] = r"""فرضيةٌ داخليّةٌ للمشروع، لا قولٌ منقول، ولا تعديلٌ لنصّ `G0.NSB-0`.

الأصل المُقترَح:

\boxed{\text{لا أنطولوجيا قبل معلوماتٍ سابقةٍ منظَّمة}}

فقد ثبت في `G0.NSB-0` تصحيحٌ أوّل: أنّ النسبةَ أسبقُ لغويًّا من الحامل والحالة
بوصفهما تمثيلًا، وأنّ:

\boxed{
LinguisticObject(x)=Representation(x)+RelationalRole(x)
}

ثمّ ظهر تصحيحٌ أعمقُ منه: أنّ أطرافَ النسبة وأنواعَها لا يجوز افتراضُها قبل أن
تُولَد من أنطولوجيا مُرخَّصة، وأنّ الأنطولوجيا نفسَها لا تبدأ قبل المعلومات
السابقة المنظَّمة.

فالسؤالُ لم يعد: أين نضع النسبةَ بين الجبر العامّ والعربيّة؟ بل صار قبله:

\boxed{\text{ما الموجودُ الذي يصلح جنسًا أو فردًا أو صفةً أو حدثًا أو علاقةً أو
كمّيّةً أو مرجعًا، وبأيّ معيارٍ تُحفَظ هويّتُه؟}}

ومحورُ الموجودات:

\boxed{
PK_0\rightarrow O_0\rightarrow O_L\rightarrow O_{AR}
}

ومحورُ الجبر الذي يعمل عليها:

\boxed{
\Sigma_M\quad\leadsto\quad\Sigma_L\quad\leadsto\quad\Sigma_{AR}
}

محورانِ لا سلسلةٌ واحدة؛ و\Sigma_M ليست طبقةً أنطولوجيّة، بل لغةُ التمثيل
والتسجيل والتحوّل والإغلاق والأثر والبقايا التي تُوصَف بها هذه البنى ويُتحقَّق
منها.

والعلاقةُ بين المحورين:

\boxed{
\Sigma_L\ \text{لا يخلق}\ O_L
}

بل:

\boxed{
\Sigma_L\ \text{يعمل على موجوداتٍ رخّصتها}\ O_L
}

وهذا هو التصحيحُ الجوهريّ.

وتتفرّع عنه قاعدةُ فصلٍ نوعيّة:

\boxed{
OntologicalKind \neq LinguisticRole
}

على منوال ما ثبت قبلُ:

\boxed{
Representation \neq RelationalRole
}

فالجهةُ إذن:

\boxed{
Genus\rightarrow TermAnchorRole
}

لا:

\boxed{
Genus\subseteq TermAnchor
}

بوصفها حقيقةً أوّليّةً غيرَ مبرهنة. ومن ثَمّ يفترق الأمرانِ اللذان جُمِعا في
مرساة الحدث: «الحدث» نوعٌ أنطولوجيّ، و«مرساةُ حدثٍ داخل نسبةٍ لغويّة» دورٌ
لغويٌّ لذلك الموجود؛ فخلطُهما خلطُ ماهيّةِ الشيء بوظيفته في اللغة.

وحدُّ المعلومات السابقة المنظَّمة أضيقُ وأقوى من مخزنِ حقائقَ جاهزة: هي تسجيلُ
الشروط التي تُجيز أصلًا ولادةَ الأنطولوجيا، وهي تسعة:

\boxed{
PK_0=\{Domain,\ UnitCriterion,\ IdentityCriterion,\ AttributePossibility,
RelationPossibility,\ TransformationConditions,\ ConditionsAndPreventers,
PreservedTrace,\ ClosureBlockingRemainder\}
}

ولا تقول: «هذا الشيءُ جنس»، بل تقول: ما الشروطُ التي تجعل من المشروع أن يُولَد
نوعٌ اسمُه «جنس»؟ فالقاعدة:

\boxed{
PriorInformationOrdersPossibilityNotResult
}

أي: تنظّم مجالَ الإمكان، ولا تختار النتيجةَ بدل البرهان.

وكلُّ مرشَّحٍ في الأنطولوجيا العامّة يلزمه أمرانِ لا يُغني أحدُهما عن الآخر:

\boxed{
OntologicalCandidate=Necessity+Irreducibility
}

والشرطُ المكتوبُ نصًّا حرًّا ليس شرطًا مبرهنًا:

\boxed{
FreeTextConditionIsNotALicensedCondition
}

فما في شرط حفظ هويّة الطرف وشرطِ قبول موضع الحجّة اليومَ تسجيلُ مرحلةٍ مقبول،
ولا يكفي متى ادُّعي برهانٌ أنطولوجيّ؛ لأنّ النظامَ لا يتحقّق من صدق نصٍّ حرٍّ
ولا من صلته بالمعلومات السابقة. فتحوُّلُهما إلى مراجعِ شروطٍ مولودةٍ مُرخَّصةٍ
واجبٌ مؤجَّلٌ مُصرَّحٌ بتأجيله، لا إهمالٌ.

والسلسلةُ الأعمقُ المُجمَّدة:

\boxed{
PriorOrganizedInformation
\rightarrow GeneralOntology
\rightarrow LinguisticOntology
\rightarrow NisbahAlgebra
\rightarrow ArabicOntology
\rightarrow ArabicAlgebra
\rightarrow Closure
\rightarrow Ifadah
}

مع بقاء الجبر العامّ أداةً صوريّةً تحكم التمثيلَ والانتقالَ والأثرَ والبقايا
عبر هذه المستويات، لا بديلًا عن الأنطولوجيا نفسِها.

و`G0.NSB-0` لا يُنقَض بهذا ولا يُحرَّر حرفُه:

\boxed{
ALayerThatFoundALayerBeneathItIsNotARefutedLayer
}

فهي طبقةٌ صحيحةٌ اكتُشِف أنّ تحتها طبقةً مفقودة؛ وحفظُ نصّها حفظٌ لتاريخ
البرهان، وهو أولى من هدمه.

ولا قراءةَ هنا:

\boxed{
NoReadoutExistsForPK0Yet
}

فلا يُشغَّل الضبطُ السلبيُّ للنسبة، ولا تُسمّى مدوّنةٌ محجوزة، حتى تستقرّ
PK_0 \rightarrow O_0 \rightarrow O_L؛ لأنّ اختبارَ أنواعٍ مولودةٍ من طبقةٍ لم
تَعُد الأسبقَ اختبارٌ لغير ما يُدّعى.
"""


class FidelityStanding(Enum):
    """منزلةُ النصّ المودَع؛ ثنائيّةٌ لأنّ الموضعَ إمّا حضر أو غاب."""

    ALL_REQUIRED_SITES_PRESENT = "كلُّ_المواضع_الحاسمة_حاضرةٌ_في_النصّ_المودَع"
    A_REQUIRED_SITE_IS_ABSENT = "موضعٌ_حاسمٌ_غائبٌ_فالتسجيلُ_باطلٌ_قبل_تشغيله"


@dataclass(frozen=True, slots=True)
class NotationSite:
    """موضعُ ترميزٍ حاسمٌ في النصّ، بما يقرّره وبما يسقط بسقوطه."""

    site_id: str
    literal: str
    what_it_decides: str
    what_its_absence_invalidates: str

    def __post_init__(self) -> None:
        for value, name in (
            (self.site_id, "مُعرِّفُ الموضع"),
            (self.literal, "حرفيّةُ الموضع"),
            (self.what_it_decides, "ما يقرّره الموضع"),
            (self.what_its_absence_invalidates, "ما يُبطله غيابُه"),
        ):
            if not isinstance(value, str) or not value.strip():
                raise PriorHypothesisError(
                    f"{name} نصٌّ غيرُ فارغ؛ وموضعٌ بلا حرفيّةٍ لا يُفحَص"
                )


REQUIRED_NOTATION_SITES: Final[tuple[NotationSite, ...]] = (
    NotationSite(
        site_id="the-two-axes",
        literal=r"\Sigma_M\quad\leadsto\quad\Sigma_L\quad\leadsto\quad\Sigma_{AR}",
        what_it_decides="أنّ الموجوداتِ محورٌ والجبرَ محورٌ آخر، لا سلسلةً واحدة",
        what_its_absence_invalidates="يُعيد `Σ_M` طبقةً أنطولوجيّةً وهي لغةُ تمثيل",
    ),
    NotationSite(
        site_id="the-existence-chain",
        literal=r"PK_0\rightarrow O_0\rightarrow O_L\rightarrow O_{AR}",
        what_it_decides="ترتيبَ محور الموجودات من المعلومات السابقة إلى العربيّة",
        what_its_absence_invalidates="أصلَ الدعوى، فتعود الأنواعُ بلا أصلٍ سابق",
    ),
    NotationSite(
        site_id="the-algebra-does-not-create-its-objects",
        literal=r"\Sigma_L\ \text{يعمل على موجوداتٍ رخّصتها}\ O_L",
        what_it_decides="أنّ الجبرَ يعمل على موجوداتٍ مُرخَّصةٍ ولا يخلقها",
        what_its_absence_invalidates="التصحيحَ الجوهريّ، فتعود الأنواعُ مولودةً بالجبر",
    ),
    NotationSite(
        site_id="kind-is-not-role",
        literal=r"OntologicalKind \neq LinguisticRole",
        what_it_decides="الفصلَ النوعيَّ بين ماهيّة الموجود ووظيفته اللغويّة",
        what_its_absence_invalidates="يُجيز دفنَ الوظيفة في الماهيّة كما وقع قبلُ",
    ),
    NotationSite(
        site_id="the-direction-of-licensing",
        literal=r"Genus\rightarrow TermAnchorRole",
        what_it_decides="أنّ الترخيصَ جهةٌ من النوع إلى الدور لا احتواءٌ أوّليّ",
        what_its_absence_invalidates="جهةَ الترخيص، فيعود الاحتواءُ مصادرةً",
    ),
    NotationSite(
        site_id="the-nine-prior-conditions",
        literal=r"PK_0=\{Domain,\ UnitCriterion,\ IdentityCriterion,\ ",
        what_it_decides="الحدَّ الأدنى للمعلومات السابقة المنظَّمة، معدودًا لا مفتوحًا",
        what_its_absence_invalidates="يجعل `PK₀` مخزنَ حقائقَ جاهزةٍ بلا حدٍّ يُفحَص",
    ),
    NotationSite(
        site_id="possibility-not-result",
        literal=r"PriorInformationOrdersPossibilityNotResult",
        what_it_decides="أنّ المعلومات السابقة تنظّم الإمكانَ ولا تختار النتيجة",
        what_its_absence_invalidates="يفتح بابَ إيداع الجواب في موضع البرهان",
    ),
    NotationSite(
        site_id="necessity-and-irreducibility",
        literal=r"OntologicalCandidate=Necessity+Irreducibility",
        what_it_decides="شرطَي المرشَّح الأنطولوجيّ مجتمعَين لا أحدَهما",
        what_its_absence_invalidates="يُدخِل مرشَّحًا بلا ضرورةٍ ولا ما يمنع اختزاله",
    ),
    NotationSite(
        site_id="free-text-is-not-a-licensed-condition",
        literal=r"FreeTextConditionIsNotALicensedCondition",
        what_it_decides="قصورَ النصّ الحرّ عن أن يكون شرطًا مبرهنًا",
        what_its_absence_invalidates="يُثبِّت الحالَ القائمةَ بوصفها كافيةً للبرهان",
    ),
    NotationSite(
        site_id="the-deepest-chain",
        literal=(
            "PriorOrganizedInformation"
            "\n"
            r"\rightarrow GeneralOntology"
            "\n"
            r"\rightarrow LinguisticOntology"
            "\n"
            r"\rightarrow NisbahAlgebra"
        ),
        what_it_decides="السلسلةَ الثمانيّةَ من المعلومات السابقة إلى الإفادة",
        what_its_absence_invalidates="ترتيبَ المستويات، فيصير كلٌّ منها قابلًا للتقديم",
    ),
    NotationSite(
        site_id="a-founded-layer-is-not-a-refuted-one",
        literal=r"ALayerThatFoundALayerBeneathItIsNotARefutedLayer",
        what_it_decides="أنّ `G0.NSB-0` قائمٌ غيرُ منقوضٍ ولا محرَّر",
        what_its_absence_invalidates="حفظَ تاريخ البرهان، فيُقرَأ هذا الإيداعُ هدمًا",
    ),
    NotationSite(
        site_id="no-readout-for-pk0",
        literal=r"NoReadoutExistsForPK0Yet",
        what_it_decides="إيقافَ الضبط السلبيّ وتسميةِ المدوّنة حتى يستقرّ الأصل",
        what_its_absence_invalidates="يُجيز تشغيلًا سابقًا لأوانه على أنواعٍ غيرِ مُرخَّصة",
    ),
)
"""مواضعُ الترميز الحاسمة؛ حضورُها يُشتَقّ من النصّ ولا يُوعَد به."""


@dataclass(frozen=True, slots=True)
class FidelitySiteReading:
    """قراءةُ موضعٍ واحد: أحاضرٌ هو؟ وما يقرّره وما يُبطله غيابُه."""

    site_id: str
    is_present: bool
    what_it_decides: str
    what_its_absence_invalidates: str


@dataclass(frozen=True, slots=True)
class FidelityReport:
    """تقريرُ الأمانة كاملًا؛ يُعرَض قبل وجود أيّ قراءة."""

    standing: FidelityStanding
    sites: tuple[FidelitySiteReading, ...]
    absent_site_ids: tuple[str, ...]
    text_digest: str

    @property
    def is_fit_to_be_run(self) -> bool:
        """التسجيلُ صالحٌ للتشغيل متى حضرت المواضعُ الحاسمة كلُّها."""

        return self.standing is FidelityStanding.ALL_REQUIRED_SITES_PRESENT


def prior_text_digest(text: str | None = None) -> str:
    """اشتقّ بصمةَ النصّ من بايتاته المعياريّة؛ ولا تُكتَب بجانبه ثابتًا."""

    text = PRIOR_HYPOTHESIS_TEXT if text is None else text
    if not isinstance(text, str) or not text.strip():
        raise PriorHypothesisError("النصُّ المُجمَّد نصٌّ غيرُ فارغ")
    return canonical_digest(canonical_bytes(text))


PRIOR_TEXT_DIGEST: Final[str] = prior_text_digest()


def derive_fidelity_report(text: str | None = None) -> FidelityReport:
    """اشتقّ حضورَ كلّ موضعٍ حاسمٍ من النصّ المودَع؛ ولا تُصرِّح بأمانةٍ منقولة."""

    text = PRIOR_HYPOTHESIS_TEXT if text is None else text
    readings: list[FidelitySiteReading] = []
    absent: list[str] = []
    for site in REQUIRED_NOTATION_SITES:
        present = site.literal in text
        if not present:
            absent.append(site.site_id)
        readings.append(
            FidelitySiteReading(
                site_id=site.site_id,
                is_present=present,
                what_it_decides=site.what_it_decides,
                what_its_absence_invalidates=site.what_its_absence_invalidates,
            )
        )
    standing = (
        FidelityStanding.ALL_REQUIRED_SITES_PRESENT
        if not absent
        else FidelityStanding.A_REQUIRED_SITE_IS_ABSENT
    )
    return FidelityReport(
        standing=standing,
        sites=tuple(readings),
        absent_site_ids=tuple(absent),
        text_digest=prior_text_digest(text),
    )


AN_INTERNAL_HYPOTHESIS_IS_NOT_A_TRANSMITTED_SOURCE_NOTE: Final[str] = (
    "AnInternalHypothesisIsNotATransmittedSource: هذا النصُّ فرضيةٌ وُلِدت في "
    "المشروع، فلا سندَ نقلٍ يُدّعى لها ولا منزلةَ روايةٍ تُقرَأ فيها"
)

FIDELITY_IS_DERIVED_NOT_PROMISED_NOTE: Final[str] = (
    "FidelityIsDerivedNotPromised: أمانةُ النصّ تُشتَقّ موضعًا بموضعٍ ويسقط "
    "الاستيرادُ عند غياب موضعٍ حاسم؛ والوعدُ بالحرفيّة ليس فحصًا لها"
)

PRIOR_INFORMATION_ORDERS_POSSIBILITY_NOT_RESULT_NOTE: Final[str] = (
    "PriorInformationOrdersPossibilityNotResult: المعلوماتُ السابقةُ المنظَّمة "
    "تنظّم مجالَ الإمكان ولا تختار النتيجةَ بدل البرهان؛ فهي تقول ما الشروطُ "
    "التي تُجيز ولادةَ نوعٍ اسمُه «جنس»، ولا تقول «هذا الشيءُ جنس»"
)

THE_ALGEBRA_DOES_NOT_CREATE_ITS_OBJECTS_NOTE: Final[str] = (
    "TheAlgebraDoesNotCreateItsObjects: `Σ_L` لا يخلق `O_L` بل يعمل على "
    "موجوداتٍ رخّصتها `O_L`؛ وجبرٌ يُولِّد أنواعَه يُثبِت ما افترضه"
)

ONTOLOGICAL_KIND_IS_NOT_LINGUISTIC_ROLE_NOTE: Final[str] = (
    "OntologicalKindIsNotLinguisticRole: ماهيّةُ الموجود غيرُ وظيفته في اللغة، "
    "على منوال `Representation ≠ RelationalRole`؛ والجهةُ ترخيصٌ من النوع إلى "
    "الدور لا احتواءٌ أوّليٌّ غيرُ مبرهن"
)

AN_EVENT_IS_A_KIND_AN_EVENT_ANCHOR_IS_A_ROLE_NOTE: Final[str] = (
    "AnEventIsAKindAnEventAnchorIsARole: «الحدث» نوعٌ أنطولوجيّ، و«مرساةُ حدثٍ "
    "في نسبة» دورٌ لغويٌّ لذلك الموجود؛ وجمعُهما في مفردةٍ واحدةٍ خلطُ الماهيّة "
    "بالوظيفة"
)

FREE_TEXT_CONDITION_IS_NOT_A_LICENSED_CONDITION_NOTE: Final[str] = (
    "FreeTextConditionIsNotALicensedCondition: شرطٌ مكتوبٌ نصًّا حرًّا تسجيلُ "
    "مرحلةٍ مقبول، ولا يكفي متى ادُّعي برهانٌ؛ لأنّ النظامَ لا يتحقّق من صدقه "
    "ولا من صلته بالمعلومات السابقة"
)

A_LAYER_THAT_FOUND_A_LAYER_BENEATH_IT_IS_NOT_REFUTED_NOTE: Final[str] = (
    "ALayerThatFoundALayerBeneathItIsNotARefutedLayer: `G0.NSB-0` طبقةٌ صحيحةٌ "
    "اكتُشِف أنّ تحتها طبقةً مفقودة؛ فلا يُحرَّر حرفُها ولا تُقرَأ منقوضةً، "
    "وحفظُ نصّها حفظٌ لتاريخ البرهان"
)

NO_READOUT_EXISTS_FOR_PK0_YET_NOTE: Final[str] = (
    "NoReadoutExistsForPK0Yet: هذا الإيداعُ نصٌّ وبنيةٌ صوريّةٌ وتسجيلٌ فقط؛ "
    "ولا يُشغَّل معه الضبطُ السلبيُّ للنسبة ولا تُسمّى مدوّنةٌ محجوزة"
)

PRIOR_HYPOTHESIS_NAMED_RESIDUALS: Final[tuple[str, ...]] = (
    AN_INTERNAL_HYPOTHESIS_IS_NOT_A_TRANSMITTED_SOURCE_NOTE,
    FIDELITY_IS_DERIVED_NOT_PROMISED_NOTE,
    PRIOR_INFORMATION_ORDERS_POSSIBILITY_NOT_RESULT_NOTE,
    THE_ALGEBRA_DOES_NOT_CREATE_ITS_OBJECTS_NOTE,
    ONTOLOGICAL_KIND_IS_NOT_LINGUISTIC_ROLE_NOTE,
    AN_EVENT_IS_A_KIND_AN_EVENT_ANCHOR_IS_A_ROLE_NOTE,
    FREE_TEXT_CONDITION_IS_NOT_A_LICENSED_CONDITION_NOTE,
    A_LAYER_THAT_FOUND_A_LAYER_BENEATH_IT_IS_NOT_REFUTED_NOTE,
    NO_READOUT_EXISTS_FOR_PK0_YET_NOTE,
)
"""البقايا المُسمّاةُ لهذا الإيداع؛ تُقرَأ ولا يُدّعى انحلالُ واحدةٍ منها."""


def _refuse_a_text_that_lost_a_required_site() -> None:
    report = derive_fidelity_report()
    if not report.is_fit_to_be_run:
        raise PriorHypothesisError(
            "سقط موضعٌ حاسمٌ من النصّ المودَع: "
            + "، ".join(report.absent_site_ids)
            + "؛ والتسجيلُ باطلٌ قبل تشغيله لا ناقصُ تنسيق"
        )


_refuse_a_text_that_lost_a_required_site()
