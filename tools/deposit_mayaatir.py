"""إيداعُ معايير الحكم العقليّ (المرحلةُ الأولى من خطّة المالك، ADR ٤٩): كلُّ معيارٍ بعباراته
بعينها وسطرِه في كتاب النبهانيّ المختوم — «التفكير» (`nabhani-tafkir.txt.gz`)، والشخصيّة
الإسلاميّة ج3 (`nabhani-shakhsiyya-3.txt.gz`) وج1 (`nabhani-shakhsiyya-1.txt.gz`، مختومٌ في هذا
الإيداع: الأصلُ `docx` ببصمة `5e327aa2…` = مدخلُ السجلّ f0024 في الغانم، من
hamil-hala-zaman-program@7de0bc2، محوَّلٌ بالطريقة التي أعادت ج3 بايتًا بايتًا: فقراتُ
`document.xml` نصوصُها `w:t` موصولةً بسطرٍ واحد بلا تطبيع).

القاعدةُ معلَنة: `CRITERIA` = (المفتاح، الاسم، الكتاب، العبارات). الأداةُ تثبت أنّ العباراتِ
كلَّها في **سطرٍ واحد** من الكتاب، وتكتب السطر؛ وما لم يوجد خطأٌ مسمًّى لا يُتجاوز. و`ABSENT`
عباراتٌ نُسبت إلى هذه الكتب في الخطّة الواردة (الدعوى بمفتاحها) وليست في أيٍّ منها بلفظها —
تثبت الأداةُ غيابَها، فإن ظهرت سقط البناءُ حتى يُراجَع الصفّ.

يكتب `formal/Slge/MayaatirTable.lean` و`src/slge/mayaatir_table.py`؛ وبـ`--check` يقارنهما بما
يولَّد الآن.
"""

from __future__ import annotations

import gzip
import hashlib
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "tests" / "data"
LEAN = ROOT / "formal" / "Slge" / "MayaatirTable.lean"
PY = ROOT / "src" / "slge" / "mayaatir_table.py"

BOOKS: dict[str, tuple[str, str]] = {
    "tafkir": ("nabhani-tafkir.txt.gz",
               "b9b08eabec468aa0f93b80c01879e3812c57f4bd677e68e448967e3575bfaae4"),
    "shakhsiyya-1": ("nabhani-shakhsiyya-1.txt.gz",
                     "b474d56021427070e2e3852b78bb774383f37bf87e2310d39dcdbaecf33aed63"),
    "shakhsiyya-3": ("nabhani-shakhsiyya-3.txt.gz",
                     "359bb5532ecee8156f266522bb5388a1711e46e136004c3ac22e43f2ce656cb4"),
}

CRITERIA: tuple[tuple[str, str, str, tuple[str, ...]], ...] = (
    ("U1", "تعريف الإدراك", "tafkir",
     ("فالعقل أو الفكر أو الإدراك هو: نقل الحس بالواقع بواسطة الحواس إلى الدماغ، ووجود"
      " معلومات سابقة يفسر بواسطتها هذا الواقع",)),
    ("U2", "المعلومة لا الرأي", "tafkir",
     ("فالمحتم في الطريقة العقلية ليس وجود رأي أو آراء سابقة عن الواقع، بل وجود معلومات"
      " سابقة عنه أو متعلقة به",
      "فإن الرأي السابق إذا استعمل قد يسبب الخطأ في الإدراك")),
    ("U3", "المفهوم والمعلومات", "shakhsiyya-1",
     ("إذا كان لهذا المعنى الذي تضمنه اللفظ واقع يقع عليه الحس أو يتصوره الذهن كشيء محسوس"
      " ويصدقه، كان هذا المعنى مفهوماً",
      "وما عدا ذلك من معاني الألفاظ والجمل لا يسمى مفهوماً، وإنما هو مجرد معلومات")),
    ("U4", "الدور باطل", "shakhsiyya-3",
     ("فلو توقف المخبر عنه، وهو وقوع الطلاق، على الخبر، وهو طلقتك، للزم الدور، وهذا باطل",)),
    ("U5", "آفات فهم الوقائع", "tafkir",
     ("فالتجريد والتعميم والقياس الشمولي، هي آفة فهم الوقائع والحوادث، أي آفة معرفة الأخبار",)),
    ("U6", "الموضوعية", "tafkir",
     ("حصر البحث في الموضوع نفسه وإبعاد أي شيء آخر عنه",)),
    ("U7", "طريق معرفة اللغة", "shakhsiyya-3",
     ("وهي الرواية الصحيحة عن العرب، إما توتراً، أو آحاداً، ولا طريق غيرهما",)),
    ("U8", "درجة النتيجة", "tafkir",
     ("ولكن تبقى فكراً صائباً حتى يتبين خطؤها",
      "إن كانت مما يتعلق بوجود الشيء كالعقائد فإنها أفكار قطعية",
      "وإن كانت مما يتعلق بالحكم على حقيقة الشيء أو صفته كالأحكام الشرعية فإنها أفكار ظنية")),
    ("M1", "المنطق أسلوب من الطريقة العقلية", "tafkir",
     ("ذلك أن المنطق تبنى نتائجه على مقدمات، وكذب هذه المقدمات أو صدقها ليس من السهل إدراكه في جميع"
      " الأحوال",
      "لذلك فإن المنطق وإن كان أسلوباً من أساليب الطريقة العقلية، ولكنه أسلوب عقيم")),
    ("M2", "المنطق ينتهي بالإحساس", "tafkir",
     ("لا يصل إلى النتائج من الإحساس بالواقع رأساً، وإنما ينتهي بالإحساس بالواقع",)),
)
"""الصفّ: (المفتاح، الاسم، الكتاب، العباراتُ بعينها في سطرٍ واحد). M1–M2 تصحيحُ نقل «المنطق» في
الخطّة."""

ABSENT: tuple[tuple[str, str], ...] = (
    ("U4", "أقبح المحال"),
    ("U5", "التعميم والتجريد والقياس الشمولي"),
    ("U7", 'إما تواترًا وإما آحادًا'),
    ("M1", "يتبنى نتائجه على مقدمات"),
)
"""(الدعوى، العبارةُ كما نُسبت في الخطّة الواردة): غائبةٌ بلفظها عن الكتب الثلاثة المختومة."""


def _read(name: str) -> list[str]:
    path, sha = BOOKS[name]
    raw = gzip.decompress((DATA / path).read_bytes())
    got = hashlib.sha256(raw).hexdigest()
    if got != sha:
        raise SystemExit(f"SOURCE_SHA_MISMATCH:{path}:{got}")
    return raw.decode("utf-8").split("\n")


def rows(books: dict[str, list[str]]) -> list[tuple[str, str, str, int, tuple[str, ...]]]:
    out = []
    for key, name, book, phrases in CRITERIA:
        lines = books[book]
        hit = [i for i, ln in enumerate(lines) if all(p in ln for p in phrases)]
        if len(hit) != 1:
            raise SystemExit(f"CRITERION_NOT_ON_ONE_LINE:{key}:{book}:{len(hit)}")
        out.append((key, name, book, hit[0] + 1, phrases))
    for key, phrase in ABSENT:
        if any(phrase in ln for lines in books.values() for ln in lines):
            raise SystemExit(f"ABSENT_PHRASE_FOUND:{key}:{phrase}")
    return out


def _lean_str(s: str) -> str:
    return '"' + s.replace("\\", "\\\\").replace('"', '\\"') + '"'


def render_lean(rs: list[tuple[str, str, str, int, tuple[str, ...]]]) -> str:
    lines = [
        "import Slge.Categories", "",
        "/-! معاييرُ الحكم العقليّ بعباراتها وأسطرها من كتب النبهانيّ المختومة (ADR ٤٩)؛",
        "مولَّدٌ بـ`tools/deposit_mayaatir.py`، لا يُحرَّر باليد. البصمات:",
    ]
    lines += [f"{b}: `{sha}`" + ("؛" if b != "shakhsiyya-3" else ".")
              for b, (_, sha) in BOOKS.items()]
    lines += [
        "الصفُّ: (المفتاح، الاسم، الكتاب، السطر، العباراتُ بعينها في ذلك السطر)؛",
        "و`absent`: عباراتٌ نُسبت إلى هذه الكتب في الخطّة الواردة وليست فيها بلفظها. -/", "",
        "namespace Slge.MayaatirTable", "",
        "def criteria : List (String × String × String × Nat × List String) := [",
    ]
    lines.append(",\n".join(
        f"  ({_lean_str(k)}, {_lean_str(n)}, {_lean_str(b)}, {ln}, "
        + "[" + ", ".join(_lean_str(p) for p in ph) + "])" for k, n, b, ln, ph in rs))
    lines += ["]", "",
              "def absent : List (String × String) := ["]
    lines.append(",\n".join(f"  ({_lean_str(k)}, {_lean_str(p)})" for k, p in ABSENT))
    lines += ["]", "",
              f"theorem criteria_length : criteria.length = {len(rs)} := by rfl", "",
              "/-- مفاتيحُ المعايير بترتيبها. -/",
              "def keys : List String := criteria.map (·.1)", "",
              "end Slge.MayaatirTable", ""]
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


def render_py(rs: list[tuple[str, str, str, int, tuple[str, ...]]]) -> str:
    lines = [
        '"""معاييرُ الحكم العقليّ بعباراتها وأسطرها من كتب النبهانيّ المختومة (ADR ٤٩)؛ مولَّدٌ',
        'بـ`tools/deposit_mayaatir.py`، لا يُحرَّر باليد."""',
        "", "from __future__ import annotations", "", "from typing import Final", "",
        "Row = tuple[str, str, str, int, tuple[str, ...]]",
        '"""(المفتاح، الاسم، الكتاب، السطر، العباراتُ بعينها في ذلك السطر)."""', "",
        "CRITERIA: Final[tuple[Row, ...]] = (",
    ]
    for k, n, b, ln, ph in rs:
        lines.append(f"    ({k!r}, {n!r}, {b!r}, {ln},")
        lines.append("     (")
        for p in ph:
            chunks = _chunks(p)
            lines += [f"         {c!r}" for c in chunks[:-1]] + [f"         {chunks[-1]!r},"]
        lines.append("     )),")
    lines += [")", "",
              "ABSENT: Final[tuple[tuple[str, str], ...]] = (",
              *[f"    ({k!r}, {p!r})," for k, p in ABSENT],
              ")", '"""(الدعوى، العبارةُ كما نُسبت في الخطّة الواردة): غائبةٌ بلفظها."""', "",
              "KEYS: Final[tuple[str, ...]] = tuple(r[0] for r in CRITERIA)", ""]
    return "\n".join(lines)


def main(argv: list[str]) -> int:
    rs = rows({b: _read(b) for b in BOOKS})
    lean, py = render_lean(rs), render_py(rs)
    if "--check" in argv:
        ok = LEAN.read_text(encoding="utf-8") == lean and PY.read_text(encoding="utf-8") == py
        sys.stdout.write("جدولا المعايير مطابقان للمختوم\n" if ok
                         else "جدولا المعايير غيرُ مطابقين\n")
        return 0 if ok else 1
    LEAN.write_text(lean, encoding="utf-8")
    PY.write_text(py, encoding="utf-8")
    for k, _, b, ln, ph in rs:
        sys.stdout.write(f"{k}\t{b}:{ln}\t{len(ph)}\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
