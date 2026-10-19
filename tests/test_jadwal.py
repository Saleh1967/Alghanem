"""جدولُ المخارج والصفات (`A116.Jadwal`، ADR ٧٣).

الصفوفُ في Lean والجدولُ المولَّد هما ما تقوله النصوصُ المختومة:

١. **البصمات** باليد للنصوص الأربعة الجديدة في `corpora/kitab/` (الخليل، ابنُ جنّي بنسختين، الجزريّ).
٢. **الصفوف**: كلُّ صفٍّ في `Jadwal.lean` بنصّه المسمّى — مرساتُه تقع فيه مرّةً واحدة بعد التطبيع، وحروفُه:
   * الكلمةُ الجامعة («فحثه شخص سكت»، «أجدت طبقك»…) حروفُها هي حروفُ الصفّ (أ ← ء، ة ← ه)؛ أو
   * أسماءُ الحروف في المرساة، بقاموسٍ مكتوبٍ هنا باليد؛ أو
   * ما تُفهم حروفُه من غير اسمها، مكتوبًا هنا باليد (`IMPLICIT`).
٣. **الجدولُ المولَّد** `formal/a116/huruf.csv` (يطبعه Lean المترجَم، ويطابقه CI بايتًا): 116 خانة؛
   ومخرجُ كلّ حرفٍ ترتيبُ صفّه عند ابن جنّي، وحيزُه ترتيبُه عند الخليل، والهمسُ والشدّةُ والاستعلاءُ
   والذلاقةُ والقلقلةُ من كلمات الجزريّ الجامعة مقروءةً من النصّ المختوم هنا لا من Lean؛ والمرخَّصُ 113
   والمبتدَأُ به 84 والموقوفُ عليه 29.

الطفرات: `MUTANT_ONE_BYTE`، `MUTANT_ANCHOR_INVENTED`، `MUTANT_MNEMONIC_LETTER`،
`MUTANT_NAME_LETTER`، `MUTANT_CSV_BIT_FLIP`، `MUTANT_CSV_MAKHRAJ_SWAP`.
"""

from __future__ import annotations

import csv
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

LEAN = ROOT / "formal" / "a116" / "A116" / "Jadwal.lean"
TABLE = ROOT / "formal" / "a116" / "huruf.csv"
FILES = {
    "khalil": "0170KhalilFarahidi.Cayn.JK000930-ara1",
    "ibnJinniJK": "0392IbnJinniMawsili.SirrSinacatIcrab.JK001326-ara1",
    "ibnJinniSh": "0392IbnJinniMawsili.SirrSinacatIcrab.Shamela0012017-ara1",
    "jazari": "0833IbnJazari.ManzumaJazariyya.Shamela0012093-ara1",
    "kitab": "0180Sibawayhi.KitabSibawayhi.JK006989-ara1",
}
HAND_SHA = {  # من الحساب على نسخ OpenITI في الجلسة (2026-10-16)
    "khalil": "e809c626239dee34bddd688b4382a8e314a559a0c700831b8b747fb01ed7d8a1",
    "ibnJinniJK": "586aa011bf4786e5d39d9027bac19cad22523825bd88fcd4715696d603fb189d",
    "ibnJinniSh": "5590c0d5bf2d352057a8c19387f362d302faa225e8eaeeca89c3f5c87885f11a",
    "jazari": "78a09ca9cba86d5c70ca70c2de70cb93f6b1b956cd8a25fd1055e2327dc4ce3b",
}

NAMES = {
    "الهمزة": "ء", "الألف": "ا", "الهاء": "ه", "العين": "ع", "الحاء": "ح", "الغين": "غ",
    "الخاء": "خ", "القاف": "ق", "الكاف": "ك", "الجيم": "ج", "الشين": "ش", "الياء": "ي",
    "الضاد": "ض", "الضاء": "ض", "اللام": "ل", "الراء": "ر", "النون": "ن", "الطاء": "ط",
    "الدال": "د", "التاء": "ت", "الصاد": "ص", "الزاي": "ز", "الزاء": "ز", "السين": "س",
    "الظاء": "ظ", "الذال": "ذ", "الثاء": "ث", "الفاء": "ف", "الباء": "ب", "الميم": "م",
    "الواو": "و",
}
MNEMONICS = {"ستشحثك خصفة", "فحثه شخص سكت", "أجدت طبقك", "أجد قط بكت", "لم يرو عنا", "لن عمر",
             "خص ضغط قظ", "فر من لب", "قطب جد"}
# صفوفٌ تُفهم حروفُها من غير أسمائها المعرَّفة (أسماءٌ بلا «ال»، أو حروفٌ مفردة، أو إحالة)، باليد.
IMPLICIT = {
    "فأقصى الحروف كلها العين ثم الحاء": "عحه",  # «ثم الهاء» بعدها في الجملة نفسِها
    "فالعين والحاء والخاء والغين حلقية": "عحخغه",  # والهاءُ في «فهذه ثلاثة أحرف في حيز واحد» قبلها
    "مما فويق الضاحك والناب والرباعية والثنية": "ل",
    "فألف الجوف وأختاها": "اوي",
    "ثم لأقصى الحلق همز هاء": "ءه",
    "ثم لوسطه فعين حاء": "عح",
    "أدناه غين خاؤها": "غخ",
    "والقاف ... أقصى اللسان فوق": "ق",
    "ثم الكاف أسفل": "ك",
    "والوسط فجيم الشين يا": "جشي",
    "والرا يدانيه لظهر أدخل": "ر",
    "والطاء والدال وتا منه": "طدت",
    "الصفير مستكن": "صزس",
    "والظاء والذال وثا للعليا": "ظذث",
    "فالفا مع اطراف الثنايا المشرفه": "ف",
    "للشفتين الواو باء ميم": "وبم",
    "ومن الخياشيم مخرج النون الخفية": "",
    "وغنة مخرجها الخيشوم": "",
    "إعلم أن الحروف الذلق والشفوية ستة وهي ر ل ن ف ب م": "رلنفبم",
    "وصاد ضاد طاء ظاء مطبقه": "صضطظ",
    "لأنهن حروف الصفير وهن أندى في السمع": "صسز",
    "صفيرها صاد وزاي سين": "صزس",
    "واو وياء سكنا وانفتحا ... قبلهما": "وي",
    "فويقهما وهو اللام": "ل",
    "والانحراف صححا في اللام والرا": "لر",
    "وبتكرير جعل": "ر",
    "ومنها المكرر وهو الراء": "ر",
    "وللتفشي الشين": "ش",
    "ضادا استطل": "ض",
    "لانحرافه إلى اللام، مخرج الراء": "ر",  # اللامُ هنا جهةُ الانحراف لا حرفُ الصفّ
    "لأن الضاد استطالت لرخاوتها حتى اتصلت بمخرج اللام": "ض",
}


def _norm(text: str) -> str:
    text = re.sub(r"PageV\d+P\d+|ms\d+|~~|\||#|[0-9]", " ", text)
    return re.sub(r"\s+", " ", text)


def _texts() -> dict[str, str]:
    return {k: _norm(KITAB.text(v)) for k, v in FILES.items()}


def _rows() -> list[tuple[str, str, str]]:
    """(المصدر، المرساة، الحروف) لكلّ صفٍّ حرفيٍّ في Jadwal.lean."""
    src = LEAN.read_text(encoding="utf-8")
    out = []
    for m in re.finditer(r'⟨(?:\.\w+, )?\.(\w+), "([^"]+)",\s*\[([^\]]*)\]⟩', src):
        out.append((m.group(1), m.group(2), "".join(re.findall(r"'(.)'", m.group(3)))))
    return out


def _named(anchor: str) -> list[str]:
    out = []
    for tok in re.sub(r"[،,]", " ", anchor).split():
        tok = tok[1:] if tok.startswith(("و", "ف")) and tok[1:] in NAMES else tok
        if tok in NAMES:
            out.append(NAMES[tok])
    return out


def _letters_of(anchor: str) -> str:
    if anchor in IMPLICIT:
        return IMPLICIT[anchor]
    if anchor in MNEMONICS:
        return anchor.replace(" ", "").replace("أ", "ء").replace("ة", "ه")
    return "".join(_named(anchor))


def _check(texts: dict[str, str], rows: list[tuple[str, str, str]]) -> list[str]:
    bad = []
    for src, anchor, letters in rows:
        if texts[src].count(anchor) != 1:
            bad.append(f"ANCHOR_NOT_ONCE {src}: {anchor}")
        if set(_letters_of(anchor)) != set(letters):
            bad.append(f"LETTERS_DIFFER {anchor}: {letters} vs {_letters_of(anchor)}")
    return bad


def _table() -> list[dict[str, str]]:
    with TABLE.open(encoding="utf-8") as f:
        return list(csv.DictReader(f))


def _check_table(texts: dict[str, str], rows: list[dict[str, str]]) -> list[str]:
    bad = []
    if len(rows) != 116 or len({(r["harf"], r["haraka"]) for r in rows}) != 116:
        bad.append("NOT_116_CELLS")
    lean_rows = _rows()
    ibn = [set(lt) for s, a, lt in lean_rows if s == "ibnJinniSh"]
    kh = [set(lt) for s, a, lt in lean_rows if s == "khalil"][:11]
    for r in rows:
        c = r["harf"]
        if c not in ibn[int(r["makhraj16"])]:
            bad.append(f"MAKHRAJ {c}")
        if c not in kh[int(r["khalil11"])]:
            bad.append(f"HAYYIZ {c}")
    jaz = texts["jazari"]
    for col, phrase in [("hams", "فحثه شخص سكت"), ("shidda", "أجد قط بكت"), ("istila", "خص ضغط قظ"),
                        ("idhlaq", "فر من لب"), ("qalqala", "قطب جد")]:
        assert jaz.count(phrase) == 1
        want = set(phrase.replace(" ", "").replace("أ", "ء"))
        got = {r["harf"] for r in rows if r[col] == "1"}
        if got != want:
            bad.append(f"SIFA {col}: {sorted(got ^ want)}")
    counts = tuple(sum(r[col] == "true" for r in rows) for col in ("licensable", "ibtida", "waqf"))
    if counts != (113, 84, 29):
        bad.append(f"COUNTS {counts}")
    return bad


def test_seals_by_hand() -> None:
    for k, sha in HAND_SHA.items():
        assert hashlib.sha256(KITAB.text(FILES[k]).encode("utf-8")).hexdigest() == sha, k
    assert KITAB.breaches() == []


def test_mutant_one_byte() -> None:
    raw = bytearray(KITAB.text(FILES["jazari"]).encode("utf-8"))
    raw[len(raw) // 2] ^= 1
    assert hashlib.sha256(bytes(raw)).hexdigest() != HAND_SHA["jazari"]  # MUTANT_ONE_BYTE


def test_rows_are_the_texts() -> None:
    rows = _rows()
    # أحياز، أسماء، مخارجُ ابن جنّي والجزريّ، ونصوصُ الصفات الحرفيّة
    assert len(rows) == 11 + 9 + 16 + 17 + 28
    assert _check(_texts(), rows) == []


def test_table_is_the_texts() -> None:
    assert _check_table(_texts(), _table()) == []


def test_mutants_rejected() -> None:
    texts = _texts()
    rows = _rows()
    assert _check(texts, [*rows, ("jazari", "مخارج الحروف ستة عشر", "")])  # MUTANT_ANCHOR_INVENTED
    mn = next(i for i, r in enumerate(rows) if r[1] == "فحثه شخص سكت")
    wrong = list(rows)
    wrong[mn] = (rows[mn][0], rows[mn][1], rows[mn][2].replace("ه", "ع"))
    assert _check(texts, wrong)  # MUTANT_MNEMONIC_LETTER
    nm = next(i for i, r in enumerate(rows) if r[1] == "ومن وسط الحلق مخرج العين والحاء")
    wrong = list(rows)
    wrong[nm] = (rows[nm][0], rows[nm][1], "عه")
    assert _check(texts, wrong)  # MUTANT_NAME_LETTER
    table = _table()
    flipped = [dict(r) for r in table]
    flipped[0]["hams"] = "1" if flipped[0]["hams"] == "0" else "0"
    assert _check_table(texts, flipped)  # MUTANT_CSV_BIT_FLIP
    swapped = [dict(r) for r in table]
    swapped[0]["makhraj16"] = "1"
    assert _check_table(texts, swapped)  # MUTANT_CSV_MAKHRAJ_SWAP


if __name__ == "__main__":
    tests = [v for k, v in sorted(globals().items()) if k.startswith("test_")]
    for t in tests:
        t()
    sys.stdout.write(f"test_jadwal: {len(tests)}/{len(tests)}\n")
