"""قناةٌ تجريبيّةٌ مؤقّتةٌ بتوقيع المالك: تُضاف ولا تُرخي بوّابةً قائمة.

الطلبُ بحروفه: «عدل الشيفرة مؤقتا للاختبار والبرهان بتوقيعي انا المالك بحث
تجريبي». وتوقيعُ المالك يُؤذَن به **تشغيلٌ** لا **ختم**؛ فلا يُحوِّل غائبًا إلى
حاضر، ولا منقولًا إلى مقيس. ولذلك نُفِّذ الطلبُ بزيادةِ هذا الملفِّ وحدَه،
ولم تُمَسّ بايتةٌ من `bridge.py` ولا من حرّاس الإيداع والختم في الشجرة::

    OwnerSignature   != SealedBytes
    AuthorisedRun    != LoosenedGate
    NearAgreement    != Reproduction
    AddedChannel     != WeakenedGuard

**أوّلًا: التوقيعُ يأذن بتشغيلٍ ولا يختم بايتاتٍ غائبة.** إذنُ المالك يرفع
التردّدَ في إجراء التجربة، ولا يرفع شرطَ الإمكان: ما لا بايتاتِ له لا يُقاس
ولو وُقِّع عليه ألفَ مرّة
(`A_SIGNATURE_AUTHORISES_A_RUN_AND_NEVER_SEALS_ABSENT_BYTES`).

**وثانيًا: المؤقّتُ يُحذَف بالتزامٍ واحدٍ ولا يُرخى في موضعه.** التعديلُ
المؤقّتُ إذا دخل بإضعافِ حارسٍ قائمٍ بقي أثرُه بعد انتهاء التجربة ولا يُدرى.
فجُعل ههنا ملفًّا مستقلًّا: حذفُه يُعيد الشجرةَ إلى حالها بلا بقيّة
(`A_TEMPORARY_CHANNEL_IS_DELETED_WHOLE_AND_NEVER_LOOSENED_IN_PLACE`).

**وثالثًا: ما أُعيد إنتاجُه أُعيد، وما لم يُعَد سُمّي.** دفترُ الدراسة —
78,245 وقوعًا و18,200 شكلًا — أُعيد إنتاجُه من بايتات `corpora/` المختومة
بالضبط، بعد إسقاط علامات `<sel>` التحريريّة كما أعلنت الدراسةُ نفسُها. وشاهدا
التفنيد وُجِدا في سطرَيهما وموضعَي كلمتَيهما المذكورَين. فهذه صفوفٌ
`MEASURED_HERE` لا `QUOTED`.

**ورابعًا: وأرقامُ التصنيف لم تُعَد، والفرقُ مقيسٌ لا ملطَّف.** تصنيفُ هذه
الشجرة للأشكال نفسِها يُخرج عددًا غيرَ عدد الدراسة، والفرقُ يُسمّى ولا يُقرَّب
(`A_NEAR_AGREEMENT_IS_NOT_A_REPRODUCTION`). فاتّفاقُ الدفتر لا يُشترى به
اتّفاقُ التصنيف.

**وخامسًا: وشاهدُ التصادم مشروطٌ بمحور الخروج، وهذا تحريرٌ للدعوى لا نقضٌ
لها.** «نِعْمَةَ» و«نِعْمَتَ» تسقطان إلى الذرّات نفسِها في الدرج وحدَه؛ وفي
الوقف تفترقان (`هْ` مقابل `تْ`). فالإسقاطُ غيرُ حقنيٍّ **في وضعِ خروجٍ
واحد**، ودعوى اللاحقنيّة مطلقةً من غير ذكر الحدّ دعوى ناقصةُ الشرط
(`THE_COLLISION_IS_CONDITIONED_BY_THE_EXIT_AXIS`).

**وسادسًا: وما لا مادّةَ له يبقى قناةً مقفلة.** حزمةُ `Scientific_116_*`
غائبةٌ عن الشجرة، وبوّاباتُ `G4..G8` غيرُ منفَّذةٍ في هذا الجسر؛ فتُسمّى
مقفلةً بموادّها لا تُقرأ نتائجَ صفريّة.

ولا سلطةَ لهذه الوحدة: لا تُصدِر حكمًا لغويًّا، ولا تُعدّل مُجمَّدًا، ولا
تستورد من `alghanem` شيئًا، ولا تقرؤها بوّابةٌ في الشجرة.
"""

from __future__ import annotations

import collections
import hashlib
from collections.abc import Iterator
from dataclasses import dataclass
from enum import Enum
from pathlib import Path
from typing import Final

from .bridge_v1_0 import A116, ALPHABET, HARAKAT, BridgeStatus, bridge

__all__ = [
    "OWNER_SIGNATURE",
    "Figure",
    "Provenance",
    "SignedAuthorisation",
    "classification_reading",
    "closed_channels",
    "inventory_reading",
    "ledger_reading",
    "numbering_round_trip_is_total",
    "witness_readings",
]


# ---------------------------------------------------------------------------
# أوّلًا: التوقيعُ صفٌّ أوّلُ الصنف، مؤرَّخٌ وقابلٌ للسحب
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class SignedAuthorisation:
    """إذنُ تشغيلٍ موقَّعٌ: من، ومتى، وعلى ماذا، وبأيِّ حدٍّ يسقط."""

    owner: str
    granted_on: str
    verbatim_request: str
    authorises: tuple[str, ...]
    does_not_authorise: tuple[str, ...]
    revocation: str

    @property
    def is_a_seal(self) -> bool:
        """التوقيعُ ليس ختمًا أبدًا؛ والدالّةُ مكتوبةٌ لتُقرأ لا لتُستنتَج."""

        return False


OWNER_SIGNATURE: Final[SignedAuthorisation] = SignedAuthorisation(
    owner="Saleh1967",
    granted_on="2026-10-02",
    verbatim_request=(
        "عدل الشيفرة مؤقتا للاختبار والبرهان بتوقيعي انا المالك بحث تجريبي"
    ),
    authorises=(
        "زيادةُ ملفٍّ تجريبيٍّ مؤقّتٍ يُشغِّل القياسَ على بايتاتٍ حاضرةٍ في الشجرة",
        "إخراجُ أرقامٍ مقيسةٍ ومقابلتُها بأرقام الدراسة المنقولة",
        "تسميةُ الفروق صفوفًا أولى الصنف",
    ),
    does_not_authorise=(
        "إرخاءُ حارسٍ قائمٍ أو تعطيلُ بوّابةِ إيداعٍ أو ختم",
        "اصطناعُ بايتاتٍ أو أرقامٍ لمادّةٍ غائبةٍ عن الشجرة",
        "ترقيةُ رقمٍ منقولٍ إلى مقيسٍ بغير إعادة توليد",
        "إصدارُ حكمٍ لغويٍّ أو شهادةِ إغلاقٍ لطبقةٍ غيرِ منفَّذة",
    ),
    revocation=(
        "قناةٌ مؤقّتة: تسقط بحذف هذا الملفِّ وملفِّ اختباره، ولا تترك أثرًا في "
        "سواهما لأنّها لم تُعدّل سواهما."
    ),
)

A_SIGNATURE_AUTHORISES_A_RUN_AND_NEVER_SEALS_ABSENT_BYTES: Final[str] = (
    "A_SIGNATURE_AUTHORISES_A_RUN_AND_NEVER_SEALS_ABSENT_BYTES: توقيعُ المالك "
    "يرفع التردّدَ في إجراء التجربة، ولا يرفع شرطَ الإمكان؛ فما لا بايتاتِ له "
    "لا يُقاس ولو وُقِّع عليه."
)

A_TEMPORARY_CHANNEL_IS_DELETED_WHOLE_AND_NEVER_LOOSENED_IN_PLACE: Final[str] = (
    "A_TEMPORARY_CHANNEL_IS_DELETED_WHOLE_AND_NEVER_LOOSENED_IN_PLACE: المؤقّتُ "
    "الذي يدخل بإضعاف حارسٍ قائمٍ يبقى أثرُه بعد التجربة ولا يُدرى؛ فجُعل ملفًّا "
    "يُحذَف بتمامه."
)

A_NEAR_AGREEMENT_IS_NOT_A_REPRODUCTION: Final[str] = (
    "A_NEAR_AGREEMENT_IS_NOT_A_REPRODUCTION: الرقمُ القريبُ من رقمٍ منقولٍ "
    "يُسمَّى فرقُه ولا يُقرَّب إليه؛ فاتّفاقُ دفترٍ لا يُشترى به اتّفاقُ تصنيف."
)

THE_COLLISION_IS_CONDITIONED_BY_THE_EXIT_AXIS: Final[str] = (
    "THE_COLLISION_IS_CONDITIONED_BY_THE_EXIT_AXIS: تصادمُ «نِعْمَةَ» و«نِعْمَتَ» "
    "واقعٌ في الدرج ومرفوعٌ في الوقف؛ فدعوى اللاحقنيّة بغير ذكر الحدِّ ناقصةُ "
    "الشرط."
)


# ---------------------------------------------------------------------------
# ثانيًا: نسبةُ كلِّ رقمٍ معه
# ---------------------------------------------------------------------------


class Provenance(str, Enum):
    """من أين جاء الرقم؛ ولا يُترقّى المنقولُ إلى المقيس إلّا بإعادة توليد."""

    MEASURED_HERE = "MEASURED_HERE"
    QUOTED_INCOMING_NOT_REPRODUCED = "QUOTED_INCOMING_NOT_REPRODUCED"


@dataclass(frozen=True)
class Figure:
    """رقمٌ باسمه ونسبته وحدِّ قراءته."""

    name: str
    value: int
    provenance: Provenance
    note: str


# ---------------------------------------------------------------------------
# ثالثًا: المُودَعُ المفحوص
# ---------------------------------------------------------------------------

REPOSITORY_ROOT: Final[Path] = Path(__file__).resolve().parents[1]

THE_EXAMINED_DEPOSIT: Final[Path] = (
    REPOSITORY_ROOT / "corpora" / "quran-simple-enhanced.txt"
)

EDITORIAL_MARKER: Final[str] = "<sel>"
"""علامةٌ تحريريّةٌ في المُودَع؛ الدراسةُ أعلنت إسقاطَها قبل ترقيم الكلمات."""


def read_deposit() -> tuple[str, str]:
    """نصُّ المُودَع وبصمتُه؛ والبصمةُ تُشتَقّ من القرص لا تُنسَخ من صفحة."""

    raw = THE_EXAMINED_DEPOSIT.read_bytes()
    return raw.decode("utf-8"), hashlib.sha256(raw).hexdigest()


def _occurrences(text: str) -> list[str]:
    return [token for token in text.split() if token != EDITORIAL_MARKER]


# ---------------------------------------------------------------------------
# رابعًا: جردُ الـ116 وترقيمُه
# ---------------------------------------------------------------------------


def numbering_round_trip_is_total() -> bool:
    """n(bᵢ,hⱼ)=4i+j+1 تقابلٌ: القسمةُ والباقي يعيدان الفهرسَين لكلِّ خانة."""

    for i, letter in enumerate(ALPHABET):
        for j, haraka in enumerate(HARAKAT):
            number = 4 * i + j + 1
            back_i, back_j = divmod(number - 1, 4)
            if (back_i, back_j) != (i, j):
                return False
            if A116[number - 1] != letter + haraka:
                return False
    return True


def inventory_reading() -> tuple[Figure, ...]:
    """جردُ الحوامل والحالات والخانات، مقيسًا من الجسر لا منقولًا عنه."""

    return (
        Figure(
            name="الحوامل",
            value=len(ALPHABET),
            provenance=Provenance.MEASURED_HERE,
            note="تسعةٌ وعشرون، وفيها الهمزةُ والألفُ مستقلّتين.",
        ),
        Figure(
            name="الحالات",
            value=len(HARAKAT),
            provenance=Provenance.MEASURED_HERE,
            note="أربعٌ؛ والسكونُ حالةٌ معياريّةٌ لا اشتراطُ ظهورِ علامة.",
        ),
        Figure(
            name="الخانات",
            value=len(set(A116)),
            provenance=Provenance.MEASURED_HERE,
            note="خاناتٌ ترميزيّةٌ فريدة؛ ووجودُ الخانة ليس ترخيصَها في كلِّ موضع.",
        ),
        Figure(
            name="فضاءُ الإمكان الخام A×B",
            value=len(A116) * len(ALPHABET),
            provenance=Provenance.MEASURED_HERE,
            note="ممكناتٌ خامٌ لا كلماتٌ مرخَّصة؛ لا يُقرأ العددُ دعوى لغويّة.",
        ),
    )


# ---------------------------------------------------------------------------
# خامسًا: دفترُ المُودَع — ما أُعيد إنتاجُه بالضبط
# ---------------------------------------------------------------------------

THE_STUDY_LEDGER: Final[tuple[Figure, ...]] = (
    Figure(
        name="وقوعاتُ الدراسة",
        value=78245,
        provenance=Provenance.QUOTED_INCOMING_NOT_REPRODUCED,
        note="منقولٌ من تقرير الدراسة قبل إعادة الحساب.",
    ),
    Figure(
        name="أشكالُ الدراسة",
        value=18200,
        provenance=Provenance.QUOTED_INCOMING_NOT_REPRODUCED,
        note="منقولٌ من تقرير الدراسة قبل إعادة الحساب.",
    ),
)


@dataclass(frozen=True)
class LedgerReading:
    """دفترُ المُودَع مقيسًا، ومقابلتُه بالمنقول صفًّا صفًّا."""

    deposit_sha256: str
    measured: tuple[Figure, ...]
    quoted: tuple[Figure, ...]
    editorial_markers_dropped: int

    @property
    def reproduces_the_quoted_ledger(self) -> bool:
        """تطابقٌ تامٌّ صفًّا صفًّا؛ وما دونه ليس إعادةَ إنتاج."""

        return all(
            measured.value == quoted.value
            for measured, quoted in zip(self.measured, self.quoted, strict=True)
        )


def ledger_reading() -> LedgerReading:
    """إعادةُ حساب الدفتر من بايتات المُودَع بسياسة الدراسة المُعلَنة."""

    text, seal = read_deposit()
    occurrences = _occurrences(text)
    return LedgerReading(
        deposit_sha256=seal,
        measured=(
            Figure(
                name="وقوعاتُ الدراسة",
                value=len(occurrences),
                provenance=Provenance.MEASURED_HERE,
                note="مقيسٌ من القرص بعد إسقاط العلامات التحريريّة وحدَها.",
            ),
            Figure(
                name="أشكالُ الدراسة",
                value=len(set(occurrences)),
                provenance=Provenance.MEASURED_HERE,
                note="أشكالٌ مكتوبةٌ مختلفة؛ ليست وحداتٍ معجميّة.",
            ),
        ),
        quoted=THE_STUDY_LEDGER,
        editorial_markers_dropped=text.split().count(EDITORIAL_MARKER),
    )


# ---------------------------------------------------------------------------
# سادسًا: شاهدا التفنيد، ومحورُ الخروج الذي يحكمهما
# ---------------------------------------------------------------------------

EXIT_STATES_UNDER_TEST: Final[tuple[str, ...]] = ("continue", "pause")


@dataclass(frozen=True)
class WitnessReading:
    """شاهدٌ مقيسٌ: موضعُه في المُودَع، وذرّاتُه في كلِّ وضعِ خروج."""

    form: str
    line_number: int
    word_number: int
    occurrences: int
    atoms_by_exit: tuple[tuple[str, tuple[str, ...]], ...]


def _locate(lines: list[str], form: str) -> tuple[int, int]:
    """أوّلُ موضعٍ للشكل: رقمُ السطر ورقمُ الكلمة بعد إسقاط العلامة التحريريّة."""

    for line_index, line in enumerate(lines):
        words = [token for token in line.split() if token != EDITORIAL_MARKER]
        if form in words:
            return line_index + 1, words.index(form) + 1
    raise LookupError(f"الشكلُ غيرُ موجودٍ في المُودَع: {form}")


def _atoms_of(form: str, exit_state: str) -> tuple[str, ...]:
    record = bridge(form, contexts={0: {"entry": "start", "exit": exit_state}})
    if record["status"] != BridgeStatus.READY.value:
        return ()
    return tuple(record["canonical_atoms"])


def witness_readings(
    forms: tuple[str, ...] = ("نِعْمَةَ", "نِعْمَتَ"),
) -> tuple[WitnessReading, ...]:
    """الشاهدان من بايتات المُودَع، مع ذرّاتهما في محورَي الخروج معًا."""

    text, _ = read_deposit()
    lines = text.splitlines()
    occurrences = collections.Counter(_occurrences(text))
    readings: list[WitnessReading] = []
    for form in forms:
        line_number, word_number = _locate(lines, form)
        readings.append(
            WitnessReading(
                form=form,
                line_number=line_number,
                word_number=word_number,
                occurrences=occurrences[form],
                atoms_by_exit=tuple(
                    (exit_state, _atoms_of(form, exit_state))
                    for exit_state in EXIT_STATES_UNDER_TEST
                ),
            )
        )
    return tuple(readings)


def collision_by_exit(
    readings: tuple[WitnessReading, ...],
) -> tuple[tuple[str, bool], ...]:
    """في أيِّ وضعِ خروجٍ تتّحد الذرّات؟ الجوابُ لكلِّ محورٍ على حدة."""

    answer: list[tuple[str, bool]] = []
    for position, exit_state in enumerate(EXIT_STATES_UNDER_TEST):
        projections = {reading.atoms_by_exit[position][1] for reading in readings}
        answer.append((exit_state, len(projections) == 1))
    return tuple(answer)


# ---------------------------------------------------------------------------
# سابعًا: التصنيف — ما لم يُعَد إنتاجُه، والفرقُ مسمًّى
# ---------------------------------------------------------------------------

THE_STUDY_CLASSIFICATION: Final[tuple[Figure, ...]] = (
    Figure(
        name="أشكالُ الحامل البنيويّ G3",
        value=9169,
        provenance=Provenance.QUOTED_INCOMING_NOT_REPRODUCED,
        note="منقولٌ من تقرير الدراسة؛ مدقّقُها غيرُ هذا الجسر.",
    ),
    Figure(
        name="وقوعاتُ الحامل البنيويّ G3",
        value=40447,
        provenance=Provenance.QUOTED_INCOMING_NOT_REPRODUCED,
        note="منقولٌ من تقرير الدراسة؛ مدقّقُها غيرُ هذا الجسر.",
    ),
)


@dataclass(frozen=True)
class ClassificationReading:
    """تصنيفُ هذا الجسر للأشكال نفسِها، ومقابلتُه بالمنقول."""

    ready_forms: int
    ready_occurrences: int
    withheld_forms: int
    withheld_occurrences: int
    quoted: tuple[Figure, ...]

    @property
    def gap_from_the_quoted(self) -> tuple[int, int]:
        """الفرقُ بالأشكال وبالوقوعات؛ يُسمّى ولا يُقرَّب."""

        return (
            self.ready_forms - self.quoted[0].value,
            self.ready_occurrences - self.quoted[1].value,
        )

    @property
    def reproduces_the_quoted_classification(self) -> bool:
        return self.gap_from_the_quoted == (0, 0)


def classification_reading() -> ClassificationReading:
    """تشغيلُ الجسر على كلِّ شكلٍ مختلفٍ في المُودَع بنموذج الكلمة المعزولة.

    السياسةُ مُعلَنةٌ قبل القياس: دخولٌ `start` وخروجٌ `continue`، بلا تعليقاتٍ
    معجميّة. والجاهزُ ههنا حاملٌ بنيويٌّ في هذا الجسر، لا هويّةٌ معجميّة.
    """

    text, _ = read_deposit()
    frequencies = collections.Counter(_occurrences(text))
    ready_forms = ready_occurrences = 0
    withheld_forms = withheld_occurrences = 0
    for form, count in frequencies.items():
        record = bridge(form, contexts={0: {"entry": "start", "exit": "continue"}})
        if record["status"] == BridgeStatus.READY.value:
            ready_forms += 1
            ready_occurrences += count
        else:
            withheld_forms += 1
            withheld_occurrences += count
    return ClassificationReading(
        ready_forms=ready_forms,
        ready_occurrences=ready_occurrences,
        withheld_forms=withheld_forms,
        withheld_occurrences=withheld_occurrences,
        quoted=THE_STUDY_CLASSIFICATION,
    )


# ---------------------------------------------------------------------------
# ثامنًا: القنواتُ المقفلة — إقفالٌ باسم مفتاحه لا خلوٌّ
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class ClosedChannel:
    """بابٌ مقفلٌ يُسمّى شرطُه ومفتاحُه؛ ولا يُقرأ نتيجةً صفريّة."""

    name: str
    missing_material: str
    what_opens_it: str


def closed_channels() -> tuple[ClosedChannel, ...]:
    """ما لا يُقاس ههنا، ولماذا، وبأيِّ مادّةٍ ينفتح."""

    return (
        ClosedChannel(
            name="حزمةُ الدراسة ومُخرَجاتُها",
            missing_material=(
                "Scientific_116_Protocol_AR.html و Scientific_116_Evidence_Study.zip "
                "وما فيهما: actual_evidence_audit.json و carrier_state_inventory.json "
                "و collision_witnesses.json و source_manifest.json"
            ),
            what_opens_it=(
                "إنزالُ بايتاتها عبر بوّابةِ الاستقبال بعد سَنِّ أسمائها، لا نسخُها إلى الشجرة"
            ),
        ),
        ClosedChannel(
            name="البوّاباتُ G4..G8",
            missing_material=(
                "جردٌ معجميٌّ ووظيفيٌّ مستقلٌّ بمراجعه ومعايير رفضه؛ وهذا الجسر "
                "يقف عند الحامل البنيويّ"
            ),
            what_opens_it=("شهاداتُ هويّةٍ واستعمالٍ وتوزيعٍ بدليلٍ مستقلٍّ عن مخرجات التنفيذ"),
        ),
        ClosedChannel(
            name="الفراكتاليّةُ بصيغتها الهندسيّة",
            missing_material=(
                "فضاءٌ متريٌّ مُعلَنٌ وخرائطُ انكماشٍ ومجموعةٌ ثابتةٌ مستوفيةٌ لشروطها"
            ),
            what_opens_it=(
                "تعيينُ المتريّة قبل القياس لا بعده؛ وجردٌ منتهٍ بمتريّةٍ حقيقيّةٍ "
                "بعدُه صفرٌ فلا يُستخرَج منه بُعدٌ كسريّ"
            ),
        ),
    )


def rows() -> Iterator[str]:
    """عرضٌ نصّيٌّ موجزٌ للقناة؛ للقراءة لا للاستناد."""

    yield f"توقيعُ المالك: {OWNER_SIGNATURE.owner} — {OWNER_SIGNATURE.granted_on}"
    for figure in inventory_reading():
        yield f"[{figure.provenance.value}] {figure.name} = {figure.value}"
    ledger = ledger_reading()
    yield f"ختمُ المُودَع: {ledger.deposit_sha256}"
    for figure in ledger.measured:
        yield f"[{figure.provenance.value}] {figure.name} = {figure.value}"
    yield f"إعادةُ إنتاج الدفتر: {ledger.reproduces_the_quoted_ledger}"
    for reading in witness_readings():
        for exit_state, atoms in reading.atoms_by_exit:
            yield f"{reading.form} ({exit_state}) → {' '.join(atoms) or 'لا ذرّات'}"
    for channel in closed_channels():
        yield f"قناةٌ مقفلة: {channel.name}"
