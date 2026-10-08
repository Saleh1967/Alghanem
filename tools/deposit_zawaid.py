"""إيداعُ الزوائد من الكتاب لسيبويه: «باب علم حروف الزوائد» (الحروفُ العشرة بمواضعها وأمثلتها) و«باب
النون الثقيلة والخفيفة» وما بعده (شواهدُ القرآن على نون التوكيد) — مولَّدٌ من المختوم
`tests/data/openiti-sibawayh-kitab.txt.gz` (OpenITI `0180Sibawayhi.KitabSibawayhi.JK006989`،
CC BY-NC-SA 4.0؛ مطابقٌ بايتًا بايتًا لنسخة hamil `corpora/sources/sibawayh_kitab_jk.txt`).

القواعدُ معلَنةٌ هنا ولا تخمينَ وراءها:
- البابُ يُقتطع بين عنوانه والعنوان التالي (`# | (`)؛ ويُقسَّم فقراتٍ بالفاصل ` | `.
- الفقرةُ التي تبدأ بـ«فالهمزة» أو «وأما الـX» أو «والـX» (X من حروف العشرة) تفتح مدخلَ ذلك الحرف؛
  وما لا يبدأ بحرفٍ يُلحق بالمدخل المفتوح. الهمزةُ لها مدخلان في الباب (أوّلًا، وهمزةُ الوصل) فيُجمعان.
  وما بعد «كما» في الفقرة تشبيهٌ بحرفٍ آخر فلا تُؤخذ أمثلتُه.
- المواضعُ: الأعدادُ الترتيبيّة كما وردت (أولا/ثانية/ثالثة/رابعة/خامسة/سادسة) → 1..6.
- الأمثلةُ: الكلماتُ بعد «نحو» أو «في» حتى «ونحو…» أو فاصلٍ أو كلمةٍ من ألفاظ الهيكل؛ تُحفظ رسمًا
  كما هي (النصُّ غيرُ مشكول) وتُربط بالحوامل بقاعدةٍ معلَنة (أإآ→ء+ا…، ة→ت، ى→ا)، فالربطُ «مطابَقٌ
  بالرسم» لا ترخيص.
- شواهدُ القرآن: ما بين `@QB@` و`@QE@` أو `^ ( … ) ^` في أبواب النون (14157–14370) كلماتٍ رسمًا.

يكتب `formal/Slge/ZawaidTable.lean` و`src/slge/zawaid_table.py`؛ وبـ`--check` يقارنهما بما يولَّد
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
LEAN = ROOT / "formal" / "Slge" / "ZawaidTable.lean"
PY = ROOT / "src" / "slge" / "zawaid_table.py"
SHA = "a160f940bb194e6fe7e6655d2c7f28e41f1fc648c4c5e340cc4e42306d5cb625"

ZAWAID_HEAD = "# | ( هذا باب علم حروف الزوائد )"
NUN_HEAD = "# | ( هذا باب النون الثقيلة والخفيفة )"
NUN_END = "# | ( هذا باب مضاعف الفعل واختلاف العرب فيه )"
LETTERS: dict[str, str] = {"الهمزة": "ء", "الألف": "ا", "الهاء": "ه", "الياء": "ي", "النون": "ن",
                           "التاء": "ت", "السين": "س", "الميم": "م", "الواو": "و", "اللام": "ل"}
ORDINALS: dict[str, int] = {"أولا": 1, "أول": 1, "ثانية": 2, "ثالثة": 3, "رابعة": 4, "خامسة": 5,
                            "سادسة": 6}
STOP = frozenset({"الاسم", "الفعل", "اسم", "فعل", "كل", "إذا", "كما", "فصاعدا", "وذلك", "ذلك",
                  "هذه",
                  "تلحق", "وتلحق", "تزاد", "وتكون", "تكون", "أنت", "هي", "قبل", "بعد", "لتبين",
                  "بها", "الحركة", "وقد", "بينا", "وسنبين", "إن", "شاء", "الله", "وستراه", "مبينا",
                  "كتاب", "ونحوهما", "ونحوه", "ونحوها", "ونحوهن", "ونحو", "نحو", "في", "مواضع",
                  "الألف", "التاء", "النون", "الياء", "الهمزة", "من", "سكن", "أول", "الحرف", "التي",
                  "تسمى", "ألف", "الوصل", "وهي", "بالتاء", "جمعت", "ثنيت", "أضيف", "مضاعفة",
                  "تدخله", "الخفيفة", "والثقيلة", "النساء", "تثنية", "الأسماء", "وجمعها",
                  "تؤنث", "الجماعة", "الواحدة", "الندبة", "النداء", "المد", "يا", "ويا", "وفيما",
                  "يتصرف", "الذي", "وفي", "وإن", "أغفلنا",
                  "موضعا", "للزوائد", "فستبين", "وأما", "فتزاد", "فتؤنث", "أولا", "ثانية", "ثالثة",
                  "رابعة", "خامسة", "سادسة", "و"})
RASM: dict[str, str] = {"أ": "ء", "إ": "ء", "ؤ": "ء", "ئ": "ء", "آ": "ءا", "ة": "ت", "ى": "ا"}


def _read() -> tuple[str, list[str]]:
    raw = gzip.decompress(SRC.read_bytes())
    sha = hashlib.sha256(raw).hexdigest()
    if sha != SHA:
        raise SystemExit(f"SOURCE_SHA_MISMATCH {sha}")
    return sha, raw.decode("utf-8").split("\n")


def _chapter(lines: list[str], head: str, end: str | None = None) -> str:
    i = lines.index(head)
    j = i + 1
    while j < len(lines) and not lines[j].startswith("# | (") if end is None else lines[j] != end:
        j += 1
    body = " ".join(ln[2:] if ln.startswith("~~") else ln.lstrip("# ") for ln in lines[i + 1:j])
    return re.sub(r"\s+", " ", re.sub(r"PageV\d+P\d+|ms\d+", " ", body)).strip()


def rasm(word: str) -> str | None:
    """رسمُ الكلمة حواملَ: ما ليس في الأبجديّة بعد التحويل المعلَن يُرفض (لا يُخمَّن)."""

    w = "".join(RASM.get(ch, ch) for ch in word)
    return w if w and all(ch in ALPHABET for ch in w) else None


def _examples(seg: str) -> list[str]:
    out: list[str] = []
    toks = seg.split()
    i = 0
    while i < len(toks):
        if toks[i] in ("نحو", "في"):
            i += 1
            while i < len(toks):
                t = toks[i]
                if t.startswith("ونحو") or t in STOP or t in ORDINALS:
                    break
                t = t[1:] if t.startswith("و") and len(t) > 3 else t
                if t not in STOP and rasm(t) and t not in out:
                    out.append(t)
                i += 1
        else:
            i += 1
    return out


def entries(lines: list[str]) -> list[dict[str, Any]]:
    text = _chapter(lines, ZAWAID_HEAD).removeprefix("وهي عشرة أحرف ")
    opener = re.compile(r"^(?:ف|و)?(?:أما )?(%s)\b" % "|".join(LETTERS))  # noqa: UP031
    out: dict[str, dict[str, Any]] = {}
    current: str | None = None
    for seg in [s.strip() for s in text.split(" | ") if s.strip()]:
        m = opener.match(seg)
        if m:
            current = m.group(1)
        elif seg.startswith("وتلحق الهمزة"):
            current = "الهمزة"
        if current is None:
            continue
        e = out.setdefault(current, {"name": current, "letter": LETTERS[current], "positions": [],
                                     "examples": [], "domains": [], "raw": []})
        e["raw"].append(seg)
        for tok in seg.split():
            o = ORDINALS.get(tok.removeprefix("و"))
            if o is not None and o not in e["positions"]:
                e["positions"].append(o)
        for ex in _examples(seg.split(" كما ")[0]):  # ما بعد «كما» تشبيهٌ بحرفٍ آخر لا مثالٌ لهذا
            if ex not in e["examples"]:
                e["examples"].append(ex)
        for d in ("الاسم", "الفعل"):
            if d in seg and d not in e["domains"]:
                e["domains"].append(d)
    order = [n for n in LETTERS if n in out]
    return [out[n] for n in order]


def witnesses(lines: list[str]) -> list[dict[str, Any]]:
    """كلماتُ شواهد القرآن في أبواب النون: رسمًا، مع البابِ الذي وردت فيه."""

    i, j = lines.index(NUN_HEAD), lines.index(NUN_END)
    out: list[dict[str, Any]] = []
    chapter: str = ""
    body: list[str] = []
    def flush() -> None:
        text = re.sub(r"\s+", " ", re.sub(r"PageV\d+P\d+|ms\d+", " ", " ".join(body)))
        for q in re.findall(r"@QB@(.*?)@QE@|\^ \((.*?)\) \^", text):
            out.append({"chapter": chapter, "words": (q[0] or q[1]).split()})
    for ln in lines[i:j]:
        if ln.startswith("# | ("):
            flush()
            chapter, body = ln[len("# | ( "):].rstrip(" )"), []
            continue
        body.append(ln[2:] if ln.startswith("~~") else ln.lstrip("# "))
    flush()
    return out


def render_lean(sha: str, es: list[dict[str, Any]], ws: list[dict[str, Any]]) -> str:
    idx = {ch: i for i, ch in enumerate(ALPHABET)}
    lines = [
        "import Slge.Bridge", "",
        "/-! حروفُ الزوائد العشرة عند سيبويه («باب علم حروف الزوائد») بمواضعها، وشواهدُ القرآن في",
        "أبواب النون الثقيلة والخفيفة — مولَّدٌ من المختوم `tests/data/openiti-sibawayh-kitab.txt.gz`",
        f"(SHA-256 `{sha}`) بـ`tools/deposit_zawaid.py`؛ لا يُحرَّر باليد.",
        "الحرفُ بفهرسه في الأبجديّة، والمواضعُ كما وردت (1..6)،",
        "والأمثلةُ حواملَ بالرسم (النصُّ غيرُ مشكول). -/", "",
        "namespace Slge.Zawaid", "",
        "/-- (الحامل، مواضعُه، أمثلتُه حواملَ) بترتيب الباب. -/",
        "def table : List (Nat × List Nat × List (List Nat)) := [",
    ]
    rows = []
    for e in es:
        exs = ", ".join("[" + ", ".join(str(idx[c]) for c in rasm(x) or "") + "]"
                        for x in e["examples"])
        pos = ", ".join(str(p) for p in e["positions"])
        rows.append(f"  ({idx[e['letter']]}, [{pos}], [{exs}])")
    lines += [",\n".join(rows), "]", "",
              f"theorem table_length : table.length = {len(es)} := by rfl", "",
              "/-- كلماتُ شواهد القرآن في أبواب النون، حواملَ بالرسم. -/",
              "def witnesses : List (List Nat) := ["]
    wrows = []
    for w in ws:
        for word in w["words"]:
            r = rasm(word)
            if r:
                wrows.append("  [" + ", ".join(str(idx[c]) for c in r) + "]")
    lines += [",\n".join(wrows), "]", "", "end Slge.Zawaid", ""]
    return "\n".join(lines)


def render_py(sha: str, es: list[dict[str, Any]], ws: list[dict[str, Any]]) -> str:
    lines = [
        '"""حروفُ الزوائد العشرة عند سيبويه بمواضعها وأمثلتها، وشواهدُ القرآن في أبواب النون —',
        f'مولَّدٌ من المختوم `tests/data/openiti-sibawayh-kitab.txt.gz` (SHA-256 {sha[:16]}…)',
        'بـ`tools/deposit_zawaid.py`؛ لا يُحرَّر باليد."""', "", "from __future__ import annotations",
        "", "from typing import Final", "",
        "TABLE: Final[tuple[tuple[str, str, tuple[int, ...], tuple[str, ...], tuple[str, ...]],",
        "                   ...]] = (",
    ]
    for e in es:
        pos = ", ".join(str(p) for p in e["positions"])
        exs = ", ".join(f'"{x}"' for x in e["examples"])
        dom = ", ".join(f'"{d}"' for d in e["domains"])
        c1 = "," if len(e["positions"]) == 1 else ""
        c2 = "," if len(e["examples"]) == 1 else ""
        c3 = "," if len(e["domains"]) == 1 else ""
        lines.append(f'    ("{e["name"]}", "{e["letter"]}", ({pos}{c1}),')
        lines.append(f'     ({exs}{c2}), ({dom}{c3})),')
    lines += [")", "", "WITNESSES: Final[tuple[tuple[str, tuple[str, ...]], ...]] = ("]
    for w in ws:
        words = ", ".join(f'"{x}"' for x in w["words"])
        lines.append(f'    ("{w["chapter"]}",')
        lines.append(f'     ({words}{"," if len(w["words"]) == 1 else ""})),')
    lines += [")", ""]
    return "\n".join(lines)


def main(argv: list[str]) -> int:
    sha, lines = _read()
    es, ws = entries(lines), witnesses(lines)
    lean, py = render_lean(sha, es, ws), render_py(sha, es, ws)
    if "--check" in argv:
        ok = LEAN.read_text(encoding="utf-8") == lean and PY.read_text(encoding="utf-8") == py
        sys.stdout.write("جدولا الزوائد مطابقان للمختوم\n" if ok else "جدولا الزوائد غيرُ مطابقين\n")
        return 0 if ok else 1
    LEAN.write_text(lean, encoding="utf-8")
    PY.write_text(py, encoding="utf-8")
    for e in es:
        sys.stdout.write(f"{e['name']} ({e['letter']}): مواضع {e['positions']} "
                         f"أمثلة {e['examples']} {e['domains']}\n")
    n = sum(len(w["words"]) for w in ws)
    sys.stdout.write(f"شواهدُ النون: {n} كلمةً في {len(ws)} اقتباسًا\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
