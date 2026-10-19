"""واوُ «أُولَئِكَ» رسمٌ لا يُنطق (ADR ٥٢): قاعدةُ `ULA_WAW` في بقيّة الرسم، مرآةُ
`A116.Residue.ulaWaw_restore`.

التوقّعاتُ باليد: «أُولَئِكَ» تُشهَد ءُ لَ ءِ كَ بلا مدّ، و«أُولُو» ءُ لُ وْ (الواوُ الأولى
وحدَها رسم)، والرسمُ يُردّ بعينه؛ وما واوُه منطوقةٌ لا يُمسّ: «الْأُولَى»، «أُولَاهُمْ»،
«أُوتُوا». والألفاظُ في المصحف المختوم التي تقع عليها القاعدة أربعَ عشرةَ صورةً، قرأتُها
باليد في المدوّنة (و«لِّأُولِي» بترتيب علاماتها هناك: الشدّةُ قبل الكسرة). والطفرات:
`MUTANT_ULA_EVERY_HAMZA_DAMMA` (كلُّ واوٍ بعد «أُ» تُحذف فيسقط مدُّ «أُوتُوا»)،
`MUTANT_NO_TAIL_CHECK` (يسقط مدُّ «الْأُولَى»)، `MUTANT_NO_RESTORE` (الحذفُ بلا سجلٍّ لا
يُردّ).
"""

from __future__ import annotations

from conftest import ROOT

from gate import enter, exit
from gate.residue import ULA_TAILS, WAW, clusters, repair, unrepair

LILULI = "\u0644\u0651\u0650\u0623\u064f\u0648\u0644\u0650\u064a"  # لِّأُولِي: الشدّةُ قبل الكسرة
FORMS = {"أُولَئِكَ", "أُولَئِكُمْ", "أُولَاءِ", "أُولَاتِ", "أُولُو", "أُولِي", "فَأُولَئِكَ", "لِأُولِي",
         LILULI, "وَأُولَئِكَ", "وَأُولَئِكُمْ", "وَأُولَاتُ", "وَأُولُو", "وَأُولِي"}


def _rules(w: str) -> list[str]:
    return [r for r, _, _ in repair(w)[1]]


def test_hand_certificates() -> None:
    c = enter("أُولَئِكَ".encode())
    assert c.atoms == ("ءُ", "لَ", "ءِ", "كَ") and exit(c) == "أُولَئِكَ".encode()
    assert enter("أُولُو".encode()).atoms == ("ءُ", "لُ", "وْ")
    assert enter("الْأُولَى".encode()).atoms[2:4] == ("ءُ", "وْ")  # الواوُ منطوقة: لا تُمسّ


def test_pronounced_waw_untouched() -> None:
    for w in ("الْأُولَى", "أُولَاهُمْ", "أُوتُوا", "أُوحِيَ", "وَالْأُولَى"):
        assert "ULA_WAW" not in _rules(w), w


def test_exact_forms_in_sealed_corpus_and_roundtrip() -> None:
    corpus = ROOT / "corpora" / "quran-simple-enhanced.txt"
    words = set(corpus.read_text(encoding="utf-8").split())
    hit = {w for w in words if "ULA_WAW" in _rules(w)}
    assert hit == FORMS
    for w in hit:
        can, res = repair(w)
        assert unrepair(can, res) == w


def test_mutants_are_caught() -> None:
    # MUTANT_ULA_EVERY_HAMZA_DAMMA: لو حُذفت كلُّ واوٍ بعد «أُ» لسقط مدُّ «أُوتُوا»
    cl = clusters("أُوتُوا")
    assert cl[0] == "أُ" and cl[1] == WAW and not "".join(c[0] for c in cl[2:]).startswith(ULA_TAILS)
    # MUTANT_NO_TAIL_CHECK: «الْأُولَى» هيكلُ ما بعد «أُو» «لى» لا من القائمة
    assert not "لى".startswith(ULA_TAILS)
    # MUTANT_NO_RESTORE: بلا سجلٍّ لا يُردّ الرسم
    can, res = repair("أُولَئِكَ")
    assert unrepair(can, ()) != "أُولَئِكَ" and unrepair(can, res) == "أُولَئِكَ"


def test_agrees_with_qac_silent_waw_mark() -> None:
    """المرجعُ المحجوب: رسمُ QAC العثمانيّ يعلّم الواوَ التي لا تُنطق بعد «أُ» بالصفر المستدير
    (`>uw@`). كُتبت القاعدةُ قبل النظر فيه؛ ولا موضعَ تحذفه القاعدة وهو منطوقٌ عنده، ولا موضعَ صامتَ
    الواو عنده تتركه القاعدةُ وواوُه في طبعتنا (سَأُرِيكُمْ: طبعتُنا بلا واو أصلًا)."""

    import importlib.util
    import re
    import sys
    from collections import Counter, defaultdict

    spec = importlib.util.spec_from_file_location("gen_qac", ROOT / "tools" / "gen_qac.py")
    assert spec and spec.loader
    q = importlib.util.module_from_spec(spec)
    sys.modules["gen_qac"] = q
    spec.loader.exec_module(q)
    forms: dict[tuple[int, int, int], str] = defaultdict(str)
    for ln in q.source().decode("utf-8").splitlines():
        if ln.startswith("("):
            loc, form, _, _ = ln.split("\t")
            s, v, w, _ = (int(x) for x in loc.strip("()").split(":"))
            forms[(s, v, w)] += form
    by_verse: dict[tuple[int, int], list[tuple[int, str]]] = defaultdict(list)
    for (s, v, w), f in forms.items():
        by_verse[(s, v)].append((w, f))
    lines = q.CORPUS.read_text(encoding="utf-8").splitlines()
    conf: Counter[tuple[bool, bool]] = Counter()
    for i, (s, v) in enumerate(sorted(by_verse)):
        raw = lines[i].split(" ")
        gs, _ = q.groups(s, v, raw)
        ws = sorted(by_verse[(s, v)])
        if len(gs) != len(ws):
            continue
        for g, (_, f) in zip(gs, ws, strict=True):
            tok = raw[g[-1]]
            if ">uw" in f or "أُو" in tok:
                mine, ref = "ULA_WAW" in _rules(tok), bool(re.search(">uw@", f))
                conf[(mine, ref)] += 1
                assert mine == ref or "أُو" not in tok, (tok, f)
    assert conf[(True, True)] == 253 and conf[(True, False)] == 0
