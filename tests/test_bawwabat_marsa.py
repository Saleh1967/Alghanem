"""البوّاباتُ على مرساتَي «الآن» و«هنا» (`A116.BawwabatMarsa`، ADR ٩١).

التوقّعاتُ مستقلّةٌ عن Lean:
١. كلُّ مرساةٍ في `BawwabatMarsa.marasi` نصٌّ في سطرها (1-based) من شرح ابن عقيل أو ج3 المختومَين.
٢. الرتبةُ بقاعدةٍ مكتوبةٍ هنا من نصّ س6471–6472: الفاءُ تأخّرٌ متّصل، وثمّ تأخّرٌ منفصل؛ وعلى شبكةٍ من
   المواضع والأُطر وحدود الاتّصال: لا تصدقان معًا، ونقلُ المرساة لا يغيّر شيئًا، ولا رتبةَ بين إطارين.
٣. صيغُ المكان من حروفها: الكافُ في «هناك» و«هنالك»، واللامُ في «هنالك»، والهاءُ في «ههنا»، وكلُّها في
   سطر الشرح؛ وتطابق أعلامَ `Sigha` المكتوبةَ في Lean.
الطفرات: `MUTANT_ITAR_IGNORED`، `MUTANT_KAF_IGNORED`، `MUTANT_LINE_SHIFTED`.
"""

from __future__ import annotations

import gzip
import hashlib
import itertools
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LEAN = ROOT / "formal" / "a116" / "A116" / "BawwabatMarsa.lean"
TEXTS = {
    "sharh": (ROOT / "corpora" / "ibn-aqil" / "sharh-alfiyya.txt.gz",
              "661e43ea265eca8c72b9e4ab7a46cd9182b34e834105b595241bc7787b471f09"),
    "j3": (ROOT / "corpora" / "nabhani" / "shakhsiyya_j3.txt.gz",
           "dd57e74bec43534ceec90797ad050cb104a16925b6d0bf0304796d42e70c425e"),
}
Pos = tuple[str, int] | None


def lines(key: str) -> list[str]:
    path, sha = TEXTS[key]
    raw = gzip.decompress(path.read_bytes())
    assert hashlib.sha256(raw).hexdigest() == sha
    return raw.decode("utf-8").splitlines()


def marasi() -> list[tuple[str, int, str]]:
    src = LEAN.read_text(encoding="utf-8")
    block = src[src.index("def marasi"):]
    return [(k, int(n), q) for k, n, q in re.findall(r'\("(\w+)", (\d+), "([^"]+)"\)', block)]


def rutba(harf: str, ittisal: int, a: Pos, c: Pos, ignore_itar: bool = False) -> bool | None:
    if a is None or c is None or (a[0] != c[0] and not ignore_itar):
        return None
    d = c[1] - a[1]
    if harf == "fa":
        return 0 < d <= ittisal
    if harf == "thumma":
        return d > ittisal
    return None


def ishara(kaf: bool, hadd: int, u: Pos, m: Pos, ignore_kaf: bool = False) -> bool | None:
    if u is None or m is None or u[0] != "huna" or m[0] != "huna":
        return None
    near = abs(m[1] - u[1]) <= hadd
    return near if ignore_kaf else near == (not kaf)


GRID = [(i, q) for i in ("alAn", "huna", "hijri") for q in range(-3, 4)]


def test_marasi_in_sealed_lines() -> None:
    ms = marasi()
    ls = {k: lines(k) for k in TEXTS}
    assert len(ms) == 7 and all(q in ls[k][n - 1] for k, n, q in ms)


def test_rutba_rule() -> None:
    sh = lines("sharh")
    assert "متصلا به" in sh[6471 - 1] and "متراخيا" in sh[6472 - 1]
    for a, c, it in itertools.product(GRID, GRID, range(3)):
        fa, th = rutba("fa", it, a, c), rutba("thumma", it, a, c)
        assert not (fa and th)
        assert (fa is None) == (a[0] != c[0])
        for k in (-5, 7):
            assert rutba("fa", it, (a[0], a[1] + k), (c[0], c[1] + k)) == fa
    assert rutba("fa", 1, ("alAn", -1), ("alAn", 0)) is True       # أمس فاليوم
    assert rutba("fa", 1, ("alAn", 0), ("alAn", -1)) is False      # اليوم فأمس
    assert rutba("thumma", 1, ("alAn", -1), ("alAn", 1)) is True   # أمس ثمّ غدًا
    assert rutba("fa", 1, ("alAn", 0), ("alAn", 0)) is False       # معًا
    assert rutba("fa", 1, None, ("alAn", 0)) is None


def test_huna_forms_from_letters() -> None:
    sh = lines("sharh")
    span = " ".join(sh[1017 - 1:1020])
    src = LEAN.read_text(encoding="utf-8")
    for name, word in [("huna", "هنا"), ("hahuna", "ههنا"), ("hunaka", "هناك"),
                       ("hunalika", "هنالك")]:
        assert word in span
        flags = (word.startswith("هه"), "ك" in word, "لك" in word)
        lean = re.search(rf"def {name} : Ihala\.Sigha := ⟨(\w+), (\w+), (\w+)⟩", src)
        assert lean is not None
        assert tuple(x == "true" for x in lean.groups()) == flags, name
    assert ishara(False, 1, ("huna", 0), ("huna", 0)) is True        # هذا قريب
    assert ishara(True, 1, ("huna", 0), ("huna", 10)) is True        # هنالك بعيد
    assert ishara(False, 1, ("huna", 0), ("alAn", 0)) is None


def test_mutants_rejected() -> None:
    assert rutba("fa", 1, ("hijri", 0), ("miladi", 1), ignore_itar=True) is not None
    assert ishara(True, 1, ("huna", 0), ("huna", 0), ignore_kaf=True) is True
    ls = {k: lines(k) for k in TEXTS}
    assert not all(q in ls[k][n] for k, n, q in marasi())
