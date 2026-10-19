"""الألفُ لا تكون أبدًا إلّا ساكنة (`A116.Alif`): من شبكة الـ116 ثلاثٌ لا تُرخَّص —
(ا،فتح) (ا،ضم) (ا،كسر).

١. المطابقة: `gate.licence.licensable_atom` = `Alif.licensable` على جدول
   `lake exe a116-table licensable` (113 سطرًا مودَعًا يطابقه CI بايتًا بايتًا).
٢. الطفرة: مرآةٌ تعدّ الألفَ الساكنة أيضًا ممنوعةً يُسقطها الجدول (`MUTANT_ALIF_SUKUN_EXCLUDED`).
٣. البوّابة: كلُّ شهادةٍ جاهزة على المدوّنة المختومة ذرّاتُها من المرخَّص (113)، والألفُ بحركةِ
   نفسها تُرفض باسمها `BARE_ALIF_OWN_MARK_NOT_LICENSED` — التوقّعُ من الكتاب («لأن الألف لا تكون
   أبدا إلا ساكنة») لا من الشيفرة.
"""

from __future__ import annotations

from pathlib import Path

from gate import Refusal, enter, gate
from gate.bridge import A116
from gate.licence import ALIF_VOWELLED, licensable_atom

ROOT = Path(__file__).resolve().parents[1]
TABLE = ROOT / "formal" / "a116" / "licensable.csv"


def _rows() -> list[str]:
    return [line.rstrip("\n") for line in TABLE.open(encoding="utf-8") if line.strip()]


def test_python_mirror_matches_lean_licensable_table() -> None:
    rows = _rows()
    assert len(rows) == 113 and len(set(rows)) == 113
    assert set(rows) == {a for a in A116 if licensable_atom(a)}
    assert set(A116) - set(rows) == set(ALIF_VOWELLED) and len(A116) == 116


def test_lean_table_rejects_named_mutant() -> None:
    """`MUTANT_ALIF_SUKUN_EXCLUDED`: من عدّ كلَّ ألفٍ ممنوعةً خالف الجدولَ في سطر الألف الساكنة."""

    mutant = {a for a in A116 if a[0] != "ا"}
    assert mutant != set(_rows()) and "اْ" in set(_rows()) - mutant


def test_every_ready_certificate_uses_licensable_atoms_only() -> None:
    g = gate()
    seen: set[str] = set()
    for surface in g.book.domain:
        cert = g.enter(surface.encode("utf-8"))
        if isinstance(cert, Refusal):
            continue
        assert all(licensable_atom(a) for a in cert.atoms), surface
        seen.update(cert.atoms)
    assert seen.isdisjoint(ALIF_VOWELLED)
    # الألفُ بحركةِ نفسها: رفضٌ مسمًّى لا شهادة (رسمٌ ليس من المدوّنة فيُفحص بإسقاطه)
    r = enter("دَاَ".encode())
    assert isinstance(r, Refusal) and "BARE_ALIF_OWN_MARK_NOT_LICENSED" in r.reasons
