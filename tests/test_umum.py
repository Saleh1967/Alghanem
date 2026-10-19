"""حروفُ «أنيت» والشخص، وعمومُ النكرة في سياق النفي (`A116.Umum`، ADR ٩٧).

التوقّعاتُ مستقلّةٌ عن Lean:
١. كلُّ مرساةٍ في `Umum.marasi` نصٌّ في سطرها (1-based) من شرح السيرافيّ وج3 المختومين ببصمتيهما.
٢. جدولُ الحرف ← الشخص مقروءٌ من نصّ السيرافيّ س48515–48516 بنمط «الحرف للشخص»،
   والتاءُ الثانية من س69188–69189 («للمخاطب أو للمؤنثة الغائبة»)، ويطابق `dalala` في Lean.
٣. النوافي مقروءةٌ من س652 بين «» في جملة «وسواء كان النافي…» وتطابق `Nafi` في Lean.
٤. العمومُ بقاعدةٍ مكتوبةٍ هنا: قرينةٌ تتناول ← عامّ، وبالتخصيص ← باقٍ، وبلا قرينة ← لا حكم؛
   والباقي فرقُ قائمتين.
الطفرات: `MUTANT_TA_ONE_READING`، `MUTANT_TAKHSIS_IGNORED`، `MUTANT_LINE_SHIFTED`.
"""

from __future__ import annotations

import gzip
import hashlib
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LEAN = ROOT / "formal" / "a116" / "A116" / "Umum.lean"
TEXTS = {
    "sirafi": (ROOT / "corpora" / "kitab"
               / "0368AbuSacidSirafi.SharhKitabSibawayhi.Sham19Y0017726-ara1.gz",
               "d53137fd4151028c5dee8ab9ff3e42275ecf0c39089e15fbf50bf0eefaa1603a"),
    "j3": (ROOT / "corpora" / "nabhani" / "shakhsiyya_j3.txt.gz",
           "dd57e74bec43534ceec90797ad050cb104a16925b6d0bf0304796d42e70c425e"),
}
HARF = {"الألف": "hamza", "النون": "nun", "التاء": "ta", "الياء": "ya"}
SHAKHS = {"للمتكلم": "mutakallim", "للجماعة": "jamaa", "للمخاطب": "mukhatab",
          "للغائب": "ghaib", "للمؤنثة الغائبة": "ghaiba"}
NAFI = {"ما": "ma", "لم": "lam", "لن": "lan", "ليس": "laysa"}


def lines(key: str) -> list[str]:
    path, sha = TEXTS[key]
    raw = gzip.decompress(path.read_bytes())
    assert hashlib.sha256(raw).hexdigest() == sha
    return raw.decode("utf-8").splitlines()


def joined(ls: list[str], a: int, b: int) -> str:
    return " ".join(x.removeprefix("~~").removeprefix("# ") for x in ls[a - 1:b])


def marasi() -> list[tuple[str, int, str]]:
    src = LEAN.read_text(encoding="utf-8")
    block = src[src.index("def marasi"):]
    pat = r'\("(\w+)", (\d+), "((?:[^"\\]|\\.)+)"\)'
    return [(k, int(n), q) for k, n, q in re.findall(pat, block)]


def dalala_from_text(s: list[str], one_ta: bool = False) -> dict[str, list[str]]:
    text = joined(s, 48515, 48516)
    out: dict[str, list[str]] = {}
    pat = r"(الألف|النون|التاء|الياء) (للمتكلم|للجماعة|للمخاطب|للغائب)"
    for harf, shakhs in re.findall(pat, text):
        out.setdefault(HARF[harf], []).append(SHAKHS[shakhs])
    ta = joined(s, 69188, 69189)
    assert "علامة للمخاطب أو للمؤنثة الغائبة" in ta
    if not one_ta:
        out["ta"].append("ghaiba")
    return out


def dalala_lean() -> dict[str, list[str]]:
    src = LEAN.read_text(encoding="utf-8")
    block = src[src.index("def dalala"):src.index("def harfOf")]
    return {h: re.findall(r"\.(\w+)", body)
            for h, body in re.findall(r"\| \.(\w+) => \[([^\]]*)\]", block)}


def umum(tanawul: str | None, takhsis: bool, ignore: bool = False) -> str:
    if tanawul is None:
        return "laHukm"
    return f"baqi:{tanawul}" if takhsis and not ignore else f"aamm:{tanawul}"


def test_marasi_in_sealed_lines() -> None:
    ls = {k: lines(k) for k in TEXTS}
    ms = marasi()
    assert len(ms) == 13 and all(q in ls[k][n - 1] for k, n, q in ms)


def test_dalala_from_sirafi() -> None:
    assert dalala_from_text(lines("sirafi")) == dalala_lean()


def test_nafi_from_j3() -> None:
    line = lines("j3")[651]
    sentence = line[line.index("وسواء كان النافي"):line.index("أم غيرها")]
    found = [NAFI[x] for x in re.findall(r"«([^»]+)»", sentence)]
    src = LEAN.read_text(encoding="utf-8")
    decl = re.search(r"inductive Nafi \| (.+)", src)
    assert decl is not None
    lean = [x.strip() for x in decl.group(1).split("|")]
    assert found == lean[:4] and "ghayruha" in lean


def test_umum_rule() -> None:
    assert umum("afrad", False) == "aamm:afrad" and umum("afrad", True) == "baqi:afrad"
    assert umum(None, False) == "laHukm"
    afrad = ["الإنسان", "الثقلان", "الملائكة"]
    assert [a for a in afrad if a not in ["الملائكة"]] == ["الإنسان", "الثقلان"]


def test_mutants_rejected() -> None:
    s = lines("sirafi")
    assert dalala_from_text(s, one_ta=True) != dalala_lean()          # MUTANT_TA_ONE_READING
    assert umum("afrad", True, ignore=True) != umum("afrad", True)      # MUTANT_TAKHSIS_IGNORED
    ls = {k: lines(k) for k in TEXTS}
    assert not all(q in ls[k][n] for k, n, q in marasi())              # MUTANT_LINE_SHIFTED
