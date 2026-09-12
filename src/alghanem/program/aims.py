"""سجلّ غايات البرنامج مفروضًا بالبنية، بلا مؤشرٍ ولا حكمٍ ولا ترقية.

هذه **المرحلة الأولى من الطور الثاني** لـ AIM.1: `docs/AIMS.md` صرّحت بالغايات
نثرًا وأعلنت صراحةً أنها الطور الأول وحده، وأن طورًا ثانيًا مُنفَّذًا يشتقّ
المؤشرات بنيويًّا مؤجَّل ومُقيَّد سلفًا بـ§٥ من تلك الوثيقة. والفارق الذي
تُغلقه هذه الوحدة هو الفارق بين النثر والبنية، مرفوعًا درجةً عن
`readiness_rank`::

    DeclaredAimProse != EnforcedAimRecord
    AimsDocument     != Authority
    Aim              != Achievement

**المصدر التصميمي المباشر، مُستشهَدًا به لا مُعادًا اشتقاقه.** تصميم هذه
الوحدة مأخوذ من سؤال التدقيق المفتوح `DeclaredVersusDerivedRecurrenceNotExplained`
(`docs/CONSTITUTION.md`، قسم `OpenAuditQuestions`) بوصفه **مصدرًا مباشرًا**، لا
بوصفه بديهةً مستقلّة يُعاد اشتقاقها هنا صامتًا. وهذا إلزامُ §٥ حرفيًّا: ذلك
السؤال **مرصودٌ غير مفسَّر** (`OBSERVED_NOT_EXPLAINED`)، وبناءُ طبقةٍ عليه دون
تسميته يُحوّل رصدًا مفتوحًا إلى أساسٍ مُسلَّم به بلا مرور بحكم. فلا يُستحدَث هنا
اسمٌ عامّ ولا صنفُ أساسٍ مشترك ولا تجريدٌ يوحّد شكلَ «المُعلَن مقابل المُشتَقّ»؛
يُستعمل الشكلُ في موضعه ويُنسَب إلى سؤاله المفتوح.

**مفردتان مستقلّتان لا مقياسٌ رتبيّ واحد**، على منهج `readiness_rank`، مع
تعليلٍ مكتوبٍ لكلّ دمجٍ مرفوض:

* دمج `AimEngagement` مع `AttainmentStanding` في محورٍ واحد يجعل «بدأت» درجةً
  في سُلَّم البلوغ، فيُقرَأ الانشغالُ بالغاية تقدّمًا نحوها؛ والحال أن غايةً
  بدأت واصطدمت بحاجزٍ مُسمّى لم تبلغ شيئًا، وأن البلوغ حكمٌ على الأثر لا على
  الانشغال. وهذا بعينه ما تمنعه §١ حين ترفض المؤشر الهندسي.
* ولا تُضاف ثالثةٌ («أولوية» أو «قرب من البلوغ»)، لأن §٦ تمنع الترتيب بالأولوية
  وتقديرَ القرب صراحةً، والتقديرُ هو عينه الحكم الذي لا سلطة هنا تملكه.

**الجهل عضوٌ في المفردة لا فراغٌ يُطوى** (§٤، على مثال `UNRESOLVED`): §٣ من
`docs/AIMS.md` تُصنّف ستّ غاياتٍ فقط من ثلاث عشرة؛ فالباقي يحمل
`UNCLASSIFIED_IN_RECORD` تصريحًا بأن السجلّ لم يُصنّفه، لا فراغًا يُقرَأ لاحقًا
«لم تبدأ» ولا «تقدَّمت».

**`REACHED` مُعلَنة ولا تُبنى اليوم**، بنفس انضباط
`QuestionStatus.CLOSED_BY_FROZEN_EXPERIMENT` و`EvidenceGenus.MORPHO_FUNCTIONAL`:
إسقاطها من المفردة يُخفي أن البلوغ ممكنٌ مبدئيًّا، وقبولها يُتيح كتابة بلوغٍ لا
سلطةَ أصدرته. والرفض عند الإنشاء نفسه لا عند سجلٍّ بعينه، وإلا أمكن بناء سجلٍّ
آخر يحمل القيمة بلا رادع.

**وجنسُ ذلك الرفض يُشتَقّ ولا يُعلَن — وهذا ما أضافته المرحلة التاسعة.** كان
النصّ السابق لـ`ATTAINMENT_DEFERRAL_NOTE` يقول «لا سلطة هنا تُصدر بلوغَ غاية»،
فيجزم بأن الرفض من جنس **الحجز لغياب سلطة اليوم** على الغايات الثلاث عشرة
دفعةً واحدة، بلا واصفٍ يُشتَقّ منه. وهذا بعينه شكلُ الثغرة التي أغلقتها
`unconstructibility_genus` في `alghanem.arabic.transmission_standing` حين رفضت
أن يُمرَّر التصنيفُ الزمنيّ وسيطًا مُعلَنًا فتنجح عليه البوّابةُ كلّها بمقدّمةٍ
غير محقَّقة. والجزمُ المضادّ — أن الرفض **خطأٌ فئويّ** لأن الغايات مفتوحةُ
النهاية فركتاليًّا — يُعيد الخطأ نفسه بجنسٍ معاكس لا يُصلحه: فـ AIM-K4 بلوغُها
شرطُ وجودٍ على مصنوعٍ مُسمّى (`FrozenFactorRef` صادرةً عن سلطة)، لا مستوًى لا
نهاية له؛ فالغايات ليست جنسًا واحدًا، وأيّ حكمٍ شاملٍ عليها حكمٌ بلا اشتقاق.

فيُفصَل **جنسُ الرفض** في مفردةٍ مغلقة (`AimAttainmentRefusalGenus`)، ويُشتَقّ
من بنية نهاية الغاية (`AimTerminationStructure`) لا من حقلٍ يُكتَب؛ على منوال
`UnconstructibilityGenus` و`EvidenceTemporalStructure` حرفًا بحرف، لا اسمًا
عامًّا يُستحدَث فوقهما. **والاشتقاق هنا أضعفُ من نظيره هناك، والفارقُ مُسمّى**:
هناك كان التزامنُ يُبرهَن ببصمة الإغلاق فبقي طرفٌ واحد بلا برهان، وهنا **لا
طرفَ يُبرهَن اليوم** — لا في الأثر المقروء ما يُثبت أن غايةً بعينها مفتوحةُ
النهاية بنيويًّا، ولا ما يُثبت أنها ذاتُ نهاية. فنتيجةُ الاشتقاق على أثر اليوم
`GENUS_NOT_SETTLED` في الغايات كلّها، وهذا **إضعافٌ صادق** لدعوى كانت أقوى من
دليلها لا تراجعٌ عن مكسب. والسلوك لا يتبدّل: `REACHED` تبقى مرفوضةً عند
الإنشاء كما كانت.

**ودعوى «كلُّ ميلادٍ يفتح مستوًى فركتاليًّا أعلى» غيرُ مُرمَّزةٍ مُشتِقًّا،
والسببُ مكتوب**: هي دعوى معقولة ولا يُسندها اليوم صفٌّ في `docs/CONSTITUTION.md`،
فتُترَك بقيّةً مُسمّاة؛ وترميزُها مُشتِقًّا يجعلها مقدّمةً غير محقَّقة تنجح
عليها القسمةُ كلّها، وهو عينُ ما تُغلقه هذه المرحلة.

**`DeclaredForeignAim != AlghanemRecord` حدٌّ نوعيّ لا قيمةُ حقل.** الغايتان
المستورَدتان تُسجَّلان بنوعٍ منفصل `ForeignDeclaredAim` بلا `AimId` وبلا أيّ
رتبة انشغالٍ أو بلوغ. ودمجهما في `AimRecord` بحقل مَصْدرية يجعل استبعادهما من
كلّ اشتقاقٍ لاحقٍ شرطًا يُكتَب في كل قارئ ويُنسى في واحد؛ وفصلُ النوع يجعل
الاستبعاد بنيةً لا انضباطًا.

نطاق الوحدة وحدودها — تسجيل صريح لا اعتذار لاحق:

* **لا مؤشر هنا**: هذه الوحدة تُنشئ السجلّ وحده. وقارئا الاشتقاق اللذان
  تُسمّيهما §٤ (تعداد صفوف الدستور، وتعداد أسئلة التدقيق) قاما في مرحلةٍ تالية
  مستقلّة في `alghanem.program.constitution_ledger`، ولا يستوردهما هذا السجلّ
  ولا يستورده أحدهما؛ والمؤشرُ المُشتَقّ منهما — أي ربطُ عددٍ مقروء بغايةٍ
  بعينها — ما زال مؤجَّلًا، ولا حقلَ قيمةٍ هنا يُكتَب فيه جوابٌ ولا خاصّيةَ تُحسَب.
* **لا ترقية**: `AimRecord != BirthVerdict`، و`AttainmentStanding != Freeze`؛ لا
  دالّة تحوّل سجلًّا إلى `SpecificationFreeze.FROZEN` ولا إلى `Freeze` ولا `E0`
  ولا حكمِ ولادة.
* **خمولٌ سلطويّ مفحوص**: لا وحدة في `kernel/` تستورد هذه الطبقة، ويُفحَص ذلك
  بمسحٍ آليّ لا يُترك لحسن النيّة.
* **ترتيب السجلّ ليس أولوية**: التسلسل هنا تسلسلُ عرضٍ مطابقٌ لترتيب §٢، ولا
  يُقرَأ ترتيبَ أهمّية ولا قربٍ من بلوغ.
"""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass, fields
from enum import Enum
from types import MappingProxyType
from typing import Final

DESIGN_SOURCE_OPEN_QUESTION: Final = "DeclaredVersusDerivedRecurrenceNotExplained"

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
)


class AimRecordError(ValueError):
    """غايةٌ مرفوضة؛ لا تُحمَل على أقرب حالةٍ مقبولة."""


class AimId(Enum):
    """معرّفات الغايات كما وردت في §٢، مُستخرَجةً لا مُبتكَرة."""

    K1 = "AIM-K1"
    K2 = "AIM-K2"
    K3 = "AIM-K3"
    K4 = "AIM-K4"
    A1 = "AIM-A1"
    A2 = "AIM-A2"
    A3 = "AIM-A3"
    X1 = "AIM-X1"
    E1 = "AIM-E1"
    E2 = "AIM-E2"
    T1 = "AIM-T1"
    T2 = "AIM-T2"
    T3 = "AIM-T3"


class AimEngagement(Enum):
    """رتبة الانشغال بالغاية كما صنّفها السجلّ، والجهلُ عضوٌ فيها."""

    NOT_STARTED = "لم_تبدأ"
    BLOCKED_BY_NAMED_OBSTACLE = "بدأت_فاصطدمت_بحاجز_مُسمّى"
    UNCLASSIFIED_IN_RECORD = "لا_تصنيف_في_السجل"


class AttainmentStanding(Enum):
    """رتبة البلوغ: لم تُبلَغ، أم بلوغٌ جزئيّ ببقيّةٍ مُسمّاة، أم بلوغ؟"""

    NOT_REACHED = "لم_تُبلَغ"
    PARTIALLY_REACHED_WITH_NAMED_REMAINDER = "بلوغٌ_جزئيّ_ببقيّة_مُسمّاة"
    REACHED = "بُلِغت"


class AimTerminationStructure(Enum):
    """بنيةُ نهاية الغاية: أمفتوحةٌ فركتاليًّا، أم ذاتُ نهايةٍ على مصنوعٍ مُسمّى؟

    والعضو الثالث ليس فراغًا يُطوى: «ليست مفتوحةً بالبرهان» ليست «إذن ذاتُ
    نهاية»، وسالبةٌ لا تُثبت نقيضًا؛ فلو بقيت المفردةُ ثنائيّةً لأنتج
    الاستبعادُ وحده نهايةً بالنفي. على منوال `TEMPORAL_STRUCTURE_NOT_SETTLED`
    في `alghanem.arabic.transmission_standing`.
    """

    OPEN_ENDED_BY_FRACTAL_RECURSION = "مفتوحةٌ_بالتعاقب_الفركتاليّ"
    TERMINAL_ON_A_NAMED_ARTEFACT = "ذاتُ_نهايةٍ_على_مصنوعٍ_مُسمّى"
    TERMINATION_STRUCTURE_NOT_SETTLED = "بنيةُ_النهاية_غير_محسومة"


class AimAttainmentRefusalGenus(Enum):
    """جنسُ رفض `REACHED`: أحجزٌ لغياب سلطةٍ اليوم، أم امتناعٌ فئويّ، أم لا يُعلَم؟

    الفارقُ عمليّ لا لفظيّ: الحجزُ ترفعه سلطةٌ تُبنى غدًا، والخطأُ الفئويّ لا
    ترفعه أداةٌ لأن العلّة في نوع السؤال لا في عدّة الفحص. والأسماء مأخوذةٌ
    لفظًا من `UnconstructibilityGenus` استشهادًا بموضعها لا استحداثًا لتجريدٍ
    يوحّد البابين.
    """

    HELD_BY_MISSING_AUTHORITY_TODAY = "محجوزة_لغياب_سلطة_اليوم"
    REFUSED_BY_STRUCTURAL_CATEGORY_MISMATCH = "ممتنعة_بخطأ_فئوي_بنيوي"
    GENUS_NOT_SETTLED = "جنسُ_الرفض_غير_محسوم"


class TerminationProofSite(Enum):
    """مواضعُ البرهان الممكنة على بنية النهاية، ولا واحدَ منها قائمٌ اليوم.

    تُسمّى المواضعُ لتكون البقيّةُ مُسمّاةً لا مطويّة: من بنى أحدَها بنى
    الاشتقاقَ الإيجابيّ، ومن لم يبنِه بقي الجنسُ غيرَ محسوم.
    """

    CONSTITUTION_ROW_ESTABLISHING_FRACTAL_OPEN_ENDEDNESS = (
        "صفٌّ دستوريّ يُثبت انفتاح الغاية بالتعاقب الفركتاليّ"
    )
    CONSTITUTION_ROW_ESTABLISHING_A_TERMINAL_ARTEFACT = (
        "صفٌّ دستوريّ يُثبت أن بلوغ الغاية شرطُ وجودٍ على مصنوعٍ مُسمًّى"
    )


if len(AimEngagement) != 3:  # pragma: no cover - guard
    raise RuntimeError("engagement is deliberately three-valued")
if len(AttainmentStanding) != 3:  # pragma: no cover - guard
    raise RuntimeError("attainment standing is deliberately three-valued")
if len(AimTerminationStructure) != 3:  # pragma: no cover - guard
    raise RuntimeError("termination structure is deliberately three-valued")
if len(AimAttainmentRefusalGenus) != 3:  # pragma: no cover - guard
    raise RuntimeError("refusal genus is deliberately three-valued")


TWO_INDEPENDENT_AXES_NOTE: Final = (
    "الانشغال بالغاية والبلوغ إليها محوران مستقلّان لا سُلَّمٌ واحد: دمجهما "
    "يجعل «بدأت» درجةً في سُلَّم البلوغ، فيُقرَأ الانشغال تقدّمًا؛ وغايةٌ بدأت "
    "فاصطدمت بحاجزٍ مُسمّى لم تبلغ شيئًا"
)

ATTAINMENT_DEFERRAL_NOTE: Final = (
    "البلوغ مُعلَنٌ في المفردة وغير قابل للبناء هنا، ويُرفض عند الإنشاء نفسه لا "
    "عند سجلٍّ بعينه؛ وجنسُ هذا الرفض لا يُجزَم به في هذا النصّ بل يُشتَقّ لكلّ "
    "غايةٍ على حدة من بنية نهايتها، فانظر "
    "`REFUSAL_GENUS_IS_DERIVED_NOT_DECLARED_NOTE`"
)

REFUSAL_GENUS_IS_DERIVED_NOT_DECLARED_NOTE: Final = (
    "جنسُ رفض البلوغ مُشتَقٌّ من بنية نهاية الغاية لا مكتوبٌ في حقل ولا مُعلَنٌ "
    "في نثر: وحكمٌ واحد على الغايات الثلاث عشرة — حجزًا كان أو امتناعًا "
    "فئويًّا — حكمٌ بلا اشتقاق، إذ AIM-K4 بلوغُها شرطُ وجودٍ على مصنوعٍ مُسمّى "
    "لا مستوًى لا نهاية له"
)

CATEGORY_MISMATCH_IS_NOT_MISSING_AUTHORITY_NOTE: Final = (
    "الامتناعُ الفئويّ غيرُ الحجز لغياب سلطة، والفارقُ مُسمًّى في موضعه من "
    "`alghanem.arabic.transmission_standing` ويُستشهَد به هنا ولا يُعاد اشتقاقه: "
    "الحجزُ ترفعه سلطةٌ تُبنى غدًا، والخطأُ الفئويّ لا ترفعه أداة"
)

NO_TERMINATION_PROOF_EXISTS_TODAY_NOTE: Final = (
    "لا موضعَ برهانٍ قائمًا اليوم على بنية نهاية أيّ غاية: لا في الأثر المقروء "
    "ما يُثبت انفتاحًا فركتاليًّا ولا ما يُثبت نهايةً على مصنوعٍ مُسمّى؛ فواصفُ "
    "كلّ غايةٍ يُرفَض عند الإنشاء إن حمل موضعَ برهانٍ لم تُصدره سلطة، ويبقى "
    "الجنسُ غيرَ محسوم"
)

FRACTAL_OPEN_ENDEDNESS_IS_AN_UNSOURCED_CLAIM_NOTE: Final = (
    "دعوى أن كلّ ميلادٍ يفتح مستوًى فركتاليًّا أعلى لا يُسندها صفٌّ في "
    "`docs/CONSTITUTION.md` اليوم، فلا تُرمَّز مُشتِقًّا: ترميزُها يجعلها "
    "مقدّمةً غير محقَّقة تنجح عليها القسمةُ كلّها"
)

NOT_SETTLED_IS_NOT_A_MIDPOINT_NOTE: Final = (
    "`GENUS_NOT_SETTLED` ليست منزلةً بين الحجز والامتناع ولا درجةً في سُلَّم: "
    "هي تصريحٌ بأن الاشتقاق عجز، ولا تُقرَأ قربًا من بلوغٍ ولا بعدًا عنه"
)

UNCLASSIFIED_IS_NOT_PROGRESS_NOTE: Final = (
    "غيابُ تصنيفٍ في السجلّ يُسجَّل قيمةً صريحة لا فراغًا يُطوى: فلا يُقرَأ "
    "«لم تبدأ» ولا يُقرَأ تقدّمًا، وإنما يُقرَأ ما هو: السجلّ لم يُصنّفها"
)

NO_PRIORITY_ORDER_NOTE: Final = (
    "ترتيب السجلّ ترتيبُ عرضٍ مطابقٌ لـ§٢، لا ترتيبَ أولوية ولا قربٍ من بلوغ؛ "
    "والتقدير هو عينه الحكم الذي لا سلطة هنا تملكه"
)

FOREIGN_AIM_BOUNDARY_NOTE: Final = (
    "الغاية الأجنبية المُعلَنة تُسجَّل بنوعٍ منفصل بلا معرّف غايةٍ محلّي وبلا "
    "رتبتَي انشغالٍ وبلوغ: لا يتحقّق هذا المستودع منها ولا يملك دليلها، "
    "ولا تدخل اشتقاقًا"
)

AIMS_AUTHORITY_NOTE: Final = (
    "تسجيلٌ فقط: لا يُنتج هذا السجلّ ولادةً ولا حكم ولادة، ولا يُجمِّد في "
    "النواة، ولا تقرأه أيّ بوّابة فيها، ولا يحمل مؤشرًا"
)

NO_INDICATOR_IN_THIS_MILESTONE_NOTE: Final = (
    "لا مؤشر في هذا السجلّ: قارئا الاشتقاق قاما في وحدةٍ مستقلّة لا يستوردها "
    "هذا السجلّ، وربطُ عددٍ مقروء بغايةٍ بعينها هو المؤشر نفسه وما زال "
    "مؤجَّلًا؛ وإعلانُ مؤشرٍ بلا اشتقاقٍ من أثرٍ قائم هو الحقل المكتوب الذي "
    "تمنعه §٤"
)


def _require_non_blank(value: str, field_name: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise AimRecordError(f"{field_name} نصٌّ غير فارغ")
    return value


def _require_blank(value: str, field_name: str, reason: str) -> str:
    if not isinstance(value, str):
        raise AimRecordError(f"{field_name} نصّ")
    if value.strip():
        raise AimRecordError(f"{field_name} يبقى فارغًا: {reason}")
    return value


@dataclass(frozen=True, slots=True)
class AimRecord:
    """غايةٌ واحدة بسؤالها وحدّيها وسندها ورتبتيها، مرفوضةً متى كذبت التوافيق."""

    aim_id: AimId
    question: str
    what_counts_as_reaching: str
    what_does_not_count: str
    citation: str
    engagement: AimEngagement
    attainment: AttainmentStanding
    named_obstacle: str = ""
    named_remainder: str = ""

    def __post_init__(self) -> None:
        if not isinstance(self.aim_id, AimId):
            raise AimRecordError("معرّف الغاية من مفردته المغلقة")
        if not isinstance(self.engagement, AimEngagement):
            raise AimRecordError("رتبة الانشغال من مفردتها المغلقة")
        if not isinstance(self.attainment, AttainmentStanding):
            raise AimRecordError("رتبة البلوغ من مفردتها المغلقة")
        for value, name in (
            (self.question, "سؤال الغاية"),
            (self.what_counts_as_reaching, "ما يُعَدّ بلوغًا"),
            (self.what_does_not_count, "ما لا يُعَدّ بلوغًا"),
            (self.citation, "مستند الغاية في السجل"),
        ):
            _require_non_blank(value, name)

        if self.attainment is AttainmentStanding.REACHED:
            raise AimRecordError(ATTAINMENT_DEFERRAL_NOTE)

        if self.engagement is AimEngagement.BLOCKED_BY_NAMED_OBSTACLE:
            _require_non_blank(self.named_obstacle, "الحاجز المُسمّى")
        else:
            _require_blank(
                self.named_obstacle,
                "الحاجز المُسمّى",
                "الحاجز لا يُسمّى إلا لغايةٍ بدأت فاصطدمت به",
            )

        partial = AttainmentStanding.PARTIALLY_REACHED_WITH_NAMED_REMAINDER
        if self.attainment is partial:
            _require_non_blank(self.named_remainder, "البقيّة المُسمّاة")
        else:
            _require_blank(
                self.named_remainder,
                "البقيّة المُسمّاة",
                "البقيّة لا تُسمّى إلا مع بلوغٍ جزئيّ مُسجَّل",
            )

        if (
            self.engagement is AimEngagement.NOT_STARTED
            and self.attainment is not AttainmentStanding.NOT_REACHED
        ):
            raise AimRecordError(
                "غايةٌ لم تبدأ لا تحمل بلوغًا جزئيًّا: البلوغ حكمٌ على أثرٍ "
                "قائم، ولا أثر لغايةٍ لم يُشرَع فيها"
            )

    @property
    def obstacle_is_named(self) -> bool:
        """هل الحاجز مُسمّى؟ `NamedObstacle != SilentAbsence` بنيويًّا."""

        return self.engagement is AimEngagement.BLOCKED_BY_NAMED_OBSTACLE

    @property
    def remains_unattained(self) -> bool:
        """هل بقيت الغاية دون بلوغٍ تامّ؟ نعم بنيويًّا في هذه المرحلة."""

        return self.attainment is not AttainmentStanding.REACHED


@dataclass(frozen=True, slots=True)
class ForeignDeclaredAim:
    """غايةٌ أجنبية مُسجَّلة كما أُعلنت، لا يتحقّق منها هذا المستودع."""

    foreign_aim_id: str
    source_project_note: str
    declared_as: str

    def __post_init__(self) -> None:
        _require_non_blank(self.foreign_aim_id, "معرّف الغاية الأجنبية")
        _require_non_blank(self.source_project_note, "سند المصدر الأجنبي")
        _require_non_blank(self.declared_as, "نصّ ما أُعلن")

    @property
    def enters_local_derivation(self) -> bool:
        """هل تدخل اشتقاقًا محلّيًّا؟ لا بنيويًّا، لا اختيارًا يُراجَع."""

        return False


@dataclass(frozen=True, slots=True)
class AimTerminationDescriptor:
    """واصفُ بنية نهاية غايةٍ واحدة: مواضعُ برهانها لا تصنيفُها المُعلَن.

    التصنيفُ نفسه لا يُمرَّر وسيطًا: لو مُرِّر لبقي مقدّمةً غير محقَّقة ينجح
    عليها الاشتقاقُ كلّه، وهو شكلُ الثغرة التي تُغلقها هذه المرحلة. ويُرفض
    موضعُ البرهان عند الإنشاء ما دامت لا سلطةَ هنا تُصدره.
    """

    aim_id: AimId
    proved_sites: frozenset[TerminationProofSite] = frozenset()

    def __post_init__(self) -> None:
        if not isinstance(self.aim_id, AimId):
            raise AimRecordError("معرّف الغاية من مفردته المغلقة")
        if not isinstance(self.proved_sites, frozenset):
            raise AimRecordError("مواضع البرهان مجموعةٌ مُجمَّدة")
        for site in self.proved_sites:
            if not isinstance(site, TerminationProofSite):
                raise AimRecordError("موضع البرهان من مفردته المغلقة")
        if self.proved_sites:
            raise AimRecordError(NO_TERMINATION_PROOF_EXISTS_TODAY_NOTE)


def _structure_of_proved_sites(
    sites: frozenset[TerminationProofSite],
) -> AimTerminationStructure:
    """صِلْ مواضعَ البرهان ببنية النهاية؛ دالّةٌ تامّة بلا فرعٍ افتراضيّ.

    وموضعا البرهان معًا تناقضٌ يُرفَض لا يُرجَّح أحدهما فيه: بنيةٌ واحدة لا
    تكون مفتوحةً وذاتَ نهايةٍ في آن.
    """

    open_ended = (
        TerminationProofSite.CONSTITUTION_ROW_ESTABLISHING_FRACTAL_OPEN_ENDEDNESS
    )
    terminal = TerminationProofSite.CONSTITUTION_ROW_ESTABLISHING_A_TERMINAL_ARTEFACT
    if open_ended in sites and terminal in sites:
        raise AimRecordError(
            "موضعا برهانٍ متناقضان لبنيةٍ واحدة: لا تكون الغايةُ مفتوحةً "
            "فركتاليًّا وذاتَ نهايةٍ على مصنوعٍ مُسمًّى معًا"
        )
    if open_ended in sites:
        return AimTerminationStructure.OPEN_ENDED_BY_FRACTAL_RECURSION
    if terminal in sites:
        return AimTerminationStructure.TERMINAL_ON_A_NAMED_ARTEFACT
    return AimTerminationStructure.TERMINATION_STRUCTURE_NOT_SETTLED


def _genus_of_structure(
    structure: AimTerminationStructure,
) -> AimAttainmentRefusalGenus:
    """صِلْ كلَّ بنيةٍ بجنس رفضها؛ دالّةٌ تامّة بلا فرعٍ افتراضيّ."""

    if structure is AimTerminationStructure.OPEN_ENDED_BY_FRACTAL_RECURSION:
        return AimAttainmentRefusalGenus.REFUSED_BY_STRUCTURAL_CATEGORY_MISMATCH
    if structure is AimTerminationStructure.TERMINAL_ON_A_NAMED_ARTEFACT:
        return AimAttainmentRefusalGenus.HELD_BY_MISSING_AUTHORITY_TODAY
    return AimAttainmentRefusalGenus.GENUS_NOT_SETTLED


def derive_aim_termination_structure(
    descriptor: AimTerminationDescriptor,
) -> AimTerminationStructure:
    """اشتقّ بنية نهاية الغاية من واصفها لا من تصنيفٍ مُمرَّر.

    ونتيجتُها على أثر اليوم `TERMINATION_STRUCTURE_NOT_SETTLED` في الغايات
    كلّها، لأنّ لا موضعَ برهانٍ قائمًا؛ وهذا تصريحٌ بعجز الاشتقاق لا منزلةٌ
    وسطى.
    """

    return _structure_of_proved_sites(descriptor.proved_sites)


def aim_attainment_refusal_genus(
    descriptor: AimTerminationDescriptor,
) -> AimAttainmentRefusalGenus:
    """أحجزٌ لغياب سلطةٍ رفضُ البلوغ هنا أم امتناعٌ فئويّ؟ مُشتَقٌّ لا مكتوب."""

    return _genus_of_structure(derive_aim_termination_structure(descriptor))


def _assert_no_fields_matching(
    declaring_type: type, markers: tuple[str, ...], message: str
) -> None:
    for item in fields(declaring_type):
        if any(marker in item.name for marker in markers):
            raise RuntimeError(message)


_assert_no_fields_matching(
    AimRecord,
    _ANSWER_BEARING_FIELD_MARKERS,
    "an aim record may not carry an answer, verdict, birth, or indicator field",
)
_assert_no_fields_matching(
    ForeignDeclaredAim,
    _ANSWER_BEARING_FIELD_MARKERS,
    "a foreign declared aim may not carry an answer, verdict, or indicator field",
)
_assert_no_fields_matching(
    AimTerminationDescriptor,
    _ANSWER_BEARING_FIELD_MARKERS,
    "a termination descriptor may not carry an answer, verdict, or indicator field",
)


_DECLARED_AIMS: Final = (
    AimRecord(
        aim_id=AimId.K1,
        question="متى يصير الانتقال مُرخَّصًا لا مقبولًا بنيويًّا فحسب؟",
        what_counts_as_reaching=(
            "سلطةٌ تُصدر `LicensedTransition` حاملةً كفايةً دليلية وسلطةَ "
            "انتقالٍ بين المجالات وسلطةَ طبقة"
        ),
        what_does_not_count=(
            "`StructurallyAdmissibleTransition` مهما كَمُلت فحوصه: "
            "`Representability != Licensability`، "
            "`StructuralValidity != EvidentialSufficiency`"
        ),
        citation=(
            "docs/CONSTITUTION.md، صفّا «Structural admission boundary» "
            "و«No epistemic promotion» (DECLARED_DEFERRED)"
        ),
        engagement=AimEngagement.UNCLASSIFIED_IN_RECORD,
        attainment=AttainmentStanding.NOT_REACHED,
    ),
    AimRecord(
        aim_id=AimId.K2,
        question=(
            "متى يُصدِر حَكَمٌ `BIRTH_IN_SCOPE` أو `NO_BIRTH_IN_SCOPE` بدل "
            "`DEFER_IN_SCOPE` وحدها؟"
        ),
        what_counts_as_reaching=(
            "`IndependentClosureDecision` صادرةٌ عن سلطةٍ فعلية تستهلكها " "بوّابة الحكم"
        ),
        what_does_not_count=("تأجيلٌ مُشتَقّ مهما صحّ اشتقاقه: `DeferredVerdict != Birth`"),
        citation="docs/CONSTITUTION.md، صفّ G0.BV.1 وصفّ G0.BV.1a",
        engagement=AimEngagement.BLOCKED_BY_NAMED_OBSTACLE,
        attainment=AttainmentStanding.NOT_REACHED,
        named_obstacle=(
            "غيابُ سلطةِ تقويمِ محتوى الدليل: `InputProvenance = "
            "DECLARED_DEFERRED` في صفّ G0.BA.1a"
        ),
    ),
    AimRecord(
        aim_id=AimId.K3,
        question=(
            "كيف يُقوَّم بقاءُ الباقي واستنفادُ النماذج الأضعف المرخَّصة، وهما "
            "ما لا سلطةَ له اليوم؟"
        ),
        what_counts_as_reaching=(
            "تقويمٌ فعليّ لمحتوى الدليل يُصيّر `is_independent_closure` قابلةً "
            "لغير `False`"
        ),
        what_does_not_count=(
            "`COMPETITION_RESOLVED_IN_POSET` وحدها: "
            "`ComparabilityClosure != IndependentClosure`؛ ولا تركيبُ "
            "الموصولات الثلاثة في G0.IC.1e: "
            "`SatisfiedConjunctsIsNotIndependentClosure`"
        ),
        citation="docs/CONSTITUTION.md، صفّ G0.IC.1a وصفّ G0.BA.1a وصفّ G0.IC.1e",
        engagement=AimEngagement.BLOCKED_BY_NAMED_OBSTACLE,
        attainment=AttainmentStanding.NOT_REACHED,
        named_obstacle=(
            "غيابُ سلطةِ تقويمِ محتوى الدليل: `InputProvenance = "
            "DECLARED_DEFERRED` في صفّ G0.BA.1a؛ وقد ضيّقه G0.IC.1e إلى "
            "`OneWitnessIsNotResidualCertification` و"
            "`SurvivalReadIsNotMeasuredReplicatedResidual` و"
            "`CoverageIsNotCorrectness`"
        ),
    ),
    AimRecord(
        aim_id=AimId.K4,
        question=(
            "مَن يُصيّر `FrozenFactorRef`/`BornBridgeRef` مُصدَرةً عن سلطة لا "
            "مجرّد عقدٍ صحيح البنية؟"
        ),
        what_counts_as_reaching=(
            "سلطةُ تجميدٍ تُصدرها، فيصحّ `Freeze(F) -> Residual(F, observation)`"
        ),
        what_does_not_count=(
            "نجاحُ الإنشاء: `ConstructibleContract != IssuedByAuthority`"
        ),
        citation="docs/CONSTITUTION.md، صفّ G0.FA.1 وقسم G0.F.1",
        engagement=AimEngagement.NOT_STARTED,
        attainment=AttainmentStanding.NOT_REACHED,
    ),
    AimRecord(
        aim_id=AimId.A1,
        question=("متى تُولَد هويةٌ أو عاملٌ أو إحداثيٌّ بنيويّ عربيّ ولادةً مرخَّصة؟"),
        what_counts_as_reaching=(
            "تباينٌ مقيس ينجو من كلّ إسقاطٍ أضعف مرخَّص ويتكرّر في جولة قياسٍ "
            "ثانية مستقلّة، ثم حكمُ ولادةٍ عليه"
        ),
        what_does_not_count=(
            "أثرُ تدخّلٍ اصطناعيّ مهما دقّ "
            "(`SyntheticInterventionMayGenerateHypothesisOnly`)، ولا تعدادُ "
            "مصادر مقيسة بديلًا عن ذلك التقويم"
        ),
        citation="src/alghanem/arabic/encoding/، وصفوف G0 في الدستور",
        engagement=AimEngagement.UNCLASSIFIED_IN_RECORD,
        attainment=AttainmentStanding.NOT_REACHED,
    ),
    AimRecord(
        aim_id=AimId.A2,
        question=(
            "أيُّ الفروض الثلاثة في `Phase2OpenQuestion` يصحّ: قصورُ السمات "
            "الخمس، أم أن التقسيم ليس جنسًا توزيعيًّا سطحيًّا، أم أنه لا "
            "يُستَرَدّ قبل ولادة متغيّرات بنيوية أدنى؟"
        ),
        what_counts_as_reaching=(
            "حسمٌ صادرٌ عن تجربةٍ مُجمَّدة قبل دليلها وناطقةٍ بمعيار تقويمها"
        ),
        what_does_not_count=(
            "نتيجةٌ سالبةٌ مُسجَّلة، ولا إسقاطُ أحد الفروض: " "`RecordedQuestion != Answer`"
        ),
        citation="docs/CONSTITUTION.md، صفّ A0.PP.1a (DOCUMENTED_OPEN_QUESTION)",
        engagement=AimEngagement.BLOCKED_BY_NAMED_OBSTACLE,
        attainment=AttainmentStanding.NOT_REACHED,
        named_obstacle=(
            "نتيجةٌ سالبة مُسجَّلة بثلاثة فروضٍ قائمة، ولا تجربةَ مُجمَّدة قبل "
            "دليلها تفصل بينها"
        ),
    ),
    AimRecord(
        aim_id=AimId.A3,
        question=(
            "متى يصير `EvidenceGenus.MORPHO_FUNCTIONAL` قابلًا للبناء لا " "مُعلَنًا فقط؟"
        ),
        what_counts_as_reaching="مفردةُ سماتٍ صرفية مولودة هنا ومُجمَّدة قبل دليلها",
        what_does_not_count=(
            "مفردةٌ مستورَدة مهما تحقّقت بصمتها: " "`ImportedVocabulary != BornOntology`"
        ),
        citation="docs/CONSTITUTION.md، صفّا A0.PP.1 وA0.PP.3",
        engagement=AimEngagement.UNCLASSIFIED_IN_RECORD,
        attainment=AttainmentStanding.NOT_REACHED,
    ),
    AimRecord(
        aim_id=AimId.X1,
        question=(
            "كيف يستقبل الغانم محتوًى مُجمَّدًا عند مصدره الأجنبي دون أن يَرِث "
            "إذنًا لم يُمنَح له؟"
        ),
        what_counts_as_reaching=(
            "عقدُ استيرادٍ يُعيد اشتقاق هوية المحتوى محلّيًّا عبر "
            "`alghanem.canonical_content` وحدها، ويرفض التوزيع المُعلَن "
            "المخالف للمشتقّ، ويُثبّت الإصدار المُسجَّل، ويُثبت أن تغطية بصمة "
            "المصدر جزءٌ حقيقيّ أضيقُ من تغطية الهوية المحلية"
        ),
        what_does_not_count=(
            "`FROZEN_LOCAL` الأجنبيّ لا يُرقَّى إلى `SpecificationFreeze.FROZEN` "
            "ولا إلى `Freeze` ولا `E0`: `ForeignFrozenExport != LocalFreeze`"
        ),
        citation=(
            "docs/CONSTITUTION.md، صفّ A0.PP.3، و"
            "src/alghanem/arabic/imported_feature_vocabulary.py"
        ),
        engagement=AimEngagement.UNCLASSIFIED_IN_RECORD,
        attainment=AttainmentStanding.PARTIALLY_REACHED_WITH_NAMED_REMAINDER,
        named_remainder=(
            "مفردتا الوزن والبناء لم تُصدَّرا بعد، وبصمةُ المصدر تُسجَّل كما "
            "أُعلنت ولا تُعاد اشتقاقًا هنا لغياب مخطّط ترميزه وحمولته"
        ),
    ),
    AimRecord(
        aim_id=AimId.E1,
        question="كيف تُطبَّق نتيجةٌ نواةٍ مأذونة على لقطة نواة الموسوعة؟",
        what_counts_as_reaching=(
            "`EncyclopediaGrowthTransition` قائمًا، فيصحّ معه "
            "`DeferPreservesOpenQuestion`"
        ),
        what_does_not_count="لقطةٌ وجبهةُ نموٍّ ساكنتان مهما صحّ عقدهما",
        citation=(
            "docs/CONSTITUTION.md، قسم «Encyclopedia Nucleus» (صفّا "
            "DeferPreservesOpenQuestion وNoIndexFeedbackIntoDiscovery)"
        ),
        engagement=AimEngagement.NOT_STARTED,
        attainment=AttainmentStanding.NOT_REACHED,
    ),
    AimRecord(
        aim_id=AimId.E2,
        question="متى تصير ملاحظةٌ موثَّقة عن هذا المستودع نفسِه معرفةً مرخَّصة؟",
        what_counts_as_reaching=(
            "`SelfKnowledgeBridgeExperiment` بعد قيام دستور دعوى/دليل، فتُميَّز "
            "`DeclaredSelfModel` عن `ImplementedSelfModel` وعن `TestedSelfModel`"
        ),
        what_does_not_count=(
            "توثُّقٌ بنيويّ للمستودع "
            "(`AuthenticatedObservationIsNotEvidence`)، ولا نجاحُ اختبارات "
            "(`TestPassIsNotUniversalTruth`)"
        ),
        citation="docs/CONSTITUTION.md، قسم «Encyclopedia Self-Observation»",
        engagement=AimEngagement.NOT_STARTED,
        attainment=AttainmentStanding.NOT_REACHED,
    ),
    AimRecord(
        aim_id=AimId.T1,
        question=(
            "ما المعيار الذي يرفع الانتظامَ المستقرّ المتكرّر إلى قابلية "
            "التمثيل الجبري الأولى؟ وما التحليل الدقيق لـ`P_0`؟"
        ),
        what_counts_as_reaching=(
            "اشتقاقُ المعيار، وفصلُ `PriorContent` عن `PriorAvailability` عن "
            "`RealityBindingCapacity` بلا مصادرة"
        ),
        what_does_not_count=(
            "ضغطٌ نحو التمثيل: `NeedForHigherRepresentation != "
            "AchievedHigherRepresentation`"
        ),
        citation=(
            "docs/CONSTITUTION.md، "
            "`FirstAlgebraRepresentabilityCriterionNotDerived`، "
            "`ExactFactorization(P_0) = OPEN`، `P0FunctionalMinimalityNotAudited`، "
            "`OrganizedPriorContentBoundaryNotDerived`"
        ),
        engagement=AimEngagement.UNCLASSIFIED_IN_RECORD,
        attainment=AttainmentStanding.NOT_REACHED,
    ),
    AimRecord(
        aim_id=AimId.T2,
        question=(
            "هل التكرار المرصود في «المُعلَن مقابل المُشتَقّ» بنيةٌ واحدة أم "
            "بنيتان: رفضٌ عند المخالفة، مقابل حَملٍ وتقريرٍ بلا سلطة؟"
        ),
        what_counts_as_reaching=(
            "تفسيرٌ مُشتَقّ، لا اسمٌ عامّ ولا صنفُ أساسٍ مُشترَك يُستحدَث بقوّة " "الرصد وحده"
        ),
        what_does_not_count="تكرارُ الصياغة نفسه؛ فهو ما لم يُفسَّر بعد",
        citation=(
            f"docs/CONSTITUTION.md، `{DESIGN_SOURCE_OPEN_QUESTION}` "
            "(OBSERVED_NOT_EXPLAINED)"
        ),
        engagement=AimEngagement.UNCLASSIFIED_IN_RECORD,
        attainment=AttainmentStanding.NOT_REACHED,
    ),
    AimRecord(
        aim_id=AimId.T3,
        question=(
            "هل ثمّة مسارُ دليلٍ ثالث قائمٌ على النقل، مستقلٌّ عن `EMPIRICAL` " "و`FORMAL`؟"
        ),
        what_counts_as_reaching=(
            "حسمٌ عبر مرحلةٍ مخصّصة تعالج أثر ذلك على هوية محتوى التجربة "
            "المُجمَّدة، إذ `evidence_requirements` جزءٌ منها"
        ),
        what_does_not_count=(
            "كثرةُ الشواهد المُعلَنة في بطاقة تدقيقٍ خارجيّ: "
            "`DeclaredWitness != AssessedEvidence`"
        ),
        citation=(
            "docs/CONSTITUTION.md، `ThirdTransmittedEvidenceModeNotDecided` (OPEN)"
        ),
        engagement=AimEngagement.UNCLASSIFIED_IN_RECORD,
        attainment=AttainmentStanding.NOT_REACHED,
    ),
)


AIM_RECORDS: Final[Mapping[AimId, AimRecord]] = MappingProxyType(
    {record.aim_id: record for record in _DECLARED_AIMS}
)

if len(AIM_RECORDS) != len(_DECLARED_AIMS):  # pragma: no cover - guard
    raise RuntimeError("an aim id must not be recorded twice")
if set(AIM_RECORDS) != set(AimId):  # pragma: no cover - guard
    raise RuntimeError("every declared aim id must carry exactly one record")


AIM_TERMINATION_DESCRIPTORS: Final[Mapping[AimId, AimTerminationDescriptor]] = (
    MappingProxyType(
        {aim_id: AimTerminationDescriptor(aim_id=aim_id) for aim_id in AimId}
    )
)

AIM_ATTAINMENT_REFUSAL_GENERA: Final[Mapping[AimId, AimAttainmentRefusalGenus]] = (
    MappingProxyType(
        {
            aim_id: aim_attainment_refusal_genus(descriptor)
            for aim_id, descriptor in AIM_TERMINATION_DESCRIPTORS.items()
        }
    )
)

if set(AIM_TERMINATION_DESCRIPTORS) != set(AimId):  # pragma: no cover - guard
    raise RuntimeError("every declared aim id must carry exactly one descriptor")


FOREIGN_DECLARED_AIMS: Final = (
    ForeignDeclaredAim(
        foreign_aim_id="WEIGHT-FIBER-EDIT-GRAPH-HGEN-INDEPENDENCE",
        source_project_note=(
            "المشروع المصدر نفسه الذي جاءت منه مفردة `gflk.origin_type.v1` "
            "(صفّ A0.PP.3)"
        ),
        declared_as="فيبرٌ مُعلَنٌ بـ٨٧ عقدة، لا يتحقّق هذا المستودع من العدد",
    ),
    ForeignDeclaredAim(
        foreign_aim_id="CHAIN-BANK-CIRCULARITY-OBSTACLE",
        source_project_note=(
            "المشروع المصدر نفسه الذي جاءت منه مفردة `gflk.origin_type.v1` "
            "(صفّ A0.PP.3)"
        ),
        declared_as=(
            "حاجزُ `ChainBank`: دائريةٌ موثَّقةٌ بسببٍ مُسمّى لا غيابًا صامتًا، "
            "ولا يملك هذا المستودع دليلها"
        ),
    ),
)

if any(
    aim.foreign_aim_id in {member.value for member in AimId}
    for aim in FOREIGN_DECLARED_AIMS
):  # pragma: no cover - guard
    raise RuntimeError("a foreign declared aim may not occupy a local aim id")


__all__ = [
    "AIMS_AUTHORITY_NOTE",
    "AIM_ATTAINMENT_REFUSAL_GENERA",
    "AIM_RECORDS",
    "AIM_TERMINATION_DESCRIPTORS",
    "ATTAINMENT_DEFERRAL_NOTE",
    "CATEGORY_MISMATCH_IS_NOT_MISSING_AUTHORITY_NOTE",
    "DESIGN_SOURCE_OPEN_QUESTION",
    "FOREIGN_AIM_BOUNDARY_NOTE",
    "FOREIGN_DECLARED_AIMS",
    "FRACTAL_OPEN_ENDEDNESS_IS_AN_UNSOURCED_CLAIM_NOTE",
    "NOT_SETTLED_IS_NOT_A_MIDPOINT_NOTE",
    "NO_INDICATOR_IN_THIS_MILESTONE_NOTE",
    "NO_PRIORITY_ORDER_NOTE",
    "NO_TERMINATION_PROOF_EXISTS_TODAY_NOTE",
    "REFUSAL_GENUS_IS_DERIVED_NOT_DECLARED_NOTE",
    "TWO_INDEPENDENT_AXES_NOTE",
    "UNCLASSIFIED_IS_NOT_PROGRESS_NOTE",
    "AimAttainmentRefusalGenus",
    "AimEngagement",
    "AimId",
    "AimRecord",
    "AimRecordError",
    "AimTerminationDescriptor",
    "AimTerminationStructure",
    "AttainmentStanding",
    "ForeignDeclaredAim",
    "TerminationProofSite",
    "aim_attainment_refusal_genus",
    "derive_aim_termination_structure",
]
