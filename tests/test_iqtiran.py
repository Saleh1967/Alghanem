"""اقترانُ الدالّ بالمدلول (`A116.Iqtiran`، ADR ٩٨).

التوقّعاتُ مستقلّةٌ عن Lean:
١. المراسي في أسطرها (1-based) من ج1 وج3 المختومين ببصمتيهما.
٢. الثنائيّ: 116 + عددُ العلامات المكتوبة في Lean = 128، والردُّ بعينه على الرموز الـ128
   كلِّها بقاعدةٍ مكتوبةٍ هنا.
٣. الاقترانُ والمنطوقُ والمرتبةُ بقاعدةٍ مكتوبةٍ هنا على شبكة قيود: الترتيبُ لا يغيّر،
   والقيدُ لا يزيد، ولا مفهومَ بلا شاهد.
٤. على مودَع الوضع (`corpora/wad/wad.tsv`): المفتاحُ ذو الجذر الواحد معيَّنٌ بلا قرينة،
   وذو الجذرين محتمَل؛ وعددُ المحتمَل يطابق `Wad.mushtarak_count` (382).
الطفرات: `MUTANT_ANY_NOT_ALL`، `MUTANT_FIRST_OF_MANY`، `MUTANT_LINE_SHIFTED`.
"""

from __future__ import annotations

import collections
import gzip
import hashlib
import itertools
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LEAN = ROOT / "formal" / "a116" / "A116" / "Iqtiran.lean"
WAD = ROOT / "formal" / "a116" / "A116" / "Wad.lean"
TEXTS: dict[str, tuple[Path, str]] = {
    "j1": (ROOT / "corpora" / "nabhani" / "shakhsiyya_j1.txt.gz",
           "77d80c69c80cdb967152702458956553a79d89d5ca220926e2b1b01cc24525ab"),
    "j3": (ROOT / "corpora" / "nabhani" / "shakhsiyya_j3.txt.gz",
           "dd57e74bec43534ceec90797ad050cb104a16925b6d0bf0304796d42e70c425e"),
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


def alamat() -> list[str]:
    src = LEAN.read_text(encoding="utf-8")
    decl = re.search(r"inductive Alama \| (.+)", src)
    assert decl is not None
    return [x.strip() for x in decl.group(1).split("|")]


def encode(r: tuple[str, int]) -> int:
    kind, i = r
    return i if kind == "khana" else 116 + i


def decode(b: int, n_alama: int) -> tuple[str, int] | None:
    if b < 116:
        return ("khana", b)
    return ("alama", b - 116) if b - 116 < n_alama else None


def iqtiran(c: list[str], quyud: list[set[str]], any_mode: bool = False) -> list[str]:
    if any_mode:
        return [m for m in c if any(m in q for q in quyud)]
    return [m for m in c if all(m in q for q in quyud)]


def mantuq(rest: list[str], first: bool = False) -> tuple[str, object]:
    if not rest:
        return ("laHukm", None)
    if len(rest) == 1 or first:
        return ("muayyan", rest[0])
    return ("muhtamal", rest)


def martaba(m: tuple[str, object], shahid: set[str]) -> str:
    if m[0] == "muayyan":
        return "mafhum" if m[1] in shahid else "maluma"
    return "maluma" if m[0] == "muhtamal" else "minHaythuHiya"


def test_marasi_in_sealed_lines() -> None:
    ls = {k: lines(k) for k in TEXTS}
    ms = marasi()
    assert len(ms) == 5 and all(q in ls[k][n - 1] for k, n, q in ms)


def test_binary_roundtrip() -> None:
    n = len(alamat())
    assert 116 + n == 2 ** 7
    codes = [("khana", i) for i in range(116)] + [("alama", i) for i in range(n)]
    assert sorted(encode(r) for r in codes) == list(range(128))
    assert all(decode(encode(r), n) == r for r in codes)


def test_rule_grid() -> None:
    c = ["a", "b", "c"]
    qs = [{"a", "b"}, {"b", "c"}, {"a", "b", "c"}, set()]
    for q1, q2 in itertools.product(qs, repeat=2):
        assert iqtiran(c, [q1, q2]) == iqtiran(c, [q2, q1])
        assert set(iqtiran(c, [q1, q2])) <= set(iqtiran(c, [q1]))
    assert mantuq(iqtiran(c, [{"b"}])) == ("muayyan", "b")
    assert mantuq(iqtiran(c, [set()])) == ("laHukm", None)
    assert mantuq(iqtiran(c, [{"a", "b"}]))[0] == "muhtamal"
    for m in [mantuq([]), mantuq(["a"]), mantuq(["a", "b"])]:
        assert martaba(m, set()) != "mafhum"


def test_wad_deposit_ternary() -> None:
    d: dict[str, set[str]] = collections.defaultdict(set)
    for line in (ROOT / "corpora" / "wad" / "wad.tsv").read_text(encoding="utf-8").splitlines():
        key, root, _src = line.split("\t")
        d[key].add(root)
    kinds = collections.Counter(mantuq(sorted(v))[0] for v in d.values())
    assert kinds["laHukm"] == 0
    count = re.search(r"mushtarak\.length = (\d+)", WAD.read_text(encoding="utf-8"))
    assert count is not None and kinds["muhtamal"] == int(count.group(1))
    assert kinds["muayyan"] + kinds["muhtamal"] == len(d)


def test_mutants_rejected() -> None:
    c = ["a", "b", "c"]
    assert iqtiran(c, [{"a"}, {"b"}], any_mode=True) != iqtiran(c, [{"a"}, {"b"}])  # ANY_NOT_ALL
    assert mantuq(["a", "b"], first=True) != mantuq(["a", "b"])                     # FIRST_OF_MANY
    ls = {k: lines(k) for k in TEXTS}
    assert not all(q in ls[k][n] for k, n, q in marasi())                           # LINE_SHIFTED
