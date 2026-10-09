"""إيداعُ تقسيمات اللفظ عند النبهانيّ من «أبحاث اللغة» (الشخصيّة الإسلاميّة ج3) و«التفكير» —
المختومان `tests/data/nabhani-shakhsiyya-3.txt.gz` و`tests/data/nabhani-tafkir.txt.gz` (بإذن المالك،
2026-10-09): لكلّ بحثٍ عنوانُه بسطره وعباراتُه بعينها في نصّ البحث — التقسيمُ الثلاثيُّ (الدالُّ وحده /
الدالُّ والمدلول / المدلولُ وحده) وما تحته: الدلالاتُ الثلاث والتراكيبُ الثلاثة، المفردُ وأقسامُ الاسم،
المدلولُ الخمسة، المركّبُ الستّة، الدالُّ والمدلولُ السبعة، علاقاتُ المجاز الإحدى عشرة والسببيّةُ الأربع،
الترجيحُ عند تعارض ما يخلّ بالفهم (خمسةُ احتمالاتٍ وعشرةُ أوجه)، الفعلُ وصيغةُ الأمر، المنطوقُ والمفهومُ
وأشكالُ المخالفة، والعموم.

القاعدةُ معلَنة: `SECTIONS` = (المفتاح، عنوانُ البحث كما في النصّ بلا تطويل، العباراتُ المطلوبة). الأداةُ
تثبت أنّ العنوانَ موجودٌ بترتيبه وأنّ كلَّ عبارةٍ واردةٌ في نصّ ذلك البحث بعينه (من عنوانه إلى عنوان البحث
التالي في القائمة)؛ ما لم يوجد خطأٌ مسمًّى لا يُتجاوز. لا يُشكَّل نصٌّ ولا يُطبَّع: التطويلُ وحدَه يُسقَط من
العناوين.

يكتب `formal/Slge/NabhaniTable.lean` و`src/slge/nabhani_table.py`؛ وبـ`--check` يقارنهما بما يولَّد
الآن.
"""

from __future__ import annotations

import gzip
import hashlib
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
J3 = ROOT / "tests" / "data" / "nabhani-shakhsiyya-3.txt.gz"
TAFKIR = ROOT / "tests" / "data" / "nabhani-tafkir.txt.gz"
LEAN = ROOT / "formal" / "Slge" / "NabhaniTable.lean"
PY = ROOT / "src" / "slge" / "nabhani_table.py"
SHA_J3 = "359bb5532ecee8156f266522bb5388a1711e46e136004c3ac22e43f2ce656cb4"
SHA_TAFKIR = "b9b08eabec468aa0f93b80c01879e3812c57f4bd677e68e448967e3575bfaae4"
TATWEEL = "ـ"

SECTIONS: tuple[tuple[str, str, tuple[str, ...]], ...] = (
    ("الوضع-والنسب", "أبحاث اللغة",
     ("الوضع هو تخصيص لفظ بمعنى", "الفكر هو الحكم على الواقع",
      "النسب الإسنادية، أو التقييدية، أو الإضافية", "الفاعلية، والمفعولية",
      "النقل المتواتر وخبر الآحاد", "وأما العقل فلا ينفع في معرفة اللغة")),
    ("الأقسام-الثلاثة", "ألفاظ اللغة وأقسامها",
     ("الأول للدال وحده", "الثاني باعتبار الدال والمدلول", "الثالث للمدلول وحده")),
    ("الدال-وحده", "تقسيم اللفظ باعتبار الدال وحده",
     ("دلالة المطابقة", "دلالة التضمن", "دلالة الالتزام", "اللزوم شرط وليس بموجب",
      "تركيب إسناد", "تركيب مزج", "تركيب إضافة")),
    ("المفرد", "المفرد", ("اسم، وفعل، وحرف", "لا يستقل بمعناه", "دل بهيئته")),
    ("الاسم", "الاسم",
     ("الكلي", "الجزئي", "المتواطئ", "المشكك", "اسم الجنس", "المشتق", "العلم", "المضمر",
      "يفتقر إلى شيء يفسره")),
    ("المدلول-وحده", "تقسيم اللفظ باعتبار المدلول وحده",
     ("مدلول اللفظ معنى", "لفظاً مفرداً مستعملاً", "لفظاً مفرداً مهملاً", "لفظاً مركباً مستعملاً",
      "لفظاً مركباً مهملاً", "الهذيان", "غير موضوع، أي لم تضعه العرب")),
    ("المركب", "المر\u064e\u0643\u0651\u064eب",  # العنوانُ مشكولٌ في النصّ بترتيب حركاته كما هو
     ("من أقسام الدال وحده", "الاستفهام", "الأمر", "الالتماس", "السؤال", "الخبر", "التنبيه",
      "مع الاستعلاء", "مع التساوي", "مع التسفل")),
    ("الدال-والمدلول", "تقسيم اللفظ باعتبار الدال والمدلول",
     ("المنفرد", "المتباين", "المترادف", "المشترك", "المنقول", "الحقيقة", "المجاز",
      "منقولاً شرعياً", "منقولاً عرفاً", "منقولاً اصطلاحاً", "الترادف خلاف الأصل",
      "المشترك خلاف الأصل", "مفتقراً إلى قرينة")),
    ("علاقات-المجاز", "الحقيقة والمجاز",
     ("النوع الأول: السببية", "النوع الثاني: المسببية", "النوع الثالث: المشابهة",
      "النوع الرابع: المضادة", "النوع الخامس: الكلية", "النوع السادس: الجزئية",
      "النوع السابع: الاستعداد", "النوع الثامن: المجاورة", "النوع التاسع: الزيادة",
      "النوع العاشر: تسمية الشيء باعتبار ما كان عليه", "الحادي عشـر: التعلق الحاصـل بين المصدر",
      "السببية القابلية", "السببية الصورية", "السببية الفاعلية", "الســببية الغائية",
      "المجاز بالذات إنما يكون في اسم الجنس", "فلا يكون المجاز في الحرف",
      "الفعل بأقسامه، والمشتق بأقسامه", "ثالثها: العلم", "الأصل في الكلام هو الحقيقة")),
    ("الترجيح", "تعارض ما يخل بالفهم",
     ("الاشتراك، والنقل، والمجاز، والإضمار، والتخصيص", "عشرة أوجه",
      "النقل أولى من الاشتراك", "المجاز أولى من الاشتراك", "الإضمار أولى من الاشتراك",
      "التخصيص أولى من الاشتراك", "المجاز أولى من النقل", "الإضمار أولى من النقل",
      "التخصيص أولى من النقل", "الإضمار مثل المجاز", "التخصيص أولى من المجاز",
      "التخصيص أولى من الإضمار")),
    ("الفعل", "الفعل",
     ("حدث مقترن بزمان محصل", "الحدث هو المصدر", "الهمزة، والتاء، والنون، والياء",
      "نـزع منه حرف المضارعة")),
    ("المنطوق", "المنطوق", ("قطعاً في محل النطق", "مطابقة أو تضمناً")),
    ("المفهوم", "المفهوم",
     ("دلالة الالتزام", "دلالة الاقتضاء", "دلالة التنبيه والإيماء", "دلالة الإشارة",
      "مفهوم الموافقة", "مفهوم المخالفة")),
    ("مفهوم-الصفة", "مفهوم الصفة", ("تعليق الحكم بصفة", "وصفاً مفهماً")),
    ("مفهوم-الشرط", "مفهوم الشرط", ("تعليق الحكم على الشيء بكلمة «إن»",)),
    ("مفهوم-الغاية", "مفهوم الغاية", ()),
    ("مفهوم-العدد", "مفهوم العدد", ()),
    ("صيغة-الأمر", "صيغة الأمر",
     ("صيـغة «افعل»", "اسم الفعل", "المضارع المقرون بلام الأمر", "لا توجد هناك صيغة غيرها",
      "لستة عشر معنى")),
    ("العموم", "طرق ثبوت العموم للفظ",
     ("«أي»", "«كل»", "«جميع»", "«الذين»", "«اللاتي»", "«من»", "«أل»", "والإضافة",
      "النكرة في سياق النفي", "الفعل المتعدي المنفي", "ترتيب الحكم على الوصف بفاء التعقيب")),
)
"""أبحاثُ ج3 بترتيبها في النصّ؛ البحثُ الأخير يمتدّ ثلاثين سطرًا بعد عنوانه."""

TAFKIR_PHRASES: tuple[str, ...] = (
    "معلومات سابقة عن موضوع النص", "مدركاً واقعها", "فهماً لغوياً",
)
"""«التفكير»: فهمُ النصّ الفكريّ لا يتمّ إلّا بمعلوماتٍ سابقةٍ مُدرَكٍ واقعُها، وإلّا كان فهمًا لغويًّا."""


def _read(path: Path, sha: str) -> list[str]:
    raw = gzip.decompress(path.read_bytes())
    got = hashlib.sha256(raw).hexdigest()
    if got != sha:
        raise SystemExit(f"SOURCE_SHA_MISMATCH:{path.name}:{got}")
    return raw.decode("utf-8").split("\n")


def _title(line: str) -> str:
    return line.replace(TATWEEL, "").strip()


def rows(lines: list[str]) -> list[tuple[str, int, tuple[str, ...]]]:
    out: list[tuple[str, int, tuple[str, ...]]] = []
    starts: list[int] = []
    pos = 0
    for key, title, _ in SECTIONS:
        found = next((i for i in range(pos, len(lines)) if _title(lines[i]) == title), None)
        if found is None:
            raise SystemExit(f"SECTION_NOT_FOUND:{key}:{title}@>{pos}")
        starts.append(found)
        pos = found + 1
    for n, (key, _, phrases) in enumerate(SECTIONS):
        a = starts[n]
        b = starts[n + 1] if n + 1 < len(starts) else a + 30
        body = "\n".join(lines[a:b])
        for ph in phrases:
            if ph not in body:
                raise SystemExit(f"PHRASE_NOT_IN_SECTION:{key}:{ph}@{a + 1}")
        out.append((key, a + 1, phrases))
    return out


def tafkir_row(lines: list[str]) -> tuple[str, int, tuple[str, ...]]:
    text = "\n".join(lines)
    for ph in TAFKIR_PHRASES:
        if ph not in text:
            raise SystemExit(f"PHRASE_NOT_IN_TAFKIR:{ph}")
    line = next(i for i, ln in enumerate(lines) if TAFKIR_PHRASES[0] in ln) + 1
    return ("التفكير-المعلومات-السابقة", line, TAFKIR_PHRASES)


def _lean_str(s: str) -> str:
    return '"' + s.replace("\\", "\\\\").replace('"', '\\"') + '"'


def render_lean(rs: list[tuple[str, int, tuple[str, ...]]]) -> str:
    lines = [
        "import Slge.Categories", "",
        "/-! تقسيماتُ اللفظ عند النبهانيّ — أبحاثُ اللغة في الشخصيّة الإسلاميّة ج3 و«التفكير»، مختومَين",
        f"(SHA-256 `{SHA_J3}`،",
        f"`{SHA_TAFKIR}`)؛",
        "مولَّدٌ بـ`tools/deposit_nabhani.py`، لا يُحرَّر باليد.",
        "الصفُّ: (مفتاحُ البحث، سطرُ عنوانه في المودَع، عباراتُه بعينها كما وُجدت في نصّه). -/", "",
        "namespace Slge.NabhaniTable", "",
        "def sections : List (String × Nat × List String) := [",
    ]
    rows_l = []
    for key, line, phrases in rs:
        ph = "[" + ", ".join(_lean_str(p) for p in phrases) + "]"
        rows_l.append(f"  ({_lean_str(key)}, {line}, {ph})")
    lines += [",\n".join(rows_l), "]", "",
              f"theorem sections_length : sections.length = {len(rs)} := by rfl", "",
              "/-- عباراتُ بحثٍ بمفتاحه (فارغةٌ إن لم يوجد). -/",
              "def phrases (key : String) : List String :=",
              "  ((sections.find? (·.1 == key)).map (·.2.2)).getD []", "",
              "end Slge.NabhaniTable", ""]
    return "\n".join(lines)


def render_py(rs: list[tuple[str, int, tuple[str, ...]]]) -> str:
    lines = [
        '"""تقسيماتُ اللفظ عند النبهانيّ — أبحاثُ اللغة (ج3) و«التفكير» مختومَين؛ مولَّدٌ',
        f'بـ`tools/deposit_nabhani.py` (SHA-256 {SHA_J3[:16]}…، {SHA_TAFKIR[:16]}…)؛',
        'لا يُحرَّر باليد."""',
        "", "from __future__ import annotations", "", "from typing import Final", "",
        "Row = tuple[str, int, tuple[str, ...]]",
        '"""(مفتاحُ البحث، سطرُ عنوانه في المودَع، عباراتُه بعينها)."""', "",
        "SECTIONS: Final[tuple[Row, ...]] = (",
    ]
    for key, line, phrases in rs:
        lines.append(f"    ({key!r}, {line},")
        lines.append("     (")
        lines += [f"         {p!r}," for p in phrases]
        lines.append("     )),")
    lines += [")", "", "",
              "def phrases(key: str) -> tuple[str, ...]:",
              "    return next((p for k, _, p in SECTIONS if k == key), ())", ""]
    return "\n".join(lines)


def main(argv: list[str]) -> int:
    rs = rows(_read(J3, SHA_J3))
    rs.append(tafkir_row(_read(TAFKIR, SHA_TAFKIR)))
    lean, py = render_lean(rs), render_py(rs)
    if "--check" in argv:
        ok = LEAN.read_text(encoding="utf-8") == lean and PY.read_text(encoding="utf-8") == py
        sys.stdout.write("جدولا النبهانيّ مطابقان للمختوم\n" if ok
                         else "جدولا النبهانيّ غيرُ مطابقين\n")
        return 0 if ok else 1
    LEAN.write_text(lean, encoding="utf-8")
    PY.write_text(py, encoding="utf-8")
    for key, line, phrases in rs:
        sys.stdout.write(f"{key}: {line} ({len(phrases)} عبارة)\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
