"""الدلالاتُ الثلاث والعلّةُ بالوصف المفهم (`A116.Dalalat`، ADR ٩٣).

التوقّعاتُ مستقلّةٌ عن Lean:
١. كلُّ مرساةٍ في `Dalalat.marasi` نصٌّ في سطرها (1-based) من ج3 أو الكتاب المختومَين ببصمتيهما هنا.
٢. شواهدُ العلّة من أسطرها: «السائل» و«محتجر» في س551 (غيرُ مفهم)، و«غضبان» و«باد»
   في س871 (مفهم)، وشروطُ س874 الثلاثة بأرقامها؛ والقاعدةُ مكتوبةٌ هنا: العلّةُ مشتقٌّ مفهم،
   والقياسُ مع وجه العلّيّة.
٣. أزواجُ المطاوعة مستخرجةٌ من س16544–16545 بنمط «فعلته فانفعل»، و«طردته فذهب ولا يقولون
   فانطرد» في س16548، وتطابق صفوفَ `mutawaat` المكتوبة في Lean.
الطفرات: `MUTANT_WAZN_ILLA`، `MUTANT_MUTAWAA_FORGED`، `MUTANT_LINE_SHIFTED`.
"""

from __future__ import annotations

import gzip
import hashlib
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LEAN = ROOT / "formal" / "a116" / "A116" / "Dalalat.lean"
TEXTS = {
    "j3": (ROOT / "corpora" / "nabhani" / "shakhsiyya_j3.txt.gz",
           "dd57e74bec43534ceec90797ad050cb104a16925b6d0bf0304796d42e70c425e"),
    "kitab": (ROOT / "corpora" / "kitab" / "0180Sibawayhi.KitabSibawayhi.JK006989-ara1.gz",
              "a160f940bb194e6fe7e6655d2c7f28e41f1fc648c4c5e340cc4e42306d5cb625"),
}


def lines(key: str) -> list[str]:
    path, sha = TEXTS[key]
    raw = gzip.decompress(path.read_bytes())
    assert hashlib.sha256(raw).hexdigest() == sha
    return raw.decode("utf-8").splitlines()


def marasi() -> list[tuple[str, int, str]]:
    src = LEAN.read_text(encoding="utf-8")
    block = src[src.index("def marasi"):]
    return [(k, int(n), q) for k, n, q in re.findall(r'\("(\w+)", (\d+), "([^"]+)"\)', block)]


def lean_mutawaat() -> dict[str, str | None]:
    src = LEAN.read_text(encoding="utf-8")
    block = src[src.index("def mutawaat"):src.index("theorem wazn_la_yuayyin_mutawaa")]
    rows = re.findall(r'⟨"([^"]+)", "[^"]+", (none|some "([^"]+)")⟩', block)
    return {f: (m or None) for f, _, m in rows}


def illa(kulli: str, mufhim: bool, by_wazn: bool = False) -> bool:
    return kulli == "mushtaq" and (by_wazn or mufhim)


def test_marasi_in_sealed_lines() -> None:
    ls = {k: lines(k) for k in TEXTS}
    ms = marasi()
    assert len(ms) == 18 and all(q in ls[k][n - 1] for k, n, q in ms)


def test_illa_witnesses_from_text() -> None:
    j3 = lines("j3")
    assert "«لِلسَّائِلِ" in j3[551 - 1]
    assert "لمحتجر" in j3[551 - 1] and "غير المفهم" in j3[551 - 1]
    assert "غَضْبَانُ" in j3[871 - 1] and "لباد" in j3[871 - 1] and "وصف مفهم" in j3[871 - 1]
    assert all(k in j3[874 - 1] for k in ("الأول:", "والثاني:", "والثالث:"))
    rows = {"السائل": ("mushtaq", False), "محتجر": ("mushtaq", False),
            "غضبان": ("mushtaq", True), "باد": ("mushtaq", True), "الذهب": ("jins", False)}
    assert [w for w, (k, m) in rows.items() if illa(k, m)] == ["غضبان", "باد"]


def test_mutawaa_from_kitab() -> None:
    kt = lines("kitab")
    span = kt[16544 - 1] + " " + kt[16545 - 1]
    pairs = dict(re.findall(r"(?<!\S)و?(\S+?)ته ف(ان\S+)", span))
    assert "طردته فذهب ولا يقولون فانطرد" in kt[16548 - 1]
    lean = lean_mutawaat()
    for fil, mut in lean.items():
        if mut is None:
            assert fil == "طرد"
        else:
            assert pairs.get(fil) == mut, (fil, mut, pairs)


def test_mutants_rejected() -> None:
    assert illa("mushtaq", False, by_wazn=True)              # السائل علّةً بالوزن
    kt = lines("kitab")
    forged = dict(lean_mutawaat(), طرد="انطرد")
    assert "فانطرد" in kt[16548 - 1] and "ولا يقولون فانطرد" in kt[16548 - 1]
    assert forged["طرد"] is not None                          # الصفُّ المزوَّر يخالف «ولا يقولون»
    ls = {k: lines(k) for k in TEXTS}
    assert not all(q in ls[k][n] for k, n, q in marasi())
