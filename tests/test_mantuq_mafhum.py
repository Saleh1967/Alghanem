"""الجسرُ من المنطوق إلى المفهوم الأصوليّ (ADR ١١٢، `A116.MantuqMafhum`).

* المراسي: كلُّ (سطر، عبارة) في `marasi` من Lean في سطره بعينه من ج3 المختومة ببصمتها،
  والقائمةُ (الموضع ← السطر) مكتوبةٌ هنا باليد.
* اقتباساتُ الترويسة: كلُّ «…» في بندٍ مرقَّمٍ بـ«سNNN» في سطرٍ من أسطر بنده.
* معاني الشواهد في Lean (`maaniShawahid`) بلفظها في أسطرها، والقائمةُ باليد.
* الحصر: الأصنافُ الأربعة في س534 وس555 بلفظها هي قيودُ `arbaa` الصادقة في Lean،
  والموانعُ بأسطرها، وكلُّ مانعٍ سطرُه سطرُ مرساته.
* ضبطٌ سالبٌ على البيانات: كلُّ مرساةٍ تسقط إذا أُزيحت سطرًا (المرساةُ بسطرها لا بقربه).
"""

from __future__ import annotations

import gzip
import hashlib
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LEAN = ROOT / "formal" / "a116" / "A116" / "MantuqMafhum.lean"
J3 = ROOT / "corpora" / "nabhani" / "shakhsiyya_j3.txt.gz"
J3_SHA = "dd57e74bec43534ceec90797ad050cb104a16925b6d0bf0304796d42e70c425e"

# باليد من قراءة ج3 في الجلسة (2026-10-18)، لا من Lean.
EXPECTED = {
    "mantuq": 516, "mafhum": 518, "iqtida": 520, "tanbih": 522, "ishara": 524,
    "muwafaqa": 526, "tabi": 528, "awlawiyya": 528, "qiyas": 532, "mukhalafa": 534,
    "sifa": 536, "shart": 541, "ghaya": 546, "adad": 548, "adadSiyaq": 548, "ism": 550,
    "ghayrMufhim": 551, "innama": 552, "aghlab": 553, "muattil": 554, "hasr": 555,
}
MAANI = [
    (536, "عدم الوجوب في المعلوفة"), (541, "عدم وجوب الإنفاق بعدم الحمل"),
    (546, "بعد دخول الليل لا صيام"), (548, "تحـريم ما زاد على المائة"),
]
MARFUDA = [
    (548, "القرشين"), (550, "زيد قائم"), (551, "للسائل"), (551, "لمحتجر"), (552, "إنما"),
    (553, "في الحجر"), (554, "أضعافاً مضاعفة"),
]
MANI = {"adadBilaSiyaq": (548, "adadSiyaq"), "ism": (550, "ism"),
        "wasfGhayrMufhim": (551, "ghayrMufhim"), "innama": (552, "innama"),
        "aghlab": (553, "aghlab"), "muattil": (554, "muattil")}


def j3() -> list[str]:
    raw = gzip.decompress(J3.read_bytes())
    assert hashlib.sha256(raw).hexdigest() == J3_SHA
    return raw.decode("utf-8").splitlines()


def src() -> str:
    return LEAN.read_text(encoding="utf-8")


def lean_marasi() -> list[tuple[str, int, str]]:
    block = src()[src().index("def marasi"):src().index("def maaniShawahid")]
    return [(k, int(n), q) for k, n, q in re.findall(r'\("(\w+)", (\d+), "([^"]+)"\)', block)]


def lean_pairs(name: str, end: str) -> list[tuple[int, str]]:
    block = src()[src().index(name):src().index(end)]
    return [(int(n), q) for n, q in re.findall(r'\((\d+), "([^"]+)"\)', block)]


def anchored(lines: list[str], n: int, q: str) -> bool:
    return 1 <= n <= len(lines) and q in lines[n - 1]


def test_marasi_in_sealed_j3() -> None:
    lines = j3()
    assert len(lines) == 1090
    m = lean_marasi()
    assert {k: n for k, n, _ in m} == EXPECTED and len(m) == len(EXPECTED)
    for k, n, q in m:
        assert anchored(lines, n, q), (k, n)


def test_anchor_shift_refused() -> None:
    """ضبطٌ سالب على البيانات: إزاحةُ أيّ مرساةٍ سطرًا تُسقطها."""
    lines = j3()
    for k, n, q in lean_marasi():
        assert not anchored(lines, n - 1, q) and not anchored(lines, n + 1, q), k


def test_header_quotes() -> None:
    """كلُّ «…» في بندٍ من الترويسة مرقَّمٍ بأسطره يقع في أحد تلك الأسطر بلفظه."""
    lines = j3()
    header = src()[:src().index("## ما يُبنى")]
    checked = 0
    for b in re.split(r"\n\* ", header)[1:]:
        text = re.sub(r"\s*\n\s*", " ", b)
        nums = [int(x) for x in re.findall(r"س(\d{3})", text)]
        for q in re.findall(r"«([^«»]+)»", text):
            assert any(anchored(lines, n, q) for n in nums), q
            checked += 1
    assert checked >= 20


def test_maani_in_lines() -> None:
    lines = j3()
    assert lean_pairs("def maaniShawahid", "def alfazMarfuda") == MAANI
    assert lean_pairs("def alfazMarfuda", "end A116.MantuqMafhum") == MARFUDA
    for n, q in MAANI + MARFUDA:
        assert q in lines[n - 1], (n, q)
    block = src()[src().index("theorem shawahid"):src().index("## ٤.")]
    for _, q in MAANI:                       # كلُّ معنًى معمولٍ به في `shawahid` بعينه
        assert block.count(f'"{q}"') == 2, q
    adafan = next(ln for ln in src().splitlines() if ln.startswith("def adafan"))
    assert '"أضعافاً مضاعفة"' in adafan       # لفظُ `adafan` لفظُ س554


def test_hasr_arbaa_from_text() -> None:
    lines = j3()
    names = ("الصفة", "الشرط", "الغاية", "العدد")
    for n in (534, 555):
        found = re.findall(r"مفهوم (\S+?)[،,.\s]", lines[n - 1])
        assert [x for x in found if x in names] == list(names), n
    assert "  | .sifa _ | .shart | .ghaya | .adad _ => true" in src()
    assert "  | .ism | .innama => false" in src()


def test_mani_lines() -> None:
    block = src()[src().index("inductive Mani"):src().index("structure MafhumUsul")]
    got = {k: int(v) for k, v in re.findall(r"\| (\w+)\s+-- س(\d+)", block)}
    assert got == {k: n for k, (n, _) in MANI.items()}
    marasi = {k: n for k, n, _ in lean_marasi()}
    for k, (n, key) in MANI.items():
        assert marasi[key] == n, k


def test_constitution_art24_names_theorems() -> None:
    const = (ROOT / "AGENT_CONSTITUTION.md").read_text(encoding="utf-8")
    start = const.index("## المادّة ٢٤")
    art = const[start:const.index("---", start)]
    for t in ("la_martaba_bila_shahid", "la_mafhum_wad_bila_shahid", "la_mafhum_waqi_bila_shahid",
              "shahid_ghayrih_la_yarfa"):
        assert t in art, t
