"""الإعلالُ والإبدال: الجبرُ المغلق صعودًا ونزولًا على الخانات، والرقمُ على المودَع.

التوقّعاتُ من الغانم (`A116.Ilal`: الأصلُ ← الصورةُ لكلّ قاعدة، والإلزامُ في حذف العين) على شواهدِ
الخانات، مستقلّةً عن شيفرة `slge.ilal`؛ والطفرةُ (قاعدةٌ في غير موضعها؛ أصلٌ لا يصعد؛ سلسلةٌ مزوَّرة؛ ألفٌ
في جذرٍ) تُرفَض.
"""

from __future__ import annotations

from pathlib import Path

from slge.cells import SUKUN, licensed
from slge.ilal import RULES, apply, ascend, descend, positions, record, restore, undo
from slge.jidh import jidh
from slge.madd import continue_licensed, pause_licensed
from slge.rawabit import cells_of

ROOT_DIR = Path(__file__).resolve().parent.parent
PAIRS = (  # (القاعدة، الموضع، الأصل، الصورة) — من جدول الغانم بعينه
    ("QALB_AYN", 0, "قَوَلَ", "قَالَ"), ("HADHF_AYN_U", 0, "قَالْتُ", "قُلْتُ"),
    ("HADHF_AYN_I", 0, "بَاعْتُ", "بِعْتُ"), ("NAQL", 0, "يَقْوُلُ", "يَقُولُ"),
    ("QALB_LAM", 1, "دَعَوَ", "دَعَا"), ("HADHF_LAM", 1, "دَعَوُوْ", "دَعَوْ"),
    ("HADHF_WAW", 0, "يَوْعِدُ", "يَعِدُ"), ("HAMZA_MADD", 0, "ءَءْمَنَ", "ءَامَنَ"),
    ("TA_TTA", 1, "إِصْتَبَرَ", "إِصْطَبَرَ"), ("TA_DAL", 1, "إِزْتَادَ", "إِزْدَادَ"),
    ("FA_TA", 1, "إِوْتَصَلَ", "إِتْتَصَلَ"), ("WAW_YA", 0, "مِوْزَانُ", "مِيزَانُ"),
    ("YA_WAW", 0, "مُيْقِنُ", "مُوقِنُ"),
)


def test_every_rule_ascends_and_descends_exactly() -> None:
    assert len(RULES) == 13 and len(PAIRS) == 13
    for rule, i, asl, sura in PAIRS:
        u, w = cells_of(asl), cells_of(sura)
        assert apply(rule, u, i) == w, rule  # الصعودُ بعينه
        assert u in undo(rule, w, i), rule  # لا أصلَ يفوت (undo_complete)
        for v in undo(rule, w, i):
            assert apply(rule, v, i) == w, (rule, v)  # النزولُ عكسُ الصعود (undo_sound)
        if i in positions(rule, len(w)):
            assert (((rule, i),), u) in descend(w, len(w)), rule  # descend_complete
    # الطفرة: القاعدةُ في غير موضعها لا تنطبق، والسلسلةُ المزوَّرة لا تصعد
    assert apply("QALB_AYN", cells_of("قَوَلَ"), 1) is None
    assert apply("NAQL", cells_of("كَتَبَ"), 0) is None
    assert ascend((("HADHF_AYN_U", 0), ("QALB_AYN", 0)), cells_of("قَوَلْ")) is None
    assert ascend((("QALB_AYN", 0), ("HADHF_AYN_U", 0)), cells_of("قَوَلْ")) == cells_of("قُلْ")


def test_roundtrip_by_the_alghanem_record() -> None:
    """الردُّ بسجلّ الغانم بعينه: `restoreEdit (apply ρ u i) (record ρ u i) = u` لكلّ زوجٍ من الجدول."""

    for rule, i, asl, sura in PAIRS:
        u, w = cells_of(asl), cells_of(sura)
        rc = record(rule, u, i)
        assert restore(w, rc) == u, rule  # apply_roundtrip
        start, inserted, removed = rc
        assert len(removed) >= 1 and w[:start] == u[:start]  # ما قبل البداية لا يُمسّ
        assert len(w) - inserted + len(removed) == len(u)
    # الطفرة: سجلٌّ مزوَّرٌ (بدايةٌ منقولة) لا يردّ الأصل
    u, w = cells_of("قَوَلَ"), cells_of("قَالَ")
    assert restore(w, (0, 1, (("و", "فتح"),))) != u
    # الترخيصُ الثلاثيُّ لا يتغيّر بإبدال تاء الافتعال طاءً أو دالًا (ibdal_ternary)
    for a, b in (("إِصْتَبَرَ", "إِصْطَبَرَ"), ("إِزْتَادَ", "إِزْدَادَ")):
        assert continue_licensed(cells_of(a)) == continue_licensed(cells_of(b))
        assert pause_licensed(cells_of(a)) == pause_licensed(cells_of(b))


def test_closure_and_forcing_on_licensing() -> None:
    for rule, _, asl, sura in PAIRS:
        u, w = cells_of(asl), cells_of(sura)
        if rule.startswith("HADHF_AYN"):
            assert not licensed(u) and licensed(w), rule  # الإلزام: الأصلُ غيرُ مرخَّص
        else:
            assert licensed(u) == licensed(w) is True, rule  # الإغلاق
    # القلبُ قبل ساكنٍ يعطي صورةً غيرَ مرخَّصة (قَالْ) فالحذفُ واجب
    v = apply("QALB_AYN", cells_of("قَوَلْ"), 0)
    assert v == cells_of("قَالْ") and not licensed(v)


def test_descent_is_bounded_and_every_descent_ascends() -> None:
    for word in ("قَالَ", "قُلْ", "كُنْتُمْ", "يَقُولُ", "دَعَا", "دَعَوْ", "يَعِدُ", "ءَامَنَ", "مِيزَانُ",
                 "كَتَبَ", "إِصْطَبَرَ"):
        w = cells_of(word)
        ds = descend(w, len(w))
        assert all(len(ch) <= 2 for ch, _ in ds)
        for ch, u in ds:
            assert ascend(ch, u) == w, (word, ch, u)  # descend_ascends
    assert descend(cells_of("كَتَبَ"), 3) == () or all(
        ascend(ch, u) == cells_of("كَتَبَ") for ch, u in descend(cells_of("كَتَبَ"), 3))
    assert positions("HADHF_WAW", 5) == (0,) and positions("HADHF_LAM", 5) == (4,)


def test_jidh_reads_by_descent_with_named_origins() -> None:
    def origins(word: str) -> list[tuple[str, tuple[tuple[str, int], ...]]]:
        return [("".join(c for c, _ in r.asl), r.ilal) for r in jidh(cells_of(word))]

    assert origins("قَالَ") == [("قول", (("QALB_AYN", 0),)), ("قيل", (("QALB_AYN", 0),))]
    assert origins("كَانَ") == [("كون", (("QALB_AYN", 0),)), ("كين", (("QALB_AYN", 0),))]
    assert origins("قُلْ") == [("قول", (("QALB_AYN", 0), ("HADHF_AYN_U", 0))),
                              ("قيل", (("QALB_AYN", 0), ("HADHF_AYN_U", 0)))]
    assert origins("دَعَا") == [("دعو", (("QALB_LAM", 1),)), ("دعي", (("QALB_LAM", 1),))]
    assert [o for o in origins("كُنْتُمْ")] == [("كون", (("QALB_AYN", 0), ("HADHF_AYN_U", 0))),
                                             ("كين", (("QALB_AYN", 0), ("HADHF_AYN_U", 0)))]
    for r in jidh(cells_of("كُنْتُمْ")):
        assert r.stem == cells_of("كُنْ") and r.suf == (("ت", "ضم"), ("م", SUKUN))
        assert ascend(r.ilal, (*r.asl, *r.suf)) == (*r.stem, *r.suf)  # jidh_ascends
    # باسمه: المبنيُّ للمجهول من الأجوف ليس من القواعد — لا قراءةَ بالإعلال؛ ويُقرأ اسمًا على فِعْل (121)
    assert [(r.templates, r.ilal) for r in jidh(cells_of("قِيلَ"))] == [((121,), ())]


def test_numbers_on_the_deposit() -> None:
    import subprocess
    import sys

    sys.path.insert(0, str(ROOT_DIR / "tools"))
    from gen_ilal_index import measure

    m = measure()
    # كانت 2,138 و1,000 قبل قوالب الاسم الأربعة (أ2): ما صار يُقرأ مباشرةً على فِعْل/فَعَال لا ينزل
    # بالإعلال
    # ثمّ 1,960 قبل زوائد سيبويه (ADR ١٨: النونُ والتاءُ لاحقتين تفتحان جذوعًا معتلّةً للإعلال)
    assert m["forms"] == 18179 and m["with"] == 2040 and m["only"] == 648
    assert m["rules"]["QALB_AYN"] > m["rules"]["HADHF_AYN_U"] > m["rules"]["NAQL"]
    # كانت 9,249 كلمةً لا تُقرأ إلّا بالإعلال فصارت 7,746 بعد قوالب الاسم (أ2)
    assert m["m_total"] == 7749 and m["m_hit"] > 0.9 * m["m_total"]  # كانت 7,746
    law = m["law"]
    assert law["itbaq_ta"] == 17 and law["itbaq_tta"] == 108 and law["dzz_ta"] == 20
    assert law["dzz_dal"] == 297 and len(law["kept"]) == 32
    assert "بسطت" in law["kept"] and "حرصتم" in law["kept"] and "ءصطبر" not in law["kept"]
    res = subprocess.run([sys.executable, str(ROOT_DIR / "tools" / "gen_ilal_index.py"), "--check"],
                         capture_output=True, text=True, cwd=ROOT_DIR)
    assert res.returncode == 0, res.stderr
