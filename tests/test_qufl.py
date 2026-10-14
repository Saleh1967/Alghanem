"""قفلُ الدالّ وحده (`A116.Qufl`، ADR ٦٢): جدولُ القفل بتوقّعاتٍ باليد، وشواهدُه عبر البوّابة ومرآة الترخيص
المستقلّة، وتجميدُ الواجهة.

١. `qufl.csv` (يطبعه Lean، ويطابقه CI): لكلّ درجةٍ 1–4 ستُّ وظائف قائمة والدلالةُ معلّقةٌ باسم الجسر —
   الصفوفُ مكتوبةٌ هنا باليد.
٢. شواهدُ القفل: كلماتُ المصحف المكتوبةُ باليد (كَتَبَ، وَعَدَ، قَالَ، رَمَى، أَخَذَ) تمرّ على `gate.enter`
   فتُقارن ذرّاتُها بصفّ الجدول؛ وما ليس في المجال المختوم (مَدَّ، دَحْرَجَ) يُحكم فيه بمرآة الترخيص
   المستقلّة (`gate.licence`) على ذرّات الجدول، لا بـLean.
٣. `INTERFACE_FROZEN`: توقيعاتُ `enter`/`exit`/`derive`/`recover`/`licence` وحقولُ الشهادة والرفض
   والسياق مكتوبةٌ هنا باليد (`FROZEN`)، و`gate.DAL_LOCK` اسمُ القفل؛ أيُّ تغييرٍ يُسقط هذا الاختبار
   حتى يُرفع الاسمُ بـADR.
الطفرات: `MUTANT_DALALA_QAIM`، `MUTANT_SIGNATURE_DRIFT`، `MUTANT_SAHIH_ONLY`.
"""

from __future__ import annotations

import dataclasses
import inspect
from pathlib import Path

import gate
from gate import Refusal, enter
from gate.licence import licence, strict_licensed, strict_pause_licensed

ROOT = Path(__file__).resolve().parents[1]
TABLE = ROOT / "formal" / "a116" / "qufl.csv"

FUNCTIONS = ("tarmiz", "imla", "sawt", "ishtiqaq", "sarf", "nahw", "dalala")
BRIDGE = "DALALA_AT_DAL_MADLUL_BRIDGE"


def _rows() -> list[list[str]]:
    return [ln.rstrip("\n").split(",") for ln in TABLE.open(encoding="utf-8")]


def test_lock_rows_by_hand() -> None:
    rows = [r for r in _rows() if r[0] == "row"]
    expected = [["row", str(d), w, "false" if w == "dalala" else "true",
                 BRIDGE if w == "dalala" else "-"] for d in (1, 2, 3, 4) for w in FUNCTIONS]
    assert rows == expected


def test_mutant_dalala_qaim_rejected() -> None:
    """`MUTANT_DALALA_QAIM`: دفترٌ يجعل الدلالةَ قائمةً بلا شاهدٍ لا يطابق الجدول."""

    rows = [r for r in _rows() if r[0] == "row"]
    mutant = [[*r[:3], "true", "-"] if r[2] == "dalala" else r for r in rows]
    assert mutant != rows and sum(r[3] == "true" for r in rows) == 24


# (كلمةُ المصحف باليد، ذرّاتُ الجدول باليد) — الصحيحُ والمثالُ والأجوفُ والناقصُ والمهموز
CORPUS_WITNESSES = [
    ("كَتَبَ", "كَ تَ بَ"), ("وَعَدَ", "وَ عَ دَ"), ("قَالَ", "قَ اْ لَ"), ("رَمَى", "رَ مَ اْ"),
    ("أَخَذَ", "ءَ خَ ذَ"),
]
OUTSIDE_DOMAIN = {"مَ دْ دَ", "دَ حْ رَ جَ"}  # المضعَّفُ والرباعيّ: ليسا في المصحف بهذه الصورة


def test_witnesses_through_the_gate_and_independent_licence() -> None:
    table = {r[1]: (r[2], r[3]) for r in _rows() if r[0] in ("madi", "rubai")}
    assert set(table) == {a for _, a in CORPUS_WITNESSES} | OUTSIDE_DOMAIN
    for word, atoms in CORPUS_WITNESSES:
        cert = enter(word.encode("utf-8"))
        assert not isinstance(cert, Refusal), word
        assert " ".join(cert.atoms) == atoms, word
    for atoms, (wasl, waqf) in table.items():
        a = atoms.split(" ")
        assert (wasl, waqf) == ("true", "true"), atoms
        assert strict_licensed(a) and licence(a) is not None, atoms
        assert strict_pause_licensed([*a[:-1], a[-1][0] + "ْ"]), atoms


def test_mutant_sahih_only_rejected() -> None:
    """`MUTANT_SAHIH_ONLY`: قفلٌ يقف عند الصحيح لا يبلغ قَالَ ولا رَمَى ولا مَدَّ."""

    weak = [a for a in (r[1] for r in _rows() if r[0] == "madi") if "اْ" in a or "دْ دَ" in a]
    assert len(weak) == 3


FROZEN = {
    "enter": "(data: 'bytes', context: 'Context | None' = None) -> 'Certificate | Refusal'",
    "exit": "(cert: 'Certificate') -> 'bytes'",
    "derive": "(root: 'str', before_object: 'bool' = False, ilhaq: 'bool' = False) "
              "-> 'dict[str, list[tuple[str, str, str]]]'",
    "recover": "(surface_or_cert: 'Certificate | str', peel: 'bool' = False) "
               "-> 'tuple[str, tuple[Reading, ...]]'",
    "licence": "(atoms: 'Sequence[str]') -> 'tuple[Lead, list[Syl]] | None'",
    "Certificate": "core:_Cert residue:tuple[Edit, ...] junction:str | None",
    "Refusal": "status:str reasons:tuple[str, ...]",
    "Context": "entry:str exit:str left:str profile:str",
}


def _surface() -> dict[str, str]:
    out = {name: str(inspect.signature(getattr(gate, name)))
           for name in ("enter", "exit", "derive", "recover")}
    out["licence"] = str(inspect.signature(licence))
    for cls in (gate.Certificate, gate.Refusal, gate.Context):
        out[cls.__name__] = " ".join(f"{f.name}:{f.type}" for f in dataclasses.fields(cls))
    return out


def test_interface_frozen() -> None:
    assert gate.DAL_LOCK == "dal-v1"
    assert _surface() == FROZEN


def test_mutant_signature_drift_caught() -> None:
    """`MUTANT_SIGNATURE_DRIFT`: معاملٌ جديد في `enter` يخالف المجمَّد."""

    drifted = dict(FROZEN, enter=FROZEN["enter"].replace("= None)",
                                                      "= None, strict: 'bool' = False)"))
    assert drifted != _surface()
