"""أوزانُ الرباعيّ وفتحُ بوّابته (`A116.Rubai`، ADR ٢٨): شاهدُ المدوّنتين وشاهدُ المقاييس، مستقلّان عن Lean.

الجدولُ `formal/a116/rubai.csv` يطبعه Lean ويطابقه CI بايتًا بايتًا. والتوقّعُ كلماتٌ مشكولةٌ من
المصحف والصحيحين مكتوبةً باليد تمرّ على البوّابة (`gate.enter`، و`Gate(corpus=HADITH_CORPUS)`)؛
والفاءُ العاطفة في أوّل الكلمة تُنزع باليد قبل المقارنة. وعددُ شاهد الدلالة يُعدّ هنا من بايتات
الجدول المختوم `maqayis_by_root_csv_999.csv` بقاعدةٍ معلنةٍ باليد، لا من شيفرة البوّابة.
والطفرات: وزنٌ بحركاتٍ مخمَّنة لافْعَنْلَلَ، وعدُّ الجذور المكتوبة بالألف، وحركةٌ مبدَّلةٌ في الشاهد.
"""

from __future__ import annotations

import csv
import hashlib
from functools import cache
from pathlib import Path

from gate import Refusal, enter
from gate.api import HADITH_CORPUS, Gate
from gate.licence import strict_licensed

ROOT = Path(__file__).resolve().parents[1]
TABLE = ROOT / "formal" / "a116" / "rubai.csv"
MAQAYIS = ROOT / "maqayis_by_root_csv_999.csv"
MAQAYIS_SHA256 = "2c6000bd47797e183294b89da77df4ddfd27921ea595c6071ba52299c382ccb0"
RADICALS = set("بتثجحخدذرزسشصضطظعغفقكلمنهويء")  # الحواملُ التسعةُ والعشرون إلّا الألف — باليد


@cache
def _rows() -> dict[tuple[str, str], tuple[str, ...]]:
    out: dict[tuple[str, str], tuple[str, ...]] = {}
    for line in TABLE.open(encoding="utf-8"):
        parts = line.rstrip("\n").split(",")
        if parts[0] != "maqayis":
            out[(parts[0], parts[1])] = tuple(parts[2].split())
    return out


def _lean_count() -> int:
    for line in TABLE.open(encoding="utf-8"):
        if line.startswith("maqayis,"):
            return int(line.strip().split(",")[1])
    raise AssertionError("no maqayis row")


# (الكلمة، المدوّنة، أتُنزع فاءٌ عاطفة، الوزن، الجذر) — باليد.
WITNESSES: list[tuple[str, str, bool, str, str]] = [
    ("حَصْحَصَ", "quran", False, "فعلل", "حصحص"),
    ("عَسْعَسَ", "quran", False, "فعلل", "عسعس"),
    ("فَدَمْدَمَ", "quran", True, "فعلل", "دمدم"),
    ("فَوَسْوَسَ", "quran", True, "فعلل", "وسوس"),
    ("بُعْثِرَ", "quran", False, "فعلل-مجهول", "بعثر"),
    ("زُحْزِحَ", "quran", False, "فعلل-مجهول", "زحزح"),
    ("يُوَسْوِسُ", "quran", False, "يفعلل", "وسوس"),
    # الشدّةُ قبل الحركة كما في المدوّنة (البوّابةُ لا تعيد ترتيب العلامات)
    ("اطْمَأَن\u0651\u064e", "quran", False, "افعللّ", "طمءن"),
    ("تَقْشَعِر\u0651\u064f", "quran", False, "تفعللّ", "قشعر"),
    ("فَتَدَحْرَجَ", "hadith", True, "تفعلل", "دحرج"),
    ("تَمَضْمَضَ", "hadith", False, "تفعلل", "مضمض"),
    ("تَدَهْدَهَ", "hadith", False, "تفعلل", "دهده"),
]


@cache
def _hadith_gate() -> Gate:
    return Gate(corpus=HADITH_CORPUS)


def _atoms(word: str, corpus: str) -> tuple[str, ...]:
    cert = enter(word.encode()) if corpus == "quran" else _hadith_gate().enter(word.encode())
    assert not isinstance(cert, Refusal), word
    return tuple(cert.atoms)


def test_every_pattern_has_a_sealed_vocalized_witness() -> None:
    for word, corpus, fa, name, root in WITNESSES:
        atoms = _atoms(word, corpus)
        if fa:
            assert atoms[0] == "فَ", word
            atoms = atoms[1:]
        assert atoms == _rows()[(name, root)], (word, name)
    assert {name for _, _, _, name, _ in WITNESSES} == {
        "فعلل", "فعلل-مجهول", "يفعلل", "تفعلل", "افعللّ", "تفعللّ"}


def test_mutant_vowel_swapped_in_a_witness_is_caught() -> None:
    # MUTANT_VOWEL_SWAPPED: فَعْلَلَ بكسر العين (حَصْحِصَ) ليس الشاهدَ ولا صفَّ Lean
    row = _rows()[("فعلل", "حصحص")]
    mutant = ("حَ", "صْ", "حِ", "صَ")
    assert mutant != row and mutant != _atoms("حَصْحَصَ", "quran")


def test_mutant_guessed_ifanlala_is_licensed_but_has_no_sealed_witness() -> None:
    # MUTANT_GUESSED_IFANLALA: اِحْرَنْجَمَ بحركاتٍ مخمَّنة مرخَّصةٌ بالمقطع، لكنّها ليست كلمةً في المدوّنتين —
    # فالرفضُ `IFANLALA_WITHOUT_SEALED_VOWELS` لغيابِ الشاهد لا لامتناع الصورة
    guessed = "اِحْرَنْجَمَ"
    assert strict_licensed(("ءِ", "حْ", "رَ", "نْ", "جَ", "مَ"))
    assert isinstance(enter(guessed.encode()), Refusal)
    assert isinstance(_hadith_gate().enter(guessed.encode()), Refusal)
    assert not any(name.startswith("افعنلل") for name, _ in _rows())


def _maqayis_roots(keep_alif: bool) -> set[str]:
    data = MAQAYIS.read_bytes()
    assert hashlib.sha256(data).hexdigest() == MAQAYIS_SHA256
    fold = {"أ": "ء", "إ": "ء", "ؤ": "ء", "ئ": "ء", "ى": "ي"}  # الكراسيُّ همزة، والمقصورةُ ياء — باليد
    out: set[str] = set()
    for row in csv.DictReader(data.decode("utf-8").splitlines()):
        root = "".join(fold.get(c, c) for c in row["root_full"].replace("آ", "ءا"))
        if len(root) == 3 and (keep_alif or set(root) <= RADICALS):
            out.add(root)
    return out


def test_dalala_witness_count_is_recounted_from_the_sealed_table() -> None:
    assert len(_maqayis_roots(keep_alif=False)) == _lean_count()


def test_mutant_counting_alif_roots_inflates_the_witness() -> None:
    # MUTANT_ALIF_ROOTS_COUNTED: عدُّ جذور المقاييس المكتوبة بالألف (حجا…) يزيد على جدول الدرجة
    with_alif = {r for r in _maqayis_roots(keep_alif=True) if all("ء" <= c <= "ي" for c in r)}
    assert len(with_alif) > _lean_count()
    assert all("ا" in r for r in with_alif - _maqayis_roots(keep_alif=False))
