"""الموزِّع: توقّعاتٌ مستقلّةٌ عن الشيفرة (المبنيُّ من جدوله بسوابقه ولاحقته ويُردّ بعينه؛ الحاملُ لا يُقرأ
وحدَه؛ التعديلاتُ مسمّاة؛ ما ليس في الجدول لا يُقرأ)، وطفراتٌ مرفوضة."""

from __future__ import annotations

from slge.cells import licensed
from slge.rawabit import cells_of
from slge.tawzi import HOSTS, KINDS, TABLE, VARIANTS, alif_to_ya, junction, restore, tawzi


def test_table_is_the_union_of_deposited_tables_without_duplicates() -> None:
    assert len(TABLE) == 246 and len(HOSTS) == 7
    assert len({w for _, _, w in TABLE}) == len(TABLE) and all(licensed(w) for _, _, w in TABLE)
    assert {k for k, _, _ in TABLE} == set(KINDS) and all(k == "حرف" for k, _, _ in HOSTS)
    assert not {w for _, _, w in HOSTS} & {w for _, _, w in TABLE}  # الحاملُ ليس مبنيًّا قائمًا بنفسه


def test_reads_particles_pronouns_and_adverbs_with_clitics_and_restores() -> None:
    for word, pre, name, suf, variant in (
        ("عَلَيْهِمْ", "", "عَلَى", "هم", "ALIF_TO_YA"),
        ("وَإِذَا", "و", "إِذَا", "", ""),
        ("بِمَا", "ب", "مَا", "", ""),
        ("مِنْهُمْ", "", "مِنْ", "هم", ""),
        ("إِنَّهُ", "", "إِنَّ", "ه", ""),
        ("فَلَمَّا", "ف", "لَمَّا", "", ""),
        ("بِهِ", "", "بِ", "ه", ""),
        ("لَكُمْ", "", "لِ", "كم", "LAM_FATHA"),
        ("مِنَ", "", "مِنْ", "", "JUNCTION_FATHA"),
        ("عَنِ", "", "عَنْ", "", "JUNCTION_KASRA"),
    ):
        w = cells_of(word)
        ms = tawzi(w)
        assert ms and all(restore(m) == w for m in ms), word
        assert any(m.name == name and "".join(k for p in m.pre for k, _ in p) == pre
                   and "".join(k for k, _ in m.suf) == suf and m.variant == variant
                   for m in ms), (word, ms)


def test_template_words_and_bare_hosts_are_not_read_here() -> None:
    assert not tawzi(cells_of("كَتَبَ")) and not tawzi(cells_of("ذَهَبَ"))
    assert not tawzi(cells_of("بِ")) and not tawzi(cells_of("لِ"))  # الحاملُ يحتاج لاحقة
    assert not tawzi(cells_of("مَعَ"))  # ليس في جداولنا — باسمه، لا من الذاكرة


def test_variants_are_named_and_minimal_and_mutants() -> None:
    assert VARIANTS == ("", "ALIF_TO_YA", "LAM_FATHA", "JUNCTION_KASRA", "JUNCTION_FATHA")
    assert alif_to_ya(cells_of("إِلَى")) == cells_of("إِلَيْ")
    assert alif_to_ya(cells_of("عَنْ")) == cells_of("عَنْ")
    k, f = junction(cells_of("عَنْ"))
    assert k == cells_of("عَنِ") and f == cells_of("عَنَ")
    assert junction(cells_of("إِذَا")) == (cells_of("إِذَا"), cells_of("إِذَا"))  # لا ساكنَ في الآخر
    # طفرة: الألفُ لا تصير ياءً بلا لاحقة (عَلَيْ وحدَها لا تُقرأ عَلَى)
    assert not any(m.name == "عَلَى" for m in tawzi(cells_of("عَلَيْ")))
    # طفرة: لاحقةٌ ليست من جدول الضمائر لا تُقطع
    assert not tawzi(cells_of("مِنْزَ"))
