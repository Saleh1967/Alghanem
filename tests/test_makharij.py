"""مستوى المخرج والصفة (`A116.Makharij`، ADR ٦٧): الجداولُ في Lean هي ما يقوله الباب بعينه.

لكلّ صفٍّ في `formal/a116/A116/Makharij.lean` مرساةٌ منقولةٌ وحروفٌ تسمّيها. هذا الاختبار:

١. يقرأ «الكتاب» المختوم (`KITAB_SIBAWAYH`: الطولُ والبصمةُ المعلنان؛ المسار من
   `ALGHANEM_SIBAWAYH_PATH` أو `corpora/kitab-sibawayhi-jk006989-ara1.txt`) ويقصّ الباب بين
   مرساتيه (بدايتُه «هذا باب عدد الحروف العربية» ونهايتُه «هذا باب الإدغام»)، ويطبّع علاماتِ
   الطبعة (`~~`، `|`، `PageV..P..`، `ms..`) مسافاتٍ.
٢. يتحقّق أنّ كلَّ مرساةٍ تقع في الباب **مرّةً واحدة**، وأنّ أسماءَ الحروف فيها — بقاموس الأسماء
   المكتوب هنا باليد — هي حروفُ الصفّ بترتيبها.
الطفرات: `MUTANT_SWAPPED_LETTERS` (حرفان مبدَّلان في صفّ)، `MUTANT_ANCHOR_NOT_IN_CHAPTER`
(مرساةٌ مخترَعة)، `MUTANT_FILLED_LAM` (اللامُ مسنَدةٌ إلى مخرجٍ من محفوظ).
لا مودَعَ هنا: إن غاب الملفُّ تخطّى الاختبارُ باسمه `KITAB_NOT_DEPOSITED` — فلا يُعدّ «مفحوصًا»
في CI حتى يُودَع.
"""

from __future__ import annotations

import hashlib
import os
import re
from pathlib import Path

try:
    import pytest
except ModuleNotFoundError:  # تشغيلٌ مباشرٌ بلا pytest
    pytest = None  # type: ignore[assignment]

ROOT = Path(__file__).resolve().parents[1]
LEAN = ROOT / "formal" / "a116" / "A116" / "Makharij.lean"
KITAB_SHA256 = "a160f940bb194e6fe7e6655d2c7f28e41f1fc648c4c5e340cc4e42306d5cb625"
KITAB_LENGTH = 2_639_395

# قاموسُ أسماء الحروف كما يكتبها الباب، باليد.
NAMES = {
    "الهمزة": "ء", "الألف": "ا", "الهاء": "ه", "العين": "ع", "الحاء": "ح", "الغين": "غ",
    "الخاء": "خ", "القاف": "ق", "الكاف": "ك", "الجيم": "ج", "الشين": "ش", "الياء": "ي",
    "الضاد": "ض", "اللام": "ل", "الراء": "ر", "النون": "ن", "الطاء": "ط", "الدال": "د",
    "التاء": "ت", "الصاد": "ص", "الزاي": "ز", "السين": "س", "الظاء": "ظ", "الذال": "ذ",
    "الثاء": "ث", "الفاء": "ف", "الباء": "ب", "الميم": "م", "الواو": "و",
}


def _kitab() -> bytes:
    default = ROOT / "corpora" / "kitab-sibawayhi-jk006989-ara1.txt"
    p = Path(os.environ.get("ALGHANEM_SIBAWAYH_PATH", default))
    if not p.exists():
        if pytest is None:
            raise SystemExit("KITAB_NOT_DEPOSITED")
        pytest.skip("KITAB_NOT_DEPOSITED")
    data = p.read_bytes()
    assert len(data) == KITAB_LENGTH
    assert hashlib.sha256(data).hexdigest() == KITAB_SHA256
    return data


def _chapter(data: bytes) -> str:
    text = data.decode("utf-8")
    start = text.index("هذا باب عدد الحروف العربية ومخارجها")
    end = text.index("هذا باب الإدغام", start)
    body = text[start:end]
    body = re.sub(r"PageV\d+P\d+|ms\d+|~~|\||#", " ", body)
    return re.sub(r"\s+", " ", body)


def _rows() -> list[tuple[str, list[str]]]:
    src = LEAN.read_text(encoding="utf-8")
    rows = re.findall(r'\(\s*"([^"]+)",\s*\[([^\]]*)\]\)', src)
    return [(a, re.findall(r"'(.)'", cs)) for a, cs in rows]


def _named(anchor: str) -> list[str]:
    out = []
    for tok in anchor.split():
        tok = tok[1:] if tok.startswith(("و", "ف")) and tok[1:] in NAMES else tok
        if tok in NAMES:
            out.append(NAMES[tok])
    return out


def _check(chapter: str, rows: list[tuple[str, list[str]]]) -> list[str]:
    bad = []
    for anchor, letters in rows:
        if chapter.count(anchor) != 1:
            bad.append(f"ANCHOR_NOT_ONCE: {anchor}")
        named = _named(anchor)
        # «مخرج النون الخفيفة» فرعٌ لا أصل: الصفُّ فارغ؛ وما سواه حروفُه آخرُ ما يسمّيه.
        expect = [] if "الخفيفة" in anchor else named[-len(letters):] if letters else named
        if letters and named[-len(letters):] != letters:
            bad.append(f"LETTERS_DIFFER: {anchor} {letters} vs {named}")
        if not letters and "الخفيفة" not in anchor:
            bad.append(f"EMPTY_ROW: {anchor} {expect}")
    return bad


def test_rows_are_the_chapter() -> None:
    chapter = _chapter(_kitab())
    rows = _rows()
    assert len(rows) == 15 + 2 + 8 + 1  # المخارج، الجهرُ والهمس، الأصناف، الإطباق
    assert _check(chapter, rows) == []


def test_stated_counts_in_chapter() -> None:
    chapter = _chapter(_kitab())
    assert "ولحروف العربية ستة عشر مخرجا" in chapter
    assert "فذلك تسعة عشر حرفا" in chapter and "فذلك عشرة أحرف" in chapter
    assert "مخرج اللام" not in chapter  # الساقطُ مسمًّى لا مسدود


def test_mutants_rejected() -> None:
    chapter = _chapter(_kitab())
    rows = _rows()
    swapped = list(rows)
    a, ls = swapped[0]
    swapped[0] = (a, [ls[1], ls[0], *ls[2:]])
    assert _check(chapter, swapped)                                        # MUTANT_SWAPPED_LETTERS
    assert _check(chapter, [*rows, ("مخرج اللام من حافة اللسان", ["ل"])])   # MUTANT_FILLED_LAM
    invented = ("ومن طرف اللسان مخرج الضاد", ["ض"])
    assert _check(chapter, [*rows, invented])  # MUTANT_ANCHOR_NOT_IN_CHAPTER


if __name__ == "__main__":
    test_rows_are_the_chapter()
    test_stated_counts_in_chapter()
    test_mutants_rejected()
    print("test_makharij: 3/3")
