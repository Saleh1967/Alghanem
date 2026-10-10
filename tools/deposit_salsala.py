"""إيداعُ «السلسلة» — أركانُ المدلول الكونيّ على سلالم النبهانيّ الثلاثة (إذنُ المالك «موافق راجع
النبهاني أولا ونفذ»، 2026-10-10؛ ADR ٣١).

جدولُ المالك العشرون أُعيد ترتيبُه على ثلاثة سلالم بوسمٍ مرتَّب: **(أ) المعلوماتُ السابقة** — حقائقُ
الأشياء وخواصُّها، مرتبتُها يقينٌ في الوجود وظنٌّ في الكنه والصفات (التفكير 65، 123)؛ **(ب) الوضعُ
والنسب** — التسميةُ والنسبُ الثلاث (إسناديّة، تقييديّة، إضافيّة — لا «تضمينيّة») والفاعليّةُ والمفعوليّةُ
والإفادةُ شرطَ عدم الهذيان (ج3 393، 414)؛ **(ج) الحكمُ: علاقاتُ المجاز** — العلاقةُ والسببيّةُ
والمسببيّة (ج3 432–434). والجذرُ الأركانُ الأربعة (واقع، إحساس، ذهن، معلومات سابقة — ج3 393،
التفكير 24) لا «أوليات».

القاعدةُ معلَنة: `ROWS` = (الرقم، السلّم، الاسم، المرتبة، المراسي، السوالف، ملاحظة). المرساةُ (المودَع،
سطرُه، عبارةٌ بعينها) تُفحص في ذلك السطر من المختوم؛ وما لا مرساةَ له **معلَنٌ بقرار المالك** باسمه في
`DECLARED` (القابليّات، المكان، العدد) ولا يُوسَم بغير ذلك. السوالفُ من جدول المالك، ويُوسَم منها «منصوص»
ما له سطر.

يكتب `formal/Slge/SalsalaTable.lean` و`src/slge/salsala_table.py`؛ وبـ`--check` يقارنهما بما يولَّد
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
LEAN = ROOT / "formal" / "Slge" / "SalsalaTable.lean"
PY = ROOT / "src" / "slge" / "salsala_table.py"
SHA_J3 = "359bb5532ecee8156f266522bb5388a1711e46e136004c3ac22e43f2ce656cb4"
SHA_TAFKIR = "b9b08eabec468aa0f93b80c01879e3812c57f4bd677e68e448967e3575bfaae4"

LADDERS = ("المعلومات السابقة", "الوضع والنسب", "الحكم: علاقات المجاز")
GRADES = ("يقين", "ظنّ", "—")
"""المرتبة: يقينٌ (الوجودُ وحقائقُه) / ظنٌّ (الكنه والصفات) / — (ليس حكمًا على واقع: الجذرُ والوضعُ
والمجاز)."""
Anchor = tuple[str, int, str]
"""(المودَع «ج3» أو «التفكير»، سطرُه، عبارةٌ بعينها في ذلك السطر)."""
Row = tuple[int, int, str, int, tuple[Anchor, ...], tuple[int, ...], str]
"""(الرقم، السلّم 0..2، الاسم، المرتبة 0..2، المراسي، السوالف، ملاحظة)."""

ROWS: tuple[Row, ...] = (
    # (أ) المعلوماتُ السابقة
    (0, 0, "الأركان الأربعة", 2,
     (("ج3", 393, "نقل الواقع بواسطة الإحساس إلى الذهن مع معلومات سابقة"),
      ("التفكير", 24, "شرط أساسي ورئيسي للعقل")),
     (), "الجذر: واقعٌ وإحساسٌ وذهنٌ ومعلوماتٌ سابقة — لا «أوليات عقل» في النصّين"),
    (1, 0, "الوجود", 0,
     (("التفكير", 65, "نتيجة قطعية عن وجود الشيء"),), (0,), "اليقينُ الوحيد: الوجود"),
    (2, 0, "الحقائق", 0,
     (("التفكير", 123, "الحقائق تتعلق بالوجود، لا بالكنه ولا بالصفات"),
      ("التفكير", 123, "الحقائق هي أمر قطعي")), (1,), "فكرٌ مطابقٌ يقينًا، متعلَّقُه الوجود"),
    (3, 0, "الكنه (الماهية)", 1,
     (("التفكير", 65, "نتيجة ظنية عن كنه الشيء وصفته"),), (2,), "ظنٌّ أبدًا ولو تواتر الشهود"),
    (4, 0, "الأجناس والأنواع", 1,
     (("ج3", 406, "اسم الجنس، وهو اللفظ الموضوع للحقيقة الذهنية من حيث هي هي"),), (3,), ""),
    (5, 0, "الصفات", 1,
     (("التفكير", 65, "نتيجة ظنية عن كنه الشيء وصفته"),), (4,), ""),
    (6, 0, "الخواصّ", 1,
     (("ج3", 395, "حقائق الأشياء وخواصها"), ("ج3", 395, "آدم عرف الأشياء ولم يعرف اللغات")),
     (5,), "مستقلّةٌ عن اللغة بنصّه"),
    (7, 0, "القابليّات", 1, (), (6,), "معلَنٌ بقرار المالك: لا سطرَ يسمّيها ركنًا (433 لفظٌ في المجاز)"),
    (8, 0, "الحدث", 1,
     (("ج3", 498, "حدث مقترن بزمان محصل"),), (7,), "الحدثُ هو المصدر"),
    (9, 0, "الزمان", 1,
     (("ج3", 498, "الزمان المحصل هو الماضي، والحال، والمستقبل"),), (8,), ""),
    (10, 0, "المكان", 1, (), (1,), "معلَنٌ بقرار المالك: لا سطرَ يسمّيه ركنًا"),
    (11, 0, "العدد", 1, (), (4,), "معلَنٌ بقرار المالك: «مفهوم العدد» (580) دلالةٌ لا ركن"),
    # (ب) الوضعُ والنسب
    (12, 1, "التسمية (الوضع)", 2,
     (("ج3", 393, "الوضع هو تخصيص لفظ بمعنى"), ("ج3", 393, "الوضع للشيء فرع عن تصوره"),
      ("ج3", 397, "طريق معرفتها أخذها عنهم")),
     (1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11), "توقيعان: إدراكٌ (فرعُ التصوّر) ووثيقةٌ (أخذُها عنهم)"),
    (13, 1, "الإسناد", 2,
     (("ج3", 393, "النسب الإسنادية، أو التقييدية، أو الإضافية"),
      ("ج3", 393, "الغرض من وضع اللفظ إفادة النسب")), (12,), ""),
    (14, 1, "التقييد", 2,
     (("ج3", 393, "النسب الإسنادية، أو التقييدية، أو الإضافية"),), (12,), ""),
    (15, 1, "الإضافة", 2,
     (("ج3", 393, "النسب الإسنادية، أو التقييدية، أو الإضافية"),), (12,),
     "الثالثةُ بنصّه؛ لا «تضمينيّة»"),
    (16, 1, "الفاعلية", 2,
     (("ج3", 393, "كالفاعلية، والمفعولية"),), (13,), "نسبةٌ بين المفردات لا ركنٌ في الواقع"),
    (17, 1, "المفعولية", 2,
     (("ج3", 393, "كالفاعلية، والمفعولية"),), (13,), ""),
    (18, 1, "الإفادة (شرط عدم الهذيان)", 2,
     (("ج3", 414, "الغرض من التركيب هو الإفادة"), ("ج3", 414, "وهو الهذيان")),
     (13, 14, 15, 16, 17), "ما لا يفيد غيرُ موضوع"),
    # (ج) الحكم: علاقاتُ المجاز
    (19, 2, "العلاقة", 2,
     (("ج3", 432, "وجود العلاقة بين المعنى الحقيقي والمعنى المجازي"),), (12, 18),
     "شرطُ المجاز؛ من طبقة الحكم (المادّة ١٣)"),
    (20, 2, "السببية", 2,
     (("ج3", 433, "النوع الأول: السببية"), ("ج3", 433, "السببية القابلية")), (19,),
     "أربعةٌ: قابلية، صورية، فاعلية، غائية"),
    (21, 2, "المسببية", 2,
     (("ج3", 434, "النوع الثاني: المسببية"),), (19,), ""),
)
DECLARED: frozenset[int] = frozenset({7, 10, 11})
"""الأركانُ بلا مرساة: معلَنةٌ بقرار المالك (2026-10-10) لا من الذاكرة."""
SALAF_ANCHORED: frozenset[tuple[int, int]] = frozenset(
    {(12, k) for k in range(1, 12)} | {(13, 12), (14, 12), (15, 12), (16, 13), (17, 13)}
    | {(18, k) for k in (13, 14, 15, 16, 17)} | {(20, 19), (21, 19)} | {(1, 0)})
"""السوالفُ المنصوصة: الوضعُ فرعُ التصوّر (393)، النسبُ بالوضع (393)، الإفادةُ غرضُ التركيب (414)، السببيّةُ
نوعُ علاقة (433)، والوجودُ على الأركان (65 مع 24)؛ وما سواها من جدول المالك رأيٌ."""


def _read(path: Path, sha: str) -> list[str]:
    raw = gzip.decompress(path.read_bytes())
    got = hashlib.sha256(raw).hexdigest()
    if got != sha:
        raise SystemExit(f"SOURCE_SHA_MISMATCH:{path.name}:{got}")
    return raw.decode("utf-8").split("\n")


def verify(j3: list[str], tafkir: list[str]) -> None:
    """كلُّ مرساةٍ في سطرها بعينه؛ ما لا مرساةَ له في `DECLARED` لا غير؛ السوالفُ أصغرُ من الرقم."""

    ids = [r[0] for r in ROWS]
    if ids != list(range(len(ROWS))):
        raise SystemExit("ROWS_NOT_NUMBERED")
    for rid, ladder, name, grade, anchors, salaf, _ in ROWS:
        if ladder >= len(LADDERS) or grade >= len(GRADES):
            raise SystemExit(f"BAD_LADDER_OR_GRADE:{rid}")
        if (not anchors) != (rid in DECLARED):
            raise SystemExit(f"ANCHOR_OR_DECLARATION_MISSING:{rid}:{name}")
        for src, line, phrase in anchors:
            text = (j3 if src == "ج3" else tafkir)[line - 1]
            if phrase not in text:
                raise SystemExit(f"PHRASE_NOT_IN_LINE:{rid}:{src}:{line}:{phrase}")
        if any(s >= rid for s in salaf):
            raise SystemExit(f"SALAF_NOT_EARLIER:{rid}")
        if "التضمين" in name:
            raise SystemExit(f"TADMIN_IS_NOT_A_NISBA:{rid}")
    for rid, s in SALAF_ANCHORED:
        if s not in ROWS[rid][5]:
            raise SystemExit(f"ANCHORED_SALAF_NOT_IN_ROW:{rid}:{s}")


def _lean_str(s: str) -> str:
    return '"' + s.replace("\\", "\\\\").replace('"', '\\"') + '"'


def render_lean() -> str:
    out = [
        "import Slge.Categories", "",
        "/-! السلسلة — أركانُ المدلول الكونيّ على سلالم النبهانيّ الثلاثة؛ مولَّدٌ",
        f"بـ`tools/deposit_salsala.py` من المختومَين (SHA-256 `{SHA_J3}`،",
        f"`{SHA_TAFKIR}`)، لا يُحرَّر باليد.",
        "الصفُّ: (الرقم، السلّم، الاسم، المرتبة، المراسي (المودَع، السطر، العبارة)، السوالف). -/", "",
        "namespace Slge.SalsalaTable", "",
        "structure Rukn where",
        "  id : Nat",
        "  ladder : Nat",
        "  name : String",
        "  grade : Nat",
        "  anchors : List (String × Nat × String)",
        "  salaf : List Nat",
        "  deriving DecidableEq, Repr", "",
        "def rows : List Rukn := [",
    ]
    rs = []
    for rid, ladder, name, grade, anchors, salaf, _ in ROWS:
        an = "[" + ", ".join(f"({_lean_str(s)}, {n}, {_lean_str(p)})" for s, n, p in anchors) + "]"
        sa = "[" + ", ".join(str(s) for s in salaf) + "]"
        rs.append(f"  ⟨{rid}, {ladder}, {_lean_str(name)}, {grade}, {an}, {sa}⟩")
    decl = "[" + ", ".join(str(d) for d in sorted(DECLARED)) + "]"
    out += [",\n".join(rs), "]", "",
            f"theorem rows_length : rows.length = {len(ROWS)} := by rfl", "",
            "/-- الأركانُ بلا مرساة، معلَنةٌ بقرار المالك. -/",
            f"def declared : List Nat := {decl}", "",
            "end Slge.SalsalaTable", ""]
    return "\n".join(out)


def render_py() -> str:
    out = [
        '"""السلسلة — أركانُ المدلول الكونيّ على سلالم النبهانيّ الثلاثة؛ مولَّدٌ',
        f'بـ`tools/deposit_salsala.py` (SHA-256 {SHA_J3[:16]}…، {SHA_TAFKIR[:16]}…)؛',
        'لا يُحرَّر باليد."""', "",
        "from __future__ import annotations", "", "from typing import Final", "",
        f"LADDERS: Final[tuple[str, ...]] = {LADDERS!r}",
        f"GRADES: Final[tuple[str, ...]] = {GRADES!r}",
        "Anchor = tuple[str, int, str]",
        "Row = tuple[int, int, str, int, tuple[Anchor, ...], tuple[int, ...], str]",
        '"""(الرقم، السلّم، الاسم، المرتبة، المراسي، السوالف، ملاحظة)."""', "",
        "ROWS: Final[tuple[Row, ...]] = (",
    ]
    for rid, ladder, name, grade, anchors, salaf, note in ROWS:
        out.append(f"    ({rid}, {ladder}, {name!r}, {grade},")
        out.append("     (")
        out += [f"         ({src!r}, {line}, {ph!r})," for src, line, ph in anchors]
        out.append("     ),")
        out.append(f"     {salaf!r},")
        out.append(f"     {note!r}),")
    sa = ",\n    ".join(repr(x) for x in sorted(SALAF_ANCHORED))
    out += [")", f"DECLARED: Final[frozenset[int]] = frozenset({sorted(DECLARED)!r})",
            "SALAF_ANCHORED: Final[frozenset[tuple[int, int]]] = frozenset([", f"    {sa},", "])",
            ""]
    return "\n".join(out)


def main(argv: list[str]) -> int:
    verify(_read(J3, SHA_J3), _read(TAFKIR, SHA_TAFKIR))
    lean, py = render_lean(), render_py()
    if "--check" in argv:
        ok = LEAN.read_text(encoding="utf-8") == lean and PY.read_text(encoding="utf-8") == py
        sys.stdout.write("جدولا السلسلة مطابقان للمختومَين\n" if ok
                         else "جدولا السلسلة غيرُ مطابقين\n")
        return 0 if ok else 1
    LEAN.write_text(lean, encoding="utf-8")
    PY.write_text(py, encoding="utf-8")
    sys.stdout.write(f"كُتب جدولا السلسلة: {len(ROWS)} ركنًا، {len(DECLARED)} معلَنة\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
