"""وسمُ الأجناس بقسمة النبهانيّ الخماسيّة «باعتبار المدلول وحده» — جدولٌ بتوقيع المالك (ADR ٣٥).

ج3 409 (المختوم): «ينقسم اللفظ باعتبار المدلول وحده إلى خمسة أقسام: أحدها أن يكون مدلول اللفظ معنى،
والثاني أن يكون لفظاً مفرداً مستعملاً، والثالث … مفرداً مهملاً، والرابع … مركباً مستعملاً، والخامس
… مركباً مهملاً». والقسمةُ مودَعةٌ أصلًا (`Slge.Nabhani.Madlul`، `nabhani.MADLUL`). وأجناسُ مودَع
المعلومات السابقة (`ajnas_table.GENERA`، 73 = عقدُ المستوى الأوّل من المخصّص) فيها كتبُ أشياء
(«كتاب خلق الإنسان») وكتبُ ألفاظٍ وأبوابٌ نحويّة («باب الممدود») وعلاماتُ أجزاء («السفر السادس»).
فالركنُ 4 (الأجناس — المعلوماتُ السابقة، «حقائق الأشياء وخواصها» ج3 395؛ «الموضوع للحقيقة الذهنية…
كالفرس والإنسان والسواد» ج3 406) لا يُحكم به إلّا بجنسٍ مدلولُه **معنى**.

تعيينُ القسم لكلّ جنسٍ حكمٌ للمالك لا للآلة: هذه الأداةُ تكتب إطارًا
(`tests/data/owner-ajnas-madlul.json`) بصفٍّ لكلّ جنس — الكتاب وعنوانه (ثابتان من الجدول)،
و`proposal` **رأيُ الوكيل** بقاعدةٍ معلَنة (`propose`) لا تقرؤه شيفرة، و`madlul` فارغٌ يملؤه المالك
بأحد الأقسام الخمسة بلفظها أو «ليس جنسًا» — ثمّ يوقّع (`signed_by`). وما لم يوقَّع فلا وسمَ لأحد
(`signed = false`، كلُّ الوسوم `none`). ويولّد من الإطار `formal/Slge/MadlulTable.lean`
و`src/slge/madlul_table.py`؛ وبـ`--check` يطابق الثابتَ والاقتراحَ والجدولين بما يولَّد الآن، ولا
يمسّ ما ملأه المالك.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any

from slge.ajnas_table import GENERA
from slge.nabhani import MADLUL

ROOT = Path(__file__).resolve().parent.parent
FRAME = ROOT / "tests" / "data" / "owner-ajnas-madlul.json"
LEAN = ROOT / "formal" / "Slge" / "MadlulTable.lean"
PY = ROOT / "src" / "slge" / "madlul_table.py"
NOT_GENUS = "ليس جنسًا"
VALUES = (*MADLUL, NOT_GENUS)
LEAN_CTOR = ("mana", "mufradMustamal", "mufradMuhmal", "murakkabMustamal", "muhmalMurakkab")
LAW = ("ج3 409: «ينقسم اللفظ باعتبار المدلول وحده إلى خمسة أقسام»؛ الركنُ 4 (الأجناس) لا يُحكم به "
       "إلّا بجنسٍ مدلولُه معنى (ج3 395، 406)؛ وما مدلولُه لفظٌ يبقى شاهدًا للدالّ لا للمعلومات السابقة")


def propose(book: int, title: str) -> str:
    """رأيُ الوكيل (قاعدةٌ معلَنة لا تقرؤها شيفرة): علاماتُ الأجزاء ليست أجناسًا؛ ما قبل «كتاب
    المكنيات والمبنيات والمثنيات» (1410) كتبُ أشياء فمدلولُها معنى؛ وما بعده كتبُ ألفاظٍ وأبوابٌ
    نحويّة فمدلولُها لفظٌ مفردٌ مستعمل."""

    if title in ("المقدمة", "المخصص") or title.startswith("السفر"):
        return NOT_GENUS
    return MADLUL[0] if book < 1410 else MADLUL[1]


def fresh() -> dict[str, Any]:
    return {"signed_by": None, "signed_on": None, "law": LAW, "values": list(VALUES),
            "rows": [{"book": b, "title": t, "proposal": propose(b, t), "madlul": None}
                     for b, t, _, _ in GENERA]}


def read_frame() -> dict[str, Any]:
    d: dict[str, Any] = json.loads(FRAME.read_text(encoding="utf-8"))
    return d


def verify(d: dict[str, Any]) -> None:
    """الثابتُ من الجدول بعينه، والاقتراحُ بقاعدته، والقيمُ من الستّ لا غير؛ والموقَّعُ تامٌّ لا فراغَ فيه."""

    want = fresh()["rows"]
    got = [{k: r.get(k) for k in ("book", "title", "proposal")} for r in d["rows"]]
    if got != [{k: r[k] for k in ("book", "title", "proposal")} for r in want]:
        raise SystemExit("FRAME_DRIFTED_FROM_GENERA")
    if d.get("values") != list(VALUES):
        raise SystemExit("VALUES_ARE_NOT_NABHANI_409")
    for r in d["rows"]:
        if r["madlul"] is not None and r["madlul"] not in VALUES:
            raise SystemExit(f"VALUE_NOT_IN_409:{r['book']}:{r['madlul']}")
    if d.get("signed_by") and any(r["madlul"] is None for r in d["rows"]):
        raise SystemExit("SIGNED_FRAME_HAS_EMPTY_ROW")


def tags(d: dict[str, Any]) -> list[tuple[int, str | None]]:
    """الوسومُ المستهلَكة: لا شيء قبل التوقيع؛ وبعده قسمُ المالك («ليس جنسًا» = لا قسم)."""

    signed = bool(d.get("signed_by"))
    out: list[tuple[int, str | None]] = []
    for r in d["rows"]:
        m = r["madlul"] if signed else None
        out.append((r["book"], None if m in (None, NOT_GENUS) else m))
    return out


def render_lean(d: dict[str, Any]) -> str:
    ts = tags(d)
    rows = [f"  ({b}, {'none' if m is None else 'some .' + LEAN_CTOR[MADLUL.index(m)]})"
            for b, m in ts]
    return "\n".join([
        "import Slge.Nabhani", "",
        "/-! وسمُ الأجناس بقسمة النبهانيّ «باعتبار المدلول وحده» (ج3 409) — مولَّدٌ",
        "بـ`tools/deposit_madlul.py` من إطار المالك `tests/data/owner-ajnas-madlul.json`؛",
        "لا يُحرَّر باليد. `signed = false` = لم يُوقَّع:",
        "كلُّ الوسوم `none`. الصفُّ: (الكتاب، القسم أو `none` — لم يُوقَّع أو «ليس جنسًا»). -/", "",
        "namespace Slge.MadlulTable", "",
        f"def signed : Bool := {'true' if d.get('signed_by') else 'false'}", "",
        "def tags : List (Nat × Option Nabhani.Madlul) := [",
        ",\n".join(rows), "]", "",
        f"theorem tags_length : tags.length = {len(ts)} := by rfl", "",
        "/-- لا وسمَ قبل التوقيع. -/",
        "theorem unsigned_none : signed = false → tags.all (·.2.isNone) = true := by decide", "",
        "end Slge.MadlulTable", "",
    ])


def render_py(d: dict[str, Any]) -> str:
    ts = tags(d)
    return "\n".join([
        '"""وسمُ الأجناس بقسمة النبهانيّ «باعتبار المدلول وحده» (ج3 409) — مولَّدٌ',
        'بـ`tools/deposit_madlul.py`',
        'من إطار المالك؛ لا يُحرَّر باليد. `SIGNED = False`: لا وسمَ قبل التوقيع."""', "",
        "from __future__ import annotations", "", "from typing import Final", "",
        f"SIGNED: Final[bool] = {bool(d.get('signed_by'))}",
        f"SIGNED_BY: Final[str | None] = {d.get('signed_by')!r}",
        "TAGS: Final[dict[int, str | None]] = {",
        *(f"    {b}: {m!r}," for b, m in ts), "}",
        "PROPOSALS: Final[dict[int, str]] = {",
        *(f"    {r['book']}: {r['proposal']!r}," for r in d["rows"]), "}",
        '"""رأيُ الوكيل للعرض على المالك وحده؛ لا يستهلكه الحكم."""', "",
    ])


def main(argv: list[str]) -> int:
    if not FRAME.exists():
        if "--check" in argv:
            sys.stderr.write("FRAME_MISSING\n")
            return 1
        FRAME.write_text(json.dumps(fresh(), ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    d = read_frame()
    verify(d)
    lean, py = render_lean(d), render_py(d)
    if "--check" in argv:
        ok = LEAN.read_text(encoding="utf-8") == lean and PY.read_text(encoding="utf-8") == py
        n = sum(1 for r in d["rows"] if r["madlul"] is not None)
        sys.stdout.write(f"وسمُ الأجناس مطابق (موقَّع: {bool(d.get('signed_by'))}، مملوء {n} من "
                         f"{len(d['rows'])})\n" if ok else "وسمُ الأجناس غيرُ مطابق\n")
        return 0 if ok else 1
    LEAN.write_text(lean, encoding="utf-8")
    PY.write_text(py, encoding="utf-8")
    sys.stdout.write(f"كُتب وسمُ الأجناس: {len(d['rows'])} صفًّا، موقَّع: {bool(d.get('signed_by'))}\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
