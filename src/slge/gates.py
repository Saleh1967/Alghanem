"""البوّاباتُ المتتابعة: شهادةُ الغانم تصعد SLGE ثمانيَ بوّاباتٍ، ولا بوّابةَ فوق مرفوضة — مرآةُ
`Grant.Ladder`.

المدخلُ ذرّاتُ شهادةٍ من بوّابة الغانم (لا نصّ)، والمخرجُ ذرّاتٌ بعينها إلى `gate.exit`. بينهما سُلَّمٌ من
بوّاباتٍ كلُّ واحدةٍ `enter(x) → Pass | Refusal` باسمه، تتابعُها ترتيبُ الترخيص التدريجيّ، ومرورُ بوّابةٍ يشترط
مرورَ ما تحتها (`Slge.Grant.ladder_implies_base`، `no_grant_of_refused` — مبرهَنان على السُّلَّم المجرّد).

الحاكمة (رفضُها يوقف الصعود): ١ الخانة (ذرّات ← خانات؛ `NOT_A_116_ATOM`)، ٢ الترخيص (ثلاثيٌّ وصلًا؛
`NOT_CONTINUE_LICENSED`)، ٣ العدد (ثنائيٌّ ← `fold`؛ والثلاثيُّ فقط `TERNARY_ONLY_NO_NUMBER`: عددُه في
شهادته).
القارئة (قراءةٌ أو «لا قراءة» باسمه، ولا ترفض): ٤ الجداول الحاصرة، ٥ الجذع (تسويةُ الآخر وفصلُ الزوائد
`jidh`)، ٦ الصرف على الصورة كما هي (`wad.senses`)، ٧ الإعراب (`tawabi.case_class`)، ٨ الجواب (القرّاء
بسياقهم). فما لا يُقرأ ليس خطأً بل حدًّا معلَنًا. الجدولُ الكامل في
`ARCHITECTURE.md` (ADR ٦). `climb(atoms)` يعيد أثرَ الصعود كلَّه.
"""

from __future__ import annotations

from collections.abc import Callable, Sequence
from dataclasses import dataclass
from typing import Any, Final

from slge.categories import PRONOUNS
from slge.cells import Cell, fold, licensed
from slge.entry import from_atoms, to_atoms
from slge.huruf import by_cells
from slge.ilal import RULES
from slge.ishara import FORMS as ISHARA
from slge.jidh import jidh
from slge.jiha import sigha
from slge.kulli import kulli
from slge.madd import continue_licensed, madd
from slge.maqayis import attested, rank
from slge.marifa import MAWSUL
from slge.tawabi import case_class
from slge.wad import senses, wad

__all__ = ["LADDER", "Gate", "Pass", "Refusal", "climb", "exit_atoms"]

Word = tuple[Cell, ...]


@dataclass(frozen=True, slots=True)
class Pass:
    """مرورٌ من بوّابة: اسمُها، وما أخرجته (قراءةٌ أو خانات)، وبقيّتُها المعلَنة."""

    gate: str
    out: Any
    residual: str = ""


@dataclass(frozen=True, slots=True)
class Refusal:
    """رفضٌ باسمه من بوّابةٍ بعينها."""

    gate: str
    code: str


@dataclass(frozen=True, slots=True)
class Gate:
    name: str
    governing: bool
    enter: Callable[[Word, dict[str, Any]], Pass | Refusal]


def _g1(w: Word, ctx: dict[str, Any]) -> Pass | Refusal:
    try:
        cells = from_atoms(ctx["atoms"])
    except ValueError as e:
        return Refusal("الخانة", str(e).split(":")[0])
    return Pass("الخانة", cells)


def _g2(w: Word, ctx: dict[str, Any]) -> Pass | Refusal:
    if not continue_licensed(w):
        return Refusal("الترخيص", "NOT_CONTINUE_LICENSED")
    return Pass("الترخيص", w, "" if licensed(w) else "ثلاثيٌّ فقط: مدٌّ لازم")


def _g3(w: Word, ctx: dict[str, Any]) -> Pass | Refusal:
    if not licensed(w):
        return Refusal("العدد", "TERNARY_ONLY_NO_NUMBER")
    return Pass("العدد", fold(w))


def _g4(w: Word, ctx: dict[str, Any]) -> Pass | Refusal:
    if w in PRONOUNS:
        return Pass("الجداول", "ضمير")
    if any(f.cells == w for f in ISHARA):
        return Pass("الجداول", "إشارة")
    if w in MAWSUL.values():
        return Pass("الجداول", "موصول")
    if by_cells(w):
        return Pass("الجداول", "أداة")
    return Pass("الجداول", None, "ليست مجدوَلة")


def _g5(w: Word, ctx: dict[str, Any]) -> Pass | Refusal:
    rs = rank(jidh(w))  # المشهودُ في المقاييس أوّلًا؛ لا قراءةَ تسقط (`mem_rank`، `length_rank`)
    used = sorted({rule for r in rs for rule, _ in r.ilal}, key=RULES.index)
    notes = ["الإعلال: " + "، ".join(used)] if used else []
    seen = sum(attested(r) for r in rs)
    if rs and seen < len(rs):
        notes.append(f"المقاييس: {seen} من {len(rs)} مشهودة")
    return Pass("الجذع", rs, "؛ ".join(notes) if rs else "لا قطعَ من الجداول يضع جذعًا على قالب")


def _g6(w: Word, ctx: dict[str, Any]) -> Pass | Refusal:
    s = senses(w)
    return Pass("الصرف", s, "" if s else "الصورةُ كما هي على غير قالب؛ انظر قراءاتِ الجذع")


def _g7(w: Word, ctx: dict[str, Any]) -> Pass | Refusal:
    c = case_class(w)
    return Pass("الإعراب", c, "" if c != "لا تقرؤه الخانة" else "لا تقرؤه الخانة")


def _g8(w: Word, ctx: dict[str, Any]) -> Pass | Refusal:
    nxt: Word = ctx.get("next", ())
    return Pass("الجواب", {"الكليّ": kulli(w), "الوضع": wad(w), "الصيغة": sigha(w),
                          "المدود": madd(w, nxt, bool(ctx.get("pause", False)))})


LADDER: Final[tuple[Gate, ...]] = (
    Gate("الخانة", True, _g1), Gate("الترخيص", True, _g2), Gate("العدد", True, _g3),
    Gate("الجداول", False, _g4), Gate("الجذع", False, _g5), Gate("الصرف", False, _g6),
    Gate("الإعراب", False, _g7), Gate("الجواب", False, _g8),
)


def climb(atoms: Sequence[str], nxt: Word = (), pause: bool = False) -> tuple[Pass | Refusal, ...]:
    """يصعد السُّلَّمَ من ذرّات الشهادة ويقف عند أوّل رفضٍ حاكم؛ البوّاباتُ القارئة لا توقف."""

    ctx: dict[str, Any] = {"atoms": tuple(atoms), "next": nxt, "pause": pause}
    trace: list[Pass | Refusal] = []
    w: Word = ()
    for g in LADDER:
        r = g.enter(w, ctx)
        trace.append(r)
        if isinstance(r, Refusal):
            if g.governing:
                break
            continue
        if g.name == "الخانة":
            w = r.out
        if g.name == "العدد":
            continue
    return tuple(trace)


def exit_atoms(trace: Sequence[Pass | Refusal]) -> tuple[str, ...] | None:
    """المخرج: ذرّاتُ الخانة بعينها (`to_atoms`) إن مرّت بوّابةُ الخانة، وإلّا لا شيء."""

    first = trace[0] if trace else None
    if isinstance(first, Pass) and first.gate == "الخانة":
        return to_atoms(first.out)
    return None


def _check() -> None:
    t = climb(("كَ", "تَ", "بَ"))
    assert [x.gate for x in t] == [g.name for g in LADDER] and exit_atoms(t) == ("كَ", "تَ", "بَ")
    assert isinstance(t[2], Pass) and t[2].out == fold(from_atoms(("كَ", "تَ", "بَ")))
    bad = climb(("كَ", "xx"))
    assert bad == (Refusal("الخانة", "NOT_A_116_ATOM"),) and exit_atoms(bad) is None
    tern = climb(("حَ", "اْ", "جْ", "جَ"))  # حَاجَّ: ثلاثيٌّ فقط — يمرّ الترخيصَ ويُرفض في العدد باسمه
    assert isinstance(tern[1], Pass) and tern[1].residual.startswith("ثلاثيٌّ")
    assert tern[2] == Refusal("العدد", "TERNARY_ONLY_NO_NUMBER") and len(tern) == 3
    unl = climb(("كْ", "تَ"))
    assert unl[1] == Refusal("الترخيص", "NOT_CONTINUE_LICENSED") and len(unl) == 2


_check()
