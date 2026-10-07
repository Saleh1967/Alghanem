"""الأدواتُ علاقاتٍ تشغيليّة: صورةٌ، رتبةٌ، أصنافُ معمولات، عملٌ دالّةً، ونوعُ علاقةٍ معلَن — مرآةُ `Adawat`.

كلُّ أداةٍ من `huruf.TABLE` (68) على بنيةٍ واحدة (`Adat`): رتبتُها وأصنافُ معمولاتها وعملُها دالّةً على خانة
آخر معمولها (`apply`؛ مرخَّصٌ على المعرب: `apply_licensed`، والجزمُ `apply_jazm_licensed`) ونوعُ علاقتها
(`REL`: معلَنٌ من كتب حروف المعاني — الخاناتُ لا تحمل معنى، فلا جداولَ صدقٍ هنا). التركيبُ بعينه والكفُّ
(`compositions`: كَأَنَّ، أَلَا، أَمَا، لِكَيْ، كَيْلَا، إِنَّمَا بلا عمل). والأداةُ المجاورة ترتّب قراءاتِ جارتها
بصنف معمولها الأوّل ولا تُسقط قراءةً (`rank`؛ `mem_rank`، `length_rank`). القياسُ على قسمة MASAQ
المحجوبة في `tools/gen_adawat_index.py`.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Final

from slge.cells import Cell
from slge.fil import MAZID_AMR
from slge.huruf import TABLE, Harf
from slge.jazm import sukun
from slge.jidh import Reading
from slge.jumla import VERB_TEMPLATES
from slge.majrurat import jarr
from slge.nawasikh import nasb
from slge.zuruf import set_last

__all__ = ["DECLARED", "TABLE_ADAWAT", "Adat", "apply", "cat_of", "fits", "of_cells", "rank"]

Word = tuple[Cell, ...]
ISM, FIL, JUMLA, AY = "اسم", "فعل", "جملة", "أيّ"


@dataclass(frozen=True, slots=True)
class Adat:
    harf: Harf
    arity: int
    args: tuple[str, ...]
    rel: str


DECLARED: Final[tuple[tuple[int, tuple[str, ...], str], ...]] = (
    *((1, (ISM,), "تعدية") for _ in range(13)),
    *((1, (ISM,), "استثناء") for _ in range(3)),
    (1, (ISM,), "تقليل"),
    (2, (ISM, AY), "توكيد"), (2, (ISM, AY), "توكيد"), (2, (ISM, AY), "تشبيه"),
    (2, (ISM, AY), "استدراك"), (2, (ISM, AY), "تمنٍّ"), (2, (ISM, AY), "ترجٍّ"),
    *((1, (ISM,), "نداء") for _ in range(6)),
    (2, (ISM, AY), "نفي"),
    (1, (ISM,), "معيّة"),
    (1, (FIL,), "مصدريّة"), (1, (FIL,), "نفي"), (1, (FIL,), "مصدريّة"), (1, (FIL,), "جزاء"),
    (1, (FIL,), "مصدريّة"), (1, (FIL,), "مصدريّة"), (1, (FIL,), "مصدريّة"), (1, (FIL,), "مصدريّة"),
    (1, (FIL,), "نفي"), (1, (FIL,), "نفي"), (1, (FIL,), "أمر"), (1, (FIL,), "نهي"),
    (2, (FIL, FIL), "شرط"), (2, (FIL, FIL), "شرط"),
    (1, (FIL,), "تنفيس"), (1, (FIL,), "تنفيس"), (1, (JUMLA,), "ردع"), (1, (FIL,), "تحقيق"),
    (2, (AY, AY), "جمع"), (2, (AY, AY), "ترتيب وتعقيب"), (2, (AY, AY), "ترتيب وتراخٍ"),
    (2, (AY, AY), "غاية"), (2, (AY, AY), "تخيير"), (2, (AY, AY), "تخيير"), (2, (AY, AY), "نفي"),
    (2, (AY, AY), "إضراب"), (2, (AY, AY), "استدراك"),
    (1, (JUMLA,), "استفهام"), (1, (JUMLA,), "استفهام"), (1, (JUMLA,), "نفي"), (1, (JUMLA,), "نفي"),
    (1, (FIL,), "نفي"), (1, (FIL,), "نفي"), (1, (JUMLA,), "نفي"), (1, (JUMLA,), "نفي"),
    (1, (JUMLA,), "استفتاح"), (1, (JUMLA,), "استفتاح"),
)
"""الأعمدةُ المعلَنة بترتيب `huruf.TABLE`: (الرتبة، أصنافُ المعمولات، نوعُ العلاقة) — معلَن."""

TABLE_ADAWAT: Final[tuple[Adat, ...]] = tuple(
    Adat(h, n, args, rel) for h, (n, args, rel) in zip(TABLE, DECLARED, strict=True)
)

_AMR: Final[tuple[int, ...]] = (8, 9, 10, 113, *MAZID_AMR)
"""قوالبُ الأمر (`Filiyya.amrTemplates`)."""


def apply(a: Adat, w: Word) -> Word:
    """العمل: الجرُّ كسرٌ، نصبُ الاسم ونصبُ المضارع فتحٌ، الجزمُ سكونٌ؛ وما لا عملَ له يعيد معمولَه
    (`apply`)."""

    if a.harf.amal == "جرّ":
        return jarr(w)
    if a.harf.amal == "نصب الاسم":
        return nasb(w)
    if a.harf.amal == "نصب الفعل":
        return set_last(w, "فتح")
    if a.harf.amal in ("جزم", "جزم فعلين"):
        return sukun(w)
    return w


def cat_of(rd: Reading) -> str:
    """صنفُ القراءة من قوالبها: فعلٌ إن كان فيها قالبُ فعل، وإلّا اسم (`catOf`)."""

    return FIL if any(k in VERB_TEMPLATES or k in _AMR for k in rd.templates) else ISM


def fits(a: Adat, rd: Reading) -> bool:
    """القراءةُ توافق الأداة: صنفُها صنفُ معمولها الأوّل، أو المعمولُ جملةٌ أو أيُّ شيء (`fits`)."""

    first = a.args[0] if a.args else AY
    return first in (AY, JUMLA) or cat_of(rd) == first


def rank(a: Adat, rs: tuple[Reading, ...]) -> tuple[Reading, ...]:
    """الموافقُ أوّلًا ثمّ الباقي بترتيبه — لا تسقط قراءة (`rank`)."""

    return (*(r for r in rs if fits(a, r)), *(r for r in rs if not fits(a, r)))


def of_cells(w: Word) -> Adat | None:
    """الأداةُ من صورتها: أوّلُ مدخلٍ صورتُه الكلمة (`ofCells`)."""

    return next((a for a in TABLE_ADAWAT if a.harf.cells == w), None)


def _check() -> None:
    from slge.cells import licensed
    from slge.jidh import jidh
    from slge.rawabit import cells_of

    assert len(TABLE_ADAWAT) == 68 and all(len(a.args) == a.arity for a in TABLE_ADAWAT)
    for a in TABLE_ADAWAT:  # العاملُ في الاسم معمولُه الأوّل اسم، وفي الفعل فعل، والعاطفُ ثنائيّ
        if a.harf.amal in ("جرّ", "نصب الاسم", "نداء", "معيّة"):
            assert a.args[0] == ISM, a
        elif a.harf.amal in ("نصب الفعل", "جزم", "جزم فعلين"):
            assert a.args[0] == FIL, a
        elif a.harf.amal == "تبعيّة":
            assert a.arity == 2, a
    lam, inna = of_cells(cells_of("لَمْ")), of_cells(cells_of("إِنَّ"))
    assert lam is not None and inna is not None
    jazm = apply(lam, cells_of("يَكْتُبُ"))
    assert jazm == cells_of("يَكْتُبْ") and licensed(jazm)
    assert apply(inna, cells_of("كِتَابُ")) == cells_of("كِتَابَ")
    assert apply(of_cells(cells_of("فِي")) or inna, cells_of("كِتَابُ")) == cells_of("كِتَابِ")
    rs = jidh(cells_of("فَرِيقٌ"))
    assert [(fits(inna, r), r.templates) for r in rank(inna, rs)] == [(True, (53,)), (True, (121,))]
    assert len(rank(lam, rs)) == len(rs) and set(rank(lam, rs)) == set(rs)
    assert [fits(lam, r) for r in rank(lam, rs)] == [False, False]  # لَمْ لا تقبل اسمًا — ولا تُسقطه
    assert cat_of(jidh(cells_of("وَجَدَ"))[0]) == FIL and of_cells(cells_of("كِتَابٌ")) is None


_check()
