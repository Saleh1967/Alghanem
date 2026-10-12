"""القراءةُ الموحَّدة (ADR ٤٢): الحرفُ يحجب الجذرَ عن الحكم ولا يحذف، والجذعُ يقرأ الأصلَ المردود.

التوقّعاتُ مكتوبةٌ باليد: فِي ومِنْ وإِلَى ولَكُمْ حروفٌ لا جذرَ لها في الحكم؛ عَلَا تُكتب في الخانات كعَلَى فهي حرفٌ
للحكم وقراءةُ الفعل (علو) باقيةٌ في الجذع؛ فَامْشُوا تُقرأ بأصلها ءِمْشُوا على م ش ي، واسْتَغْفِرُوا بعد الواو
على غ ف ر، ولا يقرأ الجذعُ صورتَيهما الموصولتين على جذرهما. والطفراتُ (حذفُ قراءات الحرف، قائمةُ
حروفٍ تشمل الظروف، ردُّ أل مكرَّرًا، تركُ الأصل المردود) تُرفض بأسمائها.
"""

from __future__ import annotations

from collections.abc import Callable

from slge.cells import Cell
from slge.gates import climb
from slge.hukm import roots_of_form
from slge.jidh import jidh
from slge.maqayis import attested, code_of_root, roots_of
from slge.qiraa import Reading, harf, hukm_readings, lifted, qiraa, restored
from slge.rawabit import cells_of
from slge.tawzi import tawzi

Word = tuple[Cell, ...]


def roots(qs: tuple[Reading, ...]) -> set[tuple[str, bool]]:
    return {("".join(x), attested(q.r)) for q in qs for x in roots_of(q.r)}


def test_particles_have_no_root_for_judgement() -> None:
    for t in ("فِي", "مِنْ", "إِلَى", "لَكُمْ", "عَلَيْهِمْ"):
        w = cells_of(t)
        assert harf(w) and hukm_readings(w) == () and roots_of_form(w) == (), t
        assert len(qiraa(w)) == len(jidh(w)), t  # حُجب ولم يُحذف (`jidh_sub_qiraa`)
    # عَلَا الفعل وعَلَى الحرف خاناتٌ واحدة: حرفٌ للحكم، وقراءةُ الفعل باقيةٌ في الجذع
    ala = cells_of("عَلَا")
    assert harf(ala) and ("علو", True) in roots(qiraa(ala)) and roots_of_form(ala) == ()
    # فَوْقَ ظرفٌ لا حرفٌ من حروف المعاني: جذرُه للحكم
    fawqa = cells_of("فَوْقَ")
    assert tawzi(fawqa) and not harf(fawqa) and roots_of_form(fawqa)


def test_restored_original_is_read() -> None:
    famshu = cells_of("فَمْشُوْ")
    assert ("مشي", True) not in roots(qiraa(famshu)[:1])  # الصورةُ الموصولة: فَمْشُ
    assert ("مشي", True) in roots(restored(famshu))
    for q in restored(famshu):
        assert q.via is not None and q.via.kind == "WASL_FIL"
        assert (*q.via.pre, *q.via.rest) == famshu  # السابقةُ تُردّ إلى الكلمة بعينها
        assert q.r.restore() == (*q.via.pre, *q.via.under)  # والجذعُ إلى الأصل المردود
    wastaghfiru = cells_of("وَسْتَغْفِرُوْ")
    assert not any(attested(r) for r in jidh(wastaghfiru))
    assert roots(restored(wastaghfiru)) == {("غفر", True)}
    assert roots_of_form(wastaghfiru) == (code_of_root(("غ", "ف", "ر")),)  # الحكمُ على الأصل
    # أل الموصولةُ لا تُردّ هنا: الجذعُ يقرؤها أصلًا
    assert not lifted(cells_of("وَلْأَرْضِ"))


def test_the_ladder_carries_both() -> None:
    from slge.entry import to_atoms
    from slge.gates import Pass

    def at(word: str, gate: str) -> Pass:
        p = next(p for p in climb(to_atoms(cells_of(word))) if p.gate == gate)
        assert isinstance(p, Pass)
        return p

    assert "حرفٌ بالموزِّع" in at("فِي", "الجذع").residual
    assert at("فِي", "الجواب").out["الوجود"] == "حرف"
    stem = at("فَمْشُوْ", "الجذع")
    assert "الأصلُ المردود: 5" in stem.residual and stem.out[0].via is not None  # المشهودُ أوّلًا


Mutant = Callable[[Word], tuple[Reading, ...]]


def _expectations(q: Mutant, hk: Mutant) -> list[str]:
    bad = []
    if len(q(cells_of("فِي"))) != len(jidh(cells_of("فِي"))):
        bad.append("HARF_READINGS_DELETED")
    if not roots(hk(cells_of("فَوْقَ"))):
        bad.append("ZARF_ROOT_HIDDEN")
    if any(x.via is not None for x in q(cells_of("وَلْأَرْضِ"))):
        bad.append("AL_RESTORED_TWICE")
    if ("مشي", True) not in roots(q(cells_of("فَمْشُوْ"))):
        bad.append("ORIGINAL_NOT_READ")
    return bad


def test_mutants_are_refused_by_name() -> None:
    from slge.sawabiq import sawabiq

    assert _expectations(qiraa, hukm_readings) == []

    def deleting(w: Word) -> tuple[Reading, ...]:
        return () if harf(w) else qiraa(w)

    def all_mabni(w: Word) -> tuple[Reading, ...]:
        return () if tawzi(w) else qiraa(w)

    def with_al(w: Word) -> tuple[Reading, ...]:
        extra = tuple(Reading(m, r) for m in sawabiq(w) if m.under != m.rest
                      for r in jidh((*m.pre, *m.under)))
        return (*(Reading(None, r) for r in jidh(w)), *extra)

    def surface_only(w: Word) -> tuple[Reading, ...]:
        return tuple(Reading(None, r) for r in jidh(w))

    assert _expectations(deleting, hukm_readings) == ["HARF_READINGS_DELETED"]
    assert _expectations(qiraa, all_mabni) == ["ZARF_ROOT_HIDDEN"]
    assert _expectations(with_al, hukm_readings) == ["AL_RESTORED_TWICE"]
    assert _expectations(surface_only, hukm_readings) == ["ORIGINAL_NOT_READ"]
