"""أبنيةُ سيبويه على الترخيص الثلاثيّ (ADR ٣٦): توقّعاتٌ مستقلّةٌ عن الشيفرة — الأبنيةُ التي
أوّلُها ألفٌ هي أبنيةُ همزة الوصل (افتعل، استفعل، انفعل…) ولا يُرخَّص لها تشكيلٌ بألفٍ ساكنةٍ
أوّلًا، ويُرخَّص بالقاعدة (اِفْتَعَلَ، اِسْتَفْعَلَ)؛ والألفُ لا تكون إلّا ساكنة؛ والشواهدُ تطابق
تصدير Lean؛ وطفراتٌ مرفوضة."""

from __future__ import annotations

from pathlib import Path

from slge.abniya_licence import counts, is_wasl, vocalizations
from slge.abniya_licence_table import WITNESSES
from slge.abniya_table import SKELETONS
from slge.cells import ALPHABET, STATES, SUKUN
from slge.madd import continue_licensed, pause_licensed

ROOT = Path(__file__).resolve().parents[1]


def _sk(name: str) -> tuple[int, ...]:
    return next(s for s in SKELETONS if "".join(ALPHABET[i] for i in s) == name)


def test_wasl_skeletons_need_the_boundary_rule() -> None:
    wasl = [s for s in SKELETONS if is_wasl(s)]
    names = {"".join(ALPHABET[i] for i in s) for s in wasl}
    assert len(wasl) == 13 and {"افتعل", "استفعل", "افعوعل"} <= names
    for s in wasl:  # فحصٌ شاملٌ لكلّ تشكيلاته: الألفُ الأولى ساكنةً كما رُسمت لا تُرخَّص أبدًا
        assert counts(s, wasl_rule=False)[1:] == (0, 0), s
        assert counts(s)[1] > 0 and counts(s)[2] > 0, s
    # اِفْتَعَلَ واِسْتَفْعَلَ مشكولتين بأيدينا (مستقلّتين عن المولِّد)
    iftaala = (("ء", "كسر"), ("ف", SUKUN), ("ت", "فتح"), ("ع", "فتح"), ("ل", "فتح"))
    istafala = (("ء", "كسر"), ("س", SUKUN), ("ت", "فتح"), ("ف", SUKUN), ("ع", "فتح"), ("ل", "فتح"))
    for w in (iftaala, istafala):
        assert continue_licensed(w) and pause_licensed(w)
        assert not continue_licensed((("ا", SUKUN), *w[1:]))


def test_every_skeleton_has_a_licensed_vocalization_and_alif_is_never_voweled() -> None:
    assert len(SKELETONS) == 158 and len(WITNESSES) == 158
    assert all(counts(s)[1] > 0 and counts(s)[2] > 0 for s in SKELETONS)
    for sk, w in WITNESSES:
        cells = tuple((ALPHABET[k], STATES[s]) for k, s in w)
        assert continue_licensed(cells) and pause_licensed(cells)
        assert all(st == SUKUN for k, st in cells if k == "ا")
        assert [ALPHABET.index(k) for k, _ in cells] == [0 if i == 0 and sk[0] == 1 else x
                                                        for i, x in enumerate(sk)]
    # فَاعِل: الألفُ مدٌّ بعد فتح — لا تشكيلَ بألفٍ متحرّكة في الفضاء أصلًا
    faail = _sk("فاعل")
    assert all(w[1][1] == SUKUN for w in vocalizations(faail))


def test_mutations_change_the_numbers() -> None:
    """الطفرة: لو تُركت الألفُ متحرّكةً لاتّسع الفضاءُ ولعدّ الترخيصُ الثلاثيُّ ما لا يُرخَّص من
    الشبكة (الألفُ المتحرّكة متحرّكٌ عنده) — فقيدُ الألف يغيّر الأرقام ولا يمرّ صامتًا. وحركةُ همزة
    الوصل لا تغيّر الترخيص (كلُّ حركةٍ متحرّك)، فلا تُعدّ طفرةً فاصلة هنا."""

    from itertools import product

    faail = _sk("فاعل")
    tot, cont, _ = counts(faail)
    assert tot == 4 ** 3  # ف ع ل حرّةٌ بأربع حالات، والألفُ ساكنةٌ أبدًا
    letters = [ALPHABET[i] for i in faail]
    free = [tuple(zip(letters, st, strict=True)) for st in product(STATES, repeat=len(letters))]
    cont_free = sum(1 for w in free if continue_licensed(w))
    assert len(free) == 4 ** 4 and cont_free > cont
    istafala = _sk("استفعل")
    damma_always = sum(1 for w in vocalizations(istafala)
                       if continue_licensed((("ء", "ضم"), *w[1:])))
    assert damma_always == counts(istafala)[1]


def test_python_matches_the_lean_export() -> None:
    rows = (ROOT / "formal" / "out" / "abniya_licence.csv").read_text(encoding="utf-8").splitlines()
    exported = [r.split(",") for r in rows if r.startswith("witness,")]
    assert len(exported) == len(WITNESSES) == 158
    for (_, sk, n, cont, pause, written), (want_sk, w) in zip(exported, WITNESSES, strict=True):
        assert tuple(int(x) for x in sk.split("-")) == want_sk and int(n) == len(w)
        assert cont == pause == "true"
        cells = tuple((ALPHABET[k], STATES[s]) for k, s in w)
        assert (written == "true") == continue_licensed((("ا", SUKUN), *cells[1:]))
