"""أدواتُ المعاني بوّاباتٌ بسببٍ وشرطٍ ومانع (`A116.Bawwabat`، ADR ٩٠).

التوقّعاتُ مستقلّةٌ عن Lean:
١. كلُّ مرساةٍ في `Bawwabat.marasi` نصٌّ في سطرها (1-based) من شرح ابن عقيل أو ج3
   المختومَين ببصمتيهما هنا.
٢. الجداولُ الثلاثيّة مكتوبةٌ هنا: على الصادق والكاذب تساوي and/or/not في بايثون، والكاذبُ
   يغلب الجمع، والصادقُ يغلب «أحدَهما»، و«لا حكم» لا يصير صدقًا ولا كذبًا بلا حسم؛ ودي
   مورغان على القيم التسع.
٣. شروطُ السياق كما في نصّ الشرح: «لكن» بعد النفي والنهي، و«لا» بعد الإثبات والأمر
   والنداء، والنصُّ المانعُ في سطره («ولا يعطف بلا بعد النفي»، «ولا يعطف بلكن في الإثبات»).
الطفرات: `MUTANT_CLOSED_WORLD`، `MUTANT_LAKIN_ITHBAT`، `MUTANT_LINE_SHIFTED`.
"""

from __future__ import annotations

import gzip
import hashlib
import itertools
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LEAN = ROOT / "formal" / "a116" / "A116" / "Bawwabat.lean"
TEXTS = {
    "sharh": (ROOT / "corpora" / "ibn-aqil" / "sharh-alfiyya.txt.gz",
              "661e43ea265eca8c72b9e4ab7a46cd9182b34e834105b595241bc7787b471f09"),
    "j3": (ROOT / "corpora" / "nabhani" / "shakhsiyya_j3.txt.gz",
           "dd57e74bec43534ceec90797ad050cb104a16925b6d0bf0304796d42e70c425e"),
}
VALS: list[bool | None] = [True, False, None]


def lines(key: str) -> list[str]:
    path, sha = TEXTS[key]
    raw = gzip.decompress(path.read_bytes())
    assert hashlib.sha256(raw).hexdigest() == sha
    return raw.decode("utf-8").splitlines()


def marasi() -> list[tuple[str, int, str]]:
    src = LEAN.read_text(encoding="utf-8")
    block = src[src.index("def marasi"):]
    return [(k, int(n), q) for k, n, q in re.findall(r'\("(\w+)", (\d+), "([^"]+)"\)', block)]


def wa(a: bool | None, c: bool | None, closed: bool = False) -> bool | None:
    if a is False or c is False:
        return False
    if a is True and c is True:
        return True
    return True if closed else None


def aw(a: bool | None, c: bool | None) -> bool | None:
    if a is True or c is True:
        return True
    if a is False and c is False:
        return False
    return None


def nafy(a: bool | None) -> bool | None:
    return None if a is None else not a


def shart(harf: str, siyaq: str, lakin_anywhere: bool = False) -> bool:
    if harf == "lakin":
        return lakin_anywhere or siyaq in ("nafy", "nahy")
    if harf == "la":
        return siyaq in ("ithbat", "amr", "nida")
    return True


def test_marasi_in_sealed_lines() -> None:
    ms = marasi()
    ls = {k: lines(k) for k in TEXTS}
    assert len(ms) == 16 and all(q in ls[k][n - 1] for k, n, q in ms)


def test_tables() -> None:
    for x, y in itertools.product([True, False], repeat=2):
        assert wa(x, y) == (x and y) and aw(x, y) == (x or y) and nafy(x) == (not x)
    assert wa(False, None) is False and wa(True, None) is None
    assert aw(True, None) is True and aw(False, None) is None
    for a, c in itertools.product(VALS, repeat=2):
        assert wa(nafy(a), nafy(c)) == nafy(aw(a, c))


def test_shart_from_text() -> None:
    sh = lines("sharh")
    assert "ولا يعطف بلا بعد" in sh[6531 - 1] and "النفي نحو ما جاء زيد لا عمرو" in sh[6532 - 1]
    assert "ولا يعطف بلكن في الإثبات" in sh[6532 - 1]
    assert not shart("la", "nafy") and not shart("lakin", "ithbat")
    assert shart("lakin", "nafy") and shart("la", "ithbat") and shart("wa", "ithbat")


def test_mutants_rejected() -> None:
    assert wa(True, None, closed=True) is not None
    assert shart("lakin", "ithbat", lakin_anywhere=True)
    ls = {k: lines(k) for k in TEXTS}
    assert not all(q in ls[k][n] for k, n, q in marasi())
