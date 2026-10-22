"""الاكتسابُ بالأمثلة المضادّة وتراكمُه (ADR ١٢٣).

* **المتعلّم** يعدّد برامجَ لغةٍ معلَنة: لغةُ `Ibara` في `A116/Iktisab.lean` (متغيّرات، صفر، ‎∧ ∨ ⊕‎)
  ومعها نداءُ ما في المكتبة، وهو في Lean تعويضٌ (`subst`). الترتيبُ بالحجم (عددُ العقد)
  ثمّ بترتيبٍ ثابتٍ معلَن.
* **المعلّم** (`Teacher`) يحمل المواصفةَ وحدَه ويُخفي عمودَها، مكتوبةً بغير لغة المتعلّم:
  الناقصُ فرقُ مجموعتين، والبتُّ «الأوّلُ المعلومُ يغلب» على قيمٍ ثلاثيّة مفكوكة.
  يُسأل عن مرشَّحٍ فيردّ «ثبت» أو أوّلَ صفٍّ صالحٍ يخالفه.
* **الحكمُ على الصفوف** جدولُ بتٍّ واحد: اللغةُ نقطيّة، فما صدق على كلّ صفٍّ صدق على كلّ عرض —
  مبرهَنٌ في Lean (`Iktisab.nuqati`، `Iktisab.min_jadwal`)، وعقودُ المكتسَب في `A116/IktisabAqd.lean`.
* **التراكم:** المرحلةُ الأولى تكتسب `naqis` وتحفظه في `docs/iktisab/library.json`؛
  والثانيةُ تقرأ المكتبةَ من الملفّ لا من الذاكرة، وتحلّ ثلاثَ مهامّ مرّتين —
  بلا المكتبة وبها — بالميزانية نفسها.

المخرجات: `docs/iktisab/library.json`، `docs/iktisab/result.json`،
`formal/a116/A116/IktisabData.lean`.
`--check` يعيد التوليدَ ويقارن بالبايت.
"""

from __future__ import annotations

import json
import sys
from collections.abc import Callable, Iterator
from functools import cache
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LIBRARY = ROOT / "docs" / "iktisab" / "library.json"
RESULT = ROOT / "docs" / "iktisab" / "result.json"
DATA = ROOT / "formal" / "a116" / "A116" / "IktisabData.lean"
MAX_SIZE = 7
"""الميزانية: أكبرُ حجمٍ يُعدّ (عددُ العقد)، واحدةٌ للمرحلتين وللمقارنتين."""

Expr = tuple  # ("v", i) | ("0",) | (op, a, b) | ("lib", name, a, b)
OPS = ("and", "or", "xor")

# ---------------------------------------------------------------- المعلّم: مواصفاتٌ بغير لغة المتعلّم


def _q(k: bool, v: bool) -> bool | None:
    """فكُّ البتّتين إلى قيمةٍ ثلاثيّة (`TawrithBit.decQ`): غيرُ المعلوم لا قيمة له."""
    return v if k else None


def spec_naqis(row: tuple[bool, ...]) -> bool:
    """الناقصُ موضعًا: المطلوبُ R في هذا الموضع، والموجودُ P ليس فيه — ‎i ∈ R \\ P‎."""
    required = {0} if row[0] else set()
    present = {0} if row[1] else set()
    return 0 in required - present


def spec_batt(row: tuple[bool, ...]) -> tuple[bool, bool]:
    """البتُّ: ما بتّه الأوّلُ يبقى وإلّا فالثاني (`TawrithBit.batt`)، ثمّ يُرمَّز (معلوم، قيمة)."""
    a, f = _q(row[0], row[1]), _q(row[2], row[3])
    out = a if a is not None else f
    return (out is not None, bool(out))


def spec_taarud(row: tuple[bool, ...]) -> bool:
    """التعارض: كلاهما معلوم وقيمتاهما مختلفتان."""
    a, f = _q(row[0], row[1]), _q(row[2], row[3])
    return a is not None and f is not None and a != f


def salih_pairs(row: tuple[bool, ...]) -> bool:
    """الصالح (`TawrithBit.salih`): الصادقُ داخلَ المعلوم، لكلّ زوج."""
    return all(row[i] or not row[i + 1] for i in range(0, len(row), 2))


Row = tuple[bool, ...]
TASKS: dict[str, tuple[int, Callable[[Row], bool], Callable[[Row], bool]]] = {
    "naqis": (2, spec_naqis, lambda _r: True),
    "batt_qima": (4, lambda r: spec_batt(r)[1], salih_pairs),
    "batt_maalum": (4, lambda r: spec_batt(r)[0], salih_pairs),
    "taarud": (4, spec_taarud, salih_pairs),
}
"""المهمّة: (عددُ المتغيّرات، المواصفة، شرطُ الصفّ). المتغيّراتُ في مهامّ الأزواج ‎K₁ V₁ K₂ V₂‎."""

# ---------------------------------------------------------------- المتعلّم: لغةٌ معلَنة وتعدادٌ بالحجم


def rows(k: int) -> list[tuple[bool, ...]]:
    """الصفوفُ بترتيبٍ ثابت: المتغيّرُ i هو البتُّ i من رقم الصفّ."""
    return [tuple(bool((r >> i) & 1) for i in range(k)) for r in range(2 ** k)]


@cache
def var_columns(k: int) -> tuple[int, ...]:
    return tuple(sum(1 << r for r, row in enumerate(rows(k)) if row[i]) for i in range(k))


def column(e: Expr, k: int, lib: dict[str, Expr]) -> int:
    """قيمةُ البرنامج على الصفوف كلّها عمودًا واحدًا (البتُّ r = قيمتُه على الصفّ r)."""
    tag = e[0]
    if tag == "v":
        return var_columns(k)[e[1]]
    if tag == "0":
        return 0
    if tag == "lib":
        return _apply(lib[e[1]], column(e[2], k, lib), column(e[3], k, lib))
    a, b = column(e[1], k, lib), column(e[2], k, lib)
    return {"and": a & b, "or": a | b, "xor": a ^ b}[tag]


def _apply(body: Expr, a: int, b: int) -> int:
    """نداءُ المكتبة: جسمُ الإجراء على متغيّرين، يُقيَّم بعمودَي وسيطيه."""
    tag = body[0]
    if tag == "v":
        return (a, b)[body[1]]
    if tag == "0":
        return 0
    x, y = _apply(body[1], a, b), _apply(body[2], a, b)
    return {"and": x & y, "or": x | y, "xor": x ^ y}[tag]


def enumerate_exprs(k: int, max_size: int, lib_names: tuple[str, ...]) -> Iterator[Expr]:
    @cache
    def of_size(s: int) -> tuple[Expr, ...]:
        if s == 1:
            return tuple([("v", i) for i in range(k)] + [("0",)])
        out: list[Expr] = []
        heads = [(op, False) for op in OPS] + [(n, True) for n in lib_names]
        for head, is_lib in heads:
            for left in range(1, s - 1):
                for a in of_size(left):
                    for b in of_size(s - 1 - left):
                        out.append(("lib", head, a, b) if is_lib else (head, a, b))
        return tuple(out)

    for s in range(1, max_size + 1):
        yield from of_size(s)


def size(e: Expr) -> int:
    if e[0] in ("v", "0"):
        return 1
    return 1 + size(e[-2]) + size(e[-1])


# ---------------------------------------------------------------- حلقةُ الاكتساب


class Teacher:
    """المعلّم: يحمل المواصفةَ ويُسأل عن عمود مرشَّح، فيردّ `None` («ثبت») أو رقمَ أوّلِ صفٍّ صالحٍ يخالفه.

    العمودُ الهدف مخفيٌّ فيه؛ والمتعلّمُ لا يرى منه إلّا ما يردّه."""

    def __init__(self, task: str) -> None:
        k, spec, valid = TASKS[task]
        table = rows(k)
        self._target = sum(1 << r for r, row in enumerate(table) if valid(row) and spec(row))
        self._valid = sum(1 << r for r, row in enumerate(table) if valid(row))
        self._table = table

    def ask(self, col: int) -> int | None:
        bad = (col ^ self._target) & self._valid
        return None if not bad else (bad & -bad).bit_length() - 1

    def value(self, r: int) -> bool:
        """قيمةُ المواصفة على صفٍّ أعاده (يعرفها المتعلّمُ بعد المثال المضادّ)."""
        return bool((self._target >> r) & 1)


def acquire(task: str, lib: dict[str, Expr]) -> dict[str, object]:
    k = TASKS[task][0]
    teacher = Teacher(task)
    table = rows(k)
    ce: dict[int, bool] = {}  # الأمثلةُ المضادّة: الصفّ ← قيمتُه المطلوبة
    enumerated = queries = 0
    trace: list[dict[str, object]] = []
    for e in enumerate_exprs(k, MAX_SIZE, tuple(sorted(lib))):
        enumerated += 1
        col = column(e, k, lib)
        if any(bool((col >> r) & 1) != want for r, want in ce.items()):
            continue  # يخالف مثالًا مضادًّا سابقًا: يُستبعد بلا سؤال
        queries += 1
        r = teacher.ask(col)
        if r is None:
            return {"task": task, "found": render(e), "size": size(e), "enumerated": enumerated,
                    "teacher_queries": queries, "counterexamples": trace}
        ce[r] = teacher.value(r)
        trace.append({"candidate": render(e), "row": [int(x) for x in table[r]]})
    return {"task": task, "found": None, "size": None, "enumerated": enumerated,
            "teacher_queries": queries, "counterexamples": trace}


def render(e: Expr) -> str:
    """الصيغةُ النصّيّة للبرنامج (هي ما يُحفظ ويُقارن)."""
    if e[0] == "v":
        return f"v{e[1]}"
    if e[0] == "0":
        return "0"
    if e[0] == "lib":
        return f"{e[1]}({render(e[2])}, {render(e[3])})"
    return f"{e[0]}({render(e[1])}, {render(e[2])})"


def parse(s: str) -> Expr:
    s = s.strip()
    if s == "0":
        return ("0",)
    if s.startswith("v") and s[1:].isdigit():
        return ("v", int(s[1:]))
    head, rest = s.split("(", 1)
    body = rest[:-1]
    depth = 0
    for i, c in enumerate(body):
        depth += c == "("
        depth -= c == ")"
        if c == "," and depth == 0:
            a, b = parse(body[:i]), parse(body[i + 1:])
            return (head, a, b) if head in OPS else ("lib", head, a, b)
    raise ValueError(f"BAD_EXPR:{s}")


def lean(e: Expr) -> str:
    if e[0] == "v":
        return f"(.var {e[1]})"
    if e[0] == "0":
        return ".sifr"
    if e[0] == "lib":
        return f"(subst {e[1]} [{lean(e[2])}, {lean(e[3])}])"
    name = {"and": "wa", "or": "aw", "xor": "xor"}[e[0]]
    return f"(.{name} {lean(e[1])} {lean(e[2])})"


def dumps(x: object) -> str:
    return json.dumps(x, ensure_ascii=False, indent=2, sort_keys=True) + "\n"


def stage_one() -> tuple[dict[str, object], str]:
    """المرحلةُ الأولى: الاكتسابُ بلا مكتبة، ونصُّ المكتبة كما يُحفظ."""
    first = acquire("naqis", {})
    assert first["found"] is not None, "NAQIS_NOT_ACQUIRED"
    library = {"naqis": {"arity": 2, "body": first["found"],
                         "contract": "A116.IktisabAqd.naqis_aqd", "spec": "spec_naqis"}}
    return first, dumps(library)


def stage_two(library_path: Path, first: dict[str, object]) -> dict[Path, str]:
    """المرحلةُ الثانية: تقرأ المكتبةَ من ملفّها على القرص."""
    return _stage_two(library_path.read_text(encoding="utf-8"), first)


def _stage_two(library_text: str, first: dict[str, object]) -> dict[Path, str]:
    # المرحلةُ الثانية: المكتبةُ من نصّها المحفوظ، لا من متغيّرٍ في الذاكرة.
    lib = {n: parse(v["body"]) for n, v in json.loads(library_text).items()}
    tasks = ("batt_qima", "batt_maalum", "taarud")
    compare = {t: {"bila_maktaba": acquire(t, {}), "bil_maktaba": acquire(t, lib)} for t in tasks}
    result = {"adr": 123, "max_size": MAX_SIZE, "stage_one": first, "stage_two": compare}
    lines = [
        "import A116.Iktisab",
        "",
        "/-! مولَّدٌ بـ`tools/gen_iktisab.py` (ADR ١٢٣) — لا يُحرَّر باليد."
        " البرامجُ كما اكتسبها المتعلّم. -/",
        "",
        "namespace A116.IktisabData",
        "",
        "open A116.Iktisab",
        "",
        f"/-- `naqis`: اكتُسب من الأمثلة المضادّة: `{first['found']}`. -/",
        f"def naqis : Ibara := {lean(parse(str(first['found'])))}",
    ]
    for t in tasks:
        for mode in ("bila_maktaba", "bil_maktaba"):
            found = compare[t][mode]["found"]
            if found is not None:
                lines += ["", f"/-- `{t}` ({mode}): `{found}`. -/",
                          f"def {t}_{mode} : Ibara := {lean(parse(str(found)))}"]
    lines += ["", "end A116.IktisabData", ""]
    return {RESULT: dumps(result), DATA: "\n".join(lines)}


def _name(p: Path) -> str:
    return str(p.relative_to(ROOT)) if p.is_relative_to(ROOT) else str(p)


def main(argv: list[str]) -> int:
    first, library_text = stage_one()
    if "--check" in argv:
        # المكتبةُ على القرص ما تكتسبه المرحلةُ الأولى الآن، ثمّ تقرؤها المرحلةُ الثانية منه.
        out = {LIBRARY: library_text, **stage_two(LIBRARY, first)} if LIBRARY.exists() else {}
        drift = [_name(p) for p, text in out.items()
                 if not p.exists() or p.read_text(encoding="utf-8") != text] or (
                     [] if out else ["docs/iktisab/library.json"])
        if drift:
            print("IKTISAB_DRIFT: " + ", ".join(drift))
            return 1
        print("iktisab: ok")
        return 0
    LIBRARY.parent.mkdir(parents=True, exist_ok=True)
    LIBRARY.write_text(library_text, encoding="utf-8")
    out = stage_two(LIBRARY, first)
    for p, text in out.items():
        p.write_text(text, encoding="utf-8")
    two = json.loads(out[RESULT])["stage_two"]
    summary = {k: (v["bila_maktaba"]["found"], v["bila_maktaba"]["enumerated"],
                   v["bil_maktaba"]["found"], v["bil_maktaba"]["enumerated"])
               for k, v in two.items()}
    print(json.dumps(summary, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
