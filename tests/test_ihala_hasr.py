"""الإحالةُ بالحصر (`A116.IhalaHasr`، ADR ٨٦، تكملةُ ADR ٨٣): صفاتُ الضمائر والعائد والموصول من شرح
ابن عقيل المختوم بأسطرها، وخاناتُ لواحق العائد ما تطبعه البوّابة.

١. الأسطرُ المرساة بأعيانها في الشرح المختوم (ببصمته): الغيبةُ والحضور س724، المرفوعُ المنفصل بصفاته
   س792–797، العائدُ اللائق س1133–1138، «من» و«ما» بالوجهين س1139–1142.
٢. لواحقُ العائد الخمس (ه، هما، هم، ها، هنّ) في Lean هي ذرّاتُ البوّابة بعد «لَ» في لَهُ لَهُمَا لَهُمْ لَهَا لَهُنَّ
   من المصحف المختوم.
الطفرات: `MUTANT_LINE_SHIFTED` (سطرٌ مجاور لا يحمل المرساة)، `MUTANT_SUFFIX_SWAPPED` (لاحقةٌ مبدَّلة لا
تطابق البوّابة)، `MUTANT_AID_WITHOUT_LAM` (الهاءُ وحدَها ليست كلمةً في المختوم).
"""

from __future__ import annotations

import gzip
import hashlib
import re

from conftest import ROOT

import gate

LEAN = ROOT / "formal" / "a116" / "A116" / "IhalaHasr.lean"
SHARH = ROOT / "corpora" / "ibn-aqil" / "sharh-alfiyya.txt.gz"
SHARH_SHA256 = "661e43ea265eca8c72b9e4ab7a46cd9182b34e834105b595241bc7787b471f09"
H = {".fatha": "َ", ".damma": "ُ", ".kasra": "ِ", ".sukun": "ْ"}
SH, FA = "ّ", "َ"

ANCHORS = {
    724: "غيبة أو حضور",
    725: "ما دل على غيبة",
    792: "اثنا عشر أنا للمتكلم",
    1133: "على ضمير لائق",
    1135: "ضمير لائق بالموصول",
    1136: "مفردا فمفرد وإن كان مذكرا فمذكر",
    1140: "مراعاة اللفظ",
}
# (الكلمةُ في المصحف، لاحقتُها) — الترتيبُ ترتيبُ `aidSifa`
AID_WORDS = ["لَهُ", "لَهُمَا", "لَهُمْ", "لَهَا", "لَهُن" + SH + FA]


def sharh_lines() -> list[str]:
    raw = gzip.decompress(SHARH.read_bytes())
    assert hashlib.sha256(raw).hexdigest() == SHARH_SHA256
    return raw.decode("utf-8").split("\n")


def lean_aid_suffixes() -> list[tuple[str, ...]]:
    text = LEAN.read_text(encoding="utf-8")
    block = text[text.index("def aidSifa") : text.index("/-- الموصولُ بصفة لفظه")]
    out = []
    for line in block.splitlines():
        if "([atom" in line:
            cells = line[line.index("([") + 1 : line.index("],")]
            out.append(tuple(c + H[h] for c, h in re.findall(r"atom '(.)' (\.\w+)", cells)))
    return out


def test_anchors_in_sealed_sharh() -> None:
    lines = sharh_lines()
    for ln, needle in ANCHORS.items():
        assert needle in lines[ln - 1], (ln, needle)


def test_aid_suffixes_are_gate_output() -> None:
    sfx = lean_aid_suffixes()
    assert len(sfx) == 5
    for word, expect in zip(AID_WORDS, sfx, strict=True):
        cert = gate.enter(word.encode())
        assert isinstance(cert, gate.Certificate), (word, cert)
        atoms = tuple(cert.atoms)
        assert atoms[0] == "ل" + H[".fatha"] and atoms[1:] == expect, (word, atoms, expect)


def test_mutant_line_shifted() -> None:
    lines = sharh_lines()
    shifted = [needle in lines[ln] for ln, needle in ANCHORS.items()]
    assert shifted.count(True) <= 1 and not shifted[-1]  # الأسطرُ المرساة لا تتكرّر في الذي بعدها


def test_mutant_suffix_swapped() -> None:
    cert = gate.enter("لَهُمْ".encode())
    assert isinstance(cert, gate.Certificate)
    assert tuple(cert.atoms)[1:] != lean_aid_suffixes()[1]  # هُمَا ≠ هُمْ


def test_mutant_aid_without_lam() -> None:
    r = gate.enter("هُ".encode())
    assert isinstance(r, gate.Refusal)
