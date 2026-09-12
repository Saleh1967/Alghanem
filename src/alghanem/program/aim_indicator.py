"""المؤشر المعرفي المُشتَقّ: عددٌ مقروءٌ مربوطٌ بغايةٍ بعينها، بلا حكمٍ ولا ترقية.

هذه **المرحلة السادسة من الطور الثاني** لـ AIM.1، وهي المرحلة التي أجّلتها
المراحل الخمس السابقة كلُّها بالعبارة نفسها: «والمؤشرُ — بشروط §٤ كاملةً —
مؤجَّلٌ إلى مرحلةٍ لاحقة». والمؤشر هو بعينه ما مُنع عنه القرّاء الثلاثة: **ربطُ
عددٍ مقروء بغايةٍ بعينها**. فما كان مُنِعَ هناك لأنه سابقٌ لأوانه يقوم هنا
بوصفه موضوع المرحلة، لا بوصفه تساهلًا في القاعدة::

    DerivedCount  != Progress
    CitedSupport  != Attainment
    Indicator     != Verdict
    AimsDocument  != Authority

**المصدر التصميمي المباشر، مُستشهَدًا به لا مُعادًا اشتقاقه.** شكلُ «الجهة
تُعلن، والقارئ لا يقبل إلا من مفردةٍ مغلقة يملكها هو، والمخالفة تُرفَض عند
الإنشاء» مأخوذٌ هنا من سؤال التدقيق المفتوح
`DeclaredVersusDerivedRecurrenceNotExplained` بوصفه **مصدرًا مباشرًا** (إلزام §٥
من `docs/AIMS.md`)، لا بوصفه بديهةً تُعاد اشتقاقًا صامتًا. وذلك السؤال مرصودٌ
غير مفسَّر، فلا يُستحدَث له هنا اسمٌ عامّ ولا صنفُ أساسٍ مشترك يوحّد الشكل بين
القرّاء الخمسة؛ يُستعمل في موضعه ويُنسَب إلى سؤاله.

**الربط مُشتَقٌّ لا مكتوب** (§٤): لا جدولَ بيدٍ يقول «الغاية الفلانية تستند إلى
الصفوف الفلانية»، فذلك هو بعينه الحقل المكتوب الذي تمنعه §٤، وهو الخطأ الذي
أغلقته المرحلة الرابعة على `aims.py` نفسها. والمصدر الوحيد للربط هو
`AimRecord.citation`: الاستشهاد **يُعلن** مستندًا، والدفاتر الثلاثة **تشتقّ** هل
لذلك المستند وجودٌ في وثيقة الدستور أو في شجرة المستودع. واستشهادٌ يُسمّي صفًّا
لا وجود له يُرفَض عند الإنشاء ولا يُقرَّر.

**مفرداتٌ مغلقة متعدّدة لا مقياسٌ رتبيّ واحد** (§٥)، مع تعليل كلّ دمجٍ مرفوض:

* `DeclaredCitationShape` (شكلُ الإشارة في النصّ) و`CitedSupportKind` (جنسُ ما
  حُلَّت إليه) مفردتان لا واحدة: شكلٌ واحد (`صفّ X`) قد يُحَلّ صفًّا، وشكلٌ آخر
  (`` `X` ``) قد يُحَلّ صفًّا أو سؤالًا؛ ودمجُهما يُسقط الفارق بين ما كُتب وما
  وُجد، وهو الفارق الذي تقوم عليه المرحلة كلُّها.
* `AimSupportStanding` لا تُدمَج في أيّ منهما، ولا تصير درجةً في سُلَّم بلوغ:
  هي وصفٌ لتجانس حالات المستندات المقروءة لا تقديرٌ لقربٍ من غاية.
* ولا تُستحدَث رتبةٌ رابعة («نسبة إنجاز» أو «ترتيب أولوية» أو «قرب من بلوغ»)،
  لأن §٦ تمنع الترتيب وتقديرَ القرب صراحةً، والتقديرُ هو عينه الحكم الذي لا
  سلطة هنا تملكه. والمنعُ بنيةٌ لا وعد: يُفحَص اسمُ كلّ حقلٍ في كلّ صنفٍ هنا
  عند الاستيراد.

**لا حقلَ عددٍ البتّة** (§٤): كلّ عددٍ هنا خاصّيةٌ تُحسَب من الإشارات المقروءة،
على منهج `LawRowLedger.row_count` و`AuditQuestionLedger.open_count`. وكلّ عضوٍ
في كلّ مفردةٍ حاضرٌ في الإحصاء ولو بصفر، فالصفرُ المقروء لا يُطوى.

**الرفض لا التخطّي الصامت، مرفوعًا طبقةً خامسة.** ارتفعت القاعدة من الخلية إلى
الجدول (المرحلة الثانية)، ثم إلى الحارس (الثالثة)، ثم إلى نقطة §٢ (الرابعة)، ثم
إلى نقطة سؤال التدقيق (الخامسة)؛ وترتفع هنا إلى **الإشارة داخل الاستشهاد**: كلّ
موضعٍ من نصّ الاستشهاد إمّا إشارةٌ مقروءةٌ بشكلٍ من المفردة المغلقة، أو رابطٌ
مُصرَّحٌ به (`DeclaredCitationFiller`)، أو مرفوضٌ باسم الغاية وموضع الحرف. فلا
يُقرَأ استشهادٌ قراءةً جزئية تُنتج «لا مستند لهذه الغاية» وهو ادّعاءُ غيابٍ لم
يُقرَأ.

**استيرادُ `AimId` والقرّاء الثلاثة معًا هو المرحلة نفسها.** مُنع القرّاء
الثلاثة من استيراد `AimId` لأن الربط سابقٌ لأوانه هناك؛ وهذه الوحدة تستوردهم
جميعًا لأنها الربط. والحدّ المحفوظ ليس حدَّ الاستيراد بل حدُّ السلطة: لا ترقية،
ولا حكم، ولا بلوغ.

**خمولٌ سلطويّ مفحوص**: `AimIndicatorLedger != BirthVerdict`؛ لا تُصدر هذه
الوحدة ولادةً ولا حكمًا ولا تجميدًا ولا `E0`، ولا تكتب `AttainmentStanding` في
أيّ موضع، ولا تقرؤها أيّ وحدةٍ في `kernel/`، وهو ما يفحصه اختبارٌ يمسح الشجرة.

**وترتيب الصفوف ترتيبُ ورود الغايات في §٢**، لا ترتيبَ أهمّية ولا قربٍ من بلوغ
(§٦).
"""

from __future__ import annotations

import re
from collections.abc import Mapping
from dataclasses import dataclass, fields
from enum import Enum
from pathlib import Path
from types import MappingProxyType
from typing import Final

from .aims import AIM_RECORDS, AimId, AimRecord
from .constitution_ledger import (
    NO_STATUS_DECLARED_IN_RECORD,
    AuditQuestionStanding,
    ConstitutionLedger,
    DeclaredLawStatus,
    constitution_document_path,
    load_constitution_ledger,
)
from .deferred_value_ledger import DeferredValueSite

DESIGN_SOURCE_CITATION_NOTE: Final = (
    "شكلُ «المُعلَن مقابل المُشتَقّ» مأخوذٌ من سؤال التدقيق المفتوح "
    "`DeclaredVersusDerivedRecurrenceNotExplained` بوصفه مصدرًا مباشرًا لا "
    "بديهةً تُعاد اشتقاقًا صامتًا؛ فالسؤال مرصودٌ غير مفسَّر، والبناءُ عليه بلا "
    "تسميته يُحوّله أساسًا مُسلَّمًا به بلا مرور بحكم"
)

AIM_INDICATOR_AUTHORITY_NOTE: Final = (
    "مؤشرٌ معرفيّ فقط: لا يُصدر هذا الدفتر ولادةً ولا حكم ولادة، ولا يُجمِّد، "
    "ولا يكتب بلوغَ غايةٍ ولا يُرقّيه، ولا تقرؤه أيّ بوّابةٍ في النواة"
)

COUNT_IS_DERIVED_NOT_WRITTEN_NOTE: Final = (
    "كلّ عددٍ هنا خاصّيةٌ تُحسَب من الإشارات المقروءة، ولا حقلَ عددٍ يُكتَب فيه "
    "جواب؛ وإعلانُ مؤشرٍ بلا اشتقاقٍ من أثرٍ قائم هو الحقل المكتوب الذي تمنعه §٤"
)

UNKNOWN_CITATION_REFERENCE_IS_REFUSED_NOTE: Final = (
    "إشارةٌ في الاستشهاد لا تُحَلّ إلى صفٍّ ولا سؤالٍ ولا قسمٍ ولا مسارٍ ولا "
    "تُستبعَد بإعلانٍ تُرفَض باسم غايتها وموضع حرفها: قراءةٌ جزئية تُنتج «لا "
    "مستند لهذه الغاية» وهو ادّعاءُ غيابٍ لم يُقرَأ"
)

UNCOVERED_CITATION_TEXT_IS_REFUSED_NOTE: Final = (
    "نصٌّ في الاستشهاد لا تُغطّيه إشارةٌ مقروءة ولا رابطٌ مُصرَّحٌ به يُرفَض "
    "باسم غايته وموضعه: التغطيةُ الناقصة تُخفي إشارةً لم تُقرَأ خلف صمت"
)

DECLARED_STATUS_MUST_MATCH_ONE_SUPPORT_NOTE: Final = (
    "الحالة المُعلَنة بين قوسين في الاستشهاد تُقابَل بحالات المستندات المقروءة، "
    "ويكفي أن تُطابق واحدًا منها: فهي تصف بعضها لا كلَّها، وإلزامُها بمطابقة "
    "الكلّ يرفض استشهادًا صادقًا، وإسقاطُها يُلغي مقابلةً قائمة"
)

SUPPORT_STANDING_IS_NOT_A_DEFERRAL_CLASS_NOTE: Final = (
    "موقفُ المستندات وصفٌ لتجانس حالاتها المُعلَنة لا تصنيفٌ لها إلى «مؤجَّلة» "
    "و«مُنفَّذة»: لا وثيقةَ تُعلن هذه القسمة، واستحداثُها هنا حكمٌ لا سلطة "
    "لهذه الطبقة به"
)

CITATION_SUPPORT_IS_DECLARED_BY_THE_RECORD_NOT_BY_THE_CONSTITUTION: Final = (
    "CITATION_SUPPORT_IS_DECLARED_BY_THE_RECORD_NOT_BY_THE_CONSTITUTION"
)

SUPPORT_COUNT_IS_NOT_PROGRESS: Final = "SUPPORT_COUNT_IS_NOT_PROGRESS"

NO_DECLARED_SUPPORT_TOTAL_TO_CROSS_CHECK: Final = (
    "NO_DECLARED_SUPPORT_TOTAL_TO_CROSS_CHECK"
)

THIRD_READER_IS_CITED_BY_NO_AIM: Final = "THIRD_READER_IS_CITED_BY_NO_AIM"

SECTION_HEADING_CARRIES_NO_DECLARED_STATUS: Final = (
    "SECTION_HEADING_CARRIES_NO_DECLARED_STATUS"
)

NAMED_RESIDUALS: Final[Mapping[str, str]] = MappingProxyType(
    {
        CITATION_SUPPORT_IS_DECLARED_BY_THE_RECORD_NOT_BY_THE_CONSTITUTION: (
            "الربط يجري في اتّجاهٍ واحد: الاستشهاد يُسمّي مستنده، ولا صفَّ في "
            "`docs/CONSTITUTION.md` يُسمّي الغاية التي يسنده. فصفٌّ كان "
            "**ينبغي** أن يُستشهَد به لغايةٍ ولم يُذكَر في استشهادها غيرُ "
            "مرئيٍّ هنا البتّة، ولا يرفع به هذا الدفتر خطأً؛ وهو شقيقُ "
            "`SECTION_3_CLASSIFIES_SIX_OF_THIRTEEN`: ما لم يُصرّح به السجلّ لا "
            "يكشفه قارئُ السجلّ"
        ),
        SUPPORT_COUNT_IS_NOT_PROGRESS: (
            "عددُ المستندات المقروءة لغايةٍ ليس مسافةً إلى بلوغها: غايتان "
            "بعددٍ واحد ليستا على قربٍ واحد، وغايةٌ بمستندٍ واحد قد تكون أبعدَ "
            "من غايةٍ بعشرة. فلا يُرتّب هذا الدفتر الغايات ولا يُقارن بينها "
            "ولا يشتقّ من العدد نسبةً ولا رتبة"
        ),
        NO_DECLARED_SUPPORT_TOTAL_TO_CROSS_CHECK: (
            "لا وثيقةَ تُعلن كم مستندًا لغايةٍ بعينها، فالعددُ المقروء مُشتَقٌّ "
            "وحده ولا يُقابَل بمرجعٍ مستقلّ. وثقتُه قائمةٌ على «لم يُرفَع خطأ» "
            "أي «لم يُكتشَف نقص»، لا على «أُثبِت عدم وجود نقص»؛ وهو شقيقُ "
            "`NO_DECLARED_TOTAL_TO_CROSS_CHECK` في موضعٍ أعلى منه"
        ),
        THIRD_READER_IS_CITED_BY_NO_AIM: (
            "القارئ الثالث (`deferred_value_ledger`) لا يبلغه أيّ استشهاد: لا "
            "غايةَ في §٢ تُسمّي `BIRTH_IN_SCOPE` ولا `MORPHO_FUNCTIONAL` ولا "
            "`CLOSED_BY_FROZEN_EXPERIMENT` في استشهادها، فعدده صفرٌ في كلّ صفّ. "
            "والصفرُ هنا **مُشتَقٌّ** بمسح أسماء المواضع في نصّ الاستشهاد لا "
            "مفترَضٌ بإسقاط القارئ؛ ومع ذلك يبقى أن §٤ سمّت ثلاثة مصادر ولم "
            "يبلغ الربطُ ثالثَها، وهذا حدٌّ يُسمّى ولا يُغلَق هنا"
        ),
        SECTION_HEADING_CARRIES_NO_DECLARED_STATUS: (
            "القسمُ المُستشهَد به يُحَلّ بوجود عنوانه في الوثيقة وحده، ولا حالةَ "
            "مُعلَنة له تدخل تجانسَ الحالات؛ فاستشهادٌ بقسمٍ كامل يُقرَأ حضورًا "
            "لا حالةً، وغايةٌ كلُّ مستندها أقسامٌ لا يُقرَأ لها موقفُ حالاتٍ "
            "البتّة. وهذا حدُّ الوثيقة لا نقصُ القارئ: العنوان لا يحمل عمود حالة"
        ),
    }
)

_ANSWER_BEARING_FIELD_MARKERS: Final = (
    "answer",
    "verdict",
    "conclusion",
    "resolution",
    "decision",
    "result",
    "outcome",
    "birth",
    "promotion",
    "indicator",
    "score",
    "percent",
    "estimate",
    "priority",
    "progress",
    "share",
    "ratio",
    "rank",
    "closeness",
    "attainment",
)


class AimIndicatorError(ValueError):
    """قراءةٌ مرفوضة؛ لا يُحمَل الاستشهاد على أقرب مستندٍ مقبول."""


class DeclaredCitationShape(Enum):
    """أشكال الإشارة في نصّ الاستشهاد، مفردةً مغلقة مُستخرَجة من النصّ لا مُبتكَرة.

    القيمة هي الشكل كما يُكتَب، لا نمطُ مطابقته؛ والأنماط مُجمَّعة في
    `_SHAPE_PATTERNS` بترتيب مطابقةٍ يُقدّم الأطول على الأقصر، كما قُدّم أطول
    وسمٍ في `constitution_ledger`.
    """

    ROW = "صفّ X"
    DUAL_ROW = "صفّا X وY"
    ROW_GROUP = "صفوف X"
    SECTION = "قسم X"
    BACKTICKED_NAME = "`X`"
    REPOSITORY_PATH = "dir/file"


class CitedSupportKind(Enum):
    """جنسُ ما حُلَّت إليه الإشارة، مفردةً مستقلّةً عن شكلها في النصّ.

    الفصلُ بين الجنس والشكل مقصود: `صفّ G0.F.1` و`قسم G0.F.1` شكلٌ واحد تقريبًا
    ومرجعان مختلفان، و`` `X` `` شكلٌ واحد يُحَلّ صفًّا مرّةً وسؤالًا أخرى.
    ودمجُ المفردتين يُسقط الفارق بين ما أُعلن وما وُجد.
    """

    LAW_ROW = "صفّ_دستورٍ_مقروء"
    AUDIT_QUESTION = "سؤال_تدقيقٍ_مقروء"
    DOCUMENT_SECTION = "قسمٌ_في_الوثيقة"
    REPOSITORY_PATH = "مسارٌ_في_الشجرة"
    DECLARED_UNRESOLVABLE = "مُستبعَدٌ_بإعلانٍ_لا_بصمت"

    @property
    def is_resolved_support(self) -> bool:
        """أمستندٌ مقروءٌ هذا؟ الاستبعادُ مُصرَّحٌ به لا مُستنتَجٌ من صمت."""

        return self is not CitedSupportKind.DECLARED_UNRESOLVABLE


class AimSupportStanding(Enum):
    """موقفُ مستندات الغاية المقروءة: تجانسُ حالاتها، والجهلُ عضوٌ فيه.

    ليست سُلَّمًا ولا تقديرًا لقربٍ من بلوغ، ولا تصنيفًا إلى «مؤجَّل» و«مُنفَّذ»؛
    فتلك قسمةٌ لا تُعلنها وثيقة، واستحداثُها هنا حكمٌ لا سلطة لهذه الطبقة به.

    والعضو الثالث «لا مستند ذا حالةٍ مُعلَنة» ليس «لا مستند»: غايةٌ كلُّ
    مستندها أقسامٌ أو مسارات لها مستندٌ مقروءٌ قائم، ولا حالةَ له تدخل
    التجانس؛ وحملُ الحالتين على اسمٍ واحد يُنكر مستندًا قُرئ فعلًا.
    """

    ONE_DECLARED_STATUS = "حالةٌ_مُعلَنةٌ_واحدة"
    DIFFERENT_DECLARED_STATUSES = "حالاتٌ_مُعلَنةٌ_مختلفة"
    NO_STATUS_BEARING_SUPPORT = "لا_مستند_ذا_حالةٍ_مُعلَنة"


class DeclaredCitationFiller(Enum):
    """الروابط المُصرَّح بها في نصّ الاستشهاد، وما عداها يُرفَض لا يُطوى.

    تُقاس على `DeclaredTableHeader`: الاستبعادُ مُعلَنٌ لا مُستنتَجٌ من صمت
    القارئ؛ فنصٌّ باقٍ بعد الإشارات والروابط يُرفَض بموضعه، ولو كان حرفًا واحدًا.
    """

    COMMA = "،"
    CONJUNCTION = "و"
    OPEN_PAREN = "("
    CLOSE_PAREN = ")"
    IN_THE_CONSTITUTION = "في الدستور"


class DeclaredUnresolvableReference(Enum):
    """إشاراتٌ قائمةٌ اليوم لا يبلغها أيٌّ من دفاتر §٤، مُستبعَدةً بإعلان.

    القيمة ثنائيّة: شكلُ الإشارة واسمُها كما يُستخرَج منه. والاستبعادُ مقيَّدٌ
    بالشكل قصدًا: اسمٌ يُستبعَد في شكلٍ لا يُستبعَد في غيره.
    """

    UNNAMED_ROW_GROUP = (DeclaredCitationShape.ROW_GROUP, "G0")
    COMMITMENT_BULLET = (
        DeclaredCitationShape.BACKTICKED_NAME,
        "ExactFactorization(P_0) = OPEN",
    )

    @property
    def shape(self) -> DeclaredCitationShape:
        """شكلُ الإشارة الذي يقع فيه الاستبعاد."""

        return self.value[0]

    @property
    def reference_name(self) -> str:
        """اسمُ الإشارة المُستبعَدة كما يُستخرَج من شكلها."""

        return self.value[1]


_EXCLUSION_REASONS: Final[Mapping[DeclaredUnresolvableReference, str]] = (
    MappingProxyType(
        {
            DeclaredUnresolvableReference.UNNAMED_ROW_GROUP: (
                "«صفوف G0» جمعٌ لا يُسمّي صفًّا بعينه، وحملُه على كلّ صفٍّ "
                "يبدأ بـ`G0` اختيارٌ من القارئ لا إعلانٌ من السجلّ"
            ),
            DeclaredUnresolvableReference.COMMITMENT_BULLET: (
                "`ExactFactorization(P_0) = OPEN` نقطةُ التزامٍ في قسمٍ ليس "
                "جدولَ قوانينَ ولا قسمَ أسئلة، فلا يبلغها دفترُ الصفوف ولا "
                "دفترُ الأسئلة؛ وحلُّها بحضورها النصّيّ وحده يستحدث قارئًا "
                "رابعًا لا تملكه هذه المرحلة"
            ),
        }
    )
)


_SHAPE_PATTERNS: Final[tuple[tuple[DeclaredCitationShape, re.Pattern[str]], ...]] = (
    (
        DeclaredCitationShape.DUAL_ROW,
        re.compile(r"صفّا\s+«?([^»،()]+?)»?\s+و«?([^»،()]+?)»?(?=\s*[،()]|$)"),
    ),
    (DeclaredCitationShape.ROW_GROUP, re.compile(r"صفوف\s+«?([^»،()\s]+)»?")),
    (DeclaredCitationShape.ROW, re.compile(r"صفّ\s+«?([^»،()\s]+)»?")),
    (
        DeclaredCitationShape.SECTION,
        re.compile(r"قسم\s+«?([^»،()]+?)»?(?=\s*[،()]|$)"),
    ),
    (DeclaredCitationShape.BACKTICKED_NAME, re.compile(r"`([^`]+)`")),
    (
        DeclaredCitationShape.REPOSITORY_PATH,
        re.compile(r"(?:docs|src|tests|examples)/[^\s،()]*"),
    ),
)

_DECLARED_STATUS_PARENTHETICAL: Final = re.compile(r"\(([A-Z][A-Z_0-9 ]*)\)")

_FILLERS_LONGEST_FIRST: Final[tuple[DeclaredCitationFiller, ...]] = tuple(
    sorted(DeclaredCitationFiller, key=lambda filler: len(filler.value), reverse=True)
)
"""الروابط مرتَّبةً بالأطول أوّلًا، على منهج `_LABELS_LONGEST_FIRST`.

الترتيب شرطُ صحّةٍ لا تحسينُ أداء: حذفُ الرابط المفرد `و` قبل العبارة «في
الدستور» يقطع حرفًا من داخلها فيبقى بقيّةٌ مبتورة تُرفَض على نصٍّ سليم.
"""

_HEADING_LINE: Final = re.compile(r"^#{2,4}\s+(.+?)\s*$")

_ROW_IDENTIFIER: Final = re.compile(r"^[A-Z][A-Za-z0-9]*(?:\.[A-Za-z0-9]+)+$")
"""شكلُ معرّف الصفّ المُصرَّح به: حروفٌ ثم نقطةٌ فأكثر، على صورة `G0.BV.1a`.

الكلمةُ الأولى من اسم الصفّ ليست معرّفًا دائمًا: «Explicit domain» و«Explicit
target anchor» يشتركان في كلمتهما الأولى، فاتّخاذُها معرّفًا يُنشئ تكرارًا
كاذبًا يرفع خطأً على وثيقةٍ سليمة. فالمعرّفُ ما طابق هذا الشكل وحده، وما عداه
اسمُ صفٍّ يُحَلّ بتمامه لا بأوّل كلمةٍ منه.
"""


if len(DeclaredCitationShape) != 6:  # pragma: no cover - guard
    raise RuntimeError("citation shapes are exactly the six read from the record")
if len(_SHAPE_PATTERNS) != len(DeclaredCitationShape) or {
    shape for shape, _ in _SHAPE_PATTERNS
} != set(DeclaredCitationShape):  # pragma: no cover - guard
    raise RuntimeError("every declared citation shape carries exactly one pattern")
if set(_EXCLUSION_REASONS) != set(
    DeclaredUnresolvableReference
):  # pragma: no cover - guard
    raise RuntimeError("every declared exclusion must name its reason")
if len(AimSupportStanding) != 3:  # pragma: no cover - guard
    raise RuntimeError("support standing is deliberately three-valued")


def _require_non_blank(value: str, field_name: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise AimIndicatorError(f"{field_name} نصٌّ غير فارغ")
    return value


def _require_blank(value: str, field_name: str, reason: str) -> str:
    if not isinstance(value, str) or value:
        raise AimIndicatorError(f"{field_name} يبقى فارغًا: {reason}")
    return value


def _require_non_negative(value: int, field_name: str) -> int:
    if not isinstance(value, int) or isinstance(value, bool) or value < 0:
        raise AimIndicatorError(f"{field_name} عددٌ غير سالب")
    return value


@dataclass(frozen=True, slots=True)
class ReadCitationReference:
    """إشارةٌ واحدة قُرئت من استشهاد غاية: شكلُها، واسمها، وما حُلَّت إليه."""

    aim_id: AimId
    shape: DeclaredCitationShape
    reference_name: str
    kind: CitedSupportKind
    citation_offset: int
    resolved_target: str = ""
    derived_status: str = ""
    question_standing: AuditQuestionStanding | None = None

    def __post_init__(self) -> None:
        if not isinstance(self.aim_id, AimId):
            raise AimIndicatorError("معرّف الغاية من مفردته المغلقة")
        if not isinstance(self.shape, DeclaredCitationShape):
            raise AimIndicatorError("شكل الإشارة من مفردته المغلقة")
        if not isinstance(self.kind, CitedSupportKind):
            raise AimIndicatorError("جنس المستند من مفردته المغلقة")
        _require_non_blank(self.reference_name, "اسم الإشارة")
        _require_non_negative(self.citation_offset, "موضع الإشارة")

        if self.kind.is_resolved_support:
            _require_non_blank(self.resolved_target, "المستند المُشتَقّ")
        else:
            _require_blank(
                self.resolved_target,
                "المستند المُشتَقّ",
                "الإشارة المُستبعَدة بإعلانٍ لا تُحَلّ إلى مستند",
            )

        if self.kind in _STATUS_BEARING_KINDS:
            _require_non_blank(self.derived_status, "الحالة المُشتَقّة")
        else:
            _require_blank(
                self.derived_status,
                "الحالة المُشتَقّة",
                "لا حالةَ مُعلَنة لهذا الجنس، وكتابةُ حالةٍ له استحداثُ عمودٍ "
                "لا تحمله الوثيقة",
            )

        if self.kind is CitedSupportKind.AUDIT_QUESTION:
            if not isinstance(self.question_standing, AuditQuestionStanding):
                raise AimIndicatorError("موقف السؤال من مفردته المغلقة")
        elif self.question_standing is not None:
            raise AimIndicatorError(
                "موقفُ سؤالٍ لجنسٍ ليس سؤالًا: الموقف قسمةُ الدستور لأسئلته وحدها"
            )

    @property
    def is_resolved(self) -> bool:
        """هل حُلَّت الإشارة إلى مستندٍ قائم؟"""

        return self.kind.is_resolved_support


_STATUS_BEARING_KINDS: Final[frozenset[CitedSupportKind]] = frozenset(
    {CitedSupportKind.LAW_ROW, CitedSupportKind.AUDIT_QUESTION}
)


@dataclass(frozen=True, slots=True)
class CitationReferenceCensus:
    """إحصاءُ كلّ إشارةٍ قُرئت، مقروءِها ومُستبعَدِها؛ فالمُستبعَد يُرى لا يُطوى."""

    references: tuple[ReadCitationReference, ...]

    def __post_init__(self) -> None:
        if not isinstance(self.references, tuple) or not self.references:
            raise AimIndicatorError("إحصاء الإشارات مجموعةٌ غير فارغة")
        for reference in self.references:
            if not isinstance(reference, ReadCitationReference):
                raise AimIndicatorError("كل عنصرٍ إشارةٌ مقروءة")

    @property
    def reference_count(self) -> int:
        """عدد الإشارات كلِّها، محسوبًا لا مكتوبًا."""

        return len(self.references)

    @property
    def kind_counts(self) -> Mapping[CitedSupportKind, int]:
        """تعدادُ الإشارات بحسب جنسها، وكل عضوٍ حاضرٌ ولو بصفر."""

        counts = dict.fromkeys(CitedSupportKind, 0)
        for reference in self.references:
            counts[reference.kind] += 1
        return MappingProxyType(counts)

    @property
    def shape_counts(self) -> Mapping[DeclaredCitationShape, int]:
        """تعدادُ الإشارات بحسب شكلها في النصّ، وكل عضوٍ حاضرٌ ولو بصفر."""

        counts = dict.fromkeys(DeclaredCitationShape, 0)
        for reference in self.references:
            counts[reference.shape] += 1
        return MappingProxyType(counts)

    @property
    def excluded_references(self) -> tuple[ReadCitationReference, ...]:
        """الإشاراتُ المُستبعَدةُ بإعلان، حاضرةً في الإحصاء لا مطويّة."""

        return tuple(
            reference for reference in self.references if not reference.is_resolved
        )


@dataclass(frozen=True, slots=True)
class AimIndicatorRow:
    """صفُّ غايةٍ واحدة: إشاراتُها المقروءة وحالتُها المُعلَنة، بلا حقل عدد."""

    aim_id: AimId
    references: tuple[ReadCitationReference, ...]
    declared_status_in_citation: str = ""

    def __post_init__(self) -> None:
        if not isinstance(self.aim_id, AimId):
            raise AimIndicatorError("معرّف الغاية من مفردته المغلقة")
        if not isinstance(self.references, tuple) or not self.references:
            raise AimIndicatorError(
                f"استشهادُ {self.aim_id.value} بلا إشارةٍ مقروءة: صفٌّ فارغ "
                "يُقرَأ «لا مستند» وهو ادّعاءُ غيابٍ لم يُقرَأ"
            )
        previous_offset = -1
        for reference in self.references:
            if not isinstance(reference, ReadCitationReference):
                raise AimIndicatorError("كل عنصرٍ إشارةٌ مقروءة")
            if reference.aim_id is not self.aim_id:
                raise AimIndicatorError(
                    "إشارةٌ من استشهاد غايةٍ أخرى لا تُحسَب لهذه: الربط يُشتَقّ "
                    "من نصّ الغاية نفسها"
                )
            if reference.citation_offset <= previous_offset:
                raise AimIndicatorError("ترتيب الإشارات ترتيبُ ورودها في الاستشهاد")
            previous_offset = reference.citation_offset

        if self.declared_status_in_citation:
            declared = self.declared_status_in_citation
            if declared not in {
                reference.derived_status
                for reference in self.references
                if reference.derived_status
            }:
                raise AimIndicatorError(
                    f"حالةٌ مُعلَنة في استشهاد {self.aim_id.value} لا تُطابق أيّ "
                    f"مستندٍ مقروء: {declared} -- "
                    f"{DECLARED_STATUS_MUST_MATCH_ONE_SUPPORT_NOTE}"
                )

    def references_of_kind(
        self, kind: CitedSupportKind
    ) -> tuple[ReadCitationReference, ...]:
        """إشاراتُ جنسٍ بعينه بترتيب ورودها في الاستشهاد."""

        if not isinstance(kind, CitedSupportKind):
            raise AimIndicatorError("جنس المستند من مفردته المغلقة")
        return tuple(
            reference for reference in self.references if reference.kind is kind
        )

    @property
    def reference_count(self) -> int:
        """عدد إشارات الاستشهاد كلِّها، محسوبًا لا مكتوبًا."""

        return len(self.references)

    @property
    def resolved_support_count(self) -> int:
        """عدد المستندات المقروءة، محسوبًا لا مكتوبًا."""

        return len([True for reference in self.references if reference.is_resolved])

    @property
    def kind_counts(self) -> Mapping[CitedSupportKind, int]:
        """تعدادُ مستندات هذه الغاية بحسب جنسها، وكل عضوٍ حاضرٌ ولو بصفر."""

        counts = dict.fromkeys(CitedSupportKind, 0)
        for reference in self.references:
            counts[reference.kind] += 1
        return MappingProxyType(counts)

    @property
    def law_status_counts(self) -> Mapping[DeclaredLawStatus, int]:
        """تعدادُ صفوف هذه الغاية بحسب حالتها المُعلَنة، وكل عضوٍ حاضرٌ ولو بصفر."""

        counts = dict.fromkeys(DeclaredLawStatus, 0)
        for reference in self.references_of_kind(CitedSupportKind.LAW_ROW):
            counts[DeclaredLawStatus(reference.derived_status)] += 1
        return MappingProxyType(counts)

    @property
    def question_standing_counts(self) -> Mapping[AuditQuestionStanding, int]:
        """تعدادُ أسئلة هذه الغاية بحسب موقفها، وكل عضوٍ حاضرٌ ولو بصفر."""

        counts = dict.fromkeys(AuditQuestionStanding, 0)
        for reference in self.references_of_kind(CitedSupportKind.AUDIT_QUESTION):
            standing = reference.question_standing
            if standing is None:  # pragma: no cover - guard
                raise AimIndicatorError("سؤالٌ مقروءٌ بلا موقف")
            counts[standing] += 1
        return MappingProxyType(counts)

    @property
    def questions_without_declared_status_count(self) -> int:
        """عدد أسئلة هذه الغاية التي لم يُصرّح السجلّ بحالتها، جهلًا مقروءًا لا مطويًّا."""

        return len(
            [
                True
                for reference in self.references_of_kind(
                    CitedSupportKind.AUDIT_QUESTION
                )
                if reference.derived_status == NO_STATUS_DECLARED_IN_RECORD
            ]
        )

    @property
    def deferred_value_site_count(self) -> int:
        """عدد مواضع §٤ الثلاثة التي يُسمّيها هذا الاستشهاد، مُشتقًّا لا مفترَضًا."""

        names = {site.member_name for site in DeferredValueSite}
        return len(
            [True for reference in self.references if reference.reference_name in names]
        )

    @property
    def support_standing(self) -> AimSupportStanding:
        """موقفُ المستندات: تجانسُ حالاتها المُعلَنة، لا قربُها من بلوغ."""

        statuses = {
            reference.derived_status
            for reference in self.references
            if reference.derived_status
        }
        if not statuses:
            return AimSupportStanding.NO_STATUS_BEARING_SUPPORT
        if len(statuses) == 1:
            return AimSupportStanding.ONE_DECLARED_STATUS
        return AimSupportStanding.DIFFERENT_DECLARED_STATUSES

    @property
    def status_is_declared_in_citation(self) -> bool:
        """هل صرّح الاستشهاد بحالةٍ تُقابَل؟ الغيابُ يُقرَأ غيابًا لا مطابقة."""

        return bool(self.declared_status_in_citation)


@dataclass(frozen=True, slots=True)
class AimIndicatorLedger:
    """دفترُ المؤشر: صفٌّ لكل غاية بترتيب §٢، وإحصاءٌ لكلّ إشارةٍ قُرئت."""

    rows: tuple[AimIndicatorRow, ...]

    def __post_init__(self) -> None:
        if not isinstance(self.rows, tuple):
            raise AimIndicatorError("دفتر المؤشر مجموعةٌ من الصفوف")
        read_ids = tuple(row.aim_id for row in self.rows)
        if read_ids != tuple(AIM_RECORDS):
            raise AimIndicatorError(
                "الدفتر يحمل صفًّا لكل غايةٍ بترتيب ورودها في §٢: غايةٌ ساقطةٌ "
                "تُقرَأ «لا مستند لها» وهو ادّعاءُ غيابٍ لم يُقرَأ، وترتيبٌ "
                "مغاير يُقرَأ ترتيبَ أولويةٍ لا تملكه هذه الطبقة"
            )
        for row in self.rows:
            if not isinstance(row, AimIndicatorRow):
                raise AimIndicatorError("كل عنصرٍ صفُّ مؤشرٍ مقروء")

    @property
    def row_count(self) -> int:
        """عدد صفوف الدفتر، محسوبًا لا مكتوبًا."""

        return len(self.rows)

    @property
    def rows_by_aim(self) -> Mapping[AimId, AimIndicatorRow]:
        """صفوف الدفتر مُفهرَسةً بغاياتها، بلا ترجيحٍ بينها."""

        return MappingProxyType({row.aim_id: row for row in self.rows})

    @property
    def census(self) -> CitationReferenceCensus:
        """إحصاءُ كلّ إشارةٍ في كلّ استشهاد، مقروءِها ومُستبعَدِها."""

        return CitationReferenceCensus(
            references=tuple(
                reference for row in self.rows for reference in row.references
            )
        )

    @property
    def support_standing_counts(self) -> Mapping[AimSupportStanding, int]:
        """تعدادُ الغايات بحسب موقف مستنداتها، وكل عضوٍ حاضرٌ ولو بصفر."""

        counts = dict.fromkeys(AimSupportStanding, 0)
        for row in self.rows:
            counts[row.support_standing] += 1
        return MappingProxyType(counts)


def _assert_no_fields_matching(
    declaring_type: type, markers: tuple[str, ...], message: str
) -> None:
    for item in fields(declaring_type):
        if any(marker in item.name for marker in markers):
            raise RuntimeError(message)


for _declaring_type in (
    ReadCitationReference,
    CitationReferenceCensus,
    AimIndicatorRow,
    AimIndicatorLedger,
):
    _assert_no_fields_matching(
        _declaring_type,
        _ANSWER_BEARING_FIELD_MARKERS,
        "an indicator type may not carry an answer, verdict, attainment, "
        "progress, or ranking field",
    )


def _law_index(
    ledger: ConstitutionLedger,
) -> tuple[Mapping[str, DeclaredLawStatus], Mapping[str, DeclaredLawStatus]]:
    by_name: dict[str, DeclaredLawStatus] = {}
    by_identifier: dict[str, DeclaredLawStatus] = {}
    for row in ledger.laws.rows:
        name = row.law.strip("`")
        by_name[name] = row.status
        tokens = name.split()
        if len(tokens) > 1 and _ROW_IDENTIFIER.match(tokens[0]):
            identifier = tokens[0]
            if identifier in by_identifier:
                raise AimIndicatorError(
                    f"معرّفُ صفٍّ مكرّر في الدستور: {identifier} -- "
                    "حلُّ إشارةٍ إليه ترجيحٌ بلا تعليل"
                )
            by_identifier[identifier] = row.status
    return MappingProxyType(by_name), MappingProxyType(by_identifier)


def _section_headings(document_text: str) -> frozenset[str]:
    headings: set[str] = set()
    for line in document_text.splitlines():
        match = _HEADING_LINE.match(line)
        if match is None:
            continue
        heading = match.group(1)
        headings.add(heading)
        headings.add(heading.split(" — ")[0].strip())
    return frozenset(headings)


def _declared_exclusion(
    shape: DeclaredCitationShape, name: str
) -> DeclaredUnresolvableReference | None:
    for member in DeclaredUnresolvableReference:
        if member.shape is shape and member.reference_name == name:
            return member
    return None


def _scan_citation(
    citation: str,
) -> tuple[tuple[tuple[int, DeclaredCitationShape, str], ...], str]:
    covered = [False] * len(citation)
    found: list[tuple[int, DeclaredCitationShape, str]] = []
    for shape, pattern in _SHAPE_PATTERNS:
        for match in pattern.finditer(citation):
            if any(covered[match.start() : match.end()]):
                continue
            for index in range(match.start(), match.end()):
                covered[index] = True
            if shape is DeclaredCitationShape.DUAL_ROW:
                for group in (1, 2):
                    found.append((match.start(group), shape, match.group(group)))
            elif shape is DeclaredCitationShape.REPOSITORY_PATH:
                found.append((match.start(), shape, match.group(0)))
            else:
                found.append((match.start(1), shape, match.group(1)))
    declared_statuses: list[str] = []
    for match in _DECLARED_STATUS_PARENTHETICAL.finditer(citation):
        if any(covered[match.start() : match.end()]):
            continue
        for index in range(match.start(), match.end()):
            covered[index] = True
        declared_statuses.append(match.group(1))
    if len(declared_statuses) > 1:
        raise AimIndicatorError(
            "حالتان مُعلَنتان في استشهادٍ واحد: ترجيحُ إحداهما على الأخرى حكمٌ "
            "لا تملكه هذه الطبقة"
        )
    residue = "".join(
        character for index, character in enumerate(citation) if not covered[index]
    )
    for filler in _FILLERS_LONGEST_FIRST:
        residue = residue.replace(filler.value, "")
    if residue.strip():
        raise AimIndicatorError(
            f"نصٌّ غير مقروءٍ في الاستشهاد: {residue.strip()!r} -- "
            f"{UNCOVERED_CITATION_TEXT_IS_REFUSED_NOTE}"
        )
    return tuple(sorted(found)), (declared_statuses[0] if declared_statuses else "")


def _resolve_reference(
    aim_id: AimId,
    shape: DeclaredCitationShape,
    name: str,
    offset: int,
    laws_by_name: Mapping[str, DeclaredLawStatus],
    laws_by_identifier: Mapping[str, DeclaredLawStatus],
    questions: Mapping[str, tuple[AuditQuestionStanding, str]],
    headings: frozenset[str],
    repository_root: Path,
) -> ReadCitationReference:
    if _declared_exclusion(shape, name) is not None:
        return ReadCitationReference(
            aim_id=aim_id,
            shape=shape,
            reference_name=name,
            kind=CitedSupportKind.DECLARED_UNRESOLVABLE,
            citation_offset=offset,
        )

    if shape is DeclaredCitationShape.REPOSITORY_PATH:
        if not (repository_root / name).exists():
            raise AimIndicatorError(
                f"استشهاد {aim_id.value} يُسمّي مسارًا لا وجود له: {name} -- "
                f"{UNKNOWN_CITATION_REFERENCE_IS_REFUSED_NOTE}"
            )
        return ReadCitationReference(
            aim_id=aim_id,
            shape=shape,
            reference_name=name,
            kind=CitedSupportKind.REPOSITORY_PATH,
            citation_offset=offset,
            resolved_target=name,
        )

    if shape is DeclaredCitationShape.SECTION:
        if name not in headings:
            raise AimIndicatorError(
                f"استشهاد {aim_id.value} يُسمّي قسمًا لا عنوانَ له في الوثيقة: "
                f"{name} -- {UNKNOWN_CITATION_REFERENCE_IS_REFUSED_NOTE}"
            )
        return ReadCitationReference(
            aim_id=aim_id,
            shape=shape,
            reference_name=name,
            kind=CitedSupportKind.DOCUMENT_SECTION,
            citation_offset=offset,
            resolved_target=name,
        )

    status = laws_by_name.get(name, laws_by_identifier.get(name))
    if status is not None:
        return ReadCitationReference(
            aim_id=aim_id,
            shape=shape,
            reference_name=name,
            kind=CitedSupportKind.LAW_ROW,
            citation_offset=offset,
            resolved_target=name,
            derived_status=status.value,
        )

    question = questions.get(name)
    if question is not None:
        return ReadCitationReference(
            aim_id=aim_id,
            shape=shape,
            reference_name=name,
            kind=CitedSupportKind.AUDIT_QUESTION,
            citation_offset=offset,
            resolved_target=name,
            derived_status=question[1],
            question_standing=question[0],
        )

    raise AimIndicatorError(
        f"إشارةٌ في استشهاد {aim_id.value} عند الحرف {offset} لا تُحَلّ إلى صفٍّ "
        f"ولا سؤالٍ ولا قسمٍ ولا مسارٍ ولا تُستبعَد بإعلان: {name} -- "
        f"{UNKNOWN_CITATION_REFERENCE_IS_REFUSED_NOTE}"
    )


def read_aim_indicator_row(
    record: AimRecord,
    ledger: ConstitutionLedger,
    document_text: str,
    repository_root: Path,
) -> AimIndicatorRow:
    """اقرأ صفَّ غايةٍ واحدة من استشهادها، ورافضًا كلَّ إشارةٍ لا تُحَلّ."""

    if not isinstance(record, AimRecord):
        raise AimIndicatorError("الغاية سجلٌّ مفروضٌ بالبنية")
    if not isinstance(ledger, ConstitutionLedger):
        raise AimIndicatorError("دفتر الدستور من نوعه")
    if not isinstance(repository_root, Path):
        raise AimIndicatorError("جذر الشجرة مسارٌ")

    laws_by_name, laws_by_identifier = _law_index(ledger)
    questions: Mapping[str, tuple[AuditQuestionStanding, str]] = MappingProxyType(
        {
            question.name: (question.standing, question.declared_status)
            for question in ledger.audit_questions.questions
        }
    )
    headings = _section_headings(document_text)

    scanned, declared_status = _scan_citation(record.citation)
    references = tuple(
        _resolve_reference(
            aim_id=record.aim_id,
            shape=shape,
            name=name,
            offset=offset,
            laws_by_name=laws_by_name,
            laws_by_identifier=laws_by_identifier,
            questions=questions,
            headings=headings,
            repository_root=repository_root,
        )
        for offset, shape, name in scanned
    )
    return AimIndicatorRow(
        aim_id=record.aim_id,
        references=references,
        declared_status_in_citation=declared_status,
    )


def read_aim_indicator_ledger(
    ledger: ConstitutionLedger,
    document_text: str,
    repository_root: Path,
) -> AimIndicatorLedger:
    """اربط كلَّ غايةٍ بمستنداتها المقروءة، صفًّا لكل غايةٍ بترتيب §٢."""

    return AimIndicatorLedger(
        rows=tuple(
            read_aim_indicator_row(
                record=record,
                ledger=ledger,
                document_text=document_text,
                repository_root=repository_root,
            )
            for record in AIM_RECORDS.values()
        )
    )


def repository_root_path() -> Path:
    """جذرُ شجرة المستودع، مشتقًّا من موضع هذه الوحدة لا مكتوبًا."""

    return Path(__file__).resolve().parents[3]


def load_aim_indicator_ledger(path: Path | None = None) -> AimIndicatorLedger:
    """اقرأ الدفتر من وثيقة الدستور نفسها؛ وغيابُها رفضٌ مُسمّى لا دفترٌ فارغ."""

    document = constitution_document_path() if path is None else path
    if not isinstance(document, Path):
        raise AimIndicatorError("موضع الوثيقة مسارٌ")
    try:
        text = document.read_text(encoding="utf-8")
    except OSError as error:
        raise AimIndicatorError(
            f"تعذّرت قراءة وثيقة الدستور عند {document}: دفترٌ فارغ يُقرَأ «لا "
            "مستند لأيّ غاية» وهو ادّعاءُ غيابٍ لم تُقرَأ الوثيقة لأجله"
        ) from error
    return read_aim_indicator_ledger(
        ledger=load_constitution_ledger(document),
        document_text=text,
        repository_root=repository_root_path(),
    )


__all__ = [
    "AIM_INDICATOR_AUTHORITY_NOTE",
    "CITATION_SUPPORT_IS_DECLARED_BY_THE_RECORD_NOT_BY_THE_CONSTITUTION",
    "COUNT_IS_DERIVED_NOT_WRITTEN_NOTE",
    "DECLARED_STATUS_MUST_MATCH_ONE_SUPPORT_NOTE",
    "DESIGN_SOURCE_CITATION_NOTE",
    "NAMED_RESIDUALS",
    "NO_DECLARED_SUPPORT_TOTAL_TO_CROSS_CHECK",
    "SECTION_HEADING_CARRIES_NO_DECLARED_STATUS",
    "SUPPORT_COUNT_IS_NOT_PROGRESS",
    "SUPPORT_STANDING_IS_NOT_A_DEFERRAL_CLASS_NOTE",
    "THIRD_READER_IS_CITED_BY_NO_AIM",
    "UNCOVERED_CITATION_TEXT_IS_REFUSED_NOTE",
    "UNKNOWN_CITATION_REFERENCE_IS_REFUSED_NOTE",
    "AimIndicatorError",
    "AimIndicatorLedger",
    "AimIndicatorRow",
    "AimSupportStanding",
    "CitationReferenceCensus",
    "CitedSupportKind",
    "DeclaredCitationFiller",
    "DeclaredCitationShape",
    "DeclaredUnresolvableReference",
    "ReadCitationReference",
    "load_aim_indicator_ledger",
    "read_aim_indicator_ledger",
    "read_aim_indicator_row",
    "repository_root_path",
]
