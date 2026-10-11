"""الأوزانُ على الخانات بعدد الأصول (`A116.Wazn`، ADR ١٦): جدولُ `lake exe a116-table wazn`
(31 سطرًا مودَعًا) يقابَل بالبوّابة على كلمات المدوّنة المختومة.

١. المطابقة: لكلّ كلمةٍ في المصحف تسترجعها البوّابة (`gate.recover`) فعلًا من جذرٍ صحيح في صيغة
   3MS (الماضي والمبنيّ للمجهول) أو 2MS (الأمر) **وآخرُها بحركة تلك الصيغة** (فتحة / سكون)، ذرّاتُ
   شهادتها = نمطُ الوزن في جدول Lean ابتداءً بأصولها؛ ومقاطعُها (`gate.licence`) = عمودُ الوصل.
   وشرطُ الحركة الأخيرة لأنّ الاسترجاعَ يطبّع بحذف آخر علامة، فيقرأ «سَاحِرُ» أمرًا من فاعَلَ —
   والحركةُ الأخيرة هي ما ينتظر الحدّ. والجدولُ لم يُكتب من البوّابة: ترجمةُ Lean للقوالب
   (`Wazn.convert`)، فالتطابقُ شاهدٌ لا مرآة. والفجوةُ المسمّاة `VI_TA_IDGHAM_NOT_IN_TABLE`:
   مولِّدُ البوّابة يُدغم تاءَ تفاعَلَ (ادَّارَكَ) والجدولُ لا.
٢. الطفرة: نمطٌ يجعل حرفَ المدّ متحرّكًا (`MUTANT_MADD_VOWELLED`) يخالف البوّابة في فَاعَلَ.
٣. الدَّينُ المسمّى `WASL_LAM_ARTICLE_VS_ROOT` ظاهر: البوّابةُ تفتح همزةَ «الْتَقَى» (قاعدةُ لام
   الأداة).
"""

from __future__ import annotations

from pathlib import Path

from gate import Refusal, enter, recover
from gate.licence import kind_of, parse

ROOT = Path(__file__).resolve().parents[1]
TABLE = ROOT / "formal" / "a116" / "wazn.csv"
CORPUS = ROOT / "corpora" / "quran-simple-enhanced.txt"

# ترتيبُ القوالب كما في `A116.Ishtiqaq.soundTemplates` — مكتوبٌ باليد من ملفّ Lean.
LABELS = (
    [("PAST", f) for f in ("I-a", "I-i", "I-u", "II", "III", "IV", "V", "VI", "VII", "VIII", "X")]
    + [("PASSIVE", f) for f in ("I", "II", "III", "IV", "V", "VI", "VII", "VIII", "X")]
    + [("IMPERATIVE", f) for f in ("I-a", "I-i", "I-u", "II", "III", "IV", "V", "VI", "VII",
                                   "VIII", "X")]
)
WEAK = set("اويءىآأإؤئ")
IFTAAL = set("صضطظدذزوي")


def _rows() -> dict[tuple[str, str], tuple[list[str], str, str]]:
    out = {}
    for line in TABLE.open(encoding="utf-8"):
        i, pattern, cont, pause = line.rstrip("\n").split(",")
        out[LABELS[int(i)]] = (pattern.split(" "), cont, pause)
    return out


def _fill(pattern: list[str], root: str) -> tuple[str, ...]:
    return tuple(root[int(t[0]) - 1] + t[1:] if t[0] in "123" else t for t in pattern)


def _sound(root: str, form: str) -> bool:
    return (len(root) == 3 and not WEAK & set(root) and root[1] != root[2] and root[0] != "ل"
            and not (form == "VIII" and root[0] in IFTAAL))


def _corpus_matches() -> list[tuple[str, tuple[str, ...], tuple[str, ...], str, str]]:
    rows = _rows()
    words = {w for w in CORPUS.read_text(encoding="utf-8").split() if w != "<sel>"}
    out = []
    for w in sorted(words):
        cert = enter(w.encode("utf-8"))
        if isinstance(cert, Refusal):
            continue
        outcome, readings = recover(cert)
        for root, kind, form, person in readings:
            want_person = "2MS" if kind == "IMPERATIVE" else "3MS"
            if person != want_person or (kind, form) not in rows or not _sound(root, form):
                continue
            pattern, cont, _ = rows[(kind, form)]
            if cert.atoms[-1][1:] != ("ْ" if kind == "IMPERATIVE" else "َ"):
                continue
            out.append((w, cert.atoms, _fill(pattern, root), cont, kind + "/" + form))
    return out


def test_lean_wazn_table_matches_gate_on_sealed_corpus() -> None:
    rows = _rows()
    assert len(rows) == 31
    found = _corpus_matches()
    gap = ("ءِ", "دْ", "دَ", "اْ", "رَ", "كَ")  # ادَّارَكَ
    mismatches = [(a, lab) for _, a, e, _, lab in found if a != e]
    # الفجوةُ المسمّاة وحدَها: تفاعَلَ بتاءٍ مدغمة (البوّابةُ تولّدها والجدولُ لا)
    assert mismatches == [(gap, "PAST/VI")]
    found = [x for x in found if x[1] != gap]
    # المقاطعُ: تقطيعُ البوّابة لذرّات الكلمة = عمودُ الوصل في جدول Lean
    for w, atoms, _, cont, _ in found:
        parsed = parse(kind_of(atoms))
        assert parsed is not None and "-".join(parsed[1]) == cont, w
    # أوزانٌ كثيرةٌ مشهودة، لا وزنٌ واحد (العددُ مقيسٌ على المختوم في CLAIMS لا هنا)
    assert len({lab for *_, lab in found}) >= 10


def test_lean_table_rejects_madd_vowelled_mutant() -> None:
    """`MUTANT_MADD_VOWELLED`: فَاعَلَ بألفٍ متحرّكة لا يطابق شهادةَ «قَاتَلَ»."""

    pattern, _, _ = _rows()[("PAST", "III")]
    cert = enter("قَاتَلَ".encode())
    assert not isinstance(cert, Refusal)
    assert cert.atoms == _fill(pattern, "قتل")
    mutant = [t.replace("اْ", "اَ") for t in pattern]
    assert cert.atoms != _fill(mutant, "قتل")


def test_by_hand_and_boundary_columns() -> None:
    rows = _rows()
    # كَتَبَ: ثلاثةُ مقاطع وصلًا، ووقفًا كَ تَبْ — حسابٌ باليد
    assert rows[("PAST", "I-a")][1:] == ("CV-CV-CV", "CV-CVC")
    # اسْتَفْعَلَ ابتداءً: ءِسْ تَفْ عَ لَ — أربعةُ مقاطع بثلاثة أصول
    assert rows[("PAST", "X")][1] == "CVC-CVC-CV-CV"
    # الأمرُ مبنيٌّ على السكون: الوقفُ لا يغيّره
    assert all(c == p for (k, _), (_, c, p) in rows.items() if k == "IMPERATIVE")


def test_wasl_lam_debt_is_visible() -> None:
    cert = enter("الْتَقَى".encode())
    assert not isinstance(cert, Refusal)
    assert cert.atoms[:3] == ("ءَ", "لْ", "تَ")  # لامُ الأصل أُخذت بقاعدة لام الأداة
