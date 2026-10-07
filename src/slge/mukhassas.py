"""شجرةُ المخصّص: الأجناسُ والقابليّاتُ معلوماتٍ سابقةً، والحكمُ عليها بشاهد — مرآةُ `Slge.Mukhassas`.

أوّلُ وحدةٍ في طبقة «الحكم» فوق سُلَّم الترخيص (المادّة ١٠): لا تدخل السُّلَّم ولا تمسّ شهادة. الجدولُ
`mukhassas_table.NODES` مولَّدٌ من المختوم (`tools/deposit_mukhassas.py`): العقدةُ (معرّف، مستوى، أب،
عنوان، جذورُ العنوان بالرسم، كتاب). الحكمُ على (عقدة، جذر) مرتبتان: «مفهوم» بشاهدٍ عقدةٍ في الكتاب نفسه
يحمل عنوانُها الجذر، أو «معلومة» بلا شاهد — ولا رفضَ ولا امتناع (المادّتان ١٣ و١٦).
"""

from __future__ import annotations

from typing import Final

from slge.maqayis import Root, _code, _matches_l, decode
from slge.maqayis_table import ROOTS
from slge.mukhassas_table import BOOKS, NODES

__all__ = ["BOOKS", "MAFHUM", "MALUMAH", "NODES", "book_of", "caps_under", "code_of_root", "judge",
           "level_of", "roots_of", "title_of"]

MAFHUM: Final[str] = "مفهوم"
MALUMAH: Final[str] = "معلومة"
_CODES: Final[tuple[tuple[int, int, int], ...]] = tuple(decode(n) for n in ROOTS)


def level_of(i: int) -> int:
    return NODES[i][1]


def title_of(i: int) -> str:
    return NODES[i][3]


def roots_of(i: int) -> tuple[int, ...]:
    return NODES[i][4]


def book_of(i: int) -> int:
    return NODES[i][5]


def caps_under(b: int) -> tuple[int, ...]:
    """القابليّاتُ الموروثة للكتاب: اتّحادُ جذور عناوين ما تحته (`capsUnder`)."""

    return BOOKS.get(b, ())


def code_of_root(r: Root) -> int | None:
    """رمزُ جذرٍ من الخانات في ترميز جدول المقاييس، أو لا شيء إن لم يكن فيه."""

    a, b, d = _code(r)
    for ta, tb, td in _CODES:
        if _matches_l(ta, a) and _matches_l(tb, b) and _matches_l(td, d):
            return ta * 900 + tb * 30 + td
    return None


def judge_in(b: int, r: int) -> tuple[str, int | None]:
    """أوّلُ عقدةٍ في الكتاب يحمل عنوانُها الجذر شاهدًا، وإلّا معلومة (`judgeIn`)."""

    for n in NODES:
        if n[5] == b and r in n[4]:
            return MAFHUM, n[0]
    return MALUMAH, None


def judge(n: int, r: int) -> tuple[str, int | None]:
    """الحكمُ على (عقدة، رمزُ جذر) داخل كتاب العقدة (`judge`)."""

    return judge_in(book_of(n), r)


def _check() -> None:
    assert len(NODES) == 1600 and sum(1 for n in NODES if n[4]) == 1080 and len(BOOKS) == 73
    assert all(n[0] == i for i, n in enumerate(NODES))
    assert all(n[2] < n[0] for n in NODES) and all((n[1] == 1) == (n[2] == -1) for n in NODES)
    assert judge_in(163, 22018) == (MAFHUM, 163) and judge_in(1, 22018) == (MALUMAH, None)
    assert judge_in(979, 4829) == (MALUMAH, None)
    assert code_of_root(("م", "ش", "ي")) == 22018 and code_of_root(("ج", "ر", "ي")) == 4829
    g, w = judge(980, 4829)
    assert g == MALUMAH and w is None


_check()
