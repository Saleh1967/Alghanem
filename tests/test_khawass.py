"""خواصُّ الجنس شرطُ الحقيقة (`A116.Khawass`، ADR ٩٦).

التوقّعاتُ مستقلّةٌ عن Lean:
١. كلُّ مرساةٍ في `Khawass.marasi` نصٌّ في سطرها (1-based) من النصوص المختومة ببصماتها.
٢. كلُّ صفٍّ بنصٍّ جنسُه في سطره؛ وصفُّ الحصر سطرُه فيه «إلا عند الإنسان» وجنسُه غيرُ الإنسان ومنفيّ؛ وصفُّ الوراثة
   معلَنٌ بالمالك وكلّيُّه صفٌّ بنصٍّ يوافقه.
٣. شرطُ المصدر مقروءٌ من نصّ السيرافيّ س23551–23552 («يخاطب ويخاطب، ويأمر، ويؤمر، وتخبر وتخبر عنه…
   إلا أنه يخبر عنه») ويطابق `shart` في Lean.
٤. الحكمُ بقاعدةٍ مكتوبةٍ هنا على شبكة المالك (الإنسان، الحجر، الكلب، القمر) × (الكلام، النطق، الفهم).
الطفرات: `MUTANT_HASR_ON_INSAN`، `MUTANT_YUKHBAR_ANHU_NEEDS_AQL`، `MUTANT_LINE_SHIFTED`.
"""

from __future__ import annotations

import gzip
import hashlib
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LEAN = ROOT / "formal" / "a116" / "A116" / "Khawass.lean"
TEXTS = {
    "kitab": (ROOT / "corpora" / "kitab" / "0180Sibawayhi.KitabSibawayhi.JK006989-ara1.gz",
              "a160f940bb194e6fe7e6655d2c7f28e41f1fc648c4c5e340cc4e42306d5cb625"),
    "sirafi": (ROOT / "corpora" / "kitab"
               / "0368AbuSacidSirafi.SharhKitabSibawayhi.Sham19Y0017726-ara1.gz",
               "d53137fd4151028c5dee8ab9ff3e42275ecf0c39089e15fbf50bf0eefaa1603a"),
    "j3": (ROOT / "corpora" / "nabhani" / "shakhsiyya_j3.txt.gz",
           "dd57e74bec43534ceec90797ad050cb104a16925b6d0bf0304796d42e70c425e"),
    "tafkir": (ROOT / "corpora" / "nabhani" / "tafkir.txt.gz",
               "f7fcc683237681e8d24dfeb59afb5e9b2e8536822a925eab010e9bed05f5d83c"),
}
HASR = "إلا عند الإنسان"


def lines(key: str) -> list[str]:
    path, sha = TEXTS[key]
    raw = gzip.decompress(path.read_bytes())
    assert hashlib.sha256(raw).hexdigest() == sha
    return raw.decode("utf-8").splitlines()


def all_lines() -> dict[str, list[str]]:
    return {k: lines(k) for k in TEXTS}


def marasi() -> list[tuple[str, int, str]]:
    src = LEAN.read_text(encoding="utf-8")
    block = src[src.index("def marasi"):]
    pat = r'\("(\w+)", (\d+), "((?:[^"\\]|\\.)+)"\)'
    return [(k, int(n), q.replace('\\"', '"')) for k, n, q in re.findall(pat, block)]


def sufuf() -> list[tuple[str, bool, str, str, str, int]]:
    src = LEAN.read_text(encoding="utf-8")
    block = src[src.index("def sufuf"):src.index("def saffOf")]
    pat = r'⟨"([^"]+)", (true|false), \.(nass|hasr|isa)(?: "([^"]+)")?, "(\w+)", (\d+)⟩'
    return [(j, a == "true", k, p, s, int(n)) for j, a, k, p, s, n in re.findall(pat, block)]


def aqil_of(rows: list[tuple[str, bool, str, str, str, int]], j: str) -> bool | None:
    by = {r[0]: r for r in rows}
    if j not in by:
        return None
    r = by[j]
    if r[2] == "isa":
        return by[r[3]][1] if r[3] in by else None
    return r[1]


def shart_from_text(ls: dict[str, list[str]]) -> dict[tuple[str, str], bool]:
    """الشرطُ من س23551–23552 بعينهما: ما يختصّ به ما يعقل، وما يبقى لما لا يعقل."""
    text = ls["sirafi"][23550] + " " + ls["sirafi"][23551]
    assert "يخاطب ويخاطب" in text and "ويأمر" in text and "ويؤمر" in text
    assert "وتخبر وتخبر عنه" in text and "إلا أنه يخبر عنه" in text
    return {("khitab", "faail"): True, ("khitab", "mafool"): True,
            ("amr", "faail"): True, ("amr", "mafool"): True,
            ("ikhbar", "faail"): True, ("ikhbar", "mafool"): False}


def shart_lean() -> dict[tuple[str, str], bool]:
    src = LEAN.read_text(encoding="utf-8")
    block = src[src.index("def shart"):src.index("/-! ## ٢.")]
    out: dict[tuple[str, str], bool] = {}
    for m, d, v in re.findall(r"\| \.(\w+), (_|\.\w+) => some (true|false)", block):
        for dd in (["faail", "mafool"] if d == "_" else [d[1:]]):
            out[(m, dd)] = v == "true"
    return out


def hukm(need: bool | None, aqil: bool | None, yukhbar_needs: bool = False) -> str:
    if need is None or aqil is None:
        return "laHukm"
    if need or yukhbar_needs:
        return "haqiqa" if aqil else "majaz"
    return "haqiqa"


def test_marasi_in_sealed_lines() -> None:
    ls = all_lines()
    ms = marasi()
    assert len(ms) == 14 and all(q in ls[k][n - 1] for k, n, q in ms)


Row = tuple[str, bool, str, str, str, int]


def row_ok(row: Row, ls: dict[str, list[str]], rows: list[Row]) -> bool:
    jins, aqil, kind, parent, src, n = row
    if kind == "nass":
        return jins in ls[src][n - 1]
    if kind == "hasr":
        return HASR in ls[src][n - 1] and jins != "الإنسان" and not aqil
    parents = [r for r in rows if r[0] == parent]
    return src == "owner" and bool(parents) and parents[0][2] == "nass" and parents[0][1] == aqil


def test_rows_from_their_lines() -> None:
    ls = all_lines()
    rows = sufuf()
    assert len(rows) == 14 and all(row_ok(r, ls, rows) for r in rows)


def test_shart_from_sirafi() -> None:
    from_text = shart_from_text(all_lines())
    lean = shart_lean()
    assert all(lean[k] == v for k, v in from_text.items())


def test_owner_grid() -> None:
    rows = sufuf()
    need = {"khitab": True, "nutq": True, "fahm": True}  # فاعلًا: كلامُه ونطقُه وفهمُه
    for j in ("الإنسان", "الحجر", "الكلب", "القمر"):
        for m in need:
            want = "haqiqa" if j == "الإنسان" else "majaz"
            assert hukm(need[m], aqil_of(rows, j)) == want, (j, m)
    assert hukm(False, aqil_of(rows, "الحجر")) == "haqiqa"        # يُخبر عنه
    assert hukm(True, aqil_of(rows, "الجبل")) == "laHukm"          # لا صفّ


def test_mutants_rejected() -> None:
    ls = all_lines()
    rows = sufuf()
    hajar = [r for r in rows if r[2] == "hasr"][0]
    assert not row_ok(("الإنسان",) + hajar[1:], ls, rows)           # MUTANT_HASR_ON_INSAN
    assert hukm(False, aqil_of(rows, "الحجر"), yukhbar_needs=True) != "haqiqa"  # YUKHBAR
    assert not all(q in ls[k][n] for k, n, q in marasi())           # MUTANT_LINE_SHIFTED
