"""فهرسُ الصنف المغلق (ADR ٥٣، ٥٤): أدواتُ القياس على مدخلاتٍ باليد، وأمانةُ نسخ S0، وطفراتٌ بأسمائها
(ومنها `MUTANT_FLOOR_IS_MAX`، `MUTANT_MAWSUL_SOURCE_DROPPED`):
`MUTANT_ZARF_IN_PRECISION` (الظرفُ الذهبيّ في الدقّة)، `MUTANT_VERDICT_IGNORES_PRECISION`،
`MUTANT_S0_ALL_CORES_HOST` (S0 بلا شرط الحامل لا يعيد أرقامَه)."""

from __future__ import annotations

import importlib.util
import sys
import types
from typing import Any

from conftest import ROOT

SPEC = importlib.util.spec_from_file_location("gen_mughlaq_index",
                                              ROOT / "tools" / "gen_mughlaq_index.py")
assert SPEC and SPEC.loader
MOD: Any = importlib.util.module_from_spec(SPEC)
sys.modules["gen_mughlaq_index"] = MOD
SPEC.loader.exec_module(MOD)


def test_gold_class_by_hand() -> None:
    assert [MOD.gold_class(t) for t in ("N", "V", "PN", "ADJ", "IMPN")] == ["مفتوح"] * 5
    assert [MOD.gold_class(t) for t in ("T", "LOC")] == ["ظرف"] * 2
    closed = ("P", "PRON", "DEM", "REL", "CONJ", "NEG", "INL")
    assert [MOD.gold_class(t) for t in closed] == ["مغلق"] * 7


def test_confusion_by_hand() -> None:
    pairs = [("مغلق", "مغلق")] * 6 + [("مغلق", "مفتوح")] * 2 + [("مفتوح", "مغلق")] * 1 + \
        [("مفتوح", "مفتوح")] * 9 + [("ظرف", "مغلق")] * 5
    c = MOD.confusion(pairs)
    assert (c["precision"]["k"], c["precision"]["n"]) == (6, 7)   # الظرفُ الذهبيّ خارجَ الدقّة
    assert (c["recall"]["k"], c["recall"]["n"]) == (6, 8)
    assert (c["open_leak"]["k"], c["open_leak"]["n"]) == (1, 10)
    assert c["matrix"]["ظرف→مغلق"] == 5


def test_verdict_by_hand() -> None:
    def s(pk: int, pn: int, rk: int, rn: int) -> dict[str, Any]:
        return {"precision": MOD.rate(pk, pn), "recall": MOD.rate(rk, rn)}

    s0 = s(900, 1000, 800, 1000)
    assert MOD.verdict(s0, s(905, 1000, 900, 1000)) == "CLOSURE_BETTER"
    assert MOD.verdict(s0, s(905, 1000, 805, 1000)) == "CLOSURE_NOT_BETTER"
    assert MOD.verdict(s0, s(800, 1000, 900, 1000)) == "CLOSURE_LOSES_PRECISION"


def test_s0_is_the_reader_before_closure() -> None:
    # الأرقامُ المنشورةُ في TAWZI_INDEX.md قبل ADR ٥٣ بعينها
    forms, _ = MOD.certificates()
    assert sum(1 for w in forms if MOD.before(w)) == 854
    split = MOD.tawzi_split(MOD.masaq_rows(), lambda w: [(p, s) for p, _, s, _ in MOD.before(w)])
    assert split == {"gold": 13151, "wrong": 655, "none": 507,
                     "open_population": 20498, "open_read": 70}  # ‎20,498 و70 كما في ADR ٥٢


def test_adr52_rule_by_hand() -> None:
    s0 = {"gold": 100, "none": 50, "open_read": 10}
    assert MOD.adr52_rule(s0, {"gold": 120, "none": 30, "open_read": 19}) == "ADR52_ACCEPTED"
    assert MOD.adr52_rule(s0, {"gold": 120, "none": 30, "open_read": 20}) == "ADR52_REJECTED"
    assert MOD.adr52_rule(s0, {"gold": 120, "none": 50, "open_read": 10}) == "ADR52_REJECTED"


def test_round1_is_recorded_by_hand() -> None:
    # أرقامُ MUGHLAQ_INDEX.md في 389d86a: الدقّةُ 24,877/25,122 والاستدعاءُ 24,877/(24,877+293+20)
    c = MOD.confusion_from_matrix(MOD.RECORDED_S1["matrix"])
    assert (c["precision"]["k"], c["precision"]["n"]) == (24877, 25122)
    assert (c["recall"]["k"], c["recall"]["n"]) == (24877, 25190)
    assert (c["open_leak"]["k"], c["open_leak"]["n"]) == (245, 245 + 921 + 49173)


def test_verdict2_by_hand() -> None:
    def s(pk: int, pn: int, rk: int, rn: int) -> dict[str, Any]:
        return {"precision": MOD.rate(pk, pn), "recall": MOD.rate(rk, rn)}

    s1 = s(900, 1000, 800, 1000)
    assert MOD.verdict2(s1, s(905, 1000, 900, 1000)) == "DEBTS_BETTER"
    assert MOD.verdict2(s1, s(905, 1000, 805, 1000)) == "DEBTS_NOT_BETTER"
    assert MOD.verdict2(s1, s(800, 1000, 900, 1000)) == "DEBTS_LOSE_PRECISION"


def test_floor_by_hand() -> None:
    # الصورة 0: 3 مغلق و1 مفتوح ووسمُنا مغلق ← خطأ 1، حدٌّ 1؛ الصورة 1: 2 مفتوح ووسمُنا مغلق ← خلافُ
    # تعريف 2؛ الصورة 2: 1 مغلق و4 مفتوح ووسمُنا مغلق ← خطأ 4، حدٌّ 1، قابلٌ للإصلاح 3؛ والظرفُ خارج
    rows = [(0, "مغلق")] * 3 + [(0, "مفتوح"), (1, "مفتوح"), (1, "مفتوح"), (2, "مغلق")] + \
        [(2, "مفتوح")] * 4 + [(2, "ظرف")]
    f = MOD.floor(rows, ["مغلق", "مغلق", "مغلق"])
    assert (f["errors"], f["floor"], f["definitional"], f["reducible"]) == (7, 2, 2, 3)


def test_meaning_classes_by_hand() -> None:
    from slge.rawabit import cells_of

    assert MOD.meaning_classes(cells_of("لِ")) == {"حرف"}
    assert MOD.meaning_classes(cells_of("هُمْ")) == {"ضمير"}
    assert MOD.meaning_classes(cells_of("ذَلِكَ")) == {"إشارة"}
    assert {"حرف", "استفهام", "موصول"} <= MOD.meaning_classes(cells_of("مَا"))


def _mutant(old: str, new: str) -> dict[str, Any]:
    src = (ROOT / "tools" / "gen_mughlaq_index.py").read_text(encoding="utf-8")
    assert old in src, old
    mod = types.ModuleType("mughlaq_index_mutant")
    sys.modules["mughlaq_index_mutant"] = mod
    mod.__dict__["__file__"] = str(ROOT / "tools" / "gen_mughlaq_index.py")
    exec(compile(src.replace(old, new, 1), "mughlaq_index_mutant", "exec"), mod.__dict__)
    return mod.__dict__


def test_named_mutants_are_caught() -> None:
    m = _mutant('core = [(g, p) for g, p in pairs if g != "ظرف"]', "core = list(pairs)")
    c = m["confusion"]([("ظرف", "مغلق"), ("مغلق", "مغلق")])
    assert c["precision"]["n"] == 2  # ZARF_IN_PRECISION
    m = _mutant('return "CLOSURE_BETTER" if up and keep', 'return "CLOSURE_BETTER" if up')
    s0 = {"precision": MOD.rate(900, 1000), "recall": MOD.rate(800, 1000)}
    s1 = {"precision": MOD.rate(800, 1000), "recall": MOD.rate(900, 1000)}
    assert m["verdict"](s0, s1) == "CLOSURE_BETTER"  # VERDICT_IGNORES_PRECISION
    m = _mutant("low = min(closed, opened)", "low = max(closed, opened)")
    f = m["floor"]([(0, "مغلق"), (0, "مغلق"), (0, "مفتوح")], ["مغلق"])
    assert f["floor"] == 2 and f["reducible"] == -1  # FLOOR_IS_MAX: الحدُّ فوق الخطأ (والصحيحُ 1 و0)
    m = _mutant('out.add("موصول")', "pass")
    assert "موصول" not in m["meaning_classes"](MOD.MAWSUL["الَّذِي"])  # MAWSUL_SOURCE_DROPPED
    m = _mutant("cores = {**_OLD_CORES, **_OLD_HOSTS} if suf else _OLD_CORES",
                "cores = _OLD_HOSTS if suf else _OLD_CORES")
    forms, _ = MOD.certificates()
    assert sum(1 for w in forms if m["before"](w)) != 854  # S0_ALL_CORES_HOST
