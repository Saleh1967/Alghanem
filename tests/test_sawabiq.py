"""السوابقُ الحرفيّة: توقّعاتٌ مستقلّةٌ عن الشيفرة — الحرفُ يُقرأ بعلاقته بما بعده على أبواب الكتاب
(باءُ الجرّ ولامُ الجرّ أمام المجرور، لامُ الأمر أمام المجزوم، لامُ كي أمام المنصوب، أل بهمزةٍ مفتوحة، همزةُ
الوصل مكسورةً إلّا أن يُضمّ الثالث)؛ الموصولُ يُردّ إلى أصله ويُقرأ عليه؛ التعدّدُ يُحصى؛ وطفراتٌ مرفوضة."""

from __future__ import annotations

from slge.cells import licensed
from slge.rawabit import cells_of
from slge.sawabiq import KINDS, PROCLITIC_CELLS, lift, restore, sawabiq, wasl_state
from slge.sawabiq_table import TABLE


def _kinds(word: str) -> set[tuple[str, str, bool]]:
    w = cells_of(word)
    ms = sawabiq(w)
    assert all(restore(m) == w for m in ms), word
    return {("".join(k for k, _ in m.pre), m.kind, m.joined) for m in ms}


def test_table_is_anchored_in_the_sealed_kitab_and_every_row_is_read() -> None:
    assert len(KINDS) == 7 and len(TABLE) == 11 and len(PROCLITIC_CELLS) == 9
    assert {r[0] for r in TABLE} == set(KINDS)
    lines = {r[2] for r in TABLE}
    assert lines == {18330, 8686, 8658, 17502, 17564}  # الأبوابُ الخمسة بأسطرها في الكتاب المختوم
    for kind, _, _, _, cells, pre, joined in TABLE:
        assert any(m.kind == kind and m.pre == pre and m.joined == joined for m in sawabiq(cells))
    # الموصولُ لا يُرخَّص وحدَه (يبدأ بساكن)، وأصلُه مرخَّص
    for *_, cells, pre, joined in TABLE:
        if joined:
            rest = cells[len(pre):]
            assert not licensed(rest)
            assert licensed(lift(rest)) or rest[0][0] == "ل"  # لامُ الأمر أصلُها المكسورة لا الهمزة


def test_ba_and_lam_read_by_the_relation_with_what_follows() -> None:
    assert ("ب", "BA_JARR", False) in _kinds("بِرَبِّ")
    assert ("ل", "LAM_JARR", False) in _kinds("لِرَبِّ")
    assert ("ل", "LAM_AMR", False) in _kinds("لِيُنْفِقْ")
    assert ("ل", "LAM_KAY", False) in _kinds("لِيَحْكُمَ")
    # التعدّدُ يُحصى: لِيَوْمٍ جرٌّ أو أمر (يَوْمِنْ على صورة المجزوم)؛ لِتَكُونُوا أمرٌ أو كي (حذفُ النون)
    assert {k for _, k, _ in _kinds("لِيَوْمٍ")} == {"LAM_JARR", "LAM_AMR"}
    assert {k for _, k, _ in _kinds("لِتَكُونُو")} >= {"LAM_AMR", "LAM_KAY"}
    # لامُ الأمر المسكَّنة بعد الفاء والواو تُردّ مكسورة
    f = [m for m in sawabiq(cells_of("فَلْيَنْظُرْ")) if m.kind == "LAM_AMR"]
    assert f and f[0].joined and f[0].under == cells_of("لِيَنْظُرْ")
    assert any(m.kind == "LAM_AMR" and m.joined for m in sawabiq(cells_of("وَلْيَكْتُبْ")))


def test_al_and_hamzat_wasl_initial_and_joined() -> None:
    assert _kinds("اَلْحَمْدُ") == {("", "AL", False)}
    assert ("", "AL", False) in _kinds("اَرْرَحْمَنِ")  # الشمسيّة (الرحمن كما في الشهادة)
    assert ("ب", "AL", True) in _kinds("بِلْحَقِّ") and ("ب", "BA_JARR", False) in _kinds("بِلْحَقِّ")
    assert ("و", "AL", True) in _kinds("وَرْرَحْمَنِ")
    assert _kinds("اِبْنَ") == {("", "WASL_ISM", False)}
    assert ("", "WASL_FIL", False) in _kinds("اُسْكُنْ")
    assert ("", "WASL_FIL", False) in _kinds("اِسْتَغْفِرْ")
    w = [m for m in sawabiq(cells_of("وَسْتَغْفِرْ")) if m.kind == "WASL_FIL"]
    assert w and w[0].joined and w[0].under == cells_of("اِسْتَغْفِرْ")
    b = sawabiq(cells_of("بِسْمِ"))
    assert {m.kind for m in b} == {"BA_JARR", "WASL_ISM"}
    # الهمزةُ مكسورةٌ أبدًا إلّا أن يُضمّ الثالث
    assert wasl_state(cells_of("سْكُنْ")) == "ضم" and wasl_state(cells_of("سْتَغْفِرْ")) == "كسر"
    assert lift(cells_of("سْكُنْ")) == cells_of("اُسْكُنْ")
    assert lift(cells_of("لْحَقِّ")) == cells_of("اَلْحَقِّ")


def test_mutants_are_refused() -> None:
    # لا سابقةَ: القالبُ وحدَه
    assert not sawabiq(cells_of("كَتَبَ")) and not sawabiq(cells_of("ذَهَبَ"))
    # باءٌ أمام مرفوع ليست باءَ جرّ؛ لامٌ أمام ماضٍ ليست أمرًا ولا كي
    assert "BA_JARR" not in {k for _, k, _ in _kinds("بِرَبُّ")}
    assert not {k for _, k, _ in _kinds("لِذَهَبَ")} & {"LAM_AMR", "LAM_KAY"}
    # همزةُ القطع ليست وصلًا: أُنْزِلَ (الثالث مكسور) وأَكْرَمَ
    assert not {k for _, k, _ in _kinds("اُنْزِلَ")} & {"WASL_FIL", "WASL_ISM"}
    assert not {k for _, k, _ in _kinds("أَكْرَمَ")} & {"WASL_FIL", "WASL_ISM"}
    # همزةُ أل لا تسقط بعد همزة الاستفهام: ءَلْحَمْدُ ليست (ءَ + لْحَمْدُ) موصولة
    assert ("ء", "AL", True) not in _kinds("اَلْحَمْدُ")
    # الساكنُ بعد الهمزة شرطُ الوصل: اِبَنَ ليست ابن
    assert not _kinds("اِبَنَ")
    # لامُ الأمر المسكَّنة بعد الباء مرفوضة (الباءُ ليست من الفاء والواو)
    assert not any(m.kind == "LAM_AMR" for m in sawabiq(cells_of("بِلْيَنْظُرْ")))
