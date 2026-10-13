"""إيداعُ بوّابات المعنى (ADR ٥٥): كلُّ بوّابةٍ بعباراتها بعينها وسطرِها في الشخصيّة الإسلاميّة ج3 المختومة
(`nabhani-shakhsiyya-3.txt.gz`) — مبحثُ المفرد والفعل والحرف (الزمنُ والنفيُ والعطف)، ومبحثُ العموم
والخصوص
(صيغُ العموم والتخصيصُ المتّصل)، ومفهومُ الشرط.

القاعدةُ معلَنة على نسق `tools/deposit_mayaatir.py`: `GATES` = (المفتاح، الاسم، العبارات). الأداةُ تثبت
أنّ
العباراتِ كلَّها في **سطرٍ واحد** من الكتاب وتكتب السطر؛ وما لم يوجد خطأٌ مسمًّى لا يُتجاوز. والمعنى الذي
تُعطيه `formal/Slge/Bawwabat.lean` لكلّ مفتاحٍ هو قراءةُ هذه العبارات لا غيرُها؛ فإن تغيّر المختوم سقط
البناء.

يكتب `formal/Slge/BawwabatTable.lean` و`src/slge/bawwabat_table.py`؛ وبـ`--check` يقارنهما بما يولَّد
الآن.
"""

from __future__ import annotations

import gzip
import hashlib
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "tests" / "data"
LEAN = ROOT / "formal" / "Slge" / "BawwabatTable.lean"
PY = ROOT / "src" / "slge" / "bawwabat_table.py"

BOOK = ("nabhani-shakhsiyya-3.txt.gz",
        "359bb5532ecee8156f266522bb5388a1711e46e136004c3ac22e43f2ce656cb4")

GATES: tuple[tuple[str, str, tuple[str, ...]], ...] = (
    # ١. الزمنُ بالهيئة وبالأداة
    ("Z_HAYAA", "الفعلُ يدلّ بهيئته على أحد الأزمنة",
     ("فإن دل بهيئته، أي بحالته التصريفية، على أحد الأزمنة الثلاثة",)),
    ("Z_FIL", "الزمانُ المحصَّل والمضارعُ والتخليصُ والأمر",
     ("والزمان المحصل هو الماضي، والحال، والمستقبل",
      "والحاضر والمستقبل في اللفظ واحد ويسمى المضارع",
      "وتخليص المستقبل عن الحاضر بدخول السين أو سوف عليه",
      "فما نـزع منه حرف المضارعة لا غير")),
    ("N_MA", "«ما» لنفي الحال أو الماضي القريب",
     ("«ما» لنفي الحـال، أو الماضي القريب من الحال", "ما تفعل، ما فعل")),
    ("N_LA", "«لا» لنفي المستقبل", ("لنفي المستقبل، إما خبراً كقولك",)),
    ("N_LAM", "«لم» و«لمّا» لقلب المضارع ماضيًا",
     ("«لم» و«لما» لقلب المضارع إلى الماضي", "لم يفعل، ولما يفعل")),
    ("N_LAN", "«لن» لتأكيد المستقبل", ("«لن» لتأكيد المستقبل",)),
    ("N_IN", "«إن» لنفي الحال", ("«إن» لنفي الحال", "إِنْ كَانَتْ")),
    ("T_QAD", "«قد» لتقريب الماضي من الحال", ("وحرف تقريب الماضي من الحال وهو «قد»", "قد قام زيد")),
    ("T_ISTIQBAL", "حروفُ الاستقبال",
     ("وحروف الاستقبال وهي: «السين» و«سوف» و«أن» و«لا» و«إن»",)),
    # ٢. العطف
    ("A_WAW", "الواو لمطلق الجمع", ("لمطـلق الجـمـع لا تفيد ترتيباً ولا معية",)),
    ("A_FA", "الفاء للترتيب والتعقيب", ("«الفاء»: تفيد الترتيب والتعقيب",)),
    ("A_THUMMA", "ثمّ للترتيب والتراخي", ("«ثم»: تفيد الترتيب والتراخي",)),
    ("A_HATTA", "حتّى للترتيب والجزء", ("تفيد الترتيب، وأن المعطوف جزء من المعطوف عليه",)),
    ("A_AW", "أو لتعليق الحكم بأحد المذكورين",
     ("«أو»: تفيد تعليق الحكم بأحد المذكورين", "وتقع في الخبر، والأمر، والاستفهام")),
    ("A_AM", "أم في الاستفهام وحده",
     ("ولا تقع إلا في الاستفهام، ومع العلم بأحدهما والشك في تعيينه",)),
    ("A_MUKHALAFA", "لا وبل ولكن: المعطوفُ مخالفٌ في حكمه",
     ("تشترك في أن المعطوف مخالف للمعطوف عليه في حكمه",)),
    # ٣. التخصيصُ المتّصل ومفهومُ الشرط
    ("K_MUTTASIL", "التخصيصُ المتّصل أربعة",
     ("والتخصيص المتصل أربعة أنواع هي: الاستثناء، والشرط، والصفة، والغاية",)),
    ("K_ISTITHNA", "الاستثناءُ إخراجٌ متّصل",
     ("التخصيص بالاستثناء هو إخراج ما بعد «إلا» أو إحدى أخواتها مما قبلها",
      "وأدوات الاستثناء هي: «إلا» و«غير» و«سوى» و«خلا» و«حاشا» و«عدا» و«ما عدا» و«ما خلا» و«ليس»"
      " و«لا يكون»",
      "وشرط صحة الاستثناء أن يكون متصلاً بالمستثنى منه")),
    ("K_SHART", "الشرطُ يُخرج ما لولاه لبقي",
     ("فإنها تخرج منه ما لولاها لبقي فيه",
      "وأما صيغ الشرط فكثيرة، وهي: «إن» الخفيفة و«إذا» و«من» و«مهما» و«حيثما» و«أينما» و«إذ ما»")),
    ("K_MAFHUM_SHART", "مفهومُ الشرط: نفيُ الحكم عند عدمه",
     ("فإنه يدل على نفي الحكم عند عدم تحقق الشرط",)),
    ("K_SIFA", "الصفةُ تُخرج ما عداها",
     ("إذا اقترن العام بصفة فإنه يخصصه بها ويخرج منه ما عداها",)),
    ("K_GHAYA", "الغايةُ تُخرج ما بعدها",
     ("وصيغ الغاية لفظان هما: «إلى» و«حتى»",
      "فإذا دخلت أي منهما على الكلام العام أخرجت منه ما بعدها")),
    # ٤. صيغُ العموم
    ("U_SIYAGH", "صيغُ العموم بأنفسها",
     ("فما يكون عاماً في كل شيء من أولي العلم أو غيرهم فإنه كـ«أي»",
      "وكذا «كل»، و«جميع»، و«الذين»، و«اللاتي»",
      "وشرط «أي» أن تكون استفهامية أو شرطية",
      "فهو كـ«من» فإن الصحيح أنها تعم الذكور والإناث",
      "وشرطها أن تكون شرطية أو استفهامية",
      "كـ«ما» نحو: اشتر ما رأيت",
      "وما يكون عاماً في الأمكنة خاصة فهو «أين» و«حيث»",
      "وما يكون عاماً في الزمان المبهم فهي «متى»")),
    ("U_NAFY", "النكرةُ في سياق النفي تعمّ",
     ("وأما القرينة في النفي فهو النكرة في سياق النفي، فإن النكرة في سياق النفي تعم",)),
)
"""الصفّ: (المفتاح، الاسم، العباراتُ بعينها في سطرٍ واحد من ج3)."""


def _read() -> list[str]:
    path, sha = BOOK
    raw = gzip.decompress((DATA / path).read_bytes())
    got = hashlib.sha256(raw).hexdigest()
    if got != sha:
        raise SystemExit(f"SOURCE_SHA_MISMATCH:{path}:{got}")
    return raw.decode("utf-8").split("\n")


def rows(lines: list[str]) -> list[tuple[str, str, int, tuple[str, ...]]]:
    out = []
    for key, name, phrases in GATES:
        hit = [i for i, ln in enumerate(lines) if all(p in ln for p in phrases)]
        if len(hit) != 1:
            raise SystemExit(f"GATE_NOT_ON_ONE_LINE:{key}:{len(hit)}")
        out.append((key, name, hit[0] + 1, phrases))
    return out


def _lean_str(s: str) -> str:
    return '"' + s.replace("\\", "\\\\").replace('"', '\\"') + '"'


def render_lean(rs: list[tuple[str, str, int, tuple[str, ...]]]) -> str:
    lines = [
        "import Slge.Categories", "",
        "/-! بوّاباتُ المعنى بعباراتها وأسطرها من الشخصيّة الإسلاميّة ج3 المختومة (ADR ٥٥)؛",
        "مولَّدٌ بـ`tools/deposit_bawwabat.py`، لا يُحرَّر باليد. بصمةُ المصدر:",
        f"`{BOOK[1]}`.",
        "الصفُّ: (المفتاح، الاسم، السطر، العباراتُ بعينها في ذلك السطر). -/", "",
        "namespace Slge.BawwabatTable", "",
        "def gates : List (String × String × Nat × List String) := [",
    ]
    lines.append(",\n".join(
        f"  ({_lean_str(k)}, {_lean_str(n)}, {ln}, "
        + "[" + ", ".join(_lean_str(p) for p in ph) + "])" for k, n, ln, ph in rs))
    lines += ["]", "",
              f"theorem gates_length : gates.length = {len(rs)} := by rfl", "",
              "/-- مفاتيحُ البوّابات بترتيبها. -/",
              "def keys : List String := gates.map (·.1)", "",
              "end Slge.BawwabatTable", ""]
    return "\n".join(lines)


def _chunks(s: str, width: int = 60) -> list[str]:
    """العبارةُ قطعًا متجاورةً عند المسافات (سطرُ بايثون ≤ 100)؛ وصلُها هو العبارةُ بعينها."""

    out, cur = [], ""
    for w in s.split(" "):
        piece = w if not cur else " " + w
        if cur and len(cur) + len(piece) > width:
            out.append(cur)
            cur = piece
        else:
            cur += piece
    out.append(cur)
    return out


def render_py(rs: list[tuple[str, str, int, tuple[str, ...]]]) -> str:
    lines = [
        '"""بوّاباتُ المعنى بعباراتها وأسطرها من الشخصيّة الإسلاميّة ج3 المختومة (ADR ٥٥)؛ مولَّدٌ',
        'بـ`tools/deposit_bawwabat.py`، لا يُحرَّر باليد."""',
        "", "from __future__ import annotations", "", "from typing import Final", "",
        "Row = tuple[str, str, int, tuple[str, ...]]",
        '"""(المفتاح، الاسم، السطر، العباراتُ بعينها في ذلك السطر)."""', "",
        "GATES: Final[tuple[Row, ...]] = (",
    ]
    for k, n, ln, ph in rs:
        lines.append(f"    ({k!r}, {n!r}, {ln},")
        lines.append("     (")
        for p in ph:
            chunks = _chunks(p)
            lines += [f"         {c!r}" for c in chunks[:-1]] + [f"         {chunks[-1]!r},"]
        lines.append("     )),")
    lines += [")", "",
              "KEYS: Final[tuple[str, ...]] = tuple(r[0] for r in GATES)", ""]
    return "\n".join(lines)


def main(argv: list[str]) -> int:
    rs = rows(_read())
    lean, py = render_lean(rs), render_py(rs)
    if "--check" in argv:
        ok = LEAN.read_text(encoding="utf-8") == lean and PY.read_text(encoding="utf-8") == py
        sys.stdout.write("جدولا البوّابات مطابقان للمختوم\n" if ok
                         else "جدولا البوّابات غيرُ مطابقين\n")
        return 0 if ok else 1
    LEAN.write_text(lean, encoding="utf-8")
    PY.write_text(py, encoding="utf-8")
    for k, _, ln, ph in rs:
        sys.stdout.write(f"{k}\t{ln}\t{len(ph)}\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
