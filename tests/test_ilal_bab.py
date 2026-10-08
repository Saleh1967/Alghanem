"""أبوابُ الإعلال: توقّعاتٌ مستقلّةٌ عن الشيفرة (كلُّ قاعدةٍ لها بابٌ واحدٌ بسطره؛ ثمانٍ تقرأ صورتَها
المودَعة بعينها والخمسُ الباقيةُ رسمٌ بلا خانات؛ سبعةُ ديونٍ بأسطرها)، وطفراتٌ مرفوضة."""

from __future__ import annotations

from slge.ilal import RULES, undo
from slge.ilal_bab import DEBTS, TABLE, anchor_of, reads, unwitnessed, witnessed

AYN = "هذا باب ما الياء والواو فيه ثانية وهما في موضع العين منه"


def test_every_rule_has_exactly_one_chapter_in_rule_order() -> None:
    assert tuple(r[0] for r in TABLE) == RULES and len(TABLE) == 13
    # الأربعُ الأُوَل (القلبُ والحذفُ بوجهيه والنقل) في باب العين الواحد؛ والبدلان في باب حروف البدل
    assert all(anchor_of(k)[1] == AYN for k in ("QALB_AYN", "HADHF_AYN_U", "HADHF_AYN_I", "NAQL"))
    assert anchor_of("TA_TTA")[2] == anchor_of("TA_DAL")[2] == 18566
    assert anchor_of("HAMZA_MADD")[1] == "هذا باب الهمز" and anchor_of("HAMZA_MADD")[3] == "آدم"
    assert anchor_of("WAW_YA")[3] == "ميزان" and anchor_of("YA_WAW")[3] == "موقن"


def test_eight_rules_read_their_deposited_forms() -> None:
    w = witnessed()
    assert tuple(r[0] for r in w) == ("QALB_AYN", "HADHF_AYN_U", "HADHF_AYN_I", "NAQL",
                                      "QALB_LAM", "HADHF_WAW", "HAMZA_MADD", "WAW_YA")
    assert all(reads(r) for r in w) and all(r[6] == "chapter" for r in w)
    # خَافَ ← خَوَفَ/خَيَفَ في الموضع 0؛ ءَلْمِيزَانَ تُقرأ في الموضع 2 بعد لام التعريف
    _, _, _, _, cells, at, _ = anchor_of("QALB_AYN")
    assert cells == (("خ", "فتح"), ("ا", "سكون"), ("ف", "فتح")) and at == 0
    assert len(undo("QALB_AYN", cells, 0)) == 2
    mizan = anchor_of("WAW_YA")
    assert mizan[5] == 2 and mizan[4] is not None
    assert mizan[4][:2] == (("ء", "فتح"), ("ل", "سكون"))


def test_five_rules_stay_unvowelled_by_name() -> None:
    assert unwitnessed() == ("HADHF_LAM", "TA_TTA", "TA_DAL", "FA_TA", "YA_WAW")
    for k in unwitnessed():
        r = anchor_of(k)
        assert r[4] is None and r[5] is None and r[6] == "none" and r[3]
        assert not reads(r)


def test_seven_debts_named_by_line_outside_anchored_chapters() -> None:
    titles = [t for t, _ in DEBTS]
    assert len(DEBTS) == 7 and all(t.startswith("هذا باب") for t in titles)
    assert any("تمال فيه الألفات" in t for t in titles)  # الإمالةُ بعنوانها المطبوع
    assert any("الإدغام" in t for t in titles)
    assert any("التضعيف في بنات الياء" in t for t in titles)
    assert not {n for _, n in DEBTS} & {r[2] for r in TABLE}
    assert len({n for _, n in DEBTS}) == 7


def test_mutants_are_refused() -> None:
    # حذفُ خانةٍ من الصورة يُسقط القراءة؛ وتحريكُ موضعٍ خاطئ كذلك
    r = anchor_of("NAQL")
    cells = r[4]
    assert cells is not None and reads(r)
    assert not reads((r[0], r[1], r[2], r[3], cells[1:], 0, r[6]))
    assert not reads((r[0], r[1], r[2], r[3], cells, 1, r[6]))
    # قاعدةٌ غيرُ قاعدتها لا تقرأ صورتَها (قلبُ اللام على خَافَ)
    q = anchor_of("QALB_AYN")
    assert not reads(("QALB_LAM", q[1], q[2], q[3], q[4], q[5], q[6]))
    # صورةٌ بلا خانات لا تُقرأ ولو حُرِّك موضعُها
    h = anchor_of("HADHF_LAM")
    assert not reads((h[0], h[1], h[2], h[3], None, 0, h[6]))
