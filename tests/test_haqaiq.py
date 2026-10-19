"""الحقائقُ الثلاث والمجازُ بقرينته (`A116.Haqaiq`، ADR ٩٢).

التوقّعاتُ مستقلّةٌ عن Lean:
١. كلُّ مرساةٍ في `Haqaiq.marasi` نصٌّ في سطرها (1-based) من ج3 المختومة ببصمتها هنا، وكلُّ لفظٍ في مودَع
   `naql` في سطر شاهده.
٢. الترجيحُ مقروءٌ من النصّ نفسِه: كلُّ جملة «X أولى من Y» في س454–462 تُستخرج بنمطٍ وتُطابَق قاعدةً مكتوبةً هنا
   (الرتبُ بترتيب س453، والمجازُ والإضمارُ سيّان)، ويُحسب الأوجهُ العشرة.
٣. الحملُ بقاعدةٍ مكتوبةٍ هنا: بلا قرينة المنقولُ على نقله وغيرُه لغويّ (س448)، والمجازُ بقرينته وحدَها.
الطفرات: `MUTANT_NAQL_OVER_MAJAZ`، `MUTANT_SHARI_DEFAULT`، `MUTANT_LINE_SHIFTED`.
"""

from __future__ import annotations

import gzip
import hashlib
import itertools
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LEAN = ROOT / "formal" / "a116" / "A116" / "Haqaiq.lean"
J3 = (ROOT / "corpora" / "nabhani" / "shakhsiyya_j3.txt.gz",
      "dd57e74bec43534ceec90797ad050cb104a16925b6d0bf0304796d42e70c425e")
WORDS = {"الاشتراك": "ishtirak", "النقل": "naql", "المجاز": "majaz",
         "الإضمار": "idmar", "التخصيص": "takhsis"}
ORDER = ["ishtirak", "naql", "majaz", "idmar", "takhsis"]


def lines() -> list[str]:
    raw = gzip.decompress(J3[0].read_bytes())
    assert hashlib.sha256(raw).hexdigest() == J3[1]
    return raw.decode("utf-8").splitlines()


def marasi() -> list[tuple[str, int, str]]:
    src = LEAN.read_text(encoding="utf-8")
    block = src[src.index("def marasi"):]
    return [(k, int(n), q) for k, n, q in re.findall(r'\("(\w+)", (\d+), "([^"]+)"\)', block)]


def naql_rows() -> list[tuple[str, int]]:
    src = LEAN.read_text(encoding="utf-8")
    block = src[src.index("def naql"):src.index("theorem huruf_la_tunqal")]
    return [(w, int(n)) for w, n in re.findall(r'⟨"([^"]+)", [^⟩]*?, (\d+)⟩', block)]


def rank(x: str, naql_high: bool = False) -> int:
    r = {"ishtirak": 0, "naql": 1, "majaz": 2, "idmar": 2, "takhsis": 3}
    if naql_high:
        r["naql"] = 4
    return r[x]


def tarjih(a: str, b: str, naql_high: bool = False) -> str | None:
    if a == b:
        return a
    ra, rb = rank(a, naql_high), rank(b, naql_high)
    return a if ra > rb else b if rb > ra else None


def haml(manqul: dict[str, str], word: str, qarina: str | None, has_qarina: bool,
         default: str = "lughawiyya") -> str:
    if has_qarina:
        return qarina if qarina in ("majaz", "idmar") else "laHukm"
    return manqul.get(word, default)


def awla_sentences(ls: list[str]) -> list[tuple[str, str]]:
    out = []
    for n in range(454, 464):
        m = re.search(r":\s*(\S+) أولى من (\S+?)[؛;،\s]", ls[n - 1])
        if m:
            out.append((WORDS[m.group(1)], WORDS[m.group(2)]))
    return out


def test_marasi_and_rows_in_sealed_lines() -> None:
    ls = lines()
    ms = marasi()
    assert len(ms) == 18 and all(q in ls[n - 1] for _, n, q in ms)
    rows = naql_rows()
    assert len(rows) == 9 and all(w in ls[n - 1] for w, n in rows)


def test_tarjih_read_from_text() -> None:
    ls = lines()
    awla = awla_sentences(ls)
    assert len(awla) == 9                              # تسعُ جملٍ «أولى»، والثامنُ (س461) تساوٍ
    assert all(tarjih(win, lose) == win for win, lose in awla)
    assert "الإضمار مثل المجاز" in ls[461 - 1] and tarjih("majaz", "idmar") is None
    pairs = {frozenset(p) for p in itertools.combinations(ORDER, 2)}
    stated = {frozenset(p) for p in awla} | {frozenset(("majaz", "idmar"))}
    assert len(pairs) == 10 and stated == pairs        # الأوجهُ العشرة كلُّها في النصّ
    assert sum(tarjih(*sorted(p)) is not None for p in pairs) == 9


def test_haml_rule() -> None:
    manqul = {"الصلاة": "shariyya", "الدابة": "urfiyya_amma", "الرفع": "urfiyya_khassa"}
    assert haml(manqul, "الصلاة", None, False) == "shariyya"
    assert haml(manqul, "الأسد", None, False) == "lughawiyya"
    assert haml(manqul, "الجبل", None, False) == "lughawiyya"      # الامتناعُ ليس قرينة
    assert haml(manqul, "ابني", None, True) == "laHukm"            # س461
    assert haml(manqul, "الأسد", "majaz", True) == "majaz"


def test_mutants_rejected() -> None:
    ls = lines()
    assert not all(tarjih(win, lose, naql_high=True) == win for win, lose in awla_sentences(ls))
    assert haml({}, "الأسد", None, False, default="shariyya") != "lughawiyya"
    assert not all(q in ls[n] for _, n, q in marasi())
