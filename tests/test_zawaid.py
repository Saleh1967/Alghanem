"""الزوائد: توقّعاتٌ مستقلّةٌ عن الشيفرة (الحروفُ العشرة بترتيب الباب، الخاناتُ أربعون، الإلصاقُ يحفظ
الترخيص، القطعُ يردّ الأصل)، وطفراتٌ مرفوضةٌ باسمها."""

from __future__ import annotations

import pytest

from slge.cells import licensed
from slge.jidh import ENCLITICS, jidh
from slge.wujud import FIL, ont_of_reading
from slge.zawaid import (
    CELLS,
    KHAFIFA,
    LETTERS,
    MUDARAA,
    TA_TANITH,
    THAQILA,
    anith,
    has_tanwin_shape,
    tawkid,
)
from slge.zawaid_table import TABLE, WITNESSES
from slge.zuruf import set_last

TAQUL = (("ت", "فتح"), ("ق", "ضم"), ("و", "سكون"), ("ل", "ضم"))  # تَقُولُ
TARID = (("ت", "ضم"), ("ع", "سكون"), ("ر", "كسر"), ("ض", "ضم"))  # تُعْرِضُ
QALA = (("ق", "فتح"), ("ا", "سكون"), ("ل", "فتح"))  # قَالَ


def test_ten_letters_in_the_order_of_the_chapter() -> None:
    """«وهي عشرة أحرف»: الهمزة، الألف، الهاء، الياء، النون، التاء، السين، الميم، الواو، اللام."""

    assert LETTERS == ("ء", "ا", "ه", "ي", "ن", "ت", "س", "م", "و", "ل")
    assert len(CELLS) == 40 == len(set(CELLS))
    assert set(MUDARAA) == {"ء", "ن", "ي", "ت"} and set(MUDARAA) <= set(LETTERS)
    names = [row[0] for row in TABLE]
    assert names[0] == "الهمزة" and names[-1] == "اللام"
    assert "استفعل" in TABLE[6][3] and "مفعول" in TABLE[7][3]


def test_attachment_keeps_licence_and_peel_returns_the_stem() -> None:
    for w in (TAQUL, TARID, QALA):
        for heavy in (True, False):
            v = tawkid(w, heavy)
            assert licensed(v) and v[len(w):] == (THAQILA if heavy else KHAFIFA)
            assert v[:len(w)] == set_last(w, "فتح")
        a = anith(w)
        assert licensed(a) and a[-1:] == TA_TANITH and a[:-1] == set_last(w, "فتح")
    assert tawkid(TAQUL, True) == (("ت", "فتح"), ("ق", "ضم"), ("و", "سكون"), ("ل", "فتح"),
                                  ("ن", "سكون"), ("ن", "فتح"))


def test_light_nun_has_the_tanwin_cell() -> None:
    assert has_tanwin_shape(tawkid(TAQUL, False)) and not has_tanwin_shape(tawkid(TAQUL, True))
    assert has_tanwin_shape((("ك", "كسر"), ("ت", "فتح"), ("ا", "سكون"), ("ب", "ضم"), ("ن", "سكون")))


def test_reader_peels_the_nun_and_the_ta_on_a_verb() -> None:
    """يَفْعَلَنَّ وفَعَلَتْ: قراءةٌ لاحقتُها الزائدة وجهتُها فعل (`thaqila_read`، `taTanith_read`)."""

    assert THAQILA in ENCLITICS and TA_TANITH in ENCLITICS
    yaktubanna = (("ي", "فتح"), ("ك", "سكون"), ("ت", "ضم"), ("ب", "فتح"), *THAQILA)
    assert any(rd.suf == THAQILA and ont_of_reading(rd) == FIL for rd in jidh(yaktubanna))
    katabat = (("ك", "فتح"), ("ت", "فتح"), ("ب", "فتح"), *TA_TANITH)
    assert any(rd.suf == TA_TANITH and ont_of_reading(rd) == FIL for rd in jidh(katabat))
    with_obj = (*yaktubanna, ("ك", "ضم"), ("م", "سكون"))  # يَكْتُبَنَّكُمْ
    assert any(rd.suf[:2] == THAQILA and ont_of_reading(rd) == FIL for rd in jidh(with_obj))


def test_witnesses_are_the_chapter_quotes() -> None:
    words = [x for _, ws in WITNESSES for x in ws]
    assert len(words) == 48 and "تقولن" in words and "تعرضن" in words and "تتبعان" in words
    assert all(ch.startswith("هذا باب") for ch, _ in WITNESSES)


@pytest.mark.parametrize("mutant", [
    (("ن", "فتح"), ("ن", "فتح")),  # نَنَ: ليست الثقيلة
    (("ن", "سكون"), ("ن", "سكون")),  # ساكنان: غيرُ مرخَّص
])
def test_mutant_suffixes_are_not_the_nun(mutant: tuple[tuple[str, str], ...]) -> None:
    assert mutant != THAQILA and mutant not in ENCLITICS
    assert not licensed(set_last(TAQUL, "فتح") + mutant) or mutant[0][1] != "سكون"
