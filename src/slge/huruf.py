"""الحروفُ والأدوات: جدولٌ واحدٌ يجمع المودَعات، وعملُها عمليّاتٌ في أبوابها — مرآةُ `Huruf.lean`.

ثلاثُ مجموعات: المختصّةُ بالأسماء (الجرُّ `majrurat`، نصبُ الاسم `nawasikh`، النداءُ `nida`، المعيّة)،
المختصّةُ بالأفعال (النواصبُ، الجوازمُ `jazm`، حرفا الشرط، التنفيسُ والردعُ والتحقيق)، والمشتركةُ (العطفُ
بالتبعيّة `tawabi`، الاستفهامُ، النفيُ، الاستفتاح). الحرفُ صورةٌ مودَعةٌ لا تنوينَ فيها (وما نونُه أصلٌ
ساكنٌ بعد حركةٍ تشابه التنوين: مسمًّى)، وعملُه عمليّةٌ على ما بعده. 68 مدخلًا على 53 صورةً: الخانةُ
الواحدةُ في أكثرَ من بابٍ، والعملُ من التيار. القياسُ على MASAQ في `tools/gen_huruf_index.py`.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Final

from slge.cells import Cell, licensed
from slge.jazm import JAZIM_ONE
from slge.majrurat import HARFS
from slge.nawasikh import INNA, LA
from slge.nida import PARTICLES as NIDA
from slge.rawabit import cells_of
from slge.tawabi import NASAQ

__all__ = ["TABLE", "Harf", "by_cells", "shared"]


@dataclass(frozen=True, slots=True)
class Harf:
    name: str
    cells: tuple[Cell, ...]
    cls: str  # "اسم" | "فعل" | "مشترك"
    amal: str  # جرّ | نصب الاسم | نداء | معيّة | نصب الفعل | جزم | جزم فعلين | تبعيّة | "" (بلا عمل)


def _h(name: str, text: str, cls: str, amal: str) -> Harf:
    return Harf(name, cells_of(text), cls, amal)


ISM: Final[tuple[Harf, ...]] = (
    *(_h(w, w, "اسم", "جرّ") for w in HARFS),
    *(_h(w, w, "اسم", "نصب الاسم") for w in INNA),
    *(Harf(p.name, p.cells, "اسم", "نداء") for p in NIDA),
    _h("لَا (النافية للجنس)", LA, "اسم", "نصب الاسم"), _h("وَ (المعيّة)", "وَ", "اسم", "معيّة"),
)
FIL: Final[tuple[Harf, ...]] = (
    _h("أَنْ", "أَنْ", "فعل", "نصب الفعل"), _h("لَنْ", "لَنْ", "فعل", "نصب الفعل"),
    _h("كَيْ", "كَيْ", "فعل", "نصب الفعل"), _h("إِذَنْ", "إِذَنْ", "فعل", "نصب الفعل"),
    _h("لِ (كي/الجحود)", "لِ", "فعل", "نصب الفعل"), _h("حَتَّى (النصب)", "حَتَّى", "فعل", "نصب الفعل"),
    _h("فَ (السببيّة)", "فَ", "فعل", "نصب الفعل"), _h("وَ (المعيّة)", "وَ", "فعل", "نصب الفعل"),
    *(_h(w, w, "فعل", "جزم") for w in JAZIM_ONE),
    _h("إِنْ", "إِنْ", "فعل", "جزم فعلين"), _h("إِذْمَا", "إِذْمَا", "فعل", "جزم فعلين"),
    _h("سَ", "سَ", "فعل", ""), _h("سَوْفَ", "سَوْفَ", "فعل", ""), _h("كَلَّا", "كَلَّا", "فعل", ""),
    _h("قَدْ", "قَدْ", "فعل", ""),
)
MUSHTARAK: Final[tuple[Harf, ...]] = (
    *(_h(w, w, "مشترك", "تبعيّة") for w in NASAQ),
    _h("أَ", "أَ", "مشترك", ""), _h("هَلْ", "هَلْ", "مشترك", ""), _h("مَا", "مَا", "مشترك", ""),
    _h("لَا", "لَا", "مشترك", ""), _h("لَمْ", "لَمْ", "مشترك", "جزم"),
    _h("لَنْ", "لَنْ", "مشترك", "نصب الفعل"),
    _h("إِنْ (النفي)", "إِنْ", "مشترك", ""), _h("لَاتَ", "لَاتَ", "مشترك", ""),
    _h("أَلَا", "أَلَا", "مشترك", ""), _h("أَمَا", "أَمَا", "مشترك", ""),
)
TABLE: Final[tuple[Harf, ...]] = (*ISM, *FIL, *MUSHTARAK)


def by_cells(cells: tuple[Cell, ...]) -> tuple[Harf, ...]:
    """كلُّ المداخل التي خانتُها هذه: الخانةُ الواحدة في أكثرَ من باب."""

    return tuple(x for x in TABLE if x.cells == cells)


def shared() -> dict[tuple[Cell, ...], tuple[str, ...]]:
    out: dict[tuple[Cell, ...], list[str]] = {}
    for x in TABLE:
        out.setdefault(x.cells, []).append(x.name)
    return {k: tuple(v) for k, v in out.items() if len(v) > 1}


def _check() -> None:
    assert len(ISM) == 31 and len(FIL) == 18 and len(MUSHTARAK) == 19 and len(TABLE) == 68
    assert all(licensed(x.cells) for x in TABLE)
    assert len({x.cells for x in TABLE}) == 53
    assert len(by_cells(cells_of("لَا"))) == 4 and len(by_cells(cells_of("وَ"))) == 4
    assert len(by_cells(cells_of("حَتَّى"))) == 3 and len(by_cells(cells_of("إِنْ"))) == 2


_check()
