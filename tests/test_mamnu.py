"""الممنوعُ من الصرف (ADR ٥٥) — مرآةُ `A116.Mamnu`.

التوقّعاتُ باليد من أبيات الألفيّة وشواهد Lean (`shape_witnesses`، `mamnu_needs_amil`، `alam_alone`،
`nakira_munsarif`، `tanwin_munsarif`). والطفرات: `MUTANT_ALAM_ALONE_BLOCKS` (العلَميّةُ وحدَها تمنع)،
`MUTANT_IGNORE_TANWIN` (التنوينُ لا يصرف)، `MUTANT_MUNTAHA_ANY_PLURAL` (كلُّ جمعٍ تكسيرٍ منتهى جموع)،
`MUTANT_READJ_ALWAYS_JARR` (حرفُ الجرّ يقرأ جرًّا أيَّ آخر).
"""

from __future__ import annotations

from gate import enter, exit
from gate import mamnu as m


def _w(s: str) -> list[tuple[str, str]]:
    return m.word(exit(enter(s.encode())).decode())


def test_logic_matches_lean() -> None:
    assert m.mamnu({"tanithAlif": True}) and m.mamnu({"muntaha": True})  # strong_alone
    assert not m.mamnu({"alam": True}) and not m.mamnu({"wasf": True})  # alam_alone، wasf_alone
    assert m.mamnu({"alam": True, "waznFil": True})  # أَحْمَدُ
    assert not m.mamnu({"alam": False, "waznFil": True})  # nakira_munsarif
    assert not m.mamnu({"muntaha": True, "tanwin": True})  # tanwin_munsarif
    assert not m.mamnu({"muntaha": True, "al": True})  # al_munsarif


def test_shapes_on_certificates() -> None:
    assert m.muntaha_shape(_w("مَسَاجِدَ")) and m.muntaha_shape(_w("بِمَصَابِيحَ")[1:])
    assert not m.muntaha_shape(_w("كِتَابٌ")) and m.afal_shape(_w("أَكْبَرُ"))
    assert m.has_tanwin("كِتَابٌ") and not m.has_tanwin("مَسَاجِدَ")


def test_shapes_outside_the_corpus() -> None:
    """شواهدُ Lean ليست في المصحف بصورها هذه (البوّابةُ ترفضها): الفحصُ هنا في tests وحدَها."""

    assert not m.afal_shape(m.word("إِصْبَعُ"))
    assert m.falan_shape(m.word("سَكْرَانُ")) and not m.falan_shape(m.word("عُثْمَانُ"))


def test_read_j() -> None:
    assert m.read_j("iMamnu", "fatha") == "jarr"  # mamnu_needs_amil: لِآدَمَ
    assert m.read_j("iSahih", "kasra") == "jarr" and m.read_j("iSahih", "fatha") is None
    assert m.read_j("iJamM", "ina") == "jarr" and m.read_j("iJamM", "una") is None


def test_mutants_are_caught() -> None:
    # MUTANT_ALAM_ALONE_BLOCKS: «نُوحٌ» علَمٌ بلا ثانية — منصرف
    assert not m.mamnu({"alam": True})
    # MUTANT_IGNORE_TANWIN: «مَسَاجِدًا» (لو نُوّن) يُصرف
    assert not m.mamnu({"muntaha": True, "tanwin": m.has_tanwin("مَسَاجِدًا")})
    # MUTANT_MUNTAHA_ANY_PLURAL: «رِجَالٌ» جمعُ تكسيرٍ ليس على مفاعل
    assert not m.muntaha_shape(m.word("رِجَالٌ"))
    # MUTANT_READJ_ALWAYS_JARR: «الْمُؤْمِنُونَ» بعد حرف جرٍّ لا يكون — فالقارئُ يمتنع لا يحكم جرًّا
    assert m.read_j("iJamM", "una") is None


def test_peel_by_qac_prefix() -> None:
    """`PEEL_BY_QAC_PREFIX` (التسجيل الثالث §٢): حروفُ السوابق باليد."""

    import importlib.util
    import sys

    from conftest import ROOT

    path = ROOT / "tools" / "gen_qac_qism.py"
    spec = importlib.util.spec_from_file_location("gen_qac_qism", path)
    assert spec and spec.loader
    t = importlib.util.module_from_spec(spec)
    sys.modules["gen_qac_qism"] = t
    spec.loader.exec_module(t)
    assert t.prefix_letters(["PREFIX|w:CONJ+", "PREFIX|Al+"]) == 3  # وَالْ
    assert t.prefix_letters(["PREFIX|l:P+", "PREFIX|Al+"]) == 2  # لِلْ
    assert t.prefix_letters(["PREFIX|ya+"]) == 0 and t.prefix_letters(["PREFIX|bi+"]) == 1
    f = {"pos": "PN", "num": "", "root": "", "prefixes": "PREFIX|l:P+"}
    sf = t.sifat(f, "لِآدَمَ")
    assert sf["alam"] and sf["ajamiOver3"] and not sf["tanwin"]  # «آدَم» أربعةُ أحرف: ء ا د م
    assert not t.sifat({**f, "prefixes": ""}, "نُوحٍ")["ajamiOver3"]  # ثلاثيٌّ منصرف
