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
    sealed_rules = set(RULES) - {"DAGGER_ALIF"}  # الخنجريّةُ طبعةُ globalquran لا المختومة
    assert set(rules) == sealed_rules and all(rules[r] > 0 for r in sealed_rules)
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


def test_long_vowel_codas_are_geminate_except_madd_al_farq() -> None:
    """«التقاء الساكنين على حدّه»: كلُّ قافيةِ CVVC في شهادات المصحف مدغمةٌ (حَاجَّ: 65) إلّا مدَّ الفرق
    (آلْآنَ: 1). قياسٌ لا برهان؛ والتضييقُ الذي كان دَينًا على `Ternary.ContinueLicensed` هو الآن
    `A116.Hadd.strictB` (تضعيفٌ أو مدُّ فرق)، والمطابقةُ والطفراتُ في `tests/test_hadd.py`."""

    from gate.licence import kind_of

    geminate, other = 0, []
    for s in sorted(_surfaces()):
        cert = enter(s.encode("utf-8"))
        if isinstance(cert, Refusal):
            continue
        k = kind_of(cert.atoms)
        for i in range(len(k) - 1):
            if k[i] == "v" and k[i + 1] == "c":
                if i + 2 < len(cert.atoms) and cert.atoms[i + 2][0] == cert.atoms[i + 1][0]:
                    geminate += 1
                else:
                    other.append(s)
    assert geminate == 65 and other == ["آلْآنَ"]


def test_dagger_alif_edition_reduces_to_the_sealed_text() -> None:
    """`Residue.daggerAlif_restore`: طبعةُ globalquran (مدوّنةُ hamil بعينها) تكتب الألفَ الخنجريّة؛
    تُحذف قاعدةً مسمّاةً فتصير الصورةُ صورةَ المدوّنة المختومة بعينها، وتُردّ بعينها. لكلّ كلمةٍ فيها
    خنجريّة: الردُّ تامّ، وصورتُها القانونيّة من صور آيتها في المختومة، وحكمُ البوّابة عليها حكمُها على
    نظيرتها."""

    dagger = "\u0670"
    gq = (ROOT / "corpora" / "globalquran-simple-enhanced.txt").read_text(encoding="utf-8-sig")
    tz = (ROOT / "corpora" / "quran-simple-enhanced.txt").read_text(encoding="utf-8")
    lines_gq = [ln for ln in gq.split("\n") if ln and not ln.startswith("#")]
    lines_tz = [ln for ln in tz.split("\n") if ln and not ln.startswith("#")]
    assert len(lines_gq) == len(lines_tz) == 6236
    words = 0
    checked: set[str] = set()
    for a, b in zip(lines_gq, lines_tz, strict=True):
        canon_tz = {repair(w)[0] for w in b.split()
                    if w != "<sel>" and any("ء" <= c <= "ي" for c in w)}
        for w in a.split():
            if dagger not in w or not any("ء" <= c <= "ي" for c in w):
                continue
            words += 1
            canon, edits = repair(w)
            assert unrepair(canon, edits) == w, w  # الردُّ بعينه
            assert any(r == "DAGGER_ALIF" for r, _, _ in edits) and dagger not in canon, w
            assert canon in canon_tz, (w, canon)  # الصورةُ صورةُ المختومة بعينها
            if w not in checked:
                checked.add(w)
                twin = w.replace(dagger, "")
                r1, r2 = enter(w.encode("utf-8")), enter(twin.encode("utf-8"))
                assert type(r1) is type(r2), (w, r1, r2)
                if not isinstance(r1, Refusal):
                    assert r1.atoms == r2.atoms and exit(r1) == w.encode("utf-8"), w
    assert words == 3216 and len(checked) > 100
    # الطفرة: خنجريّةٌ في غير موضعها تُردّ بعينها أيضًا (السجلُّ يحمل العنقودَ كما ورد)
    odd = "كَٰتَبَ"
    assert unrepair(*repair(odd)) == odd
