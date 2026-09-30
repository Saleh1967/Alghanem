"""قارئُ سجلّ مختبر الاكتشاف: تسجيلٌ مسبقٌ مسلسلُ البصمات، ثمّ جولةٌ تُصادَم.

بُني في `discovery_lab` بروتوكولُ جولةٍ واحدةٍ عديمُ الذاكرة: يقترح تفسيرَين،
ويعدّ ما يفترقان عليه، ويُخرِج ما ثبت وما سقط وما بقي معلَّقًا. وكان مانعُ
درجته الثانية والثالثة مقيسًا: قواعدُه مكتوبةٌ في بايتاته، ولا سجلَّ جولاتٍ
يقرؤه. وهذه الوحدةُ تُودِع السجلَّ وتقرؤه، وتُسمّي ما لا يبلغه::

    Chain          != Time
    PreRegistration!= Report
    LiteralCount   != Meaning
    Deposited      != Cumulative

**أوّلًا: التسجيلُ المسبقُ عقدٌ لا وصف.** كلُّ جولةٍ تستشهد ببندِ تسجيلٍ
سابقٍ في السلسلة، وفي البند: المسألةُ بنصّها، والفرضان المتنافسان، والمقياسُ
الذي يفصل بينهما بحدِّه، وحدُّ النجاح لكلّ فرض، وخَتمُ المادّة قبل قراءتها،
وضوابطُ سمعِ المسطرة، والألفاظُ القريبةُ التي تُعَدّ ولا تُحسَب وجدانًا،
والحدودُ المُعلَنة. وبندُ تسجيلٍ يحمل نتيجتَه **ليس تسجيلًا مسبقًا بل تقريرًا**،
ويُكشَف ذلك بحقولِه لا بحسن الظنّ
(`A_PRE_REGISTRATION_THAT_NAMES_ITS_RESULT_IS_A_REPORT`).

**وثانيًا: والسلسلةُ تحرس الترتيب ولا تحرس الزمن.** بصمةُ كلّ حلقةٍ تضمّ
بصمةَ سالفتها، فمن بدَّل بندًا أو أقحم واحدًا في الوسط انقطعت البصماتُ بعده.
لكنّ الختمَ الزمنيَّ حقلٌ مكتوب، ولا يشهد ملفٌّ لنفسه بزمن كتابته: فسَبقُ
التسجيل على القياس **لا يُبرهَن من داخل هذه الشجرة**، وشاهدُه خارجَها تاريخُ
الإيداع في git. وهذا عينُ ما تقرّر في `exhibits/tawlid-algebra`
(`THE_CHAIN_GUARDS_ORDER_AND_NOT_TIME`).

**وثالثًا: والجولةُ تُعاد لا تُقرأ.** ما في السجلّ من عددٍ لا يُصدَّق لأنّه
مكتوب: تُلتمَس المادّةُ بختمها، فإن خالف الختمُ رُدَّت الجولةُ؛ فإن طابق
أُعيد العدُّ بالوصفة المسجَّلة وقوبِل بالمكتوب. فالسجلُّ يُصادَم ولا يُنقَل
(`A_RECORDED_COUNT_IS_RE_RUN_AND_NOT_BELIEVED`).

**ورابعًا: وصفرٌ على آلةٍ صمّاء لا يُثبِت شيئًا.** نفيُ لفظٍ في مستخرَجٍ خشنٍ
عدمُ وجدانٍ قد يكون عدمَ قراءة، كما سُمِّي في `dal_alone_bridge` بـ
`A_CRUDE_EXTRACTION_BIASES_A_NEGATIVE_TOWARD_ITSELF`. فلا يُقرأ صفرٌ حتّى
تجتاز المسطرةُ ضوابطَ سمعٍ **مُسجَّلةً قبل العدّ**: ألفاظٌ يُشترَط وجدانُها
بحدٍّ أدنى، وكمُّ عربيّةٍ مستخرَجةٍ بحدٍّ أدنى. فإن سقط ضابطٌ منها فالصفرُ
صفرُ آلةٍ لا صفرُ نصّ (`A_ZERO_ON_A_DEAF_INSTRUMENT_IS_NOT_A_FINDING`).

**وخامسًا: والعدُّ الحرفيُّ يُسقِط اللفظَ لا المعنى.** في مادّة الجولة
الأولى عدُّ «ذكاء» صفرٌ، وعدُّ «ذكي» ثلاثٌ. فمن قرأ الصفرَ «الكتابُ لا
يتكلّم في الذكاء أصلًا» عدّى الحكمَ من اللفظ إلى المعنى بلا مادّة. والقريبُ
يُسمّى بعدده ويُخرَج في المعلَّق، ولا يُطوى ليُقوَّى به النفي
(`A_LITERAL_COUNT_FALLS_ON_THE_LAFZ_NOT_ON_THE_MEANING`).

**وسادسًا: وشِقٌّ لم يُقَس لا يسقط بسقوط قرينه.** الفرضُ الثاني في الجولة
الأولى شِقّان: أن يرد اللفظُ، وأن يفرّق الكتابُ بينه وبين العقل والتفكير.
والمقياسُ المسجَّلُ عدٌّ، وهو يفصل في الشقّ الأوّل وحدَه؛ فالثاني **بقي
معلَّقًا** ولم يسقط. ومن أدرجه في الساقط حسب للاختبار ما لم يفعله
(`AN_UNMEASURED_CONJUNCT_STAYS_PENDING_AND_DOES_NOT_FALL_WITH_ITS_MATE`).

**وسابعًا: والجولةُ الاستعراضيّةُ موسومةٌ لا ممحوّة.** في السجلّ جولةٌ
سابقةٌ وسمُها `استعراض`: تجري ولا تُحتسَب في درجةٍ لأنّها بلا تسجيلٍ مسبق.
فمحوُها تحسينُ سجلٍّ بحذف ما ينقضه، وإدراجُها في المحتسَب تسامحٌ؛ والوسمُ
يقطع الأمرين (`A_DEMO_RUN_IS_TAGGED_AND_KEPT_NOT_ERASED`).

**وثامنًا: والدرجاتُ تُقاس من السجلّ لا من حسن الظنّ.** الأولى بلغتها جولةٌ
مسجَّلةٌ مُعادةٌ سُمِعت مسطرتُها. والثانيةُ ممنوعةٌ: لا بندَ يستخرج قاعدةً
ويتحقّق منها على مادّةٍ ثانيةٍ بختمٍ مختلف. والثالثةُ ممنوعةٌ: لا جولةَ
تستشهد بجولةٍ سابقة، وإيداعُ السجلّ وحدَه ليس تراكمًا. والرابعةُ ممنوعةٌ:
مجالاتُ الجولات المحتسَبة مجالٌ واحد، وهي تُعَدّ من حقل المجال في البند لا
تُقدَّر (`A_RUNG_IS_MEASURED_FROM_THE_LEDGER_NOT_PRESUMED`).

**وما تقيسه هذه الوحدةُ بايتاتُ حاويةٍ لا عربيّةُ مدوّنة.** المادّةُ مستندٌ
مُركَّبٌ يُستخرَج منه نصٌّ خشن، وأعدادُه أعدادُ ذلك المستخرَج؛ فلا يُضاف
عددٌ منها إلى عددٍ من أعداد المدوّنات، ولا يُبنى عليه حكمٌ في العربيّة.

**خمولٌ سلطويّ**: لا ولادةَ ههنا ولا حكمَ ولادةٍ ولا تجميدَ `E0`، ولا
استيرادَ من `kernel/`، ولا تُرفَع بهذه الوحدة منزلةٌ محجوزة، ولا تكتب هذه
الوحدةُ في السجلّ شيئًا — تقرؤه وتُصادِمه.
"""

from __future__ import annotations

import json
import re
import unicodedata
from dataclasses import dataclass
from enum import Enum
from hashlib import sha256
from pathlib import Path
from typing import Any, Final

__all__ = [
    "A_DEMO_RUN_IS_TAGGED_AND_KEPT_NOT_ERASED",
    "A_LITERAL_COUNT_FALLS_ON_THE_LAFZ_NOT_ON_THE_MEANING",
    "A_PRE_REGISTRATION_THAT_NAMES_ITS_RESULT_IS_A_REPORT",
    "A_RECORDED_COUNT_IS_RE_RUN_AND_NOT_BELIEVED",
    "A_RUNG_IS_MEASURED_FROM_THE_LEDGER_NOT_PRESUMED",
    "AN_UNMEASURED_CONJUNCT_STAYS_PENDING_AND_DOES_NOT_FALL_WITH_ITS_MATE",
    "A_ZERO_ON_A_DEAF_INSTRUMENT_IS_NOT_A_FINDING",
    "THE_CHAIN_GUARDS_ORDER_AND_NOT_TIME",
    "THE_DEMO_TAG",
    "THE_LEDGER_RELATIVE_PATH",
    "THE_RESULT_BEARING_FIELDS",
    "THE_ROOT_DIGEST",
    "ControlReading",
    "Entry",
    "EntryKind",
    "LedgerError",
    "MaterialSeal",
    "RunAudit",
    "RunStanding",
    "audit_of",
    "chain_breaks",
    "counted_runs",
    "demo_runs",
    "entry_by_id",
    "ledger_path",
    "link_digest",
    "payload_digest",
    "read_ledger",
    "registrations_naming_their_outcome",
    "rung_standing",
]


class LedgerError(ValueError):
    """رُفض سجلٌّ أو بندٌ خارج ما تقبله هذه القراءة؛ ولا يُحمَل على أقربه."""


A_PRE_REGISTRATION_THAT_NAMES_ITS_RESULT_IS_A_REPORT: Final[str] = (
    "بندُ تسجيلٍ مسبقٍ يحمل حقلَ نتيجةٍ أو حكمٍ تقريرٌ لا تسجيل، ولا يُعتَدّ "
    "به سبقًا. ويُكشَف ذلك بحقوله المُسمّاة في THE_RESULT_BEARING_FIELDS، "
    "لا بحسن الظنّ بكاتبه."
)

THE_CHAIN_GUARDS_ORDER_AND_NOT_TIME: Final[str] = (
    "بصمةُ الحلقة تضمّ بصمةَ سالفتها، فالترتيبُ محروسٌ والإقحامُ مكشوف. "
    "وأمّا الختمُ الزمنيُّ فحقلٌ مكتوبٌ لا يشهد الملفُّ به لنفسه؛ فسَبقُ "
    "التسجيل على القياس لا يُبرهَن من داخل الشجرة، وشاهدُه تاريخُ git."
)

A_RECORDED_COUNT_IS_RE_RUN_AND_NOT_BELIEVED: Final[str] = (
    "عددٌ مكتوبٌ في السجلّ لا يُصدَّق لكونه مكتوبًا: يُلتمَس ختمُ المادّة "
    "فيُقابَل، ثمّ يُعاد العدُّ بالوصفة المسجَّلة ويُقابَل المكتوبُ بالمُعاد. "
    "فإن نزاح سقطت الجولةُ ولم تمضِ صامتة."
)

A_ZERO_ON_A_DEAF_INSTRUMENT_IS_NOT_A_FINDING: Final[str] = (
    "نفيٌ في مستخرَجٍ خشنٍ قد يكون عدمَ قراءةٍ لا عدمَ وجود. فلا يُقرأ صفرٌ "
    "حتّى تجتاز المسطرةُ ضوابطَ سمعٍ مسجَّلةً قبل العدّ؛ وسقوطُ ضابطٍ منها "
    "يجعل الصفرَ صفرَ آلةٍ لا صفرَ نصّ."
)

A_LITERAL_COUNT_FALLS_ON_THE_LAFZ_NOT_ON_THE_MEANING: Final[str] = (
    "العدُّ الحرفيُّ يمسك صورةً واحدةً من صور اللفظ: لا تصاريفَ ولا "
    "مرادفات. فسقوطُ «ذكاء» سقوطُ لفظٍ، و«ذكي» حاضرةٌ ثلاثًا في المادّة "
    "نفسِها؛ ومن عمّم الصفرَ على المعنى ادّعى ما لم يُقَس."
)

AN_UNMEASURED_CONJUNCT_STAYS_PENDING_AND_DOES_NOT_FALL_WITH_ITS_MATE: Final[str] = (
    "فرضٌ ذو شِقَّين لا يسقط شِقُّه الثاني بسقوط الأوّل إلّا بمقياسٍ يمسّه. "
    "والعدُّ يفصل في الورود ولا يفصل في التفريق بين المعاني، فالتفريقُ "
    "معلَّقٌ يُعَدُّ في المعلَّق لا في الساقط."
)

A_DEMO_RUN_IS_TAGGED_AND_KEPT_NOT_ERASED: Final[str] = (
    "جولةٌ جرت بلا تسجيلٍ مسبقٍ تبقى في السجلّ موسومةً «استعراض»: لا "
    "تُحتسَب في درجةٍ ولا تُمحى. فمحوُها تحسينُ سجلٍّ بحذف ما ينقضه، "
    "وإدراجُها في المحتسَب تسامحٌ بشرطٍ مُعلَن."
)

A_RUNG_IS_MEASURED_FROM_THE_LEDGER_NOT_PRESUMED: Final[str] = (
    "منزلةُ كلّ درجةٍ تُشتَقّ من بنود السجلّ عند القراءة: أثَمّ جولةٌ "
    "مسجَّلةٌ أُعيدت وسُمِعت مسطرتُها؟ أثَمّ قاعدةٌ مستخرَجةٌ قوبِلت بمادّةٍ "
    "ثانيةٍ بختمٍ مختلف؟ أثَمّ جولةٌ تستشهد بسابقة؟ كم مجالًا في المحتسَب؟"
)


THE_LEDGER_RELATIVE_PATH: Final[str] = "exhibits/discovery-lab/ledger.json"
"""موضعُ السجلّ المُودَع؛ وهو عينُ ما يلتمسه `discovery_lab` في درجته الثالثة."""

THE_ROOT_DIGEST: Final[str] = "0" * 64
"""بصمةُ سلفِ الحلقة الأولى؛ على منوال سجلّ الجبر المولِّد."""

THE_DEMO_TAG: Final[str] = "استعراض"
"""وسمُ الجولة التي لا تُحتسَب في درجةٍ ولا تُمحى من السجلّ."""

THE_RESULT_BEARING_FIELDS: Final[tuple[str, ...]] = (
    "النتيجة",
    "الحكم",
    "العدّ",
    "ما_ثبت",
    "ما_سقط",
)
"""حقولٌ لو وقعت في بندِ تسجيلٍ مسبقٍ صيّرته تقريرًا؛ تُلتمَس في حمولته."""


class EntryKind(Enum):
    """جنسُ البند في السجلّ؛ اثنان لا ثالثَ لهما ههنا."""

    PRE_REGISTRATION = "تسجيلٌ_مسبق"
    RUN = "جولة"


def _canonical(payload: Any) -> str:
    """صيغةُ الحمولة المعياريّة؛ هي عينُها في سجلّ الجبر المولِّد."""

    return json.dumps(
        payload, ensure_ascii=False, sort_keys=True, separators=(",", ":")
    )


def payload_digest(payload: Any) -> str:
    """بصمةُ الحمولة وحدَها، مشتقّةً من صيغتها المعياريّة."""

    return sha256(_canonical(payload).encode("utf-8")).hexdigest()


def link_digest(
    previous: str, stamp: str, entry_id: str, kind: str, payload: Any
) -> str:
    """بصمةُ الحلقة: سلفُها وختمُها الزمنيّ واسمُها وجنسُها وحمولتُها."""

    material = "|".join((previous, stamp, entry_id, kind, _canonical(payload)))
    return sha256(material.encode("utf-8")).hexdigest()


@dataclass(frozen=True)
class Entry:
    """حلقةٌ واحدةٌ من السجلّ، مقروءةٌ لا مُنشَأةٌ ههنا."""

    rank: int
    entry_id: str
    kind: EntryKind
    stamp: str
    domain: str
    tag: str
    cites: tuple[str, ...]
    payload: dict[str, Any]
    previous: str
    digest: str

    @property
    def is_demo(self) -> bool:
        return self.tag == THE_DEMO_TAG

    @property
    def recomputed_digest(self) -> str:
        return link_digest(
            self.previous, self.stamp, self.entry_id, self.kind.value, self.payload
        )


def _repository_root() -> Path:
    return Path(__file__).resolve().parents[3]


def ledger_path() -> Path:
    """موضعُ بايتات السجلّ على القرص؛ وغيابُها رفضٌ مُسمًّى لا فراغٌ صامت."""

    return _repository_root() / THE_LEDGER_RELATIVE_PATH


def read_ledger() -> tuple[Entry, ...]:
    """يقرأ الحلقاتِ بترتيبها؛ وحلقةٌ ناقصةُ حقلٍ رفضٌ لا تخمين."""

    path = ledger_path()
    if not path.is_file():
        raise LedgerError(f"سجلُّ المختبر غائبٌ عن {THE_LEDGER_RELATIVE_PATH}.")
    document = json.loads(path.read_text(encoding="utf-8"))
    entries: list[Entry] = []
    for rank, link in enumerate(document["الحلقات"]):
        try:
            kind = EntryKind(link["الصنف"])
        except ValueError as error:
            raise LedgerError(f"جنسٌ غيرُ معروفٍ في الحلقة {rank}.") from error
        if link["الرتبة"] != rank:
            raise LedgerError(f"رتبةٌ مكتوبةٌ تخالف موضعَها: {link['الرتبة']} ≠ {rank}.")
        entries.append(
            Entry(
                rank=rank,
                entry_id=link["المعرّف"],
                kind=kind,
                stamp=link["الختم_الزمني"],
                domain=link["المجال"],
                tag=link["الوسم"],
                cites=tuple(link["يستشهد_بـ"]),
                payload=link["الحمولة"],
                previous=link["بصمة_السلف"],
                digest=link["بصمة_الحلقة"],
            )
        )
    if not entries:
        raise LedgerError("سجلٌّ بلا حلقةٍ واحدةٍ ليس سجلًّا.")
    return tuple(entries)


def chain_breaks() -> tuple[int, ...]:
    """رتبُ الحلقات التي انقطعت عندها السلسلة؛ والمُنتظَرُ ألّا تكون."""

    broken: list[int] = []
    expected_previous = THE_ROOT_DIGEST
    for entry in read_ledger():
        if entry.previous != expected_previous or entry.digest != (
            entry.recomputed_digest
        ):
            broken.append(entry.rank)
        expected_previous = entry.digest
    return tuple(broken)


def entry_by_id(entry_id: str) -> Entry:
    """حلقةٌ بمعرّفها؛ وغيابُها رفضٌ لا حملٌ على أقرب معرّف."""

    for entry in read_ledger():
        if entry.entry_id == entry_id:
            return entry
    raise LedgerError(f"لا حلقةَ في السجلّ بمعرّف {entry_id!r}.")


def registrations_naming_their_outcome() -> tuple[str, ...]:
    """بنودُ التسجيل التي تحمل حقلَ نتيجةٍ فصارت تقاريرَ لا تسجيلات."""

    guilty: list[str] = []
    for entry in read_ledger():
        if entry.kind is not EntryKind.PRE_REGISTRATION:
            continue
        written = _canonical(entry.payload)
        if any(f'"{field}"' in written for field in THE_RESULT_BEARING_FIELDS):
            guilty.append(entry.entry_id)
    return tuple(guilty)


# --- المادّةُ وختمُها، وإعادةُ العدّ ---------------------------------------


@dataclass(frozen=True)
class MaterialSeal:
    """ختمُ مادّةٍ مسجَّلٌ قبل قراءتها: موضعُها وبصمتُها وعدّةُ بايتاتها."""

    relative_path: str
    sha256: str
    byte_length: int

    @property
    def path(self) -> Path:
        return _repository_root() / self.relative_path

    @property
    def is_present(self) -> bool:
        return self.path.is_file()

    def mismatch(self) -> tuple[str, ...]:
        """أوجُه مخالفة المادّة الحاضرة لختمها المسجَّل؛ والمُنتظَرُ ألّا تكون."""

        if not self.is_present:
            return (f"المادّةُ غائبةٌ عن {self.relative_path}",)
        raw = self.path.read_bytes()
        faults: list[str] = []
        if len(raw) != self.byte_length:
            faults.append(f"بايتات: {len(raw)} ≠ {self.byte_length}")
        measured = sha256(raw).hexdigest()
        if measured != self.sha256:
            faults.append(f"بصمة: {measured[:8]} ≠ {self.sha256[:8]}")
        return tuple(faults)


def _material_of(payload: dict[str, Any]) -> MaterialSeal:
    material = payload["المادّة"]
    return MaterialSeal(
        relative_path=material["الموضع"],
        sha256=material["البصمة"],
        byte_length=material["البايتات"],
    )


def _layer_zero(seal: MaterialSeal, encoding: str) -> str:
    """الطبقةُ صفر: استخراجٌ خشنٌ مُعلَنُ الخشونة من مستندٍ مُركَّب."""

    return seal.path.read_bytes().decode(encoding, errors="ignore")


_ARABIC_LETTERS: Final[re.Pattern[str]] = re.compile(r"[\u0621-\u064a]")


def _arabic_letter_count(text: str) -> int:
    return len(_ARABIC_LETTERS.findall(text))


@dataclass(frozen=True)
class ControlReading:
    """ضابطُ سمعٍ واحد: لفظٌ مسجَّلٌ وحدُّه الأدنى وما وُجد منه فعلًا."""

    needle: str
    floor: int
    measured: int

    @property
    def heard(self) -> bool:
        return self.measured >= self.floor


class RunStanding(Enum):
    """منزلةُ جولةٍ بعد المصادمة؛ أربعٌ لا خامسَ لها."""

    STOOD_ON_A_HEARD_INSTRUMENT = "قائمةٌ_على_مسطرةٍ_سُمِعت"
    REFUSED_FOR_A_BROKEN_SEAL = "مردودةٌ_لختمٍ_مخالف"
    REFUSED_FOR_A_DRIFTED_COUNT = "مردودةٌ_لعددٍ_نزاح"
    REFUSED_FOR_A_DEAF_INSTRUMENT = "مردودةٌ_لمسطرةٍ_لم_تُسمَع"


@dataclass(frozen=True)
class RunAudit:
    """مصادمةُ جولةٍ واحدة: ختمُها، وعددُها مُعادًا، وسمعُ مسطرتها، ومعلَّقُها."""

    run_id: str
    registration_id: str
    domain: str
    question: str
    seal_faults: tuple[str, ...]
    recorded_count: int
    recomputed_count: int
    controls: tuple[ControlReading, ...]
    arabic_letters: int
    arabic_letters_floor: int
    near_misses: tuple[tuple[str, int], ...]
    upheld: tuple[str, ...]
    fell: tuple[str, ...]
    pending: tuple[str, ...]

    @property
    def count_drifted(self) -> bool:
        return self.recorded_count != self.recomputed_count

    @property
    def instrument_is_heard(self) -> bool:
        """المسطرةُ تسمع: كلُّ ضابطٍ بلغ حدَّه، والعربيّةُ المستخرَجةُ فوق قاعها."""

        return all(control.heard for control in self.controls) and (
            self.arabic_letters >= self.arabic_letters_floor
        )

    @property
    def near_misses_found(self) -> tuple[tuple[str, int], ...]:
        """القريبُ الموجودُ بعدده؛ وهو معلَّقٌ لا وجدانٌ للمطلوب."""

        return tuple((word, count) for word, count in self.near_misses if count)

    @property
    def standing(self) -> RunStanding:
        if self.seal_faults:
            return RunStanding.REFUSED_FOR_A_BROKEN_SEAL
        if self.count_drifted:
            return RunStanding.REFUSED_FOR_A_DRIFTED_COUNT
        if not self.instrument_is_heard:
            return RunStanding.REFUSED_FOR_A_DEAF_INSTRUMENT
        return RunStanding.STOOD_ON_A_HEARD_INSTRUMENT


def audit_of(run_id: str) -> RunAudit:
    """يُعيد تنفيذ جولةٍ مسجَّلةٍ من وصفتها، ويقابل المُعادَ بالمكتوب.

    ولا تُقرأ الجولةُ إلّا من بند تسجيلها: المسألةُ والمقياسُ والضوابطُ
    والقريبُ كلُّها من البند السابق، والمكتوبُ في الجولة هو المُصادَم.
    """

    run = entry_by_id(run_id)
    if run.kind is not EntryKind.RUN:
        raise LedgerError(f"الحلقةُ {run_id!r} ليست جولةً فلا تُصادَم مصادمةَ جولة.")
    if not run.cites:
        raise LedgerError(
            f"الجولةُ {run_id!r} بلا تسجيلٍ مسبقٍ تستشهد به؛ وهي موسومةٌ "
            f"{run.tag!r} ولا تُحتسَب في درجة."
        )
    registration = entry_by_id(run.cites[0])
    if registration.kind is not EntryKind.PRE_REGISTRATION:
        raise LedgerError(f"ما استشهدت به {run_id!r} ليس بندَ تسجيلٍ مسبق.")
    if registration.rank >= run.rank:
        raise LedgerError("بندُ التسجيل بعد جولته في السلسلة؛ ولا سَبقَ في ذلك.")

    registered = registration.payload
    seal = _material_of(registered)
    faults = seal.mismatch()
    measure = registered["المقياس"]
    if measure["الجنس"] != "عدٌّ_حرفيّ":
        raise LedgerError(f"مقياسٌ غيرُ مقروءٍ ههنا: {measure['الجنس']!r}.")

    text = "" if faults else _layer_zero(seal, measure["الترميز"])
    needle = unicodedata.normalize("NFC", measure["اللفظ"])
    controls = tuple(
        ControlReading(
            needle=control["اللفظ"],
            floor=control["الحدّ_الأدنى"],
            measured=text.count(control["اللفظ"]),
        )
        for control in registered["ضوابط_السمع"]["ألفاظ"]
    )
    return RunAudit(
        run_id=run.entry_id,
        registration_id=registration.entry_id,
        domain=run.domain,
        question=registered["المسألة"],
        seal_faults=faults,
        recorded_count=run.payload["العدّ"],
        recomputed_count=text.count(needle),
        controls=controls,
        arabic_letters=_arabic_letter_count(text),
        arabic_letters_floor=registered["ضوابط_السمع"]["أدنى_محارف_عربيّة"],
        near_misses=tuple(
            (word, text.count(word)) for word in registered["ألفاظ_قريبة"]
        ),
        upheld=tuple(run.payload["ما_ثبت"]),
        fell=tuple(run.payload["ما_سقط"]),
        pending=tuple(run.payload["ما_بقي_معلَّقًا"]),
    )


def counted_runs() -> tuple[Entry, ...]:
    """الجولاتُ المحتسَبةُ في الدرجات: ما لها تسجيلٌ مسبقٌ وليست استعراضًا."""

    return tuple(
        entry
        for entry in read_ledger()
        if entry.kind is EntryKind.RUN and entry.cites and not entry.is_demo
    )


def demo_runs() -> tuple[Entry, ...]:
    """الجولاتُ الاستعراضيّة: محفوظةٌ بوسمها، ساقطةٌ من شرط الدرجة."""

    return tuple(
        entry
        for entry in read_ledger()
        if entry.kind is EntryKind.RUN and entry.is_demo
    )


def _cites_a_prior_run() -> tuple[str, ...]:
    """الجولاتُ التي تستشهد بجولةٍ سابقة؛ وهي مادّةُ الدرجة الثالثة."""

    runs = {entry.entry_id for entry in read_ledger() if entry.kind is EntryKind.RUN}
    return tuple(
        entry.entry_id
        for entry in counted_runs()
        if any(cited in runs for cited in entry.cites)
    )


def _validated_on_a_second_material() -> tuple[str, ...]:
    """الجولاتُ التي استخرجت قاعدةً وقوبِلت بمادّةٍ ثانيةٍ بختمٍ مختلف."""

    validated: list[str] = []
    for entry in counted_runs():
        registration = entry_by_id(entry.cites[0])
        payload = registration.payload
        if payload["المقياس"]["الجنس"] != "قاعدةٌ_مستخرَجة":
            continue
        seals = {material["البصمة"] for material in payload.get("مادّةٌ_ثانية", [])} | {
            _material_of(payload).sha256
        }
        if len(seals) > 1:
            validated.append(entry.entry_id)
    return tuple(validated)


def rung_standing() -> tuple[tuple[int, bool, str], ...]:
    """منزلةُ الدرجات الأربع مشتقّةً من السجلّ: رتبةٌ، وبلوغٌ، وتعليلٌ مقيس."""

    counted = counted_runs()
    audits = tuple(audit_of(entry.entry_id) for entry in counted)
    heard = RunStanding.STOOD_ON_A_HEARD_INSTRUMENT
    standing_runs = tuple(audit for audit in audits if audit.standing is heard)
    domains = {entry.domain for entry in counted}
    cumulative = _cites_a_prior_run()
    transferred = _validated_on_a_second_material()
    return (
        (
            1,
            bool(standing_runs) and not chain_breaks(),
            f"جولاتٌ مسجَّلةٌ أُعيدت وسُمِعت مسطرتُها: {len(standing_runs)} من "
            f"{len(counted)}؛ وانقطاعُ السلسلة: {len(chain_breaks())}.",
        ),
        (
            2,
            bool(transferred),
            f"جولاتٌ استخرجت قاعدةً وقوبِلت بمادّةٍ ثانيةٍ بختمٍ مختلف: "
            f"{len(transferred)}.",
        ),
        (
            3,
            bool(cumulative),
            f"جولاتٌ تستشهد بجولةٍ سابقة: {len(cumulative)}؛ وإيداعُ السجلّ "
            "وحدَه ليس تراكمًا.",
        ),
        (
            4,
            len(domains) > 1,
            f"مجالاتُ الجولات المحتسَبة: {len(domains)} ({'، '.join(sorted(domains))}).",
        ),
    )
