"""دفترُ سلسلة القرار: ستةَ عشرَ موضعًا مُشتقّةً من الشجرة لا مكتوبةً.

السلسلةُ من الصفر إلى الرابعة عشرة، ومع انقسام الحلقة الثالثة إلى شِقّيها
(الدالُّ وحده، والمدلولُ وحده) تصير مواضعُها ستةَ عشر. و**امتحانُ التخرّج**
آخرُها موضعًا ورقمُه `٧` حيث أُعِدّ، فأُعيدت تسميةُ ما كان `٧`–`١٣` إلى
`٨`–`١٤`: فالأرقامُ لم تعد تتصاعد مع المواضع، والموضعُ هو الترتيبُ والرقمُ
اسمُ القرار لا رتبتُه
(`THE_EXAM_KEEPS_ITS_DECISION_NUMBER_SO_LABELS_NO_LONGER_ASCEND_NOTE`).
وكلُّ موضعٍ يُسمّي
وحدتَه بمسارها في الشجرة، ووجودُ الوحدة **يُقرأ** من الشجرة نفسها؛ وغيابُها
يُنتج `حلقة_غير_مُرمَّزة` لا تخطّيًا صامتًا — على منوال `pipeline_stations`.

**وموضعٌ واحدٌ مادّتُه خارج هذه الشجرة**: امتحانُ التخرّج يُسمّي مُصدِّرَ
`hamil` ويُعلَّم `موصول_خارج_الشجرة` — فالعقدُ الارتباطُ بمخرج المُصدِّر لا
وجودُ ملفٍّ هنا، ولا يُصطنَع له مسارٌ نسبيٌّ ميتٌ داخل `src/alghanem/arabic`.
وهو لذلك `حلقة_غير_مُرمَّزة` بحكمِ العلامة لا بمصادفةِ مسارٍ مفقود.

**وكلُّ حلقةٍ شرطٌ لما بعدها، فالبلوغُ مُشتَقٌّ بالتتابع لا بالترميز وحده.**
حلقةٌ مُرمَّزةٌ سبقتها حلقةٌ غيرُ بالغة تُقرأ `مسبوقة_بحلقة_غير_بالغة`، لا
`بالغة`. وهذا بعينه ما يمنع قراءةَ السلسلة تامّةً بينما الحلقتان الأولى
والثانية (الحاملُ، و(حامل، حالة)) مؤجَّلتان بقانونٍ مُسمًّى في الدستور.

**والتأجيلُ بقانونٍ تصريحٌ لا قراءة.** الحلقةُ التي لا وحدةَ لها في الشجرة
أصلًا تُعلِن اسمَ القانون الذي أجّلها، ويُصرَّح بأن هذا إعلانٌ لا استنتاجٌ من
الشجرة (`LAW_DEFERRAL_IS_DECLARED_NOT_READ_NOTE`)؛ أمّا الحلقةُ التي تُسمّي
وحدةً غيرَ موجودة فحالُها مقروءةٌ من الشجرة كغيرها.

**والقيودُ الحاكمة ليست حلقاتٍ في السلسلة بل إطارُها**، فتُسجَّل على حدة
بحالٍ صريحة؛ وكلُّها غيرُ مُرمَّزٍ اليوم، **وغيابُها ليس غيابًا واحدًا**:
القيدُ (أ) ينتظر فكرةً كلّيةً غيرَ مكتوبة، ولا تُكتَب في هذه الدورة
(`UNIVERSAL_IDEA_IS_ABSENT_NOTE`)؛ والقيدُ (ب) لا ينتظر نظريةً بل تطبيقًا،
وقد جرى التطبيقُ الأوّل فعلًا على بطاقة (مَلِك) في الناس:٢ فوقف عند الحلقة
الرابعة لغيابٍ مُسمًّى (`APPLICATION_STOPS_AT_THE_FOURTH_LINK_NOTE`)، **وجنسُ
ذلك الوقوف حُسِم بعدُ** باشتقاق بنية الاستشهاد المعجميّ في
`lexical_transmission`: خطأٌ فئويٌّ بنيويّ لا حجزٌ لغياب سلطةٍ اليوم. فالفرقُ
بين الغيابين مُسجَّلٌ في سبب كلٍّ منهما، ولا تُفتَح له مفردةٌ ثالثة قبل أن
يُكسَب: حالُ القيد ثنائيةٌ حتى يقوم تطبيقٌ كاملٌ يُشتَقّ منه الإغلاق. والقيدُ
(٧) — الحاكمان اللذان يحكمان امتحانَ التخرّج — ثالثُها، وغيابُه من جنسٍ ثالث:
لا فراغَ نظريّ ولا تطبيقٌ انقطع، بل **بناءٌ لم يقع بعدُ** على مادّةٍ موصولةٍ
خارجَ الشجرة (`GRADUATION_EXAM_ABSENCE_GUARDS_NOTE`).

**والدفترُ قراءةٌ لا سلطة**: لا يُصدر ولادةً ولا تجميدًا ولا `E0`، ولا تقرؤه
وحدةٌ في `kernel/`.
"""

from __future__ import annotations

from dataclasses import dataclass, fields
from enum import Enum
from pathlib import Path
from typing import Final

__all__ = [
    "APPLICATION_STOPS_AT_THE_FOURTH_LINK_NOTE",
    "ARABIC_PACKAGE_RELATIVE_PATH",
    "CHAIN_LEDGER_IS_NOT_A_GATE_NOTE",
    "EACH_LINK_CONDITIONS_THE_NEXT_NOTE",
    "GOVERNING_CONSTRAINTS",
    "GRADUATION_EXAM_ABSENCE_GUARDS_NOTE",
    "GRADUATION_EXAM_MATERIAL_REFERENCE",
    "LAW_DEFERRAL_IS_DECLARED_NOT_READ_NOTE",
    "ONE_MODULE_MAY_SERVE_TWO_LINKS_NOTE",
    "OUT_OF_TREE_BOND_IS_TO_AN_OUTPUT_NOT_A_PATH_NOTE",
    "OUT_OF_TREE_MARKER",
    "THE_EXAM_KEEPS_ITS_DECISION_NUMBER_SO_LABELS_NO_LONGER_ASCEND_NOTE",
    "UNIVERSAL_IDEA_IS_ABSENT_NOTE",
    "ChainLedger",
    "ChainLinkCoding",
    "ChainLinkDeclaration",
    "ChainLinkReach",
    "ChainLinkReading",
    "DecisionChainError",
    "GoverningConstraint",
    "GoverningConstraintStanding",
    "read_chain",
    "repository_root_path",
]


class DecisionChainError(ValueError):
    """رفضٌ صريحٌ في دفتر سلسلة القرار."""


class ChainLinkCoding(Enum):
    """حالُ ترميز الحلقة؛ ثلاثيةٌ مغلقة، والتأجيلُ بقانونٍ عضوٌ مُسمًّى فيها."""

    مُرمَّزة = "مُرمَّزة"
    حلقة_غير_مُرمَّزة = "حلقة_غير_مُرمَّزة"
    مؤجَّلة_بقانون = "مؤجَّلة_بقانون"


class ChainLinkReach(Enum):
    """بلوغُ الحلقة، مُشتَقًّا بالتتابع؛ والترميزُ وحده لا يُنتج بلوغًا."""

    بالغة = "بالغة"
    مسبوقة_بحلقة_غير_بالغة = "مسبوقة_بحلقة_غير_بالغة"
    غير_بالغة_بذاتها = "غير_بالغة_بذاتها"


class GoverningConstraintStanding(Enum):
    """حالُ القيد الحاكم؛ ثنائيةٌ مغلقة، والغيابُ مُسمًّى لا مطويّ."""

    مُرمَّز = "مُرمَّز"
    مُصرَّح_غير_مُرمَّز = "مُصرَّح_غير_مُرمَّز"


ARABIC_PACKAGE_RELATIVE_PATH: Final[str] = "src/alghanem/arabic"

OUT_OF_TREE_MARKER: Final[str] = "موصول_خارج_الشجرة:"

GRADUATION_EXAM_MATERIAL_REFERENCE: Final[str] = (
    f"{OUT_OF_TREE_MARKER}Saleh1967/hamil-hala-zaman-program@main:"
    "induction/export_seals.py"
)

OUT_OF_TREE_BOND_IS_TO_AN_OUTPUT_NOT_A_PATH_NOTE: Final[str] = (
    "الموضعُ الذي مادّتُه في مستودعٍ آخر يُعلَّم `موصول_خارج_الشجرة` ولا "
    "يُصطنَع له مسارٌ نسبيٌّ داخل `src/alghanem/arabic`: فالإشارةُ إلى بيتٍ "
    "مجاورٍ عقدُها الارتباطُ بمخرج المُصدِّر لا بوجود ملفٍّ هنا، ومسارٌ نسبيٌّ "
    "يشير إلى ما ليس في هذه الشجرة مسارٌ ميتٌ يُقرأ غيابًا في الشجرة وهو ليس "
    "منها أصلًا. والموصولُ لذلك `حلقة_غير_مُرمَّزة` بحكمِ العلامة لا بمصادفةِ "
    "مسارٍ مفقود، ولا يُقرأ `مُرمَّزة` ولو وُجد في الشجرة ملفٌّ بذلك الاسم."
)

GRADUATION_EXAM_ABSENCE_GUARDS_NOTE: Final[str] = (
    "غيابُ هذا القيد ثلاثةُ شروطٍ مُصرَّحةٌ نصًّا لا عدّادًا ولا حكمًا: "
    "**(١)** حارسُ غيابٍ يُشغَّل — فتحُ الملفّات مراقَبٌ أو `ast` على البانِي — "
    "فإن مسّ البانِي بايتةً واحدةً من نصّ المصدر سقط البابُ بتمامه. "
    "**(٢)** إن نُقل رقمٌ إلى هذه الشجرة مكتوبًا بدل موضعه، سقط القرارُ لا "
    "الرقم: نسخةٌ ثانيةٌ تتخلّف هي القبرُ الذي جاء البابُ الخامس يفتحه. "
    "**(٣)** سلسلةُ الشهادة مفتوحةُ الطرف: الدالُّ مسنودٌ إلى البايتات وحدَها، "
    "ولا يُصادِق عقدٌ على اللغة فيدور الدور. "
    "والمادّةُ موصولةٌ لا منقولة: مُصدِّرُ `hamil` يُخرج أختامَ [بوّابة] "
    "بإزاحاتها البايتية وبصمةِ وديعةِ كلٍّ منها وفواتيرَها بأحكامها المشتقّة. "
    "والرقمُ الذي حُذف في الجولة السابقة ساقطٌ ولا يُحيا: حُذف بحكمٍ مودَعٍ في "
    "`encyclopedia/tariqa/02_tariqa_aqliyya/README.md` — رقمٌ بلا فاتورةٍ "
    "ممنوعٌ بالباب الثاني عشر، والنسخُ رفعُ حكمٍ لا محوُ سجلّ (الباب العاشر). "
    "والترميزُ ممنوعٌ قبل التطبيق: إعلانُه ادّعاءُ بناءٍ لم يقع."
)

THE_EXAM_KEEPS_ITS_DECISION_NUMBER_SO_LABELS_NO_LONGER_ASCEND_NOTE: Final[str] = (
    "امتحانُ التخرّج يحمل رقمَ قراره `٧` حيث أُعِدّ، فأُعيدت تسميةُ ما كان "
    "`٧`–`١٣` إلى `٨`–`١٤` وبقي كلُّ موضعٍ وترتيبٍ ومادّةٍ على حاله. وعنه "
    "لزمَ أثران يُصرَّحان ولا يُسكَتان: **(١)** الأرقامُ لم تعد تتصاعد مع "
    "المواضع — فالامتحانُ آخرُ السلسلة موضعًا ورقمُه `٧` — فالموضعُ هو "
    "الترتيبُ والرقمُ اسمُ القرار لا رتبتُه. **(٢)** الرقمُ `٧` يقع على "
    "الحلقة وعلى قيدها الحاكم معًا، وهذا مقصودٌ لا اشتباه: القيدُ إطارُ هذه "
    "الحلقة بعينها لا قرارٌ آخر، وحارسٌ أدناه يلزم تطابقَهما فلا يفترقان صمتًا."
)

EACH_LINK_CONDITIONS_THE_NEXT_NOTE: Final[str] = (
    "كلُّ حلقةٍ شرطٌ لما بعدها، فالبلوغُ مُشتَقٌّ بالتتابع لا بالترميز وحده: "
    "حلقةٌ مُرمَّزةٌ سبقتها حلقةٌ غيرُ بالغةٍ تُقرأ `مسبوقة_بحلقة_غير_بالغة`، "
    "وقراءتُها «بالغة» تُظهِر السلسلةَ تامّةً وهي منقطعةٌ عند موضعٍ سابق."
)

LAW_DEFERRAL_IS_DECLARED_NOT_READ_NOTE: Final[str] = (
    "التأجيلُ بقانونٍ تصريحٌ لا استنتاجٌ من الشجرة: الحلقةُ التي لا وحدةَ لها "
    "أصلًا تُسمّي القانونَ الذي أجّلها في الدستور، ولا يُقرأ غيابُ وحدتها "
    "تأجيلًا من تلقاء نفسه. والفارقُ بينه وبين `حلقة_غير_مُرمَّزة` فارقُ "
    "مصدرٍ لا فارقُ درجة."
)

ONE_MODULE_MAY_SERVE_TWO_LINKS_NOTE: Final[str] = (
    "وحدةٌ واحدةٌ قد تخدم حلقتين متغايرتين (كـ`manat_verification` لتحقيق "
    "المناط وللبيان بالقول والفعل)، فلا تُشترَط وحدةٌ لكل حلقة؛ واشتراطُه "
    "يدفع إلى شقِّ وحدةٍ قائمةٍ لأجل الجدول، وذلك ترتيبُ الشجرة على الدفتر."
)

UNIVERSAL_IDEA_IS_ABSENT_NOTE: Final[str] = (
    "لا «فكرة كلّية» معلَنةٌ مكتوبةٌ لـGFLK في هذا المستودع يُقاس عليها توافقُ "
    "الأدوات الحاملة لوجهة نظرٍ معرفية؛ فالقيدُ الأوّل مُصرَّحٌ غيرُ مُرمَّز، "
    "وفراغُه مُسجَّلٌ بنيويًّا هنا لا مطويٌّ في نثر. وكتابتُها مهمّةٌ مستقلّة لا "
    "تُحشَر في هذه الدورة."
)

APPLICATION_STOPS_AT_THE_FOURTH_LINK_NOTE: Final[str] = (
    "الاختبارُ العمليّ المقبولُ وحده تطبيقٌ كاملٌ ناجزٌ على كلمةٍ أو آيةٍ "
    "حقيقية، لا وصفُ مرحلةٍ أخرى من مراحل القياس. وقد سِيقت بطاقةُ (مَلِك) في "
    "الناس:٢ على الحلقات ٤–٦ و٨–١٤ فعلًا، فوقفت عند **الحلقة الرابعة (الوضع "
    "بالنقل)** "
    "لغيابٍ مُسمًّى: لا تُشتَقّ من طريقها المعجميّ درجةٌ من `TransmissionStanding`، "
    "وهو عينُ ما تفتقده الحلقةُ الثالثة عشرة. **وجنسُ هذا الوقوف حُسِم بعدُ ولم "
    "يبقَ منتظَرًا**: سِيقت البطاقاتُ الأربع (قُروء، وأنّى، ومَلِك، وعسعس) — وهي "
    "الأجناسُ الثلاثة: اسمٌ وأداةٌ وفعلٌ — على واصف "
    "`lexical_transmission`، فاشتُقَّت بنيةُ استشهادها المعجميِّ "
    "`عنوان_واحد_مسطح`، وجنسُ امتناعها `ممتنعة_بخطأ_فئوي_بنيوي` لا حجزًا لغياب "
    "سلطةٍ اليوم (`FlatTitleCitationIsNotATransmissionChain`). فالقيدُ (ب) "
    "مُصرَّحٌ غيرُ مُرمَّزٍ لا لفراغٍ نظريّ كالقيد (أ)، بل لأنّ التطبيق الأوّل "
    "انقطع عند موضعٍ مُسمًّى بعلّةٍ بنيويّةٍ مُشتَقّة؛ ووحدةٌ تقيس تطبيقًا لم "
    "يكتمل هي بعينها «وصفُ مرحلةٍ أخرى من آلة القياس» الذي يمنعه هذا القيدُ نفسه."
)

CHAIN_LEDGER_IS_NOT_A_GATE_NOTE: Final[str] = (
    "دفترُ السلسلة قراءةٌ للشجرة لا سلطةٌ عليها: لا يُصدر ولادةً ولا تجميدًا "
    "ولا `E0`، ولا تقرؤه وحدةٌ في `kernel/`."
)

_DECLARED_LINKS: Final[tuple[tuple[int, str, str, str | None, str | None], ...]] = (
    (
        0,
        "٠",
        "نقطةُ الترميز بلا هويةٍ ولا معنى",
        "encoding/observation.py",
        None,
    ),
    (
        1,
        "١",
        "الحاملُ جنسًا مجرَّدًا",
        None,
        "KnotNotEssence",
    ),
    (
        2,
        "٢",
        "(حامل، حالة) مشتقًّا في عالم الدالّ",
        None,
        "KnotNotEssence",
    ),
    (
        3,
        "٣أ",
        "الدالُّ وحده: البروتوكول الإحصائيّ",
        "distributional_probe_report.py",
        None,
    ),
    (
        4,
        "٣ب",
        "المدلولُ وحده: التحليلُ الفلسفيّ",
        "madlul_alone_formal.py",
        None,
    ),
    (
        5,
        "٤",
        "الوضع: الدالُّ والمدلولُ معًا، بالنقل وحده",
        "wad_naql.py",
        None,
    ),
    (
        6,
        "٥",
        "تحقيقُ المناط",
        "manat_verification.py",
        None,
    ),
    (
        7,
        "٦",
        "ما يخلّ بالفهم عند الإجمال",
        "comprehension_defect.py",
        None,
    ),
    (
        8,
        "٨",
        "البيانُ بالقول مقدَّمًا على البيان بالفعل",
        "manat_verification.py",
        None,
    ),
    (
        9,
        "٩",
        "المنطوقُ والمفهوم",
        "mantuq_mafhum_ifada.py",
        None,
    ),
    (
        10,
        "١٠",
        "القياسُ بعلّةٍ منطبقة",
        "qiyas_rabt_registration.py",
        None,
    ),
    (
        11,
        "١١",
        "العمومُ والخصوص",
        "umum_khusus.py",
        None,
    ),
    (
        12,
        "١٢",
        "الروايةُ والدراية",
        "riwaya_diraya_registration.py",
        None,
    ),
    (
        13,
        "١٣",
        "درجةُ اليقين",
        "transmission_standing.py",
        None,
    ),
    (
        14,
        "١٤",
        "المعلومةُ والمفهوم",
        "maluma_mafhum.py",
        None,
    ),
    (
        15,
        "٧",
        "امتحانُ التخرّج: أيبني البانِي برهانًا على مقاديرَ لم يرَ نصَّها؟",
        GRADUATION_EXAM_MATERIAL_REFERENCE,
        None,
    ),
)


def repository_root_path() -> Path:
    """جذرُ المستودع، مُشتقًّا من موضع هذه الوحدة لا مكتوبًا."""

    return Path(__file__).resolve().parents[3]


def _require_non_blank(value: str, label: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise DecisionChainError(f"{label} نصٌّ غير فارغ.")
    return value


@dataclass(frozen=True, slots=True)
class ChainLinkDeclaration:
    """إعلانُ موضعٍ واحد: موقعُه، ورقمُه، وعنوانُه، ووحدتُه أو قانونُ تأجيله."""

    position: int
    label: str
    title: str
    module_relative_path: str | None
    deferral_law: str | None

    def __post_init__(self) -> None:
        if isinstance(self.position, bool) or not isinstance(self.position, int):
            raise DecisionChainError("موقعُ الحلقة عددٌ صحيح.")
        if not 0 <= self.position <= 15:
            raise DecisionChainError(
                "مواقعُ السلسلة ستةَ عشرَ موضعًا من الصفر إلى الخامس عشر؛ "
                "والحلقةُ الثالثة شِقّان لا موضعٌ واحد."
            )
        _require_non_blank(self.label, "رقمُ الحلقة")
        _require_non_blank(self.title, "عنوانُ الحلقة")
        if (self.module_relative_path is None) == (self.deferral_law is None):
            raise DecisionChainError(
                "لكلّ حلقةٍ وحدةٌ مُسمّاةٌ في الشجرة أو قانونُ تأجيلٍ مُسمًّى، "
                "ولا يجتمعان ولا يرتفعان: فالجمعُ يُخفي المقروءَ خلف "
                "المُصرَّح، والرفعُ حلقةٌ بلا موضعٍ يُقرأ."
            )
        if self.module_relative_path is not None:
            _require_non_blank(self.module_relative_path, "وحدةُ الحلقة")
            if self.module_relative_path.endswith("__init__.py"):
                raise DecisionChainError("وحدةُ الحلقة وحدةٌ مُسمّاة، لا ملفَّ تجميعِ حزمة.")
            if self.is_bound_out_of_tree:
                _require_non_blank(
                    self.module_relative_path[len(OUT_OF_TREE_MARKER) :],
                    "مرجعُ المُصدِّر الموصول",
                )
        if self.deferral_law is not None:
            _require_non_blank(self.deferral_law, "قانونُ التأجيل")

    @property
    def is_bound_out_of_tree(self) -> bool:
        """أموصولةٌ مادّةُ هذا الموضع بمخرج مُصدِّرٍ خارج هذه الشجرة؟"""

        return (
            self.module_relative_path is not None
            and self.module_relative_path.startswith(OUT_OF_TREE_MARKER)
        )

    @property
    def module_path(self) -> str | None:
        """مسارُ الوحدة منسوبًا إلى جذر المستودع، أو `None` للمؤجَّلة بقانون.

        والموصولُ خارج الشجرة يُعاد مرجعًا معلَّمًا كما هو، فلا يُصطنَع له
        مسارٌ نسبيٌّ ميتٌ داخل `src/alghanem/arabic`.
        """

        if self.module_relative_path is None:
            return None
        if self.is_bound_out_of_tree:
            return self.module_relative_path
        return f"{ARABIC_PACKAGE_RELATIVE_PATH}/{self.module_relative_path}"


@dataclass(frozen=True, slots=True)
class ChainLinkReading:
    """قراءةُ حلقةٍ واحدة: إعلانُها، وحالُ ترميزها المُشتقّة من الشجرة."""

    declaration: ChainLinkDeclaration
    coding: ChainLinkCoding

    def __post_init__(self) -> None:
        if not isinstance(self.declaration, ChainLinkDeclaration):
            raise DecisionChainError("إعلانُ الحلقة إعلانٌ مُصاغ.")
        if not isinstance(self.coding, ChainLinkCoding):
            raise DecisionChainError("حالُ الترميز من مفردتها المغلقة الثلاثية.")
        deferred_by_law = self.declaration.deferral_law is not None
        if deferred_by_law != (self.coding is ChainLinkCoding.مؤجَّلة_بقانون):
            raise DecisionChainError(
                "«مؤجَّلة_بقانون» حالُ من لا وحدةَ له في الشجرة وحده؛ "
                "وإلصاقُها بحلقةٍ تُسمّي وحدةً يقرأ التصريحَ مكان الشجرة."
            )

    @property
    def is_coded(self) -> bool:
        return self.coding is ChainLinkCoding.مُرمَّزة


@dataclass(frozen=True, slots=True)
class ChainLedger:
    """السلسلةُ كلّها؛ والبلوغُ يُشتَقّ منها بالتتابع ولا يُكتَب في حقل."""

    readings: tuple[ChainLinkReading, ...]

    def __post_init__(self) -> None:
        if not isinstance(self.readings, tuple) or not self.readings:
            raise DecisionChainError("الدفترُ سلسلةٌ غيرُ فارغةٍ من القراءات.")
        for reading in self.readings:
            if not isinstance(reading, ChainLinkReading):
                raise DecisionChainError("كلُّ عنصرٍ في الدفتر قراءةُ حلقة.")
        positions = tuple(item.declaration.position for item in self.readings)
        if positions != tuple(range(len(self.readings))):
            raise DecisionChainError(
                "مواقعُ الدفتر متعاقبةٌ من الصفر بلا فجوةٍ ولا تكرار؛ "
                "والفجوةُ تُخفي شرطًا سابقًا فتُظهِر بلوغًا لم يقع."
            )

    @property
    def reach(self) -> tuple[ChainLinkReach, ...]:
        """بلوغُ كلّ حلقةٍ مُشتَقًّا بالتتابع: لا بلوغَ بعد حلقةٍ غير بالغة."""

        derived: list[ChainLinkReach] = []
        broken = False
        for reading in self.readings:
            if broken:
                derived.append(ChainLinkReach.مسبوقة_بحلقة_غير_بالغة)
                continue
            if reading.is_coded:
                derived.append(ChainLinkReach.بالغة)
                continue
            broken = True
            derived.append(ChainLinkReach.غير_بالغة_بذاتها)
        return tuple(derived)

    @property
    def first_unreached(self) -> ChainLinkReading | None:
        """أوّلُ حلقةٍ انقطعت عندها السلسلة، أو `None` إن بلغت كلُّها."""

        for reading, reach in zip(self.readings, self.reach):
            if reach is not ChainLinkReach.بالغة:
                return reading
        return None

    @property
    def is_fully_reached(self) -> bool:
        return self.first_unreached is None


@dataclass(frozen=True, slots=True)
class GoverningConstraint:
    """قيدٌ حاكمٌ على السلسلة كلّها؛ إطارُها لا حلقةٌ فيها."""

    label: str
    title: str
    question: str
    standing: GoverningConstraintStanding
    gap_note: str

    def __post_init__(self) -> None:
        for name in ("label", "title", "question", "gap_note"):
            _require_non_blank(getattr(self, name), name)
        if not isinstance(self.standing, GoverningConstraintStanding):
            raise DecisionChainError("حالُ القيد من مفردتها المغلقة الثنائية.")
        if self.standing is GoverningConstraintStanding.مُرمَّز:
            raise DecisionChainError(
                "لا قيدَ حاكمٌ مُرمَّزٌ اليوم: القيدُ الأوّل ينتظر فكرةً كلّيةً "
                "غيرَ مكتوبة، والثاني ينتظر تطبيقًا كاملًا ناجزًا على كلمةٍ أو "
                "آية؛ فإعلانُ الترميز ادّعاءُ بناءٍ لم يقع."
            )

    @property
    def is_in_the_chain(self) -> bool:
        """القيدُ إطارُ السلسلة لا موضعٌ فيها، فلا يُعَدّ في مواضعها."""

        return False


GOVERNING_CONSTRAINTS: Final[tuple[GoverningConstraint, ...]] = (
    GoverningConstraint(
        label="أ",
        title="الفكرةُ والطريقةُ والوسيلة",
        question=(
            "أهذه الأداةُ وسيلةٌ محايدةٌ حرّةُ الاستعارة (كـ`sha256` و`pytest`)، "
            "أم أداةٌ تحمل وجهةَ نظرٍ معرفيةً (كسلّم اليقين المتدرّج) فتلزمها "
            "موافقةُ الفكرة الكلّية المعلَنة؟"
        ),
        standing=GoverningConstraintStanding.مُصرَّح_غير_مُرمَّز,
        gap_note=UNIVERSAL_IDEA_IS_ABSENT_NOTE,
    ),
    GoverningConstraint(
        label="ب",
        title="الجدّيةُ والإفادة",
        question=(
            "أمُوجَّهةٌ السلسلةُ في تطبيقها الفعليّ إلى واقع اللغة نفسها لا إلى "
            "وصف آلة القياس ذاتها؟ وأنتيجتُها التراكمية تُفيد حكمًا جديدًا "
            "يُحسِن السكوتُ عليه، أم هي هذيانٌ منظَّم؟"
        ),
        standing=GoverningConstraintStanding.مُصرَّح_غير_مُرمَّز,
        gap_note=APPLICATION_STOPS_AT_THE_FOURTH_LINK_NOTE,
    ),
    GoverningConstraint(
        label="٧",
        title=(
            "صفرُ الخلاف يشهد أنّ الرقمَ يُولَد ولا يكفي، وإشارةُ الفاتورة "
            "وحدَها تحكم أنّه ربح"
        ),
        question=(
            "أتُشتَقّ من الأختام الحيّة ذاتِ الفواتير الصحيحة — مقروءةً من "
            "مواضعها في المستودع المُخرِج لا من نسخةٍ منقولة — نتيجةٌ لم تكن "
            "مكتوبةً في طرفٍ منهما؟ فصفرُ الخلاف يشهد أنّ الرقمَ يُولَد ولا "
            "يكفي: هويةُ المرآة تُولَد أيضًا وجدولُها فارغ "
            "(`hamil · induction/mirror.py`)؛ وإشارةُ الفاتورة وحدَها "
            "(`deposit_law.verdict`) تحكم أنّه ربح، لا إجماعُ الشهود."
        ),
        standing=GoverningConstraintStanding.مُصرَّح_غير_مُرمَّز,
        gap_note=GRADUATION_EXAM_ABSENCE_GUARDS_NOTE,
    ),
)


def read_chain(root: Path | None = None) -> ChainLedger:
    """اقرأ مواضعَ السلسلة الخمسةَ عشر، مُشتقًّا وجودَ كلّ وحدةٍ من الشجرة."""

    base = repository_root_path() if root is None else root
    if not isinstance(base, Path):
        raise DecisionChainError("جذرُ المستودع مسار.")
    package = base / ARABIC_PACKAGE_RELATIVE_PATH
    if not package.is_dir():
        raise DecisionChainError(
            f"طبقةُ العربية غير موجودة عند {package}: شجرةٌ غائبةٌ تُقرأ «لا "
            "وحدات» وهو ادّعاءٌ لم تُقرأ الشجرة لأجله."
        )
    readings: list[ChainLinkReading] = []
    for position, label, title, relative, law in _DECLARED_LINKS:
        declaration = ChainLinkDeclaration(
            position=position,
            label=label,
            title=title,
            module_relative_path=relative,
            deferral_law=law,
        )
        if relative is None:
            coding = ChainLinkCoding.مؤجَّلة_بقانون
        elif declaration.is_bound_out_of_tree:
            coding = ChainLinkCoding.حلقة_غير_مُرمَّزة
        elif (package / relative).is_file():
            coding = ChainLinkCoding.مُرمَّزة
        else:
            coding = ChainLinkCoding.حلقة_غير_مُرمَّزة
        readings.append(ChainLinkReading(declaration=declaration, coding=coding))
    return ChainLedger(readings=tuple(readings))


def _assert_no_fields_matching(markers: tuple[str, ...]) -> None:
    for declaring_type in (
        ChainLinkDeclaration,
        ChainLinkReading,
        ChainLedger,
        GoverningConstraint,
    ):
        for field in fields(declaring_type):
            for marker in markers:
                if marker in field.name.lower():
                    raise RuntimeError(
                        f"{declaring_type.__name__} يحمل حقلاً محظورًا: {field.name}"
                    )


if len(ChainLinkCoding) != 3:  # pragma: no cover - guard
    raise RuntimeError("حالُ الترميز ثلاثيةٌ مغلقة، والتأجيلُ بقانونٍ عضوٌ فيها.")
if len(ChainLinkReach) != 3:  # pragma: no cover - guard
    raise RuntimeError("البلوغُ ثلاثيٌّ مغلق: بالغة، ومنقطعةٌ بذاتها، ومسبوقةٌ بمنقطعة.")
if len(GoverningConstraintStanding) != 2:  # pragma: no cover - guard
    raise RuntimeError("حالُ القيد الحاكم ثنائيةٌ مغلقة.")
if len(_DECLARED_LINKS) != 16:  # pragma: no cover - guard
    raise RuntimeError(
        "مواضعُ السلسلة ستةَ عشر: ١٤ حلقةً، وشِقٌّ ثانٍ للثالثة، وامتحانُ التخرّج."
    )
if tuple(row[0] for row in _DECLARED_LINKS) != tuple(range(16)):  # pragma: no cover
    raise RuntimeError("مواقعُ السلسلة متعاقبةٌ من الصفر بلا فجوة.")
if len({row[1] for row in _DECLARED_LINKS}) != 16:  # pragma: no cover - guard
    raise RuntimeError("أرقامُ الحلقات متغايرة، ورقمٌ مُعادٌ يُخفي موضعًا تحت آخر.")
if (
    sum(  # pragma: no cover - guard
        1
        for row in _DECLARED_LINKS
        if row[3] is not None and row[3].startswith(OUT_OF_TREE_MARKER)
    )
    != 1
):
    raise RuntimeError("موضعٌ واحدٌ وحده مادّتُه موصولةٌ خارج الشجرة، وهو امتحانُ التخرّج.")
if len(GOVERNING_CONSTRAINTS) != 3:  # pragma: no cover - guard
    raise RuntimeError("القيودُ الحاكمة ثلاثة، وليست حلقاتٍ في السلسلة.")
if (  # pragma: no cover - guard
    _DECLARED_LINKS[-1][1] != GOVERNING_CONSTRAINTS[-1].label
):
    raise RuntimeError(
        "رقمُ امتحان التخرّج واحدٌ في السلسلة وفي قيده الحاكم، فلا يفترقان صمتًا."
    )
_assert_no_fields_matching(("count", "number", "total", "verdict", "birth", "freeze"))
