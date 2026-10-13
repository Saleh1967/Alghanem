"""الموزِّع: توقّعاتٌ مستقلّةٌ عن الشيفرة (المبنيُّ من جدوله بسوابقه ولاحقته ويُردّ بعينه؛ الحاملُ لا يُقرأ
وحدَه؛ التعديلاتُ مسمّاة؛ ما ليس في الجدول لا يُقرأ)، وطفراتٌ مرفوضة."""

from __future__ import annotations

import gzip
from functools import cache

from conftest import ROOT
from slge.cells import licensed
from slge.jidh import OBJECT_SUFFIXES, PROCLITICS
from slge.marifa import MAWSUL
from slge.qiraa import harf
from slge.rawabit import cells_of
from slge.tawzi import (
    _BABS,
    ANCHORS,
    GAP,
    HOSTS,
    KINDS,
    RULES,
    SOURCES,
    SUF_KASRA,
    TABLE,
    VARIANTS,
    alif_to_ya,
    is_base,
    junction,
    maana,
    maana_suffix,
    mim_damma,
    restore,
    tawzi,
    wasl_drop,
    wasm,
)


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
    # الثلاثةُ الأخيرة قواعدُ ADR ٥٢ المسجَّلةُ قبل الشيفرة بأسمائها
    assert VARIANTS == ("", "ALIF_TO_YA", "LAM_FATHA", "JUNCTION_KASRA", "JUNCTION_FATHA",
                        "MIM_DAMMA", "MA_COMPOUND", "WASL_DROP")
    assert alif_to_ya(cells_of("إِلَى")) == cells_of("إِلَيْ")
    assert alif_to_ya(cells_of("عَنْ")) == cells_of("عَنْ")
    k, f = junction(cells_of("عَنْ"))
    assert k == cells_of("عَنِ") and f == cells_of("عَنَ")
    assert junction(cells_of("إِذَا")) == (cells_of("إِذَا"), cells_of("إِذَا"))  # لا ساكنَ في الآخر
    # طفرة: الألفُ لا تصير ياءً بلا لاحقة (عَلَيْ وحدَها لا تُقرأ عَلَى)
    assert not any(m.name == "عَلَى" for m in tawzi(cells_of("عَلَيْ")))
    # طفرة: لاحقةٌ ليست من جدول الضمائر لا تُقطع
    assert not tawzi(cells_of("مِنْزَ"))


# — قواعدُ ADR ٥٢ والوسمُ المغلق —

RULE_WITNESSES = (
    # (الكلمة، القاعدة، الاسم، السوابق، اللاحقة) — مقروءةٌ باليد من المصحف والكتاب
    ("لَهُمُ", "MIM_DAMMA", "لِ", "", "همُ"),
    ("عَلَيْهِمُ", "MIM_DAMMA", "عَلَى", "", "همُ"),
    ("عَلَيْهِمِ", "MIM_KASRA", "عَلَى", "", "همِ"),
    ("لِي", "YA_SAKINA", "لِ", "", "يْ"),
    ("وَلِلَّذِينَ", "WASL_DROP", "الَّذِينَ", "ول", ""),
    ("فِيمَا", "MA_COMPOUND", "فِي", "", ""),
)


def _suf(m: object) -> str:
    return "".join(k + {"ضم": "ُ", "كسر": "ِ", "سكون": "ْ", "فتح": "َ"}[s][:1] if k == "م" or k == "ي"
                   else k for k, s in m.suf)  # type: ignore[attr-defined]


def test_rules_read_their_witnesses_and_only_with_the_rule() -> None:
    assert sorted(RULES) == ["MA_COMPOUND", "MIM_DAMMA", "MIM_KASRA", "WASL_DROP", "YA_SAKINA"]
    for word, rule, name, pre, suf in RULE_WITNESSES:
        w = cells_of(word)
        ms = [m for m in tawzi(w) if rule in (m.variant, m.suf_rule)]
        assert any(m.name == name and "".join(k for p in m.pre for k, _ in p) == pre
                   and _suf(m) == suf and restore(m) == w for m in ms), (word, ms)
        # طفرةُ الحذف: بلا القاعدة لا قراءةَ بها
        assert not any(rule in (m.variant, m.suf_rule) for m in tawzi(w, RULES - {rule})), word


def test_rule_functions_by_hand() -> None:
    assert mim_damma(cells_of("هُمْ")) == cells_of("هُمُ")
    assert mim_damma(cells_of("مِنْ")) == cells_of("مِنْ")  # لا ميمَ جمعٍ في الآخر
    assert wasl_drop(MAWSUL["الَّذِينَ"]) == MAWSUL["الَّذِينَ"][1:]  # الجدولُ يكتب همزةَ الوصل ءَ
    assert wasl_drop(cells_of("إِذَا")) == cells_of("إِذَا")
    # همزةُ الوصل لا تسقط بلا سابقة: لَّذِينَ وحدَها لا تُقرأ موصولًا
    assert not any(m.kind == "موصول" for m in tawzi(MAWSUL["الَّذِينَ"][1:]))


def test_hukm_readings_do_not_see_the_rules() -> None:
    """التسجيلُ المسبق: القواعدُ لا تمسّ قراءاتِ الحكم — `harf` بلا قاعدة."""

    assert not harf(cells_of("لَهُمُ")) and harf(cells_of("لَهُمْ"))
    for word, *_ in RULE_WITNESSES:
        assert all(is_base(m) for m in harf(cells_of(word)))


def test_closed_tag_parts_meanings_and_qism() -> None:
    w = cells_of("وَمِنْكُمْ")
    m = next(m for m in tawzi(w) if m.name == "مِنْ")
    t = wasm(m)
    assert [j.dawr for j in t.parts] == ["سابقة", "نواة", "لاحقة"] and t.qism == ("حرف",)
    assert tuple(c for j in t.parts for c in j.cells) == w
    pre, core, suf = t.parts
    assert any("العطف" in x for _, _, mm, _ in pre.babs for x in mm)  # وَ: وظيفةُ الربط من rawabit
    assert any("ابتداء الغاية" in x for _, _, mm, _ in core.babs for x in mm)  # مِنْ: من ج3
    assert suf.babs[0][2] == ("متصل نصب/جر", "مفعول به / مضاف إليه / مجرور")
    # لَيْسَ أداةٌ قسمُها غيرُ مودَع، ووظيفتُها النفي
    t2 = wasm(tawzi(cells_of("لَيْسَ"))[0])
    assert t2.qism == ("أداة",) and any("النفي" in x for x in t2.parts[0].babs[0][2])
    # مَنْ في بابين فأكثر: لا يُختار بينها
    t3 = wasm(next(m for m in tawzi(cells_of("مَنْ")) if not m.pre))
    assert {b for b, *_ in t3.parts[0].babs} >= {"استفهام", "موصول"}
    # الموصولُ معناه بنصّ ابن عقيل وسطره (ADR ٥٥)؛ وما لا ذكرَ له فيه فجوةٌ باسمها لا معنًى من الذاكرة
    alladhi = ("«الذي للمفرد المذكر» (ابن عقيل س1051)",)
    assert maana("موصول", MAWSUL["الَّذِي"]) == (alladhi, "ibn-aqil")
    assert maana("موصول", MAWSUL["اللَّوَاتِي"]) == ((), GAP)
    # طفرة: وسمٌ يُسقط السابقة لا يردّ الكلمة
    assert tuple(c for j in t.parts[1:] for c in j.cells) != w


def test_closure_every_core_has_a_bab_and_gaps_are_named() -> None:
    gaps = [w for _, _, w in (*TABLE, *HOSTS)
            if not any(maana(b, w)[1] != GAP for b, _ in _BABS[w])]
    assert all(w in _BABS for _, _, w in (*TABLE, *HOSTS))
    # ADR ٥٥: الموصولاتُ مرساةٌ في ابن عقيل إلّا اللَّوَاتِي (لا ذكرَ لها فيه) فتبقى فجوةً باسمها.
    assert gaps == [MAWSUL["اللَّوَاتِي"]] and {b for b, _ in _BABS[gaps[0]]} == {"موصول"}
    # والسوابقُ واللواحقُ كلُّها ذواتُ معنًى: لَ من الكتاب، وهاءُ الضمير المكسورة ونِي بردّهما.
    assert all(maana("حرف", p)[1] != GAP for p in PROCLITICS)
    assert all(maana_suffix(x)[1] != GAP for x in OBJECT_SUFFIXES)
    # طفرة: بلا ردّ الكسرة تعود خمسُ لواحق فجواتٍ (نِي، هِ، هِمْ، هِمَا، هِنَّ).
    assert sum(maana("ضمير", x, True)[1] == GAP for x in OBJECT_SUFFIXES) == 5


@cache
def _lines(source: str) -> tuple[str, ...]:
    raw = gzip.decompress((ROOT / "tests" / "data" / SOURCES[source][0]).read_bytes())
    return tuple(raw.decode("utf-8").split("\n"))


def _anchored(source: str, line: int, quote: str) -> bool:
    lines = _lines(source)
    return 1 <= line <= len(lines) and quote in lines[line - 1]


def test_every_anchor_is_the_quote_on_its_line_in_the_sealed_source() -> None:
    """كلُّ معنًى مرسًى عبارةٌ بعينها في سطرها من المختوم؛ وطفراتٌ: السطرُ التالي، وحرفٌ محذوف."""

    assert len(ANCHORS) == 21 and {a.source for a in ANCHORS} == {"ibn-aqil", "kitab"}
    for a in ANCHORS:
        assert _anchored(a.source, a.line, a.quote), a
        assert not _anchored(a.source, a.line + 1, a.quote), ("السطرُ التالي", a)
        assert not _anchored(a.source, a.line, a.quote[:3] + a.quote[4:]), ("حرفٌ محذوف", a)
    for _, line, quote in SUF_KASRA.values():
        assert _anchored("kitab", line, quote)
    # بالباب: الموصولاتُ كلُّها إلّا واحدةً من ابن عقيل؛ ولَ سابقةً ببابين من الكتاب بلا اختيار.
    mawsul = {a.cells for a in ANCHORS if a.bab == "موصول"}
    assert mawsul == set(MAWSUL.values()) - {MAWSUL["اللَّوَاتِي"]}
    assert len(maana("حرف", cells_of("لَ"))[0]) == 2


def test_compound_words_carry_every_part_with_its_meaning() -> None:
    """مِنْهُمْ، لَكُمْ، وَمِنْكُمْ، عَلَيْهِ: كلُّ جزءٍ بدوره ومعناه، ولا فجوة؛ والقسمُ حرفٌ لا اسمٌ ولا فعل."""

    for w, roles in (("مِنْهُمْ", ("نواة", "لاحقة")), ("لَكُمْ", ("نواة", "لاحقة")),
                     ("وَمِنْكُمْ", ("سابقة", "نواة", "لاحقة")), ("عَلَيْهِ", ("نواة", "لاحقة"))):
        tags = [wasm(m) for m in tawzi(cells_of(w))]
        assert tags, w
        t = next(t for t in tags if tuple(j.dawr for j in t.parts) == roles)
        assert t.qism == ("حرف",), (w, t.qism)
        assert all(src != GAP for j in t.parts for *_, src in j.babs), (w, t)
        assert "".join(c for j in t.parts for c in map(str, j.cells)) == "".join(
            map(str, restore(next(m for m in tawzi(cells_of(w)) if wasm(m) == t)))), w
