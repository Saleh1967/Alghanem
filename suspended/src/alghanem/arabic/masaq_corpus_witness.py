"""إيداعُ مدوَّنة MASAQ شاهدًا مُبصَّمًا غيرَ منسوخ، ومَوانعُ إيداعها مكتوبةً.

وصلت في النصّ الوارد بصمةٌ واحدةٌ لملفّ `MASAQ.csv`، ولم يصل معها **طولُ
بايتاتٍ ولا مرآةٌ فُتِحت ولا مسارٌ فيها ولا رخصةٌ مُسمّاةٌ ولا شرطُ إسناد**.
وشرطُ الإيداع في هذه الشجرة — كما في `irab_corpus_witness` — بصمةٌ **وطولٌ
ومسارٌ ورخصةٌ وشرطُ إسناد**؛ فالبصمةُ وحدَها **نصفُ تعريف**. فهذه الوحدة
تُودِع **ما وصل** وتُسمّي **ما لم يصل** مانعًا قائمًا بشرط رفعه، ولا تختلق
طولًا ولا مسارًا لملفٍّ لم يُفتَح في هذه الشجرة.

`A_DIGEST_ALONE_IS_NOT_A_DEPOSIT`: بصمةٌ بلا طولٍ ولا مسارٍ مُصرَّحٍ به لا
يُعاد بها اشتقاقُ رقم: من حاز ملفًّا بالاسم نفسِه لا يعرف أهو المقيسُ أم
سواه إلّا بمطابقتين. فالبصمةُ مُودَعةٌ هنا **مُنتظِرةً تمامَها**، ولا تُبنى
عليها وحدَها قراءةٌ لبايتات.

`TWO_CORPORA_ARE_NOT_ONE_CORPUS`: MASAQ ومدوَّنةُ القرآن الصرفية تَسِمان النصَّ
نفسَه بيدين مختلفتين. فاتّفاقُهما — إن وقع — اتّفاقُ **وَسْمَين** لا تضاعفُ
**نصّ**؛ ولا يُجمَع عددٌ من هذه إلى عددٍ من تلك، ولا يُقرأ توافقُهما شاهدين
مستقلَّين على النصّ، على منوال `TwoMirrorsOneDigestIsNotTwoWitnesses` في
`transitivity_lexicon_witness`.

`A_COLUMN_BINDING_IS_LEGISLATED_NOT_READ`: أسماءُ أعمدة `MASAQ.csv` وأيُّها
يحمل الموضعَ والصورةَ والجذرَ والوزنَ ووَسْمَ المصدر — **قرارُ ربطٍ يُسَنّ**
لا قراءةٌ تُقرأ من بصمة. فلا يُقرأ صفٌّ واحدٌ في هذه الوحدة إلّا بربطٍ
مُصرَّحٍ به يُسمّي مَن أعلنه ومُصادَرتَه، وبصمتُه تُحسَب منه. ومن ظنَّ ترتيبَ
الأعمدة فقد سنَّ قاعدةً في صورة قراءة.

وهذه الوحدة تسجيلٌ لا سلطة: لا ولادةَ فيها، ولا حكمَ ولادة، ولا تجميدَ `E0`،
ولا تستورد من `kernel/` شيئًا، ولا تقرؤها وحدةٌ فيه. وبايتاتُ المدوَّنة غيرُ
منسوخةٍ إلى الشجرة.
"""

from __future__ import annotations

import csv
import hashlib
from collections.abc import Iterable, Sequence
from dataclasses import dataclass
from enum import Enum
from io import StringIO
from pathlib import Path
from typing import Final

from ..canonical_content import canonical_bytes, canonical_digest
from .irab_corpus_witness import (
    A_MIRROR_IS_NOT_THE_UPSTREAM_NOTE,
    ATTRIBUTION_IS_A_CONDITION_NOT_A_COURTESY_NOTE,
    WITNESS_BYTES_ARE_NOT_VENDORED_NOTE,
    IrabCorpusWitness,
)

__all__ = [
    "A_COLUMN_BINDING_IS_LEGISLATED_NOT_READ_NOTE",
    "A_DIGEST_ALONE_IS_NOT_A_DEPOSIT_NOTE",
    "MASAQ_ARRIVING_SHA256",
    "MASAQ_COLUMN_BINDING",
    "MASAQ_CORPUS_WITNESS",
    "MASAQ_DEPOSIT_BARRIERS",
    "MASAQ_WITNESS_NAMED_RESIDUALS",
    "TWO_CORPORA_ARE_NOT_ONE_CORPUS_NOTE",
    "DepositStanding",
    "MasaqColumnBinding",
    "MasaqDepositBarrier",
    "MasaqSegmentRow",
    "MasaqWitnessError",
    "binding_digest",
    "deposit_masaq_witness",
    "masdar_rows",
    "open_barriers",
    "parse_masaq_rows",
    "read_masaq_rows",
    "verified_masaq_bytes",
]


class MasaqWitnessError(ValueError):
    """تُرفَع حين يُودَع شاهدٌ ناقصٌ أو يُقرأ صفٌّ بربطٍ غيرِ مُصرَّحٍ به."""


A_DIGEST_ALONE_IS_NOT_A_DEPOSIT_NOTE: Final[str] = (
    "ADigestAloneIsNotADeposit: وصلت بصمةُ `MASAQ.csv` بلا طولِ بايتاتٍ ولا "
    "مرآةٍ فُتِحت ولا مسارٍ فيها ولا رخصةٍ مُسمّاة؛ والبصمةُ وحدَها نصفُ "
    "تعريفٍ لا يُعاد به اشتقاقُ رقم، فالإيداعُ موقوفٌ على تمامه"
)

TWO_CORPORA_ARE_NOT_ONE_CORPUS_NOTE: Final[str] = (
    "TwoCorporaAreNotOneCorpus: MASAQ ومدوَّنةُ القرآن الصرفية تَسِمان النصَّ "
    "نفسَه بيدين مختلفتين؛ فاتّفاقُهما اتّفاقُ وَسْمَين لا تضاعفُ نصّ، ولا "
    "يُجمَع عددٌ من إحداهما إلى عددٍ من الأخرى"
)

A_COLUMN_BINDING_IS_LEGISLATED_NOT_READ_NOTE: Final[str] = (
    "AColumnBindingIsLegislatedNotRead: أسماءُ الأعمدة وأيُّها يحمل الجذرَ "
    "والوزنَ ووَسْمَ المصدر قرارُ ربطٍ يُسَنّ ويُعلَن بمُصادَرته ومَن أعلنه؛ "
    "ومن ظنَّ ترتيبَ الأعمدة سنَّ قاعدةً في صورة قراءة"
)

MASAQ_WITNESS_NAMED_RESIDUALS: Final[dict[str, str]] = {
    "ADigestAloneIsNotADeposit": A_DIGEST_ALONE_IS_NOT_A_DEPOSIT_NOTE,
    "TwoCorporaAreNotOneCorpus": TWO_CORPORA_ARE_NOT_ONE_CORPUS_NOTE,
    "AColumnBindingIsLegislatedNotRead": (A_COLUMN_BINDING_IS_LEGISLATED_NOT_READ_NOTE),
    "WitnessBytesAreNotVendored": WITNESS_BYTES_ARE_NOT_VENDORED_NOTE,
    "AttributionIsAConditionNotACourtesy": (
        ATTRIBUTION_IS_A_CONDITION_NOT_A_COURTESY_NOTE
    ),
    "AMirrorIsNotTheUpstream": A_MIRROR_IS_NOT_THE_UPSTREAM_NOTE,
}


MASAQ_ARRIVING_SHA256: Final[str] = (
    "d43d2a813afbe0490254bb26623d6041ed352a273d333e731ddbcda3bd0b6f3a"
)
"""البصمةُ الوحيدةُ التي وصلت لـ`MASAQ.csv`؛ ولا يُودَع شاهدٌ بغيرها."""


class DepositStanding(Enum):
    """منزلةُ المانع. `OPEN` تعني أنّ الإيداعَ ناقصٌ حتّى يُرفَع."""

    OPEN = "قائمٌ: الإيداعُ ناقص"
    LIFTED = "مرفوعٌ: شرطُه استُوفي"


@dataclass(frozen=True, slots=True)
class MasaqDepositBarrier:
    """مانعٌ يحول دون تمام الإيداع، وشرطُ رفعه مكتوبًا لا متروكًا للرأي."""

    what_is_blocked: str
    barrier: str
    what_lifts_it: str
    standing: DepositStanding

    def __post_init__(self) -> None:
        for value, label in (
            (self.what_is_blocked, "الممنوع"),
            (self.barrier, "نصُّ المانع"),
            (self.what_lifts_it, "شرطُ الرفع"),
        ):
            if not isinstance(value, str) or not value.strip():
                raise MasaqWitnessError(f"{label} نصٌّ غير فارغ؛ ولا يُترَك صمتًا.")
        if not isinstance(self.standing, DepositStanding):
            raise MasaqWitnessError("منزلةُ المانع من مفردتها المغلقة.")


MASAQ_DEPOSIT_BARRIERS: Final[tuple[MasaqDepositBarrier, ...]] = (
    MasaqDepositBarrier(
        what_is_blocked="إيداعُ `MASAQ.csv` شاهدًا تامًّا في `IrabCorpusWitness`",
        barrier=(
            "وصلت البصمةُ وحدَها: لا طولَ بايتاتٍ، ولا اسمَ مرآةٍ فُتِحت، ولا "
            "مسارَ ملفٍّ فيها، ولا رخصةً مُسمّاةً، ولا شرطَ إسناد. "
            + A_DIGEST_ALONE_IS_NOT_A_DEPOSIT_NOTE
        ),
        what_lifts_it=(
            "وصولُ طولِ البايتات والمرآةِ التي فُتِحت والمسارِ فيها والرخصةِ "
            "ومواضعِ الإحالة المشروطة، ثمّ استدعاءُ `deposit_masaq_witness` "
            "بها؛ فتُبنى منها شهادةٌ تُطابَق بها البايتات"
        ),
        standing=DepositStanding.OPEN,
    ),
    MasaqDepositBarrier(
        what_is_blocked="قراءةُ صفوف `MASAQ.csv` بربطِ أعمدةٍ مُجمَّدٍ في الشجرة",
        barrier=(
            "لم تصل أسماءُ أعمدة الملفّ ولا أيُّها يحمل الموضعَ والصورةَ "
            "والجذرَ والوزنَ ووَسْمَ المصدر. " + A_COLUMN_BINDING_IS_LEGISLATED_NOT_READ_NOTE
        ),
        what_lifts_it=(
            "إعلانُ `MasaqColumnBinding` بأسماء أعمدةٍ مُصرَّحٍ بمصدرها "
            "ومُصادَرتها؛ وتُحسَب بصمتُه فيُعرَف أيُّ ربطٍ خرج منه أيُّ رقم"
        ),
        standing=DepositStanding.OPEN,
    ),
)
"""ما يمنع تمامَ الإيداع اليوم؛ ولا يُرفَع مانعٌ إلّا باستيفاء شرطه المكتوب."""


def open_barriers() -> tuple[MasaqDepositBarrier, ...]:
    """الموانعُ القائمةُ الآن؛ وخلوُّها شرطُ أيِّ رقمٍ من هذه البايتات."""

    return tuple(
        barrier
        for barrier in MASAQ_DEPOSIT_BARRIERS
        if barrier.standing is DepositStanding.OPEN
    )


MASAQ_CORPUS_WITNESS: Final[IrabCorpusWitness | None] = None
"""لا شهادةَ مُودَعةً بعد: الموانعُ في `MASAQ_DEPOSIT_BARRIERS` قائمة.

ولم يُوضَع هنا شاهدٌ بطولٍ مُقدَّرٍ ولا بمسارٍ مُرجَّح: ملفٌّ لم يُفتَح لا
يُسنَد إليه مسارٌ في هذه الشجرة.
"""


def deposit_masaq_witness(
    *,
    version: str,
    upstream: str,
    measured_mirror: str,
    measured_path: str,
    byte_length: int,
    licenses: Sequence[str],
    required_attribution_links: Sequence[str],
    attribution_requirement: str,
    annotation_note: str,
    sha256: str = MASAQ_ARRIVING_SHA256,
) -> IrabCorpusWitness:
    """ابْنِ شهادةَ MASAQ من وقائعَ يُصرِّح بها حائزُ البايتات، لا من ظنٍّ.

    ولا تُبنى شهادةٌ ببصمةٍ غيرِ البصمة الواردة: ملفٌّ آخرُ بالاسم نفسِه
    شاهدٌ آخرُ يُودَع بتسجيلٍ آخر، ولا يدخل من هذا الباب.
    """

    if sha256 != MASAQ_ARRIVING_SHA256:
        raise MasaqWitnessError(
            f"البصمةُ {sha256} ليست البصمةَ الواردةَ {MASAQ_ARRIVING_SHA256}؛ "
            "وملفٌّ آخرُ شاهدٌ آخرُ لا يدخل باسم هذا."
        )
    return IrabCorpusWitness(
        corpus="MASAQ (Morphologically and Syntactically Annotated Quran)",
        version=version,
        upstream=upstream,
        measured_mirror=measured_mirror,
        measured_path=measured_path,
        sha256=sha256,
        byte_length=byte_length,
        licenses=tuple(licenses),
        required_attribution_links=tuple(required_attribution_links),
        attribution_requirement=(
            attribution_requirement
            + " "
            + ATTRIBUTION_IS_A_CONDITION_NOT_A_COURTESY_NOTE
        ),
        annotation_note=(
            annotation_note
            + " "
            + TWO_CORPORA_ARE_NOT_ONE_CORPUS_NOTE
            + " "
            + A_MIRROR_IS_NOT_THE_UPSTREAM_NOTE
        ),
    )


@dataclass(frozen=True, slots=True)
class MasaqColumnBinding:
    """ربطُ أعمدة `MASAQ.csv` بما يُقرأ منها، مُصرَّحًا بمَن أعلنه ومُصادَرته."""

    declared_by: str
    what_it_assumes: str
    location_column: str
    form_column: str
    morphological_tag_column: str
    root_column: str
    lemma_column: str
    verb_form_column: str
    masdar_tag_values: tuple[str, ...]
    meemi_masdar_tag_values: tuple[str, ...]

    def __post_init__(self) -> None:
        for value, label in (
            (self.declared_by, "مَن أعلن الربط"),
            (self.what_it_assumes, "مُصادَرةُ الربط"),
        ):
            if not isinstance(value, str) or not value.strip():
                raise MasaqWitnessError(
                    f"{label} نصٌّ غير فارغ. "
                    + A_COLUMN_BINDING_IS_LEGISLATED_NOT_READ_NOTE
                )
        columns = self.columns
        for column in columns:
            if not isinstance(column, str) or not column.strip():
                raise MasaqWitnessError("اسمُ العمود نصٌّ غير فارغ؛ ولا يُخمَّن.")
        if len(set(columns)) != len(columns):
            raise MasaqWitnessError("عمودٌ واحدٌ مربوطٌ بمعنيين؛ والتكرارُ يُوهِم قراءتين.")
        for values, label in (
            (self.masdar_tag_values, "وَسْمُ المصدر"),
            (self.meemi_masdar_tag_values, "وَسْمُ المصدر الميميّ"),
        ):
            if not values:
                raise MasaqWitnessError(f"{label} لا يُترَك فارغًا؛ فالعدُّ به يقع.")
            if len(set(values)) != len(values):
                raise MasaqWitnessError(f"{label} فيه تكرارٌ يُوهِم سَعةً.")
        overlap = set(self.masdar_tag_values) & set(self.meemi_masdar_tag_values)
        if overlap:
            raise MasaqWitnessError(
                f"وَسْمٌ مشتركٌ بين المصدر والمصدر الميميّ: {sorted(overlap)}؛ "
                "والفصلُ بينهما هو محلُّ الدعوى فلا يُخلَطان."
            )

    @property
    def columns(self) -> tuple[str, ...]:
        """الأعمدةُ المطلوبةُ بأسمائها؛ وغيابُ واحدٍ منها يُوقِف القراءة."""

        return (
            self.location_column,
            self.form_column,
            self.morphological_tag_column,
            self.root_column,
            self.lemma_column,
            self.verb_form_column,
        )

    @property
    def all_masdar_tag_values(self) -> tuple[str, ...]:
        """وسومُ المصدر كلُّها، المجرَّدُ منها والميميّ، بلا خلطِ البابين."""

        return self.masdar_tag_values + self.meemi_masdar_tag_values


MASAQ_COLUMN_BINDING: Final[MasaqColumnBinding | None] = None
"""لا ربطَ مُجمَّدًا في الشجرة: أسماءُ الأعمدة لم تصل، ولا تُخمَّن هنا."""


def binding_digest(binding: MasaqColumnBinding) -> str:
    """بصمةُ الربط؛ فتبديلُ عمودٍ أو وَسْمٍ بعد الرقم يُغيّرها فيُرى."""

    return canonical_digest(
        canonical_bytes(
            {
                "declared_by": binding.declared_by,
                "what_it_assumes": binding.what_it_assumes,
                "columns": list(binding.columns),
                "masdar_tag_values": list(binding.masdar_tag_values),
                "meemi_masdar_tag_values": list(binding.meemi_masdar_tag_values),
            }
        )
    )


@dataclass(frozen=True, slots=True)
class MasaqSegmentRow:
    """صفٌّ واحدٌ مقروءٌ بالربط المُصرَّح به، بحقوله كما وُسِمت لا كما نقرؤها."""

    location: str
    form: str
    morphological_tag: str
    root: str
    lemma: str
    verb_form: str

    def is_masdar(self, binding: MasaqColumnBinding) -> bool:
        """أوُسِم هذا الصفُّ مصدرًا بأحد الوسوم المُصرَّح بها؟"""

        return self.morphological_tag in binding.all_masdar_tag_values


def parse_masaq_rows(
    text: str, binding: MasaqColumnBinding
) -> tuple[MasaqSegmentRow, ...]:
    """اقرأ نصَّ الملفّ صفوفًا بالربط المُصرَّح به، ولا تتخطَّ صفًّا صامتًا.

    وصفٌّ ينقصه عمودٌ من أعمدة الربط يُرفَع به خطأ: تخطّي صفٍّ لا يُقرأ
    يُنقِص العددَ بلا أثرٍ يُتتبَّع، فيصير النقصُ خاصّيّةً في اللغة عند من
    قرأ الرقم.
    """

    reader = csv.DictReader(StringIO(text, newline=""))
    header = reader.fieldnames
    if header is None:
        raise MasaqWitnessError("ملفٌّ بلا ترويسةِ أعمدةٍ لا يُقرأ بربطٍ بالأسماء.")
    missing = [column for column in binding.columns if column not in header]
    if missing:
        raise MasaqWitnessError(
            f"أعمدةٌ مُعلَنةٌ في الربط غائبةٌ عن الترويسة: {missing}؛ "
            "ولا يُحمَل عمودٌ على أقرب اسمٍ إليه. "
            + A_COLUMN_BINDING_IS_LEGISLATED_NOT_READ_NOTE
        )
    rows: list[MasaqSegmentRow] = []
    for number, record in enumerate(reader, start=2):
        values: list[str] = []
        for column in binding.columns:
            value = record.get(column)
            if value is None:
                raise MasaqWitnessError(
                    f"الصفُّ {number} ينقصه العمودُ «{column}»؛ ولا يُتخطّى صامتًا."
                )
            values.append(value)
        location, form, tag, root, lemma, verb_form = values
        rows.append(
            MasaqSegmentRow(
                location=location,
                form=form,
                morphological_tag=tag,
                root=root,
                lemma=lemma,
                verb_form=verb_form,
            )
        )
    return tuple(rows)


def verified_masaq_bytes(path: Path, witness: IrabCorpusWitness) -> bytes:
    """بايتاتُ MASAQ مرفوضةً إن خالفت طولَ الشهادة أو بصمتَها.

    ولا تُقبَل شهادةٌ بصمتُها غيرُ البصمة الواردة: القراءةُ من هذا الباب
    قراءةُ ذلك الملفّ بعينه لا قراءةُ ملفٍّ يُشبهه.
    """

    if witness.sha256 != MASAQ_ARRIVING_SHA256:
        raise MasaqWitnessError(
            "الشهادةُ المُمرَّرة ليست شهادةَ `MASAQ.csv` الواردة بصمتُها."
        )
    if not path.is_file():
        raise MasaqWitnessError(f"ملفُّ المدوَّنة غيرُ موجودٍ في المسار: {path}")
    data = path.read_bytes()
    if len(data) != witness.byte_length:
        raise MasaqWitnessError(
            f"طولُ البايتات {len(data)} لا يطابق الشهادة {witness.byte_length}"
        )
    digest = hashlib.sha256(data).hexdigest()
    if digest != witness.sha256:
        raise MasaqWitnessError(
            f"بصمةُ البايتات {digest} لا تطابق الشهادة {witness.sha256}"
        )
    return data


def read_masaq_rows(
    path: Path, witness: IrabCorpusWitness, binding: MasaqColumnBinding
) -> tuple[MasaqSegmentRow, ...]:
    """صفوفُ المدوَّنة بعد مطابقة البصمة والطول، ثمّ بالربط المُصرَّح به."""

    data = verified_masaq_bytes(path, witness)
    return parse_masaq_rows(data.decode("utf-8"), binding)


def masdar_rows(
    rows: Iterable[MasaqSegmentRow], binding: MasaqColumnBinding
) -> tuple[MasaqSegmentRow, ...]:
    """الصفوفُ الموسومةُ مصدرًا وحدَها، بالوسوم المُصرَّح بها لا بقراءةِ صورة."""

    return tuple(row for row in rows if row.is_masdar(binding))
