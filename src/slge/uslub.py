"""الأسلوب: الخبرُ وحدَه يحتمل الصدقَ والكذب، والإنشاءُ يُقرأ من الخانة لا يُكتب باليد — مرآةُ `Uslub`.

الإنشاءُ طلبيٌّ (أمرٌ بصيغته، نهيٌ بلَا والجزم، استفهامٌ بأداته أو اسمه، نداءٌ بأداته، تمنٍّ بلَيْتَ، ترجٍّ
بلَعَلَّ) وغيرُ طلبيّ (تعجّبٌ بمَا أَفْعَلَ ومنصوب، مدحٌ وذمٌّ بنِعْمَ وبِئْسَ)؛ وما سواه خبر (`uslub`). الصدقُ
والكذبُ للخبر وحده (`truth_apt`). لَا تفصل النهيَ عن النفي بخانة آخر الفعل (لَا تَكْذِبْ / لَا تَكْذِبُ)،
ومَا أَفْعَلَ تعجّبٌ أو نفيٌ بخانة ما بعده. الأدواتُ جدولٌ حاصر (`TOOLS`). القياسُ على MASAQ في
`tools/gen_uslub_index.py`.
"""

from __future__ import annotations

from typing import Final

from slge.cells import STATES, Cell
from slge.istifham import FORMS as ISTIFHAM_FORMS
from slge.jiha import sigha
from slge.jumla import mubtada_kind
from slge.maqam import _on_template_root as on_template_root
from slge.nida import PARTICLES as NIDA_PARTICLES
from slge.rawabit import PARTICLES, cells_of
from slge.tawabi import case_class
from slge.zuruf import set_last

__all__ = ["LA", "MA", "TOOLS", "present_any_mood", "truth_apt", "uslub"]

_A, _I, _U, SUKUN = STATES
Word = tuple[Cell, ...]

LA: Final[Word] = cells_of("لَا")
MA: Final[Word] = cells_of("مَا")
LAYTA: Final[Word] = cells_of("لَيْتَ")
LAALLA: Final[Word] = cells_of("لَعَلَّ")
NIMA: Final[Word] = cells_of("نِعْمَ")
BISA: Final[Word] = cells_of("بِئْسَ")
ISTIFHAM_TOOLS: Final[tuple[Word, ...]] = ((("ء", _A),), cells_of("هَلْ"))
TOOLS: Final[tuple[tuple[str, Word, str], ...]] = (
    ("لَا", LA, "نهي"), ("أَ", (("ء", _A),), "استفهام"), ("هَلْ", cells_of("هَلْ"), "استفهام"),
    ("لَيْتَ", LAYTA, "تمنّ"), ("لَعَلَّ", LAALLA, "ترجّ"), ("مَا", MA, "تعجّب"),
    ("نِعْمَ", NIMA, "مدح وذمّ"), ("بِئْسَ", BISA, "مدح وذمّ"),
    *((p.name, p.cells, "نداء") for p in NIDA_PARTICLES),
)
INSHA: Final[tuple[str, ...]] = ("أمر", "نهي", "استفهام", "نداء", "تمنّ", "ترجّ", "تعجّب", "مدح وذمّ")


def truth_apt(u: str) -> bool:
    """الصدقُ والكذبُ للخبر وحده."""

    return u == "خبر"


def present_any_mood(w: Word) -> bool:
    return bool(w) and sigha(set_last(w, _U)) == "مضارع"


def uslub(prev: Word, w: Word, nxt: Word | None = None) -> str:
    """الأسلوبُ من الكلمة وما قبلها وما بعدها (انظر `Uslub.uslub`)."""

    if sigha(w) == "أمر":
        return "أمر"
    if prev == LA and present_any_mood(w):
        return "نهي" if w[-1][1] == SUKUN else "خبر"
    if prev == MA and on_template_root(11, w):
        if nxt is None:
            return "—"
        return "تعجّب" if case_class(nxt) == "نصب" else "خبر"
    if prev in ISTIFHAM_TOOLS or (any(f.cells == prev for f in ISTIFHAM_FORMS) and prev != MA):
        return "استفهام"
    if any(p.cells == prev for p in NIDA_PARTICLES):
        return "نداء"
    if prev == LAYTA:
        return "تمنّ"
    if prev == LAALLA:
        return "ترجّ"
    if w in (NIMA, BISA):
        return "مدح وذمّ"
    if sigha(w) is not None or present_any_mood(w) or mubtada_kind(w) != "—":
        return "خبر"
    return "—"


def _check() -> None:
    from slge.jazm import sukun
    from slge.majrurat import jarr
    from slge.marifa import al
    from slge.nawasikh import nasb, tanwin

    names = {p.name: p for p in PARTICLES}
    assert names["لَا"].cells == LA and names["هَلْ"].amal == ""
    assert names["لَيْتَ"].amal.startswith("نصب الاسم") and names["لَعَلَّ"].amal == names["لَيْتَ"].amal
    assert len(TOOLS) == 14 and all(truth_apt(u) == (u == "خبر") for u in (*INSHA, "خبر", "—"))
    taktub, akrama, rajul = cells_of("تَكْتُبُ"), cells_of("أَكْرَمَ"), cells_of("رَجُلُ")
    assert uslub((), cells_of("اُكْتُبْ")) == "أمر"
    assert uslub(LA, sukun(taktub)) == "نهي" and uslub(LA, taktub) == "خبر"
    assert uslub(cells_of("هَلْ"), taktub) == "استفهام" and uslub(cells_of("يَا"), rajul) == "نداء"
    assert uslub(LAYTA, cells_of("زَيْدًا")) == "تمنّ" and uslub(LAALLA, cells_of("زَيْدًا")) == "ترجّ"
    assert uslub(MA, akrama, tanwin(nasb(rajul))) == "تعجّب"
    assert uslub(MA, akrama, cells_of("زَيْدٌ")) == "خبر"
    assert uslub((), NIMA) == "مدح وذمّ" and uslub((), cells_of("كَتَبَ")) == "خبر"
    assert uslub((), al(rajul)) == "خبر" and uslub((), LA) == "—"
    assert uslub((), jarr(rajul)) == "—"  # مجرورٌ لا يبتدئ به
    assert truth_apt(uslub(LA, taktub)) and not truth_apt(uslub(LA, sukun(taktub)))


_check()
