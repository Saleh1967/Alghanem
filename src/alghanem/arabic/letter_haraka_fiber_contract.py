"""عقدٌ ليفيٌّ للحرف والحركة: كلُّ عنصرٍ بدليله وموانعه وبقاياه.

**ما تفعله هذه الوحدة**: تُعدِّد عناصرَ دعوى الحرف والحركة عنصرًا عنصرًا، وتُلزِم
كلَّ عنصرٍ بأربعةٍ مجتمعة — ما يُدَّعى، والدليلُ عليه، والموانعُ من انعقاده،
والبقايا التي لم يحملها — ثمّ تُشغِّل العقدَ على إيداعٍ مُبصَّمٍ فتُخرِج منزلةَ
كلِّ عنصرٍ على حدةٍ لا منزلةً جامعة.

**والفصلُ الأوّل محفوظٌ بنيويًّا: الحرفُ المكتوب ليس صوتًا**
(`AWrittenLetterIsNotASound`). فجنسُ الدليل مُعلَنٌ في كلّ عنصر، وعنصرٌ دليلُه
`RECORDED_SOUND` **لا ينعقد بحال** في هذه الشجرة، لأنّ `UnicodeIsNotRecordedSound`
قائمٌ: لا قطعةَ ههنا صوتٌ مُسجَّل. فعناصرُ القيمة الصوتيّة للحرف والحركة
والسكون مكتوبةٌ في العقد **محجوبةً بمانعها**، لا محذوفةً لأنّها لم تنعقد.

**والفصلُ الثاني محفوظٌ بنيويًّا كذلك: السكونُ المكتوب ليس غيابَ التشكيل**
(`AWrittenSukunIsNotAnAbsentDiacritic`). فهما موضوعان متمايزان لا يجمعهما
عنصرٌ واحد، ويُرَدُّ جمعُهما عند الإنشاء؛ وتمايزُهما مقيسٌ لا مفترَض: علامةُ
السكون محمولةٌ على محورها، والغيابُ خلوُّ المحاور المقيسة جميعًا، والعددان
يُشتقّان من الإيداع نفسِه فيختلفان.

**والدليلُ مُشتَقٌّ لا منقول**: كلُّ عددٍ في العقد يُعاد اشتقاقُه من بايتات
الإيداع المُبصَّمة عند كلّ تشغيل، ولا يُكتَب رقمٌ باليد
(`EveryFigureIsRederivedFromTheDepositedBytes`).

**وتجربةُ هذا العقد غيرُ موقوفةٍ على شهادة ولادة**
(`RunningTheContractIsNotBlockedOnACertificate`): يُشغَّل اليومَ ويُقرأ اليومَ،
وشهادةُ ولادة `CV` غيرُ صادرةٍ في `fiber_transfer_contracts`؛ فالعقدُ يُجرَّب
ولا يُصدِر شهادة. وانعقادُ عنصرٍ هنا **ليس ولادةً** ولا حكمَ ولادةٍ كرنليًّا
ولا تجميدَ `E0`، ولا تُوصَل `BirthVerdictGate` بهذه الوحدة، ولا تستورد من
`kernel/` شيئًا.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Final

from .carrier_state_observed_fiber import (
    ABSENT,
    ObservedFiberTable,
    OccurrenceRow,
    run_observed_fiber_on_the_deposited_fatiha,
)

__all__ = [
    "A_WRITTEN_LETTER_IS_NOT_A_SOUND_NOTE",
    "A_WRITTEN_SUKUN_IS_NOT_AN_ABSENT_DIACRITIC_NOTE",
    "EVERY_FIGURE_IS_REDERIVED_FROM_THE_DEPOSITED_BYTES_NOTE",
    "LETTER_HARAKA_CONTRACT_ID",
    "LETTER_HARAKA_NAMED_RESIDUALS",
    "RUNNING_THE_CONTRACT_IS_NOT_BLOCKED_ON_A_CERTIFICATE_NOTE",
    "THIS_CONTRACT_ISSUES_NO_BIRTH_NOTE",
    "ContractElement",
    "ElementReading",
    "ElementStanding",
    "EvidenceGenus",
    "LetterHarakaContractError",
    "LetterHarakaReport",
    "Subject",
    "build_letter_haraka_contract",
    "count_absent_diacritic_rows",
    "count_written_sukun_rows",
    "run_letter_haraka_contract",
]


class LetterHarakaContractError(ValueError):
    """رفضٌ صريح: عنصرٌ بلا دليلٍ أو بلا مانعٍ أو جامعٌ بين موضوعين متمايزين."""


LETTER_HARAKA_CONTRACT_ID: Final[str] = "contract.letter_haraka.g0_fiber_1"


class Subject(Enum):
    """موضوعاتُ العقد، متمايزةً لا يجمع عنصرٌ واحدٌ اثنين منها."""

    WRITTEN_LETTER = "الحرفُ المكتوب"
    WRITTEN_HARAKA = "الحركةُ المكتوبة"
    WRITTEN_SUKUN = "السكونُ المكتوب"
    ABSENT_DIACRITIC = "غيابُ التشكيل"


class EvidenceGenus(Enum):
    """جنسُ الدليل؛ وهو الذي يحفظ الفصلَ بين المكتوب والمسموع."""

    ORTHOGRAPHIC_OBSERVATION = "رصدٌ على الرسم المُرمَّز"
    RECORDED_SOUND = "صوتٌ مُسجَّل"


class ElementStanding(Enum):
    """منزلةُ العنصر بعد التشغيل، لكلِّ عنصرٍ على حدة."""

    HELD_ON_THE_DEPOSIT = "انعقد_على_الإيداع"
    WITHHELD_BY_A_PREVENTER = "محجوبٌ_بمانعٍ_مُسمّى"


# --- العنصر: ما يُدَّعى، ودليلُه، وموانعُه، وبقاياه -------------------------------


@dataclass(frozen=True)
class ContractElement:
    """عنصرٌ واحدٌ في العقد، لا يُقبَل ناقصَ واحدةٍ من أربعته."""

    element_id: str
    subject: Subject
    what_is_claimed: str
    evidence_genus: EvidenceGenus
    what_the_evidence_counts: str
    preventers: tuple[str, ...]
    residuals: tuple[str, ...]

    def __post_init__(self) -> None:
        for name, value in (
            ("element_id", self.element_id),
            ("what_is_claimed", self.what_is_claimed),
            ("what_the_evidence_counts", self.what_the_evidence_counts),
        ):
            if not value.strip():
                raise LetterHarakaContractError(f"العنصرُ بلا «{name}» مكتوب")
        if not self.residuals:
            raise LetterHarakaContractError(
                f"العنصرُ «{self.element_id}» بلا بقيّةٍ مُسمّاة؛ والخلوُّ ليس إعفاءً"
            )
        for field_name, values in (
            ("preventers", self.preventers),
            ("residuals", self.residuals),
        ):
            if any(not item.strip() for item in values):
                raise LetterHarakaContractError(
                    f"«{field_name}» في «{self.element_id}» فيه مدخلٌ فارغ"
                )
            if len(set(values)) != len(values):
                raise LetterHarakaContractError(
                    f"«{field_name}» في «{self.element_id}» فيه تكرار"
                )
        if self.evidence_genus is EvidenceGenus.RECORDED_SOUND and not self.preventers:
            raise LetterHarakaContractError(
                "عنصرٌ دليلُه صوتٌ مُسجَّلٌ بلا مانعٍ مكتوب " "(AWrittenLetterIsNotASound)"
            )

    @property
    def is_reachable_in_this_tree(self) -> bool:
        """أيمكن أن ينعقد هذا العنصرُ ههنا؟ لا، إن كان دليلُه صوتًا مُسجَّلًا."""

        return self.evidence_genus is EvidenceGenus.ORTHOGRAPHIC_OBSERVATION


@dataclass(frozen=True)
class ElementReading:
    """قراءةُ عنصرٍ بعد التشغيل: منزلتُه، وعددُه المُشتَقّ، وسببُ حجبه إن حُجِب."""

    element: ContractElement
    standing: ElementStanding
    observed_count: int
    withheld_because: str

    def __post_init__(self) -> None:
        if self.observed_count < 0:
            raise LetterHarakaContractError("عددٌ مرصودٌ سالب")
        if self.standing is ElementStanding.WITHHELD_BY_A_PREVENTER:
            if not self.withheld_because.strip():
                raise LetterHarakaContractError("حجبٌ بلا سببٍ مكتوب")
        elif self.withheld_because.strip():
            raise LetterHarakaContractError("عنصرٌ منعقدٌ ويُكتَب له سببُ حجب")
        elif self.observed_count <= 0:
            raise LetterHarakaContractError(
                f"«{self.element.element_id}» انعقد بلا وقوعٍ مرصودٍ واحد"
            )


@dataclass(frozen=True)
class LetterHarakaReport:
    """مخرَجُ تشغيلٍ واحد: قراءةٌ لكلّ عنصر، وبصمةُ الإيداع الذي اشتُقَّت منه."""

    contract_id: str
    deposit_sha256: str
    readings: tuple[ElementReading, ...]

    def reading_for(self, element_id: str) -> ElementReading:
        for reading in self.readings:
            if reading.element.element_id == element_id:
                return reading
        raise LetterHarakaContractError(f"لا عنصرَ في العقد باسم «{element_id}»")

    @property
    def held(self) -> tuple[str, ...]:
        return tuple(
            reading.element.element_id
            for reading in self.readings
            if reading.standing is ElementStanding.HELD_ON_THE_DEPOSIT
        )

    @property
    def withheld(self) -> tuple[str, ...]:
        return tuple(
            reading.element.element_id
            for reading in self.readings
            if reading.standing is ElementStanding.WITHHELD_BY_A_PREVENTER
        )


# --- عدُّ الموضوعين المتمايزين من الإيداع نفسِه ------------------------------------


def _axis(row: OccurrenceRow, axis_id: str) -> str:
    for measured_axis, value in row.state_vector:
        if measured_axis == axis_id:
            return value
    raise LetterHarakaContractError(f"المحورُ «{axis_id}» ليس في المتَّجِه المقيس")


def count_written_sukun_rows(table: ObservedFiberTable) -> int:
    """الوقوعاتُ الحاملةُ علامةَ سكونٍ مكتوبةً على محورها."""

    return sum(1 for row in table.rows if _axis(row, "quiescence") != ABSENT)


def count_absent_diacritic_rows(table: ObservedFiberTable) -> int:
    """الوقوعاتُ الخاليةُ من كلّ علامةٍ على المحاور المقيسة؛ وهي غيرُ السكون."""

    return sum(
        1 for row in table.rows if all(value == ABSENT for _, value in row.state_vector)
    )


def _count_written_haraka_rows(table: ObservedFiberTable) -> int:
    return sum(1 for row in table.rows if _axis(row, "vowel") != ABSENT)


def _count_haraka_with_gemination_rows(table: ObservedFiberTable) -> int:
    return sum(
        1
        for row in table.rows
        if _axis(row, "vowel") != ABSENT and _axis(row, "gemination") != ABSENT
    )


def _count_haraka_with_sukun_rows(table: ObservedFiberTable) -> int:
    return sum(
        1
        for row in table.rows
        if _axis(row, "vowel") != ABSENT and _axis(row, "quiescence") != ABSENT
    )


# --- العقد نفسُه ------------------------------------------------------------------


_NO_RECORDED_SOUND_PREVENTER: Final[str] = (
    "UnicodeIsNotRecordedSound: لا قطعةَ في هذه الشجرة صوتٌ مُسجَّل، فالقيمةُ "
    "الصوتيّة غيرُ قابلةٍ للاختبار ههنا بحال"
)

_A_TRANSCRIPTION_IS_THE_PRODUCERS: Final[str] = (
    "ATranscriptionIsTheProducersChoice: ما في الإيداع رسمُ ناسخٍ بعينه، "
    "فالعددُ عددُ وقوعاتٍ في هذا النصّ لا حكمٌ على العربيّة"
)


def build_letter_haraka_contract() -> tuple[ContractElement, ...]:
    """عناصرُ العقد مُجمَّدةً قبل أيّ تشغيل؛ لا عددَ فيها ولا منزلة."""

    return (
        ContractElement(
            element_id="letter.written.is_an_observed_carrier",
            subject=Subject.WRITTEN_LETTER,
            what_is_claimed="الحرفُ المكتوب حاملٌ مرصودٌ يُعَدُّ وقوعُه في الإيداع",
            evidence_genus=EvidenceGenus.ORTHOGRAPHIC_OBSERVATION,
            what_the_evidence_counts="وقوعاتُ الحوامل في الإيداع المُبصَّم",
            preventers=(),
            residuals=(
                _A_TRANSCRIPTION_IS_THE_PRODUCERS,
                "رسمُ الحرف لا يُميِّز صوَرَه الموضعيّة، فلا تُدَّعى هنا وحدةُ صورة",
            ),
        ),
        ContractElement(
            element_id="letter.phonetic.has_a_determinate_value",
            subject=Subject.WRITTEN_LETTER,
            what_is_claimed="للحرف المكتوب قيمةٌ صوتيّةٌ مُعيَّنةٌ تُختبَر هنا",
            evidence_genus=EvidenceGenus.RECORDED_SOUND,
            what_the_evidence_counts="قطعُ الصوت المُسجَّل المقابلةُ لكلّ حرف",
            preventers=(_NO_RECORDED_SOUND_PREVENTER,),
            residuals=("بقاءُ العنصر مكتوبًا محجوبًا شاهدٌ على أنّه لم يُحذَف لتعذّره",),
        ),
        ContractElement(
            element_id="haraka.written.is_an_observed_mark",
            subject=Subject.WRITTEN_HARAKA,
            what_is_claimed="الحركةُ المكتوبة علامةٌ مرصودةٌ على محورٍ خاصٍّ بها",
            evidence_genus=EvidenceGenus.ORTHOGRAPHIC_OBSERVATION,
            what_the_evidence_counts="الوقوعاتُ الحاملةُ علامةَ حركةٍ على محور الحركة",
            preventers=(),
            residuals=(
                _A_TRANSCRIPTION_IS_THE_PRODUCERS,
                "المدُّ محورٌ مؤجَّلٌ لا يدخل المتَّجِه المقيس، فليس في العدد",
            ),
        ),
        ContractElement(
            element_id="haraka.written.is_not_the_letter_itself",
            subject=Subject.WRITTEN_HARAKA,
            what_is_claimed=(
                "الحركةُ ليست قيمةً في الحرف نفسِه، بدليل اجتماع علامتين من "
                "محورين على حاملٍ واحد"
            ),
            evidence_genus=EvidenceGenus.ORTHOGRAPHIC_OBSERVATION,
            what_the_evidence_counts="الوقوعاتُ الجامعةُ بين علامة حركةٍ وعلامة شدّة",
            preventers=(),
            residuals=("اجتماعُ علامتين في الرسم لا يُثبِت استقلالَهما في النطق",),
        ),
        ContractElement(
            element_id="haraka.phonetic.has_a_determinate_value",
            subject=Subject.WRITTEN_HARAKA,
            what_is_claimed="للحركة المكتوبة قيمةٌ صوتيّةٌ مُعيَّنةٌ تُختبَر هنا",
            evidence_genus=EvidenceGenus.RECORDED_SOUND,
            what_the_evidence_counts="قطعُ الصوت المُسجَّل المقابلةُ لكلّ حركة",
            preventers=(_NO_RECORDED_SOUND_PREVENTER,),
            residuals=("كمّيّةُ الحركة زمنًا غيرُ مقيسةٍ هنا، والعدُّ ليس زمنًا",),
        ),
        ContractElement(
            element_id="sukun.written.is_an_observed_mark",
            subject=Subject.WRITTEN_SUKUN,
            what_is_claimed="السكونُ المكتوب علامةٌ مرصودةٌ محمولةٌ على محورها",
            evidence_genus=EvidenceGenus.ORTHOGRAPHIC_OBSERVATION,
            what_the_evidence_counts="الوقوعاتُ الحاملةُ علامةَ السكون",
            preventers=(),
            residuals=(
                _A_TRANSCRIPTION_IS_THE_PRODUCERS,
                "العلامةُ محمولةٌ، وحملُها لا يقول ما تفعله في النطق",
            ),
        ),
        ContractElement(
            element_id="sukun.phonetic.is_the_absence_of_a_vowel_sound",
            subject=Subject.WRITTEN_SUKUN,
            what_is_claimed="السكونُ المكتوب غيابُ صوتِ حركةٍ في النطق",
            evidence_genus=EvidenceGenus.RECORDED_SOUND,
            what_the_evidence_counts="قطعُ الصوت المُسجَّل عند مواضع السكون",
            preventers=(_NO_RECORDED_SOUND_PREVENTER,),
            residuals=("تعذُّرُ الاختبار هنا ليس نفيًا للدعوى ولا إثباتًا لها",),
        ),
        ContractElement(
            element_id="absence.is_not_the_written_sukun",
            subject=Subject.ABSENT_DIACRITIC,
            what_is_claimed=(
                "غيابُ التشكيل صنفٌ ثالثٌ غيرُ السكون المكتوب وغيرُ الحركة "
                "المكتوبة، ويُعَدُّ على حدة"
            ),
            evidence_genus=EvidenceGenus.ORTHOGRAPHIC_OBSERVATION,
            what_the_evidence_counts="الوقوعاتُ الخاليةُ من كلّ علامةٍ على المحاور المقيسة",
            preventers=(),
            residuals=(
                "خلوُّ الموضع من علامةٍ قد يكون اختيارَ الناسخ، فلا يُقرَأ حكمًا "
                "لغويًّا على الموضع",
            ),
        ),
    )


def _refuse_a_conflated_subject(elements: tuple[ContractElement, ...]) -> None:
    """ارفض عنصرًا يجمع السكونَ المكتوب وغيابَ التشكيل في موضوعٍ واحد."""

    identifiers = tuple(element.element_id for element in elements)
    if len(set(identifiers)) != len(identifiers):
        raise LetterHarakaContractError("مُعرِّفُ العنصر لا يتكرّر في العقد")
    subjects = {element.subject for element in elements}
    if (
        Subject.WRITTEN_SUKUN not in subjects
        or Subject.ABSENT_DIACRITIC not in subjects
    ):
        raise LetterHarakaContractError(
            "AWrittenSukunIsNotAnAbsentDiacritic: يلزم للموضوعين عنصران متمايزان، "
            "فلا يُطوى أحدهما في الآخر"
        )
    for required in Subject:
        if required not in subjects:
            raise LetterHarakaContractError(f"العقدُ بلا عنصرٍ لموضوع «{required.value}»")


def run_letter_haraka_contract(
    table: ObservedFiberTable | None = None,
) -> LetterHarakaReport:
    """شغِّل العقدَ على إيداعٍ مُبصَّم؛ ولا شيءَ في تشغيله موقوفٌ على شهادة ولادة."""

    measured = run_observed_fiber_on_the_deposited_fatiha() if table is None else table
    elements = build_letter_haraka_contract()
    _refuse_a_conflated_subject(elements)

    written_sukun = count_written_sukun_rows(measured)
    absent_diacritic = count_absent_diacritic_rows(measured)
    if written_sukun == absent_diacritic:
        raise LetterHarakaContractError(
            "AWrittenSukunIsNotAnAbsentDiacritic: تساوى العددان، فلا يُقرَأ "
            "تمايزُ الصنفين من هذا الإيداع"
        )
    if _count_haraka_with_sukun_rows(measured):
        raise LetterHarakaContractError(
            "وقوعٌ يحمل حركةً وسكونًا معًا؛ والعدُّ ههنا يفترض قراءتهما محورين"
        )

    counts: dict[str, int] = {
        "letter.written.is_an_observed_carrier": len(measured.rows),
        "haraka.written.is_an_observed_mark": _count_written_haraka_rows(measured),
        "haraka.written.is_not_the_letter_itself": _count_haraka_with_gemination_rows(
            measured
        ),
        "sukun.written.is_an_observed_mark": written_sukun,
        "absence.is_not_the_written_sukun": absent_diacritic,
    }

    readings: list[ElementReading] = []
    for element in elements:
        if not element.is_reachable_in_this_tree:
            readings.append(
                ElementReading(
                    element=element,
                    standing=ElementStanding.WITHHELD_BY_A_PREVENTER,
                    observed_count=0,
                    withheld_because=element.preventers[0],
                )
            )
            continue
        observed = counts[element.element_id]
        if observed <= 0:
            readings.append(
                ElementReading(
                    element=element,
                    standing=ElementStanding.WITHHELD_BY_A_PREVENTER,
                    observed_count=0,
                    withheld_because=(
                        "لا وقوعَ لهذا العنصر في هذا الإيداع؛ والصفرُ غيابٌ في "
                        "مدوّنةٍ لا نفيٌ في اللغة"
                    ),
                )
            )
            continue
        readings.append(
            ElementReading(
                element=element,
                standing=ElementStanding.HELD_ON_THE_DEPOSIT,
                observed_count=observed,
                withheld_because="",
            )
        )

    return LetterHarakaReport(
        contract_id=LETTER_HARAKA_CONTRACT_ID,
        deposit_sha256=measured.deposit.sha256,
        readings=tuple(readings),
    )


# --- الحدودُ مُسمّاةً -------------------------------------------------------------


A_WRITTEN_LETTER_IS_NOT_A_SOUND_NOTE: Final[str] = (
    "AWrittenLetterIsNotASound: جنسُ الدليل مُعلَنٌ في كلّ عنصر، وعنصرٌ دليلُه "
    "صوتٌ مُسجَّلٌ محجوبٌ في هذه الشجرة بمانعه؛ فلا تُقرَأ منزلةُ المكتوب "
    "منزلةً للمنطوق"
)

A_WRITTEN_SUKUN_IS_NOT_AN_ABSENT_DIACRITIC_NOTE: Final[str] = (
    "AWrittenSukunIsNotAnAbsentDiacritic: السكونُ المكتوب علامةٌ محمولةٌ على "
    "محورها، وغيابُ التشكيل خلوُّ المحاور المقيسة جميعًا؛ موضوعان متمايزان "
    "لا يجمعهما عنصرٌ واحد، وتمايزُهما مقيسٌ من الإيداع لا مفترَض"
)

EVERY_FIGURE_IS_REDERIVED_FROM_THE_DEPOSITED_BYTES_NOTE: Final[str] = (
    "EveryFigureIsRederivedFromTheDepositedBytes: لا رقمَ مكتوبًا باليد في هذا "
    "العقد؛ وكلُّ عددٍ يُشتَقّ عند التشغيل من بايتاتٍ مُبصَّمة، وبصمتُها في المخرَج"
)

RUNNING_THE_CONTRACT_IS_NOT_BLOCKED_ON_A_CERTIFICATE_NOTE: Final[str] = (
    "RunningTheContractIsNotBlockedOnACertificate: تجربةُ هذا العقد غيرُ "
    "موقوفةٍ على صدور شهادة ولادة CV؛ يُشغَّل اليومَ ويُقرأ اليومَ، والشهادةُ "
    "تبقى غيرَ صادرةٍ بنقصها المُعدَّد في fiber_transfer_contracts"
)

THIS_CONTRACT_ISSUES_NO_BIRTH_NOTE: Final[str] = (
    "ThisContractIssuesNoBirth: انعقادُ عنصرٍ منزلةٌ على إيداعٍ بعينه، لا "
    "ولادةً ولا حكمَ ولادةٍ كرنليًّا ولا تجميدَ E0؛ ولا تستورد هذه الوحدةُ "
    "من kernel/ شيئًا"
)

LETTER_HARAKA_NAMED_RESIDUALS: Final[tuple[str, ...]] = (
    A_WRITTEN_LETTER_IS_NOT_A_SOUND_NOTE,
    A_WRITTEN_SUKUN_IS_NOT_AN_ABSENT_DIACRITIC_NOTE,
    EVERY_FIGURE_IS_REDERIVED_FROM_THE_DEPOSITED_BYTES_NOTE,
    RUNNING_THE_CONTRACT_IS_NOT_BLOCKED_ON_A_CERTIFICATE_NOTE,
    THIS_CONTRACT_ISSUES_NO_BIRTH_NOTE,
)
