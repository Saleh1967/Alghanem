"""معينٌ مشترك: سَوقُ بطاقةٍ واحدة على حلقات سلسلة القرار ٤–١٣.

هذا **معينُ اختبارٍ لا وحدةُ قياس**: لا يُنشئ سلطةً ولا مفردةً ولا دفترًا، ولا
يُصدر ولادةً ولا تجميدًا ولا `E0`، ولا تقرؤه وحدةٌ في الشجرة. وقد أُخرِج من
اختبار بطاقة (مَلِك) وحده ليُساق عليه أكثرُ من بطاقة بالمنهج نفسه، فيُقرأ موضعُ
الوقوف من البطاقات جميعًا لا من واحدةٍ يُعمَّم حكمُها.

**والوقوفُ مُشتَقٌّ من البطاقة لا مكتوبٌ هنا**: لكلّ حلقةٍ إعلانٌ تحتاجه من
مفرداتها المغلقة، ويُفحَص نصُّ البطاقة كلُّه عن أعضاء تلك المفردات؛ فإن لم يَرِد
منها عضوٌ فالحلقةُ واقفةٌ لغياب إعلانٍ مُسمًّى.

**والحلقةُ الرابعة وحدها لا تُقرأ بالبحث النصّيّ بل بالاشتقاق**: درجةُ النقل
تُشتَقّ من طريق النقل المعجميّ المُعلَن في البطاقة
(`alghanem.arabic.lexical_transmission`)، فإن لم يقم طريقٌ فلا درجة، ووقوفُ
الحلقة حينئذٍ مُعلَّلٌ ببنية الاستشهاد وجنس امتناعها لا بغياب كلمةٍ مكتوبة.

**والبلوغُ يُشتَقّ بالتتابع كما في `decision_chain`**: حلقةٌ قامت وقد سبقتها
واقفةٌ لا تُقرأ بالغة، وإلا ظهر التطبيقُ تامًّا وهو منقطعٌ عند موضعٍ سابق.
"""

import re
from dataclasses import dataclass
from enum import Enum
from typing import Any

from alghanem.arabic.comprehension_defect import canonical_defect_classification
from alghanem.arabic.lexical_transmission import (
    card_lexical_citation_structure,
    card_lexical_wad_path,
    card_transmission_standing,
)
from alghanem.arabic.maluma_mafhum import SanadOrigin, SemanticTarget
from alghanem.arabic.manat_verification import (
    FIL_MODEL_ID,
    QAWL_MODEL_ID,
    derive_bayan_models,
    read_manat_qarain,
)
from alghanem.arabic.mantuq_mafhum_ifada import DalalaChannel, MafhumKind
from alghanem.arabic.qiyas_rabt_registration import (
    IllaApplication,
    frozen_asl_references,
)
from alghanem.arabic.riwaya_diraya_registration import DirayaBranch, RiwayaStanding
from alghanem.arabic.text_key import comparison_key
from alghanem.arabic.transmission_standing import (
    KnowledgeBasis,
    RepetitionPattern,
    SourceIndependence,
    UnconstructibilityGenus,
)
from alghanem.arabic.umum_khusus import DalilScope, RuleGenus


def _texts(payload: Any) -> tuple[str, ...]:
    """كلُّ نصوص البطاقة، مفاتيحَ وقيَمًا، مسرودةً بلا تأويل."""

    if isinstance(payload, str):
        return (payload,)
    if isinstance(payload, dict):
        collected: list[str] = []
        for key, value in payload.items():
            collected.extend(_texts(key))
            collected.extend(_texts(value))
        return tuple(collected)
    if isinstance(payload, list):
        collected = []
        for item in payload:
            collected.extend(_texts(item))
        return tuple(collected)
    return ()


def declares(card: dict[str, Any], term: str) -> bool:
    """أيرِد المصطلحُ في البطاقة كلمةً قائمةً بنفسها، لا جزءًا من كلمةٍ أخرى؟"""

    boundary = r"[\w\u0621-\u064a]"
    pattern = re.compile(
        f"(?<!{boundary})" + re.escape(comparison_key(term)) + f"(?!{boundary})"
    )
    return any(pattern.search(comparison_key(text)) for text in _texts(card))


def declared_members(card: dict[str, Any], vocabulary: type[Enum]) -> tuple[Enum, ...]:
    """أعضاءُ المفردة المغلقة التي تُصرّح بها البطاقة نصًّا، وقد تكون فارغة."""

    return tuple(member for member in vocabulary if declares(card, str(member.value)))


@dataclass(frozen=True, slots=True)
class LinkAttempt:
    """محاولةُ حلقةٍ واحدة على هذه البطاقة: أقامت، أم وقفت ولأيّ إعلانٍ غائب."""

    label: str
    module_relative_path: str
    stood_up: bool
    missing_declaration: str


def lexical_citation_genus(card: dict[str, Any]) -> UnconstructibilityGenus:
    """جنسُ امتناع التواتر على استشهاد هذه البطاقة، مُشتَقًّا من طريقها."""

    path = card_lexical_wad_path(card)
    if path is None:
        return UnconstructibilityGenus.GENUS_NOT_SETTLED
    return path.genus


def link_four(card: dict[str, Any]) -> LinkAttempt:
    """٤ الوضع بالنقل: درجتُه تُشتَقّ من طريق النقل المعجميّ لا تُقرأ مكتوبةً."""

    structure = card_lexical_citation_structure(card)
    standing = card_transmission_standing(card)
    return LinkAttempt(
        label="٤",
        module_relative_path="wad_naql.py",
        stood_up=standing is not None,
        missing_declaration=(
            ""
            if standing is not None
            else "درجةُ النقل من `TransmissionStanding` (متواتر/آحاد/فرض) لا "
            "تُشتَقّ من هذه البطاقة: بنيةُ استشهادها المعجميّ "
            f"`{structure.value}`، وجنسُ امتناعها "
            f"`{lexical_citation_genus(card).value}`؛ فـ`WadRecord` غيرُ "
            "قابلٍ للتسجيل منها، و`DistributionalCorroboration` لا تقوم إلا "
            "على منقولٍ سابق."
        ),
    )


def link_five(card: dict[str, Any]) -> LinkAttempt:
    """٥ تحقيقُ المناط: البطاقةُ مصوغةٌ لهذه الحلقة بعينها."""

    read_manat_qarain(card)
    return LinkAttempt(
        label="٥",
        module_relative_path="manat_verification.py",
        stood_up=True,
        missing_declaration="",
    )


def link_six(card: dict[str, Any]) -> LinkAttempt:
    """٦ ما يخلّ بالفهم: البطاقةُ تُصنّف كلَّ قراءةٍ منافسةٍ بسببٍ من المفردة."""

    declared = tuple(
        canonical_defect_classification(reading["سبب_الإخلال_بالفهم"])
        for reading in card["القراءات_المنافسة"]
        if "سبب_الإخلال_بالفهم" in reading
    )
    return LinkAttempt(
        label="٦",
        module_relative_path="comprehension_defect.py",
        stood_up=len(declared) == len(card["القراءات_المنافسة"]),
        missing_declaration=(
            ""
            if len(declared) == len(card["القراءات_المنافسة"])
            else "سبب_الإخلال_بالفهم لكلّ قراءةٍ منافسة"
        ),
    )


def link_seven(card: dict[str, Any]) -> LinkAttempt:
    """٧ البيانُ بالقول مقدَّمًا على البيان بالفعل: الترتيبُ مُشتَقٌّ من القرائن."""

    derived = derive_bayan_models(read_manat_qarain(card))
    models = {model.model_id: model for model in derived}
    qawl = models.get(QAWL_MODEL_ID)
    fil = models.get(FIL_MODEL_ID)
    ordered = (
        qawl is not None
        and fil is not None
        and qawl.weaker_model_ids == ()
        and fil.weaker_model_ids == (QAWL_MODEL_ID,)
    )
    return LinkAttempt(
        label="٧",
        module_relative_path="manat_verification.py",
        stood_up=ordered,
        missing_declaration="" if ordered else "قرينتا قولٍ وفعلٍ معًا في البطاقة",
    )


def link_eight(card: dict[str, Any]) -> LinkAttempt:
    """٨ المنطوقُ والمفهوم: يلزمه قناةُ دلالةٍ وجنسُ مفهومٍ مُعلَنان."""

    declared = declared_members(card, DalalaChannel) and declared_members(
        card, MafhumKind
    )
    return LinkAttempt(
        label="٨",
        module_relative_path="mantuq_mafhum_ifada.py",
        stood_up=bool(declared),
        missing_declaration=(
            ""
            if declared
            else "قناةُ الدلالة (`DalalaChannel`) وجنسُ المفهوم (`MafhumKind`): "
            "البطاقةُ تُعلن مدلولَ اللفظ ولا تُعلن دلالةً ثانيةً يُحمَل عليها."
        ),
    )


def link_nine(card: dict[str, Any]) -> LinkAttempt:
    """٩ القياسُ بعلّةٍ منطبقة: يلزمه أصلٌ مُجمَّدٌ مُسمًّى وعلّةٌ مُعلَنة."""

    declared = any(
        declares(card, reference) for reference in frozen_asl_references()
    ) and bool(declared_members(card, IllaApplication))
    return LinkAttempt(
        label="٩",
        module_relative_path="qiyas_rabt_registration.py",
        stood_up=declared,
        missing_declaration=(
            ""
            if declared
            else "أصلٌ من `frozen_asl_references()` وانطباقُ علّةٍ من "
            "`IllaApplication`: البطاقةُ موضعٌ واحد بلا فرعٍ مقيسٍ عليه."
        ),
    )


def link_ten(card: dict[str, Any]) -> LinkAttempt:
    """١٠ العمومُ والخصوص: يلزمه دليلان بنطاقَيهما، أو جنسُ قاعدةٍ للتفريع."""

    declared = bool(declared_members(card, DalilScope)) or bool(
        declared_members(card, RuleGenus)
    )
    return LinkAttempt(
        label="١٠",
        module_relative_path="umum_khusus.py",
        stood_up=declared,
        missing_declaration=(
            ""
            if declared
            else "نطاقُ الدليل (`DalilScope`) أو جنسُ القاعدة (`RuleGenus`): "
            "لا عامَّ في البطاقة ولا مخصِّصَ له ولا موضعَ تعارضٍ مُسمًّى."
        ),
    )


def link_eleven(card: dict[str, Any]) -> LinkAttempt:
    """١١ الروايةُ والدراية: يلزمها قناةُ نقلٍ مُعرَّفةٌ ببصمتها، أو فرعُ درايةٍ."""

    declared = bool(declared_members(card, RiwayaStanding)) or bool(
        declared_members(card, DirayaBranch)
    )
    return LinkAttempt(
        label="١١",
        module_relative_path="riwaya_diraya_registration.py",
        stood_up=declared,
        missing_declaration=(
            ""
            if declared
            else "حالُ الرواية (`RiwayaStanding`) أو فرعُ الدراية "
            "(`DirayaBranch`): البطاقةُ نصٌّ مقروء لا تشغيلُ أداةٍ بهويةٍ وبصمة."
        ),
    )


def link_twelve(card: dict[str, Any]) -> LinkAttempt:
    """١٢ درجةُ اليقين: تُشتَقّ من أساسٍ واستقلالٍ وتكرارٍ مُعلَنة."""

    declared = (
        bool(declared_members(card, KnowledgeBasis))
        and bool(declared_members(card, SourceIndependence))
        and bool(declared_members(card, RepetitionPattern))
    )
    return LinkAttempt(
        label="١٢",
        module_relative_path="transmission_standing.py",
        stood_up=declared,
        missing_declaration=(
            ""
            if declared
            else "أساسُ المعرفة واستقلالُ المصادر ونمطُ التكرار، وهي عينُ ما "
            "تفتقده الحلقةُ ٤: البطاقةُ تُسمّي مصادرَها ولا تصف طريقَ ورودها."
        ),
    )


def link_thirteen(card: dict[str, Any]) -> LinkAttempt:
    """١٣ المعلومةُ والمفهوم: يلزمها هدفٌ دلاليٌّ وسندٌ ينتهي إلى حسٍّ مباشر."""

    declared = bool(declared_members(card, SemanticTarget)) and bool(
        declared_members(card, SanadOrigin)
    )
    return LinkAttempt(
        label="١٣",
        module_relative_path="maluma_mafhum.py",
        stood_up=declared,
        missing_declaration=(
            ""
            if declared
            else "هدفُ الفهم (`SemanticTarget`) وأصلُ السند (`SanadOrigin`): "
            "لا سلسلةَ تسليمٍ في البطاقة تنتهي إلى حسٍّ مباشر."
        ),
    )


def traverse(card: dict[str, Any]) -> tuple[LinkAttempt, ...]:
    """سَوقُ البطاقة على الحلقات ٤–١٣ بترتيبها، بلا تقديمٍ ولا تأخير."""

    return (
        link_four(card),
        link_five(card),
        link_six(card),
        link_seven(card),
        link_eight(card),
        link_nine(card),
        link_ten(card),
        link_eleven(card),
        link_twelve(card),
        link_thirteen(card),
    )


def first_stop(attempts: tuple[LinkAttempt, ...]) -> LinkAttempt | None:
    """أوّلُ حلقةٍ وقفت؛ وما بعدها لا يُقرأ بالغًا وإن قام بذاته."""

    for attempt in attempts:
        if not attempt.stood_up:
            return attempt
    return None
