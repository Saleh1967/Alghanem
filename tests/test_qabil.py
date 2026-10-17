"""الحقيقةُ بالقابليّة (`A116.Qabil`، ADR ٩٥).

التوقّعاتُ مستقلّةٌ عن Lean:
١. كلُّ مرساةٍ في `Qabil.marasi` نصٌّ في سطرها (1-based) من الكتاب أو شرح السيرافيّ أو ج3 أو التفكير
   المختومة ببصماتها هنا.
٢. كلُّ صفٍّ في `sufuf` جنسُه في سطر شاهده، وكلُّ صفٍّ منفيٍّ في سطره علامةُ النفي أو الصرف
   («لا …»، «لغير»، «يريد أهل»، «قابله»).
٣. الحكمُ بقاعدةٍ مكتوبةٍ هنا: ثبوتُ القابليّة حقيقة، وانتفاؤها مجاز، وغيابُ الصفّ «لا حكم»؛ والحقيقةُ
   في الجمع ⟺ الصيغةُ والقابليّة حقيقتان.
الطفرات: `MUTANT_GHIYAB_MAJAZ`، `MUTANT_ONE_LINK`، `MUTANT_LINE_SHIFTED`.
"""

from __future__ import annotations

import gzip
import hashlib
import itertools
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LEAN = ROOT / "formal" / "a116" / "A116" / "Qabil.lean"
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
MARKERS = ("لا ", "لغير", "يريد أهل", "قابله", "غير موجود")
VALS = ["haqiqa", "majaz", "laHukm"]


def lines(key: str) -> list[str]:
    path, sha = TEXTS[key]
    raw = gzip.decompress(path.read_bytes())
    assert hashlib.sha256(raw).hexdigest() == sha
    return raw.decode("utf-8").splitlines()


def marasi() -> list[tuple[str, int, str]]:
    src = LEAN.read_text(encoding="utf-8")
    block = src[src.index("def marasi"):]
    pat = r'\("(\w+)", (\d+), "((?:[^"\\]|\\.)+)"\)'
    return [(k, int(n), q.replace('\\"', '"')) for k, n, q in re.findall(pat, block)]


def sufuf() -> list[tuple[str, bool, str, int]]:
    src = LEAN.read_text(encoding="utf-8")
    block = src[src.index("def sufuf"):src.index("def lookup")]
    pat = r'⟨"([^"]+)", "[^"]+", \.\w+, (true|false), [^,]+(?:"[^"]*")?, "(\w+)", (\d+)⟩'
    rows = re.findall(pat, block)
    return [(j, i == "true", k, int(n)) for j, i, k, n in rows]


def hukm(ijab: bool | None, ghiyab_majaz: bool = False) -> str:
    if ijab is None:
        return "majaz" if ghiyab_majaz else "laHukm"
    return "haqiqa" if ijab else "majaz"


def jam(s: str, q: str, one_link: bool = False) -> str:
    if one_link and s == "haqiqa":
        return "haqiqa"
    if s == q == "haqiqa":
        return "haqiqa"
    if "laHukm" in (s, q):
        return "laHukm"
    return "majaz"


def test_marasi_in_sealed_lines() -> None:
    ls = {k: lines(k) for k in TEXTS}
    ms = marasi()
    assert len(ms) == 16 and all(q in ls[k][n - 1] for k, n, q in ms)


def test_rows_from_their_lines() -> None:
    ls = {k: lines(k) for k in TEXTS}
    rows = sufuf()
    assert len(rows) == 10
    for jins, ijab, k, n in rows:
        line = ls[k][n - 1]
        assert jins in line, (jins, k, n)
        if not ijab:
            assert any(m in line for m in MARKERS), (jins, k, n)


def test_rule() -> None:
    assert hukm(True) == "haqiqa" and hukm(False) == "majaz" and hukm(None) == "laHukm"
    for s, q in itertools.product(VALS, repeat=2):
        assert (jam(s, q) == "haqiqa") == (s == q == "haqiqa")
    assert jam("haqiqa", hukm(False)) == "majaz"                # نهارك صائم


def test_mutants_rejected() -> None:
    assert hukm(None, ghiyab_majaz=True) != "laHukm"
    assert jam("haqiqa", "majaz", one_link=True) == "haqiqa"   # ربطٌ واحدٌ لا يكفي
    ls = {k: lines(k) for k in TEXTS}
    assert not all(q in ls[k][n] for k, n, q in marasi())
