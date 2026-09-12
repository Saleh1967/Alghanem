"""درجاتُ اليقين الثلاث ونطاقُ الاستقراء، مُشتَقَّين من حوامل لا مكتوبَين.

ثلاثُ درجات لا سُلَّمٌ متدرِّج بينها: الانتقال بينها مشروطٌ بشروطٍ **نوعيّة**، لا
بعددٍ يكبر حتى ينقلب يقينًا. فالعددُ وحده لا يُنتج تواترًا، وتكرارُ الادّعاء لا
يُنتج قياسًا:

* **متواتر**: (١) علمٌ لا ظنّ، مستندٌ إلى مشاهدةٍ مباشرة لا إلى استنتاج؛
  (٢) استقلالُ مصادرَ يستحيل معه التواطؤ — لا حجمُ عيّنةٍ وحده؛ (٣) تكرارٌ عبر
  أجيالٍ أو دوراتٍ مستقلّة متعاقبة، لا دفعةً واحدة.
* **آحاد**: ظنٌّ مقبولٌ شرطيًّا، يحتاج تثبّتَ روايةٍ ودرايةٍ معًا قبل **كلّ**
  قبول، ولا يُعفى أبدًا من إعادة الفحص.
* **فرض**: مجرّدُ تقديرٍ لم يقع عليه حسٌّ مستقلٌّ بعد؛ ولا يتحوّل إلى آحادٍ أو
  تواترٍ إلا بقياسٍ مستقلٍّ فعليّ، لا بتكرار الادّعاء.

**لا حقلَ عددٍ في أيّ صنفٍ هنا** (§٤ من `docs/AIMS.md`: «التعدادُ خاصّيةٌ تُحسَب
لا حقلٌ يُكتَب»)، ويُفحَص ذلك عند الاستيراد على حقول الأصناف نفسها. وإدخالُ عددِ
مصادرَ هنا يُعيد بابَ «كثرةُ الرواة تُنتج تواترًا» الذي تُغلقه الشروط النوعيّة.

**الدرجةُ تُشتَقّ من ثلاثة حوامل مغلقة ولا تُكتَب**، على منوال حوامل
`word_class_formal.py`: أساسُ العلم، واستقلالُ المصادر، ونمطُ التكرار. وأيُّ
درجةٍ مكتوبةٍ تخالف المُشتَقّة تُرفَض عند الإنشاء، فلا موضعَ تُكتَب فيه النتيجة
مباشرةً.

**المتواتر مُعلَنٌ في المفردة وممتنعٌ عن الكسب الداخليّ بخطأٍ فئويّ، لا محجوزٌ
لغياب سلطة** (`TawaturRequiresDiachronicSuccession` في §G0.N من
`docs/CONSTITUTION.md`): التواترُ **بتعريفه** يشترط تعاقبَ أجيالٍ مستقلّةٍ
زمنيًّا — شهاداتٌ تَرِد في دوراتٍ متعاقبةٍ متباعدةٍ في الزمن — والمدوّنةُ
المغلقة **مقطعٌ متزامنٌ مُجمَّد**: نصٌّ واحدٌ لا يزيد ولا يتجدّد، فلا بُعدَ
زمنيَّ فيه يقع فيه التعاقبُ أصلًا. فسؤالُ «أمتواترٌ هذا؟» على بنيةٍ كهذه **غيرُ
مستقيم الوضع**، كسؤال «أمتواطئٌ العددُ خمسةٌ أم مشكَّك؟»؛ وهو غيرُ سؤالٍ بلا
جوابٍ بعد.

والفرقُ عمليّ لا لفظيّ: «حاولنا فلم نجد سلطة» يُنقَض بسلطةٍ تُبنى غدًا — وهو
بعينه ما تمنع `NoReachingWrite != ProvenUnreachable` أن يُقرَأ برهانًا — أمّا
«البنيةُ لا تحمل البُعدَ الذي يفترضه المفهوم» فلا تنقضه أداة، لأن العلّة في نوع
السؤال لا في عدّة الفحص. ولذلك يُفصَل **جنسُ الامتناع** في مفردةٍ مغلقة
(`UnconstructibilityGenus`) بدل دمج البابين في «غير قابلة للبناء» وحدها، على
منوال ما كشفه `DeferredValueShape` من أن الحجز أشكالٌ لا شكلٌ واحد: فعلى بنيةٍ
متزامنة الامتناعُ فئويّ، وعلى تعاقبٍ زمنيٍّ حقيقيّ يعود الامتناعُ حجزًا عاديًّا
لغياب سلطةٍ تفحص استقلالَ المصادر.

ويُرفَض إصدارُ الدرجة برسالته الخاصّة **قبل** الرسالة العامّة، كيلا يُقرَأ رفضٌ
فئويٌّ رفضًا أضعفَ مبنيًّا على نقص حامل.

**ولا مدخلَ استيرادٍ لادّعاء تواترٍ أجنبيّ هنا، والسببُ فئويٌّ مكتوبٌ لا
صامت**: لمّا كان الخطأ في نوع السؤال لا في السلطة، فلا معنى لاستيراد «ادّعاء
تواتر» ليُسجَّل على بنيةٍ لا يصحّ المفهومُ عليها؛ فيبقى `متواتر` عضوًا في
المفردة بلا مدخل، بخلاف `ForeignDeclaredCase` و`ImportedInferenceStanding` حيث
كان الامتناعُ سلطويًّا فصحّ فيه الاستيرادُ المُصرَّح به.

**الاستقراء نطاقان لا مبلغان من الدقّة**: تامٌّ داخل مجموعةٍ مغلقة فيُنتج يقينًا
**داخل حدودها**، وناقصٌ خارجها فيبقى ظنيًّا مهما اتّسع. وجملةُ النطاق **تُشتَقّ
ولا تُكتَب**: الحقلُ المكتوب يُقابَل بالمُشتَقّ ويُرفَض عند الاختلاف، فالتعميمُ
المباشر من مدوّنةٍ مغلقة إلى اللسان الذي أُخذت منه ممتنعٌ بنيويًّا لا مُتّقًى
بتحفّظٍ في النثر.

**إعفاءُ «المعلومات المنظّمة الأولى» سؤالٌ مفتوح لا إعفاءٌ ممنوح**: يُسجَّل بلا
حقل جوابٍ أصلًا، على منوال `Phase2OpenQuestion`، لأنّ بداهةَ الشيء عند الباحث
ليست تواترًا، والفرقُ بينهما هو بعينه ما تفصله الشروطُ النوعيّة أعلاه.

**خمولٌ سلطويّ**: `TransmissionStanding != BirthVerdict` و
`ScopedFinding != CertifiedResidual`؛ لا ولادةَ ولا تجميدَ ولا `E0`، ولا تقرأ
هذه الوحدةَ أيّ بوّابةٍ في `kernel/`، وحقولُ التدقيق الخارجيّ تبقى متطابقةً
بايتًا.

**والبقايا مُسمّاةٌ لا مطويّة** (`NAMED_RESIDUALS`)، ومنها أنّ جنسَ الامتناع
لا يُصنَّف هنا لأخوات هذا الحجز في الشجرة، وأنّ منشأ تطابق هذا التصميم مع نقاشٍ
سابق غيرُ متحقَّقٍ بشيءٍ في المستودع فلا يُقرَأ تحقّقًا مستقلًّا.
"""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass, fields
from enum import Enum
from types import MappingProxyType
from typing import Final

_FORBIDDEN_COUNT_FIELD_MARKERS: Final = (
    "count",
    "number",
    "size",
    "total",
    "verdict",
    "birth",
)


class TransmissionStandingError(ValueError):
    """درجةٌ أو نطاقٌ مرفوض؛ لا يُحمَل على أقرب درجةٍ مقبولة."""


class KnowledgeBasis(Enum):
    """حاملُ أساس العلم: أمشاهدةٌ مباشرة، أم استنتاجٌ من غيرها؟"""

    DIRECT_OBSERVATION = "مشاهدة_مباشرة"
    INFERENCE = "استنتاج"


class SourceIndependence(Enum):
    """حاملُ استقلال المصادر: أيستحيل التواطؤ، أم لم يُثبَت استحالتُه؟"""

    COLLUSION_IMPOSSIBLE = "يستحيل_معه_التواطؤ"
    NOT_ESTABLISHED = "غير_مُثبَت"


class RepetitionPattern(Enum):
    """حاملُ نمط التكرار: أأجيالٌ متعاقبة، أم دفعةٌ واحدة، أم لا تكرار؟"""

    SUCCESSIVE_GENERATIONS = "دورات_مستقلة_متعاقبة"
    SINGLE_BATCH = "دفعة_واحدة"
    NONE = "لا_تكرار"


class TransmissionStanding(Enum):
    """الدرجاتُ الثلاث، مفردةً مغلقة؛ ولا تدرّجَ بينها بل انتقالٌ بشروط."""

    MUTAWATIR = "متواتر"
    AHAD = "آحاد"
    FARD = "فرض"


class IstiqraScope(Enum):
    """نطاقُ الاستقراء: تامٌّ داخل مجموعةٍ مغلقة، أو ناقصٌ خارجها."""

    COMPLETE_WITHIN_CLOSED_SET = "تام_داخل_مجموعة_مغلقة"
    INCOMPLETE = "ناقص"


class ExemptionHypothesis(Enum):
    """احتمالاتُ سؤال الإعفاء الثلاثة كاملةً، فالثنائيةُ هنا كاذبة."""

    EXEMPT_BY_GENUINE_RECURRENCE = "مُعفاة_لبلوغها_تواترًا_حقيقيًّا"
    NOT_EXEMPT_MERE_SELF_EVIDENCE = "غير_معفاة_وبداهتها_ليست_تواترًا"
    EXEMPTION_QUESTION_ILL_POSED = "السؤال_نفسه_غير_مستقيم_الوضع"


class EvidenceTemporalStructure(Enum):
    """بنيةُ قاعدة الشواهد زمنيًّا: مقطعٌ متزامن، أو تعاقبٌ زمنيٌّ مستقلّ.

    المدوّنةُ المغلقة `مقطع_متزامن_مُجمَّد` بحكم كونها مغلقة: نصٌّ لا يزيد ولا
    يتجدّد لا يحمل بُعدًا زمنيًّا تقع فيه دوراتٌ متعاقبة.
    """

    SYNCHRONIC_FROZEN_SECTION = "مقطع_متزامن_مُجمَّد"
    DIACHRONIC_INDEPENDENT_SUCCESSION = "تعاقب_زمني_مستقل"


class UnconstructibilityGenus(Enum):
    """جنسُ امتناع قيمةٍ مُعلَنة: أحجزٌ لغياب سلطة، أم خطأٌ فئويّ بنيويّ؟

    ودمجُ الجنسين في «غير قابلة للبناء» وحدها يُسقط فارقًا عمليًّا: الأوّل
    تَرفعه سلطةٌ تُبنى غدًا، والثاني لا ترفعه أداةٌ لأن العلّة في نوع السؤال.
    والعضوُ الثالث لمن لم تُحسَم جهتُه، فلا يُحمَل على أقربهما.
    """

    HELD_BY_MISSING_AUTHORITY_TODAY = "محجوزة_لغياب_سلطة_اليوم"
    REFUSED_BY_STRUCTURAL_CATEGORY_MISMATCH = "ممتنعة_بخطأ_فئوي_بنيوي"
    GENUS_NOT_SETTLED = "جنس_الامتناع_غير_محسوم"


class TawaturQuestionStanding(Enum):
    """حالُ سؤال التواتر على بنيةٍ بعينها: أمستقيمُ الوضع أصلًا أم لا؟"""

    ILL_POSED_ON_THIS_STRUCTURE = "غير_مستقيم_الوضع_على_هذه_البنية"
    WELL_POSED_AND_UNVERIFIED_HERE = "مستقيم_الوضع_وغير_متحقق_هنا"


if len(TransmissionStanding) != 3:  # pragma: no cover - guard
    raise RuntimeError("the transmission standings are deliberately three")
if len(IstiqraScope) != 2:  # pragma: no cover - guard
    raise RuntimeError("induction scope is deliberately two-valued")
if len(ExemptionHypothesis) != 3:  # pragma: no cover - guard
    raise RuntimeError("the exemption question declares exactly three hypotheses")
if len(EvidenceTemporalStructure) != 2:  # pragma: no cover - guard
    raise RuntimeError("an evidence base is a synchronic section or a succession")
if len(UnconstructibilityGenus) != 3:  # pragma: no cover - guard
    raise RuntimeError("a hold is by authority, by category mismatch, or unsettled")
if len(TawaturQuestionStanding) != 2:  # pragma: no cover - guard
    raise RuntimeError("a question is ill-posed on a structure or well-posed on it")


CLOSED_CORPUS_TEMPORAL_STRUCTURE: Final = (
    EvidenceTemporalStructure.SYNCHRONIC_FROZEN_SECTION
)

TAWATUR_REQUIRES_DIACHRONIC_SUCCESSION_NOTE: Final = (
    "TawaturRequiresDiachronicSuccession: التواترُ بتعريفه يشترط تعاقبَ أجيالٍ "
    "مستقلّةٍ زمنيًّا، والمدوّنةُ المغلقة مقطعٌ متزامنٌ مُجمَّد لا يزيد ولا "
    "يتجدّد؛ فلا بُعدَ زمنيَّ فيها يقع فيه التعاقبُ أصلًا"
)

CATEGORY_MISMATCH_IS_NOT_MISSING_AUTHORITY_NOTE: Final = (
    "الامتناعُ الفئويّ غيرُ الحجز لغياب سلطة: الحجزُ ترفعه سلطةٌ تُبنى غدًا، "
    "والخطأُ الفئويّ لا ترفعه أداةٌ لأن العلّة في نوع السؤال لا في عدّة الفحص؛ "
    "فسؤالُ التواتر على بنيةٍ متزامنة باطلُ الصياغة لا بلا جوابٍ بعد"
)

NO_IMPORT_ENTRY_FOR_A_FOREIGN_RECURRENCE_CLAIM_NOTE: Final = (
    "لا مدخلَ استيرادٍ لادّعاء تواترٍ أجنبيّ، والسببُ فئويٌّ لا سلطويّ: استيرادُ "
    "ادّعاءٍ مُصرَّحٍ غيرِ متحقَّق يصحّ حيث يصحّ المفهومُ على البنية ويُعوز "
    "الفحصُ وحده، ولا يصحّ حيث لا يستقيم السؤالُ أصلًا؛ فيبقى `متواتر` عضوًا "
    "بلا مدخل، وسببُ ذلك مكتوبٌ هنا لا مطويّ"
)


MUTAWATIR_IS_UNCONSTRUCTIBLE_NOTE: Final = (
    "المتواترُ مُعلَنٌ وممتنعٌ عن الكسب الداخليّ بخطأٍ فئويٍّ بنيويّ لا بغياب "
    "سلطةٍ اليوم: التواترُ يشترط تعاقبَ أجيالٍ مستقلّةٍ زمنيًّا، والمدوّنةُ "
    "المغلقة مقطعٌ متزامنٌ مُجمَّد لا بُعدَ زمنيَّ فيه؛ فسؤالُ التواتر عليها "
    "غيرُ مستقيم الوضع، لا سؤالٌ بلا جوابٍ بعد ترفعه سلطةٌ تُبنى غدًا"
)

COUNT_IS_NOT_RECURRENCE_NOTE: Final = (
    "حجمُ العيّنة ليس استقلالًا، وكثرةُ النقل ليست تعاقبَ أجيال: الشروطُ نوعيّةٌ "
    "لا عدديّة، فلا حقلَ عددٍ هنا يُرقّي درجةً"
)

FARD_NEEDS_MEASUREMENT_NOT_REPETITION_NOTE: Final = (
    "الفرضُ تقديرٌ لم يقع عليه حسٌّ مستقلٌّ بعد؛ ولا يتحوّل إلى آحادٍ أو تواترٍ "
    "إلا بقياسٍ مستقلٍّ فعليّ، وتكرارُ الادّعاء ليس قياسًا"
)

AHAD_IS_NEVER_EXEMPT_FROM_RECHECK_NOTE: Final = (
    "الآحادُ مقبولٌ شرطيًّا: يحتاج تثبّتَ روايةٍ ودرايةٍ معًا قبل كلّ قبول، ولا "
    "يُعفى أبدًا من إعادة الفحص مهما تكرّر قبولُه سابقًا"
)

DIRECT_GENERALIZATION_IS_REFUSED_NOTE: Final = (
    "استقراءٌ تامٌّ داخل مدوّنةٍ مغلقة يُنتج يقينًا داخل حدودها وحدها؛ والتعميمُ "
    "المباشر على اللسان الذي أُخذت منه يبقى ظنيًّا حتى يُستقرَأ كوربصٌ مستقلٌّ "
    "ثانٍ، فجملةُ النطاق تُشتَقّ ولا تُكتَب"
)

TRANSMISSION_AUTHORITY_NOTE: Final = (
    "تسجيلٌ فقط: لا تُصدر هذه الوحدة ولادةً ولا حكمًا ولا تجميدًا ولا `E0`، ولا "
    "تقرؤها أيّ بوّابةٍ في النواة"
)

SUCCESSION_CARRIER_IS_WRITABLE_WITHOUT_A_TEMPORAL_AUTHORITY: Final = (
    "SUCCESSION_CARRIER_IS_WRITABLE_WITHOUT_A_TEMPORAL_AUTHORITY"
)

SIBLING_HOLDS_ARE_NOT_CLASSIFIED_HERE: Final = "SIBLING_HOLDS_ARE_NOT_CLASSIFIED_HERE"

DESIGN_CONVERGENCE_PROVENANCE_IS_UNVERIFIED: Final = (
    "DESIGN_CONVERGENCE_PROVENANCE_IS_UNVERIFIED"
)

NAMED_RESIDUALS: Final[Mapping[str, str]] = MappingProxyType(
    {
        SUCCESSION_CARRIER_IS_WRITABLE_WITHOUT_A_TEMPORAL_AUTHORITY: (
            "`RepetitionPattern.SUCCESSIVE_GENERATIONS` يبقى حاملًا يُكتَب، ولا "
            "سلطةَ هنا تشتقّ بنيةَ قاعدة الشواهد زمنيًّا من الخبر نفسه؛ "
            "فكاتبُه على خبرٍ مأخوذٍ من مدوّنةٍ مغلقة يقع في الخطأ الفئويّ "
            "نفسه، ويُدرِكه رفضُ الدرجة لا رفضُ الحامل. وربطُ الخبر ببنيته "
            "الزمنية مشروطٌ بسلطةٍ لا توجد اليوم، فهو حجزٌ لغياب سلطة لا "
            "امتناعٌ فئويّ، ولا يُحسَم هنا بتشديد الحوامل"
        ),
        SIBLING_HOLDS_ARE_NOT_CLASSIFIED_HERE: (
            "في الشجرة قيمٌ مُعلَنةٌ أخرى غيرُ قابلةٍ للبناء "
            "(`ImportedInferenceStanding.VERIFIED_LOCALLY`، "
            "و`OntologicalLayer.PHYSICAL_EXISTENCE`، "
            "و`QuestionStatus.CLOSED_BY_FROZEN_EXPERIMENT`)، ولا تُصنَّف "
            "أجناسُ امتناعها هنا: تصنيفُ حجزٍ في وحدةٍ أخرى حكمٌ على وحدةٍ لا "
            "تملكه هذه، والاستبعادُ مُسمّى لا مطويّ"
        ),
        DESIGN_CONVERGENCE_PROVENANCE_IS_UNVERIFIED: (
            "تطابقُ هذا التصميم مع نقاشٍ خارجيٍّ سابق واقعةٌ لا يملك المستودعُ "
            "ما يفحص منشأها: أتزامنٌ مستقلّ هو أم أثرُ عرضٍ مباشر؟ لا شيءَ هنا "
            "يُقرَأ منه الجواب، فيُسجَّل السؤالُ ولا يُحسَم، ولا يُستشهَد "
            "بالتطابق تحقّقًا مستقلًّا لأيّ قرارٍ في هذه الوحدة"
        ),
    }
)


def unconstructibility_genus(
    structure: EvidenceTemporalStructure,
) -> UnconstructibilityGenus:
    """اشتقّ جنسَ امتناع `متواتر` من بنية قاعدة الشواهد؛ دالّةٌ تامّة بلا فرعٍ افتراضيّ.

    على المقطع المتزامن الامتناعُ فئويّ فلا ترفعه أداة؛ وعلى التعاقب الزمنيّ
    الحقيقيّ يعود حجزًا عاديًّا لغياب سلطةٍ تفحص استقلالَ المصادر عبر الدورات.
    """

    if not isinstance(structure, EvidenceTemporalStructure):
        raise TransmissionStandingError("بنيةُ قاعدة الشواهد من مفردتها المغلقة")
    if structure is EvidenceTemporalStructure.SYNCHRONIC_FROZEN_SECTION:
        return UnconstructibilityGenus.REFUSED_BY_STRUCTURAL_CATEGORY_MISMATCH
    return UnconstructibilityGenus.HELD_BY_MISSING_AUTHORITY_TODAY


def tawatur_question_standing(
    structure: EvidenceTemporalStructure,
) -> TawaturQuestionStanding:
    """أمستقيمُ الوضع سؤالُ التواتر على هذه البنية؟ مُشتَقٌّ من البنية لا مكتوب."""

    if unconstructibility_genus(structure) is (
        UnconstructibilityGenus.REFUSED_BY_STRUCTURAL_CATEGORY_MISMATCH
    ):
        return TawaturQuestionStanding.ILL_POSED_ON_THIS_STRUCTURE
    return TawaturQuestionStanding.WELL_POSED_AND_UNVERIFIED_HERE


def _require_non_blank(value: str, field_name: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise TransmissionStandingError(f"{field_name} نصٌّ غير فارغ")
    return value


def derive_standing(
    basis: KnowledgeBasis,
    independence: SourceIndependence,
    repetition: RepetitionPattern,
) -> TransmissionStanding:
    """اشتقّ الدرجةَ من حواملها الثلاثة؛ دالّةٌ تامّةٌ بلا فرعٍ افتراضيّ."""

    for value, expected, name in (
        (basis, KnowledgeBasis, "حاملُ أساس العلم"),
        (independence, SourceIndependence, "حاملُ استقلال المصادر"),
        (repetition, RepetitionPattern, "حاملُ نمط التكرار"),
    ):
        if not isinstance(value, expected):
            raise TransmissionStandingError(f"{name} من مفردته المغلقة")

    if basis is KnowledgeBasis.INFERENCE:
        return TransmissionStanding.FARD
    if (
        independence is SourceIndependence.COLLUSION_IMPOSSIBLE
        and repetition is RepetitionPattern.SUCCESSIVE_GENERATIONS
    ):
        return TransmissionStanding.MUTAWATIR
    return TransmissionStanding.AHAD


@dataclass(frozen=True, slots=True)
class TransmissionStandingRecord:
    """درجةُ خبرٍ واحد بحواملها الثلاثة، مُشتَقّةً ومُقابَلةً بالمكتوب."""

    report_id: str
    basis: KnowledgeBasis
    independence: SourceIndependence
    repetition: RepetitionPattern
    declared_standing: TransmissionStanding
    justification: str

    def __post_init__(self) -> None:
        _require_non_blank(self.report_id, "معرّف الخبر")
        _require_non_blank(self.justification, "تبرير الدرجة")
        if not isinstance(self.declared_standing, TransmissionStanding):
            raise TransmissionStandingError("الدرجةُ المكتوبة من مفردتها المغلقة")

        derived = derive_standing(self.basis, self.independence, self.repetition)
        if derived is TransmissionStanding.MUTAWATIR:
            raise TransmissionStandingError(MUTAWATIR_IS_UNCONSTRUCTIBLE_NOTE)
        if self.declared_standing is TransmissionStanding.MUTAWATIR:
            raise TransmissionStandingError(MUTAWATIR_IS_UNCONSTRUCTIBLE_NOTE)
        if self.declared_standing is not derived:
            raise TransmissionStandingError(
                "الدرجةُ المكتوبة تخالف المُشتَقّة من الحوامل: "
                f"{self.declared_standing.value} مكتوبةً و{derived.value} مُشتَقّة"
            )

    @property
    def standing(self) -> TransmissionStanding:
        """الدرجةُ المُشتَقّة من الحوامل، لا المكتوبةُ بجانبها."""

        return derive_standing(self.basis, self.independence, self.repetition)

    @property
    def requires_recheck_before_every_acceptance(self) -> bool:
        """أيلزم تثبّتٌ جديد قبل كلّ قبول؟ نعم في الدرجتين المتاحتين هنا."""

        return True

    @property
    def awaits_independent_measurement(self) -> bool:
        """أينتظر هذا الخبرُ قياسًا مستقلًّا لم يقع بعد؟ مُشتَقٌّ لا مكتوب."""

        return self.standing is TransmissionStanding.FARD


def derive_scope_statement(
    scope: IstiqraScope, enumerated_set: str, wider_set: str
) -> str:
    """اشتقّ جملةَ النطاق الواجبة؛ لا موضعَ تُكتَب فيه هذه الجملةُ حرًّا."""

    if not isinstance(scope, IstiqraScope):
        raise TransmissionStandingError("نطاقُ الاستقراء من مفردته المغلقة")
    enumerated = _require_non_blank(enumerated_set, "المجموعة المُستقرأة").strip()
    wider = _require_non_blank(wider_set, "المجموعة الأوسع").strip()
    if scope is IstiqraScope.COMPLETE_WITHIN_CLOSED_SET:
        return (
            f"ثبت الأمر يقينًا داخل {enumerated}، ويبقى ظنيًّا بخصوص {wider} "
            "حتى يُستقرَأ كوربصٌ مستقلٌّ ثانٍ"
        )
    return (
        f"لم يُستقرَأ {enumerated} استقراءً تامًّا، فيبقى الأمر ظنيًّا داخله "
        f"وبخصوص {wider} معًا"
    )


@dataclass(frozen=True, slots=True)
class ScopedFinding:
    """نتيجةٌ بنطاقها: الجملةُ مُشتَقّةٌ من المجموعتين، والمكتوبُ يُقابَل بها."""

    finding_id: str
    scope: IstiqraScope
    enumerated_set: str
    wider_set: str
    declared_statement: str

    def __post_init__(self) -> None:
        _require_non_blank(self.finding_id, "معرّف النتيجة")
        _require_non_blank(self.enumerated_set, "المجموعة المُستقرأة")
        _require_non_blank(self.wider_set, "المجموعة الأوسع")
        _require_non_blank(self.declared_statement, "جملة النطاق المكتوبة")
        if not isinstance(self.scope, IstiqraScope):
            raise TransmissionStandingError("نطاقُ الاستقراء من مفردته المغلقة")
        if self.enumerated_set.strip() == self.wider_set.strip():
            raise TransmissionStandingError(
                "المجموعةُ المُستقرأة والمجموعةُ الأوسع واحدة: فلا نطاقَ يُتجاوَز "
                "أصلًا، وتسجيلُ ذلك يُوهم حدًّا لا وجود له"
            )
        if self.declared_statement.strip() != self.derived_statement:
            raise TransmissionStandingError(
                f"جملةُ النطاق تُشتَقّ ولا تُكتَب. {DIRECT_GENERALIZATION_IS_REFUSED_NOTE}"
            )

    @property
    def derived_statement(self) -> str:
        """جملةُ النطاق الواجبة، مُشتَقّةً من النطاق والمجموعتين وحدها."""

        return derive_scope_statement(self.scope, self.enumerated_set, self.wider_set)

    @property
    def is_certain_within_the_enumerated_set(self) -> bool:
        """أيقينٌ داخل المجموعة المُستقرأة؟ مُشتَقٌّ من النطاق لا مكتوب."""

        return self.scope is IstiqraScope.COMPLETE_WITHIN_CLOSED_SET

    @property
    def is_certain_beyond_the_enumerated_set(self) -> bool:
        """`False` بنيويًّا: لا استقراءَ تامٌّ يُخرج يقينًا من حدوده."""

        return False


@dataclass(frozen=True, slots=True)
class ExemptionOpenQuestion:
    """سؤالُ إعفاء المعلومات المنظّمة الأولى: احتمالاته كلّها، ولا جوابَ فيه."""

    question_id: str
    hypotheses: tuple[ExemptionHypothesis, ...]
    why_open: str

    def __post_init__(self) -> None:
        _require_non_blank(self.question_id, "معرّف السؤال")
        _require_non_blank(self.why_open, "سبب بقاء السؤال مفتوحًا")
        if not isinstance(self.hypotheses, tuple):
            raise TransmissionStandingError("الاحتمالات تُعلَن مجموعةً مرتَّبة")
        for hypothesis in self.hypotheses:
            if not isinstance(hypothesis, ExemptionHypothesis):
                raise TransmissionStandingError("كلُّ احتمالٍ من مفردته المغلقة")
        if set(self.hypotheses) != set(ExemptionHypothesis) or len(
            self.hypotheses
        ) != len(ExemptionHypothesis):
            raise TransmissionStandingError(
                "السؤالُ المفتوح يُعلِن احتمالاته كلّها بلا تكرار؛ وإسقاطُ احتمالٍ "
                "منها يصنع ثنائيةً كاذبة"
            )

    @property
    def remains_open(self) -> bool:
        """هل بقي السؤال بلا جواب؟ نعم دائمًا في هذه المرحلة، بنيويًّا."""

        return True


FIRST_ORGANIZED_INFORMATION_QUESTION: Final = ExemptionOpenQuestion(
    question_id="first-organized-information-exemption",
    hypotheses=tuple(ExemptionHypothesis),
    why_open=(
        "الإعفاءُ من بروتوكول الولادة الكامل مشروطٌ ببلوغ تواترٍ حقيقيّ بالمعنى "
        "النوعيّ أعلاه — إجماعٌ مؤسّسيّ أو علميّ مستقلٌّ عبر مصادرَ متنوّعةٍ "
        "فعلًا — لا بمجرّد بداهةِ الأمر عند الباحث؛ ولا سلطةَ هنا تفحص ذلك، فلا "
        "يُسجَّل إعفاءٌ ممنوح ولا مَنعٌ مُثبَت، بل سؤالٌ مفتوحٌ باحتمالاته الثلاثة"
    ),
)


def _assert_no_fields_matching(
    declaring_type: type, markers: tuple[str, ...], message: str
) -> None:
    for item in fields(declaring_type):
        if any(marker in item.name for marker in markers):
            raise RuntimeError(message)


for _declaring_type in (
    TransmissionStandingRecord,
    ScopedFinding,
    ExemptionOpenQuestion,
):
    _assert_no_fields_matching(
        _declaring_type,
        _FORBIDDEN_COUNT_FIELD_MARKERS,
        "no type here may carry a count, size, verdict, or birth field",
    )


__all__ = [
    "AHAD_IS_NEVER_EXEMPT_FROM_RECHECK_NOTE",
    "CATEGORY_MISMATCH_IS_NOT_MISSING_AUTHORITY_NOTE",
    "CLOSED_CORPUS_TEMPORAL_STRUCTURE",
    "COUNT_IS_NOT_RECURRENCE_NOTE",
    "DESIGN_CONVERGENCE_PROVENANCE_IS_UNVERIFIED",
    "DIRECT_GENERALIZATION_IS_REFUSED_NOTE",
    "FARD_NEEDS_MEASUREMENT_NOT_REPETITION_NOTE",
    "FIRST_ORGANIZED_INFORMATION_QUESTION",
    "MUTAWATIR_IS_UNCONSTRUCTIBLE_NOTE",
    "NAMED_RESIDUALS",
    "NO_IMPORT_ENTRY_FOR_A_FOREIGN_RECURRENCE_CLAIM_NOTE",
    "SIBLING_HOLDS_ARE_NOT_CLASSIFIED_HERE",
    "SUCCESSION_CARRIER_IS_WRITABLE_WITHOUT_A_TEMPORAL_AUTHORITY",
    "TAWATUR_REQUIRES_DIACHRONIC_SUCCESSION_NOTE",
    "TRANSMISSION_AUTHORITY_NOTE",
    "EvidenceTemporalStructure",
    "ExemptionHypothesis",
    "ExemptionOpenQuestion",
    "IstiqraScope",
    "KnowledgeBasis",
    "RepetitionPattern",
    "ScopedFinding",
    "SourceIndependence",
    "TawaturQuestionStanding",
    "TransmissionStanding",
    "TransmissionStandingError",
    "TransmissionStandingRecord",
    "UnconstructibilityGenus",
    "derive_scope_statement",
    "derive_standing",
    "tawatur_question_standing",
    "unconstructibility_genus",
]
