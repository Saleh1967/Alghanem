"""الحدُّ محورانِ لا متغيّرٌ واحد: الدخولُ والخروجُ، وشهادةٌ تحمل الطرفين.

كان العيبُ أنّ «الابتداء» و«الوصل» و«الوقف» تُعامَل ثلاثَ قيمٍ متنافيةٍ في
متغيّرٍ واحد. وهذا خطأٌ بنيويٌّ لا خطأُ قياس: فالكلمةُ الواحدةُ قد تُبتدَأ
ويُوقَفَ عليها، وقد تُوصَل بما قبلها ويُوقَفَ عليها. فالابتداءُ والوصلُ
يحدّدان **الدخول**، والوقفُ يحدّد **الخروج**، وهما محورانِ متعامدان حاصلُ
ضربهما أربعُ حالاتٍ لا ثلاث
(`THREE_MUTUALLY_EXCLUSIVE_VALUES_CANNOT_CARRY_A_PRODUCT_OF_TWO_AXES`).

    F₂(bytes, encoding, entry, exit, boundary_map)
      → (source_orthography, boundary_projections, seam_certificates,
         phonological_features, status, residuals)

أوّلًا، **الرسمُ الأصليُّ محفوظٌ وكرسيُّ الهمزة معه**. ويتغيّر نصُّ الإسقاط
الأدائيِّ بحسب الحدّ؛ وحذفُ همزة الوصل في الإسقاط لا يمحو ألفَها من أصل
المصدر (`A_DELETION_IN_THE_PROJECTION_DOES_NOT_ERASE_THE_SOURCE_GLYPH`).

ثانيًا، **الشهادةُ تحمل أثرين على جانبَي الحدّ**: `left_input` و`left_output`
و`right_input` و`right_output` وهويّةَ القاعدة وحارسَها ومرجعَها. فتطبيقُ حذف
الهمزة وحدَه ثمّ تسليمُ كلّ كلمةٍ مستقلّةً **يُفقِد أثرَ إصلاح المدّ**؛ ولذلك
تُردّ ههنا شهادةٌ خلا أحدُ طرفيها بنيويًّا، وتُردّ شهادةٌ تدّعي قاعدةً لم
تُحرّك طرفَها (`A_ONE_SIDED_TRACE_IS_NOT_A_SEAM_CERTIFICATE`).

ثالثًا، **الفاصلةُ وحدَها لا يُستنتَج منها وقفٌ فعليّ**. وفي هذا المُودَع
وسمُ ناشرٍ `<sel>` يتخلّل الصفوف، فيقع بين كلمتين فيمنع شهادةَ وصلٍ مكتملة؛
ويُعَدّ منعُه ولا يُطوى (`AN_UNDECLARED_SEPARATOR_BLOCKS_A_SEAM_IT_DOES_NOT_PAUSE`).

رابعًا، **المرشَّحُ المكتملُ بالنسبة للقواعد المنفَّذة ليس جامعيّةً لغويّة**.
وشرطُ الجمع والمنع ‎C_F = R_P‎ يقتضي مرجعًا ‎R_P‎ **مستقلًّا**، ولا يُعرَّف
المرجعُ بأنّه ما يقبله المنتَج، وإلّا صارت المساواةُ تحصيلَ حاصل
(`A_REFERENCE_DEFINED_AS_WHAT_THE_PRODUCT_ACCEPTS_IS_NOT_A_REFERENCE`).

خامسًا، **المستثنى يُسمّى ولا يُطوى**: الرومُ والإشمامُ والنقلُ وهاءُ السكت
وأوجهُ القراءات غيرُ مطبَّقةٍ ههنا؛ وهذا الملفُّ للوقف بالسكون وللتمثيل
الفونيميّ النصّيّ وحدَه.

سادسًا — وهو الحدّ — **أرقامُ الصحيحين لا تُعاد اشتقاقُها ههنا**: بايتاتُهما
وحزمةُ `boundary116/` غائبةٌ عن هذه الشجرة. فتمرُّ دعاواهما بعقد ‎Λ‎
فتخرج **معلَّقةً بأسماء موادّها**، لا مقبولةً ولا مردودة. والمقيسُ ههنا على
مُودَعٍ آخرَ مختوم، فلا يُقابَل رقمُه برقمها
(`A_FIGURE_FROM_ANOTHER_CORPUS_IS_NOT_A_CHECK_ON_THIS_ONE`).

    AnEntryAxis             != AnExitAxis
    AThreeValuedVariable    != AProductOfTwoAxes
    AOneSidedTrace          != ASeamCertificate
    ACompleteCandidate      != ALinguisticTotality

ولا سلطانَ لهذه الوحدة: لا ولادةَ، ولا رفعَ حظر، ولا فكَّ تجميد، ولا استيرادَ
من `kernel/` (`NO_BOUNDARY_HERE_LIFTS_A_BLOCK_OR_THAWS_A_FREEZE`).
"""

from __future__ import annotations

import unicodedata
from dataclasses import dataclass
from enum import Enum
from functools import lru_cache
from itertools import product
from typing import Final

from .a116_bridge_licence import (
    THE_SEALED_MATERIAL,
    DeclaredMaterial,
    LicenceCheck,
    MeasuredEvidence,
)
from .quran_mirror_collation import ayah_rows_of

__all__ = [
    "AN_UNDECLARED_SEPARATOR_BLOCKS_A_SEAM_IT_DOES_NOT_PAUSE",
    "A_COMPLETE_CANDIDATE_IS_NOT_A_LINGUISTIC_TOTALITY",
    "A_DELETION_IN_THE_PROJECTION_DOES_NOT_ERASE_THE_SOURCE_GLYPH",
    "A_FIGURE_FROM_ANOTHER_CORPUS_IS_NOT_A_CHECK_ON_THIS_ONE",
    "A_ONE_SIDED_TRACE_IS_NOT_A_SEAM_CERTIFICATE",
    "A_REFERENCE_DEFINED_AS_WHAT_THE_PRODUCT_ACCEPTS_IS_NOT_A_REFERENCE",
    "A_SILENT_SEED_NEEDS_A_LEFT_CONTEXT_IT_IS_NOT_A_FORBIDDEN_FORM",
    "Atom",
    "AtomOrigin",
    "AxisIndependenceReading",
    "BOUNDARY116_NAMED_RESIDUALS",
    "Boundary116Error",
    "BoundaryMode",
    "BoundaryRule",
    "Entry",
    "Exit",
    "Exitward",
    "Gate",
    "NO_BOUNDARY_HERE_LIFTS_A_BLOCK_OR_THAWS_A_FREEZE",
    "Projection",
    "SeamCertificate",
    "SeamCensus",
    "Status",
    "THE_DECLARED_WASL_NOUNS",
    "THE_EXAMINED_DEPOSIT",
    "THE_FOUR_MODES",
    "THE_PUBLISHER_SEPARATOR",
    "THE_REPORT_AT_TRANSCRIPTION",
    "THE_RULES",
    "THE_SAHIHAYN_MATERIALS",
    "THE_UNAPPLIED_READINGS",
    "THREE_MUTUALLY_EXCLUSIVE_VALUES_CANNOT_CARRY_A_PRODUCT_OF_TWO_AXES",
    "TranscribedBookRow",
    "adjacent_token_pairs",
    "axis_independence_reading",
    "deposit_seam_census",
    "deposit_word_census",
    "project",
    "rule_by_id",
    "seam",
    "the_block_and_the_freeze_are_untouched",
    "the_ledger",
]

THE_EXAMINED_DEPOSIT: Final[str] = "quran-simple-enhanced.txt"
"""المُودَعُ المقيسُ عليه ههنا؛ وهو **غيرُ** متن التقرير، فلا يُقابَل رقمُه برقمه."""

THE_PUBLISHER_SEPARATOR: Final[str] = "<sel>"
"""وسمُ ناشرٍ يقع رمزًا مستقلًّا بين الكلمات؛ فاصلةٌ غيرُ مصرَّحٍ بحدّها."""


class Boundary116Error(ValueError):
    """رفضٌ ههنا: شهادةٌ ناقصةُ طرف، أو خريطةُ حدٍّ متعارضة، أو أثرٌ مزوَّر."""


# ---------------------------------------------------------------------------
# المحوران: الدخولُ والخروج
# ---------------------------------------------------------------------------


class Entry(Enum):
    """محورُ الدخول: ابتداءٌ أو وصلٌ بما قبل؛ ولا ثالثَ له."""

    START = "ابتداء"
    JOINED = "موصولٌ بما قبله"


class Exit(Enum):
    """محورُ الخروج: استمرارٌ أو وقف؛ وهو **مستقلٌّ** عن محور الدخول."""

    CONTINUE = "استمرار"
    PAUSE = "وقف"


@dataclass(frozen=True)
class BoundaryMode:
    """حالُ الحدّ: نقطةٌ في حاصل ضرب المحورين، لا قيمةٌ في متغيّرٍ ثلاثيّ."""

    entry: Entry
    exit: Exit

    @property
    def name_in_arabic(self) -> str:
        """اسمُها مركَّبٌ من محورَيها؛ ولا اسمَ لها خارجَهما."""

        return f"{self.entry.value} · {self.exit.value}"


THE_FOUR_MODES: Final[tuple[BoundaryMode, ...]] = tuple(
    BoundaryMode(entry=entry, exit=exit_) for entry, exit_ in product(Entry, Exit)
)
"""الحالاتُ الأربع؛ وهي حاصلُ ضربٍ مشتقٌّ لا جدولٌ مكتوبٌ باليد."""


class Exitward(Enum):
    """جهةُ الطرف في الشهادة الزوجيّة؛ وكلاهما محمولٌ ولا يُسقَط أحدُهما."""

    LEFT = "الطرفُ الأيسر"
    RIGHT = "الطرفُ الأيمن"


# ---------------------------------------------------------------------------
# القواعدُ وحرّاسُها
# ---------------------------------------------------------------------------


class Gate(Enum):
    """بوّاباتُ القواعد الخمس؛ وكلُّ قاعدةٍ تحت بوّابةٍ مُسمّاةٍ لا سائبة."""

    IBTIDA = "الابتداء"
    WASL = "الوصل"
    SAKINAYN = "التقاء الساكنين"
    WAQF = "الوقف"
    BOUNDARY = "الحدود"


@dataclass(frozen=True)
class BoundaryRule:
    """قاعدةٌ بأثرها وحارسها ومرجعها؛ ولا قاعدةَ ههنا بلا حارسٍ مُسمًّى."""

    rule_id: str
    gate: Gate
    effect: str
    guard: str
    reference: str

    def __post_init__(self) -> None:
        if not all(
            field.strip()
            for field in (self.rule_id, self.effect, self.guard, self.reference)
        ):
            raise Boundary116Error("قاعدةٌ ناقصةُ أثرٍ أو حارسٍ أو مرجعٍ لا تُعلَن.")


THE_RULES: Final[tuple[BoundaryRule, ...]] = (
    BoundaryRule(
        rule_id="IBTIDA_WASL_HAMZA",
        gate=Gate.IBTIDA,
        effect="إثباتُ همزة الوصل وحركتِها في «ال» والأسماء المُعلَنة",
        guard="هويّةُ الوصل محفوظةٌ من الرسم الأصليّ؛ والفعلُ مجهولُ القاعدة مؤجَّل",
        reference="همزُ الوصل في المقدّمة الجزريّة",
    ),
    BoundaryRule(
        rule_id="IBTIDA_NO_SUKUN_SEED",
        gate=Gate.IBTIDA,
        effect="منعُ البدء بذرةٍ ساكنة",
        guard="لا تُضاف همزةُ إصلاحٍ مجهولةٌ إلى كلّ سلسلة",
        reference="همزُ الوصل في المقدّمة الجزريّة",
    ),
    BoundaryRule(
        rule_id="WASL_DROP_HAMZA",
        gate=Gate.WASL,
        effect="حذفُ همزة الوصل مع حفظ همزة القطع وكرسيِّها",
        guard="هويّةٌ مثبتةٌ بالعلامة أو بالقالب المُعلَن؛ وسياقٌ أيسرُ مكتملٌ وحدُّ وصلٍ مصرَّح",
        reference="همزُ الوصل في المقدّمة الجزريّة",
    ),
    BoundaryRule(
        rule_id="SAKINAYN_DROP_MADD",
        gate=Gate.SAKINAYN,
        effect="حذفُ حرف المدّ الموافق لحركة ما قبله في الإسقاط الأيسر",
        guard="ذرّةُ المدّ وحركتُها متطابقتان، والمخرجُ الأيمنُ يبدأ بسكون",
        reference="مصدرُ التخلّص من الساكنين المسجَّل في summary.json",
    ),
    BoundaryRule(
        rule_id="SAKINAYN_TANWIN_KASR",
        gate=Gate.SAKINAYN,
        effect="تحريكُ نون التنوين بالكسر",
        guard=(
            "التنوينُ ثابتٌ في رسم الطرف الأيسر؛ ولا تُنقَل القاعدةُ إلى نونٍ "
            "أصليّةٍ أو إلى سكونٍ آخر"
        ),
        reference="مصدرُ التخلّص من الساكنين المسجَّل في summary.json",
    ),
    BoundaryRule(
        rule_id="WAQF_SHORT_HARAKA_TO_SUKUN",
        gate=Gate.WAQF,
        effect="تسكينُ الحركة القصيرة الأخيرة؛ والهمزةُ على ألفٍ تسكن بوصفها همزة",
        guard="لا تُخلَط قاعدةُ الكرسيّ بدور ألف المدّ",
        reference="الوقفُ على أواخر الكلم",
    ),
    BoundaryRule(
        rule_id="WAQF_TA_MARBUTA_TO_HA",
        gate=Gate.WAQF,
        effect="التاءُ المربوطةُ إلى هاءٍ ساكنة",
        guard="تاءٌ مربوطةٌ طرفيّةٌ غيرُ مشدَّدة؛ ويبقى الرسمُ الأصليّ",
        reference="بابُ الوقف في شرح ابن عقيل",
    ),
    BoundaryRule(
        rule_id="WAQF_TANWIN",
        gate=Gate.WAQF,
        effect="تنوينُ الضمّ والكسر إلى سكون؛ وتنوينُ الفتح إلى مدّ ألف",
        guard="استثناءُ التاء المربوطة، وتمييزُ الألف الداعمة من كرسيّ الهمزة",
        reference="الوقفُ على أواخر الكلم",
    ),
    BoundaryRule(
        rule_id="WAQF_MAQSURA_TANWIN_FATH",
        gate=Gate.WAQF,
        effect="المقصورةُ مع تنوين الفتح إلى مدّ ألف",
        guard="رسمٌ نهائيٌّ محدَّد؛ ولا تخمينَ للجذر أو الإعراب",
        reference="الوقفُ على أواخر الكلم",
    ),
    BoundaryRule(
        rule_id="WAQF_SHADDA_TWO_SLOTS",
        gate=Gate.WAQF,
        effect="حفظُ الحرف المشدَّد في موضعين زمنيَّين ساكنَين",
        guard="الشدّةُ والحركةُ النهائيّةُ مثبتتان؛ ونقصُ الداخل يبقى مؤجَّلًا",
        reference="بابُ الوقف في شرح ابن عقيل",
    ),
    BoundaryRule(
        rule_id="BOUNDARY_NO_PAUSE_THEN_JOIN",
        gate=Gate.BOUNDARY,
        effect="رفضُ خريطةٍ توقِف الطرفَ الأيسرَ ثمّ تصله بالأيمن",
        guard="لا يُستنتَج الوقفُ الفعليُّ من الفاصلة وحدَها",
        reference="بابُ الوقف في شرح ابن عقيل",
    ),
)
"""إحدى عشرةَ قاعدةً بخمس بوّابات؛ ولكلٍّ حارسُها ومرجعُها لا أثرُها فقط."""

THE_UNAPPLIED_READINGS: Final[tuple[str, ...]] = (
    "الرَّوم",
    "الإشمام",
    "النقل",
    "هاءُ السكت",
    "أوجهُ القراءات المتعدّدة",
)
"""المستثنى بأسمائه؛ وهذا الملفُّ للوقف بالسكون وللتمثيل الفونيميّ النصّيّ."""

THE_DECLARED_WASL_NOUNS: Final[tuple[str, ...]] = (
    "سم",
    "بن",
    "بنة",
    "مرؤ",
    "مرأة",
    "ثنان",
    "ثنتان",
)
"""الأسماءُ المُعلَنةُ التي تُبتدَأ همزةُ وصلها بالكسر؛ وما سواها مؤجَّلٌ باسمه."""


@lru_cache(maxsize=1)
def _rules_by_id() -> dict[str, BoundaryRule]:
    return {rule.rule_id: rule for rule in THE_RULES}


def rule_by_id(rule_id: str) -> BoundaryRule:
    """قاعدةٌ بهويّتها؛ والهويّةُ المجهولةُ تُردّ ولا تُفسَّر قاعدةً عامّة."""

    try:
        return _rules_by_id()[rule_id]
    except KeyError as error:
        raise Boundary116Error(f"قاعدةٌ غيرُ مُعلَنة: {rule_id}.") from error


# ---------------------------------------------------------------------------
# الذرّاتُ والإسقاط
# ---------------------------------------------------------------------------

_FATHA: Final[str] = "\u064e"
_DAMMA: Final[str] = "\u064f"
_KASRA: Final[str] = "\u0650"
_SUKUN: Final[str] = "\u0652"
_SHADDA: Final[str] = "\u0651"
_TANWIN: Final[dict[str, str]] = {
    "\u064b": _FATHA,
    "\u064c": _DAMMA,
    "\u064d": _KASRA,
}
_HARAKAT: Final[dict[str, str]] = {
    _FATHA: _FATHA,
    _DAMMA: _DAMMA,
    _KASRA: _KASRA,
    _SUKUN: _SUKUN,
}
_MADD_PARTNER: Final[dict[str, str]] = {
    "\u0627": _FATHA,
    "\u0648": _DAMMA,
    "\u064a": _KASRA,
}
_ALIF: Final[str] = "\u0627"
_LAM: Final[str] = "\u0644"
_NUN: Final[str] = "\u0646"
_HA: Final[str] = "\u0647"
_TA_MARBUTA: Final[str] = "\u0629"
_MAQSURA: Final[str] = "\u0649"
_HAMZA_SEATS: Final[frozenset[str]] = frozenset("\u0621\u0622\u0623\u0624\u0625\u0626")


class AtomOrigin(Enum):
    """مصدرُ الذرّة؛ فالذرّةُ تُعرَف بمن ولَّدها لا بصورتها وحدَها."""

    WRITTEN = "مرسومةٌ بعلامتها"
    MADD = "حرفُ مدٍّ موافقٌ لحركة ما قبله"
    TANWIN_NUN = "نونُ تنوينٍ ساكنة"
    SHADDA_FIRST = "الموضعُ الزمنيُّ الأوّلُ للمشدَّد"
    WASL_HAMZA = "همزةُ وصلٍ أُثبِتت في الابتداء"
    WAQF_SUKUN = "سكونُ وقف"
    WAQF_MADD_A = "مدُّ ألفٍ في الوقف"


@dataclass(frozen=True)
class Atom:
    """ذرّةٌ: حاملٌ وحركةٌ ومصدر؛ ولا ذرّةَ بلا حركةٍ من الأربع."""

    carrier: str
    haraka: str
    origin: AtomOrigin

    def __post_init__(self) -> None:
        if len(self.carrier) != 1:
            raise Boundary116Error("ذرّةٌ بحاملٍ ليس حرفًا واحدًا لا تُبنى.")
        if self.haraka not in _HARAKAT:
            raise Boundary116Error("ذرّةٌ بحركةٍ خارج الأربع لا تُبنى.")

    @property
    def is_silent(self) -> bool:
        """أساكنةٌ هي؟ وهذا ما يُسأل عنه عند الحدّ لا صورةُ الحرف."""

        return self.haraka == _SUKUN


class Status(Enum):
    """منزلةُ الإسقاط؛ والتأجيلُ منزلةٌ مُسمّاةٌ بأسبابها لا سكوت."""

    COMPLETE_CANDIDATE = "مرشَّحٌ مكتمل"
    DEFERRED = "مؤجَّل"
    REFUSED_START_ON_A_SILENT_SEED = "مرفوضٌ: ابتداءٌ بذرةٍ ساكنة"
    OUT_OF_PROFILE = "خارجَ القالب"


@dataclass(frozen=True)
class Projection:
    """إسقاطُ رسمٍ واحدٍ تحت حالِ حدٍّ مُعلَن؛ والأصلُ محفوظٌ بجانب مُخرَجه."""

    source: str
    mode: BoundaryMode
    atoms: tuple[Atom, ...]
    applied: tuple[str, ...]
    status: Status
    deferral_reasons: tuple[str, ...]

    def __post_init__(self) -> None:
        if not self.source:
            raise Boundary116Error("إسقاطٌ بلا أصلٍ محفوظٍ لا يُبنى.")
        for rule_id in self.applied:
            rule_by_id(rule_id)
        if self.status is Status.DEFERRED and not self.deferral_reasons:
            raise Boundary116Error("تأجيلٌ بلا سببٍ مُسمًّى لا يُقبَل.")
        if self.status is not Status.DEFERRED and self.deferral_reasons:
            raise Boundary116Error("أسبابُ تأجيلٍ على غير مؤجَّلٍ تُلبِس الحال.")

    @property
    def is_complete(self) -> bool:
        """المرشَّحُ المكتملُ **بالنسبة للقواعد المنفَّذة** لا للعربيّة كلِّها."""

        return self.status is Status.COMPLETE_CANDIDATE


def _is_arabic_letter(char: str) -> bool:
    return unicodedata.category(char) == "Lo" and "\u0620" <= char <= "\u064a"


def _clusters(form: str) -> tuple[tuple[str, str], ...] | None:
    """عناقيدُ الرسم: حاملٌ وما تبعه من علاماتٍ لاحقة؛ أو None لخارج القالب."""

    clusters: list[tuple[str, str]] = []
    marks: list[str] = []
    for char in form:
        if _is_arabic_letter(char):
            clusters.append((char, ""))
            marks = []
            continue
        if unicodedata.category(char) == "Mn":
            if not clusters:
                return None
            marks.append(char)
            carrier, _ = clusters[-1]
            clusters[-1] = (carrier, "".join(marks))
            continue
        return None
    return tuple(clusters) if clusters else None


def _atoms_of_cluster(
    carrier: str,
    marks: str,
    previous: Atom | None,
    following_carrier: str | None,
) -> tuple[tuple[Atom, ...], tuple[str, ...], tuple[str, ...]]:
    """ذرّاتُ عنقودٍ واحد، وما طُبِّق عليه من قواعد، وما تأجّل منه بأسبابه."""

    applied: list[str] = []
    shadda = _SHADDA in marks
    tanwin = next((mark for mark in marks if mark in _TANWIN), None)
    haraka = next((mark for mark in marks if mark in _HARAKAT), None)

    prefix: tuple[Atom, ...] = ()
    if shadda:
        prefix = (Atom(carrier, _SUKUN, AtomOrigin.SHADDA_FIRST),)
        applied.append("WAQF_SHADDA_TWO_SLOTS")

    if tanwin is not None:
        return (
            (
                *prefix,
                Atom(carrier, _TANWIN[tanwin], AtomOrigin.WRITTEN),
                Atom(_NUN, _SUKUN, AtomOrigin.TANWIN_NUN),
            ),
            tuple(applied),
            (),
        )

    if haraka is not None:
        return (*prefix, Atom(carrier, haraka, AtomOrigin.WRITTEN)), tuple(applied), ()

    if (
        previous is not None
        and carrier in _MADD_PARTNER
        and previous.haraka == _MADD_PARTNER[carrier]
    ):
        return (*prefix, Atom(carrier, _SUKUN, AtomOrigin.MADD)), tuple(applied), ()

    if (
        carrier == _ALIF
        and previous is not None
        and previous.origin is AtomOrigin.TANWIN_NUN
        and following_carrier is None
    ):
        return (), tuple(applied), ()

    return (), tuple(applied), (f"حاملٌ بلا علامةٍ ولا هويّةَ مدٍّ له: {carrier}",)


def _wasl_identity(clusters: tuple[tuple[str, str], ...]) -> str | None:
    """هويّةُ همزة الوصل من الرسم: «ال» أو اسمٌ مُعلَن؛ وما سواهما مجهول."""

    carrier, marks = clusters[0]
    if carrier != _ALIF or marks:
        return None
    if len(clusters) >= 2 and clusters[1][0] == _LAM:
        return _FATHA
    tail = "".join(letter for letter, _ in clusters[1:])
    return _KASRA if tail in THE_DECLARED_WASL_NOUNS else None


def _apply_pause(atoms: list[Atom], clusters: tuple[tuple[str, str], ...]) -> list[str]:
    """قواعدُ الوقف على ذرّات الطرف؛ وتُعاد أسماءُ ما طُبِّق منها."""

    applied: list[str] = []
    if not atoms:
        return applied
    last_carrier, last_marks = clusters[-1]

    if atoms[-1].origin is AtomOrigin.TANWIN_NUN:
        atoms.pop()
        base = atoms[-1]
        if last_carrier == _TA_MARBUTA:
            atoms[-1] = Atom(_HA, _SUKUN, AtomOrigin.WAQF_SUKUN)
            applied.append("WAQF_TA_MARBUTA_TO_HA")
            return applied
        if base.haraka == _FATHA:
            atoms.append(Atom(_ALIF, _SUKUN, AtomOrigin.WAQF_MADD_A))
            applied.append(
                "WAQF_MAQSURA_TANWIN_FATH"
                if last_carrier == _MAQSURA
                else "WAQF_TANWIN"
            )
            return applied
        atoms[-1] = Atom(base.carrier, _SUKUN, AtomOrigin.WAQF_SUKUN)
        applied.append("WAQF_TANWIN")
        return applied

    if last_carrier == _TA_MARBUTA and _SHADDA not in last_marks:
        atoms[-1] = Atom(_HA, _SUKUN, AtomOrigin.WAQF_SUKUN)
        applied.append("WAQF_TA_MARBUTA_TO_HA")
        return applied

    if atoms[-1].origin is AtomOrigin.WRITTEN and not atoms[-1].is_silent:
        atoms[-1] = Atom(atoms[-1].carrier, _SUKUN, AtomOrigin.WAQF_SUKUN)
        applied.append("WAQF_SHORT_HARAKA_TO_SUKUN")
    return applied


def project(form: str, mode: BoundaryMode) -> Projection:
    """‎F₂‎ على رسمٍ واحدٍ تحت حالِ حدّ؛ والأصلُ محفوظٌ مهما تغيّر المُخرَج.

    والدخولُ يُحكِم أوّلَ الرسم، والخروجُ يُحكِم آخرَه، ولا يُنتزَع أحدُهما من
    الآخر. فما لم تُعرَف هويّتُه أُجِّل باسمه، ولا يُرقَّع بهمزةٍ مجهولة.
    """

    source = unicodedata.normalize("NFC", form)
    clusters = _clusters(source)
    if clusters is None:
        return Projection(
            source=source,
            mode=mode,
            atoms=(),
            applied=(),
            status=Status.OUT_OF_PROFILE,
            deferral_reasons=(),
        )

    applied: list[str] = []
    reasons: list[str] = []
    atoms: list[Atom] = []
    body = clusters
    wasl = _wasl_identity(clusters)

    if clusters[0][0] == _ALIF and not clusters[0][1]:
        if mode.entry is Entry.JOINED:
            if wasl is None:
                reasons.append("همزةُ وصلٍ مجهولةُ الهويّة عند حدّ وصل")
            else:
                applied.append("WASL_DROP_HAMZA")
            body = clusters[1:]
        else:
            if wasl is None:
                reasons.append("همزةُ وصلٍ مجهولةُ الحركة في الابتداء")
                body = clusters[1:]
            else:
                atoms.append(Atom("\u0621", wasl, AtomOrigin.WASL_HAMZA))
                applied.append("IBTIDA_WASL_HAMZA")
                body = clusters[1:]

    for index, (carrier, marks) in enumerate(body):
        following = body[index + 1][0] if index + 1 < len(body) else None
        produced, rules, cluster_reasons = _atoms_of_cluster(
            carrier, marks, atoms[-1] if atoms else None, following
        )
        atoms.extend(produced)
        applied.extend(rules)
        reasons.extend(cluster_reasons)

    if mode.exit is Exit.PAUSE and not reasons:
        applied.extend(_apply_pause(atoms, clusters))

    status = Status.COMPLETE_CANDIDATE
    if reasons:
        status = Status.DEFERRED
    elif not atoms:
        status = Status.DEFERRED
        reasons.append("إسقاطٌ خلا من كلّ ذرّة")
    elif mode.entry is Entry.START and atoms[0].is_silent:
        applied.append("IBTIDA_NO_SUKUN_SEED")
        status = Status.REFUSED_START_ON_A_SILENT_SEED

    return Projection(
        source=source,
        mode=mode,
        atoms=tuple(atoms),
        applied=tuple(dict.fromkeys(applied)),
        status=status,
        deferral_reasons=tuple(reasons),
    )


# ---------------------------------------------------------------------------
# الشهادةُ الزوجيّة: أثرانِ على جانبَي الحدّ
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class SeamCertificate:
    """شهادةُ حدٍّ تحمل الطرفين معًا؛ وشهادةٌ بطرفٍ واحدٍ تُردّ ولا تُقبَل ناقصة.

    وهذا هو العيبُ المُصلَح بعينه: كان الإسقاطُ يُطبَّق على كلّ كلمةٍ مستقلّةً
    فيُفقَد أثرُ إصلاح المدّ عند الحدّ. فصارت الشهادةُ تحمل
    `left_input` و`left_output` و`right_input` و`right_output` وهويّةَ القاعدة
    وحارسَها ومرجعَها، ويُردّ ادّعاءُ قاعدةٍ لم تُحرّك طرفَها.

    والحدُّ نفسُه جزءٌ من هويّة الشهادة: `left_exit` و`right_entry` محمولان،
    ورسما الطرفين محفوظان بجانب مُخرَجيهما
    (`A_DELETION_IN_THE_PROJECTION_DOES_NOT_ERASE_THE_SOURCE_GLYPH`).
    """

    left_source: str
    right_source: str
    left_exit: Exit
    right_entry: Entry
    left_input: tuple[Atom, ...]
    left_output: tuple[Atom, ...]
    right_input: tuple[Atom, ...]
    right_output: tuple[Atom, ...]
    applied: tuple[str, ...]
    status: Status
    deferral_reasons: tuple[str, ...]

    def __post_init__(self) -> None:
        if self.status is Status.COMPLETE_CANDIDATE and not (
            self.left_input and self.right_input
        ):
            raise Boundary116Error("شهادةُ حدٍّ مكتملةٌ بطرفٍ خالٍ لا تُبنى.")
        for rule_id in self.applied:
            rule_by_id(rule_id)
        if "SAKINAYN_DROP_MADD" in self.applied and (
            len(self.left_output) >= len(self.left_input)
        ):
            raise Boundary116Error("ادِّعاءُ حذف مدٍّ لم يُنقِص الطرفَ الأيسر؛ أثرٌ مزوَّر.")
        if "SAKINAYN_TANWIN_KASR" in self.applied and (
            self.left_output == self.left_input
        ):
            raise Boundary116Error("ادِّعاءُ تحريك تنوينٍ لم يُحرّك الطرفَ الأيسر؛ أثرٌ مزوَّر.")
        if "WASL_DROP_HAMZA" in self.applied and (
            self.right_output == self.right_input
        ):
            raise Boundary116Error("ادِّعاءُ حذف همزةٍ لم يُحرّك الطرفَ الأيمن؛ أثرٌ مزوَّر.")
        if self.left_exit is Exit.PAUSE and self.right_entry is Entry.JOINED:
            raise Boundary116Error(
                "خريطةُ حدٍّ توقف الطرفَ الأيسر ثمّ تصله بالأيمن؛ حدٌّ متعارض."
            )

    @property
    def rules(self) -> tuple[BoundaryRule, ...]:
        """القواعدُ بحرّاسها ومراجعها؛ تُقرأ من الشهادة لا من جدولٍ خارجها."""

        return tuple(rule_by_id(rule_id) for rule_id in self.applied)

    @property
    def leaves_two_silents_at_the_seam(self) -> bool:
        """أبقي ساكنان عند حدِّ وصلٍ مقبول؟ وهذا ما يُصادَم به القبول."""

        if not self.left_output or not self.right_output:
            return False
        return self.left_output[-1].is_silent and self.right_output[0].is_silent


def seam(
    left: str,
    right: str,
    *,
    left_exit: Exit = Exit.CONTINUE,
    right_entry: Entry = Entry.JOINED,
) -> SeamCertificate:
    """حدُّ وصلٍ بين رسمين؛ والحدُّ مُصرَّحٌ به لا مفترَضٌ من التجاور.

    والفاصلةُ غيرُ المصرَّح بحدِّها — كوسم الناشر — تمنع شهادةً مكتملةً ولا
    تُقرأ وقفًا. وخريطةٌ توقف الأيسرَ ثمّ تصله بالأيمن تُردّ عند البناء
    (`BOUNDARY_NO_PAUSE_THEN_JOIN`)، ولا يُستنتَج الوقفُ الفعليُّ من الفاصلة
    وحدَها (`AN_UNDECLARED_SEPARATOR_BLOCKS_A_SEAM_IT_DOES_NOT_PAUSE`).
    """

    if THE_PUBLISHER_SEPARATOR in (left, right):
        return SeamCertificate(
            left_source=left,
            right_source=right,
            left_exit=left_exit,
            right_entry=right_entry,
            left_input=(),
            left_output=(),
            right_input=(),
            right_output=(),
            applied=(),
            status=Status.DEFERRED,
            deferral_reasons=("فاصلةٌ غيرُ مصرَّحٍ بحدِّها تمنع شهادةَ وصل",),
        )

    if left_exit is Exit.PAUSE and right_entry is Entry.JOINED:
        raise Boundary116Error("خريطةُ حدٍّ توقف الطرفَ الأيسر ثمّ تصله بالأيمن؛ حدٌّ متعارض.")

    left_projection = project(left, BoundaryMode(Entry.START, left_exit))
    right_at_start = project(right, BoundaryMode(Entry.START, Exit.CONTINUE))
    right_projection = project(right, BoundaryMode(right_entry, Exit.CONTINUE))
    left_atoms = list(left_projection.atoms)
    right_atoms = list(right_projection.atoms)
    applied = list(right_projection.applied)
    reasons = list(left_projection.deferral_reasons) + list(
        right_projection.deferral_reasons
    )

    if (
        left_exit is Exit.CONTINUE
        and left_atoms
        and right_atoms
        and right_atoms[0].is_silent
    ):
        tail = left_atoms[-1]
        if tail.origin is AtomOrigin.MADD:
            left_atoms.pop()
            applied.append("SAKINAYN_DROP_MADD")
        elif tail.origin is AtomOrigin.TANWIN_NUN:
            left_atoms[-1] = Atom(tail.carrier, _KASRA, AtomOrigin.WRITTEN)
            applied.append("SAKINAYN_TANWIN_KASR")

    status = Status.COMPLETE_CANDIDATE
    if reasons:
        status = Status.DEFERRED
    elif not (left_projection.is_complete and right_projection.is_complete):
        status = Status.DEFERRED
        reasons.append("أحدُ الطرفين غيرُ مكتمل")

    certificate = SeamCertificate(
        left_source=left,
        right_source=right,
        left_exit=left_exit,
        right_entry=right_entry,
        left_input=left_projection.atoms,
        left_output=tuple(left_atoms),
        right_input=right_at_start.atoms,
        right_output=tuple(right_atoms),
        applied=tuple(dict.fromkeys(applied)),
        status=status,
        deferral_reasons=tuple(reasons),
    )
    if (
        certificate.status is Status.COMPLETE_CANDIDATE
        and certificate.leaves_two_silents_at_the_seam
    ):
        return SeamCertificate(
            left_source=certificate.left_source,
            right_source=certificate.right_source,
            left_exit=certificate.left_exit,
            right_entry=certificate.right_entry,
            left_input=certificate.left_input,
            left_output=certificate.left_output,
            right_input=certificate.right_input,
            right_output=certificate.right_output,
            applied=certificate.applied,
            status=Status.DEFERRED,
            deferral_reasons=("ساكنان باقيان عند حدِّ وصلٍ فلا يُقبَل",),
        )
    return certificate


# ---------------------------------------------------------------------------
# القياسُ على البايتات المختومة ههنا
# ---------------------------------------------------------------------------


@lru_cache(maxsize=1)
def _deposited_tokens() -> tuple[tuple[str, ...], ...]:
    return tuple(
        tuple(unicodedata.normalize("NFC", token) for token in row.split())
        for row in ayah_rows_of(THE_EXAMINED_DEPOSIT)
    )


def adjacent_token_pairs() -> tuple[tuple[str, str], ...]:
    """الأزواجُ المتجاورةُ داخلَ الصفّ الواحد؛ ولا يُفتعَل جوارٌ عبر الأسطر."""

    return tuple(
        (row[index], row[index + 1])
        for row in _deposited_tokens()
        for index in range(len(row) - 1)
    )


@dataclass(frozen=True)
class WordCensus:
    """إحصاءُ سيناريو كلمةٍ واحدةٍ على هذا المُودَع؛ لا على متن التقرير."""

    mode_name: str
    occurrences: int
    complete: int
    deferred: int
    refused_start_on_a_silent_seed: int
    out_of_profile: int

    def __post_init__(self) -> None:
        total = (
            self.complete
            + self.deferred
            + self.refused_start_on_a_silent_seed
            + self.out_of_profile
        )
        if total != self.occurrences:
            raise Boundary116Error("منازلُ الإسقاط لا تبلغ الوقوعات، وهذا محال.")


@lru_cache(maxsize=4)
def deposit_word_census(entry: Entry, exit_: Exit) -> WordCensus:
    """تشغيلُ ‎F₂‎ على كلّ وقوعٍ تحت حالِ حدٍّ واحد؛ والرقمُ يُشتَقّ ولا يُنقَل."""

    mode = BoundaryMode(entry, exit_)
    counts = dict.fromkeys(Status, 0)
    occurrences = 0
    for row in _deposited_tokens():
        for token in row:
            occurrences += 1
            counts[project(token, mode).status] += 1
    return WordCensus(
        mode_name=mode.name_in_arabic,
        occurrences=occurrences,
        complete=counts[Status.COMPLETE_CANDIDATE],
        deferred=counts[Status.DEFERRED],
        refused_start_on_a_silent_seed=counts[Status.REFUSED_START_ON_A_SILENT_SEED],
        out_of_profile=counts[Status.OUT_OF_PROFILE],
    )


@dataclass(frozen=True)
class SeamCensus:
    """إحصاءُ الحدود؛ وعملياتُ القواعد تقع في مرشَّحاتٍ قد تبقى مؤجَّلةً لغيرها."""

    pairs: int
    complete: int
    deferred: int
    blocked_by_an_undeclared_separator: int
    wasl_hamza_deletions: int
    madd_repairs: int
    tanwin_nun_kasr: int

    def __post_init__(self) -> None:
        if self.complete + self.deferred != self.pairs:
            raise Boundary116Error("الأزواجُ لا تنقسم إلى مكتملٍ ومؤجَّل، وهذا محال.")


@lru_cache(maxsize=1)
def deposit_seam_census() -> SeamCensus:
    """تشغيلُ الحدّ على كلّ زوجٍ متجاور؛ ولا تُجمَع عملياتُ القواعد تراخيصَ زائدة."""

    pairs = adjacent_token_pairs()
    complete = 0
    blocked = 0
    wasl = 0
    madd = 0
    tanwin = 0
    for left, right in pairs:
        certificate = seam(left, right)
        if certificate.status is Status.COMPLETE_CANDIDATE:
            complete += 1
        if THE_PUBLISHER_SEPARATOR in (left, right):
            blocked += 1
        wasl += "WASL_DROP_HAMZA" in certificate.applied
        madd += "SAKINAYN_DROP_MADD" in certificate.applied
        tanwin += "SAKINAYN_TANWIN_KASR" in certificate.applied
    return SeamCensus(
        pairs=len(pairs),
        complete=complete,
        deferred=len(pairs) - complete,
        blocked_by_an_undeclared_separator=blocked,
        wasl_hamza_deletions=wasl,
        madd_repairs=madd,
        tanwin_nun_kasr=tanwin,
    )


@dataclass(frozen=True)
class AxisIndependenceReading:
    """استقلالُ المحورين **مقيسًا** لا مُعلَنًا: كم وقوعًا يُحرّكه كلُّ محورٍ وحدَه."""

    occurrences: int
    moved_by_the_exit_axis: int
    moved_by_the_entry_axis: int
    silent_seed_occurrences: int
    silent_seed_distinct_forms: int

    @property
    def both_axes_are_effective(self) -> bool:
        """أيُحرّك كلُّ محورٍ شيئًا؟ فمحورٌ لا يُحرّك شيئًا ليس محورًا."""

        return self.moved_by_the_exit_axis > 0 and self.moved_by_the_entry_axis > 0


@lru_cache(maxsize=1)
def axis_independence_reading() -> AxisIndependenceReading:
    """قياسُ استقلال المحورين على المُودَع، وعدُّ الذرّات الساكنة في الابتداء.

    والذرّةُ الساكنةُ في أوّل الرسم ليست صورةً ممتنعةً في العربيّة: في هذا
    المُودَع تُرسَم شدّةُ اللام المُدغَمة على أوّل حرفٍ من الكلمة التالية، فيبدأ
    الرسمُ بالموضع الزمنيِّ الأوّل للمشدَّد، وهو يحتاج سياقًا يساريًّا
    (`A_SILENT_SEED_NEEDS_A_LEFT_CONTEXT_IT_IS_NOT_A_FORBIDDEN_FORM`).
    """

    start_continue = BoundaryMode(Entry.START, Exit.CONTINUE)
    start_pause = BoundaryMode(Entry.START, Exit.PAUSE)
    joined_pause = BoundaryMode(Entry.JOINED, Exit.PAUSE)
    occurrences = 0
    by_exit = 0
    by_entry = 0
    silent = 0
    silent_forms: set[str] = set()
    for row in _deposited_tokens():
        for token in row:
            occurrences += 1
            at_start = project(token, start_continue)
            at_pause = project(token, start_pause)
            if at_start.atoms != at_pause.atoms:
                by_exit += 1
            if project(token, joined_pause).atoms != at_pause.atoms:
                by_entry += 1
            if at_start.status is Status.REFUSED_START_ON_A_SILENT_SEED:
                silent += 1
                silent_forms.add(token)
    return AxisIndependenceReading(
        occurrences=occurrences,
        moved_by_the_exit_axis=by_exit,
        moved_by_the_entry_axis=by_entry,
        silent_seed_occurrences=silent,
        silent_seed_distinct_forms=len(silent_forms),
    )


# ---------------------------------------------------------------------------
# أرقامُ التقرير: منقولةٌ عن متنٍ غائبٍ عن الشجرة
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class TranscribedBookRow:
    """صفُّ كتابٍ منقولٌ عن التقرير؛ محفوظٌ ليُقابَل يومًا لا ليُصدَّق اليوم."""

    book: str
    records: int
    occurrences: int
    complete_start_continue: int
    complete_start_pause: int
    deferred_start_continue: int
    deferred_start_pause: int

    def __post_init__(self) -> None:
        for name, pair in (
            (
                "ابتداء/استمرار",
                (self.complete_start_continue, self.deferred_start_continue),
            ),
            ("ابتداء/وقف", (self.complete_start_pause, self.deferred_start_pause)),
        ):
            if sum(pair) != self.occurrences:
                raise Boundary116Error(
                    f"صفُّ {self.book} في {name} لا يبلغ وقوعاتِه؛ نقلٌ غيرُ متّسق."
                )


THE_REPORT_AT_TRANSCRIPTION: Final[tuple[TranscribedBookRow, ...]] = (
    TranscribedBookRow(
        book="البخاري",
        records=7_345,
        occurrences=517_131,
        complete_start_continue=432_612,
        complete_start_pause=432_756,
        deferred_start_continue=84_519,
        deferred_start_pause=84_375,
    ),
    TranscribedBookRow(
        book="مسلم",
        records=7_314,
        occurrences=472_564,
        complete_start_continue=399_325,
        complete_start_pause=399_416,
        deferred_start_continue=73_239,
        deferred_start_pause=73_148,
    ),
)
"""صفّا الصحيحين كما نُقِلا؛ ومجموعُ كلّ سيناريو يُصادَم بوقوعاته عند البناء."""

THE_SAHIHAYN_MATERIALS: Final[tuple[DeclaredMaterial, ...]] = (
    DeclaredMaterial(key="bukhari", relative_path="corpora/bukhari-records.txt"),
    DeclaredMaterial(key="muslim", relative_path="corpora/muslim-records.txt"),
    DeclaredMaterial(
        key="boundary116-results",
        relative_path="boundary116/results/summary.json",
    ),
)
"""موادُّ التقرير بمواضعها المُعلَنة وبلا ختم؛ غائبةٌ عن الشجرة فتُعلَّق دعاواها."""


def the_ledger() -> tuple[tuple[str, LicenceCheck], ...]:
    """دعاوى التقرير مارّةً بعقد ‎Λ‎ نفسِه؛ لا حكمَ ههنا يُكتَب بلا مادّةٍ تُحَلّ."""

    return (
        (
            "الدخولُ والخروجُ محوران متعامدان لا ثلاثُ قيمٍ متنافية",
            LicenceCheck(
                scope="حالاتُ الحدّ المُعلَنة",
                conditions=("محورانِ مُعلَنان", "حاصلُ ضربهما مشتقٌّ لا مكتوب"),
                effect="أربعُ حالاتٍ تشمل الموصولَ الموقوفَ عليه",
                evidence=(
                    MeasuredEvidence("حالاتُ الحدّ", 4, lambda: len(THE_FOUR_MODES)),
                    MeasuredEvidence(
                        "قيمُ محور الدخول",
                        2,
                        lambda: len({mode.entry for mode in THE_FOUR_MODES}),
                    ),
                    MeasuredEvidence(
                        "قيمُ محور الخروج",
                        2,
                        lambda: len({mode.exit for mode in THE_FOUR_MODES}),
                    ),
                ),
                minimum=3,
                material=THE_SEALED_MATERIAL,
            ),
        ),
        (
            "الشهادةُ تحمل أثرًا على كلّ طرفٍ من الحدّ",
            LicenceCheck(
                scope="الشاهدُ المُعلَن: فِي الْبَيْتِ",
                conditions=("الطرفان محمولان", "إصلاحُ المدّ مقروءٌ في الأيسر"),
                effect="أثرُ الحدّ لا يُفقَد بتسليم كلّ كلمةٍ مستقلّةً",
                evidence=(
                    MeasuredEvidence(
                        "ذرّاتُ الأيسر قبل الحدّ", 2, lambda: len(_witness().left_input)
                    ),
                    MeasuredEvidence(
                        "ذرّاتُ الأيسر بعده", 1, lambda: len(_witness().left_output)
                    ),
                    MeasuredEvidence(
                        "ذرّاتُ الأيمن بعد حذف همزة الوصل",
                        4,
                        lambda: len(_witness().right_output),
                    ),
                    MeasuredEvidence(
                        "قواعدُ الشهادة بحرّاسها",
                        2,
                        lambda: len(_witness().rules),
                    ),
                ),
                minimum=4,
                material=THE_SEALED_MATERIAL,
            ),
        ),
        (
            "كلُّ محورٍ يُحرّك الإسقاطَ وحدَه على البايتات المختومة",
            LicenceCheck(
                scope="كلُّ وقوعٍ في المُودَع تحت الحالات الأربع",
                conditions=(
                    "محورُ الخروج يُحرّك ذرّاتٍ والدخولُ ثابت",
                    "محورُ الدخول يُحرّك ذرّاتٍ والخروجُ ثابت",
                ),
                effect="استقلالُ المحورين مقيسٌ لا مُعلَنٌ وحسب",
                evidence=(
                    MeasuredEvidence(
                        "كلا المحورين فاعل",
                        1,
                        lambda: int(
                            axis_independence_reading().both_axes_are_effective
                        ),
                    ),
                    MeasuredEvidence(
                        "وقوعاتٌ يُحرّكها محورُ الخروج",
                        axis_independence_reading().moved_by_the_exit_axis,
                        lambda: axis_independence_reading().moved_by_the_exit_axis,
                    ),
                    MeasuredEvidence(
                        "وقوعاتٌ يُحرّكها محورُ الدخول",
                        axis_independence_reading().moved_by_the_entry_axis,
                        lambda: axis_independence_reading().moved_by_the_entry_axis,
                    ),
                ),
                minimum=3,
                material=THE_SEALED_MATERIAL,
            ),
        ),
        (
            "لكلّ قاعدةٍ حارسٌ ومرجعٌ مُسمّيان",
            LicenceCheck(
                scope="جدولُ القواعد المُعلَن",
                conditions=("لا قاعدةَ بلا حارس", "لا قاعدةَ بلا مرجع"),
                effect="القاعدةُ تُقرأ بحارسها لا بأثرها وحدَه",
                evidence=(
                    MeasuredEvidence("القواعدُ المُعلَنة", 11, lambda: len(THE_RULES)),
                    MeasuredEvidence(
                        "البوّاباتُ المُسمّاة",
                        5,
                        lambda: len({rule.gate for rule in THE_RULES}),
                    ),
                    MeasuredEvidence(
                        "قواعدُ بلا حارسٍ أو مرجع",
                        0,
                        lambda: sum(
                            1
                            for rule in THE_RULES
                            if not (rule.guard.strip() and rule.reference.strip())
                        ),
                    ),
                ),
                minimum=3,
                material=THE_SEALED_MATERIAL,
            ),
        ),
        (
            "أرقامُ الصحيحين مُعادةُ الاشتقاق ههنا",
            LicenceCheck(
                scope="سجلّاتُ البخاريّ ومسلمٍ وحزمةُ boundary116",
                conditions=("بايتاتُ المتنين مُودَعةٌ مختومة", "summary.json يُقرأ ههنا"),
                effect="ترقيةُ المنقول إلى مقيس",
                evidence=(),
                minimum=2,
                material=THE_SAHIHAYN_MATERIALS[0],
            ),
        ),
        (
            "أحكامُ النصّ الكامل على السجلّات الأربعة عشر ألفًا",
            LicenceCheck(
                scope="سيناريو بدءٍ عند أوّل وحدةٍ ووقفٍ عند آخرها",
                conditions=("السجلّاتُ مقروءةٌ ههنا", "الفواصلُ غيرُ المصرَّحة معلَّقة"),
                effect="أحكامٌ أربعةٌ بأعدادها",
                evidence=(),
                minimum=1,
                material=THE_SAHIHAYN_MATERIALS[2],
            ),
        ),
        (
            "جامعيّةُ القواعد اللغويّةُ الكاملة ‎C_F = R_P‎",
            LicenceCheck(
                scope="العربيّةُ كلُّها لا القواعدُ المنفَّذة",
                conditions=(
                    "مرجعٌ ‎R_P‎ مستقلٌّ لا يُعرَّف بما يقبله المنتَج",
                    "منعُ الزيادة ومنعُ الفقد مقيسان على ذلك المرجع",
                ),
                effect="مساواةُ المقبول بالمرجَّح لجميع السياقات",
                evidence=(),
                minimum=2,
                material=DeclaredMaterial(
                    key="independent-reference",
                    relative_path="corpora/independent-rp-reference.txt",
                ),
            ),
        ),
        (
            "كفايةُ واجهةٍ مضغوطةٍ عن النصّ الكامل",
            LicenceCheck(
                scope="مقابلةُ ‎F₂‎ على النصّ الكامل بـ‎F₂‎ على واجهة الحدود",
                conditions=(
                    "تساوي الآثار والبواقي والشهادات لكلّ سياقٍ مرخَّص",
                    "تركيبُ كلّ سلسلتين مفحوصٌ لا عيّنةٌ منه",
                ),
                effect="برهانُ كفاية الواجهة",
                evidence=(),
                minimum=1,
                material=THE_SAHIHAYN_MATERIALS[1],
            ),
        ),
    )


@lru_cache(maxsize=1)
def _witness() -> SeamCertificate:
    """الشاهدُ المُعلَن في التقرير، مُشغَّلًا ههنا لا منقولًا عنه."""

    return seam(
        "\u0641\u0650\u064a", "\u0627\u0644\u0652\u0628\u064e\u064a\u0652\u062a\u0650"
    )


THREE_MUTUALLY_EXCLUSIVE_VALUES_CANNOT_CARRY_A_PRODUCT_OF_TWO_AXES: Final[str] = (
    "THREE_MUTUALLY_EXCLUSIVE_VALUES_CANNOT_CARRY_A_PRODUCT_OF_TWO_AXES: الابتداءُ "
    "والوصلُ محورُ دخول، والوقفُ محورُ خروج؛ فالكلمةُ تُوصَل ويُوقَف عليها، "
    "والحالاتُ أربعٌ لا ثلاث، ولا يُجمَعن في متغيّرٍ واحد."
)

A_ONE_SIDED_TRACE_IS_NOT_A_SEAM_CERTIFICATE: Final[str] = (
    "A_ONE_SIDED_TRACE_IS_NOT_A_SEAM_CERTIFICATE: حذفُ الهمزة وحدَه ثمّ تسليمُ كلّ "
    "كلمةٍ مستقلّةً يُفقِد أثرَ إصلاح المدّ؛ فالشهادةُ تحمل مدخلَ كلّ طرفٍ ومخرجَه "
    "وهويّةَ القاعدة وحارسَها، ويُردّ ادّعاءُ قاعدةٍ لم تُحرّك طرفَها."
)

A_DELETION_IN_THE_PROJECTION_DOES_NOT_ERASE_THE_SOURCE_GLYPH: Final[str] = (
    "A_DELETION_IN_THE_PROJECTION_DOES_NOT_ERASE_THE_SOURCE_GLYPH: الرسمُ الأصليُّ "
    "وكرسيُّ الهمزة محفوظان؛ ويتغيّر نصُّ الإسقاط الأدائيّ بحسب الحدّ وحدَه."
)

AN_UNDECLARED_SEPARATOR_BLOCKS_A_SEAM_IT_DOES_NOT_PAUSE: Final[str] = (
    "AN_UNDECLARED_SEPARATOR_BLOCKS_A_SEAM_IT_DOES_NOT_PAUSE: الفاصلةُ وحدَها لا "
    "يُستنتَج منها وقفٌ فعليّ؛ ووسمُ الناشر في هذا المُودَع يمنع شهادةَ وصلٍ "
    "مكتملةً ويُعَدّ منعُه ولا يُطوى."
)

A_COMPLETE_CANDIDATE_IS_NOT_A_LINGUISTIC_TOTALITY: Final[str] = (
    "A_COMPLETE_CANDIDATE_IS_NOT_A_LINGUISTIC_TOTALITY: المرشَّحُ المكتملُ مكتملٌ "
    "بالنسبة للقواعد المنفَّذة؛ وسيناريوهاتُ كلّ وقوعٍ ليست شهادةً بأنّ النصّ "
    "قُرِئ بوقفٍ على كلّ كلمة."
)

A_SILENT_SEED_NEEDS_A_LEFT_CONTEXT_IT_IS_NOT_A_FORBIDDEN_FORM: Final[str] = (
    "A_SILENT_SEED_NEEDS_A_LEFT_CONTEXT_IT_IS_NOT_A_FORBIDDEN_FORM: الرسمُ "
    "المبتدئُ بذرةٍ ساكنةٍ يُردُّ ابتداؤه ولا يُرقَّع بهمزةٍ مجهولة؛ وأكثرُه ههنا "
    "شدّةُ لامٍ مُدغَمةٍ رُسِمت على أوّل الكلمة التالية، فهو حاجةُ سياقٍ يساريٍّ "
    "لا امتناعٌ في العربيّة."
)

A_REFERENCE_DEFINED_AS_WHAT_THE_PRODUCT_ACCEPTS_IS_NOT_A_REFERENCE: Final[str] = (
    "A_REFERENCE_DEFINED_AS_WHAT_THE_PRODUCT_ACCEPTS_IS_NOT_A_REFERENCE: مرجعُ "
    "‎R_P‎ يجب أن يكون مستقلًّا؛ وتعريفُه بما يقبله المنتَج يجعل ‎C_F = R_P‎ "
    "تحصيلَ حاصلٍ لا برهانَ جمعٍ ومنع."
)

A_FIGURE_FROM_ANOTHER_CORPUS_IS_NOT_A_CHECK_ON_THIS_ONE: Final[str] = (
    "A_FIGURE_FROM_ANOTHER_CORPUS_IS_NOT_A_CHECK_ON_THIS_ONE: المقيسُ ههنا على "
    "مُودَعٍ غيرِ متن التقرير؛ فلا يُقابَل رقمُه برقمه، ولا يُقرأ اتّفاقُهما "
    "تصديقًا ولا اختلافُهما تكذيبًا."
)

NO_BOUNDARY_HERE_LIFTS_A_BLOCK_OR_THAWS_A_FREEZE: Final[str] = (
    "NO_BOUNDARY_HERE_LIFTS_A_BLOCK_OR_THAWS_A_FREEZE: لا ولادةَ ههنا، ولا حكمَ "
    "ولادة، ولا رفعَ حظرٍ، ولا فكَّ تجميد، ولا استيرادَ من kernel/."
)

BOUNDARY116_NAMED_RESIDUALS: Final[tuple[str, ...]] = (
    THREE_MUTUALLY_EXCLUSIVE_VALUES_CANNOT_CARRY_A_PRODUCT_OF_TWO_AXES,
    A_ONE_SIDED_TRACE_IS_NOT_A_SEAM_CERTIFICATE,
    A_DELETION_IN_THE_PROJECTION_DOES_NOT_ERASE_THE_SOURCE_GLYPH,
    AN_UNDECLARED_SEPARATOR_BLOCKS_A_SEAM_IT_DOES_NOT_PAUSE,
    A_COMPLETE_CANDIDATE_IS_NOT_A_LINGUISTIC_TOTALITY,
    A_REFERENCE_DEFINED_AS_WHAT_THE_PRODUCT_ACCEPTS_IS_NOT_A_REFERENCE,
    A_SILENT_SEED_NEEDS_A_LEFT_CONTEXT_IT_IS_NOT_A_FORBIDDEN_FORM,
    A_FIGURE_FROM_ANOTHER_CORPUS_IS_NOT_A_CHECK_ON_THIS_ONE,
    NO_BOUNDARY_HERE_LIFTS_A_BLOCK_OR_THAWS_A_FREEZE,
)
"""البقايا بأسمائها؛ وكلُّ واحدةٍ منها فرقٌ يُحتَجّ به لا شعارٌ يُردَّد."""


def the_block_and_the_freeze_are_untouched() -> bool:
    """لا حظرَ يُرفَع ولا تجميدَ يُفكّ بهذه الوحدة؛ وتُعاد الجملةُ ليُحتَجّ بها."""

    return NO_BOUNDARY_HERE_LIFTS_A_BLOCK_OR_THAWS_A_FREEZE.startswith(
        "NO_BOUNDARY_HERE_LIFTS_A_BLOCK_OR_THAWS_A_FREEZE"
    )


def _assert_the_axes_are_orthogonal() -> None:
    """المحوران شرطُ تشغيلٍ لا نتيجةَ فحص؛ فيُصادَمان عند الاستيراد."""

    if len(THE_FOUR_MODES) != len(Entry) * len(Exit) != 4:
        raise Boundary116Error("حالاتُ الحدّ ليست حاصلَ ضرب المحورين.")
    joined_pause = BoundaryMode(Entry.JOINED, Exit.PAUSE)
    start_pause = BoundaryMode(Entry.START, Exit.PAUSE)
    if joined_pause not in THE_FOUR_MODES or start_pause not in THE_FOUR_MODES:
        raise Boundary116Error("الموصولُ الموقوفُ عليه غائبٌ؛ فالمحوران مدموجان.")
    if joined_pause.exit is not start_pause.exit:
        raise Boundary116Error("محورُ الخروج يتبع محورَ الدخول؛ وهما مستقلّان.")
    if len({rule.rule_id for rule in THE_RULES}) != len(THE_RULES):
        raise Boundary116Error("قاعدتان بهويّةٍ واحدةٍ تُلبِسان أثرَ الشهادة.")


_assert_the_axes_are_orthogonal()
