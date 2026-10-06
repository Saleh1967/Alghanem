"""المتباين: مادّتان لا تلتقيان — والأصلُ في الوضع التباين — مرآةُ `Tabayun`.

المادّةُ على الخانات جذرُ الكلمة بقالبٍ يقرؤها (`key`)، وموادُّها جذورُها بكلّ قالبٍ قارئ (`mawadd`).
الحصرُ السباعيُّ باعتبار الدالّ والمدلول يُقرأ بعدد الكلمات وعدد الموادّ: منفردٌ، مشترك، متّحدا المادّة
(ترادفُ صورة)، متباينان (`tabayun`: لا مادّةَ بينهما — متماثلٌ غيرُ انعكاسيّ
`tabayun_symm`/`tabayun_irrefl`)، ومتداخلان — قسمٌ ثامن تقرؤه الخانة (`seven_not_exhaustive`).
الأصلُ في الوضع التباين: على القالب المعزول (77 من الـ121 `isolated_count`) جذران مختلفان كلمتان
متباينتان على قالبٍ واحد (`tabayun_of_isolated`). القياسُ على MASAQ في `tools/gen_tabayun_index.py`.
"""

from __future__ import annotations

from typing import Final

from slge.cells import Cell
from slge.marifa import drop_tanwin
from slge.wad import may_collide, senses
from slge.wazn import AWZAN, root_of

__all__ = ["isolated", "key", "mawadd", "rel", "share_madda", "tabayun"]

Word = tuple[Cell, ...]
Key = tuple[str, str, str] | None
_TEMPLATES: Final[tuple[tuple[object, ...], ...]] = tuple(w.template for w in AWZAN)


def key(q: int, w: Word) -> Key:
    """مادّةُ الكلمة بقالبٍ: جذرُها المستخرَج."""

    return root_of(AWZAN[q].template, w)


def mawadd(w: Word) -> tuple[Key, ...]:
    """موادُّ الكلمة: جذورُها بكلّ قالبٍ يقرؤها."""

    return tuple(key(q, w) for q in senses(w))


def share_madda(a: Word, b: Word) -> bool:
    mb = mawadd(b)
    return any(m in mb for m in mawadd(a))


def tabayun(a: Word, b: Word) -> bool:
    """متباينان: كلمتان مختلفتان ذواتا مادّةٍ لا مادّةَ بينهما."""

    return a != b and bool(mawadd(a)) and bool(mawadd(b)) and not share_madda(a, b)


def isolated(k: int) -> bool:
    """القالبُ المعزول: لا يلتقي بقالبٍ غيرِ مطابقٍ له."""

    return all(not may_collide(AWZAN[k].template, AWZAN[q].template)
               or AWZAN[q].template == AWZAN[k].template for q in range(len(AWZAN)))


def rel(a: Word, b: Word) -> str:
    """علاقةُ كلمتين بعد ردّ التنوين: كلمةٌ واحدة (منفردٌ بمادّة، مشتركٌ بمادّتين)، أو كلمتان (متّحدتا
    المادّة، متباينتان، متداخلتان)، أو لا يُقرأ."""

    a, b = drop_tanwin(a), drop_tanwin(b)
    ma, mb = set(mawadd(a)), set(mawadd(b))
    if not ma or not mb:
        return "—"
    if a == b:
        return "منفرد" if len(ma) == 1 else "مشترك"
    if not ma & mb:
        return "متباينان"
    if ma == mb:
        return "متّحدا المادّة"
    return "متداخلان"


def _check() -> None:
    from slge.rawabit import cells_of
    from slge.wazn import fill

    assert sum(isolated(k) for k in range(len(AWZAN))) == 77
    for k in (0, 29, 35, 48):
        assert isolated(k)
        w1, w2 = fill(AWZAN[k].template, ("ك", "ت", "ب")), fill(AWZAN[k].template, ("د", "ر", "س"))
        assert tabayun(w1, w2) and tabayun(w2, w1) and not tabayun(w1, w1)
        assert mawadd(w1) == (("ك", "ت", "ب"),) * len(mawadd(w1))
    darb, qatl = cells_of("ضَرْبٌ"), cells_of("قَتْلٌ")
    assert rel(darb, qatl) == "متباينان" and rel(qatl, darb) == "متباينان"
    assert rel(darb, cells_of("ضِرَابٌ")) == "متّحدا المادّة"
    assert rel(cells_of("اِنْتِشَارٌ"), cells_of("نَشْرٌ")) == "متداخلان"  # القسمُ الثامن
    assert rel(cells_of("كِتَابٌ"), cells_of("كِتَابٌ")) == "منفرد"
    assert rel(cells_of("اِنْتِشَارٌ"), cells_of("اِنْتِشَارٌ")) == "مشترك"
    assert rel(cells_of("لَا"), darb) == "—"


_check()
