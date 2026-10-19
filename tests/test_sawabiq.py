"""السوابقُ قبل الفعل المبنيّ (ADR ٤٦): مرآةُ `A116.Sawabiq` في `gate.sawabiq`، و`recover(peel=True)`.

التوقّعاتُ مكتوبةٌ باليد من تعريف Lean (الخاناتُ الثلاث بترتيبها)، لا من الشيفرة. والطفرات:
`MUTANT_SLOT_ORDER` (العاطفةُ قبل الهمزة لا تُقشَّر)، `MUTANT_KASRA_LAM` (اللامُ المكسورة خارج القائمة)،
`MUTANT_PEEL_DROPS_DIRECT` (القراءةُ المباشرة أوّلًا: وَجَدَ يبقى من وجد).
"""

from __future__ import annotations

from gate import recover
from gate.sawabiq import candidates

F = "َ"


def test_hand_candidates() -> None:
    assert candidates("فَقَالُوا") == ["فَقَالُوا", "قَالُوا"]
    assert candidates("قَالَ") == ["قَالَ"]
    full = "أ" + F + "ف" + F + "ل" + F + "قَالَ"
    assert candidates(full) == [full, full[2:], full[4:], full[6:]] and full[6:] == "قَالَ"


def test_lean_properties_hold_on_hand_words() -> None:
    for w in ["فَقَالُوا", "وَاعْبُدُوا", "أَفَلَمْ", "لَقَدْ", "وَلَوْ", "فَلَا", "أَوَلَمْ"]:
        cs = candidates(w)
        assert cs[0] == w and len(cs) <= 12  # candidates_head، candidates_length_le
        assert all(w.endswith(c) for c in cs)  # candidates_suffix


def test_recover_peel() -> None:
    assert recover("فَقَالُوا")[0] == "NOT_GENERATED"
    assert "قول" in {r[0] for r in recover("فَقَالُوا", peel=True)[1]}
    assert {r[0] for r in recover("وَاعْبُدُوا", peel=True)[1]} == {"عبد"}


def test_mutants_are_caught() -> None:
    # MUTANT_SLOT_ORDER: «فَأَ» ليس ترتيبَ الخانات
    assert "قَالَ" not in candidates("ف" + F + "أ" + F + "قَالَ")
    # MUTANT_KASRA_LAM: «لِ» ليست من القائمة
    assert candidates("لِيَقُولَ") == ["لِيَقُولَ"]
    # MUTANT_PEEL_DROPS_DIRECT: وَجَدَ يُقرأ بعينه فلا يُقشَّر إلى «جَدَ»
    assert {r[0] for r in recover("وَجَدَ", peel=True)[1]} == {"وجد"}
