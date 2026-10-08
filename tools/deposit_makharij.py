"""إيداعُ المخارج والصفات من الكتاب لسيبويه: «هذا باب الإدغام — باب عدد الحروف العربية ومخارجها
ومهموسها ومجهورها» — مولَّدٌ من المختوم `tests/data/openiti-sibawayh-kitab.txt.gz` (JK006989،
CC BY-NC-SA 4.0).

القواعدُ معلَنةٌ ولا تخمينَ وراءها (كلُّ قاعدةٍ مرساتُها عبارةٌ من النصّ بعينها):
- **الأصول**: «فأصل حروف العربية تسعة وعشرون حرفا» ثمّ أسماؤها بترتيبها حتى «وتكون خمسة وثلاثين».
- **الفروع**: الستّةُ المستحسنة بين «وهي النون الخفيفة» و«|»، والثمانيةُ غيرُ المستحسنة بين «وهي الكاف
  التي» و«|»؛ الفرعُ يبدأ باسم حرفٍ يليه «التي/الخفيفة/الضعيفة/التفخيم».
- **المخارج**: من «ولحروف العربية ستة عشر مخرجا» إلى «فأما المجهورة»؛ كلُّ «مخرج»/«مخرجا» يفتح مخرجًا:
  وصفُه ما قبله في فقرته، وحروفُه الأسماءُ المتتالية بعده (بعد «من الفم» إن وردت)؛ «ومن مخرج النون»
  في وصف الراء إحالةٌ لا مخرج؛ «النون الخفيفة» في الخياشيم تُسجَّل نونًا بوسم الخفيفة. العددُ المنطوق
  (ستة عشر) = المعدودُ + الساقطُ باسمه (اللام في هذه النشرة).
- **الصفات**: كلُّ صفةٍ بمرساتها: «فأما المجهورة ف…فذلك تسعة عشر حرفا»، «وأما المهموسة ف…فذلك عشرة
  أحرف»،
  «ومن الحروف الشديد… وهو …وذلك»، «ومنها الرخوة وهي …وذلك»، «وأما العين فبين الرخوة والشديدة»،
  «ومنها المنحرف… وهو اللام»، «غنة… وهو النون وكذلك الميم»، «ومنها المكرر… وهو الراء»، «ومنها اللينة
  وهي الواو والياء»، «ومنها الهاوي… وهي الألف»، «فأما المطبقة فالصاد والضاد والطاء والظاء»؛
  والمنفتحة
  «كل ما سوى ذلك» تُحسب. الأعدادُ المنطوقة (تسعة عشر، عشرة) تُطابَق بالمستخرَج.
- أسماءُ الحروف تُربط بالحوامل بجدولٍ معلَن (الهمزة→ء … الألف→ا)؛ ما ليس اسمَ حرفٍ في موضع اسمٍ خطأٌ
  مسمًّى لا يُتجاوز.

يكتب `formal/Slge/MakharijTable.lean` و`src/slge/makharij_table.py`؛ وبـ`--check` يقارنهما بما يولَّد
الآن.
"""

from __future__ import annotations

import gzip
import hashlib
import re
import sys
from pathlib import Path
from typing import Any

from slge.cells import ALPHABET

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "tests" / "data" / "openiti-sibawayh-kitab.txt.gz"
LEAN = ROOT / "formal" / "Slge" / "MakharijTable.lean"
PY = ROOT / "src" / "slge" / "makharij_table.py"
SHA = "a160f940bb194e6fe7e6655d2c7f28e41f1fc648c4c5e340cc4e42306d5cb625"
HEAD = "# | ( هذا باب الإدغام )"
NAMES: dict[str, str] = {
    "الهمزة": "ء", "الألف": "ا", "الهاء": "ه", "العين": "ع", "الحاء": "ح", "الغين": "غ",
    "الخاء": "خ", "الكاف": "ك", "القاف": "ق", "الضاد": "ض", "الجيم": "ج", "الشين": "ش",
    "الياء": "ي", "اللام": "ل", "الراء": "ر", "النون": "ن", "الطاء": "ط", "الدال": "د",
    "التاء": "ت", "الصاد": "ص", "الزاي": "ز", "السين": "س", "الظاء": "ظ", "الذال": "ذ",
    "الثاء": "ث", "الفاء": "ف", "الباء": "ب", "الميم": "م", "الواو": "و",
}
NUMBERS: dict[str, int] = {"تسعة وعشرون": 29, "ستة عشر": 16, "تسعة عشر": 19, "عشرة": 10}
SIFAT: tuple[tuple[str, str, str], ...] = (
    ("majhura", "المجهورة", r"فأما المجهورة ف(.+?) فذلك (\S+(?: \S+)?) حرفا"),
    ("mahmusa", "المهموسة", r"وأما المهموسة ف(.+?) فذلك (\S+) أحرف"),
    ("shadida", "الشديدة", r"ومن الحروف الشديد وهو الذي .+? وهو (.+?) وذلك"),
    ("rikhwa", "الرخوة", r"ومنها الرخوة وهي (.+?) وذلك"),
    ("baynBayn", "بين الرخوة والشديدة", r"وأما (\S+) فبين الرخوة والشديدة"),
    ("munharif", "المنحرف", r"ومنها المنحرف .+? وهو (\S+) وإن"),
    ("ghunna", "الغنّة", r"غنة من الأنف .+? وهو (\S+ وكذلك \S+) \|"),
    ("mukarrar", "المكرّر", r"ومنها المكرر .+? وهو (\S+) \|"),
    ("layyina", "اللينة", r"ومنها اللينة وهي (.+?) لأن"),
    ("hawi", "الهاوي", r"ومنها الهاوي .+? وهي (\S+) \|"),
    ("mutbaqa", "المطبقة", r"فأما المطبقة ف(.+?) \|"),
)


def _read() -> tuple[str, str]:
    raw = gzip.decompress(SRC.read_bytes())
    sha = hashlib.sha256(raw).hexdigest()
    if sha != SHA:
        raise SystemExit(f"SOURCE_SHA_MISMATCH {sha}")
    lines = raw.decode("utf-8").split("\n")
    i = lines.index(HEAD)
    j = i + 1
    while not lines[j].startswith("# | ("):
        j += 1
    body = " ".join(ln[2:] if ln.startswith("~~") else ln.lstrip("# ") for ln in lines[i + 1:j])
    return sha, re.sub(r"\s+", " ", re.sub(r"PageV\d+P\d+|ms\d+", " ", body)).strip()


def names_in(span: str, where: str) -> list[str]:
    """الأسماءُ المتتالية في المقطع حروفًا؛ كلمةٌ ليست اسمَ حرفٍ (غير «وكذلك») خطأٌ مسمًّى."""

    out: list[str] = []
    for tok in span.split():
        if tok == "وكذلك":
            continue
        t = tok[1:] if tok[0] in "وف" and tok[1:] in NAMES else tok
        if t not in NAMES:
            raise SystemExit(f"NOT_A_LETTER_NAME:{where}:{tok}")
        out.append(NAMES[t])
    return out


def usul(text: str) -> list[str]:
    m = re.search(r"فأصل حروف العربية (\S+ \S+) حرفا (.+?) وتكون خمسة", text)
    assert m, "USUL_ANCHOR"
    letters = names_in(m.group(2), "الأصول")
    assert len(letters) == NUMBERS[m.group(1)], (len(letters), m.group(1))
    return letters


def furu(text: str) -> tuple[list[str], list[str]]:
    a = re.search(r"وهي (النون الخفيفة .+?) \|", text)
    b = re.search(r"وهي (الكاف التي .+?) \|", text)
    assert a and b, "FURU_ANCHOR"
    # الفرعُ يبدأ باسم حرفٍ (أو «ألف») يليه «التي/الخفيفة/الضعيفة/التفخيم»
    rx = r" و(?=(?:ال\S+|ألف) (?:التي|الخفيفة|الضعيفة|التفخيم))"

    def split(span: str) -> list[str]:
        return [x.strip() for x in re.split(rx, " " + span) if x.strip()]

    return split(a.group(1)), split(b.group(1))


def makharij(text: str) -> tuple[list[dict[str, Any]], int, list[str]]:
    m = re.search(r"ولحروف العربية (\S+ \S+) مخرجا (.+?) \| فأما المجهورة", text)
    assert m, "MAKHARIJ_ANCHOR"
    out: list[dict[str, Any]] = []
    for seg in m.group(2).split(" | "):
        # «ومن مخرج النون غير أنه…» إحالةٌ في وصف الراء لا مخرجٌ جديد
        pieces = re.split(r"(?<!ومن )\bمخرجا?\b", seg)
        desc = pieces[0].strip()
        for piece in pieces[1:]:
            toks = piece.split()
            letters: list[str] = []
            light = False
            k = 0
            while k < len(toks):
                tok = toks[k]
                t = tok[1:] if tok[0] in "وف" and tok[1:] in NAMES else tok
                if not letters and tok in ("من", "الفم"):  # «مخرجا من الفم الغين والخاء»
                    k += 1
                    continue
                if t in NAMES:
                    letters.append(NAMES[t])
                    k += 1
                elif t == "الخفيفة" and letters and letters[-1] == "ن":
                    light = True
                    k += 1
                else:
                    break
            out.append({"desc": desc, "letters": letters, "light": light})
            desc = " ".join(toks[k:]).strip()
    stated = NUMBERS[m.group(1)]
    covered = {c for mk in out for c in mk["letters"]}
    missing = [c for c in NAMES.values() if c not in covered]
    # النصُّ يقول «ستة عشر» والمعدودُ في هذه النشرة خمسةَ عشر: مخرجُ اللام ساقطٌ من التعداد (في نشرتي
    # jk وShamela معًا) وإن ذُكر «مخرج اللام» في الباب لاحقًا. يُسجَّل نقصًا باسمه ولا يُرمَّم.
    assert stated == len(out) + len(missing), (stated, len(out), missing)
    return out, stated, missing


def sifat(text: str) -> dict[str, dict[str, Any]]:
    out: dict[str, dict[str, Any]] = {}
    for key, name, rx in SIFAT:
        m = re.search(rx, text)
        assert m, f"SIFA_ANCHOR:{name}"
        letters = names_in(m.group(1), name)
        if m.lastindex and m.lastindex >= 2:
            assert len(letters) == NUMBERS[m.group(2)], (name, len(letters), m.group(2))
        out[key] = {"name": name, "letters": letters}
    mutbaqa = out["mutbaqa"]["letters"]
    rest = [c for c in NAMES.values() if c not in mutbaqa]
    out["munfatiha"] = {"name": "المنفتحة", "letters": rest}
    return out


def extract() -> tuple[str, dict[str, Any]]:
    sha, text = _read()
    good, bad = furu(text)
    mk, stated, missing = makharij(text)
    return sha, {"order": usul(text), "furu_good": good, "furu_bad": bad, "makharij": mk,
                 "stated": stated, "missing": missing, "sifat": sifat(text)}


def render_lean(sha: str, d: dict[str, Any]) -> str:
    idx = {ch: i for i, ch in enumerate(ALPHABET)}

    def ls(cs: list[str]) -> str:
        return "[" + ", ".join(str(idx[c]) for c in cs) + "]"

    lines = [
        "import Slge.Bridge", "",
        "/-! المخارجُ والصفات من «باب عدد الحروف العربية ومخارجها ومهموسها ومجهورها» في الكتاب",
        "لسيبويه —",
        f"مولَّدٌ من المختوم `tests/data/openiti-sibawayh-kitab.txt.gz` (SHA-256 `{sha}`)",
        "بـ`tools/deposit_makharij.py`؛ لا يُحرَّر باليد. الحرفُ بفهرسه في أبجديّة SLGE. -/", "",
        "namespace Slge.Makharij", "",
        "/-- الأصولُ التسعةُ والعشرون بترتيب سيبويه (الهمزةُ فالألفُ فالهاء … فالواو). -/",
        f"def order : List Nat := {ls(d['order'])}", "",
        "theorem order_length : order.length = 29 := by rfl", "",
        "/-- المخارجُ بترتيب الباب: حروفُ كلّ مخرج (النونُ الخفيفة في الخياشيم نونًا). النصُّ يقول",
        f"«ستة عشر» والمعدودُ في النشرة {len(d['makharij'])}: مخرجُ اللام ساقطٌ من التعداد",
        "(نقصٌ مسمًّى). -/",
        "def makharij : List (List Nat) := [",
        ",\n".join(f"  {ls(m['letters'])}" for m in d["makharij"]), "]", "",
        f"/-- العددُ المنطوق في النصّ. -/\ndef statedCount : Nat := {d['stated']}", "",
        f"/-- ما لم يرد له مخرجٌ في التعداد. -/\ndef missing : List Nat := {ls(d['missing'])}", "",
    ]
    for key, v in d["sifat"].items():
        lines += [f"/-- {v['name']} -/", f"def {key} : List Nat := {ls(v['letters'])}", ""]
    lines += ["end Slge.Makharij", ""]
    return "\n".join(lines)


def render_py(sha: str, d: dict[str, Any]) -> str:
    def q(cs: list[str], indent: int = 4) -> list[str]:
        """أسطرٌ مطويّةٌ لصفٍّ من السلاسل داخل قوسين."""

        rows, line = [], " " * indent
        for c in cs:
            item = f'"{c}", '
            if len(line) + len(item) > 96:
                rows.append(line.rstrip())
                line = " " * indent
            line += item
        rows.append(line.rstrip())
        return rows

    lines = [
        '"""المخارجُ والصفات من «باب عدد الحروف العربية ومخارجها» في الكتاب لسيبويه — مولَّدٌ من',
        f'المختوم `tests/data/openiti-sibawayh-kitab.txt.gz` (SHA-256 {sha[:16]}…)',
        'بـ`tools/deposit_makharij.py`؛ لا يُحرَّر باليد."""', "",
        "from __future__ import annotations", "", "from typing import Final", "",
        "ORDER: Final[tuple[str, ...]] = (", *q(d["order"]), ")", "",
        "MAKHARIJ: Final[tuple[tuple[str, tuple[str, ...], bool], ...]] = (",
    ]
    for m in d["makharij"]:
        desc = m["desc"].replace('"', '\\"')
        if len(desc) > 90:  # وصفٌ طويل: سلسلةٌ متجاورة على سطرين
            cut = desc.rfind(" ", 0, 85)
            lines.append(f'    ("{desc[:cut]} "')
            lines.append(f'     "{desc[cut + 1:]}",')
        else:
            lines.append(f'    ("{desc}",')
        cells = ", ".join(f'"{c}"' for c in m["letters"])
        lines.append(f'     ({cells},), {m["light"]}),')
    lines += [")", "", f"STATED_COUNT: Final[int] = {d['stated']}",
              "MISSING: Final[tuple[str, ...]] = (", *q(d["missing"]), ")", "",
              "SIFAT: Final[dict[str, tuple[str, tuple[str, ...]]]] = {"]
    for key, v in d["sifat"].items():
        lines += [f'    "{key}": ("{v["name"]}", (', *q(v["letters"], 8), "    )),"]
    lines += ["}", "", "FURU_GOOD: Final[tuple[str, ...]] = (", *q(d["furu_good"]), ")", "",
              "FURU_BAD: Final[tuple[str, ...]] = (", *q(d["furu_bad"]), ")", ""]
    return "\n".join(lines)


def main(argv: list[str]) -> int:
    sha, d = extract()
    lean, py = render_lean(sha, d), render_py(sha, d)
    if "--check" in argv:
        ok = LEAN.read_text(encoding="utf-8") == lean and PY.read_text(encoding="utf-8") == py
        sys.stdout.write("جدولا المخارج مطابقان للمختوم\n" if ok else "جدولا المخارج غيرُ مطابقين\n")
        return 0 if ok else 1
    LEAN.write_text(lean, encoding="utf-8")
    PY.write_text(py, encoding="utf-8")
    sys.stdout.write(f"الأصول {''.join(d['order'])}\n")
    for m in d["makharij"]:
        light = " (خفيفة)" if m["light"] else ""
        sys.stdout.write(f"  {''.join(m['letters'])}{light}: {m['desc']}\n")
    sys.stdout.write(f"المنطوق {d['stated']}، المعدود {len(d['makharij'])}، "
                     f"الساقط {d['missing']}\n")
    for v in d["sifat"].values():
        sys.stdout.write(f"  {v['name']}: {''.join(v['letters'])}\n")
    sys.stdout.write(f"الفروع: {d['furu_good']}\n          {d['furu_bad']}\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
