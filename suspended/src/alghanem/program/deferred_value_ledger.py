"""القارئ الثالث: القيم المُعلَنة غير القابلة للبناء، مقروءةً من الشيفرة نفسها.

هذه **المرحلة الثالثة من الطور الثاني** لـ AIM.1. §٤ من `docs/AIMS.md` تُسمّي
ثلاثة مصادر اشتقاقٍ مرشَّحة، «كلّها مقروءةٌ آليًّا وغيرُ تقديرية»؛ وقامت اثنتان
منها في `alghanem.program.constitution_ledger` (تعداد صفوف الدستور، وتعداد
أسئلة التدقيق). وهذه الوحدة تُنشئ **الثالث وحده**: تعدادُ القيم المُعلَنة غير
القابلة للبناء التي ما زالت تحجز غايةً بعينها، وهي الثلاث التي تُسمّيها §٤
نصًّا: `BIRTH_IN_SCOPE` و`MORPHO_FUNCTIONAL` و`CLOSED_BY_FROZEN_EXPERIMENT`::

    SourceCode        != DerivedLedger
    DerivedCount      != Indicator
    DeclaredValue     != ConstructibleValue
    NoReachingWrite   != ProvenUnreachable

**المصدر شيفرةٌ لا نثر.** القارئان السابقان يقرآن وثيقةً؛ وهذا يقرأ شجرة
`src/` نفسها: يستورد المفردة حيًّا فيتحقّق أن العضو ما زال قائمًا باسمه، ثم
يُحلّل نصّ الوحدة التي تحجزه (`ast`) فيستخرج موضع الحجز وشكله. فإعادةُ تسمية
عضوٍ أو نقلُ حجزه يُرفَع بها خطأٌ باسمها، ولا تُقرَأ «لم يعد محجوزًا».

**المصدر التصميمي المباشر، مُستشهَدًا به لا مُعادًا اشتقاقه.** شكلُ «الجهةُ
تُعلن، والقارئ لا يقبل إلا من مفردةٍ مغلقة يملكها هو، والمخالفة تُرفَض عند
الإنشاء» مأخوذٌ من سؤال التدقيق المفتوح
`DeclaredVersusDerivedRecurrenceNotExplained` بوصفه **مصدرًا مباشرًا** (إلزام §٥
من `docs/AIMS.md`)، لا بوصفه بديهةً تُعاد هنا صامتةً. وذلك السؤال مرصودٌ غير
مفسَّر، فلا يُستحدَث له اسمٌ عامّ ولا صنفُ أساسٍ مشترك يوحّد الشكل بين القرّاء
الثلاثة؛ يُستعمل في موضعه ويُنسَب إلى سؤاله. وهنا يظهر الشكلُ في موضعه الأصدق:
كلّ صفٍّ يحمل **الشكل المُعلَن** في مفردة المواضع و**الشكل المُشتَقّ** من نصّ
الشيفرة معًا، واختلافُهما يُرفَض عند الإنشاء ولا يُقرَّر.

**شكلُ الحجز ثلاثيٌّ لا واحد**، وهو ما كشفه الترميز لا ما فُرض عليه:

* `REFUSED_BY_NAMING_THE_VALUE`: حارسٌ يُسمّي العضو نفسه ثم يرفع خطأً.
* `REFUSED_BY_ADMITTING_ONLY_A_SIBLING`: حارسٌ لا يُسمّي العضو البتّة، بل يقبل
  أخاه وحده في مفردةٍ ثنائية القيمة؛ فالحجزُ مُستلزَمٌ من قائمة قبولٍ وحجمِ
  مفردة، لا مكتوبٌ في موضع.
* `UNREACHABLE_FROM_SOLE_AUTHORITY`: لا حارس أصلًا ولا خطأ؛ السلطةُ الوحيدة
  التي تُصدر القيمة لا تكتبها في أيّ موضع، فمجالُها المُشتَقّ لا يحوي العضو.

ودمجُ الثلاثة في «غير قابلة للبناء» وحدها يُسقط فارقًا قائمًا: الأول يُرفَع به
خطأٌ عند المحاولة، والثاني لا يُذكر فيه العضو فلا يُعثَر عليه بالبحث عن اسمه،
والثالث لا يُرفَع به خطأٌ أصلًا لأن لا محاولةَ تُرفَض. فالمفردة ثلاثية.

**التعداد خاصّيةٌ تُحسَب لا حقلٌ يُكتَب** (§٤): لا حقلَ عددٍ في أيّ صنفٍ هنا.

**الرفض لا التخطّي الصامت.** موضعٌ مُعلَن لا يُعثَر على حجزه في نصّ وحدته يُوقف
القراءة باسمه، ولا يُتخطّى؛ والتخطّي يُنتج دفترًا ناقصًا يُقرَأ لاحقًا «لم تعد
هذه القيمة محجوزة»، وهو ادّعاءُ انفراجٍ لم يحدث. وترتفع القاعدة طبقةً كما ارتفعت
في القارئ السابق من الخلية إلى الجدول: يُحصى **كلّ** حارسٍ على مفرداتٍ متتبَّعة
في الوحدات الممسوحة (`GuardCensus`)، فالحارسُ الذي لا يقابله موضعٌ مُعلَن حاضرٌ
في الإحصاء لا مطويّ.

**الجهل والبقيّة مُسمّيان لا مطويّان** (`NAMED_RESIDUALS`): ما لم يُغلَق هنا
مكتوبٌ في الشيفرة لا في النثر وحده، ويُفحَص آليًّا.

**لا مؤشر هنا، ولا ربط بغاية.** لا تستورد هذه الوحدة `AimRecord` ولا `AimId`
ولا `AttainmentStanding`، ولا تحمل حقلًا يُنسَب إلى غاية. فربطُ العدد بالغاية هو
المؤشر بعينه، وهو المرحلة التالية المُقيَّدة سلفًا بـ§٤.

**خمولٌ سلطويّ**: `DeferredValueLedger != BirthVerdict`؛ لا تُصدر هذه الوحدة
ولادةً ولا حكمًا ولا تجميدًا ولا `E0`، ولا تُغيّر حالة أيّ قيمةٍ تقرؤها ولا
تُرقّيها، ولا تقرؤها أيّ وحدةٍ في `kernel/`، وهو ما يفحصه اختبارٌ يمسح وحداتها.

**وترتيب الصفوف ترتيبُ ورود الأسماء في §٤**، لا ترتيبَ أهمّية ولا أولوية (§٦).

---

**ما أضافته المرحلة العاشرة إلى هذه الوحدة (إعادةُ فتحٍ لا مطالبةٌ أولى).**
تركت المرحلةُ التاسعة سؤالًا مُعلَّقًا باسمه: أيحتاج «غائبٌ في الأثر المقروء»
تفريعًا بين «لم يُبحَث عنه في هذا المصدر» و«بُحِث فلم يُوجَد»؟ وقد نُصَّ هناك
على أنه لا يُحسَم إلا على أثر هذا القارئ لا على أثر وحدة الغايات؛ فيُحسَم هنا
على أثره::

    Mention        != Construction
    NotSearched    != NotFound
    ReadForms      != AllForms
    ExhaustedSource!= ExhaustedWorld

والجواب: **يحتاج، وينقسم ثلاثًا لا اثنتين** (`AbsenceGenus`). فبين «لم يُبحَث»
و«بُحِث فلم يُوجَد» تقع حالةٌ ثالثة قائمةٌ بنيويًّا: بحثٌ جرى وفي النصّ صيغةٌ
لا يقرأ هذا القارئ عضوَها، فبقي بحثُه غيرَ مستقصٍ. ولولا الثالثة لوجب حملُ
البحث غير المستقصي على إحدى الأُخريين، وكلاهما كذبٌ في اتجاه.

* **والجنسُ مُشتَقٌّ من موضع الحجز لا مكتوبٌ في حقل**: البحث في مجال السلطة لا
  يجري إلا حيث كان الحجز `UNREACHABLE_FROM_SOLE_AUTHORITY`؛ فالموضعان
  الآخران وُجد حجزُهما بحارسٍ قبل أن يُسأل عن مجال سلطة، فهما «لم يُبحَث» لا
  «بُحِث فلم يُوجَد». واختلافُ الجنس عن شكل الحجز يُرفَض عند الإنشاء.
* **ومن ادّعى بحثًا لزمه نطاقُه**: صفٌّ يحمل جنسًا فيه بحثٌ بلا `searched_forms`
  يُرفَض عند الإنشاء (`SEARCH_SCOPE_IS_REQUIRED_OF_THE_SEARCHER_NOTE`)، ودعوى
  استقصاءٍ مع موضعٍ غير مقروء تُرفَض كذلك، وبحثٌ مُعلَنٌ غيرُ مستقصٍ بلا موضعٍ
  يُسمّي مانعَه يُرفَض ثالثًا.
* **وصيغُ الإشارة أربعٌ مقروءةٌ من موضعها في الشجرة لا من دلالةٍ تُقدَّر**
  (`ReferenceForm`)، والرابعةُ `UNREAD_FORM` **حملٌ على الأضعف** لا سلّةَ طيّ:
  ما لم يُقرَأ موضعُه يُسجَّل طريقًا قد يُنتج أيّ عضو، فيمنع دعوى الاستقصاء.
* **وما كشفه الترميز فبدّل قراءةً قائمة**: `BIRTH_IN_SCOPE` **مكتوبٌ** في نصّ
  سلطته الوحيدة، طرفًا في مقارنة، ومع ذلك لا تبلغه. فالذكرُ ليس إنتاجًا
  (`members_mentioned_without_construction`)، وغيابُه عن مجال السلطة ليس غيابًا
  عن النصّ؛ وقراءةُ «لا يُذكر أصلًا» كانت ستكون خطأً لو قِيلت.
* **والحدُّ لم يُمَسّ**: لا يُقرَأ جنسُ الغياب رفعًا لحجزٍ ولا قربًا منه،
  و`NOT_SEARCHED_AT_THIS_SITE` ليست درجةً أدنى في سُلَّم عثور
  (`NOT_SEARCHED_IS_NOT_A_WEAKER_FOUND_NOTE`).
"""

from __future__ import annotations

import ast
import importlib
from collections.abc import Mapping
from dataclasses import dataclass
from enum import Enum
from pathlib import Path
from types import MappingProxyType
from typing import Final

from .aims import DESIGN_SOURCE_OPEN_QUESTION

SECTION_4_DECLARED_VALUE_NAMES: Final = (
    "BIRTH_IN_SCOPE",
    "MORPHO_FUNCTIONAL",
    "CLOSED_BY_FROZEN_EXPERIMENT",
)

DEFERRED_VALUE_LEDGER_AUTHORITY_NOTE: Final = (
    "قراءةٌ فقط: لا يُنتج هذا الدفتر ولادةً ولا حكمًا ولا تجميدًا ولا `E0`، "
    "ولا يرفع الحجز عن قيمةٍ ولا يُرقّيها، ولا تقرؤه بوّابةٌ في النواة"
)

NO_INDICATOR_IN_THIS_READER_NOTE: Final = (
    "لا مؤشر في هذه المرحلة ولا ربطَ بغاية: القارئ الثالث وحده مُنشأٌ هنا، "
    "وربطُ العدد بغايةٍ بعينها هو المؤشر نفسه، وهو مرحلةٌ تالية"
)

DESIGN_SOURCE_CITATION_NOTE: Final = (
    "شكلُ «الجهة تُعلن، والقارئ لا يقبل إلا من مفردةٍ مغلقة يملكها، والمخالفة "
    f"تُرفَض» مأخوذٌ من `{DESIGN_SOURCE_OPEN_QUESTION}` مصدرًا مباشرًا، لا "
    "بديهةً تُعاد هنا صامتةً"
)

MISSING_HOLD_IS_REFUSED_NOTE: Final = (
    "موضعٌ مُعلَن لا يُعثَر على حجزه في نصّ وحدته يُوقف القراءة باسمه: "
    "دفترٌ ناقصٌ يُقرَأ «لم تعد القيمة محجوزة»، وهو ادّعاءُ انفراجٍ لم يحدث"
)

SHAPE_DISAGREEMENT_IS_REFUSED_NOTE: Final = (
    "شكلُ حجزٍ مُعلَنٌ يخالف المُشتَقّ من نصّ الشيفرة يُرفَض عند الإنشاء ولا "
    "يُقرَّر: القيمة المُعلَنة لا تُصحِّح الأثر، والأثر لا يُعاد كتابته لها"
)

THREE_SHAPES_ARE_NOT_ONE_NOTE: Final = (
    "أشكال الحجز ثلاثة لا شكلٌ واحد: حارسٌ يُسمّي العضو، وحارسٌ يقبل أخاه "
    "وحده فلا يُذكر العضو أصلًا، وسلطةٌ لا تكتب العضو في أيّ موضع فلا يُرفَع "
    "خطأٌ أصلًا؛ ودمجُها يُسقط فارقًا قائمًا اليوم"
)

ABSENCE_IS_NOT_ONE_CATEGORY_NOTE: Final = (
    "غيابُ العضو من مجال سلطته ليس مقولةً واحدة: موضعٌ لم يجرِ فيه بحثٌ أصلًا "
    "لأن حجزه وُجد قبله، وموضعٌ بُحِث في نصّه كلِّه بصيغٍ مقروءة فلم يُوجَد، "
    "وموضعٌ بُحِث فيه وفي نصّه صيغةٌ لا تُقرَأ فبقي بحثُه غيرَ مستقصٍ. ودمجُها "
    "في «غائبٌ في الأثر المقروء» يُسوّي بين من لم يبحث ومن بحث فلم يجد"
)

SEARCH_SCOPE_IS_REQUIRED_OF_THE_SEARCHER_NOTE: Final = (
    "من أعلن «بُحِث فلم يُوجَد» لزمه نطاقُ بحثٍ مقروء — صيغُ الإشارة التي "
    "قرأها فعلًا — ويُرفَض عند الإنشاء بدونه: دعوى بحثٍ بلا نطاقٍ مقروء "
    "استقصاءٌ مُدّعًى، وهي أقوى من دعوى «لم أبحث» بلا زيادة دليل"
)

NOT_SEARCHED_IS_NOT_A_WEAKER_FOUND_NOTE: Final = (
    "`NOT_SEARCHED_AT_THIS_SITE` ليست درجةً أدنى في سُلَّم عثورٍ ولا منزلةً "
    "بين الوجود والعدم: هي تصريحٌ بأن هذا القارئ لم يُجرِ بحثًا في ذلك "
    "الموضع، ولا تُقرَأ ترجيحًا لأحد الطرفين"
)

REFUSAL_SHAPE_IS_NOT_A_DECLARED_VOCABULARY: Final = (
    "REFUSAL_SHAPE_IS_NOT_A_DECLARED_VOCABULARY"
)

SIBLING_ADMISSION_REFUSAL_DEPENDS_ON_VOCABULARY_SIZE: Final = (
    "SIBLING_ADMISSION_REFUSAL_DEPENDS_ON_VOCABULARY_SIZE"
)

CODOMAIN_DERIVED_FROM_LITERAL_WRITES_ONLY: Final = (
    "CODOMAIN_DERIVED_FROM_LITERAL_WRITES_ONLY"
)

SECTION_4_NAMES_THREE_VALUES_ONLY: Final = "SECTION_4_NAMES_THREE_VALUES_ONLY"

SEARCH_SCOPE_IS_DECLARED_NOT_PROVEN: Final = "SEARCH_SCOPE_IS_DECLARED_NOT_PROVEN"

FORM_VOCABULARY_IS_READ_NOT_LAWFUL: Final = "FORM_VOCABULARY_IS_READ_NOT_LAWFUL"

SEARCHED_OVER_UNREAD_FORMS_IS_UNOCCUPIED_TODAY: Final = (
    "SEARCHED_OVER_UNREAD_FORMS_IS_UNOCCUPIED_TODAY"
)

NAMED_RESIDUALS: Final[Mapping[str, str]] = MappingProxyType(
    {
        REFUSAL_SHAPE_IS_NOT_A_DECLARED_VOCABULARY: (
            "أشكال الحجز الثلاثة مُستخرَجةٌ من شيفرة هذا المستودع اليوم، ولا "
            "صفَّ في `docs/CONSTITUTION.md` يُصرّح بأن الحجز يلزمه أحدها؛ "
            "فشكلٌ رابع يُستحدَث غدًا يُرفَع به خطأٌ هنا باسمه، لكنّ شيئًا في "
            "السجلّ لا يُلزم الحاجز بأن يأخذ شكلًا من هذه الثلاثة أصلًا"
        ),
        SIBLING_ADMISSION_REFUSAL_DEPENDS_ON_VOCABULARY_SIZE: (
            "حجزُ العضو بقبول أخيه وحده غيرُ مكتوبٍ في أيّ موضع: هو مُستلزَمٌ "
            "من قائمة قبولٍ ومن كون المفردة ثنائية القيمة، ويُفحَص العدد حيًّا "
            "هنا؛ فإضافةُ عضوٍ ثالثٍ غدًا تُبقي العضو محجوزًا وتُضيف محجوزًا "
            "آخر بلا موضعٍ يُسمّيه، وهذا القارئ يرفع خطأً عند تغيّر العدد ولا "
            "يكشف المحجوز الجديد بنفسه"
        ),
        CODOMAIN_DERIVED_FROM_LITERAL_WRITES_ONLY: (
            "مجالُ السلطة مُشتَقٌّ من مواضع كتابة العضو الحرفية في نصّها؛ "
            "فحالةٌ تُحسَب وقت التنفيذ (متغيّرٌ أو استدعاءٌ أو جدول) لا تُرى "
            "هنا. فـ«لم يُعثَر على موضع كتابةٍ يبلغه» ليس «أُثبِت أن التنفيذ لا "
            "يبلغه»، وهو شقيقُ `NO_DECLARED_TOTAL_TO_CROSS_CHECK`: ثقةٌ قائمةٌ "
            "على «لم يُكتشَف» لا على برهان"
        ),
        SECTION_4_NAMES_THREE_VALUES_ONLY: (
            "في الشجرة قيمٌ مُعلَنةٌ أخرى غيرُ قابلةٍ للبناء "
            "(`AttainmentStanding.REACHED`، و`BirthVerdictStatus.NO_BIRTH_IN_SCOPE`)، "
            "و§٤ تُسمّي ثلاثًا نصًّا؛ فتوسيعُ القائمة حكمٌ لا تملكه هذه "
            "المرحلة، واستيرادُ `AttainmentStanding` هنا يربط القارئ بوحدة "
            "الغايات وهو ما تمنعه المرحلة. والاستبعاد مُسمّى لا مطويّ"
        ),
        SEARCH_SCOPE_IS_DECLARED_NOT_PROVEN: (
            "نطاقُ البحث المقروء هنا نصُّ وحدةٍ واحدة: وحدةُ الحجز نفسها. "
            "فـ«بُحِث فلم يُوجَد» استقصاءٌ على المصدر المقروء لا على العالم، "
            "وهو شقيقُ `ExhaustedSourceIsNotAnExhaustedWorld`: عضوٌ يُنتَج في "
            "وحدةٍ أخرى أو يُبنى وقت التنفيذ من قيمةٍ واردة لا يراه هذا "
            "القارئ، ولا يُقرَأ غيابُه من نصٍّ واحد برهانًا على غيابه من كلّ نصّ"
        ),
        FORM_VOCABULARY_IS_READ_NOT_LAWFUL: (
            "صيغُ الإشارة الأربع مُستخرَجةٌ من نصّ هذا المستودع اليوم، ولا صفَّ "
            "في `docs/CONSTITUTION.md` يُلزم إشارةً بأن تأخذ إحداها؛ وما خرج "
            "عنها يُحمَل على `UNREAD_FORM` وحدها — وهي الجهةُ الأضعف دعوى لا "
            "الأقوى — فيُقرَأ الغيابُ غيرَ مستقصًى بدل أن يُقرَأ مستقصًى. "
            "والحملُ على الأضعف اختيارُ اتجاهٍ مُسمًّى، لا برهانَ أن الصيغة "
            "تُنتج عضوًا فعلًا"
        ),
        SEARCHED_OVER_UNREAD_FORMS_IS_UNOCCUPIED_TODAY: (
            "`SEARCHED_OVER_UNREAD_FORMS` لا يشغلها موضعٌ في الشجرة اليوم، "
            "وصفرُها مقروءٌ في الإحصاء لا مطويّ: فخلوُّها ليس دليلًا على أن "
            "الصيغ غير المقروءة لا تقع، وإنما على أن وحدةَ الحجز الوحيدة التي "
            "جرى فيها بحثٌ خلت منها. ولا يُقرَأ هذا الخلوّ تزكيةً للشجرة"
        ),
    }
)


class DeferredValueLedgerError(ValueError):
    """قراءةٌ مرفوضة؛ لا تُحمَل الشيفرة على أقرب شكلٍ مقبول."""


class DeferredValueShape(Enum):
    """شكل حجز القيمة كما استُخرج من الشيفرة، ثلاثةٌ لا واحد."""

    REFUSED_BY_NAMING_THE_VALUE = "مرفوضة_بحارسٍ_يُسمّيها"
    REFUSED_BY_ADMITTING_ONLY_A_SIBLING = "مرفوضة_بقبول_أخيها_وحده"
    UNREACHABLE_FROM_SOLE_AUTHORITY = "لا_تبلغها_سلطتها_الوحيدة"


class ReferenceForm(Enum):
    """صيغُ الإشارة إلى مفردةٍ في نصّ وحدتها، مُستخرَجةً من موضع الإشارة نفسه.

    والصيغة الرابعة ليست سلّةَ مهملاتٍ تُطوى فيها الإشارات: هي **الحملُ على
    الأضعف دعوى**، فما لم يُقرَأ موضعُه يُقرَأ طريقًا قد يُنتج أيّ عضو، فيمنع
    دعوى الاستقصاء بدل أن يُسكَت عنه فتقوم الدعوى بلا مانع.
    """

    MEMBER_ATTRIBUTE_IN_CONSTRUCTOR_KEYWORD = "عضوٌ مكتوبٌ وسيطًا مُسمًّى في بناء"
    MEMBER_ATTRIBUTE_IN_COMPARISON = "عضوٌ مكتوبٌ طرفًا في مقارنة"
    VOCABULARY_IN_TYPE_POSITION = "المفردةُ في موضع نوعٍ لا موضع قيمة"
    UNREAD_FORM = "صيغةٌ لا يقرأ هذا القارئ عضوَها"

    @property
    def is_read(self) -> bool:
        """أقرأ هذا القارئُ ما تُنتجه الصيغة؟ وإلا فالبحثُ فيها لم يجرِ."""

        return self is not ReferenceForm.UNREAD_FORM

    @property
    def writes_a_member_into_a_construction(self) -> bool:
        """أتكتب الصيغةُ عضوًا في بناءٍ فيبلغه مجالُ السلطة المُشتَقّ؟"""

        return self is ReferenceForm.MEMBER_ATTRIBUTE_IN_CONSTRUCTOR_KEYWORD


class AbsenceGenus(Enum):
    """جنسُ غياب العضو عن مجال سلطته: أبحثٌ لم يجرِ، أم بحثٌ لم يجد، أم بحثٌ غيرُ مستقصٍ؟

    ثلاثةٌ لا اثنان، والثالثُ ليس منزلةً بين الأوّلين: `NOT_SEARCHED_AT_THIS_SITE`
    تصريحٌ بأن البحث لم يجرِ أصلًا، و`SEARCHED_AND_NOT_FOUND` دعوى استقصاءٍ على
    نصٍّ قُرئت صيغُه كلُّها، و`SEARCHED_OVER_UNREAD_FORMS` بحثٌ جرى وبقي فيه
    طريقٌ لم يُقرَأ. على منوال `TERMINATION_STRUCTURE_NOT_SETTLED` في
    `alghanem.program.aims`: الجهلُ عضوٌ في المفردة لا فراغٌ يُطوى.
    """

    NOT_SEARCHED_AT_THIS_SITE = "لم_يُبحَث_عنه_في_هذا_المصدر"
    SEARCHED_AND_NOT_FOUND = "بُحِث_فلم_يُوجَد"
    SEARCHED_OVER_UNREAD_FORMS = "بُحِث_وفي_النصّ_صيغةٌ_لا_تُقرَأ"

    @property
    def a_search_ran(self) -> bool:
        """أجرى بحثٌ في نصّ الوحدة أصلًا؟"""

        return self is not AbsenceGenus.NOT_SEARCHED_AT_THIS_SITE

    @property
    def claims_an_exhausted_source(self) -> bool:
        """أتدّعي هذه الرتبةُ استقصاءً على المصدر المقروء وحده؟"""

        return self is AbsenceGenus.SEARCHED_AND_NOT_FOUND


class DeferredValueSite(Enum):
    """مواضع القيم الثلاث التي تُسمّيها §٤، مُستخرَجةً لا مُبتكَرة.

    القيمة ثلاثيّةٌ: الوحدة التي تُمسَح، واسم المفردة المغلقة، واسم العضو.
    والوحدة الممسوحة هي وحدة **الحجز** لا وحدة الإعلان بالضرورة: فالعضو
    `BIRTH_IN_SCOPE` مُعلَنٌ في `alghanem.kernel.birth`، وحاجزُه مجالُ سلطته
    الوحيدة في `alghanem.kernel.birth_verdict`.
    """

    BIRTH_IN_SCOPE = (
        "alghanem.kernel.birth_verdict",
        "BirthVerdictStatus",
        "BIRTH_IN_SCOPE",
    )
    MORPHO_FUNCTIONAL = (
        "alghanem.arabic.probe_preregistration",
        "EvidenceGenus",
        "MORPHO_FUNCTIONAL",
    )
    CLOSED_BY_FROZEN_EXPERIMENT = (
        "alghanem.arabic.readiness_rank",
        "QuestionStatus",
        "CLOSED_BY_FROZEN_EXPERIMENT",
    )

    @property
    def module_name(self) -> str:
        """الوحدة التي يُمسَح نصُّها بحثًا عن الحجز."""

        return self.value[0]

    @property
    def vocabulary_name(self) -> str:
        """اسم المفردة المغلقة التي ينتمي العضو إليها."""

        return self.value[1]

    @property
    def member_name(self) -> str:
        """اسم العضو المحجوز كما تُسمّيه §٤."""

        return self.value[2]


_DECLARED_SHAPE_BY_SITE: Final[Mapping[DeferredValueSite, DeferredValueShape]] = (
    MappingProxyType(
        {
            DeferredValueSite.BIRTH_IN_SCOPE: (
                DeferredValueShape.UNREACHABLE_FROM_SOLE_AUTHORITY
            ),
            DeferredValueSite.MORPHO_FUNCTIONAL: (
                DeferredValueShape.REFUSED_BY_ADMITTING_ONLY_A_SIBLING
            ),
            DeferredValueSite.CLOSED_BY_FROZEN_EXPERIMENT: (
                DeferredValueShape.REFUSED_BY_NAMING_THE_VALUE
            ),
        }
    )
)

if len(DeferredValueShape) != 3:  # pragma: no cover - guard
    raise RuntimeError("a hold takes one of exactly three observed shapes")
if len(ReferenceForm) != 4:  # pragma: no cover - guard
    raise RuntimeError("a reference takes one of exactly four read forms")
if len(AbsenceGenus) != 3:  # pragma: no cover - guard
    raise RuntimeError("an absence is deliberately three-valued")
if set(_DECLARED_SHAPE_BY_SITE) != set(DeferredValueSite):  # pragma: no cover - guard
    raise RuntimeError("every declared site must declare the shape it expects")
if tuple(site.member_name for site in DeferredValueSite) != (
    SECTION_4_DECLARED_VALUE_NAMES
):  # pragma: no cover - guard
    raise RuntimeError("the sites are exactly section 4's three values, in its order")


def _require_non_blank(value: str, field_name: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise DeferredValueLedgerError(f"{field_name} نصٌّ غير فارغ")
    return value


def _require_blank(value: str, field_name: str, reason: str) -> str:
    if not isinstance(value, str):
        raise DeferredValueLedgerError(f"{field_name} نصّ")
    if value.strip():
        raise DeferredValueLedgerError(f"{field_name} يبقى فارغًا: {reason}")
    return value


def _require_positive_line(value: int, field_name: str) -> int:
    if not isinstance(value, int) or isinstance(value, bool) or value <= 0:
        raise DeferredValueLedgerError(f"{field_name} رقم سطرٍ موجب")
    return value


@dataclass(frozen=True, slots=True)
class ReadGuard:
    """حارسٌ واحد على مفردةٍ متتبَّعة، كما وُجد في نصّ وحدةٍ ممسوحة."""

    module_name: str
    vocabulary_name: str
    member_name: str
    negated: bool
    document_line: int

    def __post_init__(self) -> None:
        _require_non_blank(self.module_name, "اسم الوحدة")
        _require_non_blank(self.vocabulary_name, "اسم المفردة")
        _require_non_blank(self.member_name, "اسم العضو")
        if not isinstance(self.negated, bool):
            raise DeferredValueLedgerError("نفيُ الحارس قيمةٌ منطقية")
        _require_positive_line(self.document_line, "موضع الحارس")

    @property
    def admits_only_this_member(self) -> bool:
        """أيقبل الحارسُ هذا العضو وحده ويرفض ما سواه؟"""

        return self.negated


@dataclass(frozen=True, slots=True)
class GuardCensus:
    """إحصاءُ كلّ حارسٍ على المفردات المتتبَّعة، الموافقُ منها وغيرُ الموافق.

    حضورُ الحارس غير الموافق في الإحصاء هو الفارق بين «رُئي ولم يوافق موضعًا
    مُعلَنًا» و«لم يُرَ أصلًا»؛ ولا حقلَ عددٍ هنا، فالتعداد خاصّيةٌ تُحسَب.
    """

    guards: tuple[ReadGuard, ...]

    def __post_init__(self) -> None:
        if not isinstance(self.guards, tuple):
            raise DeferredValueLedgerError("إحصاء الحرّاس مجموعةٌ")
        for guard in self.guards:
            if not isinstance(guard, ReadGuard):
                raise DeferredValueLedgerError("كل عنصرٍ حارسٌ مرصود")

    @property
    def guard_count(self) -> int:
        """عدد الحرّاس المرصودين، محسوبًا لا مكتوبًا."""

        return len(self.guards)

    def guards_over(self, vocabulary_name: str) -> tuple[ReadGuard, ...]:
        """حرّاسُ مفردةٍ بعينها بترتيب ورودها في نصّ وحداتها."""

        _require_non_blank(vocabulary_name, "اسم المفردة")
        return tuple(
            guard for guard in self.guards if guard.vocabulary_name == vocabulary_name
        )


@dataclass(frozen=True, slots=True)
class VocabularyReference:
    """إشارةٌ واحدة إلى مفردةٍ متتبَّعة في نصّ وحدتها: صيغتُها وعضوُها وموضعُها."""

    module_name: str
    vocabulary_name: str
    form: ReferenceForm
    member_name: str
    document_line: int

    def __post_init__(self) -> None:
        _require_non_blank(self.module_name, "اسم الوحدة")
        _require_non_blank(self.vocabulary_name, "اسم المفردة")
        if not isinstance(self.form, ReferenceForm):
            raise DeferredValueLedgerError("صيغة الإشارة من مفردتها المغلقة")
        if self.form in (
            ReferenceForm.MEMBER_ATTRIBUTE_IN_CONSTRUCTOR_KEYWORD,
            ReferenceForm.MEMBER_ATTRIBUTE_IN_COMPARISON,
        ):
            _require_non_blank(self.member_name, "اسم العضو المُشار إليه")
        else:
            _require_blank(
                self.member_name,
                "اسم العضو المُشار إليه",
                "لا يُسمّى العضو إلا حيث قرأه القارئ في موضع الإشارة نفسه",
            )
        _require_positive_line(self.document_line, "موضع الإشارة")


@dataclass(frozen=True, slots=True)
class ReferenceCensus:
    """إحصاءُ كلّ إشارةٍ إلى المفردة في نصّ الوحدة الممسوحة، مقروءةً أو غير مقروءة.

    هذا الإحصاء **هو** نطاق البحث: من ادّعى «بُحِث فلم يُوجَد» أراه ما قرأ،
    ومن وقعت في نصّه صيغةٌ غير مقروءة رُدَّت دعواه إلى الأضعف. ولا حقلَ عددٍ
    هنا؛ التعدادُ خاصّيةٌ تُحسَب.
    """

    references: tuple[VocabularyReference, ...]

    def __post_init__(self) -> None:
        if not isinstance(self.references, tuple):
            raise DeferredValueLedgerError("إحصاء الإشارات مجموعةٌ")
        for reference in self.references:
            if not isinstance(reference, VocabularyReference):
                raise DeferredValueLedgerError("كل عنصرٍ إشارةٌ مرصودة")

    @property
    def reference_count(self) -> int:
        """عدد الإشارات المرصودة، محسوبًا لا مكتوبًا."""

        return len(self.references)

    @property
    def form_counts(self) -> Mapping[ReferenceForm, int]:
        """تعدادُ الإشارات بحسب صيغتها، وكل صيغةٍ حاضرةٌ ولو بصفر."""

        counts = dict.fromkeys(ReferenceForm, 0)
        for reference in self.references:
            counts[reference.form] += 1
        return MappingProxyType(counts)

    @property
    def read_forms(self) -> tuple[ReferenceForm, ...]:
        """الصيغُ المقروءة التي وقعت فعلًا، بترتيب أوّل وقوعها: نطاقُ البحث."""

        seen: list[ReferenceForm] = []
        for reference in self.references:
            if reference.form.is_read and reference.form not in seen:
                seen.append(reference.form)
        return tuple(seen)

    @property
    def unread_lines(self) -> tuple[int, ...]:
        """مواضعُ الصيغ غير المقروءة بترتيب ورودها؛ وخلوُّها لا يُطوى."""

        return tuple(
            reference.document_line
            for reference in self.references
            if not reference.form.is_read
        )

    @property
    def members_mentioned_without_construction(self) -> tuple[str, ...]:
        """أعضاءٌ مكتوبةٌ في النصّ قراءةً لا بناءً، بترتيب ورودها بلا تكرار.

        الذكرُ ليس إنتاجًا: عضوٌ يُقارَن به مكتوبٌ في نصّ سلطته ولا تبلغه، فلا
        يُقرَأ حضورُه في النصّ رفعًا لحجزه، ولا يُقرَأ غيابُه عن مجال السلطة
        غيابًا عن النصّ كلِّه.
        """

        constructed = {
            reference.member_name
            for reference in self.references
            if reference.form.writes_a_member_into_a_construction
        }
        mentioned: list[str] = []
        for reference in self.references:
            name = reference.member_name
            if not name or name in constructed or name in mentioned:
                continue
            mentioned.append(name)
        return tuple(mentioned)

    def references_in(self, module_name: str) -> tuple[VocabularyReference, ...]:
        """إشاراتُ وحدةٍ بعينها بترتيب ورودها في نصّها."""

        _require_non_blank(module_name, "اسم الوحدة")
        return tuple(
            reference
            for reference in self.references
            if reference.module_name == module_name
        )


@dataclass(frozen=True, slots=True)
class DeferredValueRow:
    """قيمةٌ مُعلَنةٌ واحدة غيرُ قابلةٍ للبناء، بشكلَي حجزها المُعلَن والمُشتَقّ."""

    site: DeferredValueSite
    declared_shape: DeferredValueShape
    derived_shape: DeferredValueShape
    evidence_line: int
    admitted_sibling: str = ""
    authority_codomain: tuple[str, ...] = ()
    absence_genus: AbsenceGenus = AbsenceGenus.NOT_SEARCHED_AT_THIS_SITE
    searched_forms: tuple[ReferenceForm, ...] = ()
    unread_form_lines: tuple[int, ...] = ()

    def __post_init__(self) -> None:
        if not isinstance(self.site, DeferredValueSite):
            raise DeferredValueLedgerError("موضع القيمة من مفردته المغلقة")
        for shape, name in (
            (self.declared_shape, "شكل الحجز المُعلَن"),
            (self.derived_shape, "شكل الحجز المُشتَقّ"),
        ):
            if not isinstance(shape, DeferredValueShape):
                raise DeferredValueLedgerError(f"{name} من مفردته المغلقة")
        _require_positive_line(self.evidence_line, "موضع الشاهد")

        if self.declared_shape is not self.derived_shape:
            raise DeferredValueLedgerError(
                f"{self.site.member_name}: شكلٌ مُعلَن "
                f"{self.declared_shape.value} وشكلٌ مُشتَقّ "
                f"{self.derived_shape.value} — {SHAPE_DISAGREEMENT_IS_REFUSED_NOTE}"
            )

        sibling_shape = DeferredValueShape.REFUSED_BY_ADMITTING_ONLY_A_SIBLING
        if self.derived_shape is sibling_shape:
            _require_non_blank(self.admitted_sibling, "الأخ المقبول وحده")
            if self.admitted_sibling == self.site.member_name:
                raise DeferredValueLedgerError(
                    "الأخ المقبول ليس العضو نفسه: قبولُ العضو نفسه رفعُ حجزٍ " "لا حجز"
                )
        else:
            _require_blank(
                self.admitted_sibling,
                "الأخ المقبول وحده",
                "الأخ لا يُسمّى إلا حيث كان الحجز بقبوله وحده",
            )

        unreachable = DeferredValueShape.UNREACHABLE_FROM_SOLE_AUTHORITY
        if not isinstance(self.authority_codomain, tuple) or any(
            not isinstance(item, str) or not item.strip()
            for item in self.authority_codomain
        ):
            raise DeferredValueLedgerError("مجال السلطة أسماءُ أعضاءٍ غير فارغة")
        if self.derived_shape is unreachable:
            if not self.authority_codomain:
                raise DeferredValueLedgerError(
                    "سلطةٌ بمجالٍ فارغ لا تشهد بشيء: مجالٌ لم يُعثَر فيه على "
                    "أيّ موضع كتابةٍ يُقرَأ «لا سلطة» لا «سلطةٌ لا تبلغ العضو»"
                )
            if self.site.member_name in self.authority_codomain:
                raise DeferredValueLedgerError(
                    f"{self.site.member_name} حاضرٌ في مجال سلطته المُشتَقّ: "
                    "الحجز مرفوعٌ فعلًا، ولا يُسجَّل قائمًا"
                )
        elif self.authority_codomain:
            raise DeferredValueLedgerError(
                "مجال السلطة لا يُسجَّل إلا حيث كان الحجز انعدامَ بلوغٍ منها"
            )

        self._validate_absence()

    def _validate_absence(self) -> None:
        """رُدَّ جنسَ غيابٍ يخالف شكلَ الحجز، أو دعوى بحثٍ بلا نطاقٍ مقروء."""

        if not isinstance(self.absence_genus, AbsenceGenus):
            raise DeferredValueLedgerError("جنس الغياب من مفردته المغلقة")
        if not isinstance(self.searched_forms, tuple) or any(
            not isinstance(form, ReferenceForm) or not form.is_read
            for form in self.searched_forms
        ):
            raise DeferredValueLedgerError(
                "نطاق البحث صيغُ إشارةٍ مقروءة من مفردتها المغلقة: "
                "والصيغةُ غير المقروءة ليست نطاقًا بُحِث فيه"
            )
        if len(set(self.searched_forms)) != len(self.searched_forms):
            raise DeferredValueLedgerError(
                "صيغةٌ مكرّرة في نطاق البحث: التكرار يُضخّم النطاق ولا يُوسّعه"
            )
        if not isinstance(self.unread_form_lines, tuple) or any(
            not isinstance(line, int) or isinstance(line, bool) or line <= 0
            for line in self.unread_form_lines
        ):
            raise DeferredValueLedgerError("مواضع الصيغ غير المقروءة أرقامُ أسطرٍ موجبة")

        searched_here = self.derived_shape is (
            DeferredValueShape.UNREACHABLE_FROM_SOLE_AUTHORITY
        )
        if searched_here != self.absence_genus.a_search_ran:
            raise DeferredValueLedgerError(
                f"{self.site.member_name}: شكلُ الحجز "
                f"{self.derived_shape.value} وجنسُ الغياب "
                f"{self.absence_genus.value} — البحثُ في مجال السلطة لا يجري "
                "إلا حيث كان الحجز انعدامَ بلوغٍ منها، ولا يُدّعى حيث لم يجرِ"
            )

        if not self.absence_genus.a_search_ran:
            if self.searched_forms or self.unread_form_lines:
                raise DeferredValueLedgerError(
                    "موضعٌ لم يجرِ فيه بحثٌ لا يحمل نطاقًا ولا مواضعَ غير "
                    f"مقروءة — {NOT_SEARCHED_IS_NOT_A_WEAKER_FOUND_NOTE}"
                )
            return

        if not self.searched_forms:
            raise DeferredValueLedgerError(
                f"{self.site.member_name}: بحثٌ بلا نطاقٍ مقروء — "
                f"{SEARCH_SCOPE_IS_REQUIRED_OF_THE_SEARCHER_NOTE}"
            )

        if self.absence_genus.claims_an_exhausted_source:
            if self.unread_form_lines:
                raise DeferredValueLedgerError(
                    f"{self.site.member_name}: دعوى استقصاءٍ ونصُّها يحمل صيغةً "
                    f"غير مقروءة عند {self.unread_form_lines[0]} — "
                    f"{NAMED_RESIDUALS[FORM_VOCABULARY_IS_READ_NOT_LAWFUL]}"
                )
        elif not self.unread_form_lines:
            raise DeferredValueLedgerError(
                f"{self.site.member_name}: بحثٌ مُعلَنٌ غيرُ مستقصٍ بلا صيغةٍ "
                "غير مقروءةٍ تُسمّى بموضعها: غيرُ المستقصي يُرى مانعُه"
            )

    @property
    def is_named_by_its_hold(self) -> bool:
        """أيُسمّي موضعُ الحجز العضوَ نفسه؟ وإلا فالحجز مُستلزَمٌ لا مكتوب."""

        return self.derived_shape is DeferredValueShape.REFUSED_BY_NAMING_THE_VALUE

    @property
    def raises_on_attempt(self) -> bool:
        """أيُرفَع خطأٌ عند محاولة البناء؟ لا خطأ حيث لا محاولةَ تُرفَض."""

        return self.derived_shape is not (
            DeferredValueShape.UNREACHABLE_FROM_SOLE_AUTHORITY
        )


@dataclass(frozen=True, slots=True)
class DeferredValueLedger:
    """دفتر القيم المحجوزة وإحصاءُ حرّاسه، بتعدادٍ مُشتَقّ لا مكتوب."""

    rows: tuple[DeferredValueRow, ...]
    guards: GuardCensus
    references: ReferenceCensus

    def __post_init__(self) -> None:
        if not isinstance(self.rows, tuple) or not self.rows:
            raise DeferredValueLedgerError("دفتر القيم مجموعةٌ غير فارغة")
        if not isinstance(self.guards, GuardCensus):
            raise DeferredValueLedgerError("إحصاء الحرّاس من نوعه")
        if not isinstance(self.references, ReferenceCensus):
            raise DeferredValueLedgerError("إحصاء الإشارات من نوعه")
        seen: set[DeferredValueSite] = set()
        for row in self.rows:
            if not isinstance(row, DeferredValueRow):
                raise DeferredValueLedgerError("كل عنصرٍ صفُّ قيمةٍ مقروء")
            if row.site in seen:
                raise DeferredValueLedgerError(
                    f"موضعٌ مكرّر: {row.site.member_name} — التكرار يُفسد "
                    "التعداد ولا يُطوى"
                )
            seen.add(row.site)
        missing = set(DeferredValueSite) - seen
        if missing:
            raise DeferredValueLedgerError(
                "مواضع مُعلَنة لم تُقرَأ: "
                + "، ".join(sorted(site.member_name for site in missing))
                + f" — {MISSING_HOLD_IS_REFUSED_NOTE}"
            )

    @property
    def row_count(self) -> int:
        """عدد القيم المحجوزة المقروءة، محسوبًا لا مكتوبًا."""

        return len(self.rows)

    @property
    def shape_counts(self) -> Mapping[DeferredValueShape, int]:
        """تعدادُ الصفوف بحسب شكل حجزها، وكل عضوٍ حاضرٌ ولو بصفر."""

        counts = dict.fromkeys(DeferredValueShape, 0)
        for row in self.rows:
            counts[row.derived_shape] += 1
        return MappingProxyType(counts)

    def rows_with_shape(
        self, shape: DeferredValueShape
    ) -> tuple[DeferredValueRow, ...]:
        """صفوفُ شكلٍ بعينه بترتيب ورود أسمائها في §٤."""

        if not isinstance(shape, DeferredValueShape):
            raise DeferredValueLedgerError("شكل الحجز من مفردته المغلقة")
        return tuple(row for row in self.rows if row.derived_shape is shape)

    @property
    def absence_genus_counts(self) -> Mapping[AbsenceGenus, int]:
        """تعدادُ الصفوف بحسب جنس غيابها، وكل عضوٍ حاضرٌ ولو بصفر."""

        counts = dict.fromkeys(AbsenceGenus, 0)
        for row in self.rows:
            counts[row.absence_genus] += 1
        return MappingProxyType(counts)

    def rows_with_absence_genus(
        self, genus: AbsenceGenus
    ) -> tuple[DeferredValueRow, ...]:
        """صفوفُ جنسِ غيابٍ بعينه بترتيب ورود أسمائها في §٤."""

        if not isinstance(genus, AbsenceGenus):
            raise DeferredValueLedgerError("جنس الغياب من مفردته المغلقة")
        return tuple(row for row in self.rows if row.absence_genus is genus)


def _member_attribute(node: ast.expr, vocabulary_name: str) -> str:
    """اسمُ العضو إن كان التعبير `Vocabulary.MEMBER`، وإلا فسلسلةٌ فارغة."""

    if (
        isinstance(node, ast.Attribute)
        and isinstance(node.value, ast.Name)
        and node.value.id == vocabulary_name
    ):
        return node.attr
    return ""


def _body_raises(body: list[ast.stmt]) -> bool:
    return any(isinstance(statement, ast.Raise) for statement in body)


def _scan_guards(
    tree: ast.AST, module_name: str, vocabulary_name: str
) -> list[ReadGuard]:
    """امسح كلّ حارسٍ يقارن بعضوٍ من المفردة ثم يرفع خطأً، ولا تتخطَّ واحدًا."""

    guards: list[ReadGuard] = []
    for node in ast.walk(tree):
        if not isinstance(node, ast.If) or not _body_raises(node.body):
            continue
        test = node.test
        if not isinstance(test, ast.Compare) or len(test.ops) != 1:
            continue
        operator = test.ops[0]
        if not isinstance(operator, ast.Is | ast.IsNot):
            continue
        member = _member_attribute(test.comparators[0], vocabulary_name)
        if not member:
            continue
        guards.append(
            ReadGuard(
                module_name=module_name,
                vocabulary_name=vocabulary_name,
                member_name=member,
                negated=isinstance(operator, ast.IsNot),
                document_line=test.lineno,
            )
        )
    return guards


def _scan_authority_codomain(
    tree: ast.AST, vocabulary_name: str
) -> tuple[tuple[str, ...], int]:
    """استخرج مجال السلطة من مواضع كتابة العضو الحرفية وحدها، وموضعَ أوّلها."""

    members: list[str] = []
    first_line = 0
    for node in ast.walk(tree):
        if not isinstance(node, ast.Call):
            continue
        for keyword in node.keywords:
            member = _member_attribute(keyword.value, vocabulary_name)
            if not member:
                continue
            if member not in members:
                members.append(member)
            line = keyword.value.lineno
            first_line = line if first_line == 0 else min(first_line, line)
    return tuple(members), first_line


_TYPE_CHECK_CALLS: Final = ("isinstance", "issubclass")


def _type_positions(tree: ast.AST) -> set[int]:
    """مواضعُ النوع: التعليقاتُ التوضيحية ووسيطا `isinstance`/`issubclass`.

    تُقرَأ من بنية الشجرة لا من دلالةٍ تُقدَّر: موضعُ التعليق التوضيحيّ حقلٌ
    مستقلّ في العقدة، ووسيطُ فحص النوع يُسمّى باسمه الحرفيّ. وما عداهما يبقى
    موضعَ قيمة.
    """

    marked: set[int] = set()
    for node in ast.walk(tree):
        annotations: list[ast.expr | None] = []
        if isinstance(node, ast.AnnAssign | ast.arg):
            annotations.append(node.annotation)
        elif isinstance(node, ast.FunctionDef | ast.AsyncFunctionDef):
            annotations.append(node.returns)
        elif (
            isinstance(node, ast.Call)
            and isinstance(node.func, ast.Name)
            and node.func.id in _TYPE_CHECK_CALLS
        ):
            annotations.extend(node.args)
        for annotation in annotations:
            if annotation is None:
                continue
            for inner in ast.walk(annotation):
                marked.add(id(inner))
    return marked


def _scan_references(
    tree: ast.AST, module_name: str, vocabulary_name: str, member_names: frozenset[str]
) -> list[VocabularyReference]:
    """امسح كلّ إشارةٍ إلى المفردة في نصّ الوحدة، ولا تتخطَّ واحدة.

    الحملُ على الأضعف: ما لم يُقرَأ موضعُه يُسجَّل `UNREAD_FORM` لا يُطوى، لأن
    الطيَّ يُنتج دعوى استقصاءٍ بلا مانعٍ مرئيّ.
    """

    type_positions = _type_positions(tree)
    keyword_values = {
        id(keyword.value)
        for node in ast.walk(tree)
        if isinstance(node, ast.Call)
        for keyword in node.keywords
    }
    comparison_operands: set[int] = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Compare):
            comparison_operands.add(id(node.left))
            comparison_operands.update(id(item) for item in node.comparators)

    references: list[VocabularyReference] = []
    attribute_bases = {
        id(node.value)
        for node in ast.walk(tree)
        if isinstance(node, ast.Attribute)
        and isinstance(node.value, ast.Name)
        and node.value.id == vocabulary_name
    }
    for node in ast.walk(tree):
        if isinstance(node, ast.Attribute):
            if not isinstance(node.value, ast.Name) or node.value.id != vocabulary_name:
                continue
            if node.attr not in member_names:
                form, member = ReferenceForm.UNREAD_FORM, ""
            elif id(node) in keyword_values:
                form, member = (
                    ReferenceForm.MEMBER_ATTRIBUTE_IN_CONSTRUCTOR_KEYWORD,
                    node.attr,
                )
            elif id(node) in comparison_operands:
                form, member = ReferenceForm.MEMBER_ATTRIBUTE_IN_COMPARISON, node.attr
            else:
                form, member = ReferenceForm.UNREAD_FORM, ""
            references.append(
                VocabularyReference(
                    module_name=module_name,
                    vocabulary_name=vocabulary_name,
                    form=form,
                    member_name=member,
                    document_line=node.lineno,
                )
            )
        elif isinstance(node, ast.Name) and node.id == vocabulary_name:
            if id(node) in attribute_bases:
                continue
            form = (
                ReferenceForm.VOCABULARY_IN_TYPE_POSITION
                if id(node) in type_positions
                else ReferenceForm.UNREAD_FORM
            )
            references.append(
                VocabularyReference(
                    module_name=module_name,
                    vocabulary_name=vocabulary_name,
                    form=form,
                    member_name="",
                    document_line=node.lineno,
                )
            )
    return sorted(references, key=lambda reference: reference.document_line)


def _absence_genus(
    census: ReferenceCensus,
) -> tuple[AbsenceGenus, tuple[ReferenceForm, ...], tuple[int, ...]]:
    """اشتقّ جنسَ الغياب من نطاق البحث المقروء ومن الصيغ التي لم تُقرَأ."""

    unread = census.unread_lines
    genus = (
        AbsenceGenus.SEARCHED_OVER_UNREAD_FORMS
        if unread
        else AbsenceGenus.SEARCHED_AND_NOT_FOUND
    )
    return genus, census.read_forms, unread


def _live_vocabulary(site: DeferredValueSite) -> type[Enum]:
    """استورد المفردة حيّةً؛ وغيابُ العضو رفضٌ مُسمّى لا حجزٌ يُقرَأ مرفوعًا."""

    module = importlib.import_module(site.module_name)
    vocabulary = getattr(module, site.vocabulary_name, None)
    if not isinstance(vocabulary, type) or not issubclass(vocabulary, Enum):
        raise DeferredValueLedgerError(
            f"المفردة {site.vocabulary_name} غير مرئيّة في {site.module_name}: "
            f"{MISSING_HOLD_IS_REFUSED_NOTE}"
        )
    if site.member_name not in vocabulary.__members__:
        raise DeferredValueLedgerError(
            f"العضو {site.member_name} غير موجود في {site.vocabulary_name}: "
            f"{MISSING_HOLD_IS_REFUSED_NOTE}"
        )
    return vocabulary


def _module_source(module_name: str) -> str:
    module = importlib.import_module(module_name)
    origin = getattr(module, "__file__", None)
    if origin is None:
        raise DeferredValueLedgerError(
            f"تعذّر بلوغ نصّ الوحدة {module_name}: {MISSING_HOLD_IS_REFUSED_NOTE}"
        )
    try:
        return Path(origin).read_text(encoding="utf-8")
    except OSError as error:  # pragma: no cover - filesystem failure
        raise DeferredValueLedgerError(
            f"تعذّرت قراءة الوحدة {module_name}: {MISSING_HOLD_IS_REFUSED_NOTE}"
        ) from error


def _read_row(
    site: DeferredValueSite, tree: ast.AST, guards: list[ReadGuard]
) -> tuple[DeferredValueRow, tuple[VocabularyReference, ...]]:
    """اشتقّ شكل الحجز من نصّ الوحدة، ورُدَّ الموضع الذي لا شاهد له.

    ويُرَدّ مع الصفّ ما قُرئ من إشارات: نطاقُ البحث يُرى ولا يُدّعى، وموضعٌ لم
    يجرِ فيه بحثٌ لا يُسجَّل له نطاق.
    """

    vocabulary = _live_vocabulary(site)
    declared = _DECLARED_SHAPE_BY_SITE[site]
    own_guards = [
        guard for guard in guards if guard.vocabulary_name == site.vocabulary_name
    ]

    naming = [
        guard
        for guard in own_guards
        if guard.member_name == site.member_name and not guard.negated
    ]
    if naming:
        return (
            DeferredValueRow(
                site=site,
                declared_shape=declared,
                derived_shape=DeferredValueShape.REFUSED_BY_NAMING_THE_VALUE,
                evidence_line=naming[0].document_line,
            ),
            (),
        )

    sibling_guards = [
        guard
        for guard in own_guards
        if guard.negated and guard.member_name != site.member_name
    ]
    if sibling_guards:
        if len(vocabulary.__members__) != 2:
            raise DeferredValueLedgerError(
                f"{site.member_name}: الحجز بقبول الأخ وحده يقوم على مفردةٍ "
                f"ثنائية، وعددُ أعضائها اليوم {len(vocabulary.__members__)} — "
                f"{NAMED_RESIDUALS[SIBLING_ADMISSION_REFUSAL_DEPENDS_ON_VOCABULARY_SIZE]}"
            )
        return (
            DeferredValueRow(
                site=site,
                declared_shape=declared,
                derived_shape=(DeferredValueShape.REFUSED_BY_ADMITTING_ONLY_A_SIBLING),
                evidence_line=sibling_guards[0].document_line,
                admitted_sibling=sibling_guards[0].member_name,
            ),
            (),
        )

    codomain, line = _scan_authority_codomain(tree, site.vocabulary_name)
    if not codomain:
        raise DeferredValueLedgerError(
            f"{site.member_name}: لا حارسَ يُسمّيه ولا أخًا يُقبَل دونه ولا "
            f"مجالَ سلطةٍ مكتوبًا في {site.module_name} — "
            f"{MISSING_HOLD_IS_REFUSED_NOTE}"
        )
    references = tuple(
        _scan_references(
            tree,
            site.module_name,
            site.vocabulary_name,
            frozenset(vocabulary.__members__),
        )
    )
    genus, searched_forms, unread_lines = _absence_genus(
        ReferenceCensus(references=references)
    )
    return (
        DeferredValueRow(
            site=site,
            declared_shape=declared,
            derived_shape=DeferredValueShape.UNREACHABLE_FROM_SOLE_AUTHORITY,
            evidence_line=line,
            authority_codomain=codomain,
            absence_genus=genus,
            searched_forms=searched_forms,
            unread_form_lines=unread_lines,
        ),
        references,
    )


def read_deferred_value_ledger() -> DeferredValueLedger:
    """اقرأ دفتر القيم المحجوزة من نصّ وحداتها، ورُدَّ ما لا شاهد له."""

    rows: list[DeferredValueRow] = []
    all_guards: list[ReadGuard] = []
    all_references: list[VocabularyReference] = []
    for site in DeferredValueSite:
        tree = ast.parse(_module_source(site.module_name))
        guards = _scan_guards(tree, site.module_name, site.vocabulary_name)
        all_guards.extend(guards)
        row, references = _read_row(site, tree, guards)
        rows.append(row)
        all_references.extend(references)
    return DeferredValueLedger(
        rows=tuple(rows),
        guards=GuardCensus(guards=tuple(all_guards)),
        references=ReferenceCensus(references=tuple(all_references)),
    )


__all__ = [
    "ABSENCE_IS_NOT_ONE_CATEGORY_NOTE",
    "CODOMAIN_DERIVED_FROM_LITERAL_WRITES_ONLY",
    "DEFERRED_VALUE_LEDGER_AUTHORITY_NOTE",
    "DESIGN_SOURCE_CITATION_NOTE",
    "FORM_VOCABULARY_IS_READ_NOT_LAWFUL",
    "MISSING_HOLD_IS_REFUSED_NOTE",
    "NAMED_RESIDUALS",
    "NOT_SEARCHED_IS_NOT_A_WEAKER_FOUND_NOTE",
    "NO_INDICATOR_IN_THIS_READER_NOTE",
    "REFUSAL_SHAPE_IS_NOT_A_DECLARED_VOCABULARY",
    "SEARCHED_OVER_UNREAD_FORMS_IS_UNOCCUPIED_TODAY",
    "SEARCH_SCOPE_IS_DECLARED_NOT_PROVEN",
    "SEARCH_SCOPE_IS_REQUIRED_OF_THE_SEARCHER_NOTE",
    "SECTION_4_DECLARED_VALUE_NAMES",
    "SECTION_4_NAMES_THREE_VALUES_ONLY",
    "SHAPE_DISAGREEMENT_IS_REFUSED_NOTE",
    "SIBLING_ADMISSION_REFUSAL_DEPENDS_ON_VOCABULARY_SIZE",
    "THREE_SHAPES_ARE_NOT_ONE_NOTE",
    "AbsenceGenus",
    "DeferredValueLedger",
    "DeferredValueLedgerError",
    "DeferredValueRow",
    "DeferredValueShape",
    "DeferredValueSite",
    "GuardCensus",
    "ReadGuard",
    "ReferenceCensus",
    "ReferenceForm",
    "VocabularyReference",
    "read_deferred_value_ledger",
]
