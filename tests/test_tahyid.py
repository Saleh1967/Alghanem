"""التحييد (ADR ٥٩): سلسلةُ الحاويتين ← الباب ← النصّ المختوم ← الصورة القانونيّة، بتوقّعاتٍ مستقلّة.

١. البصماتُ أرقامٌ مكتوبةٌ باليد من سجلّ الغانم (f0024، f0025) ومن الختم السابق للنصّين، لا من الأداة.
٢. الاستثناءُ البنيويّ يُعاد بمفسِّرٍ آخر: مكدَّسُ وسومٍ على نصّ `document.xml` بالتعبير النمطيّ، لا شجرة
   ElementTree التي يمشي عليها الباب؛ والفقراتُ المستثناةُ في ج3 مكتوبةٌ باليد.
٣. القاعدتان وترتيبُهما بأسطرٍ باليد؛ والشكلُ يُعدّ بـ`unicodedata` على النصّ المختوم مباشرة.
وكلُّ قسمٍ بطفرةٍ مرفوضةٍ باسمها: `STRIP_BEFORE_TAB`، `NO_STRUCTURAL_EXCLUSION`، `EXCLUSION_BY_CONTENT`،
`MARKS_DROPPED`، `DOOR_NORMALIZES`.
"""

from __future__ import annotations

import gzip
import hashlib
import importlib.util
import io
import re
import sys
import unicodedata
import zipfile
from collections.abc import Callable
from pathlib import Path

from slge import tahyid as T

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "tests" / "data"
SPEC = importlib.util.spec_from_file_location("deposit_tahyid",
                                              ROOT / "tools" / "deposit_tahyid.py")
assert SPEC is not None and SPEC.loader is not None
MOD = importlib.util.module_from_spec(SPEC)
sys.modules["deposit_tahyid"] = MOD
SPEC.loader.exec_module(MOD)

# (الحاوية — سجلُّ الغانم f0024/f0025، النصُّ المختوم — test_seals، الصورةُ القانونيّة، عددُ أسطرها)
SEALS = {
    1: ("5e327aa2563af094962833951972b7537a872119a58bbfce5f2a813d20c88e17",
        "b474d56021427070e2e3852b78bb774383f37bf87e2310d39dcdbaecf33aed63",
        "263bbd85a961ced7d982c99bde7d0715409490314aad1222e0d681d082741567", 742),
    3: ("360f7653df4e3396d18153d0ea31e607523d33e0cb552b419340400b2211d5bd",
        "359bb5532ecee8156f266522bb5388a1711e46e136004c3ac22e43f2ce656cb4",
        "80801201508b4c41771eab5cb7dc4fa420770913fde0a5177f589b3aa67ea9a1", 1079),
}
EXCLUDED_J3 = [*range(18, 23), *range(427, 430), *range(680, 683), *range(879, 882)]
"""فقراتُ ج3 داخل جدولٍ أو صندوقِ نصٍّ أو حاملةٌ له (1-based) — بالعين من document.xml."""

Rows = list[tuple[bool, str]]


def _raw(n: int) -> bytes:
    return (DATA / f"nabhani-shakhsiyya-{n}.docx").read_bytes()


def _sealed(n: int) -> str:
    return gzip.decompress((DATA / f"nabhani-shakhsiyya-{n}.txt.gz").read_bytes()).decode("utf-8")


def _canonical(n: int) -> bytes:
    return gzip.decompress((DATA / f"nabhani-shakhsiyya-{n}.canonical.txt.gz").read_bytes())


TAG = re.compile(rb"<(/?)w:(p|tbl|txbxContent)(?=[\s>/])([^>]*?)(/?)>")


def _excluded_by_stack(raw: bytes) -> list[int]:
    """مفسِّرٌ مستقلّ: مكدَّسُ الوسوم على النصّ الخامّ؛ صندوقُ نصٍّ يُفتح يُعلِّم كلَّ فقرةٍ مفتوحةٍ حاملةً."""

    xml = zipfile.ZipFile(io.BytesIO(raw)).read("word/document.xml")
    stack: list[tuple[str, int]] = []
    flags: list[bool] = []
    for m in TAG.finditer(xml):
        close, name, selfclose = m.group(1) == b"/", m.group(2).decode(), m.group(4) == b"/"
        if close:
            assert stack and stack[-1][0] == name
            stack.pop()
            continue
        if name == "p":
            flags.append(any(k in ("tbl", "txbxContent") for k, _ in stack))
            if not selfclose:
                stack.append(("p", len(flags) - 1))
        elif not selfclose:
            if name == "txbxContent":
                for k, i in stack:
                    if k == "p":
                        flags[i] = True
            stack.append((name, -1))
    return [i + 1 for i, x in enumerate(flags) if x]


# ١. البصماتُ والباب -----------------------------------------------------------------------------

def test_containers_and_door_reproduce_the_seals() -> None:
    for n, (c_sha, t_sha, _, _) in SEALS.items():
        raw = _raw(n)
        assert hashlib.sha256(raw).hexdigest() == c_sha
        text = "\n".join(t for _, t in MOD.door(raw))
        assert text == _sealed(n)
        assert hashlib.sha256(text.encode("utf-8")).hexdigest() == t_sha


def test_mutant_door_normalizes_rejected() -> None:
    """`DOOR_NORMALIZES`: بابٌ يطبّع (NFC) لا يعيد المختوم — فالبابُ بلا تطبيعٍ شرطٌ لا ذوق."""

    for n in SEALS:
        text = "\n".join(unicodedata.normalize("NFC", t) for _, t in MOD.door(_raw(n)))
        assert text != _sealed(n)


# ٢. الاستثناءُ البنيويّ -----------------------------------------------------------------------------

def test_structural_exclusion_by_independent_parser() -> None:
    for n in SEALS:
        rows = MOD.door(_raw(n))
        assert [i + 1 for i, (x, _) in enumerate(rows) if x] == _excluded_by_stack(_raw(n))
    assert _excluded_by_stack(_raw(3)) == EXCLUDED_J3
    assert _excluded_by_stack(_raw(1)) == []


def test_mutant_no_structural_exclusion_rejected() -> None:
    """`NO_STRUCTURAL_EXCLUSION`: بلا استثناءٍ تزيد الصورةُ القانونيّة لج3 أسطرَ الجداول والصناديق."""

    rows = MOD.door(_raw(3))
    got = T.canon((False, t) for _, t in rows)
    assert len(got) > SEALS[3][3]
    assert "\n".join(got).encode("utf-8") != _canonical(3)


def test_mutant_exclusion_by_content_rejected() -> None:
    """`EXCLUSION_BY_CONTENT`: استثناءُ الأسطر القصيرة (دون عشرين حرفًا) بدل البنية يغيّر الصورتين."""

    for n in SEALS:
        rows = [(len(t.strip()) < 20, t) for _, t in MOD.door(_raw(n))]
        assert "\n".join(T.canon(rows)).encode("utf-8") != _canonical(n)


# ٣. القاعدتان وترتيبُهما والشكل --------------------------------------------------------------------

LINES = (  # (السطر، clean، يغيّر الترتيبُ الناتج) — باليد
    ("", "", False), (" \t ", "", False), ("a \t", "a", True), ("\t a", "a", True),
    ("a\t ", "a", False), (" a\tb ", "ab", False), (" بِسْمِ ", "بِسْمِ", False),
)


def test_rules_by_hand() -> None:
    for line, clean, crit in LINES:
        assert T.clean(line) == clean
        assert T.order_matters(line) is crit
    assert T.canon([(False, " a\t"), (False, "\t "), (True, "x"), (False, "c")]) == ["a", "c"]


def _canon_with(clean: Callable[[str], str], rows: Rows) -> list[str]:
    return [c for x, t in rows if not x and (c := clean(t))]


def test_mutant_strip_before_tab_rejected() -> None:
    """`STRIP_BEFORE_TAB`: القصُّ قبل حذف الجدولة يترك المسافةَ في «a \\t» —
    والترتيبُ معلنٌ لأنّه يغيّر."""

    def mutant(t: str) -> str:
        return T.del_tab(T.strip_sp(t))

    assert _canon_with(mutant, [(False, "a \t")]) == ["a "]
    assert T.canon([(False, "a \t")]) == ["a"]


def _marks(text: str) -> int:
    return sum(1 for ch in text if unicodedata.category(ch) == "Mn")


def test_canonical_deposits_and_marks() -> None:
    for n, (_, _, k_sha, lines) in SEALS.items():
        data = _canonical(n)
        assert hashlib.sha256(data).hexdigest() == k_sha
        out = data.decode("utf-8").split("\n")
        assert len(out) == lines
        assert all(ln and ln == ln.strip(" ") and "\t" not in ln for ln in out)
        kept = [t for x, t in MOD.door(_raw(n)) if not x]
        assert _marks("".join(out)) == _marks("".join(kept)) > 0
        assert T.canon((False, ln) for ln in out) == out


def test_mutant_marks_dropped_rejected() -> None:
    """`MARKS_DROPPED`: تنظيفٌ يحذف علامات الشكل مع المسافات يُسقط ما تحفظه `marks_preserved`."""

    def mutant(t: str) -> str:
        return "".join(ch for ch in T.clean(t) if unicodedata.category(ch) != "Mn")

    kept = [t for x, t in MOD.door(_raw(1)) if not x]
    assert _marks("".join(_canon_with(mutant, [(False, t) for t in kept]))) < _marks("".join(kept))


# ADR ٦٠: استخراجُ hamil لج3 منظرٌ للحاوية نفسها. بصمتُه وطولُه منقولان باليد من ختم hamil
# (`shakhsiyya_v0.json`: «ختمُ متن الشخصية ج٣»، «طولُ متن الشخصية ج٣»)، لا من الأداة.
HAMIL_J3_BY_HAND = ("520b8e9d55135217d2c07bf521a63ed93431d46bd5cdf16f360c915d8bbfc783", 1241712)


def _sha_len(b: bytes) -> tuple[str, int]:
    return hashlib.sha256(b).hexdigest(), len(b)


def test_hamil_view_is_a_view_of_the_same_container() -> None:
    rows = MOD.door_tabs(_raw(3))
    view = MOD.hamil_view(rows)
    assert _sha_len(view) == HAMIL_J3_BY_HAND
    lines = view.decode("utf-8").split("\n")[:-1]
    # حذفُ الجدولة يردّ منظرَ hamil إلى الصورة القانونيّة سطرًا سطرًا
    assert [ln.replace("\t", "") for ln in lines] == _canonical(3).decode("utf-8").split("\n")
    # والبابُ ذو الجدولة لا يخالف البابَ المختوم إلّا بالجدولة
    assert [t.replace("\t", "") for _, t in rows] == _sealed(3).split("\n")
    assert MOD.AUTHORITY == "sealed"


def test_mutant_hamil_view_tab_blind_rejected() -> None:
    # HAMIL_VIEW_TAB_BLIND: البابُ المختوم بلا جدولة لا يعيد ختمَ hamil
    assert _sha_len(MOD.hamil_view(MOD.door(_raw(3)))) != HAMIL_J3_BY_HAND


def test_mutant_hamil_view_space_only_strip_rejected() -> None:
    # HAMIL_VIEW_SPACE_ONLY_STRIP: قصُّ المسافة وحدَها يُبقي جدولةً في الطرف
    rows = MOD.door_tabs(_raw(3))
    kept = [c for x, t in rows if not x and (c := t.strip(" "))]
    assert _sha_len(("\n".join(kept) + "\n").encode("utf-8")) != HAMIL_J3_BY_HAND
