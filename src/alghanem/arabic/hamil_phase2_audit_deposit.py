"""الجولةُ الثانية من تدقيق hamil: على سجلّ الأختام الحيّ، لا على نقلٍ مُلصَق.

اختلفت أرضيّةُ هذه الجولة عن الأولى اختلافًا يُغيِّر جنسَ الفحص لا حجمَه.
فالجولةُ الأولى (`hamil_phase1_audit_deposit`) قامت على **نقلٍ مُلصَقٍ في
محادثة**: أرقامٌ نُسِخت إلى هذه الشجرة فأُعيد اشتقاقُها من أنفسها. وأمّا
ههنا فبايتاتُ ذاك السجلّ **مُودَعةٌ بحروفها** في `exhibits/hamil-induction/`
ببصمتيهما، فيُفتَح الملفّان عند كلّ قراءةٍ ويُعاد كلُّ حسابٍ منهما. فارتفع
جنسُ الفحص من «مُعادٌ من نقلٍ في نثرٍ» إلى «مُعادٌ من بايتاتٍ مُودَعة»، ولم
يرتفع إلى «مقيسٌ على مصدرهم»: مدوّنتُهم ليست مدوّنتَنا، والفصلُ بينهما قائمٌ
كما عُقِد في الجولة الأولى ولم يُرفَع
(`DEPOSITED_BYTES_RAISE_THE_GENUS_OF_A_CHECK_NOT_ITS_REACH`).

**أوّلًا: التدقيقُ الأوّلُ صار تاريخًا موثَّقًا لا حكمًا قائمًا.** فسجلُّهم
تحرَّك بعده: صار فيه أختامٌ بأصنافها ومسابرُها واختبارُ تكذيبٍ لم يكن. ولا
يُحاكَم سجلٌّ حاضرٌ بنقلٍ ماضٍ، ولا يُمحى حكمٌ ماضٍ لأنّ الحاضرَ خالفه. فالجولةُ
الأولى تبقى بتاريخها، وتُقرأ مناقضاتُها ههنا **واحدةً واحدة** فيُعلَن لكلٍّ
منها مصيرُها بالقياس على البايتات المُودَعة الآن
(`THE_FIRST_ROUND_IS_HISTORY_AND_HISTORY_IS_NOT_OVERWRITTEN`).

**وثانيًا: ولا تُحذَف مناقضةٌ ألبتّة.** لكلِّ واحدةٍ من الخمس مصيرٌ من ثلاثة
لا رابعَ له، وكلُّها **مشتقٌّ من الحساب لا مكتوبٌ في حقل**::

    RESOLVED_BY_REMEASUREMENT  — قِيست ثانيةً على سجلّهم الحاضر فوافقت
    STILL_CONTRADICTS          — أُعيدت فبقي الفارقُ مسمًّى بمقداره
    WITHDRAWN_BY_THE_REGISTER  — سقط أحدُ طرفيها من سجلّهم، فلا صِدام

والثالثُ ليس موافقةً ولا مناقضة: هو **انسحابُ طرفٍ**، ويُسمّى باسمه لأنّ
عدَّه موافقةً تبييضٌ، وعدَّه مناقضةً محاكمةُ نصٍّ لا يقوله أحد
(`A_WITHDRAWN_SIDE_IS_NEITHER_AN_AGREEMENT_NOR_A_CONTRADICTION`).

**وثالثًا: وقد تحوَّلت واحدةٌ فعلًا.** كان معدَّلُ ربح ماركوف يُنقَل عنهم
0.2133 بتًّا للبوّابة، ونقضَه الحسابُ في الجولة الأولى. وسجلُّهم الحاضر
يُعلن نصيبَ البوّابة على مقامٍ مُسمًّى — `Np` — فيوافقه الحسابُ ههنا إلى
أربع منازل. فالمناقضةُ الثانيةُ **مرفوعةٌ بإعادة القياس**، والرقمُ الباطل
يبقى في الجولة الأولى شاهدَ اتّهامٍ مؤرَّخًا لا رقمَ عمل.

**ورابعًا: سترلنج يبقى موضعَ التقاطع الحقيقيّ الوحيد.** فما يُعاد ههنا من
`letter_haraka_partition` — S(5,k) وBell(4) وBell(5) — تنفيذٌ ثانٍ مستقلّ،
واتّفاقُه شهادةٌ على الحسابين معًا. وما عداه اتّساقٌ داخل النقل: **نفيُ عطلٍ
لا إثباتُ صحّة**.

**خمولٌ سلطويّ**: لا ولادةَ هنا ولا حكمَ ولادة، ولا استيرادَ من `kernel/`
ولا من `program/`، ولا بوّابةَ في هذه الشجرة تقرأ هذا الإيداع حكمًا على
مادّةٍ عربيّة.
"""

from __future__ import annotations

import json
from dataclasses import dataclass, fields
from enum import Enum
from pathlib import Path
from typing import Any, Final

from .letter_haraka_partition import bell_number, stirling_second_kind

__all__ = [
    "AN_INTERNAL_IDENTITY_IS_STILL_NOT_AN_EXTERNAL_CONFIRMATION",
    "A_WITHDRAWN_SIDE_IS_NEITHER_AN_AGREEMENT_NOR_A_CONTRADICTION",
    "ArithmeticCheck",
    "CheckGenus",
    "CheckVerdict",
    "DEPOSITED_BYTES_RAISE_THE_GENUS_OF_A_CHECK_NOT_ITS_REACH",
    "HamilPhase2Error",
    "PhaseOneResidual",
    "ResidualStanding",
    "THE_EXHIBIT_DIRECTORY",
    "THE_FIRST_ROUND_IS_HISTORY_AND_HISTORY_IS_NOT_OVERWRITTEN",
    "phase_one_residuals",
    "register_tally",
    "the_checks",
    "verdict_tally",
]


class HamilPhase2Error(ValueError):
    """رفضٌ مُسمًّى في إيداع الجولة الثانية؛ ولا يُبتلَع خللٌ ههنا صمتًا."""


THE_EXHIBIT_DIRECTORY: Final[str] = "exhibits/hamil-induction"


def _exhibit_root() -> Path:
    root = Path(__file__).resolve().parents[3] / THE_EXHIBIT_DIRECTORY
    if not root.is_dir():
        raise HamilPhase2Error("معروضاتُ الجولة الثانية غائبةٌ عن القرص.")
    return root


def _read(name: str) -> Any:
    path = _exhibit_root() / name
    if not path.is_file():
        raise HamilPhase2Error(f"معروضٌ مُسمًّى غائب: {name}")
    return json.loads(path.read_text(encoding="utf-8"))


def the_register() -> dict[str, Any]:
    """سجلُّ أختامهم كما أُودِع، يُفتَح عند كلّ قراءةٍ ولا يُخزَن نسخةً."""

    loaded = _read("seals.json")["سجلُّ_الأختام"]
    if not isinstance(loaded, dict):
        raise HamilPhase2Error("سجلُّ الأختام لا يُقرأ خريطةً مسمّاة.")
    return loaded


def the_measurements() -> dict[str, Any]:
    """مقيسُ نتائجهم كما أُودِع؛ ولا يُقرأ رقمٌ منه سندًا لرقمٍ ههنا."""

    loaded = _read("results.json")["مقيس"]
    if not isinstance(loaded, dict):
        raise HamilPhase2Error("مقيسُ النتائج لا يُقرأ خريطةً مسمّاة.")
    return loaded


class CheckGenus(Enum):
    """جنسُ الفحص: من أين اشتُقَّ طرفاه؟ ولا يُخلَط جنسٌ بجنس."""

    RECOMPUTED_FROM_THE_DEPOSITED_BYTES = "مُعادٌ_من_البايتات_المودَعة"
    RECOMPUTED_BY_AN_INDEPENDENT_IMPLEMENTATION = "مُعادٌ_بتنفيذٍ_ثانٍ_مستقلّ"
    NOT_CHECKABLE_HERE = "غيرُ_قابلٍ_للفحص_ههنا"


class CheckVerdict(Enum):
    """حكمُ فحصٍ، مشتقٌّ من طرفيه عند القراءة ولا يُكتَب في حقل."""

    AGREES = "يوافق"
    CONTRADICTS = "يناقض"
    NOT_CHECKABLE_HERE = "لا_يُفحَص_ههنا"


@dataclass(frozen=True)
class ArithmeticCheck:
    """متطابقةٌ بطرفين وهامشٍ؛ وحكمُها يُحسَب ولا يُنقَل."""

    name: str
    statement: str
    genus: CheckGenus
    left: float | None
    right: float | None
    tolerance: float

    def __post_init__(self) -> None:
        if not self.name.strip():
            raise HamilPhase2Error("فحصٌ بلا اسمٍ لا يُودَع.")
        if not self.statement.strip():
            raise HamilPhase2Error("فحصٌ بلا نصِّ متطابقةٍ دعوى لا فحص.")
        if self.tolerance < 0:
            raise HamilPhase2Error("هامشٌ سالبٌ لا معنى له.")
        uncheckable = self.genus is CheckGenus.NOT_CHECKABLE_HERE
        if uncheckable != (self.left is None or self.right is None):
            raise HamilPhase2Error(
                "ما له طرفان يُفحَص، وما نقصه طرفٌ يُجنَّس غيرَ قابلٍ للفحص."
            )

    @property
    def verdict(self) -> CheckVerdict:
        """الحكمُ مشتقٌّ من الطرفين الآن؛ ولا حقلَ حكمٍ في هذه الوديعة."""

        if self.left is None or self.right is None:
            return CheckVerdict.NOT_CHECKABLE_HERE
        if abs(self.left - self.right) <= self.tolerance:
            return CheckVerdict.AGREES
        return CheckVerdict.CONTRADICTS

    @property
    def gap(self) -> float | None:
        """مقدارُ الفارق مسمًّى؛ فالمناقضةُ تُقاس ولا تُوصَف بالإجمال."""

        if self.left is None or self.right is None:
            return None
        return self.left - self.right


class ResidualStanding(Enum):
    """مصيرُ مناقضةٍ من الجولة الأولى بعد إعادة القياس على السجلّ الحاضر."""

    RESOLVED_BY_REMEASUREMENT = "مرفوعةٌ_بإعادة_القياس"
    STILL_CONTRADICTS = "باقيةٌ_بفجوةٍ_مسمّاة"
    WITHDRAWN_BY_THE_REGISTER = "منسحبٌ_أحدُ_طرفيها_من_سجلّهم"


@dataclass(frozen=True)
class PhaseOneResidual:
    """مناقضةٌ من الجولة الأولى، ومصيرُها ههنا مشتقٌّ لا مكتوب."""

    phase_one_name: str
    what_the_current_register_says: str
    check: ArithmeticCheck
    side_withdrawn: bool

    def __post_init__(self) -> None:
        if not self.phase_one_name.strip():
            raise HamilPhase2Error("بقيّةٌ بلا اسمِ فحصِها الأوّل لا تُتابَع.")
        if not self.what_the_current_register_says.strip():
            raise HamilPhase2Error("بقيّةٌ بلا بيانِ ما يقوله سجلُّهم الحاضر.")

    @property
    def standing(self) -> ResidualStanding:
        """المصيرُ يُشتقّ من الحساب ومن حضور الطرفين، لا من حقلٍ يُكتَب."""

        if self.side_withdrawn:
            return ResidualStanding.WITHDRAWN_BY_THE_REGISTER
        if self.check.verdict is CheckVerdict.AGREES:
            return ResidualStanding.RESOLVED_BY_REMEASUREMENT
        return ResidualStanding.STILL_CONTRADICTS


def _seal_values() -> dict[str, Any]:
    return {entry["اسم"]: entry["قيمة"] for entry in the_register()["أختام"]}


def register_tally() -> dict[str, int]:
    """تعدادُ سجلّهم مُشتقًّا من قائمته، لا منقولًا عن حقول التعداد فيه."""

    seals = the_register()["أختام"]
    return {
        "أختام": len(seals),
        "بوّابات": sum(1 for entry in seals if entry["صنف"] == "بوّابة"),
        "شواهد": sum(1 for entry in seals if entry["صنف"] == "شاهد"),
        "ودائع": len({entry["وديعة"] for entry in seals}),
    }


def the_checks() -> tuple[ArithmeticCheck, ...]:
    """كلُّ متطابقةٍ تُعاد ههنا من البايتات المُودَعة، وحكمُها يُحسَب الآن."""

    measured = the_measurements()
    register = the_register()
    tally = register_tally()
    seal = _seal_values()
    field = measured["حقل112"]
    reconciliation = measured["مصالحة_العد"]

    return (
        ArithmeticCheck(
            name="سجلُّهم: المجموعُ بأصنافه",
            statement="بوّاباتٌ + شواهدُ بإزاء طولِ قائمة الأختام نفسِها",
            genus=CheckGenus.RECOMPUTED_FROM_THE_DEPOSITED_BYTES,
            left=float(tally["بوّابات"] + tally["شواهد"]),
            right=float(tally["أختام"]),
            tolerance=0.0,
        ),
        ArithmeticCheck(
            name="سجلُّهم: المسابرُ بإزاء ودائع الأختام",
            statement="عددُ المسابر المُعلَن بإزاء عددِ الودائع المذكورة في الأختام",
            genus=CheckGenus.RECOMPUTED_FROM_THE_DEPOSITED_BYTES,
            left=float(len(register["مسبارات"])),
            right=float(tally["ودائع"]),
            tolerance=0.0,
        ),
        ArithmeticCheck(
            name="سجلُّهم: حيويّتُه مشتقّةٌ لا مُعلَنة",
            statement=(
                "«حيٌّ: كلُّ ختمٍ يولَّد ويُصادَم» بإزاء خلوِّ المنزاحة وبلا "
                "المولِّد والودائعِ المخالِفة معًا"
            ),
            genus=CheckGenus.RECOMPUTED_FROM_THE_DEPOSITED_BYTES,
            left=float(
                len(register["أختامٌ_انحرفت"])
                + len(register["أختامٌ_بلا_مولِّد"])
                + len(register["ودائعُ_خالفت"])
            ),
            right=0.0,
            tolerance=0.0,
        ),
        ArithmeticCheck(
            name="سجلُّهم: اختبارُ التكذيب يرفض فعلًا",
            statement="محاولاتُ التكذيب المُعلَنة بإزاء عددِ المرفوضة منها",
            genus=CheckGenus.RECOMPUTED_FROM_THE_DEPOSITED_BYTES,
            left=float(len(register["اختبارُ_التكذيب"])),
            right=float(
                sum(1 for trial in register["اختبارُ_التكذيب"] if trial["مرفوضة"])
            ),
            tolerance=0.0,
        ),
        ArithmeticCheck(
            name="ماركوف: الربحُ الكلّيُّ فرقُ كلفتين",
            statement="ختمُ «الربحُ الكلّيّ» بإزاء فرقِ كلفتَي ماركوف في ملفّ النتائج",
            genus=CheckGenus.RECOMPUTED_FROM_THE_DEPOSITED_BYTES,
            left=float(seal["ماركوف · الربحُ الكلّيّ"]),
            right=float(measured["markov"][0] - measured["markov"][1]),
            tolerance=1e-9,
        ),
        ArithmeticCheck(
            name="ماركوف: نصيبُ البوّابة على مقامٍ مُسمًّى",
            statement=(
                "0.0465 المُعلَنُ في ملاحظة الختم بإزاء قسمةِ الربح الكلّيّ "
                "على Np — وهذا موضعُ المناقضة الثانية من الجولة الأولى"
            ),
            genus=CheckGenus.RECOMPUTED_FROM_THE_DEPOSITED_BYTES,
            left=0.0465,
            right=float(seal["ماركوف · الربحُ الكلّيّ"]) / float(measured["Np"]),
            tolerance=0.0001,
        ),
        ArithmeticCheck(
            name="ماركوف: فارقُ الترتيبين",
            statement="ختمُ «فارقُ الترتيبين» بإزاء orders_gap في ملفّ النتائج",
            genus=CheckGenus.RECOMPUTED_FROM_THE_DEPOSITED_BYTES,
            left=float(seal["ماركوف · فارقُ الترتيبين"]),
            right=float(measured["orders_gap"]),
            tolerance=1e-9,
        ),
        ArithmeticCheck(
            name="الجشعُ = الاستنفاد",
            statement="ختمُ الفارق الصفر بإزاء gap في ملفّ النتائج",
            genus=CheckGenus.RECOMPUTED_FROM_THE_DEPOSITED_BYTES,
            left=float(seal["الجشعُ = الاستنفاد"]),
            right=float(measured["gap"]),
            tolerance=0.0,
        ),
        ArithmeticCheck(
            name="الانتقالاتُ بإزاء شطر التدريب",
            statement="مجموعُ خانات جدول الانتقالات بإزاء Ntr المُعلَن",
            genus=CheckGenus.RECOMPUTED_FROM_THE_DEPOSITED_BYTES,
            left=float(sum(measured["transitions"].values())),
            right=float(measured["Ntr"]),
            tolerance=0.0,
        ),
        ArithmeticCheck(
            name="الهوامشُ بإزاء حجم المجموع",
            statement="مجموعُ الهوامش الخمسة بإزاء Nv المُعلَن",
            genus=CheckGenus.RECOMPUTED_FROM_THE_DEPOSITED_BYTES,
            left=float(sum(measured["marginal"].values())),
            right=float(measured["Nv"]),
            tolerance=0.0,
        ),
        ArithmeticCheck(
            name="شطرا الاختبار والتدريب بإزاء المجموع",
            statement="Ntr + Nte بإزاء Np المُعلَن",
            genus=CheckGenus.RECOMPUTED_FROM_THE_DEPOSITED_BYTES,
            left=float(measured["Ntr"] + measured["Nte"]),
            right=float(measured["Np"]),
            tolerance=0.0,
        ),
        ArithmeticCheck(
            name="البوّاباتُ بإزاء المجموع",
            statement="Np بإزاء Nv ناقصَ واحد — بوّابةٌ بين كلّ متجاورين",
            genus=CheckGenus.RECOMPUTED_FROM_THE_DEPOSITED_BYTES,
            left=float(measured["Np"]),
            right=float(measured["Nv"] - 1),
            tolerance=0.0,
        ),
        ArithmeticCheck(
            name="مصالحةُ العدّ تُقفِل",
            statement="الحقلُ 112 المرخَّص + الفارقُ الكامل بإزاء المرخَّص بالأبجد الخام",
            genus=CheckGenus.RECOMPUTED_FROM_THE_DEPOSITED_BYTES,
            left=float(
                reconciliation["الحقل112_المرخص"] + reconciliation["الفارق_الكامل"]
            ),
            right=float(reconciliation["مرخص_الكل_بالأبجد_الخام"]),
            tolerance=0.0,
        ),
        ArithmeticCheck(
            name="تفكيكُ الفارق يجمع فارقَه",
            statement="مجموعُ بنود التفكيك الثلاثة بإزاء الفارق الكامل المُعلَن",
            genus=CheckGenus.RECOMPUTED_FROM_THE_DEPOSITED_BYTES,
            left=float(sum(reconciliation["تفكيكه"].values())),
            right=float(reconciliation["الفارق_الكامل"]),
            tolerance=0.0,
        ),
        ArithmeticCheck(
            name="قاعدةُ السلسلة في الحقل 112",
            statement=(
                "H(ح)+H(هـ|ح) بإزاء H(هـ)+H(ح|هـ) — متطابقةٌ بالتعريف، "
                "والفرقُ ههنا أكبرُ من تقريبِ أربعِ منازل"
            ),
            genus=CheckGenus.RECOMPUTED_FROM_THE_DEPOSITED_BYTES,
            left=float(field["H_letter"] + field["H_state_letter"]),
            right=float(field["H_state"] + field["H_letter_state"]),
            tolerance=0.0001,
        ),
        ArithmeticCheck(
            name="التقسيمُ بإزاء اللاتقسيم",
            statement="كلفةُ الأمثل بإزاء كلفةِ الأحاديّ؛ والأرخصُ هو المشتري",
            genus=CheckGenus.RECOMPUTED_FROM_THE_DEPOSITED_BYTES,
            left=float(measured["optimal"][0]),
            right=float(measured["unigram"][0]),
            tolerance=0.0,
        ),
        ArithmeticCheck(
            name="سترلنج: S(5,k) بتنفيذٍ ثانٍ",
            statement="جدولُ سترلنج المنقولُ بإزاء ما يحسبه letter_haraka_partition",
            genus=CheckGenus.RECOMPUTED_BY_AN_INDEPENDENT_IMPLEMENTATION,
            left=float(sum(int(value) for value in measured["stirling"].values())),
            right=float(sum(stirling_second_kind(5, k) for k in range(1, 6))),
            tolerance=0.0,
        ),
        ArithmeticCheck(
            name="بِلّ(5) بتنفيذٍ ثانٍ",
            statement="Bell5 المنقولُ بإزاء ما يحسبه letter_haraka_partition",
            genus=CheckGenus.RECOMPUTED_BY_AN_INDEPENDENT_IMPLEMENTATION,
            left=float(measured["bell"]),
            right=float(bell_number(5)),
            tolerance=0.0,
        ),
        ArithmeticCheck(
            name="سترلنج: S(28,4) بتنفيذٍ ثانٍ",
            statement="S28_k2_k6[4] المنقولُ بإزاء ما يحسبه letter_haraka_partition",
            genus=CheckGenus.RECOMPUTED_BY_AN_INDEPENDENT_IMPLEMENTATION,
            left=float(field["stirling"]["S28_k2_k6"]["4"]),
            right=float(stirling_second_kind(28, 4)),
            tolerance=0.0,
        ),
        ArithmeticCheck(
            name="بايتاتُ مدوّنتهم على مدوّنتنا",
            statement=(
                "لا يُفحَص ههنا: مُخرَجُ نموذجهم المُدرَّب على مدوّنتهم لا "
                "يُعاد من بايتاتٍ مُودَعةٍ ولا من مدوّنتنا"
            ),
            genus=CheckGenus.NOT_CHECKABLE_HERE,
            left=None,
            right=None,
            tolerance=0.0,
        ),
    )


def phase_one_residuals() -> tuple[PhaseOneResidual, ...]:
    """مناقضاتُ الجولة الأولى الخمس، لكلٍّ مصيرٌ مشتقٌّ ولا واحدةَ تُحذَف."""

    measured = the_measurements()
    by_name = {check.name: check for check in the_checks()}

    return (
        PhaseOneResidual(
            phase_one_name="قاعدةُ السلسلة في الحقل 112",
            what_the_current_register_says=(
                "سجلُّهم الحاضرُ لا يُعلن الإنتروبيّاتِ أختامًا، وملفُّ "
                "النتائج يُبقيها كما كانت؛ فأُعيد الحسابُ عليها بعينها."
            ),
            check=by_name["قاعدةُ السلسلة في الحقل 112"],
            side_withdrawn=False,
        ),
        PhaseOneResidual(
            phase_one_name="معدّلُ ربح ماركوف لكلّ بوّابة",
            what_the_current_register_says=(
                "المقامُ صار مُسمًّى: «بت على 6,235 بوّابة»، ونصيبُ البوّابة "
                "0.0465؛ فسقط 0.2133 من سجلّهم الحاضر ووافق الحسابُ المُعلَن."
            ),
            check=by_name["ماركوف: نصيبُ البوّابة على مقامٍ مُسمًّى"],
            side_withdrawn=False,
        ),
        PhaseOneResidual(
            phase_one_name="ربحُ خارج العيّنة",
            what_the_current_register_says=(
                "لا ختمَ لربح خارج العيّنة في سجلّهم الحاضر، ولا يُعلَن 4.96 "
                "فيه بمقامٍ؛ فالطرفُ المنقولُ منسحب."
            ),
            check=ArithmeticCheck(
                name="ربحُ خارج العيّنة — الطرفُ المنسحب",
                statement=(
                    "فرقُ الإنتروبيتين المتقاطعتين مضروبًا في حجم شطر الاختبار "
                    "= 49.890 بتًّا؛ ولا طرفَ ثانيَ له في سجلّهم الحاضر"
                ),
                genus=CheckGenus.NOT_CHECKABLE_HERE,
                left=None,
                right=None,
                tolerance=0.0,
            ),
            side_withdrawn=True,
        ),
        PhaseOneResidual(
            phase_one_name="التقسيمُ بإزاء اللاتقسيم",
            what_the_current_register_says=(
                "ملفُّ النتائج يُبقي كلفتَي الأمثل والأحاديّ كما كانتا، "
                "والأمثلُ أغلى؛ فالفجوةُ باقيةٌ بمقدارها."
            ),
            check=by_name["التقسيمُ بإزاء اللاتقسيم"],
            side_withdrawn=False,
        ),
        PhaseOneResidual(
            phase_one_name="الهامشُ T بين نقلين",
            what_the_current_register_says=(
                "T = 102 في ملفّ النتائج المُودَع، ولا ذكرَ لـ209 في سجلّهم "
                "الحاضر ولا في بايتاته؛ فالطرفُ الشفاهيُّ منسحب."
            ),
            check=ArithmeticCheck(
                name="الهامشُ T — الطرفُ المنسحب",
                statement=(
                    f"T = {measured['marginal']['T']} في البايتات المُودَعة، "
                    "وما نُقل شفاهًا لا بايتاتِ له ههنا فلا يُصادَم"
                ),
                genus=CheckGenus.NOT_CHECKABLE_HERE,
                left=None,
                right=None,
                tolerance=0.0,
            ),
            side_withdrawn=True,
        ),
    )


def verdict_tally() -> dict[str, int]:
    """تعدادُ أحكام الجولة الثانية، مشتقًّا من الفحوص لا مكتوبًا فيها."""

    checks = the_checks()
    residuals = phase_one_residuals()
    tally = {verdict.name.lower(): 0 for verdict in CheckVerdict}
    for check in checks:
        tally[check.verdict.name.lower()] += 1
    tally["checks"] = len(checks)
    tally["independent_cross_checks"] = sum(
        1
        for check in checks
        if check.genus is CheckGenus.RECOMPUTED_BY_AN_INDEPENDENT_IMPLEMENTATION
    )
    for standing in ResidualStanding:
        tally[standing.name.lower()] = sum(
            1 for residual in residuals if residual.standing is standing
        )
    return tally


DEPOSITED_BYTES_RAISE_THE_GENUS_OF_A_CHECK_NOT_ITS_REACH: Final[str] = (
    "DEPOSITED_BYTES_RAISE_THE_GENUS_OF_A_CHECK_NOT_ITS_REACH: إيداعُ "
    "البايتات يرفع الفحصَ من نقلٍ مُلصَقٍ إلى مصدرٍ مقروء، ولا يبلغ به "
    "مدوّنتَهم؛ فالفصلُ بين المدوّنتين قائمٌ كما عُقِد."
)

THE_FIRST_ROUND_IS_HISTORY_AND_HISTORY_IS_NOT_OVERWRITTEN: Final[str] = (
    "THE_FIRST_ROUND_IS_HISTORY_AND_HISTORY_IS_NOT_OVERWRITTEN: الجولةُ "
    "الأولى تبقى بتاريخها؛ لا يُمحى حكمُها لأنّ الحاضرَ خالفه، ولا يُحاكَم "
    "سجلٌّ حاضرٌ بنقلٍ ماضٍ."
)

A_WITHDRAWN_SIDE_IS_NEITHER_AN_AGREEMENT_NOR_A_CONTRADICTION: Final[str] = (
    "A_WITHDRAWN_SIDE_IS_NEITHER_AN_AGREEMENT_NOR_A_CONTRADICTION: سقوطُ "
    "طرفٍ من سجلّهم انسحابٌ يُسمّى باسمه؛ عدُّه موافقةً تبييض، وعدُّه "
    "مناقضةً محاكمةُ نصٍّ لا يقوله أحد."
)

AN_INTERNAL_IDENTITY_IS_STILL_NOT_AN_EXTERNAL_CONFIRMATION: Final[str] = (
    "AN_INTERNAL_IDENTITY_IS_STILL_NOT_AN_EXTERNAL_CONFIRMATION: اتّساقُ "
    "بايتاتٍ مُودَعةٍ مع نفسها نفيُ عطلٍ لا إثباتُ صحّة؛ وعددان مختلقان "
    "متّسقان يمرّان هذا الفحصَ بعينه."
)


def _assert_no_verdict_field_is_written() -> None:
    """حارسٌ بنيويّ: لا حقلَ حكمٍ في فحصٍ ولا مصيرٍ في بقيّة."""

    for holder in (ArithmeticCheck, PhaseOneResidual):
        written = {item.name for item in fields(holder)}
        for forbidden in ("verdict", "standing", "gap"):
            if forbidden in written:
                raise HamilPhase2Error(f"{holder.__name__}: الحكمُ يُشتقّ ولا يُكتَب حقلًا.")


def _assert_every_residual_is_followed() -> None:
    """حارسٌ بنيويّ: لا تُحذَف مناقضةٌ من الخمس، ولكلٍّ مصيرٌ مُسمًّى."""

    residuals = phase_one_residuals()
    if len(residuals) != 5:
        raise HamilPhase2Error("مناقضاتُ الجولة الأولى خمسٌ، ولا تُطوى واحدةٌ منها.")
    if len({residual.phase_one_name for residual in residuals}) != 5:
        raise HamilPhase2Error("اسمٌ مكرَّرٌ في متابعة المناقضات.")
    for residual in residuals:
        if not isinstance(residual.standing, ResidualStanding):
            raise HamilPhase2Error("مصيرٌ خارجَ الأجناس الثلاثة لا يُقبَل.")


_assert_no_verdict_field_is_written()
_assert_every_residual_is_followed()
