"""المجازُ في المصدر والمشتقّ، والحقيقةُ شرطُ إمكان المجاز (`A116.Majaz`، ADR ٩٤).

التوقّعاتُ مستقلّةٌ عن Lean:
١. كلُّ مرساةٍ في `Majaz.marasi` نصٌّ في سطرها (1-based) من ج3 المختومة ببصمتها هنا.
٢. الأقسامُ الستّة مستخرجةٌ من س410 بنمط «إطلاق X على Y»، وتطابق صفوفَ `sitta` في Lean، وتغطّي
   كلَّ الأزواج المرتّبة المتباينة من الثلاثة.
٣. شروطُ س415 مقروءةٌ من سطرها: المجازُ إلى الوضع الأوّل والمناسبة والنقل، والحقيقةُ إلى الوضع
   الأوّل وحدَه؛ وما لا يدخله المجازُ بالذات في س412–414 بترتيبه (الحرف، الفعل والمشتقّ، العلم).
الطفرات: `MUTANT_PAIR_DROPPED`، `MUTANT_WAZN_IS_ROLE`، `MUTANT_LINE_SHIFTED`.
"""

from __future__ import annotations

import gzip
import hashlib
import itertools
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LEAN = ROOT / "formal" / "a116" / "A116" / "Majaz.lean"
J3 = (ROOT / "corpora" / "nabhani" / "shakhsiyya_j3.txt.gz",
      "dd57e74bec43534ceec90797ad050cb104a16925b6d0bf0304796d42e70c425e")
NAMES = {"المصدر": "masdar", "اسم الفاعل": "faail", "اسم المفعول": "mafool"}


def lines() -> list[str]:
    raw = gzip.decompress(J3[0].read_bytes())
    assert hashlib.sha256(raw).hexdigest() == J3[1]
    return raw.decode("utf-8").splitlines()


def marasi() -> list[tuple[str, int, str]]:
    src = LEAN.read_text(encoding="utf-8")
    block = src[src.index("def marasi"):]
    return [(k, int(n), q) for k, n, q in re.findall(r'\("(\w+)", (\d+), "([^"]+)"\)', block)]


def pairs_from_text(ls: list[str]) -> list[tuple[str, str]]:
    alt = "|".join(NAMES)
    line = ls[410 - 1].replace("\u0640", "")                     # الطبعةُ تكتب «اسـم» بالتطويل
    found = re.findall(rf"إطلاق ({alt}) على ({alt})", line)
    return [(NAMES[a], NAMES[b]) for a, b in found]


def pairs_from_lean() -> list[tuple[str, str]]:
    src = LEAN.read_text(encoding="utf-8")
    block = src[src.index("def sitta"):src.index("def sighat")]
    return re.findall(r"\(\.(\w+), \.(\w+), \"", block)


def test_marasi_in_sealed_lines() -> None:
    ls = lines()
    ms = marasi()
    assert len(ms) == 17 and all(q in ls[n - 1] for _, n, q in ms)


def test_sitta_from_text() -> None:
    text = pairs_from_text(lines())
    assert len(text) == 6 and len(set(text)) == 6
    assert set(text) == set(pairs_from_lean())
    allp = {(a, b) for a, b in itertools.permutations(NAMES.values(), 2)}
    assert set(text) == allp


def test_shurut_and_order_from_text() -> None:
    ls = lines()
    l415 = ls[415 - 1]
    majaz = [k for k in ("إلى الوضع الأول", "وإلى المناسبة", "وإلى النقل") if k in l415]
    assert len(majaz) == 3 and "الحقيقة لا تحتاج إلا إلى الوضع الأول" in l415
    assert ls[412 - 1].startswith("أحدها الحرف")
    assert ls[413 - 1].startswith("ثانيها: الفعل بأقسامه، والمشتق بأقسامه")
    assert ls[414 - 1].startswith("ثالثها: العلم")


def test_mutants_rejected() -> None:
    text = pairs_from_text(lines())
    allp = {(a, b) for a, b in itertools.permutations(NAMES.values(), 2)}
    assert set(text[:-1]) != allp                                 # قسمٌ ساقط
    assert any(a != b for a, b in text)                           # الوزنُ ليس الدور
    ls = lines()
    assert not all(q in ls[n] for _, n, q in marasi())
