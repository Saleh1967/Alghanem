"""التصريفُ على الخانات (`A116.Tasrif`، ADR ٢٦): شاهدُ المصحف المختوم على جدول
Lean، مستقلٌّ عن Lean.

الجدولُ `formal/a116/tasrif.csv` يطبعه Lean (`lake exe a116-table tasrif`)
ويطابقه CI بايتًا بايتًا. والتوقّعُ هنا كلماتُ المصحف مكتوبةً باليد كما هي في
المدوّنة المختومة، تمرّ على البوّابة (`gate.enter`) فتُقارن ذرّاتُها بصفّ الجدول
— فلا رقمَ ولا ذرّةَ تحسبها الشيفرةُ المفحوصة. وما ليس في المصحف (يَقِي، قِ،
يَنْمُو…) يُكتب باليد من نصّ المالك ومن الكتاب المختوم (عِهْ، قِهْ: السطر
17497–17499). والطفراتُ ثلاث بأسمائها؛ والحكمُ فيها بمرآة الترخيص المستقلّة
(`gate.licence`) لا بـLean.
"""

from __future__ import annotations

from functools import cache
from pathlib import Path

from gate import Refusal, enter
from gate.licence import strict_licensed, strict_pause_licensed

ROOT = Path(__file__).resolve().parents[1]
TABLE = ROOT / "formal" / "a116" / "tasrif.csv"

Key = tuple[str, str, str, str, str, str]


@cache
def _rows() -> dict[Key, tuple[str, ...]]:
    out: dict[Key, tuple[str, ...]] = {}
    for line in TABLE.open(encoding="utf-8"):
        root, kind, bab, v, p, m, atoms = line.rstrip("\n").split(",")
        out[(root, kind, bab, v, p, m)] = tuple(atoms.split())
    return out


# (كلمةُ المصحف، الجذر، الصيغة، الباب، حركةُ العين، حرفُ المضارعة، الإعراب) — باليد.
CORPUS_WITNESSES: list[tuple[str, Key]] = [
    ("قَامَ", ("قوم", "madi", "I", "a", "-", "-")),
    ("قَالَ", ("قول", "madi", "I", "a", "-", "-")),
    ("خَافَ", ("خوف", "madi", "I", "i", "-", "-")),
    ("دَعَا", ("دعو", "madi", "I", "a", "-", "-")),
    ("يَقُومُ", ("قوم", "mudari", "I", "u", "ي", "u")),
    ("يَقُولُ", ("قول", "mudari", "I", "u", "ي", "u")),
    ("أَقُولُ", ("قول", "mudari", "I", "u", "ء", "u")),
    ("نَقُولُ", ("قول", "mudari", "I", "u", "ن", "u")),
    ("تَقُولُ", ("قول", "mudari", "I", "u", "ت", "u")),
    ("يَكُونُ", ("كون", "mudari", "I", "u", "ي", "u")),
    ("تَكُونُ", ("كون", "mudari", "I", "u", "ت", "u")),
    ("تَقُمْ", ("قوم", "mudari", "I", "u", "ت", "0")),
    ("يَقُلْ", ("قول", "mudari", "I", "u", "ي", "0")),
    ("قُمْ", ("قوم", "amr", "I", "u", "-", "-")),
    ("قُلْ", ("قول", "amr", "I", "u", "-", "-")),
    ("يَخَافُ", ("خوف", "mudari", "I", "a", "ي", "u")),
    ("نَخَافُ", ("خوف", "mudari", "I", "a", "ن", "u")),
    ("أَخَافُ", ("خوف", "mudari", "I", "a", "ء", "u")),
    ("تَخَافُ", ("خوف", "mudari", "I", "a", "ت", "u")),
    ("يَعِدُ", ("وعد", "mudari", "I", "i", "ي", "u")),
    ("يَصِلُ", ("وصل", "mudari", "I", "i", "ي", "u")),
    ("يَلِدْ", ("ولد", "mudari", "I", "i", "ي", "0")),
    ("يَدْعُو", ("دعو", "mudari", "I", "u", "ي", "u")),
    ("نَدْعُو", ("دعو", "mudari", "I", "u", "ن", "u")),
    ("أَدْعُو", ("دعو", "mudari", "I", "u", "ء", "u")),
    ("تَدْعُو", ("دعو", "mudari", "I", "u", "ت", "u")),
    ("يَخْشَى", ("خشي", "mudari", "I", "a", "ي", "u")),
    ("يَرْضَى", ("رضي", "mudari", "I", "a", "ي", "u")),
    ("يَنْهَى", ("نهي", "mudari", "I", "a", "ي", "u")),
    ("تَنْهَى", ("نهي", "mudari", "I", "a", "ت", "u")),
    ("يَهْدِي", ("هدي", "mudari", "I", "i", "ي", "u")),
    ("يَمْشِي", ("مشي", "mudari", "I", "i", "ي", "u")),
    ("يَأْمُرُ", ("ءمر", "mudari", "I", "u", "ي", "u")),
    ("يَأْخُذُ", ("ءخذ", "mudari", "I", "u", "ي", "u")),
    ("خُذْ", ("ءخذ", "khudh", "I", "u", "-", "-")),
    ("أَقِمْ", ("قوم", "amr", "IV", "i", "-", "-")),
]

# ما ليس كلمةً في المصحف: ذرّاتٌ باليد من نصّ المالك (2026-10-12) ومن الكتاب المختوم.
OWNER_WITNESSES: list[tuple[str, Key]] = [
    ("نَ اْ مَ", ("نوم", "madi", "I", "i", "-", "-")),
    ("يَ نَ اْ مُ", ("نوم", "mudari", "I", "a", "ي", "u")),
    ("نَ مْ", ("نوم", "amr", "I", "a", "-", "-")),
    ("وَ قَ اْ", ("وقي", "madi", "I", "a", "-", "-")),
    ("يَ قِ يْ", ("وقي", "mudari", "I", "i", "ي", "u")),
    ("قِ", ("وقي", "amr", "I", "i", "-", "-")),
    ("قِ هْ", ("وقي", "amr-pause", "I", "i", "-", "-")),
    ("يَ عِ يْ", ("وعي", "mudari", "I", "i", "ي", "u")),
    ("عِ", ("وعي", "amr", "I", "i", "-", "-")),
    ("عِ هْ", ("وعي", "amr-pause", "I", "i", "-", "-")),
    ("نَ مَ اْ", ("نمو", "madi", "I", "a", "-", "-")),
    ("يَ نْ مُ وْ", ("نمو", "mudari", "I", "u", "ي", "u")),
    ("تَ نْ مُ وْ", ("نمو", "mudari", "I", "u", "ت", "u")),
    ("نَ نْ مُ وْ", ("نمو", "mudari", "I", "u", "ن", "u")),
    ("ءَ نْ مُ وْ", ("نمو", "mudari", "I", "u", "ء", "u")),
    ("ءُ نْ مُ", ("نمو", "amr", "I", "u", "-", "-")),
    ("ءَ خَ ذَ", ("ءخذ", "madi", "I", "a", "-", "-")),
    ("ءَ اْ خُ ذُ", ("ءخذ", "mudari", "I", "u", "ء", "u")),
    ("ءُ وْ خُ ذْ", ("ءخذ", "amr", "I", "u", "-", "-")),
    ("يُ عْ طِ يْ", ("عطو", "mudari", "IV", "i", "ي", "u")),
    ("تُ عْ طِ يْ", ("عطو", "mudari", "IV", "i", "ت", "u")),
    ("نُ عْ طِ يْ", ("عطو", "mudari", "IV", "i", "ن", "u")),
    ("ءُ عْ طِ يْ", ("عطو", "mudari", "IV", "i", "ء", "u")),
    ("ءَ عْ طِ", ("عطو", "amr", "IV", "i", "-", "-")),
    ("يَ مُ دْ دُ", ("مدد", "mudari", "I", "u", "ي", "u")),
    ("يَ مْ دُ دْ", ("مدد", "mudari", "I", "u", "ي", "0")),
]


def test_every_corpus_witness_is_the_gate_certificate() -> None:
    for word, key in CORPUS_WITNESSES:
        cert = enter(word.encode())
        assert not isinstance(cert, Refusal), word
        assert tuple(cert.atoms) == _rows()[key], (word, key)


def test_owner_witnesses_by_hand() -> None:
    for atoms, key in OWNER_WITNESSES:
        assert _rows()[key] == tuple(atoms.split()), key


def test_mutant_madd_kept_is_refused_by_the_licence() -> None:
    # MUTANT_MADD_KEPT: مجزومُ الأجوف بلا حذف المدّ (تَقُومْ) ليس كلمةَ المصحف، ومرآةُ الترخيص ترفضه
    corpus = tuple(enter("تَقُمْ".encode()).atoms)  # type: ignore[union-attr]
    mutant = ("تَ", "قُ", "وْ", "مْ")
    assert mutant != corpus
    assert not strict_licensed(mutant) and strict_licensed(corpus)
    qum = _rows()[("قوم", "amr", "I", "u", "-", "-")]
    assert not strict_licensed(("قُ", "وْ", "مْ")) and strict_licensed(qum)


def test_mutant_one_letter_pause_without_haa_is_refused() -> None:
    # MUTANT_NO_HAA: الوقفُ على قِ بلا هاء (قْ) غيرُ مرخَّص، وقِهْ مرخَّصة —
    # «فلا يستطاع أن يتكلم بها في الوقف» (الكتاب 17498)
    for root in ("وقي", "وعي"):
        row = _rows()[(root, "amr-pause", "I", "i", "-", "-")]
        assert strict_pause_licensed(row) and row[-1] == "هْ"
        bare = (row[0][0] + "ْ",)
        assert not strict_pause_licensed(bare)


def test_mutant_mithal_waw_kept_is_licensed_but_not_the_corpus() -> None:
    # MUTANT_MITHAL_KEPT: يَوْعِدُ مرخَّصةٌ بالمقطع — فحذفُ واو المثال وضعٌ يشهد له المصحف
    # (يَعِدُ) لا يُلزمه الترخيص
    mutant = ("يَ", "وْ", "عِ", "دُ")
    assert strict_licensed(mutant)
    assert mutant != tuple(enter("يَعِدُ".encode()).atoms)  # type: ignore[union-attr]
