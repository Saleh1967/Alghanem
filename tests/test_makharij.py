"""مستوى المخرج والصفة وقانونُ الإدغام (`A116.Makharij`، `A116.MakharijIdgham`؛ ADR ٦٧، ٦٨).

الصفوفُ في Lean هي ما تقوله النصوصُ المختومة بعينها. النصوصُ من `corpora/kitab/` بعد التحقّق
من بصماتها (`tools/gen_kitab.py`). هذا الاختبار:

١. **باب المخارج** («هذا باب عدد الحروف العربية ومخارجها» … «هذا باب الإدغام») من نسخة
   JK006989: كلُّ مرساةٍ تقع فيه **مرّةً واحدة**، وأسماءُ الحروف فيها — بقاموس أسماءٍ مكتوبٍ
   هنا باليد — هي حروفُ الصفّ بترتيبها.
٢. **مخرجُ اللام**: غائبٌ من نسختي الكتاب، وحاضرٌ مرّةً واحدة في نقل السيرافيّ بعد «قال سيبويه»،
   بين مخرج الضاد ومخرج النون؛ وموضعُ إدخاله في Lean (`makharij.take N`) بين صفّي الضاد والنون.
٣. **أبوابُ الإدغام** الثلاثة من JK006989: كلُّ مرساةٍ تقع فيها مرّةً واحدة، وحروفُ الصفّ هي
   المسمّاةُ فيها، أو — لما تُفهم حروفُه من المثال أو الضمير أو الإحالة — ما كُتب هنا باليد.

الطفرات: `MUTANT_SWAPPED_LETTERS`، `MUTANT_ANCHOR_NOT_IN_CHAPTER`، `MUTANT_FILLED_LAM` (مخرجُ
اللام بصياغةٍ من محفوظ)، `MUTANT_LAM_AFTER_NUN`، `MUTANT_IDGHAM_LETTER_WRONG`، `MUTANT_ONE_BYTE`.
"""

from __future__ import annotations

import hashlib
import importlib.util
import re
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("gen_kitab", ROOT / "tools" / "gen_kitab.py")
assert SPEC and SPEC.loader
KITAB: Any = importlib.util.module_from_spec(SPEC)
sys.modules["gen_kitab"] = KITAB
SPEC.loader.exec_module(KITAB)

LEAN = ROOT / "formal" / "a116" / "A116"
JK = "0180Sibawayhi.KitabSibawayhi.JK006989-ara1"
SHAMELA = "0180Sibawayhi.KitabSibawayhi.Shamela0023018-ara1.mARkdown"
SIRAFI = "0368AbuSacidSirafi.SharhKitabSibawayhi.Sham19Y0017726-ara1"
HAND_SHA = {  # من الحساب على نسخ OpenITI في الجلسة (2026-10-15)
    JK: "a160f940bb194e6fe7e6655d2c7f28e41f1fc648c4c5e340cc4e42306d5cb625",
    SHAMELA: "ad676dffaa6df22a7b2ef4c4dbc4424d1e214e09e3f296a538ce887c89affcad",
    SIRAFI: "d53137fd4151028c5dee8ab9ff3e42275ecf0c39089e15fbf50bf0eefaa1603a",
}

# قاموسُ أسماء الحروف كما تكتبها الأبواب، باليد.
NAMES = {
    "الهمزة": "ء", "الألف": "ا", "الهاء": "ه", "العين": "ع", "الحاء": "ح", "الغين": "غ",
    "الخاء": "خ", "القاف": "ق", "الكاف": "ك", "الجيم": "ج", "الشين": "ش", "الياء": "ي",
    "الضاد": "ض", "اللام": "ل", "الراء": "ر", "النون": "ن", "الطاء": "ط", "الدال": "د",
    "التاء": "ت", "الصاد": "ص", "الزاي": "ز", "السين": "س", "الظاء": "ظ", "الذال": "ذ",
    "الثاء": "ث", "الفاء": "ف", "الباء": "ب", "الميم": "م", "الواو": "و",
}

# صفوفُ الإدغام التي تُفهم حروفُها من المثال أو من الضمير: (المدغَمات، المدغَمُ فيها) باليد.
IMPLICIT = {
    "الهاء مع الحاء كقولك اجبه حملا": ("ه", "ح"),
    "وتدغم في اللام لأنها قريبة منها": ("ن", "ل"),
    "ولا تدغم في حروف الحلق البتة": ("ن", "ءهعحغخ"),
    "وأما اللام فقد تدغم فيها وذلك قولك هنرى": ("ل", "ن"),
    "اصحمطرا تريد اصحب مطرا مدغم": ("ب", "م"),
    "والأحد عشر حرفا النون والراء والدال والتاء والصاد والطاء والزاي والسين والظاء والثاء والذال":
        ("ل", "نردتصطزسظثذ"),
    "واللذان خالطاها الضاد والشين": ("ل", "ضش"),
    "ومن الحروف ما لا يدغم في مقاربه ولا يدغم فيه مقاربه": ("ءه", "ءه"),
    "وكذلك التاء وهو قولك انعطالبا": ("ت", "ط"),
    "وذلك قولك افحسالما فتصير سينا": ("ص", "س"),
    "وتقول افحزردة": ("ص", "ز"),
    "وذلك قولك احبصابرا وأحوصابرا": ("سز", "ص"),
    "وذلك قولك احفذلك فتدغم": ("ظ", "ذ"),
    "وتقول احفثابتا": ("ظ", "ث"),
    "وذلك قولك خظالما": ("ذ", "ظ"),
    "وذلك احفضرمة وخضرمة وابعضرمة": ("ظذث", "ض"),
    "ولا تدغم الصاد وأختاها فيها": ("صسز", "ض"),
    "وتدغم الظاء والذال والثاء فيها لأنهم قد أنزلوها منزلة الضاد": ("ظذث", "ش"),
    # تشبيهٌ يسمّي حرفين آخرين («بمنزلة التاء والدال»)، أو إحالةٌ إلى ما قبلها («وكذلك»، «هذه الحروف»):
    "والزاي والسين بمنزلة التاء والدال تقول احبزردة ورسلمة فتدغم": ("زس", "زس"),
    "والذال والثاء منزلة كل واحدة منهما من صاحبتها منزلة الدال والتاء": ("ذث", "ذث"),
    "وكذلك الظاء والثاء والذال لأنهن من طرف اللسان وأطراف الثنايا": ("ظثذ", "صزس"),
    "وأما الصاد والسين والزاي فلا تدغمهن في هذه الحروف التي أدغمت فيهن": ("صسز", "طدتظثذ"),
}


def _norm(body: str) -> str:
    body = re.sub(r"PageV\d+P\d+|ms\d+|~~|\||#", " ", body)
    return re.sub(r"\s+", " ", body)


def _between(name: str, start: str, end: str) -> str:
    text = KITAB.text(name)
    a = text.index(start)
    return _norm(text[a:text.index(end, a)])


def _makharij_chapter() -> str:
    return _between(JK, "هذا باب عدد الحروف العربية ومخارجها", "هذا باب الإدغام")


def _idgham_chapters() -> str:
    return _between(JK, "هذا باب الإدغام في الحرفين اللذين", "هذا باب الحرف الذي يضارع")


def _sirafi_lemma() -> str:
    start = "قال سيبويه: وحروف العربية ستة عشر مخرجا"
    return _between(SIRAFI, start, "ومن الخياشيم مخرج النون الخفيفة")


def _rows() -> list[tuple[str, list[str]]]:
    src = (LEAN / "Makharij.lean").read_text(encoding="utf-8")
    rows = re.findall(r'\(\s*"([^"]+)",\s*\[([^\]]*)\]\)', src)
    return [(a, re.findall(r"'(.)'", cs)) for a, cs in rows]


def _idgham_rows() -> list[tuple[str, str, str, bool]]:
    src = (LEAN / "MakharijIdgham.lean").read_text(encoding="utf-8")
    rows = re.findall(r'⟨"([^"]+)", \[([^\]]*)\], \[([^\]]*)\], (true|false)⟩', src)
    return [(a, "".join(re.findall(r"'(.)'", s)), "".join(re.findall(r"'(.)'", d)), f == "true")
            for a, s, d, f in rows]


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
        if letters and named[-len(letters):] != letters:
            bad.append(f"LETTERS_DIFFER: {anchor} {letters} vs {named}")
        if not letters and "الخفيفة" not in anchor:
            bad.append(f"EMPTY_ROW: {anchor}")
    return bad


def _lam_row(rows: list[tuple[str, list[str]]]) -> tuple[str, list[str]]:
    return next(r for r in rows if r[1] == ["ل"] and "مخرج اللام" in r[0])


def _check_lam(lemma: str, anchor: str, take: int,
               kitab_rows: list[tuple[str, list[str]]]) -> list[str]:
    bad = []
    if lemma.count(anchor) != 1:
        bad.append("LAM_ANCHOR_NOT_IN_SIRAFI")
    elif not lemma.index("من الأضراس") < lemma.index(anchor) < lemma.index("مخرج النون"):
        bad.append("LAM_NOT_BETWEEN_DAD_AND_NUN")
    if kitab_rows[take - 1][1] != ["ض"] or kitab_rows[take][1] != ["ن"]:
        bad.append("LAM_INSERTED_ELSEWHERE")
    return bad


def _take() -> int:
    src = (LEAN / "Makharij.lean").read_text(encoding="utf-8")
    m = re.search(r"makharij\.take (\d+) \+\+ \[lamRow\]", src)
    assert m
    return int(m.group(1))


def _check_idgham(chapters: str, rows: list[tuple[str, str, str, bool]]) -> list[str]:
    bad = []
    for anchor, src, dst, _ in rows:
        if chapters.count(anchor) != 1:
            bad.append(f"ANCHOR_NOT_ONCE: {anchor}")
        if anchor in IMPLICIT:
            hs, hd = IMPLICIT[anchor]
            if not (set(src) <= set(hs) and set(dst) <= set(hd)):
                bad.append(f"IMPLICIT_DIFFERS: {anchor}")
        elif set(_named(anchor)) != set(src) | set(dst):
            bad.append(f"LETTERS_DIFFER: {anchor} {src}/{dst} vs {_named(anchor)}")
    return bad


def test_seals_by_hand() -> None:
    for name, sha in HAND_SHA.items():
        assert hashlib.sha256(KITAB.text(name).encode("utf-8")).hexdigest() == sha, name
    assert KITAB.breaches() == []


def test_mutant_one_byte_rejected() -> None:
    raw = bytearray(KITAB.text(JK).encode("utf-8"))
    raw[len(raw) // 2] ^= 1
    assert hashlib.sha256(bytes(raw)).hexdigest() != HAND_SHA[JK]  # MUTANT_ONE_BYTE


def test_rows_are_the_chapter() -> None:
    rows = _rows()
    lam = _lam_row(rows)
    kitab_rows = [r for r in rows if r != lam]
    assert len(kitab_rows) == 15 + 2 + 8 + 1  # المخارج، الجهرُ والهمس، الأصناف، الإطباق
    assert _check(_makharij_chapter(), kitab_rows) == []


def test_stated_counts_in_chapter() -> None:
    chapter = _makharij_chapter()
    assert "ولحروف العربية ستة عشر مخرجا" in chapter
    assert "فذلك تسعة عشر حرفا" in chapter and "فذلك عشرة أحرف" in chapter


def test_lam_absent_from_both_kitab_texts_present_in_sirafi() -> None:
    assert "مخرج اللام" not in _makharij_chapter()
    shamela = _between(SHAMELA, "ولحروف العربية ستة عشر مخرجا", "مخرج النون الخفيفة")
    assert "مخرج اللام" not in shamela
    rows = _rows()
    lam = _lam_row(rows)
    kitab_rows = [r for r in rows if r != lam][:15]
    assert _check_lam(_sirafi_lemma(), lam[0], _take(), kitab_rows) == []


def test_idgham_rows_are_the_chapters() -> None:
    rows = _idgham_rows()
    assert len(rows) == 52
    assert _check_idgham(_idgham_chapters(), rows) == []


def test_mutants_rejected() -> None:
    chapter = _makharij_chapter()
    rows = _rows()
    lam = _lam_row(rows)
    kitab_rows = [r for r in rows if r != lam]
    swapped = list(kitab_rows)
    a, ls = swapped[0]
    swapped[0] = (a, [ls[1], ls[0], *ls[2:]])
    assert _check(chapter, swapped)  # MUTANT_SWAPPED_LETTERS
    invented = ("ومن طرف اللسان مخرج الضاد", ["ض"])
    assert _check(chapter, [*kitab_rows, invented])  # MUTANT_ANCHOR_NOT_IN_CHAPTER
    lemma = _sirafi_lemma()
    remembered = "ومن حافة اللسان من أدناها إلى منتهى طرف اللسان مخرج اللام"
    assert _check_lam(lemma, remembered, _take(), kitab_rows[:15])  # MUTANT_FILLED_LAM
    assert _check_lam(lemma, lam[0], _take() + 1, kitab_rows[:15])  # MUTANT_LAM_AFTER_NUN
    idg = _idgham_rows()
    wrong = [(a, s, "ع" if d == "ش" else d, f) for a, s, d, f in idg]
    assert _check_idgham(_idgham_chapters(), wrong)  # MUTANT_IDGHAM_LETTER_WRONG


if __name__ == "__main__":
    tests = [v for k, v in sorted(globals().items()) if k.startswith("test_")]
    for t in tests:
        t()
    sys.stdout.write(f"test_makharij: {len(tests)}/{len(tests)}\n")
