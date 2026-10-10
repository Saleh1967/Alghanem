"""إيداعُ صور الشرطيّ المتّصل عند الغزاليّ بأسطرها من مودَعه المختوم (إذنُ المالك «أودع ما يوافق النبهاني
وأعطي إذنًا لغيره كشاهدٍ أو رأيٍ ثانٍ»، 2026-10-10؛ ADR ٣٣).

جدولُ `Slge.Ghazali.stated` كان مكتوبًا باليد من الذاكرة؛ وهنا تُرسى خاناتُه الثماني كلٌّ بسطرها وعبارتها
من المختومات الثلاثة (معيار العلم، المستصفى، محكّ النظر)، على ثلاثة أصناف بوسم المالك:

* **خانةُ منطق** (`kind = 0`، ثمانٍ): الدرجةُ (أخصّ/مساوٍ) والصورةُ (عين المقدَّم، نقيض التالي، نقيض
  المقدَّم، عين التالي) وهل تُنتج — **رأيٌ ثانٍ**: لا مرساةَ لها في النبهانيّ، والمنطقُ عنده «أسلوبٌ من
  أساليب البحث» لا طريقةٌ، فيه «قابلية الخداع» (التفكير 67، 72–73).
* **قراءةٌ أصوليّة** (`kind = 1`، اثنتان): مفهومُ الموافقة (الأخصُّ يُنتج عينَ المقدَّم: «لا تقل لهما أفّ»)
  ومفهومُ المخالفة بالشرط (المساوي يُنتج نقيضَ المقدَّم: «عدم المشروط عند عدم الشرط») — **موافقةٌ
  للنبهانيّ**: مرساةٌ في المودَعَين معًا (المستصفى، ج3 559–577).
* **منهجٌ** (`kind = 2`، واحد): نصُّ النبهانيّ في المنطق، وبه يُوسَم الصنفُ الأوّل رأيًا ثانيًا لا مودَعًا.

القاعدةُ معلَنة: `ROWS` = (الرقم، الصنف، الدرجة، الصورة، هل تُنتج، مراسي الغزاليّ، مراسي النبهانيّ،
ملاحظة). المرساةُ (المودَع، سطرُه، عبارةٌ بعينها) تُفحص في ذلك السطر من المختوم. يكتب
`formal/Slge/GhazaliTable.lean` و`src/slge/ghazali_table.py`؛ وبـ`--check` يقارنهما بما يولَّد الآن.
"""

from __future__ import annotations

import gzip
import hashlib
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "tests" / "data"
LEAN = ROOT / "formal" / "Slge" / "GhazaliTable.lean"
PY = ROOT / "src" / "slge" / "ghazali_table.py"
SOURCES = {
    "ج3": (DATA / "nabhani-shakhsiyya-3.txt.gz",
           "359bb5532ecee8156f266522bb5388a1711e46e136004c3ac22e43f2ce656cb4"),
    "التفكير": (DATA / "nabhani-tafkir.txt.gz",
                "b9b08eabec468aa0f93b80c01879e3812c57f4bd677e68e448967e3575bfaae4"),
    "المستصفى": (DATA / "openiti-ghazali-mustasfa.txt.gz",
                 "59cda7d5424b26ab73aa2d7d8130d1fbe28fc465ab6075d759dc782ebe1697ac"),
    "محك النظر": (DATA / "openiti-ghazali-mihakk.txt.gz",
                  "9e54d050a9178392f48057738dd96796ddee094faff357bdb554e9e3cf6f5948"),
    "معيار العلم": (DATA / "openiti-ghazali-micyar.txt.gz",
                    "2ddf91651376fddd834fbf27ba14c532f3a32303eb1b82860fc2314fd3392259"),
}
NABHANI = ("ج3", "التفكير")
"""العمود: مراسي الموافقة لا تكون إلّا منه."""
GHAZALI = ("المستصفى", "محك النظر", "معيار العلم")

KINDS = ("خانة منطق (رأي ثانٍ)", "قراءة أصولية (موافقة للنبهاني)", "منهج النبهاني في المنطق")
DEGREES = ("akhass", "musawi")
FORMS = ("aynMuqaddam", "naqidTali", "naqidMuqaddam", "aynTali")
Anchor = tuple[str, int, str]
Row = tuple[int, int, int, int, bool, tuple[Anchor, ...], tuple[Anchor, ...], str]
"""(الرقم، الصنف 0..2، الدرجة 0..1، الصورة 0..3، هل تُنتج، مراسي الغزاليّ، مراسي النبهانيّ، ملاحظة)."""

_M = "معيار العلم"
_S = "المستصفى"
_H = "محك النظر"
_SHAMS = (_M, 1525, "التالي مساو للمقدم لا أعم منه ولا")
_MUSAWI = (_M, 1524, "وإنما ينتج إستثناء عين التالي ونقيض المقدم، إذا ثبت أن")

ROWS: tuple[Row, ...] = (
    # خاناتُ المنطق الثماني — رأيٌ ثانٍ
    (0, 0, 0, 0, True,
     ((_M, 1510, "والمنتج منه إثنان وهو عين المقدم ونقيض التالي"),
      (_S, 1240, "أما المنتج فتسليم عين المقدم ينتج عين اللازم"),
      (_H, 143, "فتسليم عين القضية التي سميناها مقدما")), (),
     "«إن كان إنسانا فهو حيوان، لكنه إنسان» ← حيوان"),
    (1, 0, 0, 1, True,
     ((_M, 1510, "والمنتج منه إثنان وهو عين المقدم ونقيض التالي"),
      (_S, 1243, "تسليم نقيض اللازم فإنه ينتج نقيض المقدم"),
      (_H, 155, "فانظر كيف أنتج تسليم نقيض اللازم نقيض المقدم")), (),
     "«لكنه ليس بحيوان» ← ليس بإنسان"),
    (2, 0, 0, 2, False,
     ((_M, 1516, "فأما إستثناء نقيض المقدم، وهو أنه ليس بإنسان، فلا ينتج لا"),
      (_M, 1517, "إذ ربما يكون فرسا"),
      (_S, 1253, "وكذلك تسليم نقيض المقدم لا ينتج"),
      (_H, 176, "وكذالك تسليم نقيض المقدم لا ينتج لا عين اللازم ولا نقيضه")), (),
     "عقيم: «ربما يكون فرسا» وربما «حجرا»"),
    (3, 0, 0, 3, False,
     ((_M, 1510, "وأما عين التالي ونقيض"), (_M, 1511, "المقدم فلا ينتجان"),
      (_S, 1251, "وأما الذي لا ينتج فهو تسليم عين اللازم"),
      (_H, 172, "فأما الذي لا ينتج . . فهو تسليم عين اللازم")), (),
     "عقيم: «قد تفسد الصلاة بعلة أخرى»"),
    (4, 0, 1, 0, True, ((_M, 1526, "لكن الشمس طالعة فالنهار موجود"), _SHAMS), (),
     "المساوي: «إن كانت الشمس طالعة فالنهار موجود»"),
    (5, 0, 1, 1, True,
     ((_M, 1527, "لكن النهار غير موجود"), (_M, 1528, "فالشمس غير طالعة"), _SHAMS), (), ""),
    (6, 0, 1, 2, True,
     ((_M, 1526, "لكن الشمس غير طالعة"), (_M, 1527, "فالنهار ليس بموجود"), _MUSAWI), (),
     "يُنتج نقيضُ المقدَّم إذا كان التالي مساويًا"),
    (7, 0, 1, 3, True, ((_M, 1527, "لكن النهار موجود فالشمس طالعة"), _MUSAWI), (), ""),
    # القراءتان الأصوليّتان — موافقتان للنبهانيّ، مرساتان في المودَعَين
    (8, 1, 0, 0, True,
     ((_S, 10949, "وهذا قد يسمى مفهوم الموافقة"),
      (_S, 10938, "هذا من قبيل التنبيه بالأدنى على الأعلى"),
      (_S, 10931, "كفهم تحريم الشتم، والقتل، والضرب من قوله")),
     (("ج3", 559, "ويسمى فحوى الخطاب"), ("ج3", 560, "التنبيه بالأدنى على الأعلى"),
      ("ج3", 563, "مفهوم الموافقة من الدلالة الالتزامية")),
     "مفهوم الموافقة: الأخصُّ (التأفيف) يُنتج الأعمَّ (الإيذاء) — `akhass_chain`"),
    (9, 1, 1, 2, True,
     ((_S, 10952, "الاستدلال بتخصيص الشيء بالذكر على نفي الحكم عما عداه"),
      (_S, 10954, "وربما سمي هذا دليل الخطاب"), _MUSAWI),
     (("ج3", 567, "ويسمى دليل الخطاب"),
      ("ج3", 576, "ولا خلاف في عدم المشروط عند عدم الشرط اللغوي"),
      ("ج3", 577, "لزم من عدمه عدم المشروط")),
     "مفهوم المخالفة بالشرط: المساوي يُنتج نقيضَ المقدَّم — `licence_makes_mafhum`"),
    # منهجُ النبهانيّ في المنطق — به يُوسَم الصنفُ الأوّل رأيًا ثانيًا
    (10, 2, 0, 0, False, (),
     (("التفكير", 67, "أما البحث المنطقي فإنه ليس طريقة في التفكير"),
      ("التفكير", 72, "فيه قابلية الخداع"),
      ("التفكير", 73, "وأسلوب فيه قابلية الخداع والتضليل")),
     "«أسلوب من أساليب البحث المبنية على الطريقة العقلية» — لا مودَعَ واقعٍ"),
)


def _read(path: Path, sha: str) -> list[str]:
    raw = gzip.decompress(path.read_bytes())
    got = hashlib.sha256(raw).hexdigest()
    if got != sha:
        raise SystemExit(f"SOURCE_SHA_MISMATCH:{path.name}:{got}")
    return raw.decode("utf-8").split("\n")


def read_sources() -> dict[str, list[str]]:
    return {name: _read(path, sha) for name, (path, sha) in SOURCES.items()}


def verify(texts: dict[str, list[str]]) -> None:
    """كلُّ مرساةٍ في سطرها من مودَعها المسمّى؛ مراسي الغزاليّ من مودَعاته ومراسي النبهانيّ من العمود؛
    الخاناتُ الثماني كلُّها بلا تكرار؛ خانةُ المنطق لا مرساةَ لها في النبهانيّ (رأيٌ ثانٍ لا موافقة)؛
    والقراءةُ الأصوليّة مرساةٌ في المودَعَين معًا؛ والمنهجُ من النبهانيّ وحده."""

    if [r[0] for r in ROWS] != list(range(len(ROWS))):
        raise SystemExit("ROWS_NOT_NUMBERED")
    cells = [(r[2], r[3]) for r in ROWS if r[1] == 0]
    if sorted(cells) != [(d, f) for d in range(2) for f in range(4)]:
        raise SystemExit("CELLS_NOT_COVERING")
    for rid, kind, degree, form, _, ghazali, nabhani, _ in ROWS:
        if kind >= len(KINDS) or degree >= len(DEGREES) or form >= len(FORMS):
            raise SystemExit(f"BAD_KIND_OR_CELL:{rid}")
        for src, line, phrase in (*ghazali, *nabhani):
            if src not in texts:
                raise SystemExit(f"UNKNOWN_SOURCE:{rid}:{src}")
            if phrase not in texts[src][line - 1]:
                raise SystemExit(f"PHRASE_NOT_IN_LINE:{rid}:{src}:{line}:{phrase}")
        if any(src not in GHAZALI for src, _, _ in ghazali):
            raise SystemExit(f"GHAZALI_ANCHOR_NOT_FROM_GHAZALI:{rid}")
        if any(src not in NABHANI for src, _, _ in nabhani):
            raise SystemExit(f"NABHANI_ANCHOR_NOT_FROM_SPINE:{rid}")
        if kind == 0 and (nabhani or not ghazali):
            raise SystemExit(f"LOGIC_CELL_IS_SECOND_OPINION:{rid}")
        if kind == 1 and not (nabhani and ghazali):
            raise SystemExit(f"USUL_READING_NOT_IN_BOTH:{rid}")
        if kind == 2 and (ghazali or not nabhani):
            raise SystemExit(f"MANHAJ_NOT_FROM_SPINE:{rid}")


def _lean_str(s: str) -> str:
    return '"' + s.replace("\\", "\\\\").replace('"', '\\"') + '"'


def _lean_anchors(anchors: tuple[Anchor, ...]) -> str:
    return "[" + ", ".join(f"({_lean_str(s)}, {n}, {_lean_str(p)})" for s, n, p in anchors) + "]"


def render_lean() -> str:
    shas = "، ".join(f"{name} `{sha}`" for name, (_, sha) in SOURCES.items())
    out = [
        "import Slge.Ghazali", "",
        "/-! صورُ الشرطيّ المتّصل عند الغزاليّ بأسطرها من المختومات؛ مولَّدٌ بـ`tools/deposit_ghazali.py`",
        f"(SHA-256 {shas})، لا يُحرَّر باليد.",
        "الصفُّ: (الرقم، الصنف 0 خانةُ منطق/1 قراءةٌ أصوليّة/2 منهجُ النبهانيّ، الدرجة، الصورة، هل تُنتج، "
        "مراسي الغزاليّ، مراسي النبهانيّ). -/", "",
        "namespace Slge.GhazaliTable", "",
        "structure Row where",
        "  id : Nat",
        "  kind : Nat",
        "  degree : Ghazali.Degree",
        "  form : Ghazali.Form",
        "  stated : Bool",
        "  ghazali : List (String × Nat × String)",
        "  nabhani : List (String × Nat × String)",
        "  deriving DecidableEq, Repr", "",
        "def rows : List Row := [",
    ]
    for rid, kind, degree, form, stated, ghazali, nabhani, _ in ROWS:
        out.append(f"  ⟨{rid}, {kind}, .{DEGREES[degree]}, .{FORMS[form]}, "
                   f"{'true' if stated else 'false'}, {_lean_anchors(ghazali)}, "
                   f"{_lean_anchors(nabhani)}⟩,")
    out[-1] = out[-1].rstrip(",")
    out += ["]", "", f"theorem rows_length : rows.length = {len(ROWS)} := rfl", "",
            "end Slge.GhazaliTable", ""]
    return "\n".join(out)


def render_py() -> str:
    out = [
        '"""صورُ الشرطيّ المتّصل عند الغزاليّ بأسطرها من المختومات؛ مولَّدٌ بـ`tools/deposit_ghazali.py`',
        "(SHA-256 " + "، ".join(f"{sha[:12]}…" for _, (_, sha) in SOURCES.items()) + ")؛",
        'لا يُحرَّر باليد."""', "",
        "from __future__ import annotations", "", "from typing import Final", "",
        "KINDS: Final[tuple[str, ...]] = (", *(f"    {k!r}," for k in KINDS), ")",
        f"DEGREES: Final[tuple[str, ...]] = {DEGREES!r}",
        f"FORMS: Final[tuple[str, ...]] = {FORMS!r}",
        f"NABHANI: Final[tuple[str, ...]] = {NABHANI!r}",
        f"GHAZALI: Final[tuple[str, ...]] = {GHAZALI!r}",
        "Anchor = tuple[str, int, str]",
        "Row = tuple[int, int, int, int, bool, tuple[Anchor, ...], tuple[Anchor, ...], str]",
        '"""(الرقم، الصنف، الدرجة، الصورة، هل تُنتج، مراسي الغزاليّ، مراسي النبهانيّ، ملاحظة)."""', "",
        "ROWS: Final[tuple[Row, ...]] = (",
    ]
    for rid, kind, degree, form, stated, ghazali, nabhani, note in ROWS:
        out.append(f"    ({rid}, {kind}, {degree}, {form}, {stated},")
        for anchors in (ghazali, nabhani):
            out.append("     (")
            out += [f"         {a!r}," for a in anchors]
            out.append("     ),")
        out.append(f"     {note!r}),")
    out += [")", ""]
    return "\n".join(out)


def main(argv: list[str]) -> int:
    verify(read_sources())
    lean, py = render_lean(), render_py()
    if "--check" in argv:
        ok = LEAN.read_text(encoding="utf-8") == lean and PY.read_text(encoding="utf-8") == py
        sys.stdout.write("جدولا الغزاليّ مطابقان للمختومات\n" if ok
                         else "جدولا الغزاليّ غيرُ مطابقين\n")
        return 0 if ok else 1
    LEAN.write_text(lean, encoding="utf-8")
    PY.write_text(py, encoding="utf-8")
    sys.stdout.write(f"كُتب جدولا الغزاليّ: {len(ROWS)} صفًّا\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
