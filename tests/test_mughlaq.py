"""الصنفُ المغلق (ADR ٥٣): الوسمُ الثلاثيّ وإغلاقُ المعنى بتوقّعاتٍ باليد مستقلّةٍ عن الشيفرة،
وطفراتٌ مرفوضة بأسمائها:
`MUTANT_ZARF_IS_CLOSED`، `MUTANT_FIRST_ENTRY_ONLY`، `MUTANT_HA_KASRA_UNNAMED`."""

from __future__ import annotations

import sys
import types
from pathlib import Path
from typing import Any

from slge.mughlaq import QISM, SOURCES, closed, closed_core, mana, qism, src
from slge.rawabit import cells_of
from slge.tawzi import COMPOUNDS, HOSTS, TABLE, tawzi

SRC = Path(__file__).resolve().parent.parent / "src" / "slge" / "mughlaq.py"


def test_qism_by_hand() -> None:
    assert QISM == ("مغلق", "ظرف", "مفتوح")
    for word, q in (("لَهُمُ", "مغلق"), ("وَهُمْ", "مغلق"), ("مِنْكُمْ", "مغلق"), ("وَمِنْ", "مغلق"),
                    ("وَمِنْكُمْ", "مغلق"), ("فِيمَا", "مغلق"), ("وَلِلَّذِينَ", "مغلق"), ("ذَلِكُمْ", "مغلق"),
                    ("أَنْتُمُ", "مغلق"), ("عِنْدَهُ", "ظرف"), ("قَبْلَ", "ظرف"), ("حَيْثُ", "ظرف"),
                    ("كَتَبَ", "مفتوح"), ("الْكِتَابُ", "مفتوح"), ("ظَنَّ", "مفتوح")):
        assert qism(cells_of(word)) == q, word


def test_partition() -> None:
    # المفتوحُ ما لا يقرؤه الموزِّعُ بعينه، والمغلقُ ما له قراءةٌ نواتُها غيرُ ظرف
    for word in ("لَهُمُ", "عِنْدَهُ", "كَتَبَ", "فِيمَا", "مِنْ"):
        w = cells_of(word)
        assert (qism(w) == "مفتوح") == (not tawzi(w))
        assert (qism(w) == "مغلق") == any(closed_core(m.core) for m in tawzi(w))


def test_every_closed_core_has_a_named_meaning() -> None:
    cores = [w for _, _, w in (*TABLE, *COMPOUNDS, *HOSTS) if closed_core(w)]
    assert cores and all(src(w) in SOURCES for w in cores)
    got = {src(w) for w in cores}
    assert got == set(SOURCES) - {"عمل"} or got == set(SOURCES)


def test_meanings_by_hand() -> None:
    def core_mana(word: str) -> tuple[str, ...]:
        ms = closed(cells_of(word))
        return next(m for x in ms for k, m in mana(x) if k not in ("سابقة", "لاحقة"))

    assert "الاختصاص" in core_mana("لِي")              # مبحثُ الحرف: لِ للاختصاص
    assert core_mana("فِي")[0] == "الظرفية"
    assert "عمل: نصب الاسم" in core_mana("إِنَّ")
    assert core_mana("هُمْ") == ("منفصل رفع: مبتدأ أو فاعل",)
    assert core_mana("ذَلِكَ") == ("بعيد: المفرد المذكّر",)
    assert core_mana("أَلَّذِي") == ("اسم موصول",)
    assert core_mana("مِمَّا")[:1] == ("ابتداء الغاية",) and core_mana("مِمَّا")[-1] == "تركيب مع مَا"
    # الواوُ سابقةً بكلّ مداخلها لا بأوّلها: العطفُ («مطلق الجمع») والقسم معًا
    pre = dict(mana(closed(cells_of("وَمِنْ"))[0]))["سابقة"]
    assert "مطلق الجمع" in pre and "القسم" in pre
    suf = dict(mana(closed(cells_of("عَلَيْهِمُ"))[0]))["لاحقة"][0]
    assert suf.startswith("ـهُمْ") and "موصولة" in suf and "مكسورة" in suf


def _mutant(old: str, new: str) -> dict[str, Any]:
    src_ = SRC.read_text(encoding="utf-8")
    assert old in src_, old
    mod = types.ModuleType("mughlaq_mutant")
    sys.modules["mughlaq_mutant"] = mod
    src_ = src_.replace(old, new, 1).replace("\n_check()\n", "\n")
    exec(compile(src_, "mughlaq_mutant", "exec"), mod.__dict__)
    return mod.__dict__


def test_named_mutants_are_caught() -> None:
    m = _mutant("return core not in ZARF_CELLS", "return True")
    assert m["qism"](cells_of("عِنْدَهُ")) == "مغلق"  # ZARF_IS_CLOSED
    m = _mutant("for i in _HURUF_IDX[core] for x in", "for i in _HURUF_IDX[core][:1] for x in")
    pre = dict(m["mana"](closed(cells_of("وَمِنْ"))[0]))["سابقة"]
    assert "مطلق الجمع" not in pre  # FIRST_ENTRY_ONLY
    m = _mutant('if suf[0] == ("ه", "كسر"):', "if False:")
    assert dict(m["mana"](closed(cells_of("عَلَيْهِمْ"))[0]))["لاحقة"] == ("",)  # HA_KASRA_UNNAMED
