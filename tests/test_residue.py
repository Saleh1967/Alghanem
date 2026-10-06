"""بقيّةُ الرسم: كلُّ مفردات المصحف تدخل وتخرج بعينها، والموقوفُ مسمًّى ومعدود."""

from __future__ import annotations

from collections import Counter

from conftest import ROOT

from gate import Refusal, enter, exit
from gate.residue import RULES, repair, unrepair


def _surfaces() -> set[str]:
    text = (ROOT / "corpora" / "quran-simple-enhanced.txt").read_text(encoding="utf-8")
    return {w for w in text.split() if w != "<sel>" and any("ء" <= c <= "ي" for c in w)}


def test_every_surface_round_trips_through_repair() -> None:
    """`unrepair ∘ repair = id` على 18,200 رسمًا (مرآةُ `Residue.chain_restore`)."""

    surfaces = _surfaces()
    assert len(surfaces) == 18200
    assert all(unrepair(*repair(s)) == s for s in surfaces)


def test_gate_frees_the_edition_and_names_the_rest() -> None:
    """READY 8,532 → 18,179 بقواعد الطبعة الثماني؛ والـ21 الباقية مسمّاة: 14 من الحروف المقطّعة (بلا
    علامة فلا تُخمَّن)، 3 بهمزةٍ محذوفة تحت تنوين، 3 بسكونٍ أوّل الكلمة، ورسمٌ واحدٌ غيرُ مرخَّص (بِأَييِّكُمُ)."""

    status: Counter[str] = Counter()
    rules: Counter[str] = Counter()
    refused: list[str] = []
    for s in sorted(_surfaces()):
        cert = enter(s.encode("utf-8"))
        if isinstance(cert, Refusal):
            status[cert.status] += 1
            refused.append(s)
            continue
        status["READY"] += 1
        assert exit(cert) == s.encode("utf-8"), s
        for rule, _, _ in cert.residue:
            rules[rule] += 1
    assert status == {"READY": 18179, "REJECT": 7, "DEFER": 14}
    assert set(rules) == set(RULES) and all(rules[r] > 0 for r in RULES)
    assert {"حم", "طس", "ص", "ق", "خَطَاً"} <= set(refused)
    assert any(r.startswith("بِأَي") for r in refused)  # بِأَييِّكُمُ: رسمٌ لا يُرخَّص بعد الإصلاح


def test_same_canonical_different_residue_is_two_surfaces() -> None:
    """`residue_separates`: آمَنُوا وآمَنُوْا صورةٌ واحدة وبقيّتان، فرسمان؛ ولا يُخلط بينهما عند الخروج."""

    a, b = enter("آمَنُوا".encode()), enter("آمَنُوْا".encode())
    assert not isinstance(a, Refusal) and not isinstance(b, Refusal)
    assert a.atoms == b.atoms and a.integer == b.integer and a.residue != b.residue
    assert exit(a) == "آمَنُوا".encode() and exit(b) == "آمَنُوْا".encode()


def test_wasl_vowel_follows_the_rule() -> None:
    """فتحةٌ في «ال»، ضمّةٌ إن كان ثالثُ الفعل مضمومًا، وإلّا كسرة."""

    assert repair("الْحَمْدُ")[0].startswith("ٱَ")
    assert repair("انْصُرْ")[0].startswith("ٱُ")
    assert repair("اضْرِبْ")[0].startswith("ٱِ")
