"""إيداعُ توقيع الحاجة (ADR ٥٦): ما يحتاجه كلُّ بابٍ من أبواب المغلق ليتمّ — بعباراته بعينها وسطرِه في ج3
المختوم (`nabhani-shakhsiyya-3.txt.gz`) أو في الكتاب المختوم (`openiti-sibawayh-kitab.txt.gz`).

القاعدةُ معلَنة على نسق `tools/deposit_bawwabat.py`: `ANCHORS` = (المفتاح، الكتاب، الاسم، العبارات)،
والعباراتُ كلُّها
في **سطرٍ واحد** من كتابها؛ وما لم يوجد خطأٌ مسمًّى (`HAJA_NOT_ON_ONE_LINE`). والحاجةُ المكتوبة في
`formal/Slge/Haja.lean` قراءةُ هذه العبارات لا غيرُها.

يكتب `formal/Slge/HajaTable.lean` و`src/slge/haja_table.py`؛ وبـ`--check` يقارنهما بما يولَّد الآن.
"""

from __future__ import annotations

import gzip
import hashlib
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "tests" / "data"
LEAN = ROOT / "formal" / "Slge" / "HajaTable.lean"
PY = ROOT / "src" / "slge" / "haja_table.py"

BOOKS: dict[str, tuple[str, str]] = {
    "shakhsiyya-3": ("nabhani-shakhsiyya-3.txt.gz",
                     "359bb5532ecee8156f266522bb5388a1711e46e136004c3ac22e43f2ce656cb4"),
    "kitab": ("openiti-sibawayh-kitab.txt.gz",
              "a160f940bb194e6fe7e6655d2c7f28e41f1fc648c4c5e340cc4e42306d5cb625"),
}

ANCHORS: tuple[tuple[str, str, str, tuple[str, ...]], ...] = (
    ("H_MUSTAQILL", "shakhsiyya-3", "المستقلُّ يُفهم معناه بلا لفظٍ آخر",
     ("وإن كان يستقل بمعناه، أي يفهم معناه من غير حاجة للفظ آخر",)),
    ("H_HARF", "shakhsiyya-3", "الحرفُ لا يستقلّ: متعلَّقُ معناه لفظٌ آخر",
     ("فهو لا يستقل بمعناه؛ لأنه لا يفهم معناه الذي وضع له إلا باعتبار لفظ آخر دال على"
      " معنى هو متعلق معنى الحرف",)),
    ("H_DAMIR", "shakhsiyya-3", "المضمرُ يفتقر إلى ما يفسّره",
     ("وإن لم يستقل، بأن كان يفتقر إلى شيء يفسره، فهو المضمر",)),
    ("H_IDAFA", "shakhsiyya-3", "حروفُ الإضافة تُفضي بمعاني الأفعال إلى الأسماء",
     ("حروف الإضافة، وهي ما يفضي بمعاني الأفعال إلى الأسماء",)),
    ("H_MUSHABBAHA", "shakhsiyya-3", "المشبّهةُ بالفعل تنصب الاسم وترفع الخبر",
     ("وهي تنـصـب الاسـم وترفـع الخـبر",)),
    ("H_ATF", "shakhsiyya-3", "العطفُ بين معطوفٍ ومعطوفٍ عليه",
     ("تشترك في أن المعطوف مخالف للمعطوف عليه في حكمه", "تقول: جاءني زيد لا عمرو")),
    ("H_ISTITHNA", "shakhsiyya-3", "الاستثناءُ يُخرج ما بعده ممّا قبله متّصلًا",
     ("إخراج ما بعد «إلا» أو إحدى أخواتها مما قبلها",
      "وشرط صحة الاستثناء أن يكون متصلاً بالمستثنى منه",
      "وأدوات الاستثناء هي: «إلا» و«غير» و«سوى»")),
    ("H_SHART", "shakhsiyya-3", "الشرطُ متّصلٌ بالمشروط قبله أو بعده",
     ("أن يكون متصلاً بالمشروط حقيقة من غير تخلل فاصل بينهما",
      "ويجوز تقديمه على المشروط وتأخيره عنه ولكن مع بقاء الاتصال",
      "وهي: «إن» الخفيفة و«إذا» و«من» و«مهما» و«حيثما» و«أينما»")),
    ("H_NAFY", "shakhsiyya-3", "النفيُ على ما بعده", ("«ما» لنفي الحـال", "ما تفعل، ما فعل")),
    ("H_ISTIQBAL", "shakhsiyya-3", "أدواتُ الفعل تدخل عليه",
     ("وحروف الاستقبال وهي: «السين» و«سوف» و«أن» و«لا» و«إن»", "وسوف يفعل")),
    ("H_TANBIH", "shakhsiyya-3", "التنبيهُ على ما بعده",
     ("حروف التنبيه، وهي: «ها» و«ألا» و«أما»", "«ألا رجل يدلني على الطريق»")),
    ("H_JAWAB", "shakhsiyya-3", "الجوابُ لما سبق من قول",
     ("«نعم»: مصدقة لما سبق من قول القائل",)),
    ("H_JAWAB_HURUF", "shakhsiyya-3", "حروفُ الجواب بأسمائها",
     ("حروف الجواب وهي: «نعم» و«بلى» و«أجل»",)),
    ("H_LAW", "shakhsiyya-3", "حرفا الشرط إنْ ولو", ("وحروف الشرط وهي: «إن» و«لو»",)),
    ("H_RAD", "shakhsiyya-3", "الردعُ جوابٌ لما قيل",
     ("وحرف الردع وهو «كلا» في قولك جواباً لمن قال لك",)),
    ("H_MAWSUL", "kitab", "الموصولُ لا يتمّ إلّا بصلته",
     ("كما كان الذي لا يتم إلا بحشوه",)),
    ("H_SADARA", "kitab", "الاستفهامُ والجزاءُ ليس ما بعدهما صلةً لما قبلهما",
     ("الجزاء بصلة لما قبله كما أنه في حروف الاستفهام ليس صلة لما قبله",)),
    ("H_NIDA", "kitab", "المنادى اسمٌ منصوبٌ على إضمار الفعل",
     ("اعلم أن النداء كل اسم مضاف فيه فهو نصب على إضمار الفعل المتروك",)),
)
"""الصفّ: (المفتاح، الكتاب، الاسم، العباراتُ بعينها في سطرٍ واحد)."""


def _read(name: str) -> list[str]:
    path, sha = BOOKS[name]
    raw = gzip.decompress((DATA / path).read_bytes())
    got = hashlib.sha256(raw).hexdigest()
    if got != sha:
        raise SystemExit(f"SOURCE_SHA_MISMATCH:{path}:{got}")
    return raw.decode("utf-8").split("\n")


def rows(books: dict[str, list[str]]) -> list[tuple[str, str, str, int, tuple[str, ...]]]:
    out = []
    for key, book, name, phrases in ANCHORS:
        hit = [i for i, ln in enumerate(books[book]) if all(p in ln for p in phrases)]
        if len(hit) != 1:
            raise SystemExit(f"HAJA_NOT_ON_ONE_LINE:{key}:{book}:{len(hit)}")
        out.append((key, book, name, hit[0] + 1, phrases))
    return out


def _lean_str(s: str) -> str:
    return '"' + s.replace("\\", "\\\\").replace('"', '\\"') + '"'


def render_lean(rs: list[tuple[str, str, str, int, tuple[str, ...]]]) -> str:
    lines = [
        "import Slge.Categories", "",
        "/-! توقيعُ الحاجة بعباراته وأسطره من ج3 والكتاب المختومَين (ADR ٥٦)؛",
        "مولَّدٌ بـ`tools/deposit_haja.py`، لا يُحرَّر باليد. البصمات:",
    ]
    lines += [f"{b}: `{sha}`" + ("؛" if b != "kitab" else ".") for b, (_, sha) in BOOKS.items()]
    lines += [
        "الصفُّ: (المفتاح، الكتاب، الاسم، السطر، العباراتُ بعينها في ذلك السطر). -/", "",
        "namespace Slge.HajaTable", "",
        "def anchors : List (String × String × String × Nat × List String) := [",
    ]
    lines.append(",\n".join(
        f"  ({_lean_str(k)}, {_lean_str(b)}, {_lean_str(n)}, {ln}, "
        + "[" + ", ".join(_lean_str(p) for p in ph) + "])" for k, b, n, ln, ph in rs))
    lines += ["]", "",
              f"theorem anchors_length : anchors.length = {len(rs)} := by rfl", "",
              "/-- مفاتيحُ المراسي بترتيبها. -/",
              "def keys : List String := anchors.map (·.1)", "",
              "end Slge.HajaTable", ""]
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
        '"""توقيعُ الحاجة بعباراته وأسطره من ج3 والكتاب المختومَين (ADR ٥٦)؛ مولَّدٌ',
        'بـ`tools/deposit_haja.py`، لا يُحرَّر باليد."""',
        "", "from __future__ import annotations", "", "from typing import Final", "",
        "Row = tuple[str, str, str, int, tuple[str, ...]]",
        '"""(المفتاح، الكتاب، الاسم، السطر، العباراتُ بعينها في ذلك السطر)."""', "",
        "ANCHORS: Final[tuple[Row, ...]] = (",
    ]
    for k, b, n, ln, ph in rs:
        lines.append(f"    ({k!r}, {b!r}, {n!r}, {ln},")
        lines.append("     (")
        for p in ph:
            chunks = _chunks(p)
            lines += [f"         {c!r}" for c in chunks[:-1]] + [f"         {chunks[-1]!r},"]
        lines.append("     )),")
    lines += [")", "",
              "KEYS: Final[tuple[str, ...]] = tuple(r[0] for r in ANCHORS)", ""]
    return "\n".join(lines)


def main(argv: list[str]) -> int:
    rs = rows({b: _read(b) for b in BOOKS})
    lean, py = render_lean(rs), render_py(rs)
    if "--check" in argv:
        ok = LEAN.read_text(encoding="utf-8") == lean and PY.read_text(encoding="utf-8") == py
        sys.stdout.write("جدولا الحاجة مطابقان للمختوم\n" if ok else "جدولا الحاجة غيرُ مطابقين\n")
        return 0 if ok else 1
    LEAN.write_text(lean, encoding="utf-8")
    PY.write_text(py, encoding="utf-8")
    for k, b, _, ln, ph in rs:
        sys.stdout.write(f"{k}\t{b}:{ln}\t{len(ph)}\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
