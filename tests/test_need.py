"""قانونُ الحاجة المتبادلة (`A116.Hajah`، ADR ٢٢): c يحتاج v، وv تحتاج c، تحت «ا و ا و ا».

١. الشاهد (لا المرآة): جدولُ `lake exe a116-table need` (كلُّ سلسلةِ أدوارٍ بطول 1 … 8، 9,840
   سطرًا) يقابَل بمُقطِّع البوّابة `gate.licence.parse` — شيفرةٌ كُتبت قبل القانون ولم تُكتب منه —
   فالقانونُ يقبل السلسلةَ ⟺ يقطّعها المُقطِّعُ بلا قطعةٍ صادرة (`need_law_iff_parse`).
٢. الطفرة: قانونٌ يقبل المدَّ بعد المُغلِق (`MUTANT_MADD_AFTER_CLOSER`: c ثمّ v) يخالف الجدول.
٣. المدوّنة: كلُّ شهادةٍ جاهزةٍ على المصحف تحقّق القانونَ على أدوارها (`strict_need`)، وحالةُ الوراثة بعد كلّ
   كلمةٍ ثلاثةُ مواضع على الأكثر (`state_le_three`). وباليد: بَحْرْ تقضي حاجاتِها ولا تُرخَّص وصلًا.
"""

from __future__ import annotations

from pathlib import Path

from gate import Refusal, enter
from gate.licence import continue_licensed, kind_of, parse

ROOT = Path(__file__).resolve().parents[1]
TABLE = ROOT / "formal" / "a116" / "need.csv"
CORPUS = ROOT / "corpora" / "quran-simple-enhanced.txt"
NAME = {"CV": "cv", "V": "v", "C": "c"}


def _rows() -> list[tuple[list[str], bool, str]]:
    out = []
    for line in TABLE.open(encoding="utf-8"):
        key, law, state = line.rstrip("\n").split(",")
        out.append(([NAME[x] for x in key.split("-")], law == "true", state))
    return out


def test_lean_need_table_is_the_gate_parser() -> None:
    rows = _rows()
    assert len(rows) == sum(3**n for n in range(1, 9))
    for k, law, _ in rows:
        parsed = parse(k)
        assert law == (parsed is not None and parsed[0] == "none"), k
    assert sum(1 for _, law, _ in rows if law) == 810


def _mutant(k: list[str]) -> bool:
    """`MUTANT_MADD_AFTER_CLOSER`: ذيلٌ حتى ثلاثة بأيّ ترتيب."""

    if not k or k[0] != "cv":
        return False
    tail = 0
    for x in k:
        tail = 0 if x == "cv" else tail + 1
        if tail > 3:
            return False
    return True


def test_lean_table_rejects_named_mutant() -> None:
    rows = _rows()
    wrong = [k for k, law, _ in rows if _mutant(k) != law]
    assert wrong and ["cv", "c", "v"] in wrong


def test_every_corpus_certificate_meets_the_law() -> None:
    lean = {"-".join(k): (law, st) for k, law, st in _rows()}
    words = {w for w in CORPUS.read_text(encoding="utf-8").split() if w != "<sel>"}
    checked = 0
    for w in words:
        cert = enter(w.encode("utf-8"))
        if isinstance(cert, Refusal):
            continue
        k = kind_of(cert.atoms)
        if len(k) > 8:
            continue
        law, state = lean["-".join(k)]
        assert law, w
        assert state.count("-") <= 2  # ذيلٌ من ثلاثةٍ على الأكثر
        checked += 1
    assert checked > 10_000


def test_by_hand() -> None:
    # بَحْرْ: cv c c — حاجاتُها مقضيّة، ولا تُرخَّص إلّا وقفًا
    assert parse(["cv", "c", "c"]) == ("none", ["CVCC"])
    assert not continue_licensed(["cv", "c", "c"])
    # حَاجَّ: cv v c cv — المُغلِقُ بعد المدّ ابنُ الحاء
    assert parse(["cv", "v", "c", "cv"]) == ("none", ["CVVC", "CV"])
