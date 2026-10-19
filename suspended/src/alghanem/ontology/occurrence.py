"""الوقوعُ اللفظيُّ: موضعٌ في مصدرٍ محفوظ، وشهادةُ تمثيلٍ تُنفَّذ لا تُدَّعى.

الفصلُ المحفوظُ ههنا أنّ **اللفظَ غيرُ الفرد**: «زيدٌ اسمٌ قصير» حكمٌ على
الوقوع اللفظيّ، لا على من سُمّي به. فـ`Occurrence` لا تحمل مُعرِّفَ فردٍ أصلًا؛
تحمل مرشَّحي إحالةٍ **مُشتقّين** يُسلَّمون إليها من خارجها.

**أوّلًا: الموضعُ يُقابَل بالبايتات.**
`witness_occurrence` تفتح المسار المُعلَن، وتقيس ختمَه، وتقطع المدى المذكور
بوحدته، وتقابل النصَّ المكتوب بما قُطِع. فإن خالف، فـ`TEXT_DOES_NOT_MATCH`؛
ولا يُمرَّر حرفٌ واحدٌ على حسن الظنّ.

**ثانيًا: الحقلُ المستهلَكُ يُشتَقّ من المُعاد تنفيذُه لا من السجلّ المُقدَّم.**
`canonical116.verify` في النسخة المفحوصة تقابل `status` و`source_sha256` و
`canonical_atoms` ولا تحرس `canonical_text`. فمن قرأ `record["canonical_text"]`
قرأ حقلًا غيرَ محروس. وعليه `canonical_reading` **تقرأ من `outcome["replay"]`**
بعد `reproduced`، فتحريفُ الحقل في السجلّ المُقدَّم لا يُغيِّر شيئًا. وهذا
اشتقاقٌ من المتحقَّق، لا توسيعٌ لعقد الحزمة.

**ثالثًا: المقدّمةُ المعلَّقةُ تُسمّى ولا يُرجَع عنها صمتًا.**
إن لم تبلغ ١١٦ حالَ `READY`، فلا تُمنَح شهادةُ المسار المكتمل. ويبقى الوقوعُ
وشهادةُ موضعه نافذَين — وهما عملُ سجلٍّ بنيويٍّ لا اشتقاقٌ لغويٌّ مكتمل.

تسجيلٌ لا سلطة: لا ولادةَ ولا حكمَ ولادةٍ ولا تجميدَ `E0`.
"""

from __future__ import annotations

import hashlib
from dataclasses import dataclass
from enum import Enum
from pathlib import Path
from typing import Any, Final

from ..canonical_content import canonical_bytes, canonical_digest


class OccurrenceError(ValueError):
    """خطأٌ في الوقوع وشهادته؛ صنفٌ مستقلٌّ لا يُلتبَس بغيره."""


A_WORD_IS_NOT_ITS_BEARER: Final[str] = (
    "«زيدٌ اسمٌ قصير» حكمٌ على الوقوع اللفظيّ لا على من سُمّي به؛ فالوقوعُ لا "
    "يحمل مُعرِّفَ فردٍ، وإنّما يُسلَّم إليه مرشَّحون مُشتقّون من خارجه"
)

THE_CONSUMED_FIELD_IS_DERIVED_FROM_THE_REPLAY: Final[str] = (
    "`canonical116.verify` تقابل الحالَ وختمَ المصدر والذرّات، ولا تحرس "
    "`canonical_text`؛ فالحقلُ المستهلَكُ يُقرَأ من `replay` بعد `reproduced` "
    "لا من السجلّ المُقدَّم، وتحريفُه في المُقدَّم لا يُحرِّك المشتَقّ"
)

A_SUSPENDED_PREMISE_IS_NAMED_NOT_BYPASSED: Final[str] = (
    "إن تعلّقت مقدّمةٌ لازمةٌ في ١١٦ فلا تُمنَح شهادةُ المسار المكتمل، ولا "
    "يُرجَع إلى النصّ الخام صمتًا؛ ويبقى عملُ السجلّ البنيويّ ولا يُسمّى "
    "اشتقاقًا لغويًّا مكتملًا"
)

A_SEAL_FAILURE_IS_NOT_AN_ABSENT_WITNESS: Final[str] = (
    "رفضُ نسخةٍ لفساد ختمها غيرُ رفضِ دعوى لغياب شاهدها داخل نسخةٍ معرّفة؛ "
    "فالأوّل لا يُثبِت الثاني، ومنزلتاهما مفصولتان"
)


class OffsetUnit(Enum):
    """وحدةُ الإزاحة؛ مفردةٌ مغلقةٌ لأنّ البايتَ غيرُ نقطة الرمز."""

    UTF8_BYTE = "utf8_byte"
    CODEPOINT = "codepoint"


class RepresentationStanding(Enum):
    """منزلةُ شهادة التمثيل؛ مفردةٌ مغلقةٌ فيها منازلُ الإخفاق مُسمّاة."""

    REPRODUCED = "reproduced"
    SOURCE_MISSING = "source_missing"
    SEAL_MISMATCH = "seal_mismatch"
    RANGE_OUT_OF_BOUNDS = "range_out_of_bounds"
    TEXT_DOES_NOT_MATCH = "text_does_not_match"
    NOT_A_TEXT_BOUNDARY = "not_a_text_boundary"

    @property
    def is_reproduced(self) -> bool:
        """أأُعيد إنتاجُه من المصدر؟ خاصّيّةٌ تُشتَقّ لا حقلٌ يُكتَب."""

        return self is RepresentationStanding.REPRODUCED


class CanonicalStanding(Enum):
    """منزلةُ مرور ١١٦؛ وغيرُ `READY` تُسمّى ولا تُطوى."""

    READY_AND_REPRODUCED = "ready_and_reproduced"
    NOT_READY = "not_ready"
    REPLAY_DISAGREED = "replay_disagreed"

    @property
    def is_complete(self) -> bool:
        """أاكتمل المسارُ اللغويُّ؟ وحدَها الأولى تُقرَأ اكتمالًا."""

        return self is CanonicalStanding.READY_AND_REPRODUCED


def _require_text(value: object, label: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise OccurrenceError(f"{label} نصٌّ غير فارغ")
    return value


@dataclass(frozen=True, slots=True)
class Occurrence:
    """وقوعُ لفظٍ: مصدرُه المحفوظُ بختمه، ومداه بوحدته، ونصُّه المكتوب.

    ولا مُعرِّفَ فردٍ ههنا بحال؛ والمرشَّحون يُشتقّون خارجَه ثمّ يُقابَلون به.
    """

    occurrence_id: str
    source_path: str
    source_sha256: str
    offset_unit: OffsetUnit
    start: int
    end: int
    surface: str

    def __post_init__(self) -> None:
        _require_text(self.occurrence_id, "مُعرِّفُ الوقوع")
        _require_text(self.source_path, "مسارُ المصدر المحفوظ")
        _require_text(self.source_sha256, "ختمُ المصدر")
        if not isinstance(self.offset_unit, OffsetUnit):
            raise OccurrenceError("وحدةُ الإزاحة عضوٌ في مفردتها المغلقة")
        for bound, label in ((self.start, "بدايةُ المدى"), (self.end, "نهايةُ المدى")):
            if not isinstance(bound, int) or isinstance(bound, bool) or bound < 0:
                raise OccurrenceError(f"{label} عددٌ صحيحٌ غيرُ سالب")
        if self.start >= self.end:
            raise OccurrenceError("حدّا المدى مرتّبانِ والمدى غيرُ فارغ")
        _require_text(self.surface, "نصُّ الوقوع كما كُتب؛ و" + A_WORD_IS_NOT_ITS_BEARER)

    @property
    def length(self) -> int:
        """طولُ المدى بوحدته؛ خاصّيّةٌ تُشتَقّ لا حقلٌ يُكتَب."""

        return self.end - self.start

    def as_canonical_content(self) -> dict[str, object]:
        """محتوى الوقوع للبصمة."""

        return {
            "occurrence_id": self.occurrence_id,
            "source_path": self.source_path,
            "source_sha256": self.source_sha256,
            "offset_unit": self.offset_unit.value,
            "start": self.start,
            "end": self.end,
            "surface": self.surface,
        }


@dataclass(frozen=True, slots=True)
class RepresentationWitness:
    """شهادةُ تمثيلٍ مُنفَّذة: منزلتُها، وما قُطِع فعلًا، وبصمةُ ما قُرئ."""

    occurrence_id: str
    standing: RepresentationStanding
    measured_sha256: str | None
    cut_text: str | None
    note: str

    def __post_init__(self) -> None:
        _require_text(self.occurrence_id, "مُعرِّفُ الوقوع المشهود له")
        if not isinstance(self.standing, RepresentationStanding):
            raise OccurrenceError("منزلةُ الشهادة عضوٌ في مفردتها المغلقة")
        if self.measured_sha256 is not None:
            _require_text(self.measured_sha256, "الختمُ المقيس إن قيس")
        if self.standing.is_reproduced and not isinstance(self.cut_text, str):
            raise OccurrenceError(
                "شهادةٌ مُعادةُ الإنتاج بلا نصٍّ مقطوع: منزلةٌ تُخالف حاملَها"
            )
        _require_text(self.note, "سببُ المنزلة مُسمًّى")

    def as_canonical_content(self) -> dict[str, object]:
        """محتوى الشهادة للبصمة."""

        return {
            "occurrence_id": self.occurrence_id,
            "standing": self.standing.value,
            "measured_sha256": self.measured_sha256,
            "cut_text": self.cut_text,
            "note": self.note,
        }

    @property
    def content_id(self) -> str:
        """بصمةُ الشهادة؛ وكلُّ تغييرٍ في المقروء يُخرِج بصمةً أخرى."""

        return canonical_digest(canonical_bytes(self.as_canonical_content()))


def witness_occurrence(occurrence: Occurrence, root: Path) -> RepresentationWitness:
    """نفِّذ شهادةَ التمثيل: افتح، واختم، واقطع، وقابِل. ولا تمرّ على ظنّ.

    المدخل: وقوعٌ بمداه وختم مصدره، وجذرُ الشجرة.
    الشرط: المسارُ موجودٌ، وختمُه يُطابق المُعلَن، والمدى داخلَ الحدود.
    المخرج: شهادةٌ بمنزلةٍ مُسمّاةٍ وبصمةِ ما قُرئ.
    ما تحفظه: كلُّ إخفاقٍ منزلةٌ مُسمّاةٌ لا استثناءٌ يُسكِت الباقي.
    """

    if not isinstance(occurrence, Occurrence):
        raise OccurrenceError("المشهودُ له وقوعٌ قائم")
    if not isinstance(root, Path):
        raise OccurrenceError("جذرُ الشجرة مسارٌ قائم")
    path = root / occurrence.source_path
    if not path.is_file():
        return RepresentationWitness(
            occurrence_id=occurrence.occurrence_id,
            standing=RepresentationStanding.SOURCE_MISSING,
            measured_sha256=None,
            cut_text=None,
            note=(
                f"المسارُ `{occurrence.source_path}` غائبٌ عن الشجرة؛ و"
                + A_SEAL_FAILURE_IS_NOT_AN_ABSENT_WITNESS
            ),
        )
    raw = path.read_bytes()
    measured = hashlib.sha256(raw).hexdigest()
    if measured != occurrence.source_sha256:
        return RepresentationWitness(
            occurrence_id=occurrence.occurrence_id,
            standing=RepresentationStanding.SEAL_MISMATCH,
            measured_sha256=measured,
            cut_text=None,
            note=(
                f"ختمُ المقروء `{measured}` يخالف المُعلَن "
                f"`{occurrence.source_sha256}`؛ و"
                + A_SEAL_FAILURE_IS_NOT_AN_ABSENT_WITNESS
            ),
        )
    if occurrence.offset_unit is OffsetUnit.UTF8_BYTE:
        body: bytes | str = raw
    else:
        body = raw.decode("utf-8")
    if occurrence.end > len(body):
        return RepresentationWitness(
            occurrence_id=occurrence.occurrence_id,
            standing=RepresentationStanding.RANGE_OUT_OF_BOUNDS,
            measured_sha256=measured,
            cut_text=None,
            note=(
                f"المدى [{occurrence.start}, {occurrence.end}) يتجاوز طولَ "
                f"المصدر {len(body)} بوحدة `{occurrence.offset_unit.value}`"
            ),
        )
    cut = body[occurrence.start : occurrence.end]
    if isinstance(cut, bytes):
        try:
            cut_text = cut.decode("utf-8")
        except UnicodeDecodeError as error:
            return RepresentationWitness(
                occurrence_id=occurrence.occurrence_id,
                standing=RepresentationStanding.NOT_A_TEXT_BOUNDARY,
                measured_sha256=measured,
                cut_text=None,
                note=(
                    f"المدى [{occurrence.start}, {occurrence.end}) بوحدة "
                    f"`{occurrence.offset_unit.value}` لا يقع على حدِّ محرفٍ: "
                    f"{error.reason}؛ فالبايتُ غيرُ نقطة الرمز"
                ),
            )
    else:
        cut_text = cut
    if cut_text != occurrence.surface:
        return RepresentationWitness(
            occurrence_id=occurrence.occurrence_id,
            standing=RepresentationStanding.TEXT_DOES_NOT_MATCH,
            measured_sha256=measured,
            cut_text=cut_text,
            note=(
                f"المقطوعُ `{cut_text}` يخالف المكتوبَ `{occurrence.surface}`؛ "
                "فالموضعُ لا يُصدَّق بالاسم"
            ),
        )
    return RepresentationWitness(
        occurrence_id=occurrence.occurrence_id,
        standing=RepresentationStanding.REPRODUCED,
        measured_sha256=measured,
        cut_text=cut_text,
        note=(
            f"قُطِع المدى [{occurrence.start}, {occurrence.end}) بوحدة "
            f"`{occurrence.offset_unit.value}` فطابق المكتوب"
        ),
    )


@dataclass(frozen=True, slots=True)
class CanonicalReading:
    """قراءةُ ١١٦ لوقوعٍ مشهودٍ له: منزلتُها، وذرّاتُها، ونصُّها **المُشتَقّ**.

    و`canonical_text` ههنا مأخوذٌ من `replay` لا من السجلّ المُقدَّم؛ فهو
    مُشتَقٌّ من المُعاد تنفيذُه لا منقولٌ عن مُدَّعٍ.
    """

    occurrence_id: str
    standing: CanonicalStanding
    atom_count: int | None
    derived_text: str | None
    note: str

    def __post_init__(self) -> None:
        _require_text(self.occurrence_id, "مُعرِّفُ الوقوع المقروء")
        if not isinstance(self.standing, CanonicalStanding):
            raise OccurrenceError("منزلةُ القراءة عضوٌ في مفردتها المغلقة")
        if self.standing.is_complete:
            if not isinstance(self.atom_count, int) or self.atom_count < 0:
                raise OccurrenceError("قراءةٌ مكتملةٌ بلا عددِ ذرّاتٍ مقيس")
            if not isinstance(self.derived_text, str):
                raise OccurrenceError("قراءةٌ مكتملةٌ بلا نصٍّ مُشتَقّ")
        _require_text(self.note, "سببُ المنزلة مُسمًّى")

    def as_canonical_content(self) -> dict[str, object]:
        """محتوى القراءة للبصمة."""

        return {
            "occurrence_id": self.occurrence_id,
            "standing": self.standing.value,
            "atom_count": self.atom_count,
            "derived_text": self.derived_text,
            "note": self.note,
        }


def canonical_reading(
    occurrence: Occurrence, witness: RepresentationWitness
) -> CanonicalReading:
    """مرِّر الوقوعَ المشهودَ له على ١١٦، واقرأ المُعاد تنفيذُه وحدَه.

    المدخل: وقوعٌ وشهادةُ تمثيلٍ مُعادةُ الإنتاج.
    الشرط: الشهادةُ منزلتُها `REPRODUCED`؛ وإلّا فلا تمريرَ أصلًا.
    المخرج: منزلةُ ١١٦، وعددُ ذرّاتها، ونصُّها المُشتَقّ من `replay`.
    ما تحفظه: لا تقرأ حقلًا من السجلّ المُقدَّم، ولا تُسمّي غيرَ المكتمل مكتملًا.
    """

    if not isinstance(witness, RepresentationWitness):
        raise OccurrenceError("القراءةُ تُبنى على شهادةٍ قائمة")
    if witness.occurrence_id != occurrence.occurrence_id:
        raise OccurrenceError("شهادةٌ لوقوعٍ آخَرَ لا تُقرَأ لهذا")
    if not witness.standing.is_reproduced:
        raise OccurrenceError(
            "لا تمريرَ على ١١٦ قبل شهادةِ تمثيلٍ مُعادةِ الإنتاج؛ والمنزلةُ "
            f"المقروءة `{witness.standing.value}`"
        )
    from canonical116.bridge import BridgeStatus, bridge, verify

    record: dict[str, Any] = bridge(occurrence.surface.encode("utf-8"))
    if record.get("status") != BridgeStatus.READY.value:
        return CanonicalReading(
            occurrence_id=occurrence.occurrence_id,
            standing=CanonicalStanding.NOT_READY,
            atom_count=None,
            derived_text=None,
            note=(
                f"١١٦ وقفت عند `{record.get('status')}`؛ و"
                + A_SUSPENDED_PREMISE_IS_NAMED_NOT_BYPASSED
            ),
        )
    outcome = verify(record)
    if not outcome["reproduced"]:
        return CanonicalReading(
            occurrence_id=occurrence.occurrence_id,
            standing=CanonicalStanding.REPLAY_DISAGREED,
            atom_count=None,
            derived_text=None,
            note="إعادةُ التنفيذ لم تُطابق الشهادة، فلا يُقرَأ منها حقل",
        )
    replay = outcome["replay"]
    atoms = replay["canonical_atoms"]
    return CanonicalReading(
        occurrence_id=occurrence.occurrence_id,
        standing=CanonicalStanding.READY_AND_REPRODUCED,
        atom_count=len(atoms),
        derived_text=str(replay["canonical_text"]),
        note=THE_CONSUMED_FIELD_IS_DERIVED_FROM_THE_REPLAY,
    )
