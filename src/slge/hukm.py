"""الحكم: من جذور الشهادة إلى ركنٍ من السلسلة بمرتبته وشاهده، أو «لا حكم» — مرآةُ `Slge.Hukm`
(ADR ٣٤).

أوّلُ دالّةِ حكمٍ تستهلك جدولَ السلسلة (`salsala`) ومودَعَ المعلومات السابقة (`ajnas_table`: الأجناسُ
والقابليّاتُ من المخصّص بشاهدها). المدخلُ جذورُ قراءات الشهادة (رموزُ جدول المقاييس كما يقرؤها الجذع)؛
والمخرجُ لكلّ جذرٍ حكمان على ركنَي السلّم الأوّل: **الأجناسُ والأنواع** (4: الجذرُ اسمُ كتابٍ — شاهدُه
الكتاب) و**القابليّات** (7: الجذرُ في عنوان عقدةٍ تحت كتاب — شاهدُه العقدة)، كلٌّ «مفهومٌ» بشاهدٍ من المودَع
أو «معلومةٌ» بلا شاهد؛ ولا جذرَ فـ«لا حكم». لا يُسقط جذرًا ولا يزيد (`hukm_length`، `hukm_mem`)، ولا
«مفهوم» بلا شاهدٍ عقدةٍ من الشجرة (`qabiliyya_witness_in_tree`)، ولا يمسّ الشهادة
(`shahada_untouched`). طبقةُ «الحكم» فوق السُّلَّم (المادّة ١٠): تقرأ الشهادةَ ولا تمسّها.
"""

from __future__ import annotations

from collections.abc import Sequence
from dataclasses import dataclass
from typing import Final

from slge.ajnas_table import GENERA
from slge.cells import Cell
from slge.madlul_table import TAGS
from slge.maqayis import code_of_root, roots_of
from slge.qiraa import hukm_readings
from slge.salsala_table import GRADES, ROWS

__all__ = [
    "JINS",
    "LA_HUKM",
    "MAFHUM",
    "MALUMAH",
    "MANA",
    "QABILIYYA",
    "Judgement",
    "Row",
    "accepted",
    "hukm",
    "hukm_of_form",
    "judge_jins",
    "judge_qabiliyya",
    "judge_root",
    "lafz_witness",
    "rank",
    "roots_of_form",
    "tag_of",
]

JINS: Final[int] = 4
QABILIYYA: Final[int] = 7
MAFHUM: Final[str] = "مفهوم"
MALUMAH: Final[str] = "معلومة"
LA_HUKM: Final[str] = "لا حكم"
Word = tuple[Cell, ...]


@dataclass(frozen=True)
class Judgement:
    """(الركن، اسمُه، مرتبتُه من جدول السلسلة، الشاهدُ من المودَع أو لا شيء)."""

    rukn: int
    witness: int | None

    @property
    def name(self) -> str:
        return ROWS[self.rukn][2]

    @property
    def grade(self) -> str:
        """المرتبةُ من جدول السلسلة نفسِه (`gradeOf`)."""

        return GRADES[ROWS[self.rukn][3]]

    @property
    def kind(self) -> str:
        return MAFHUM if self.witness is not None else MALUMAH


Row = tuple[int, Judgement, Judgement]
"""(الجذر، حكمُ الجنس، حكمُ القابليّة)."""


MANA: Final[str] = "مدلول اللفظ معنى"
"""القسمُ الأوّل من ج3 409: «أن يكون مدلول اللفظ معنى» (`Nabhani.Madlul.mana`)."""


def tag_of(book: int) -> str | None:
    """قسمُ الجنس من جدول المالك (`tagOf`)؛ لا شيء = لم يُوقَّع أو «ليس جنسًا»."""

    return TAGS.get(book)


def accepted(book: int) -> bool:
    """الجنسُ المقبولُ شاهدًا للركن 4: ما مدلولُه معنى وحدَه (`accepted`، ADR ٣٥)."""

    return tag_of(book) == MANA


def judge_jins(r: int) -> Judgement:
    """الجنس: أوّلُ كتابٍ مقبولٍ جذورُ عنوانه تحمل الجذر (`judgeJins`)."""

    for book, _, roots, _ in GENERA:
        if accepted(book) and r in roots:
            return Judgement(JINS, book)
    return Judgement(JINS, None)


def lafz_witness(r: int) -> int | None:
    """شاهدُ الدالّ: أوّلُ كتابٍ غيرِ مقبول جذورُ عنوانه تحمل الجذر (`lafzWitness`) — لا يُحكم به."""

    for book, _, roots, _ in GENERA:
        if not accepted(book) and r in roots:
            return book
    return None


def judge_qabiliyya(r: int) -> Judgement:
    """القابليّة: أوّلُ عقدةٍ شاهدةٍ في جدول القابليّات تحمل الجذر (`judgeQabiliyya`)."""

    for _, _, _, caps in GENERA:
        for root, witness in caps:
            if root == r:
                return Judgement(QABILIYYA, witness)
    return Judgement(QABILIYYA, None)


def judge_root(r: int) -> Row:
    return r, judge_jins(r), judge_qabiliyya(r)


def hukm(roots: Sequence[int]) -> list[Row] | None:
    """الحكمُ على جذور الشهادة: `None` = لا حكم (بلا جذر)، وإلّا لكلّ جذرٍ حكمُه بعدد الجذور (`hukm`)."""

    if not roots:
        return None
    return [judge_root(r) for r in roots]


def rank(rows: Sequence[Row]) -> list[Row]:
    """ما فيه مفهومٌ أوّلًا، ولا شيءَ يُحذف (`mem_rank`، `length_rank`)."""

    def has(x: Row) -> bool:
        return x[1].witness is not None or x[2].witness is not None

    return [x for x in rows if has(x)] + [x for x in rows if not has(x)]


def roots_of_form(w: Word) -> tuple[int, ...]:
    """جذورُ القراءة الموحَّدة رموزًا من جدول المقاييس — الجذعُ على الصورة ثمّ على أصلها المردود، ولا جذرَ
    لما قرأه الموزِّعُ حرفًا (`Qiraa.harf_no_hukm`، ADR ٤٢) — بترتيب القراءات وبلا تكرار؛ لا نصَّ هنا."""

    out: list[int] = []
    for q in hukm_readings(w):
        for r in roots_of(q.r):
            c = code_of_root(r)
            if c is not None and c not in out:
                out.append(c)
    return tuple(out)


def hukm_of_form(w: Word) -> list[Row] | None:
    """حكمُ الصورة: جذورُها من الجذع ثمّ `hukm` مرتَّبًا — والشهادةُ لا تُمسّ."""

    h = hukm(roots_of_form(w))
    return None if h is None else rank(h)


def _check() -> None:
    assert ROWS[JINS][2] == "الأجناس والأنواع" and ROWS[QABILIYYA][2] == "القابليّات"
    assert judge_jins(22018) == Judgement(JINS, 163 if accepted(163) else None)
    assert accepted(163) or lafz_witness(22018) == 163
    assert judge_qabiliyya(24998) == Judgement(QABILIYYA, 2)
    assert judge_jins(24998).witness is None and judge_jins(22018).grade == "ظنّ"
    assert hukm([]) is None and len(hukm([22018, 24998]) or []) == 2
    assert rank([judge_root(5), judge_root(22018)])[0][0] == 22018


_check()
