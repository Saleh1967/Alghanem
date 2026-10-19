"""حدودُ الوحدات (`A116.Hudud`، ADR ٨٥): خاناتُ كلّ صورةٍ مبنيّةٍ في Lean هي ما تطبعه البوّابة للكلمة
بعينها من المصحف المختوم، لا شكلٌ باليد.

١. الصورُ الأربعون باليد (المرفوعُ المنفصل 10، المنصوبُ 4، الموصولُ 9، الإشارةُ 9، النداءُ 1،
   الاستفهامُ 7)، كلٌّ كلمةٌ في المصحف المختوم بعينها (بترتيب الشدّة قبل الحركة كما في المختوم)،
   تدخل البوّابة شهادةً وذرّاتُها هي خاناتُ Lean حرفًا حرفًا.
٢. ما قوائمُ الشرح تذكره ولا شكلَ مختومًا له (أَنْتِ، اللَّذَانِ، إِيَّايَ…) ليس في المصحف فلا يُودَع
   (`FORM_WITHOUT_SEALED_VOWELS`).
الطفرات: `MUTANT_HARAKA_BEFORE_SHADDA` (الترتيبُ المعكوس ليس الكلمةَ بعينها: رفضٌ لا تطبيع)،
`MUTANT_ATOM_SWAPPED` (خانةٌ مبدَّلة في Lean لا تطابق البوّابة)، `MUTANT_UNSEALED_FORM` (صورةٌ بلا
شكلٍ مختوم تُرفض بـ`OUTSIDE_DECLARED_DOMAIN`).
"""

from __future__ import annotations

import re

from conftest import ROOT

import gate

LEAN = ROOT / "formal" / "a116" / "A116" / "Hudud.lean"
H = {".fatha": "َ", ".damma": "ُ", ".kasra": "ِ", ".sukun": "ْ"}
BY_HAND = {"damirRaf": 10, "damirNasb": 4, "mawsul": 9, "ishara": 9, "nida": 1, "istifham": 7}


def lean_lists() -> dict[str, list[tuple[str, tuple[str, ...]]]]:
    """(الكلمةُ في التعليق، ذرّاتُها) لكلّ قائمةٍ مبنيّة في Lean."""
    out: dict[str, list[tuple[str, tuple[str, ...]]]] = {}
    name = None
    for line in LEAN.read_text(encoding="utf-8").splitlines():
        m = re.match(r"def (damirRaf|damirNasb|mawsul|ishara|nida|istifham) ", line)
        if m:
            name = m.group(1)
            out[name] = []
            continue
        if name and "atom '" in line and "--" in line:
            atoms = tuple(c + H[h] for c, h in re.findall(r"atom '(.)' (\.\w+)", line))
            out[name].append((line.split("--")[-1].strip(), atoms))
        elif name and line.strip() == "":
            name = None
    return out


def corpus_words() -> set[str]:
    return set((ROOT / "corpora" / "quran-simple-enhanced.txt").read_text(encoding="utf-8").split())


def test_forms_are_gate_output() -> None:
    lists = lean_lists()
    assert {k: len(v) for k, v in lists.items()} == BY_HAND and sum(BY_HAND.values()) == 40
    words = corpus_words()
    for name, items in lists.items():
        for word, atoms in items:
            assert word in words, (name, word)
            cert = gate.enter(word.encode())
            assert isinstance(cert, gate.Certificate), (name, word, cert)
            assert tuple(cert.atoms) == atoms, (name, word, cert.atoms, atoms)
            assert gate.exit(cert) == word.encode()


def test_unsealed_forms_absent() -> None:
    words = corpus_words()
    for w in ["أَنْتِ", "أَنتُنَّ", "إِيَّايَ", "اللَّذَانِ", "اللَّتَانِ", "تَا", "أَيَا", "هَيَا"]:
        assert w not in words, w


def test_mutant_haraka_before_shadda() -> None:
    shadda, fatha = "\u0651", "\u064e"
    sealed = "ال" + shadda + fatha + "ذِي"  # ل ثمّ شدّة ثمّ فتحة، كما في المختوم
    swapped = "ال" + fatha + shadda + "ذِي"
    assert isinstance(gate.enter(sealed.encode()), gate.Certificate)
    r = gate.enter(swapped.encode())
    assert isinstance(r, gate.Refusal) and r.status == "OUTSIDE_DECLARED_DOMAIN"


def test_mutant_atom_swapped() -> None:
    word, atoms = lean_lists()["damirRaf"][5]  # هُوَ
    assert word == "هُوَ"
    cert = gate.enter(word.encode())
    assert isinstance(cert, gate.Certificate)
    mutant = (atoms[0], atoms[1][0] + H[".damma"])  # هُوُ
    assert tuple(cert.atoms) != mutant


def test_mutant_unsealed_form_refused() -> None:
    r = gate.enter("أَنتُنَّ".encode())
    assert isinstance(r, gate.Refusal) and r.status == "OUTSIDE_DECLARED_DOMAIN"
