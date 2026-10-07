"""القرينةُ المعجميّة: عضويّةُ الجذر في مقاييس اللغة دالّةٌ على الخانات — مرآةُ `Maqayis`.

الجذعُ يعيد قراءاتٍ متعدّدة والتعدّدُ يُقرأ كما هو؛ والقرينةُ التي تفصله عضويّةُ جذر القراءة في جدولٍ مختوم
(مقاييسُ اللغة لابن فارس، 4,561 جذرًا ثلاثيًّا حواملَ في `maqayis_table`، مولَّدٌ من المودَع). العضويّةُ
دالّةٌ على الخانات لا بحثَ خارج الجدول (`member_sound`)، والعينُ أو اللامُ المعتلّةُ في الطبعة تطابق
الواوَ أو الياءَ لا غير (`matchesL_weak`)، والترتيبُ بالقرينة — المشهودُ أوّلًا — لا يُسقط قراءةً ولا يزيدها
(`mem_rank`، `length_rank`)، وقراءةٌ أصلُها على قالبٍ سليم بجذرٍ مشهود مشهودةٌ (`attested_of_member`).
الجدولُ يفصل ما لم يُشهَد ولا يختار بين مشهودَين (قَالَ: قول وقيل كلاهما في المقاييس — `rank_qala`).
القياسُ على مودَع شهادات المصحف وعلى قسمة MASAQ المحجوبة في `tools/gen_maqayis_index.py`.
"""

from __future__ import annotations

from typing import Final

from slge.cells import ALPHABET
from slge.jidh import Reading
from slge.maqayis_table import ROOTS, SHA256, WEAK
from slge.wazn import AWZAN, root_of

__all__ = ["ROOTS", "SHA256", "WEAK", "attested", "decode", "member", "rank", "roots_of"]

Root = tuple[str, str, str]


def decode(n: int) -> tuple[int, int, int]:
    """رمزُ الجدول ← حوامله الثلاثة (29 = معتلّة)."""

    return n // 900, n // 30 % 30, n % 30


def _matches_l(t: int, k: int) -> bool:
    """حاملُ الجدول يطابق حاملَ الجذر: بعينه، أو معتلّةٌ تطابق و/ي."""

    return k in (27, 28) if t == WEAK else t == k


def _code(r: Root) -> tuple[int, int, int]:
    return tuple(ALPHABET.index(x) for x in r)  # type: ignore[return-value]


_TABLE: Final[frozenset[tuple[int, int, int]]] = frozenset(decode(n) for n in ROOTS)


def member(r: Root) -> bool:
    """العضويّةُ: جذرٌ من الخانات في جدول المقاييس (`member`)."""

    a, b, d = _code(r)
    return any(_matches_l(ta, a) and _matches_l(tb, b) and _matches_l(td, d)
               for ta, tb, td in _TABLE)


def roots_of(rd: Reading) -> tuple[Root, ...]:
    """جذورُ القراءة: جذرُ أصلها على كلّ قالبٍ من قوالبها (`Reading.roots`)."""

    out = []
    for k in rd.templates:
        r = root_of(AWZAN[k].template, rd.asl)
        if r is not None:
            out.append(r)
    return tuple(out)


def attested(rd: Reading) -> bool:
    """قراءةٌ مشهودة: أحدُ جذورها في المقاييس (`attested`)."""

    return any(member(r) for r in roots_of(rd))


def rank(rs: tuple[Reading, ...]) -> tuple[Reading, ...]:
    """الترتيبُ بالقرينة: المشهودُ أوّلًا ثمّ الباقي، بترتيبه (`rank`)."""

    return (*(r for r in rs if attested(r)), *(r for r in rs if not attested(r)))


def _check() -> None:
    from slge.jidh import jidh
    from slge.rawabit import cells_of

    assert len(ROOTS) == 4561 and len(_TABLE) == 4561
    assert member(("ق", "و", "ل")) and member(("ق", "ي", "ل")) and member(("ك", "ت", "ب"))
    assert not member(("ذ", "ب", "و"))
    assert member(("ر", "م", "ي")) and member(("ر", "م", "و"))  # رمى: المعتلّةُ مجهولةُ العين
    rs = rank(jidh(cells_of("كَذَّبُو")))
    assert [(attested(r), r.al, r.templates) for r in rs] == [
        (True, 0, (12,)), (False, 2, (2,)), (False, 2, (0, 36)), (False, 2, (0, 36)),
        (False, 2, (2,)), (False, 2, (2,))]
    assert [attested(r) for r in rank(jidh(cells_of("قَالَ")))] == [True, True]


_check()
